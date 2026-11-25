# -*- coding: utf-8 -*-
"""世界银行 API 真实指标序列 → 内联 SVG 折线图（含数值与年份）。"""
import json, os, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "geo", "wb")
BASE = "https://api.worldbank.org/v2/country/{c}/indicator/{ind}?format=json&per_page=80&date=1960:2024"

def _path(ind, c): return os.path.join(CACHE, f"{ind}_{c}.json")

_last = [0.0]
def _ok(d):
    return isinstance(d, list) and len(d) > 1 and isinstance(d[1], list)

def series(ind, c="WLD"):
    os.makedirs(CACHE, exist_ok=True)
    p = _path(ind, c)
    d = None
    if os.path.exists(p) and os.path.getsize(p) > 40:
        try: d = json.load(open(p, encoding="utf-8"))
        except Exception: d = None
    if not _ok(d):
        url = BASE.format(c=c, ind=ind)
        for _ in range(6):
            dt = time.time() - _last[0]
            if dt < 1.2: time.sleep(1.2 - dt)
            subprocess.run(["curl", "-L", "-sS", "--ssl-no-revoke", "--compressed", "-m", "60",
                            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "-H", "Accept: application/json", "-o", p, url], capture_output=True)
            _last[0] = time.time()
            try: d = json.load(open(p, encoding="utf-8"))
            except Exception: d = None
            if _ok(d) and d[1]:
                break
            time.sleep(2.5)
        if not _ok(d) or not d[1]:
            try: os.remove(p)
            except Exception: pass
            return []
    rows = d[1]
    vals = [(int(r["date"]), float(r["value"])) for r in rows if r.get("value") is not None]
    vals.sort()
    return vals

def _fmt(v):
    a = abs(v)
    if a >= 1e9: return f"{v/1e9:.2f}e9"
    if a >= 1e6: return f"{v/1e6:.1f}M"
    if a >= 1e4: return f"{v/1e3:.1f}k"
    if a >= 100: return f"{v:.0f}"
    if a >= 10: return f"{v:.1f}"
    return f"{v:.2f}"

def panel(box, vals, title, label, unit):
    x0, y0, w, h = box
    s = [f"<rect x='{x0}' y='{y0}' width='{w}' height='{h}' rx='8' fill='#f7f4ec' stroke='var(--line)'/>"]
    if not vals:
        s.append(f"<text x='{x0+20}' y='{y0+40}' class='lbl-s'>{label}：数据暂缺</text>")
        return "".join(s), None
    xs = [v[0] for v in vals]; ys = [v[1] for v in vals]
    minv, maxv = min(ys), max(ys); xmin, xmax = min(xs), max(xs)
    pad_l, pad_r, pad_t, pad_b = 70, 30, 24, 34
    def px(x): return x0 + pad_l + (x - xmin) / max(1, (xmax - xmin)) * (w - pad_l - pad_r)
    def py(y): return y0 + h - pad_b - (y - minv) / max(1e-9, (maxv - minv)) * (h - pad_t - pad_b)
    # 轴
    s.append(f"<path d='M{x0+pad_l} {y0+pad_t} L{x0+pad_l} {y0+h-pad_b} L{x0+w-pad_r} {y0+h-pad_b}' fill='none' stroke='var(--line)' stroke-width='1'/>")
    # 折线
    pts = " ".join(f"{px(x):.0f} {py(y):.0f}" for x, y in vals)
    s.append(f"<polyline points='{pts}' fill='none' stroke='#2f6f8f' stroke-width='2.4'/>")
    # 末点
    lx, ly = px(xs[-1]), py(ys[-1])
    s.append(f"<circle cx='{lx:.0f}' cy='{ly:.0f}' r='4' fill='#c0392b'/>")
    s.append(f"<text x='{min(lx+6, x0+w-70):.0f}' y='{ly-6:.0f}' class='lbl-s'>{_fmt(ys[-1])}</text>")
    # 年/值标注
    s.append(f"<text x='{x0+pad_l}' y='{y0+h-pad_b+18}' class='lbl-s'>{xs[0]}</text>")
    s.append(f"<text x='{x0+w-pad_r-40}' y='{y0+h-pad_b+18}' class='lbl-s'>{xs[-1]}</text>")
    s.append(f"<text x='{x0+6}' y='{y0+pad_t+4}' class='lbl-s'>{_fmt(maxv)}</text>")
    s.append(f"<text x='{x0+6}' y='{y0+h-pad_b}' class='lbl-s'>{_fmt(minv)}</text>")
    s.append(f"<text x='{x0+pad_l}' y='{y0+18}' class='lbl'>{label}（{unit}）· 世界银行 WLD，{xs[0]}–{xs[-1]}</text>")
    s.append(f"<text x='{x0+pad_l}' y='{y0+h-6}' class='dim'>数据：World Bank API（{title}）；真实数值，非示意</text>")
    return "".join(s), (xs[-1], ys[-1])
