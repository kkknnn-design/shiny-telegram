# 俄语册插图（2026-11-20）。运行：py work/figures_09_russian.py
# 俄文用 Times New Roman（含西里尔字母），中文用宋体。
from figlib import *
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge, Arc

style()
plt.rcParams['font.family'] = ['Times New Roman', 'SimSun']  # 俄文用 Times，中文回退宋体
P = '09_'
RU = ['Times New Roman', 'SimSun']


def ru(ax, x, y, s, **kw):
    kw.setdefault('fontsize', 11)
    return ax.text(x, y, s, family=RU, **kw)


def cases():
    fig, ax = canvas(6.4, 2.6, (0, 15), (0, 6))
    data = [('一 主格', 'кто? что?', 'студент', BLUE), ('二 属格', 'кого? чего?', 'студента', GREEN), ('三 与格', 'кому? чему?', 'студенту', ORANGE),
            ('四 宾格', 'кого? что?', 'студента', RED), ('五 工具格', 'кем? чем?', 'студентом', PURPLE), ('六 前置格', 'о ком? о чём?', 'о студенте', GRAY)]
    for i, (name, q, form, c) in enumerate(data):
        x, y = .2 + (i % 3) * 5.0, 3.2 - (i // 3) * 3.0
        box(ax, x, y, 4.6, 2.5, '', LIGHT.get({BLUE: 'blue', GREEN: 'green', ORANGE: 'orange', RED: 'red', PURPLE: 'purple', GRAY: 'gray'}[c]), c)
        ax.text(x + 2.3, y + 2.0, name, ha='center', fontsize=11, color=c)
        ru(ax, x + 2.3, y + 1.2, q, ha='center', fontsize=12)
        ru(ax, x + 2.3, y + .45, form, ha='center', fontsize=11.5, style='italic', color=INK)
    save(fig, P + 'six_cases.png', ticks=False)


def sentence():
    fig, ax = canvas(6.2, 2.2, (0, 15), (0, 5))
    words = [('Новый', 'какой?', '定语', GREEN, 'wave'), ('студент', '', '主语', BLUE, 'single'), ('внимательно', 'как?', '状语', ORANGE, 'dashdot'),
             ('слушает', '', '谓语', RED, 'double'), ('лекцию.', 'что?', '补语', PURPLE, 'dash')]
    x = .3
    for w, q, role, c, line in words:
        width = len(w) * .3 + .55
        ru(ax, x, 2.5, w, fontsize=14)
        xs = np.linspace(x, x + width - .3, 60); y0 = 2.15
        if line == 'single':
            ax.plot(xs, 0 * xs + y0, color=c, lw=1.6)
        elif line == 'double':
            ax.plot(xs, 0 * xs + y0, color=c, lw=1.4); ax.plot(xs, 0 * xs + y0 - .15, color=c, lw=1.4)
        elif line == 'wave':
            ax.plot(xs, y0 + .07 * np.sin(xs * 14), color=c, lw=1.4)
        elif line == 'dash':
            ax.plot(xs, 0 * xs + y0, color=c, lw=1.6, ls='--')
        else:
            ax.plot(xs, 0 * xs + y0, color=c, lw=1.6, ls='-.')
        ax.text(x + (width - .3) / 2, 1.4, role, ha='center', fontsize=10.5, color=c)
        if q:
            ru(ax, x + (width - .3) / 2, 3.5, q, ha='center', fontsize=10.5, color=c, style='italic')
        x += width
    arrow(ax, (1.7, 3.3), (2.4, 3.0), color=GREEN, lw=.8, rad=-.3)
    ax.text(7.5, .3, '主语单线、谓语双线、定语波浪线、补语虚线、状语点划线', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'sentence_parts.png', ticks=False)


def devoicing():
    fig, ax = canvas(6.0, 2.4, (0, 14), (0, 5.6))
    pairs = [('б', 'п'), ('в', 'ф'), ('г', 'к'), ('д', 'т'), ('ж', 'ш'), ('з', 'с')]
    ax.text(.2, 4.95, '浊', fontsize=11, color=BLUE); ax.text(.2, 3.75, '清', fontsize=11, color=RED)
    for i, (v, u) in enumerate(pairs):
        x = 1.2 + i * 1.1
        box(ax, x, 4.6, .8, .8, '', LIGHT['blue'], BLUE); ru(ax, x + .4, 5.0, v, ha='center', va='center', fontsize=14)
        box(ax, x, 3.4, .8, .8, '', LIGHT['red'], RED); ru(ax, x + .4, 3.8, u, ha='center', va='center', fontsize=14)
        arrow(ax, (x + .4, 4.55), (x + .4, 4.25), color=GRAY, lw=1)
    ax.text(4.5, 2.8, '词末浊辅音读成对应的清辅音', ha='center', fontsize=10.5)
    for i, (w, s) in enumerate([('хлеб', '[хлеп]'), ('город', '[горат]'), ('друг', '[друк]')]):
        x = 8.4 + i * 1.95
        ru(ax, x, 4.6, w, ha='center', fontsize=13); arrow(ax, (x, 4.3), (x, 3.7), color=RED, lw=1); ru(ax, x, 3.3, s, ha='center', fontsize=12, color=RED)
    for i, (w, s) in enumerate([('водка', '[вотка]'), ('сделать', '[зделать]')]):
        x = 3.0 + i * 5.2
        ru(ax, x, 1.6, w, ha='center', fontsize=13); arrow(ax, (x + .9, 1.7), (x + 1.7, 1.7), color=PURPLE, lw=1); ru(ax, x + 2.7, 1.6, s, ha='center', fontsize=12, color=PURPLE)
    ax.text(7.0, .5, '辅音连缀中，前一个辅音随后一个辅音同化（清化或浊化）', ha='center', fontsize=10, color=PURPLE)
    save(fig, P + 'devoicing.png', ticks=False)


def house(ax, x, y, w=2.4, h=1.8, label=''):
    ax.add_patch(Rectangle((x, y), w, h, fc='#f3f4f6', ec=GRAY, lw=1.2))
    ax.add_patch(Polygon([(x - .2, y + h), (x + w / 2, y + h + 1.0), (x + w + .2, y + h)], fc='#e5e7eb', ec=GRAY, lw=1.2))
    if label:
        ax.text(x + w / 2, y - .35, label, ha='center', fontsize=9.5, color=GRAY)


def v_na():
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.4))
    for ax in axs:
        ax.set_xlim(0, 6); ax.set_ylim(0, 4.4); ax.set_aspect('equal'); ax.axis('off')
    house(axs[0], 1.8, .8); axs[0].add_patch(Circle((3.0, 1.5), .3, fc=ORANGE))
    ru(axs[0], 3.0, 3.9, 'в доме', ha='center', fontsize=13); axs[0].text(3.0, .25, '在内部：в + 前置格', ha='center', fontsize=10)
    axs[1].add_patch(Rectangle((1.6, 1.0), 2.8, .3, fc='#d6c7a8', ec=GRAY)); axs[1].plot([1.9, 1.9], [0, 1.0], color=GRAY, lw=2); axs[1].plot([4.1, 4.1], [0, 1.0], color=GRAY, lw=2)
    axs[1].add_patch(Rectangle((2.7, 1.3), .6, .7, fc=LIGHT['blue'], ec=BLUE))
    ru(axs[1], 3.0, 3.9, 'на столе', ha='center', fontsize=13); axs[1].text(3.0, -.3, '在表面上：на + 前置格', ha='center', fontsize=10)
    fig.tight_layout(); save(fig, P + 'v_na.png', ticks=False)


