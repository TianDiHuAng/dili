# -*- coding: utf-8 -*-
"""第93轮B：D151——level_of 与 content_count 同源（按去重后的独立内容源判 A）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D151" in t:
    print("已存在"); raise SystemExit(1)
old='''    c = count_entry(entry, sources)
    if c["strong"] >= 2:
        return "A"'''
new='''    c = count_entry(entry, sources)
    # D151：A 级须有 **≥2 个独立的**内容来源（同一域名多页只算 1，见 D150）。
    # 此前用 c["strong"]>=2，与 content_count 的去重口径不一致（D146 的同类问题）。
    if c["strong"] >= 2 and content_count(entry, sources) >= 2:
        return "A"'''
if old in t:
    t=t.replace(old,new); print("level_of 已与 content_count 统一（D151）")
else:
    print("⚠ 未匹配"); raise SystemExit(1)
open(p,"w",encoding="utf-8").write(t)