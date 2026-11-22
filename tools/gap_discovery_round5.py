# -*- coding: utf-8 -*-
"""第5轮缺口发现：B5 待核实、B7 深度、B2 矩阵、B4 读者问题、B1 新来源探测。"""
import json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
es=cov["entries"]
gaps={}
gaps["B5_pending"]={"total":sum(1 for e in es if e["pending_count"]>0)}
gaps["B7_depth"]={"core_l1":[e["id"] for e in es if e["tier"]=="核心" and e["level"]=="L1"],
                  "important_l1":sum(1 for e in es if e["tier"]=="重要" and e["level"]=="L1")}
sparse=[];blanks=[]
NAMES={"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
for u,c in cov.get("matrix",{}).items():
    for t in ("地形","气候","农业","贸易","政权更替","区域"):
        n=c.get(t,0)
        if n==0: blanks.append(f"{NAMES[u]}×{t}")
        elif n<=2: sparse.append(f"{NAMES[u]}×{t}")
gaps["B2_matrix"]={"blanks":blanks,"sparse":sparse}
gaps["B4_reader"]={"remaining":["地图投影","争议边界处理原则"],"count":2}
gaps["B1_source_probe"]={"tried":["Met Museum Heilbrunn","Khan Academy","UNESCO WHC","World History Encyclopedia","OpenLearn"],
 "result":"Met 连接失败；Khan/whc/WHE/OpenLearn 返回 200 挑战页或 403，未取得可核验专题标题",
 "count":5}
json.dump({"round":5,"gaps":gaps},open(os.path.join(ROOT,"reports","gap_round5.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B5",gaps["B5_pending"]["total"],"B7核心L1",len(gaps["B7_depth"]["core_l1"]),"重要L1",gaps["B7_depth"]["important_l1"],
      "B2稀疏",len(sparse),"B4缺口",2,"B1探测失败",5)
