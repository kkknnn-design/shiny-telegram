# 生成大学物理册第 14 章“狭义相对论力学”的静态插图（2026-10-28 增补）。
# 输出到 outputs/教材/figures/，由 build_pdf.py 与 render_books.mjs 按 ![标题](figures/文件名) 引用。
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/教材/figures'
OUT.mkdir(parents=True, exist_ok=True)
font_manager.fontManager.addfont('C:/Windows/Fonts/simsun.ttc')
plt.rcParams.update({'font.family': ['SimSun'], 'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
                     'font.size': 10, 'savefig.dpi': 300})
ORANGE, PURPLE, GREEN, GRAY, BLUE, RED = '#d9822b', '#7b5ea7', '#3c8d5a', '#6b7280', '#3b6ea8', '#b8433a'
V = 0.6  # 示意用相对速度 v/c


def save(fig, name):
    # 坐标刻度用 STIX 数字，避免宋体数字中小数点后的空隙
    from matplotlib.ticker import FuncFormatter
    for ax in fig.axes:
        if ax.axison:
            for axis in (ax.xaxis, ax.yaxis):
                axis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:g}$'))
    fig.savefig(OUT / name, bbox_inches='tight', pad_inches=0.04, facecolor='white')
    plt.close(fig)


def arrow(ax, p, q, color='k', lw=1.2, ms=10, ls='-'):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=ms, color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0))


def mirror(ax, x, y, w, h, angle=0, color='#3d556b'):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, angle=angle, rotation_point='center',
                           fc='#c9d6e3', ec=color, lw=1))


# 图 14-1：迈克耳孙干涉仪与以太系中垂直臂的光路
def fig_michelson():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.9), gridspec_kw={'width_ratios': [1.05, 1]})
    ax = axs[0]; ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((-2.3, -0.18), 0.35, 0.36, fc='#fde6c8', ec=ORANGE)); ax.text(-2.12, -0.42, '光源 S', ha='center', fontsize=8)
    mirror(ax, 0, 0, 0.7, 0.07, angle=45); ax.text(-0.95, -0.42, '半透镜', fontsize=8)
    mirror(ax, 0.9, 0, 0.5, 0.07, angle=45, color=GRAY); ax.text(0.62, -0.45, '补偿板', fontsize=8, color=GRAY)
    mirror(ax, 0, 1.9, 0.8, 0.09); ax.text(0.5, 1.88, '镜 1', fontsize=8)
    mirror(ax, 2.1, 0, 0.09, 0.8); ax.text(2.2, 0.45, '镜 2', fontsize=8)
    ax.plot([-1.95, 2.05], [0, 0], color=RED, lw=1.1); ax.plot([0, 0], [0, 1.85], color=BLUE, lw=1.1)
    ax.plot([0, 0], [0, -1.3], color='k', lw=1.0, ls='--')
    ax.add_patch(Rectangle((-0.25, -1.65), 0.5, 0.35, fc='white', ec='k')); ax.text(0.35, -1.55, '观察筒', fontsize=8)
    ax.text(-0.42, 0.95, '$L$', color=BLUE)
    ax.text(-0.9, 1.45, '垂直臂', color=BLUE, fontsize=8); ax.text(1.15, 0.15, '平行臂 $L$', color=RED, fontsize=8)
    arrow(ax, (1.2, -1.0), (2.1, -1.0), GREEN); ax.text(1.15, -1.6, '装置相对“以太”\n的速度 $v$', fontsize=8, color=GREEN)
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-1.8, 2.2); ax.set_title('(a) 装置示意', fontsize=9)

    ax = axs[1]; ax.set_aspect('equal'); ax.axis('off')
    d = 1.0  # 单程中镜子平移 v t⊥/2（示意）
    for x0, a in ((0, 1), (d, .55), (2 * d, .3)):
        ax.plot([x0 - .25, x0 + .25], [0, 0], color='#3d556b', lw=2, alpha=a)
        ax.plot([x0 - .25, x0 + .25], [1.6, 1.6], color='#3d556b', lw=2, alpha=a)
    ax.plot([0, d, 2 * d], [0, 1.6, 0], color=BLUE, lw=1.3)
    ax.plot([d, d], [0, 1.6], color=GRAY, lw=.8, ls=':')
    ax.annotate('', (d, -0.2), (0, -0.2), arrowprops=dict(arrowstyle='<->', lw=.8))
    ax.text(d / 2, -0.45, r'$\frac{v t_\perp}{2}$', ha='center')
    ax.text(d + 0.08, 0.75, '$L$'); ax.text(0.1, 0.95, r'$\frac{c t_\perp}{2}$', color=BLUE)
    arrow(ax, (0.2, 2.0), (1.2, 2.0), GREEN); ax.text(1.3, 1.95, '$v$', color=GREEN)
    ax.text(d, -0.95, '镜子随装置移动，光须斜行才能追上', ha='center', fontsize=8)
    ax.set_xlim(-0.5, 2.6); ax.set_ylim(-1.1, 2.3); ax.set_title('(b) 以太系中垂直臂的光路', fontsize=9)
    save(fig, '05_rel_michelson.png')


