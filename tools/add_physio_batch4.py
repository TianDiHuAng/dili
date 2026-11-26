# -*- coding: utf-8 -*-
"""新增 5 条自然地理：冰碛丘陵、海蚀崖、潮滩、土壤侵蚀、冰川湖。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")
E=[
 dict(title="冰碛丘陵",tier="重要",theme="地形",
  definition="冰碛丘陵：冰川消融后堆积的冰碛物（漂砾、砂、黏土混杂）形成的波状丘岗，常见于冰前/冰退区。",
  tp="第四纪冰期—冰后期（冰退后遗留）",
  overview="冰碛丘陵：冰川搬运的碎屑在消融区堆积成冰碛，经冰退后形成起伏的丘岗与垄状地形。冰碛物分选差、砾砂黏混杂；终碛、底碛与侧碛可指示古冰川范围与进退。",
  geo="冰川把大量碎屑裹挟至消融区堆积（底碛、终碛、侧碛），冰退后残留为丘岗与垄状地形。冰碛物无分选、棱角分明；其分布可重建古冰川边缘与冰流方向。",
  infl="所引 2010 年研究以冰岛高原冰帽前缘为例，分析受控冰碛的发育与碎屑搬运路径；所引 1985 年研究把北爱尔兰的横谷冰碛垄分为多种成因类型（如由冰前三角洲合并而成）。本条「冰碛丘陵为冰川消融堆积的冰碛物丘岗，可指示古冰川范围与冰流」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="冰碛丘陵与冰期历史、冰川湖泊和冰水沉积相关；影响地形与土壤。",
  src=[("openalex-W2003505124","Controlled moraine development and debris transport pathways",2010,40,1761),
       ("openalex-W2028454173","Genesis of late Pleistocene cross-valley moraine ridges",1985,9,1085)],kw=["moraine"]),
 dict(title="海蚀崖",tier="重要",theme="地形",
  definition="海蚀崖：波浪侵蚀基岩海岸形成的陡崖，崖前常发育海蚀平台与海蚀凹槽，是海岸侵蚀的标志。",
  tp="现代—全新世（持续受波浪侵蚀）",
  overview="海蚀崖：海浪冲击与掏蚀基岩海岸坡脚，使崖壁后退形成陡崖；崖前残留波切台（海蚀平台）与海蚀凹槽。海平面上升与风暴会加快崖壁后退。",
  geo="波浪在崖脚掏蚀形成凹槽，上部岩体失稳崩塌，崖壁逐步后退，崖前留下向海微倾的海蚀平台。岩性、波浪能量与海平面决定后退速率；软岩海岸后退更快。",
  infl="所引 2024 年研究用数值模型模拟海平面上升下崖前波浪动力变化及其对海岸的影响；所引 2020 年研究指出英国东盎格利亚软岩崖在无防护时可达约 2–5 米/年的长期平均后退速率。本条「海蚀崖由波浪掏蚀—崩塌后退形成，并伴海蚀平台」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="海蚀崖与海岸侵蚀、海平面上升和海岸防护相关；后退威胁沿岸设施。",
  src=[("openalex-W4393582291","Modeling future cliff-front waves during sea level rise",2024,26,1366),
       ("openalex-W3042497364","Soft rock cliff retreat under changing climate drivers",2020,0,2602)],kw=["cliff"]),
 dict(title="潮滩",tier="重要",theme="地形",
  definition="潮滩：潮间带由细砂、粉砂和黏土淤积而成的平缓滩地，随潮汐周期性出露与淹没，发育潮沟。",
  tp="现代（潮汐—泥沙作用持续塑造）",
  overview="潮滩：位于潮间带、坡度极缓的淤泥/粉砂质滩地，随涨落潮周期性淹没与出露。潮水携带细颗粒在滩面淤积，发育潮沟排水；波浪与潮汐强弱决定滩面形态。",
  geo="潮滩在掩护性海岸与河口由细颗粒泥沙淤积形成，坡度极缓、滩面细腻；落潮时出露、涨潮时淹没，潮沟是主要排水与输沙通道。波控与潮控条件交替改变滩面沉积。",
  infl="所引 2005 年研究指出韩国西南开放海岸潮滩的沉积受向岸风浪季节变化控制，出现夏潮控、冬波控的交替；所引 2025 年研究基于 2,538 条断面分析中国潮滩形态的时空变化与驱动。本条「潮滩由潮汐—泥沙淤积形成，并受波浪/潮汐强弱塑造」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="潮滩与河口泥沙、湿地生态和海岸防护相关；围垦与海平面上升威胁潮滩。",
  src=[("openalex-W2144169221","Sedimentation on a wave-dominated, open-coast tidal flat",2005,214,1535),
       ("openalex-W4408122855","Dynamics and drivers of tidal flat morphology in China",2025,43,1193)],kw=["tidal flat","tidal flats"]),
 dict(title="土壤侵蚀",tier="重要",theme="地形",
  definition="土壤侵蚀：水力、风力等外营力剥离并搬运表层土壤的过程，导致土层变薄、肥力下降与土地退化。",
  tp="现代（人类活动显著加速）",
  overview="土壤侵蚀：雨滴溅蚀、坡面径流与风力等剥离、搬运表土，造成土层变薄、养分流失与土地退化，是土壤资源丧失与荒漠化的重要过程。植被覆盖与耕作方式显著影响侵蚀强度。",
  geo="降雨溅蚀打击土表、坡面径流汇集成细沟与切沟搬运泥沙；风蚀吹走细颗粒。坡度、降雨强度、植被与土壤可蚀性决定侵蚀速率；坡脚堆积、沟道输移连接坡面与河流。",
  infl="所引 2016 年研究讨论降雨模拟等实验室方法对径流与土壤侵蚀速率测定的影响；所引 2023 年研究在同一半干旱黄土上比较风蚀与水蚀速率，强调二者常被分开研究。本条「土壤侵蚀由水/风等外营力剥离搬运表土，受植被与耕作显著影响」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="土壤侵蚀与土地退化、荒漠化、河流泥沙和农业可持续相关；水保措施（梯田、植被）可减缓。",
  src=[("openalex-W2510677556","The impact of standard preparation practice on the runoff and soil erosion rates",2016,21,1949),
       ("openalex-W4321480809","Comparison of soil erosion rates by wind and water in a semi-arid loess soil",2023,0,1133)],kw=["soil erosion"]),
 dict(title="冰川湖",tier="重要",theme="地形",
  definition="冰川湖：由冰川侵蚀洼地蓄水、或由冰碛/冰体堰塞而成的湖泊，常位于高山与冰川前缘，存在溃决风险。",
  tp="现代（随冰川退缩而扩张）",
  overview="冰川湖：冰川挖蚀的洼地蓄水，或被冰碛垄、冰体堰塞而成的湖泊。全球变暖使冰川退缩、冰湖扩张，冰碛堰塞或冰堰塞湖可能溃决形成冰川湖溃决洪水（GLOF）。",
  geo="冰川湖多见于高山冰川前缘与冰蚀洼地：冰碛垄或冰体可堰塞成湖；湖盆形态受冰蚀与堆积控制。冰川退缩使冰湖数量与面积增加，湖岸冰碛坝失稳可引发溃决。",
  infl="所引 2023 年研究指出全球变暖与冰川退缩使冰湖形成与扩张，并建立冰湖水深分布的概念模型；所引 2024 年研究对尼泊尔 Tsho Rolpa 冰湖的溃决洪水（GLOF）建模。本条「冰川湖为冰蚀/冰碛堰塞成湖，随冰川退缩扩张并有溃决风险」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="冰川湖与冰川变化、水资源和山地灾害（GLOF）相关。",
  src=[("openalex-W4389420139","A conceptual model for glacial lake bathymetric distribution",2023,28,1914),
       ("openalex-W4404485352","Glacial lake outburst flood (GLOF) modeling of Tsho Rolpa glacial lake, Nepal",2024,8,1335)],kw=["glacial lake"]),
]
P=os.path.join(DATA,"global-themes.json");doc=json.load(open(P,encoding="utf-8"));ids={e["id"] for e in doc["entries"]}
sd=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"));have={s["id"] for s in sd["sources"]}
ow=json.load(open(os.path.join(DATA,"object_words.json"),encoding="utf-8"));ss=json.load(open(os.path.join(DATA,"semantic_scan.json"),encoding="utf-8"))
added=[]
for m in E:
    eid="global-themes-"+sid(m["title"])
    if eid in ids: continue
    doc["entries"].append({"id":eid,"title":m["title"],"tier":m["tier"],"unit_id":"global-themes","region":"全球","theme":m["theme"],"level":"L2","status":"L2完成(新增·自然地理)","definition":m["definition"],"time_or_place":m["tp"],"overview":m["overview"],"related":[],"sources":[x[0] for x in m["src"]],"needs_verification":True,"pending_notes":"新增自然地理条目：形态/过程为教科书性常识；机制与数据据所引文献，具体数值待专门核验。","outlines":[m["title"]+"·自然地理"],"last_update":"2026-11-26","geo":m["geo"],"influence":m["infl"],"polities":m["pol"],"connections":m["conn"],"today":"（本条的当代指标不在本页展开。）","svg":""})
    ids.add(eid);added.append(m["title"])
    for sid_,t,y,c,ln in m["src"]:
        if sid_ in have: continue
        sd["sources"].append({"id":sid_,"title":f"OpenAlex {sid_[9:]} — {t}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":y,"type":"学术文献","url":f"https://api.openalex.org/works/{sid_[9:]}","url2":None,"link_ok":True,"verified":True,"page_title":t[:200],"note":f"OpenAlex 作品 {sid_[9:]}；{y}年；被引 {c}。摘要长度 {ln} 字符。经 Crossref 检索 + DOI 桥取得，摘要已人工阅读。证据强度：strong。"})
        have.add(sid_)
    ow[m["title"]]=m["kw"];ss["scanned_entries"]=sorted(set(ss["scanned_entries"])|{m["title"]})
json.dump(doc,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sd,open(os.path.join(DATA,"sources.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(ow,open(os.path.join(DATA,"object_words.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(ss,open(os.path.join(DATA,"semantic_scan.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]}
save_docs(docs);update_coverage(docs)
print("added",len(added),added)
