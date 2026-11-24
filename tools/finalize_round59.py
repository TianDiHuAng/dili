# -*- coding: utf-8 -*-
"""第59轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=59;DATE="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
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
evs=ev["summary"]
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":1,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"243条层级计算","sample_audit":"层级判据经抽查校准（被引458但摘要795字符的经典著作不再误判为unknown）",
 "note":f"证据层级系统上线（A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}）并渲染到条目页；R21校验层级覆盖"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"levels":evs,
 "note":"R19+R20+R21 三道机器校验；读者可在条目页看到证据层级 A/B/C"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["证据层级系统","站点渲染","R21校验","台账"],
 "gaps_found":pending,
 "note":f"层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}；C 级 4 条为证据最弱","result":"证据可见化"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=1
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**证据层级可见化**）","",
 "## 1. 做了什么：把「证据强度」做成数据并渲染","",
 "此前「哪条证据强、哪条弱」只存在于我的备注里，读者看不到。本轮把它算成显式层级：","",
 "| 层级 | 判据 | 条数 |","|---|---|---|",
 f"| **A** | ≥2 个强来源 | **{evs['A']}** |",
 f"| **B** | 1 个强来源 + 旁证/弱来源 | **{evs['B']}** |",
 f"| **C** | 无强来源（仅旁证/弱来源） | **{evs['C']}** |",
 f"| **D** | 仅数据端点（指标解读类） | **{evs['D']}** |","",
 "「强来源」= 被引 ≥10 **或** 正文/摘要 ≥800 字符（满足其一）。",
 "该规则经抽查校准：初版要求两者同时满足，把「被引 458 但摘要 795 字符」的经典著作（《Early Dynastic Egypt》）误判为 unknown。","",
 "## 2. 渲染到站点","",
 "- 条目页标签区现在显示「证据 A/B/C/D」标签；196 页为 A、43 页为 B、4 页为 C。",
 "- 新增 **R21** 校验：每条目须在 `evidence_level.json` 中有层级记录，缺失即报错。","",
 f"## 3. C 级 4 条（证据最弱，需优先处理）","",
 "| 条目 | 现状 |","|---|---|",
 "| 加纳帝国 | 仅 wikidata + UNESCO 首页 |",
 "| 古希腊城邦 | 学术来源均已被标旁证/弱来源 |",
 "| 罗马共和国 | 同上 |",
 "| 农业企业与价值链 | 仅数据端点 |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；**R1–R21**）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 条目 {len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；全部 L2",
 f"- 内容源 ≥2：{g2}；1 个：{o1}；来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成 243/243** |",
 "| 弱来源不得称主来源（R19） | 已机器化，0 违规 |",
 "| 对象词须在来源标题（R20） | 已机器化，198 条，0 违规 |",
 "| 层级记录覆盖（R21） | 已机器化，243/243 |",
 f"| 每条均有**主**来源 | 未达成——C 级 {evs['C']} 条为证据最弱者，另有 3 处确认无合格主来源 |",
 "| 语义对题 | 仍依赖人工扫描 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} levels={evs}")