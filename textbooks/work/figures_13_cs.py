# 计算机科学基础册插图（2026-11-20）。运行：py work/figures_13_cs.py
from figlib import *
from matplotlib.patches import Circle, Rectangle, Polygon, Arc

style()
P = '13_'


def state(ax, xy, name, accept=False, start=False, r=.55, fc=LIGHT['blue'], ec=BLUE, fs=11):
    ax.add_patch(Circle(xy, r, fc=fc, ec=ec, lw=1.3))
    if accept:
        ax.add_patch(Circle(xy, r * .8, fc='none', ec=ec, lw=1.1))
    ax.text(*xy, name, ha='center', va='center', fontsize=fs)
    if start:
        arrow(ax, (xy[0] - r - .9, xy[1]), (xy[0] - r, xy[1]))


def loop(ax, xy, label, r=.45, up=True):
    s = 1 if up else -1
    ax.add_patch(Arc((xy[0], xy[1] + s * (r + .22)), .55, .6, theta1=-30 if up else 150, theta2=210 if up else 390, color=INK, lw=1))
    ax.text(xy[0], xy[1] + s * (r + .65), label, ha='center', va='center', fontsize=10)


def channel():
    fig, ax = canvas(6.4, 1.7, (0, 18), (0, 4.4))
    items = ['信源', '编码', '信道', '解码', '信宿']
    for i, t in enumerate(items):
        box(ax, .3 + i * 3.6, 1.2, 2.4, 1.4, t, LIGHT['red'] if t == '信道' else LIGHT['blue'], RED if t == '信道' else BLUE, fs=11)
        if i < 4:
            arrow(ax, (2.75 + i * 3.6, 1.9), (3.85 + i * 3.6, 1.9))
    arrow(ax, (8.5, 4.2), (8.5, 2.65), color=RED, text='噪声', toff=(.7, .3), fs=10)
    ax.text(9, .45, '消息 → 信号 → 受干扰的信号 → 还原的消息', ha='center', fontsize=10, color=GRAY)
    save(fig, P + 'communication_model.png', ticks=False)


def sampling():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.4), sharey=True)
    t = np.linspace(0, 1, 500); f = lambda x: 1.6 + 1.2 * np.sin(2 * np.pi * 1.3 * x) + .4 * np.sin(2 * np.pi * 3.1 * x)
    ts = np.arange(0, 1.0001, 1 / 12)
    a.plot(t, f(t), color=GRAY, lw=1.2); a.stem(ts, f(ts), linefmt=BLUE, markerfmt='o', basefmt=' '); a.set_title('采样：按固定时间间隔取值', fontsize=10)
    q = np.round(f(ts) * 2) / 2
    b.plot(t, f(t), color=GRAY, lw=1, alpha=.5); b.step(ts, q, where='post', color=ORANGE); b.plot(ts, q, 'o', color=ORANGE, ms=4)
    for lv in np.arange(0, 3.6, .5):
        b.axhline(lv, color='#eef0f3', lw=.8, zorder=0)
    b.set_title('量化：把取值归到有限个等级', fontsize=10)
    for ax in (a, b):
        ax.set_xlabel('时间'); ax.set_xticks([])
    a.set_ylabel('信号值')
    fig.tight_layout(); save(fig, P + 'sampling_quantization.png')


