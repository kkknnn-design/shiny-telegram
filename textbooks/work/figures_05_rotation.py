# 生成大学物理册第 8–10 节转动部分的静态插图（2026-10-19 增补）。
# 输出到 outputs/教材/figures/，由 build_pdf.py 与 render_books.mjs 按 ![标题](figures/文件名) 引用。
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Circle, FancyArrowPatch, Arc, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/教材/figures'
OUT.mkdir(parents=True, exist_ok=True)
font_manager.fontManager.addfont('C:/Windows/Fonts/simsun.ttc')
plt.rcParams.update({'font.family': ['SimSun'], 'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
                     'font.size': 10, 'savefig.dpi': 300})
ORANGE, PURPLE, GREEN, GRAY, BLUE, RED = '#d9822b', '#7b5ea7', '#3c8d5a', '#6b7280', '#3b6ea8', '#b8433a'


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=0.04, facecolor='white')
    plt.close(fig)


def clean3d(ax, lim=1.15, elev=22, azim=-58):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()


def arrow3d(ax, p, q, color, lw=1.4):
    ax.quiver(*p, *(np.array(q) - np.array(p)), color=color, lw=lw, arrow_length_ratio=0.12)


# 图 8-1：空心圆盘与厚球壳的剖切模型
def fig_ring_shell():
    fig = plt.figure(figsize=(6.4, 3.1))
    R1, R2, r, h = 0.45, 1.0, 0.72, 0.18
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    th = np.linspace(0, 1.5 * np.pi, 80)
    for z in (-h / 2, h / 2):
        rr, tt = np.meshgrid(np.linspace(R1, R2, 2), th)
        ax.plot_surface(rr * np.cos(tt), rr * np.sin(tt), z + 0 * rr, color='#c9d6e3', alpha=.55, lw=0)
    for R in (R1, R2):
        zz, tt = np.meshgrid([-h / 2, h / 2], th)
        ax.plot_surface(R * np.cos(tt), R * np.sin(tt), zz, color='#aebfd0', alpha=.5, lw=0)
    zz, tt = np.meshgrid([-h / 2, h / 2], th)
    ax.plot_surface(r * np.cos(tt), r * np.sin(tt), zz, color=ORANGE, alpha=.9, lw=0)
    ax.plot([0, 0], [0, 0], [-0.75, 0.75], color=GRAY, lw=1.2)
    ax.plot([0, R1], [0, 0], [h / 2] * 2, color='k', lw=.8); ax.plot([0, 0], [0, -R2], [h / 2] * 2, color='k', lw=.8)
    ax.text(R1 / 2, 0.02, h / 2 + .08, '$R_1$'); ax.text(0.05, -R2 / 2, h / 2 + .08, '$R_2$')
    ax.text(r, -.05, h / 2 + .1, '$r$', color=ORANGE)
    clean3d(ax, 1.0, 28, -50); ax.set_title('(a) 空心圆盘：薄圆柱层 $dm=\\sigma\\,2\\pi r\\,dr$', fontsize=9)

    # 切去朝向读者的一半，剖面是一个平面圆环，橙色圆是半径 r 的薄球层的截线
    ax = fig.add_subplot(1, 2, 2)
    ax.set_aspect('equal'); ax.axis('off')
    from matplotlib.patches import Wedge
    ax.add_patch(Circle((0, 0), R2, fc='#dfe7ef', ec='#3d556b', lw=1))
    ax.add_patch(Circle((0, 0), R1, fc='white', ec='#3d556b', lw=1))
    ax.add_patch(Wedge((0, 0), r + .03, 0, 360, width=.06, fc=ORANGE, ec='none'))
    ax.plot([0, 0], [-1.25, 1.25], color=GRAY, lw=1.2)
    ax.plot([0, R1 * .707], [0, -R1 * .707], 'k', lw=.8); ax.text(R1 * .45, -R1 * .3, '$R_1$', fontsize=9)
    ax.plot([0, -R2 * .707], [0, -R2 * .707], 'k', lw=.8); ax.text(-R2 * .6, -R2 * .45, '$R_2$', fontsize=9)
    ax.text(r * .74 + .03, r * .74 + .03, '$r$', color=ORANGE); ax.text(.05, 1.12, '转轴', fontsize=8)
    ax.text(-1.05, 1.0, '阴影：过轴剖面', fontsize=8)
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.3, 1.3)
    ax.set_title('(b) 厚球壳剖面：薄球层 $dm=\\rho\\,4\\pi r^2dr$', fontsize=9)
    save(fig, '05_ring_shell.png')


