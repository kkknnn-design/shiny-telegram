"""Cut the user's handwriting samples into glyph units (letters, pairs, words).

Reads assets/manifest.json, writes assets/glyphs.pkl and assets/contact_sheet.png.
Rule from experience: keep the raw strokes exactly as written - one global scale,
no redrawing, no per-letter resizing, no stroke-width changes.
"""
import json, pickle, sys
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
INK_T = 110          # pixels darker than this are "core" ink
ALPHA_HI, ALPHA_LO = 210, 50   # gray -> alpha ramp (keeps natural pen pressure)
DESC = set("рудзфщцДЦЩУФРЗ79,;()")      # units whose tails go below the line
NOT_BASE = DESC | set(".-—«»:?")


def find_rows(core, n_rows):
    cnt, lab, st, cen = cv2.connectedComponentsWithStats(core, 8)
    big = [i for i in range(1, cnt) if st[i, 4] >= 60]
    best = None
    for K in np.arange(-0.08, 0.081, 0.01):          # page may be slightly rotated
        yc = lambda i: cen[i][1] + K * (cen[i][0] - 100)
        for gap in (14, 12, 16, 10, 18):
            items = sorted(big, key=yc)
            groups = [[items[0]]]
            for i in items[1:]:
                if yc(i) - yc(groups[-1][-1]) > gap:
                    groups.append([i])
                else:
                    groups[-1].append(i)
            groups = [g for g in groups if len(g) > 1]
            if len(groups) == n_rows:
                best = (K, groups)
                break
        if best:
            break
    if not best:
        sys.exit(f"could not split image into {n_rows} rows")
    K, groups = best
    yc = lambda i: cen[i][1] + K * (cen[i][0] - 100)
    centers = [np.median([yc(i) for i in g]) for g in groups]
    rows = [[] for _ in groups]
    for i in range(1, cnt):
        if st[i, 4] < 5:
            continue
        d = [abs(yc(i) - c) for c in centers]
        r = int(np.argmin(d))
        if d[r] < 30:
            rows[r].append(i)
    return lab, st, rows


def group_row(ids, st, n, is_punct):
    ids = sorted(ids, key=lambda i: st[i, 0])
    for T in np.arange(-6, 20, 0.5):
        gs = []
        for i in ids:
            x, y, w, h, a = st[i]
            if gs and (x - gs[-1]["x1"] < T or (a < 60 and x < gs[-1]["x1"] + 6)):
                gs[-1]["ids"].append(i)
                gs[-1]["x1"] = max(gs[-1]["x1"], x + w)
                continue
            gs.append({"ids": [i], "x1": x + w})
        if not is_punct:
            gs = [q for q in gs if sum(st[i, 4] for i in q["ids"]) >= 40]
        if len(gs) == n:
            return gs
    return None


