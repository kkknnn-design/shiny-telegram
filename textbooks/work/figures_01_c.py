# C 语言程序设计册插图（2026-11-20）。运行：py work/figures_01_c.py
# 内存示意图中的地址均为示意值。
from figlib import *
from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch

style()
P = '01_'
MONO = ['Consolas', 'SimSun']


def mono(ax, x, y, s, **kw):
    kw.setdefault('fontsize', 10.5)
    return ax.text(x, y, s, family=MONO, **kw)


def mbox(ax, x, y, w, h, s, fc='white', ec=GRAY, fs=10.5, color=INK, r=.04):
    box(ax, x, y, w, h, '', fc, ec, r=r)
    mono(ax, x + w / 2, y + h / 2, s, ha='center', va='center', fontsize=fs, color=color)


def pointer(ax, p, q, color=RED, rad=0, lw=1.4):
    ax.plot(*p, 'o', color=color, ms=4)
    arrow(ax, p, q, color=color, lw=lw, rad=rad)


def pipeline():
    fig, ax = canvas(6.6, 1.9, (0, 20), (0, 5.2))
    steps = [('hello.c', '源文件', 'gray'), ('预处理', '#include\n宏展开', 'orange'), ('编译', '生成汇编', 'blue'), ('汇编', 'hello.obj', 'blue'), ('链接', '+ 库函数', 'green'), ('hello.exe', '可执行文件', 'purple')]
    for i, (a, b, c) in enumerate(steps):
        x = .2 + i * 3.3
        box(ax, x, 1.8, 2.7, 1.6, '', LIGHT[c], {'gray': GRAY, 'orange': ORANGE, 'blue': BLUE, 'green': GREEN, 'purple': PURPLE}[c])
        mono(ax, x + 1.35, 2.9, a, ha='center', va='center', fontsize=10.5); ax.text(x + 1.35, 2.25, b, ha='center', va='center', fontsize=8.5, color=GRAY)
        if i < 5:
            arrow(ax, (x + 2.75, 2.6), (x + 3.25, 2.6))
    ax.text(10, .8, '“生成”一步在 Visual Studio 中包含前四步；运行时再由操作系统加载可执行文件', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'build_pipeline.png', ticks=False)


def scanf_fig():
    fig, ax = canvas(6.0, 2.2, (0, 16), (0, 6))
    mono(ax, .3, 5.2, 'scanf("%d %d", &a, &b);', fontsize=12)
    chars = list(' 12  -7\\n')
    chars = [' ', '1', '2', ' ', ' ', '-', '7', '\\n']
    ax.text(.3, 3.6, '输入流', fontsize=10, va='center')
    for i, ch in enumerate(chars):
        c = LIGHT['blue'] if ch in '12' else LIGHT['orange'] if ch in '-7' else 'white'
        mbox(ax, 2.0 + i * .75, 3.2, .7, .8, ch, c, fs=11)
    mbox(ax, 10.0, 3.8, 2.0, .9, '12', LIGHT['blue'], BLUE, fs=12); mono(ax, 9.7, 4.25, 'a', ha='right', va='center', fontsize=12)
    mbox(ax, 10.0, 2.4, 2.0, .9, '-7', LIGHT['orange'], ORANGE, fs=12); mono(ax, 9.7, 2.85, 'b', ha='right', va='center', fontsize=12)
    arrow(ax, (3.5, 3.15), (9.9, 4.2), color=BLUE, rad=.15); arrow(ax, (6.5, 3.15), (9.9, 2.8), color=ORANGE, rad=.1)
    ax.text(12.4, 3.6, '&a、&b 告诉 scanf\n把结果写到哪里', fontsize=9.5, va='center')
    ax.text(5.0, 1.6, '%d 先跳过空白，再读尽可能多的数字；换行仍留在输入流中', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'scanf_stream.png', ticks=False)


def type_sizes():
    fig, ax = plt.subplots(figsize=(5.0, 2.6))
    names = ['char', 'short', 'int', 'long', 'long long', 'float', 'double', '指针 (x64)']
    sizes = [1, 2, 4, 4, 8, 4, 8, 8]; cols = [BLUE] * 5 + [ORANGE] * 2 + [PURPLE]
    ax.barh(range(len(names))[::-1], sizes, color=cols, alpha=.7)
    for i, (n, s) in enumerate(zip(names, sizes)):
        ax.text(s + .1, len(names) - 1 - i, f'{s} 字节', va='center', fontsize=9.5)
    ax.set_yticks(range(len(names))[::-1]); ax.set_yticklabels(names, family=MONO); ax.set_xlim(0, 9.5); ax.set_xlabel('sizeof（Windows x64，MSVC）'); ax.set_xticks([0, 2, 4, 6, 8]); ax.set_xticklabels([f'${v}$' for v in (0, 2, 4, 6, 8)])
    fig.tight_layout(); save(fig, P + 'type_sizes.png', ticks=False)


def expr_tree():
    fig, ax = canvas(5.4, 2.8, (0, 14), (-1.2, 6))
    mono(ax, .3, 5.2, 'x = a + b * c > d && e', fontsize=12)
    nodes = {'=': (7, 4.6), 'x': (5, 3.6), '&&': (9, 3.6), '>': (7.5, 2.6), 'e': (10.5, 2.6), '+': (6.3, 1.6), 'd': (8.7, 1.6), 'a': (5.3, .6), '*': (7.3, .6), 'b': (6.6, -.6), 'c': (8.0, -.6)}
    edges = [('=', 'x'), ('=', '&&'), ('&&', '>'), ('&&', 'e'), ('>', '+'), ('>', 'd'), ('+', 'a'), ('+', '*'), ('*', 'b'), ('*', 'c')]
    for a, b in edges:
        ax.plot(*zip(nodes[a], nodes[b]), color=GRAY, lw=1)
    for k, (x, y) in nodes.items():
        op = k in ('=', '&&', '>', '+', '*')
        ax.add_patch(Circle((x, y), .38, fc=LIGHT['orange'] if op else LIGHT['blue'], ec=ORANGE if op else BLUE)); mono(ax, x, y, k, ha='center', va='center', fontsize=10.5)
    ax.text(10.5, .6, '优先级高的运算\n在树的下层，先计算', fontsize=9.5, va='center')
    save(fig, P + 'expression_tree.png', ticks=False)


