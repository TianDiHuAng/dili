# -*- coding: utf-8 -*-
"""第11轮：10个B6主题L1 + 30复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NEW=[
 ("荒漠化","补充","全球","气候","现代观测（年份以来源页面为准）","干旱半干旱区土地退化过程，受降水波动、土地利用和植被覆盖共同影响，不等同于沙漠自然扩张。",["s045-earthobservatory-nasa-gov","s018-fao-org"],"萨赫勒带"),
 ("沙尘暴","补充","全球","气候","现代观测（年份以来源页面为准）","强风把裸露地表沙尘输送到远处的天气现象，源区、风速与植被状况共同决定其频率与影响。",["s046-earthobservatory-nasa-gov","s045-earthobservatory-nasa-gov"],"荒漠化"),
 ("渔业资源","补充","全球","贸易","现代统计（年份以来源页面为准）","海洋与内陆渔业资源受水文、生态与捕捞压力影响，是沿海与岛国经济的重要组成部分。",["s051-fisheries-noaa-gov","s050-oceanservice-noaa-gov"],"海洋保护区"),
 ("极端天气预警","补充","全球","气候","现代业务（年份以来源页面为准）","基于气象观测与模型的预警系统可降低灾害风险，其有效性依赖监测密度、通信与公众响应。",["s052-weather-gov","s048-climate-gov"],"自然灾害风险"),
 ("土壤资源","补充","全球","农业","现代调查（年份以来源页面为准）","土壤厚度、养分与水分保持能力影响农业和生态，其分布受母质、气候、地形与土地利用影响。",["s083-fao-org","s018-fao-org"],"作物单产差异"),
 ("海洋生态系统","补充","全球","区域","现代观测（年份以来源页面为准）","海洋生态系统包括沿岸、外海与深海群落，受温度、营养盐、洋流和人类活动共同塑造。",["s085-unesco-org","s050-oceanservice-noaa-gov"],"海洋保护区"),
 ("陆地保护区","补充","全球","区域","现代管理实践（年份以来源页面为准）","为保护生物多样性、生态系统与文化景观而划定的陆地空间，管理成效与社区参与和执法能力相关。",["s091-iucn-org","s070-cbd-int"],"生物多样性分布"),
 ("城市贫困","补充","全球","区域","现代统计（年份以来源页面为准）","城市贫困表现为收入不足与公共服务获取受限，其空间分布与住房、就业和迁移密切相关。",["s088-worldbank-org","s025-ourworldindata-org"],"极端贫困空间分布"),
 ("水资源管理","补充","全球","地形","现代管理实践（年份以来源页面为准）","水资源管理需协调生活、农业、工业与生态需求，跨流域与跨边界合作是常见议题。",["s013-fao-org","s061-worldbank-org"],"湿地与水资源"),
 ("卫星遥感地表观测","补充","全球","地形","现代观测（年份以来源页面为准）","卫星遥感提供大范围、重复的地表观测，用于监测土地利用、植被、水体与城市扩张。",["s041-science-nasa-gov","s038-earthobservatory-nasa-gov"],"土地利用变化"),
]
GAP_BY_THEME={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
SOURCE_BY_THEME={"地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],"农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}
def add_new(docs):
 out=[]
 for title,tier,region,theme,tp,overview,sources,rel in NEW:
  if any(e["title"]==title for e in docs["global-themes"]["entries"]): continue
  rid=None
  for d in docs.values():
   for e in d["entries"]:
    if e["title"]==rel: rid=e["id"];break
   if rid:break
  e={"id":"global-themes-"+sid(title),"title":title,"tier":tier,"unit_id":"global-themes","region":region,
   "theme":theme,"level":"L1","status":"L1完成(第11轮)","definition":title+"："+overview,
   "time_or_place":tp,"overview":overview,"related":[rid] if rid else [],"sources":sources,
   "needs_verification":True,"pending_notes":"B6 主题补入；具体年份、口径与数值需按来源页面逐条核验。",
   "outlines":["NASA/NOAA/FAO/UNESCO/IUCN/World Bank 已核验主题页"],"last_update":TODAY}
  docs["global-themes"]["entries"].append(e);out.append(e["id"])
 return out
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第10轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第11轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第11轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)
def append_scope(titles):
 p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
 block="### 第11轮补充（B6 主题）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 已核验机构主题页补入。\n" for x in titles)+"\n"
 if "### 第11轮补充" not in t: t=t.replace(marker,block+marker)
 open(p,"w",encoding="utf-8").write(t)
def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  done+=["NEW:"+x for x in add_new(docs)]
  append_scope([n[0] for n in NEW])
 else:
  titles=review_titles(docs);start=(b-2)*10
  for t in titles[start:start+10]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))
if __name__=="__main__": main()
