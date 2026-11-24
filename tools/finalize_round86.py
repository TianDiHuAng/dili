# -*- coding: utf-8 -*-
"""第86轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=86;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":10,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"重要G3b前10条（综述性检索词）","sample_audit":"9/10命中、1%失败；6条登记",
 "note":f"改用综述词（history/state formation）→G3 26→{gd['G3']}；重要G3b 20→{sp['G3b']['tiers'].get('重要')}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：26 → "+str(gd["G3"])+"**）","",
 "## 1. 换了检索词策略：用综述性语汇","",
 "此前对这批政权类条目，我总是用「对象词 + 具体主题词（state/administration/economy）」检索，结果命中的多是侧面（钱币、铭文、墓葬、方言、医学、性别）。",
 "本轮改用**综述性语汇**——`history`、`state formation`、`political economy`、`in crusading movement` 等，让检索偏向「整体研究」而非「某个专题」。","",
 "**结果：9/10 有候选，登记 6 条**：","",
 "| 条目 | 来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 阿拉伯征服北非 | A History of the **Maghrib** in the Islamic Period (1987) | **400** | 1,108 |",
 "| 桑海帝国 | The Fall of the Songhai Empire (2018) | 0 | 937 |",
 "| 十字军东征 | The Fifth Crusade in Context: Crusading Movement (2016) | 8 | 1,247 |",
 "| 克里特文明 | Understanding Minoan In-House Relationships (2017) | 4 | 2,001 |",
 "| 萨珊波斯 | Sasanian Empire (2016) | 3 | 800 |",
 "| 河中地区 | Mongol invasion of Transoxiana 1219–1221 (2022) | 3 | 1,310 |","",
 "**阿拉伯征服北非那条被引 400**——是马格里布伊斯兰时期的通史，正是本条整体背景所需。","",
 "## 2. 四条仍不行（三条还是侧面）","",
 "| 条目 | 候选主题 |","|---|---|",
 "| 笈多王朝 | **钱币之美**（第二次命中钱币学，第76轮也命中过「Role of Coins」） |",
 "| 明清 | **一本书的编辑与流传史**（书籍史） |",
 "| 吠陀时代 | **非洲—印度的史前邻近性**（泛论，不涉吠陀） |",
 "| 马来群岛 | 本轮 0 候选 |","",
 "**笈多王朝这条已经连续两轮命中钱币学**——该主题的英文文献确实以钱币研究为主。这不是检索问题。","",
 "## 3. R20 第四次逼我补别名","",
 "阿拉伯征服北非的来源标题用的是 **MAGHRIB**（不是 ARAB 或 NORTH AFRICA）→ 对象词补 `maghrib`、`north africa`。",
 "前三次：indus→harappan、andes→andean、nazca→nasca。","",
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
 "| 检索失败与无结果分离（D144） | 已落地，本轮 1% 失败 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，重要 {sp['G3b']['tiers'].get('重要')} / 补充 {sp['G3b']['tiers'].get('补充')}） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3b={sp['G3b']['count']} 重要={sp['G3b']['tiers'].get('重要')}")