def hex_group():
    fig, ax = canvas(5.6, 1.8, (0, 14), (0, 4.4))
    bits = '11111010'
    for i, b in enumerate(bits):
        x = 2.0 + i * 1.1 + (.5 if i >= 4 else 0)
        box(ax, x, 2.4, 1.0, 1.0, b, LIGHT['blue'] if i < 4 else LIGHT['orange'], BLUE if i < 4 else ORANGE, r=.05)
        ax.text(x + .5, 3.75, f'$2^{7 - i}$', ha='center', fontsize=9, color=GRAY)
    ax.text(.3, 2.9, '$250=$', fontsize=12, va='center')
    for k, (x0, h, c) in enumerate([(2.0, 'F', BLUE), (6.9, 'A', ORANGE)]):
        ax.plot([x0 + .1, x0 + 4.2], [2.1, 2.1], color=c, lw=1.5); ax.text(x0 + 2.15, 1.35, h, ha='center', fontsize=14, color=c, family='monospace')
    ax.text(12.0, 1.35, '$=(\\mathrm{FA})_{16}$', fontsize=12, va='center')
    ax.text(7.0, .3, '每四位二进制对应一位十六进制', ha='center', fontsize=10, color=GRAY)
    save(fig, P + 'binary_hex.png', ticks=False)


def ranges():
    fig, ax = plt.subplots(figsize=(6.2, 1.8)); ax.axis('off'); ax.set_xlim(-430, 270); ax.set_ylim(-3, 3.4)
    for y, lo, hi, c, t in [(2, 0, 255, BLUE, '8 位无符号：0 … 255'), (-.6, -128, 127, ORANGE, '8 位补码：−128 … 127')]:
        ax.add_patch(Rectangle((lo, y - .4), hi - lo, .8, fc=c, alpha=.25, ec=c)); ax.text(lo, y + .7, str(lo), fontsize=9.5, ha='center'); ax.text(hi, y + .7, str(hi), fontsize=9.5, ha='center')
        ax.text(-425, y, t.replace('−', '-'), fontsize=10, va='center')
    ax.plot([0, 0], [-2.2, 3.4], color=GRAY, lw=.8, ls=':')
    ax.text(127, -2.4, '127 + 1 越界：位串 10000000 在补码下读作 -128', fontsize=9.5, color=RED, ha='center')
    save(fig, P + 'integer_ranges.png', ticks=False)


def endian():
    fig, ax = canvas(5.8, 2.2, (0, 14), (0, 5.4))
    bytes_ = ['12', '34', '56', '78']
    for row, (name, order, y) in enumerate([('大端序', bytes_, 3.4), ('小端序', bytes_[::-1], 1.2)]):
        ax.text(.2, y + .45, name, fontsize=11, va='center')
        for i, b in enumerate(order):
            c = [BLUE, GREEN, ORANGE, RED][bytes_.index(b)]
            box(ax, 2.6 + i * 1.6, y, 1.5, .9, b, 'white', c, fs=12, r=.05, family='monospace')
            if row == 1:
                ax.text(2.6 + i * 1.6 + .75, y - .45, f'a+{i}', ha='center', fontsize=9, color=GRAY, family='monospace')
    ax.text(9.4, 2.8, '整数 0x12345678\n各字节在内存中的排列\n（地址自左向右递增）', fontsize=10, va='center')
    save(fig, P + 'endianness.png', ticks=False)


def float_layout():
    fig, (a, b) = plt.subplots(2, 1, figsize=(6.0, 2.8), gridspec_kw={'height_ratios': [1, 1.2]})
    a.set_xlim(0, 32); a.set_ylim(0, 2); a.axis('off')
    for i in range(32):
        c = RED if i == 0 else ORANGE if i <= 8 else BLUE
        a.add_patch(Rectangle((i, .6), 1, .8, fc=c, alpha=.25, ec=c, lw=.5))
    a.text(.5, .2, '符号 1', ha='center', fontsize=9, color=RED); a.text(5, .2, '指数 8 位', ha='center', fontsize=9, color=ORANGE); a.text(20.5, .2, '尾数 23 位', ha='center', fontsize=9, color=BLUE)
    a.set_title('IEEE 754 单精度：$(-1)^s\\times1.f\\times2^{e-127}$', fontsize=10.5)
    vals = [m * 2.0 ** e for e in range(-2, 3) for m in np.arange(1, 2, .125)]
    b.plot(vals, np.zeros(len(vals)), '|', color=BLUE, ms=14); b.set_xlim(0, 8); b.set_yticks([]); b.spines['left'].set_visible(False)
    b.set_title('玩具浮点（尾数 3 位）可表示的数：越大越稀疏', fontsize=10)
    fig.tight_layout(); save(fig, P + 'floating_point.png')


