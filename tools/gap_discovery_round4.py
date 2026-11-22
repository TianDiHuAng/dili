# -*- coding: utf-8 -*-
"""第4轮缺口发现：B3 悬空引用、B4 读者问题、B2 矩阵、B5 待核实、B7 深度。"""
import json, os, re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
all_es=[e for d in docs.values() for e in d["entries"]]
by_id={e["id"]:e for e in all_es}
titles={e["title"] for e in all_es}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
gaps={}

# B3 悬空引用
dangling=[]
for e in all_es:
    for rid in e.get("related",[]):
        if rid not in by_id: dangling.append(f"{e['id']}->{rid}")
text=" ".join(e.get("overview","")+e.get("definition","") for e in all_es)
for nm in re.findall(r"另见[：:]([\u4e00-\u9fff、，, ]+)",text):
    for x in re.split(r"[、，, ]+",nm.strip()):
        if x and x not in titles: dangling.append("另见:"+x)
gaps["B3_dangling"]=dangling

# B4 20个读者问题（初学者/学生/爱好者/从业者各5）
QUESTIONS=[
 ("初学者","为什么河流两岸容易出现文明？",["河流","河谷","冲积"]),
 ("初学者","沙漠为什么不适合大规模农业？",["沙漠","干旱","绿洲"]),
 ("初学者","什么是季风？",["季风"]),
 ("初学者","山脉如何影响降水？",["山脉","雨影","地形"]),
 ("初学者","为什么沿海城市多？",["沿海","港口","海岸"]),
 ("学生","人口地理研究什么？",["人口地理","人口分布"]),
 ("学生","城市地理研究什么？",["城市地理","城市化"]),
 ("学生","地图投影为什么重要？",["地图投影","投影"]),
 ("学生","地理信息系统有什么用？",["地理信息系统"]),
 ("学生","气候带怎么划分？",["气候带"]),
 ("爱好者","丝路上交换了哪些商品？",["丝绸","贸易","香料"]),
 ("爱好者","玛雅城市为什么建在雨林里？",["玛雅","雨林"]),
 ("爱好者","安第斯山地如何种地？",["梯田","垂直农业"]),
 ("爱好者","南极为什么没有国家？",["南极条约","南极洲"]),
 ("爱好者","波利尼西亚人如何跨海航行？",["波利尼西亚","航海"]),
 ("从业者","GIS 标准由谁制定？",["OGC","标准","地理信息系统"]),
 ("从业者","三角洲面临哪些风险？",["三角洲","海平面","沉降"]),
 ("从业者","牧业如何适应干旱区？",["游牧","牧业","干旱"]),
 ("从业者","现状人口数据怎么标注？",["年份","来源","人口"]),
 ("从业者","争议边界该怎么处理？",["争议边界","立场"]),
]
qgap=[]
for persona,q,kws in QUESTIONS:
    hits=[e for e in all_es if any(k in (e["title"]+e.get("overview","")) for k in kws)]
    if not hits: qgap.append({"persona":persona,"question":q,"keywords":kws})
gaps["B4_reader_questions"]={"checked":len(QUESTIONS),"missing":qgap,"count":len(qgap)}

# B2 稀疏
sparse=[];blanks=[]
for u,c in cov.get("matrix",{}).items():
    for t in ["地形","气候","农业","贸易","政权更替","区域"]:
        n=c.get(t,0)
        if n==0: blanks.append(f"{u}×{t}")
        elif n<=2: sparse.append(f"{u}×{t}")
gaps["B2_matrix"]={"blanks":blanks,"sparse":sparse}
gaps["B5_pending"]={"total":sum(1 for e in cov["entries"] if e["pending_count"]>0)}
gaps["B7_depth"]={"core_l1":sum(1 for e in cov["entries"] if e["tier"]=="核心" and e["level"]=="L1"),
                  "important_l1":sum(1 for e in cov["entries"] if e["tier"]=="重要" and e["level"]=="L1")}

json.dump({"round":4,"gaps":gaps},open(os.path.join(ROOT,"reports","gap_round4.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("B3悬空",len(dangling),"B4问题缺口",len(qgap),"B2空白",len(blanks),"稀疏",len(sparse),
      "B5待核实",gaps["B5_pending"]["total"],"B7核心L1",gaps["B7_depth"]["core_l1"],"重要L1",gaps["B7_depth"]["important_l1"])
for x in qgap: print("  Q:",x["persona"],x["question"])
