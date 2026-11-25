# -*- coding: utf-8 -*-
"""从 world-atlas countries-110m TopoJSON 解码中国陆地轮廓，生成内联 SVG 定位图。"""
import json, os, math, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "geo", "countries-110m.json")
URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"


def _ensure_cache():
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    if not os.path.exists(CACHE) or os.path.getsize(CACHE) < 50000:
        r = subprocess.run(["curl", "-L", "-sS", "--ssl-no-revoke", "--compressed", "-m", "40",
                            "-A", "Mozilla/5.0", "-o", CACHE, URL], capture_output=True)
        if not os.path.exists(CACHE):
            raise RuntimeError("下载 TopoJSON 失败")


def _decode_arcs(topo):
    tr = topo.get("transform")
    sx, sy = tr["scale"]; tx, ty = tr["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def _ring_points(ring, arcs):
    pts = []
    for idx in ring:
        if idx >= 0:
            seg = arcs[idx]
        else:
            seg = list(reversed(arcs[~idx]))
        if pts and seg:
            pts.extend(seg[1:])
        else:
            pts.extend(seg)
    return pts


def china_rings():
    """返回中国陆地各环的经纬度点列（取面积最大的若干环）。"""
    _ensure_cache()
    topo = json.load(open(CACHE, encoding="utf-8"))
    arcs = _decode_arcs(topo)
    geoms = topo["objects"]["countries"]["geometries"]
    # 中国本体（156）+ 台湾（158）合并为一国轮廓
    want = {"156", "158"}
    picked = [it for it in geoms if str(it.get("id")) in want
              or it.get("properties", {}).get("name") in ("China", "Taiwan")]
    if not picked:
        raise RuntimeError("未找到 China/Taiwan 几何")
    rings = []
    for g in picked:
        if g["type"] == "Polygon":
            for ring in g["arcs"]:
                rings.append(_ring_points(ring, arcs))
        else:
            for poly in g["arcs"]:
                for ring in poly:
                    rings.append(_ring_points(ring, arcs))
    # 面积（经纬度近似）排序
    def area(r):
        a = 0
        for i in range(len(r) - 1):
            a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]
        return abs(a)
    rings.sort(key=area, reverse=True)
    return rings


def _project(lon, lat, box, bounds):
    lon0, lon1, lat0, lat1 = bounds
    x0, y0, w, h = box
    # 等距圆柱 + 纬度余弦校正（以中纬为基准），保证东西不拉伸
    k = math.cos(math.radians((lat0 + lat1) / 2))
    spanx = (lon1 - lon0) * k
    spany = (lat1 - lat0)
    s = min(w / spanx, h / spany)
    cx = x0 + w / 2; cy = y0 + h / 2
    mx = (lon0 + lon1) / 2; my = (lat0 + lat1) / 2
    px = cx + (lon - mx) * k * s
    py = cy - (lat - my) * s
    return px, py


def locator_svg(lon, lat, label, box=(30, 34, 840, 210), bounds=(72, 137, 16, 55)):
    """返回 900x? 画布内的定位图片段（含国界轮廓、经纬网刻度、标记点与标签）。"""
    rings = china_rings()
    x0, y0, w, h = box
    parts = []
    # 外框
    parts.append(f"<rect x='{x0-10}' y='{y0-16}' width='{w+20}' height='{h+34}' rx='10' fill='none' stroke='var(--line)'/>")
    # 经纬网刻度（淡）
    for lo in (80, 100, 120):
        px, _ = _project(lo, bounds[2], box, bounds)
        parts.append(f"<path d='M{px:.1f} {y0} L{px:.1f} {y0+h}' stroke='var(--line)' stroke-width='.7' opacity='.6'/>")
        parts.append(f"<text x='{px-10:.1f}' y='{y0+h+14}' class='lbl-s'>{lo}°E</text>")
    for la in (20, 30, 40, 50):
        _, py = _project(bounds[0], la, box, bounds)
        parts.append(f"<path d='M{x0} {py:.1f} L{x0+w} {py:.1f}' stroke='var(--line)' stroke-width='.7' opacity='.6'/>")
        parts.append(f"<text x='{x0-8:.1f}' y='{py+4:.1f}' class='lbl-s' text-anchor='end'>{la}°N</text>")
    # 中国陆地轮廓（每个环一条 path）
    for ring in rings[:6]:
        d = []
        for i, (lo, la) in enumerate(ring):
            px, py = _project(lo, la, box, bounds)
            d.append(('M' if i == 0 else 'L') + f"{px:.1f} {py:.1f}")
        parts.append("<path d='" + ' '.join(d) + " Z' fill='#e8e2d2' stroke='#8a8272' stroke-width='1'/>")
    # 标记点
    px, py = _project(lon, lat, box, bounds)
    parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='6' fill='#c0392b' stroke='#7a1f14' stroke-width='1.4'/>")
    parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='11' fill='none' stroke='#c0392b' stroke-width='1' opacity='.6'/>")
    lx = px + 14 if px < x0 + w - 150 else px - 150
    parts.append(f"<path d='M{px:.1f} {py:.1f} L{lx:.1f} {py-24:.1f}' stroke='#c0392b' stroke-width='1'/>")
    parts.append(f"<text x='{lx:.1f}' y='{py-28:.1f}' class='lbl'>{label}</text>")
    # 说明
    parts.append(f"<text x='{x0-8}' y='{y0-6}' class='lbl-s'>位置图（中国大陆轮廓示意；国界不作政治主张）</text>")
    return "".join(parts)


