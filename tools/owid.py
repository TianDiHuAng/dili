# -*- coding: utf-8 -*-
"""Our World in Data grapher CSV → 真实序列 + 复用 wbdata 折线面板。"""
import os, subprocess, csv
import wbdata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "geo", "owid")
BASE = "https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=true"
_C = {}

def _csv(slug):
    if slug in _C: return _C[slug]
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, slug + ".csv")
    if not os.path.exists(p) or os.path.getsize(p) < 500:
        for _ in range(3):
            subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","90","-A","Mozilla/5.0","-o",p,BASE.format(slug=slug)],capture_output=True)
            if os.path.exists(p) and os.path.getsize(p) > 500: break
    _C[slug] = p
    return p

def series(slug, entity, column):
    p = _csv(slug); rows=[]
    try:
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("entity") == entity and r.get(column):
                    try: rows.append((int(r["year"]), float(r[column])))
                    except: pass
    except Exception: rows=[]
    rows.sort(); return rows

def _temp():
    return series("temperature-anomaly", "World", "near_surface_temperature_anomaly")

def panel(box, label="全球近地表气温距平", unit="°C（相对 1850–1900）"):
    return wbdata.panel(box, _temp(), "temperature-anomaly", label, unit, source="Our World in Data")[0]

def panel2(box, slug, entity, column, label, unit):
    return wbdata.panel(box, series(slug, entity, column), slug, label, unit, source="Our World in Data")[0]
