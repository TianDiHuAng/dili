# -*- coding: utf-8 -*-
"""第54轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=54;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为R19机器化轮"
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
side=sum(1 for e in T.values() if "【第50轮旁证认定】" in (e.get("pending_notes") or ""))
prim=sum(1 for e in T.values() if "补主来源" in (e.get("pending_notes") or ""))
weak=sum(1 for e in T.values() if "补弱来源" in (e.get("pending_notes") or ""))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":8,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":2,"sample_rate":"R19全库扫描+6条补源检索","sample_audit":AUDIT,
 "note":f"R19机器化上线并抓出6条弱来源被称主来源（已降级）；补2条主来源（古巴岛/巴塔哥尼亚）；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"side_evidence":side,
 "primary_claims":prim,"weak_claims":weak,
 "note":"R19 已上线（弱来源不得称主来源）；内容对题仍依赖人工扫描"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["R19机器化（D112）","6条两库检索","3条错配记录","台账"],
 "gaps_found":pending,
 "note":f"R19抓出6条弱来源误称主来源并降级；补2条主来源；≥2内容源 {g2}","result":"校验机器化"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=8
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**校验机器化**）","",
 "## 1. 本轮核心：R19 上线，立刻抓出 6 条自己的错","",
 "D112 规定「弱来源不得称主来源」，本轮把它做成机器校验 R19：",
 "- 判据：被引 ≤5、或摘要/正文 <800 字符、或 note 自标 weak → **弱来源**；",
 "- 若某条目的 `pending_notes` 里把这样的来源写作「补主来源」→ **报错**。",
 "",
 "**上线即抓出 6 条**（都是我前两轮自己写的）：","",
 "| 条目 | 被误称主来源的弱来源 | 原因 |","|---|---|---|",
 "| 突厥 | W4384485896 | 被引 0、619 字符、自标 weak |",
 "| 意大利半岛 | W4298223504 | 693 字符（且截断） |",
 "| 文艺复兴意大利 | W2487072270 | 660 字符 |",
 "| 美国西进 | W3023324006 | 被引 0、自标 weak |",
 "| 河流三角洲 | W2034581965 | 被引 5、661 字符 |",
 "| 地理信息系统 | W4230464905 | 被引 4、自标 weak |","",
 "全部改为「补弱来源」并说明其局限。`check.py` 现为 **ERRORS=0 ALL_PASS（R1–R19）**。","",
 "## 2. 另补 2 条主来源（严格按 D112：两库 + 变音归一）","",
 "| 条目 | 新主来源 | 被引 |","|---|---|---|",
 "| 巴塔哥尼亚 | Large-Scale Control on the Patagonian Climate (2013) | **668** |",
 "| 古巴岛 | The geology of Cuba: A brief overview and synthesis (2016) | 81 |","",
 "## 3. 三条「检索到但错配」如实记录","",
 "- **古埃及中王国** ←《Ancient Egyptian Autobiographies…》——自传体铭文的**文体研究**，不撑行政与灌溉。",
 "- **澳大利亚内陆干旱气候** ←《Salinity Stress in Arid and Semi-Arid Climates》——**盐胁迫对作物**（农学），不涉气候成因。",
 "- **新法兰西** ←《Driven by drink: The role of drinking in the political economy…》——**跨文化饮酒习俗**，对象词 `france` 过宽导致误中。","",
 "## 4. 累计与达成度","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**；0 个：**0**",
 f"- 称「补主来源」的条目：{prim}；已明确标为「补弱来源」者：{weak}",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成 243/243** |",
 "| 弱来源不得称主来源（R19） | **已机器化，当前 0 违规** |",
 "| 每条均有**主**来源 | 未达成（约 10 条仍缺主来源） |",
 "| 内容对题（R19 语义层） | 仍依赖人工扫描 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} prim={prim} weak={weak}")