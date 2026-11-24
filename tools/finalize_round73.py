# -*- coding: utf-8 -*-
"""第73轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, level_of, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=73;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":8,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"8条核心G3全查","sample_audit":"6条登记、2条不采用（食肉动物/死海裂谷碰撞）",
 "note":f"补6条第二内容源→G3 93→{gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：93 → "+str(gd["G3"])+"**）","",
 "## 1. 为首批 8 条核心 G3 找第二内容源","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 爱琴海世界 | Modelling maritime interaction in the Aegean Bronze Age (2008) | **251** | 749 |",
 "| 白令陆桥 | The Colonization of Beringia and the Peopling of the New World (1993) | **241** | 742 |",
 "| 罗马帝国 | Market-Days in the Roman Empire (1970) | 198 | 1,995 |",
 "| 两河流域 | Soil Salinity Mapping…in Mesopotamia (2014) | 129 | 1,552 |",
 "| 文艺复兴意大利 | The Economy of Renaissance Italy (2022) | 11 | 1,333 |",
 "| 马里帝国 | Sociological reflections on the empire of Mali (2004) | 9 | 848 |","",
 "**两条须注意限定**：",
 "- **两河流域**：那篇是**现代伊拉克**的土壤盐渍化遥感测绘，不是古代灌溉史——落点句已写明「该文是现代测绘，不作古代灌溉史的定论」。",
 "- **马里帝国**：被引仅 9（<10），但摘要 848 字符 ≥800，按 D117「满足其一」成立。","",
 "## 2. 两条对象碰撞（不采用）","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| 撒哈拉沙漠 | Global warming drives changes in **carnivore communities** (2017) | 主题是食肉动物，与沙漠无关 |",
 "| **东非大裂谷** | …paleohydrology of the **Dead Sea** rift valley (2006) | **死海裂谷**，地名碰撞 |","",
 "## 3. 口径（全部来自 tools/assess.py）","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：**{o1}**；0 个：**{z0}**",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3={gd['G3']}** / G4=243",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现（D138） | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 f"| 每个条目都有强来源（G1=0） | 未达成（{gd['G1']} 条） |",
 f"| 每条都有 ≥2 内容源 | 未达成（{o1+z0} 条不足） |",
 "| G4 语义对题 | 38/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} ge2={g2} one={o1} zero={z0} G3={gd['G3']}")