# 线性代数册插图（2026-11-20）。运行：py work/figures_02_linalg.py
from figlib import *
from matplotlib.patches import Polygon, Rectangle

style()
P = '02_'


def vec(ax, v, color, label=None, o=(0, 0), off=(0.08, 0.08), lw=1.8, fs=12):
    ax.annotate('', xy=(o[0] + v[0], o[1] + v[1]), xytext=o,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=13, shrinkA=0, shrinkB=0))
    if label:
        ax.text(o[0] + v[0] + off[0], o[1] + v[1] + off[1], label, color=color, fontsize=fs)


def plane(ax, lim=(-1, 4), ylim=None, grid=True):
    ylim = ylim or lim
    ax.set_xlim(*lim); ax.set_ylim(*ylim); ax.set_aspect('equal')
    ax.axhline(0, color='#9aa3ad', lw=.8); ax.axvline(0, color='#9aa3ad', lw=.8)
    if grid:
        ax.grid(color='#eef0f3', lw=.6)
    ax.tick_params(length=2)


# 1 行图与列图
def row_col():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 3.0))
    x = np.linspace(-1, 4, 50)
    plane(a, (-0.5, 4), (-1.2, 3.5))
    a.plot(x, 3 - x, color=BLUE, label='$x+y=3$'); a.plot(x, x - 1, color=ORANGE, label='$x-y=1$')
    a.plot(2, 1, 'o', color=RED); a.text(2.15, 1.2, '解 $(2,1)$', color=RED)
    a.legend(loc='upper right', fontsize=9.5); a.set_title('行图：每个方程是一条直线')
    plane(b, (-0.5, 3.6), (-1.4, 2.6))
    vec(b, (1, 1), BLUE, '$a_1$', off=(-.35, .05)); vec(b, (1, -1), ORANGE, '$a_2$', off=(.05, -.25))
    vec(b, (2, 2), BLUE, None, lw=1.1); vec(b, (1, -1), ORANGE, None, o=(2, 2), lw=1.1)
    vec(b, (3, 1), RED, '$b$', off=(.08, -.05))
    b.text(.55, 1.75, '$2a_1$', color=BLUE); b.text(2.6, 1.75, '$1\\cdot a_2$', color=ORANGE)
    b.set_title('列图：$x a_1+y a_2=b$')
    fig.tight_layout(); save(fig, P + 'row_column.png')


# 2 乘法次序
def order():
    A = np.array([[1, 1], [0, 1]]); B = np.array([[2, 0], [0, 3]])
    sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1]]).T
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.6))
    for ax, M, t, c in [(axs[0], np.eye(2), '单位正方形', GRAY), (axs[1], A @ B, '$AB$：先 $B$ 后 $A$', BLUE), (axs[2], B @ A, '$BA$：先 $A$ 后 $B$', ORANGE)]:
        plane(ax, (-.3, 5.3), (-.3, 3.5))
        pts = M @ sq
        ax.add_patch(Polygon(pts.T, fc=c, alpha=.25, ec=c, lw=1.4))
        ax.set_title(t, fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'product_order.png')


# 3 三种结局
def outcomes():
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.4))
    x = np.linspace(-1, 4, 50)
    cases = [((3 - x), (x - 1), '唯一解：相交'), ((3 - x), (4 - x), '无解：平行'), ((3 - x), (3 - x), '无穷多解：重合')]
    for ax, (y1, y2, t) in zip(axs, cases):
        plane(ax, (-.5, 4), (-1, 4.5))
        ax.plot(x, y1, color=BLUE)
        ax.plot(x, y2, color=ORANGE, ls='--' if t.startswith('无穷') else '-', lw=2.4 if t.startswith('无穷') else 1.8)
        if t.startswith('唯一'):
            ax.plot(2, 1, 'o', color=RED)
        ax.set_title(t, fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'three_outcomes.png')


# 4 列空间与相容性
def colspace():
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    plane(ax, (-.6, 2.4), (-.6, 3.6))
    t = np.linspace(-.3, 1.75, 2)
    ax.plot(t, 2 * t, color=BLUE, lw=5, alpha=.18)
    ax.text(1.25, 2.95, '列空间\n$y=2x$', color=BLUE, fontsize=10)
    vec(ax, (1, 2), BLUE, '$a_1=a_2$', off=(.08, -.25), fs=10.5)
    vec(ax, (1, 3), RED, '$b$', off=(-.25, .05))
    ax.plot([1, 1], [2, 3], ':', color=GRAY)
    ax.set_title('$Ax$ 只能落在直线上，$b$ 不在其中', fontsize=10)
    fig.tight_layout(); save(fig, P + 'column_space.png')


