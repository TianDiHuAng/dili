# -*- coding: utf-8 -*-
"""Phase1：全站地图叠加 Natural Earth 物理图层；地貌条目保留彩绘剖面，仅替换定位图。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import illos, ne
from locator import map_svg
from round2_apply import save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from apply_illos_all import COORD

UNITS = ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
MARK = "<g transform='translate(0,258)'>"
CHINA_BB = (60, 146, 10, 58)

def landform_svg(entry, inner):
    lon, lat = COORD[entry["title"]]
    box = (30, 34, 840, 196)
    ov = ne.overlay(box, CHINA_BB, entry["title"])
    loc = map_svg(box, CHINA_BB, lon, lat, label=entry["title"], overlay=ov)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760' role='img' aria-label='位置图与剖面示意图'>"
            + loc + "<g transform='translate(0,258)'>" + inner + "</g></svg>")

docs = {u: json.load(open(os.path.join(DATA, u + ".json"), encoding="utf-8")) for u in UNITS}
n = 0; lf = 0
for u, d in docs.items():
    for e in d["entries"]:
        s = e.get("svg") or ""
        if MARK in s:  # 已含位置图的地貌条目：换定位图、留剖面
            inner = s[s.index(MARK) + len(MARK): s.rindex("</g></svg>")]
            e["svg"] = landform_svg(e, inner); lf += 1
        else:
            e["svg"] = illos.build(e, COORD.get(e["title"]))
        e["last_update"] = "2026-11-25"; n += 1
save_docs(docs); update_coverage(docs)
print("rebuilt", n, "landform-rebuild", lf)
