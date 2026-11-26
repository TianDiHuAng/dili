# -*- coding: utf-8 -*-
"""新增 3 条自然地理：河漫滩、冲积扇、多年冻土。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")
E=[
 dict(title="河漫滩",tier="重要",theme="地形",
  definition="河漫滩：河流中下游谷底在洪水期被淹没、由细粒泥沙淤积而成的平坦滩地，分布于河床两侧。",
  tp="现代（洪水泛滥持续加积）",
  overview="河漫滩：河流中下游谷底平坦、洪水期被淹没的滩地，由洪水携带的细砂/粉砂在河床两侧淤积而成。近河处因粗粒沉积与反复加积形成天然堤，远离河道为低洼的洼地/沼泽。",
  geo="洪水期河水漫出河床，流速骤减，携带的细粒泥沙在河床两侧沉积，逐步加高成河漫滩。近河因沉积较粗较快形成天然堤，远离河道地势低洼、多为细粒与有机质堆积（沼泽）。",
  infl="所引 1995 年研究用沉积物捕集器实测莱茵河与马斯河洪水期河漫滩沉积的数量与格局，指出沉积受地形与洪水过程控制；所引 2020 年研究把河漫滩地貌用于洪水管理。本条「河漫滩由洪水泛滥的细粒淤积形成，并具有天然堤—洼地分异」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="河漫滩与洪水调蓄、农业与湿地生态相关；围垦与堤防改变其加积过程。",
  src=[("openalex-W2162121861","Floodplain sedimentation: Quantities, patterns and processes",1995,341,1108),
       ("openalex-W3097668409","Applying floodplain geomorphology to flood management",2020,34,1014)],kw=["floodplain"]),
 dict(title="冲积扇",tier="重要",theme="地形",
  definition="冲积扇：河流出山口后因坡度骤减、流速降低，泥沙在山前堆积成的扇形堆积体。",
  tp="现代（山前持续堆积）",
  overview="冲积扇：河流出山口进入平原时坡度骤减、搬运能力下降，携带的砾砂在山前堆积成向平原展开的扇形地貌。扇顶颗粒粗、向下游变细，扇面常分汊；洪水可重塑扇面。",
  geo="河流出山口坡度骤减，水流分散、流速降低，先堆积粗砾（扇顶），细粒被带到扇缘，形成“粗—细”分选与扇形展开。扇面河道分汊、易迁移，洪水与泥石流可改造扇面。",
  infl="所引 1987 年研究讨论冲积扇的堆积与切割关系及其与物源—主河道的耦合；所引 2022 年研究指出冲积扇由主（建扇，十年尺度）与次（改造）两级地貌过程共同塑造。本条「冲积扇为出山口坡度骤减时的扇形堆积，扇顶粗扇缘细」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="冲积扇与山前洪积、绿洲/城镇分布和山洪灾害相关。",
  src=[("openalex-W1989559645","Alluvial fan dissection: relationships between morphology and sedimentation",1987,87,1996),
       ("openalex-W4220883426","Secondary Geomorphic Processes and Their Influence on Alluvial Fan Morphology",2022,36,1723)],kw=["alluvial fan"]),
 dict(title="多年冻土",tier="重要",theme="地形",
  definition="多年冻土：连续两年以上保持冻结的土层，上部为季节性冻融的活动层，分布于高纬与高海拔地区。",
  tp="现代（受气候变暖影响退化）",
  overview="多年冻土：持续两年以上处于冻结状态的土层，地表之下为夏季融化、冬季冻结的活动层。多分布于高纬（西伯利亚、北美）与青藏高原等高海拔区；气候变暖导致冻土退化，释放碳并引发热喀斯特。",
  geo="多年冻土上覆季节性冻融的“活动层”，下部常年冻结；冰楔、冻胀丘与热喀斯特洼地是典型现象。地温与年均气温决定其分布；升温使活动层加深、冻土退化。",
  infl="所引 2012 年研究综述中国多年冻土分布及其编制的多套冻土图；所引 2014 年研究评估气候变暖与冻土退化对北方泥炭地碳通量的影响。本条「多年冻土为常年冻结土层、上覆活动层，暖化导致退化与碳释放」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="多年冻土与寒区水文、碳循环和工程稳定性相关；退化引发热喀斯特与地基失稳。",
  src=[("openalex-W2159555251","Distribution of Permafrost in China: An Overview of Existing Permafrost Maps",2012,349,1462),
       ("openalex-W2148042884","Assessing effects of permafrost thaw on C fluxes based on multiyear modeling",2014,58,1670)],kw=["permafrost"]),
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
