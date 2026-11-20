"""各册插图的共用工具（2026-11-20 起）。

- style()：统一字体（宋体 + STIX 数学字体）、配色与 300dpi 输出。
- save(fig, name)：输出到 outputs/教材/figures/。
- 若干示意图辅助函数：方框、箭头、内存格等。
- place(md, figs)：把插图插到正文中某段之后；figs 为 (锚点文字, 文件名, 图题) 列表，
  锚点取该段中一段独有的原文。已引用的文件不重复插入。插入后按章重编“图 章-序号”。

插图尺寸偏小（宽约 4.6–6 英寸）、字号 11pt，便于手机阅读时仍看得清。
"""
from pathlib import Path
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / 'outputs/教材'
OUT = BOOKS / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE, GREEN, RED, PURPLE, GRAY = '#3b6ea8', '#d9822b', '#3c8d5a', '#b8433a', '#7b5ea7', '#6b7280'
LIGHT = {'blue': '#dbe7f3', 'orange': '#f8e3cc', 'green': '#d9eedf', 'red': '#f3d9d6', 'purple': '#e6def0', 'gray': '#eceef1'}
INK = '#1f2933'


def style():
    font_manager.fontManager.addfont('C:/Windows/Fonts/simsun.ttc')
    plt.rcParams.update({
        'font.family': ['SimSun'], 'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
        'font.size': 11, 'axes.titlesize': 11, 'axes.labelsize': 11, 'legend.fontsize': 10,
        'xtick.labelsize': 10, 'ytick.labelsize': 10, 'savefig.dpi': 300,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#4b5563',
        'axes.linewidth': .8, 'lines.linewidth': 1.8, 'legend.frameon': False,
    })


def stix_ticks(ax):
    """坐标刻度用 STIX 数字（宋体数字的小数点有空隙）。"""
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:g}$'))


def save(fig, name, ticks=True):
    if ticks:
        for ax in fig.axes:
            if ax.axison and ax.name == 'rectilinear':
                stix_ticks(ax)
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=0.05, facecolor='white')
    plt.close(fig)
    print('  图', name)


def canvas(w=5.2, h=2.6, xlim=(0, 10), ylim=(0, 5)):
    """无坐标轴的示意图画布，数据坐标与 xlim/ylim 一致，纵横等比。"""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect('equal'); ax.axis('off')
    return fig, ax


def box(ax, x, y, w, h, text='', fc=LIGHT['blue'], ec=BLUE, fs=11, r=0.08, lw=1.1, color=INK, family=None, **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc, ec=ec, lw=lw, **kw))
    if text != '':
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, color=color, family=family)


def arrow(ax, p, q, color=INK, lw=1.2, style='-|>', ms=11, rad=0, text=None, tpos=.5, toff=(0, .18), fs=10, ls='-', **kw):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, linestyle=ls,
                        connectionstyle=f'arc3,rad={rad}', shrinkA=1, shrinkB=1, **kw)
    ax.add_patch(a)
    if text:
        mx, my = p[0] + (q[0] - p[0]) * tpos + toff[0], p[1] + (q[1] - p[1]) * tpos + toff[1]
        ax.text(mx, my, text, ha='center', va='center', fontsize=fs, color=color)


def cells(ax, x, y, values, w=.8, h=.6, fc='white', ec=GRAY, fs=10.5, labels=None, lfs=8.5, lcolor=GRAY, highlight=None, hfc=LIGHT['orange'], family=None):
    """一行连续的内存格；labels 写在格下方（如地址或下标）。"""
    for i, v in enumerate(values):
        c = hfc if highlight and i in highlight else fc
        ax.add_patch(Rectangle((x + i * w, y), w, h, fc=c, ec=ec, lw=.9))
        ax.text(x + i * w + w / 2, y + h / 2, str(v), ha='center', va='center', fontsize=fs, family=family)
        if labels:
            ax.text(x + i * w + w / 2, y - .22, str(labels[i]), ha='center', va='center', fontsize=lfs, color=lcolor)


def axes_plot(w=4.8, h=3.0):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax


def center_axes(ax):
    """坐标轴穿过原点的函数图样式。"""
    ax.spines['left'].set_position('zero'); ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)


# ---------------------------------------------------------------- 逻辑门符号（国际通用形状）
def gate(ax, kind, x, y, s=1.0, label=None, fc='white', ec=INK, lw=1.3):
    """在 (x,y) 画门，宽约 1.6s、高 1.2s；返回 (输入端坐标列表, 输出端坐标)。kind: and/or/not/nand/nor/xor/buf"""
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    h, w = 1.2 * s, 1.6 * s
    base = kind.replace('n', '', 1) if kind in ('nand', 'nor') else kind
    if base == 'and':
        verts = [(x, y - h / 2), (x + w / 2, y - h / 2)]
        th = np.linspace(-np.pi / 2, np.pi / 2, 30)
        verts += [(x + w / 2 + h / 2 * np.cos(t), y + h / 2 * np.sin(t)) for t in th]
        verts += [(x, y + h / 2), (x, y - h / 2)]
        ax.add_patch(Polygon(verts, closed=True, fc=fc, ec=ec, lw=lw))
        out = x + w / 2 + h / 2
        ins = [(x, y + h / 4), (x, y - h / 4)]
    elif base in ('or', 'xor'):
        t = np.linspace(0, 1, 30)
        back = [(x + .25 * w * np.sin(np.pi * u), y - h / 2 + h * u) for u in t]
        top = [(x + w * u, y + h / 2 - (h / 2) * u ** 2) for u in t]
        bot = [(x + w * (1 - u), y - h / 2 + (h / 2) * (1 - u) ** 2) for u in t]
        ax.add_patch(Polygon(back[::-1] + top + bot, closed=True, fc=fc, ec=ec, lw=lw))
        if base == 'xor':
            ax.plot([x - .18 * s + .25 * w * np.sin(np.pi * u) for u in t], [y - h / 2 + h * u for u in t], color=ec, lw=lw)
        out = x + w
        ins = [(x + .25 * w * np.sin(np.pi * .75) - .02, y + h / 4), (x + .25 * w * np.sin(np.pi * .25) - .02, y - h / 4)]
        ins = [(x - (.18 * s if base == 'xor' else 0), p[1]) for p in ins]
    else:  # not / buf
        ax.add_patch(Polygon([(x, y - h / 2.4), (x, y + h / 2.4), (x + w * .8, y)], closed=True, fc=fc, ec=ec, lw=lw))
        out = x + w * .8
        ins = [(x, y)]
    if kind in ('nand', 'nor', 'not'):
        r = .1 * s
        ax.add_patch(Circle((out + r, y), r, fc='white', ec=ec, lw=lw))
        out += 2 * r
    if label:
        ax.text(x + w * .42, y, label, ha='center', va='center', fontsize=9 * s)
    return ins, (out, y)


