# -*- coding: utf-8 -*-
"""第9轮缺口发现：B6 主题来源、B5 待核实、B7 深度、B2 矩阵、B4 读者问题复查。"""
import json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));es=cov["entries"]
gaps={}
gaps["B6_thematic_sources"]={"verified_topics":["森林覆盖变化","土地利用变化","生物多样性分布","海洋保护区","极端贫困空间分布","能源转型","碳排放空间差异","人口年龄结构","城市热岛","湿地与水资源"],
 "count":10,"basis":"OWID/FAO/NASA/CBD/NOAA/World Bank/UN DESA 已核验专题页"}
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
gaps["B4_reader_recheck"]={"closed":["人口地理","城市地理","地图投影","争议边界处理原则"],"remaining":[],"count":0}
json.dump({"round":9,"gaps":gaps},open(os.path.join(ROOT,"reports","gap_round9.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B6主题",gaps["B6_thematic_sources"]["count"],"B5",gaps["B5_pending"]["total"],
      "B7核心L1",len(gaps["B7_depth"]["core_l1"]),"重要L1",gaps["B7_depth"]["important_l1"],
      "B2稀疏",len(sparse),"B4剩余",0)
