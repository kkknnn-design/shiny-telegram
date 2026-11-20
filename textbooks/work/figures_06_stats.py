# 概率统计与实验数据处理册插图（2026-11-20）。运行：py work/figures_06_stats.py
# 模拟数据均为示范数据，固定随机种子以便重现。
from figlib import *
from matplotlib.patches import Circle, Rectangle
from math import comb, factorial, erf

style()
P = '06_'
rng = np.random.default_rng(20261120)
phi = lambda x: np.exp(-x * x / 2) / np.sqrt(2 * np.pi)


def mean_median():
    fig, axs = plt.subplots(2, 1, figsize=(4.8, 2.4), sharex=True)
    base = np.array([2.31, 2.33, 2.34, 2.35, 2.36, 2.36, 2.37, 2.38, 2.40])
    for ax, d, t in [(axs[0], np.append(base, 2.39), '十个读数'), (axs[1], np.append(base, 2.80), '其中一个误记为 2.80')]:
        ax.plot(d, np.zeros_like(d), 'o', color=BLUE, ms=6, alpha=.8)
        ax.axvline(np.mean(d), color=RED, lw=1.4); ax.axvline(np.median(d), color=GREEN, lw=1.4, ls='--')
        ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_title(t, fontsize=10, loc='left')
    axs[0].text(2.55, .02, '红：均值　绿虚线：中位数', fontsize=9.5)
    axs[1].set_xlabel('读数 / s（示范数据）')
    fig.tight_layout(); save(fig, P + 'mean_median.png')


def venn(ax, shade):
    ax.set_xlim(-2, 2); ax.set_ylim(-1.35, 1.35); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((-1.9, -1.25), 3.8, 2.5, fc='white', ec=GRAY))
    x = np.linspace(-2, 2, 400); X, Y = np.meshgrid(x, np.linspace(-1.3, 1.3, 300))
    A = (X + .5) ** 2 + Y ** 2 < 1; B = (X - .5) ** 2 + Y ** 2 < 1
    ax.contourf(X, Y, shade(A, B).astype(float), levels=[.5, 1.5], colors=[BLUE], alpha=.3)
    for cx in (-.5, .5):
        ax.add_patch(Circle((cx, 0), 1, fc='none', ec=INK, lw=1))
    ax.text(-1.15, .75, '$A$', fontsize=12); ax.text(1.0, .75, '$B$', fontsize=12); ax.text(1.55, -1.1, '$\\Omega$', fontsize=11)


def venns():
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 1.9))
    for ax, f, t in [(axs[0], lambda A, B: A | B, '$A\\cup B$'), (axs[1], lambda A, B: A & B, '$A\\cap B$'), (axs[2], lambda A, B: A & ~B, '$A\\setminus B$')]:
        venn(ax, f); ax.set_title(t, fontsize=11)
    fig.tight_layout(); save(fig, P + 'venn.png', ticks=False)


def conditional():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.0))
    venn(axs[0], lambda A, B: B); axs[0].set_title('已知 $B$ 发生：样本空间缩小为 $B$', fontsize=9.5)
    venn(axs[1], lambda A, B: A & B); axs[1].set_title('$P(A\\mid B)=P(A\\cap B)/P(B)$', fontsize=10)
    fig.tight_layout(); save(fig, P + 'conditional.png', ticks=False)


def tree():
    fig, ax = canvas(5.6, 2.8, (0, 10), (0, 5))
    ax.plot(.5, 2.5, 'o', color=INK)
    ys = [4.2, 2.5, .8]
    for i, y in enumerate(ys, 1):
        arrow(ax, (.6, 2.5), (3.6, y), color=BLUE, text=f'$P(B_{i})$', toff=(0, .3), fs=10)
        ax.text(3.8, y, f'$B_{i}$', va='center', fontsize=11, color=BLUE)
        arrow(ax, (4.4, y), (7.2, y), color=ORANGE, text=f'$P(A\\mid B_{i})$', toff=(0, .28), fs=10)
        ax.text(7.35, y, f'$P(B_{i})P(A\\mid B_{i})$', va='center', fontsize=10)
    ax.text(5.0, -.05, '$P(A)=\\sum_i P(B_i)P(A\\mid B_i)$　　贝叶斯：$P(B_j\\mid A)=$ 第 $j$ 枝 / 各枝之和', ha='center', fontsize=9.5)
    save(fig, P + 'probability_tree.png', ticks=False)


