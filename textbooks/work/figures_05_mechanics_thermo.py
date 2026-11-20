# 大学物理册第 1–7、9.6、11–13 节补充插图（2026-11-20）。运行：py work/figures_05_mechanics_thermo.py
# 第 8–10、14 节原有插图由 figures_05_rotation.py 与 figures_05_relativity.py 生成。
from figlib import *
from matplotlib.patches import Polygon, Rectangle, Circle, Arc, Ellipse

style()
P = '05_'


def vec(ax, p, d, color, label=None, off=(.06, .06), lw=1.8, fs=11):
    q = (p[0] + d[0], p[1] + d[1])
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=12, shrinkA=0, shrinkB=0))
    if label:
        ax.text(q[0] + off[0], q[1] + off[1], label, color=color, fontsize=fs)


def flat(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')


def kinematics():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 2.6))
    t = np.linspace(0, 4, 100); v0, acc = 1, 1.5
    a.plot(t, v0 + acc * t, color=BLUE); a.fill_between(t[t <= 3], v0 + acc * t[t <= 3], color=BLUE, alpha=.15)
    a.text(1.5, 1.3, '面积 = 位移', ha='center', fontsize=10); a.set_xlabel('$t$'); a.set_ylabel('$v$')
    a.text(.1, v0 + .2, '$v_0$', fontsize=10); a.text(3.3, 6.2, '斜率 $=a$', fontsize=10, color=BLUE); a.set_ylim(0, 7.5)
    b.plot(t, v0 * t + acc * t ** 2 / 2, color=ORANGE); b.set_xlabel('$t$'); b.set_ylabel('$x$')
    b.text(.3, 9, '$x=v_0t+\\frac{1}{2}at^2$', fontsize=10.5, color=ORANGE)
    a.set_title('$v$–$t$ 图', fontsize=10.5); b.set_title('$x$–$t$ 图：切线斜率 = 速度', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'uniform_acceleration.png')


def tangential_normal():
    fig, ax = plt.subplots(figsize=(4.2, 3.0)); flat(ax, (-.2, 4.4), (-.2, 3.0))
    t = np.linspace(0, 4, 200); y = .15 * t ** 2 + .2 * np.sin(2 * t) + .5; ax.plot(t, y, color=GRAY)
    x0 = 2.2; y0 = .15 * x0 ** 2 + .2 * np.sin(2 * x0) + .5; dy = .3 * x0 + .4 * np.cos(2 * x0)
    tau = np.array([1, dy]) / np.hypot(1, dy); n = np.array([-tau[1], tau[0]])
    ax.plot(x0, y0, 'o', color=INK, ms=4)
    vec(ax, (x0, y0), 1.1 * tau, BLUE, '$\\mathbf{v}$', (.05, -.25))
    vec(ax, (x0, y0), .7 * tau + .9 * n, RED, '$\\mathbf{a}$', (-.1, .08))
    vec(ax, (x0, y0), .7 * tau, ORANGE, None, lw=1.3); vec(ax, (x0, y0), .9 * n, GREEN, None, lw=1.3)
    ax.text(x0 + .55 * tau[0] + .1, y0 + .55 * tau[1] - .3, '$a_\\tau=\\dfrac{dv}{dt}$', color=ORANGE, fontsize=10)
    ax.text(x0 + .9 * n[0] - .95, y0 + .9 * n[1] + .05, '$a_n=\\dfrac{v^2}{\\rho}$', color=GREEN, fontsize=10)
    ax.set_title('切向加速度改变速率，法向加速度改变方向', fontsize=10)
    save(fig, P + 'tangential_normal.png', ticks=False)


def projectile():
    fig, ax = plt.subplots(figsize=(4.6, 2.6)); g, v = 9.8, 10
    for ang, c in [(15, GRAY), (30, BLUE), (45, RED), (60, GREEN), (75, ORANGE)]:
        th = np.radians(ang); T = 2 * v * np.sin(th) / g; t = np.linspace(0, T, 100)
        ax.plot(v * np.cos(th) * t, v * np.sin(th) * t - g * t ** 2 / 2, color=c, lw=2 if ang == 45 else 1.3, label=f'{ang}°')
    ax.set_xlabel('$x$ / m'); ax.set_ylabel('$y$ / m'); ax.set_ylim(0, 5.2); ax.legend(fontsize=9, ncol=5, loc='upper center', bbox_to_anchor=(.5, 1.18), handlelength=1.2)
    ax.text(5.6, .25, '互余角射程相同；45° 射程最大', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'projectile.png')


