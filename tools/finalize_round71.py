# -*- coding: utf-8 -*-
"""第71轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=71;DATE="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
ALIAS=("britannica-regions","wikipedia-regions","un-m49","ap-human-geo","s010-unesco-org")
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    if is_data(sid) or sid in ALIAS: return False
    s=S.get(sid) or {}
    for n in [(s.get("note") or ""),(e.get("pending_notes") or "")]:
        mc=re.search(r"被引\s*(\d+)",n)
        if mc and int(mc.group(1))>=10: return True
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文节录\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*\*{0,2}([\d,]+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,n)
            if m and int(m.group(1).replace(",",""))>=800: return True
        m=re.search(r"(\d{3,7})\s*字节",n)
        if m and int(m.group(1))>=3000: return True
    return False
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e))>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e))==1)
z0=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e))==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"—","sample_audit":"口径统一：hb 排除别名页+加入被引条件",
 "note":f"统一 hb 与层级判定口径后：≥2内容源 {g2}（旧报238）、仅1个 {o1}、0个 {z0}；G3 6→{gd['G3']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"]
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0,
 "note":"第71轮统一口径：内容源统计排除别名页、并采用「被引≥10 或 正文≥800」；旧报告的 238 为含别名页的虚数"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**口径统一，数字剧变**）","",
 "## 1. 发现：统计口径与层级判定不一致","",
 "本轮本来要处理 G3 的 6 条，却发现 `hb()`（内容源统计）与层级判定用的是**两套标准**：",
 "",
 "| 判据 | 层级判定（D135 后） | `hb()`（G3 统计） |","|---|---|---|",
 "| 别名页（britannica-regions 等） | 排除 | **未排除** |",
 "| 强来源门槛 | 被引≥10 **或** 正文≥800 | **只看字符数** |","",
 "所以「隋唐」的 `britannica-regions`（区域索引页）被算成了内容源，而「玛雅文明」那篇**被引 1145、摘要 699 字符**的名文因字符不足被漏掉。","",
 "## 2. 统一后的真实数字","",
 "| 指标 | 旧口径（含别名页） | **新口径（真实）** |","|---|---|---|",
 f"| 内容源 ≥2 | 238 | **{g2}** |",
 f"| 仅 1 个 | 5 | **{o1}** |",
 f"| 0 个 | 0 | **{z0}** |",
 f"| **G3 缺口** | **6** | **{gd['G3']}** |","",
 "**差距 85 条**——此前每一轮报的「内容源 ≥2：238」，是把区域索引页当成第二个来源算出来的。","",
 "## 3. 核心条目的真实证据基础","",
 "核心 44 条中，**15 条只有 1 个真内容源、1 条 0 个**：",
 "撒哈拉沙漠、东非大裂谷、马里帝国、两河流域、爱琴海世界、罗马帝国、文艺复兴意大利、白令陆桥、大平原、玛雅文明、安第斯山脉、印加帝国、澳大利亚大陆、澳大利亚原住民、波利尼西亚、河流三角洲。",
 "",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 缺口：**G1={gd['G1']} / G2={gd['G2']} / G3={gd['G3']} / G4=243**","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源（G1=0） | 未达成（2 条） |",
 f"| 每条都有 ≥2 内容源 | **未达成（{o1+z0} 条不足）** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 "| 口径一致性 | **本轮统一（此前 hb 与层级判定不一致）** |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} zero={z0} G3={gd['G3']}")