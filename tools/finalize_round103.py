# -*- coding: utf-8 -*-
"""第103轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=103;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":7,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"G3b重要7条（跳过3无解）","sample_audit":"7/7命中2%失败；登记4条（明清军制/威尼斯马赛克/ATS/山地梯田）；3条碰撞",
 "note":f"补4条→G3 20→{gd['G3']}、G3b重要 10→{sp['G3b']['tiers'].get('重要')}；A{evs['A']}；一致性0问题"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：20 → "+str(gd["G3"])+"**）","",
 "## 1. 按 D156 先看已有来源，再找互补的","",
 "这一步很关键——7 条的现有强来源分别是「佛山镇个案」「土壤有机碳」「降水分布」这类**局部/侧面**研究，所以第二来源要找**国家层面或另一侧面**的。","",
 "| 条目 | 已有强源（局部/侧面） | 新补（互补） | 被引 |","|---|---|---|---|",
 "| 明清 | What Made **Foshan** a Town?（佛山镇个案） | **清代绿营改革中的国家与地方社会** | 0（摘要936） |",
 "| 威尼斯 | International Trade and Institutional Change | **圣马可马赛克与海上帝国**的意识形态 | 0（摘要1281） |",
 "| 南极条约体系 | International law, climate change and the Antarctic | **Antarctic Treaty System 的发展** | **38** |",
 "| 山地农业 | Soil organic carbon fractions | **Mountain Terraces**（山地梯田） | **16** |","",
 "## 2. 三条碰撞，其中一条是最「隐形」的","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| **大分水岭** | 《The **great divide**: population comparison using 3D/2D geometric morphometrics》 | **`great divide` 是隐喻**——论文是几何形态测量学的种群比较，与山脉无关 |",
 "| 隋唐 | Pirates and Publishers: A Social History of **Copyright in Modern China** | 1890s–1950s 中国版权史 |",
 "| 冲积平原 | Walls Formation, Western **Shetland** | 设得兰群岛的一处局部泥盆纪层序 |","",
 "**大分水岭那条最难发现**：它的标题确实含 `great divide` 三个词，但要读摘要才知道那是个比喻（原文说的是「澳大利亚陆生物种的地理分布」——连澳大利亚都对得上，只是学科完全不同）。",
 "这已经是**第六种同名/近名碰撞**（Songhai 养鱼、Great Lakes 水泥、Dead Sea rift、Yuan 人民币、Uitenhage 盆地、great divide 隐喻）。","",
 "## 3. 口径与验证","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 "- `round100_consist.py`：**6 项交叉一致性 0 问题**",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**（{g2*100//243}%）；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3a={sp['G3a']['count']}** / **G3b={sp['G3b']['count']}** / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 核心条目全部有 ≥2 内容源 | **已达成** |",
 "| 判据单一实现 + 收敛（D155） | **已达成（本轮复验）** |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 243/243 已扫描 |","",
 "## 4. 剩余 16 条","",
 "| 类别 | 条数 | 内容 |","|---|---|---|",
 "| G3a 重要 | **3** | 朝鲜半岛、中南半岛、黎凡特 |",
 "| G3a 补充 | 4 | 古埃及中王国、争议边界处理原则、教育机会地域差异、人文地理学 |",
 "| G3b 重要 | **6** | 笈多（无解）、隋唐、巴西高原（无解）、拉普拉塔（无解）、大分水岭、冲积平原 |",
 "| G3b 补充 | 3 | 非洲大湖、西北海岸、荒漠化 |","",
 "**扣掉 3 条无解，实际在追 13 条。** 距 243 条全达标还差 16 条（6.6%）。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")