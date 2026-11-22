# -*- coding: utf-8 -*-
"""第14轮：11条重要L1窄化升级L2（仅写来源可支撑的自然地理/生态/人口）+ 29复核。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import make_svg,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
TP="时期与年代待专门来源核验（详见待核实）"
NAT="本条只写自然地理与生态背景，不叙述具体政权、王朝与年代序列（相关历史条目待专门史料核验）。"

C={
"五大湖":{
 "defn":"五大湖：北美中东部的淡水湖群，位于美加交界地带，由地质与冰川过程塑造，通过圣劳伦斯河通向大西洋。",
 "geo":"湖群由多个相连的大型淡水湖组成，湖岸线曲折，水域面积广阔。湖区受温带气候影响，冬季结冰与季节水位变化是重要水文特征；湖泊沉积与岸线形态记录了冰川作用的影响。",
 "influence":"淡水与航运条件支撑沿岸聚落与产业，湖泊生态对营养盐输入和外来物种敏感。人类利用方式与流域管理相关，具体开发格局需结合专门资料，不作单一环境解释。",
 "polities":NAT,
 "connections":"湖群经河道与运河网络连接大西洋水系，湖区内部以水道相连，形成跨区域的淡水与运输系统。",
 "today":"湖泊富营养化、外来物种与水位波动是长期管理议题；渔业与饮用水供给依赖持续监测。面积、水量与水质指标需按年份从 EPA/NOAA 等机构页面核验。",
 "sources":["epa-great-lakes","noaa-glerl"]},
"大堡礁":{
 "defn":"大堡礁：澳大利亚东北岸外的珊瑚礁系统，是世界上规模最大的珊瑚礁群，由珊瑚虫骨骼长期堆积形成。",
 "geo":"礁体分布于热带浅海，依赖温暖水质、清澈度与适宜盐度。珊瑚与共生藻的关系对水温变化敏感，强光、径流与风暴都会影响礁体状态。",
 "influence":"珊瑚礁支撑渔业与海岸防护，其健康与海温、水质和人为压力相关。保护成效取决于管理措施与区域环境条件，需结合监测数据判断。",
 "polities":NAT,
 "connections":"礁区与邻近海岸带、河口和开阔海域存在水体与生物幼体交换，是区域生态连通的一部分。",
 "today":"海水升温与珊瑚白化是主要关注点；保护区管理与监测持续进行。珊瑚覆盖率与水温数据需按年份从 NOAA/UNESCO 等机构页面核验。",
 "sources":["s050-oceanservice-noaa-gov","s085-unesco-org"]},
"格陵兰岛":{
 "defn":"格陵兰岛：世界最大岛屿，大部分面积被冰盖覆盖，位于北大西洋与北冰洋之间。",
 "geo":"岛屿内陆为巨厚冰盖，边缘分布冰原、峡湾与裸露岩地。高纬位置带来极昼极夜与严寒气候，冰盖积累与消融决定冰体质量平衡。",
 "influence":"冰盖储量变化影响全球海平面，是气候系统的关键变量；沿海地带受海冰与洋流影响，人类活动集中于少数定居点。具体影响需结合观测，不作单因推断。",
 "polities":NAT,
 "connections":"岛屿与北大西洋、北冰洋水域相连，冰盖与海洋通过冰川输出和大气环流相互作用。",
 "today":"冰盖质量变化与海平面关系是研究重点。冰量、气温与融水数据需按年份从 NASA/NOAA 等机构页面核验。",
 "sources":["s037-science-nasa-gov","s039-climate-nasa-gov"]},
"北美冰盖":{
 "defn":"北美冰盖：更新世时期覆盖北美北部的巨大冰体，对地形、水系与沉积物分布留下深远影响。",
 "geo":"冰盖中心位于今加拿大北部，向南推进时侵蚀基岩、搬运碎屑，并在退却后留下冰碛、鼓丘与冰川湖。冰体消长与气候波动同步。",
 "influence":"冰川作用塑造了五大湖盆地、冰碛丘陵与河谷，影响后来的水系与土壤分布。地貌与气候的因果关系有明确证据，但具体时序仍需区域资料细化。",
 "polities":NAT,
 "connections":"冰盖范围变化改变了水系与海岸线，进而影响生物迁移与后续人类活动的地理条件。",
 "today":"作为古环境研究对象，其范围与消退时间由地质与湖泊沉积记录重建。年代与范围数据需按年份从 USGS/NASA 等机构页面核验。",
 "sources":["s038-earthobservatory-nasa-gov","s043-earthobservatory-nasa-gov"]},
"科罗拉多高原":{
 "defn":"科罗拉多高原：北美西南部的高原区，以层状沉积岩、深切峡谷与干旱地貌著称。",
 "geo":"高原由多套沉积岩层构成，河流下切形成深峡谷。气候干旱，降水集中于短时强降雨，物理风化与流水侵蚀主导地貌演化。",
 "influence":"干旱与深切地形限制农业与交通，河谷与泉水点决定聚落位置。地貌与气候条件提供约束，土地利用方式还受制度与技术影响。",
 "polities":NAT,
 "connections":"高原通过河流系统与下游干旱区相连，水系把泥沙与溶解物质输送到更远区域。",
 "today":"水资源分配、侵蚀与旅游管理是当代议题。降水、径流与地层数据需按年份从 USGS/NASA 等机构页面核验。",
 "sources":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"]},
"墨西哥湾":{
 "defn":"墨西哥湾：北美南部的大型海湾，被美国南部与墨西哥环绕，与大西洋和加勒比海相连。",
 "geo":"海湾水深较浅，沿岸有三角洲、湿地与堡礁带。暖湿海面为风暴提供水汽与能量，季节性的环流与径流输入影响盐度与营养分布。",
 "influence":"海湾渔业与航运价值高，暖湿条件也使沿岸易受飓风影响。灾害风险取决于暴露程度与防护能力，不能只由气候条件解释。",
 "polities":NAT,
 "connections":"海湾与加勒比海、大西洋水体交换，密西西比河等河流带来淡水与泥沙，形成独特的河口生态。",
 "today":"湿地流失、缺氧区与风暴灾害是管理重点。海温、水位与渔业数据需按年份从 NOAA 等机构页面核验。",
 "sources":["s050-oceanservice-noaa-gov","s048-climate-gov"]},
"尼罗河三角洲":{
 "defn":"尼罗河三角洲：尼罗河入地中海处的冲积平原，地势低平、河网密布，是重要的农业与人口密集区。",
 "geo":"三角洲由河流泥沙沉积形成，分流河道与潟湖交错，地势低洼。北缘受地中海波浪与盐水入侵影响，部分区域排水困难。",
 "influence":"肥沃冲积土与灌溉条件支撑密集农业；低洼地形也带来洪涝与盐化风险。三角洲的利用方式与水利管理相关，具体制度与年代不在本条展开。",
 "polities":NAT,
 "connections":"三角洲通过地中海连接南欧与西亚，通过尼罗河连接非洲内陆，是粮食与物资转运的水陆交汇处。",
 "today":"海平面上升、地面沉降与用水压力是主要议题。面积、人口与沉降速率需按年份从 FAO/NASA 等机构页面核验。",
 "sources":["fao-aquastat-basins","s013-fao-org"]},
"湄公河三角洲":{
 "defn":"湄公河三角洲：湄公河入海处的低平冲积平原，位于越南南部并延伸至柬埔寨东南部。",
 "geo":"三角洲由河流泥沙长期沉积形成，水网密集、地势低洼，受季风降水与上游来水共同影响。咸潮入侵与沉积速率是重要水文特征。",
 "influence":"水网与冲积土支撑稻作农业与密集聚落；低洼地形使区域对洪水与盐水入侵敏感。种植制度与水利安排的具体演变需专门资料。",
 "polities":NAT,
 "connections":"三角洲通过河口与南海相连，通过湄公河干流与上游流域（含中国、老挝、泰国、柬埔寨）形成跨国的水文联系。",
 "today":"咸潮入侵、地面沉降与上游水坝影响是主要议题。面积、产量与沉降数据需按年份从 FAO 等机构页面核验。",
 "sources":["fao-aquastat-basins","s013-fao-org"]},
"冲积平原":{
 "defn":"冲积平原：河流搬运的泥沙在河道两侧或下游堆积形成的平坦地形，常见于大河中下游。",
 "geo":"地形由河流沉积作用形成，土层深厚、地势平缓，河网与古河道交错。沉积物粒径与厚度记录了水动力变化，洪水泛滥是塑造过程的一部分。",
 "influence":"深厚土层与灌溉便利有利于农业，地势低平也带来洪涝与排水问题。土地利用与防洪体系相关，不能仅由地形推断社会形态。",
 "polities":NAT,
 "connections":"冲积平原与上游流域、下游三角洲和沿海湿地在物质输移上连成一体，泥沙与养分沿水系传递。",
 "today":"洪水管理、地面沉降与土壤质量是主要议题。沉积速率、耕地面积与洪水频率需按年份从 FAO 等机构页面核验。",
 "sources":["s015-fao-org","s016-fao-org"]},
"山地农业":{
 "defn":"山地农业：在高差大、坡度陡的地区进行的农业活动，常以梯田、轮作与多样作物组合适应环境。",
 "geo":"山地具有明显的垂直气候带，气温与降水随海拔变化，土层薄且易受侵蚀。坡面水文过程快，水土保持是耕作的前提条件。",
 "influence":"垂直分带使同一区域可种植不同作物，梯田与等高耕作有助于保持水土。耕作方式受土地制度与技术条件影响，不是环境的必然结果。",
 "polities":NAT,
 "connections":"山地农业区常与低地市场形成垂直交换，山货与粮食沿山路与河谷流动。",
 "today":"坡地退化、劳动力变化与气候变化是主要议题。耕地面积、产量与土壤侵蚀数据需按年份从 FAO 等机构页面核验。",
 "sources":["s016-fao-org","s083-fao-org"]},
"人口迁移":{
 "defn":"人口迁移：人口在地理空间上的移动，按范围可分为区域内、跨区域与国际迁移。",
 "geo":"迁移流与来源地、目的地之间的经济机会、环境条件与交通可达性相关；迁移网络一旦形成，会沿既有路径持续。",
 "influence":"迁移改变人口分布与年龄结构，也影响来源地与目的地的劳动力与公共服务。迁移决策由多因素驱动，不宜归因于单一环境压力。",
 "polities":NAT,
 "connections":"迁移把不同区域连成网络，伴随资金、信息与文化的流动，形成跨区域联系。",
 "today":"城市化与国际迁移是当代主要趋势，统计口径因国家而异。净迁移率、城市化率与人口分布数据需按年份从 UN/OWID 等机构页面核验。",
 "sources":["s004-population-un-org","s023-ourworldindata-org"]},
}

GAP={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
POOL={"地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],"农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}

def upgrade(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    c=C[title]
    e.update({"level":"L2","status":"L2完成(第14轮)-窄化自然地理","definition":c["defn"],
     "overview":c["defn"].split("：",1)[1],"time_or_place":TP,
     "geo":c["geo"],"influence":c["influence"],"polities":c["polities"],
     "connections":c["connections"],"today":c["today"],
     "svg":make_svg(title,e["region"],e["theme"]),"sources":c["sources"],
     "needs_verification":True,
     "pending_notes":"第14轮窄化升级：仅写来源可支撑的自然地理/生态/人口内容，政权与年代细节留待专门史料；现状数值待按年份核验。"})
    return e["id"]
 raise SystemExit("未找到:"+title)

def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第13轮)" not in e["status"]:
    out.append(e["title"])
 return out[:29]

def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP.get(e["theme"],"专题来源");pool=POOL.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第14轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第14轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)

def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  for t in C: done.append(upgrade(docs,t))
  for t in review_titles(docs)[:1]: done.append("REVIEW:"+review(docs,t))
 else:
  titles=review_titles(docs);start=1+(b-2)*9
  for t in titles[start:start+9]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))
if __name__=="__main__": main()