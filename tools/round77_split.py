# -*- coding: utf-8 -*-
"""第77轮起：G3 拆分为 G3a（有侧面/弱辅助）与 G3b（无任何辅助）。D 级排除。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, level_of, UNITS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TODAY = os.environ.get("DILI_TODAY", "2026-11-24")
S = load_sources(); T = load_entries(UNITS)

g3a = []; g3b = []
for t, e in T.items():
    if content_count(e, S) != 1: continue
    if level_of(e, S) == "D": continue        # D141：指标解读类不计入 G3
    c = count_entry(e, S)
    rec = {"entry": t, "tier": e["tier"], "counts": c}
    if c["side"] > 0 or c["weak"] > 0: g3a.append(rec)
    else: g3b.append(rec)

def tc(lst):
    from collections import Counter
    return dict(Counter(x["tier"] for x in lst))

out = {"round": 78, "date": TODAY,
 "definitions": {
   "G3a": "内容源仅 1 个但有侧面/弱来源可补充（缺整体研究）",
   "G3b": "内容源仅 1 个且无任何其他来源"},
 "excluded": "D 级（指标解读类）不计入 G3——其正文为指标解释，机构长文即主体（D141）",
 "G3a": {"count": len(g3a), "tiers": tc(g3a), "entries": [x["entry"] for x in g3a]},
 "G3b": {"count": len(g3b), "tiers": tc(g3b), "entries": [x["entry"] for x in g3b]}}
json.dump(out, open(os.path.join(ROOT, "reports", "round77_g3split.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("G3a:", len(g3a), tc(g3a), "| G3b:", len(g3b), tc(g3b))
