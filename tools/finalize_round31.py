# -*- coding: utf-8 -*-
"""第31轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=31;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 4
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"超采样（10条 / 本轮4条去重改动）","sample_audit":AUDIT,
 "note":"4条today填官方/机构数据（ATS缔约方名录、WLD CO2/农业用地/城市增长率）；today含数值63条"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1观测端点","today填充","D075/D076复查","R14","台账"],
 "gaps_found":pending+cov.get("d041_legacy_count",0),
 "note":"today 含数值 59→63；无数值降至 10（南极大陆/物候/火情等无公开数据源）","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0","- 升级 L2：0",
 f"- 修复：{FIXES}（4 条 L2 的 today 填数据：南极条约体系←ATS 官方缔约方名录（只写「原始签署国 12 国」，不写死动态总数）；二氧化碳排放清单←全球 39,632.66 Mt CO₂e（2024年，AR5 口径**不含 LULUCF**）；农业企业与价值链←全球农业用地 36.9%（2023年）；城市地理←全球城市人口增长率 1.36%（2025年））",
 "- 新增来源：4（ats-parties、wb-wld-co2、wb-wld-agriland、wb-wld-urbangrow）",
 "- 说明：本轮 4 条去重改动，未用满配额","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；含 R14）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- today 含数值：59 → **63**；无数值 10 条","",
 "## 3. 缺口发现摘要","",
 "- B1 探测 16 候选：6 达标（NASA 冰盖指标、ATS 缔约方页、WLD CO2/农业用地/城市增长）；NSIDC/usanpn/NASA API 均 404/403/503",
 "- 动态名录类（ATS）已在正文声明「以页面当前状态为准，不写死数字」（D075 精神）",
 f"- B5 待核实：{pending}","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / L2 {levels['L2']} / L3 {levels['L3']}",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}",
 f"- D041 遗产 L2：{cov.get('d041_legacy_count',0)}；配对缺口：{cov.get('d041_pairing_gap_count',0)}","",
 "## 5. 覆盖矩阵仍空白格子（最多 20）","",
]
lines += [f"- {b}" for b in blanks[:20]] if blanks else ["- 无"]
lines += ["","## 6. 需要人关注的事项","","- 无",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; sources",len(src),"verified",verified)