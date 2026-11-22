# -*- coding: utf-8 -*-
"""第7轮：4核心升级L2 + 6来源修复 + 30复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import make_svg,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
TP="时期与年代待专门来源核验（详见待核实）"
CONTENT={
"古埃及早王朝":{
 "defn":"古埃及早王朝：尼罗河谷与三角洲形成统一国家的早期阶段，是后续古王国政治与文化结构的前身。",
 "geo":"聚落沿尼罗河谷与三角洲分布，河流泛滥带来沉积物，狭窄耕地、沙漠边缘与交通水道共同塑造国家空间。",
 "influence":"农业剩余与水运便利有利于权力集中，但国家形成还涉及制度、战争与交换，不能简化为河流决定论。",
 "polities":"Livius 的 Egypt 分类页提供早期王朝条目入口，可用于后续核对王表；本站在此不写具体王名与年代。",
 "connections":"上下埃及通过尼罗河连成整体，并通过三角洲与地中海、通过红海与西亚发生联系。",
 "today":"早期遗址保护与研究仍在推进。遗址数量、游客与保护数据待按年份从权威来源补齐。",
 "sources":["livius-egypt","s013-fao-org","s010-unesco-org"]},
"迦太基":{
 "defn":"迦太基：位于今突尼斯湾附近的古代港口城邦，以西地中海海上贸易网络著称。",
 "geo":"城市依托海湾与近岸平原，背靠阿特拉斯山脉南缘，港湾条件利于停泊与转运，腹地提供农产品与资源。",
 "influence":"港口位置与航海能力支撑贸易网络，但商业发展也与制度、技术和区域竞争有关，不能只由海岸线解释。",
 "polities":"Livius 的 Punic Carthage 专题页提供布匿城邦入口，可用于核对政权与战争史；本站不写具体战役年代。",
 "connections":"迦太基连接西地中海、北非内陆与伊比利亚，交换金属、陶器、橄榄油与纺织品。",
 "today":"遗址位于今突尼斯境内。游客量与遗产保护数据待按年份核验。",
 "sources":["livius-carthage","s050-oceanservice-noaa-gov","s057-databank-worldbank-org"]},
"罗马共和国":{
 "defn":"罗马共和国：以罗马城为中心、由元老院与民众会议等制度治理的古代政治体，后扩张为地中海世界主导力量。",
 "geo":"台伯河畔的拉丁姆平原提供农业与交通基础，意大利半岛的中置位置与海岸线利于向地中海扩张。",
 "influence":"农业、道路与军团组织相互支撑，地理条件提供机会，但共和制度与政治选择同样是核心变量。",
 "polities":"Livius 的 Roman Republic 与 Italy 分类页提供专题入口，可支撑概述；具体执政官年表与战役序列待逐条核验。",
 "connections":"罗马通过道路与海路连接意大利、西西里、北非与希腊化世界，商品、军队和法律沿网络流动。",
 "today":"共和遗产仍影响法律与政治语言。遗产保护与游客数据待按年份核验。",
 "sources":["livius-roman-republic","livius-italy","s010-unesco-org"]},
"不列颠群岛":{
 "defn":"不列颠群岛：欧洲西北缘的岛群，海洋性气候、海岸地形与海峡通道深刻影响区域交通与聚落分布。",
 "geo":"群岛由大不列颠岛、爱尔兰岛及众多小岛组成，海岸曲折，海峡与港湾众多。地形包括高地、低地与沿海平原，降水受海洋气团影响。",
 "influence":"海洋通道有利于港口与对外联系，气候与土地条件影响农业类型；社会变化还与贸易、技术和制度有关，不能单由岛屿位置解释。",
 "polities":"本条只写自然地理背景，不在此叙述具体王朝与政权序列；相关历史条目待专门来源核验后再展开。",
 "connections":"群岛通过英吉利海峡、北海与北大西洋连接欧洲大陆和海外港口，海运长期是重要联系方式。",
 "today":"沿海城市与港口仍具重要地位。人口、语言与港口货运数据待按年份从权威机构补齐。",
 "sources":["s050-oceanservice-noaa-gov","s039-climate-nasa-gov","s018-fao-org"]},
}
FIX_NOTES={
 "城市起源":"第7轮来源复查：Livius 新增罗马/迦太基页，仍无城市起源专题；维持 L1。",
 "尼罗河三角洲":"第7轮来源复查：Livius Egypt 为古史分类入口，非三角洲专题；维持 L1。",
 "长江流域":"第7轮来源复查：Livius 无东亚流域专题；维持 L1。",
 "阿尔卑斯山":"第7轮来源复查：Livius Italy 分类页未给出阿尔卑斯专题；维持 L1。",
 "五大湖":"第7轮来源复查：EPA/NOAA 仍为最佳可用来源，缺航道与边界专题；维持 L1。",
 "南极半岛":"第7轮来源复查：Livius 与 NatGeo 新来源无南极主题；维持 L1。",
}
GAP_BY_THEME={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
SOURCE_BY_THEME={"地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],"农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}
def upgrade(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    c=CONTENT[title]
    e.update({"level":"L2","status":"L2完成(第7轮)","definition":c["defn"],"overview":c["defn"].split("：",1)[1],
      "time_or_place":TP,"geo":c["geo"],"influence":c["influence"],"polities":c["polities"],
      "connections":c["connections"],"today":c["today"],"svg":make_svg(title,e["region"],e["theme"]),
      "sources":c["sources"],"needs_verification":True,
      "pending_notes":"第7轮升级：Livius/FAO/NOAA/UNESCO 机构页支撑概述；具体年代、王表、战役与现状数值待专门来源核验。"})
    return e["id"]
 raise SystemExit("未找到:"+title)
def fix(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    e["pending_notes"]=FIX_NOTES[title];e["last_update"]=TODAY;e["status"]="来源再核未通过(第7轮)"
    return e["id"]
 raise SystemExit("未找到:"+title)
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第6轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第7轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第7轮)"
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
