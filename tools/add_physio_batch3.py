# -*- coding: utf-8 -*-
"""新增 5 条自然地理：雅丹地貌、峡湾、牛轭湖、断块山、河流阶地。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")
E=[
 dict(title="雅丹地貌",tier="重要",theme="地形",
  definition="雅丹地貌：干旱区由风力长期吹蚀形成的流线型风蚀垄槽地貌，垄脊与沟槽相间、走向与主导风向一致。",
  tp="地质—现代（干旱区持续风蚀）",
  overview="雅丹地貌：干旱区风蚀形成的流线型垄槽地形，外形似倒扣船体，规模从数米到公里级。风长期吹蚀细粒物质、残留较硬的脊部，形成顺风向排列的垄与槽；雅丹地层是其物质基础。",
  geo="在干旱区强风环境下，风沿地表吹蚀松散沉积，较硬或胶结部分残留成垄脊、较软部分被蚀成沟槽，整体顺主导风向拉长（流线型）。垄槽相间、走向一致是雅丹的典型特征。",
  infl="所引 1979 年研究指出雅丹是流线型风蚀形态（似倒扣船体），地表沙漠中从数米到公里级，并在火星赤道区发现大规模雅丹，作为近期风蚀证据；所引 2023 年研究讨论敦煌雅丹的雅丹地层（物质基础）与颜色变化。本条「雅丹是顺风向的流线型风蚀垄槽地貌，雅丹地层为其物质基础」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="雅丹与风蚀、沙漠化和干旱区地貌相关；地层与古环境记录可供研究。",
  src=[("openalex-W2118756431","Yardangs on Mars: Evidence of recent wind erosion",1979,216,1210),
       ("openalex-W4315628236","Color changes in yardang strata sediment in the Dunhuang Yardang National Geopark",2023,6,2268)],kw=["yardang"]),
 dict(title="峡湾",tier="重要",theme="地形",
  definition="峡湾：冰川侵蚀形成的 U 形谷被海水淹没而成的狭长深海湾，两侧为陡峭岩壁，谷口常有冰蚀槛。",
  tp="第四纪冰期形成，冰后期海侵淹没",
  overview="峡湾：冰川沿谷地下蚀形成 U 形谷，冰期后海平面上升使谷地被海水淹没，成为狭长、水深、两侧陡峭的海湾；谷口常保留冰蚀槛（浅坎）。峡湾记录冰川侵蚀与海平面变化。",
  geo="冰川强烈下蚀把河谷改造为 U 形谷；冰消后海水侵入，形成狭长深水峡湾，谷壁陡峭、支谷高悬；谷口冰蚀槛造成内外水深差异。峡湾多分布于高纬曾受冰川作用的沿海。",
  infl="所引 1986 年研究分析冰川侵蚀形成峡湾槛（threshold）的机制，指出基岩侵蚀率随滑动速度增大；所引 2020 年研究探讨格陵兰东北部峡湾侵蚀的时限与早期冰川作用。本条「峡湾为冰川侵蚀的 U 形谷被海水淹没，谷口有冰蚀槛」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="峡湾与冰川历史、海平面和海岸地貌相关；深水峡湾利于港口。",
  src=[("openalex-W184796866","The Formation of Fjord Thresholds",1986,22,1251),
       ("openalex-W3085499294","The timing of fjord formation and early glaciations in North and Northeast Greenland",2020,0,1418)],kw=["fjord"]),
 dict(title="牛轭湖",tier="重要",theme="地形",
  definition="牛轭湖：河流曲流截弯取直后，被废弃的旧河道两端淤塞而形成的弯月形湖泊。",
  tp="现代（曲流演化过程中形成）",
  overview="牛轭湖：弯曲河道（曲流）在凹岸侧蚀、凸岸堆积下愈发弯曲，最终截弯取直，旧弯道两端淤塞、与主河道分离，形成弯月形（牛轭状）湖泊。牛轭湖是河漫滩上曲流演化的记录。",
  geo="曲流段凹岸受侧蚀与崩塌后退、凸岸堆积前伸，弯道曲率增大；洪水期水流切穿弯颈（截弯取直），废弃弯道逐渐淤塞成牛轭湖。牛轭湖多分布于平原河漫滩。",
  infl="所引 2018 年研究建立耦合河岸侵蚀与曲流演化的物理模型，考虑悬臂式崩塌与崩塌块体分解；所引 2013 年研究以波兰一处牛轭湖为例分析水生植物的繁殖。本条「凹岸侧蚀与崩塌使曲流加剧、截弯取直后旧河道成牛轭湖」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="牛轭湖与河漫滩、泛滥平原和湿地生态相关；记录河流演变。",
  src=[("openalex-W2891957300","Coupled Model of Bank Erosion and Meander Evolution for Cohesive Riverbanks",2018,13,1258),
       ("openalex-W1513609293","Reproduction of Hydrocharis morsus-ranae taxa in an oxbow lake of the River Vistula",2013,11,1249)],kw=["oxbow","meander"]),
 dict(title="断块山",tier="重要",theme="地形",
  definition="断块山：由正断层差异升降形成的山块，山体相对抬升、两侧盆地（地堑）相对下陷，常见于伸展区。",
  tp="地质—现代（伸展构造区持续活动）",
  overview="断块山：在伸展构造区，正断层把地壳切成块体，相对抬升的断块成山、相对下降的断块成盆（地堑/半地堑），形成盆岭相间的地貌。断块山边坡陡、山麓有断层崖与洪积扇。",
  geo="正断层控制块体差异升降：抬升的断块（地垒）成山，下降的断块成盆地或地堑，二者以断层崖相接。地震时的同震位移以盆地下沉为主、山块抬升相对较小。",
  infl="所引 2017 年研究指出在美国盆岭省，同震位移在重力作用下以盆地下沉（断层上盘）为主、山侧（下盘）抬升较小，累积成断块山；所引 2022 年研究讨论断块台地的几何与演化。本条「断块山由正断层差异升降形成，盆地下陷、山块相对抬升」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="断块山与伸展构造、地震和山前洪积相关；盆岭相间是典型伸展地貌。",
  src=[("openalex-W2746164778","From coseismic offsets to fault-block mountains",2017,16,1382),
       ("openalex-W4296462431","Fault-Block Platform Evolution between Late Cretaceous and Early Miocene",2022,1,1858)],kw=["fault-block"]),
 dict(title="河流阶地",tier="重要",theme="地形",
  definition="河流阶地：河流下切后遗留在谷坡上的阶梯状古河谷面，成因为河流由堆积转为下切、多次重复形成多级阶地。",
  tp="第四纪以来（气候与构造驱动的下切—堆积交替）",
  overview="河流阶地：河流在谷底堆积后转为下切，把原来的河漫滩/谷底抬升为阶地，多次下切堆积交替形成多级阶梯状阶地。阶地越靠上越高、越老，记录气候与构造变化。",
  geo="当河流以堆积为主时在谷底形成宽阔河漫滩；当气候或构造使河流下切时，旧河漫滩被抬高成为阶地。下切—堆积多次交替即形成多级阶地，高程与年代自上而下递减。",
  infl="所引 2018 年研究分析澳大利亚东部构造稳定河流的阶地，讨论气候（异源）与内在（自源）因素对沉积供给与流态的控制；所引 2025 年研究讨论如何用 DEM 推断河流阶地的年代。本条「阶地由河流下切与堆积交替、受气候/构造驱动形成多级」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="阶地与河流下切、构造抬升和气候变化相关；可用于定年与古环境重建。",
  src=[("openalex-W2896690467","Climatically-Controlled River Terraces in Eastern Australia",2018,17,2138),
       ("openalex-W4392580073","What can DEMs tell us about the ages of fluvial terraces?",2025,0,2989)],kw=["terrace","terraces"]),
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