def histogram():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 2.6))
    edges = np.array([0, 1, 2, 3, 5, 8]); counts = np.array([6, 14, 12, 12, 6]); w = np.diff(edges); N = counts.sum()
    a.bar(edges[:-1], counts, width=w, align='edge', fc=LIGHT['red'], ec=RED); a.set_title('按频数画：宽组显得过高', fontsize=10)
    b.bar(edges[:-1], counts / (N * w), width=w, align='edge', fc=LIGHT['blue'], ec=BLUE); b.set_title('按频率密度画：面积 = 频率', fontsize=10)
    for ax in (a, b):
        ax.set_xlabel('取值（示范数据，$N=50$）')
    a.set_ylabel('频数'); b.set_ylabel('频率 / 组宽')
    fig.tight_layout(); save(fig, P + 'histogram_density.png')


def pdf_cdf():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 2.5)); x = np.linspace(0, 4, 300); lam = 1.2
    f = lam * np.exp(-lam * x); F = 1 - np.exp(-lam * x); x1, x2 = .5, 1.5
    a.plot(x, f, color=BLUE); m = (x >= x1) & (x <= x2); a.fill_between(x[m], f[m], color=BLUE, alpha=.25)
    a.text(1.0, .25, '面积\n$=F(x_2)-F(x_1)$', ha='center', fontsize=9.5); a.set_title('密度 $f(x)$', fontsize=10.5)
    b.plot(x, F, color=ORANGE); Fa, Fb = 1 - np.exp(-lam * x1), 1 - np.exp(-lam * x2)
    b.plot([x1, x1, 0], [0, Fa, Fa], ':', color=GRAY); b.plot([x2, x2, 0], [0, Fb, Fb], ':', color=GRAY)
    b.annotate('', xy=(.15, Fb), xytext=(.15, Fa), arrowprops=dict(arrowstyle='<->', color=BLUE)); b.set_title('分布函数 $F(x)=\\int_{-\\infty}^x f$', fontsize=10.5)
    for ax in (a, b):
        ax.set_xticks([x1, x2]); ax.set_xticklabels(['$x_1$', '$x_2$'])
    fig.tight_layout(); save(fig, P + 'pdf_cdf.png', ticks=False)


def binomial():
    fig, ax = plt.subplots(figsize=(4.6, 2.7)); n = 10; k = np.arange(n + 1)
    for p, c, off in [(.2, BLUE, -.2), (.5, ORANGE, .2)]:
        ax.bar(k + off, [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in k], width=.38, color=c, alpha=.85, label=f'$p={p}$')
    ax.set_xticks(k); ax.set_xlabel('成功次数 $k$'); ax.set_ylabel('$P(X=k)$'); ax.legend(fontsize=9.5)
    ax.set_title('二项分布 $B(10,p)$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'binomial.png')


def poisson_exp():
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.2, 2.5)); k = np.arange(0, 11)
    for lam, c, off in [(1, BLUE, -.2), (4, ORANGE, .2)]:
        a.bar(k + off, [lam ** i * np.exp(-lam) / factorial(i) for i in k], width=.38, color=c, label=f'$\\lambda={lam}$')
    a.legend(fontsize=9.5); a.set_xlabel('时段内次数 $k$'); a.set_title('泊松分布：次数', fontsize=10.5)
    t = np.linspace(0, 4, 300)
    for lam, c in [(1, BLUE), (4, ORANGE)]:
        b.plot(t, lam * np.exp(-lam * t), color=c, label=f'$\\lambda={lam}$')
    b.set_ylim(0, 2.2); b.legend(fontsize=9.5); b.set_xlabel('等待时间 $t$'); b.set_title('指数分布：等待时间', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'poisson_exponential.png')