def closest_approach():
    fig, ax = plt.subplots(figsize=(4.2, 3.0)); flat(ax, (-1.3, 4.6), (-.6, 3.2))
    A = np.array([0, 0]); B0 = np.array([3.6, 2.6]); vr = np.array([-1.0, -.2])
    ax.plot(*A, 'o', color=BLUE); ax.text(-.25, -.35, '$A$（静止于相对系）', fontsize=10, color=BLUE)
    t = np.linspace(0, 5.2, 2); pts = B0[:, None] + vr[:, None] * t; ax.plot(*pts, color=ORANGE)
    ax.plot(*B0, 'o', color=ORANGE); ax.text(B0[0] - .15, B0[1] + .15, '$B$ 的初位置', color=ORANGE, fontsize=10)
    vec(ax, B0, .9 * vr, RED, '$\\mathbf{v}_B-\\mathbf{v}_A$', (-.2, .15), fs=10)
    u = vr / np.linalg.norm(vr); H = B0 + ((A - B0) @ u) * u
    ax.plot(*zip(A, H), ls='--', color=GREEN); ax.text(*(A + H) / 2 + [.08, -.1], '$d_{\\min}$', color=GREEN)
    ax.set_title('在 $A$ 的参考系中，$B$ 沿直线运动；最近距离是垂线段', fontsize=9.5)
    save(fig, P + 'closest_approach.png', ticks=False)