# 图 8-2：一点到三根坐标轴的距离
def fig_symmetry():
    fig = plt.figure(figsize=(3.4, 3.2)); ax = fig.add_subplot(projection='3d')
    for v, lab in (((1.25, 0, 0), '$x$'), ((0, 1.25, 0), '$y$'), ((0, 0, 1.2), '$z$')):
        arrow3d(ax, (0, 0, 0), v, 'k', 1); ax.text(*(np.array(v) * 1.08), lab)
    x, y, z = .85, .75, .8
    ax.scatter([x], [y], [z], color=RED, s=18); ax.text(x + .05, y + .05, z + .08, '$P$')
    for foot, col in (((x, 0, 0), BLUE), ((0, y, 0), GREEN), ((0, 0, z), ORANGE)):
        ax.plot(*zip(foot, (x, y, z)), color=col, lw=1.8)
    for a, b in (((x, y, 0), (x, 0, 0)), ((x, y, 0), (0, y, 0)), ((x, y, 0), (x, y, z))):
        ax.plot(*zip(a, b), color=GRAY, lw=.6, ls='--')
    ax.set_xlim(0, 1.1); ax.set_ylim(0, 1.1); ax.set_zlim(0, 1.1); ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -55); ax.set_axis_off()
    for k, (txt, col) in enumerate((('到 $x$ 轴：$y^2+z^2$', BLUE), ('到 $y$ 轴：$x^2+z^2$', GREEN), ('到 $z$ 轴：$x^2+y^2$', ORANGE),
                                    ('三者之和 $=2(x^2+y^2+z^2)=2r^2$', 'k'))):
        ax.text2D(.02, .02 - .08 * k, txt, color=col, transform=ax.transAxes, fontsize=9)
    save(fig, '05_symmetry_axes.png')


