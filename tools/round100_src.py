# -*- coding: utf-8 -*-
"""第100轮：D154——区分「库中登记数」与「实际引用数」；标注未引用来源。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
S=load_sources();T=load_entries(UNITS)
used=set()
for e in T.values(): used.update(e.get("sources",[]))

P=os.path.join(DATA,"sources.json")
sd=json.load(open(P,encoding="utf-8"))
n_ref=0;n_unref=0;n_fail=0
for s in sd["sources"]:
    sid=s["id"]
    if sid in used:
        s.pop("referenced",None); n_ref+=1
        continue
    s["referenced"]=False
    n_unref+=1
    nt=(s.get("note") or "")
    if (not s.get("link_ok")) or "404" in (s.get("page_title") or "") or "未取得页面标题" in (s.get("page_title") or "") or "Just a moment" in (s.get("page_title") or ""):
        s["fetch_failed"]=True; n_fail+=1
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"登记 {len(sd['sources'])} | 实际引用 {n_ref} | 未引用 {n_unref}（其中抓取失败 {n_fail}）")

# SATURATION 里区分两个数
sp=os.path.join(ROOT,"SATURATION.json")
sat=json.load(open(sp,encoding="utf-8"))
sat.setdefault("evidence",{})["sources_registered"]=len(sd["sources"])
sat["evidence"]["sources_referenced"]=n_ref
sat["evidence"]["sources_unreferenced"]=n_unref
sat["evidence"]["sources_fetch_failed"]=n_fail
sat["evidence"]["note_sources"]=("sources.json 是**登记库**（含抓取失败的尝试记录与未被采用的候选），"
  "实际被条目引用的是 sources_referenced。此前报告「777 来源」用的是登记数，"
  "会让来源显得比实际多（D154）。")
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# check.py 增加统计输出（不新增错误，只提示）
print("SATURATION 已更新")