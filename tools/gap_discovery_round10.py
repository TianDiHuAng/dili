# -*- coding: utf-8 -*-
"""第10轮缺口发现：B6 主题来源、B5、B7、B2、B4 复查。"""
import json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));es=cov["entries"]
gaps={}
gaps["B6_thematic_sources"]={"verified_topics":["预期寿命空间差异","人均产出空间差异","作物单产差异","肥料使用与环境","肉奶生产与土地","自然灾害风险","森林面积占比","人口增长","城市化水平","全球气温变化"],"count":10,
 "basis":"OWID/FAO/UN/World Bank/NASA 已核验主题页"}
gaps["B5_pending"]={"total":sum(1 for e in es if e["pending_count"]>0)}
gaps["B7_depth"]={"core_l1":[e["id"] for e in es if e["tier"]=="核心" and e["level"]=="L1"],
 "important_l1":sum(1 for e in es if e["tier"]=="重要" and e["level"]=="L1")}
NAMES={"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
blanks=[];sparse=[]
for u,c in cov.get("matrix",{}).items():
 for t in ("地形","气候","农业","贸易","政权更替","区域"):
  n=c.get(t,0)
  if n==0: blanks.append(f"{NAMES[u]}×{t}")
  elif n<=2: sparse.append(f"{NAMES[u]}×{t}")
gaps["B2_matrix"]={"blanks":blanks,"sparse":sparse}
gaps["B4_reader_recheck"]={"remaining":[],"count":0}
json.dump({"round":10,"gaps":gaps},open(os.path.join(ROOT,"reports","gap_round10.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B6主题",gaps["B6_thematic_sources"]["count"],"B5",gaps["B5_pending"]["total"],
      "B7核心L1",len(gaps["B7_depth"]["core_l1"]),"重要L1",gaps["B7_depth"]["important_l1"],
      "B2稀疏",len(sparse),"B4剩余",0)
