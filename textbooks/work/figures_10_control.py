# 自动控制与仿真册插图（2026-11-20）。运行：py work/figures_10_control.py
from figlib import *
from matplotlib.patches import Circle, Rectangle, Polygon

style()
P = '10_'


def summer(ax, x, y, r=.32, signs=('+', '−')):
    ax.add_patch(Circle((x, y), r, fc='white', ec=INK, lw=1.2))
    ax.plot([x - r * .7, x + r * .7], [y - r * .7, y + r * .7], color=INK, lw=.8); ax.plot([x - r * .7, x + r * .7], [y + r * .7, y - r * .7], color=INK, lw=.8)
    ax.text(x - r - .25, y + .22, '$+$', fontsize=10); ax.text(x + .08, y - r - .42, '$-$', fontsize=11)


def system_boundary():
    fig, ax = canvas(6.2, 2.4, (0, 16), (0, 6))
    box(ax, 5.5, 2.0, 4.0, 2.0, '对象\n（水箱）', LIGHT['blue'], BLUE, fs=11)
    arrow(ax, (1.0, 3.0), (5.5, 3.0), text='输入 $u$\n（泵电压、进流）', toff=(0, .7), fs=10)
    arrow(ax, (7.5, 5.6), (7.5, 4.0), color=RED, text='扰动 $d$', toff=(1.1, .3), fs=10)
    arrow(ax, (9.5, 3.0), (14.5, 3.0), text='输出 $y$（液位）', toff=(0, .4), fs=10)
    ax.add_patch(Rectangle((4.8, 1.2), 5.4, 3.6, fc='none', ec=GRAY, ls='--', lw=1)); ax.text(5.0, .75, '系统边界：状态 $x$ 记录对象的“记忆”', fontsize=9.5, color=GRAY)
    save(fig, P + 'system_boundary.png', ticks=False)


def tank():
    fig, ax = canvas(4.0, 3.0, (0, 8), (0, 6))
    ax.plot([2, 2, 6, 6], [5.2, .8, .8, 5.2], color=INK, lw=2)
    ax.add_patch(Rectangle((2, .8), 4, 2.6, fc=LIGHT['blue'], ec='none'))
    ax.plot([2, 6], [3.4, 3.4], color=BLUE, lw=1.4)
    arrow(ax, (.2, 5.0), (3.2, 5.0), color=BLUE, lw=2); ax.plot([3.2, 3.2], [5.0, 3.6], color=BLUE, lw=2, ls=':'); ax.text(.3, 5.35, '$q_{in}=u$', fontsize=11)
    ax.plot([6, 6.6], [1.1, 1.1], color=INK, lw=6, solid_capstyle='butt'); arrow(ax, (6.6, 1.1), (7.9, 1.1), color=BLUE, lw=2); ax.text(6.5, 1.5, '$q_{out}\\approx kh$', fontsize=11)
    ax.annotate('', xy=(1.5, 3.4), xytext=(1.5, .8), arrowprops=dict(arrowstyle='<->', color=RED)); ax.text(1.0, 2.1, '$h$', color=RED, fontsize=12)
    ax.text(4, 2.0, '截面积 $A$', ha='center', fontsize=10.5)
    ax.text(4, .2, '$A\\dot h=q_{in}-q_{out}$', ha='center', fontsize=11)
    save(fig, P + 'tank.png', ticks=False)


def first_order():
    fig, ax = plt.subplots(figsize=(4.6, 2.8)); tau, hinf = 20, .2; t = np.linspace(0, 100, 400)
    ax.plot(t, hinf * (1 - np.exp(-t / tau)), color=BLUE)
    ax.plot([0, tau], [0, hinf], ':', color=GRAY); ax.axhline(hinf, color=GRAY, ls='--', lw=1)
    ax.plot([tau, tau, 0], [0, .632 * hinf, .632 * hinf], ':', color=RED); ax.plot(tau, .632 * hinf, 'o', color=RED)
    ax.text(tau + 2, .632 * hinf - .02, '$t=\\tau$ 时达到 63.2%', color=RED, fontsize=10)
    ax.text(60, hinf + .007, '$h_\\infty=u/k=0.20$ m', fontsize=10)
    ax.set_xlabel('$t$ / s'); ax.set_ylabel('$h$ / m'); ax.set_ylim(0, .23)
    ax.set_title('一阶系统阶跃响应（$\\tau=A/k=20$ s）', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'first_order_step.png')


