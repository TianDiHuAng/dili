# -*- coding: utf-8 -*-
"""第16轮缺口发现：B1(D044探测)、B6(未使用来源)、B5、B7、B2、B3、B4。"""
import json,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));es=cov["entries"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
all_es=[e for d in docs.values() for e in d["entries"]];ids={e["id"] for e in all_es}
gaps={}
gaps["B1_d044_probe"]={"candidates":20,"usable":1,
 "note":"按 D044（正文≥8000字节、命中≥5、剔除 chrome）探测 20 个路径，仅 Livius『Cyrus the Great』可用（body 9220/hits 45）；NPS/USGS/FAO/GBRMPA 多数 403/404/0 连接",
 "count":1}
used=set()
for e in all_es: used.update(e.get("sources",[]))
src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
unused=[s["id"] for s in src if s["verified"] and s["id"] not in used]
gaps["B6_unused_sources"]={"count":len(unused),"ids":unused[:12]}
dangling=[]
for e in all_es:
 for r in e.get("related",[]):
  if r not in ids: dangling.append(f"{e['id']}->{r}")
gaps["B3_dangling"]=dangling
NAMES={"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
blanks=[]
for u,c in cov.get("matrix",{}).items():
 for t in ("地形","气候","农业","贸易","政权更替","区域"):
  if c.get(t,0)==0: blanks.append(f"{NAMES[u]}×{t}")
gaps["B2_matrix"]={"blanks":blanks}
gaps["B5_pending"]={"total":sum(1 for e in es if e["pending_count"]>0)}
gaps["B7_depth"]={"core_l1":sum(1 for e in es if e["tier"]=="核心" and e["level"]=="L1"),
 "important_l1":sum(1 for e in es if e["tier"]=="重要" and e["level"]=="L1"),
 "legacy_l2":cov.get("d041_legacy_count",0)}
json.dump({"round":16,"gaps":gaps},open(os.path.join(ROOT,"reports","gap_round16.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B1可用",gaps["B1_d044_probe"]["usable"],"B6未用来源",len(unused),"B3悬空",len(dangling),
      "B5",gaps["B5_pending"]["total"],"核心L1",gaps["B7_depth"]["core_l1"],
      "重要L1",gaps["B7_depth"]["important_l1"],"遗产L2",gaps["B7_depth"]["legacy_l2"],"矩阵空白",len(blanks))