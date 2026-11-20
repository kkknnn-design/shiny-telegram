# 解析几何册插图（2026-11-20）。运行：py work/figures_03_geometry.py
from figlib import *
from matplotlib.patches import Polygon, Ellipse, Arc

style()
P = '03_'


def vec(ax, p, q, color, label=None, off=(.08, .08), lw=1.8, fs=12):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=13, shrinkA=0, shrinkB=0))
    if label:
        ax.text(q[0] + off[0], q[1] + off[1], label, color=color, fontsize=fs)


def flat(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')


def dot(ax, p, label, off=(.1, .1), color=INK, fs=12):
    ax.plot(*p, 'o', color=color, ms=4.5)
    ax.text(p[0] + off[0], p[1] + off[1], label, color=color, fontsize=fs)


def a3(fig, pos, elev=22, azim=-55, lim=None):
    ax = fig.add_subplot(*pos, projection='3d')
    ax.view_init(elev, azim); ax.set_axis_off()
    if lim:
        ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_zlim(*lim[2])
    return ax


def q3(ax, p, d, color, label=None, off=(0, 0, .08), lw=1.6, fs=11):
    ax.quiver(*p, *d, color=color, arrow_length_ratio=.12, lw=lw)
    if label:
        e = np.array(p) + np.array(d) + np.array(off)
        ax.text(*e, label, color=color, fontsize=fs)


def section():
    fig, ax = plt.subplots(figsize=(4.6, 2.2)); flat(ax, (-.3, 6.4), (-.4, 2.6))
    A, B = np.array([0.5, .3]), np.array([5.5, 2.2]); lam = 1.5
    M = (A + lam * B) / (1 + lam)
    ax.plot(*zip(A, B), color=GRAY, lw=1.2)
    dot(ax, A, '$A$', (-.3, .1)); dot(ax, B, '$B$', (.1, -.1)); dot(ax, M, '$M$', (-.1, .2), RED)
    ax.text(*(A + M) / 2 + [0, -.4], '$\\lambda$ 份', ha='center', color=BLUE); ax.text(*(M + B) / 2 + [0, -.4], '$1$ 份', ha='center', color=ORANGE)
    ax.text(3.2, 2.3, '$M=\\dfrac{A+\\lambda B}{1+\\lambda}$，$\\lambda=1$ 时为中点', ha='center', fontsize=11)
    save(fig, P + 'section_point.png', ticks=False)


def param():
    fig = plt.figure(figsize=(6.2, 2.8))
    ax = fig.add_subplot(1, 2, 1); flat(ax, (-.3, 5), (-.3, 3.3))
    r0, s = np.array([1, .8]), np.array([1.2, .6])
    ax.plot(*zip(r0 - 0.7 * s, r0 + 2.6 * s), color=BLUE, lw=1.3)
    vec(ax, (0, 0), r0, GRAY, '$r_0$', (-.4, .05)); vec(ax, r0, r0 + s, RED, '$s$', (0, -.35))
    for t in (1, 2):
        dot(ax, r0 + t * s, f'$t={t}$', (-.2, .2), BLUE, 10)
    dot(ax, (0, 0), '$O$', (-.3, -.1))
    ax.set_title('直线 $r=r_0+ts$', fontsize=11)
    ax = a3(fig, (1, 2, 2), 25, -60, ((-.2, 2.2), (-.2, 2.2), (0, 1.5)))
    u, v = np.meshgrid(np.linspace(-1, 1.5, 2), np.linspace(-1, 1.5, 2))
    o, a, b = np.array([.6, .4, .5]), np.array([.8, 0, .2]), np.array([0, .8, .25])
    ax.plot_surface(o[0] + u * a[0] + v * b[0], o[1] + u * a[1] + v * b[1], o[2] + u * a[2] + v * b[2], color=BLUE, alpha=.15)
    q3(ax, o, a, RED, '$a$'); q3(ax, o, b, ORANGE, '$b$'); ax.scatter(*o, color=INK, s=10); ax.text(*(o + [-.15, 0, -.2]), '$r_0$')
    ax.set_box_aspect((1, 1, .7), zoom=1.4); ax.set_title('平面 $r=r_0+ua+vb$', fontsize=11)
    fig.tight_layout(); save(fig, P + 'param_line_plane.png', ticks=False)


def projection():
    fig, ax = plt.subplots(figsize=(4.6, 2.6)); flat(ax, (-.4, 4.6), (-.5, 2.4))
    a, b = np.array([4, .8]), np.array([1.8, 2])
    e = a / np.linalg.norm(a); p = (b @ e) * e
    vec(ax, (0, 0), a, BLUE, '$a$', (.05, -.3)); vec(ax, (0, 0), b, ORANGE, '$b$', (-.25, .05))
    ax.plot(*zip(b, p), ls=':', color=GRAY); vec(ax, (0, 0), p, RED, None, lw=2.6)
    ax.text(p[0] - .2, p[1] - .45, '$\\mathrm{proj}_a b=\\dfrac{a\\cdot b}{|a|^2}a$', color=RED, fontsize=11, ha='center')
    th = np.degrees(np.arctan2(b[1], b[0])); ta = np.degrees(np.arctan2(a[1], a[0]))
    ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=ta, theta2=th, color=GRAY)); ax.text(.62, .48, '$\\theta$', fontsize=11)
    ax.text(3.0, 1.9, '标量投影 $|b|\\cos\\theta=\\dfrac{a\\cdot b}{|a|}$', fontsize=10.5, ha='center')
    save(fig, P + 'projection.png', ticks=False)