def diamond(ax, x, y, w, h, t, fs=10):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], fc=LIGHT['orange'], ec=ORANGE)); mono(ax, x, y, t, ha='center', va='center', fontsize=fs)


def if_for():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.0))
    for ax in (a, b):
        ax.set_xlim(0, 10); ax.set_ylim(0, 9.5); ax.set_aspect('equal'); ax.axis('off')
    diamond(a, 5, 7.6, 3.6, 1.6, 'x > 0 ?'); mbox(a, 1.0, 4.4, 3.0, 1.0, 'y = 1;', LIGHT['blue'], BLUE); mbox(a, 6.0, 4.4, 3.0, 1.0, 'y = -1;', LIGHT['blue'], BLUE)
    arrow(a, (3.2, 7.6), (2.5, 5.4), text='真', toff=(-.5, 0)); arrow(a, (6.8, 7.6), (7.5, 5.4), text='假', toff=(.5, 0))
    wire(a, (2.5, 4.4), (2.5, 3.2), (7.5, 3.2), (7.5, 4.4)); arrow(a, (5, 3.2), (5, 2.0)); a.text(5, 1.5, '后续语句', ha='center', fontsize=10)
    arrow(a, (5, 9.3), (5, 8.4)); a.set_title('if–else', fontsize=10.5, family=MONO)
    mbox(b, 3.0, 8.0, 4.0, .9, 'i = 0', LIGHT['gray'], GRAY); diamond(b, 5, 6.3, 3.6, 1.6, 'i < n ?')
    mbox(b, 3.0, 3.8, 4.0, .9, '循环体', LIGHT['blue'], BLUE); mbox(b, 3.0, 2.2, 4.0, .9, 'i++', LIGHT['gray'], GRAY)
    arrow(b, (5, 8.0), (5, 7.1)); arrow(b, (5, 5.5), (5, 4.7), text='真', toff=(.4, 0)); arrow(b, (5, 3.8), (5, 3.1))
    wire(b, (3.0, 2.65), (1.2, 2.65), (1.2, 6.3)); arrow(b, (1.2, 6.3), (3.2, 6.3)); arrow(b, (6.8, 6.3), (9.3, 6.3), text='假', toff=(0, .3)); b.text(9.3, 5.6, '退出', ha='center', fontsize=10)
    b.set_title('for (i = 0; i < n; i++)', fontsize=10.5, family=MONO)
    fig.tight_layout(); save(fig, P + 'if_for_flow.png', ticks=False)


def switch_fig():
    fig, ax = canvas(5.4, 2.4, (0, 14), (0, 6.2))
    diamond(ax, 2.0, 3.2, 3.4, 1.6, 'switch(k)')
    labels = ['case 1:', 'case 2:', 'case 3:', 'default:']
    for i, l in enumerate(labels):
        y = 5.4 - i * 1.4
        mbox(ax, 5.0, y - .45, 2.6, .9, l, LIGHT['blue'], BLUE, fs=10); mbox(ax, 8.2, y - .45, 2.6, .9, '语句…', 'white', GRAY, fs=10)
        arrow(ax, (3.7, 3.2), (5.0, y), color=GRAY, lw=.8); arrow(ax, (7.6, y), (8.2, y), lw=.9)
        if i == 1:
            mono(ax, 11.0, y, 'break;', va='center', fontsize=10, color=GREEN); arrow(ax, (12.2, y), (13.6, y), color=GREEN)
        elif i < 3:
            arrow(ax, (9.5, y - .45), (9.5, y - .95), color=RED)
    ax.text(10.6, 4.95, '没有 break：\n贯穿到下一个 case', fontsize=9, color=RED, va='center')
    save(fig, P + 'switch_fallthrough.png', ticks=False)


def stack_frames():
    fig, ax = canvas(5.4, 3.0, (0, 13), (0, 7.4))
    frames = [('main', ['int x = 3', 'int r'], BLUE), ('square(int n)', ['n = 3（x 的副本）', '返回地址'], ORANGE), ('printf …', ['参数', '返回地址'], GREEN)]
    for i, (name, vars_, c) in enumerate(frames):
        y = .6 + i * 2.2
        ax.add_patch(Rectangle((1.0, y), 5.8, 2.0, fc={BLUE: LIGHT['blue'], ORANGE: LIGHT['orange'], GREEN: LIGHT['green']}[c], ec=c))
        mono(ax, 1.2, y + 1.6, name, fontsize=10.5, va='center', color=c)
        for j, v in enumerate(vars_):
            mono(ax, 1.5, y + 1.0 - j * .55, v, fontsize=9.5, va='center')
    arrow(ax, (7.5, 1.0), (7.5, 6.9), color=GRAY); ax.text(7.8, 4.0, '调用时压入新帧\n返回时弹出，\n局部变量随之失效', fontsize=9.5, va='center')
    ax.text(3.9, 7.2, '栈顶', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'call_stack.png', ticks=False)


def recursion():
    fig, ax = canvas(6.0, 2.6, (0, 15), (0, 6.4))
    calls = ['fact(3)', 'fact(2)', 'fact(1)', 'fact(0)']
    rets = ['3*2 = 6', '2*1 = 2', '1*1 = 1', '1']
    for i, (c, r) in enumerate(zip(calls, rets)):
        y = 5.4 - i * 1.4
        mbox(ax, 1.0 + i * 1.2, y - .4, 2.4, .8, c, LIGHT['blue'], BLUE)
        mbox(ax, 9.0 - i * .0 + i * 1.2 * 0, y - .4, 2.6, .8, r, LIGHT['green'], GREEN)
        if i < 3:
            arrow(ax, (2.2 + i * 1.2, y - .4), (2.2 + (i + 1) * 1.2, y - 1.0), color=BLUE)
            arrow(ax, (10.3, y - 1.0), (10.3, y - .4), color=GREEN)
    ax.text(3.0, .2, '递推：逐层调用', fontsize=10, color=BLUE, ha='center'); ax.text(10.3, .2, '回归：逐层返回', fontsize=10, color=GREEN, ha='center')
    arrow(ax, (7.2, 1.0), (8.9, 1.0), color=GRAY)
    save(fig, P + 'recursion_fact.png', ticks=False)


