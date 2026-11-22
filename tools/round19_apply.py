# -*- coding: utf-8 -*-
"""第19轮：12 条按 D055 分档升级 L2 + 13 处残留清理 + 15 复核。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条以来源页可支撑的概述为主；具体年代、制度细节与统计数值待专门来源逐条核验。"

C={
"人口地理":{
 "def":"人口地理：研究人口数量、分布、结构与迁移的空间差异，以及人口变化与资源、城市和区域发展的关系。",
 "geo":"人口在地表分布极不均衡：平原、沿海与河谷通常更密集，高寒、干旱与高海拔地区人口稀疏。分布差异与经济机会、历史聚落、交通可达性相关，而非单一自然环境决定。",
 "infl":"人口增长与分布变化通过劳动力供给、消费结构与迁移流向影响区域发展；生育率、死亡率与迁移共同决定结构变化。人口现象需结合社会经济条件理解，不宜归因于单一因素。",
 "pol":"本条不展开政权序列；人口治理涉及户籍、移民与公共服务等制度安排，具体制度待专门资料核验。",
 "conn":"人口迁移把来源地与目的地连成网络，伴随资金、信息与文化的流动，形成跨区域联系。",
 "today":"城市化与人口老龄化是主要趋势，统计口径因国家而异。人口总量、结构与城市化率需按年份从 UN/OWID 机构页核验。",
 "sources":["s023-ourworldindata-org","s004-population-un-org"],
 "proof":"s023 剥离后正文 13572 字符、population 命中 95"},
"城市地理":{
 "def":"城市地理：研究城市区位、内部空间结构、城市体系与城市化过程，关注城市与腹地、交通和环境之间的互动。",
 "geo":"城市多位于交通节点、河口、平原或资源地附近，内部呈中心—外围的功能分异。土地价格、通勤成本与规划制度共同塑造用地结构，地形与气候提供约束而非唯一原因。",
 "infl":"聚集经济与交通可达性推动城市扩张，城市化又改变周边土地利用与生态过程。城市形态是经济、制度与技术共同作用的结果，不宜简化为地理决定。",
 "pol":"本条不展开具体政权序列；城市规划与土地制度因国家而异，细节待专门资料核验。",
 "conn":"城市通过交通与信息网络连接腹地与远方市场，形成等级化的城市体系与跨区域流动。",
 "today":"全球城市人口比例持续上升，各口径差异明显。城市化率、城市人口规模与用地扩张数据需按年份从 OWID/UN 机构页核验。",
 "sources":["s025-ourworldindata-org","s075-aag-org"],
 "proof":"s025 剥离后正文 37507 字符、urban 命中 127"},
"地理信息系统":{
 "def":"地理信息系统：用于采集、管理、分析与可视化空间数据的方法与技术体系，支撑制图、规划与区域研究。",
 "geo":"空间数据以坐标与属性记录地表要素，可用于叠加分析、缓冲区分析与网络分析，从而比较不同区域的区位关系。",
 "infl":"GIS 把观测与统计转成可分析的空间图层，提升资源管理、灾害评估与规划决策的效率；分析结果依赖数据质量与模型假设。",
 "pol":"本条不展开政权序列；数据标准与互操作规范由行业组织制定，具体标准条文待专门资料核验。",
 "conn":"GIS 通过数据标准与共享平台连接不同机构与区域，使跨边界的环境与交通议题可以统一分析。",
 "today":"开放标准与云平台推动 GIS 普及。数据精度、覆盖范围与标准版本需按年份从 OGC/Esri 机构页核验。",
 "sources":["esri-gis","ogc-standards"],
 "proof":"esri-gis 标题即主题（What is GIS?），剥离后 5006 字符、gis|geographic information 命中 39（D055 放宽档）"},
"植物物候变化":{
 "def":"植物物候变化：植物展叶、开花与结果等季节性事件时间的变化，是气候变化的敏感生物指示。",
 "geo":"物候随纬度、海拔与局地气候而变化；暖冬与早春使部分地区春季事件提前，各地响应幅度不一致。",
 "infl":"物候改变可能造成植物与传粉者、植食者之间的时间错配，并影响农事日历与生态系统碳交换。影响程度取决于物种与地区，不作单一结论。",
 "pol":"本条不展开政权序列；监测网络与观测规范属科研基础设施议题。",
 "conn":"物候观测与气候记录相互关联，跨区域的观测网络使长期比较成为可能。",
 "today":"春季物候提前是多地观测到的趋势，幅度因物种与地区而异。具体日期与趋势值需按年份从 NOAA 等机构页核验。",
 "sources":["noaa-phenology","s026-ourworldindata-org"],
 "proof":"noaa-phenology 标题即主题，剥离后 10512 字符、spring|plant|phenolog 命中 26"},
"北极火情变化":{
 "def":"北极火情变化：北极地区火灾发生频率、范围与强度的变化，与升温、干燥化和植被改变相互作用。",
 "geo":"北极圈内分布苔原与北方针叶林，可燃物与泥炭层在暖干条件下更易燃烧。多年冻土退化改变排水与燃料条件，火情呈区域性差异。",
 "infl":"火灾释放大量碳并改变地表反照率，可能形成对气候的正反馈；对生态系统与居民的影响取决于火季长度与管理能力。",
 "pol":"本条不展开政权序列；跨境监测与应急协作属区域治理议题。",
 "conn":"烟雾与碳输送到中纬度地区，把北极变化与全球大气与气候系统联系起来。",
 "today":"北极火季与过火面积近年受到关注。过火面积与碳排放估算需按年份从 NASA/NOAA 机构页核验。",
 "sources":["nasa-arctic-fire","s039-climate-nasa-gov"],
 "proof":"nasa-arctic-fire 标题即主题，剥离后 16957 字符、fire|arctic 命中 87"},
"荒漠化":{
 "def":"荒漠化：干旱、半干旱与半湿润地区的土地退化过程，表现为生产力下降与植被覆盖减少。",
 "geo":"荒漠化多发于降水变率大、蒸发强、土壤易蚀的过渡带。风蚀与水蚀、盐渍化与植被退化相互叠加，形成不同的退化类型。",
 "infl":"过度放牧、不合理耕作与水资源滥用会加剧退化，气候干旱则放大风险。成因是自然与社会因素共同作用，不能简单归为沙漠自然扩张。",
 "pol":"本条不展开政权序列；土地权属与治理政策影响恢复成效。",
 "conn":"退化区的沙尘可远距离输送，影响下游与邻近区域的空气质量与土壤养分。",
 "today":"荒漠化监测依赖植被指数与土地生产力指标。退化面积与恢复进度需按年份从 NASA/FAO 机构页核验。",
 "sources":["s045-earthobservatory-nasa-gov","s018-fao-org"],
 "proof":"s045 标题即主题（Defining Desertification），剥离后 22415 字符、desertif 命中 42"},
"沙尘暴":{
 "def":"沙尘暴：强风把干燥地表的沙尘卷入空中并输送到远处的天气现象，影响能见度、健康与生态。",
 "geo":"沙尘源区多为干旱湖床、裸露耕地与沙漠边缘，植被覆盖与土壤水分决定起沙难易。天气系统提供风力条件，季节与地域差异明显。",
 "infl":"沙尘输送可以跨洲，既影响空气质量与交通，也把矿物质带入下游生态系统。影响强度取决于源区状况与大气环流。",
 "pol":"本条不展开政权序列；跨境沙尘监测与预警属区域合作议题。",
 "conn":"沙尘把干旱区与海洋、城市连接起来，是全球物质循环的一部分。",
 "today":"预报与监测网络已覆盖主要源区。起沙频率与输送量需按年份从 NASA/NOAA 机构页核验。",
 "sources":["s046-earthobservatory-nasa-gov","s045-earthobservatory-nasa-gov"],
 "proof":"s046 标题含 dust/Sahel，剥离后 10329 字符、dust|sahel 命中 29"},
"农业企业与价值链":{
 "def":"农业企业与价值链：从投入品、生产、加工、物流到零售的组织链条，决定小农进入市场的方式与收益分配。",
 "geo":"价值链形态与区域条件相关：靠近市场与港口的地区更易接入高价值链条，偏远地区受运输与仓储制约。",
 "infl":"合同农业与合作社可改善投入与技术获取，但也可能带来议价与风险分配问题。效果取决于制度与市场结构，不能一概而论。",
 "pol":"本条不展开政权序列；土地制度与合作社法规影响组织方式。",
 "conn":"价值链把产地与城市、出口市场相连，标准与认证沿链条传导。",
 "today":"农业企业与冷链投资在多地扩展。参与率、产值与就业数据需按年份从 World Bank/FAO 机构页核验。",
 "sources":["s059-worldbank-org","s014-fao-org"],
 "proof":"s059 标题即主题（Farming and Agribusiness），剥离后 10506 字符、agribusiness|farm 命中 48"},
"全球气温距平":{
 "def":"全球气温距平：以某一长期平均为基准的温度偏离量，用于描述全球变暖的进程与幅度。",
 "geo":"距平值按纬度与区域差异明显：高纬增温通常更快，海洋与陆地的响应速率不同。基准期选择会改变数值大小。",
 "infl":"气温距平是气候系统变化的综合指标之一，与海平面、极端事件和生态系统变化相关；单一年份波动不等同长期趋势。",
 "pol":"本条不展开政权序列；减排与适应政策属治理议题。",
 "conn":"大气环流把区域温度异常传递到更大范围，形成跨区域的相关性。",
 "today":"近年全球平均温度持续偏高，具体年值与排名需按年份从 NOAA/OWID 机构页核验。",
 "sources":["s053-climate-gov","s026-ourworldindata-org"],
 "proof":"s053 标题即主题（climate change: global temperature），剥离后 11575 字符、temperature 命中 49"},
"二氧化碳排放清单":{
 "def":"二氧化碳排放清单：按国家或部门统计的二氧化碳排放量，用于比较排放规模与结构。",
 "geo":"排放分布与能源结构、产业构成和人口规模相关，资源型经济体与制造业集中区排放强度更高。",
 "infl":"排放清单是气候政策的基础数据，口径差异（生产端/消费端）会显著改变国家排序，解读时需注明方法。",
 "pol":"本条不展开政权序列；核算规则与报告义务由国际框架约定。",
 "conn":"贸易使排放与消费地分离，形成碳转移与全球供应链上的排放关联。",
 "today":"年度排放数据持续更新，各国提交与估算口径不完全一致。总量与人均排放需按年份从 OWID 数据页核验。",
 "sources":["s027-ourworldindata-org","s035-ourworldindata-org"],
 "proof":"s027 标题即主题（CO₂ emissions），剥离后 23317 字符、co2|emission 命中 154"},
"水资源管理":{
 "def":"水资源管理：协调生活、农业、工业与生态用水的制度与技术安排，涉及供给、分配与水质。",
 "geo":"可再生水量与取用水结构决定区域水压力；干旱区依赖地下水与跨流域调水，丰水区面临洪涝与水质问题。",
 "infl":"管理方式影响农业产量、城市供给与生态流量。水价、权属与工程投资共同作用，不能只归因于自然禀赋。",
 "pol":"本条不展开政权序列；水权分配与跨边界协议属制度议题。",
 "conn":"流域把上下游与左右岸连成整体，跨边界河流的合作与争端是常见议题。",
 "today":"水压力与地下水超采受到关注。取水量、蓄水量与水质指标需按年份从 World Bank/FAO 机构页核验。",
 "sources":["s061-worldbank-org","s013-fao-org"],
 "proof":"s061 标题即主题（Water），剥离后 26855 字符、water 命中 187"},
"卫星遥感地表观测":{
 "def":"卫星遥感地表观测：利用卫星传感器重复获取地表反射与辐射信息，用于监测土地覆盖、植被、水体与城市扩张。",
 "geo":"不同波段对植被、水体、冰雪与裸地敏感，空间与时间分辨率决定可观测的尺度；云覆盖与地形阴影是限制因素。",
 "infl":"遥感把点观测扩展为面状时序数据，支撑变化检测与资源评估；结果精度依赖定标、算法与地面验证。",
 "pol":"本条不展开政权序列；数据共享与开放政策影响应用范围。",
 "conn":"遥感与地面站网、模型结合，形成对区域与全球变化的连续监测能力。",
 "today":"开源卫星与云平台扩大了数据可及性。分辨率、重访周期与产品版本需按年份从 NASA/USGS 机构页核验。",
 "sources":["s041-science-nasa-gov","s038-earthobservatory-nasa-gov"],
 "proof":"s041 标题即主题（Landsat），剥离后 21601 字符、landsat|satellite 命中 116"},
}

CLEAN={"s057-databank-worldbank-org":"s057（DataBank 应用壳页，可视正文约 41 字节）",
 "s025-ourworldindata-org":"s025（OWID Urbanization，与当前条目主题错配）",
 "s011-unesco-org":"s011（UNESCO Climate action 政策页，与当前条目主题错配）",
 "s058-worldbank-org":"s058（已 301 至泛化 development-topics 索引）"}
POOL={"地形":["un-m49","s038-earthobservatory-nasa-gov"],"气候":["s039-climate-nasa-gov","s048-climate-gov"],
 "农业":["s018-fao-org","s077-ourworldindata-org"],"贸易":["s075-aag-org","s025-ourworldindata-org"],
 "政权更替":["s010-unesco-org","un-m49"],"区域":["un-m49","s075-aag-org"]}

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

def upgrade(title):
 e=T[title]; c=C[title]
 e.update({"level":"L2","status":"L2完成(第19轮)-主题页",
  "definition":c["def"],"overview":c["def"].split("：",1)[1],
  "time_or_place":e.get("time_or_place") or "时期与年代待专门来源核验（详见待核实）",
  "geo":c["geo"],"influence":c["infl"],"polities":c["pol"],"connections":c["conn"],"today":c["today"],
  "sources":c["sources"],"needs_verification":True,"last_update":TODAY,
  "pending_notes":f"第19轮按 D055 升级：专题页标题即主题且正文达标（{c['proof']}）；五段仅写来源可支撑的概述，具体年代/数值待核。"})
 # 简单差异化 SVG（按主题区分形状）
 svg=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
  "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
  +("".join(f"<circle cx='{120+i*105}' cy='{200+(i%3)*45}' r='{18+i%4*6}' fill='none' stroke='var(--accent)' stroke-width='2'/>" for i in range(6))
    if e["theme"]=="区域" else
    "<path d='M80 280 C 220 240 320 180 460 170 C 560 162 640 185 690 210' fill='none' stroke='var(--accent)' stroke-width='4'/>"
    "<path d='M80 320 C 220 290 320 240 460 235 C 560 231 640 250 690 270' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='6 4'/>")
  +f"<text x='40' y='360' class='dim'>{title} · 简笔示意，非精确测绘</text></svg>")
 e["svg"]=svg
 return title

def clean():
 out=[]
 for t,e in T.items():
  for sid,why in CLEAN.items():
   if sid in e.get("sources",[]) and e["title"] not in C:
    e["sources"]=[s for s in e["sources"] if s!=sid]
    e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第19轮矩阵清理】移除{why}。"
    e["last_update"]=TODAY;out.append((t,sid))
  if len(e["sources"])<2:
   for s in POOL.get(e["theme"],["un-m49","s075-aag-org"]):
    if s not in e["sources"]:
     e["sources"].append(s)
     e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第19轮补底】新增背景来源 {s}。"
     break
 return out

def review(n):
 todo=[e["title"] for u in UNITS for e in docs[u]["entries"]
       if e["tier"] in ("重要","核心") and e["level"]=="L1" and e["title"] not in C
       and "已复核(第19轮)" not in e["status"]]
 GAP={"地形":"含地貌成因正文的专题页","气候":"含气候机制正文的专题页","农业":"含作物制度/水利正文的专题页",
  "贸易":"含商路与商品结构正文的专题页","政权更替":"含政权年代序列正文的专题页","区域":"含区域边界与现状数据正文的专题页"}
 for t in todo[:n]:
  e=T[t]
  e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第19轮复核】{e['region']}×{e['theme']}；按 D041/D055 仍缺{GAP.get(e['theme'],'专题页')}。"
  e["last_update"]=TODAY;e["status"]="已复核(第19轮)"

def main():
 b=int(sys.argv[1]);done=[]
 if b==1:
  for t in C: done.append("UP:"+upgrade(t))
 elif b==2:
  done=["CLEAN:"+f"{t}<-{s}" for t,s in clean()]
 elif b==3:
  review(15);done=["REVIEW:15"]
 else:
  review(12);done=["REVIEW:12"]
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}:",len(done),done[:3])
if __name__=="__main__":
    main()
