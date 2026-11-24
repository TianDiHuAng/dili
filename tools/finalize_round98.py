# -*- coding: utf-8 -*-
"""第98轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=98;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":11,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":11,"sample_rate":"G3a重要剩余12条","sample_audit":"12/12命中1%失败；登记11条（阿塔卡马505/格陵兰239/莱茵194）；大自流盆地←南非Uitenhage碰撞",
 "note":f"补11条→G3 48→{gd['G3']}、重要G3a 15→{sp['G3a']['tiers'].get('重要')}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=11
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：48 → "+str(gd["G3"])+"**）","",
 "## 1. 本轮登记 11 条，是本项目单轮最多","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| **阿塔卡马沙漠** | Oligocene–Miocene age of aridity in the Atacama (2005) | **505** | 751 |",
 "| **格陵兰岛** | Greenland ice sheet hydrology: A review (2013) | **239** | 1,671 |",
 "| **莱茵河** | Middle and late Holocene **avulsion** history of the River Rhine (1994) | **194** | 1,095 |",
 "| 多瑙河 | Hydrology and floodplain ecological processes (1999) | 55 | 781 |",
 "| 落基山脉 | Large-scale geomorphology and fission-track (1998) | 39 | 3,923 |",
 "| 维京时代 | Viking Expansion Northwards (1995) | 18 | 1,372 |",
 "| 新西兰南岛 | Stratigraphy and Paleoecology, South Island (1975) | 15 | 1,004 |",
 "| 马丘比丘 | **Inca Foundations**, Site Preparation, and Drainage (2012) | 5 | 922 |",
 "| 大堡礁 | Taxonomy and ecology of non-geniculate corals (2002) | 2 | 5,705 |",
 "| 巴尔干半岛 | The Balkans: History, Religion and Society (2024) | 0 | **7,541** |",
 "| **元代** | The **Mongol Yuan Dynasty** in China (2023) | 0 | 1,346 |","",
 "**元代终于找到了对位的**——此前命中「人民币汇率」（Yuan 歧义）。这次的《The Mongol Yuan Dynasty in China》摘要讨论蒙古征服的影响、多语言治理、族群文化差异，正是本条要的。","",
 "## 2. 一条很硬的对象碰撞","",
 "**大自流盆地** ←《The hydrogeology of the **Uitenhage** Artesian Basin》(2001, 被引 37)。",
 "原文摘要写明：「The Uitenhage Artesian Basin (UAB) lies in the **Eastern Cape** and is **South Africa's** most important artesian groundwater basin」。",
 "澳大利亚的大自流盆地（Great Artesian Basin）与南非的 Uitenhage 自流盆地**完全不是同一个盆地**——只是都叫「artesian basin」。",
 "这已是**第五种同名碰撞**（前四种：Songhai 养鱼、Great Lakes 水泥、Dead Sea rift、Yuan 人民币）。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3a={sp['G3a']['count']}**（核心 {sp['G3a']['tiers'].get('核心')} / 重要 {sp['G3a']['tiers'].get('重要')} / 补充 {sp['G3a']['tiers'].get('补充')}） / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 判据单一实现 | 已达成（四次收敛） |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，核心 {sp['G3a']['tiers'].get('核心')+sp['G3b']['tiers'].get('核心')}） |",
 "| G4 语义对题 | 243/243 已扫描 |","",
 "## 4. 进度","",
 "| 轮 | G3 | A |","|---|---|---|",
 "| 95（G1 清零） | 62 | 159 |",
 "| 96 | 56 | 165 |",
 "| 97 | 48 | 173 |",
 "| **98** | **" + str(gd["G3"]) + "** | **" + str(evs["A"]) + "** |","",
 "**三轮回补 25 条**，且**没有出现新的虚高**——这与前几轮不同，因为判据已经收敛。",
 "剩余 37 条里：G3a 20（核心3/重要4/补充13）、G3b 17（核心3/重要10/补充4）。**核心共 6 条**。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")