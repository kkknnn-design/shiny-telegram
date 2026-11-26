"""Typeset text in the user's handwriting (from assets/glyphs.pkl) onto A4 paper -> PDF (+ PNG previews).

usage: python render.py input.txt output.pdf [--paper grid|lines|plain] [--xh 2.4] [--ink black|blue]
                        [--png-dir DIR] [--seed 1]
Input text (UTF-8):
  "# Title"      -> centered line
  blank line     -> an empty row
  leading spaces -> indent
  a line "===="  -> page break
"""
import argparse, pickle, sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "assets"
DPI = 480
MM = DPI / 25.4
CELL = 5 * MM                      # 5 mm squares
A4 = (int(round(210 * MM)), int(round(297 * MM)))
INKS = {"black": (24, 24, 30), "blue": (28, 45, 120)}
CENTERED = {"-": 0.42, "—": 0.42, "«": 0.45, "»": 0.45}   # mark centre height, in x-heights
FALLBACK_FONTS = ["C:/Windows/Fonts/segoepr.ttf", "C:/Windows/Fonts/segoesc.ttf", "C:/Windows/Fonts/arial.ttf"]

# Style measured from the user's natural pages (assets/natural/n2-n5, ~600 words), relative to the
# lowercase body height (x-height): slant 0.30-0.35, word gap ~0.8, letters joined (gap ~0),
# words ~10% wider than the alphabet letters set side by side, x-height ~0.22 of line pitch.
SLANT = 0.32        # target shear (x shift per unit height), right-leaning
XSTRETCH = 1.08     # horizontal stretch of glyphs
GAP = 0.03          # gap between units inside a word, in x-heights
SPACE = 0.8         # word space, in x-heights
PEN = 0.24          # stroke width / x-height (the thickness the user approved)

NORMALIZE = {"–": "—", "−": "-", "‐": "-", "…": "...", "\u00a0": " ", "'": "’"}


