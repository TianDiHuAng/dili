# -*- coding: utf-8 -*-
"""第72轮起：缺口统计改用 tools/assess.py 的单一判据实现（D138）。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assess import (load_sources, load_entries, content_count, level_of, UNITS, is_data, is_alias)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TODAY = os.environ.get("DILI_TODAY", "2026-11-24")

S = load_sources()
T = load_entries(UNITS)

# G3：内容源仅 1 个，**排除 D 级**（指标解读类只需机构长文 + 数据端点）
lvl = {t: level_of(e, S) for t, e in T.items()}
lvl = {t: level_of(e, S) for t, e in T.items()}
one = [t for t, e in T.items() if content_count(e, S) == 1 and lvl[t] != "D"]
zero = [t for t, e in T.items() if content_count(e, S) == 0 and lvl[t] != "D"]
# G1：无强来源（**仅 C 级**——D 级是指标解读类，本不要求强来源，不计入缺口）
g1 = [t for t, v in lvl.items() if v == "C"]
NOFIX = ("河中地区", "库什与努比亚", "莫切文化")   # 已确认无合格主来源
gaps = []
for t in g1:
    gaps.append({"entry": t, "gap": "无强来源（C/D）", "detail": f"层级 {lvl[t]}"})

out = {"round": 72, "date": TODAY,
 "gap_definitions": [
   {"id": "G1", "name": "无强来源（仅 C 级；D 级指标解读类不计）", "count": len(g1),
    "fixed_by": "补一条被引≥10 或正文≥800 的来源（且非别名页/书评）"},
   {"id": "G2", "name": "检索确认无合格主来源", "count": len(NOFIX),
    "fixed_by": "仅待新文献出现；不再重试同类检索"},
   {"id": "G3", "name": "内容源仅 1 个（需第二互证）", "count": len(one),
    "fixed_by": "补第二内容源，须过 R19/R20/R22/R25"},
   {"id": "G4", "name": "语义对题未经机器校验", "count": len(T),
    "fixed_by": "人工逐条扫描（不可自动化）"}],
 "gaps": gaps, "one_source_entries": one, "zero_source_entries": zero,
 "levels": lvl,
 "criterion": "tools/assess.py（D138 单一实现）：排除数据端点与别名页 + 排除书评；门槛 被引≥10 或 正文≥800"}
json.dump(out, open(os.path.join(ROOT, "reports", "round62_gaps.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("缺口定义：", {d["id"]: d["count"] for d in out["gap_definitions"]})
print("G1 明细：", g1)
