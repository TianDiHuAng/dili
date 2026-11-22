# -*- coding: utf-8 -*-
"""修复：重新标记 D041 遗产 L2（update_coverage 曾清空标记）。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
ALIAS={"britannica-regions","wikipedia-regions","un-m49","ap-human-geo"}
EXEMPT={"五大湖","科罗拉多高原","格陵兰岛","人口迁移","萨赫勒带","阿契美尼德波斯"}
TAG="（D041 前遗产 L2·待补专题页）"
tagged=[]
for u,d in docs.items():
 for e in d["entries"]:
  if e["level"]!="L2" or e["title"] in EXEMPT: continue
  srcs=set(e.get("sources",[]))
  thematic=[x for x in srcs if x not in ALIAS]
  weak=(len(thematic)==0) or (len(thematic)==1 and any(k in (thematic[0] or "") for k in ("s056-earthquake","s057-databank","s011-unesco","s014-fao")))
  if weak:
   if TAG not in e["status"]:
    e["status"]=e["status"]+TAG
   tagged.append(e["title"])
for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
cp=os.path.join(DATA,"coverage.json");cov=json.load(open(cp,encoding="utf-8"))
bytitle={e["title"]:e["id"] for d in docs.values() for e in d["entries"]}
ids={bytitle[t] for t in tagged}
for c in cov["entries"]:
 if c["id"] in ids: c["d041_legacy"]=True
 if c["id"]==bytitle["阿契美尼德波斯"]:
  c["d041_pairing_gap"]=True
cov["d041_legacy_count"]=sum(1 for c in cov["entries"] if c.get("d041_legacy"))
cov["d041_pairing_gap_count"]=sum(1 for c in cov["entries"] if c.get("d041_pairing_gap"))
json.dump(cov,open(cp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("legacy",cov["d041_legacy_count"],"pairing",cov["d041_pairing_gap_count"])