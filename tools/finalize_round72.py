# -*- coding: utf-8 -*-
"""第72轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, level_of, count_entry, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=72;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
es=cov["entries"]
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"—","sample_audit":"D138 单一实现完成：assess.py 被 gaps/levels/check 三处引用",
 "note":f"建立 tools/assess.py 统一判据；check/gaps/levels 全部引用；权威数字 ≥2内容源 {g2}/1个 {o1}/0个 {z0}、层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0,
 "criterion":"tools/assess.py（D138 单一实现）"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**判据单一实现完成**）","",
 "## 1. D138 落地：建立 `tools/assess.py`","",
 "上一轮发现 `hb()`（内容源统计）与层级判定是两套标准，导致数字虚报。本轮把它们抽成**唯一实现**：","",
 "```","tools/assess.py","  ALIAS_PAGES / DATA_PREFIX / BAD_TYPES      常量集中","  has_content(sid, src, entry)               内容源判定","  strength(sid, src, entry)                  层级判定（strong/weak/side/data/alias）","  content_count(entry, sources)               条目内容源数","  level_of(entry, sources)                    A/B/C/D","```","",
 "**`check.py`（R22）、`round62_gaps.py`、`round68_levels.py` 全部改为引用它**——此前三处各写一份，任何一处改动都会造成不一致。","",
 "切换过程中 R22 立刻报出 3 条不一致（印度河文明、水资源管理、水资源供给概览），证明三处确实在算不同的东西；统一后 **0 错误**。","",
 "## 2. 统一后的权威数字","",
 "| 指标 | 数值 |","|---|---|",
 f"| 层级 A / B / C / D | **{evs['A']} / {evs['B']} / {evs['C']} / {evs['D']}** |",
 f"| 内容源 ≥2 | **{g2}** |",
 f"| 内容源 1 个 | **{o1}** |",
 f"| 内容源 0 个 | **{z0}** |",
 f"| G1 无强来源 | **{gd['G1']}** |",
 f"| G3 仅 1 内容源 | **{gd['G3']}** |","",
 f"G1 明细：阿卡德帝国、隋唐、澳大利亚大陆、水资源管理。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| **判据单一实现（D138）** | **已达成** |",
 "| 每个条目都有强来源（G1=0） | 未达成（4 条） |",
 f"| 每条都有 ≥2 内容源 | 未达成（{o1+z0} 条不足） |",
 "| G4 语义对题 | 30/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} B={evs['B']} C={evs['C']} D={evs['D']} ge2={g2} one={o1} zero={z0} G1={gd['G1']} G3={gd['G3']}")