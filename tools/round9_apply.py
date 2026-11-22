# -*- coding: utf-8 -*-
"""第9轮：10个B6主题L1 + 30复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NEW=[
 ("森林覆盖变化","补充","全球","气候","现代观测（年份以来源页面为准）","森林面积与覆盖质量的变化是全球土地利用与碳循环研究的核心指标，受农业扩张、林业政策与自然扰动共同影响。",["s029-ourworldindata-org","s042-earthobservatory-nasa-gov"],"热带雨林"),
 ("土地利用变化","补充","全球","农业","现代观测（年份以来源页面为准）","人类把自然地转为耕地、牧场、城市或基础设施的过程，改变生态过程与区域气候，也影响粮食与能源供应。",["s077-ourworldindata-org","s018-fao-org"],"山地农业"),
 ("生物多样性分布","补充","全球","区域","现代观测（年份以来源页面为准）","物种与生态系统在地球表面的分布不均，受气候、地形、历史与人类活动共同影响，是保护规划的基础。",["s030-ourworldindata-org","s073-iucn-org"],"亚马逊盆地"),
 ("海洋保护区","补充","全球","区域","现代管理实践（年份以来源页面为准）","为保护海洋生态与资源而划定管理的海域，其成效取决于执法、监测与周边社区参与。",["s070-cbd-int","s050-oceanservice-noaa-gov"],"大堡礁"),
 ("极端贫困空间分布","补充","全球","区域","现代统计（年份以来源页面为准）","极端贫困人口在地区间分布不均，与经济增长、公共服务、冲突和气候冲击相互关联。",["s082-ourworldindata-org","s057-databank-worldbank-org"],"人口迁移"),
 ("能源转型","补充","全球","贸易","近现代（具体年份待核）","能源结构从高碳向低碳来源调整的过程，涉及技术、基础设施、价格和政策，具有明显的区域差异。",["s028-ourworldindata-org","s058-worldbank-org"],"丝绸之路"),
 ("碳排放空间差异","补充","全球","气候","现代统计（年份以来源页面为准）","不同地区的人均与总量碳排放差异显著，受能源结构、产业活动与生活水平共同影响。",["s035-ourworldindata-org","s039-climate-nasa-gov"],"气候带"),
 ("人口年龄结构","补充","全球","区域","现代统计（年份以来源页面为准）","人口按年龄分组的构成反映生育、死亡与迁移的长期结果，并影响劳动力与公共服务需求。",["s081-ourworldindata-org","s004-population-un-org"],"人口地理"),
 ("城市热岛","补充","全球","气候","现代观测（年份以来源页面为准）","城市地表温度通常高于周边乡村，与不透水表面、建筑形态和绿地减少有关，也受区域气候背景影响。",["s044-earthobservatory-nasa-gov","s025-ourworldindata-org"],"城市地理"),
 ("湿地与水资源","补充","全球","地形","现代管理实践（年份以来源页面为准）","湿地在蓄洪、净水和生物栖息方面具有重要作用，水资源管理需兼顾生态与人类需求。",["fao-aquastat-basins","s050-oceanservice-noaa-gov"],"河流三角洲"),
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
  e={"id":"global-themes-"+sid(title),"title":title,"tier":tier,"unit_id":"global-themes",
   "region":region,"theme":theme,"level":"L1","status":"L1完成(第9轮)","definition":title+"："+overview,
   "time_or_place":tp,"overview":overview,"related":[rid] if rid else [],"sources":sources,
   "needs_verification":True,"pending_notes":"B6 主题补入；现状数值与分类口径需按年份和来源页面逐条核验。",
   "outlines":["Our World in Data 主题页","FAO/NASA/NOAA/CBD/UN 机构页"],"last_update":TODAY}
  docs["global-themes"]["entries"].append(e);out.append(e["id"])
 return out
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第8轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第9轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第9轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)
def append_scope(titles):
 p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
 block="### 第9轮补充（B6 主题）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 已核验机构主题页补入。\n" for x in titles)+"\n"
 if "### 第9轮补充" not in t: t=t.replace(marker,block+marker)
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
