# -*- coding: utf-8 -*-
"""第78轮B：修正缺口定义——G1 只含 C 级；G3 排除 D 级（指标解读类）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- 重写 round62_gaps.py 的 G1/G3 定义 ---
p=os.path.join(ROOT,"tools","round62_gaps.py")
t=open(p,encoding="utf-8").read()
t=t.replace('''# G1：无强来源（C/D 级）
g1 = [t for t, v in lvl.items() if v in ("C", "D")]''',
'''# G1：无强来源（**仅 C 级**——D 级是指标解读类，本不要求强来源，不计入缺口）
g1 = [t for t, v in lvl.items() if v == "C"]''')
t=t.replace('''one = [t for t, e in T.items() if content_count(e, S) == 1]''',
'''# G3：内容源仅 1 个，**排除 D 级**（指标解读类只需机构长文 + 数据端点）
one = [t for t, e in T.items() if content_count(e, S) == 1 and lvl[t] != "D"]''')
t=t.replace('''zero = [t for t, e in T.items() if content_count(e, S) == 0]''',
'''zero = [t for t, e in T.items() if content_count(e, S) == 0 and lvl[t] != "D"]''')
# lvl 需在 one 之前定义
t=t.replace('''one = [t for t, e in T.items() if content_count(e, S) == 1 and lvl[t] != "D"]''',
'''lvl = {t: level_of(e, S) for t, e in T.items()}
one = [t for t, e in T.items() if content_count(e, S) == 1 and lvl[t] != "D"]''')
t=t.replace('''lvl = {t: level_of(e, S) for t, e in T.items()}

# G1''','''# G1''')
t=t.replace('''{"id": "G1", "name": "无强来源（C/D 级）", "count": len(g1),''',
'''{"id": "G1", "name": "无强来源（仅 C 级；D 级指标解读类不计）", "count": len(g1),''')
open(p,"w",encoding="utf-8").write(t)
print("round62_gaps 定义已修正")

# --- 重写 round77_split.py ---
sp='''# -*- coding: utf-8 -*-
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
'''
open(os.path.join(ROOT,"tools","round77_split.py"),"w",encoding="utf-8").write(sp)
print("round77_split 已重写")