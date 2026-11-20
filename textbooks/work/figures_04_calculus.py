# 微积分与微分方程册插图（2026-11-20）。运行：py work/figures_04_calculus.py
from figlib import *
from matplotlib.patches import Polygon, Rectangle, Wedge

style()
P = '04_'


def frame(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl)
    ax.axhline(0, color='#9aa3ad', lw=.8); ax.axvline(0, color='#9aa3ad', lw=.8)


def transforms():
    x = np.linspace(-3.5, 3.5, 400); f = lambda t: np.exp(-t ** 2) * 1.6 + 0 * t
    g = lambda t: t ** 2 / 2 - 1
    items = [('$f(x-1)$：右移 1', lambda t: g(t - 1)), ('$f(x)+1$：上移 1', lambda t: g(t) + 1),
             ('$f(2x)$：横向压缩一半', lambda t: g(2 * t)), ('$2f(x)$：纵向拉伸 2 倍', lambda t: 2 * g(t)),
             ('$-f(x)$：关于 $x$ 轴翻折', lambda t: -g(t)), ('$|f(x)|$：下方部分翻上', lambda t: np.abs(g(t)))]
    fig, axs = plt.subplots(2, 3, figsize=(6.6, 4.0), sharex=True, sharey=True)
    for ax, (t, h) in zip(axs.flat, items):
        frame(ax, (-3, 3), (-2.6, 3.2))
        ax.plot(x, g(x), color=GRAY, ls='--', lw=1.2); ax.plot(x, h(x), color=BLUE)
        ax.set_title(t, fontsize=10)
    fig.text(.5, -.01, '虚线为原函数 $f(x)=x^2/2-1$', ha='center', fontsize=10, color=GRAY)
    fig.tight_layout(); save(fig, P + 'graph_transforms.png')


def inverse():
    fig, ax = plt.subplots(figsize=(3.6, 3.4)); frame(ax, (-2.5, 4), (-2.5, 4)); ax.set_aspect('equal')
    x = np.linspace(-2.5, 1.4, 200); ax.plot(x, np.exp(x), color=BLUE, label='$y=e^x$')
    x2 = np.linspace(.08, 4, 200); ax.plot(x2, np.log(x2), color=ORANGE, label='$y=\\ln x$')
    t = np.linspace(-2.5, 4, 2); ax.plot(t, t, ':', color=GRAY, label='$y=x$')
    ax.plot([1, 0], [0, 1], 'o', color=RED, ms=4); ax.plot([1, 0], [0, 1], ':', color=RED, lw=1)
    ax.legend(loc='lower right', fontsize=9.5); ax.set_title('互为反函数的图像关于 $y=x$ 对称', fontsize=10)
    fig.tight_layout(); save(fig, P + 'inverse_function.png')


def hyperbolic():
    fig, ax = plt.subplots(figsize=(4.2, 3.0)); frame(ax, (-2.5, 2.5), (-3, 3.6))
    x = np.linspace(-2.5, 2.5, 300)
    ax.plot(x, np.cosh(x), color=BLUE, label='$\\cosh x$'); ax.plot(x, np.sinh(x), color=ORANGE, label='$\\sinh x$'); ax.plot(x, np.tanh(x), color=GREEN, label='$\\tanh x$')
    ax.plot(x, np.exp(x) / 2, ':', color=GRAY, lw=1, label='$e^x/2$')
    ax.legend(loc='lower right', fontsize=9.5, ncol=2); ax.set_title('双曲函数', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'hyperbolic.png')


def eps_delta():
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    x = np.linspace(0, 4, 300); f = lambda t: .25 * t ** 2 + .5
    ax.plot(x, f(x), color=BLUE)
    a, L, e = 2, f(2), .45; d = np.sqrt(4 * (L + e - .5)) - a
    ax.axhspan(L - e, L + e, color=ORANGE, alpha=.15); ax.axvspan(a - d, a + d, color=GREEN, alpha=.15)
    ax.axhline(L, color=ORANGE, ls='--', lw=1); ax.axvline(a, color=GREEN, ls='--', lw=1)
    ax.set_xticks([a - d, a, a + d]); ax.set_xticklabels(['$a-\\delta$', '$a$', '$a+\\delta$'])
    ax.set_yticks([L - e, L, L + e]); ax.set_yticklabels(['$A-\\varepsilon$', '$A$', '$A+\\varepsilon$'])
    ax.set_xlim(0, 4); ax.set_ylim(0, 4)
    ax.set_title('先给 $\\varepsilon$，再找 $\\delta$：绿带内的点，函数值都落在橙带内', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'epsilon_delta.png', ticks=False)