def three_way():
    fig, ax = canvas(6.4, 2.4, (0, 16), (0, 6))
    house(ax, 6.6, 1.2, 2.8, 2.2, 'университет')
    arrow(ax, (1.0, 2.3), (6.4, 2.3), color=BLUE, lw=2); arrow(ax, (9.6, 2.3), (15.0, 2.3), color=RED, lw=2)
    ax.add_patch(Circle((8.0, 2.0), .3, fc=GREEN))
    ru(ax, 3.4, 3.1, 'куда?  в университет', ha='center', fontsize=12, color=BLUE); ax.text(3.7, 1.5, '去向：в / на + 宾格', ha='center', fontsize=10, color=BLUE)
    ru(ax, 8.0, 4.9, 'где?  в университете', ha='center', fontsize=12, color=GREEN); ax.text(8.0, .3, '所在：в / на + 前置格', ha='center', fontsize=10, color=GREEN)
    ru(ax, 12.6, 3.1, 'откуда?  из университета', ha='center', fontsize=12, color=RED); ax.text(12.3, 1.5, '来源：из / с + 属格', ha='center', fontsize=10, color=RED)
    ax.text(8.0, -.4, 'в 对应 из，на 对应 с；对人用 к + 与格、у + 属格、от + 属格', ha='center', fontsize=9.5, color=GRAY)
    save(fig, P + 'where_whither_whence.png', ticks=False)


