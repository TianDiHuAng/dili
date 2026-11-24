# -*- coding: utf-8 -*-
"""第75轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=75;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":9,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":9,"sample_rate":"重要条目首批12条","sample_audit":"9条登记、3条不采用（桑海←鱼养殖项目、萨珊←钱币学、阿拉伯征服←史学史）",
 "note":f"补9条→G3 83→{gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=9
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：83 → "+str(gd["G3"])+"**）","",
 "## 1. 重要条目首批 12 条：登记 9 条","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 埃塞俄比亚高原 | Ethiopian vegetation types, climate and topography (2020) | **281** | — |",
 "| 大津巴布韦 | The Rise and Fall of Zimbabwe (1972) | **114** | — |",
 "| 古埃及新王国 | State Correspondence in the Ancient World (2014) | 24 | — |",
 "| 亚述帝国 | Emblems of Power: Ideology and Identity in L… (2016) | 15 | — |",
 "| 马格里布 | Trade and Religious Boundaries in the Medieval Maghrib (2019) | 4 | 5,197 |",
 "| 古巴比伦 | Foreign Ruling Elites in Traditional State Societies (2014) | 4 | 4,076 |",
 "| 加纳帝国 | Pioneers in Ancient Ghana (2014) | 0 | 858 |",
 "| 斯瓦希里海岸 | The Swahili World (2022) | 0 | **13,723** |",
 "| 帕提亚帝国 | Parthian kingdom – state of Iranians-Zoroastrians (2024) | 0 | 8,926 |","",
 "**中低被引但摘要长**是这批的特点：斯瓦希里那篇摘要 13,723 字符、被引 0；帕提亚 8,926 字符、被引 0。按 D117「被引≥10 **或** 正文≥800」，它们成立。","",
 "## 2. 三条不采用（两条对象碰撞）","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| **桑海帝国** | Assessment of farmers' perception of the effectiveness of **Songhai-Delta fish culture training programme** (2011) | 「Songhai」在此是**现代尼日尔河三角洲的养鱼培训项目名**，与桑海帝国无关 |",
 "| 萨珊波斯 | Are Georgian-Sasanian **Coins** an Indicator of… (2016) | 钱币学，物质文化侧面，不撑国家与行政 |",
 "| 阿拉伯征服北非 | Concepts, conquests, and contexts (2021) | 摩洛哥**民族主义史学**如何叙述征服，史学史侧面 |","",
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
 f"| 每个条目都有强来源（G1=0） | 未达成（{gd['G1']} 条） |",
 f"| 每条都有 ≥2 内容源 | 未达成（{o1+z0} 条不足） |",
 "| G4 语义对题 | 38/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} ge2={g2} one={o1} zero={z0} G3={gd['G3']}")