# 图 14-2：光钟在静止系与运动系中的光路
def fig_light_clock():
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.6), gridspec_kw={'width_ratios': [0.6, 1.4]})
    ax = axs[0]; ax.set_aspect('equal'); ax.axis('off')
    for y in (0, 1.6):
        ax.plot([-.35, .35], [y, y], color='#3d556b', lw=2.2)
    arrow(ax, (-.08, 0.05), (-.08, 1.55), BLUE); arrow(ax, (.08, 1.55), (.08, 0.05), BLUE)
    ax.text(0.2, 0.75, '$L$'); ax.text(0, -0.45, r'$\Delta t_0=2L/c$', ha='center')
    ax.set_xlim(-0.8, 0.8); ax.set_ylim(-0.7, 1.9); ax.set_title('(a) 与钟相对静止', fontsize=9)

    ax = axs[1]; ax.set_aspect('equal'); ax.axis('off')
    h = 1.2
    for x0, a in ((0, 1), (h, .55), (2 * h, .3)):
        ax.plot([x0 - .3, x0 + .3], [0, 0], color='#3d556b', lw=2.2, alpha=a)
        ax.plot([x0 - .3, x0 + .3], [1.6, 1.6], color='#3d556b', lw=2.2, alpha=a)
    ax.plot([0, h, 2 * h], [0, 1.6, 0], color=BLUE, lw=1.3)
    ax.add_patch(Polygon([[0, 0], [h, 0], [h, 1.6]], closed=True, fc='#e8eef6', ec='none', zorder=0))
    ax.plot([h, h], [0, 1.6], color=GRAY, lw=.8, ls=':')
    ax.text(h / 2, -0.35, r'$v\,\Delta t/2$', ha='center'); ax.text(h + 0.08, 0.75, '$L$')
    ax.text(0.15, 1.0, r'$c\,\Delta t/2$', color=BLUE)
    arrow(ax, (1.9, 1.9), (2.8, 1.9), GREEN); ax.text(2.9, 1.85, '$v$', color=GREEN)
    ax.text(h, -0.75, r'观察者 A：$\Delta t=\gamma_v\,\Delta t_0$', ha='center')
    ax.set_xlim(-0.5, 3.2); ax.set_ylim(-0.95, 2.2); ax.set_title('(b) 钟以速度 $v$ 运动', fontsize=9)
    save(fig, '05_rel_light_clock.png')


def st_axes(ax, lim=4.2):
    ax.set_aspect('equal'); ax.axis('off')
    arrow(ax, (-0.3, 0), (lim, 0), 'k', 1.0); arrow(ax, (0, -0.3), (0, lim), 'k', 1.0)
    ax.text(lim, -0.3, '$x$'); ax.text(-0.35, lim, '$ct$')


# 图 14-3：时空图中的 S' 坐标轴与同时性
def fig_minkowski():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 3.2))
    ax = axs[0]; st_axes(ax)
    L = 4.0
    ax.plot([0, L], [0, L], color=ORANGE, lw=1, ls='--'); ax.text(3.2, 3.6, '光线 $x=ct$', color=ORANGE, fontsize=8)
    arrow(ax, (0, 0), (V * L, L), BLUE, 1.2); ax.text(V * L + 0.05, L - 0.1, "$ct'$", color=BLUE)
    arrow(ax, (0, 0), (L, V * L), BLUE, 1.2); ax.text(L - 0.1, V * L + 0.15, "$x'$", color=BLUE)
    for k in (1, 2):  # S' 的同时线 ct' = 常数 平行于 x' 轴
        t0 = k * 1.2
        xs = np.array([0, 3.6]); ax.plot(xs, t0 + V * xs, color=BLUE, lw=.6, ls=':')
    ax.text(2.2, 0.35, "点线：$S'$ 中的同时线\n（平行于 $x'$ 轴）", color=BLUE, fontsize=7.5)
    ax.set_xlim(-0.5, 4.6); ax.set_ylim(-0.6, 4.5)
    ax.set_title("(a) $S'$ 的轴在 $S$ 的时空图中（$v=0.6c$）", fontsize=9)

    ax = axs[1]; st_axes(ax)
    A, B = (0.8, 1.6), (3.2, 1.6)
    ax.plot([0, 4], [1.6, 1.6], color=GRAY, lw=.8, ls='--'); ax.text(3.35, 1.75, '$S$ 中同时', fontsize=8, color=GRAY)
    for (x, t), name in ((A, '事件 A'), (B, '事件 B')):
        ax.plot(x, t, 'o', color=RED, ms=5); ax.text(x - 0.25, t - 0.42, name, fontsize=8, color=RED)
        xs = np.array([max(0, x - 1.6), min(4.2, x + 1.0)]); ax.plot(xs, t + V * (xs - x), color=BLUE, lw=.9)
    ax.text(1.0, 3.6, "过 A、B 的 $S'$ 同时线不重合：\n在 $S'$ 中 A 晚于 B",
            fontsize=7.5, color=BLUE)
    ax.set_xlim(-0.5, 4.6); ax.set_ylim(-0.6, 4.5)
    ax.set_title('(b) 同时性的相对性', fontsize=9)
    save(fig, '05_rel_minkowski.png')


