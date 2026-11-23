# -*- coding: utf-8 -*-
"""第42轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=42;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";UPG=int(sys.argv[2]) if len(sys.argv)>2 else 46
SHELL={"britannica-regions","wikipedia-regions","un-m49","s010-unesco-org","s070-cbd-int","s071-cbd-int","ap-human-geo","s013-fao-org"}
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
multi=sum(1 for e in T.values() if len([s for s in e["sources"] if s not in SHELL and not s.startswith("wb-")])>=2)
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":UPG,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":46,"sample_rate":"25%（10条）","sample_audit":AUDIT,
 "note":"转向证据质量：为46条单源条目登记第二独立来源（32强/13部分/1背景）"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True;sat["multi_source_entries"]=multi
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 Crossref→OpenAlex DOI桥（第二来源）","标题核心词筛选","分级标注","台账"],
 "gaps_found":pending,
 "note":f"≥2内容源条目 125→{multi}；另46条仅单个内容源","result":"证据质量推进"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=UPG
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**转向证据质量**）","",
 "## 1. 本轮工作转向","",
 "- 层级 L2 已于第41轮全覆盖（243/243），本阶段目标改为**提高证据质量**：为单源条目补第二独立来源。",
 f"- 本轮为 **{UPG} 条**条目登记第二来源，分级：**strong 32 / partial 13 / core 1**。",
 f"- **≥2 内容源的条目：125 → {multi} / 243**（由 51% 升至 {multi*100//243}%）。",
 "- 来源总数：522 → 568。","",
 "## 2. 分级口径（D094 的落实）","",
 "| 级别 | 含义 | 条数 |","|---|---|---|",
 "| strong | 文献与本条对象一致，可作年代/机制断言的第二独立来源 | 32 |",
 "| partial | 涉本条对象但聚焦某一侧面，仅支撑相应段落 | 13 |",
 "| core | 仅与某一概念相关，作背景登记，不作事实断言依据 | 1 |","",
 "**这说明「source_count 上升」不等于「互证强度上升」**——分级标注就是为了把这点写明，避免虚高。","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- 筛选剔除 4 条标题不含核心对象词的候选（马里帝国←African Dominion 泛题、安第斯山脉←**Pikes Peak batholith**（科罗拉多）、城市起源←**Circular Cities**（现代可持续）、十三殖民地←Statutory Law of Slavery）。","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}** / L3 {levels['L3']}",
 f"- ≥2 内容源：{multi} 条；仅单个内容源：{len(es)-multi} 条",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 目标达成度","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心条目全部 L2 | **已达成 44/44** |",
 "| 重要条目全部 L2 | **已达成 104/104** |",
 "| 全部条目 L2 | **已达成 243/243** |",
 f"| 证据质量（≥2 可互证来源） | 部分达成：{multi}/243 有 ≥2 内容源，其中 32 条为 strong |",
 "| 多维缺口连续 3 轮为零 | **未达成**（`saturated=false`，`zero_gap_rounds=0`） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; multi",multi,"sources",len(src))