# 图 8-3：球坐标与体积元
def fig_spherical():
    fig = plt.figure(figsize=(4.4, 4.0)); ax = fig.add_subplot(projection='3d')
    u = np.linspace(0, 2 * np.pi, 60)
    for lat in np.linspace(-60, 60, 5) * np.pi / 180:
        ax.plot(np.cos(lat) * np.cos(u), np.cos(lat) * np.sin(u), np.sin(lat) + 0 * u, color='#c3ccd6', lw=.5)
    for lon in np.linspace(0, np.pi, 6, endpoint=False):
        ax.plot(np.sin(u) * np.cos(lon), np.sin(u) * np.sin(lon), np.cos(u), color='#c3ccd6', lw=.5)
    for v, lab in (((1.35, 0, 0), '$x$'), ((0, 1.35, 0), '$y$'), ((0, 0, 1.4), '$z$（转轴）')):
        arrow3d(ax, (0, 0, 0), v, 'k', .9); ax.text(*(np.array(v) * 1.05), lab, fontsize=9)
    r, th, ph = 1.0, np.radians(58), np.radians(25)
    sph = lambda r, t, p: np.array([r * np.sin(t) * np.cos(p), r * np.sin(t) * np.sin(p), r * np.cos(t)])
    P = sph(r, th, ph)
    ax.plot(*zip((0, 0, 0), P), color=RED, lw=1.5); ax.text(*(P * .5 + [0, -.08, .05]), '$r$', color=RED)
    ax.scatter(*P, color=RED, s=14); ax.text(*(P + [.06, 0, -.2]), '$P$')
    tt = np.linspace(0, th, 30); ax.plot(*np.array([sph(.35, a, ph) for a in tt]).T, color=PURPLE, lw=1.2)
    ax.text(*sph(.42, th / 2, ph), '$\\theta$', color=PURPLE)
    pp = np.linspace(0, ph, 30); ax.plot(.35 * np.cos(pp), .35 * np.sin(pp), 0 * pp, color=GREEN, lw=1.2)
    ax.text(.45 * np.cos(ph / 2), .45 * np.sin(ph / 2), -.06, '$\\varphi$', color=GREEN)
    foot = np.array([0, 0, P[2]]); ax.plot(*zip(foot, P), color=ORANGE, lw=1.6)
    ax.text(*((foot + P) / 2 + [0, 0, .06]), '$r\\sin\\theta$', color=ORANGE, fontsize=9)
    ax.plot(*zip(P, [P[0], P[1], 0]), color=GRAY, lw=.6, ls='--'); ax.plot(*zip((0, 0, 0), [P[0], P[1], 0]), color=GRAY, lw=.6, ls='--')
    hh = np.linspace(0, 2 * np.pi, 60); rs = r * np.sin(th)
    ax.plot(rs * np.cos(hh), rs * np.sin(hh), P[2] + 0 * hh, color=GREEN, lw=.7, ls=':')
    dr, dt, dp = .34, np.radians(20), np.radians(28)
    for a, b, col in ((sph(r, th, ph), sph(r + dr, th, ph), GRAY), (sph(r, th, ph), sph(r, th + dt, ph), PURPLE), (sph(r, th, ph), sph(r, th, ph + dp), GREEN)):
        ax.plot(*zip(a, b), color=col, lw=2.6)
    corners = [sph(r + i * dr, th + j * dt, ph + k * dp) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    for i, a in enumerate(corners):
        for j, b in enumerate(corners):
            if j > i and bin(i ^ j).count('1') == 1:
                ax.plot(*zip(a, b), color='#d2689a', lw=.8)
    ax.text2D(.0, .04, '体积元三边：灰 $dr$　紫 $r\\,d\\theta$　绿 $r\\sin\\theta\\,d\\varphi$', transform=ax.transAxes, fontsize=9)
    clean3d(ax, 1.05, 18, -25)
    save(fig, '05_spherical_element.png')


# 图 8-4：实心球沿转轴切成薄圆盘
def fig_disk_slices():
    fig = plt.figure(figsize=(3.4, 3.2)); ax = fig.add_subplot(projection='3d')
    u = np.linspace(0, 2 * np.pi, 60)
    for lat in np.linspace(-75, 75, 7) * np.pi / 180:
        ax.plot(np.cos(lat) * np.cos(u), np.cos(lat) * np.sin(u), np.sin(lat) + 0 * u, color='#c3ccd6', lw=.5)
    for lon in np.linspace(0, np.pi, 6, endpoint=False):
        ax.plot(np.sin(u) * np.cos(lon), np.sin(u) * np.sin(lon), np.cos(u), color='#c3ccd6', lw=.5)
    z = .5; a = np.sqrt(1 - z * z)
    rr, tt = np.meshgrid(np.linspace(0, a, 2), u)
    for dz in (0, .06):
        ax.plot_surface(rr * np.cos(tt), rr * np.sin(tt), z + dz + 0 * rr, color=ORANGE, alpha=.3, lw=0)
    ax.plot([0, 0], [0, 0], [-1.3, 1.3], color='k', lw=1)
    ax.plot([0, 0], [0, 0], [0, z], color=BLUE, lw=1.8); ax.text(.04, .04, z / 2, '$z$', color=BLUE)
    ax.plot([0, a], [0, 0], [z + .07] * 2, color=GREEN, lw=2.2); ax.text(a / 2, 0, z + .2, '$a$', color=GREEN, fontsize=11)
    ax.plot([0, a], [0, 0], [0, z], color=RED, lw=1.5); ax.text(a / 2 + .05, 0, z / 2 - .08, '$R$', color=RED)
    ax.text(a + .08, 0, z + .03, '厚 $dz$', fontsize=9)
    clean3d(ax, 1.0, 16, -60); ax.set_title('$a^2=R^2-z^2$，薄片按圆盘 $\\frac{1}{2}dm\\,a^2$', fontsize=9)
    save(fig, '05_disk_slices.png')


def arrow(ax, p, q, color, lab=None, off=(0, 0), lw=1.6, fs=10):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=11, color=color, lw=lw))
    if lab:
        ax.text(q[0] + off[0], q[1] + off[1], lab, color=color, fontsize=fs)


