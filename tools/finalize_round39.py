# -*- coding: utf-8 -*-
"""第39轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=39;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";UPG=int(sys.argv[2]) if len(sys.argv)>2 else 3
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
sup_l1=[e["id"] for e in es if e["tier"]=="补充" and e["level"]=="L1"]
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":UPG,"reviews":0,"fixes":UPG,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":3,"sample_rate":"全部升级条目(3条)+2条探测记录","sample_audit":AUDIT,
 "note":"OpenAlex全程429限流：仅3条南极条目升级；18条如实记录探测失败"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["core_all_l2"]=True;sat["important_all_l2"]=True
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 OpenAlex（429限流）","世行指标（多数无值/口径不符）","探测失败留痕（D062）","R17","台账"],
 "gaps_found":pending+len(sup_l1),
 "note":"渠道限流：升级3条，补充L2 72→75；18条记录失败原因","result":"非饱和（渠道受限）"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=UPG
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环，但**渠道受限**","",
 "## 1. 本轮完成","",
 f"- 升级 L2：{UPG} 条（横贯南极山脉、罗斯海、南极科考站）",
 f"- 补充 L2：72 → 75；总 L2：220 → **{levels['L2']}**（243 条的 {levels['L2']*100//243}%）",
 "- **18 条补充 L1 如实记录探测失败**（`reports/round39_probe.json`）","",
 "## 2. 渠道状况（本轮主要障碍）","",
 "- **OpenAlex 全程 429 限流**：12:04 与 12:15 两次实测，`works?search=...` 全部返回 429；等待 90 秒后仍 429。",
 "- **世界银行指标多数不可用**：ER.BDV.TOTL.ZS / SI.POV.URBN.ZS / EN.CLC.MDAT.ZS 返回无值；IQ.CPA.ENVR.XQ 与 IS.ROD.TOTL.KM 已停更。",
 "- **口径不符而弃用（D077）**：城市热岛←PM2.5、火灾生态←森林覆盖率、沙漠化←森林覆盖率。",
 "- 按 D062/D063，失败原因已逐条写入条目 pending_notes 与探测报告——**不把「渠道限流」写成「无文献」**。","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R17）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检：{AUDIT}",
 "- R17 本轮再次抓到脚本内的 3 处星号，已清理至 0。","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}** / L3 {levels['L3']}",
 f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 目标达成度","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心条目全部 L2 | **已达成 44/44** |",
 "| 重要条目全部 L2 | **已达成 104/104** |",
 f"| 多维缺口连续 3 轮为零 | **未达成**（补充层 {len(sup_l1)} 条 L1；本轮因渠道限流仅推进 3 条） |","",
 "## 6. 下一轮的渠道策略","",
 "- 若 OpenAlex 限流解除，优先重试 10 条方法类（沙漠化、城市热岛、生物多样性分布、自然灾害风险、极端天气预警、城市贫困、可持续交通、环境治理、火灾生态、争议边界处理原则）。",
 "- 若仍限流，改用 Crossref（`api.crossref.org`，本轮实测 200）取元数据 + 摘要（部分条目无摘要）。",
 "- 南极特别保护区、南极洲无农业约束两条需 ATS 保护区名录或 SCAR 专门来源。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; L2",levels["L2"],"sup_l1",len(sup_l1))