def sin_limit():
    fig, ax = plt.subplots(figsize=(3.8, 3.2)); ax.set_aspect('equal'); ax.axis('off')
    x = .75; ax.set_xlim(-.15, 1.35); ax.set_ylim(-.15, 1.15)
    ax.add_patch(Wedge((0, 0), 1, 0, np.degrees(x), fc=LIGHT['blue'], ec=BLUE))
    th = np.linspace(0, 1.5, 100); ax.plot(np.cos(th), np.sin(th), color=GRAY, lw=1)
    ax.add_patch(Polygon([(0, 0), (1, 0), (np.cos(x), np.sin(x))], fc='none', ec=GREEN, lw=1.6))
    ax.add_patch(Polygon([(0, 0), (1, 0), (1, np.tan(x))], fc='none', ec=ORANGE, lw=1.6))
    ax.plot([np.cos(x), np.cos(x)], [0, np.sin(x)], ':', color=GREEN)
    ax.text(.05, .07, '$x$', fontsize=12); ax.text(1.03, np.tan(x) / 2, '$\\tan x$', color=ORANGE); ax.text(np.cos(x) - .2, np.sin(x) / 2, '$\\sin x$', color=GREEN)
    ax.text(-.1, -.12, '三角形 $<$ 扇形 $<$ 大三角形：$\\sin x<x<\\tan x$', fontsize=10)
    save(fig, P + 'sinx_over_x.png', ticks=False)


def asymptotes():
    fig, ax = plt.subplots(figsize=(4.4, 3.2)); frame(ax, (-4, 6), (-6, 10))
    f = lambda t: (t ** 2 + 1) / (t - 1)
    for seg in (np.linspace(-4, .85, 200), np.linspace(1.15, 6, 200)):
        ax.plot(seg, f(seg), color=BLUE)
    ax.axvline(1, color=RED, ls='--', lw=1.1); t = np.linspace(-4, 6, 2); ax.plot(t, t + 1, '--', color=ORANGE, lw=1.1)
    ax.text(1.15, 8.6, '铅直渐近线 $x=1$', color=RED, fontsize=10); ax.text(2.8, 2.0, '斜渐近线\n$y=x+1$', color=ORANGE, fontsize=10)
    ax.set_title('$y=\\dfrac{x^2+1}{x-1}$ 的两条渐近线', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'asymptotes.png')


def ivt():
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    x = np.linspace(0, 4, 300); f = lambda t: .12 * (t - 1.6) ** 3 + .35 * (t - 1.6) + .2
    ax.plot(x, f(x), color=BLUE); ax.axhline(0, color='#9aa3ad', lw=.8)
    from scipy.optimize import brentq
    r = brentq(f, 0, 4); ax.plot([0, 4], [f(0), f(4)], 'o', color=INK, ms=4); ax.plot(r, 0, 'o', color=RED)
    ax.text(0.05, f(0) - .5, '$f(a)<0$', fontsize=10); ax.text(3.3, f(4) - .6, '$f(b)>0$', fontsize=10); ax.text(r + .05, .25, '$\\xi$', color=RED)
    ax.set_xticks([]); ax.set_title('闭区间上连续，端点异号，则中间必有零点', fontsize=10)
    fig.tight_layout(); save(fig, P + 'intermediate_value.png')


def secant():
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    x = np.linspace(0, 3, 200); f = lambda t: .4 * t ** 2 + .3; fp = lambda t: .8 * t
    ax.plot(x, f(x), color=BLUE); x0 = 1
    for h, c in [(1.6, '#c7d0d9'), (1.0, '#9aa8b6'), (.5, '#6b7a89')]:
        k = (f(x0 + h) - f(x0)) / h; ax.plot(x, f(x0) + k * (x - x0), color=c, lw=1); ax.plot(x0 + h, f(x0 + h), 'o', color=c, ms=4)
    ax.plot(x, f(x0) + fp(x0) * (x - x0), color=RED, lw=1.6, label='切线：$h\\to0$ 的极限位置')
    ax.plot(x0, f(x0), 'o', color=INK, ms=5); ax.set_ylim(0, 4); ax.set_xlim(0, 3)
    ax.legend(loc='upper left', fontsize=9.5); ax.set_title('割线斜率 $\\dfrac{f(x+h)-f(x)}{h}$ 趋于切线斜率', fontsize=10)
    fig.tight_layout(); save(fig, P + 'secant_tangent.png')