def von_neumann():
    fig, ax = canvas(6.0, 2.8, (0, 15), (0, 7))
    ax.add_patch(Rectangle((.4, 2.6), 5.6, 4.0, fc=LIGHT['gray'], ec=GRAY)); ax.text(3.2, 6.25, '处理器 CPU', ha='center', fontsize=10.5)
    box(ax, .9, 4.2, 2.2, 1.4, '控制器', LIGHT['blue'], BLUE, fs=10); box(ax, 3.4, 4.2, 2.2, 1.4, '运算器\nALU', LIGHT['blue'], BLUE, fs=10)
    box(ax, .9, 2.9, 4.7, .9, '寄存器（含程序计数器 PC）', LIGHT['orange'], ORANGE, fs=9.5)
    box(ax, 8.4, 3.6, 3.0, 2.4, '内存\n指令与数据\n同存一处', LIGHT['green'], GREEN, fs=10)
    box(ax, 12.0, 3.6, 2.6, 2.4, '输入/输出\n设备', LIGHT['purple'], PURPLE, fs=10)
    ax.add_patch(Rectangle((.4, .8), 14.2, .7, fc='#e5e7eb', ec=GRAY)); ax.text(7.5, 1.15, '总线：地址、数据、控制信号', ha='center', va='center', fontsize=10)
    for x in (3.2, 9.9, 13.3):
        arrow(ax, (x, 1.5), (x, 2.6 if x < 5 else 3.6), style='<|-|>', color=GRAY)
    ax.text(7.2, 6.4, '取指 → 译码 → 执行 → 写回', fontsize=10, color=BLUE)
    save(fig, P + 'von_neumann.png', ticks=False)


def hierarchy():
    fig, ax = canvas(5.4, 2.9, (0, 13.2), (0, 6.6))
    levels = [('寄存器', '< 1 ns'), ('高速缓存', '约 1–10 ns'), ('内存', '约 100 ns'), ('固态硬盘', '约 100 µs'), ('机械硬盘、网络存储', '约 10 ms')]
    for i, (t, s) in enumerate(levels):
        y = 5.6 - i * 1.15; w = 2.0 + i * 1.6; x = 4.0 - w / 2
        ax.add_patch(Polygon([(x, y), (x + w, y), (x + w + .8, y - 1.0), (x - .8, y - 1.0)], fc=plt.cm.Blues(.25 + .13 * (4 - i)), ec='white'))
        ax.text(4.0, y - .5, t, ha='center', va='center', fontsize=10, color='white' if i < 2 else INK)
        ax.text(9.0, y - .5, s, va='center', fontsize=9.5, color=GRAY)
    arrow(ax, (12.2, .5), (12.2, 5.5), color=GRAY); ax.text(12.2, 6.0, '更快、更小、更贵', ha='center', fontsize=9, color=GRAY)
    save(fig, P + 'memory_hierarchy.png', ticks=False)


