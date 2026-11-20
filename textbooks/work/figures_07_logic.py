# 逻辑学册插图（2026-11-20）。运行：py work/figures_07_logic.py
from figlib import *
from matplotlib.patches import Circle, Ellipse, Rectangle

style()
P = '07_'
T, F = LIGHT['green'], LIGHT['red']


def truth_grid():
    fig, ax = canvas(6.4, 2.3, (0, 13), (0, 4.6))
    rows = [(1, 1), (1, 0), (0, 1), (0, 0)]
    ops = [('$p\\wedge q$', lambda p, q: p and q), ('$p\\vee q$', lambda p, q: p or q), ('$p\\to q$', lambda p, q: (not p) or q), ('$p\\leftrightarrow q$', lambda p, q: p == q), ('$p\\oplus q$', lambda p, q: p != q)]
    for j, h in enumerate(['$p$', '$q$']):
        ax.text(.6 + j * 1.0, 4.2, h, ha='center', fontsize=11)
    for i, (p, q) in enumerate(rows):
        y = 3.3 - i * .85
        for j, v in enumerate((p, q)):
            box(ax, .2 + j, y, .8, .7, str(v), LIGHT['gray'], GRAY, fs=11, r=.03)
        for k, (h, f) in enumerate(ops):
            v = int(f(p, q)); box(ax, 2.6 + k * 2.1, y, 1.8, .7, str(v), T if v else F, GREEN if v else RED, fs=11, r=.03)
    for k, (h, f) in enumerate(ops):
        ax.text(3.5 + k * 2.1, 4.2, h, ha='center', fontsize=11)
    save(fig, P + 'truth_tables.png', ticks=False)


def euler(ax, outer, inner, lo='$Q$', li='$P$', co=BLUE, ci=ORANGE):
    ax.add_patch(Ellipse(*outer, fc=LIGHT['blue'], ec=co, lw=1.2)); ax.add_patch(Ellipse(*inner, fc=LIGHT['orange'], ec=ci, lw=1.2))
    ax.text(outer[0][0] + outer[1] * .2, outer[0][1] + outer[2] * .28, lo, color=co, fontsize=10, ha='center')
    ax.text(*inner[0], li, color=ci, fontsize=10, ha='center', va='center')


def sufficient():
    fig, ax = canvas(4.4, 2.7, (0, 8), (-.7, 4.4))
    euler(ax, ((3.6, 2.2), 6.4, 4.0), ((2.6, 2.0), 2.4, 1.6), '$q$ 成立的情形', '$p$ 成立的情形')
    ax.text(4.0, -.45, '$p\\to q$：$p$ 是 $q$ 的充分条件，$q$ 是 $p$ 的必要条件', ha='center', fontsize=10)
    save(fig, P + 'sufficient_necessary.png', ticks=False)


def consequence():
    fig, ax = canvas(4.6, 2.6, (0, 8), (0, 4.6))
    ax.add_patch(Rectangle((.1, .5), 7.8, 4.0, fc='white', ec=GRAY)); ax.text(7.7, .65, '全部赋值', ha='right', fontsize=9.5, color=GRAY)
    euler(ax, ((4.4, 2.6), 6.0, 3.2), ((3.4, 2.5), 2.6, 1.6), '使 $A$ 为真的赋值', '使 $\\Gamma$ 全真\n的赋值')
    ax.text(4, .1, '$\\Gamma\\models A$：凡使前提全真的赋值都使结论为真', ha='center', fontsize=10)
    save(fig, P + 'consequence.png', ticks=False)


def demorgan():
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.0))
    x = np.linspace(-2, 2, 400); X, Y = np.meshgrid(x, np.linspace(-1.3, 1.3, 300))
    A = (X + .5) ** 2 + Y ** 2 < 1; B = (X - .5) ** 2 + Y ** 2 < 1
    for ax, reg, t in [(axs[0], ~(A & B), '$\\neg(A\\wedge B)$'), (axs[1], ~A, '$\\neg A$'), (axs[2], ~B, '$\\neg B$')]:
        ax.set_xlim(-2, 2); ax.set_ylim(-1.35, 1.35); ax.set_aspect('equal'); ax.axis('off')
        ax.contourf(X, Y, reg.astype(float), levels=[.5, 1.5], colors=[BLUE], alpha=.3)
        ax.add_patch(Rectangle((-1.95, -1.3), 3.9, 2.6, fc='none', ec=GRAY))
        for cx in (-.5, .5):
            ax.add_patch(Circle((cx, 0), 1, fc='none', ec=INK))
        ax.text(-1.2, .75, '$A$'); ax.text(1.0, .75, '$B$'); ax.set_title(t, fontsize=11)
    fig.text(.5, -.02, '左图阴影 = 中图阴影与右图阴影的并：$\\neg(A\\wedge B)\\equiv\\neg A\\vee\\neg B$', ha='center', fontsize=10)
    fig.tight_layout(); save(fig, P + 'de_morgan.png', ticks=False)