def wire(ax, *pts, color=INK, lw=1.1, dot_end=False):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round')
    if dot_end:
        ax.plot(*pts[-1], 'o', color=color, ms=3)


# ---------------------------------------------------------------- 插入与编号
CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}


def cn_num(s):
    if s.isdigit():
        return int(s)
    if s == '十':
        return 10
    if s.startswith('十'):
        return 10 + CN[s[1]]
    if s.endswith('十'):
        return CN[s[0]] * 10
    if '十' in s:
        a, b = s.split('十')
        return CN[a] * 10 + CN[b]
    return CN[s]


def chapter_of(line, prev):
    m = re.match(r'## 第(.+?)章', line)
    if m:
        return cn_num(m.group(1))
    m = re.match(r'## (\d+)\.', line)
    if m:
        return int(m.group(1))
    return prev


FIG_RE = re.compile(r'^!\[(?:图 \d+-\d+　)?(.*?)\]\((figures/[^)]+)\)\s*$')


def renumber(lines):
    ch, k, out = 0, 0, []
    for ln in lines:
        if ln.startswith('## '):
            new = chapter_of(ln, ch)
            if new != ch:
                ch, k = new, 0
        m = FIG_RE.match(ln)
        if m:
            k += 1
            ln = f'![图 {ch}-{k}　{m.group(1)}]({m.group(2)})'
        out.append(ln)
    return out


def normalize(lines):
    """插图行前后各留一个空行，使其独立成段（HTML 渲染器只识别独立段落中的图片）。"""
    out = []
    for i, ln in enumerate(lines):
        if FIG_RE.match(ln):
            if out and out[-1].strip():
                out.append('')
            out.append(ln)
            if i + 1 < len(lines) and lines[i + 1].strip():
                out.append('')
        else:
            out.append(ln)
    return out


def block_end(lines, i):
    """从第 i 行所在段落/公式块/代码块/列表/表格向后找到其结束行。"""
    n = len(lines)
    s = lines[i].strip()
    if s.startswith('\\[') and not s.rstrip().endswith('\\]'):
        while i < n and not lines[i].strip().endswith('\\]'):
            i += 1
        return block_end_after(lines, i)
    if s.startswith('```'):
        i += 1
        while i < n and not lines[i].strip().startswith('```'):
            i += 1
        return i
    j = i
    while j + 1 < n and lines[j + 1].strip() and not lines[j + 1].startswith('#') and not FIG_RE.match(lines[j + 1]):
        nxt = lines[j + 1].strip()
        if nxt.startswith('```'):
            break
        if nxt.startswith('\\[') and not nxt.endswith('\\]'):
            j += 1
            while j + 1 < n and not lines[j].strip().endswith('\\]'):
                j += 1
            continue
        j += 1
    return j


def block_end_after(lines, i):
    return i


def place(md_name, figs):
    path = BOOKS / md_name
    raw = path.read_bytes().decode('utf-8')
    eol = '\r\n' if '\r\n' in raw else '\n'
    text = raw.replace('\r\n', '\n')
    lines = text.split('\n')
    missing = []
    for anchor, fname, caption in figs:
        if f'(figures/{fname})' in text:
            continue
        if anchor.startswith('§'):  # 小节标题：插在标题后的第一段之后
            idx = [i for i, ln in enumerate(lines) if ln.startswith('#') and ln.lstrip('#').strip() == anchor[1:]] or \
                  [i for i, ln in enumerate(lines) if ln.startswith('#') and anchor[1:] in ln]
        else:
            idx = [i for i, ln in enumerate(lines) if anchor in ln]
        if len(idx) != 1:
            missing.append((anchor, len(idx)))
            continue
        i0 = idx[0]
        if anchor.startswith('§'):
            i0 += 1
            while i0 < len(lines) and not lines[i0].strip():
                i0 += 1
        end = block_end(lines, i0)
        lines[end + 1:end + 1] = ['', f'![{caption}](figures/{fname})', '']
        text = '\n'.join(lines)
    lines = renumber(normalize(lines))
    new = '\n'.join(lines)
    path.write_bytes(new.replace('\n', eol).encode('utf-8'))
    total = len(re.findall(r'^!\[', new, flags=re.M))
    print(f'{md_name}: 共 {total} 张插图')
    for a, c in missing:
        print(f'  !! 锚点{"未找到" if c == 0 else f"不唯一({c})"}：{a}')
    return missing
