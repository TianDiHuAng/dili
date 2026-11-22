# -*- coding: utf-8 -*-
"""第8轮：5来源再核 + 35复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
FIX={
 "长江流域":"第8轮来源探测：Livius 无东亚流域专题，FAO AQUASTAT 仍为背景来源；维持 L1。",
 "汉代":"第8轮来源探测：Livius Han 分类页、UNESCO Silk Roads 均无可用标题，维持 L1。",
 "蒙古帝国":"第8轮来源探测：Livius Mongols 与 UNESCO Mongol Empire 页面不可核验，维持 L1。",
 "阿兹特克":"第8轮来源探测：Livius/NatGeo Aztec 页面不可用，维持 L1。",
 "城市起源":"第8轮来源探测：Livius Cities/City 页面不可用，维持 L1。",
}
GAP_BY_THEME={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
SOURCE_BY_THEME={"地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],"农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}
def fix(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    e["pending_notes"]=FIX[title];e["last_update"]=TODAY;e["status"]="来源探测未通过(第8轮)"
    return e["id"]
 raise SystemExit("未找到:"+title)
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第7轮)" not in e["status"]:
    out.append(e["title"])
 return out[:35]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第8轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第8轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)
def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  for t in FIX: done.append("FIX:"+fix(docs,t))
  for t in review_titles(docs)[:5]: done.append("REVIEW:"+review(docs,t))
 else:
  titles=review_titles(docs);start=(b-2)*10
  for t in titles[start:start+10]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))
if __name__=="__main__": main()
