# 数字电子技术基础册插图（2026-11-20）。运行：py work/figures_08_digital.py
from figlib import *
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Arc, Polygon

style()
P = '08_'


def levels():
    fig, ax = plt.subplots(figsize=(5.0, 2.6)); t = np.linspace(0, 10, 1000)
    v = 2.5 + 2.2 * np.tanh(3 * np.sin(1.1 * t)) + .15 * np.sin(17 * t)
    ax.axhspan(3.5, 5.2, color=GREEN, alpha=.12); ax.axhspan(-.2, 1.5, color=BLUE, alpha=.12); ax.axhspan(1.5, 3.5, color=RED, alpha=.07)
    ax.plot(t, v, color=INK, lw=1.4)
    ax.text(10.1, 4.3, '逻辑 1\n$v\\geq V_{IH}$', fontsize=9.5, color=GREEN, va='center'); ax.text(10.1, .6, '逻辑 0\n$v\\leq V_{IL}$', fontsize=9.5, color=BLUE, va='center')
    ax.text(10.1, 2.5, '不确定区', fontsize=9.5, color=RED, va='center')
    ax.set_xticks([]); ax.set_ylabel('电压 / V（示范）'); ax.set_xlim(0, 10); ax.set_ylim(-.2, 5.2)
    ax.set_title('逻辑值对应电压范围，而不是某个精确电压', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'logic_levels.png')


