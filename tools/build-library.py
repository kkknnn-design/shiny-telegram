"""把 textbooks/outputs/教材/*.html 构建成适合手机阅读的线上教材书架 library/。

用法：python tools/build-library.py
- 输入：textbooks/outputs/教材清单.json 与各册离线 HTML（KaTeX 已预渲染，字体与图片内嵌）。
- 输出：library/index.html（书架）、library/<编号>.html（阅读页）、共用的 CSS/JS、
  拆出的 KaTeX 字体 library/fonts/ 与插图 library/img/、PWA 清单与 Service Worker。
- 页面源码在 tools/library/（library.css、reader.js、shelf.js），不要直接改 library/ 下的生成文件。
"""
import hashlib
import html
import json
import re
import shutil
import struct
import base64
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / 'textbooks' / 'outputs' / '教材'
MANIFEST = ROOT / 'textbooks' / 'outputs' / '教材清单.json'
ASSETS = ROOT / 'tools' / 'library'
OUT = ROOT / 'library'

COLORS = {
    '01': '#2f4858', '02': '#7a2e3a', '03': '#35573a', '04': '#2b3f6b', '05': '#8a5a2b',
    '06': '#4b3f72', '07': '#5c5346', '08': '#1f5f5b', '09': '#9c3d2e', '10': '#4a5a26',
    '11': '#6b4a2b', '12': '#2d5a73', '13': '#3a4150',
}
FALLBACK = ['#2f4858', '#7a2e3a', '#35573a', '#8a5a2b', '#4b3f72']

EARLY = ("<script>try{var s=JSON.parse(localStorage.getItem('lib-settings')||'{}'),r=document.documentElement;"
         "r.setAttribute('data-theme',s.theme||'auto');if(s.font)r.setAttribute('data-font',s.font);"
         "if(s.size)r.style.setProperty('--fs',s.size+'px')}catch(e){}</script>")

ICON_BACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>'
ICON_TOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/></svg>'
ICON_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>'
ICON_THEME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'


def short_hash(data: bytes, n=10) -> str:
    return hashlib.sha256(data).hexdigest()[:n]


def text_of(fragment: str) -> str:
    fragment = re.sub(r'<span class="katex-mathml">.*?</span>', '', fragment, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


def png_size(data: bytes):
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24])
    return None


