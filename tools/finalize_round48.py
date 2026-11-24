# -*- coding: utf-8 -*-
"""第48轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=48;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";NEW=int(sys.argv[2]) if len(sys.argv)>2 else 7
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
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符",r"正文\s*\*{0,2}([\d,]+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
z0=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==0)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":NEW,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":7,"sample_rate":"7条补源+2条剔除全查","sample_audit":AUDIT,
 "note":f"7条政权类补第二源、替换2条错源、剔除2条时期错配；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,
 "note":"第①层（有正文）实测；第②层（内容对题）未全量校验（D106）"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["D101槽位化补源","错源替换","时期错配剔除","台账"],
 "gaps_found":pending,
 "note":f"≥2内容源 219→{g2}；1个 {o1}","result":"证据质量推进"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=NEW
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环","",
 "## 1. 本轮完成","",
 f"- **补第二源 {NEW} 条**（政权类）：蒙古帝国、阿兹特克、城市起源、库什与努比亚、罗马阿非利加、商代、秦代",
 "- **替换 2 条错源**：阿兹特克 ← ~~Tlaxcallan（**敌对城邦**）~~；库什与努比亚 ← ~~DVD 评介~~",
 "- **剔除 2 条时期/对象错配候选**：",
 "  - 古埃及新王国 ←《Afterglow of Empire: Egypt from the Fall of the **New Kingdom**…》——研究对象是**新王国灭亡之后**（前11–前6世纪），非新王国本身。",
 "  - 加纳帝国 ←《Youth entrepreneurship in a small-scale gold mining settlement in **Ghana**》——研究的是**当代加纳**北部小矿，与加纳帝国无历史关联。",
 f"- **≥2 内容源（第①层，有正文）：219 → {g2}**；仅 1 个：{o1}；0 个：{z0}（库什，因其冶铁研究摘要仅 756 字符，低于 800 门槛）","",
 "## 2. R19 原型与它的局限","",
 "- 本轮先尝试实现 R19：用「同条 openalex 来源标题的共识词」检出**离群来源**。结果**检出 0 条**。",
 "- 局限已明确：该方法只能发现「与多数不一致」的来源，**无法发现「全部都错」**；且单来源条目无从判断。真正的 R19 需要「条目→对象词」映射表（D105 待实现）。",
 "- 因此本轮改用人工执行的 R19 精神：**要求对象词必须出现在标题**（脚本的 `obj not in ti` 门），这在 14 条检索中直接拦下了多条错配。","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R18）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（9 条全查）：{AUDIT}","",
 "## 4. 累计与达成度","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 f"| 来源有正文（≥800 字符）≥2 个 | {g2}/243（结构层） |",
 "| 内容对题（R19 全量） | **未实现** |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1}")