def pointer_basic():
    fig, ax = canvas(5.6, 2.2, (0, 14), (0, 5.4))
    mono(ax, .3, 4.8, 'int x = 5;  int *p = &x;  *p = 8;', fontsize=11.5)
    mbox(ax, 1.5, 1.8, 2.6, 1.1, '0x0060FF20', LIGHT['orange'], ORANGE, fs=10); mono(ax, 2.8, 3.25, 'p', ha='center', fontsize=12, color=ORANGE); ax.text(2.8, 1.3, '地址 0x0060FF28', ha='center', fontsize=8.5, color=GRAY)
    mbox(ax, 8.5, 1.8, 2.6, 1.1, '5 → 8', LIGHT['blue'], BLUE, fs=11); mono(ax, 9.8, 3.25, 'x', ha='center', fontsize=12, color=BLUE); ax.text(9.8, 1.3, '地址 0x0060FF20', ha='center', fontsize=8.5, color=GRAY)
    pointer(ax, (4.1, 2.35), (8.45, 2.35))
    ax.text(6.3, 2.75, '*p 即 x', ha='center', fontsize=10, color=RED)
    ax.text(7.0, .4, '声明中的 * 表示“p 是指针”；表达式中的 *p 表示“p 所指的对象”', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'pointer_basic.png', ticks=False)


def swap_fig():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.6))
    for ax in (a, b):
        ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.set_aspect('equal'); ax.axis('off')
    for ax, title, ok in [(a, 'swap(int x, int y)：交换副本', False), (b, 'swap(int *x, int *y)：通过地址交换', True)]:
        ax.text(.2, 6.1, 'main', fontsize=10, color=BLUE)
        mbox(ax, .3, 4.3, 1.8, .9, '3' if not ok else '3→7', LIGHT['blue'], BLUE); mbox(ax, 2.6, 4.3, 1.8, .9, '7' if not ok else '7→3', LIGHT['blue'], BLUE)
        mono(ax, 1.2, 5.45, 'a', ha='center'); mono(ax, 3.5, 5.45, 'b', ha='center')
        ax.text(5.5, 2.9, 'swap', fontsize=10, color=ORANGE)
        if ok:
            mbox(ax, 5.5, 1.0, 1.8, .9, '&a', LIGHT['orange'], ORANGE); mbox(ax, 7.8, 1.0, 1.8, .9, '&b', LIGHT['orange'], ORANGE)
            pointer(ax, (6.4, 1.9), (1.4, 4.25), rad=-.2); pointer(ax, (8.7, 1.9), (3.7, 4.25), rad=-.2)
        else:
            mbox(ax, 5.5, 1.0, 1.8, .9, '3→7', LIGHT['orange'], ORANGE); mbox(ax, 7.8, 1.0, 1.8, .9, '7→3', LIGHT['orange'], ORANGE)
            arrow(ax, (1.2, 4.25), (6.4, 1.95), color=GRAY, ls='--', rad=.2); arrow(ax, (3.5, 4.25), (8.7, 1.95), color=GRAY, ls='--', rad=.2)
            ax.text(4.6, .2, '函数返回后副本消失，a、b 不变', fontsize=9, color=RED, ha='center')
        mono(ax, 6.4, .6 if ok else 2.15, 'x', ha='center', fontsize=10) if False else None
        ax.set_title(title, fontsize=10, family=MONO)
    fig.tight_layout(); save(fig, P + 'swap_value_pointer.png', ticks=False)


def pointer_arith():
    fig, ax = canvas(6.4, 2.2, (0, 17), (0, 5.6))
    for i in range(16):
        mbox(ax, .5 + i * 1.0, 2.2, 1.0, .8, '', 'white', '#d1d5db')
        if i % 4 == 0:
            ax.text(.5 + i * 1.0, 1.85, f'1000+{i}', fontsize=7.5, color=GRAY)
    for k in range(4):
        ax.add_patch(Rectangle((.5 + k * 4, 2.2), 4, .8, fc=LIGHT['blue'], ec=BLUE, alpha=.6)); mono(ax, 2.5 + k * 4, 2.6, f'a[{k}]', ha='center', va='center')
        arrow(ax, (.5 + k * 4, 4.2), (.5 + k * 4, 3.05), color=ORANGE); mono(ax, .5 + k * 4, 4.5, 'p' if k == 0 else f'p+{k}', ha='center', color=ORANGE, fontsize=10)
    ax.text(8.5, .8, 'int *p：p+1 前进 sizeof(int) = 4 个字节，而不是 1 个字节', ha='center', fontsize=10)
    save(fig, P + 'pointer_arithmetic.png', ticks=False)


def array_layout():
    fig, ax = canvas(6.2, 2.0, (0, 16), (0, 5.2))
    vals = [10, 20, 30, 40, 50]
    for i, v in enumerate(vals):
        mbox(ax, 2.0 + i * 2.2, 2.2, 2.2, 1.0, str(v), LIGHT['blue'], BLUE, fs=12)
        mono(ax, 3.1 + i * 2.2, 3.55, f'a[{i}]', ha='center', fontsize=10); ax.text(3.1 + i * 2.2, 1.8, f'{0x1000 + 4 * i:#x}', ha='center', fontsize=8.5, color=GRAY, family=MONO)
    mono(ax, .3, 2.7, 'int a[5]', va='center', fontsize=10.5)
    ax.text(8.0, .6, 'a[i] 等价于 *(a + i)：首地址加上 i 个元素的大小', ha='center', fontsize=10)
    save(fig, P + 'array_layout.png', ticks=False)