# 图 10-1：斜面纯滚动的受力与速度
def fig_incline():
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.8))
    al = np.radians(28); R = .55
    for k, ax in enumerate(axs):
        ax.set_aspect('equal'); ax.axis('off')
        L = 4.2
        ax.add_patch(Polygon([(0, 0), (L, 0), (0, L * np.tan(al))], closed=True, fc='#e8edf2', ec='#7d8b98'))
        ax.add_patch(Arc((L, 0), 1.1, 1.1, theta1=180 - np.degrees(al), theta2=180, color='k', lw=.8))
        ax.text(L - .85, .1, '$\\theta$')
        s = 1.7; t = np.array([np.cos(al), -np.sin(al)]); n = np.array([np.sin(al), np.cos(al)])
        Pc = np.array([0, L * np.tan(al)]) + s * t; C = Pc + R * n
        ax.add_patch(Circle(C, R, fc='#c9d6e3', ec='#3d556b', lw=1))
        ax.plot(*C, 'k.', ms=3)
        if k == 0:
            arrow(ax, C, C + [0, -1.15], BLUE, '$mg$', (.06, 0))
            arrow(ax, Pc, Pc + 1.25 * n, GREEN, '$N$', (.05, 0))
            arrow(ax, Pc, Pc - .85 * t, RED, '$f$', (-.25, .08))
            ax.plot(*Pc, 'o', color=RED, ms=3.5); ax.text(*(Pc + [.08, -.32]), '$P$')
            ax.set_title('(a) 受力：静摩擦沿斜面向上', fontsize=9)
        else:
            top = C + R * n
            arrow(ax, C, C + .8 * t, BLUE, '$v$', (0, .1))
            arrow(ax, top, top + 1.6 * t, PURPLE, '$2v$', (0, .1))
            ax.plot(*Pc, 'o', color=RED, ms=4); ax.text(*(Pc + [.12, -.38]), '$v_P=v-\\omega R=0$', color=RED, fontsize=9)
            ax.add_patch(Arc(C, .55, .55, theta1=110, theta2=330, color=ORANGE, lw=1.2))
            ax.text(*(C + [-.48, .25]), '$\\omega$', color=ORANGE)
            ax.set_title('(b) 速度：接触点瞬时静止', fontsize=9)
        ax.set_xlim(-.2, L + .2); ax.set_ylim(-.5, L * np.tan(al) + .4)
    save(fig, '05_incline_rolling.png')


# 图 9-3：圆柱缠绳挂重物
def fig_cylinder_weight():
    fig, ax = plt.subplots(figsize=(3.0, 3.2)); ax.set_aspect('equal'); ax.axis('off')
    R = 1.0
    ax.add_patch(Circle((0, 0), R, fc='#c9d6e3', ec='#3d556b', lw=1.2)); ax.plot(0, 0, 'ko', ms=3); ax.text(-.25, -.2, '$O$')
    ax.plot([-1.4, -.6], [1.35, 1.35], color='k', lw=1.5); ax.plot([-1, 0], [1.35, 0], color='#7d8b98', lw=1)
    ax.plot([R, R], [0, -2.0], color='k', lw=1.1)
    ax.add_patch(Rectangle((R - .3, -2.6), .6, .6, fc='#e2c49b', ec='#8a6a3f')); ax.text(R - .1, -2.38, '$m$')
    ax.plot([0, R], [0, 0], color=RED, lw=1.6); ax.text(.42, .07, '$R$', color=RED)
    arrow(ax, (R, -.02), (R, -.62), PURPLE, '$T$', (.08, .1))
    arrow(ax, (R, -2.0), (R, -1.45), PURPLE, '$T$', (.08, -.2))
    arrow(ax, (R, -2.6), (R, -3.3), BLUE, '$mg$', (.08, .1))
    # 重物在右侧下落，圆柱顺时针转
    ax.add_patch(FancyArrowPatch((-.45, .3), (.45, .3), connectionstyle='arc3,rad=-.5', arrowstyle='-|>',
                                 mutation_scale=10, color=ORANGE, lw=1.3))
    ax.text(-.08, .62, '$\\omega$', color=ORANGE)
    ax.text(-1.45, -1.2, '$M,\\ I=\\frac{1}{2}MR^2$', fontsize=9)
    ax.set_xlim(-1.6, 1.8); ax.set_ylim(-3.45, 1.5)
    save(fig, '05_cylinder_weight.png')


