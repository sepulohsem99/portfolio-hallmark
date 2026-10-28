"""Crop both hero images to the same 4:3 ratio so the pair balances."""
from PIL import Image, ImageOps
import os

SRC = r"C:\Users\mrsai\Desktop\Media ITCS TRAINING MBPG 20 21 OCTOBER\linkedin"
OUT = r"C:\Users\mrsai\Desktop\saifullahisonline-local\assets"
TARGET = 4 / 3.0

def to_ratio(im, target=TARGET, anchor=0.5):
    W, H = im.size
    cur = W / float(H)
    if cur > target:                      # too wide -> trim sides
        nw = int(H * target)
        x = int((W - nw) * 0.5)
        return im.crop((x, 0, x + nw, H))
    else:                                 # too tall -> trim top/bottom
        nh = int(W / target)
        y = int((H - nh) * anchor)
        return im.crop((0, y, W, y + nh))

# training: already pre-cropped 960x781, anchor low so the slide + presenter stay
t = Image.open(os.path.join(OUT, "field_training.webp")).convert("RGB")
t = to_ratio(t, anchor=0.15)
t.save(os.path.join(OUT, "field_training.webp"), "WEBP", quality=86, method=6)
print("training ", t.size)

# devices: full 960x1280, anchor to the phone grid (roughly 0.30 down)
d = ImageOps.exif_transpose(Image.open(os.path.join(SRC, "WhatsApp Image 2026-10-22 at 4.12.35 PM.jpeg"))).convert("RGB")
d = to_ratio(d, anchor=0.28)
if d.width > 1600:
    d = d.resize((1600, int(d.height * 1600 / d.width)), Image.LANCZOS)
d.save(os.path.join(OUT, "field_devices.webp"), "WEBP", quality=84, method=6)
print("devices  ", d.size)

# room: same 4:3, anchor mid
r = ImageOps.exif_transpose(Image.open(os.path.join(SRC, "WhatsApp Image 2026-10-22 at 4.12.26 PM.jpeg"))).convert("RGB")
r = to_ratio(r, anchor=0.45)
r.save(os.path.join(OUT, "field_room.webp"), "WEBP", quality=84, method=6)
print("room     ", r.size)

for f in ("field_training", "field_devices", "field_room"):
    p = os.path.join(OUT, f + ".webp")
    print("%-16s %.0f KB" % (f, os.path.getsize(p) / 1024))