def incline():
    fig, ax = plt.subplots(figsize=(4.0, 2.8)); flat(ax, (-.3, 5.2), (-.3, 3.2))
    th = np.radians(28); ax.add_patch(Polygon([(0, 0), (5, 0), (0, 5 * np.tan(th))], fc='#eef0f3', ec=GRAY))
    ax.add_patch(Arc((5, 0), 1.2, 1.2, theta1=180 - 28, theta2=180, color=GRAY)); ax.text(4.1, .1, '$\\theta$', fontsize=11)
    d = np.array([np.cos(th), -np.sin(th)]); n = np.array([np.sin(th), np.cos(th)])
    c = np.array([0, 5 * np.tan(th)]) + 2.2 * d + .35 * n
    corners = [c + sx * .4 * d + sy * .35 * n for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    ax.add_patch(Polygon(corners, fc=LIGHT['blue'], ec=BLUE))
    vec(ax, c, (0, -1.3), RED, '$m\\mathbf{g}$', (.05, -.1)); vec(ax, c, 1.1 * n, GREEN, '$\\mathbf{N}$')
    vec(ax, c, -.7 * d, ORANGE, '$\\mathbf{f}$', (-.25, .05))
    vec(ax, c, 1.3 * np.sin(th) * d, RED, None, lw=1); ax.text(*(c + 1.3 * np.sin(th) * d + [.0, -.32]), '$mg\\sin\\theta$', color=RED, fontsize=9.5)
    ax.set_title('斜面上的受力分析', fontsize=10.5)
    save(fig, P + 'incline_forces.png', ticks=False)


def atwood():
    fig, ax = plt.subplots(figsize=(2.8, 3.2)); flat(ax, (-1.6, 1.6), (-.4, 4.2))
    ax.add_patch(Circle((0, 3.4), .45, fc='#eef0f3', ec=GRAY)); ax.plot([-.6, .6], [3.95, 3.95], color=GRAY, lw=3); ax.plot([0, 0], [3.4, 3.95], color=GRAY)
    ax.plot([-.45, -.45], [3.4, 1.8], color=INK, lw=1); ax.plot([.45, .45], [3.4, 1.0], color=INK, lw=1)
    ax.add_patch(Rectangle((-.75, 1.2), .6, .6, fc=LIGHT['blue'], ec=BLUE)); ax.text(-.45, 1.5, '$m_1$', ha='center')
    ax.add_patch(Rectangle((.1, .2), .7, .8, fc=LIGHT['orange'], ec=ORANGE)); ax.text(.45, .6, '$m_2$', ha='center')
    vec(ax, (-1.1, 1.3), (0, .7), GREEN, '$a$', (-.3, -.2)); vec(ax, (1.15, .9), (0, -.7), GREEN, '$a$', (.08, .2))
    ax.text(0, -.35, '$a=\\dfrac{m_2-m_1}{m_1+m_2}\\,g$', ha='center', fontsize=10.5)
    save(fig, P + 'atwood.png', ticks=False)


def work_path():
    fig, ax = plt.subplots(figsize=(4.2, 2.8)); flat(ax, (-.3, 4.6), (-.3, 2.8))
    s = np.linspace(0, 1, 200); x = .3 + 3.8 * s; y = .4 + 1.6 * np.sin(2.6 * s) * (1 - .4 * s)
    ax.plot(x, y, color=GRAY); ax.text(.1, .2, '1', fontsize=11); ax.text(4.2, y[-1] - .05, '2', fontsize=11)
    for k in (40, 90, 140):
        p = np.array([x[k], y[k]]); dr = np.array([x[k + 12] - x[k], y[k + 12] - y[k]])
        F = np.array([.6, -.35 + .3 * np.cos(k / 30)])
        vec(ax, p, F, RED, '$\\mathbf{F}$' if k == 40 else None, lw=1.4); vec(ax, p, dr * 1.6, BLUE, '$d\\mathbf{r}$' if k == 40 else None, (-.4, .05), lw=1.4)
    ax.text(2.3, 2.45, '$W=\\int_1^2 \\mathbf{F}\\cdot d\\mathbf{r}$', fontsize=12, ha='center')
    save(fig, P + 'work_path.png', ticks=False)


def collision_transfer():
    fig, ax = plt.subplots(figsize=(4.4, 2.8)); x = np.linspace(0, 8, 400)
    ax.plot(x, 2 * x / (1 + x), color=BLUE, label='动量比 $\\eta_p=\\dfrac{2x}{1+x}$')
    ax.plot(x, 4 * x / (1 + x) ** 2, color=ORANGE, label='动能比 $\\eta_E=\\dfrac{4x}{(1+x)^2}$')
    ax.plot(1, 1, 'o', color=RED); ax.axhline(2, color=BLUE, ls=':', lw=1)
    ax.set_xlabel('质量比 $x=m_2/m_1$'); ax.set_ylim(0, 2.2); ax.legend(fontsize=9.5, loc='center right')
    ax.set_title('弹性正碰中球二获得的份额', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'collision_transfer.png')


def rocket():
    fig, ax = plt.subplots(figsize=(4.2, 2.7)); r = np.linspace(1, 20, 300)
    ax.plot(r, np.log(r), color=BLUE); ax.set_xlabel('质量比 $m_0/m$'); ax.set_ylabel('$\\Delta v/u$')
    for k in (2.718, 7.39):
        ax.plot([k, k, 1], [0, np.log(k), np.log(k)], ':', color=GRAY, lw=1)
    ax.set_title('$\\Delta v=u\\ln(m_0/m)$：速度增量只随质量比对数增长', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'rocket_equation.png')


def vertical_circle():
    fig, ax = plt.subplots(figsize=(3.6, 3.8)); flat(ax, (-1.9, 1.9), (-2.4, 2.2))
    th = np.linspace(0, 2 * np.pi, 200); ax.plot(np.cos(th), np.sin(th), color=GRAY, ls='--', lw=1); ax.plot(0, 0, 'o', color=INK, ms=3)
    ax.plot([0, 0], [0, 1], color=INK, lw=.8); ax.plot([0, 0], [0, -1], color=INK, lw=.8)
    for y, s in [(1, -1), (-1, 1)]:
        ax.add_patch(Circle((0, y), .1, fc=BLUE)); vec(ax, (0, y), (0, -.6), RED, '$mg$', (-.55, .05), fs=10)
        vec(ax, (.15, y), (0, .55 * s), GREEN, '$T$', (.08, -.1 * s), fs=10)
    ax.text(-1.85, 1.65, '最高点：$T+mg=mv^2/l$\n临界 $T=0$，$v^2=gl$', fontsize=9.5); ax.text(-1.85, -2.3, '最低点：$T-mg=mv^2/l$', fontsize=9.5)
    save(fig, P + 'vertical_circle.png', ticks=False)


def torque():
    fig, ax = plt.subplots(figsize=(4.4, 3.0)); flat(ax, (-.5, 5), (-1.5, 2.6))
    ax.add_patch(Rectangle((0, -.15), 4.2, .3, fc='#eef0f3', ec=GRAY)); ax.plot(0, 0, 'o', color=INK); ax.text(-.4, -.5, '转轴 $O$', fontsize=10)
    p = np.array([3.4, 0]); F = np.array([.6, 1.6])
    vec(ax, (0, 0), p, BLUE, '$\\mathbf{r}$', (-.3, -.4)); vec(ax, p, F, RED, '$\\mathbf{F}$')
    ax.add_patch(Arc(p, .8, .8, theta1=0, theta2=np.degrees(np.arctan2(F[1], F[0])), color=GRAY)); ax.text(p[0] + .45, .2, '$\\alpha$', fontsize=10)
    t = np.linspace(-2.2, 1.0, 2); ax.plot(p[0] + F[0] * t, p[1] + F[1] * t, ':', color=GRAY, lw=1)
    u = F / np.linalg.norm(F); foot = p + ((-p) @ u) * u
    ax.plot([0, foot[0]], [0, foot[1]], color=GREEN, lw=1.6); ax.text(foot[0] / 2 + .1, foot[1] / 2 - .35, '力臂 $d=r\\sin\\alpha$', color=GREEN, fontsize=10)
    ax.text(2.6, 2.2, '$M=Fd=rF\\sin\\alpha$', fontsize=11)
    save(fig, P + 'torque_lever_arm.png', ticks=False)


def kepler():
    fig, ax = plt.subplots(figsize=(4.4, 2.8)); flat(ax, (-2.4, 2.4), (-1.5, 1.5))
    a, e = 2, .6; b = a * np.sqrt(1 - e * e); c = a * e
    E = np.linspace(0, 2 * np.pi, 400); ax.plot(a * np.cos(E), b * np.sin(E), color=GRAY)
    ax.plot(c, 0, 'o', color=ORANGE, ms=9); ax.text(c - .15, -.35, '太阳', fontsize=9.5)
    def pos(M):
        from scipy.optimize import brentq
        Ee = brentq(lambda x: x - e * np.sin(x) - M, -1e-9, 2 * np.pi + 1e-9); return a * np.cos(Ee), b * np.sin(Ee)
    for M0, col in [(-.25, BLUE), (np.pi - .25, RED)]:
        Ms = np.linspace(M0, M0 + .5, 30); pts = [pos(m % (2 * np.pi)) for m in Ms]
        ax.add_patch(Polygon([(c, 0)] + pts, fc=col, alpha=.3, ec=col))
    ax.text(1.9, .55, '近日点附近\n走得快', fontsize=9.5, color=BLUE); ax.text(-2.3, .7, '远日点附近\n走得慢', fontsize=9.5, color=RED)
    ax.set_title('开普勒第二定律：相等时间扫过相等面积', fontsize=10)
    save(fig, P + 'kepler_areas.png', ticks=False)


def potential():
    fig, ax = plt.subplots(figsize=(4.4, 2.8)); a, b = 1, .25; x = np.linspace(-2.6, 2.6, 300)
    ax.plot(x, -a * x ** 2 + b * x ** 4, color=BLUE); ax.axhline(0, color='#9aa3ad', lw=.8)
    xm = np.sqrt(a / (2 * b)); um = -a * xm ** 2 + b * xm ** 4
    ax.plot([-xm, xm], [um, um], 'o', color=GREEN); ax.plot(0, 0, 'o', color=RED)
    ax.text(0, .25, '不稳定平衡\n$U\'\'<0$', ha='center', color=RED, fontsize=9.5); ax.text(xm, um - .45, '稳定平衡 $U\'\'>0$', ha='center', color=GREEN, fontsize=9.5)
    ax.set_ylim(-1.8, 1.8); ax.set_xlabel('$x$'); ax.set_ylabel('$U$'); ax.set_title('$U=-ax^2+bx^4$ 的三个平衡点', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'potential_equilibria.png')


def shm_energy():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.6), gridspec_kw={'width_ratios': [1.5, 1]})
    t = np.linspace(0, 2 * np.pi, 300)
    a.plot(t, np.cos(t) ** 2, color=BLUE, label='势能 $\\frac{1}{2}kx^2$'); a.plot(t, np.sin(t) ** 2, color=ORANGE, label='动能 $\\frac{1}{2}mv^2$')
    a.axhline(1, color=GRAY, ls='--', lw=1, label='总能量')
    for k in range(4):
        a.axvline(np.pi / 4 + k * np.pi / 2, color=GREEN, ls=':', lw=1)
    a.set_xticks([0, np.pi, 2 * np.pi]); a.set_xticklabels(['$0$', '$T/2$', '$T$']); a.set_yticks([0, .5, 1]); a.set_yticklabels(['$0$', '$E/2$', '$E$'])
    a.legend(fontsize=8.5, loc='center right', bbox_to_anchor=(1.0, .62)); a.set_title('一个周期内四次动能等于势能', fontsize=10)
    b.plot(np.cos(t), -np.sin(t), color=PURPLE); b.set_aspect('equal'); b.axhline(0, color='#9aa3ad', lw=.8); b.axvline(0, color='#9aa3ad', lw=.8)
    b.set_xlabel('$x/A$'); b.set_ylabel('$v/(A\\omega)$'); b.set_title('相平面中的椭圆', fontsize=10)
    fig.tight_layout(); save(fig, P + 'shm_energy_phase.png', ticks=False)