def array2d():
    fig, ax = canvas(6.4, 2.6, (0, 17), (0, 6.6))
    mono(ax, .2, 6.0, 'int m[3][4]', fontsize=11)
    for i in range(3):
        for j in range(4):
            mbox(ax, .5 + j * 1.3, 4.0 - i * 1.0, 1.3, 1.0, f'{i}{j}', [LIGHT['blue'], LIGHT['orange'], LIGHT['green']][i], [BLUE, ORANGE, GREEN][i], fs=10)
        mono(ax, 5.9, 4.5 - i * 1.0, f'm[{i}]', va='center', fontsize=10, color=[BLUE, ORANGE, GREEN][i])
    ax.text(3.0, 1.3, '逻辑上：3 行 4 列', ha='center', fontsize=9.5, color=GRAY)
    for k in range(12):
        i = k // 4
        mbox(ax, 7.6 + k * .75, 3.0, .75, .9, f'{i}{k % 4}', [LIGHT['blue'], LIGHT['orange'], LIGHT['green']][i], [BLUE, ORANGE, GREEN][i], fs=8.5)
    ax.text(12.1, 2.4, '内存中：按行连续存放', ha='center', fontsize=9.5, color=GRAY)
    arrow(ax, (7.6, 4.4), (7.6, 3.95), color=BLUE); mono(ax, 7.6, 4.6, 'm[0]', ha='center', fontsize=9, color=BLUE)
    arrow(ax, (10.6, 4.4), (10.6, 3.95), color=ORANGE); mono(ax, 10.6, 4.6, 'm[1]', ha='center', fontsize=9, color=ORANGE)
    ax.text(12.1, 1.2, 'm[i][j] 的地址 = 首地址 + (i×4 + j)×sizeof(int)', ha='center', fontsize=9.5)
    save(fig, P + 'array_2d.png', ticks=False)


def const_ptr():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.0))
    for ax, title, lock_p, lock_x in [(a, 'const int *p', False, True), (b, 'int *const p', True, False)]:
        ax.set_xlim(0, 10); ax.set_ylim(0, 4.5); ax.set_aspect('equal'); ax.axis('off')
        mbox(ax, .5, 1.6, 2.6, 1.0, '&x', LIGHT['orange'], ORANGE); mbox(ax, 6.2, 1.6, 2.6, 1.0, 'x', LIGHT['blue'], BLUE)
        pointer(ax, (3.1, 2.1), (6.15, 2.1))
        ax.text(1.8, 3.0, '不能改指向' if lock_p else '可改指向', ha='center', fontsize=9.5, color=RED if lock_p else GREEN)
        ax.text(7.5, 3.0, '不能经 p 修改' if lock_x else '可经 p 修改', ha='center', fontsize=9.5, color=RED if lock_x else GREEN)
        ax.set_title(title, fontsize=11, family=MONO)
    fig.text(.5, .02, 'const 修饰紧挨着它右边（或左边）的部分', ha='center', fontsize=9.5, color=GRAY)
    fig.tight_layout(); save(fig, P + 'const_pointer.png', ticks=False)


def cstring():
    fig, ax = canvas(5.8, 1.9, (0, 15), (0, 5))
    mono(ax, .2, 4.3, 'char s[8] = "hello";', fontsize=11.5)
    chars = ["'h'", "'e'", "'l'", "'l'", "'o'", "'\\0'", "'\\0'", "'\\0'"]
    for i, ch in enumerate(chars):
        mbox(ax, .5 + i * 1.6, 1.8, 1.6, 1.1, ch, LIGHT['blue'] if i < 5 else LIGHT['orange'] if i == 5 else LIGHT['gray'], BLUE if i < 5 else ORANGE if i == 5 else GRAY, fs=10)
        ax.text(1.3 + i * 1.6, 1.45, str(i), ha='center', fontsize=8.5, color=GRAY)
    ax.text(5.0, .6, 'strlen(s) = 5', ha='center', fontsize=10, color=BLUE, family=MONO); ax.text(11.0, .6, 'sizeof(s) = 8', ha='center', fontsize=10, color=GRAY, family=MONO)
    save(fig, P + 'c_string.png', ticks=False)


def string_arrays():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.4))
    for ax in (a, b):
        ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.set_aspect('equal'); ax.axis('off')
    words = ['cat', 'horse', 'ox']
    mono(a, .2, 5.1, 'char *w[3]', fontsize=10.5)
    for i, wd in enumerate(words):
        y = 3.6 - i * 1.3
        mbox(a, .3, y, 1.4, .9, '●', LIGHT['orange'], ORANGE, fs=8)
        for j, ch in enumerate(wd + '\\0' if False else list(wd) + ['\\0']):
            mbox(a, 3.6 + j * .9, y, .9, .9, ch, LIGHT['blue'], BLUE, fs=9)
        pointer(a, (1.7, y + .45), (3.55, y + .45))
    a.set_title('指针数组：各串长度不同', fontsize=10)
    mono(b, .2, 5.1, 'char w[3][6]', fontsize=10.5)
    for i, wd in enumerate(words):
        y = 3.6 - i * 1.3
        cells_ = list(wd) + ['\\0'] + [''] * (5 - len(wd))
        for j, ch in enumerate(cells_):
            mbox(b, 1.0 + j * .9, y, .9, .9, ch, LIGHT['blue'] if ch else LIGHT['gray'], BLUE if ch else GRAY, fs=9)
    b.set_title('二维字符数组：每行 6 个字节', fontsize=10)
    fig.tight_layout(); save(fig, P + 'string_arrays.png', ticks=False)


