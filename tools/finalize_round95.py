# -*- coding: utf-8 -*-
"""第95轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=95;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":4,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"G1 全部4条","sample_audit":"4/4命中0%失败；4条登记（Polis被引494）",
 "note":f"G1 4→0、C 4→0；G3 60→{gd['G3']}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
sat["milestones"]=sat.get("milestones",[])
sat["milestones"].append({"round":ROUND,"event":"G1=0、C=0（D152 判据收敛并完成全量复核后重算；与第85轮的假清零不同）"})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G1 与 C 级清零（重建后）**）","",
 "## 1. 补上 G1 的 4 条","",
 "| 条目 | 新强来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| **古希腊城邦** | Polis: An Introduction to the Ancient Greek City-State (2006) | **494** | 867 |",
 "| 南锥体 | The Southern Cone Model (2004) | **79** | 792 |",
 "| 古埃及古王国 | Territorial Appropriation during the Old Kingdom (2007) | 9 | 944 |",
 "| 苏美尔城邦 | The Sumerian City-state (1997) | 0 | 1,053 |","",
 "**古希腊城邦那条被引 494**——是本轮质量最高的一条，摘要直接给出「两种国家形态：内含若干城市的大型国家 vs 由城邦构成的区域」，与条目的政体叙述完全对位。",
 "**苏美尔城邦**的摘要写明「迄今最早明确证实的国家约在前 3200 年出现于尼罗河谷与南美索不达米亚」，并解释「明确」是因为这两地发明了文字——正是本条要的机制。",
 "**南锥体**那条是政治经济学研究，落点句已注明「该文是政治经济学研究，不涉本条的温带气候与地形叙述」。","",
 "## 2. 一个必须说清的差别","",
 "第85轮我也写过「G1 清零」，第94轮证明那是假的（`for…break` 让 4 条降级记录被忽略）。",
 "**这次不同**：清零是在 D152 修正**之后**重算的，而且 A 级全量复核（191 条）已完成。按 D153，这才能写入 `milestones`，并已注明「与第85轮的假清零不同」。",
 "但仍有保留：**这是「按当前判据」的结果**。若日后判据再修，可能又会推翻——所以 SATURATION 里保留了两条里程碑记录，不删除旧的。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / **C {evs['C']}** / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：**G1={gd['G1']}** / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| **每个条目都有强来源（G1=0）** | **已达成（D152 后重算）** |",
 "| 判据单一实现 | 已达成（四次收敛） |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 243/243 已扫描 |","",
 "## 4. 下一阶段的重心","",
 "现在每个条目都有**至少一个**强来源，但 **62 条只有 1 个**（G3a 45 + G3b 17）。",
 "这是本项目最后一类实质缺口：**「有一条对位文献」与「有两条可互证」之间**。",
 "其中 G3a 的 45 条已有侧面/弱来源可补，G3b 的 17 条（含 3 条已判无解）需要真正对位的整体研究。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} C={evs['C']} G1={gd['G1']} G3={gd['G3']}")