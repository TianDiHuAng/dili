# -*- coding: utf-8 -*-
"""第90轮收尾（重大修正）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, level_of, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=90;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":8,"fixes":2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"41项边界用例 + 8条A级抽样","sample_audit":"代码全绿；抽样发现2处虚高 → 修出 content_count 不认 side 的根本缺陷",
 "note":f"D146：content_count 须与 strength 同源→G3 14→{gd['G3']}（此前旁证被算作内容源）；A{evs['A']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
sat["milestones"]=sat.get("milestones",[])
sat["milestones"].append({"round":ROUND,"event":"D146：content_count 与 strength 同源；G3 由虚低的 14 修正为 45"})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=2
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**审计查出根本缺陷：G3 从 14 修正为 "+str(gd["G3"])+"**）","",
 "## 1. 审计结果：41 项代码用例全绿，但抽样曝出真问题","",
 "按 D143 的周期点，本轮先用 **41 项边界用例**测 `assess.py` 的每个函数（is_data/is_alias/is_bad_type/_nums/has_content/strength/level_of/count_entry/content_count）——**全部通过，0 失败**。",
 "D138/D141/D142 的修复看起来已经到位。","",
 "然后做第二层：**随机抽 8 条 A 级条目，人工看两个来源是否真的都支撑该条**。抽到了两条可疑：","",
 "| 条目 | 来源 | 问题 |","|---|---|---|",
 "| **汉代** | 《Dogs in Early Imperial China: …from the **Han Dynasty**》(2019, 被引0) | 主题是**汉代图像中的狗**（动物考古），但标题含 Han Dynasty → **R20 放行** |",
 "| 撒哈拉沙漠 | 《Twentieth-Century Climate Change over Africa》(2018, 被引181) | 是 **20 世纪**非洲季节性水文气候，不是地质时期干旱化 |","",
 "这两条正是我第87轮写过的「**R20 拦不住的那一层：标题含对象词而主题无关**」。","",
 "## 2. 顺着汉代那条，挖到根本缺陷","",
 "把「Dogs」标为旁证后重算，汉代的内容源数**仍是 2**——查下去发现：","",
 "```python\ndef content_count(entry, sources):\n    return sum(1 for sid in entry.get(\"sources\", [])\n               if has_content(sid, …))   # ← 不认 side 标记！\n```","",
 "`has_content()` 只看数值门槛与 data/alias/书评/空壳页，**完全不看条目备注里的「旁证/剔除/降级/不作」**。",
 "而 `strength()` 看。**层级用 strength（认旁证），G3 用 content_count（不认）——两套逻辑并存。**","",
 "**后果**：所有被标为旁证的来源，一直都在被算作「内容源」。这让条目的内容源数虚高、G3 虚低。","",
 "**这是 D138「判据单一实现」的第三次破裂**（前两次：D141 指标类、D142 多值取大）。","",
 "## 3. 修复（D146）与数字修正","",
 "`content_count` 改为**必须 `strength()==\"strong\"` 且 `has_content()` 为真**才计数。","",
 "| 指标 | 修正前 | **修正后** |","|---|---|---|",
 f"| **G3** | 14 | **{gd['G3']}** |",
 f"| G3a（有侧面可补） | 4 | **{sp['G3a']['count']}**（核心6/重要10/补充10） |",
 f"| G3b（无其他来源） | 10 | **{sp['G3b']['count']}**（核心4/重要11/补充4） |",
 f"| A 级 | 186 | {evs['A']}（汉代降 B） |",
 f"| 内容源 ≥2 | 229 | **{g2}** |","",
 "**G3 从 14 涨到 45**——不是退步，是**此前 40 轮的 G3 数字一直偏低**。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243",
 "- 无解清单（D145）：笈多王朝、巴西高原、拉普拉塔平原","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |",
 "| 判据单一实现（D146 后） | **已达成（第三次破裂已修）** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 检索失败与无结果分离（D144） | 已落地 |",
 "| 重复命中即停止重试（D145） | 已建立，3 条在册 |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 58/243 已扫描 |","",
 "## 5. 为什么这轮最重要","",
 "**41 项代码用例全绿，却在抽样里发现了根本缺陷**——因为用例只测「我想到的情况」，而缺陷在「两个函数不一致」。",
 "如果我只跑用例就收工，G3=14 会作为既成事实继续下去；**它比真实值低 31 条**。",
 "这印证了 D143 的价值：**定期审计要审「函数之间是否一致」，不只是「单函数对不对」**。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']} ge2={g2}")