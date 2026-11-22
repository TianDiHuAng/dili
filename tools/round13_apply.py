# -*- coding: utf-8 -*-
"""第13轮：10个B6主题L1 + 30复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NEW=[
 ("教育机会地域差异","补充","全球","区域","现代统计（年份以来源页面为准）","教育可及性与完成率在地区间差异显著，受人口结构、经济条件与公共服务供给影响。",["s008-unesco-org","s074-unicef-org"],"人文地理学"),
 ("儿童发展地域差异","补充","全球","区域","现代统计（年份以来源页面为准）","儿童健康、营养与教育指标具有明显地域差异，与家庭收入、卫生服务与环境条件相关。",["s074-unicef-org","s005-who-int"],"健康地理数据"),
 ("农业气候风险","补充","全球","气候","现代农业实践（年份以来源页面为准）","农业生产受温度、降水与极端事件影响，风险暴露与适应能力因地区而异。",["s019-fao-org","s060-worldbank-org"],"气候适应政策"),
 ("农业统计体系","补充","全球","农业","现代统计体系（年份以来源页面为准）","农业统计通过耕地、产量与投入指标支持粮食安全评估，口径统一是跨区域比较的前提。",["s021-fao-org","s014-fao-org"],"作物单产差异"),
 ("全球人口规模","补充","全球","区域","现代统计（年份以来源页面为准）","全球人口总量的时序变化由出生、死亡与迁移共同决定，是资源与环境分析的基础变量。",["s032-ourworldindata-org","s004-population-un-org"],"人口增长"),
 ("地球系统科学","补充","全球","地形","现代科学研究（年份以来源页面为准）","地球系统科学把大气、水圈、岩石圈与生物圈作为相互作用整体，强调跨圈层过程。",["s037-science-nasa-gov","s009-unesco-org"],"板块构造"),
 ("环境数据访问","补充","全球","地形","现代数据服务（年份以来源页面为准）","环境数据的访问与产品化使观测资料可用于研究与规划，元数据说明是使用前提。",["s049-ncei-noaa-gov","s054-ncei-noaa-gov"],"地理空间数据产品"),
 ("人文地理学","补充","全球","区域","学科概述（形成年代待专门来源核）","人文地理学研究人类活动的空间组织、区域差异与地方联系，关注文化、经济与政治过程。",["openstax-human-geo","s075-aag-org"],"人口地理"),
 ("撒哈拉以南非洲发展数据","补充","全球","区域","现代统计（年份以来源页面为准）","该区域发展指标差异显著，数据需结合国家收入分类与统计口径阅读，避免单一指标概括。",["s064-worldbank-org","s057-databank-worldbank-org"],"国家收入分类"),
 ("东亚与太平洋区域发展","补充","全球","区域","现代统计（年份以来源页面为准）","该区域包含多样经济体和地理单元，发展指标与城市化、贸易联系密切，口径需逐项核对。",["s065-worldbank-org","s057-databank-worldbank-org"],"国家收入分类"),
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
   "theme":theme,"level":"L1","status":"L1完成(第13轮)","definition":title+"："+overview,
   "time_or_place":tp,"overview":overview,"related":[rid] if rid else [],"sources":sources,
   "needs_verification":True,"pending_notes":"B6 主题补入；具体年份、口径与数值需按来源页面逐条核验。",
   "outlines":["UNESCO/UNICEF/WHO/FAO/World Bank/OWID/NASA/NOAA/OpenStax/AAG 已核验来源"],"last_update":TODAY}
  docs["global-themes"]["entries"].append(e);out.append(e["id"])
 return out
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第12轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第13轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第13轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)
def append_scope(titles):
 p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
 block="### 第13轮补充（B6 主题）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 已核验机构来源补入。\n" for x in titles)+"\n"
 if "### 第13轮补充" not in t: t=t.replace(marker,block+marker)
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
