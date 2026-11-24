# -*- coding: utf-8 -*-
"""第92轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=92;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":52,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"A级全量复核africa+asia（52条）","sample_audit":"发现AAG首页被12条当强来源、CBD首页4条；另修2处侧面",
 "note":f"D149首页规则：A 183→{evs['A']}、D 14→{evs['D']}、G3 46→{gd['G3']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**A 级全量复核：一个协会首页撑起 12 个 A 级**）","",
 "## 1. 逐条看完 africa + asia 的 52 条 A 级","",
 "本轮按 D148 开始 A 级全量复核。africa 19 条 + asia 33 条，全部人工读来源标题。","",
 "### 最大发现：`Home - AAG` 被当成 **12 个条目**的强来源","",
 "`s075-aag-org`（**Home - AAG**，美国地理学家协会**首页**）实测 **8,453 字符**——抓的是首页的导航与新闻列表，因此轻松过了 `has_content` 的 800 字符门槛。",
 "它被登记在 **12 条**里：","",
 "> 朝鲜半岛、中南半岛、黎凡特、伊比利亚半岛、高卢、多瑙河、巴尔干半岛、城市地理、人均产出空间差异、可持续交通、国家收入分类、人文地理学","",
 "同类的还有 **CBD 首页**（`s070-cbd-int`，4 条：南极特别保护区、争议边界处理原则、海洋保护区、陆地保护区）、**FAO 首页**（2 条）。",
 "**一个首页撑起多个 A 级**——这比上一轮「城市化←Climate Change」严重得多。","",
 "### 另两处侧面","",
 "| 条目 | 来源 | 问题 |","|---|---|---|",
 "| 尼罗河三角洲 | Heavy metal concentrations in surface river water… | **现代重金属污染监测**，非三角洲沉积演变 |",
 "| 古埃及中王国 | **Poetry and Culture** in Middle Kingdom Egypt | **文学**，不支撑中央行政 |","",
 "## 2. 修复（D149）：首页/导航页不算内容来源","",
 "在 `assess.py` 加规则：标题形如「Home - X」「Home \\| X」者判为**机构首页** → `has_content` 返回 False、`strength` 返回 weak。","",
 "实测：`Home - AAG` → True；`Earth Observatory - NASA Science`、`NOAA's National Ocean Service`、`The Great Lakes`、`Urbanization \\| OWID`、`AQUASTAT — Countries and Basins` → 均为 False（这些是专题页，不是首页，规则没有误伤）。","",
 "## 3. 数字修正","",
 "| 指标 | 修正前 | 修正后 |","|---|---|---|",
 f"| **A 级** | 183 | **{evs['A']}** |",
 f"| **D 级** | 14 | **{evs['D']}** |",
 f"| **G3** | 46 | **{gd['G3']}** |",
 f"| G3a | 27 | **{sp['G3a']['count']}**（核心6/重要18/补充10） |",
 f"| G3b | 19 | **{sp['G3b']['count']}** |","",
 "**A 级掉了 12 条，G3 涨了 7 条**——这些条目本来就不是 A 级，它们是被一个首页撑上去的。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | 已达成（**但需注意**：G1=0 曾因首页达标而成立，D149 后仍为 0） |",
 "| 判据单一实现（D146） | **已达成** |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 "| **A 级来源真实对位** | **africa+asia 已复核完（52/171），发现 14 处问题** |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 122/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} D={evs['D']} G3={gd['G3']} G3a={sp['G3a']['count']}")