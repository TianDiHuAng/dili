# -*- coding: utf-8 -*-
"""第14轮缺口发现：B1 来源适配性复核、B3 悬空、B4 读者问题、B5、B7。"""
import json,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));es=cov["entries"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
all_es=[e for d in docs.values() for e in d["entries"]];ids={e["id"] for e in all_es}
gaps={}

# B1：来源适配性复核——哪些重要L1的自然地理内容可由主题直接对应的已核验来源支撑
gaps["B1_source_fit"]={
 "method":"把 L2 内容窄化为来源可支撑的自然地理/生态/人口部分，政权与年代细节留待专门史料",
 "candidates":[
  ("五大湖",["epa-great-lakes","noaa-glerl"]),
  ("大堡礁",["s050-oceanservice-noaa-gov","s085-unesco-org"]),
  ("格陵兰岛",["s037-science-nasa-gov","s039-climate-nasa-gov"]),
  ("北美冰盖",["s038-earthobservatory-nasa-gov","s043-earthobservatory-nasa-gov"]),
  ("科罗拉多高原",["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"]),
  ("墨西哥湾",["s050-oceanservice-noaa-gov","s048-climate-gov"]),
  ("尼罗河三角洲",["fao-aquastat-basins","s013-fao-org"]),
  ("湄公河三角洲",["fao-aquastat-basins","s013-fao-org"]),
  ("冲积平原",["s015-fao-org","s016-fao-org"]),
  ("山地农业",["s016-fao-org","s083-fao-org"]),
  ("人口迁移",["s004-population-un-org","s023-ourworldindata-org"])],
 "count":11}

# B3 悬空引用
dangling=[]
for e in all_es:
 for rid in e.get("related",[]):
  if rid not in ids: dangling.append(f"{e['id']}->{rid}")
gaps["B3_dangling"]=dangling

# B4 读者问题抽查（新问 10 条）
Q=[("五大湖为什么会形成？",["五大湖","冰盖","冰川"]),
   ("珊瑚礁为什么怕升温？",["大堡礁","珊瑚","海温"]),
   ("格陵兰冰盖和全球海平面有什么关系？",["格陵兰","冰盖","海平面"]),
   ("三角洲为什么会下沉？",["三角洲","沉降","海平面"]),
   ("山地为什么适合梯田？",["山地农业","梯田","冲积"]),
   ("人口为什么跨境迁移？",["人口迁移","迁移"]),
   ("海湾为什么容易有飓风？",["墨西哥湾","飓风","暖湿"]),
   ("高原为什么干旱？",["科罗拉多高原","干旱","雨影"]),
   ("为什么大河流域容易形成平原？",["冲积平原","沉积"]),
   ("冰川地貌有哪些特征？",["冰盖","冰川","冰碛"])]
qgap=[]
for q,kws in Q:
 hits=[e for e in all_es if any(k in (e["title"]+(e.get("overview") or "")) for k in kws)]
 if not hits: qgap.append(q)
gaps["B4_reader_questions"]={"checked":len(Q),"missing":qgap,"count":len(qgap)}

gaps["B5_pending"]={"total":sum(1 for e in es if e["pending_count"]>0)}
gaps["B7_depth"]={"core_l1":[e["id"] for e in es if e["tier"]=="核心" and e["level"]=="L1"],
 "important_l1":sum(1 for e in es if e["tier"]=="重要" and e["level"]=="L1")}
json.dump({"round":14,"gaps":gaps},open(os.path.join(ROOT,"reports","gap_round14.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B1可窄化升级",gaps["B1_source_fit"]["count"],"B3悬空",len(dangling),
      "B4缺口",len(qgap),"B5",gaps["B5_pending"]["total"],
      "B7核心L1",len(gaps["B7_depth"]["core_l1"]),"重要L1",gaps["B7_depth"]["important_l1"])
for q in qgap: print("  Q:",q)