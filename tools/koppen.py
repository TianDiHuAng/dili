# -*- coding: utf-8 -*-
"""Köppen-Geiger 气候分区（矢量，Beck et al.；数据经 rjerue/koppen-map）。"""
import json, os, time
import locator as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "geo", "koppen.geojson")
_C = None
GROUP = {"A": "#6fae6a", "B": "#e0c078", "C": "#a9d0a0", "D": "#9fb8d8", "E": "#dfe8ea"}
CN = {"Af":"热带雨林","Am":"热带季风","Aw":"热带草原","BWh":"热带沙漠","BWk":"冷沙漠","BSh":"半干旱(热)","BSk":"半干旱(冷)",
      "Cfa":"副热带湿润","Cfb":"温带海洋性","Csa":"地中海(夏干热)","Csb":"地中海(夏干暖)","Cwa":"副热带季风","Cwb":"高地季风",
      "Dfa":"温带大陆性湿润","Dfb":"温带大陆性","Dwa":"冷温带季风","Dwb":"冷温带","Dfc":"亚寒带","Dwc":"亚寒带",
      "ET":"苔原","EF":"冰原"}

URL = "https://cdn.jsdelivr.net/gh/rjerue/koppen-map@main/raw-data.json"
def _load():
    global _C
    if _C is None:
        if not os.path.exists(P) or os.path.getsize(P) < 50000:
            import subprocess
            os.makedirs(os.path.dirname(P), exist_ok=True)
            subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","240","-A","Mozilla/5.0","-o",P,URL],capture_output=True)
        _C = json.load(open(P, encoding="utf-8")) if os.path.exists(P) else {"features": []}
    return _C

def _rings(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon": return geom["coordinates"]
    return []

def _pip(lon, lat, ring):
    inside=False; n=len(ring); j=n-1
    for i in range(n):
        xi,yi=ring[i][0],ring[i][1]; xj,yj=ring[j][0],ring[j][1]
        if ((yi>lat)!=(yj>lat)) and (lon < (xj-xi)*(lat-yi)/(yj-yi+1e-12)+xi): inside=not inside
        j=i
    return inside

def _area(ring):
    a=0.0
    for i in range(len(ring)-1): a+=ring[i][0]*ring[i+1][1]-ring[i+1][0]*ring[i][1]
    return abs(a)

def _simp(pts,t):
    if len(pts)<=t: return pts
    st=max(1,len(pts)//t); out=pts[::st]
    if out[-1]!=pts[-1]: out.append(pts[-1])
    return out

def cn_of(climate):
    code = climate.split(" ")[0]
    for k,v in CN.items():
        if code.startswith(k): return v, k
    return climate.split(" ")[-1], code

def overlay(box, bounds, point=None, max_polys=70, alpha=0.62, alpha_hit=0.9):
    x0,y0,w,h=box
    def proj(lo,la): return L._project(lo,la,box,bounds)
    data=_load(); feats=[]
    for f in data["features"]:
        polys=_rings(f["geometry"]); pmax=0
        for poly in polys:
            ring=poly[0]
            if len(ring)<4: continue
            lo=[p[0] for p in ring]; la=[p[1] for p in ring]
            if max(lo)<bounds[0] or min(lo)>bounds[1] or max(la)<bounds[2] or min(la)>bounds[3]: continue
            pmax=max(pmax,_area(ring))
        if pmax>0: feats.append((pmax,f))
    feats.sort(key=lambda t:-t[0]); feats=feats[:max_polys]
    out=[]; hit=None; drawn=0; MAXP=200; groups={};
    for ar,f in feats:
        if drawn>=MAXP: break
        cl=f["properties"].get("climate",""); code=cl.split(" ")[0]; grp=code[0] if code else "C"
        col=GROUP.get(grp,"#a9d0a0")
        is_hit=False
        for poly in _rings(f["geometry"]):
            for ri,ring in enumerate(poly):
                if len(ring)<4 or _area(ring)<1.5: continue
                if point and ri==0 and _pip(point[0],point[1],ring): is_hit=True
                d=[]
                for lo,la in _simp(ring,18):
                    px,py=proj(lo,la)
                    if px<x0-25 or px>x0+w+25 or py<y0-25 or py>y0+h+25: continue
                    d.append(("M" if not d else "L")+f"{px:.0f} {py:.0f}")
                if len(d)<3: continue
                drawn+=1
                if is_hit:
                    out.append(f"<path d='{' '.join(d)} Z' fill='{col}' fill-opacity='{alpha_hit}' stroke='#333' stroke-width='1.4'/>")
                else:
                    groups.setdefault((col,alpha), []).append(' '.join(d))
        if is_hit and not hit: hit=(cl,code)
    for (col,alpha),lst in groups.items():
        out.append("<path d='" + ' '.join(x + ' Z' for x in lst) + f"' fill='{col}' fill-opacity='{alpha}' fill-rule='evenodd' stroke='{col}' stroke-width='.4'/>")
    if point:
        px,py=proj(point[0],point[1])
        if x0<=px<=x0+w and y0<=py<=y0+h:
            out.append(f"<circle cx='{px:.0f}' cy='{py:.0f}' r='5' fill='#c0392b' stroke='#7a1f14'/>")
    return "".join(out), hit


def faint(box, bounds, point=None):
    return overlay(box, bounds, point=point, max_polys=26, alpha=0.20, alpha_hit=0.45)[0]