def zi_zs():
    fig, ax = plt.subplots(figsize=(4.6, 2.7)); t = np.linspace(0, 3, 300); y0, u = 1.5, 1
    zi = y0 * np.exp(-2 * t); zs = u / 2 * (1 - np.exp(-2 * t))
    ax.plot(t, zi + zs, color=INK, lw=2, label='全响应'); ax.plot(t, zi, '--', color=BLUE, label='零输入响应'); ax.plot(t, zs, '--', color=ORANGE, label='零状态响应')
    ax.set_xlabel('$t$'); ax.legend(fontsize=9.5); ax.set_title("$\\dot y+2y=u$，$y(0)=1.5$，$u=1$", fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'zero_input_state.png')


def block_algebra():
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 1.9))
    for ax in axs:
        ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.set_aspect('equal'); ax.axis('off')
    a = axs[0]; box(a, 2, 2, 2.2, 1.2, '$G_1$', fs=11); box(a, 5.6, 2, 2.2, 1.2, '$G_2$', fs=11)
    arrow(a, (.3, 2.6), (2, 2.6)); arrow(a, (4.2, 2.6), (5.6, 2.6)); arrow(a, (7.8, 2.6), (9.6, 2.6)); a.set_title('串联：$G_1G_2$', fontsize=10)
    b = axs[1]; box(b, 3.4, 3.2, 2.2, 1.1, '$G_1$', fs=11); box(b, 3.4, .9, 2.2, 1.1, '$G_2$', fs=11)
    wire(b, (.6, 2.6), (2.2, 2.6)); wire(b, (2.2, 3.75), (2.2, 1.45)); arrow(b, (2.2, 3.75), (3.4, 3.75)); arrow(b, (2.2, 1.45), (3.4, 1.45))
    wire(b, (5.6, 3.75), (7.0, 3.75), (7.0, 2.95)); wire(b, (5.6, 1.45), (7.0, 1.45), (7.0, 2.25)); b.add_patch(Circle((7.0, 2.6), .35, fc='white', ec=INK)); b.text(7.0, 2.6, '$+$', ha='center', va='center', fontsize=9)
    arrow(b, (7.35, 2.6), (9.4, 2.6)); b.set_title('并联：$G_1+G_2$', fontsize=10)
    c = axs[2]; summer(c, 1.8, 3.2); box(c, 3.6, 2.6, 2.4, 1.2, '$G$', fs=11); box(c, 3.6, .6, 2.4, 1.1, '$H$', LIGHT['gray'], GRAY, fs=11)
    arrow(c, (.2, 3.2), (1.45, 3.2)); arrow(c, (2.15, 3.2), (3.6, 3.2)); wire(c, (6.0, 3.2), (9.6, 3.2)); arrow(c, (8.2, 3.2), (9.6, 3.2))
    wire(c, (8.2, 3.2), (8.2, 1.15), (6.0, 1.15)); wire(c, (3.6, 1.15), (1.8, 1.15)); arrow(c, (1.8, 1.15), (1.8, 2.85))
    c.set_title('负反馈：$\\dfrac{G}{1+GH}$', fontsize=10)
    fig.tight_layout(); save(fig, P + 'block_algebra.png', ticks=False)