def flow_max():
    fig, ax = canvas(5.4, 3.4, (0, 12), (0, 8))
    box(ax, 3.4, 7.0, 3.6, .8, '$m\\leftarrow a_1$，$k\\leftarrow1$', fs=10.5)
    ax.add_patch(Polygon([(5.2, 6.3), (7.2, 5.5), (5.2, 4.7), (3.2, 5.5)], fc=LIGHT['orange'], ec=ORANGE)); ax.text(5.2, 5.5, '$k<n$ ?', ha='center', va='center', fontsize=10.5)
    box(ax, 3.4, 3.4, 3.6, .8, '$k\\leftarrow k+1$', fs=10.5)
    ax.add_patch(Polygon([(5.2, 2.9), (7.2, 2.1), (5.2, 1.3), (3.2, 2.1)], fc=LIGHT['orange'], ec=ORANGE)); ax.text(5.2, 2.1, '$a_k>m$ ?', ha='center', va='center', fontsize=10.5)
    box(ax, 8.4, 1.7, 2.6, .8, '$m\\leftarrow a_k$', fs=10.5); box(ax, 8.4, 5.1, 2.6, .8, '输出 $m$', LIGHT['green'], GREEN, fs=10.5)
    arrow(ax, (5.2, 7.0), (5.2, 6.3)); arrow(ax, (5.2, 4.7), (5.2, 4.2), text='是', toff=(.4, 0)); arrow(ax, (5.2, 3.4), (5.2, 2.9))
    arrow(ax, (7.2, 5.5), (8.4, 5.5), text='否', toff=(0, .25)); arrow(ax, (7.2, 2.1), (8.4, 2.1), text='是', toff=(0, .25))
    wire(ax, (5.2, 1.3), (5.2, .5), (2.4, .5), (2.4, 5.5)); arrow(ax, (2.4, 5.5), (3.2, 5.5)); ax.text(4.9, .8, '否', fontsize=10)
    wire(ax, (9.7, 1.7), (9.7, .5), (5.2, .5))
    ax.text(.2, 7.4, '不变量：$m$ 是\n$a_1,\\ldots,a_k$ 的最大值', fontsize=9.5, color=BLUE)
    save(fig, P + 'max_flowchart.png', ticks=False)


def euclid():
    fig, ax = plt.subplots(figsize=(5.0, 2.4)); ax.set_aspect('equal'); ax.axis('off')
    a, b = 48, 18; x0, y0 = 0, 0; W, H = a, b; cols = [BLUE, ORANGE, GREEN, RED]; k = 0
    ax.add_patch(Rectangle((0, 0), 48, 18, fc='none', ec=INK, lw=1.2))
    x, y, w, h = 0, 0, 48, 18
    while w and h:
        if w >= h:
            n = w // h
            for i in range(n):
                ax.add_patch(Rectangle((x + i * h, y), h, h, fc=cols[k % 4], alpha=.3, ec=cols[k % 4]))
                ax.text(x + i * h + h / 2, y + h / 2, str(h), ha='center', va='center', fontsize=10 if h > 8 else 8)
            x += n * h; w -= n * h
        else:
            n = h // w
            for i in range(n):
                ax.add_patch(Rectangle((x, y + i * w), w, w, fc=cols[k % 4], alpha=.3, ec=cols[k % 4]))
                ax.text(x + w / 2, y + i * w + w / 2, str(w), ha='center', va='center', fontsize=9)
            y += n * w; h -= n * w
        k += 1
    ax.set_xlim(-1, 49); ax.set_ylim(-5, 19)
    ax.text(24, -3.5, '$(48,18)\\to(18,12)\\to(12,6)\\to(6,0)$，最大公约数为 6', ha='center', fontsize=10.5)
    save(fig, P + 'euclid_gcd.png', ticks=False)


def growth():
    fig, ax = plt.subplots(figsize=(4.6, 2.9)); n = np.linspace(1, 20, 300)
    for f, lab, c in [(np.log2(n), '$\\log n$', GREEN), (n, '$n$', BLUE), (n * np.log2(n), '$n\\log n$', ORANGE), (n ** 2, '$n^2$', RED), (2 ** n, '$2^n$', PURPLE)]:
        ax.plot(n, f, color=c, label=lab)
    ax.set_ylim(0, 420); ax.set_xlabel('问题规模 $n$'); ax.set_ylabel('步数'); ax.legend(fontsize=9.5, loc='upper left')
    ax.set_title('常见复杂度的增长速度', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'complexity_growth.png')


