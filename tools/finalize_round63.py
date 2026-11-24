# -*- coding: utf-8 -*-
"""第63轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=63;DATE="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
es=cov["entries"]
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    if is_data(sid): return False
    for note in [(S.get(sid) or {}).get("note") or "", e.get("pending_notes") or ""]:
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"9条政权类全查","sample_audit":"R22 主动检出3条层级落后并已重算",
 "note":f"补4条第二来源（阿兹特克/阿拉伯半岛/马格里布/汉代）；G3 19→{gd['G3']}；层级 A{evs['A']}/B{evs['B']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3 推进**）","",
 "## 1. 补 4 条第二来源（G3：19 → "+str(gd["G3"])+"）","",
 "| 条目 | 新第二来源 | 被引 |","|---|---|---|",
 "| 阿拉伯半岛 | Recent climate change in the Arabian Peninsula (2012) | **396** |",
 "| 阿兹特克 | Aztec city-state capitals (2008) | **202** |",
 "| 马格里布 | The Invention of the Maghreb (2021) | 62 |",
 "| 汉代 | Fortified settlements…Northern Zone (2014) | 17 |","",
 "## 2. R22 主动抓到我自己的滞后","",
 "补完来源后 `check.py` 立刻报：汉代、阿拉伯半岛、马格里布三条「层级记录为 B，按来源重算应为 A」。",
 "**这正是 R22 的设计意图**——来源变了而层级没更新，此前只能靠人记得去重算。重算后：**A 211 / B 31 / C 0 / D 1**。","",
 "## 3. 未获第二来源的（如实记录）","",
 "| 条目 | 状况 |","|---|---|",
 "| 古埃及新王国 | 候选是《Literacy and Ancient Egyptian Society》——讲**埃及文字与社会**，不专新王国，仅可作背景 |",
 "| 周代 | 11 条候选无一条同时满足「标题含 zhou」与两个主题槽 |",
 "| 桑海帝国 | 3 条候选无过筛者 |",
 "| 笈多王朝 | 7 条候选无过筛者 |",
 "| 加纳帝国 | 命中的仍是已登记的 W2010072736，非第二来源 |","",
 "## 4. 缺口现状","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| G1 | 无强来源 | {gd['G1']} |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| **G3** | 仅 1 内容源 | **{gd['G3']}**（本轮 −4） |",
 "| G4 | 语义对题未机器校验 | 243 |","",
 "## 5. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R22）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 条目 {len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；全部 L2",
 f"- 内容源 ≥2：**{g2}**（较上轮 +4）；1 个：{o1}",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心/重要/全部 243 条 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成** |",
 "| 证据层级 C 级清零 | **已达成** |",
 "| R19–R22 四道机器校验 | 均已上线，0 违规 |",
 f"| G1 无强来源 | {gd['G1']} 条 |",
 f"| G3 仅 1 内容源 | {gd['G3']} 条 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} G3={gd['G3']} levels={evs}")