def counting():
    fig, ax = plt.subplots(figsize=(6.4, 2.0)); ax.axis('off'); ax.set_xlim(-.5, 25.5); ax.set_ylim(-1.6, 2.2)
    def form(n):
        if 11 <= n % 100 <= 14:
            return 2
        d = n % 10
        return 0 if d == 1 else 1 if 2 <= d <= 4 else 2
    cols = [BLUE, GREEN, ORANGE]
    for n in range(1, 26):
        f = form(n); ax.add_patch(Rectangle((n - .45, 0), .9, .9, fc=cols[f], alpha=.25, ec=cols[f])); ax.text(n, .45, str(n), ha='center', va='center', fontsize=9.5)
    for i, (t, c) in enumerate([('один стол（单数主格）', BLUE), ('два стола（单数属格）', GREEN), ('пять столов（复数属格）', ORANGE)]):
        ax.add_patch(Rectangle((1 + i * 8.2, 1.4), .5, .5, fc=c, alpha=.3, ec=c)); ru(ax, 1.7 + i * 8.2, 1.6, t, fontsize=10.5, va='center')
    ax.text(12.5, -1.0, '看最后一位数字；11–14 例外，一律用复数属格', ha='center', fontsize=10)
    fig.tight_layout(); save(fig, P + 'number_noun_forms.png', ticks=False)


def clock(ax, h, m, title, sub):
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.75, 1.35); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Circle((0, 0), 1, fc='white', ec=INK, lw=1.4))
    for k in range(12):
        a = np.pi / 2 - 2 * np.pi * k / 12; ax.plot([.85 * np.cos(a), np.cos(a)], [.85 * np.sin(a), np.sin(a)], color=INK, lw=1.2 if k % 3 == 0 else .7)
        ax.text(.7 * np.cos(a), .7 * np.sin(a), str(k or 12), ha='center', va='center', fontsize=8)
    am = np.pi / 2 - 2 * np.pi * m / 60; ah = np.pi / 2 - 2 * np.pi * ((h % 12) + m / 60) / 12
    ax.plot([0, .78 * np.cos(am)], [0, .78 * np.sin(am)], color=BLUE, lw=2); ax.plot([0, .5 * np.cos(ah)], [0, .5 * np.sin(ah)], color=INK, lw=3)
    if m <= 30:
        ax.add_patch(Wedge((0, 0), .95, np.degrees(am), 90, fc=GREEN, alpha=.18))
    else:
        ax.add_patch(Wedge((0, 0), .95, 90, np.degrees(am) + 360, fc=RED, alpha=.18))
    ru(ax, 0, -1.3, title, ha='center', fontsize=11.5); ax.text(0, -1.65, sub, ha='center', fontsize=9.5, color=GRAY)


def clocks():
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.6))
    clock(axs[0], 8, 10, 'десять минут девятого', '8:10——第九个小时的十分')
    clock(axs[1], 7, 30, 'половина восьмого', '7:30——第八个小时的一半')
    clock(axs[2], 7, 40, 'без двадцати восемь', '7:40——差二十分八点')
    fig.tight_layout(); save(fig, P + 'telling_time.png', ticks=False)


