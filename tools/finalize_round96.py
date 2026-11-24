# -*- coding: utf-8 -*-
"""第96轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=96;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":9,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"核心G3a 9条","sample_audit":"9/9命中3%失败；登记6条（苏美尔244引）；3条不采用",
 "note":f"补6条→G3 62→{gd['G3']}、核心G3a 9→3；A{evs['A']}；R20第7-8次补别名"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：62 → "+str(gd["G3"])+"，核心 G3a 9→3**）","",
 "## 1. 核心 G3a 9 条：登记 6 条","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 苏美尔城邦 | Early Mesopotamian urbanism: a new view (2007) | **244** | 1,067 |",
 "| 撒哈拉沙漠 | The impact of Sahara **desertification** on Arctic cooling (2015) | 21 | 1,150 |",
 "| 汉代 | **War economy** during the Western Han Dynasty (2019) | 1 | 945 |",
 "| 大平原 | The Great Plains: **Agriculture and the Environment** (2001) | 1 | 999 |",
 "| 马里帝国 | The Grand Empires of the **Sahel**: Gold, Trade (2025) | 0 | 935 |",
 "| 南极冰盖 | Present and future **Ross Ice Shelf** dynamics (2023) | 0 | 3,172 |","",
 "**撒哈拉那条是意外的好**：研究的是「撒哈拉沙漠化对全新世北极降温的影响」——正是本条要的「干旱化与全球气候耦合」机制，而不是又一次「20 世纪非洲气候」。",
 "**苏美尔**那条被引 244，是本轮最高。","",
 "## 2. 三条不采用","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| 澳大利亚大陆 | Australian Participation in the **IPCC** | 国际气候治理的政策史 |",
 "| 波利尼西亚 | Southeast **Solomon Islands** in regional perspective | **所罗门群岛属美拉尼西亚**，与波利尼西亚文化圈不同（对象偏差） |",
 "| 长江流域 | Geographic patterns of **industrial water consumption** | 现代工业用水的地理格局 |","",
 "## 3. R20 第七、第八次逼我补别名","",
 "| 条目 | 来源标题实际用词 | 补入 |","|---|---|---|",
 "| 马里帝国 | **SAHEL**（萨赫勒） | `sahel`、`saharan` |",
 "| 苏美尔城邦 | **MESOPOTAMIAN** | `mesopotamia`、`mesopotamian` |","",
 "前六次：indus→harappan、andes→andean、nazca→nasca、conquest→maghrib、zone→biome、malay→southeast asia。",
 "**R20 现在是全项目触发次数最多的规则（8 次）**，每次都在我自以为完成时冒出来——它的价值就在这。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3a={sp['G3a']['count']}**（核心 {sp['G3a']['tiers'].get('核心')}） / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 判据单一实现 | 已达成（四次收敛） |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，核心仅 {sp['G3a']['tiers'].get('核心')+sp['G3b']['tiers'].get('核心')}） |",
 "| G4 语义对题 | 243/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} 核心G3a={sp['G3a']['tiers'].get('核心')}")