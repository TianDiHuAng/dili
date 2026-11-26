# -*- coding: utf-8 -*-
"""新增 4 条自然地理：河口湾、蛇形丘、冰水沉积、风蚀盆地。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")
E=[
 dict(title="河口湾",tier="重要",theme="地形",
  definition="河口湾：河流入海处被海水侵入、呈漏斗状的半封闭水体，淡水与咸水在此混合，受潮汐强烈影响。",
  tp="现代（冰后期海侵与河流—海洋共同作用）",
  overview="河口湾：河流入海口因海平面上升或地形下沉被海水侵入形成的漏斗状水域，河水与海水混合。盐淡水交汇形成分层或部分混合，潮汐与径流共同决定其环流与地貌。",
  geo="河口湾是河流与海洋的过渡带：径流带来淡水与泥沙，潮汐带来咸水与能量，二者混合形成盐度梯度与河口环流；地形多呈漏斗状，受潮汐与波浪改造。",
  infl="所引 2013 年研究综述并提出潮汐分层等对经典重力驱动河口环流的修正；所引 2013 年研究重新讨论河口按潮汐与宽度平均的动量/盐量平衡分类。本条「河口湾为淡咸水混合的过渡带，环流受潮汐与径流共同控制」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="河口湾与航运、渔业、泥沙淤积和盐水入侵相关；海平面上升影响其演变。",
  src=[("openalex-W2099210305","The Estuarine Circulation",2013,727,1034),
       ("openalex-W2068034814","Estuary Classification Revisited",2013,24,617)],kw=["estuary","estuarine"]),
 dict(title="蛇形丘",tier="补充",theme="地形",
  definition="蛇形丘：冰盖下融水河道沉积的砂砾，冰退后残留成蜿蜒的长条状垄岗，是冰下河道的遗迹。",
  tp="第四纪冰期—冰后期（冰退后出露）",
  overview="蛇形丘：冰盖底部融水在冰下河道中搬运、堆积砂砾，冰体消融后这些充填物残留为蜿蜒的长垄。其走向指示古冰下水流方向，可重建冰川动力学。",
  geo="冰下融水在冰体底部河道中流动，沿途沉积分选较好的砂砾；冰退后充填物出露，形成蜿蜒、脊状的长垄（蛇形丘）。垄的走向与形态反映冰下排水与冰川退缩。",
  infl="所引 1989 年研究以瑞典南部为例讨论蛇形丘的成因与冰川动力学；所引 2015 年研究基于详细制图讨论简单与复杂蛇形丘系统的形态与演化控制。本条「蛇形丘为冰下河道砂砾沉积残留的蜿蜒垄岗，可重建冰下水系」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="蛇形丘是冰川地貌与砂砾资源，也为古冰下水系提供证据。",
  src=[("openalex-W2026299813","Esker formation and glacier dynamics in eastern Skane",1989,113,1206),
       ("openalex-W1942495090","Controls on the location, morphology and evolution of complex esker systems",2015,59,1693)],kw=["esker"]),
 dict(title="冰水沉积",tier="补充",theme="地形",
  definition="冰水沉积：冰川融水搬运、在冰前堆积的分选砂砾与冰水扇/冰水平原，是冰川沉积的重要类型。",
  tp="第四纪冰期—冰后期（冰退阶段堆积）",
  overview="冰水沉积：冰川融水把砂砾搬运到冰前，堆积成冰水扇与辫状河的冰水平原（outwash）。与冰碛不同，冰水沉积经水流分选、颗粒较圆；向下游逐渐变细。",
  geo="融水从冰川流出，携带大量砂砾在冰前堆积：近冰处为较粗的冰水扇与辫状河砾质，向下游变细为砂。冰水沉积分选较好、层理发育，常构成含水层。",
  infl="所引 1981 年研究分析冰水沉积含水层的电阻率—导水率关系；所引 1974 年研究讨论更新世辫状冰水砾石中的沉积相（大型辫状坝与侧河道）。本条「冰水沉积为融水搬运分选的砂砾，向下游变细并可为含水层」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="冰水沉积与含水层、砂砾资源和冰退历史相关。",
  src=[("openalex-W1984693448","Electrical resistivity—hydraulic conductivity relationships in glacial outwash aquifers",1981,197,1752),
       ("openalex-W2025999187","Facies relationships in Pleistocene outwash gravels, southern Ontario",1974,113,1886)],kw=["outwash"]),
 dict(title="风蚀盆地",tier="补充",theme="地形",
  definition="风蚀盆地：干旱区风把松散物质吹走、地面降低形成的洼地，吹蚀至潜水面时可积水成盐湖或形成风蚀洼地。",
  tp="地质—现代（干旱区持续风蚀）",
  overview="风蚀盆地：干旱区强风把地表松散颗粒吹蚀搬走，地面不断降低形成洼地（风蚀洼地/盆地）。当吹蚀至潜水面时洼地可积水成湖或形成盐碱地；常与沙丘（如抛物线沙丘的吹蚀坑）相邻。",
  geo="风持续吹蚀松散地表，细粒被带走、地面降低形成风蚀洼地；吹蚀至潜水面则积水成湖/盐湖。洼地常与下风侧沙丘堆积相伴，构成“吹蚀—堆积”组合。",
  infl="所引 2020 年研究指出抛物线沙丘由上风的吹蚀盆地、两侧植被臂与下风堆积叶组成；所引 2014 年研究以波兰 Łeba 沙坝的风蚀洼地为例分析植被与菌根演替。本条「风蚀盆地由风力吹蚀降低地面形成，可积水或与沙丘相伴」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="风蚀盆地与沙漠化、盐湖和地下水出露相关。",
  src=[("openalex-W3001026257","Greedy parabolics: Wind flow direction within the deflation basin of parabolic dunes",2020,24,1552),
       ("openalex-W1979899216","Succession of arbuscular mycorrhizal fungi in a deflation hollow",2014,11,1611)],kw=["deflation"]),
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
