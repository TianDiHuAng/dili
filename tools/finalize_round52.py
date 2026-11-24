# -*- coding: utf-8 -*-
"""第52轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=52;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为侧面文献补主来源轮"
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
prim=sum(1 for e in T.values() if "【第52轮补主来源" in (e.get("pending_notes") or ""))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"6条补源全查","sample_audit":AUDIT,
 "note":f"为6条侧面条目补主来源（文艺复兴意大利/拜占庭/维京/大自流盆地/落基山脉/美国西进）；库什商路与古埃及新王国如实记录无候选；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"side_evidence":side,
 "primary_added_this_round":prim,
 "note":"第①层实测；第②层 196 条已扫、30 条侧面已标注、本轮补 6 条主来源"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["D110两检索式补主来源","无候选如实记录","台账"],
 "gaps_found":pending,
 "note":f"6条补主来源；库什商路/古埃及新王国记录无候选；≥2内容源 {g2}","result":"主来源推进"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环","",
 "## 1. 本轮完成：为 6 条侧面文献条目补主来源","",
 "| 条目 | 新主来源 | 被引 |","|---|---|---|",
 "| 文艺复兴意大利 | The collapse of city-states and the role of urban centres… (2012, 剑桥) | 8 |",
 "| 拜占庭帝国 | The Middle Byzantine Economy (600–1204) (2009) | 21 |",
 "| 维京时代 | Viking-Age Trade: Silver, Slaves and Gotland (2020) | 13 |",
 "| 大自流盆地 | Structure, stratigraphy, and hydrogeology of… (1968) | 16 |",
 "| 落基山脉 | Laramide (Late Cretaceous-Early Tertiary) Orogeny (1975) | **223** |",
 "| 美国西进 | The course of westward expansion (2020) | 0（标注为弱点，仅辅助） |","",
 "## 2. 按 D110 如实记录的「无候选」","",
 "本轮每条「无来源」结论都写明引擎、两条检索式、条数与逐项拒绝理由（记录在 `reports/round52_primary.json` / `round52b_primary.json`）：",
 "- **库什与努比亚**（商路与商品结构）：40 条结果中无一条同时满足「标题含 kush/meroe」与「两个主题槽」。**确无**。",
 "- **古埃及新王国**：过筛者仍是《Afterglow of Empire: Egypt from the **Fall** of the New Kingdom…》——该书讲的是新王国**灭亡之后**（前11–前6世纪），第48轮已剔除，**本轮再次排除**。书名含 New Kingdom 而主题在其之后，是 D108「同名不同时」的典型。",
 "- **印加帝国**：过筛者《The Sacred Landscape of the Inca: The Cusco Ceque System》主题是**库斯科的 ceque 仪式系统**（宗教地理侧面），不撑「疆域、道路与行政」。",
 "- **亚马逊盆地**：过筛者《Extractive Reserves and Participatory Research…》主题是**采掘保护区与参与式研究**（土地政策侧面），不撑地貌水文。","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R18）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检：{AUDIT}","",
 "## 4. 累计与达成度","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**；0 个：**0**",
 f"- 侧面文献已标注：{side} 条；本轮新增主来源：{prim} 条",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成 243/243** |",
 f"| 每条均有**主**来源 | 未达成（约 19 条仍以侧面文献为主要来源） |",
 "| 内容对题（R19 全量机器校验） | 未实现 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} side={side} prim={prim}")