def shape():
    fig, ax = plt.subplots(figsize=(4.6, 3.0)); frame(ax, (-2.4, 2.4), (-3, 3))
    x = np.linspace(-2.2, 2.2, 300); ax.plot(x, x ** 3 - 3 * x, color=BLUE)
    ax.plot([-1, 1], [2, -2], 'o', color=RED); ax.plot(0, 0, 's', color=GREEN, ms=5)
    ax.text(-1.2, 2.3, '极大', color=RED); ax.text(.85, -2.6, '极小', color=RED); ax.text(.1, .3, '拐点', color=GREEN)
    ax.text(-2.3, -2.6, '$x<0$：凸（$f\'\'<0$）', fontsize=9.5); ax.text(.35, 2.4, '$x>0$：凹（$f\'\'>0$）', fontsize=9.5)
    ax.set_title('$f(x)=x^3-3x$：单调性、极值与凹凸', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'monotone_extrema.png')


def mvt():
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    x = np.linspace(0, 3.2, 300); f = lambda t: np.sin(t) + .3 * t + .5
    a, b = .3, 2.9; k = (f(b) - f(a)) / (b - a)
    from scipy.optimize import brentq
    xi = brentq(lambda t: np.cos(t) + .3 - k, a, 1.6)
    ax.plot(x, f(x), color=BLUE); ax.plot([a, b], [f(a), f(b)], color=GRAY, lw=1.2)
    t = np.linspace(xi - 1.1, xi + 1.1, 2); ax.plot(t, f(xi) + k * (t - xi), color=RED, lw=1.4)
    ax.plot([a, b, xi], [f(a), f(b), f(xi)], 'o', color=INK, ms=4)
    ax.set_xticks([a, xi, b]); ax.set_xticklabels(['$a$', '$\\xi$', '$b$']); ax.set_yticks([])
    ax.set_title('拉格朗日中值定理：某点切线平行于弦', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'mean_value.png', ticks=False)


def riemann():
    fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.6), sharey=True)
    r = lambda t: 2 * t + 1; x = np.linspace(0, 2, 100)
    for ax, n in zip(axs, (4, 16)):
        w = 2 / n
        for i in range(1, n + 1):
            ax.add_patch(Rectangle(((i - 1) * w, 0), w, r(i * w), fc=LIGHT['blue'], ec=BLUE, lw=.6))
        ax.plot(x, r(x), color=RED); s = sum(r(i * w) * w for i in range(1, n + 1))
        ax.set_title(f'$n={n}$：右端点和 $={s:g}$', fontsize=10.5); ax.set_xlim(0, 2.1); ax.set_ylim(0, 5.3)
    fig.text(.5, -.02, '$r(t)=2t+1$，精确值 $\\int_0^2(2t+1)\\,dt=6$', ha='center', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'riemann_sum.png')


def signed_area():
    fig, ax = plt.subplots(figsize=(4.2, 2.6)); frame(ax, (0, 2 * np.pi + .3), (-1.3, 1.3))
    x = np.linspace(0, 1.5 * np.pi, 300); y = np.sin(x)
    ax.fill_between(x, y, where=y >= 0, color=BLUE, alpha=.25); ax.fill_between(x, y, where=y < 0, color=RED, alpha=.25)
    ax.plot(x, y, color=INK, lw=1.4); ax.text(1.3, .35, '$+$', fontsize=16, color=BLUE); ax.text(3.9, -.5, '$-$', fontsize=16, color=RED)
    ax.set_title('$\\int_0^{3\\pi/2}\\sin x\\,dx=2-1=1$：$x$ 轴下方的面积取负', fontsize=10)
    fig.tight_layout(); save(fig, P + 'signed_area.png')


