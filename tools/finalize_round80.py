# -*- coding: utf-8 -*-
"""第80轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=80;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":7,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":7,"sample_rate":"重要条目第三批12条","sample_audit":"7条登记、4条不采用、1条0候选",
 "note":f"补7条→G3 64→{gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=7
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：64 → "+str(gd["G3"])+"**）","",
 "## 1. 重要条目第三批 12 条：登记 7 条","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 特奥蒂瓦坎 | Human Sacrifice, Militarism, and Rulership (2005) | **189** | 1,058 |",
 "| 马其顿与亚历山大 | Alexander the Great and His Empire (2010) | **107** | 1,799 |",
 "| 加勒比海群岛 | In the shadow of the plantation: Caribbean… (2002) | 75 | 1,889 |",
 "| 法兰克王国 | Frankish military duty and the fate of Roman… (2008) | 28 | 982 |",
 "| 十三殖民地 | Colonial America: A History to 1763 (2011) | 27 | 4,323 |",
 "| 奥尔梅克 | Discovering the Olmecs (2014) | 15 | 1,641 |",
 "| 莱茵河 | The Rhine: An Eco-Biography, 1815–2000 (2005) | 1 | 4,440 |","",
 "## 2. 四条不采用（两条是时段/局部错位）","",
 "| 条目 | 候选 | 问题 |","|---|---|---|",
 "| 十字军东征 | Military Orders and **Women of the Nobility** (2023) | 性别侧面 |",
 "| 威尼斯 | Negotiating Transcultural Relations… (2014) | 时段是 **16–17 世纪**，而本条讲威尼斯**鼎盛期 13–15 世纪**（D108 时期错配） |",
 "| 巴西高原 | GIS relief mapping of **central Brazilian highlands** (2020) | 只覆盖一处**喀斯特保护区**（局部） |",
 "| 拉普拉塔平原 | Sustainable intensification of agriculture (2022) | 摘要以泛论开场，无针对潘帕斯的具体结论 |",
 "| 大分水岭 | 本轮 **0 候选** |","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}** / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现 + 经主动审计（D138/D143） | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 f"| 每个条目都有强来源或属 D 级 | 未达成（{gd['G1']} 条：隋唐） |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3b={sp['G3b']['count']}")