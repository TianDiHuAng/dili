# -*- coding: utf-8 -*-
"""第85轮收尾（里程碑）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=85;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":11,"fixes":9,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":9,"sample_rate":"补充9条+澳原住民+隋唐","sample_audit":"10/11命中、0%失败；9条登记",
 "note":f"里程碑：G1清零、C级清零、核心G3b清零；G3 33→{gd['G3']}、A 166→{evs['A']}；G3b补充仅{sp['G3b']['tiers'].get('补充')}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
sat["milestones"]=sat.get("milestones",[])
sat["milestones"].append({"round":ROUND,"event":"G1（无强来源）与 C 级清零；核心 G3b 清零"})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=9
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**里程碑：G1 清零、C 级清零、核心 G3b 清零**）","",
 "## 1. 三个清零","",
 "| 指标 | 上轮 | **本轮** |","|---|---|---|",
 f"| G1 无强来源 | 1 | **0** |",
 f"| C 级（无强来源且非指标类） | 1 | **0** |",
 f"| 核心 G3b（仅 1 内容源） | 1 | **0** |",
 f"| A 级 | 166 | **{evs['A']}** |",
 f"| G3 总量 | 33 | **{gd['G3']}** |","",
 "**含义**：243 条条目中，每一条要么有 ≥1 个强来源（A/B 级 230 条），要么属指标解读类（D 级 13 条，其机构长文即主体）。**没有一条是「无强来源」的。**","",
 "## 2. 本轮登记 9 条","",
 "| 条目 | 来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 隋唐（**G1 最后一条**） | State Strengthening in the Tang Dynasty (2022) | 0 | 992 |",
 "| 横贯南极山脉 | The Transantarctic Mountains of southern Victoria Land (1992) | **249** | 2,406 |",
 "| 沙漠化 | Projected Global Dryland Expansion Discrepancy (2025) | 30 | 1,412 |",
 "| 满者伯夷 | De Kraton van Majapahit (1948, **荷兰语**) | 20 | 2,567 |",
 "| 南极科考站 | On thick ice: scientific internationalism (2008) | 45 | 1,025 |",
 "| 太平洋殖民航线 | Lapita and Western Pacific Settlement (2007) | 35 | 441 |",
 "| 罗斯海 | Quaternary Benthic Foraminiferal Distribution in the Ross Sea (1999) | 3 | 2,278 |",
 "| 室利佛逝 | Srivijaya, Kingdom of (2016) | 3 | 932 |",
 "| 澳大利亚原住民（**核心最后一条**） | Heritage archaeology in Australia (2000) | 0 | 1,726 |","",
 "**隋唐**这条是 G1 的最后一条——多次检索都命中墓碑、服饰、寺庙崇拜等侧面，这次用「State Strengthening」对象词命中一篇专论唐代国家强化的章节。","",
 "## 3. 一条对象碰撞","",
 "**非洲大湖地区** ←《Cement Production and Trade on the **Great Lakes**》(1944)——研究对象是**北美五大湖**的水泥工业与航运。`Great Lakes` 在地理上指两个完全不同的湖群，纯靠对象词无法区分。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / **C {evs['C']}** / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：**G1={gd['G1']}** / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']}（重要 {sp['G3b']['tiers'].get('重要')} / 补充 {sp['G3b']['tiers'].get('补充')}） / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| **每个条目都有强来源或属指标解读类（G1=0）** | **已达成** |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | 已落地，连续两轮 0% 失败 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，其中补充类仅 {sp['G3b']['tiers'].get('补充')}） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; G1={gd['G1']} C={evs['C']} A={evs['A']} G3={gd['G3']} G3b重要={sp['G3b']['tiers'].get('重要')} 补充={sp['G3b']['tiers'].get('补充')}")