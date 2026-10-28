"""Locate the bright 'Galaxy A13' watermark in the bottom-left of each phone photo."""
from PIL import Image
import os

SRC = r"C:\Users\mrsai\Desktop\Media ITCS TRAINING MBPG 20 21 OCTOBER\linkedin"
FILES = [
    "WhatsApp Image 2026-10-21 at 3.31.22 PM.jpeg",
    "WhatsApp Image 2026-10-21 at 3.31.22 PM (1).jpeg",
    "WhatsApp Image 2026-10-21 at 3.31.18 PM (1).jpeg",
]

for f in FILES:
    im = Image.open(os.path.join(SRC, f)).convert("L")
    W, H = im.size
    # scan the bottom-left block for near-white pixels
    box = (0, int(H * 0.86), int(W * 0.45), H)
    crop = im.crop(box)
    px = crop.load()
    cw, ch = crop.size
    maxy = 0
    count = 0
    for y in range(ch):
        row = 0
        for x in range(cw):
            if px[x, y] > 215:
                row += 1
        if row >= 6:
            maxy = max(maxy, y)
            count += row
    print("%-46s H=%d  watermark bottom at y=%d (%.1f%% of height), bright px=%d"
          % (f[:46], H, box[1] + maxy, 100.0 * (box[1] + maxy) / H, count))
