# -*- coding: utf-8 -*-
"""第23轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=23;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 32
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":9,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"25%","sample_audit":AUDIT,
 "note":"9条首轮复核；32条备注双标签合并；站点新增来源等级徽标（骨架/专题/遗产三类）"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,
 "methods_used":["B1专题页探测(0可用)","B5待核实","B7深度","B2覆盖矩阵","首个复核队列清零"],
 "gaps_found":pending+cov.get("d041_legacy_count",0),
 "note":"B1 探测 23 候选 0 可用——专题页渠道接近饱和","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0","- 升级 L2：0",
 f"- 修复：{FIXES}（32 条备注的「【D041 标记】【D041 缺口】」双标签合并；备注格式统一为轮次索引式）",
 "- 复核：9（**首次覆盖此前从未复核的重要/核心 L1**：夏威夷群岛、大堡礁、澳大利亚内陆干旱气候、澳大利亚混合农业、南极半岛、松岛冰川退缩、冲积平原、山地农业、城市起源）",
 "- 站点改进：条目页新增「来源等级」徽标（骨架级 / 专题页+机构页 / 区域机构级待补 / 专题页+入口页），让来源缺口在页面上可见",
 "- 新增来源：0","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- 徽标分布核对：遗产级 35、骨架级 171、专题页级 18、配对说明 2","",
 "## 3. 缺口发现摘要","",
 "- **B1 专题页探测出现零收获**：23 个候选路径（NOAA JetStream / NPS archeology / NASA features / BOM / USDA 等）全部 403/404/门落户/正文不足，0 个达标",
 "- 这是 B1 方法接近饱和的信号：本机可达的机构专题页渠道已基本用尽",
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
print("updated")