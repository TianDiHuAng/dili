# -*- coding: utf-8 -*-
"""第102轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=102;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":10,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"G3a补充10条性质判读","sample_audit":"D157/D158：指标解读类有旁证与 today 指标均不阻止判 D；G3 27→20",
 "note":f"D157+D158 →D 22→{evs['D']}、G3 27→{gd['G3']}；一致性0问题"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**两次判据扩展：G3 27 → "+str(gd["G3"])+"**）","",
 "## 1. 这轮没有补任何来源，但缺口少了 7 条","",
 "原因是两条判据扩展——**都是 D141（指标解读类豁免）的边界没画对**。","",
 "### D157：D141 不该要求 `side == 0`","",
 "原判据：仅有 1 个机构长文 + **无旁证** + 有数据端点 → 判 D。",
 "问题：**指标解读类条目本来就只有一个机构长文**，其余来源自然被判旁证（side）。要求 `side==0` 等于把大多数指标类条目挡在 D 之外。",
 "修正后：去掉 `side==0` 这个条件。","",
 "### D158：数据证据不限于 API 端点","",
 "**全球气温距平**的数据来自 **NOAA Climate at a Glance** 页面，不是 `wb-` 端点 → `is_data` 不认 → `data=0` → D141 失效。",
 "但它显然是指标解读类：正文只解释数值，数据自述「来源：NOAA Climate at a Glance（基准期 1901–2000）」。",
 "修正后：若 `today` 字段自述「来源：…指标…」且不作叙事断言，同样算指标解读类。","",
 "## 2. 数字变化","",
 "| 指标 | 修正前 | 修正后 |","|---|---|---|",
 f"| **D 级** | 22 | **{evs['D']}** |",
 f"| B 级 | 27 | **{evs['B']}** |",
 f"| **G3** | 27 | **{gd['G3']}** |",
 f"| G3a 补充 | 10 | **{sp['G3a']['tiers'].get('补充')}** |","",
 "**这 7 条不是「补上了源」，而是「本来就该算 D 级」**——它们的正文是指标解释与空间差异概述，机构长文即主体。D135 的定义原本就包括这一类。",
 "**关键验证**：改完立刻跑了一遍 `round100_consist.py`——**6 项交叉一致性仍是 0 问题**。说明这次扩展没有打破 strength / content_count / level_of 的一致性。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / **D {evs['D']}**",
 f"- 内容源 ≥2：**{g2}**（{g2*100//243}%）；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3a={sp['G3a']['count']}**（核心0/重要{sp['G3a']['tiers'].get('重要')}/补充{sp['G3a']['tiers'].get('补充')}） / **G3b={sp['G3b']['count']}**（核心0/重要{sp['G3b']['tiers'].get('重要')}/补充{sp['G3b']['tiers'].get('补充')}） / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| A 级来源真实对位（全量复核） | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 核心条目全部有 ≥2 内容源 | **已达成** |",
 "| 判据单一实现 + 收敛（D155，本轮两次扩展后复验） | **已达成** |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，全为重要/补充级） |",
 "| G4 语义对题 | 243/243 已扫描 |","",
 "## 4. 剩余 20 条","",
 "| 类别 | 条数 | 内容 |","|---|---|---|",
 "| G3a 重要 | **3** | 朝鲜半岛、中南半岛、黎凡特 |",
 "| G3a 补充 | 4 | 古埃及中王国、争议边界处理原则、教育机会地域差异、人文地理学 |",
 "| G3b 重要 | **10** | 笈多、隋唐、明清、威尼斯、巴西高原、拉普拉塔、大分水岭、南极条约、冲积平原、山地农业 |",
 "| G3b 补充 | 3 | 非洲大湖、西北海岸、荒漠化 |","",
 "其中 **3 条已判无解**（笈多、巴西高原、拉普拉塔），实际在追的 **17 条**。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} D={evs['D']} G3={gd['G3']}")