class Builder:
    def __init__(self):
        self.fonts_done = False
        self.katex_css = ''
        self.files = {}  # 相对路径 -> bytes，最后统一写出

    def put(self, rel, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.files[rel] = data

    # KaTeX 字体与规则（各册相同，只取一次）
    def take_fonts(self, style: str):
        if self.fonts_done:
            return
        css_rules = re.sub(r'@font-face\{.*?\}', '', style, flags=re.S)
        self.katex_css = css_rules.split('@page')[0].strip()
        faces = []
        for face in re.findall(r'@font-face\{.*?\}', style, flags=re.S):
            fam = re.search(r'font-family:([^;}]+)', face).group(1).strip().strip('"\'')
            weight = (re.search(r'font-weight:([^;}]+)', face) or [None, '400'])[1].strip()
            fstyle = (re.search(r'font-style:([^;}]+)', face) or [None, 'normal'])[1].strip()
            m = re.search(r'url\(data:font/woff2;base64,([^)]+)\)', face)
            if not m:
                m = re.search(r'url\(data:font/(woff);base64,([^)]+)\)', face)
                ext, b64 = 'woff', m.group(2)
            else:
                ext, b64 = 'woff2', m.group(1)
            name = f'{fam}-{weight}-{fstyle}.{ext}'.replace(' ', '_')
            self.put(f'fonts/{name}', base64.b64decode(b64))
            faces.append(f'@font-face{{font-display:swap;font-family:{fam};font-style:{fstyle};font-weight:{weight};'
                         f'src:url(fonts/{name}) format("{ext}")}}')
        self.katex_css = '\n'.join(faces) + '\n' + self.katex_css
        self.fonts_done = True

    def take_images(self, body: str, code: str) -> str:
        def repl(m):
            mime, b64 = m.group(1), m.group(2)
            data = base64.b64decode(b64)
            ext = {'png': 'png', 'jpeg': 'jpg', 'jpg': 'jpg', 'webp': 'webp', 'gif': 'gif', 'svg+xml': 'svg'}[mime]
            rel = f'img/{code}-{short_hash(data)}.{ext}'
            self.put(rel, data)
            size = png_size(data)
            dims = f' width="{size[0]}" height="{size[1]}"' if size else ''
            return f'<img src="{rel}"{dims} loading="lazy" decoding="async"'
        body = re.sub(r'<img src="data:image/([a-z+]+);base64,([A-Za-z0-9+/=]+)"', repl, body)

        def repl_file(m):  # 少数插图在源 HTML 中以相对路径引用 figures/ 下的文件
            src = SRC_DIR / html.unescape(m.group(1))
            if not src.is_file():
                print('  警告：找不到插图', src)
                return m.group(0)
            data = src.read_bytes()
            rel = f'img/{code}-{short_hash(data)}{src.suffix.lower()}'
            self.put(rel, data)
            size = png_size(data)
            dims = f' width="{size[0]}" height="{size[1]}"' if size else ''
            return f'<img src="{rel}"{dims} loading="lazy" decoding="async"'
        return re.sub(r'<img src="((?!data:|img/|https?:)[^"]+)"', repl_file, body)


def transform_body(body: str):
    """去掉隐藏的 MathML、给 h3 加 id、表格加横向滚动容器，并收集目录。"""
    body = re.sub(r'<span class="katex-mathml">.*?</span>', '', body, flags=re.S)
    body = re.sub(r'<table\b[^>]*>', lambda m: '<div class="tbl">' + m.group(0), body)
    body = body.replace('</table>', '</table></div>')
    toc = []
    state = {'h2': 0, 'h3': 0}

    def repl(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        if tag == 'h2':
            if not idm:
                return m.group(0)  # 原书内目录页的“本册目录”标题
            hid = idm.group(1)
            state['h2'] += 1
            state['h3'] = 0
            toc.append(('2', hid, inner))
            return m.group(0)
        state['h3'] += 1
        hid = idm.group(1) if idm else f's{state["h2"]}-{state["h3"]}'
        toc.append(('3', hid, inner))
        if idm:
            return m.group(0)
        return f'<h3 id="{hid}"{attrs}>{inner}</h3>'

    body = re.sub(r'<(h2|h3)([^>]*)>(.*?)</\1>', repl, body, flags=re.S)
    return body, toc


def reader_page(b, body, toc, v, next_book):
    items = ''.join(
        f'<li class="l{lvl}"><a href="#{hid}">{inner}</a></li>' for lvl, hid, inner in toc)
    nxt = (f'<a href="{next_book["href"]}">下一册 · {html.escape(next_book["title"])}</a>' if next_book
           else '<a href="./">回到书架</a>')
    return f'''<!doctype html>
<html lang="zh-CN" data-book="{b["code"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(b["title"])} · 教材书架</title>
<meta name="description" content="{html.escape(b["sub"])}">
<meta name="theme-color" content="{b["color"]}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="stylesheet" href="library.css?v={v}">
{EARLY}
</head>
<body>
<header class="topbar"><div class="row">
<a class="tb" href="./" aria-label="返回书架">{ICON_BACK}<span>书架</span></a>
<div class="where"><span class="bk">{html.escape(b["title"])}</span><span class="ch" id="curCh">封面</span></div>
<button class="tb" id="tocBtn" aria-label="目录">{ICON_TOC}</button>
<button class="tb" id="setBtn" aria-label="阅读设置" style="font-family:var(--serif);font-size:17px">Aa</button>
</div><div class="progress"><i id="prog"></i></div></header>
<main id="book" class="book">
{body}
<div class="book-end">— 全书完 —<br>{nxt}</div>
</main>
<nav id="toc" class="drawer" aria-label="目录">
<header><div class="k">{b["code"]} · {b["pages"]} 页 · 版本 {html.escape(b["rev"])}</div><h2>{html.escape(b["title"])}</h2>
<div class="links"><a class="chip" href="./">书架</a><a class="chip" href="#">回到封面</a><a class="chip" href="{b["pdf"]}">PDF 版</a></div></header>
<ol>{items}</ol>
</nav>
<div id="settings" class="sheet" role="dialog" aria-label="阅读设置"><div class="grab"></div>
<div class="opt"><span>字号</span><div class="seg"><button data-k="size" data-v="-">A−</button><button disabled id="sizeVal" style="min-width:40px">17</button><button data-k="size" data-v="+">A+</button></div></div>
<div class="opt"><span>字体</span><div class="seg"><button data-k="font" data-v="serif" style="font-family:var(--serif)">宋体</button><button data-k="font" data-v="sans" style="font-family:var(--sans)">黑体</button></div></div>
<div class="opt"><span>主题</span><div class="seg"><button data-k="theme" data-v="auto">自动</button><button data-k="theme" data-v="light">浅</button><button data-k="theme" data-v="sepia">护眼</button><button data-k="theme" data-v="dark">深</button></div></div>
</div>
<div id="scrim" class="scrim"></div>
<div id="toast" class="toast" role="status"></div>
<button id="totop" class="totop" aria-label="回到顶部">{ICON_UP}</button>
<script src="reader.js?v={v}"></script>
</body>
</html>
'''


def shelf_page(books, meta, v):
    cards = []
    for b in books:
        cards.append(f'''<a class="book-card" href="{b["href"]}">
<div class="cover-art" style="background:{b["color"]}"><div class="no">No. {b["code"]}</div>
<div class="ttl">{html.escape(b["title"])}</div><div class="rule"></div><div class="sub">{html.escape(b["sub"])}</div>
<div class="bar"><i data-bar="{b["code"]}"></i></div></div>
<div class="card-meta"><span>{b["pages"]} 页 · {b["chapters"]} 章</span><span data-pct="{b["code"]}"></span></div></a>''')
    data = [{k: b[k] for k in ('code', 'title', 'sub', 'route', 'href', 'color')} | {'toc': [[hid, t] for _, hid, t in b['toc_text']]} for b in books]
    data_json = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    combined = '../textbooks/outputs/' + quote('各学科教材合集.pdf')
    total_pages = sum(b['pages'] for b in books)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>教材书架</title>
<meta name="description" content="个人学科教材的在线阅读版：{len(books)} 册，适合手机阅读。">
<meta name="theme-color" content="#8a4b2a">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="stylesheet" href="library.css?v={v}">
{EARLY}
</head>
<body>
<div class="shelf-page">
<div class="masthead"><div><h1>教材书架</h1><p>{len(books)} 册 · {total_pages} 页 · 更新于 {html.escape(meta.get("date", ""))}</p></div>
<button class="icon-btn" id="themeBtn" aria-label="主题">{ICON_THEME}</button></div>
<div class="search">{ICON_SEARCH}<input id="q" type="search" placeholder="搜索书名或章节，如：特征值" autocomplete="off" enterkeyhint="search"></div>
<a class="continue" id="continue" hidden href="#"><div class="mini"></div><div class="info"><div class="t">继续阅读</div><div class="b"></div><div class="c"></div></div><div class="go">打开 ›</div></a>
<ul class="results" id="results" hidden></ul>
<section id="shelf"><h2 class="section-title">全部教材</h2><div class="grid">
{"".join(cards)}
</div></section>
<footer class="foot">阅读位置、字号与主题保存在本机浏览器。读过的册会缓存，断网也能打开。<br>
<a href="{combined}">下载全部教材合集 PDF</a></footer>
</div>
<script id="books-data" type="application/json">{data_json}</script>
<script src="shelf.js?v={v}"></script>
</body>
</html>
'''


def make_icons(builder):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#8a4b2a"/>'
           '<rect x="118" y="136" width="70" height="250" rx="10" fill="#f3e3c4"/>'
           '<rect x="206" y="112" width="70" height="274" rx="10" fill="#e8c88f"/>'
           '<rect x="292" y="150" width="70" height="236" rx="10" fill="#f3e3c4" transform="rotate(-12 327 386)"/>'
           '<rect x="96" y="386" width="320" height="18" rx="9" fill="#f3e3c4"/></svg>')
    builder.put('icon.svg', svg)
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print('未安装 Pillow，跳过 PNG 图标')
        return False
    import io
    big = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.rounded_rectangle((0, 0, 1023, 1023), radius=224, fill='#8a4b2a')
    d.rounded_rectangle((236, 272, 376, 772), radius=20, fill='#f3e3c4')
    d.rounded_rectangle((412, 224, 552, 772), radius=20, fill='#e8c88f')
    lean = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    ImageDraw.Draw(lean).rounded_rectangle((584, 300, 724, 772), radius=20, fill='#f3e3c4')
    big.alpha_composite(lean.rotate(12, center=(654, 772), resample=Image.BICUBIC))
    d.rounded_rectangle((192, 772, 832, 808), radius=18, fill='#f3e3c4')
    for size in (180, 192, 512):
        im = big.resize((size, size), Image.LANCZOS)
        if size == 180:  # iOS 图标不要透明圆角
            bg = Image.new('RGB', (size, size), '#8a4b2a'); bg.paste(im, mask=im); im = bg
        buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
        builder.put(f'icon-{size}.png', buf.getvalue())
    return True


def main():
    meta = json.loads(MANIFEST.read_text(encoding='utf-8'))
    builder = Builder()
    books = []
    for i, entry in enumerate(meta['books']):
        src = SRC_DIR / entry['html']
        if not src.exists():
            print('跳过（缺少 HTML）：', entry['html'])
            continue
        raw = src.read_text(encoding='utf-8')
        style = re.search(r'<style>(.*?)</style>', raw, flags=re.S).group(1)
        builder.take_fonts(style)
        body = raw[raw.index('<body>') + len('<body>'):]
        body = re.sub(r'</body>\s*</html>\s*$', '', body).strip()
        sub = re.search(r'<div class="subtitle">(.*?)</div>', body, flags=re.S)
        sub_text = text_of(sub.group(1)) if sub else ''
        if not sub_text or sub_text.startswith('#'):
            # 部分分册封面副标题误写成了 Markdown 标题“# 书名”，改用学习路线
            sub_text = entry.get('route', '')
            if sub:
                body = body.replace(sub.group(0), f'<div class="subtitle">{html.escape(sub_text)}</div>', 1)
        body = builder.take_images(body, entry['code'])
        body, toc = transform_body(body)
        code = entry['code']
        books.append({
            'code': code, 'title': entry['title'], 'route': entry.get('route', ''),
            'sub': sub_text,
            'pages': entry.get('pages', 0), 'rev': entry.get('source_revision', ''),
            'href': f'{code}.html', 'color': COLORS.get(code, FALLBACK[i % len(FALLBACK)]),
            'pdf': '../textbooks/outputs/' + quote('教材/' + entry['file']),
            'body': body, 'toc': toc, 'chapters': sum(1 for t in toc if t[0] == '2'),
            'toc_text': [(lvl, hid, text_of(inner)) for lvl, hid, inner in toc],
        })

    css = (ASSETS / 'library.css').read_text(encoding='utf-8') + '\n/* KaTeX（取自教材离线 HTML） */\n' + builder.katex_css + '\n'
    builder.put('library.css', css)
    builder.put('reader.js', (ASSETS / 'reader.js').read_bytes())
    builder.put('shelf.js', (ASSETS / 'shelf.js').read_bytes())
    has_png = make_icons(builder)

    v = short_hash(b''.join(builder.files[k] for k in sorted(builder.files)) +
                   ''.join(b['body'] for b in books).encode('utf-8'), 8)
    for idx, b in enumerate(books):
        nxt = books[idx + 1] if idx + 1 < len(books) else None
        builder.put(b['href'], reader_page(b, b['body'], b['toc'], v, nxt))
    builder.put('index.html', shelf_page(books, meta, v))

    icons = [{'src': 'icon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]
    if has_png:
        icons += [{'src': f'icon-{s}.png', 'sizes': f'{s}x{s}', 'type': 'image/png'} for s in (192, 512)]
    builder.put('manifest.webmanifest', json.dumps({
        'name': '教材书架', 'short_name': '教材', 'lang': 'zh-CN', 'start_url': './', 'scope': './',
        'display': 'standalone', 'background_color': '#f7f4ee', 'theme_color': '#8a4b2a', 'icons': icons,
    }, ensure_ascii=False, indent=1))

    core = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', f'library.css?v={v}',
            f'reader.js?v={v}', f'shelf.js?v={v}'] + sorted(k for k in builder.files if k.startswith('fonts/'))
    sw = f'''// 由 tools/build-library.py 生成。书架与公共资源预缓存；阅读过的册在打开时缓存，便于离线阅读。
const CACHE = 'textbook-library-{v}';
const CORE = {json.dumps(core)};
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('textbook-library-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  const scope = new URL('./', self.registration.scope).pathname;
  if (!url.pathname.startsWith(scope)) return;
  const put = res => {{ if (res.ok) {{ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }} return res; }};
  if (req.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname === scope) {{
    e.respondWith(fetch(req).then(put).catch(() => caches.match(req, {{ ignoreSearch: true }}).then(r => r || caches.match('index.html'))));
  }} else {{
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(put)));
  }}
}});
'''
    builder.put('sw.js', sw)

    if OUT.exists():
        shutil.rmtree(OUT)
    for rel, data in builder.files.items():
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    total = sum(len(d) for d in builder.files.values())
    print(f'已生成 {len(books)} 册 → {OUT}（{len(builder.files)} 个文件，{total / 1e6:.1f} MB，版本 {v}）')
    for b in books:
        print(f'  {b["href"]:8} {len(builder.files[b["href"]]) / 1e6:5.2f} MB  {b["title"]}')


if __name__ == '__main__':
    main()
