"""把 outputs/教材/figures/ 中的插图转为 256 色调色板 PNG（分辨率不变），减小 PDF、HTML 与下载包体积。
可重复运行：已是调色板模式的文件跳过。"""
from pathlib import Path
from PIL import Image
D = Path(__file__).resolve().parents[1] / 'outputs/教材/figures'
before = after = 0
for p in sorted(D.glob('*.png')):
    im = Image.open(p); size = p.stat().st_size; before += size
    if im.mode == 'P':
        after += size; continue
    q = im.convert('RGB').quantize(256, method=Image.Quantize.FASTOCTREE)
    tmp = p.with_suffix('.tmp.png'); q.save(tmp, optimize=True, dpi=im.info.get('dpi', (300, 300)))
    if tmp.stat().st_size < size:
        tmp.replace(p)
    else:
        tmp.unlink()
    after += p.stat().st_size
print(f'插图 {before / 1e6:.1f} MB → {after / 1e6:.1f} MB')
