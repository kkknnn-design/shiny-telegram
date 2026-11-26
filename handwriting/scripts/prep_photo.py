"""Clean a phone photo of handwriting on squared paper into a natural sample (assets/natural/pN.jpg).

   python prep_photo.py photo.jpg assets/natural/pN.jpg [x0 y0 x1 y1]

Crop box = the paper only (no desk). Steps: flatten lighting; use the max RGB channel (blue-grey grid
lines are bright there, black ink is dark in every channel); remove long straight grid lines; keep ink by
hysteresis (seeds = clearly dark ink, grown only a few px so thin/light strokes stay joined without leaking
along the grid); drop the teacher's red pen. Output: black ink on white, ink core ~235 darkness.
Thresholds were set on p1 (light top lines: ink core ~180-195, grid <= ~150 darkness).
"""
import sys
import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
box = [int(v) for v in sys.argv[3:7]] if len(sys.argv) >= 7 else [30, 60, 1420, 1990]
im = cv2.imread(src)
x0, y0, x1, y1 = box
im = im[y0:y1, x0:x1]
b, g, r = [c.astype(np.float32) for c in cv2.split(im)]
gray = np.maximum(np.maximum(b, g), r)
bg = cv2.medianBlur(cv2.morphologyEx(gray.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)), 31)
d = 255 - np.clip(gray / np.maximum(bg.astype(np.float32), 1) * 255, 0, 255)

STRONG, WEAK, FULL = 150, 95, 160
strong = (d > STRONG).astype(np.uint8)
weak = d > WEAK
# grid: long straight runs in the weak mask
lines = np.zeros_like(strong)
for k in [(45, 1), (1, 45)]:
    lines |= cv2.morphologyEx(weak.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, k))
near = cv2.dilate(strong, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
keep = weak & near & ~((lines > 0) & (d < STRONG))
# drop specks: components without any strong seed or tiny
n, lab, st, _ = cv2.connectedComponentsWithStats(keep.astype(np.uint8), 8)
has_seed = np.zeros(n, bool)
has_seed[np.unique(lab[strong > 0])] = True
ok = has_seed & (st[:, 4] >= 6)
ok[0] = False
keep = ok[lab]

red = (r - np.maximum(g, b)) > 10
keep &= ~(cv2.dilate(red.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)
out = np.clip((d - WEAK) / (FULL - WEAK), 0, 1) * 235 * keep
# grid-crossing specks left next to ink: core < 20 px (ё dots and full stops measure 30+ px on p1)
n, lab, st, _ = cv2.connectedComponentsWithStats((out > 0).astype(np.uint8), 8)
core = np.bincount(lab[out > 120], minlength=n)
small = core < 20
small[0] = False
out[small[lab]] = 0
cv2.imwrite(dst, cv2.cvtColor((255 - out).astype(np.uint8), cv2.COLOR_GRAY2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
print("written", dst, im.shape[1], "x", im.shape[0])