def cross():
    fig = plt.figure(figsize=(4.4, 3.4))
    ax = a3(fig, (1, 1, 1), 20, -50, ((0, 1.6), (0, 1.6), (0, 1.6)))
    a, b = np.array([1.3, .1, 0]), np.array([.4, 1.2, 0]); c = np.cross(a, b) / 1.2
    ax.add_collection3d(__import__('mpl_toolkits.mplot3d.art3d', fromlist=['Poly3DCollection']).Poly3DCollection([[(0, 0, 0), a, a + b, b]], fc=LIGHT['blue'], ec=BLUE, alpha=.6))
    q3(ax, (0, 0, 0), a, BLUE, '$a$', (.05, 0, -.12)); q3(ax, (0, 0, 0), b, ORANGE, '$b$', (0, .05, -.1)); q3(ax, (0, 0, 0), c, RED, '$a\\times b$', (.05, 0, .05))
    ax.text(.8, .7, 0, '面积 $=|a\\times b|$', color=BLUE, fontsize=10.5)
    ax.text2D(.5, .02, '右手四指从 $a$ 转向 $b$，拇指指向 $a\\times b$', transform=ax.transAxes, ha='center', fontsize=10)
    save(fig, P + 'cross_product.png', ticks=False)


def triple():
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(4.4, 3.4))
    ax = a3(fig, (1, 1, 1), 18, -55, ((0, 2), (0, 2), (0, 1.6)))
    a, b, c = np.array([1.4, 0, 0]), np.array([.3, 1.2, 0]), np.array([.4, .3, 1.1])
    O = np.zeros(3); V = [O, a, a + b, b, c, a + c, a + b + c, b + c]
    faces = [[V[0], V[1], V[2], V[3]], [V[4], V[5], V[6], V[7]], [V[0], V[1], V[5], V[4]], [V[3], V[2], V[6], V[7]], [V[1], V[2], V[6], V[5]], [V[0], V[3], V[7], V[4]]]
    ax.add_collection3d(Poly3DCollection(faces, fc=LIGHT['blue'], ec=BLUE, alpha=.18, lw=.8))
    q3(ax, O, a, BLUE, '$a$', (0, -.15, -.12)); q3(ax, O, b, ORANGE, '$b$'); q3(ax, O, c, RED, '$c$', (-.1, 0, .05))
    ax.plot([c[0], c[0]], [c[1], c[1]], [0, c[2]], ':', color=GRAY); ax.text(c[0] + .05, c[1], .5, '$h$', color=GRAY)
    ax.text2D(.5, .02, '$|(a\\times b)\\cdot c|=$ 底面积 $\\times h=$ 平行六面体体积', transform=ax.transAxes, ha='center', fontsize=10)
    save(fig, P + 'triple_product.png', ticks=False)


