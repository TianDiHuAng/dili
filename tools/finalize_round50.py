# -*- coding: utf-8 -*-
"""第50轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=50;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为侧面文献处置轮"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
z0=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==0)
side=sum(1 for e in T.values() if "【第50轮旁证认定】" in (e.get("pending_notes") or ""))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":side+2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":2,"sample_rate":"30条侧面+2条主来源全查","sample_audit":AUDIT,
 "note":f"30条侧面文献标注旁证、2条核心补主来源（密西西比河/河流三角洲）；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"zero_has_body":z0,
 "side_evidence_annotated":side,
 "note":"第①层（有正文）实测；第②层（内容对题）已扫描196条并对30条侧面文献标注旁证"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["30条侧面文献标注","核心条目补主来源","台账"],
 "gaps_found":pending,
 "note":f"侧面文献 {side} 条已标注；2条核心补主来源；≥2内容源 {g2}","result":"证据分层"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=side+2
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**证据分层**）","",
 "## 1. 本轮做了什么","",
 f"- 为 **{side} 条**「侧面文献」条目逐条标注**旁证性质**：对象同一，但只涉该条目主题的一个侧面，不能作整条的主来源。",
 "  例：拜占庭←医院史、元代←高丽青瓷、印加←玉米酒、莫切←艺术图像、维京←婚姻与女性、美国西进←非裔史、阿塔卡马←岩内微生物、复活节岛←农业策略、密克罗尼西亚←珊瑚遗传。",
 "- 为核心 7 条补主来源，成功 **2 条**：",
 "  - **密西西比河** ←《Tritium hydrology of the Mississippi River basin》（2004, 被引 57）：氚示踪的干支流水文过程。",
 "  - **河流三角洲** ←《Mathematical modeling of the formation and progradation of a river mouth…》（2008）：河口沙坝形成与前积模型。","",
 "## 2. 未采用的候选（诚实记录）","",
 "| 条目 | 候选 | 未采用原因 |","|---|---|---|",
 "| 季风系统 | Eddy-Mediated Regime Transitions in the Seasonal Cycle of a **Hadley Circulation** | 研究的是**哈德莱环流**的季节循环，与季风（海陆热力差异驱动的风向反转）不是同一对象 |",
 "| 南极大陆 | Deglacial climate and ice sheet evolution of the **Ross Embayment** | 只覆盖**一个扇区**，不支撑「大陆」总体 |",
 "- 印加帝国、亚马逊盆地、文艺复兴意大利：三端口径下无合格候选（拒绝记录在 `reports/round50_primary.json`）。","",
 "## 3. 为什么「侧面文献」要单独标出","",
 "上一轮扫描发现：这些文献**对象没错**（确实讲拜占庭、确实讲元代），但讲的是**其中一个侧面**。若当作主来源，就会得出「拜占庭帝国=医院史」这种失真结论。",
 "按 D095② 的口径，它们只能算旁证；标注出来，读者能看到证据的真实强度。","",
 "## 4. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R18）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS","",
 "## 5. 累计与达成度","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**；0 个：**{z0}**",
 f"- 已标注侧面文献：**{side}** 条",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 f"| 来源有正文 ≥2 个 | {g2}/243（结构层） |",
 f"| 对象同位扫描 | 196 条已扫；错配 4 条已剔；**侧面 {side} 条已标注** |",
 "| 每条均有主来源 | **未达成**（约 28 条仍以侧面文献为主要来源） |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} zero={z0} side={side}")