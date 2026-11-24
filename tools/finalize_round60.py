# -*- coding: utf-8 -*-
"""第60轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=60;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":2,"sample_rate":"C级4条全查","sample_audit":"层级判据经段污染bug修复后重算",
 "note":f"C级清零：实测livius正文、补2条学术来源（加纳/罗马）、修层级判定段污染bug；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"levels":evs,
 "note":"层级 C 已清零；D 级 1 条为指标解读类"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["livius正文实测","补2条学术来源","层级判据修bug","台账"],
 "gaps_found":pending,
 "note":f"C级 4→0；层级 A{evs['A']}/B{evs['B']}/D{evs['D']}","result":"证据层级修正"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**C 级清零**）","",
 "## 1. C 级 4 条的处置","",
 "| 条目 | 处置 | 结果 |","|---|---|---|",
 "| 古希腊城邦 | livius-polis/athens/greece 实测正文 2,469 / 6,313 / 43,476 字符 | 升为 A |",
 "| 罗马共和国 | livius-roman-republic 实测 25,552 字符 | 升为 A |",
 "| 加纳帝国 | 补《Archaeology and the prehistoric origins…》(1980, **被引107**, 摘要 1,265 字符) | 升为 A |",
 "| 农业企业与价值链 | 判定为**指标解读类**（worldbank + FAOSTAT + 数据端点） | 归入 D |","",
 "## 2. 修出一个层级判定 bug：段污染","",
 "初版 `grade_of()` 取 `pending_notes` 中 sid 附近的**字符窗口**判断「旁证/剔除」。但加纳帝国历史上剔除过多条来源，那些「剔除」字样落在了新补来源的窗口内 → **新来的强来源被误判为旁证**，条目仍停在 C。",
 "修法：**按【】分段**，只在该 sid 自己所属的段落里判断。","",
 "重算后：**A 207 / B 35 / C 0 / D 1**。","",
 "## 3. 另一处实测陷阱","",
 "- livius 页面的第二次实测部分返回 HTTP 0（连接波动）。若照写会把有正文的页面记成「0 字符」——已改用**首次成功值**并注明波动。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R21）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 条目 {len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；全部 L2",
 f"- 内容源 ≥2：{g2}；1 个：{o1}；来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成 243/243** |",
 "| 证据层级 C 级清零 | **已达成（C=0）** |",
 "| R19 / R20 / R21 | 均已机器化，0 违规 |",
 f"| 每条均有**主**来源 | 未达成（D 级 1 条为指标解读类；另有 3 处确认无合格主来源） |",
 "| 语义对题 | 仍依赖人工扫描 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} levels={evs}")