def sierpinski(ax, A, B, C, n, colors_=None):
    if n == 0:
        ax.add_patch(Polygon([A, B, C], closed=True, fc=colors_ or '#3d556b', ec='none')); return
    AB, BC, CA = (A + B) / 2, (B + C) / 2, (C + A) / 2
    sierpinski(ax, A, AB, CA, n - 1, colors_); sierpinski(ax, AB, B, BC, n - 1, colors_); sierpinski(ax, CA, BC, C, n - 1, colors_)


# 图 9-2：谢尔宾斯基三角形
def fig_sierpinski():
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.6), gridspec_kw={'width_ratios': [1, 1, 1.05], 'wspace': .45})
    a = 1.0; h = np.sqrt(3) / 2
    A, B, C = np.array([-.5, 0]), np.array([.5, 0]), np.array([0, h])
    ax = axs[0]
    for k in range(4):
        dx = (k % 2) * 1.15; dy = -(k // 2) * 1.05
        sierpinski(ax, A * .5 + [dx, dy], B * .5 + [dx, dy], C * .5 + [dx, dy], k)
        ax.text(dx - .05, dy - .14, f'$n={k}$', fontsize=8)
    ax.set_title('(a) 逐次挖去中间', fontsize=9)
    ax = axs[1]
    for P, Q, R_, col in ((C, (A + C) / 2, (B + C) / 2, GREEN), (A, (A + B) / 2, (A + C) / 2, PURPLE), ((A + B) / 2, B, (B + C) / 2, ORANGE)):
        P, Q, R_ = np.array(P), np.array(Q), np.array(R_)
        order = sorted([P, Q, R_], key=lambda v: (v[1], v[0]))
        sierpinski(ax, order[0], order[1], order[2], 3, col)
    ax.plot([0, 0], [-.12, h + .1], color='k', ls='--', lw=1)
    ax.plot([-.25, -.25], [-.02, h / 2], color=PURPLE, ls=':', lw=1); ax.plot([.25, .25], [-.02, h / 2], color=ORANGE, ls=':', lw=1)
    ax.annotate('', (-.25, -.08), (0, -.08), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(-.18, -.2, '$a/4$', fontsize=8)
    ax.set_title('(b) 三个缩小一半的自身', fontsize=9)
    ax = axs[2]
    n = np.arange(0, 8); c = 1 / 18 - (1 / 72) * 0.25 ** n
    ax.axis('on'); ax.plot(n, c, 'o-', color=BLUE, ms=3.5, lw=1); ax.axhline(1 / 18, color=RED, lw=.9, ls='--')
    ax.text(3.2, 1 / 18 + .0006, '$c_\\infty=1/18$', color=RED, fontsize=9)
    ax.set_xlabel('挖空次数 $n$', fontsize=8); ax.set_ylabel('$c_n$', fontsize=9)
    ax.tick_params(labelsize=7); ax.set_ylim(.04, .058); ax.set_title('(c) 系数收敛', fontsize=9)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for ax in axs[:2]:
        ax.set_aspect('equal'); ax.axis('off')
    axs[0].set_xlim(-.35, 1.45); axs[0].set_ylim(-1.2, .5); axs[1].set_xlim(-.55, .55); axs[1].set_ylim(-.25, h + .12)
    save(fig, '05_sierpinski_triangle.png')


def carpet(ax, x, y, s, n, col):
    if n == 0:
        ax.add_patch(Rectangle((x, y), s, s, fc=col, ec='none')); return
    t = s / 3
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            carpet(ax, x + i * t, y + j * t, t, n - 1, col)


# 图 9-3：谢尔宾斯基地毯
def fig_carpet():
    fig, ax = plt.subplots(figsize=(3.2, 3.0)); ax.set_aspect('equal'); ax.axis('off')
    t = 1 / 3
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            col = GREEN if (i == 1 or j == 1) else ORANGE
            carpet(ax, -.5 + i * t, -.5 + j * t, t, 2, col)
    ax.plot([-.68, .68], [0, 0], color='k', ls='--', lw=1); ax.text(.6, .04, '轴 1', fontsize=8)
    ax.plot(0, 0, 'o', mfc='white', mec='k', ms=7); ax.plot(0, 0, 'k.', ms=3); ax.text(.04, -.1, '轴 2（垂直纸面）', fontsize=8)
    ax.text(-.5, -.66, '绿：边块 $d^2=a^2/9$　橙：角块 $d^2=2a^2/9$', fontsize=8)
    ax.set_xlim(-.72, .72); ax.set_ylim(-.72, .58)
    save(fig, '05_sierpinski_carpet.png')


# 图 9-1：垂直轴定理与平面图形的对称
def fig_perpendicular():
    fig = plt.figure(figsize=(6.4, 2.9))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    xx, yy = np.meshgrid([-.3, 1.4], [-.3, 1.1])
    ax.plot_surface(xx, yy, 0 * xx, color='#c9d6e3', alpha=.5, lw=0)
    for v, lab in (((1.6, 0, 0), '$x$'), ((0, 1.3, 0), '$y$'), ((0, 0, 1.1), '$z$')):
        arrow3d(ax, (0, 0, 0), v, 'k', .9); ax.text(*(np.array(v) * 1.07), lab)
    P = np.array([1.1, .8, 0]); ax.scatter(*P, color=RED, s=14); ax.text(*(P + [.05, .05, .05]), '$P(x,y,0)$', fontsize=8)
    ax.plot(*zip(P, (P[0], 0, 0)), color=BLUE, lw=1.6); ax.text(P[0] + .1, P[1] / 2, 0, '$|y|$', color=BLUE, fontsize=9)
    ax.plot(*zip(P, (0, P[1], 0)), color=GREEN, lw=1.6); ax.text(P[0] / 2, P[1] + .12, 0, '$|x|$', color=GREEN, fontsize=9)
    ax.plot(*zip(P, (0, 0, 0)), color=ORANGE, lw=1.6); ax.text(P[0] / 2 + .1, P[1] / 2 - .32, 0, '$\\sqrt{x^2+y^2}$', color=ORANGE, fontsize=9)
    ax.set_xlim(-.3, 1.5); ax.set_ylim(-.3, 1.5); ax.set_zlim(-.3, 1.2); ax.set_box_aspect((1, 1, .8))
    ax.view_init(32, -60); ax.set_axis_off(); ax.set_title('(a) 薄板：$I_z=I_x+I_y$', fontsize=9)
    ax = fig.add_subplot(1, 2, 2)
    th = np.linspace(0, 360, 400); A, Rw, ph = 1.0, .35, 50
    ax.plot(th, A + Rw * np.cos(np.radians(2 * th - ph)), color=PURPLE, lw=1.2, label='$A+R\\cos(2\\theta-\\phi)$')
    ax.axhline(A, color=GREEN, lw=1.2, label='$R=0$ 时为常数')
    t0 = ph / 2
    for k, mk in zip(range(3), ('o', 's', '^')):
        tk = t0 + 120 * k
        ax.plot(tk, A + Rw * np.cos(np.radians(2 * tk - ph)), mk, color=RED, ms=5)
    ax.text(t0 + 4, A + Rw + .03, '$\\theta_0$', fontsize=8); ax.text(t0 + 100, A - Rw / 2 - .13, '$\\theta_0+120^\\circ$', fontsize=8)
    ax.set_xticks([0, 90, 180, 270, 360]); ax.tick_params(labelsize=7); ax.set_xlabel('轴与 $x$ 轴夹角 $\\theta$/(°)', fontsize=8)
    ax.set_ylabel('$I(\\theta)$', fontsize=9); ax.legend(fontsize=7, frameon=False, loc='upper center', bbox_to_anchor=(.5, -.22), ncol=2)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_title('(b) 转 $120^\\circ$ 重合迫使波幅为零', fontsize=9)
    save(fig, '05_perpendicular_axis.png')


if __name__ == '__main__':
    for f in (fig_ring_shell, fig_symmetry, fig_spherical, fig_disk_slices, fig_perpendicular, fig_sierpinski,
              fig_carpet, fig_cylinder_weight, fig_incline):
        f(); print('ok', f.__name__)