def parity_dfa():
    fig, ax = canvas(4.6, 2.0, (0, 10), (0, 4.4))
    state(ax, (3, 2), '偶', accept=False, start=True); state(ax, (7, 2), '奇', accept=True)
    arrow(ax, (3.45, 2.25), (6.55, 2.25), rad=-.3, text='1', toff=(0, .75)); arrow(ax, (6.55, 1.75), (3.45, 1.75), rad=-.3, text='1', toff=(0, -.75))
    loop(ax, (3, 2), '0'); loop(ax, (7, 2), '0')
    ax.text(5, .1, '识别“1 的个数为奇数”的串；双圈为接受状态', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'parity_dfa.png', ticks=False)


def nfa_dfa():
    fig, (a, b) = plt.subplots(2, 1, figsize=(4.8, 4.2))
    for ax in (a, b):
        ax.set_aspect('equal'); ax.axis('off')
    a.set_xlim(-1.4, 9); a.set_ylim(-.6, 3.8)
    state(a, (1, 1.5), '$q_0$', start=True); state(a, (4, 1.5), '$q_1$'); state(a, (7, 1.5), '$q_2$', accept=True)
    arrow(a, (1.45, 1.5), (3.55, 1.5), text='0', toff=(0, .25)); arrow(a, (4.45, 1.5), (6.55, 1.5), text='1', toff=(0, .25)); loop(a, (1, 1.5), '0, 1')
    a.set_title('NFA：猜测“最后两位开始了”', fontsize=10)
    b.set_xlim(-1.6, 9); b.set_ylim(-.9, 3.8)
    state(b, (1, 1.5), '{0}', start=True, fs=10); state(b, (4, 1.5), '{0,1}', fs=10); state(b, (7, 1.5), '{0,2}', accept=True, fs=10)
    arrow(b, (1.45, 1.5), (3.55, 1.5), text='0', toff=(0, .25)); arrow(b, (4.45, 1.5), (6.55, 1.5), text='1', toff=(0, .25))
    loop(b, (1, 1.5), '1'); loop(b, (4, 1.5), '0')
    arrow(b, (6.7, 1.15), (4.3, 1.15), rad=-.35, text='0', toff=(0, -.75)); arrow(b, (6.8, 1.1), (1.2, 1.1), rad=-.45, text='1', toff=(0, -1.5))
    b.set_title('子集构造得到的 DFA', fontsize=10)
    fig.tight_layout(); save(fig, P + 'nfa_to_dfa.png', ticks=False)


def pumping():
    fig, ax = canvas(5.6, 2.2, (0, 14), (0, 5.4))
    for i in range(6):
        ax.text(.4 + i * 1.2, 4.5, f'$a^{i}$', fontsize=11, ha='center')
    for j in range(4):
        state(ax, (2.2 + j * 2.8, 1.4), f'$q_{j}$', r=.5)
    tg = [0, 1, 2, 3, 1, 2]
    for i, t in enumerate(tg):
        arrow(ax, (.4 + i * 1.2, 4.2), (2.2 + t * 2.8, 1.95), color=RED if i in (1, 4) else GRAY, lw=1.4 if i in (1, 4) else .8)
    ax.text(12.0, 3.4, '状态只有有限个，\n必有 $a^i,a^j$（$i\\neq j$）\n落到同一状态，\n再接 $b^i$ 就无法区分', fontsize=9.5, va='center', color=RED)
    save(fig, P + 'finite_memory.png', ticks=False)


def turing():
    fig, ax = canvas(5.8, 2.2, (0, 15), (0, 5.4))
    tape = ['□', '1', '0', '1', '1', '□', '□', '□']
    for i, s in enumerate(tape):
        box(ax, 1.0 + i * 1.5, 1.0, 1.5, 1.2, s, LIGHT['orange'] if i == 3 else 'white', GRAY, r=.02, fs=13)
    ax.text(.4, 1.6, '…', fontsize=14, ha='center'); ax.text(13.6, 1.6, '…', fontsize=14, ha='center')
    ax.add_patch(Polygon([(5.25, 2.25), (5.75, 2.25), (5.5, 2.75)], fc=RED)); box(ax, 4.2, 3.0, 2.6, 1.6, '控制器\n状态 $s$', LIGHT['blue'], BLUE, fs=10)
    ax.text(8.0, 3.8, '每一步：读当前格，\n写一个符号，左移或右移，\n转到新状态', fontsize=9.5, va='center')
    save(fig, P + 'turing_machine.png', ticks=False)


