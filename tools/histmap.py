# -*- coding: utf-8 -*-
"""historical-basemaps（aourednik, CC BY 4.0）年代快照 → 裁剪到视野、高亮所属政权。"""
import json, os, subprocess, time
import locator as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "data", "geo", "hist")
BASE = "https://cdn.jsdelivr.net/gh/aourednik/historical-basemaps@master/geojson/"
YEARS = [-123000,-10000,-8000,-5000,-4000,-3000,-2000,-1500,-1000,-700,-500,-400,-323,-300,-200,-100,-1,
         100,200,300,400,500,600,700,800,900,1000,1100,1200,1279,1300,1400,1492,1500,1530,1600,1650,
         1700,1715,1783,1800,1815,1878,1880,1900,1914,1920,1930,1938,1945,1960,1994,2000,2010]
_C = {}
PALETTE = ["#c9b28a","#a8bfa0","#c99f92","#9fb2c8","#c9c08e","#b7a0c0","#d0b48c","#9fc0bd","#c2a7a0","#b0b48a"]

def nearest(y):
    return min(YEARS, key=lambda v: abs(v - y))

def _fname(y):
    return ("world_bc%d" % (-y)) if y < 0 else ("world_%d" % y)

def _load(y):
    if y in _C: return _C[y]
    os.makedirs(HIST, exist_ok=True)
    p = os.path.join(HIST, _fname(y) + ".geojson")
    for _try in range(3):
        if os.path.exists(p) and os.path.getsize(p) > 5000:
            break
        subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","240","-A","Mozilla/5.0","-o",p,BASE+_fname(y)+".geojson"],capture_output=True)
        time.sleep(1.5)
    try:
        _C[y] = json.load(open(p,encoding="utf-8"))
    except Exception:
        _C[y] = {"features": []}
    return _C[y]

def _rings(geom):
    if geom["type"]=="Polygon":
        return [geom["coordinates"]]
    if geom["type"]=="MultiPolygon":
        return geom["coordinates"]
    return []

def _area(ring):
    a=0.0
    for i in range(len(ring)-1):
        a+=ring[i][0]*ring[i+1][1]-ring[i+1][0]*ring[i][1]
    return abs(a)

def _pip(lon,lat,ring):
    inside=False; n=len(ring); j=n-1
    for i in range(n):
        xi,yi=ring[i][0],ring[i][1]; xj,yj=ring[j][0],ring[j][1]
        if ((yi>lat)!=(yj>lat)) and (lon < (xj-xi)*(lat-yi)/(yj-yi+1e-12)+xi):
            inside=not inside
        j=i
    return inside

def _simp(pts,target):
    if len(pts)<=target: return pts
    st=max(1,len(pts)//target); out=pts[::st]
    if out[-1]!=pts[-1]: out.append(pts[-1])
    return out

def overlay(box, bounds, year, point=None, title=None, max_polys=60):
    x0,y0,w,h=box
    def proj(lo,la): return L._project(lo,la,box,bounds)
    data=_load(year)
    feats=[]
    for f in data["features"]:
        polys=_rings(f["geometry"])
        # 面积（度²）近似 + bbox 相交
        pmax=0
        for poly in polys:
            ring=poly[0]
            if len(ring)<4: continue
            lo=[p[0] for p in ring]; la=[p[1] for p in ring]
            if max(lo)<bounds[0] or min(lo)>bounds[1] or max(la)<bounds[2] or min(la)>bounds[3]: continue
            pmax=max(pmax,_area(ring))
        if pmax>0:
            feats.append((pmax,f))
    feats.sort(key=lambda t:-t[0]); feats=feats[:max_polys]
    out=[]
    hit_name=None
    for idx,(ar,f) in enumerate(feats):
        nm=f["properties"].get("SUBJECTO") or f["properties"].get("NAME") or ""
        col=PALETTE[idx % len(PALETTE)]
        is_hit=False
        for poly in _rings(f["geometry"]):
            for ri,ring in enumerate(poly):
                if len(ring)<4: continue
                if point and ri==0 and _pip(point[0],point[1],ring): is_hit=True
                d=[]
                for lo,la in _simp(ring,40):
                    px,py=proj(lo,la)
                    if px<x0-25 or px>x0+w+25 or py<y0-25 or py>y0+h+25: continue
                    d.append(("M" if not d else "L")+f"{px:.0f} {py:.0f}")
                if len(d)<3: continue
                if is_hit:
                    out.append(f"<path d='{' '.join(d)} Z' fill='{col}' fill-opacity='.85' stroke='#c0392b' stroke-width='1.6'/>")
                else:
                    out.append(f"<path d='{' '.join(d)} Z' fill='{col}' fill-opacity='.55' stroke='{col}' stroke-width='.5'/>")
        if is_hit and not hit_name: hit_name=nm
    if point:
        px,py=proj(point[0],point[1])
        if x0<=px<=x0+w and y0<=py<=y0+h:
            out.append(f"<circle cx='{px:.0f}' cy='{py:.0f}' r='5' fill='#c0392b' stroke='#7a1f14'/>")
            if hit_name:
                out.append(f"<text x='{min(px+10,x0+w-120):.0f}' y='{py-8:.0f}' class='lbl'>{hit_name}</text>")
    return "".join(out), hit_name
