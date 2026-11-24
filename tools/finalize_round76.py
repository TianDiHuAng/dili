# -*- coding: utf-8 -*-
"""第76轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=76;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":5,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":5,"sample_rate":"重要条目第二批12条","sample_audit":"5条登记、7条侧面不采用",
 "note":f"补5条→G3 74→{gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=5
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：74 → "+str(gd["G3"])+"**）","",
 "## 1. 重要条目第二批 12 条：登记 5 条","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 阿拉伯半岛 | Chronology of the impact of Quaternary climate change (2009) | **95** | 976 |",
 "| 吴哥 | Top-down and bottom-up water management in Greater **Angkor** (2020) | 48 | 1,413 |",
 "| 匈奴 | Iron Smelting in the Nomadic Empire of **Xiongnu** (2014) | 21 | 1,451 |",
 "| 周代 | Radiocarbon dating for the founding of Yan Vassal State (2025) | 6 | 1,387 |",
 "| 孔雀王朝 | The Empire Under One **Umbrella**: Espionage, Reporting… (2026) | 2 | 3,665 |","",
 "五条都对得上摘要：",
 "- **吴哥**：摘要写「9–15 世纪高棉帝国发展出大规模农业与水资源管理系统」——正是本条要的水利机制；",
 "- **孔雀**：摘要论证「若无信息获取、传递与核验系统，孔雀帝国无法维系于单一权威之下」；",
 "- **周代**：摘要点明「西周灭商后建立中国最早的**分封制**」；",
 "- **匈奴**：摘要写「匈奴是东亚欧第一个游牧帝国」，并报告冶铁遗址（前209–公元155）；",
 "- **阿拉伯半岛**：摘要据古湖遗迹指出半岛过去远比今天湿润。","",
 "## 2. 七条侧面，不采用（占用本批一半以上）","",
 "| 条目 | 候选主题 |","|---|---|",
 "| 吠陀时代 | 吠陀文献中的**女性地位**（性别） |",
 "| 笈多王朝 | **钱币学** |",
 "| 明清 | **医学制度** |",
 "| 马来群岛 | **方言语言学** |",
 "| 河中地区 | **粟特铭文**文献学 |",
 "| 突厥 | **女性墓葬**（性别与考古） |",
 "| 克里特文明 | 本轮 **0 候选**（已多次检索无果） |","",
 "## 3. 口径（tools/assess.py）","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：**{o1}**；0 个：**{z0}**",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / **G3={gd['G3']}** / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现（D138） | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 f"| 每个条目都有强来源（G1=0） | 未达成（{gd['G1']} 条） |",
 f"| 每条都有 ≥2 内容源 | 未达成（{o1+z0} 条不足） |",
 "| G4 语义对题 | 38/243 已扫描 |","",
 "## 4. 一个趋势：命中率在下降","",
 "本批 12 条中 11 条有候选，但只有 5 条对位——**7 条是侧面**（性别、钱币、医学、方言、铭文、墓葬）。",
 "被引与摘要门槛都已通过，卡在最后一步「摘要讲的是不是这条要的事」。这说明：**越往后，剩下的条目越是「文献都只研究它的某个侧面」**——这不是检索问题，是研究对象本身的分布。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} ge2={g2} one={o1} zero={z0} G3={gd['G3']}")