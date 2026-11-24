# -*- coding: utf-8 -*-
"""第89轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=89;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":3,"fixes":2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":2,"sample_rate":"3条重要级新尝试 + G3a 4条说明","sample_audit":"3/3命中0%失败；登记2条（吠陀/马来群岛）；明清史学史不采用",
 "note":f"补2条→G3 16→{gd['G3']}；重要G3b 10→{sp['G3b']['tiers'].get('重要')}；A{evs['A']}；澄清隋唐G1清零≠无缺口"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=2
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：17 → "+str(gd["G3"])+"**）","",
 "## 1. 先澄清一处此前的表述","",
 "第85轮我写「**G1 清零**」，容易读成「隋唐的问题解决了」。本轮核对：",
 "隋唐的 sources 只有 **1 个** openalex 来源（《State Strengthening in the Tang Dynasty》，strong）。",
 "**G1 清零的含义是「每条都有强来源」（C 级归零），不是「每条都有 ≥2 内容源」。隋唐仍在 G3 里。**",
 "这两个指标是分开的，此前没写清。","",
 "## 2. 登记 2 条","",
 "| 条目 | 来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 马来群岛 | Southeast Asian Early Maritime **Silk Road** Trading Polities (2021) | 2 | — |",
 "| 吠陀时代 | The Vedic Tribes (2024) | 0 | — |","",
 "**吠陀那条有一处需谨慎**：该文把「吠陀部落进入印度」定在**公元前二世纪前半**，与传统断代（约前1500–前500）不符。本条的落点句已写明「**不采用其年代表述**」，只取其「部落社会与战争交替」的社会描述。","",
 "## 3. 一条不采用","",
 "**明清** ←《Changes over Time in Qing History: The Importance of Context》(2016, Paul Cohen)——是**清史研究的史学方法论**（强调语境），史学史侧面。","",
 "## 4. G3a 4 条已按 D140 写明","",
 "宋代、突厥、马丘比丘、教育机会地域差异——这 4 条都有 1 个整体性来源 + 1–2 个弱/侧面来源，已在条目页写明「按 D140 归入 G3a」。",
 "**它们不会被算作「有第二内容源」**，但读者能看到「另有一篇侧面文献，它只研究什么」。","",
 "## 5. R20 第六次逼我补别名","",
 "马来群岛的来源标题用 **SOUTHEAST ASIAN**（不是 MALAY / ARCHIPELAGO）→ 对象词补 `southeast asia`、`southeast asian`、`nusantara`。",
 "前五次：indus→harappan、andes→andean、nazca→nasca、conquest→maghrib、zone→biome。","",
 "## 6. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}**（重要 {sp['G3b']['tiers'].get('重要')} / 补充 {sp['G3b']['tiers'].get('补充')}） / G4=243",
 "- 无解清单（D145）：笈多王朝、巴西高原、拉普拉塔平原","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | **已达成**（≠ 每条都有 2 源） |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | 已落地，本轮 0% 失败 |",
 "| 重复命中即停止重试（D145） | 已建立，3 条在册 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，含 3 条无解） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} 重要={sp['G3b']['tiers'].get('重要')}")