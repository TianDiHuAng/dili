# -*- coding: utf-8 -*-
"""第93轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=93;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":42,"fixes":3,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"A级全量复核europe+north-america（42条）","sample_audit":"查出同域名多页12条（D150）、层级与内容源口径不一致（D151）、Rhine书评",
 "note":f"D150/D151：A 171→{evs['A']}、D 19→{evs['D']}、G3 53→{gd['G3']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=3
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**A 级全量复核 europe+42 条；查出同域名多页问题**）","",
 "## 1. 复核范围：europe 23 条 + north-america 19 条","",
 "逐条读完 42 条 A 级，发现三类问题。","",
 "### 问题一：同一网站的多个页面被当成「两个独立来源」（12 条）","",
 "| 条目 | 同域来源 |","|---|---|",
 "| **古希腊城邦** | `livius.org` 的 **Polis + Athens + Greece 三页** |",
 "| **罗马共和国** | `livius.org` 的 Roman Republic + Italy 两页 |",
 "| 湄公河三角洲 / 亚马逊河 / 土壤资源 | `fao.org` 的 AQUASTAT + Forestry 两页 |",
 "| 科罗拉多高原 | `nps.gov` 的 Geologic Formations + 公园主页 |",
 "| 板块构造 | `usgs.gov` 的 Understanding plate motions + This Dynamic Earth |",
 "| 肉奶生产与土地 | `ourworldindata.org` 两页 |",
 "| 健康地理数据 | `who.int` 两页 |",
 "| 环境数据访问 | `ncei.noaa.gov` 两页 |",
 "| 亚马逊盆地 / 火灾生态 | `earthobservatory.nasa.gov` 两页 |","",
 "**同一出版者的两个页面不能互证**——这与 D135「别名页」同源，只是维度从「同一页被多处引用」变成「同一站的多页」。",
 "（`openalex-` 来源不受影响：它们是不同论文，URL 同为 API 端点只是接口形式。）","",
 "### 问题二：层级与内容源判定又不一致（D146 同类，换维度）","",
 "加了域名去重后，`content_count` 变了，但 `level_of` 仍在用 `c[\"strong\"]>=2` ——**一个看域名、一个不看**。",
 "结果：古希腊城邦（4 个 strong，其中 3 个同属 livius）仍算 **A 级**，而它的独立内容源只有 2（Livius 计 1 + 海岸地貌 1）。",
 "**这是 D146「两套逻辑」的同一形态换了个维度**（D146 是 side 标记，这次是域名）。","",
 "### 问题三：书评的 type 字段标成了「学术文献」","",
 "**莱茵河** ←《The Rhine: An Eco-Biography, 1815–2000》**(review)**，DOI 是 `10.1353/tech.2005.0070`（Technology and Culture 期刊的书评），被引仅 1。",
 "OpenAlex 的 `type` 标为「学术文献」，**R25 只看 type 因而漏检**——D136 的再一次实例。","",
 "## 2. 修复","",
 "| 编号 | 内容 |","|---|---|",
 "| **D150** | `content_count` 按**域名去重**：同一域名下多个页面最多计 1 个内容源（`openalex-`/`wikidata-` 除外） |",
 "| **D151** | `level_of` 的 A 级判定改为 **`strong>=2` 且 `content_count>=2`**，与 D150 同口径 |",
 "| — | 莱茵河标签为旁证 |","",
 "## 3. 数字修正","",
 "| 指标 | 修正前 | 修正后 |","|---|---|---|",
 f"| **A 级** | 171 | **{evs['A']}** |",
 f"| **D 级** | 19 | **{evs['D']}** |",
 f"| **G3** | 53 | **{gd['G3']}** |",
 f"| G3a | 34 | **{sp['G3a']['count']}**（核心6/重要18/补充10） |",
 f"| G3b | 19 | **{sp['G3b']['count']}** |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | **已达成**（D150/D151 后仍为 0） |",
 "| 判据单一实现 | **已达成（D146 + D150 + D151 三次收敛）** |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 "| **A 级来源真实对位** | **africa/asia/europe/n-america 已复核（94/168）** |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 164/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} D={evs['D']} G3={gd['G3']}")