def normal_line():
    fig, ax = plt.subplots(figsize=(4.2, 2.8)); flat(ax, (-.5, 5), (-.6, 3.4))
    n = np.array([1, 2]) / np.sqrt(5); d = np.array([2, -1]) / np.sqrt(5); M0 = np.array([2, 1.4])
    ax.plot(*zip(M0 - 2.6 * d, M0 + 2.4 * d), color=BLUE)
    vec(ax, M0, M0 + 1.3 * n, RED, '$n=(A,B)$', (.05, 0)); M = M0 + 1.7 * d
    vec(ax, M0, M, ORANGE, None); dot(ax, M0, '$M_0$', (-.45, -.2)); dot(ax, M, '$M$', (.05, .12))
    ax.text(2.6, .2, '$\\overrightarrow{M_0M}\\perp n$', color=ORANGE, fontsize=11)
    ax.text(2.4, 3.1, '$A(x-x_0)+B(y-y_0)=0$', ha='center', fontsize=11)
    save(fig, P + 'point_normal.png', ticks=False)


def distance():
    fig, ax = plt.subplots(figsize=(4.2, 2.8)); flat(ax, (-.5, 5), (-.5, 3.4))
    n = np.array([1, 2]) / np.sqrt(5); d = np.array([2, -1]) / np.sqrt(5); M0 = np.array([1.5, 1.3])
    ax.plot(*zip(M0 - 1.8 * d, M0 + 3 * d), color=BLUE); ax.text(*(M0 + 2.8 * d + [.05, .15]), '$Ax+By+C=0$', color=BLUE, fontsize=10)
    Pp = M0 + 1.2 * d + 1.5 * n; H = M0 + 1.2 * d
    ax.plot(*zip(Pp, H), color=RED); dot(ax, Pp, '$P$', (.1, .05)); dot(ax, H, '$H$', (.1, -.3)); dot(ax, M0, '$M_0$', (-.45, -.25))
    vec(ax, M0, Pp, GRAY, None, lw=1)
    ax.text(*(Pp + H) / 2 + [.12, -.05], '$d=\\dfrac{|Ax_P+By_P+C|}{\\sqrt{A^2+B^2}}$', color=RED, fontsize=10.5)
    save(fig, P + 'point_line_distance.png', ticks=False)


def bisector():
    fig, ax = plt.subplots(figsize=(3.8, 3.2)); flat(ax, (-3, 3), (-2.5, 2.5))
    for ang, c in [(15, BLUE), (75, ORANGE)]:
        t = np.radians(ang); ax.plot([-3 * np.cos(t), 3 * np.cos(t)], [-3 * np.sin(t), 3 * np.sin(t)], color=c)
    for ang in (45, 135):
        t = np.radians(ang); ax.plot([-3 * np.cos(t), 3 * np.cos(t)], [-3 * np.sin(t), 3 * np.sin(t)], color=GREEN, ls='--', lw=1.2)
    t = np.radians(45); p = 1.8 * np.array([np.cos(t), np.sin(t)])
    for ang in (15, 75):
        u = np.radians(ang); dvec = np.array([np.cos(u), np.sin(u)]); foot = (p @ dvec) * dvec
        ax.plot(*zip(p, foot), ':', color=GRAY)
    dot(ax, p, '', color=GREEN); ax.text(-2.9, 2.1, '虚线：两条角平分线\n其上的点到两直线距离相等', fontsize=9.5, color=GREEN)
    save(fig, P + 'bisector.png', ticks=False)