# 图 14-4：车库系中的杆与车库（4 m，v=0.6c，长度单位 m，ct 也以 m 计）
def fig_garage():
    fig, ax = plt.subplots(figsize=(4.6, 3.5)); ax.set_aspect('equal'); ax.axis('off')
    arrow(ax, (-3.2, 0), (6.5, 0), 'k', 1.0); arrow(ax, (-3.0, -3.0), (-3.0, 3.6), 'k', 1.0)
    ax.text(6.5, -0.4, '$x$/m'); ax.text(-3.4, 3.7, '$ct$/m')
    ax.axvspan(0, 4, color='#eef2f6'); ax.plot([0, 0], [-3, 3.4], color='#3d556b', lw=1.4)
    ax.plot([4, 4], [-3, 3.4], color='#3d556b', lw=1.4)
    ax.text(0.05, 3.45, '库门', fontsize=8); ax.text(4.05, 3.45, '后墙', fontsize=8)
    ct = np.linspace(-3, 3.4, 2)
    ax.plot(V * ct, ct, color=RED, lw=1.3); ax.plot(4 + V * ct, ct, color=RED, lw=1.3)
    ax.text(-1.95, -2.8, '杆尾', color=RED, fontsize=8); ax.text(2.4, -2.8, '杆头', color=RED, fontsize=8)
    ax.plot([0, 4], [0, 0], color=RED, lw=3, alpha=.35)
    ax.plot(0, 0, 'o', color='k', ms=4); ax.plot(4, 0, 'o', color='k', ms=4)
    ax.text(-1.6, 0.25, '尾进门', fontsize=8); ax.text(4.2, -0.45, '头到墙', fontsize=8)
    xs = np.array([-1.5, 5.5]); ax.plot(xs, V * xs, color=BLUE, lw=.9, ls='--')
    ax.text(5.4, -1.9, '虚线：杆系中与“尾进门”\n同时的事件（此刻杆头\n早已越过后墙）', color=BLUE, fontsize=7.5, ha='center')
    ax.set_xlim(-3.6, 6.9); ax.set_ylim(-3.2, 4.3)
    ax.set_title('车库系时空图：两端事件在车库系同时，在杆系不同时', fontsize=9)
    save(fig, '05_rel_garage.png')


# 图 14-5：光锥与间隔的分类
def fig_light_cone():
    fig, ax = plt.subplots(figsize=(4.0, 3.4)); ax.set_aspect('equal'); ax.axis('off')
    L = 2.6
    ax.fill([-L, 0, L], [L, 0, L], color='#e6f0e9'); ax.fill([-L, 0, L], [-L, 0, -L], color='#e6f0e9')
    ax.plot([-L, L], [-L, L], color=ORANGE, lw=1); ax.plot([-L, L], [L, -L], color=ORANGE, lw=1)
    arrow(ax, (-2.9, 0), (2.9, 0), GRAY, .8); arrow(ax, (0, -2.9), (0, 2.9), GRAY, .8)
    ax.text(2.9, -0.3, '$x$'); ax.text(-0.35, 2.85, '$ct$')
    ax.text(-0.9, 1.8, '类时：未来\n$\\Delta s^2>0$', ha='center', fontsize=8, color=GREEN)
    ax.text(0, -2.1, '类时：过去', ha='center', fontsize=8, color=GREEN)
    ax.text(1.9, 0.35, '类空\n$\\Delta s^2<0$', ha='center', fontsize=8, color=PURPLE)
    ax.text(-1.9, 0.35, '类空', ha='center', fontsize=8, color=PURPLE)
    ax.text(2.0, 2.4, '光锥 $\\Delta s^2=0$', fontsize=8, color=ORANGE)
    t = np.linspace(0, 2.4, 50); ax.plot(0.5 * np.sin(1.3 * t), t, color=BLUE, lw=1.2)
    ax.text(0.55, 1.05, '粒子世界线', fontsize=7.5, color=BLUE)
    ax.plot(0, 0, 'ko', ms=4); ax.text(0.12, -0.3, 'O', fontsize=8)
    ax.set_xlim(-3.1, 3.3); ax.set_ylim(-2.95, 3.05)
    ax.set_title('以事件 O 为顶点的光锥', fontsize=9)
    save(fig, '05_rel_light_cone.png')


