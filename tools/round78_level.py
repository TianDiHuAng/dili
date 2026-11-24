# -*- coding: utf-8 -*-
"""第78轮A：D141——指标解读类（1 个机构长文作主体 + 数据端点，无学术论文）判 D 而非 B。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D141" in t:
    print("已存在"); raise SystemExit
t=t.replace('''def level_of(entry, sources):
    """A/B/C/D 四档。"""
    c = count_entry(entry, sources)
    if c["strong"] >= 2:
        return "A"
    if c["strong"] == 1:
        return "B"
    if c["data"] > 0 and c["side"] == 0 and c["weak"] == 0:
        return "D"
    return "C"''',
'''def _strong_sids(entry, sources):
    return [sid for sid in entry.get("sources", [])
            if strength(sid, sources.get(sid) or {}, entry) == "strong"]


def level_of(entry, sources):
    """A/B/C/D 四档。
    D141：若仅有 1 个强来源、且该强来源是**机构长文**（非 openalex- 学术论文）、
    同时条目带数据端点——判为 D（指标解读类），因为其正文是指标解释与空间差异概述，
    机构长文即主体，不要求第二篇学术文献。"""
    c = count_entry(entry, sources)
    if c["strong"] >= 2:
        return "A"
    if c["strong"] == 1:
        sids = _strong_sids(entry, sources)
        is_institutional = sids and not any(s.startswith("openalex-") for s in sids)
        if is_institutional and c["data"] > 0 and c["side"] == 0:
            return "D"
        return "B"
    if c["data"] > 0 and c["side"] == 0 and c["weak"] == 0:
        return "D"
    return "C"''')
open(p,"w",encoding="utf-8").write(t)
print("D141 已加入 assess.py")