def build():
    man = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    units, xhs = {}, []
    for im_i, spec in enumerate(man["images"]):
        img = cv2.imread(str(ASSETS / spec["file"]))
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        b, gr, r = [c.astype(int) for c in cv2.split(img)]
        red = (r - np.maximum(gr, b) > 40).astype(np.uint8)       # spell-check underlines
        g[cv2.dilate(red, np.ones((5, 5), np.uint8)) > 0] = 255
        core = (g < INK_T).astype(np.uint8)
        lab, st, rows = find_rows(core, len(spec["rows"]))
        excl = {(e["unit"], e["row"]) for e in spec.get("exclude", [])}
        gf = g.astype(np.float32)
        raw = []
        for r_i, line in enumerate(spec["rows"]):
            labels = line.split()
            punct = all(not ch.isalnum() for ch in line.replace(" ", ""))
            gs = group_row(rows[r_i], st, len(labels), punct)
            if gs is None:
                sys.exit(f"{spec['file']} row {r_i}: could not split into {len(labels)} units: {line}")
            for q, key in zip(gs, labels):
                ids = q["ids"]
                x0 = min(st[i, 0] for i in ids); x1 = max(st[i, 0] + st[i, 2] for i in ids)
                y0 = min(st[i, 1] for i in ids); y1 = max(st[i, 1] + st[i, 3] for i in ids)
                raw.append({"key": key, "row": r_i, "ids": ids, "bbox": (x0, y0, x1, y1),
                            "skip": (key, r_i) in excl})
        # baseline line per row, fitted on bottoms of letters without tails
        pts = {}
        for u in raw:
            if not (set(u["key"]) & NOT_BASE):
                x0, y0, x1, y1 = u["bbox"]
                pts.setdefault(u["row"], []).append(((x0 + x1) / 2, y1))
        fits = {}
        for r_i in range(len(spec["rows"])):
            p = pts.get(r_i, [])
            if len(p) < 2:   # punctuation-only row: use flat small marks
                p = [((x0 + x1) / 2, y1) for u in raw if u["row"] == r_i
                     for (x0, y0, x1, y1) in [u["bbox"]] if u["key"] in ".:,"] or \
                    [((u["bbox"][0] + u["bbox"][2]) / 2, u["bbox"][3]) for u in raw if u["row"] == r_i]
            p = np.array(p, float)
            k, c0 = 0.0, float(np.median(p[:, 1]))
            for _ in range(3):
                if len(p) < 2:
                    break
                M = np.vstack([p[:, 0], np.ones(len(p))]).T
                k, c0 = np.linalg.lstsq(M, p[:, 1], rcond=None)[0]
                res = p[:, 1] - (k * p[:, 0] + c0)
                keep = np.abs(res - np.median(res)) < 5
                if keep.sum() >= 2:
                    p = p[keep]
            fits[r_i] = (k, c0)
        for u in raw:
            x0, y0, x1, y1 = u["bbox"]
            k, c0 = fits[u["row"]]
            u["base_abs"] = k * ((x0 + x1) / 2) + c0
            if u["key"] in list("аоесинмкх"):
                xhs.append(u["base_abs"] - y0)
        for u in raw:
            if u["skip"]:
                continue
            x0, y0, x1, y1 = u["bbox"]
            mg = 3
            X0, Y0, X1, Y1 = max(0, x0 - mg), max(0, y0 - mg), x1 + mg, y1 + mg
            sel = cv2.dilate(np.isin(lab[Y0:Y1, X0:X1], u["ids"]).astype(np.uint8), np.ones((3, 3), np.uint8))
            a = np.clip((ALPHA_HI - gf[Y0:Y1, X0:X1]) / (ALPHA_HI - ALPHA_LO), 0, 1) * sel
            units.setdefault(u["key"], []).append({
                "a": a.astype(np.float32), "base": float(u["base_abs"] - Y0),
                "src": f"{spec['file']}#row{u['row']}"})
    xh = float(np.median(xhs))
    # refine each unit's baseline from its own ink, drop stray marks below the line
    for key, vs in units.items():
        desc = bool(set(key) & DESC)
        for v in vs:
            a = v["a"] > 0.35
            b0 = v["base"]
            if not desc and key.isalpha():
                n, lb, s2, _ = cv2.connectedComponentsWithStats(a.astype(np.uint8), 8)
                for j in range(1, n):
                    if s2[j, 1] > b0 + 0.25 * xh and s2[j, 3] < 0.5 * xh:
                        v["a"][lb == j] = 0
                a = v["a"] > 0.35
            cols = np.where(a.any(0))[0]
            if len(cols) < 4 or not key.isalpha():
                continue
            bottoms = np.array([np.where(a[:, c])[0].max() + 1 for c in cols], float)
            hi = 0.1 * xh if desc else 0.25 * xh
            keep = bottoms[(bottoms > b0 - 0.35 * xh) & (bottoms < b0 + hi)]
            if len(keep) >= 3:
                nb = float(np.percentile(keep, 70 if desc else 85))
                if abs(nb - b0) < 0.3 * xh:
                    v["base"] = nb
    body = assess(units, xh)
    alpha_only = {k: list(v) for k, v in units.items()}
    contact_sheet(alpha_only, xh)
    if (ASSETS / "natural" / "words.json").exists():
        from natural_words import word_units, chunk_sheet
        nat = word_units(body, alpha_only)
        assess(nat, xh, target_body=body)
        for key, vs in nat.items():
            if len(key) == 1 and key in units:
                continue      # one-letter words (я, в, с…): body height can't be measured; use the alphabet
            vs.sort(key=lambda v: v["score"])
            units.setdefault(key, []).extend(vs[:6])          # keep the nicest few of each
        chunk_sheet(nat, ASSETS / "natural" / "chunk_sheet.png")
    for vs in units.values():
        for v in vs:
            v["a"] = (np.clip(v["a"], 0, 1) * 255).astype(np.uint8)   # compact storage
    pickle.dump({"xh": xh, "body": body, "units": units}, open(ASSETS / "glyphs.pkl", "wb"))
    singles = sorted(k for k in units if len(k) == 1)
    multi = sorted(k for k in units if len(k) > 1)
    print(f"x-height {xh:.1f}px; {len(singles)} single chars, {len(multi)} joined units, "
          f"{sum(len(v) for v in units.values())} variants")
    print("chars:", "".join(singles))


