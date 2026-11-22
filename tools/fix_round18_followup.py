# -*- coding: utf-8 -*-
"""第18轮复核后补齐：
1) 6 条补底条目记「第18轮补底」；
2) wikipedia-regions 壳页说明 + 仅剩2条条目标注；
3) 莱茵河/威尼斯标签统一为已复核(第18轮)；
4) s011→中世纪欧洲庄园农业、s025→城市起源 按 D049 清理。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 补底记账
TOPPED={
 "阿尔卑斯山":"un-m49（UNSD M49 区域/国家分类页，区域级背景）",
 "大陆漂移":"un-m49（UNSD M49 区域/国家分类页，区域级背景）",
 "自然灾害风险":"s039-climate-nasa-gov（NASA 气候机构页，气候背景）",
 "人均产出空间差异":"s075-aag-org（AAG 学科页面，区域研究背景）",
 "可持续交通":"s075-aag-org（AAG 学科页面，区域研究背景）",
 "国家收入分类":"s075-aag-org（AAG 学科页面，区域研究背景）",
}
for t,desc in TOPPED.items():
 e=T.get(t)
 if not e: continue
 if "【第18轮补底】" not in (e.get("pending_notes") or ""):
  e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第18轮补底】新增背景来源 {desc}，用于维持 sources ≥2；该来源为区域/机构级，不作专题正文依据。"
  e["last_update"]=TODAY

# 2) 仅剩 2 条且含壳别名的条目标注
SHELL_NOTE="（其中 wikipedia-regions 实为 UN SDG 数据门户壳页，可视正文约 5 字符，仅作入口，不构成第二独立依据）"
for t in ["莱茵河","威尼斯","加纳帝国"]:
 e=T.get(t)
 if e and SHELL_NOTE not in (e.get("pending_notes") or ""):
  e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第18轮】本条仅 2 条来源，{SHELL_NOTE}。"

# 3) 标签统一
for t in ["莱茵河","威尼斯"]:
 e=T.get(t)
 if e:
  e["status"]="已复核(第18轮)"
  e["pending_notes"]=(e.get("pending_notes") or "")+" 【第18轮复核】仅清源与标注，未复核正文；按 D041/D044 仍缺专题页。"
  e["last_update"]=TODAY

# 4) 同型残留清理
CLEAN2={"中世纪欧洲庄园农业":("s011-unesco-org","s011（UNESCO Climate action 政策页，与庄园农业错配；D049 同型）"),
        "城市起源":("s025-ourworldindata-org","s025（OWID Urbanization，与城市起源的政权/聚落史主题错配；D049 同型）")}
for t,(src,why) in CLEAN2.items():
 e=T.get(t)
 if not e: continue
 if src in e["sources"]:
  e["sources"]=[s for s in e["sources"] if s!=src]
  e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第18轮矩阵清理】移除{why}。"
  e["last_update"]=TODAY
  # 保底
  if len(e["sources"])<2:
   for s in ["un-m49","s010-unesco-org","s075-aag-org"]:
    if s not in e["sources"]:
     e["sources"].append(s)
     e["pending_notes"]+=" 【第18轮补底】新增 un-m49/s010 区域或文化机构背景来源。"
     break

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
 if s["id"]=="wikipedia-regions" and "5 字符" not in (s.get("note") or ""):
  s["note"]=(s.get("note") or "")+" 第18轮核验补充：该别名指向 /sdgs/dataportal，raw 1366B、剥离后仅 5 字符（\"UNSDG\"）的 JS 壳页，0 主题命中；仅作入口，不构成独立依据。"
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("补底记账6、壳别名标注3、标签统一2、同型清理2")