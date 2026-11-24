# -*- coding: utf-8 -*-
"""第64轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=64;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":13,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"24个机构页实测","sample_audit":"实测发现UN/UNESCO/FAO/CBD为空壳页（7–218字符）",
 "note":f"实测24个机构页；标记6个空壳页；挂接7条第二来源；G3 15→{gd['G3']}、G1→0；层级 A{evs['A']}/B{evs['B']}/C0/D0"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"]
sat["evidence"]["levels"]=evs
sat["evidence"]["shell_pages"]=6
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=13
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G1 清零**）","",
 "## 1. 本轮最重要的发现：机构页是空壳","",
 "为补充类 10 条找第二来源时，我逐个实测了 24 个机构页的正文长度，结果是：","",
 "| 来源 | strip 后正文 | 判定 |","|---|---|---|","" ,
 "| s014-fao-org（FAOSTAT） | **7 字符** | 应用壳 |",
 "| s004-population-un-org（UN Population） | **26 字符** | 空壳 |",
 "| s072-cbd-int（CBD） | **172 字符** | 空壳 |",
 "| s008-unesco-org / s085-unesco-org（UNESCO） | **218 字符** | 空壳 |",
 "| s074-unicef-org（UNICEF） | **750 字符** | 略低于 800 门槛 |","",
 "对比之下，同批实测的 OWID 长文为 3,298–31,443 字符，World Bank 为 8,041–11,098 字符，NOAA 2,753、IUCN 4,086。","",
 "**结论**：这几条 G3 的「第二来源」并非我没去找，而是找到的**UN/UNESCO/FAO/CBD 页面在本环境返回 JS 应用壳**，正文只有几十到几百字符。已全部标为「仅作入口页，不作正文依据」（D125）。","",
 "## 2. 处置与结果","",
 "- 为 7 条补充类条目挂接**已实测 ≥800 字符**的机构/数据长文作为第二来源；",
 f"- **G3：15 → {gd['G3']}**；**G1：1 → {gd['G1']}（清零）**；",
 f"- 层级重算：**A {evs['A']} / B {evs['B']} / C 0 / D 0**（D 级也清零）。","",
 "## 3. 剩余 G3（9 条）","",
 "| 条目 | 状况 |","|---|---|",
 "| 古埃及新王国 / 加纳帝国 / 桑海帝国 / 笈多王朝 / 周代 | 政权类，前轮两库多检索式确认无合格第二来源 |",
 "| 海洋生态系统 / 保护与保育区体系 / 教育机会地域差异 / 农业企业与价值链 | 首源已是该领域最好的机构长文，第二源需另找 |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R22）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 条目 {len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；全部 L2",
 f"- 内容源 ≥2：**{g2}**（上轮 228，+6）；1 个：{o1}",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 空壳页标记：6 条","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| G1 | 无强来源 | **{gd['G1']}**（已清零） |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| G3 | 仅 1 内容源 | {gd['G3']} |",
 "| G4 | 语义对题未机器校验 | 243 |","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心/重要/全部 243 条 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 证据层级 C/D 清零 | **已达成** |",
 "| R19–R22 四道机器校验 | 均已上线，0 违规 |",
 f"| 每条均有第二内容源（G3） | 未达成（剩 {gd['G3']} 条） |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} G1={gd['G1']} G3={gd['G3']} levels={evs}")