ASC = set("бвф")                        # her lowercase letters that rise above the x-height
LOWER = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")


def body_band(v, key, xh):
    """Top and bottom of the x-height body (ignores ascenders, tails, dots and breves)."""
    a = v["a"] > 0.35
    b = v["base"]
    H = a.shape[0]
    p = a.sum(1).astype(float)
    lo, hi = max(0, int(b - 1.1 * xh)), min(H, int(b) + 1)
    m = p[lo:hi].max() if hi > lo else 0
    if m == 0:
        return None
    thr = 0.3 * m
    down = int(b + (0.08 if set(key) & set(DESC) else 0.3) * xh)
    rows_b = [r for r in range(max(0, int(b - 0.5 * xh)), min(H, down)) if p[r] >= thr]
    rows_t = [r for r in range(max(0, int(b - 1.6 * xh)), max(0, int(b - 0.4 * xh))) if p[r] >= thr]
    if not rows_b or not rows_t:
        return None
    return float(rows_t[0]), float(rows_b[-1] + 1)


def stroke_slant(a):
    """Slant from the direction of near-vertical stroke edges (robust for short pieces).
    Returns k = x shift per unit of height going up (right-leaning > 0), or None."""
    f = cv2.GaussianBlur(np.clip(a.astype(np.float32), 0, 1), (0, 0), 1.2)
    gx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    sel = (mag > 0.25 * mag.max()) & (np.abs(gx) > 1.5 * np.abs(gy))     # edges of steep strokes
    if sel.sum() < 15:
        return None
    k = gy[sel] / gx[sel]                 # edge normal (gx, gy) -> stroke direction slope
    w = mag[sel]
    o = np.argsort(k)
    cw = np.cumsum(w[o])
    return float(k[o][np.searchsorted(cw, cw[-1] / 2)])


def slant_of(a):
    """Shear k (x shift per pixel of height) that makes strokes most vertical."""
    m = (a > 0.35).astype(np.float32)
    h, w = m.shape
    best, bk = -1, 0.0
    for k in np.arange(-0.8, 0.81, 0.05):
        M = np.float32([[1, k, -k * h if k > 0 else 0], [0, 1, 0]])
        sh = cv2.warpAffine(m, M, (w + int(abs(k) * h) + 2, h))
        e = float((sh.sum(0) ** 2).sum())
        if e > best:
            best, bk = e, float(k)
    return bk


