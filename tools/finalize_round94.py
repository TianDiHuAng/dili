# -*- coding: utf-8 -*-
"""第94轮收尾（撤销假里程碑）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=94;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":77,"fixes":3,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"A级全量复核south-america/oceania/antarctica/global-themes（77条）","sample_audit":"查出 strength 的 for…break 只查首段（D152）——4条虚高、G1 假清零",
 "note":f"D152：A 167→{evs['A']}、C 0→{evs['C']}、G1 0→{gd['G1']}、G3 54→{gd['G3']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
sat["milestones"]=sat.get("milestones",[])
sat["milestones"].append({"round":ROUND,"event":"修正：第85轮「G1 清零」不成立（D152 发现 for…break 忽略降级记录）；G1 真实为 4"})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=3
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**撤销一个里程碑：G1 并非 0，真实为 4**）","",
 "## 1. A 级全量复核完成（77 条）","",
 "south-america 15 + oceania 11 + antarctica 8 + global-themes 43 = **77 条**，加上前几轮的 94 条，**A 级全量复核已完成**。","",
 "### 三处具体虚高","",
 "| 条目 | 来源 | 问题 |","|---|---|---|",
 "| **南锥体** | 两条**都不对位**：《**Climate Change** \\| OWID》+《**Spanish postwar emigration** to the Southern Cone》 | 一个是全球气候页，一个是 20 世纪西班牙移民史 |",
 "| 大堡礁 | 《Effects of **herbicides** diuron and atrazine on corals》 | 除草剂毒理学 |",
 "| 南极科考站 | 《Survey of **waste water** disposal practices at Antarctic stations》 | 污水处理做法 |","",
 "## 2. 顺着南锥体，挖到一个更根本的缺陷","",
 "把南锥体两条都标为旁证后，它**仍是 B 级**（strong 1）。查下去发现 `strength()` 里这段：","",
 "```python\nfor part in re.split(r\"【\", pending_notes):\n    if sid in part:\n        seg = part\n        break          # ← 只取第一个含 sid 的段落\n```","",
 "**`break` 让函数只检查 sid 的第一次出现。** 而一个来源在条目生命周期里常常先被「补登记」，**后来才被「降级」**——降级记录写在后面，被完全忽略。",
 "南锥体的 `openalex-W4224441281` 就是这样：第40轮登记时说「第二来源已升级」，第94轮才降级；前者被读到，后者被跳过。","",
 "## 3. 后果：第85轮的「G1 清零」是假的","",
 "改成检查**所有**出现段落后重算：","",
 "| 指标 | 修正前 | **修正后** |","|---|---|---|",
 f"| **G1（无强来源）** | 0 | **{gd['G1']}** |",
 f"| **C 级** | 0 | **{evs['C']}** |",
 f"| A 级 | 167 | **{evs['A']}** |",
 f"| G3 | 54 | **{gd['G3']}** |","",
 "**G1 真实为 4 条**：","",
 "> 古埃及古王国、苏美尔城邦、古希腊城邦、南锥体","",
 "这四条此前都靠「先补后降」的来源撑着。**第85轮我写下的「G1 清零、C 级清零」这个里程碑不成立**，已在 SATURATION 中标注修正。","",
 "## 4. 修复（D152）","",
 "`strength()` 改为取 sid 的**全部**出现段落，**任一**含「旁证/剔除/不作/降级」即判 `side`。",
 "（降级是不可逆的：一旦某来源在生命周期的任一环节被判旁证，就不该再被算作强来源。）","",
 "## 5. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / **C {evs['C']}** / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：**G1={gd['G1']}** / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| **A 级来源真实对位（全量复核完毕）** | **已达成（171 条全查，查出 20+ 处问题）** |",
 f"| 每个条目都有强来源 | **未达成（{gd['G1']} 条：古埃及古王国、苏美尔城邦、古希腊城邦、南锥体）** |",
 "| 判据单一实现 | **已达成（D146/D150/D151/D152 四次收敛）** |",
 "| 机器校验 R19–R25 | 已上线，0 违规 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 241/243 已扫描 |","",
 "## 6. 四轮复核的累计","",
 "| 轮 | 范围 | 查出 |","|---|---|---|",
 "| 90 | 抽 8 | 2（狗、20 世纪气候） |",
 "| 91 | 抽 12 | 2（错挂气候页、双耳瓶） |",
 "| 92 | 全量 52 | 14（**AAG 首页×12**、CBD×4 + 2 处侧面） |",
 "| 93 | 全量 42 | 12（**同域名多页**）+ 口径不一致 + 书评 |",
 "| 94 | 全量 77 | 3 处 + **for…break 缺陷（4 条虚高）** |",
 "| **合计** | **191 条** | **33+ 处** |","",
 "**全量复核的价值在此显现**：抽样 20 条只发现 4 处，全量 191 条发现 33+ 处，而且**最严重的两个缺陷（AAG 首页、for…break）抽样都没碰到**。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} C={evs['C']} G1={gd['G1']} G3={gd['G3']}")