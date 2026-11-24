# -*- coding: utf-8 -*-
"""第69轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=69;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":10,"fixes":5,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":5,"sample_rate":"10条G1全查","sample_audit":"被引1145/398/169/82/24等；R25拦下1条书评(标题即书名)",
 "note":f"补5条强来源→G1 10→{gd['G1']}；R25拦下「标题即书名」的书评；G3 {gd['G3']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=5
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**G1：10 → "+str(gd["G1"])+"**）","",
 "## 1. 为 G1 十条找真正的强来源","",
 "| 条目 | 新强来源 | 被引 |","|---|---|---|",
 "| 玛雅文明 | Climate and the **Collapse of Maya Civilization** (2003) | **1145** |",
 "| 维京时代 | Population genomics of the Viking world (2020) | **398** |",
 "| 澳大利亚原住民 | Visions from the Past: Archaeology of Australian Aboriginal Art (2002) | 169 |",
 "| 印加帝国 | Segmentary State Formation and the Ritual Control of Water (1993) | 162 |",
 "| 孔雀王朝 | The Mauryan empire in early India (2006) | 24 |","",
 "**G1：10 → "+str(gd["G1"])+"**；层级 A 119 / B 119 / C 3 / D 2。","",
 "## 2. 一条重要教训：书评的标题可能就是书名","",
 "我为「隋唐」检索到一个看起来完美的候选：《Son of Heaven and Heavenly Qaghan: Sui-Tang China and Its Neighbors》(1999, 被引 82)。",
 "**标题就是那本书的书名**——但它是一条 **book-review**，即对这本书的**书评**，不是书本身。",
 "R25 当场报错拦下，我随即清理了据此写下的落点句（否则又是一次「用书评撑正文」）。",
 "教训：**不能凭标题判断一条记录是著作还是书评**，必须看 `type`（D136）。","",
 "## 3. 四条未获强来源（如实记录）","",
 "| 条目 | 候选 | 为何不用 |","|---|---|---|",
 "| 澳大利亚大陆 | Refining Rodinia: Australia–Western U.S. connection (1999, 引668) | 讲**前寒武超大陆拼合**，不支撑大陆地形气候总体 |",
 "| 十字军东征 | Commerce of Amalfi **Before the Crusades** (1968, 引155) | 时段是「十字军**之前**」，D108 时期槽否决 |",
 "| 大平原 | Water quality in the **Canadian** Great Plains (1999, 引407) | 只涉加拿大段水质，与农业/野牛/交通/沙尘暴无对应 |",
 "| 克里特文明 | The Volcanic Destruction of Minoan Crete (**1939**, 引224) | 对象对位但为 1939 年火山摧毁说，学界后多修正 |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 内容源 ≥2：{g2}；1 个：{o1}",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| **G1** | 无强来源 | **{gd['G1']}**（上轮 10） |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| G3 | 仅 1 内容源 | {gd['G3']} |",
 "| G4 | 语义对题未机器校验 | 243（已扫描 30 条） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; G1={gd['G1']} G3={gd['G3']} levels={evs}")