def ftc():
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    x = np.linspace(0, 3, 200); f = lambda t: .5 + .4 * np.sin(1.5 * t) + .25 * t
    ax.plot(x, f(x), color=BLUE); a, X, h = .3, 1.8, .35
    xs = np.linspace(a, X, 100); ax.fill_between(xs, f(xs), color=BLUE, alpha=.18)
    xs = np.linspace(X, X + h, 30); ax.fill_between(xs, f(xs), color=ORANGE, alpha=.5)
    ax.text(1.0, .35, '$\\Phi(x)=\\int_a^x f(t)\\,dt$', ha='center', fontsize=10.5)
    ax.annotate('$\\Phi(x+h)-\\Phi(x)\\approx f(x)\\,h$', xy=(X + h / 2, f(X) * .8), xytext=(2.15, 1.75), fontsize=10, arrowprops=dict(arrowstyle='->', color=ORANGE), color=ORANGE)
    ax.set_xticks([a, X, X + h]); ax.set_xticklabels(['$a$', '$x$', '$x+h$']); ax.set_yticks([]); ax.set_ylim(0, 2.1)
    ax.set_title('累积函数的增量就是一窄条面积', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'accumulation.png', ticks=False)


def revolution():
    fig = plt.figure(figsize=(4.8, 3.2)); ax = fig.add_subplot(projection='3d')
    xs = np.linspace(0, 2, 40); th = np.linspace(0, 2 * np.pi, 50); X, T = np.meshgrid(xs, th)
    R = np.sqrt(X) * .8
    ax.plot_surface(X, R * np.cos(T), R * np.sin(T), color=BLUE, alpha=.15, lw=0)
    x0, dx = 1.2, .12
    for xx in (x0, x0 + dx):
        r = np.sqrt(xx) * .8; ax.plot(xx + 0 * th, r * np.cos(th), r * np.sin(th), color=ORANGE, lw=1.4)
    r = np.sqrt(x0) * .8; Y, Z = r * np.cos(th), r * np.sin(th)
    ax.plot_surface(np.array([x0 + 0 * th, x0 + dx + 0 * th]), np.array([Y, Y]), np.array([Z, Z]), color=ORANGE, alpha=.6)
    ax.plot(xs, np.sqrt(xs) * .8, 0 * xs, color=RED, lw=1.6)
    ax.text(x0, 0, r + .25, '$dV=\\pi f(x)^2\\,dx$', color=ORANGE, fontsize=10.5); ax.text(2.0, 1.2, 0, '$y=f(x)$', color=RED, fontsize=10)
    ax.set_axis_off(); ax.view_init(18, -65); ax.set_box_aspect((2, 1.3, 1.3), zoom=1.3)
    save(fig, P + 'solid_of_revolution.png', ticks=False)


def series():
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    n = np.arange(1, 41)
    ax.plot(n, np.cumsum(1 / n), 'o-', color=RED, ms=2.5, lw=1, label='$\\sum 1/n$：发散，增长如 $\\ln n$')
    ax.plot(n, np.cumsum(1 / n ** 2), 'o-', color=BLUE, ms=2.5, lw=1, label='$\\sum 1/n^2\\to\\pi^2/6$')
    ax.plot(n, np.cumsum((-1) ** (n + 1) / n), 'o-', color=GREEN, ms=2.5, lw=1, label='$\\sum(-1)^{n+1}/n\\to\\ln 2$')
    ax.axhline(np.pi ** 2 / 6, color=BLUE, ls=':', lw=1); ax.axhline(np.log(2), color=GREEN, ls=':', lw=1)
    ax.set_xlabel('项数 $N$'); ax.set_ylabel('部分和 $S_N$'); ax.legend(fontsize=9, loc='upper left')
    fig.tight_layout(); save(fig, P + 'partial_sums.png')