# 5 行列式与面积
def det_area():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.0, 2.9))
    for ax, u, v, t in [(a, (2, .5), (.7, 1.6), '$\\det A=ad-bc$ = 平行四边形面积'), (b, (2, 1), (1, .5), '$\\det A=0$：两列共线，面积为零')]:
        plane(ax, (-.4, 3.2), (-.4, 2.4))
        ax.add_patch(Polygon([(0, 0), u, (u[0] + v[0], u[1] + v[1]), v], fc=BLUE, alpha=.18, ec=BLUE))
        vec(ax, u, BLUE, '$(a,c)$', off=(.05, -.28), fs=10.5); vec(ax, v, ORANGE, '$(b,d)$', off=(-.2, .1), fs=10.5)
        ax.set_title(t, fontsize=10)
    fig.tight_layout(); save(fig, P + 'det_area.png')


# 6 初等行变换求逆
def inverse_rowops():
    fig, ax = canvas(6.0, 1.9, (0, 12), (0, 3.6))
    box(ax, .2, .9, 1.8, 1.8, '$A$', fs=15); box(ax, 2.0, .9, 1.8, 1.8, '$I$', LIGHT['gray'], GRAY, fs=15)
    arrow(ax, (4.1, 1.8), (7.6, 1.8), text='初等行变换\n$E_k\\cdots E_2E_1$', toff=(0, .55), fs=10)
    box(ax, 7.9, .9, 1.8, 1.8, '$I$', LIGHT['gray'], GRAY, fs=15); box(ax, 9.7, .9, 2.0, 1.8, '$A^{-1}$', LIGHT['orange'], ORANGE, fs=15)
    ax.text(3.0, .45, '左块化为 $I$ 时，右块恰为 $E_k\\cdots E_1=A^{-1}$', ha='center', fontsize=10, color=GRAY)
    ax.text(9.8, .45, '$(E_k\\cdots E_1)\\,[A\\mid I]=[I\\mid A^{-1}]$', ha='center', fontsize=10, color=GRAY)
    save(fig, P + 'inverse_rowops.png', ticks=False)


# 7 克莱默法则的面积解释
def cramer():
    a1, a2, x1 = np.array([2, .4]), np.array([.6, 1.5]), 1.5
    b_ = x1 * a1 + .8 * a2
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 3.0))
    for ax in (a, b):
        plane(ax, (-.4, 4.4), (-.4, 2.6))
    a.add_patch(Polygon([(0, 0), a1, a1 + a2, a2], fc=BLUE, alpha=.2, ec=BLUE))
    vec(a, a1, BLUE, '$a_1$', off=(.05, -.3)); vec(a, a2, ORANGE, '$a_2$', off=(-.3, .05))
    a.set_title('$D=\\det(a_1,a_2)$', fontsize=10.5)
    b.add_patch(Polygon([(0, 0), b_, b_ + a2, a2], fc=RED, alpha=.15, ec=RED))
    b.add_patch(Polygon([(0, 0), x1 * a1, x1 * a1 + a2, a2], fc=BLUE, alpha=.12, ec=BLUE, ls='--'))
    vec(b, b_, RED, '$b$', off=(.05, .05)); vec(b, a2, ORANGE, '$a_2$', off=(-.3, .05))
    b.set_title('$D_1=\\det(b,a_2)=x_1D$', fontsize=10.5)
    b.text(2.2, -.32, '沿 $a_2$ 方向错切，面积不变', ha='center', fontsize=9, color=GRAY)
    fig.tight_layout(); save(fig, P + 'cramer_area.png')


