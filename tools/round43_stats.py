# -*- coding: utf-8 -*-
"""第43轮：全站「真实学术来源数」统计（以是否有摘要/正文为准）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
R=json.load(open(os.path.join(ROOT,"reports","round43_review.json"),encoding="utf-8"))
abscount={}
for t,rows in R.items():
    abscount[t]=sum(1 for r in rows if len(r["abs"])>=300)

# 对未在 round43_review 中的条目（单源/零源），按类型估算
def is_academic(sid):
    return sid.startswith("openalex-")
def content_count(e):
    n=0
    for sid in e["sources"]:
        if sid in abscount: continue
        if is_academic(sid): n+=1
        elif sid.startswith("livius-"): n+=1          # 有正文的专题站
        elif sid in ("nasa-ice-cores","usgs-glaciers-pdf","noaa-global-temp","nasa-pine-island"): n+=1
    return n

stats={"0":[],"1":[],"ge2":[]}
for t,e in T.items():
    n = abscount.get(t, content_count(e))
    if n==0: stats["0"].append(t)
    elif n==1: stats["1"].append(t)
    else: stats["ge2"].append(t)
print("=== 全站真实学术来源数（以有正文/摘要为准）===")
print(f"  0 个: {len(stats['0'])} 条")
print(f"  1 个: {len(stats['1'])} 条")
print(f"  ≥2 个: {len(stats['ge2'])} 条  →", "、".join(stats["ge2"]))
rep={"round":43,"date":TODAY,
 "definition":"仅计有实际正文或摘要的来源（OpenAlex/Livius/NASA/USGS 专题）；机构首页（FAO/OWID/UNESCO/NOAA 首页/AAG/UNSDG）与世界银行指标端点不计",
 "zero":len(stats["0"]),"one":len(stats["1"]),"ge2":len(stats["ge2"]),
 "ge2_list":stats["ge2"],
 "correction":"此前「≥2 内容源 143 条」把机构首页计入内容源，属口径虚高；按本定义仅 "+str(len(stats["ge2"]))+" 条达 ≥2"}
json.dump(rep,open(os.path.join(ROOT,"reports","round43_stats.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 为 0 源条目在 pending 标注诚实说明
for t in stats["0"]:
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    if "【第43轮口径订正】" in pn: continue
    e["pending_notes"]=(pn+" 【第43轮口径订正】经复核，本条现有来源中**没有带正文/摘要的学术来源**（其余为机构首页或数据指标端点），"
      "正文的地理与机制描述属常识性表述、无学术来源支撑；数据类条目以「今天的状况」中的指标为准。").strip()
    e["last_update"]=TODAY
save_docs(docs)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=43
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("\n已为 0 源条目补口径订正说明:",len(stats["0"]))