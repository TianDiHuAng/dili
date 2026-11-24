# -*- coding: utf-8 -*-
"""第101轮收尾（核心缺口清零）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=101;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
nref=sat["evidence"]["sources_referenced"]
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":4,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"4条核心缺口","sample_audit":"4/4有候选0%失败；3+1条登记，核心缺口清零",
 "note":f"核心清零：G3a核心 1→0、G3b核心 3→0；G3 31→{gd['G3']}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
sat["milestones"].append({"round":ROUND,"event":"核心缺口清零（G3a 核心 0 / G3b 核心 0）；剩余 27 条均为重要或补充级"})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**核心缺口清零**）","",
 "## 1. 四条核心全部解决","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| **尼罗河谷** | A Re-Examination of the Evidence for **Agricultural Origins in the Nile Valley** (1971) | **94** | — |",
 "| 古埃及早王朝 | Early Dynastic **Sealing Practices** as a Reflection of State Formation (2018) | 3 | 994 |",
 "| **黄河流域** | Evolution of agricultural civilization in the **Yellow River Basin** (2020) | 7 | 1,789 |",
 "| 长江流域 | Starch granule analysis…Neolithic sites in the **Yangtze River Basin** (2021) | 3 | 816 |","",
 "**G3a 核心：1 → 0；G3b 核心：3 → 0。核心缺口清零。**","",
 "## 2. 一个过程失误值得记","",
 "古埃及早王朝我一开始去「找」《EARLY DYNASTIC EGYPT》（462引）——**结果它本来就在条目里**。",
 "那条的缺口不是缺这篇，而是**缺第二个独立来源**（Livius 首页被 D149 判为 weak，机构页不算）。",
 "所以真正补上的是《Sealing Practices》（3引）——一篇讲**印章实践如何反映国家形成**的论文，主题精准。",
 "**教训：检索前应先看条目已有来源，确认缺的到底是「哪一篇」还是「第二个独立来源」**。这轮多做了一次无效检索。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**（{g2*100//243}%）；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3a={sp['G3a']['count']}**（核心 **0**） / **G3b={sp['G3b']['count']}**（核心 **0**） / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| **核心条目全部有 ≥2 内容源** | **已达成（本轮清零）** |",
 "| 判据单一实现 + 收敛（D155） | 已达成 |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，**全部为重要或补充级**） |",
 "| G4 语义对题 | 243/243 已扫描 |","",
 "## 4. 剩余 27 条的构成","",
 "| 类别 | 条数 | 示例 |","|---|---|---|",
 "| G3a 重要 | 3 | 朝鲜半岛、中南半岛、黎凡特 |",
 "| G3a 补充 | 10 | 多为指标解读类（人口年龄结构、预期寿命、全球人口规模…） |",
 "| G3b 重要 | 10 | 笈多、隋唐、明清、威尼斯、巴西高原、拉普拉塔、大分水岭、南极条约、冲积平原、山地农业 |",
 "| G3b 补充 | 4 | 非洲大湖、西北海岸、荒漠化、卫星遥感 |","",
 "**没有一条是核心。** 这是本项目第一次在「核心」这一级上做到完整。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")