def normal_forms():
    fig, ax = canvas(6.2, 2.6, (0, 13), (0, 5.2))
    rows = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    for j, h in enumerate(['$a$', '$b$', '$a\\oplus b$']):
        ax.text(.6 + j * 1.1, 4.7, h, ha='center', fontsize=11)
    for i, (a, b, v) in enumerate(rows):
        y = 3.8 - i * .9
        for j, c in enumerate((a, b)):
            box(ax, .2 + j * 1.1, y, .9, .7, str(c), LIGHT['gray'], GRAY, r=.03)
        box(ax, 2.4, y, .9, .7, str(v), T if v else F, GREEN if v else RED, r=.03)
        term = ('$\\neg a\\wedge b$' if (a, b) == (0, 1) else '$a\\wedge\\neg b$') if v else ('$a\\vee b$' if (a, b) == (0, 0) else '$\\neg a\\vee\\neg b$')
        arrow(ax, (3.5, y + .35), (5.0, y + .35), color=GREEN if v else RED, lw=1)
        ax.text(5.15, y + .35, ('极小项 ' if v else '极大项 ') + term, va='center', fontsize=10.5, color=GREEN if v else RED)
    ax.text(8.6, 3.3, '完全析取范式（取 1 行）：\n$(\\neg a\\wedge b)\\vee(a\\wedge\\neg b)$', fontsize=10.5, color=GREEN, va='center')
    ax.text(8.6, 1.4, '完全合取范式（取 0 行）：\n$(a\\vee b)\\wedge(\\neg a\\vee\\neg b)$', fontsize=10.5, color=RED, va='center')
    save(fig, P + 'normal_forms.png', ticks=False)


def nand():
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 1.9))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
    ax = axs[0]; ax.set_xlim(-.6, 3.6); ax.set_ylim(-1.1, 1.1)
    ins, out = gate(ax, 'nand', .6, 0, .8)
    wire(ax, (-.2, 0), (.3, 0)); wire(ax, (.3, 0), (.3, ins[0][1]), ins[0]); wire(ax, (.3, 0), (.3, ins[1][1]), ins[1]); ax.plot(.3, 0, 'o', color=INK, ms=3)
    wire(ax, out, (3.0, 0)); ax.text(-.5, 0, '$A$', va='center'); ax.text(3.05, 0, '$\\neg A$', va='center'); ax.set_title('非：$A\\uparrow A$', fontsize=10)
    ax = axs[1]; ax.set_xlim(-.6, 5.6); ax.set_ylim(-1.1, 1.1)
    ins, out = gate(ax, 'nand', 0, 0, .8); ax.text(-.4, ins[0][1], '$A$', va='center'); ax.text(-.4, ins[1][1], '$B$', va='center')
    i2, o2 = gate(ax, 'nand', 2.6, 0, .8); wire(ax, out, (2.3, 0)); wire(ax, (2.3, 0), (2.3, i2[0][1]), i2[0]); wire(ax, (2.3, 0), (2.3, i2[1][1]), i2[1])
    wire(ax, o2, (4.9, 0)); ax.text(4.95, 0, '$A\\wedge B$', va='center'); ax.set_title('与：$(A\\uparrow B)\\uparrow(A\\uparrow B)$', fontsize=10)
    ax = axs[2]; ax.set_xlim(-.9, 5.4); ax.set_ylim(-1.5, 1.5)
    a1, o1 = gate(ax, 'nand', 0, .75, .7); b1, p1 = gate(ax, 'nand', 0, -.75, .7)
    for (g, y, lab) in [(a1, .75, '$A$'), (b1, -.75, '$B$')]:
        wire(ax, (-.4, y), (-.2, y)); wire(ax, (-.2, y), (-.2, g[0][1]), g[0]); wire(ax, (-.2, y), (-.2, g[1][1]), g[1]); ax.text(-.8, y, lab, va='center')
    c, o3 = gate(ax, 'nand', 2.4, 0, .7); wire(ax, o1, (2.0, o1[1]), (2.0, c[0][1]), c[0]); wire(ax, p1, (2.0, p1[1]), (2.0, c[1][1]), c[1])
    wire(ax, o3, (4.5, 0)); ax.text(4.55, 0, '$A\\vee B$', va='center'); ax.set_title('或：$(A\\uparrow A)\\uparrow(B\\uparrow B)$', fontsize=10)
    fig.tight_layout(); save(fig, P + 'nand_complete.png', ticks=False)


