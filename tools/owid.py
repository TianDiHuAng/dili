# -*- coding: utf-8 -*-
"""Our World in Data 真实序列（全球近地表气温距平）→ 复用 wbdata 折线面板。"""
import os, subprocess, csv
import wbdata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "geo", "owid", "temp.csv")
URL = "https://ourworldindata.org/grapher/temperature-anomaly.csv?v=1&csvType=full&useColumnShortNames=true"
_C = None

def _load():
    global _C
    if _C is not None: return _C
    os.makedirs(os.path.dirname(P), exist_ok=True)
    if not os.path.exists(P) or os.path.getsize(P) < 2000:
        subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","90","-A","Mozilla/5.0","-o",P,URL],capture_output=True)
    rows=[]
    try:
        with open(P, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("entity")=="World" and r.get("near_surface_temperature_anomaly"):
                    try: rows.append((int(r["year"]), float(r["near_surface_temperature_anomaly"])))
                    except: pass
    except Exception: rows=[]
    rows.sort(); _C=rows; return rows

def panel(box, label="全球近地表气温距平", unit="°C（相对 1850–1900）"):
    return wbdata.panel(box, _load(), "temperature-anomaly", label, unit, source="Our World in Data")[0]