def aspect():
    fig, ax = canvas(6.0, 2.2, (0, 14), (0, 5))
    ax.plot([.5, 13.5], [1.0, 1.0], color=GRAY, lw=1); ax.text(13.6, 1.0, '时间', va='center', fontsize=9.5, color=GRAY)
    ax.add_patch(Rectangle((1.0, 2.6), 5.5, .5, fc=LIGHT['blue'], ec=BLUE)); arrow(ax, (1.0, 2.35), (6.5, 2.35), color=BLUE, lw=1.2)
    ru(ax, 3.75, 3.5, 'Я читал книгу.', ha='center', fontsize=12, color=BLUE); ax.text(3.75, 1.6, '未完成体：过程、持续、反复', ha='center', fontsize=10, color=BLUE)
    ax.add_patch(Rectangle((8.0, 2.6), 3.6, .5, fc=LIGHT['gray'], ec=GRAY, ls='--')); ax.plot(11.6, 2.85, 'o', color=RED, ms=9)
    ru(ax, 10.0, 3.5, 'Я прочитал книгу.', ha='center', fontsize=12, color=RED); ax.text(10.0, 1.6, '完成体：到达结果（读完）', ha='center', fontsize=10, color=RED)
    save(fig, P + 'verb_aspect.png', ticks=False)


def motion():
    fig, axs = plt.subplots(1, 2, figsize=(6.0, 2.2))
    for ax in axs:
        ax.set_xlim(0, 8); ax.set_ylim(0, 4); ax.set_aspect('equal'); ax.axis('off')
    a = axs[0]; arrow(a, (1, 2), (7, 2), color=BLUE, lw=2.2); ru(a, 4, 2.6, 'идти / ехать', ha='center', fontsize=13, color=BLUE)
    a.text(4, 1.0, '定向：此刻朝一个方向', ha='center', fontsize=10)
    b = axs[1]; arrow(b, (1, 2.2), (7, 2.2), color=ORANGE, lw=1.6); arrow(b, (7, 1.8), (1, 1.8), color=ORANGE, lw=1.6)
    for x, y in [(1.4, 3.3), (2.6, 3.5), (3.8, 3.2)]:
        pass
    ru(b, 4, 2.8, 'ходить / ездить', ha='center', fontsize=13, color=ORANGE); b.text(4, .9, '不定向：往返、反复、泛指', ha='center', fontsize=10)
    fig.tight_layout(); save(fig, P + 'motion_verbs.png', ticks=False)


def prefixes():
    fig, ax = canvas(6.4, 2.6, (0, 16), (0, 6.4))
    house(ax, 6.8, 1.6, 2.4, 2.0)
    items = [((1.0, 2.4), (6.6, 2.4), 'при-', 'пришёл', '到达', BLUE, (3.8, 3.35)),
             ((9.4, 2.4), (15.0, 2.4), 'у-', 'ушёл', '离开', RED, (12.2, 3.35)),
             ((4.0, 5.6), (6.8, 3.9), 'по-', 'пошёл', '出发、动身', GREEN, (2.4, 5.6)),
             ((8.0, .4), (8.0, 1.5), 'в-', 'вошёл', '进入', PURPLE, (9.6, .9))]
    for p, q, pre, w, mean, c, tp in items:
        arrow(ax, p, q, color=c, lw=1.8)
        ru(ax, tp[0], tp[1], f'{pre}  {w}', ha='center', fontsize=12, color=c); ax.text(tp[0], tp[1] - .55, mean, ha='center', fontsize=9.5, color=c)
    ru(ax, 8.0, 5.85, 'Он ... в университет / из университета', ha='left', fontsize=10, color=GRAY)
    save(fig, P + 'motion_prefixes.png', ticks=False)


def uzhe():
    fig, ax = canvas(6.4, 2.6, (0, 16), (0, 6.6))
    ax.plot([.5, 15.5], [3.2, 3.2], color=GRAY); ax.plot(8, 3.2, 'v', color=INK, ms=8); ax.text(8, 3.7, '现在', ha='center', fontsize=10)
    rows = [('уже', '已经发生/开始', 'Он уже пришёл.', (6, 8), BLUE, 4.6), ('ещё', '仍在持续', 'Он ещё работает.', (3, 11), GREEN, 5.9),
            ('уже не', '原有状态已结束', 'Он уже не работает.', (3, 6.5), RED, 1.9), ('ещё не', '预期的事尚未发生', 'Он ещё не пришёл.', (10, 10), ORANGE, .6)]
    for w, mean, ex, (a, b), c, y in rows:
        if a != b:
            ax.plot([a, b], [y, y], color=c, lw=4, alpha=.6, solid_capstyle='round')
        else:
            ax.plot(a, y, 'o', color=c, ms=8, mfc='white', mew=2)
        ru(ax, .3, y, w, fontsize=12, color=c, va='center', weight='bold')
        ax.text(11.8, y + .12, mean, fontsize=9.5, color=c, va='center'); ru(ax, 11.8, y - .38, ex, fontsize=10, color=c, va='center', style='italic')
    save(fig, P + 'uzhe_eshchyo.png', ticks=False)


