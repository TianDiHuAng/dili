# -*- coding: utf-8 -*-
"""第77轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=77;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"—","sample_audit":"G3 拆分为 G3a/G3b；发现 G3a 仅 2 条、G3b 67 条",
 "note":f"结构性改进：G3a={gd.get('G3a')}/G3b={gd.get('G3b')}；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=2
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3 拆分：G3a / G3b**）","",
 "## 1. 一个出乎意料的发现","",
 "上轮我预判「剩下的条目多是文献只研究其侧面，可考虑接受侧面文献作补充源」。本轮把 G3（仅 1 个内容源）拆成两类验证这个预判：","",
 "| 类别 | 定义 | 条数 |","|---|---|---|",
 f"| **G3a** | 已有侧面/弱来源**可作补充** | **{sp['G3a']['count']}**（仅突厥、马丘比丘） |",
 f"| **G3b** | **无任何其他来源** | **{sp['G3b']['count']}**（核心 5 / 重要 26 / 补充 36） |","",
 "**预判错了**：不是「一半有侧面文献可用」，而是 **69 条里只有 2 条**。",
 "那 67 条 G3b 的实情是：只有 1 个 strong 内容源 + 一批别名页 + 数据端点。**它们不是「缺整体研究」，是「连侧面向来源都未登记」**——我检索时命中的侧面文献，大多因不撑整条而被我判退，没留在这里。","",
 "## 2. 处置：两类分开","",
 "| 类别 | 处置 |","|---|---|",
 "| G3a | 把侧面向文献登记为**补充源**，正文限定其范围（D140） |",
 "| G3b | 只能继续检索找对位文献，或承认无解 |","",
 "已为突厥、马丘比丘两条在条目页写明「本条另有侧面向文献（已降旁证），按 D140 归入 G3a」。","",
 "## 3. 缺口现状","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| G1 | 无强来源 | {gd['G1']} |",
 f"| G2 | 检索确认无主来源 | {gd['G2']} |",
 f"| **G3a** | 仅 1 源但有侧面可补 | **{sp['G3a']['count']}** |",
 f"| **G3b** | 仅 1 源且无其他来源 | **{sp['G3b']['count']}** |",
 "| G4 | 语义对题未机器校验 | 243（已扫描 50 条） |","",
 "## 4. 口径（tools/assess.py）","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：**{o1}**；0 个：**{z0}**","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现（D138） | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 f"| 每个条目都有强来源（G1=0） | 未达成（{gd['G1']} 条） |",
 f"| 每条都有 ≥2 内容源 | 未达成（{o1+z0} 条不足，其中 {sp['G3b']['count']} 条无任何第二来源） |",
 "| G4 语义对题 | 50/243 已扫描 |","",
 "## 5. 这轮的意义","",
 "拆分没有减少缺口，反而把问题的性质说清楚了：**67 条是「只有一个来源」的硬缺口，不是「差一口气」**。",
 "此前混在一起时，我容易用「补侧面文献」自我安慰；拆开后才知道，那 67 条需要的是**一篇真正对位的整体研究**——而这在现有文献分布下，有些条目可能永远等不到。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; G3a={sp['G3a']['count']} G3b={sp['G3b']['count']} ge2={g2} one={o1}")