def memory_layout():
    fig, ax = canvas(4.4, 3.2, (0, 10), (0, 8))
    segs = [('代码区', '函数的机器指令', LIGHT['gray'], GRAY), ('静态区', '全局变量、static、\n字符串字面量', LIGHT['purple'], PURPLE), ('堆', 'malloc / free', LIGHT['green'], GREEN), ('', '', 'white', '#d1d5db'), ('栈', '局部变量、参数、\n返回地址', LIGHT['blue'], BLUE)]
    hs = [1.0, 1.3, 1.5, 1.6, 1.6]; y = .4
    for (n, d, fc, ec), h in zip(segs, hs):
        ax.add_patch(Rectangle((1.0, y), 3.6, h, fc=fc, ec=ec)); ax.text(2.8, y + h / 2, n, ha='center', va='center', fontsize=10.5)
        if d:
            ax.text(5.0, y + h / 2, d, va='center', fontsize=9, color=GRAY)
        y += h
    arrow(ax, (2.8, 4.25), (2.8, 4.95), color=GREEN); arrow(ax, (2.8, 6.15), (2.8, 5.45), color=BLUE)
    ax.text(.9, .1, '低地址', fontsize=8.5, color=GRAY); ax.text(.9, 7.55, '高地址', fontsize=8.5, color=GRAY)
    save(fig, P + 'memory_layout.png', ticks=False)


def realloc_fig():
    fig, ax = canvas(6.0, 2.2, (0, 16), (0, 5.8))
    mono(ax, .2, 5.2, 'q = realloc(p, 8 * sizeof(int));', fontsize=11)
    for i in range(4):
        mbox(ax, .5 + i * .9, 3.3, .9, .8, str(i + 1), LIGHT['blue'], BLUE, fs=10)
    mbox(ax, 4.1, 3.3, 1.8, .8, '已占用', LIGHT['gray'], GRAY, fs=9); mono(ax, .4, 4.3, 'p', fontsize=11, color=ORANGE)
    ax.text(.5, 2.8, '后面没有足够空闲空间', fontsize=9, color=RED)
    for i in range(8):
        mbox(ax, 7.5 + i * .9, 1.0, .9, .8, str(i + 1) if i < 4 else '?', LIGHT['green'] if i < 4 else 'white', GREEN if i < 4 else GRAY, fs=10)
    mono(ax, 7.4, 2.0, 'q', fontsize=11, color=GREEN)
    arrow(ax, (2.3, 3.25), (8.5, 1.85), color=GREEN, rad=.2, text='复制原内容', toff=(.3, .5), fs=9.5)
    ax.text(11.0, 3.6, '旧块随后被释放：\np 失效，只能用 q；\n失败时返回 NULL，旧块仍有效', fontsize=9.5, va='center')
    save(fig, P + 'realloc_move.png', ticks=False)