def damped():
    fig, ax = plt.subplots(figsize=(4.8, 2.6)); t = np.linspace(0, 12, 600); beta, w = .18, 2.4
    ax.plot(t, np.exp(-beta * t) * np.cos(w * t), color=BLUE); ax.plot(t, np.exp(-beta * t), '--', color=ORANGE, lw=1.1); ax.plot(t, -np.exp(-beta * t), '--', color=ORANGE, lw=1.1)
    ax.axhline(0, color='#9aa3ad', lw=.8); ax.text(6.5, .45, '包络 $\\pm A_0e^{-\\beta t}$', color=ORANGE, fontsize=10)
    ax.set_xlabel('$t$'); ax.set_ylabel('$x/A_0$'); ax.set_title('弱阻尼振动：振幅按指数衰减', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'damped_oscillation.png')


def resonance():
    fig, ax = plt.subplots(figsize=(4.6, 2.9)); r = np.linspace(0, 2.2, 500)
    for z, c in [(.05, RED), (.1, ORANGE), (.2, GREEN), (.5, BLUE)]:
        ax.plot(r, 1 / np.sqrt((1 - r ** 2) ** 2 + (2 * z * r) ** 2), color=c, label=f'$\\beta/\\omega_0={z:g}$')
    ax.set_ylim(0, 11); ax.set_xlabel('$\\omega/\\omega_0$'); ax.set_ylabel('稳态振幅 / 静态位移'); ax.legend(fontsize=9)
    ax.set_title('共振曲线：阻尼越小，峰越高越窄', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'resonance_curves.png')


