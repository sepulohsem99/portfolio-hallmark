"""Prepare ITCS field photos: remove the phone watermark, resize, export webp."""
from PIL import Image, ImageOps
import os

SRC = r"C:\Users\mrsai\Desktop\Media ITCS TRAINING MBPG 20 21 OCTOBER\linkedin"
OUT = r"C:\Users\mrsai\Desktop\saifullahisonline-local\assets"
os.makedirs(OUT, exist_ok=True)

# name, file, crop_bottom_fraction, crop_top_fraction
PLAN = [
    ("field_training",  "Latihan Aplikasi Mobile ITCS.jpg",             0.00, 0.00),
    ("field_room",      "WhatsApp Image 2026-10-22 at 4.12.26 PM.jpeg", 0.00, 0.00),
    ("field_devices",   "WhatsApp Image 2026-10-22 at 4.12.35 PM.jpeg", 0.00, 0.00),
    # these three carry the phone's "Galaxy A13" watermark at ~92% height
    ("field_depot",     "WhatsApp Image 2026-10-21 at 3.31.22 PM.jpeg",     0.145, 0.00),
    ("field_handover",  "WhatsApp Image 2026-10-21 at 3.31.22 PM (1).jpeg", 0.145, 0.00),
    ("field_briefing",  "WhatsApp Image 2026-10-21 at 3.31.18 PM (1).jpeg", 0.145, 0.00),
    ("field_deck",      "Pembentangan iSystem di Bilik Mesyuarat.png",  0.00, 0.00),
]

MAXW = 1600
for name, f, cb, ct in PLAN:
    p = os.path.join(SRC, f)
    if not os.path.exists(p):
        print("MISSING", f)
        continue
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    W, H = im.size
    top = int(H * ct)
    bot = int(H * (1 - cb))
    im = im.crop((0, top, W, bot))
    if im.width > MAXW:
        im = im.resize((MAXW, int(im.height * MAXW / im.width)), Image.LANCZOS)
    dst = os.path.join(OUT, name + ".webp")
    im.save(dst, "WEBP", quality=82, method=6)
    print("%-16s %4dx%-4d %5.0f KB" % (name, im.width, im.height, os.path.getsize(dst) / 1024))
