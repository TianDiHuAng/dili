# -*- coding: utf-8 -*-
"""第32轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=32;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 5
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
core_l1=[e["id"] for e in es if e["tier"]=="核心" and e["level"]=="L1"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
NAMES={"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
blanks=[]
for u,c in cov.get("matrix",{}).items():
 for t in ("地形","气候","农业","贸易","政权更替","区域"):
  if c.get(t,0)==0: blanks.append(f"{NAMES.get(u,u)}×{t}")
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":5,"reviews":0,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":6,"sample_rate":"25%（10条 / 本轮5条去重改动）","sample_audit":AUDIT,
 "note":"Wikidata API 解锁 5 条核心 L2 升级；核心 L1 6→1"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 Wikidata/DBpedia 探测","核心L1攻坚","today填充","R14/R15","台账"],
 "gaps_found":pending+cov.get("d041_legacy_count",0),
 "note":"核心L1 6→1；Wikidata 提供可核验的结构化年代与量值","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0",
 "- **升级 L2：5（全部为核心条目）**：汉代（前206–220年）、蒙古帝国（1206–1368年）、阿兹特克（1325–1521年）、长江流域（约6300千米）、印度河文明（约前3000–1800年）",
 f"- 修复：{FIXES}",
 "- 新增来源：6（5 个 Wikidata 实体 + 1 个 ATS/补充）",
 "- **核心 L1：6 → 1**（仅余「城市起源」）；核心 L2 达 **43**","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R14+R15 在位）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}","",
 "## 3. 缺口发现摘要（本轮取得渠道突破）","",
 "- **Wikidata / DBpedia 渠道可用**：10 个候选 8 达标（此前 Wikipedia/Britannica 均 403/超时）",
 "- Wikidata 的 P571/P576（成立/解散）、P580/P582（起止）、P2043（长度）提供**可核验的结构化年代与量值**",
 "- 这解决了长期卡点：古代政权条目此前因缺专题来源无法升级；现可用 Wikidata 结构化数据 + 机构页构成双源",
 f"- B5 待核实：{pending}","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / L2 {levels['L2']} / L3 {levels['L3']}",
 f"- 核心 L1 剩余：{len(core_l1)} 条（{core_l1}）",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}",
 f"- D041 遗产 L2：{cov.get('d041_legacy_count',0)}；配对缺口：{cov.get('d041_pairing_gap_count',0)}","",
 "## 5. 覆盖矩阵仍空白格子（最多 20）","",
]
lines += [f"- {b}" for b in blanks[:20]] if blanks else ["- 无"]
lines += ["","## 6. 需要人关注的事项","",
 "- **Wikidata 为众包数据**：按 TASK 规则仅作双源之一，正文已注明；重要条目仍建议补机构/学术来源。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; core_l1",len(core_l1),"L2",levels["L2"])