def fitch():
    fig, ax = canvas(5.8, 2.8, (0, 12), (0, 5.6))
    lines = ['$p\\to q$', '$q\\to r$', '$p$', '$q$', '$r$', '$p\\to r$']
    why = ['前提', '前提', '假设（开启子推导）', '1、3 蕴含消去', '2、4 蕴含消去', '3–5 蕴含引入（解除假设）']
    for i, (l, w) in enumerate(zip(lines, why)):
        y = 5.0 - i * .8; x = 1.6 if 2 <= i <= 4 else 1.0
        ax.text(.3, y, f'{i + 1}', fontsize=10.5, color=GRAY, va='center'); ax.text(x, y, l, fontsize=11.5, va='center'); ax.text(6.9, y, w, fontsize=10, va='center', color=GRAY)
    ax.plot([.8, .8], [5.35, .55], color=INK, lw=1.2); ax.plot([.8, 2.6], [4.62, 4.62], color=INK, lw=1)
    ax.add_patch(Rectangle((1.35, 1.7), 3.4, 1.95, fc=LIGHT['orange'], ec=ORANGE, lw=1.1, alpha=.6))
    ax.plot([1.45, 2.4], [3.02, 3.02], color=ORANGE, lw=1)
    ax.text(4.85, 2.65, '子推导', fontsize=9.5, color=ORANGE, va='center')
    save(fig, P + 'natural_deduction.png', ticks=False)


def resolution():
    fig, ax = canvas(5.6, 2.9, (0, 11), (0, 5.8))
    def node(x, y, t, c=BLUE):
        box(ax, x - .9, y - .3, 1.8, .6, t, LIGHT['blue'] if c == BLUE else LIGHT['red'], c, fs=10.5, r=.08)
    node(1.2, 5.0, '$p$'); node(3.6, 5.0, '$\\neg p\\vee q$'); node(6.0, 3.6, '$\\neg q\\vee r$'); node(8.4, 2.2, '$\\neg r$')
    node(2.4, 3.6, '$q$'); node(4.8, 2.2, '$r$'); node(6.6, .8, '□', RED)
    for a, b in [((1.2, 4.7), (2.3, 3.9)), ((3.6, 4.7), (2.5, 3.9)), ((2.4, 3.3), (4.7, 2.5)), ((6.0, 3.3), (4.9, 2.5)), ((4.8, 1.9), (6.5, 1.1)), ((8.4, 1.9), (6.7, 1.1))]:
        arrow(ax, a, b, color=GRAY, lw=1)
    ax.text(8.9, .8, '空子句：矛盾', fontsize=10, color=RED, va='center')
    ax.text(.1, .2, '前提子句 + 目标的否定（$p$、$\\neg r$）', fontsize=9.5, color=GRAY)
    save(fig, P + 'resolution_tree.png', ticks=False)


def quantifier_order():
    fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.4))
    xs = [-1, 0, 1, 2]
    for ax, mode, t in [(axs[0], 'each', '$\\forall x\\,\\exists y\\,(y=x+1)$：真\n每个 $x$ 各有自己的 $y$'), (axs[1], 'one', '$\\exists y\\,\\forall x\\,(y=x+1)$：假\n要一个 $y$ 对所有 $x$ 都成立')]:
        ax.set_xlim(-.5, 3.5); ax.set_ylim(-2.7, 3.3); ax.axis('off')
        for i, x in enumerate(xs):
            box(ax, 0, 2.2 - i * 1.1, .9, .7, f'${x}$', LIGHT['blue'], BLUE, fs=10.5)
            if mode == 'each':
                box(ax, 2.4, 2.2 - i * 1.1, .9, .7, f'${x + 1}$', LIGHT['orange'], ORANGE, fs=10.5)
                arrow(ax, (.95, 2.55 - i * 1.1), (2.35, 2.55 - i * 1.1), color=GREEN)
            else:
                arrow(ax, (.95, 2.55 - i * 1.1), (2.35, .9), color=GREEN if i == 1 else RED, ls='-' if i == 1 else '--')
        if mode == 'one':
            box(ax, 2.4, .55, .9, .7, '$1$', LIGHT['orange'], ORANGE, fs=10.5); ax.text(2.85, -.25, '只对 $x=0$\n成立', ha='center', fontsize=9, color=RED)
        ax.text(1.6, -2.65, t, ha='center', va='bottom', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'quantifier_order.png', ticks=False)


