// 复习资料构建：textbooks/outputs/复习资料/清单.json 中每份 Markdown → 离线 HTML（KaTeX 预渲染）+ PDF（Edge 无头打印）。
// 用法：node tools/build-review.mjs        （在仓库根目录运行；之后运行 python tools/build-library.py 更新线上书架）
// Markdown 约定与教材相同：行内公式 \( … \)，独立公式 \[ … \]；## 为节标题（进入书架目录），### 为小节。
// 依赖 textbooks/work/math 中的 katex 与 marked（缺失时在该目录运行 npm ci）。
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {pathToFileURL, fileURLToPath} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'textbooks/outputs/复习资料');
const mathDir = path.join(ROOT, 'textbooks/work/math');
const req = createRequire(path.join(mathDir, 'package.json'));
const katex = req('katex');
const {marked} = await import(pathToFileURL(path.join(mathDir, 'node_modules/marked/lib/marked.esm.js')));
const dist = path.dirname(req.resolve('katex/package.json'));
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';

const katexCSS = fs.readFileSync(path.join(dist, 'dist/katex.min.css'), 'utf8')
  .replace(/url\(([^)]+)\)\s*format\("(woff|truetype)"\)/g, 'url()')
  .replace(/url\((fonts\/[^)]+\.woff2)\)/g, (m, p) => `url(data:font/woff2;base64,${fs.readFileSync(path.join(dist, 'dist', p)).toString('base64')})`);

const PAGE_CSS = `
@page{size:A4;margin:16mm 16mm 18mm}
body{font-family:'Times New Roman',SimSun,serif;font-size:11pt;line-height:1.75;color:#1b1f24;max-width:820px;margin:auto}
h1{font-size:20pt;text-align:center;margin:4mm 0 2mm;color:#173a5e}
h1+p{text-align:center;color:#4b5563;margin-bottom:6mm}
h2{font-size:15pt;color:#173a5e;border-bottom:1px solid #b9c4cc;padding-bottom:1.5mm;margin:8mm 0 3mm;break-after:avoid}
h3{font-size:12.5pt;color:#173a5e;margin:6mm 0 2mm;break-after:avoid;background:#eef3f8;padding:1.5mm 3mm;border-left:3px solid #3b6ea8}
p{text-align:justify;margin:2mm 0}
blockquote{margin:3mm 0;padding:2mm 4mm;background:#f4f6f7;border-left:3px solid #8d9ca8}
table{border-collapse:collapse;width:100%;margin:3mm 0;font-size:10pt;break-inside:avoid}
th,td{border:.5pt solid #b9c4cc;padding:1.5mm 2mm;text-align:left}th{background:#edf1f4}
.math-block{margin:2.5mm 0;break-inside:avoid;text-align:center}.katex{font-size:1.06em}
ol,ul{margin:2mm 0;padding-left:7mm}li{margin:1mm 0}strong{color:#0f2f4f}`;

function render(md, title) {
  const tokens = [], errors = [];
  const tex = (t, display) => {
    try { return katex.renderToString(t.trim(), {displayMode: display, throwOnError: true, strict: 'ignore', output: 'html'}); }
    catch (e) { errors.push(t + ' :: ' + e.message); return '<b style="color:red">公式错误</b>'; }
  };
  let s = md.replace(/\\\[([\s\S]*?)\\\]/g, (_, a) => { tokens.push(`<div class="math-block">${tex(a, true)}</div>`); return `\n\nMTK${tokens.length - 1}E\n\n`; });
  s = s.replace(/\\\(([\s\S]*?)\\\)/g, (_, a) => { tokens.push(tex(a, false)); return `MTK${tokens.length - 1}E`; });
  let body = marked.parse(s, {gfm: true});
  body = body.replace(/<p>MTK(\d+)E<\/p>/g, (_, i) => tokens[+i]).replace(/MTK(\d+)E/g, (_, i) => tokens[+i]);
  let n = 0;
  body = body.replace(/<h2>/g, () => `<h2 id="section-${n++}">`);  // 书架阅读页按 section-N 生成目录
  const esc = x => x.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  return {errors, html: `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>${esc(title)}</title><style>${katexCSS}\n${PAGE_CSS}</style><body>${body}</body></html>`};
}

const list = JSON.parse(fs.readFileSync(path.join(DIR, '清单.json'), 'utf8'));
let failed = 0;
for (const item of list.items) {
  const md = fs.readFileSync(path.join(DIR, item.source), 'utf8');
  const {html, errors} = render(md, item.title);
  const htmlPath = path.join(DIR, item.html);
  fs.writeFileSync(htmlPath, html);
  errors.forEach(e => console.error('  公式错误：', e)); failed += errors.length;
  if (fs.existsSync(EDGE)) {
    execFileSync(EDGE, ['--headless=new', '--disable-gpu', '--no-pdf-header-footer', `--print-to-pdf=${path.join(DIR, item.file)}`, pathToFileURL(htmlPath).href], {stdio: 'ignore'});
  } else {
    console.warn('  未找到 Edge，跳过 PDF：', item.file);
  }
  console.log(`${item.code} ${item.title}：HTML 与 PDF 已生成${errors.length ? `（${errors.length} 处公式错误）` : ''}`);
}
process.exitCode = failed ? 1 : 0;
