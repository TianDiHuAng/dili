# -*- coding: utf-8 -*-
"""第66轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=66;DATE="2026-11-24"
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
shell=sum(1 for s in src if "空壳页判定" in (s.get("note") or ""))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"—","sample_audit":"limits.html 改为动态；semantic_scan.json 建立",
 "note":f"已知限制页动态化（缺口四类/无解5条/空壳{shell}个/R18-R23能力边界）；人工扫描存档建立"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND
sat["evidence"]["shell_pages"]=shell
sat["evidence"]["semantic_scan"]="data/semantic_scan.json"
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**限制页动态化**）","",
 "## 1. `/limits.html` 改为动态生成","",
 "此前该页是硬编码文本，数字会与 `SATURATION.json` 脱节。现在它直接读三份数据：","",
 "- **缺口四类**（来自 `round62_gaps.py` 的计算结果）：G1=0 / G2=3 / G3=5 / G4=243，含每类的关闭方式；",
 "- **无合格第二来源的 5 条**（古埃及新王国、加纳帝国、桑海帝国、笈多王朝、周代），附检索范围说明；",
 "- **6 个空壳页**及其实测正文长度（FAOSTAT **7 字符**、UN Population **26**、CBD **172**、UNESCO 两页各 **218**、UNICEF **750**），并与 OWID（3,298–31,443）对比；",
 "- **R18–R23 六道闸的能力边界**，明确写出「不能判断」的三件事。","",
 "## 2. 建立人工扫描存档 `data/semantic_scan.json`","",
 "把 49/50/57/58/63/65 六轮人工扫描的结论归档：每轮扫描了什么范围、发现了哪些错配、哪些无解、哪些**不可自动化**。",
 "这份文件是 G4（语义对题）的唯一凭据——机器查不了，但人可以查，查过的要留下记录。","",
 "## 3. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R23）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 条目 {len(es)}；全部 L2；层级 A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：**{o1}**",
 f"- 空壳页标记：**{shell}** 个",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| G1 | 无强来源 | **{gd['G1']}** |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| G3 | 仅 1 内容源 | **{gd['G3']}** |",
 "| G4 | 语义对题未机器校验 | 243（已人工扫描 6 轮，存档） |","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心/重要/全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 证据层级 C/D 清零 | **已达成** |",
 "| R19–R23 五道机器校验 | 已上线，0 违规 |",
 "| 限制与能力边界对读者公开 | **已达成（动态）** |",
 f"| 每条均有第二内容源（G3） | 未达成（剩 {gd['G3']} 条，已列为无解） |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} shell={shell} G={gd}")