def second_order():
    fig, ax = plt.subplots(figsize=(4.8, 2.9)); t = np.linspace(0, 12, 600); wn = 1
    for z, c in [(.2, RED), (.5, ORANGE), (.7, GREEN), (1.0, BLUE), (2.0, PURPLE)]:
        if z < 1:
            wd = wn * np.sqrt(1 - z * z); y = 1 - np.exp(-z * wn * t) * (np.cos(wd * t) + z / np.sqrt(1 - z * z) * np.sin(wd * t))
        elif z == 1:
            y = 1 - np.exp(-t) * (1 + t)
        else:
            r1, r2 = -z + np.sqrt(z * z - 1), -z - np.sqrt(z * z - 1); y = 1 + (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r1 - r2)
        ax.plot(t, y, color=c, label=f'$\\zeta={z:g}$')
    ax.axhline(1, color=GRAY, ls='--', lw=1); z = .5; Mp = np.exp(-np.pi * z / np.sqrt(1 - z * z)); tp = np.pi / np.sqrt(1 - z * z)
    ax.annotate(f'超调 {Mp * 100:.0f}%', xy=(tp, 1 + Mp), xytext=(tp + 1.5, 1.45), fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle='->', color=ORANGE))
    ax.set_xlabel('$\\omega_n t$'); ax.legend(fontsize=9, ncol=2, loc='lower right'); ax.set_ylim(0, 1.65)
    ax.set_title('标准二阶环节的单位阶跃响应', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'second_order_step.png')


def feedback_loop():
    fig, ax = canvas(6.4, 2.2, (0, 17), (0, 5.6))
    summer(ax, 2.6, 3.4); box(ax, 4.4, 2.8, 2.6, 1.2, '控制器 $C$', LIGHT['orange'], ORANGE, fs=10.5); box(ax, 9.4, 2.8, 2.6, 1.2, '对象 $G$', fs=10.5)
    ax.add_patch(Circle((13.4, 3.4), .32, fc='white', ec=INK)); ax.text(13.4, 3.4, '$+$', ha='center', va='center', fontsize=9)
    arrow(ax, (.4, 3.4), (2.25, 3.4), text='$r$', toff=(-.6, .3)); arrow(ax, (2.95, 3.4), (4.4, 3.4), text='$e$', toff=(0, .3))
    arrow(ax, (7.0, 3.4), (9.4, 3.4), text='$u$', toff=(0, .3)); arrow(ax, (12.0, 3.4), (13.05, 3.4)); arrow(ax, (13.4, 5.2), (13.4, 3.75), color=RED, text='$d$', toff=(.4, .3))
    arrow(ax, (13.75, 3.4), (16.6, 3.4), text='$y$', toff=(.6, .3)); wire(ax, (15.4, 3.4), (15.4, 1.0), (2.6, 1.0)); arrow(ax, (2.6, 1.0), (2.6, 3.05))
    ax.text(9.0, .45, '测量', fontsize=9.5, color=GRAY)
    save(fig, P + 'feedback_loop.png', ticks=False)


def p_control():
    fig, ax = plt.subplots(figsize=(4.6, 2.8)); tau = 2; t = np.linspace(0, 6, 400)
    for K, c in [(1, BLUE), (3, ORANGE), (9, GREEN)]:
        yi = K / (1 + K); ax.plot(t, yi * (1 - np.exp(-(1 + K) * t / tau)), color=c, label=f'$K_p={K}$：终值 {yi:.2f}')
    ax.axhline(1, color=GRAY, ls='--', lw=1); ax.text(4.3, 1.02, '目标 $r=1$', fontsize=9.5)
    ax.annotate('', xy=(5.6, .75), xytext=(5.6, 1.0), arrowprops=dict(arrowstyle='<->', color=RED)); ax.text(5.65, .86, '稳态误差', color=RED, fontsize=9)
    ax.set_xlabel('$t$ / s'); ax.legend(fontsize=9, loc='lower right'); ax.set_ylim(0, 1.15)
    ax.set_title('比例控制 $G=1/(2s+1)$：增益越大越快，但仍有误差', fontsize=10)
    fig.tight_layout(); save(fig, P + 'proportional_control.png')