def normal_rule():
    fig, ax = plt.subplots(figsize=(4.8, 2.7)); x = np.linspace(-4, 4, 400); ax.plot(x, phi(x), color=INK)
    for k, c in [(3, '#e5ecf4'), (2, '#c5d6ea'), (1, '#9ab9dc')]:
        m = abs(x) <= k; ax.fill_between(x[m], phi(x[m]), color=c)
    for k, txt, y in [(1, '68.3%', .2), (2, '95.4%', .06), (3, '99.7%', .012)]:
        ax.annotate('', xy=(-k, y), xytext=(k, y), arrowprops=dict(arrowstyle='<->', color=INK, lw=.8)); ax.text(0, y + .012, txt, ha='center', fontsize=9.5)
    ax.set_xticks(range(-3, 4)); ax.set_xticklabels(['$\\mu-3\\sigma$', '', '$\\mu-\\sigma$', '$\\mu$', '$\\mu+\\sigma$', '', '$\\mu+3\\sigma$']); ax.set_yticks([])
    ax.set_title('正态分布：$\\mu\\pm k\\sigma$ 内的概率', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'normal_rule.png', ticks=False)


def binom_normal():
    fig, ax = plt.subplots(figsize=(4.6, 2.7)); n, p = 100, .5; k = np.arange(30, 71)
    ax.bar(k, [comb(n, i) * p ** n for i in k], width=1, fc=LIGHT['blue'], ec=BLUE, lw=.5, label='$B(100,\\,0.5)$')
    x = np.linspace(30, 70, 300); s = np.sqrt(n * p * (1 - p)); ax.plot(x, phi((x - 50) / s) / s, color=RED, label='$N(50,\\,5^2)$')
    ax.set_xlabel('正面次数'); ax.legend(fontsize=9.5); ax.set_title('二项分布的正态近似', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'binomial_normal.png')


def clt():
    fig, axs = plt.subplots(1, 4, figsize=(6.6, 2.0), sharey=False)
    for ax, n in zip(axs, (1, 2, 5, 30)):
        m = rng.exponential(1, size=(20000, n)).mean(axis=1)
        ax.hist(m, bins=50, density=True, color=LIGHT['blue'], ec=BLUE, lw=.3)
        if n >= 5:
            x = np.linspace(m.min(), m.max(), 200); s = 1 / np.sqrt(n); ax.plot(x, phi((x - 1) / s) / s, color=RED, lw=1.2)
        ax.set_title(f'$n={n}$', fontsize=10.5); ax.set_yticks([]); ax.set_xlim(0, 4 if n < 5 else 2.2)
    fig.text(.5, -.04, '指数分布总体的 $n$ 个样本均值（模拟 20000 次）；红线为正态近似', ha='center', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'central_limit.png')


def lln():
    fig, ax = plt.subplots(figsize=(4.8, 2.6)); n = np.arange(1, 2001)
    for i, c in enumerate((BLUE, ORANGE, GREEN)):
        ax.plot(n, np.cumsum(rng.random(2000) < .5) / n, color=c, lw=1)
    ax.axhline(.5, color=RED, ls='--', lw=1); ax.set_xscale('log'); ax.set_ylim(0, 1)
    ax.set_xlabel('试验次数 $n$（对数刻度）'); ax.set_ylabel('正面频率'); ax.set_title('大数定律：频率随 $n$ 增大而稳定在概率附近', fontsize=10)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:g}$'))
    fig.tight_layout(); save(fig, P + 'law_of_large_numbers.png', ticks=False)


def correlation():
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.2))
    for ax, r in zip(axs, (.9, 0, -.6)):
        z = rng.multivariate_normal([0, 0], [[1, r], [r, 1]], 150); ax.plot(z[:, 0], z[:, 1], 'o', ms=2.5, color=BLUE, alpha=.7)
        ax.set_title(f'$\\rho={r:g}$', fontsize=11); ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)
    fig.tight_layout(); save(fig, P + 'correlation.png')


def standard_error():
    fig, ax = plt.subplots(figsize=(4.6, 2.6)); x = np.linspace(-3.5, 3.5, 400); N = 9
    ax.plot(x, phi(x), color=BLUE, label='单次读数：标准差 $\\sigma$')
    s = 1 / np.sqrt(N); ax.plot(x, phi(x / s) / s, color=RED, label='9 次均值：$\\sigma/\\sqrt{9}=\\sigma/3$')
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels(['$-\\sigma$', '$\\mu$', '$\\sigma$']); ax.set_yticks([]); ax.legend(fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'standard_error.png', ticks=False)