def dyn2d():
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.4))
    for ax in axs:
        ax.set_xlim(0, 8); ax.set_ylim(0, 6); ax.set_aspect('equal'); ax.axis('off')
    a = axs[0]; mono(a, .1, 5.4, 'int **m', fontsize=9.5)
    for i in range(3):
        mbox(a, .3, 3.8 - i * 1.3, 1.0, .8, '●', LIGHT['orange'], ORANGE, fs=8)
        for j in range(4):
            mbox(a, 2.6 + j * .9 + (i % 2) * .3, 3.8 - i * 1.3, .9, .8, '', LIGHT['blue'], BLUE)
        pointer(a, (1.3, 4.2 - i * 1.3), (2.55 + (i % 2) * .3, 4.2 - i * 1.3))
    a.set_title('一：行指针表', fontsize=10)
    b = axs[1]; mono(b, .1, 5.4, 'int *m', fontsize=9.5)
    for k in range(12):
        mbox(b, .3 + (k % 6) * 1.2, 3.4 - (k // 6) * 1.0, 1.2, .8, f'{k // 4}{k % 4}', [LIGHT['blue'], LIGHT['orange'], LIGHT['green']][k // 4], GRAY, fs=8)
    b.text(4, 1.0, 'm[i*4 + j]', ha='center', fontsize=9.5, family=MONO); b.set_title('二：一整块', fontsize=10)
    c = axs[2]; mono(c, .1, 5.4, 'int (*m)[4]', fontsize=9.5)
    for i in range(3):
        for j in range(4):
            mbox(c, 2.4 + j * 1.0, 3.8 - i * 1.0, 1.0, .9, '', [LIGHT['blue'], LIGHT['orange'], LIGHT['green']][i], GRAY)
    pointer(c, (.9, 4.25), (2.35, 4.25)); mbox(c, .2, 3.85, 1.0, .8, '●', LIGHT['orange'], ORANGE, fs=8)
    c.text(4.4, 0.6, 'm[i][j]，一次 free', ha='center', fontsize=9.5); c.set_title('三：指向数组的指针', fontsize=10)
    fig.tight_layout(); save(fig, P + 'dynamic_2d.png', ticks=False)


def selection_sort():
    fig, ax = canvas(5.2, 2.4, (0, 13), (0, 6))
    rows = [[3, 8, 2, 6], [8, 3, 2, 6], [8, 6, 2, 3], [8, 6, 3, 2]]
    swaps = [(0, 1), (1, 3), (2, 3), None]
    for r, (vals, sw) in enumerate(zip(rows, swaps)):
        y = 5.0 - r * 1.3
        ax.text(.3, y + .35, ['初始', '第 0 轮', '第 1 轮', '第 2 轮'][r], fontsize=9.5, va='center')
        for i, v in enumerate(vals):
            done = i < r
            mbox(ax, 2.6 + i * 1.3, y, 1.2, .75, str(v), LIGHT['green'] if done else 'white', GREEN if done else GRAY, fs=11)
        if r < 3:
            nxt = swaps[r]
            i, j = nxt
            ax.annotate('', xy=(3.2 + j * 1.3, y - .05), xytext=(3.2 + i * 1.3, y - .05), arrowprops=dict(arrowstyle='<->', color=RED, connectionstyle='arc3,rad=.4', lw=1))
    ax.text(8.4, 3.0, '每轮在未排序部分\n找最大值，与该部分\n第一个元素交换；\n绿色为已就位', fontsize=9.5, va='center')
    save(fig, P + 'selection_sort.png', ticks=False)


def insertion_sort():
    fig, ax = canvas(5.4, 1.9, (0, 14), (0, 4.8))
    vals = [2, 5, 7, 9, 4, 1]
    for i, v in enumerate(vals):
        mbox(ax, 1.0 + i * 1.4, 2.0, 1.2, .9, str(v), LIGHT['green'] if i < 4 else LIGHT['orange'] if i == 4 else 'white', GREEN if i < 4 else ORANGE if i == 4 else GRAY, fs=12)
    for i in (3, 2):
        arrow(ax, (1.6 + i * 1.4, 3.05), (1.6 + (i + 1) * 1.4, 3.05), color=BLUE, rad=-.4)
    arrow(ax, (6.6, 1.95), (3.0, 1.95), color=ORANGE, rad=-.3)
    ax.text(5.0, 4.4, '比 4 大的 9、7、5 依次后移一格', ha='center', fontsize=9.5, color=BLUE)
    ax.text(5.0, .4, '4 插到 2 之后；左侧始终有序', ha='center', fontsize=9.5, color=ORANGE)
    save(fig, P + 'insertion_sort.png', ticks=False)


def binary_search():
    fig, ax = canvas(6.0, 2.4, (0, 16), (0, 6.2))
    arr = [1, 3, 4, 7, 9, 11, 15, 18, 21, 25]; target = 15
    lo, hi = 0, 9; r = 0
    while lo <= hi:
        mid = (lo + hi) // 2; y = 5.0 - r * 1.4
        for i, v in enumerate(arr):
            inside = lo <= i <= hi
            mbox(ax, 1.5 + i * 1.3, y, 1.2, .8, str(v), LIGHT['orange'] if i == mid else LIGHT['blue'] if inside else 'white', ORANGE if i == mid else BLUE if inside else '#d1d5db', fs=10, color=INK if inside else '#c0c4ca')
        ax.text(.2, y + .4, f'第{r + 1}次', fontsize=9, va='center')
        if arr[mid] == target:
            ax.text(1.5 + mid * 1.3 + .6, y - .35, '找到', ha='center', fontsize=9.5, color=GREEN); break
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
        r += 1
    ax.text(8.0, .2, '查找 15：每次比较中间元素（橙色），范围减半', ha='center', fontsize=10)
    save(fig, P + 'binary_search.png', ticks=False)


def neighbors():
    fig, ax = canvas(4.6, 2.6, (0, 12), (0, 6.6))
    for i in range(5):
        for j in range(5):
            ax.add_patch(Rectangle((.5 + j, 5.5 - i), 1, 1, fc='white', ec='#d1d5db'))
    ax.add_patch(Rectangle((2.5, 3.5), 1, 1, fc=ORANGE, alpha=.6))
    k = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0:
                continue
            ax.add_patch(Rectangle((2.5 + dc, 3.5 - dr), 1, 1, fc=LIGHT['blue'], ec=BLUE))
            ax.text(3.0 + dc, 4.0 - dr, f'{dr:+d},{dc:+d}', ha='center', va='center', fontsize=7.5, family=MONO)
            k += 1
    ax.text(3.0, 4.0, '(r,c)', ha='center', va='center', fontsize=8, family=MONO)
    mono(ax, 6.5, 4.9, 'dr[8] = {-1,-1,-1, 0,0, 1,1,1}', fontsize=9); mono(ax, 6.5, 4.1, 'dc[8] = {-1, 0, 1,-1,1,-1,0,1}', fontsize=9)
    ax.text(6.5, 2.7, '第 k 个邻格为\n(r + dr[k], c + dc[k])；\n越界或障碍则跳过', fontsize=9.5, va='center')
    save(fig, P + 'grid_neighbors.png', ticks=False)


def wave():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.0))
    N = 8; rng = np.random.default_rng(7)
    wall = np.zeros((N, N), bool)
    for (r, c) in [(1, 3), (2, 3), (3, 3), (4, 3), (5, 5), (5, 6), (6, 1), (2, 6), (3, 6)]:
        wall[r, c] = True
    INF = 99; d = np.full((N, N), INF); s = (0, 0); d[s] = 0
    from collections import deque
    q = deque([s])
    while q:
        r, c = q.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if (dr or dc) and 0 <= rr < N and 0 <= cc < N and not wall[rr, cc] and d[rr, cc] == INF:
                    d[rr, cc] = d[r, c] + 1; q.append((rr, cc))
    goal = (7, 7); path = [goal]
    while path[-1] != s:
        r, c = path[-1]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < N and 0 <= cc < N and d[rr, cc] == d[r, c] - 1:
                    path.append((rr, cc)); break
            else:
                continue
            break
    for ax, show_path in ((a, False), (b, True)):
        ax.set_xlim(0, N); ax.set_ylim(0, N); ax.set_aspect('equal'); ax.axis('off')
        for r in range(N):
            for c in range(N):
                y = N - 1 - r
                if wall[r, c]:
                    ax.add_patch(Rectangle((c, y), 1, 1, fc='#4b5563'))
                else:
                    ax.add_patch(Rectangle((c, y), 1, 1, fc=plt.cm.Blues(.12 + .6 * d[r, c] / d[d < INF].max()) if not show_path else 'white', ec='#d1d5db'))
                    ax.text(c + .5, y + .5, str(d[r, c]), ha='center', va='center', fontsize=8, color='white' if (not show_path and d[r, c] > 4) else INK)
        if show_path:
            xs = [c + .5 for r, c in path]; ys = [N - 1 - r + .5 for r, c in path]
            ax.plot(xs, ys, color=RED, lw=2.2); ax.plot(xs[0], ys[0], 's', color=RED); ax.plot(xs[-1], ys[-1], 'o', color=GREEN)
    a.set_title('波从起点逐层扩展：格内为步数', fontsize=10); b.set_title('从终点每次走到步数少 1 的邻格', fontsize=10)
    fig.tight_layout(); save(fig, P + 'wave_path.png', ticks=False)


