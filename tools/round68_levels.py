# -*- coding: utf-8 -*-
"""第72轮起：层级计算改用 tools/assess.py（D138）。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, count_entry, level_of, UNITS

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
S = load_sources()
T = load_entries(UNITS)
out = {}; summary = {"A": [], "B": [], "C": [], "D": []}
for t, e in T.items():
    lv = level_of(e, S)
    out[t] = {"level": lv, "counts": count_entry(e, S), "tier": e["tier"]}
    summary[lv].append(t)
json.dump({"round": 72, "levels": out, "summary": {k: len(v) for k, v in summary.items()},
 "definition": {"A": "≥2 强来源", "B": "1 强来源", "C": "无强来源", "D": "仅数据端点+机构页"},
 "criterion": "tools/assess.py（D138）"},
 open(os.path.join(DATA, "evidence_level.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("层级:", {k: len(v) for k, v in summary.items()})