def plane_normal_and_intersection():
    fig = plt.figure(figsize=(6.4, 3.0))
    ax = a3(fig, (1, 2, 1), 22, -60, ((-1, 1), (-1, 1), (-1, 1)))
    u, v = np.meshgrid(np.linspace(-1, 1, 2), np.linspace(-1, 1, 2))
    ax.plot_surface(u, v, -.2 * u - .1 * v, color=BLUE, alpha=.18)
    q3(ax, (0, 0, 0), (.2, .1, 1) / np.linalg.norm((.2, .1, 1)) * .9, RED, '$n=(A,B,C)$')
    q3(ax, (0, 0, 0), (.7, -.3, -.11), ORANGE, '$\\overrightarrow{M_0M}$', (0, -.1, -.2))
    ax.set_box_aspect((1, 1, .8), zoom=1.35); ax.scatter(0, 0, 0, color=INK, s=8); ax.set_title('平面：$n\\cdot\\overrightarrow{M_0M}=0$', fontsize=10.5)
    ax = a3(fig, (1, 2, 2), 20, -55, ((-1, 1), (-1, 1), (-1, 1)))
    ax.plot_surface(u, v, .5 * u, color=BLUE, alpha=.3)
    ax.plot_surface(u, v, -.6 * v, color=ORANGE, alpha=.3)
    s = np.linspace(-1, 1, 20); z = .5 * s; y = -z / .6
    ax.plot(s, y, z, color=RED, lw=2.2)
    ax.text(.9, -.8, .55, '交线方向\n$s=n_1\\times n_2$', color=RED, fontsize=10)
    ax.set_box_aspect((1, 1, .8), zoom=1.35); ax.set_title('两平面的交线', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'plane_and_line.png', ticks=False)


def skew():
    fig = plt.figure(figsize=(4.4, 3.4))
    ax = a3(fig, (1, 1, 1), 20, -62, ((-1.2, 1.2), (-1.2, 1.2), (-.2, 1.2)))
    t = np.linspace(-1.2, 1.2, 2)
    ax.plot(t, 0 * t, 0 * t, color=BLUE, lw=2); ax.plot(0 * t, t, 1 + 0 * t, color=ORANGE, lw=2)
    ax.plot([0, 0], [0, 0], [0, 1], color=RED, lw=2, ls='--')
    ax.text(1.15, 0, -.15, '$\\ell_1$', color=BLUE); ax.text(0, 1.2, 1.05, '$\\ell_2$', color=ORANGE)
    ax.text(.05, .05, .45, '公垂线段 $d$', color=RED, fontsize=10.5)
    ax.text2D(.5, .02, '$d=\\dfrac{|(P_2-P_1)\\cdot(s_1\\times s_2)|}{|s_1\\times s_2|}$', transform=ax.transAxes, ha='center', fontsize=11)
    save(fig, P + 'skew_lines.png', ticks=False)


