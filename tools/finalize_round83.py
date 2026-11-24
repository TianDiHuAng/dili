# -*- coding: utf-8 -*-
"""第83轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=83;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":9,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"被撤销的9条重跑（Crossref 路线）","sample_audit":"7/9命中、失败率2%——证明上轮0候选是429假象",
 "note":f"D144 首次执行：Crossref 路线重跑得6条→G3 50→{gd['G3']}；层级 A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0,
 "search_route":"Crossref query.bibliographic → DOI → OpenAlex by-ID（D144；OpenAlex search 端点 429 不可用）"})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**D144 首次执行：7/9 命中**）","",
 "## 1. 用 Crossref 路线重跑被撤销的 9 条","",
 "上轮因 OpenAlex search 端点 429，12 条被误判为「0 候选」并撤销。本轮按 D144 写了合规脚本：**记录每次请求的 HTTP 状态、失败率超 50% 即中止、失败与无结果分开统计**。","",
 "**结果：7/9 命中，HTTP 成功 184 / 失败 3（失败率 2%）**。","",
 "| 条目 | 来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 古埃及中王国 | Setting a State Anew: Central Administration… (2013) | **52** | 912 |",
 "| 非洲大湖地区（type=book，未采用） | Conflict and Peacebuilding… (2013) | 51 | 2,692 |",
 "| 贵霜帝国 | The Kushan Empire (2020) | 1 | 1,598 |",
 "| 迈锡尼文明 | Beyond the Palace: Mycenaean East Lokris (2008) | **39** | 1,195 |",
 "| 帖木儿帝国 | Diplomacy of The Timurid Empire (2026) | 0 | 1,610 |",
 "| 法蒂玛王朝 | The Fatimid Caliphate (2023) | 0 | 876 |",
 "| 仰韶文化 | Painted Pottery Motifs in the Yangshao… (2025) | 2 | 1,194 |","",
 "登记 6 条（非洲大湖地区因主题为当代冲突与和平建设、属政治侧面，不采用；其 type 经查为 `book` 非书评，故不是书评问题）。","",
 "## 2. 两条真实的无过筛结果","",
 "**室利佛逝、满者伯夷**：Crossref 路线检索成功（本次整体失败率仅 2%），20 条结果中确无同时满足「标题含对象词」与「两主题槽」者。",
 "**这两条现在可以算「真实的无结果」**——因为同一批次里其余 7 条都命中了，说明检索通道畅通。这正是 D144 想要的区分：**「检索失败」与「检索成功但无结果」必须能分开**。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}** / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | **已落地并通过实测** |",
 f"| 每个条目都有强来源或属 D 级 | 未达成（{gd['G1']} 条：隋唐） |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3b={sp['G3b']['count']}")