/**
 * Guest recommendations API — Cloudflare Pages Function.
 * GET  /api/recs  -> { items: [...] }  newest first
 * POST /api/recs  -> { ok: true, item: {...} }
 * Storage: KV binding RECS (free tier).
 */

const MAX_NAME = 60;
const MAX_COMPANY = 80;
const MAX_TEXT = 600;
const MIN_TEXT = 20;
const LIST_LIMIT = 60;
const WRITE_WINDOW = 90; // seconds between submissions per IP

const RELATIONSHIPS = new Set([
  "managed me",
  "reported to me",
  "same team",
  "different companies",
  "client",
  "mentor",
  "studied together",
  "colleague",
]);

const CORS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store",
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: CORS });
}

function clean(v, max) {
  return String(v == null ? "" : v)
    .replace(/[\u0000-\u001F\u007F]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, max);
}

async function keyOf(ip) {
  const data = new TextEncoder().encode("recs:" + ip);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return "rl:" + [...new Uint8Array(hash)].slice(0, 12).map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function onRequestGet({ env }) {
  const list = await env.RECS.list({ prefix: "r:", limit: 1000 });
  const keys = list.keys.map((k) => k.name).sort().reverse().slice(0, LIST_LIMIT);

  const items = await Promise.all(
    keys.map(async (k) => {
      const raw = await env.RECS.get(k);
      if (!raw) return null;
      try {
        const o = JSON.parse(raw);
        return { name: o.name, relationship: o.relationship, company: o.company, text: o.text, at: o.at };
      } catch {
        return null;
      }
    })
  );

  return json({ items: items.filter(Boolean), total: list.keys.length });
}

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Could not read the form." }, 400);
  }

  // honeypot: real people never fill a hidden field
  if (body.website) return json({ ok: true, item: null });

  const name = clean(body.name, MAX_NAME);
  const company = clean(body.company, MAX_COMPANY);
  const text = clean(body.text, MAX_TEXT);
  const relationship = clean(body.relationship, 40);

  if (name.length < 2) return json({ error: "Please add your name." }, 400);
  if (!RELATIONSHIPS.has(relationship)) return json({ error: "Please choose how we worked together." }, 400);
  if (text.length < MIN_TEXT) return json({ error: "A little longer, please. At least a sentence." }, 400);

  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const rlKey = await keyOf(ip);
  if (await env.RECS.get(rlKey)) {
    return json({ error: "That went through already. Try again in a minute." }, 429);
  }

  const at = new Date().toISOString();
  const id = "r:" + String(Date.now()).padStart(16, "0") + ":" + crypto.randomUUID().slice(0, 8);
  const item = { name, relationship, company, text, at };

  await env.RECS.put(id, JSON.stringify(item));
  await env.RECS.put(rlKey, "1", { expirationTtl: WRITE_WINDOW });

  return json({ ok: true, item });
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      ...CORS,
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type",
    },
  });
}
