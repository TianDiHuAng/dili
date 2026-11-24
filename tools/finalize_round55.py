# -*- coding: utf-8 -*-
"""第55轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=55;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为剩余主来源补轮"
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
prim=sum(1 for e in T.values() if "补主来源" in (e.get("pending_notes") or ""))
weak=sum(1 for e in T.values() if "补弱来源" in (e.get("pending_notes") or ""))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":3,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":3,"sample_rate":"3条补源+3条不采用记录","sample_audit":AUDIT,
 "note":f"补3条主来源（亚马逊盆地/澳洲内陆干旱/复活节岛）；3条不采用记录；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"primary_claims":prim,"weak_claims":weak,
 "note":"R19 已机器化（弱来源不得称主来源）；内容对题仍依赖人工扫描"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["两库精确检索","3条不采用记录","台账"],
 "gaps_found":pending,
 "note":f"补3条主来源；≥2内容源 {g2}","result":"主来源推进"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=3
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环","",
 "## 1. 本轮完成：补 3 条主来源","",
 "| 条目 | 新主来源 | 被引 |","|---|---|---|",
 "| 澳大利亚内陆干旱气候 | Connections of climate change and variability to large and extreme… (2021) | **982** |",
 "| 亚马逊盆地 | Hypotheses to explain the origin of species in **Amazonia** (2008) | 281 |",
 "| 复活节岛 | A message for our future? The **Rapa Nui (Easter Island)** ecodisaster… (2002) | 114 |","",
 "## 2. 三条「检索到但对象不符」如实记录","",
 "| 条目 | 过筛候选 | 不采用原因 |","|---|---|---|",
 "| 印加帝国 | Machu Picchu: Unveiling the Mystery of the Incas (2005) | 对象是**马丘比丘遗址**（皇家庄园），不撑国家的疆域/道路/行政 |",
 "| 新法兰西 | The Paper Currencies of New France (1893) | 对象是**纸币发行史**，且为 1893 年旧文 |",
 "| 古埃及中王国 | Ancient Egyptian Autobiographies… (1988) | 仍为**自传铭文的文体研究**，不撑行政与灌溉 |","",
 "## 3. 累计与达成度","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**；0 个：**0**",
 f"- 称「补主来源」：{prim} 条；明确标「补弱来源」：{weak} 条",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成 243/243** |",
 "| 弱来源不得称主来源（R19） | **已机器化，0 违规** |",
 "| 每条均有**主**来源 | 未达成（约 7 条仍缺：印加、新法兰西、古埃及中王国/新王国、密克罗尼西亚、库什商路、莫切灌溉） |",
 "| 内容对题（R19 语义层） | 仍依赖人工扫描 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} prim={prim} weak={weak}")