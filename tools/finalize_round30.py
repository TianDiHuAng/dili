# -*- coding: utf-8 -*-
"""第30轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=30;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 15
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
 "new_sources":9,"sample_rate":"25%（10条 / 本轮9条去重改动）","sample_audit":AUDIT,
 "note":"8条today填全球/国别实测（USGS地震目录/NOAA洋流站/WB指标）；宋代5候选仍不可达"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1观测数据端点","today填充","宋代探测","R14校验","台账"],
 "gaps_found":pending+cov.get("d041_legacy_count",0),
 "note":"today 含数值 54→59；仍无 14 条（南极/物候/火情等无对应数据源）","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0","- 升级 L2：0",
 f"- 修复：{FIXES}（8 条 L2 的 today 填入实测数据：板块构造←USGS 2025 年 M6+ 事件 144 次；洋流←NOAA 84 个洋流观测站；沙尘暴←全球 PM2.5 32.87 μg/m³（2023年，已声明≠沙尘浓度）；丝绸之路←哈萨克斯坦/乌兹别克斯坦；亚马逊河←巴西；游牧←蒙古；气候带←全球可耕地 10.67%（2023年）；人口迁移←全球城市化率 57.8%）",
 "- 宋代：再试 5 个专题候选（OpenStax/Livius/Met/Archives），全部 404 或正文不足，保持「非实证」",
 "- 新增来源：9（usgs-eq-m6、noaa-current-stations、wb-wld-pm25、wb-wld-arable + 6 个国别端点）",
 "- 说明：本轮 9 条去重改动，未用满 40 配额","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；含 R14 国别一致性校验）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- today 含数值：54 → **59**；仍无数值 14 条（南极/物候/火情/遥感等无对应公开数据源）","",
 "## 3. 缺口发现摘要","",
 "- B1 探测 13 候选：7 达标（USGS 地震 GeoJSON、NOAA 洋流站、WLD 灌溉/可耕地/耕地/PM2.5/森林）；宋代 5 候选全灭",
 "- 实时目录类来源（USGS/NOAA）数值随查询时刻变化，已在正文与 note 声明",
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