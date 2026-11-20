"""把若干插图拼成一张缩略图，便于目视检查。用法：py work/contact.py 前缀 输出.png"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw
src = Path(__file__).resolve().parents[1] / 'outputs/教材/figures'
files = sorted(f for p in sys.argv[1].split(',') for f in src.glob(p + '*.png'))
W = 900
ims = []
for f in files:
    im = Image.open(f).convert('RGB'); s = W / im.width
    ims.append((f.name, im.resize((W, int(im.height * s)))))
cols = 2
rows = math.ceil(len(ims) / cols)
hs = [max(im.height for _, im in ims[r*cols:(r+1)*cols]) + 30 for r in range(rows)]
sheet = Image.new('RGB', (cols * (W + 20), sum(hs)), 'white')
d = ImageDraw.Draw(sheet); y = 0
for r in range(rows):
    for c, (n, im) in enumerate(ims[r*cols:(r+1)*cols]):
        sheet.paste(im, (c * (W + 20), y + 26)); d.text((c * (W + 20) + 4, y + 6), n, fill='red')
    y += hs[r]
sheet.save(sys.argv[2]); print(sheet.size, len(ims))