def student_t():
    fig, ax = plt.subplots(figsize=(4.6, 2.7)); x = np.linspace(-4.5, 4.5, 400)
    from scipy.stats import t as T
    ax.plot(x, phi(x), color=INK, lw=2, label='标准正态')
    for nu, c in [(1, RED), (4, ORANGE), (9, GREEN)]:
        ax.plot(x, T.pdf(x, nu), color=c, lw=1.3, label=f'$t$，$\\nu={nu}$')
    ax.legend(fontsize=9); ax.set_title('自由度越小，$t$ 分布尾部越厚', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'student_t.png')


def ci():
    fig, ax = plt.subplots(figsize=(4.8, 3.0)); mu, sig, N = 10, 1, 8
    from scipy.stats import t as T
    tc = T.ppf(.95, N - 1)
    for i in range(25):
        d = rng.normal(mu, sig, N); m, se = d.mean(), d.std(ddof=1) / np.sqrt(N)
        hit = abs(m - mu) <= tc * se; c = BLUE if hit else RED
        ax.plot([m - tc * se, m + tc * se], [i, i], color=c, lw=1.6); ax.plot(m, i, 'o', color=c, ms=3)
    ax.axvline(mu, color=INK, ls='--', lw=1); ax.set_yticks([]); ax.set_xlabel('真值 $\\mu=10$（虚线）')
    ax.set_title('25 组模拟样本的 90% 区间：约九成覆盖真值（红色未覆盖）', fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'confidence_intervals.png')


def accuracy():
    fig, axs = plt.subplots(1, 4, figsize=(6.6, 1.9))
    cases = [(0, 0, .12, '随机小、系统小'), (0, 0, .4, '随机大'), (.5, .35, .12, '系统偏移'), (.5, .35, .4, '两者都大')]
    for ax, (dx, dy, s, t) in zip(axs, cases):
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect('equal'); ax.axis('off')
        for r in (1, .66, .33):
            ax.add_patch(Circle((0, 0), r, fc='none', ec=GRAY, lw=.8))
        z = rng.normal(0, s, (12, 2)) + [dx, dy]; ax.plot(z[:, 0], z[:, 1], 'o', color=RED, ms=3)
        ax.set_title(t, fontsize=9.5)
    fig.tight_layout(); save(fig, P + 'random_systematic.png')


def uniform_u():
    fig, ax = plt.subplots(figsize=(4.4, 2.4)); a = 1
    ax.plot([-1.6, -a, -a, a, a, 1.6], [0, 0, .5, .5, 0, 0], color=BLUE)
    ax.fill_between([-a / np.sqrt(3), a / np.sqrt(3)], .5, color=BLUE, alpha=.18)
    ax.set_xticks([-a, -a / np.sqrt(3), 0, a / np.sqrt(3), a]); ax.set_xticklabels(['$-a$', '$-u$', '$0$', '$u$', '$a$']); ax.set_yticks([.5]); ax.set_yticklabels(['$\\dfrac{1}{2a}$'])
    ax.set_ylim(0, .7); ax.set_title('均匀分布的标准不确定度 $u=a/\\sqrt{3}$', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'uniform_uncertainty.png', ticks=False)


def linefit():
    fig, ax = plt.subplots(figsize=(4.6, 2.9)); n = np.arange(1, 8); y = 8.6 * n + 1.2 + rng.normal(0, .9, 7)
    A = np.vstack([np.ones_like(n), n]).T; (a0, b0), *_ = np.linalg.lstsq(A, y, rcond=None)
    xx = np.linspace(.5, 7.5, 2); ax.plot(xx, a0 + b0 * xx, color=BLUE, label=f'$y={a0:.1f}+{b0:.2f}\\,n$')
    for xi, yi in zip(n, y):
        ax.plot([xi, xi], [yi, a0 + b0 * xi], color=GREEN, lw=1.2)
    ax.plot(n, y, 'o', color=RED, label='测量点（示范）'); ax.set_xlabel('谐振序号 $n$'); ax.set_ylabel('位置 / cm'); ax.legend(fontsize=9.5)
    ax.set_title('最小二乘：使残差（绿线）平方和最小', fontsize=10.5)
    fig.tight_layout(); save(fig, P + 'line_fit.png')


