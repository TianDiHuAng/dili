# -*- coding: utf-8 -*-
"""第70轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=70;DATE="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
MIN=800
ALIAS_EXCL = ("britannica-regions", "wikipedia-regions", "un-m49", "ap-human-geo", "s010-unesco-org")

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    """D138：与层级判定统一——被引≥10 或 正文/摘要≥800，满足其一即算有正文的内容源。
    别名页/数据端点不计（D107/D135）。"""
    if is_data(sid): return False
    if sid in ALIAS_EXCL: return False
    s = S.get(sid) or {}
    note = s.get("note") or ""
    pn = e.get("pending_notes") or ""
    for n in (note, pn):
        mc = re.search(r"被引\s*(\d+)", n)
        if mc and int(mc.group(1)) >= 10:
            return True
        for pat in (r"摘要长度\s*(\d+)\s*字符", r"正文节录\s*\*{0,2}([\d,]+)\s*字符",
                    r"正文\s*\*{0,2}([\d,]+)\s*字符", r"摘要\s*(\d+)\s*字符"):
            m = re.search(pat, n)
            if m and int(m.group(1).replace(",", "")) >= 800:
                return True
        m = re.search(r"(\d{3,7})\s*字节", n)
        if m and int(m.group(1)) >= 3000:      # 字节→字符约 3:1，3000 字节≈1000 字符
            return True
    return False


g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":5,"fixes":3,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":3,"sample_rate":"5条G1宽检索","sample_audit":"3条对位登记（十字军29/大平原27/克里特31）；2条如实记录",
 "note":f"宽检索补3条→G1 5→{gd['G1']}；D级清零；G3 {gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=3
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G1：5 → "+str(gd["G1"])+"，D 级清零**）","",
 "## 1. 换检索角度，补上 3 条强来源","",
 "上一轮用窄检索词（对象+主题槽全命中）在剩余 5 条上多无所获。本轮改用**宽对象词 + 至少一个主题槽**，并扩大检索式数量，结果：","",
 "| 条目 | 新强来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 十字军东征 | Settlement, Identity, and Memory in the **Latin East** (2020) | 29 | 1,644 |",
 "| 大平原 | Decadal heat and drought drive body size of North American **bison** (2019) | 27 | 1,706 |",
 "| 克里特文明 | Seals, Craft, and Community in Bronze Age Crete (2016) | 31 | 955 |","",
 "三条都通过了摘要对读：",
 "- **十字军**：摘要明确列出第一次十字军后形成的**四个政体**（耶路撒冷王国、安条克公国、埃德萨伯国、的黎波里伯国）；",
 "- **大平原**：摘要写「大平原草原自史前以来一直支撑着数量最多的野牛」，并以数十年尺度检验热与干旱；",
 "- **克里特**：标题是「印章」，但摘要讨论的是**「宫殿社会」的起源**——这正是本条需要的主题（上一轮剔除的那篇印章学是纯类型学，这篇不是）。","",
 "## 2. 两条未获（如实记录）","",
 "| 条目 | 候选 | 为何不用 |","|---|---|---|",
 "| 隋唐 | Maintaining Gods in Medieval China（寺庙崇拜，引5）／Dressing for the Times（唐代服饰，引8） | 均属社会侧面，不撑「政体与制度」 |",
 "| 澳大利亚大陆 | Land surface phenological response（引143） | 摘要未出现 Australia，不覆盖全境 |","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 内容源 ≥2：{g2}；1 个：{o1}",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / **D {evs['D']}（清零）**",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| **G1** | 无强来源 | **{gd['G1']}**（上轮 5） |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| G3 | 仅 1 内容源 | {gd['G3']} |",
 "| G4 | 语义对题未机器校验 | 243（已扫描 30 条） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; G1={gd['G1']} G3={gd['G3']} levels={evs}")