def pi_control():
    fig, ax = plt.subplots(figsize=(4.6, 2.7)); t = np.linspace(0, 8, 400)
    ax.plot(t, .5 * (1 - np.exp(-2 * t)), color=ORANGE, label='P：$K_p=1$，终值 0.5')
    ax.plot(t, 1 - np.exp(-t) * (1 + t) + t * np.exp(-t), color=BLUE, label='PI：$K_p=K_i=1$，终值 1')
    ax.axhline(1, color=GRAY, ls='--', lw=1); ax.set_xlabel('$t$'); ax.legend(fontsize=9.5, loc='lower right'); ax.set_ylim(0, 1.15)
    ax.set_title("对象 $\\dot y=-y+u$：积分作用消除稳态误差", fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'pi_control.png')


def membership():
    fig, ax = plt.subplots(figsize=(4.8, 2.5)); x = np.linspace(0, 10, 500)
    tri = np.clip(np.minimum((x - 1) / 2, (5 - x) / 2), 0, 1)
    gauss = np.exp(-(x - 7) ** 2 / (2 * .9 ** 2))
    ax.plot(x, tri, color=BLUE, label='三角形'); ax.plot(x, np.clip(np.minimum((x - 3.5) / 1.5, (9.5 - x) / 1.5), 0, 1), color=ORANGE, label='梯形')
    ax.plot(x, gauss, color=GREEN, label='高斯形')
    ax.set_ylim(0, 1.15); ax.set_ylabel('隶属度 $\\mu$'); ax.legend(fontsize=9.5, ncol=3, loc='upper center', bbox_to_anchor=(.5, 1.2))
    fig.tight_layout(); save(fig, P + 'membership_functions.png')


def mamdani():
    fig, axs = plt.subplots(2, 3, figsize=(6.4, 3.0), gridspec_kw={'width_ratios': [1, 1, 1.2]})
    x = np.linspace(-1, 1, 400); out = np.linspace(-1, 1, 400)
    tri = lambda v, a, b, c: np.clip(np.minimum((v - a) / (b - a), (c - v) / (c - b)), 0, 1)
    e0, de0 = .3, -.2
    rules = [((-.2, .4, 1.0), (-1, -.4, .2), (0, .5, 1.0)), ((-.6, 0, .6), (-.6, 0, .6), (-.5, 0, .5))]
    agg = np.zeros_like(out)
    for r, (A, B, C) in enumerate(rules):
        a, b, c = axs[r]
        a.plot(x, tri(x, *A), color=BLUE); a.axvline(e0, color=RED, lw=1); m1 = tri(np.array(e0), *A); a.axhline(m1, color=RED, ls=':', lw=1)
        b.plot(x, tri(x, *B), color=BLUE); b.axvline(de0, color=RED, lw=1); m2 = tri(np.array(de0), *B); b.axhline(m2, color=RED, ls=':', lw=1)
        w = min(m1, m2); clipped = np.minimum(tri(out, *C), w); agg = np.maximum(agg, clipped)
        c.plot(out, tri(out, *C), color=GRAY, lw=1); c.fill_between(out, clipped, color=ORANGE, alpha=.5)
        c.text(-.95, .8, f'强度 $\\min={w:.2f}$', fontsize=8.5)
        for ax in (a, b, c):
            ax.set_ylim(0, 1.1); ax.set_yticks([]); ax.set_xticks([]); ax.spines['left'].set_visible(False)
        a.set_ylabel(f'规则 {r + 1}', fontsize=9.5)
    axs[0][0].set_title('误差 $e$', fontsize=10); axs[0][1].set_title('误差变化 $\\dot e$', fontsize=10); axs[0][2].set_title('输出（削顶）', fontsize=10)
    cen = (agg * out).sum() / agg.sum()
    axs[1][2].plot(out, agg, color=INK, lw=1.2); axs[1][2].axvline(cen, color=GREEN, lw=1.6); axs[1][2].text(cen + .05, 1.0, f'重心 {cen:.2f}', color=GREEN, fontsize=8.5)
    fig.tight_layout(); save(fig, P + 'mamdani_inference.png', ticks=False)


