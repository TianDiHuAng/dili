# -*- coding: utf-8 -*-
"""Natural Earth 物理图层叠加（河流/湖泊/地貌区域/冰川）。公有领域数据。"""
import json, os
import locator as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE = os.path.join(ROOT, "data", "geo", "ne")
Cache = {}

import subprocess
NEBASE = "https://cdn.jsdelivr.net/gh/nvkelso/natural-earth-vector@v5.1.2/geojson/"

def _ensure(name):
    p = os.path.join(NE, name + ".geojson")
    if not os.path.exists(p) or os.path.getsize(p) < 1000:
        os.makedirs(NE, exist_ok=True)
        subprocess.run(["curl", "-L", "-sS", "--ssl-no-revoke", "--compressed", "-m", "180",
                        "-A", "Mozilla/5.0", "-o", p, NEBASE + name + ".geojson"], capture_output=True)

def _load(name):
    if name in Cache: return Cache[name]
    _ensure(name)
    p = os.path.join(NE, name + ".geojson")
    Cache[name] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"features": []}
    return Cache[name]

def _iter_rings(geom):
    t = geom["type"]; c = geom["coordinates"]
    if t == "Polygon":
        for ring in c: yield ring, "poly"
    elif t == "MultiPolygon":
        for poly in c:
            for ring in poly: yield ring, "poly"
    elif t == "LineString":
        yield c, "line"
    elif t == "MultiLineString":
        for line in c: yield line, "line"

def _in_bbox(ring, bounds):
    lo = [p[0] for p in ring]; la = [p[1] for p in ring]
    return not (max(lo) < bounds[0] or min(lo) > bounds[1] or max(la) < bounds[2] or min(la) > bounds[3])

def _area(ring):
    a = 0.0
    for i in range(len(ring) - 1):
        a += ring[i][0]*ring[i+1][1]-ring[i+1][0]*ring[i][1]
    return abs(a)

def _simp(pts, target):
    if len(pts) <= target: return pts
    step = max(1, len(pts) // target)
    out = pts[::step]
    if out[-1] != pts[-1]: out.append(pts[-1])
    return out

TINT = {"Desert": ("#e8d39a", .55), "Plain": ("#cfe0c0", .5), "Plateau": ("#e3cfae", .55),
        "Basin": ("#dcd2c0", .55), "Range/mtn": ("#ccc3b3", .45), "Tundra": ("#dfe8ea", .6),
        "Wetlands": ("#cfe0e6", .6), "Lowland": ("#d9e2cf", .5)}

def overlay(box, bounds, title=None, max_regions=12, max_rivers=20, max_lakes=10):
    x0, y0, w, h = box
    def proj(lo, la): return L._project(lo, la, box, bounds)
    out = []
    # ---- 地貌区域 ----
    regs = _load("ne_50m_geography_regions_polys")["features"]
    cand = []
    for f in regs:
        fc = f["properties"].get("FEATURECLA")
        if fc not in TINT: continue
        nm = f["properties"].get("NAME_ZH") or f["properties"].get("NAME") or ""
        en = f["properties"].get("NAME") or ""
        hit = bool(title) and (title == nm or title in nm or nm in title or (title and title == en))
        for ring, kind in _iter_rings(f["geometry"]):
            if len(ring) < 4 or not _in_bbox(ring, bounds): continue
            cand.append((0 if hit else 1, _area(ring), fc, ring, nm, hit))
    cand.sort(key=lambda t: (t[0], -t[1]))
    for i, (_, ar, fc, ring, nm, hit) in enumerate(cand):
        if i >= max_regions and not hit: break
        col, op = TINT[fc]
        d = []
        for j, (lo, la) in enumerate(ring):
            px, py = proj(lo, la)
            if px < x0-30 or px > x0+w+30 or py < y0-30 or py > y0+h+30: continue
            d.append(("M" if not d else "L") + f"{px:.0f} {py:.0f}")
        if len(d) < 3: continue
        if hit:
            out.append(f"<path d='{' '.join(d)} Z' fill='{col}' fill-opacity='.78' stroke='#c0392b' stroke-width='1.8'/>")
            # 标签放在环的质心附近
            cx = sum(proj(lo, la)[0] for lo, la in ring)/len(ring); cy = sum(proj(lo, la)[1] for lo, la in ring)/len(ring)
            if x0 < cx < x0+w and y0 < cy < y0+h:
                out.append(f"<text x='{cx:.0f}' y='{cy:.0f}' class='lbl' text-anchor='middle'>{title}</text>")
        else:
            out.append(f"<path d='{' '.join(d)} Z' fill='{col}' fill-opacity='{op}' stroke='{col}' stroke-width='.4'/>")
    # ---- 湖泊 ----
    lakes = _load("ne_50m_lakes")["features"][:1400]
    n = 0
    for f in lakes:
        for ring, kind in _iter_rings(f["geometry"]):
            if n >= max_lakes: break
            if len(ring) < 4 or not _in_bbox(ring, bounds): continue
            d = []
            for lo, la in _simp(ring, 32):
                px, py = proj(lo, la)
                if px < x0-30 or px > x0+w+30 or py < y0-30 or py > y0+h+30: continue
                d.append(("M" if not d else "L") + f"{px:.0f} {py:.0f}")
            if len(d) < 3: continue
            out.append(f"<path d='{' '.join(d)} Z' fill='#a9cbe0' fill-opacity='.9' stroke='#6f9db8' stroke-width='.5'/>"); n += 1
    # ---- 河流 ----
    rivers = _load("ne_50m_rivers_lake_centerlines")["features"]
    n = 0
    for f in rivers:
        if n >= max_rivers: break
        for line, kind in _iter_rings(f["geometry"]):
            if n >= max_rivers: break
            if len(line) < 2 or not _in_bbox(line, bounds): continue
            d = []
            for lo, la in _simp(line, 32):
                px, py = proj(lo, la)
                if px < x0-20 or px > x0+w+20 or py < y0-20 or py > y0+h+20: continue
                d.append(("M" if not d else "L") + f"{px:.0f} {py:.0f}")
            if len(d) < 2: continue
            out.append(f"<path d='{' '.join(d)}' fill='none' stroke='#5b93b8' stroke-width='1.1' opacity='.85'/>"); n += 1
    # ---- 冰川 ----
    glaciers = _load("ne_10m_glaciated_areas")["features"]
    n = 0
    for f in glaciers:
        if n >= 6: break
        for ring, kind in _iter_rings(f["geometry"]):
            if n >= 6: break
            if len(ring) < 4 or not _in_bbox(ring, bounds): continue
            d = []
            for lo, la in ring:
                px, py = proj(lo, la)
                if px < x0-30 or px > x0+w+30 or py < y0-30 or py > y0+h+30: continue
                d.append(("M" if not d else "L") + f"{px:.0f} {py:.0f}")
            if len(d) < 3: continue
            out.append(f"<path d='{' '.join(d)} Z' fill='#eef4f6' fill-opacity='.85' stroke='#c3d3d9' stroke-width='.5'/>"); n += 1
    return "".join(out)
