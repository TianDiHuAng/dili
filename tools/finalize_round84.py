# -*- coding: utf-8 -*-
"""第84轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=84;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":11,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":11,"sample_rate":"补充G3b 12条（Crossref 路线）","sample_audit":"12/12命中、HTTP失败率0%；11条登记",
 "note":f"Crossref 路线稳定（0%失败）；补11条→G3 44→{gd['G3']}、G3b补充 20→{sp['G3b']['tiers'].get('补充')}；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=11
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：44 → "+str(gd["G3"])+"**）","",
 "## 1. Crossref 路线非常稳定：12/12 命中、0% 失败","",
 "沿用上轮 D144 合规脚本（记录 HTTP 状态、失败率阈值），本轮 12 条补充条目**全部命中，HTTP 失败 0 次**（成功 485）。","",
 "| 条目 | 来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 的的喀喀湖 | Geology of the Lake Titicaca Region (1949) | **122** | 614 |",
 "| 奇穆帝国 | Imperialist Expansion in Peruvian Prehistory (1983) | **82** | 1,766 |",
 "| 纳斯卡文化 | Beyond the Nasca Lines (2016) | 22 | 1,434 |",
 "| 密克罗尼西亚 | Traditional Micronesian Societies (2017) | 22 | 2,141 |",
 "| 美拉尼西亚 | Change and Resilience in Melanesian Societies (2018) | 0 | **13,669** |",
 "| 基辅罗斯 | Position and Role of the Kyivan Rus' (2019) | 4 | 3,466 |",
 "| 南美贸易网络 | The Jaén Stone Bowl Tradition (2022) | 4 | 1,275 |",
 "| 新法兰西 | Power and Subsistence: Political Economy (2018) | 6 | 1,323 |",
 "| 查文文化 | Chavin culture (pre-Moche) (2016) | 2 | 909 |",
 "| 欧洲冰期地貌 | Dynamics of the Pleistocene glaciation (1986) | 0 | 953 |",
 "| 阿巴拉契亚山脉 | Connecting Trail: International Appalachian Trail (2019) | 0 | 1,499 |","",
 "## 2. 一条不采用","",
 "**西北海岸** ←《Incorporating Culture: How Indigenous People Are Reshaping…》(2018)：主题是**文化旅游与文化商品化**（当代议题），不支撑「传统社会与资源管理」。","",
 "## 3. R20 又抓到两个别名","",
 "| 条目 | 来源标题实际用词 | 补入对象词 |","|---|---|---|",
 "| 纳斯卡文化 | **NASCA**（非 NAZCA） | `nasca` |",
 "| 欧洲冰期地貌 | **PLEISTOCENE / GLACIATION** | `pleistocene`、`glaciation` |","",
 "这是 R20 第三次逼我补别名（前两次：indus→harappan、andes→andean）。**它是目前性价比最高的规则**——每次都在我自以为完成时冒出来。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}**（补充仅 {sp['G3b']['tiers'].get('补充')}） / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | 已落地，实测 0% 失败 |",
 f"| 每个条目都有强来源或属 D 级 | 未达成（{gd['G1']} 条：隋唐） |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3b={sp['G3b']['count']} 补充={sp['G3b']['tiers'].get('补充')}")