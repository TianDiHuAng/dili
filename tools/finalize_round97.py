# -*- coding: utf-8 -*-
"""第97轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=97;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":8,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":8,"sample_rate":"G3a重要前12条","sample_audit":"12/12命中0%失败；登记8条（拜占庭590引）；元代←人民币汇率碰撞",
 "note":f"补8条→G3 56→{gd['G3']}、重要G3a 23→{sp['G3a']['tiers'].get('重要')}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=8
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：56 → "+str(gd["G3"])+"**）","",
 "## 1. G3a 重要前 12 条：登记 8 条","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| **拜占庭帝国** | A History of the Byzantine State and Society (1997) | **590** | 2,345 |",
 "| 尼罗河三角洲 | Clay Distributions, Grain Sizes, Sediment Transport (2013) | 35 | 2,180 |",
 "| 高卢 | Gaul (1996) | 34 | 910 |",
 "| 宋代 | Schooling, State, and Society in Song and Jin (2023) | 0 | 1,266 |",
 "| 古埃及古王国 | Egyptian Economic History: Locating Power (2014) | 0 | 1,115 |",
 "| 古埃及新王国 | Egypt: 1. Ancient (New Kingdom) (2016) | 1 | 954 |",
 "| 伊比利亚半岛 | The Iberian Peninsula: A Geographical Study (1920) | 1 | 1,259 |",
 "| 突厥 | Relations between Ancient Korea and Turkey（高句丽—突厥汗国接触） (2016) | 1 | 4,145 |","",
 "**拜占庭那条被引 590**，是拜占庭国家与社会的通史，直接对位。",
 "**伊比利亚**那条要特别说明：它是 1920 年**面向五、六年级的地理读本**，年代很早，只用于地形与气候分区的框架性描述——落点句已写明这点。","",
 "## 2. 一条很典型的碰撞：元代 ← 人民币汇率","",
 "**元代** ←《Chinese **Yuan** after Chinese **Exchange Rate** System Reform》(2006, **被引 77**)。",
 "`Yuan` 既是「元代」，也是「人民币」。这篇研究的是 **2005 年汇率改革后的人民币汇率政策**——被引 77、摘要够长、标题含 `Yuan`，**机器全绿**。",
 "这是继「Songhai 养鱼项目」「Great Lakes 水泥」「Dead Sea rift」之后，**第四次纯同名碰撞**。","",
 "## 3. 其余三条不采用","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| 黎凡特 | **Woman's Share** in Neolithic Society | 性别考古侧面 |",
 "| 朝鲜半岛 | Peace Settlement of the Korean Peninsula | 当代和平协议 |",
 "| 中南半岛 | China–Indochina Peninsula **Economic Corridor** | 当代基建与经济走廊 |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3a={sp['G3a']['count']}**（重要 {sp['G3a']['tiers'].get('重要')}） / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 判据单一实现 | 已达成（四次收敛） |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，核心 {sp['G3a']['tiers'].get('核心')+sp['G3b']['tiers'].get('核心')}） |",
 "| G4 语义对题 | 243/243 已扫描 |","",
 "## 5. 四种同名碰撞的清单","",
 "| 条目 | 撞上的东西 |","|---|---|",
 "| 桑海帝国 | **Songhai**-Delta 养鱼培训项目 |",
 "| 非洲大湖地区 | **Great Lakes** 北美五大湖的水泥贸易 |",
 "| 东非大裂谷 | **Dead Sea** rift valley |",
 "| **元代** | **Yuan** = 人民币汇率 |","",
 "四条的共同点：**标题含对象词、数值门槛全过、R20 放行，只有读摘要才看得出**。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} 重要G3a={sp['G3a']['tiers'].get('重要')}")