def double_pendulum():
    fig, ax = plt.subplots(figsize=(3.0, 3.2)); flat(ax, (-1.4, 1.8), (-2.4, .3))
    ax.plot([-.5, .5], [0, 0], color=GRAY, lw=3); p1 = np.array([np.sin(.5), -np.cos(.5)]); p2 = p1 + 1.0 * np.array([np.sin(1.0), -np.cos(1.0)])
    ax.plot([0, p1[0], p2[0]], [0, p1[1], p2[1]], color=INK, lw=1.4)
    ax.add_patch(Circle(p1, .09, fc=BLUE)); ax.add_patch(Circle(p2, .09, fc=ORANGE))
    ax.plot([0, 0], [0, -1.1], ':', color=GRAY); ax.plot([p1[0], p1[0]], [p1[1], p1[1] - 1.0], ':', color=GRAY)
    ax.add_patch(Arc((0, 0), .8, .8, theta1=-90, theta2=-90 + np.degrees(.5), color=RED)); ax.text(.06, -.55, '$\\varphi_1$', color=RED)
    ax.add_patch(Arc(p1, .8, .8, theta1=-90, theta2=-90 + np.degrees(1.0), color=RED)); ax.text(p1[0] + .12, p1[1] - .58, '$\\varphi_2$', color=RED)
    ax.text(p1[0] - .45, p1[1] + .05, '$m_1$', color=BLUE); ax.text(p2[0] + .12, p2[1], '$m_2$', color=ORANGE)
    ax.text(.25, -.15, '$l_1$', fontsize=10); ax.text(p1[0] + .5, p1[1] - .2, '$l_2$', fontsize=10)
    save(fig, P + 'double_pendulum.png', ticks=False)


