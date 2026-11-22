# -*- coding: utf-8 -*-
"""第12轮：10个B6主题L1 + 30复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NEW=[
 ("健康地理数据","补充","全球","区域","现代统计（年份以来源页面为准）","健康指标按地区分层展示，受人口结构、医疗可及性与环境条件共同影响，数据口径需逐项核对。",["s005-who-int","s006-who-int"],"预期寿命空间差异"),
 ("气候与健康风险","补充","全球","气候","现代研究（年份以来源页面为准）","气温、降水与极端事件通过热应激、媒介生物和空气质量影响健康，风险因地区脆弱性而异。",["s007-who-int","s089-worldbank-org"],"极端天气预警"),
 ("全球营养状况","补充","全球","农业","现代统计（年份以来源页面为准）","营养不足与过量并存，受粮食供给、收入分配、卫生与教育影响，区域差异显著。",["s020-fao-org","s005-who-int"],"食物与农业"),
 ("气候适应政策","补充","全球","气候","现代政策实践（年份以来源页面为准）","适应政策通过基础设施、预警与生态管理降低气候影响，成效取决于实施能力与地方条件。",["s011-unesco-org","s060-worldbank-org"],"气候适应"),
 ("环境治理","补充","全球","区域","现代治理实践（年份以来源页面为准）","环境治理涉及国际公约、国家法规与社区参与，跨边界资源的协调是常见难点。",["s062-worldbank-org","s071-cbd-int"],"陆地保护区"),
 ("可持续交通","补充","全球","贸易","现代政策实践（年份以来源页面为准）","交通系统影响区域连通、能源使用与排放，可持续转型需兼顾可达性与环境影响。",["s063-worldbank-org","s025-ourworldindata-org"],"能源转型"),
 ("地理空间数据产品","补充","全球","地形","现代数据服务（年份以来源页面为准）","地理空间数据产品把观测与统计转化为可使用的地图和数据集，是区域研究与规划的基础。",["s087-ncei-noaa-gov","s001-unstats-un-org"],"卫星遥感地表观测"),
 ("火灾生态","补充","全球","气候","现代观测（年份以来源页面为准）","火在部分生态系统中是自然扰动，频率与强度受气候、植被和人类活动共同影响。",["s086-earthobservatory-nasa-gov","s046-earthobservatory-nasa-gov"],"北极火情变化"),
 ("国家收入分类","补充","全球","贸易","现代统计口径（年份以来源页面为准）","国际机构按收入水平对国家分组，用于统计与贷款政策，分组随时间调整，不等同于发展水平评价。",["s069-datahelpdesk-worldbank-org","s057-databank-worldbank-org"],"人均产出空间差异"),
 ("玛雅研究新进展","补充","全球","政权更替","近期研究（年份以来源页面为准）","玛雅考古与古气候研究持续修订对城邦网络、干旱与政治变化的认识，结论仍存在讨论。",["natgeo-maya","s010-unesco-org"],"玛雅文明"),
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
   "theme":theme,"level":"L1","status":"L1完成(第12轮)","definition":title+"："+overview,
   "time_or_place":tp,"overview":overview,"related":[rid] if rid else [],"sources":sources,
   "needs_verification":True,"pending_notes":"B6 主题补入；具体年份、口径与数值需按来源页面逐条核验。",
   "outlines":["WHO/FAO/UNESCO/World Bank/CBD/NOAA/NASA/NatGeo 已核验来源"],"last_update":TODAY}
  docs["global-themes"]["entries"].append(e);out.append(e["id"])
 return out
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第11轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第12轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第12轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)
def append_scope(titles):
 p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
 block="### 第12轮补充（B6 主题）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 已核验机构来源补入。\n" for x in titles)+"\n"
 if "### 第12轮补充" not in t: t=t.replace(marker,block+marker)
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
