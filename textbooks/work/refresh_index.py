# 刷新教材总目录（Markdown 与 HTML）：沿用现有目录中的学习路线文字，
# 按当前分册 PDF 重算页数，跳过 教材清单.json 中 removed_books 列出的已移除册。
# 2026-10-28 增补；应在 combine_books.py 之后运行，以取得合集页数。
import json, re, datetime, html
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'; B = OUT / '教材'
manifest = json.loads((OUT / '教材清单.json').read_text(encoding='utf-8'))
removed = {b['code']: b['title'] for b in manifest.get('removed_books', [])}

# 从现有目录读取各册的学习路线说明
routes = {}
old = (OUT / '教材总目录.md').read_text(encoding='utf-8')
for m in re.finditer(r'^## (\d\d)\. (.+?)\n\n.*?\n\n(.+?)\n', old, re.M | re.S):
    routes[m.group(1)] = m.group(3).strip()

books = []
for pdf in sorted(B.glob('[0-9][0-9]_*.pdf')):
    code = pdf.name[:2]
    if code in removed:
        continue
    md = pdf.with_suffix('.md')
    title = next(l[2:].strip() for l in md.read_text(encoding='utf-8').splitlines() if l.startswith('# '))
    books.append((code, title, pdf.stem, fitz.open(pdf).page_count, routes.get(code, '')))

total = sum(b[3] for b in books)
combined = fitz.open(OUT / '各学科教材合集.pdf').page_count
today = datetime.date.today().isoformat()
gone = '、'.join(removed.values())

lines = ['# 各学科教材总目录', '',
         f'更新日期：{today}。共 {len(books)} 科，分册合计 {total} 页；合集含总封面与总目录，共 {combined} 页。'
         f'已按用户要求移除的册：{gone}；国情作业不纳入。', '',
         '[打开教材合集](各学科教材合集.pdf) · [下载分册与源文件包](各学科教材_分册与源文件.zip)', '']
for code, title, stem, pages, route in books:
    lines += [f'## {code}. {title}', '',
              f'[PDF 分册](教材/{stem}.pdf) · [离线阅读](教材/{stem}.html) · [可编辑源文件](教材/{stem}.md) · {pages} 页', '']
    if route:
        lines += [route, '']
(OUT / '教材总目录.md').write_text('\n'.join(lines), encoding='utf-8')

h = OUT / '教材总目录.html'
page = h.read_text(encoding='utf-8')
head = page[:page.index('<h1>')]
items = ''.join(
    f'<li><h2>{html.escape(t)}</h2><p>{html.escape(r.rstrip("。"))}</p>'
    f'<a href="教材/{s}.pdf">PDF · {p} 页</a>　<a href="教材/{s}.html">离线阅读</a>　<a href="教材/{s}.md">源文件</a></li>'
    for c, t, s, p, r in books)
body = (f'<h1>个人学科教材</h1><p>{len(books)} 个学科 · {total} 页分册 · 合集 {combined} 页 · {today}</p>'
        '<p>宋体正文，规范数学排版；按知识先修关系组织，合并重复追问。国情作业及已移除的册不纳入。</p>'
        '<p><a href="各学科教材合集.pdf">打开全部教材</a>　<a href="各学科教材_分册与源文件.zip">下载分册和源文件</a></p>'
        f'<ul>{items}</ul><p><a href="来源覆盖与编写说明.md">来源与编写范围</a>　<a href="更新日志.md">更新日志</a></p>'
        '<small>每天北京时间22:00检查增量；无新增内容时保持安静。</small></html>')
h.write_text(head + body, encoding='utf-8')
print(json.dumps({'books': len(books), 'book_pages': total, 'combined_pages': combined}, ensure_ascii=False))
