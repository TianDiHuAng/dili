# -*- coding: utf-8 -*-
"""第65轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=65;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":5,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"4条补充类全查","sample_audit":"R23上线；修s074测量口径冲突（5455 vs 750）",
 "note":f"补4条第二来源（海洋生态861/保护区244/教育53/农企72）；G3 9→{gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C0/D0"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"]
sat["evidence"]["levels"]=evs
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=5
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G3 降至 5**）","",
 "## 1. R23 上线：空壳页不得被称内容来源","",
 "上轮实测发现 UN/UNESCO/FAO/CBD 页面是空壳（7–218 字符）后，本轮把规则做成机器校验：",
 "- 若某来源 note 含「空壳页判定」，而条目备注里把它称作「第二来源/互证/内容来源/主来源」→ 报错。",
 "- 结果 0 违规，`check.py` 现为 **R1–R23**。","",
 "## 2. 修出一处测量口径冲突","",
 "`s074-unicef-org` 的 note 里同时有「正文 5,455 字符」（文本提取口径）与第64轮 strip 后的 **750 字符**。两值都真实，但**口径不同**。已注明：以 strip 值为准，750 < 800，故仅作入口页与案例引用。","",
 "## 3. 补 4 条第二来源（G3：9 → "+str(gd["G3"])+"）","",
 "| 条目 | 新第二来源 | 被引 | 适用范围 |","|---|---|---|---|",
 "| 海洋生态系统 | Assessment of Marine and Coastal Ecosystem Services (2013) | **861** | 全球评述 |",
 "| 保护与保育区体系 | Effectiveness of Marine Protected Areas in the Philippines (2010) | 244 | **菲律宾个案** |",
 "| 农业企业与价值链 | Contract farming in Indonesia (2004) | 72 | **印尼个案** |",
 "| 教育机会地域差异 | Regional Inequality of Higher Education in China (2023) | 53 | **中国个案** |","",
 "**三条是个案**——落在正文时已明确写「该文是××个案，不代全球」。这是 D083④ 的要求：个案可作例证，不可当通例。","",
 "## 4. 剩余 G3 五条：全是政权类","",
 "古埃及新王国、加纳帝国、桑海帝国、笈多王朝、周代——此前已用两库、多条检索式检索，均无合格第二来源。按 D110 如实记录，不再重试同类检索。","",
 "## 5. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；**R1–R23**）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 条目 {len(es)}；全部 L2",
 f"- 内容源 ≥2：**{g2}**（上轮 234，+4）；1 个：**{o1}**",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| G1 | 无强来源 | **{gd['G1']}** |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| G3 | 仅 1 内容源 | **{gd['G3']}** |",
 "| G4 | 语义对题未机器校验 | 243 |","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心/重要/全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 证据层级 C/D 清零 | **已达成** |",
 "| R19–R23 五道机器校验 | 均已上线，0 违规 |",
 f"| 每条均有第二内容源（G3） | 未达成（剩 {gd['G3']} 条，全为政权类且已确认无解） |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} G3={gd['G3']} levels={evs}")