class Hand:
    def __init__(self, xh_mm, seed):
        d = pickle.load(open(ASSETS / "glyphs.pkl", "rb"))
        self.native_xh = d.get("body", d["xh"])     # lowercase body height in the sample
        self.xh = xh_mm * MM                         # rendered lowercase body height
        self.s = self.xh / self.native_xh
        self.rng = np.random.default_rng(seed)
        self.raw, self.uscore, self.cache = {}, {}, {}
        for key, vs in d["units"].items():
            best = min(v.get("score", 0) for v in vs)
            self.uscore[key] = best
            self.raw[key] = [v for v in vs if v.get("score", 0) <= best + 0.25]   # only the nicer variants
        self.units = self.raw          # key lookup (segment / key_for)
        self.chunky = {k for k, vs in self.raw.items() if all("[" in v.get("src", "") for v in vs)}
        self.pen = PEN * self.xh
        self.last = {}
        self.missing = set()
        self.stats = {"joined": 0, "single": 0, "fallback": 0}
        self.font = None

    def prepare(self, key, k):
        """Scale, slant-fix, pen-fix one variant (cached)."""
        if (key, k) in self.cache:
            return self.cache[(key, k)]
        v = self.raw[key][k]
        a = v["a"].astype(np.float32) / 255 if v["a"].dtype == np.uint8 else v["a"]
        h, w = a.shape
        s = self.s * v.get("f", 1.0)                         # size fix: bodies come out the same height
        big = cv2.resize(a, (max(1, int(round(w * s * XSTRETCH))), max(1, int(round(h * s)))),
                         interpolation=cv2.INTER_CUBIC)
        # lowercase sits on its measured body bottom, others on their fitted baseline
        base = (v["bot"] if v.get("bot_fix") or v.get("natural") else v["base"]) * s
        sl = v.get("slant")                                   # measured per piece from its stroke edges
        if sl is None and v.get("upright"):
            sl = 0.0
        c = float(np.clip(sl * XSTRETCH - SLANT, -0.45, 0.45)) if sl is not None else 0.0
        if abs(c) > 0.02:
            hh, ww = big.shape
            ends = [c * (0 - base), c * (hh - base)]
            off = -min(ends)
            M = np.float32([[1, c, off - c * base], [0, 1, 0]])
            big = cv2.warpAffine(big, M, (ww + int(np.ceil(max(ends) - min(ends))) + 1, hh),
                                 flags=cv2.INTER_CUBIC)
        big = np.clip((big - 0.15) / 0.7, 0, 1)              # crisp edges, same stroke centre
        P = 8                                                # room for thickening strokes
        big = np.pad(big, P)
        base += P
        rows = np.where((big > 0.1).any(1))[0]
        if key in CENTERED:
            mid = (rows.min() + rows.max()) / 2
            base = mid + CENTERED[key] * self.xh
        if key in "()":                                      # written tiny: bring up to bracket height
            ink = big[rows.min():rows.max() + 1]
            f = 1.7 * self.xh / ink.shape[0]
            big = cv2.resize(ink, (max(1, int(ink.shape[1] * f)), int(ink.shape[0] * f)),
                             interpolation=cv2.INTER_CUBIC).clip(0, 1)
            base = big.shape[0] - 0.35 * self.xh
        if key.isalnum() or key in "()?«»-—" or len(key) > 1:
            big = self.even_pen(big)
        # spacing uses the letter body (x-height band), so tails/flourishes may tuck under neighbours
        y0 = max(0, int(base - self.xh)); y1 = max(y0 + 1, int(base))
        body = np.where((big[y0:y1] > 0.1).any(0))[0]
        cols = body if len(body) >= 2 and key[0].isalpha() else np.where((big > 0.1).any(0))[0]
        g = {"a": big, "base": base, "x0": int(cols.min()), "x1": int(cols.max()) + 1}
        self.cache[(key, k)] = g
        return g

    def even_pen(self, a):
        """Same pen everywhere: move the outline in/out by a uniform distance so the typical stroke
        width matches PEN * x-height. Stroke paths and pressure changes inside a letter stay."""
        from skimage.morphology import skeletonize
        m = a > 0.5
        din = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
        sk = skeletonize(m)
        if sk.sum() < 5:
            return a
        w = float(2 * np.median(din[sk]))
        delta = float(np.clip((self.pen - w) / 2, -0.35 * w, 0.45 * w))
        if abs(delta) < 0.5:
            return a
        dout = cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5)
        sd = np.where(m, din - 0.5, 0.5 - dout)              # signed distance to the outline
        return np.clip((sd + delta) / 1.4 + 0.5, 0, 1).astype(np.float32)

    def key_for(self, ch):
        if ch in self.units:
            return ch
        if ch.lower() in self.units and ch.isupper():      # no capital variant written -> lowercase
            return ch.lower()
        return None

    def segment(self, word):
        """Split a word into as few written units as possible (whole words > pairs > letters)."""
        n = len(word)
        best = [0.0] + [1e9] * n
        prev = [None] * (n + 1)
        maxlen = max(len(k) for k in self.units)
        for i in range(1, n + 1):
            for L in range(1, min(maxlen, i) + 1):
                piece = word[i - L:i]
                key = piece if L > 1 else self.key_for(piece)
                if L > 1 and piece not in self.units:
                    continue
                # fewer units is better, but an ugly unit costs extra; fallback glyph is expensive
                cost = 1.0 + 0.4 * self.uscore.get(key, 0.0) if key is not None else 5.0
                if key is not None and key in self.chunky:              # cut-out piece: slightly less trusted
                    cost += 0.15
                if best[i - L] + cost < best[i]:
                    best[i] = best[i - L] + cost
                    prev[i] = i - L
        out, i = [], n
        while i > 0:
            j = prev[i]
            out.append(word[j:i])
            i = j
        return out[::-1]

    def pick(self, key):
        vs = self.raw[key]
        if len(vs) == 1:
            return self.prepare(key, 0)
        choices = [k for k in range(len(vs)) if k != self.last.get(key)]
        k = int(self.rng.choice(choices))
        self.last[key] = k
        return self.prepare(key, k)

    def fallback(self, ch):
        """Character never written by the user: draw it from a handwriting-ish system font (flagged)."""
        self.missing.add(ch)
        if self.font is None:
            for f in FALLBACK_FONTS:
                if Path(f).exists():
                    self.font = ImageFont.truetype(f, int(self.xh * 1.75))
                    break
        img = Image.new("L", (int(self.xh * 4), int(self.xh * 4)), 0)
        dr = ImageDraw.Draw(img)
        dr.text((int(self.xh), int(self.xh * 2.6)), ch, fill=255, font=self.font, anchor="ls",
                stroke_width=max(1, int(self.xh * 0.05)), stroke_fill=255)
        a = np.asarray(img, np.float32) / 255
        cols = np.where((a > 0.1).any(0))[0]
        if len(cols) == 0:
            return {"a": a, "base": self.xh * 2.6, "x0": 0, "x1": int(self.xh * 0.5)}
        return {"a": a, "base": self.xh * 2.6, "x0": int(cols.min()), "x1": int(cols.max()) + 1}

    def word(self, word):
        """Return list of (glyph, x offset) and the ink width of the word."""
        placed, x = [], 0.0
        gap = GAP * self.xh
        for piece in self.segment(word):
            if len(piece) > 1 or self.key_for(piece):
                key = piece if len(piece) > 1 else self.key_for(piece)
                g = self.pick(key)
                self.stats["joined" if len(piece) > 1 else "single"] += 1
            else:
                g = self.fallback(piece)
                self.stats["fallback"] += 1
            if placed:
                x += gap
            placed.append((g, x - g["x0"]))
            x += g["x1"] - g["x0"]
        return placed, x


