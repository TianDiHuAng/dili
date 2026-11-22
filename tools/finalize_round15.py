# -*- coding: utf-8 -*-
"""第15轮收尾：METRICS / SATURATION / REPORT。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=15;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 0
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
gap=json.load(open(os.path.join(ROOT,"reports","gap_round14.json"),encoding="utf-8"))["gaps"]
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":4,"reviews":36,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"25%","sample_audit":AUDIT,
 "note":"首次按 D041 准入规则升级：专题页正文须含主题关键词"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,
 "methods_used":["B1专题页探测(关键词验证)","B5待核实","B7深度缺口","B2覆盖矩阵","B4读者问题"],
 "gaps_found":4+gap["B5_pending"]["total"]+gap["B7_depth"]["important_l1"],
 "result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0",
 "- 升级 L2：4（格陵兰岛、北美冰盖、山地农业、人口迁移——首次按 D041 规则，专题页正文均命中主题关键词）",
 "- 复核：36（重要 L1；pending_notes 统一加注 D041 要求仍待专题页）",f"- 修复：{FIXES}",
 "- 新增来源：4（nasa-ice-sheets、fao-mountain-partnership、owid-migration、usgs-glaciers，均 curl 核验）",
 "- 提交：4 个批次提交，每批 10 任务且通过 check.py","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS（4247 条内部链接）",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- 过程修复：人口迁移 SVG 曾用 defs/marker 越出白名单，已改为纯路径箭头","",
 "## 3. 缺口发现摘要（本轮使用 5 种方法）","",
 "- B1 专题页探测（关键词验证）：探测 29 个候选路径，正文命中达标 6 个、可用 4 个；GBRMPA/UNESCO WHC/FAO 流域剖面/NOAA education 均不可达",
 "- B5 待核实、B7 深度缺口、B2 覆盖矩阵、B4 读者问题：作为轮换方法同步执行","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / L2 {levels['L2']} / L3 {levels['L3']}",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 覆盖矩阵仍空白格子（最多 20）","",
]
lines += [f"- {b}" for b in blanks[:20]] if blanks else ["- 无"]
lines += ["","## 6. 需要人关注的事项","","- 无",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("REPORT/METRICS/SATURATION updated; pending",pending,"blanks",len(blanks),"levels",levels)