def taylor():
    fig, ax = plt.subplots(figsize=(4.6, 3.0)); frame(ax, (-2 * np.pi, 2 * np.pi), (-2, 2))
    x = np.linspace(-2 * np.pi, 2 * np.pi, 400); ax.plot(x, np.sin(x), color=INK, lw=2.2, label='$\\sin x$')
    from math import factorial
    for k, c in zip((1, 3, 5, 7), (BLUE, GREEN, ORANGE, RED)):
        p = sum((-1) ** j * x ** (2 * j + 1) / factorial(2 * j + 1) for j in range((k + 1) // 2))
        ax.plot(x, p, color=c, lw=1.2, label=f'{k} 阶')
    ax.legend(fontsize=9, ncol=5, loc='upper center', bbox_to_anchor=(.5, 1.15), handlelength=1.2, columnspacing=.8)
    fig.tight_layout(); save(fig, P + 'taylor_sin.png')


def gradient():
    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    x = np.linspace(-2, 2, 200); X, Y = np.meshgrid(x, x); Z = X ** 2 + 2 * Y ** 2
    cs = ax.contour(X, Y, Z, levels=[.5, 1.5, 3, 5], colors=[BLUE], linewidths=1); ax.clabel(cs, fontsize=8, fmt='%g')
    for p in [(1, .5), (-1.2, .6), (.3, -1.1), (-.6, -.9)]:
        g = np.array([2 * p[0], 4 * p[1]]) * .18; ax.annotate('', xy=(p[0] + g[0], p[1] + g[1]), xytext=p, arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.4))
    ax.set_aspect('equal'); ax.set_title('$f=x^2+2y^2$：梯度垂直于等值线，指向增大方向', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'gradient_contours.png')


def lagrange():
    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    x = np.linspace(-.2, 3, 200); X, Y = np.meshgrid(x, x); Z = X * Y
    ax.contour(X, Y, Z, levels=[.5, 1, 1.5625, 2.2, 3], colors=[GRAY], linewidths=.9)
    ax.contour(X, Y, Z, levels=[1.5625], colors=[BLUE], linewidths=1.8)
    ax.plot(x, 2.5 - x, color=ORANGE, lw=1.8); ax.plot(1.25, 1.25, 'o', color=RED)
    ax.annotate('', xy=(1.25 + .45, 1.25 + .45), xytext=(1.25, 1.25), arrowprops=dict(arrowstyle='-|>', color=RED))
    ax.text(1.75, 1.45, '$\\nabla f\\parallel\\nabla g$', color=RED, fontsize=10.5)
    ax.text(2.0, .25, '约束 $x+y=2.5$', color=ORANGE, fontsize=10); ax.text(.1, 2.75, '$f=xy$ 的等值线', color=GRAY, fontsize=10)
    ax.set_xlim(0, 3); ax.set_ylim(0, 3); ax.set_aspect('equal'); ax.set_title('条件极值：等值线与约束曲线相切', fontsize=10)
    fig.tight_layout(); save(fig, P + 'lagrange_multiplier.png')


def slope_field():
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    T, Yv = np.meshgrid(np.linspace(0, 2, 15), np.linspace(-2, 3, 13))
    S = Yv; L = np.sqrt(1 + S ** 2); ax.quiver(T, Yv, 1 / L, S / L, color=GRAY, angles='xy', scale=22, width=.004, headwidth=0, headlength=0, headaxislength=0, pivot='mid')
    t = np.linspace(0, 2, 100)
    for C in (-.5, .3, 1):
        ax.plot(t, C * np.exp(t), color=BLUE, lw=1.4)
    ax.plot(t, np.exp(t), color=RED, lw=2, label='$y(0)=1$：$y=e^t$')
    ax.set_xlim(0, 2); ax.set_ylim(-2, 3); ax.legend(loc='upper left', fontsize=9.5)
    ax.set_title("$y'=y$ 的方向场与积分曲线", fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'slope_field.png')


def rc():
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    a, w, b = 1.0, 3.0, 1.0; t = np.linspace(0, 8, 600)
    steady = b * (a * np.sin(w * t) - w * np.cos(w * t)) / (a * a + w * w)
    q0 = .6; K = q0 + b * w / (a * a + w * w); trans = K * np.exp(-a * t)
    ax.plot(t, steady + trans, color=BLUE, label='$q(t)$')
    ax.plot(t, trans, '--', color=ORANGE, lw=1.2, label='暂态 $Ke^{-at}$'); ax.plot(t, steady, ':', color=GREEN, lw=1.4, label='稳态正弦项')
    ax.axhline(0, color='#9aa3ad', lw=.8); ax.set_xlabel('$t$（示范：$a=1,\\ \\omega=3$）'); ax.legend(fontsize=9, loc='upper right')
    ax.set_title('RC 电路：暂态衰减后只剩稳态', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'rc_transient.png')


def damping():
    fig, ax = plt.subplots(figsize=(4.8, 2.8)); t = np.linspace(0, 10, 500)
    ax.plot(t, np.exp(-.25 * t) * (np.cos(1.97 * t) + .25 / 1.97 * np.sin(1.97 * t)), color=BLUE, label='共轭复根：衰减振荡')
    ax.plot(t, (1 + 2 * t) * np.exp(-2 * t), color=GREEN, label='重根：临界')
    r1, r2 = -.27, -3.73; ax.plot(t, (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r2 - r1), color=ORANGE, label='两个实根：过阻尼')
    ax.axhline(0, color='#9aa3ad', lw=.8); ax.set_xlabel('$t$'); ax.legend(fontsize=9)
    ax.set_title("$y''+py'+qy=0$，$y(0)=1,\\ y'(0)=0$ 的三种情形", fontsize=10)
    fig.tight_layout(); save(fig, P + 'damping_cases.png')


def variation():
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    t = np.linspace(0, 1, 200); y = .3 + .9 * t ** 1.5; eta = np.sin(np.pi * t) * .9
    ax.plot(t, y, color=BLUE, lw=2, label='$y(t)$')
    for e, c in [(.15, ORANGE), (-.12, GREEN)]:
        ax.plot(t, y + e * eta, color=c, lw=1.2, ls='--', label=f'$y+\\varepsilon\\eta$，$\\varepsilon={e:g}$')
    ax.plot([0, 1], [.3, 1.2], 'o', color=INK)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['$t_1$', '$t_2$']); ax.set_yticks([]); ax.legend(fontsize=9, loc='upper left')
    ax.set_title('变分：端点固定，$\\eta(t_1)=\\eta(t_2)=0$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'variation.png', ticks=False)


for f in [transforms, inverse, hyperbolic, eps_delta, sin_limit, asymptotes, ivt, secant, shape, mvt, riemann, signed_area, ftc, revolution, series, taylor, gradient, lagrange, slope_field, rc, damping, variation]:
    f()

place('04_微积分与微分方程.md', [
    ('规律是：改动括号内自变量的变换', P + 'graph_transforms.png', '图像的平移、伸缩与翻折'),
    ('在一个区间上严格单调的函数，可', P + 'inverse_function.png', '指数函数与对数函数互为反函数'),
    ('**双曲函数。**', P + 'hyperbolic.png', '双曲余弦、双曲正弦与双曲正切'),
    ('**柯西定义。**', P + 'epsilon_delta.png', '函数极限的 ε–δ 定义'),
    ('第一个可以用夹逼定理证明', P + 'sinx_over_x.png', '第一个重要极限的面积比较'),
    ('**渐近线。**', P + 'asymptotes.png', '铅直渐近线与斜渐近线'),
    ('介值定理保证', P + 'intermediate_value.png', '零点定理'),
    ('函数在点 \\(x\\) 的导数定', P + 'secant_tangent.png', '导数是割线斜率的极限'),
    ('**凹凸性与拐点。**', P + 'monotone_extrema.png', '由导数符号判断单调、极值与凹凸'),
    ('几何上，曲线上至少有一点的切线', P + 'mean_value.png', '拉格朗日中值定理的几何意义'),
    ('当分段无限细化', P + 'riemann_sum.png', '分段越细，矩形面积和越接近定积分'),
    ('定积分允许被积函数取负值', P + 'signed_area.png', '定积分是有向面积'),
    ('右边是窄条上函数的平均高度', P + 'accumulation.png', '微积分基本定理：累积函数的导数等于被积函数'),
    ('旋转体体积的微元', P + 'solid_of_revolution.png', '旋转体的圆片微元'),
    ('几何级数的有限和', P + 'partial_sums.png', '三个级数的部分和'),
    ('多项式的系数这样选取', P + 'taylor_sin.png', 'sin x 的各阶泰勒多项式'),
    ('梯度把各个偏导数组成一个向量', P + 'gradient_contours.png', '梯度与等值线'),
    ('前两式的几何意义是', P + 'lagrange_multiplier.png', '拉格朗日乘数法的几何意义'),
    ('例如 \\(y\'=y\\)：在', P + 'slope_field.png', '方向场与初值确定的一条积分曲线'),
    ('若 \\(q(0)=q_0\\)', P + 'rc_transient.png', 'RC 电路正弦输入下的暂态与稳态（示范参数）'),
    ('重根时只有一个指数解', P + 'damping_cases.png', '二阶常系数齐次方程三种特征根对应的解'),
    ('比较一条曲线 \\(y\\) 与它', P + 'variation.png', '比较曲线与它的变分'),
])
