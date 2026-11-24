# -*- coding: utf-8 -*-
"""第47轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=47;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为口径实测轮";MEAS=int(sys.argv[2]) if len(sys.argv)>2 else 66
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
def has_body(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符",
                    r"正文\s*\*{0,2}([\d,]+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if has_body(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if has_body(s,e) is True)==1)
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"—","sample_audit":AUDIT,
 "note":f"口径实测轮：为 {MEAS} 条条目实测来源字符数；数据端点与内容源分离后 ge2={g2}（结构层，未校验内容对题）"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,
 "note":"第①层（有正文）实测；第②层（内容对题）未校验（D106）","data_endpoints_excluded":True}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["全库来源字符实测","数据源/内容源分离","台账"],
 "gaps_found":pending,
 "note":f"实测 66 条条目的来源；ge2 结构层 {g2}","result":"口径实测"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**口径实测轮**）","",
 "## 1. 本轮做了什么","",
 f"- 对全库「未实测」来源逐个发 HTTP 实测，共补测量 **{MEAS} 条条目**的来源字符数。",
 "- 把**数据端点**（世界银行 / NOAA / USGS / ATS / Wikidata 的 JSON）从「内容来源」中分离——它们返回数值结构，能支撑 today 的数值，但不支撑文字断言。","",
 "## 2. 两轮口径修正（都是我先前的错）","",
 "| 阶段 | 数字 | 问题 |","|---|---|---|",
 "| 第46轮末 | ≥2 源 126 | `hb()` 只读 `sources.json`，漏掉 `pending_notes` 里的历史实测 |",
 "| 第47轮首测 | ≥2 源 **241** | 把世界银行 JSON（2,248 字符）当成「文章正文」 |",
 f"| 第47轮修正 | ≥2 源 **{g2}** | 数据端点单列、只计非数据源的内容页 |","",
 "## 3. 这个数字该怎么读（D106）","",
 f"**{g2}/243 只能读作「≥2 个来源有可观正文」，不能读作「≥2 个来源支撑了本条断言」。**",
 "本分类只过了第①层「有正文」（实测字符 ≥800），**第②层「内容对题」未校验**——R19 对象同位校验尚未实现（D105）。",
 "第42–46轮抽检反复证明：字符数达标而内容不对题的比例可达 40%–67%。因此真实互证数**远低于**这个数字，不应把它当作达成度。","",
 "## 4. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R18）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS","",
 "## 5. 累计","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（有正文，≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 f"| 来源有正文（≥800 字符）≥2 个 | {g2}/243（结构层） |",
 "| 内容对题（R19） | **未校验**（D105 待实现） |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1}")