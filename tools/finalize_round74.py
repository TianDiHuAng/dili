# -*- coding: utf-8 -*-
"""第74轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=74;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":8,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"第二批8条核心G3全查","sample_audit":"6条登记（安第斯2762/澳大利亚941/玛雅191）、2条不采用",
 "note":f"补6条第二内容源→G3 88→{gd['G3']}、G1 4→{gd['G1']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：88 → "+str(gd["G3"])+"，G1：4 → "+str(gd["G1"])+"**）","",
 "## 1. 第二批核心 G3：登记 6 条","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 安第斯山脉 | Amazonia Through Time: **Andean Uplift**, Climate Change, Landscape Evolution (2010) | **2762** | 802 |",
 "| 澳大利亚大陆 | Climate change and Australia: Trends, projections and impacts (2003) | **941** | 3,793 |",
 "| 玛雅文明 | Ancestral Maya Economies in Archaeological Perspective (2010) | 191 | 1,121 |",
 "| 河流三角洲 | High-Resolution Stratigraphy of a Mississippi Subdelta-Lobe (2006) | 23 | 1,150 |",
 "| 大平原 | Ethnicity on the Great Plains (1980) | 12 | — |",
 "| 波利尼西亚 | Micronesian and Polynesian Voyaging: Three Readings (1976) | 5 | 2,690 |","",
 "其中**安第斯**那篇（被引 2762）与**澳大利亚大陆**那篇（941）是本轮质量最高的两条——两篇都直接讨论「隆升如何改变气候与景观」「全澳气候趋势与影响」，与本条 geo 段一一对得上。","",
 "## 2. 两条不采用（如实记录）","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| **印加帝国** | Machu Picchu: Unveiling the Mystery of the Incas (2005) | 对象是**遗址**（皇家庄园），第55轮已判不撑国家的疆域/道路/行政，本轮再次不采用 |",
 "| 澳大利亚原住民 | Reempowering Ourselves: Australian Aboriginal **Women** (2010) | 性别侧面，不撑「适应干旱生态、语言与文化传统」总体 |","",
 "## 3. 口径（tools/assess.py）","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：**{o1}**；0 个：**{z0}**",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3={gd['G3']}** / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现（D138） | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 f"| 每个条目都有强来源（G1=0） | 未达成（{gd['G1']} 条：阿卡德帝国、隋唐、水资源管理） |",
 f"| 每条都有 ≥2 内容源 | 未达成（{o1+z0} 条不足） |",
 "| G4 语义对题 | 38/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} ge2={g2} one={o1} zero={z0} G1={gd['G1']} G3={gd['G3']}")