def linked_list():
    fig, ax = canvas(6.4, 2.6, (0, 17), (0, 6.6))
    mono(ax, .2, 5.4, 'head', fontsize=11, color=ORANGE); mbox(ax, .2, 4.0, 1.4, .9, '●', LIGHT['orange'], ORANGE, fs=8)
    xs = [3.0, 7.0, 11.0]
    for i, (x, v) in enumerate(zip(xs, [12, 37, 99])):
        mbox(ax, x, 4.0, 1.5, .9, str(v), LIGHT['blue'], BLUE, fs=11); mbox(ax, x + 1.5, 4.0, 1.2, .9, '●' if i < 2 else 'NULL', LIGHT['gray'], GRAY, fs=8 if i < 2 else 8.5)
        mono(ax, x + .75, 5.1, 'data', ha='center', fontsize=8.5, color=GRAY); mono(ax, x + 2.1, 5.1, 'next', ha='center', fontsize=8.5, color=GRAY)
    pointer(ax, (1.6, 4.45), (2.95, 4.45))
    for x0, x1 in zip(xs[:-1], xs[1:]):
        pointer(ax, (x0 + 2.1, 4.45), (x1 - .05, 4.45))
    ax.text(.2, 2.9, '在 37 之后插入 50：', fontsize=10)
    mbox(ax, 9.0, 1.2, 1.5, .9, '50', LIGHT['green'], GREEN, fs=11); mbox(ax, 10.5, 1.2, 1.2, .9, '●', LIGHT['gray'], GRAY, fs=8)
    pointer(ax, (11.1, 1.65), (11.6, 3.95), color=GREEN, rad=.3); pointer(ax, (9.1, 4.0), (9.5, 2.15), color=GREEN, rad=.2)
    ax.text(.2, 1.9, '① new->next = p->next;\n② p->next = new;', fontsize=9.5, family=MONO, va='top', color=GREEN)
    save(fig, P + 'linked_list.png', ticks=False)


def dlist():
    fig, ax = canvas(6.0, 1.6, (0, 16), (0, 4.0))
    xs = [1.0, 6.0, 11.0]
    for x, v in zip(xs, [5, 8, 13]):
        mbox(ax, x, 1.4, 1.0, .9, '●', LIGHT['gray'], GRAY, fs=8); mbox(ax, x + 1.0, 1.4, 1.4, .9, str(v), LIGHT['blue'], BLUE, fs=11); mbox(ax, x + 2.4, 1.4, 1.0, .9, '●', LIGHT['gray'], GRAY, fs=8)
        mono(ax, x + .5, 2.6, 'prev', ha='center', fontsize=8, color=GRAY); mono(ax, x + 2.9, 2.6, 'next', ha='center', fontsize=8, color=GRAY)
    for x0, x1 in zip(xs[:-1], xs[1:]):
        pointer(ax, (x0 + 2.9, 2.0), (x1, 2.0), color=RED); pointer(ax, (x1 + .5, 1.6), (x0 + 3.4, 1.6), color=BLUE)
    ax.text(.2, .4, '首结点 prev 与尾结点 next 为 NULL；摘下结点时两侧指针都要改', fontsize=9.5, color=GRAY)
    save(fig, P + 'doubly_linked.png', ticks=False)


def bst():
    fig, ax = canvas(4.6, 2.6, (0, 10), (0, 5.8))
    pos = {5: (5, 5), 3: (2.6, 3.6), 8: (7.4, 3.6), 7: (6.2, 2.2), 15: (8.6, 2.2), 11: (7.6, .8)}
    edges = [(5, 3), (5, 8), (8, 7), (8, 15), (15, 11)]
    for a, b in edges:
        ax.plot(*zip(pos[a], pos[b]), color=GRAY, lw=1)
    for k, p in pos.items():
        ax.add_patch(Circle(p, .5, fc=LIGHT['green'] if k == 11 else LIGHT['blue'], ec=GREEN if k == 11 else BLUE)); ax.text(*p, str(k), ha='center', va='center', fontsize=11)
    ax.text(.2, 1.4, '依次插入\n5、8、15、3、7、11\n\n11：比 5 大往右，\n比 8 大往右，\n比 15 小往左', fontsize=9, va='center')
    save(fig, P + 'bst_insert.png', ticks=False)


def dir_tree():
    fig, ax = canvas(5.8, 2.8, (0, 14), (.4, 6.6))
    nodes = {'C:\\': (.6, 6.0), 'Users': (1.6, 5.2), 'student': (2.6, 4.4), 'proj': (3.6, 3.6), 'main.c': (4.6, 2.8), 'data': (3.6, 2.0), 'in.txt': (4.6, 1.2)}
    edges = [('C:\\', 'Users'), ('Users', 'student'), ('student', 'proj'), ('student', 'data'), ('proj', 'main.c'), ('data', 'in.txt')]
    for a, b in edges:
        (x0, y0), (x1, y1) = nodes[a], nodes[b]
        ax.plot([x0 + .2, x0 + .2, x1 - .15], [y0 - .3, y1, y1], color=GRAY, lw=1)
    for k, (x, y) in nodes.items():
        folder = '.' not in k
        mono(ax, x, y, k, va='center', fontsize=10, color=BLUE if folder else INK)
    ax.add_patch(Rectangle((3.45, 3.3), 1.3, .6, fc='none', ec=ORANGE, lw=1.2))
    ax.text(7.2, 5.0, '当前目录：C:\\Users\\student\\proj', fontsize=9.5, family=MONO, color=ORANGE)
    ax.text(7.2, 4.0, '相对路径 ..\\data\\in.txt', fontsize=9.5, family=MONO, color=GREEN)
    ax.text(7.2, 3.3, '“..”回到上一级 student，\n再进入 data', fontsize=9, color=GRAY, va='top')
    save(fig, P + 'directory_tree.png', ticks=False)