if __name__ == "__main__":
    rings = china_rings()
    lons = [p[0] for r in rings[:6] for p in r]; lats = [p[1] for r in rings[:6] for p in r]
    print("rings", len(rings), "points", sum(len(r) for r in rings[:6]))
    print("bbox lon %.1f..%.1f lat %.1f..%.1f" % (min(lons), max(lons), min(lats), max(lats)))


def combine(existing_svg, lon, lat, label):
    """把定位图叠加到既有剖面图上方，返回 900x760 的合成 SVG。"""
    inner = existing_svg.strip()
    inner = inner[inner.index(">") + 1: inner.rindex("</svg>")]
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760' role='img' aria-label='位置图与剖面示意图'>"
            + locator_svg(lon, lat, label) + "<g transform='translate(0,258)'>" + inner + "</g></svg>")


def combine_inner(inner, lon, lat, label):
    """inner 为不含 <svg> 包裹的绘图内容；返回 900x760 合成 SVG（定位图在上、剖面在下）。"""
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760' role='img' aria-label='位置图与剖面示意图'>"
            + locator_svg(lon, lat, label) + "<g transform='translate(0,258)'>" + inner + "</g></svg>")


_ALL = None

def all_rings():
    """全部国家陆地环（经纬度点列），带面积过滤，供大洲/世界底图使用。"""
    global _ALL
    if _ALL is not None:
        return _ALL
    _ensure_cache()
    topo = json.load(open(CACHE, encoding="utf-8"))
    arcs = _decode_arcs(topo)
    out = []
    for g in topo["objects"]["countries"]["geometries"]:
        polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"]
        for poly in polys:
            for ring in poly:
                pts = _ring_points(ring, arcs)
                if len(pts) >= 4:
                    out.append(pts)
    _ALL = out
    return out


def _area(r):
    a = 0.0
    for i in range(len(r) - 1):
        a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]
    return abs(a)


def map_svg(box, bounds, lon=None, lat=None, label=None, overlay=None):
    """在给定 box 内画 bbox 范围内的真实陆地轮廓，可标点。返回 (frag, project_fn)。"""
    x0, y0, w, h = box
    parts = [f"<rect x='{x0}' y='{y0}' width='{w}' height='{h}' rx='8' fill='#eef1f3' stroke='var(--line)'/>"]
    def proj(lo, la):
        return _project(lo, la, box, bounds)
    # 经纬网
    lon0, lon1, lat0, lat1 = bounds
    step_lon = 30 if lon1 - lon0 > 90 else 20
    lo = int((lon0 // step_lon + 1) * step_lon)
    while lo < lon1:
        px, _ = proj(lo, lat0)
        parts.append(f"<path d='M{px:.1f} {y0} L{px:.1f} {y0+h}' stroke='#cfd6da' stroke-width='.6'/>")
        lo += step_lon
    step_lat = 20 if lat1 - lat0 > 60 else 10
    la = int((lat0 // step_lat + 1) * step_lat)
    while la < lat1:
        _, py = proj(lon0, la)
        parts.append(f"<path d='M{x0} {py:.1f} L{x0+w} {py:.1f}' stroke='#cfd6da' stroke-width='.6'/>")
        la += step_lat
    # 陆地
    for ring in all_rings():
        rlo = [p[0] for p in ring]; rla = [p[1] for p in ring]
        if max(rlo) < lon0 or min(rlo) > lon1 or max(rla) < lat0 or min(rla) > lat1:
            continue
        if _area(ring) < 3.0:
            continue
        _r = ring if len(ring) <= 55 else ring[::max(1, len(ring)//55)]
        d = []
        for i, (plo, pla) in enumerate(_r):
            px, py = proj(plo, pla)
            if px < x0 - 20 or px > x0 + w + 20 or py < y0 - 20 or py > y0 + h + 20:
                continue
            d.append(('M' if not d else 'L') + f"{px:.1f} {py:.1f}")
        if len(d) > 3:
            parts.append("<path d='" + ' '.join(d) + " Z' fill='#e5dfd0' stroke='#9a9384' stroke-width='.8'/>")
    if overlay:
        parts.append(overlay)
    if lon is not None and lat is not None:
        px, py = proj(lon, lat)
        if px < x0 or px > x0 + w or py < y0 or py > y0 + h:
            return "".join(parts)  # 点落在图外则只画底图
        parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='6' fill='#c0392b' stroke='#7a1f14' stroke-width='1.3'/>")
        parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='11' fill='none' stroke='#c0392b' stroke-width='.9' opacity='.55'/>")
        if label:
            lx = px + 14 if px < x0 + w - 160 else px - 160
            parts.append(f"<path d='M{px:.1f} {py:.1f} L{lx:.1f} {py-22:.1f}' stroke='#c0392b' stroke-width='.9'/>")
            parts.append(f"<text x='{lx:.1f}' y='{py-26:.1f}' class='lbl'>{label}</text>")
    return "".join(parts)
