# 只生成合集 PDF 与分册下载包，不重算会话检查点（package_books.py 依赖原 Codex 工程的历史库，本目录无法完整运行）。
# 封面与分科目录的样式沿用 package_books.py。2026-10-20 起用于 12 科版本。
import json, hashlib, zipfile, datetime
from pathlib import Path
import fitz  # PyMuPDF；本机未安装 pypdf
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / 'outputs'; B = OUT / '教材'
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))); STAMP = NOW.date().isoformat()
manifest_path = OUT / '教材清单.json'; manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
routes = {b['code']: b.get('route', '') for b in manifest.get('books', [])}
excluded = {b['code'] for b in manifest.get('removed_books', [])}

books = []
for p in sorted(B.glob('[0-9][0-9]_*.pdf')):
    code = p.name[:2]
    if code in excluded:
        continue
    md = p.with_suffix('.md'); assert md.exists(), md
    title = next(l[2:].strip() for l in md.read_text(encoding='utf-8').splitlines() if l.startswith('# '))
    books.append({'code': code, 'title': title, 'route': routes.get(code, ''), 'file': p.name, 'source': md.name,
                  'html': p.with_suffix('.html').name, 'pages': fitz.open(p).page_count,
                  'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
total = sum(b['pages'] for b in books)

pdfmetrics.registerFont(TTFont('Song', 'C:/Windows/Fonts/simsun.ttc', subfontIndex=0))
st = ParagraphStyle('body', fontName='Song', fontSize=11, leading=19, wordWrap='CJK', alignment=1, spaceAfter=9)
small = ParagraphStyle('small', fontName='Song', fontSize=9, leading=15, wordWrap='CJK')
h = ParagraphStyle('title', fontName='Song', fontSize=27, leading=40, alignment=1, textColor=colors.HexColor('#172a3c'), spaceAfter=20)
rows = [[Paragraph('学科', st), Paragraph('合集页码', st), Paragraph('学习顺序', st)]]
pos = 3
for b in books:
    b['combined_start'] = pos; b['combined_end'] = pos + b['pages'] - 1
    rows.append([Paragraph(b['title'], small), Paragraph(f"{pos}-{b['combined_end']}", small), Paragraph(b['route'], small)]); pos += b['pages']
toc = Table(rows, colWidths=[110, 60, 315], repeatRows=1)
toc.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .35, colors.HexColor('#bcc8d0')), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#edf1f4')),
                         ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
cover = ROOT / 'work/combined_front.pdf'
story = [Spacer(1, 45 * mm), Paragraph('各学科个人教材', h), Paragraph('概念、推导与讲解型例题 · 修订版', st), Spacer(1, 12 * mm),
         Paragraph(f'{len(books)} 个学科 · 分册共 {total} 页 · {STAMP}', st), Paragraph('中文正文宋体 · 章标题与独立公式居中', st), Spacer(1, 15 * mm),
         Paragraph('程序设计 · 数学 · 物理 · 逻辑与数字技术<br/>俄语 · 控制 · 经济学 · 计算机科学', st),
         Paragraph('按各学科的概念联系与先修关系编排，结合现有课程与 first CC 教材的相关讲解。', st),
         Paragraph('每日北京时间 22:00 检查新对话，有实质内容时增补到相应章节。', st), PageBreak(), Paragraph('分科目录', h), toc, Spacer(1, 8 * mm),
         Paragraph('可使用 PDF 书签跳转各册及其章节。各册页脚为本册页码，上表为合集页码。来源范围与待核实部分见随包说明。', small)]
SimpleDocTemplate(str(cover), pagesize=(595.276, 841.89), leftMargin=51, rightMargin=51, topMargin=51, bottomMargin=51).build(story)
assert fitz.open(cover).page_count == 2, '封面与目录应恰为两页'
w = fitz.open(); w.insert_pdf(fitz.open(cover)); outline = []
for b in books:
    src = fitz.open(B / b['file']); start = w.page_count
    w.insert_pdf(src)
    outline.append([1, b['title'], start + 1])
    outline += [[lvl + 1, t, pg + start] for lvl, t, pg in src.get_toc(simple=True)]
w.set_toc(outline)
w.set_metadata({'title': '各学科个人教材合集 - ' + STAMP, 'author': '个人学习教材', 'subject': '宋体正文、矢量公式、按知识依赖组织'})
combined = OUT / '各学科教材合集.pdf'
w.save(combined, garbage=3, deflate=True)
assert fitz.open(combined).page_count == total + 2

manifest.update({'date': STAMP, 'book_count': len(books), 'book_pages': total, 'combined_pages': total + 2,
                 'combined_sha256': hashlib.sha256(combined.read_bytes()).hexdigest(), 'combined_built_at': NOW.isoformat(),
                 'combined_builder': 'work/combine_books.py'})
old = {b['code']: b for b in manifest.get('books', [])}
manifest['books'] = [{**old.get(b['code'], {}), **b} for b in books]
manifest.pop('note_2026_10_20', None)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
zpath = OUT / '各学科教材_分册与源文件.zip'
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
    for b in books:
        for n in (b['html'], b['source'], b['file']):
            z.write(B / n, '教材/' + n)
    for fig in sorted((B / 'figures').glob('*.png')):
        z.write(fig, '教材/figures/' + fig.name)
    for n in ('教材总目录.md', '教材总目录.html', '来源覆盖与编写说明.md', '更新日志.md', '教材清单.json', '内容增补核对记录.md', '各学科教材合集.pdf'):
        z.write(OUT / n, n)

print(json.dumps({'books': len(books), 'book_pages': total, 'combined_pages': total + 2,
                  'zip_entries': len(zipfile.ZipFile(zpath).namelist())}, ensure_ascii=False))
