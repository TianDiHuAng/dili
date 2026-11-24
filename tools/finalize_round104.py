# -*- coding: utf-8 -*-
"""第104轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=104;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":7,"fixes":5,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":5,"sample_rate":"G3a剩余7条","sample_audit":"5/7命中；登记5条（中王国107引/争议边界117引/黎凡特98引/朝鲜半岛/中南半岛）；教育机会、人文地理学无通过候选；1条对象碰撞（季风对流）",
 "note":f"补5条→G3 16→{gd['G3']}、G3b重要 6→{sp['G3b']['tiers'].get('重要')}；A{evs['A']}；一致性0问题"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：16 → "+str(gd["G3"])+"**）","",
 "## 1. G3a 剩余 7 条：5 条命中","",
 "| 条目 | 新补第二来源 | 被引 | 说明 |","|---|---|---|---|",
 "| 古埃及中王国 | The Middle Kingdom of Ancient Egypt: History, Archaeology and Society (2006) | **107** | 历史与考古的社会视角 |",
 "| 争议边界处理原则 | Equitable Principles of Maritime Boundary Delimitation (2015) | **117** | 仅海洋划界，已在条目注明 |",
 "| 黎凡特 | Structural Transformations in Settlement Systems of the Northern Levant (2007) | **98** | 阿姆克谷地聚落，已注明样本范围 |",
 "| 朝鲜半岛 | Learning Geography of Korea by Mountains and Island (2024) | 1 | 教学性概述，证据强度有限，已注明 |",
 "| 中南半岛 | Land Use History in Montane Mainland Southeast Asia (2005) | 2 | 仅山地大陆东南亚，被引很少，已注明 |","",
 "## 2. 未命中与碰撞","",
 "- 教育机会地域差异、人文地理学：本轮无通过候选，需换检索角度。",
 "- 中南半岛的另一候选（2007，被引 21）研究季风对流起始，属大气科学，不采用。","",
 "## 3. 流程教训","",
 "登记后首次校验出现 R22 与一致性共 10 处问题，原因是 `evidence_level.json` 与缺口报告未重新生成（数据本身无误）。",
 "**登记后须先依次运行 `round68_levels.py` → `round62_gaps.py` → `round77_split.py`，再做校验与收尾。**","",
 "## 4. 口径与验证","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 "- `round100_consist.py`：一致性 0 问题",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "## 5. 剩余 11 条","",
 "| 类别 | 条数 | 内容 |","|---|---|---|",
 "| G3a 补充 | 2 | 教育机会地域差异、人文地理学 |",
 "| G3b 重要 | 6 | 笈多（无解）、隋唐、巴西高原（无解）、拉普拉塔（无解）、大分水岭、冲积平原 |",
 "| G3b 补充 | 3 | 非洲大湖、西北海岸、荒漠化 |","",
 "扣掉 3 条无解，实际在追 8 条。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")