def conics():
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.5))
    a, b = 2, 1.2; c = np.sqrt(a * a - b * b); th = np.linspace(0, 2 * np.pi, 300)
    ax = axs[0]; flat(ax, (-2.6, 2.6), (-1.8, 1.8)); ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE)
    P_ = np.array([a * np.cos(1.1), b * np.sin(1.1)])
    for f in (-c, c):
        ax.plot([f, P_[0]], [0, P_[1]], color=ORANGE, lw=1); dot(ax, (f, 0), '', color=RED)
    ax.set_title('椭圆：$r_1+r_2=2a$', fontsize=10)
    ax = axs[1]; flat(ax, (-3, 3), (-2, 2)); a, b = 1, 1.1; c = np.sqrt(a * a + b * b)
    s = np.linspace(-1.4, 1.4, 100)
    for sg in (1, -1):
        ax.plot(sg * a * np.cosh(s), b * np.sinh(s), color=BLUE)
    x = np.linspace(-3, 3, 2); ax.plot(x, b / a * x, ':', color=GRAY, lw=1); ax.plot(x, -b / a * x, ':', color=GRAY, lw=1)
    P_ = np.array([a * np.cosh(.9), b * np.sinh(.9)])
    for f in (-c, c):
        ax.plot([f, P_[0]], [0, P_[1]], color=ORANGE, lw=1); dot(ax, (f, 0), '', color=RED)
    ax.set_title('双曲线：$|r_1-r_2|=2a$', fontsize=10)
    ax = axs[2]; flat(ax, (-1.2, 3), (-2.2, 2.2)); p = 1
    y = np.linspace(-2.1, 2.1, 100); ax.plot(y ** 2 / (2 * p), y, color=BLUE)
    ax.axvline(-p / 2, color=GRAY, ls='--', lw=1); dot(ax, (p / 2, 0), '', color=RED)
    y0 = 1.4; P_ = (y0 ** 2 / 2, y0)
    ax.plot([p / 2, P_[0]], [0, P_[1]], color=ORANGE, lw=1); ax.plot([-p / 2, P_[0]], [y0, y0], color=ORANGE, lw=1)
    ax.set_title('抛物线：到焦点 = 到准线', fontsize=10)
    fig.tight_layout(); save(fig, P + 'conics.png', ticks=False)


def eccentricity():
    fig, ax = plt.subplots(figsize=(4.8, 3.2)); flat(ax, (-3.2, 3.6), (-2.6, 2.6))
    p = 1.0
    th = np.linspace(-np.pi, np.pi, 800)
    for e, col, lab in [(.5, BLUE, '$e=0.5$ 椭圆'), (1, GREEN, '$e=1$ 抛物线'), (1.6, ORANGE, '$e=1.6$ 双曲线')]:
        r = e * p / (1 - e * np.cos(th))
        m = (r > 0) & (r < 6)
        x, y = r * np.cos(th), r * np.sin(th); x[~m] = np.nan
        ax.plot(x, y, color=col, label=lab)
    ax.axvline(-p, color=GRAY, ls='--', lw=1); ax.text(-p - .1, 2.3, '准线', ha='right', color=GRAY, fontsize=10)
    dot(ax, (0, 0), '焦点 $F$', (.1, -.35), RED, 10)
    ax.legend(loc='lower right', fontsize=9.5)
    ax.set_title('同一焦点与准线：$e=|PF|\\,/\\,d$，$d$ 为到准线的距离', fontsize=10.5)
    save(fig, P + 'eccentricity.png', ticks=False)


def cone_sections():
    fig, ax = plt.subplots(figsize=(4.4, 3.4)); flat(ax, (-2.6, 3.4), (-2.4, 2.4))
    ax.add_patch(Polygon([(0, 0), (-2.2, 2.2), (2.2, 2.2)], fc='#eef2f6', ec='none'))
    ax.add_patch(Polygon([(0, 0), (-2.2, -2.2), (2.2, -2.2)], fc='#eef2f6', ec='none'))
    x = np.linspace(-2.2, 2.2, 2); ax.plot(x, x, color=GRAY); ax.plot(x, -x, color=GRAY)
    ax.plot([0, 0], [-2.3, 2.3], ':', color=GRAY, lw=.8); ax.text(.08, 2.25, '轴', color=GRAY, fontsize=9.5)
    ax.plot([-1.2, 1.9], [1.0, 1.9], color=BLUE, lw=2); ax.text(1.95, 1.75, '椭圆', color=BLUE, fontsize=10.5)
    ax.plot([-.8, 1.5], [0.0, -2.3], color=GREEN, lw=2); ax.text(1.4, -1.6, '抛物线\n（平行于母线）', color=GREEN, fontsize=10)
    ax.plot([-1.5, -1.5], [-2.3, 2.3], color=ORANGE, lw=2); ax.text(-1.6, 2.0, '双曲线\n（截两叶）', color=ORANGE, fontsize=10, ha='right')
    ax.set_title('圆锥的轴截面：截平面的倾角决定曲线类型', fontsize=10.5)
    save(fig, P + 'cone_sections.png', ticks=False)


