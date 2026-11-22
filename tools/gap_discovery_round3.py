# -*- coding: utf-8 -*-
"""第3轮缺口发现：B1 权威大纲、B6 近期动态、B2 矩阵、B5 待核实、B7 深度。"""
import json, os

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
es=cov["entries"]
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
titles={e["title"] for u in UNITS for e in json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8"))["entries"]}
gaps={}

# B1：OpenStax 开放教材目录（前端渲染，静态页仅核到站点标题）+ AAG 学科页面
b1_expected=["地理信息系统","人口地理","城市地理"]
b1_missing=[x for x in b1_expected if x not in titles]
gaps["B1_outline"]={"sources":["openstax-intro-geo","openstax-human-geo","s075-aag-org"],
                    "missing_topics":b1_missing,"count":len(b1_missing)}

# B6：近12个月 NOAA / NASA 页面
b6_expected=["植物物候变化","北极火情变化","松岛冰川退缩"]
b6_missing=[x for x in b6_expected if x not in titles]
gaps["B6_recent"]={"sources":["noaa-phenology","nasa-arctic-fire","nasa-pine-island"],
                   "missing_topics":b6_missing,"count":len(b6_missing)}

# B2：稀疏格子
sparse=[]; blanks=[]
for u,c in cov.get("matrix",{}).items():
    for t in ["地形","气候","农业","贸易","政权更替","区域"]:
        n=c.get(t,0)
        if n==0: blanks.append(f"{u}×{t}")
        elif n<=2: sparse.append(f"{u}×{t}")
gaps["B2_matrix"]={"blanks":blanks,"sparse":sparse}

# B5：待核实
gaps["B5_pending"]={"total":sum(1 for e in es if e["pending_count"]>0)}

# B7：重要 L1
gaps["B7_depth"]={"important_l1":sum(1 for e in es if e["tier"]=="重要" and e["level"]=="L1"),
                  "core_l1":sum(1 for e in es if e["tier"]=="核心" and e["level"]=="L1")}

out=os.path.join(ROOT,"reports","gap_round3.json")
json.dump({"round":3,"gaps":gaps},open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B1缺口",len(b1_missing),"B6缺口",len(b6_missing),"矩阵空白",len(blanks),"稀疏",len(sparse),
      "待核实",gaps["B5_pending"]["total"],"重要L1",gaps["B7_depth"]["important_l1"])
print("报告",out)
