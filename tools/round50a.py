# -*- coding: utf-8 -*-
"""第50轮A：为 30 条「侧面文献」条目标注旁证性质（对象同一但仅涉一侧面）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

SIDE={
"印加帝国":"《The Role of Chicha in Inca State Expansion》研究的是**玉米酒（chicha）在国家扩张中的角色**——印加的一个侧面（仪式与再分配），不涉疆域、道路与行政。",
"南极大陆":"《Diatom stratigraphy defining ice sheet grounding…》研究的是**硅藻地层与冰盖接地线**——南极的一个侧面（地层学），不涉大陆地貌总体。",
"密西西比河":"《The Mississippi River Basin Compact》讨论的是**流域跨州治理协定**（法律与制度），不涉水系本身的走向与水文。",
"亚马逊盆地":"《The Atmospheric Component of Biogeochemical Cycles in…》研究的是**大气输送的生物地球化学循环**，不涉盆地地貌与人口。",
"季风系统":"《Mid-Tropospheric Cyclones of the Summer Monsoon》(1978) 研究的是**夏季风中的中层气旋**，属季风系统的一个子现象。",
"河流三角洲":"《Nutrient and Sediment Effects on Oligohaline Marsh…》研究的是**寡盐沼泽的养分与泥沙效应**，属三角洲的一个生态侧面。",
"文艺复兴意大利":"《Poverty Makes Me Invisible: Street Singers…in Italian Renaissance Cities》研究的是**街头艺人与贫困**（社会史侧面）；《Patronage and Italian Renaissance Sculpture》研究的是**雕塑赞助**。两者都不涉城邦竞争与商业财富的整体格局。",
"维京时代":"《Polygyny, Concubinage, and the Social Lives of Women in Viking-Age Scandinavia》研究的是**婚姻与女性社会角色**（性别史侧面）。",
"美国西进":"《The Black West》是**非裔美国人在西部**的史料集，属西进运动的一个群体侧面。",
"莫切文化":"《Moche Art and Iconography》研究的是**莫切的图像与器物**（艺术史侧面），不涉河谷政治经济。",
"阿塔卡马沙漠":"《Endolithic Cyanobacteria in Halite Rocks…》研究的是**岩盐中的岩内蓝细菌**（微生物侧面），不涉沙漠的形成与气候。",
"南锥体":"《The Spanish postwar emigration to the Southern Cone》研究的是**战后西班牙移民**（人口史侧面）。",
"新法兰西":"《Travel Writing, Ethnography, and the Colony-Centric…》研究的是**耶稣会《Relations》的文本流通**（文献史侧面）。",
"古埃及中王国":"《Poetry and Culture in Middle Kingdom Egypt》研究的是**文学与文化**（文本侧面），不涉行政与灌溉。",
"古巴岛":"《Age and Tectonic Setting of the Camagüey Volcanic-Intrusive Arc》研究的是**中部古巴的火山—侵入弧**（构造地质侧面）。",
"巴塔哥尼亚":"《Ancient genomes in South Patagonia…》研究的是**古基因组与人群史**，且本条 theme 为「气候」，属跨领域侧面。",
"复活节岛":"《Prehistoric and early historic agriculture at Maunga Orito》研究的是**一处采石场旁的农业序列**（遗址侧面）。",
"密克罗尼西亚":"《Exploring the role of Micronesian islands in the maintenance of coral…》研究的是**珊瑚礁遗传多样性的维持**（海洋生物侧面）。",
"元代":"《Koryŏ inlay celadon from Taicang Port of the Yuan Dynasty》研究的是**太仓港出土的高丽镶嵌青瓷**（陶瓷贸易侧面）。",
"拜占庭帝国":"《The Birth of the Hospital in the Byzantine Empire》研究的是**医院的起源**（医疗制度侧面）。",
"大自流盆地":"《A mid-Cretaceous microfossil assemblage…》研究的是**白垩纪微体化石组合**（古生物侧面）；《Chlorine 36 dating of very old groundwater》研究的是**地下水定年**（水文地质侧面）。",
"新西兰南岛":"《Naturalised plants in south-west South Island》研究的是**归化植物**（植物侧面）；《Origin of the Torlesse terrane…》研究的是**地体成因**（构造侧面）。",
"古埃及新王国":"《Amphorae in New Kingdom Egypt》研究的是**双耳瓶**（器物侧面）。",
"地理信息系统":"《Remote Scheduling System for Drip Irrigation》是**滴灌远程调度**的应用案例，属 GIS 应用的一个侧面。",
"城市地理":"《2008 Urban Geography Plenary Lecture—Public Health as…》讨论的是**公共卫生与城市政治**（一个专题侧面）。",
"意大利半岛":"《Paleomagnetic evidence for rotation of the Italian Peninsula》研究的是**古地磁记录的半岛旋转**（构造侧面）。",
"澳大利亚内陆干旱气候":"《Evolutionary refugia and ecological refuges…》研究的是**干旱区的生态避难所**（生态侧面）。",
"落基山脉":"《The Yavapai-Mazatzal crustal boundary in the Southern Rocky…》研究的是**南部落基山的地壳边界**（构造侧面）。",
"河中地区":"《The Connection of the Genetic, Cultural and Geographic…》讨论的是**遗传、文化与地理的关联**（多学科侧面）。",
"突厥":"《The Genetic Legacy of the Expansion of Turkic-Speaking…》研究的是**突厥语人群扩张的遗传遗产**（遗传侧面）。",
}
n=0
for t,why in SIDE.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    if "【第50轮旁证认定】" in pn: continue
    e["pending_notes"]=(pn+" 【第50轮旁证认定】本条现有学术来源属**侧面文献**："+why+
      " 按 D095②/D108 的口径，此类文献**对象同一但只支撑某一段或某一侧面**，不能作为整条目的主来源；"
      "已标为旁证，正文相应段落亦已限定范围。主来源待补。").strip()
    e["last_update"]=TODAY;n+=1
print("标注侧面文献:",n)
save_docs(docs)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=50
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)