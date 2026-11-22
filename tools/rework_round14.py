# -*- coding: utf-8 -*-
"""第14轮抽检返工：
- 保留 2 条有真实专题来源的 L2（五大湖、科罗拉多高原），并修正越界表述；
- 其余 9 条降级 L1（来源不支持五段）；
- 修正 related 语义错配。
"""
import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条只写自然地理与生态背景，不叙述具体政权、王朝与年代序列（相关历史条目待专门史料核验）。"

KEEP={
"五大湖":{
 "definition":"五大湖：北美中东部的五个相连大型淡水湖群，位于美加交界地带，经河道与大西洋水系相连。",
 "overview":"北美中东部的五个相连大型淡水湖群，位于美加交界地带，经河道与大西洋水系相连。",
 "geo":"湖群由五个相连的大型淡水湖组成，湖岸线曲折、水域面积广阔。湖区属温带气候，季节水位变化是重要水文特征。",
 "influence":"淡水与航运条件支撑沿岸聚落与产业，湖泊生态对营养盐输入和外来物种敏感。人类利用方式与流域管理相关，不作单一环境解释。",
 "polities":NAT,
 "connections":"湖群内部以水道相连，并经河道与运河网络通向大西洋水系，构成跨区域的淡水与运输系统。",
 "today":"富营养化、外来物种与水位波动是长期管理议题；渔业与饮用水供给依赖持续监测。面积、水量与水质指标需按年份从 EPA/NOAA 机构页面核验。",
 "sources":["epa-great-lakes","noaa-glerl"],
 "svg_theme":"区域"},
"科罗拉多高原":{
 "definition":"科罗拉多高原：北美西南部的高原区，以层状沉积岩与深切峡谷著称，大峡谷是其代表地貌。",
 "overview":"北美西南部的高原区，以层状沉积岩与深切峡谷著称，大峡谷是其代表地貌。",
 "geo":"高原由多套沉积岩层构成，河流长期下切形成深峡谷。国家公园署的地质说明记录了岩层序列与侵蚀过程，可作为核对地貌成因的入口。",
 "influence":"干旱与深切地形限制农业与交通，河谷与泉水点决定聚落位置。地貌条件提供约束，土地利用方式还受制度与技术影响。",
 "polities":NAT,
 "connections":"高原通过河流系统与下游干旱区相连，水系把泥沙与溶解物质输送到更远区域。",
 "today":"水资源分配、侵蚀与旅游管理是当代议题。降水、径流与地层数据需按年份从 USGS/NPS 机构页面核验。",
 "sources":["nps-grand-canyon-geology","nps-grand-canyon"],
 "svg_theme":"地形"},
}

DOWN={
"大堡礁":("大堡礁：澳大利亚东北岸外的珊瑚礁群，由珊瑚骨骼长期堆积形成，是重要的海洋生态系统。",
 ["s050-oceanservice-noaa-gov","s085-unesco-org"],
 "二次返工：抽检 FAIL——现用来源正文不含珊瑚礁专题内容，且「世界规模最大」为无源极值断言；已降级 L1，待 GBRMPA 或 UNESCO 大堡礁遗产页等专题来源到位后再升级。"),
"格陵兰岛":("格陵兰岛：位于北大西洋与北冰洋之间的大型岛屿，大部分面积被冰盖覆盖。",
 ["s039-climate-nasa-gov","s049-ncei-noaa-gov"],
 "二次返工：抽检 FAIL——现用 NASA/NOAA 页面为新闻门户与泛论气候页，不含格陵兰专题内容；「世界最大岛屿」为无源极值断言，已改写并降级 L1。待 NASA Greenland / NOAA Arctic 专题页到位后再升级。"),
"北美冰盖":("北美冰盖：地质历史时期覆盖北美北部的巨大冰体，对当地地形与水系留下深远影响。",
 ["s038-earthobservatory-nasa-gov","s056-earthquake-usgs-gov"],
 "二次返工：抽检 FAIL——原两条来源实为同一落地页（实质单源），且「更新世」时代叙述与「年代待核」自相矛盾；已删去时代与冰川过程序列并降级 L1。待第四纪冰川专题来源（如 USGS 冰川地质页）到位后再升级。"),
"墨西哥湾":("墨西哥湾：北美南部的大型海湾，被美国南部与墨西哥环绕，与大西洋和加勒比海相连。",
 ["s050-oceanservice-noaa-gov","s048-climate-gov"],
 "二次返工：抽检 FAIL——原稿「沿岸有堡礁带」为事实错误（应为障壁岛与佛罗里达礁区珊瑚礁），且来源不含墨西哥湾专题内容；已改写并降级 L1。theme 由气候改为地形。"),
"尼罗河三角洲":("尼罗河三角洲：尼罗河入地中海处的冲积平原，地势低平、河网密布，是重要的农业区。",
 ["fao-aquastat-basins","s013-fao-org"],
 "二次返工：抽检 FAIL——AQUASTAT 现用页为目录级（不含尼罗河/三角洲专题正文），且 connections 曾写「粮食与物资转运」经济史断言、与窄化声明冲突；已删去该断言并降级 L1。待 AQUASTAT 埃及/尼罗河流域剖面页到位后再升级。"),
"湄公河三角洲":("湄公河三角洲：湄公河入海处的低平冲积平原，水网密集，是重要的稻作区。",
 ["fao-aquastat-basins","s013-fao-org"],
 "二次返工：抽检判 PASS 但来源仅目录级（不含湄公河/三角洲正文）；按整批返工原则一并降级 L1，待 AQUASTAT 流域剖面页到位后再升级。"),
"冲积平原":("冲积平原：河流搬运的泥沙在河道两侧或下游堆积形成的平坦地形，常见于大河中下游。",
 ["s015-fao-org","s016-fao-org"],
 "二次返工：抽检判 PASS 但来源为土地/土壤落地页（不含 alluvial/floodplain 概念）；按整批返工原则降级 L1，待地貌专题来源到位后再升级。"),
"山地农业":("山地农业：在高差大、坡度陡的地区进行的农业活动，常以梯田与多样作物组合适应环境。",
 ["s016-fao-org","s083-fao-org"],
 "二次返工：抽检判 PASS 但来源为土地概览与土壤门户（不含 mountain/terrace 内容）；按整批返工原则降级 L1，待 FAO 山地农业专题到位后再升级。"),
"人口迁移":("人口迁移：人口在地理空间上的移动，按范围可分为区域内、跨区域与国际迁移。",
 ["s004-population-un-org","s023-ourworldindata-org"],
 "二次返工：本轮未抽中，但同批来源均为机构入口级；按整批返工原则降级 L1，待迁移专题数据页到位后再升级。"),
}