def processes():
    fig, ax = plt.subplots(figsize=(4.4, 3.0)); V = np.linspace(1, 3, 200); p1, V1, g = 3, 1, 1.4
    ax.plot([1, 3], [p1, p1], color=BLUE, label='等压'); ax.plot([1, 1], [p1, .6], color=GREEN, label='等容')
    ax.plot(V, p1 * V1 / V, color=ORANGE, label='等温 $pV=$常量'); ax.plot(V, p1 * (V1 / V) ** g, color=RED, label='绝热 $pV^{\\gamma}=$常量')
    ax.fill_between(V, p1 * (V1 / V) ** g, color=RED, alpha=.08)
    ax.set_xlabel('$V$'); ax.set_ylabel('$p$'); ax.set_xlim(.8, 3.2); ax.set_ylim(0, 3.9); ax.legend(fontsize=9, loc='upper right', ncol=2)
    ax.set_title('同一初态出发的四种基本过程；曲线下面积为功', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'thermo_processes.png', ticks=False)


def carnot():
    fig, ax = plt.subplots(figsize=(4.4, 3.0)); g = 5 / 3; T1, T2 = 2.0, 1.6; V1, V2 = 1, 2
    V3 = V2 * (T1 / T2) ** (1 / (g - 1)); V4 = V1 * (T1 / T2) ** (1 / (g - 1))
    def iso(Va, Vb, T): V = np.linspace(Va, Vb, 100); return V, T / V
    def adi(Va, Vb, T, Vref): V = np.linspace(Va, Vb, 100); return V, (T / Vref) * (Vref / V) ** g
    segs = [iso(V1, V2, T1), adi(V2, V3, T1, V2), iso(V3, V4, T2)[::1], adi(V4, V1, T1, V1)]
    xs = np.concatenate([segs[0][0], segs[1][0], segs[2][0], segs[3][0]]); ys = np.concatenate([segs[0][1], segs[1][1], segs[2][1], segs[3][1]])
    ax.fill(xs, ys, color=BLUE, alpha=.12)
    for (V, p), c in zip(segs, [RED, GRAY, BLUE, GRAY]):
        ax.plot(V, p, color=c, lw=1.8)
    ax.text(1.5, 1.62, '等温吸热 $Q_1$（$T_1$）', color=RED, fontsize=9.5); ax.text(1.5, .8, '等温放热 $Q_2$（$T_2$）', color=BLUE, fontsize=9.5)
    ax.text(2.45, .9, '绝热', color=GRAY, fontsize=9.5); ax.text(1.02, 1.3, '绝热', color=GRAY, fontsize=9.5)
    ax.text(1.75, 1.15, '净功', ha='center', fontsize=10)
    ax.set_xlabel('$V$'); ax.set_ylabel('$p$'); ax.set_title('卡诺循环：$\\eta=1-T_2/T_1$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'carnot_cycle.png', ticks=False)


def maxwell():
    fig, ax = plt.subplots(figsize=(4.6, 2.9)); M, R = .028, 8.314; v = np.linspace(0, 1600, 500)
    for T, c in [(300, BLUE), (900, ORANGE)]:
        a = M / (2 * R * T); f = 4 * np.pi * (a / np.pi) ** 1.5 * v ** 2 * np.exp(-a * v * v)
        ax.plot(v, f * 1e3, color=c, label=f'$T={T}$ K')
        vp = np.sqrt(2 * R * T / M); vm = np.sqrt(8 * R * T / (np.pi * M)); vr = np.sqrt(3 * R * T / M)
        for vv, ls in [(vp, '-'), (vm, '--'), (vr, ':')]:
            ax.plot([vv, vv], [0, np.interp(vv, v, f * 1e3)], ls=ls, color=c, lw=1)
    ax.text(950, 1.55, '$v_p<\\langle v\\rangle<\\sqrt{\\langle v^2\\rangle}$', fontsize=10)
    ax.set_xlabel('$v$ / (m/s)'); ax.set_ylabel('$f(v)$ / (10$^{-3}$ s/m)'); ax.legend(fontsize=9.5)
    ax.set_title('氮气的麦克斯韦速率分布', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'maxwell_distribution.png', ticks=False)


def barometric():
    fig, ax = plt.subplots(figsize=(4.0, 2.7)); z = np.linspace(0, 30, 200)
    ax.plot(np.exp(-z / 8.4), z, color=BLUE); ax.set_xlabel('$p/p_0$'); ax.set_ylabel('高度 $z$ / km')
    ax.axhline(8.4, color=GRAY, ls=':', lw=1); ax.text(.4, 9.2, '$z=RT/(Mg)\\approx8.4$ km 处降为 $1/e$', fontsize=9.5)
    ax.set_title('等温大气的气压公式 $p=p_0e^{-Mgz/(RT)}$', fontsize=10)
    fig.tight_layout(); save(fig, P + 'barometric.png', ticks=False)


def vdw():
    fig, ax = plt.subplots(figsize=(4.6, 3.0)); V = np.linspace(.45, 4, 500)
    for t, c in [(.85, BLUE), (.95, GREEN), (1.0, RED), (1.1, ORANGE)]:
        p = 8 * t / (3 * V - 1) - 3 / V ** 2; ax.plot(V, p, color=c, lw=2 if t == 1 else 1.3, label=f'$T/T_k={t:g}$')
    ax.plot(1, 1, 'o', color=RED); ax.text(1.08, 1.08, '临界点 $K$', color=RED, fontsize=10)
    ax.set_xlim(.4, 4); ax.set_ylim(0, 2); ax.set_xlabel('$V/V_k$'); ax.set_ylabel('$p/p_k$'); ax.legend(fontsize=9)
    ax.set_title('范德瓦耳斯等温线：临界温度以下出现波浪段', fontsize=10)
    fig.tight_layout(); save(fig, P + 'van_der_waals.png', ticks=False)


for f in [kinematics, tangential_normal, projectile, closest_approach, incline, atwood, work_path, collision_transfer, rocket, vertical_circle, torque, kepler, potential, shm_energy, damped, resonance, double_pendulum, processes, carnot, maxwell, barometric, vdw]:
    f()

place('05_大学物理.md', [
    ('**匀变速直线运动的公式组。', P + 'uniform_acceleration.png', '匀加速直线运动的速度图与位置图'),
    ('切向分量改变速率，法向分量改', P + 'tangential_normal.png', '曲线运动中加速度的切向与法向分量'),
    ('**抛体运动。**', P + 'projectile.png', '同一初速、不同抛射角的轨迹（忽略空气阻力）'),
    ('求两质点的最近距离，也有两条', P + 'closest_approach.png', '换到一个质点的参考系求最近距离'),
    ('取固定斜面向下为正，倾角为', P + 'incline_forces.png', '斜面上物块的受力'),
    ('若滑轮和绳均理想、质量忽略', P + 'atwood.png', '阿特伍德机：理想滑轮与轻绳'),
    ('力做功定义为沿真实路径的积分', P + 'work_path.png', '变力沿曲线路径做功'),
    ('设质量比 \\(x=m_2/m', P + 'collision_transfer.png', '弹性正碰中动量与动能的传递比例'),
    ('这是齐奥尔科夫斯基公式', P + 'rocket_equation.png', '齐奥尔科夫斯基公式'),
    ('临界时 \\(T=0\\)', P + 'vertical_circle.png', '竖直圆周运动最高点与最低点的受力'),
    ('一扇门在铰链处几乎不移动', P + 'torque_lever_arm.png', '力矩与力臂'),
    ('**开普勒三定律。**', P + 'kepler_areas.png', '行星在椭圆轨道上相等时间扫过相等面积'),
    ('取 \\(U=-ax^2+bx', P + 'potential_equilibria.png', '势能曲线上的稳定与不稳定平衡'),
    ('这是以位移、速度为坐标的椭圆', P + 'shm_energy_phase.png', '简谐运动中的能量交换与相平面轨迹'),
    ('余弦负责往复，指数因子使振幅', P + 'damped_oscillation.png', '弱阻尼振动及其指数包络'),
    ('**共振曲线的宽度。**', P + 'resonance_curves.png', '不同阻尼下的受迫振动振幅'),
    ('双摆使动能交叉项的几何来源更', P + 'double_pendulum.png', '双摆的广义坐标'),
    ('四种基本过程的计算归纳如下', P + 'thermo_processes.png', '理想气体的四种基本过程（p–V 图）'),
    ('卡诺循环由两个等温过程和两个', P + 'carnot_cycle.png', '卡诺循环'),
    ('温度升高时，峰的位置右移、高', P + 'maxwell_distribution.png', '两种温度下的麦克斯韦速率分布与三种特征速率'),
    ('以地面 \\(z=0\\) 处', P + 'barometric.png', '等温大气中气压随高度指数下降'),
    ('临界温度以下，范德瓦耳斯等温', P + 'van_der_waals.png', '对比态下的范德瓦耳斯等温线'),
])