def optics():
    fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.6))
    ax = axs[0]; flat(ax, (-2.4, 2.4), (-1.5, 1.5)); a, b = 2, 1.2; c = np.sqrt(a * a - b * b)
    th = np.linspace(0, 2 * np.pi, 300); ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE)
    for t in (.7, 1.6, 2.4, 4.0, 5.2):
        P_ = (a * np.cos(t), b * np.sin(t))
        ax.plot([-c, P_[0], c], [0, P_[1], 0], color=ORANGE, lw=.9)
    dot(ax, (-c, 0), '$F_1$', (-.1, -.3), RED, 10); dot(ax, (c, 0), '$F_2$', (-.1, -.3), RED, 10)
    ax.set_title('椭圆：自 $F_1$ 发出的光反射后过 $F_2$', fontsize=10)
    ax = axs[1]; flat(ax, (-.6, 3), (-1.8, 1.8)); p = 1
    y = np.linspace(-1.8, 1.8, 100); ax.plot(y ** 2 / 2, y, color=BLUE)
    for y0 in (-1.4, -.8, .5, 1.2):
        x0 = y0 ** 2 / 2; ax.plot([3, x0, p / 2], [y0, y0, 0], color=ORANGE, lw=.9)
    dot(ax, (p / 2, 0), '$F$', (-.05, -.3), RED, 10)
    ax.set_title('抛物线：平行于轴的光汇聚于焦点', fontsize=10)
    fig.tight_layout(); save(fig, P + 'optical_property.png', ticks=False)


def rotation():
    fig, ax = plt.subplots(figsize=(4.0, 3.2)); flat(ax, (-1.6, 3.2), (-.6, 3.0))
    vec(ax, (0, 0), (3, 0), GRAY, '$x$', (.05, -.2)); vec(ax, (0, 0), (0, 2.8), GRAY, '$y$', (-.25, 0))
    t = np.radians(30)
    vec(ax, (0, 0), (2.9 * np.cos(t), 2.9 * np.sin(t)), BLUE, "$x'$"); vec(ax, (0, 0), (-2.4 * np.sin(t), 2.4 * np.cos(t)), BLUE, "$y'$", (-.3, 0))
    ax.add_patch(Arc((0, 0), 1.4, 1.4, theta1=0, theta2=30, color=RED)); ax.text(.8, .18, '$\\varphi$', color=RED)
    Pp = np.array([2.2, 1.9]); dot(ax, Pp, '$P$', (.08, .05))
    ax.text(-1.5, -.5, "$x=x'\\cos\\varphi-y'\\sin\\varphi,\\ \\ y=x'\\sin\\varphi+y'\\cos\\varphi$", fontsize=9.5)
    save(fig, P + 'axis_rotation.png', ticks=False)