def standing_wave():
    fig, ax = plt.subplots(figsize=(5.4, 2.0)); lam = 2.0; x = np.linspace(0, 3 * lam / 2 + .2, 400)
    for ph in np.linspace(0, np.pi, 5):
        ax.plot(x, np.cos(2 * np.pi * x / lam) * np.cos(ph), color=BLUE, lw=.8, alpha=.6)
    for k in range(4):
        ax.axvline(k * lam / 2, color=RED, ls=':', lw=1)
    ax.annotate('', xy=(lam / 2, -1.25), xytext=(lam, -1.25), arrowprops=dict(arrowstyle='<->', color=INK)); ax.text(3 * lam / 4, -1.15, '$\\lambda/2$', ha='center', fontsize=10.5)
    ax.set_ylim(-1.5, 1.3); ax.set_yticks([]); ax.set_xticks([]); ax.set_title('驻波：相邻谐振位置相差半个波长', fontsize=10.5)
    ax.spines['left'].set_visible(False)
    fig.tight_layout(); save(fig, P + 'standing_wave.png')


for f in [mean_median, venns, conditional, tree, histogram, pdf_cdf, binomial, poisson_exp, normal_rule, binom_normal, clt, lln, correlation, standard_error, student_t, ci, accuracy, uniform_u, linefit, standing_wave]:
    f()

place('06_概率统计与实验数据处理.md', [
    ('均值对极端值敏感', P + 'mean_median.png', '一个异常读数对均值和中位数的不同影响（示范数据）'),
    ('减去交集是因为同时属于两事件', P + 'venn.png', '事件的并、交与差'),
    ('在 \\(P(B)>0\\) 时，', P + 'conditional.png', '条件概率：在 B 内看 A 所占的比例'),
    ('右边每项先描述某一种情况', P + 'probability_tree.png', '全概率公式与贝叶斯公式的树形图'),
    ('**例3：不等宽组的直方图。', P + 'histogram_density.png', '不等宽分组时应画频率密度'),
    ('例如 X 在区间 \\([0,2', P + 'pdf_cdf.png', '密度曲线下的面积与分布函数的增量'),
    ('组合数计数成功发生位置', P + 'binomial.png', '二项分布'),
    ('所以 \\(F_T(t)=1-e', P + 'poisson_exponential.png', '泊松过程中的次数分布与等待时间分布'),
    ('其中 \\(\\Phi\\) 是标准', P + 'normal_rule.png', '正态分布在一、二、三倍标准差内的概率'),
    ('**二项分布的正态近似。**', P + 'binomial_normal.png', '二项分布的正态近似'),
    ('中心极限定理主要讨论', P + 'central_limit.png', '中心极限定理：样本均值的分布随 n 增大趋于正态'),
    ('这就是大数定律', P + 'law_of_large_numbers.png', '三次模拟掷硬币的频率变化'),
    ('当两者标准差均正，相关系数为', P + 'correlation.png', '不同相关系数下的散点'),
    ('因此均值标准误差常估计为', P + 'standard_error.png', '单次读数与均值的分散程度'),
    ('服从自由度 \\(\\nu=N-1', P + 'student_t.png', 'Student t 分布与标准正态分布'),
    ('频率学置信区间的意思是', P + 'confidence_intervals.png', '置信区间的频率解释（模拟）'),
    ('随机影响使重复读数波动，系统影', P + 'random_systematic.png', '随机影响与系统影响'),
    ('若仅知道未知偏移在 \\([-a', P + 'uniform_uncertainty.png', '只知界限时按均匀分布估计标准不确定度'),
    ('拟合的好坏和参数的不确定度', P + 'line_fit.png', '最小二乘直线拟合（示范数据）'),
    ('波速、频率和波长满足', P + 'standing_wave.png', '相邻谐振位置与半波长'),
])