def partitions():
    fig, ax = plt.subplots(figsize=(5.0, 2.0)); x = np.linspace(-3.4, 3.4, 600); names = ['NB', 'NM', 'NS', 'ZO', 'PS', 'PM', 'PB']
    for i, n in enumerate(names):
        c = i - 3; y = np.clip(1 - abs(x - c), 0, 1)
        if i == 0:
            y = np.where(x < c, 1, y)
        if i == 6:
            y = np.where(x > c, 1, y)
        ax.plot(x, y, color=plt.cm.coolwarm(i / 6), lw=1.6); ax.text(c, 1.07, n, ha='center', fontsize=9.5)
    ax.axvline(.4, color=GRAY, ls=':', lw=1); ax.text(.45, .25, '任一输入最多属于\n相邻两个词，隶属度和为 1', fontsize=9)
    ax.set_ylim(0, 1.2); ax.set_yticks([0, 1]); ax.set_xticks(range(-3, 4)); ax.set_xlabel('归一化误差 $e$')
    fig.tight_layout(); save(fig, P + 'fuzzy_partition.png')


def linearize():
    fig, ax = plt.subplots(figsize=(4.4, 2.8)); h = np.linspace(0, 2, 300); c = 1; h0 = 1
    ax.plot(h, c * np.sqrt(h), color=BLUE, label='$q_{out}=c\\sqrt{h}$')
    ax.plot(h, c * np.sqrt(h0) + c / (2 * np.sqrt(h0)) * (h - h0), '--', color=RED, label='在 $h_0$ 处的切线')
    ax.plot(h0, c, 'o', color=RED); ax.set_xlabel('$h$'); ax.set_ylabel('$q_{out}$'); ax.legend(fontsize=9.5, loc='lower right')
    ax.set_title('局部线性化：工作点附近用切线代替曲线', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'linearization.png')


def euler():
    fig, ax = plt.subplots(figsize=(4.8, 2.8)); a = 10; T = 1.0; t = np.linspace(0, T, 400)
    ax.plot(t, np.exp(-a * t), color=INK, lw=2, label='精确解 $e^{-10t}$')
    for dt, c in [(.05, BLUE), (.15, ORANGE), (.22, RED)]:
        n = int(T / dt) + 1; tt = np.arange(n) * dt; y = (1 - a * dt) ** np.arange(n)
        ax.plot(tt, y, 'o-', color=c, ms=3, lw=1, label=f'欧拉 $\\Delta t={dt}$')
    ax.set_ylim(-1.6, 1.6); ax.axhline(0, color='#9aa3ad', lw=.8); ax.set_xlabel('$t$'); ax.legend(fontsize=9, ncol=2, loc='lower right')
    ax.set_title('$\\dot y=-10y$：$\\Delta t>0.2$ 时显式欧拉法发散', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'euler_stability.png')


def bouncing():
    fig, ax = plt.subplots(figsize=(5.0, 2.8)); g, e, h0 = 9.81, .8, 25
    t0, v = np.sqrt(2 * h0 / g), np.sqrt(2 * g * h0); T = [0]; H = []
    tt = np.linspace(0, t0, 100); ax.plot(tt, h0 - g * tt ** 2 / 2, color=BLUE)
    ts = [t0]
    for k in range(8):
        v *= e; dur = 2 * v / g; tt = np.linspace(0, dur, 100); ax.plot(ts[-1] + tt, v * tt - g * tt ** 2 / 2, color=BLUE); ts.append(ts[-1] + dur)
    ax.plot(ts[:5], [0] * 5, 'o', color=RED, ms=4)
    ax.text(t0 + .1, 1.2, '$t_1\\approx2.26$ s', fontsize=9.5, color=RED); ax.axhline(16, color=GRAY, ls=':', lw=1); ax.text(10, 16.6, '$e^2h_0=16$ m', fontsize=9.5)
    tinf = t0 + 2 * np.sqrt(2 * h0 / g) * e / (1 - e); ax.axvline(tinf, color=PURPLE, ls='--', lw=1); ax.text(tinf - .2, 21, f'累积时刻\n$\\approx{tinf:.1f}$ s', color=PURPLE, fontsize=9.5, ha='right')
    ax.set_xlabel('$t$ / s'); ax.set_ylabel('$h$ / m'); ax.set_title('弹跳球：$h_0=25$ m，$e=0.8$（解析解）', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'bouncing_ball.png')


