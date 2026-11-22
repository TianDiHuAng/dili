# -*- coding: utf-8 -*-
"""第17轮收尾：METRICS / SATURATION / REPORT。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=17;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 7
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":33,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"25%","sample_audit":AUDIT,
 "note":"清理7条泛化来源误贴（第16轮审查清单）；专题页探测14路径仅1可用"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,
 "methods_used":["B1 D044专题页探测","B5待核实","B7深度(遗产L2)","B2覆盖矩阵","修复清理(第16轮遗留)"],
 "gaps_found":1+pending+cov.get("d041_legacy_count",0),"result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0","- 升级 L2：0",
 f"- 修复：{FIXES}（清理 7 条泛化来源误贴：北美冰盖/大自流盆地/巴西高原移除 FAO 水资源概览页；巴西殖民经济、加勒比海群岛、十三殖民地、美国西进移除同型背景页）",
 "- 复核：33（重要 L1；pending_notes 写明 D041/D044 缺口）","- 新增来源：0",
 "- 提交：4 个批次提交 + 补配额提交","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS（4375 条内部链接）",
 f"- 抽检（25%，10 条）：{AUDIT}","- 回滚/降级：无","",
 "## 3. 缺口发现摘要（本轮使用 5 种方法）","",
 "- B1 D044 专题页探测：14 条候选路径仅 1 个达标（NASA Paleoclimatology Ice Cores，body 18931/hits 70），且不直接支撑北美冰盖本体；Met/Smithsonian/LOC 均 403 或不通",
 f"- B5 待核实：{pending}",
 f"- B7 深度：核心 L1 6、重要 L1 50（未复核）、遗产 L2 {cov.get('d041_legacy_count',0)}、配对缺口 {cov.get('d041_pairing_gap_count',0)}",
 "- B2 覆盖矩阵、修复清理：同步执行","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / L2 {levels['L2']} / L3 {levels['L3']}",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}",
 f"- D041 遗产 L2：{cov.get('d041_legacy_count',0)} 条；配对缺口：{cov.get('d041_pairing_gap_count',0)} 条","",
 "## 5. 覆盖矩阵仍空白格子（最多 20）","",
]
lines += [f"- {b}" for b in blanks[:20]] if blanks else ["- 无"]
lines += ["","## 6. 需要人关注的事项","","- 无",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; pending",pending,"levels",levels)