# -*- coding: utf-8 -*-
"""第88轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=88;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":6,"fixes":1,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":1,"sample_rate":"6条首次尝试","sample_audit":"6/6命中0%失败；仅1条登记（气候带）；3条列无解",
 "note":f"D145：3条重复命中列无解；补1条→G3 17→{gd['G3']}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
sat["unsolvable"]=["笈多王朝","巴西高原","拉普拉塔平原"]
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=1
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**立 D145：停止重试规则**）","",
 "## 1. 一个此前没做的决断","",
 "上轮结尾我写过：「已多轮重复命中同一候选的条目，该停止重试了」。本轮把它变成规则。","",
 "**D145**：同一候选在**两轮独立检索**中被重复命中，即视为该条目的「最佳可得文献」，停止重试并列入无解清单——不再每轮空转。","",
 "### 已列无解的三条","",
 "| 条目 | 重复命中的候选 | 两轮 |","|---|---|---|",
 "| **笈多王朝** | 钱币学研究（《Role of Coins》/《Treasures of the Gupta Empire》） | 76、86 |",
 "| **巴西高原** | 局部喀斯特地貌制图（仅里约韦尔梅柳保护区） | 80、87 |",
 "| **拉普拉塔平原** | 泛论（「任何人类活动都有影响」开场，无潘帕斯结论） | 80、87 |","",
 "**判据**：同一篇在两轮独立检索（不同检索词）中被命中，说明它就是这条目的天花板——再搜也是它。","",
 "## 2. 6 条首次尝试：6/6 有候选，仅 1 条登记","",
 "| 条目 | 登记 | 说明 |","|---|---|---|",
 "| **气候带** | ✅ | 《On coupling global **biome** models with climate models》(1994)，**被引 145**——全球生物群区模型与气候模型耦合 |",
 "| 大分水岭 | — | 候选《降水季节性分布》**已在库**（原本就是唯一来源），无新增 |",
 "| 威尼斯 | ✗ | 17 世纪**北欧海员**，与本条鼎盛期**时期+主题双重错配** |",
 "| 马来群岛 | ✗ | **殖民主义与马来西亚史学论战**（史学史） |",
 "| 吠陀时代 | ✗ | 吠陀文献中的**化学知识**（科技史） |",
 "| 明清 | ✗ | **望远镜**的科技史侧面 |","",
 "## 3. R20 第五次逼我补别名","",
 "气候带的来源标题用 **BIOME / VEGETATION**（不是 CLIMATE ZONE）→ 对象词补 `biome`、`vegetation`。",
 "前四次：indus→harappan、andes→andean、nazca→nasca、conquest→maghrib。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}**（重要 {sp['G3b']['tiers'].get('重要')} / 补充 {sp['G3b']['tiers'].get('补充')}） / G4=243",
 "- **无解清单（D145）**：笈多王朝、巴西高原、拉普拉塔平原","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | 已落地，本轮 0% 失败 |",
 "| 重复命中即停止重试（D145） | **本轮建立，已列 3 条** |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，含 3 条无解） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} 重要={sp['G3b']['tiers'].get('重要')}")