def fseek_fig():
    fig, ax = canvas(6.2, 2.0, (0, 16), (0, 5))
    for i in range(12):
        mbox(ax, 1.0 + i * 1.1, 2.0, 1.1, .9, '', LIGHT['blue'], BLUE)
        ax.text(1.55 + i * 1.1, 1.6, str(i), ha='center', fontsize=8, color=GRAY)
    ax.text(14.4, 2.45, 'EOF', fontsize=9, color=GRAY, va='center', family=MONO)
    for x, lab, c in [(1.0, 'SEEK_SET', GREEN), (6.5, 'SEEK_CUR', ORANGE), (14.2, 'SEEK_END', PURPLE)]:
        arrow(ax, (x, 4.2), (x, 3.0), color=c); mono(ax, x, 4.45, lab, ha='center', fontsize=9.5, color=c)
    ax.annotate('', xy=(8.7, 1.2), xytext=(6.5, 1.2), arrowprops=dict(arrowstyle='->', color=ORANGE)); mono(ax, 7.6, .6, 'fseek(f, 2, SEEK_CUR)', ha='center', fontsize=9, color=ORANGE)
    ax.text(12.0, .6, 'ftell 返回当前位置（字节）', fontsize=9, ha='center', color=GRAY)
    save(fig, P + 'fseek.png', ticks=False)


def argv_fig():
    fig, ax = canvas(5.8, 2.4, (0, 15), (0, 6.2))
    mono(ax, .2, 5.6, '> copy.exe in.txt out.txt', fontsize=11)
    mono(ax, .2, 4.6, 'argc = 3', fontsize=10.5, color=ORANGE)
    words = ['copy.exe', 'in.txt', 'out.txt']
    for i in range(4):
        y = 3.5 - i * .9
        mbox(ax, 1.2, y, 1.4, .8, '●' if i < 3 else 'NULL', LIGHT['orange'], ORANGE, fs=8 if i < 3 else 8.5); mono(ax, .2, y + .4, f'argv[{i}]', va='center', fontsize=8.5)
        if i < 3:
            w = words[i] + '\\0'
            mbox(ax, 4.0, y, .45 * len(words[i]) + 1.0, .8, words[i] + '\\0', LIGHT['blue'], BLUE, fs=9.5)
            pointer(ax, (2.6, y + .4), (3.95, y + .4))
    ax.text(11.0, 2.4, 'int main(int argc,\n         char *argv[])', fontsize=9.5, family=MONO, va='center')
    save(fig, P + 'argv.png', ticks=False)


for f in [pipeline, scanf_fig, type_sizes, expr_tree, if_for, switch_fig, stack_frames, recursion, pointer_basic, swap_fig, pointer_arith, array_layout, array2d, const_ptr, cstring, string_arrays, memory_layout, realloc_fig, dyn2d, selection_sort, insertion_sort, binary_search, neighbors, wave, linked_list, dlist, bst, dir_tree, fseek_fig, argv_fig]:
    f()

place('01_C语言程序设计.md', [
    ('§程序结构与标准输入', P + 'build_pipeline.png', '从源文件到可执行文件'),
    ('**scanf：地址和格式', P + 'scanf_stream.png', 'scanf 从输入流中取数并写入变量'),
    ('§基本类型的大小与取', P + 'type_sizes.png', '常见类型在 Windows x64（MSVC）下的大小'),
    ('§运算符的优先级、结', P + 'expression_tree.png', '按优先级和结合性得到的表达式树'),
    ('§循环迭代', P + 'if_for_flow.png', 'if–else 与 for 循环的流程'),
    ('§多路选择', P + 'switch_fallthrough.png', 'switch 的跳转与贯穿'),
    ('§作用域、存储期与调用栈', P + 'call_stack.png', '函数调用时的栈帧'),
    ('§递归计算', P + 'recursion_fact.png', '递归的递推与回归：fact(3)'),
    ('**同一个 `*` 的两种', P + 'pointer_basic.png', '指针保存另一个对象的地址（地址为示意值）'),
    ('**指针参数**', P + 'swap_value_pointer.png', '值传递与指针传递的交换函数'),
    ('§指针的算术运算', P + 'pointer_arithmetic.png', '指针加一按所指类型的大小前进'),
    ('**数组元素连续存放**', P + 'array_layout.png', '一维数组的连续存储'),
    ('§多维数组与行指针', P + 'array_2d.png', '二维数组按行连续存放'),
    ('**先分开两个问题**', P + 'const_pointer.png', 'const 位置不同，限制对象不同'),
    ('§字符编码与零结尾表示', P + 'c_string.png', '字符串以零字符结尾'),
    ('§字符串指针数组与双', P + 'string_arrays.png', '字符串指针数组与二维字符数组'),
    ('§堆与 malloc', P + 'memory_layout.png', '程序运行时的内存分区（示意）'),
    ('§realloc 与', P + 'realloc_move.png', 'realloc 可能搬到新位置'),
    ('§动态二维数组的三种', P + 'dynamic_2d.png', '动态二维数组的三种组织方式'),
    ('**小例子。** 3、8、', P + 'selection_sort.png', '选择排序（降序）的每一轮'),
    ('**插入排序**像整理手中', P + 'insertion_sort.png', '插入排序的一步'),
    ('§二分查找', P + 'binary_search.png', '二分查找的范围逐次减半'),
    ('从一格可以走到相邻的 8 格', P + 'grid_neighbors.png', '八邻域与偏移表'),
    ('§由代价表恢复路径', P + 'wave_path.png', '波算法：逐层扩展与沿步数递减回溯路径（示范场地）'),
    ('§链表', P + 'linked_list.png', '单链表与在中间插入结点'),
    ('§双向链表与柔性数组', P + 'doubly_linked.png', '双向链表'),
    ('**插入规则。** 新键从根开始', P + 'bst_insert.png', '二叉搜索树的插入'),
    ('§目录树与路径', P + 'directory_tree.png', '目录树与相对路径'),
    ('§文件定位与随机访问', P + 'fseek.png', 'fseek 的三种起点'),
    ('§命令行参数', P + 'argv.png', '命令行参数 argc 与 argv'),
])