def quadrics():
    fig = plt.figure(figsize=(6.6, 4.4))
    u = np.linspace(0, 2 * np.pi, 40)
    items = []
    v = np.linspace(0, np.pi, 24); U, V = np.meshgrid(u, v)
    items.append(('椭球面', 1.2 * np.cos(U) * np.sin(V), .8 * np.sin(U) * np.sin(V), .6 * np.cos(V)))
    s = np.linspace(-1.2, 1.2, 20); U, S = np.meshgrid(u, s)
    items.append(('单叶双曲面', np.cosh(S) * np.cos(U) * .7, np.cosh(S) * np.sin(U) * .7, np.sinh(S) * .8))
    s = np.linspace(0, 1.3, 16); U, S = np.meshgrid(u, s)
    X2, Y2, Z2 = .6 * np.sinh(S) * np.cos(U), .6 * np.sinh(S) * np.sin(U), .6 * np.cosh(S)
    items.append(('双叶双曲面', np.vstack([X2, X2]), np.vstack([Y2, Y2]), np.vstack([Z2, -Z2[::-1]])))
    r = np.linspace(0, 1.1, 14); U, R = np.meshgrid(u, r)
    items.append(('椭圆抛物面', R * np.cos(U), .8 * R * np.sin(U), R ** 2))
    x = np.linspace(-1, 1, 20); X, Y = np.meshgrid(x, x)
    items.append(('双曲抛物面', X, Y, X ** 2 - Y ** 2))
    r = np.linspace(-1, 1, 16); U, R = np.meshgrid(u, r)
    items.append(('二次锥面', R * np.cos(U), R * np.sin(U), R))
    for i, (t, X, Y, Z) in enumerate(items):
        ax = fig.add_subplot(2, 3, i + 1, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='Blues', alpha=.85, lw=.2, edgecolor='#5b7fa8', rstride=1, cstride=2, vmin=-1.5, vmax=1.5)
        ax.set_axis_off(); ax.view_init(20, -55); ax.set_box_aspect((1, 1, .9))
        ax.set_title(t, fontsize=10.5, y=.92)
    fig.subplots_adjust(wspace=0, hspace=0, left=0, right=1, top=1, bottom=0)
    save(fig, P + 'quadric_surfaces.png', ticks=False)


for f in [section, param, projection, cross, triple, normal_line, distance, bisector, plane_normal_and_intersection, skew, conics, eccentricity, cone_sections, optics, rotation, quadrics]:
    f()

place('03_解析几何.md', [
    ('**定比分点与中点。**', P + 'section_point.png', '定比分点：M 把线段 AB 分成 λ∶1'),
    ('用向量可以很自然地描述直线和平面', P + 'param_line_plane.png', '用一点和方向向量写出直线与平面的参数形式'),
    ('点积最重要的用途是计算投影', P + 'projection.png', '标量投影与向量投影'),
    ('在三维右手直角坐标系中，两个向量', P + 'cross_product.png', '叉积的方向（右手法则）与大小（平行四边形面积）'),
    ('混合积的几何意义是有向体积', P + 'triple_product.png', '混合积的绝对值是平行六面体的体积'),
    ('这称为直线的点法式方程', P + 'point_normal.png', '点法式：直线上任一点与已知点的连线垂直于法向量'),
    ('点到直线的距离，是从这个点到直线', P + 'point_line_distance.png', '点到直线的距离与垂足'),
    ('**两直线夹角的平分线。**', P + 'bisector.png', '两相交直线的两条角平分线互相垂直'),
    ('两个不平行平面的交线同时位于两个', P + 'plane_and_line.png', '空间平面的点法式与两平面的交线'),
    ('若两条直线方向不平行，它们的公垂', P + 'skew_lines.png', '异面直线的公垂线与距离'),
    ('**抛物线**是到一个焦点与到一', P + 'conics.png', '三种二次曲线的距离定义'),
    ('椭圆、抛物线和双曲线还可以用同一', P + 'eccentricity.png', '焦点—准线定义：离心率 e 决定曲线类型'),
    ('椭圆、双曲线和抛物线合称圆锥曲线', P + 'cone_sections.png', '平面截圆锥得到三类曲线'),
    ('**光学性质。**', P + 'optical_property.png', '椭圆与抛物线的光学性质'),
    ('平面上把坐标轴逆时针旋转角', P + 'axis_rotation.png', '坐标轴旋转'),
    ('判断曲面的形状，应结合截面来理解', P + 'quadric_surfaces.png', '六类常见二次曲面'),
])