# 图 14-6：恒力加速，从静止开始
def fig_const_force():
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    tau = np.linspace(0, 6, 300)
    ax.plot(tau, tau / np.sqrt(1 + tau ** 2), color=BLUE, lw=1.6, label='相对论 $v=\\dfrac{Ft/m}{\\sqrt{1+(Ft/mc)^2}}$')
    ax.plot(tau[tau <= 1.6], tau[tau <= 1.6], color=GRAY, lw=1.2, ls='--', label='牛顿 $v=Ft/m$')
    ax.axhline(1, color=ORANGE, lw=.9, ls=':'); ax.text(4.3, 1.03, '$v=c$', color=ORANGE)
    ax.plot(7.02 / 1.0, 0.99, alpha=0)
    ax.set_xlabel('$Ft/(mc)$'); ax.set_ylabel('$v/c$'); ax.set_xlim(0, 6); ax.set_ylim(0, 1.25)
    ax.legend(loc='lower right', fontsize=8, frameon=False)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    save(fig, '05_rel_const_force.png')


# 图 14-7：能量—动量双曲线
def fig_energy_momentum():
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    pc = np.linspace(0, 3, 300)
    ax.plot(pc, np.sqrt(pc ** 2 + 1), color=BLUE, lw=1.6, label='$E=\\sqrt{p^2c^2+m^2c^4}$')
    ax.plot(pc, pc, color=ORANGE, lw=1.1, ls='--', label='$E=pc$（无质量粒子，渐近线）')
    ax.plot(pc[pc <= 1.6], 1 + pc[pc <= 1.6] ** 2 / 2, color=GRAY, lw=1.1, ls=':', label='牛顿 $E\\approx mc^2+p^2/2m$')
    p6 = 0.75; ax.plot(p6, 1.25, 'o', color=RED, ms=4); ax.text(p6 - 0.45, 1.4, '$v=0.6c$', color=RED, fontsize=8)
    ax.text(0.05, 1.08, '$mc^2$', fontsize=8)
    ax.set_xlabel('$pc/(mc^2)$'); ax.set_ylabel('$E/(mc^2)$'); ax.set_xlim(0, 3); ax.set_ylim(0, 3.4)
    ax.legend(loc='upper left', fontsize=7.5, frameon=False)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    save(fig, '05_rel_energy_momentum.png')


# 图 14-8：速度与动能的关系，贝尔托齐实验点
def fig_bertozzi():
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    T = np.linspace(0, 6, 400)
    ax.plot(T, 1 - 1 / (1 + T) ** 2, color=BLUE, lw=1.6, label='相对论 $v^2/c^2=1-(1+T/mc^2)^{-2}$')
    Tc = T[2 * T <= 1.45]; ax.plot(Tc, 2 * Tc, color=GRAY, lw=1.2, ls='--', label='牛顿 $v^2/c^2=2T/mc^2$')
    ax.axhline(1, color=ORANGE, lw=.9, ls=':'); ax.text(5.0, 1.03, '$v=c$', color=ORANGE)
    Tb = 0.5 / 0.511; ax.plot(Tb, 0.87 ** 2, 's', color=RED, ms=5)
    ax.text(Tb + 0.15, 0.62, '实验点：$T=0.5$ MeV，\n$v\\approx0.87c$', color=RED, fontsize=8)
    ax.set_xlabel('$T/(mc^2)$'); ax.set_ylabel('$v^2/c^2$'); ax.set_xlim(0, 6); ax.set_ylim(0, 1.45)
    ax.legend(loc='lower right', fontsize=8, frameon=False)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    save(fig, '05_rel_bertozzi.png')


if __name__ == '__main__':
    fig_michelson(); fig_light_clock(); fig_minkowski(); fig_garage(); fig_light_cone()
    fig_const_force(); fig_energy_momentum(); fig_bertozzi()
    print('ok')