def switches():
    fig, axs = plt.subplots(1, 2, figsize=(6.0, 2.0))
    for ax, mode in zip(axs, ('串联：与', '并联：或')):
        ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.set_aspect('equal'); ax.axis('off')
        lamp = (8.6, 2); ax.add_patch(Circle(lamp, .55, fc=LIGHT['orange'], ec=ORANGE)); ax.plot([8.2, 9.0], [1.6, 2.4], color=ORANGE, lw=.8); ax.plot([8.2, 9.0], [2.4, 1.6], color=ORANGE, lw=.8)
        def sw(x, y, lab):
            ax.plot([x, x + .3], [y, y], color=INK); ax.plot([x + .3, x + 1.2], [y, y + .45], color=INK); ax.plot([x + 1.3, x + 1.6], [y, y], color=INK)
            ax.plot([x + .3, x + 1.3], [y, y], 'o', color=INK, ms=3); ax.text(x + .8, y + .6, lab, ha='center', fontsize=11)
        if mode.startswith('串'):
            wire(ax, (.5, 2), (1.5, 2)); sw(1.5, 2, '$A$'); wire(ax, (3.1, 2), (4.3, 2)); sw(4.3, 2, '$B$'); wire(ax, (5.9, 2), (8.05, 2))
        else:
            wire(ax, (.5, 2), (1.5, 2)); wire(ax, (1.5, 3), (1.5, 1)); sw(1.5, 3, '$A$'); sw(1.5, 1, '$B$')
            wire(ax, (3.1, 3), (4.5, 3), (4.5, 1), (3.1, 1)); wire(ax, (4.5, 2), (8.05, 2))
        wire(ax, (9.15, 2), (9.7, 2), (9.7, .2), (.5, .2), (.5, 2)); ax.text(.1, 1.0, '电源', fontsize=9, rotation=90, va='center')
        ax.set_title(f'{mode}　$Y={"AB" if mode.startswith("串") else "A+B"}$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'switches.png', ticks=False)


def division():
    fig, ax = canvas(4.4, 2.6, (0, 9), (0, 5.4))
    n, rows = 13, []
    while n:
        rows.append((n, n // 2, n % 2)); n //= 2
    for i, (a, q, r) in enumerate(rows):
        y = 4.6 - i * 1.0
        ax.text(1.0, y, f'${a}\\div 2={q}$', fontsize=12, va='center'); ax.text(4.0, y, '余', fontsize=11, va='center', color=GRAY)
        box(ax, 4.6, y - .35, .7, .7, str(r), LIGHT['orange'], ORANGE, fs=12)
    arrow(ax, (6.0, .6), (6.0, 4.7), color=RED, lw=1.6); ax.text(6.3, 2.6, '自下而上读：\n$13=(1101)_2$', fontsize=11, color=RED, va='center')
    save(fig, P + 'division_by_two.png', ticks=False)


def twos_wheel():
    fig, ax = canvas(3.8, 3.8, (-1.6, 1.6), (-1.6, 1.6))
    ax.add_patch(Circle((0, 0), 1.05, fc='none', ec=GRAY))
    for k in range(16):
        ang = np.pi / 2 - 2 * np.pi * k / 16; x, y = np.cos(ang), np.sin(ang)
        val = k if k < 8 else k - 16; col = BLUE if val >= 0 else RED
        ax.text(1.3 * x, 1.3 * y, f'{k:04b}', ha='center', va='center', fontsize=8.5, family='monospace')
        ax.text(.78 * x, .78 * y, f'${val}$', ha='center', va='center', fontsize=10, color=col)
        ax.plot([.95 * x, 1.05 * x], [.95 * y, 1.05 * y], color=GRAY, lw=.8)
    a1 = np.pi / 2 - 2 * np.pi * 7.5 / 16; ax.plot([.3 * np.cos(a1), 1.1 * np.cos(a1)], [.3 * np.sin(a1), 1.1 * np.sin(a1)], color=RED, lw=2)
    ax.text(0, -.05, '四位补码\n$+1$ 顺时针', ha='center', va='center', fontsize=9.5)
    ax.text(.55, -1.5, '$7$ 与 $-8$ 之间：有符号溢出', fontsize=9, color=RED)
    save(fig, P + 'twos_complement_wheel.png', ticks=False)


def gray():
    fig, ax = canvas(5.6, 2.4, (0, 12), (0, 5.0))
    for j, h in enumerate(['十进制', '自然二进制', '格雷码']):
        ax.text([0.8, 4.0, 9.0][j], 4.6, h, ha='center', fontsize=10)
    prev_b = prev_g = None
    for k in range(8):
        y = 4.0 - k * .5; b = f'{k:03b}'; g = f'{k ^ (k >> 1):03b}'
        ax.text(.8, y, str(k), ha='center', va='center', fontsize=10)
        for j, (s, prev, x0) in enumerate([(b, prev_b, 3.1), (g, prev_g, 8.1)]):
            for i, ch in enumerate(s):
                changed = prev is not None and prev[i] != ch
                ax.add_patch(Rectangle((x0 + i * .6, y - .22), .58, .44, fc=LIGHT['orange'] if changed else 'white', ec=GRAY, lw=.6))
                ax.text(x0 + i * .6 + .29, y, ch, ha='center', va='center', fontsize=10, family='monospace')
        prev_b, prev_g = b, g
    ax.text(6.0, -.1, '橙色为相对上一行改变的位：自然二进制一次可变 3 位，格雷码每次只变 1 位', ha='center', fontsize=9.5)
    save(fig, P + 'gray_code.png', ticks=False)


def gates():
    fig, ax = canvas(6.4, 2.6, (0, 15), (0, 6))
    items = [('and', '与', '$Y=AB$'), ('or', '或', '$Y=A+B$'), ('not', '非', '$Y=\\overline{A}$'), ('nand', '与非', '$Y=\\overline{AB}$'), ('nor', '或非', '$Y=\\overline{A+B}$'), ('xor', '异或', '$Y=A\\oplus B$')]
    for i, (k, name, expr) in enumerate(items):
        cx, cy = 1.2 + (i % 3) * 5.0, 4.4 - (i // 3) * 3.0
        ins, out = gate(ax, k, cx, cy, .9)
        for p in ins:
            wire(ax, (p[0] - .6, p[1]), p)
        wire(ax, out, (out[0] + .6, out[1]))
        ax.text(cx + 3.0, cy + .25, name, fontsize=11, va='center'); ax.text(cx + 3.0, cy - .35, expr, fontsize=11, va='center')
    save(fig, P + 'gate_symbols.png', ticks=False)


def majority():
    fig, ax = canvas(5.4, 2.8, (0, 12), (0, 6.2))
    ys = [5.0, 3.1, 1.2]; pairs = [('A', 'B'), ('B', 'C'), ('A', 'C')]
    xs = {'A': .8, 'B': 1.4, 'C': 2.0}
    for v, x in xs.items():
        ax.plot([x, x], [.4, 5.9], color=INK, lw=1); ax.text(x, 6.0, f'${v}$', ha='center', fontsize=11)
    outs = []
    for y, (u, v) in zip(ys, pairs):
        ins, out = gate(ax, 'and', 4.0, y, .9); outs.append(out)
        for p, var in zip(ins, (u, v)):
            wire(ax, (xs[var], p[1]), p); ax.plot(xs[var], p[1], 'o', color=INK, ms=3)
    # 三输入或门：画两个两输入或门级联的简化形式，用一个较大的或门表示
    ins, out = gate(ax, 'or', 8.0, 3.1, 1.4)
    tgt = [(8.15, 3.75), (8.3, 3.1), (8.15, 2.45)]
    for o, t in zip(outs, tgt):
        wire(ax, o, (7.2, o[1]), (7.2, t[1]), t)
    wire(ax, out, (11.2, 3.1)); ax.text(11.3, 3.1, '$Y$', va='center', fontsize=12)
    ax.text(6.0, .1, '$Y=AB+BC+AC$', ha='center', fontsize=11)
    save(fig, P + 'majority_voter.png', ticks=False)


def mux():
    fig, ax = canvas(5.4, 2.6, (-.8, 12), (0, 6))
    i1, o1 = gate(ax, 'and', 5.0, 4.4, .9); i2, o2 = gate(ax, 'and', 5.0, 1.6, .9)
    ni, no = gate(ax, 'not', 2.4, 3.0, .6)
    wire(ax, (.6, 4.4 + .27), i1[0]); ax.text(-.5, 4.67, '$D_0$', va='center')
    wire(ax, (.6, 1.6 - .27), i2[1]); ax.text(-.5, 1.33, '$D_1$', va='center')
    wire(ax, (.6, 3.0), ni[0]); ax.text(-.5, 3.0, '$S$', va='center'); ax.plot(1.5, 3.0, 'o', color=INK, ms=3)
    wire(ax, no, (4.4, 3.0), (4.4, i1[1][1]), i1[1]); wire(ax, (1.5, 3.0), (1.5, i2[0][1]), i2[0])
    io, oo = gate(ax, 'or', 8.4, 3.0, .9)
    wire(ax, o1, (7.8, o1[1]), (7.8, io[0][1]), io[0]); wire(ax, o2, (7.8, o2[1]), (7.8, io[1][1]), io[1])
    wire(ax, oo, (11.0, 3.0)); ax.text(11.1, 3.0, '$Y$', va='center')
    ax.text(6.0, .1, '$Y=\\overline{S}D_0+SD_1$：$S=0$ 选 $D_0$，$S=1$ 选 $D_1$', ha='center', fontsize=10.5)
    save(fig, P + 'mux2.png', ticks=False)


def kmap(ax, nr, nc, rl, cl, vals, rvar, cvar, groups):
    for i in range(nr):
        for j in range(nc):
            ax.add_patch(Rectangle((j, nr - 1 - i), 1, 1, fc='white', ec=GRAY))
            v = vals[i][j]
            ax.text(j + .5, nr - .5 - i, v, ha='center', va='center', fontsize=12, color=INK if v == '1' else '#9aa3ad')
    for j, l in enumerate(cl):
        ax.text(j + .5, nr + .25, l, ha='center', fontsize=9.5, family='monospace')
    for i, l in enumerate(rl):
        ax.text(-.3, nr - .5 - i, l, ha='center', va='center', fontsize=9.5, family='monospace')
    ax.text(-.55, nr + .3, f'{rvar}\\{cvar}', fontsize=9, ha='center')
    for (x, y, w, h, c) in groups:
        ax.add_patch(FancyBboxPatch((x + .08, y + .08), w - .16, h - .16, boxstyle='round,pad=0,rounding_size=.3', fc=c, ec=c, alpha=.25, lw=1.5))
    ax.set_xlim(-1, nc + .3); ax.set_ylim(-.5, nr + .6); ax.set_aspect('equal'); ax.axis('off')


def kmaps():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 2.8))
    vals3 = [['0', '1', '1', '0'], ['0', '1', '1', '0']]
    kmap(a, 2, 4, ['0', '1'], ['00', '01', '11', '10'], vals3, 'A', 'BC', [(1, 0, 2, 2, BLUE)])
    a.set_title('$Y=\\Sigma m(1,3,5,7)=C$', fontsize=10.5)
    gray4 = ['00', '01', '11', '10']
    vals4 = [['1' if (r in ('00', '10') and c in ('00', '10')) else '0' for c in gray4] for r in gray4]
    kmap(b, 4, 4, gray4, gray4, vals4, 'AB', 'CD', [(-.3, 3, .8, 1, ORANGE), (3.5, 3, .8, 1, ORANGE), (-.3, 0, .8, 1, ORANGE), (3.5, 0, .8, 1, ORANGE)])
    b.set_title('四角相邻：$\\overline{B}\\,\\overline{D}$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'karnaugh.png', ticks=False)


def full_adder():
    fig, ax = canvas(6.0, 2.8, (0, 14), (0, 6.4))
    x1, o1 = gate(ax, 'xor', 2.4, 4.6, .9); x2, o2 = gate(ax, 'xor', 6.6, 4.0, .9)
    a1, p1 = gate(ax, 'and', 6.6, 2.2, .9); a2, p2 = gate(ax, 'and', 6.6, .9, .9)
    og, oo = gate(ax, 'or', 10.0, 1.6, .9)
    ax.text(.2, x1[0][1], '$A$', va='center'); ax.text(.2, x1[1][1], '$B$', va='center'); ax.text(.2, 3.4, '$C_{in}$', va='center')
    wire(ax, (1.0, x1[0][1]), x1[0]); wire(ax, (1.4, x1[1][1]), x1[1])
    wire(ax, (1.0, x1[0][1]), (1.0, a2[0][1]), a2[0]); wire(ax, (1.4, x1[1][1]), (1.4, a2[1][1]), a2[1])
    ax.plot([1.0, 1.4], [x1[0][1], x1[1][1]], 'o', color=INK, ms=3)
    wire(ax, o1, (5.4, o1[1]), (5.4, x2[0][1]), x2[0]); wire(ax, (5.4, x2[0][1]), (5.4, a1[0][1]), a1[0]); ax.plot(5.4, x2[0][1], 'o', color=INK, ms=3)
    wire(ax, (.9, 3.4), (5.0, 3.4), (5.0, x2[1][1]), x2[1]); wire(ax, (5.0, 3.4), (5.0, a1[1][1]), a1[1]); ax.plot(5.0, 3.4, 'o', color=INK, ms=3)
    wire(ax, o2, (12.6, o2[1])); ax.text(12.7, o2[1], '$S$', va='center')
    wire(ax, p1, (9.4, p1[1]), (9.4, og[0][1]), og[0]); wire(ax, p2, (9.4, p2[1]), (9.4, og[1][1]), og[1])
    wire(ax, oo, (12.6, oo[1])); ax.text(12.7, oo[1], '$C_{out}$', va='center')
    ax.text(7.0, 6.0, '$S=A\\oplus B\\oplus C_{in}$　　$C_{out}=AB+(A\\oplus B)C_{in}$', ha='center', fontsize=10.5)
    save(fig, P + 'full_adder.png', ticks=False)


def ripple():
    fig, ax = canvas(6.4, 2.0, (0, 16), (0, 4.6))
    bits = [('0', '0'), ('1', '0'), ('1', '1'), ('1', '1')]
    carries = [0, 1, 1, 1, 0]; sums = '1010'
    for k in range(4):
        x = 12.2 - k * 3.6
        box(ax, x, 1.4, 2.2, 1.6, 'FA', LIGHT['blue'], BLUE, fs=11)
        a, b = bits[3 - k][0], bits[3 - k][1]
        a = '0111'[3 - k]; b = '0011'[3 - k]
        ax.text(x + 1.1, 3.55, f'$A_{k}B_{k}={a}{b}$', ha='center', fontsize=9.5)
        wire(ax, (x + .6, 3.3), (x + .6, 3.0)); wire(ax, (x + 1.6, 3.3), (x + 1.6, 3.0))
        wire(ax, (x + 1.1, 1.4), (x + 1.1, .9)); ax.text(x + 1.1, .55, f'$S_{k}={sums[3 - k]}$', ha='center', fontsize=9.5, color=GREEN)
        arrow(ax, (x, 2.2), (x - 1.35, 2.2), color=RED, lw=1.2)
        ax.text(x - .7, 2.45, f'{carries[k + 1]}', ha='center', fontsize=9.5, color=RED)
    ax.text(15.4, 2.2, '$C_0=0$', fontsize=9.5, va='center', color=RED); arrow(ax, (15.3, 2.2), (14.45, 2.2), color=RED, lw=1.2)
    ax.text(8, -.1, '$0111+0011=1010$：进位（红）逐位向高位传递', ha='center', fontsize=10)
    save(fig, P + 'ripple_carry.png', ticks=False)


def wave(ax, y, seq, t, label, color=INK, h=.7):
    xs, ys = [], []
    for i, v in enumerate(seq):
        xs += [t[i], t[i + 1]]; ys += [y + v * h, y + v * h]
    ax.plot(xs, ys, color=color, lw=1.6, drawstyle='steps-post' if False else 'default')
    ax.text(t[0] - .3, y + h / 2, label, ha='right', va='center', fontsize=11)


def hazard():
    fig, ax = plt.subplots(figsize=(5.2, 2.6)); ax.axis('off')
    t = [0, 3, 6.0, 10]; ax.set_xlim(-1.8, 10.2); ax.set_ylim(-.3, 4.2)
    wave(ax, 3.2, [1, 0, 0], [0, 3, 6, 10], '$A$')
    wave(ax, 2.1, [0, 0, 1], [0, 3, 3.8, 10], '$\\overline{A}$', BLUE)
    wave(ax, 1.0, [1, 0, 1], [0, 3.2, 4.0, 10], '$AB$ 与 $\\overline{A}C$\n之或 $Y$', RED)
    ax.axvspan(3.0, 3.8, color=RED, alpha=.08); ax.text(3.4, -.25, '非门延迟', ha='center', fontsize=9.5, color=RED)
    for y in (3.2, 2.1, 1.0):
        ax.plot([-.1, 10], [y, y], color='#e5e7eb', lw=.6, zorder=0)
    ax.set_title('$B=C=1$ 时 $A$ 由 1 变 0：$Y$ 出现短暂的 0（毛刺）', fontsize=10)
    fig.tight_layout(); save(fig, P + 'hazard.png', ticks=False)


def latch_ff():
    fig, ax = plt.subplots(figsize=(5.6, 2.9)); ax.axis('off'); ax.set_xlim(-2.2, 12.2); ax.set_ylim(-.4, 4.6)
    clk_t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; clk = [0, 1] * 6
    wave(ax, 3.6, clk, clk_t, 'CLK/EN')
    d_t = [0, 1.4, 2.6, 3.3, 5.5, 8.4, 9.3, 12]; d = [0, 1, 0, 1, 0, 1, 0]
    wave(ax, 2.4, d, d_t, '$D$', BLUE)
    # 锁存器：EN=1 期间透明
    lt, lv = [0], [0]; cur = 0
    ts = np.linspace(0, 12, 1201)
    def dval(x):
        for i in range(len(d)):
            if d_t[i] <= x < d_t[i + 1]:
                return d[i]
        return d[-1]
    q = []
    for x in ts:
        if int(x) % 2 == 1:
            cur = dval(x)
        q.append(cur)
    ax.plot(ts, 1.2 + .7 * np.array(q), color=ORANGE, lw=1.6); ax.text(-.3, 1.55, '锁存器 $Q$', ha='right', va='center', fontsize=10.5)
    cur = 0; qf = []
    for x in ts:
        if abs(x - round(x)) < 1e-9 and int(round(x)) % 2 == 1:
            cur = dval(x)
        qf.append(cur)
    ax.plot(ts, 0 + .7 * np.array(qf), color=GREEN, lw=1.6); ax.text(-.3, .35, '触发器 $Q$', ha='right', va='center', fontsize=10.5)
    for x in range(1, 12, 2):
        ax.axvline(x, color=GRAY, ls=':', lw=.7)
    ax.set_title('锁存器在使能为 1 期间跟随 $D$；边沿触发器只在上升沿采样', fontsize=10)
    fig.tight_layout(); save(fig, P + 'latch_vs_flipflop.png', ticks=False)


def state_diagrams():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.8))
    for ax in (a, b):
        ax.set_aspect('equal'); ax.axis('off')
    a.set_xlim(-2.2, 2.2); a.set_ylim(-2.2, 2.2)
    pos = {0: (0, 1.3), 1: (1.3, 0), 2: (0, -1.3), 3: (-1.3, 0)}
    for k, p in pos.items():
        a.add_patch(Circle(p, .38, fc=LIGHT['blue'], ec=BLUE)); a.text(*p, f'{k:02b}', ha='center', va='center', fontsize=10, family='monospace')
        n = pos[(k + 1) % 4]; arrow(a, (p[0] + (n[0] - p[0]) * .3, p[1] + (n[1] - p[1]) * .3), (p[0] + (n[0] - p[0]) * .7, p[1] + (n[1] - p[1]) * .7), color=GREEN, rad=-.25)
        a.add_patch(Arc((p[0] * 1.42, p[1] * 1.42), .5, .5, color=GRAY, lw=1))
    a.text(0, 0, '$E=1$：加一\n$E=0$：保持\n（灰圈）', ha='center', va='center', fontsize=9)
    a.set_title('模四计数器', fontsize=10.5)
    b.set_xlim(-2.4, 2.4); b.set_ylim(-1.8, 1.8)
    for k, x in [(0, -1.2), (1, 1.2)]:
        b.add_patch(Circle((x, 0), .5, fc=LIGHT['orange'], ec=ORANGE)); b.text(x, 0, f'$Q={k}$\n' + ('偶' if k == 0 else '奇'), ha='center', va='center', fontsize=9.5)
    arrow(b, (-.7, .2), (.7, .2), color=RED, rad=-.3, text='$X=1$', toff=(0, .5)); arrow(b, (.7, -.2), (-.7, -.2), color=RED, rad=-.3, text='$X=1$', toff=(0, -.5))
    b.add_patch(Arc((-1.85, 0), .7, .7, theta1=60, theta2=300, color=GRAY)); b.text(-2.35, .55, '$X=0$', fontsize=9.5, color=GRAY)
    b.add_patch(Arc((1.85, 0), .7, .7, theta1=-120, theta2=120, color=GRAY)); b.text(1.95, .55, '$X=0$', fontsize=9.5, color=GRAY)
    b.set_title('奇偶检测：$Q^+=Q\\oplus X$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'state_diagrams.png', ticks=False)


def shift_register():
    fig, ax = canvas(6.2, 1.9, (0, 16), (0, 4.6))
    for k in range(4):
        x = 2.0 + k * 3.4
        box(ax, x, 1.4, 2.0, 2.0, '', LIGHT['blue'], BLUE)
        ax.text(x + .35, 2.4, 'D', fontsize=10, va='center'); ax.text(x + 1.65, 2.4, 'Q', fontsize=10, va='center', ha='right')
        ax.add_patch(Polygon([(x + .8, 1.4), (x + 1.2, 1.4), (x + 1.0, 1.75)], fc='none', ec=BLUE))
        arrow(ax, (x - 1.4 if k else .5, 2.4), (x, 2.4), color=INK, lw=1.1)
        ax.text(x + 1.0, 3.7, f'$Q_{k}$', ha='center', fontsize=10.5)
        wire(ax, (x + 1.0, 1.4), (x + 1.0, .7))
    ax.text(.3, 2.75, '串行\n输入', fontsize=9, ha='left', va='bottom')
    wire(ax, (3.0, .7), (13.2, .7)); ax.text(14.2, .7, 'CLK', fontsize=10, va='center')
    arrow(ax, (14.0, 2.4), (15.6, 2.4), color=INK, lw=1.1)
    save(fig, P + 'shift_register.png', ticks=False)


for f in [levels, switches, division, twos_wheel, gray, gates, majority, mux, kmaps, full_adder, ripple, hazard, latch_ff, state_diagrams, shift_register]:
    f()

place('08_数字电子技术基础.md', [
    ('逻辑一不等于一伏', P + 'logic_levels.png', '电压范围与逻辑值（示范电平）'),
    ('现在考虑两个开关控制一盏灯', P + 'switches.png', '开关的串联与并联对应与、或'),
    ('十进制整数转二进制时', P + 'division_by_two.png', '除二取余法'),
    ('为了在固定字长中表示负数', P + 'twos_complement_wheel.png', '四位补码的数轮'),
    ('三位自然二进制 \\(B_2B_', P + 'gray_code.png', '自然二进制码与格雷码'),
    ('同一张真值表可以用门图、公式或', P + 'gate_symbols.png', '常用逻辑门符号（国际通用形状）'),
    ('设计一个三输入多数表决器', P + 'majority_voter.png', '三输入多数表决器'),
    ('数据选择器是把', P + 'mux2.png', '二选一数据选择器'),
    ('边界相邻可用具体最小项核对', P + 'karnaugh.png', '三变量与四变量卡诺图的圈组'),
    ('全加器还要接收低位进位', P + 'full_adder.png', '由两个半加器和一个或门组成的全加器'),
    ('逐位串接全加器形成行波进位', P + 'ripple_carry.png', '四位行波进位加法器'),
    ('增加冗余项 \\(BC\\) 得', P + 'hazard.png', '路径延迟造成的毛刺'),
    ('锁存器在使能有效期间', P + 'latch_vs_flipflop.png', '电平敏感的锁存器与边沿触发器的波形比较'),
    ('从输入串 \\(1,0,1,1\\)', P + 'state_diagrams.png', '模四计数器与奇偶检测器的状态图'),
    ('**移位寄存器。**', P + 'shift_register.png', '四位串入移位寄存器'),
])