RELATED_FIX={
 "科罗拉多高原":None,"墨西哥湾":None,"大堡礁":None,"格陵兰岛":None,
}

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
titles={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 保留 L2 并修正
for t,c in KEEP.items():
 e=titles[t]
 e.update({"level":"L2","status":"L2完成(第14轮)-专题来源",
   "definition":c["definition"],"overview":c["overview"],
   "geo":c["geo"],"influence":c["influence"],"polities":c["polities"],
   "connections":c["connections"],"today":c["today"],
   "sources":c["sources"],"needs_verification":True,"last_update":TODAY,
   "pending_notes":"第14轮二次返工后保留：只用专题页正文可支撑的自然地理内容，政权与年代细节留待专门史料。"})
 # 重新生成 SVG（区分主题，避免模板复用）
 e["svg"]=(
  "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
  "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
  + ("<ellipse cx='250' cy='200' rx='90' ry='60' fill='none' stroke='var(--accent)' stroke-width='3'/>"
     "<ellipse cx='420' cy='170' rx='70' ry='45' fill='none' stroke='var(--accent)' stroke-width='3'/>"
     "<ellipse cx='530' cy='235' rx='60' ry='40' fill='none' stroke='var(--accent)' stroke-width='3'/>"
     "<circle cx='300' cy='170' r='5' class='pt'/><text x='315' y='175' class='lbl'>上湖</text>"
     "<text x='60' y='370' class='dim'>示意图，非精确测绘</text>"
     if t=="五大湖" else
     "<path d='M60 300 L200 250 L340 250 L480 250 L620 250 L700 300' fill='none' stroke='var(--accent)' stroke-width='3'/>"
     "<path d='M340 250 L380 330' fill='none' stroke='var(--accent)' stroke-width='4'/>"
     "<text x='90' y='240' class='lbl'>层状岩层</text><text x='390' y='345' class='lbl'>河谷下切</text>"
     "<text x='60' y='370' class='dim'>示意图，非精确测绘</text>")
  +"</svg>")

# 2) 降级 9 条
DOWNED=[]
for t,(defn,srcs,note) in DOWN.items():
 e=titles[t]
 for k in ["geo","influence","polities","connections","today","svg"]:
  e.pop(k,None)
 e.update({"level":"L1","status":"二次返工降级L1(第14轮)","definition":defn,
   "overview":defn.split("：",1)[1],"time_or_place":"时期与年代待专门来源核验（详见待核实）",
   "sources":srcs,"needs_verification":True,"pending_notes":note,"last_update":TODAY})
 if t=="墨西哥湾": e["theme"]="地形"
 DOWNED.append(t)

# 3) related 语义修正：把明显错配的 related 替换为同单元同主题条目
for u,d in docs.items():
 same={}
 for e in d["entries"]: same.setdefault(e["theme"],[]).append(e["id"])
 for e in d["entries"]:
  rel=[r for r in e.get("related",[]) if r in titles]
  bad=[r for r in rel if titles[r]["unit_id"]!=e["unit_id"]]
  if len(bad)>=2:
   pool=[i for i in same.get(e["theme"],[]) if i!=e["id"]][:2]
   pool+= [i for th,ids in same.items() if th!=e["theme"] for i in ids if i!=e["id"]][:1]
   e["related"]=list(dict.fromkeys(pool))[:3] or rel[:1]

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("保留L2:",list(KEEP))
print("降级L1:",len(DOWNED),"->","、".join(DOWNED))