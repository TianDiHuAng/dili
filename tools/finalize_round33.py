# -*- coding: utf-8 -*-
"""第33轮收尾（本轮为 30/30 上限轮，报告须如实说明目标未达成）。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=33;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 13
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
imp_l1=[e["id"] for e in es if e["tier"]=="重要" and e["level"]=="L1"]
core_l1=[e["id"] for e in es if e["tier"]=="核心" and e["level"]=="L1"]
legacy=cov.get("d041_legacy_count",0)
single=sum(1 for u in ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
  for e in json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8"))["entries"]
  if "单源待互证" in (e.get("pending_notes") or ""))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":13,"reviews":0,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":13,"sample_rate":"25%（10条 / 本轮13条升级）","sample_audit":AUDIT,
 "note":"13条重要L1升级L2（Wikidata年代/面积/海拔），全部标单源待互证"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 Wikidata批量","重要L1攻坚","D079单源标注","R14/R15","台账"],
 "gaps_found":pending+len(imp_l1)+legacy,
 "note":"重要L1 77→64；总L2 78→91","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

lines=[f"# REPORT.md — 第 {ROUND} 轮摘要（自主循环第 30/30 轮上限）","",f"- 日期：{DATE}","- 状态：正常（NORMAL）**——目标未达成，详见第 7 节**","",
 "## 1. 本轮完成","",
 "- 新增条目：0",
 f"- **升级 L2：13（全部为重要条目）**：古埃及新王国、库什与努比亚、罗马阿非利加、加纳帝国、桑海帝国、笈多王朝、商代、周代、秦代、元代（用 Wikidata 起止年代）；马格里布、阿拉伯半岛（面积）、埃塞俄比亚高原（海拔）",
 f"- 修复：{FIXES}（13 条统一标注「单源待互证」；渲染徽标「结构化数据集（单源待互证）」）",
 "- 新增来源：13（Wikidata 实体）","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R15 在位）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}","",
 "## 3. 缺口发现摘要","",
 "- Wikidata 批量查询：政权类 31 条中 10 条有完整起止；地理类 23 条中仅 3 条有可用量值",
 f"- 仍缺：重要 L1 {len(imp_l1)} 条、核心 L1 {len(core_l1)} 条、遗产 L2 {legacy} 条、配对缺口 {cov.get('d041_pairing_gap_count',0)} 条","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}** / L3 {levels['L3']}",
 f"- 待核实总数：{pending}（其中「单源待互证」{single} 条）",
 f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 覆盖矩阵仍空白格子","",
 "- 无（8 个大洲 × 6 主题格子均非空）","",
 "## 6. 需要人关注的事项","",
 "- **Wikidata 单源依赖**：13+5 条条目（共 18 条）的关键年代/量值仅有 Wikidata 一处来源，已全部显式标注「单源待互证」。若要达到 TASK 要求的双源互证，需补学术或机构专题来源（本环境 Wikipedia/Britannica/DBpedia 均不可达）。","",
 "## 7. 目标达成度（如实评估）","",
 "**目标未达成。** 依据 AUTONOMOUS.md 的饱和判据（连续 3 轮七法无新缺口 + 核心与重要条目全部 L2）：","",
 f"- **核心条目**：L2 {tiers['核心'] - len(core_l1)}/{tiers['核心']}，仍剩 {len(core_l1)} 条 L1（城市起源）。",
 f"- **重要条目**：L2 {tiers['重要'] - len(imp_l1)}/{tiers['重要']}，仍剩 {len(imp_l1)} 条 L1。",
 f"- **缺口发现**：每轮仍有新缺口（重要 L1 {len(imp_l1)}、遗产 L2 {legacy}、单源待互证 {single}），未出现连续 3 轮零缺口。",
 "- **结论**：处于「正常循环」，未饱和，不具备进入维护模式的条件。","",
 "结构化阻塞条件（非难度问题）：",
 "1. 本环境 Wikipedia / Britannica / DBpedia / Met / Smithsonian / UNESCO WHC / GBRMPA 等站点普遍 403/000，古代史与区域专题页几乎无法获取。",
 "2. 因此重要 L1 的升级只能依赖 Wikidata 单一结构化来源，无法满足「两个独立来源互相印证」。",
 "3. 32 条遗产 L2 的来源仍为数据层别名级（UNSD M49/UNSDG），无法转为专题页支撑。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; L2",levels["L2"],"imp_l1",len(imp_l1),"core_l1",len(core_l1))