def event_location():
    fig, ax = plt.subplots(figsize=(4.6, 2.6)); g = 9.81; t = np.linspace(2.0, 2.45, 200); h = 25 - g * t ** 2 / 2
    ax.plot(t, h, color=BLUE, lw=1.4, label='真实轨迹'); ax.axhline(0, color=INK, lw=.8)
    tk, tk1 = 2.1, 2.35; hk, hk1 = 25 - g * tk ** 2 / 2, 25 - g * tk1 ** 2 / 2
    ax.plot([tk, tk1], [hk, hk1], 'o', color=ORANGE); ax.plot([tk, tk1], [hk, hk1], ':', color=ORANGE)
    ts = np.sqrt(50 / g); ax.plot(ts, 0, 's', color=RED); ax.text(ts - .02, .35, '事件时刻 $t^*$', color=RED, fontsize=10, ha='right')
    ax.text(tk + .005, hk + .25, '$h_k>0$', fontsize=10, color=ORANGE); ax.text(tk1 - .1, hk1 - .45, '$h_{k+1}<0$', fontsize=10, color=ORANGE)
    ax.set_xlabel('$t$ / s'); ax.set_ylabel('$h$ / m'); ax.set_title('步长两端变号：在步内求零点，回到 $t^*$ 再重置速度', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'event_location.png')


for f in [system_boundary, tank, first_order, zi_zs, block_algebra, second_order, feedback_loop, p_control, pi_control, membership, mamdani, partitions, linearize, euler, bouncing, event_location]:
    f()

place('10_自动控制与仿真.md', [
    ('把水箱作为对象，泵电压', P + 'system_boundary.png', '对象、输入、扰动与输出'),
    ('先看水箱的体积守恒', P + 'tank.png', '水箱的体积守恒'),
    ('经过一个时间常数，液位达到最', P + 'first_order_step.png', '一阶系统的阶跃响应与时间常数'),
    ('还可以把解分成零输入与零状态', P + 'zero_input_state.png', '全响应 = 零输入响应 + 零状态响应'),
    ('串联两个环节时', P + 'block_algebra.png', '框图的串联、并联与反馈'),
    ('例如 \\(\\zeta=0.5', P + 'second_order_step.png', '阻尼比对二阶阶跃响应的影响'),
    ('开环系统按预定输入运行，闭环', P + 'feedback_loop.png', '单位负反馈回路'),
    ('取 \\(\\tau=2\\,\\m', P + 'proportional_control.png', '比例控制的速度与稳态误差'),
    ('例如被控对象 \\(\\dot', P + 'pi_control.png', '比例控制与比例积分控制的比较'),
    ('连续论域上常用三种参数化的隶', P + 'membership_functions.png', '三种常用隶属函数'),
    ('规则库至少要使每个输出词语都', P + 'mamdani_inference.png', '两条规则的模糊推理：取小、削顶、合成与重心解模糊（示意）'),
    ('相邻词语的三角形隶属函数两两', P + 'fuzzy_partition.png', '七个语言值的三角形划分'),
    ('这是偏差变量的线性方程', P + 'linearization.png', '非线性出流在工作点处的线性化'),
    ('它利用起点斜率外推整个步长', P + 'euler_stability.png', '显式欧拉法的步长与稳定性'),
    ('第一次碰撞后的第 \\(k\\)', P + 'bouncing_ball.png', '弹跳球高度随时间的变化'),
    ('在积分步的两端发现高度由正变', P + 'event_location.png', '事件定位'),
])