def diagonal():
    fig, ax = canvas(4.8, 3.0, (0, 9), (0, 6.4))
    n = 5; vals = [['停', '不', '停', '停', '不'], ['不', '不', '停', '不', '停'], ['停', '停', '停', '不', '停'], ['不', '停', '不', '停', '不'], ['停', '不', '不', '停', '停']]
    for j in range(n):
        ax.text(2.2 + j * 1.0, 5.9, f'$P_{j + 1}$', ha='center', fontsize=10)
    for i in range(n):
        ax.text(1.2, 5.0 - i * .9, f'$P_{i + 1}$', ha='center', va='center', fontsize=10)
        for j in range(n):
            d = i == j
            ax.add_patch(Rectangle((1.7 + j, 4.55 - i * .9), 1.0, .9, fc=LIGHT['orange'] if d else 'white', ec=GRAY, lw=.6))
            ax.text(2.2 + j, 5.0 - i * .9, vals[i][j], ha='center', va='center', fontsize=9.5)
    ax.text(.2, .3, '对角线上取反构造 $D$：$D$ 与每个 $P_i$ 在输入 $P_i$ 处不同', fontsize=9.5)
    ax.text(.1, 6.2, '程序', fontsize=9, color=GRAY); ax.text(7.0, 5.9, '输入', fontsize=9, color=GRAY)
    save(fig, P + 'diagonal.png', ticks=False)


for f in [channel, sampling, hex_group, ranges, endian, float_layout, von_neumann, hierarchy, flow_max, euclid, growth, parity_dfa, nfa_dfa, pumping, turing, diagonal]:
    f()

place('13_计算机科学基础.md', [
    ('传递过程可以按信源、编码、信', P + 'communication_model.png', '信息传递的基本模型'),
    ('**采集过程示例。**', P + 'sampling_quantization.png', '连续信号的采样与量化'),
    ('二进制只用零和一，十六进制用', P + 'binary_hex.png', '二进制按四位分组得到十六进制'),
    ('数学整数没有固定上限', P + 'integer_ranges.png', '八位整数的两种解释与溢出'),
    ('字节序说明多字节对象的各字节', P + 'endianness.png', '大端序与小端序'),
    ('浮点数以有限位记录符号、指数', P + 'floating_point.png', '浮点数的位布局与可表示数的分布'),
    ('处理器执行指令，运行内存保存', P + 'von_neumann.png', '存储程序计算机的组成'),
    ('正在运行的程序频繁访问的数据', P + 'memory_hierarchy.png', '存储层次（量级为典型值）'),
    ('求最大值的算法可先令当前最大', P + 'max_flowchart.png', '求最大值算法的流程图与循环不变量'),
    ('**欧几里得算法。**', P + 'euclid_gcd.png', '欧几里得算法的几何解释：用正方形铺满矩形'),
    ('按步数随问题规模', P + 'complexity_growth.png', '复杂度函数的增长比较'),
    ('转移规则为 \\(\\delta', P + 'parity_dfa.png', '奇数个 1 的识别自动机'),
    ('可以用一个状态集合记录当前所', P + 'nfa_to_dfa.png', '识别“以 01 结尾”的 NFA 与子集构造'),
    ('此后给两者都接上', P + 'finite_memory.png', '有限自动机的状态不够记住任意大的计数'),
    ('图灵机包含有限控制状态、带字', P + 'turing_machine.png', '图灵机：控制器、读写头与无限纸带'),
    ('**对角论证。**', P + 'diagonal.png', '停机问题的对角论证'),
])