def clause():
    fig, ax = canvas(6.6, 2.0, (0, 19), (0, 5))
    parts = [('Система,', BLUE, 0), ('которая получает данные от датчика,', ORANGE, 1), ('управляет процессом.', BLUE, 0)]
    x = .3
    for t, c, lvl in parts:
        w = len(t) * .27 + .4; y = 3.2 - lvl * 1.4
        box(ax, x - .1, y - .35, w, .8, '', LIGHT['blue'] if c == BLUE else LIGHT['orange'], c, r=.15)
        ru(ax, x + w / 2 - .1, y + .05, t, ha='center', va='center', fontsize=11.5)
        x += w + .2
    arrow(ax, (2.2, 2.85), (2.9, 2.25), color=ORANGE, lw=1); ax.text(6.2, .8, '关系从句修饰 Система（先略去）', ha='center', fontsize=10, color=ORANGE)
    ax.text(13.0, 4.3, '主干：Система управляет процессом', ha='center', fontsize=10.5, color=BLUE)
    save(fig, P + 'relative_clause.png', ticks=False)


def report():
    fig, ax = canvas(6.4, 1.5, (0, 16), (0, 3.6))
    steps = [('Цель работы', '目的'), ('Ход работы', '过程'), ('Результаты', '结果'), ('Вывод', '结论')]
    for i, (r, z) in enumerate(steps):
        x = .2 + i * 4.0
        box(ax, x, .9, 3.2, 1.8, '', LIGHT['blue'], BLUE); ru(ax, x + 1.6, 2.05, r, ha='center', va='center', fontsize=12); ax.text(x + 1.6, 1.35, z, ha='center', va='center', fontsize=10.5)
        if i < 3:
            arrow(ax, (x + 3.25, 1.8), (x + 3.95, 1.8), color=GRAY)
    save(fig, P + 'report_structure.png', ticks=False)


for f in [cases, sentence, devoicing, v_na, three_way, counting, clocks, aspect, motion, prefixes, uzhe, clause, report]:
    f()

place('09_俄语.md', [
    ('俄语常用六格', P + 'six_cases.png', '六个格的提问词与 студент 的单数各格'),
    ('**句子分析：Новый', P + 'sentence_parts.png', '句子成分的划线标记'),
    ('辅音中有六对清浊对立', P + 'devoicing.png', '清浊辅音对与词末清化、连缀同化'),
    ('в 与 на 的选择不能简', P + 'v_na.png', 'в 表示内部，на 表示表面'),
    ('地点表达还应连同', P + 'where_whither_whence.png', '去向、所在与来源的三向对应'),
    ('在主格计数以及常见无生命宾', P + 'number_noun_forms.png', '数词后名词形式由末位数字决定'),
    ('过了半点可从下一整点倒数', P + 'telling_time.png', '俄语口语报时：以“下一个小时”为参照'),
    ('читать 为未完成体，', P + 'verb_aspect.png', '未完成体与完成体'),
    ('表示移动时，应先分清交通方', P + 'motion_verbs.png', '定向与不定向运动动词'),
    ('到达与离开又需要不同前缀', P + 'motion_prefixes.png', '运动动词前缀的空间意义'),
    ('уже не 说明一个原有', P + 'uzhe_eshchyo.png', 'уже、ещё 及其否定在时间轴上的含义'),
    ('Система, кото', P + 'relative_clause.png', '先略去关系从句，找出句子主干'),
    ('Цель работы —', P + 'report_structure.png', '实验报告的常见结构'),
])
