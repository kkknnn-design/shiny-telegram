"""Cut whole words out of natural handwriting pages (screenshots of a notes app).

  python natural_words.py segment IMG...   -> assets/natural/boxes.json + numbered overlays (for labelling)
Labels go into assets/natural/words.json: {"<file>": {"<box id>": "word as written", ...}}.
build_glyphs.py then turns every labelled box into a whole-word unit.
"""
import json, sys
from pathlib import Path
import cv2
import numpy as np

NAT = Path(__file__).resolve().parent.parent / "assets" / "natural"
# app chrome on these screenshots: collapse button, "..." handle, page counter, home bar
CHROME = [(0, 0, 80, 55), (730, 0, 830, 30), (15, 990, 130, 1040), (540, 1045, 1000, 1080)]


def darkness(path):
    """Ink darkness 0..255 on a white-paper scale (dark pages are inverted); red ink and app chrome removed."""
    im = cv2.imread(str(path))
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    if np.median(g) < 128:
        g = 255 - g
    b, gr, r = [c.astype(int) for c in cv2.split(im)]
    red = (r - np.maximum(gr, b)) > 50
    d = 255 - g
    d[cv2.dilate(red.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0
    H, W = d.shape
    for x0, y0, x1, y1 in CHROME:
        if x1 <= W and y1 <= H:
            d[y0:y1, x0:x1] = 0
    return d


def ink_alpha(d):
    return np.clip((d - 110) / 100, 0, 1)     # grid dots/lines (darkness <= ~95) -> 0, pen ink -> 1


def is_cjk(ch):
    return "一" <= ch <= "鿿"


def body_band(m, H):
    """x-height band of a word whose body should be about H px tall: the densest H-row window
    (descenders/ascenders are thin, so they can't pull it), then edges refined within ±25% of H."""
    p = m.sum(1).astype(float)
    if p.max() == 0 or len(p) < H:
        return body_rows(m)
    H = int(round(H))
    win = np.convolve(p, np.ones(H), "valid")
    t = int(np.argmax(win))
    b = t + H
    ref = p[t:b].mean()
    lim = int(0.25 * H)
    while t > 0 and b - t < H + lim and p[t - 1] >= 0.6 * ref:
        t -= 1
    while t < len(p) - 1 and b - t > H - lim and p[t] < 0.35 * ref:
        t += 1
    while b < len(p) and b - t < H + lim and p[b] >= 0.6 * ref:
        b += 1
    while b > t + 1 and b - t > H - lim and p[b - 1] < 0.35 * ref:
        b -= 1
    return t, b


def body_rows(m):
    p = m.sum(1).astype(float)
    if p.max() == 0:
        return None
    band = np.where(p >= 0.35 * p.max())[0]
    return int(band[0]), int(band[-1]) + 1


def letter_widths(alpha_units):
    """Relative body width of each character (in body heights), from the alphabet sample."""
    W = {}
    for key, vs in alpha_units.items():
        if len(key) != 1:
            continue
        ws = []
        for v in vs:
            m = v["a"] > 0.35
            t, b = int(v.get("top", v["base"] - 17)), int(v.get("bot", v["base"]))
            band = m[max(0, t):max(t + 1, b)]
            cols = np.where(band.any(0))[0] if band.size else []
            if len(cols) < 2:
                cols = np.where(m.any(0))[0]
            ws.append((cols.max() - cols.min() + 1) / max(1.0, b - t))
        W[key] = float(np.median(ws))
    return W


def char_w(W, ch):
    if ch in W:
        return W[ch]
    if ch.lower() in W:
        return W[ch.lower()] * 1.15
    return 1.6 if is_cjk(ch) else 0.8


def shear(a, k, anchor):
    """x' = x + k*(y - anchor); returns sheared image and x offset added."""
    h, w = a.shape
    ends = [k * (0 - anchor), k * (h - anchor)]
    off = -min(ends)
    M = np.float32([[1, k, off - k * anchor], [0, 1, 0]])
    return cv2.warpAffine(a, M, (w + int(np.ceil(max(ends) - min(ends))) + 2, h), flags=cv2.INTER_LINEAR)


DESC_L = set("рудзфщц")
ASC_L = set("бвф")


def plausible(piece, msk, top, bot, W, word_ratio=1.0):
    """Reject chunks whose shape can't be these letters: missing/extra tails or loops, wrong width."""
    hb = bot - top
    ys, xs = np.nonzero(msk)
    tot = len(ys)
    below = (ys > bot + 0.35 * hb).sum() / tot
    above = (ys < top - 0.35 * hb).sum() / tot
    want_desc = any(c in DESC_L for c in piece)
    want_asc = any(c in ASC_L or c.isupper() for c in piece)
    if want_desc and below < 0.04:
        return False
    if not want_desc and below > 0.06:
        return False
    if want_asc and above < 0.04:
        return False
    if not want_asc and not any(c in "ёй" for c in piece) and above > 0.08:
        return False
    width = (xs.max() - xs.min() + 1) / hb
    expect = sum(char_w(W, c) for c in piece) * word_ratio   # this word's own letter spacing
    return 0.8 <= width / expect <= 1.22


def flatten(a, top, bot):
    """Words drift uphill: fit a line to the bottoms of the letter bodies and shear it level."""
    m = a > 0.35
    h, w = m.shape
    xs, ys = [], []
    lo, hi = top + 0.4 * (bot - top), bot + 0.35 * (bot - top)
    for x in range(w):
        col = np.where(m[:, x])[0]
        col = col[(col >= lo) & (col <= hi)]
        if len(col):
            xs.append(x); ys.append(col.max())
    if len(xs) < 10:
        return a
    xs, ys = np.array(xs, float), np.array(ys, float)
    keep = np.ones(len(xs), bool)
    for _ in range(3):
        k, b = np.polyfit(xs[keep], ys[keep], 1)
        res = ys - (k * xs + b)
        keep = res > -0.15 * (bot - top)            # tops of connectors lie above the line; ignore them
        keep &= res < 0.25 * (bot - top)            # tails below
        if keep.sum() < 8:
            return a
    k = float(np.clip(k, -0.25, 0.25))
    if abs(k) * w < 1.0:
        return a
    xc = w / 2
    M = np.float32([[1, 0, 0], [-k, 1, k * xc]])     # y' = y - k*(x - xc)
    pad = int(abs(k) * w / 2) + 2
    a2 = cv2.warpAffine(np.pad(a, ((pad, pad), (0, 0))), M, (w, h + 2 * pad), flags=cv2.INTER_LINEAR)
    return a2


def cut_word(a, text, W, top, bot):
    """Find cut columns between letters on an upright word. Returns list of (column, clean?) of len(text)-1."""
    n = len(text)
    m = a > 0.35
    band = m[top:bot]
    ink = band.sum(0).astype(float) / max(1, bot - top)          # ~0.2 for a connector, ~1 for a stem
    cols = np.where(m.any(0))[0]
    L, R = cols.min(), cols.max() + 1
    widths = np.array([char_w(W, c) for c in text])
    e = L + np.cumsum(widths)[:-1] / widths.sum() * (R - L)
    avg = (R - L) / widths.sum()
    win = [np.arange(max(L + 1, int(x - 0.6 * avg * widths[i:i + 2].mean())),
                     min(R - 1, int(x + 0.6 * avg * widths[i:i + 2].mean())) + 1) for i, x in enumerate(e)]
    win = [w if len(w) else np.array([int(x)]) for w, x in zip(win, e)]
    # DP over boundaries
    cost_prev = {int(c): ink[c] + 3 * ((c - e[0]) / avg) ** 2 for c in win[0]}
    back = [{}]
    for i in range(1, n - 1):
        cur, bk = {}, {}
        for c in win[i]:
            best, arg = 1e18, None
            for p, cp in cost_prev.items():
                if c - p >= 0.25 * avg and cp < best:
                    best, arg = cp, p
            if arg is None:
                continue
            cur[int(c)] = best + ink[c] + 3 * ((c - e[i]) / avg) ** 2
            bk[int(c)] = arg
        if not cur:
            return None
        cost_prev = cur
        back.append(bk)
    c = min(cost_prev, key=cost_prev.get)
    path = [c]
    for i in range(n - 2, 0, -1):
        c = back[i][c]
        path.append(c)
    path = path[::-1]
    # a cut is trusted only on a thin connector, close to where the letter widths say it should be
    return [(c, ink[c] < 0.32 and abs(c - e[i]) < 0.45 * avg * widths[i:i + 2].mean())
            for i, c in enumerate(path)]


def word_units(body, alpha_units, keep_per_key=6):
    """Whole words + clean letter chunks (2-6 letters) from the labelled natural pages."""
    import json as _json
    W = letter_widths(alpha_units)
    boxes = _json.loads((NAT / "boxes.json").read_text(encoding="utf-8"))
    labels = _json.loads((NAT / "words.json").read_text(encoding="utf-8"))
    out, stats = {}, {"words": 0, "chunks": 0, "uncut": 0}
    for fname, lab in labels.items():
        if fname.startswith("_"):
            continue
        d = darkness(NAT / fname)
        alpha = ink_alpha(d)
        core = (d > 120).astype(np.uint8)
        n, cl, st, cen = cv2.connectedComponentsWithStats(core, 8)
        items = []
        for ids, text in lab.items():
            bx = [boxes[fname][int(i)] for i in ids.split("+")]
            x0 = min(b[0] for b in bx); y0 = min(b[1] for b in bx)
            x1 = max(b[0] + b[2] for b in bx); y1 = max(b[1] + b[3] for b in bx)
            inside = np.zeros(n, bool)
            for i in range(1, n):
                cx, cy = cen[i]
                if st[i, 4] >= 4 and any(b[0] - 2 <= cx <= b[0] + b[2] + 2 and b[1] - 2 <= cy <= b[1] + b[3] + 2 for b in bx):
                    inside[i] = True
            sel = cv2.dilate(inside[cl[y0:y1, x0:x1]].astype(np.uint8), np.ones((3, 3), np.uint8))
            a = alpha[y0:y1, x0:x1] * sel
            items.append((f"{fname}#{ids}", text, a))
        # one scale per page: that page's median Russian body height -> alphabet body height
        bh = [r[1] - r[0] for _, t, a in items if not any(is_cjk(c) for c in t) and len(t) >= 3
              for r in [body_rows(a > 0.35)] if r]
        page_s = body / float(np.median(bh))
        for where, text, a in items:
            a = cv2.resize(a, None, fx=page_s, fy=page_s, interpolation=cv2.INTER_CUBIC).clip(0, 1)
            a = np.pad(a, 6)
            m = a > 0.35
            r = body_band(m, body)
            if r is None:
                continue
            top, bot = r
            cjk = any(is_cjk(c) for c in text)
            if cjk:
                rows = np.where(m.any(1))[0]
                top, bot = int(rows.min()), int(rows.max()) + 1
            from build_glyphs import slant_of
            k = 0.0 if cjk else slant_of(a)
            up = shear(a, k, bot) if abs(k) > 0.02 else a
            if not cjk:
                up = flatten(up, top, bot)
                r = body_band(up > 0.35, body)
                if r:
                    top, bot = r
            src = f"{where}:{text}"
            core_text = text
            unit = {"a": up, "base": float(bot), "top": float(top), "bot": float(bot), "upright": not cjk, "src": src,
                    "natural": True, "cjk": cjk}
            out.setdefault(text, []).append(unit)
            stats["words"] += 1
            if len(core_text) < 3:
                continue
            cuts = cut_word(up, core_text, W, top, bot)
            if cuts is None:
                stats["uncut"] += 1
                continue
            # split pixels between letters: break the body band at each cut, then follow connectivity
            mm = (up > 0.2).astype(np.uint8)
            brk = mm.copy()
            for c, _ in cuts:
                brk[top:bot, c] = 0
            nc, lb, s2, c2 = cv2.connectedComponentsWithStats(brk, 8)
            edges = [c for c, _ in cuts]
            seg_of = np.zeros(nc, int)
            for j in range(1, nc):
                ys, xs = np.nonzero(lb == j)
                inb = (ys >= top) & (ys < bot)
                xm = np.median(xs[inb]) if inb.any() else np.median(xs)
                seg_of[j] = int(np.searchsorted(edges, xm))
            segmap = seg_of[lb]
            segmap[lb == 0] = -1
            # cut-line pixels go to the left letter
            for c, _ in cuts:
                col = segmap[:, c]
                seg = np.searchsorted(edges, c)
                col[(mm[:, c] > 0) & (col < 0)] = seg
            clean = [True] + [cl_ for _, cl_ in cuts] + [True]   # clean[i] = boundary before letter i
            for q in range(1, len(core_text)):        # ф has loops on both sides: never cut next to it
                if "ф" in (core_text[q - 1], core_text[q]):
                    clean[q] = False
            m_up = up > 0.35
            cols_ = np.where(m_up.any(0))[0]
            avg_w = (cols_.max() - cols_.min() + 1) / max(1, len(core_text))
            word_ratio = ((cols_.max() - cols_.min() + 1) / (bot - top)) / sum(char_w(W, c) for c in core_text)
            N = len(core_text)
            for i in range(N):
                for j in range(i + 2, min(N, i + 10) + 1):
                    if (i, j) == (0, N):
                        continue
                    if not (clean[i] and clean[j]):
                        continue
                    piece = core_text[i:j]
                    if not piece.strip() or any(not ch.isalpha() for ch in piece):
                        continue
                    msk = (segmap >= i) & (segmap < j)
                    # drop slivers of neighbouring letters hanging at the chunk edges
                    nn, l3, s3, _ = cv2.connectedComponentsWithStats(msk.astype(np.uint8), 8)
                    if nn > 2:
                        tot = s3[1:, 4].sum()
                        lo = edges[i - 1] if i > 0 else -1e9
                        hi = edges[j - 1] if j <= len(edges) else 1e9
                        for q in range(1, nn):
                            near = s3[q, 0] < lo + 0.4 * avg_w or s3[q, 0] + s3[q, 2] > hi - 0.4 * avg_w
                            if s3[q, 4] < 0.12 * tot and near and s3[q, 1] + s3[q, 3] > top:
                                msk[l3 == q] = False
                    ys, xs = np.nonzero(msk)
                    if len(xs) == 0:
                        continue
                    if not plausible(piece, msk, top, bot, W, word_ratio):
                        stats["rejected"] = stats.get("rejected", 0) + 1
                        continue
                    # trim long connector tails at interior cuts (they look like hyphens on their own)
                    hb = bot - top
                    colink = (msk & (up > 0.5))[top:bot].mean(0)
                    inkcols = np.where(msk.any(0))[0]
                    xa, xb = inkcols.min(), inkcols.max()
                    strong = np.where(colink >= 0.45)[0]           # columns crossing a real letter stroke
                    if len(strong):
                        if j < N and xb - strong.max() > 0.3 * hb:
                            msk[:, int(strong.max() + 0.12 * hb):] = False
                        if i > 0 and strong.min() - xa > 0.3 * hb:
                            msk[:, :int(strong.min() - 0.12 * hb)] = False
                    ys, xs = np.nonzero(msk)
                    if len(xs) == 0:
                        continue
                    X0, X1 = max(0, xs.min() - 3), xs.max() + 4
                    ca = (up * cv2.dilate(msk.astype(np.uint8), np.ones((3, 3), np.uint8)))[:, X0:X1]
                    out.setdefault(piece, []).append({"a": ca.astype(np.float32), "base": float(bot), "top": float(top),
                                                      "bot": float(bot), "upright": True, "natural": True,
                                                      "src": f"{src}[{i}:{j}]"})
                    stats["chunks"] += 1
    # overlapping screenshots show the same physical word twice: find those (same text, near-identical
    # shape) so they neither count as independent evidence nor as extra variants
    phys = {}
    for key, vs in out.items():
        whole = [v for v in vs if "[" not in v["src"]]
        reps = []
        for v in whole:
            for r in reps:
                if same_ink(v, r):
                    phys[v["src"]] = phys[r["src"]]
                    v["dup"] = True
                    break
            else:
                reps.append(v)
                phys[v["src"]] = f"{v['src']}#{len(reps)}"
    dupsrc = {v["src"] for vs in out.values() for v in vs if v.get("dup")}
    for key in list(out):                 # chunks cut from a duplicate copy are duplicates too
        out[key] = [v for v in out[key] if not v.get("dup") and v["src"].split("[")[0] not in dupsrc]
        if not out[key]:
            del out[key]
    stats["duplicate_words"] = len(dupsrc)
    # cross-check: a chunk is kept only if another cut of the same letters, from a different piece of
    # writing, looks the same (independent cutting mistakes rarely agree)
    for key in list(out):
        vs = out[key]
        whole = [v for v in vs if "[" not in v["src"]]
        ch = [v for v in vs if "[" in v["src"]]
        good = []
        for i, v in enumerate(ch):
            pv = phys.get(v["src"].split("[")[0])
            for j, u in enumerate(ch):
                pu = phys.get(u["src"].split("[")[0])
                if i != j and pv != pu and similar(v, u):
                    good.append(v)
                    break
        stats["chunks_verified"] = stats.get("chunks_verified", 0) + len(good)
        if whole or good:
            out[key] = whole + good
        else:
            del out[key]
    bad = set(labels.get("_bad_chunks", []))          # pieces found unreadable on visual check
    for key in list(out):
        out[key] = [v for v in out[key] if v["src"] not in bad]
        if not out[key]:
            del out[key]
    print("natural:", stats, "keys", len(out))
    return out


def _profile(v, bins=24):
    m = v["a"] > 0.35
    t, b = int(v["top"]), int(v["bot"])
    band = m[max(0, t):b]
    cols = np.where(m.any(0))[0]
    band = band[:, cols.min():cols.max() + 1]
    col = band.mean(0)
    row = m[:, cols.min():cols.max() + 1].mean(1)
    col = np.interp(np.linspace(0, len(col) - 1, bins), np.arange(len(col)), col)
    # vertical extent: ink above/below the body
    hb = b - t
    ys = np.nonzero(m)[0]
    above = (ys < t - 0.35 * hb).mean()
    below = (ys > b + 0.35 * hb).mean()
    width = (cols.max() - cols.min() + 1) / hb
    return col, width, above, below


def ink_ncc(v, u):
    """Best normalised cross-correlation of two word images (same scale), allowing small shifts."""
    def crop(a):
        a = a.astype(np.float32)
        if a.max() > 1.5:
            a = a / 255
        ys, xs = np.nonzero(a > 0.35)
        return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    A, B = crop(v["a"]), crop(u["a"])
    if not (0.8 <= A.shape[1] / B.shape[1] <= 1.25 and 0.75 <= A.shape[0] / B.shape[0] <= 1.33):
        return 0.0
    A = cv2.GaussianBlur(A, (0, 0), 1.0)
    B = cv2.GaussianBlur(cv2.resize(B, (A.shape[1], A.shape[0])), (0, 0), 1.0)
    p = 4
    Ap = np.pad(A, p)
    return float(cv2.matchTemplate(Ap, B, cv2.TM_CCOEFF_NORMED).max())


def same_ink(v, u):
    """The same handwritten word captured in two overlapping screenshots (long words only:
    short ones like «на» look alike even when written separately)."""
    key = v["src"].split(":", 1)[-1]
    return len(key) >= 4 and ink_ncc(v, u) > 0.8


def similar(v, u):
    c1, w1, a1, b1 = _profile(v)
    c2, w2, a2, b2 = _profile(u)
    if not 0.85 <= w1 / w2 <= 1.18:
        return False
    if abs(a1 - a2) > 0.06 or abs(b1 - b2) > 0.06:
        return False
    r = np.corrcoef(c1, c2)[0, 1]
    return r > 0.75


def segment(path):
    d = darkness(path)
    core = (d > 120).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(core, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, 4] >= 8
    core = keep[lab].astype(np.uint8)
    merged = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5)))
    m, wl, ws, _ = cv2.connectedComponentsWithStats(merged, 8)
    boxes = []
    for i in range(1, m):
        x, y, w, h, a = ws[i]
        if w < 20 or h < 10 or h > 140 or w > 900:
            continue
        boxes.append([int(x), int(y), int(w), int(h)])
    boxes.sort(key=lambda b: (b[1] // 40, b[0]))
    return boxes


def overlay(path, boxes, out_prefix):
    im = cv2.imread(str(path))
    if np.median(im) < 128:
        im = 255 - im
    for k, (x, y, w, h) in enumerate(boxes):
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.putText(im, str(k), (x, max(10, y - 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1)
    H = im.shape[0]
    for j, (a, b) in enumerate([(0, H // 2 + 40), (H // 2 - 40, H)]):
        cv2.imwrite(f"{out_prefix}_{j}.png", im[a:b])


def chunk_sheet(nat, path, n=90, seed=3):
    """Random sample of cut chunks with their labels, to eyeball whether cuts land between the right letters."""
    from PIL import Image, ImageDraw, ImageFont
    rng = np.random.default_rng(seed)
    keys = [k for k in nat if 2 <= len(k) <= 6 and not any(is_cjk(c) for c in k)]
    pick = rng.choice(len(keys), size=min(n, len(keys)), replace=False)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    tiles = []
    for i in pick:
        v = nat[keys[i]][0]
        a = np.pad(v["a"], ((50, 50), (0, 0)))
        v = dict(v, bot=v["bot"] + 50)
        t = Image.fromarray((255 * (1 - np.clip(a, 0, 1))).astype(np.uint8)).convert("RGB")
        canvas = Image.new("RGB", (max(t.width, 70) + 8, 90), "white")
        canvas.paste(t.crop((0, max(0, int(v["bot"]) - 45), t.width, int(v["bot"]) + 25)), (4, 0))
        ImageDraw.Draw(canvas).text((4, 70), keys[i], fill=(200, 0, 0), font=font)
        tiles.append(canvas)
    rows, cur, wsum = [], [], 0
    for t in tiles:
        if wsum + t.width > 1500:
            rows.append(cur); cur, wsum = [], 0
        cur.append(t); wsum += t.width
    rows.append(cur)
    sheet = Image.new("RGB", (1500, 92 * len(rows)), (220, 220, 220))
    for r, row in enumerate(rows):
        x = 0
        for t in row:
            sheet.paste(t, (x, r * 92)); x += t.width + 2
    sheet.save(path)


if __name__ == "__main__":
    if sys.argv[1] == "segment":
        out_dir = Path(sys.argv[2])
        allb = {}
        for p in sys.argv[3:]:
            p = Path(p)
            b = segment(p)
            allb[p.name] = b
            overlay(p, b, str(out_dir / p.stem))
            print(p.name, len(b), "boxes")
        (NAT / "boxes.json").write_text(json.dumps(allb), encoding="utf-8")