def syllogism():
    fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.4))
    ax = axs[0]; ax.set_xlim(0, 6); ax.set_ylim(0, 4); ax.set_aspect('equal'); ax.axis('off')
    for (c, w, h, col, lab, ly) in [((3, 2), 5.6, 3.6, BLUE, '$C$', 3.45), ((2.6, 2), 3.8, 2.6, GREEN, '$B$', 2.95), ((2.2, 2), 1.8, 1.4, ORANGE, '$A$', 2.0)]:
        ax.add_patch(Ellipse(c, w, h, fc='none', ec=col, lw=1.4)); ax.text(c[0], ly, lab, color=col, fontsize=12, va='center', ha='center')
    ax.set_title('所有 $A$ 是 $B$，所有 $B$ 是 $C$\n$\\Rightarrow$ 所有 $A$ 是 $C$', fontsize=10)
    ax = axs[1]; ax.set_xlim(0, 6); ax.set_ylim(0, 4); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Ellipse((3.6, 2), 3.6, 2.8, fc='none', ec=GREEN, lw=1.4)); ax.text(4.6, 2, '$B$', color=GREEN, fontsize=12)
    ax.add_patch(Ellipse((3.0, 2), 1.2, .9, fc='none', ec=ORANGE, lw=1.4, ls='--')); ax.text(3.0, 2, '$A=\\emptyset$?', color=ORANGE, fontsize=10, ha='center', va='center')
    ax.set_title('“所有 $A$ 是 $B$”在 $A$ 为空时也真，\n推不出“有些 $A$ 是 $B$”', fontsize=10)
    fig.tight_layout(); save(fig, P + 'syllogism.png', ticks=False)


def short_circuit():
    fig, ax = canvas(5.4, 2.4, (0, 11), (0, 4.8))
    box(ax, .2, 1.9, 2.4, 1.0, '求 $a$', LIGHT['blue'], BLUE)
    box(ax, 4.0, 1.9, 2.4, 1.0, '求 $b$', LIGHT['blue'], BLUE)
    box(ax, 8.0, 3.2, 2.6, .9, '结果 1', T, GREEN); box(ax, 8.0, .6, 2.6, .9, '结果 0', F, RED)
    arrow(ax, (2.6, 2.4), (4.0, 2.4), color=GREEN, text='真', toff=(0, .25))
    arrow(ax, (6.4, 2.6), (8.0, 3.6), color=GREEN, text='真', toff=(0, .3)); arrow(ax, (6.4, 2.2), (8.0, 1.1), color=RED, text='假', toff=(.1, -.3))
    arrow(ax, (1.4, 1.9), (1.4, 1.05), color=RED); arrow(ax, (1.4, 1.05), (8.0, 1.05), color=RED, text='假：不再求 $b$', toff=(-1.6, -.3))
    ax.text(5.5, 4.55, 'C 语言 a && b 的短路求值', ha='center', fontsize=10.5)
    save(fig, P + 'short_circuit.png', ticks=False)


for f in [truth_grid, sufficient, consequence, demorgan, normal_forms, nand, fitch, resolution, quantifier_order, syllogism, short_circuit]:
    f()

place('07_逻辑学.md', [
    ('蕴含 \\(p\\to q\\) 只', P + 'truth_tables.png', '五种二元联结词的真值表（绿为真，红为假）'),
    ('**讲解例：充分条件与必要条件', P + 'sufficient_necessary.png', '充分条件与必要条件的集合图'),
    ('写 \\(\\Gamma\\mode', P + 'consequence.png', '逻辑后承：前提的模型包含在结论的模型之中'),
    ('德摩根律的作用是把', P + 'de_morgan.png', '德摩根律的文氏图验证'),
    ('完全析取范式中，每个合取项包含', P + 'normal_forms.png', '由真值表读出异或的两种完全范式'),
    ('与非 \\(A\\uparrow', P + 'nand_complete.png', '只用与非门实现非、与、或'),
    ('第六行的结论不再以', P + 'natural_deduction.png', '自然演绎中假设的作用域'),
    ('**归结例：证明传递推理。**', P + 'resolution_tree.png', '归结反驳：推出空子句'),
    ('**讲解例：量词次序。**', P + 'quantifier_order.png', '量词次序不同，含义不同'),
    ('传统三段论中的', P + 'syllogism.png', '三段论的集合图与存在条件'),
    ('短路求值', P + 'short_circuit.png', '逻辑与的短路求值'),
])