# 8 解集结构
def solution_set():
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    plane(ax, (-2.5, 4.5), (-1.5, 3.2))
    t = np.linspace(-3, 5, 2)
    ax.plot(t, -t / 2, color=BLUE, label='$Ax=0$ 的解：$t\\,\\xi$')
    ax.plot(t, 1.5 - t / 2, color=ORANGE, label='$Ax=b$ 的解：$x_p+t\\,\\xi$')
    vec(ax, (0, 1.5), RED, '$x_p$', off=(.1, 0))
    vec(ax, (2, -1), BLUE, '$\\xi$', off=(.05, -.3)); vec(ax, (2, -1), BLUE, None, o=(0, 1.5), lw=1.1)
    ax.legend(loc='upper right', fontsize=9.5)
    ax.set_title('例：$x+2y=3$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'solution_set.png')


# 9 特征向量
def eigen():
    A = np.array([[2, 1], [1, 2]])
    th = np.linspace(0, 2 * np.pi, 200)
    c = np.vstack([np.cos(th), np.sin(th)])
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    plane(ax, (-3.3, 3.3), (-2.6, 2.6))
    ax.plot(*c, color=GRAY, lw=1, ls='--'); ax.plot(*(A @ c), color=BLUE, lw=1.4)
    s = 1 / np.sqrt(2)
    vec(ax, (s, s), GREEN, None); vec(ax, (3 * s, 3 * s), GREEN, '$Av_1=3v_1$', off=(-.2, .12), lw=1.1, fs=10.5)
    vec(ax, (-s, s), PURPLE, '$v_2$', off=(-.35, .05), fs=10.5)
    w = np.array([1, 0]); vec(ax, w, ORANGE, '$w$', off=(0, -.35), fs=10.5); vec(ax, A @ w, ORANGE, '$Aw$', off=(.05, .05), fs=10.5)
    ax.text(-3.1, -2.4, '虚线：单位圆　实线：单位圆的像', fontsize=9, color=GRAY)
    ax.set_title('8.1 节例中的 $A$：$\\lambda_1=3,\\ \\lambda_2=1$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'eigenvectors.png')


# 10 对角化：特征基下只是坐标伸缩
def diagonalize():
    A = np.array([[2, 1], [1, 2]])
    v1, v2 = np.array([1, 1]) / np.sqrt(2), np.array([-1, 1]) / np.sqrt(2)
    fig, axs = plt.subplots(1, 2, figsize=(6.2, 3.0))
    for ax, M, t in [(axs[0], np.eye(2), '特征向量网格'), (axs[1], A, '经 $A$ 作用：沿 $v_1$ 伸 3 倍，沿 $v_2$ 不变')]:
        plane(ax, (-3.2, 3.2), (-3.2, 3.2), grid=False)
        for k in range(-2, 3):
            for d, e, col in [(v1, v2, GREEN), (v2, v1, PURPLE)]:
                p, q = M @ (k * d - 2 * e), M @ (k * d + 2 * e)
                ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=.8, alpha=.6)
        vec(ax, M @ v1, GREEN, '$v_1$' if M is not A else '$3v_1$', fs=10.5)
        vec(ax, M @ v2, PURPLE, '$v_2$', off=(-.4, .05), fs=10.5)
        ax.set_title(t, fontsize=10)
    fig.tight_layout(); save(fig, P + 'diagonalize.png')


# 11 二次型的主轴
def quadform():
    fig, ax = plt.subplots(figsize=(3.8, 3.5))
    x = np.linspace(-2, 2, 300); X, Y = np.meshgrid(x, x)
    Q = 2 * X ** 2 + 2 * X * Y + 2 * Y ** 2
    cs = ax.contour(X, Y, Q, levels=[1, 2, 4, 6], colors=[BLUE], linewidths=1)
    ax.clabel(cs, fontsize=8, fmt='%g')
    ax.set_aspect('equal'); ax.axhline(0, color='#9aa3ad', lw=.8); ax.axvline(0, color='#9aa3ad', lw=.8)
    for d, col, lab in [((1, 1), GREEN, "$y_1$ 轴（$\\lambda=3$）"), ((-1, 1), PURPLE, "$y_2$ 轴（$\\lambda=1$）")]:
        d = np.array(d) / np.sqrt(2)
        ax.plot([-1.9 * d[0], 1.9 * d[0]], [-1.9 * d[1], 1.9 * d[1]], color=col, lw=1.2, ls='--')
        ax.text(1.55 * d[0] - (.95 if d[0] < 0 else -.05), 1.55 * d[1] + .1, lab, color=col, fontsize=9.5)
    ax.set_title('$2x^2+2xy+2y^2=3y_1^2+y_2^2$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'quadratic_form.png')


# 12 格拉姆—施密特
def gram_schmidt():
    v1, v2 = np.array([2.4, .6]), np.array([1.2, 1.8])
    e1 = v1 / np.linalg.norm(v1)
    proj = (v2 @ e1) * e1
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    plane(ax, (-.4, 3.0), (-.3, 2.2))
    vec(ax, v1, BLUE, '$v_1$', off=(.05, -.25)); vec(ax, v2, ORANGE, '$v_2$', off=(-.1, .1))
    vec(ax, proj, GRAY, '投影', off=(-.25, -.3), lw=1.2, fs=10)
    vec(ax, v2 - proj, GREEN, None, o=proj)
    ax.text(1.62, 1.05, '$u_2=v_2-\\mathrm{proj}_{v_1}v_2$', color=GREEN, fontsize=10)
    vec(ax, v2 - proj, GREEN, None, lw=1.1)
    ax.plot([v2[0], proj[0]], [v2[1], proj[1]], ':', color=GRAY)
    sq = .12; n = (v2 - proj) / np.linalg.norm(v2 - proj)
    c = proj; ax.plot([c[0] - sq * e1[0], c[0] - sq * e1[0] + sq * n[0], c[0] + sq * n[0]], [c[1] - sq * e1[1], c[1] - sq * e1[1] + sq * n[1], c[1] + sq * n[1]], color=GRAY, lw=.8)
    ax.set_title('减去在 $v_1$ 上的投影，余下部分与 $v_1$ 正交', fontsize=10)
    fig.tight_layout(); save(fig, P + 'gram_schmidt.png')


# 13 最小二乘的投影图与拟合直线
def least_squares():
    fig = plt.figure(figsize=(6.6, 3.0))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    u, v = np.meshgrid(np.linspace(-1, 1.6, 2), np.linspace(-1, 1.6, 2))
    ax.plot_surface(u, v, 0 * u, color=BLUE, alpha=.15)
    p = np.array([1, .7, 0]); bb = np.array([1, .7, 1.2])
    ax.quiver(0, 0, 0, *bb, color=RED, arrow_length_ratio=.08, lw=1.6)
    ax.quiver(0, 0, 0, *p, color=BLUE, arrow_length_ratio=.1, lw=1.6)
    ax.quiver(*p, *(bb - p), color=GREEN, arrow_length_ratio=.12, lw=1.6)
    ax.text(*(bb + [.05, 0, .05]), '$b$', color=RED); ax.text(*(p + [.05, .05, -.25]), '$A\\hat x$', color=BLUE)
    ax.text(1.05, .75, .55, '$e=b-A\\hat x$', color=GREEN, fontsize=10)
    ax.text(-1, 1.4, 0, '列空间 $C(A)$', color=BLUE, fontsize=10)
    ax.set_xlim(-1, 1.6); ax.set_ylim(-1, 1.6); ax.set_zlim(0, 1.3); ax.view_init(20, -55); ax.set_axis_off(); ax.set_box_aspect((1, 1, .55), zoom=1.35)
    ax.set_title('$e\\perp C(A)$：$A^Te=0$', fontsize=10.5, y=.98)
    ax2 = fig.add_subplot(1, 2, 2)
    t = np.array([0, 1, 2]); y = np.array([1, 2, 2]); fit = 7 / 6 + t / 2
    tt = np.linspace(-.3, 2.3, 2)
    ax2.plot(tt, 7 / 6 + tt / 2, color=BLUE, label='$y=\\frac{7}{6}+\\frac{t}{2}$')
    for a_, b_, c_ in zip(t, y, fit):
        ax2.plot([a_, a_], [b_, c_], color=GREEN, lw=1.4)
    ax2.plot(t, y, 'o', color=RED, label='数据点')
    ax2.set_xlim(-.3, 2.4); ax2.set_ylim(.6, 2.6); ax2.legend(loc='lower right', fontsize=9.5)
    ax2.set_title('绿色竖线为残差 $(-\\frac{1}{6},\\frac{1}{3},-\\frac{1}{6})$', fontsize=10)
    fig.tight_layout(); save(fig, P + 'least_squares.png')


for f in [row_col, order, outcomes, colspace, det_area, inverse_rowops, cramer, solution_set, eigen, diagonalize, quadform, gram_schmidt, least_squares]:
    f()

place('02_线性代数.md', [
    ('线性方程是指未知数只以一次', P + 'row_column.png', '二元方程组的两种看法：行图中两直线交于解，列图中两列按解的分量组合出右端'),
    ('两个结果不同，说明交换乘法', P + 'product_order.png', '乘法次序：AB 与 BA 把单位正方形变成不同的图形'),
    ('一个线性方程组只可能有三种', P + 'three_outcomes.png', '二元线性方程组的三种结局'),
    ('从列的角度看得更清楚', P + 'column_space.png', '列空间与相容性：b 不在 A 的列空间中时方程组无解'),
    ('行列式的几何意义是理解它的', P + 'det_area.png', '二阶行列式是两列张成的平行四边形的有向面积'),
    ('原理如下。每一次初等行变换都相当于在左边', P + 'inverse_rowops.png', '用初等行变换求逆：对增广矩阵 [A | I] 消元'),
    ('这个法则的道理并不复杂', P + 'cramer_area.png', '克莱默法则的面积解释：第一个未知数等于两块平行四边形面积之比'),
    ('非齐次方程组 \\(Ax=b\\) 的解集不', P + 'solution_set.png', '非齐次通解等于特解加齐次通解：解集是把过原点的解空间平移'),
    ('一般来说，矩阵作用在向量上会同时改变向量', P + 'eigenvectors.png', '特征向量经变换后方向不变，只伸缩 λ 倍；一般向量方向改变'),
    ('对角矩阵的作用最简单', P + 'diagonalize.png', '对角化：在特征向量构成的基下，变换只是各坐标分别伸缩'),
    ('正交对角化的一个重要应用是二次型', P + 'quadratic_form.png', '二次型的等值线与主轴：正交变换后交叉项消失'),
    ('给定一组线性无关的向量，常常希望', P + 'gram_schmidt.png', '格拉姆—施密特正交化的一步'),
    ('几何上，\\(Ax\\) 只能取遍', P + 'least_squares.png', '最小二乘：拟合值是 b 在列空间上的正交投影；右图为本节拟合直线的例子'),
])
