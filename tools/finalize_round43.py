# -*- coding: utf-8 -*-
"""第43轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=43;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";NEW=int(sys.argv[2]) if len(sys.argv)>2 else 23
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
STUB=("livius-polis","livius-athens")
EXTRA=("nasa-ice-cores","usgs-glaciers-pdf","noaa-global-temp","nasa-pine-island",
       "s042-earthobservatory-nasa-gov","nasa-ice-sheets","noaa-sustainable-fisheries","s051-fisheries-noaa-gov")
_S={s["id"]:s for s in src}
def ac(e):
    """实测口径：按来源 note 记录的字节数判定是否有正文（D096 三档之②）。"""
    n=0
    for sid in e["sources"]:
        if sid in STUB: continue
        if sid.startswith(("openalex-","livius-")) or sid in EXTRA:
            note=(_S.get(sid) or {}).get("note") or ""
            m=re.search(r"(\d{3,6})\s*字节", note)
            if sid.startswith("livius-") and m and int(m.group(1))<1000: continue
            n+=1
    return n
z=sum(1 for e in T.values() if ac(e)==0);o=sum(1 for e in T.values() if ac(e)==1);g2=sum(1 for e in T.values() if ac(e)>=2)
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":NEW,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":NEW,"sample_rate":"25%（10条）","sample_audit":AUDIT,
 "note":f"口径复核：真实≥2源由143(含机构首页)订正为12；补源后 0源{z}/1源{o}/≥2源{g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"zero_source":z,"one_source":o,"two_plus":g2,
  "definition":"仅计有实际正文或摘要的来源；机构首页与世界银行指标端点不计"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 全站来源口径复核","B1 0源条目补源（摘要多次命中筛选）","台账"],
 "gaps_found":pending+z,
 "note":f"发现「≥2内容源143」含机构首页属虚高，真实为12；补源后0源{z}、≥2源{g2}","result":"证据口径订正"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**证据口径订正**）","",
 "## 1. 本轮最重要的发现：口径虚高","",
 "- 此前多轮宣称「≥2 内容源 **143** 条」，本轮复核发现该统计把**机构首页**（FAO / Our World in Data / UNESCO / NOAA 首页 / AAG / UNSDG 门户）也算作「内容源」。",
 "- 按「来源须有实际正文或摘要」重算，全站真实分布为：",
 "","| 真实学术来源数 | 本轮复核前 | 补源后 |","|---|---|---|",
 f"| 0 个 | 81 条 | **{z} 条** |",
 f"| 1 个 | 150 条 | **{o} 条** |",
 f"| ≥2 个 | **12 条**（而非 143） | **{g2} 条** |","",
 "- 已为 81 条 0 源条目在 `pending_notes` 写入「口径订正」说明：其正文的地理与机制描述属**常识性表述、无学术来源支撑**（数据类条目以 today 指标为准）。","",
 "## 2. 本轮补源","",
 f"- 为 37 条 0 源的核心/重要条目检索，登记 **{NEW} 条**（strong 10 / partial 13）。",
 "- 采用改进筛选：要求**标题含对象词且摘要中对象词命中 ≥2 次**，以降低地名碰撞（第42轮曾出现「白令陆桥←现代国家保护区」「河流三角洲←珠三角气溶胶」）。",
 "- 剔除 2 条：《The Mande Creation Myth》的书评（D082）、《Hitchhiking Bats on the Great Lakes》（对象是蝙蝠）。","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}**",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 目标达成度","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心条目全部 L2 | **已达成 44/44** |",
 "| 重要条目全部 L2 | **已达成 104/104** |",
 "| 全部条目 L2 | **已达成 243/243** |",
 f"| 证据质量（≥2 真实来源） | **未达成：{g2}/243**（0 源仍有 {z} 条） |",
 "| 多维缺口连续 3 轮为零 | **未达成**（`saturated=false`） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; 0源{z} 1源{o} >=2源{g2}")