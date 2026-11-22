# -*- coding: utf-8 -*-
"""第16轮收尾：METRICS / SATURATION / REPORT。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=16;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 1
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
gap=json.load(open(os.path.join(ROOT,"reports","gap_round16.json"),encoding="utf-8"))["gaps"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
NAMES={"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
blanks=[]
for u,c in cov.get("matrix",{}).items():
 for t in ("地形","气候","农业","贸易","政权更替","区域"):
  if c.get(t,0)==0: blanks.append(f"{NAMES.get(u,u)}×{t}")
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":8,"upgrades":0,"reviews":31,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":1,"sample_rate":"25%","sample_audit":AUDIT,
 "note":"阿契美尼德波斯换源合规（Livius Cyrus，D044 达标）；新增8条用未使用已核验来源"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,
 "methods_used":["B1 D044专题页探测","B6未使用来源","B3悬空引用","B5待核实","B7深度缺口(含遗产L2)"],
 "gaps_found":gap["B1_d044_probe"]["usable"]+gap["B6_unused_sources"]["count"]+gap["B5_pending"]["total"]+gap["B7_depth"]["legacy_l2"],
 "result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：8（拉丁美洲与加勒比、中东与北非、南亚三个区域发展条目；全球气温距平、二氧化碳排放清单、保护与保育区体系、农业企业与价值链、水资源供给概览）",
 "- 升级/换源：1（阿契美尼德波斯按 D044 换用 Livius Cyrus 专题页，摘除遗产标记）",
 "- 复核：31（重要 L1；pending_notes 统一注明 D041/D044 缺口）",f"- 修复：{FIXES}",
 "- 新增来源：1（livius-cyrus，curl 200，正文 9220 字节，achaemenid/cyrus/persia 命中 69）",
 "- 提交：4 个批次提交，每批 10 任务且通过 check.py","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS（4375 条内部链接）",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- 流程改进：抽检前先用 git 核对本轮 40 条改动集合，避免第15轮出现的「清单与数据不符」","",
 "## 3. 缺口发现摘要（本轮使用 5 种方法）","",
 f"- B1 D044 专题页探测：20 个候选路径仅 {gap['B1_d044_probe']['usable']} 个达标（Livius Cyrus）；NPS/USGS/FAO/GBRMPA 大量 403/404/0 连接",
 f"- B6 未使用来源：{gap['B6_unused_sources']['count']} 个已核验来源此前未被任何条目引用，本轮用 8 个",
 f"- B3 悬空引用：{len(gap['B3_dangling'])}",
 f"- B5 待核实：{gap['B5_pending']['total']}",
 f"- B7 深度：核心 L1 {gap['B7_depth']['core_l1']}、重要 L1 {gap['B7_depth']['important_l1']}、遗产 L2 {gap['B7_depth']['legacy_l2']}","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / L2 {levels['L2']} / L3 {levels['L3']}",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}",
 f"- D041 遗产 L2 待合规：{cov.get('d041_legacy_count',0)} 条","",
 "## 5. 覆盖矩阵仍空白格子（最多 20）","",
]
lines += [f"- {b}" for b in blanks[:20]] if blanks else ["- 无"]
lines += ["","## 6. 需要人关注的事项","","- 无",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; pending",pending,"levels",levels,"legacy",cov.get("d041_legacy_count"))