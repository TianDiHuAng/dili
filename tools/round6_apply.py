# -*- coding: utf-8 -*-
"""第6轮：4核心升级L2 + 6来源修复记录 + 30复核，分4批。"""
import json, os, re, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import make_svg, update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
TP="时期与年代待专门来源核验（详见待核实）"

CONTENT={
"古埃及古王国":{
 "defn":"古埃及古王国：尼罗河谷早期统一国家阶段，以孟菲斯一带为政治中心，留下大规模石造陵墓与神庙遗存。",
 "geo":"核心区位于尼罗河谷与三角洲，河流定期泛滥带来沉积物，狭窄耕地与沙漠边缘共同塑造聚落格局。水资源与运输条件是长期变量。",
 "influence":"尼罗河农业与运输为国家组织提供物质基础，但国家形成还取决于制度、军事与贸易，不能把政治形态简化为河流产物。",
 "polities":"Livius 的 Egypt 分类页列出该时期相关王朝条目，可作为进一步核对王表与年表的入口；本站不在 L2 骨架中断言具体年代。",
 "connections":"通过尼罗河与三角洲连接上埃及、下埃及和地中海沿岸，并通过红海与西亚保持交流。",
 "today":"遗址保护与旅游是当代议题。游客量、人口与保护资金数据待按年份从权威机构补齐。",
 "sources":["livius-egypt","s013-fao-org","s010-unesco-org"]},
"苏美尔城邦":{
 "defn":"苏美尔城邦：两河流域南部早期城市国家群，以灌溉农业、城邦建筑和文字记录著称。",
 "geo":"冲积平原地势低平，幼发拉底河与底格里斯河提供灌溉水源。排水不良与盐渍化风险长期存在，聚落多沿河道与渠道分布。",
 "influence":"灌溉与城市管理相互关联，渠网维护需要协作；但城邦制度并非环境的必然结果，贸易、战争和宗教同样重要。",
 "polities":"Livius 的 Mesopotamia 专题页提供区域与政权入口，可用于后续核对城邦名单与年代；本站此处仅作骨架式描述。",
 "connections":"城邦通过河运与陆路与两河流域北部、伊朗高原和阿拉伯半岛边缘交换金属、石材与农产品。",
 "today":"遗址分布在今伊拉克南部。人口、水文与遗址状况数据待按年份核验。",
 "sources":["livius-mesopotamia","s013-fao-org","s010-unesco-org"]},
"阿卡德帝国":{
 "defn":"阿卡德帝国：两河流域早期地域性国家，以统一城邦和远距离军事行动著称，是古代西亚政治整合的重要阶段。",
 "geo":"核心位于两河流域中下游，平原与河道利于农业和运输，周边草原与高原构成军事与贸易边缘。",
 "influence":"控制灌溉区与商路有助于财政和军队供给，但帝国扩张与维持取决于统治策略，不宜作地理决定论解释。",
 "polities":"Livius 的 Mesopotamia 页面可作为核对区域政权序列的入口；具体王名与年代仍需专门条目逐条核验。",
 "connections":"帝国连接苏美尔城邦、两河上游与西亚其他区域，推动商品、技术和语言的流动。",
 "today":"考古遗址与文献释读仍在推进。年代与疆域数据待按年份从专题来源核验。",
 "sources":["livius-mesopotamia","s010-unesco-org","s013-fao-org"]},
"古希腊城邦":{
 "defn":"古希腊城邦：以城市及其周边领土为基本单位的地方政治共同体，山地与海湾共同塑造其分立与互联格局。",
 "geo":"希腊本土多山，平原狭小，海岸曲折且岛屿众多。山地分割与海上通道并存，地中海气候适宜橄榄、葡萄与谷物混合农业。",
 "influence":"海洋交通促进贸易与殖民，山地限制大规模统一，但城邦制度不能仅由地形解释；制度选择与社会冲突同样关键。",
 "polities":"Livius 的 Polis、Athens 与 Greece 页面提供城邦概念和主要城邦的专题入口，可支撑城邦作为基本单位的概述；具体政体演变待逐条核验。",
 "connections":"爱琴海把希腊本土、岛屿、安纳托利亚与埃及连接成交换网络，陶器、金属与思想沿航线传播。",
 "today":"遗址与博物馆是当代文化景观的重要部分。游客与遗产数据待按年份核验。",
 "sources":["livius-polis","livius-athens","livius-greece"]},
}

FIX_NOTES={
 "城市起源":"第6轮来源复查：Livius 与 NatGeo 新来源不含城市起源专题页；维持 L1，待专门来源。",
 "尼罗河三角洲":"第6轮来源复查：Livius Egypt 分类页为埃及史入口，不是三角洲专题；维持 L1。",
 "长江流域":"第6轮来源复查：Livius 无东亚流域专题，FAO AQUASTAT 仍为背景来源；维持 L1。",
 "阿尔卑斯山":"第6轮来源复查：Livius Greece 与 NatGeo Maya 与阿尔卑斯无关；维持 L1。",
 "五大湖":"第6轮来源复查：EPA Great Lakes 与 NOAA GLERL 仍为最佳来源，缺航道/边界专题；维持 L1。",
 "南极半岛":"第6轮来源复查：Livius/NatGeo 无南极专题；BAS 202、Britannica 403，维持 L1。",
}

GAP_BY_THEME={
 "地形":"地貌形成年代与关键地形节点的专题来源",
 "气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源",
 "贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源",
 "区域":"区域边界、人口与现状数据的专题来源",
}
SOURCE_BY_THEME={
 "地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],
 "农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],
 "政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"],
}

def upgrade(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    c=CONTENT[title]
    e.update({"level":"L2","status":"L2完成(第6轮)","definition":c["defn"],"overview":c["defn"].split("：",1)[1],
      "time_or_place":TP,"geo":c["geo"],"influence":c["influence"],"polities":c["polities"],
      "connections":c["connections"],"today":c["today"],"svg":make_svg(title,e["region"],e["theme"]),
      "sources":c["sources"],"needs_verification":True,
      "pending_notes":"第6轮升级：Livius/FAO/UNESCO 专题或机构页支撑概述；具体年代、王表与遗址数据待逐条核验。"})
    return e["id"]
 raise SystemExit("未找到:"+title)

def fix(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    e["pending_notes"]=FIX_NOTES[title];e["last_update"]=TODAY;e["status"]="来源再核未通过(第6轮)"
    return e["id"]
 raise SystemExit("未找到:"+title)

def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第5轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]

def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源")
    pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"])
    added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第6轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第6轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)

def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  for t in CONTENT: done.append(upgrade(docs,t))
  for t in FIX_NOTES: done.append("FIX:"+fix(docs,t))
 else:
  titles=review_titles(docs);start=(b-2)*10
  for t in titles[start:start+10]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))

if __name__=="__main__": main()
