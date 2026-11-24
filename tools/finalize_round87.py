# -*- coding: utf-8 -*-
"""第87轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=87;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":10,"fixes":3,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":3,"sample_rate":"重要G3b剩余10条","sample_audit":"10/10命中、2%失败；3条登记",
 "note":f"补3条（洋流120/毛利人/巴西殖民）→G3 20→{gd['G3']}；重要G3b 14→{sp['G3b']['tiers'].get('重要')}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=3
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：20 → "+str(gd["G3"])+"**）","",
 "## 1. 登记 3 条","",
 "| 条目 | 来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 洋流 | Climate and the Ocean Circulation (1969) | **120** | 3,355 |",
 "| 毛利人 | Maori Values Can Reinvigorate a New Zealand Philosophy (2012) | 14 | **6,902** |",
 "| 巴西殖民经济 | Sugar and the Formation of Colonial Brazil (2019) | 3 | 842 |","",
 "10/10 有候选，但只登记了 3 条——其余 6 条是侧面或碰撞，1 条重复。","",
 "## 2. 本轮的碰撞最有意思：大分水岭 ← 新种螯虾","",
 "**大分水岭** ←《Euastacus vesper sp. nov., a new giant spiny **crayfish**》(2017)。",
 "摘要说的是「新种螯虾描述自新南威尔士 Cudgegong 河上游」，只因标本产地「位于 **Great Dividing Range** 西部水系」而命中。",
 "**这是「产地碰撞」**——山脉在这里只是一个地理位置状语，论文主题是动物分类学。R20 能拦住「标题不含对象词」，但拦不住「标题含对象词而主题无关」。","",
 "## 3. 其余不采用","",
 "| 条目 | 候选主题 |","|---|---|",
 "| 威尼斯 | **面具文化**（社会习俗） |",
 "| 马来群岛 | **颅测量学**的人群迁移史（体质人类学） |",
 "| 巴西高原 | 局部喀斯特保护区（第80轮已拒） |",
 "| 拉普拉塔平原 | 泛论（第80轮已拒） |",
 "| 南极条约体系 | 命中的来源第39轮已登记（无新增） |",
 "| 气候带 | 候选来源已在库中，本次未新增到该条目 |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}**（重要 {sp['G3b']['tiers'].get('重要')} / 补充 {sp['G3b']['tiers'].get('补充')}） / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | 已落地，本轮 2% 失败 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条：重要 {sp['G3b']['tiers'].get('重要')} / 补充 {sp['G3b']['tiers'].get('补充')} / G3a {sp['G3a']['count']}） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} 重要={sp['G3b']['tiers'].get('重要')}")