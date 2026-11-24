# -*- coding: utf-8 -*-
"""第106轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=108;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":3,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":2,"sample_rate":"G3b 3 条全部检索","sample_audit":"登记2条：非洲大湖地区(被引35)、西北海岸(被引62)计入第二内容源；卫星遥感地表观测无合格候选",
 "note":f"G3 8→{gd['G3']}；A{evs['A']}；一致性0问题"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3：8 → "+str(gd["G3"])+"**）","",
 "## 1. 本轮登记","",
 "| 条目 | 新增来源 | 被引 | 处理 |","|---|---|---|---|",
 "| 非洲大湖地区 | Prognosis for long-term sustainable fisheries in the African Great Lakes (2018) | 35 | 计入第二内容源；仅引其渔业评估与作者论断，不推断具体数值或成因 |",
 "| 西北海岸 | Salmon, Science, and Reciprocity on the Northwest Coast (2009) | 62 | 计入第二内容源；属单篇研究的论证，已注明作者口径，摘要外机制不引用 |","",
 "## 2. 未命中","",
 "- 卫星遥感地表观测：本轮检索无满足标题含对象词且摘要命中≥2个主题槽的候选。",
 "- 大分水岭、冲积平原：沿用第107轮结论，暂缓。","",
 "## 3. 口径与验证","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 "- `round100_consist.py`：一致性 0 问题",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "## 4. 剩余 "+str(gd['G3'])+" 条","",
 "- G3a：大分水岭、冲积平原",
 "- G3b：笈多王朝（无解）、巴西高原（无解）、拉普拉塔平原（无解）、卫星遥感地表观测",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")

pr=os.path.join(ROOT,"PROGRESS.md")
txt=open(pr,encoding="utf-8").read()
if "第108轮：G3" not in txt:
    txt+=f"""
- **第108轮：G3 8→{gd['G3']}，A 206→{evs['A']}**（登记2条）
  | 条目 | 新来源 | 被引 | 处理 |
  |---|---|---|---|
  | 非洲大湖地区 | Prognosis for long-term sustainable fisheries in the African Great Lakes (2018) | 35 | 计入；仅引渔业评估与作者论断 |
  | 西北海岸 | Salmon, Science, and Reciprocity on the Northwest Coast (2009) | 62 | 计入；单篇论证，已注明作者口径 |
  - 卫星遥感地表观测：无合格候选。
  - 第108轮收尾：层级 A{evs['A']} / B{evs['B']} / C{evs['C']} / D{evs['D']}；缺口 G1={gd['G1']} / G2={gd['G2']} / G3={gd['G3']}（G3a {sp['G3a']['count']} + G3b {sp['G3b']['count']}）/ G4=243；check.py 0 错误，check_links.py 0 断链，round100_consist.py 0 问题。
  - 下一轮起点（第109轮）：追卫星遥感地表观测；大分水岭、冲积平原换角度；笈多/巴西高原/拉普拉塔已多轮无解，除非有新渠道不再重复检索。
"""
    open(pr,"w",encoding="utf-8").write(txt)
