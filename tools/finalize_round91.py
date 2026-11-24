# -*- coding: utf-8 -*-
"""第91轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=91;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"A级抽样12条","sample_audit":"12条又发现2处虚高（城市化←气候页错挂、埃及新王国←双耳瓶）",
 "note":f"抽样复核：A 185→{evs['A']}、D 13→{evs['D']}、G3 45→{gd['G3']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=2
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**A 级抽样复核：12 条又查出 2 处**）","",
 "## 1. 继续抽样：上轮 8 条查出 2 处，这轮 12 条又查出 2 处","",
 "| 条目 | 被当作强来源的页面 | 问题 |","|---|---|---|",
 "| **城市化水平** | 《**Climate Change** \\| Our World in Data》 | **主题是气候变化，与城市化无关**——明显错挂 |",
 "| 古埃及新王国 | 《**Amphorae** in New Kingdom Egypt》 | 研究**双耳陶瓶**（器物类型学），不支撑「以文书与官僚体系治理」 |","",
 "## 2. 第一条更值得说","",
 "《Urbanization | OWID》（39,569 字符）本身是极好的来源。问题在于**第二个来源挂错了**——挂的是同一机构的《Climate Change》页（7,460 字符）。",
 "两页都是 OWID、都是长文、都过 `has_content` 门槛，**机器上完全合规**，但内容风马牛不相及。",
 "这种形态我该记住：**它看起来像是在「凑第二个强来源以达 A 级」**。不是有意造假，但结果一样——A 级里混进了一个不相关的页。",
 "移除后，本条自然落回 **D 级**（1 个机构长文 + 数据端点）——**这恰恰是它的正确形态**：城市化水平本就是指标解读类条目。","",
 "## 3. 修正结果","",
 "| 指标 | 修正前 | 修正后 |","|---|---|---|",
 f"| A 级 | 185 | **{evs['A']}** |",
 f"| D 级 | 13 | **{evs['D']}** |",
 f"| G3 | 45 | **{gd['G3']}** |","",
 "## 4. 两轮抽样的合计","",
 "| 轮次 | 抽样数 | 发现问题 | 比例 |","|---|---|---|---|",
 "| 第90轮 | 8 | 2 | 25% |",
 "| 第91轮 | 12 | 2 | 17% |",
 "| **合计** | **20** | **4** | **20%** |","",
 "**20 条里 4 条有问题。** 样本小，但这个比例足以说明：**A 级 183 条里可能还有类似虚高**。",
 "接下来应当把「A 级全量复核」当成正式任务，而不是抽样。185 条 × 每个来源看一眼，是能做完的。","",
 "## 5. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / **D {evs['D']}**",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |",
 "| 判据单一实现（D146 后） | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| **A 级来源真实对位** | **部分达成（20 抽 4 错，需全量复核）** |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 70/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} D={evs['D']} G3={gd['G3']}")