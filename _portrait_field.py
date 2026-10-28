"""Regenerate the portrait pair at 3:4 so the six handsets stay whole."""
from PIL import Image, ImageOps
import os

SRC = r"C:\Users\mrsai\Desktop\Media ITCS TRAINING MBPG 20 21 OCTOBER\linkedin"
OUT = r"C:\Users\mrsai\Desktop\saifullahisonline-local\assets"
TARGET = 3 / 4.0

def to_ratio(im, target=TARGET, anchor=0.5, xanchor=0.5):
    W, H = im.size
    cur = W / float(H)
    if cur > target:
        nw = int(H * target)
        x = int((W - nw) * xanchor)
        return im.crop((x, 0, x + nw, H))
    nh = int(W / target)
    y = int((H - nh) * anchor)
    return im.crop((0, y, W, y + nh))

jobs = [
    ("field_devices", "WhatsApp Image 2026-10-22 at 4.12.35 PM.jpeg", 0.50, 0.50),
    ("field_room",    "WhatsApp Image 2026-10-22 at 4.12.26 PM.jpeg", 0.42, 0.50),
]

for name, f, ay, ax in jobs:
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f))).convert("RGB")
    im = to_ratio(im, anchor=ay, xanchor=ax)
    if im.width > 1400:
        im = im.resize((1400, int(im.height * 1400 / im.width)), Image.LANCZOS)
    p = os.path.join(OUT, name + ".webp")
    im.save(p, "WEBP", quality=84, method=6)
    print("%-16s %4dx%-4d %5.0f KB" % (name, im.width, im.height, os.path.getsize(p) / 1024))
