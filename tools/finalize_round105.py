# -*- coding: utf-8 -*-
"""第105轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=105;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":5,"fixes":2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"G3 剩余 11 条中 5 条检索","sample_audit":"登记4条：人文地理学、隋唐计入内容源；大分水岭、冲积平原因标题不含对象词(R20)只能作旁证，不计入内容源；教育机会地域差异无合格候选",
 "note":f"G3 11→{gd['G3']}（登记2条计入，2条旁证不计）；A{evs['A']}；一致性0问题"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：11 → "+str(gd["G3"])+"**）","",
 "## 1. 本轮登记","",
 "| 条目 | 新增来源 | 被引 | 处理 |","|---|---|---|---|",
 "| 人文地理学 | Charting the development of social and cultural geography in Mainland China (2014) | 19 | 计入第二内容源，已注明仅中国大陆视角 |",
 "| 隋唐 | City of Marvel and Transformation: Changan in Tang Dynasty China (2015) | 9 | 计入第二内容源，证据偏弱，已注明 |",
 "| 大分水岭 | Post-orogenic evolution of a mountain range: South-eastern Australian Highlands (1985) | 9 | 标题不含对象词，按 R20 作旁证，不计内容源 |",
 "| 冲积平原 | Channel-floodplain response to changes in sediment supply and floodplain width (2020) | 2 | 标题不含对象词，按 R20 作旁证，不计内容源 |","",
 "## 2. 未命中与教训","",
 "- 教育机会地域差异：候选一重叠（中国高等教育城乡差距），候选二主题仅部分对位（撒哈拉以南非洲性别差异），均不采用。",
 "- 大分水岭、冲积平原仍缺标题含对象词的第二来源，需换检索角度。",
 "- 教训：R20 要求标题含对象词，豁免要求标「旁证」，但旁证按 D146 又不计内容源，两者合起来意味着标题不含对象词的来源不可能抬升 G3。选候选时应优先要求标题含对象词。",
 "- 豁免标记须写在来源 id 第一次出现处的前 120 字内，否则 R20 读不到。","",
 "## 3. 口径与验证","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 "- `round100_consist.py`：一致性 0 问题",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "## 4. 剩余 "+str(gd['G3'])+" 条","",
 "- G3a：大分水岭、冲积平原、教育机会地域差异",
 "- G3b：非洲大湖地区、笈多王朝（无解）、西北海岸、巴西高原（无解）、拉普拉塔平原（无解）、卫星遥感地表观测",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")