def paper(kind, top_y, pitch):
    W, H = A4
    img = np.full((H, W, 3), 255, np.float32)
    col = np.array([196, 206, 222], np.float32)
    lw = max(1, int(round(0.12 * MM)))
    if kind == "grid":
        for k in range(int(W / CELL) + 1):
            x = int(round(k * CELL)); img[:, x:x + lw] = col
        for k in range(int(H / CELL) + 1):
            y = int(round(k * CELL)); img[y:y + lw, :] = col
    elif kind == "lines":
        y = top_y
        while y < H - 10 * MM:
            yi = int(round(y)); img[yi:yi + lw, int(15 * MM):W - int(10 * MM)] = col
            y += pitch
    return img


def layout(text, hand, xh_mm):
    W, H = A4
    left, right = 2 * CELL, W - 1.5 * CELL
    pitch = 2 * CELL if xh_mm <= 4.2 else 3 * CELL
    top, bottom = 3 * CELL, H - 2 * CELL
    space = SPACE * hand.xh
    pages, rows = [], []          # rows: list of (page_index, baseline_y, [(glyph, x)])
    page, y = 0, top

    def newline():
        nonlocal page, y
        y += pitch
        if y > bottom:
            page += 1
            y = top

    lines = text.replace("\r\n", "\n").split("\n")
    for raw in lines:
        for a, b in NORMALIZE.items():
            raw = raw.replace(a, b)
        raw = fix_quotes(raw)
        if raw.strip() == "====":
            if rows and rows[-1][0] == page:
                page += 1; y = top
            continue
        center = raw.startswith("# ")
        body = raw[2:] if center else raw
        indent = (len(body) - len(body.lstrip(" "))) * 0.5 * hand.xh
        words = body.split()
        if not words:
            rows.append((page, y, [])); newline(); continue
        cur, x = [], left + indent
        for w in words:
            placed, wlen = hand.word(w)
            if cur and x + wlen > right:
                rows.append((page, y, cur, center)); newline()
                cur, x = [], left
            cur.extend((g, x + dx) for g, dx in placed)
            x += wlen + space
        rows.append((page, y, cur, center)); newline()
    return rows, pitch, top


def fix_quotes(s):
    out, open_ = [], True
    for i, ch in enumerate(s):
        if ch in "\"“”„":
            out.append("«" if open_ else "»"); open_ = not open_
        else:
            out.append(ch)
    return "".join(out)


def draw(rows, kind, ink, pitch, top):
    W, H = A4
    n_pages = max(r[0] for r in rows) + 1 if rows else 1
    pages = [paper(kind, top, pitch) for _ in range(n_pages)]
    alpha = [np.zeros((H, W), np.float32) for _ in range(n_pages)]
    for row in rows:
        if len(row) == 3 or not row[2]:
            continue
        p, by, items, center = row
        shift = 0.0
        if center:
            x0 = min(x + g["x0"] for g, x in items); x1 = max(x + g["x1"] for g, x in items)
            shift = (W - (x1 - x0)) / 2 - x0
        A = alpha[p]
        for g, x in items:
            a = g["a"]; h, w = a.shape
            X = int(round(x + shift)); Y = int(round(by - g["base"]))
            xa, ya = max(0, -X), max(0, -Y)
            xb, yb = min(w, W - X), min(h, H - Y)
            if xb <= xa or yb <= ya:
                continue
            sub = A[Y + ya:Y + yb, X + xa:X + xb]
            np.maximum(sub, a[ya:yb, xa:xb], out=sub)
    out = []
    inkc = np.array(INKS[ink], np.float32)
    for img, A in zip(pages, alpha):
        img = img * (1 - A[..., None]) + inkc * A[..., None]
        out.append(Image.fromarray(img.clip(0, 255).astype(np.uint8)))
    return out


def save_pdf(images, path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4 as RA4
    from reportlab.lib.utils import ImageReader
    c = canvas.Canvas(str(path), pagesize=RA4)
    for im in images:
        c.drawImage(ImageReader(im), 0, 0, width=RA4[0], height=RA4[1])
        c.showPage()
    c.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--paper", default="grid", choices=["grid", "lines", "plain"])
    ap.add_argument("--xh", type=float, default=2.4, help="lowercase body (x-)height in mm")
    ap.add_argument("--ink", default="black", choices=list(INKS))
    ap.add_argument("--png-dir", default=None)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    text = Path(a.input).read_text(encoding="utf-8-sig")
    hand = Hand(a.xh, a.seed)
    rows, pitch, top = layout(text, hand, a.xh)
    images = draw(rows, a.paper, a.ink, pitch, top)
    save_pdf(images, a.output)
    if a.png_dir:
        d = Path(a.png_dir); d.mkdir(parents=True, exist_ok=True)
        for i, im in enumerate(images, 1):
            im.resize((im.width // 3, im.height // 3), Image.LANCZOS).save(d / f"page{i}.png")
    print(f"pages {len(images)}; units {hand.stats}")
    if hand.missing:
        print("MISSING (drawn with fallback font):", "".join(sorted(hand.missing)))


if __name__ == "__main__":
    main()