def assess(units, xh, target_body=None):
    """Measure every variant (body size, baseline, slant, ink blobs) and score how good it looks.
    Lower score = nicer. render.py uses 'f' (size fix), 'shear' (slant fix), 'top'/'bot', 'score'."""
    from skimage.morphology import skeletonize
    for key, vs in units.items():
        for v in vs:
            v["f"], v["shear"], v["dev"] = 1.0, 0.0, 0.0
            if not v.get("natural"):      # natural pieces already carry a measured body band
                band = body_band(v, key, xh) if all(c in LOWER for c in key) else None
                v["top"], v["bot"] = band if band else (v["base"] - xh, v["base"])
            ss = stroke_slant(v["a"]) if key.isalnum() else None
            v["slant"] = ss / 0.75 if ss is not None else None      # 0.75: estimator gain (calibrated)
            m = v["a"] > 0.35
            dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
            sk = skeletonize(m)
            half = float(np.median(dt[sk])) if sk.any() else 1.0
            v["blob"] = float(dt.max() / max(half, 0.5))      # filled loops -> big blobs
    # size groups: lowercase body height; capitals and digits total height above the line
    def ht(v):
        a = v["a"] > 0.35
        rows = np.where(a.any(1))[0]
        return v["base"] - rows.min()
    groups = {"low": [], "cap": [], "dig": [], "nat": []}
    for key, vs in units.items():
        for v in vs:
            if v.get("natural"):
                if not v.get("cjk"):
                    v["meas"] = v["bot"] - v["top"]; groups["nat"].append(v)
            elif all(c in LOWER for c in key) and not (set(key) & ASC):
                v["meas"] = v["bot"] - v["top"]; groups["low"].append(v)
            elif len(key) == 1 and key.isupper():
                v["meas"] = ht(v); groups["cap"].append(v)
            elif len(key) == 1 and key.isdigit():
                v["meas"] = ht(v); groups["dig"].append(v)
    for name, vs in groups.items():
        if not vs:
            continue
        med = float(np.median([v["meas"] for v in vs])) if name != "nat" or target_body is None else target_body
        for v in vs:
            raw = med / max(v["meas"], 1.0)
            v["dev"] = abs(np.log(raw))
            v["f"] = float(np.clip(raw, 0.8, 1.25))
            if name == "low":    # body now exactly med tall: snap top/bot to the body band
                v["bot_fix"] = True
    slants = [v["slant"] for vs in units.values() for v in vs if v["slant"] is not None]
    target = float(np.median(slants))
    for key, vs in units.items():
        for v in vs:
            sd = 0.0
            if v["slant"] is not None:
                sd = abs(v["slant"] - target)
                v["shear"] = float(np.clip(v["slant"] - target, -0.2, 0.2))
            v["score"] = 2.0 * v["dev"] + 0.6 * max(0.0, v["blob"] - 2.2) + 1.2 * sd
    body = float(np.median([v["meas"] for v in groups["low"]])) if groups["low"] else float(target_body or 0)
    print(f"sample slant {target:.2f}; lowercase body median {body:.1f}px")
    return body


def contact_sheet(units, xh):
    H = int(4 * xh)
    tiles, lines = [], []
    for key in sorted(units, key=lambda k: (len(k), k)):
        for v in units[key]:
            a = v["a"]; top = int(round(2.2 * xh - v["base"]))
            t = np.full((H, a.shape[1] + 6), 255, np.uint8)
            y0 = max(0, top); ys = y0 - top
            h = min(a.shape[0] - ys, H - y0)
            t[y0:y0 + h, 3:3 + a.shape[1]] = (255 * (1 - a[ys:ys + h])).astype(np.uint8)
            t = cv2.cvtColor(t, cv2.COLOR_GRAY2BGR)
            t[int(2.2 * xh), :] = (0, 0, 255)
            ty = int(round(v.get("top", v["base"] - xh) + top))
            if 0 <= ty < H:
                t[ty, :] = (0, 170, 0)
            cv2.putText(t, f"{v.get('score', 0):.1f}", (2, H - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 0, 0), 1)
            tiles.append(t)
            if sum(x.shape[1] for x in tiles) > 1400:
                lines.append(np.hstack(tiles)); tiles = []
    if tiles:
        lines.append(np.hstack(tiles))
    W = max(l.shape[1] for l in lines)
    sheet = np.vstack([np.pad(l, ((0, 2), (0, W - l.shape[1]), (0, 0)), constant_values=200) for l in lines])
    cv2.imwrite(str(ASSETS / "contact_sheet.png"), sheet)


if __name__ == "__main__":
    build()
