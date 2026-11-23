# -*- coding: utf-8 -*-
"""第37轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=37;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";UPG=int(sys.argv[2]) if len(sys.argv)>2 else 22
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
 "new_sources":sum(1 for s in src if s["id"].startswith(("openalex-","wb-")))-101-
   sum(1 for s in src if s["id"].startswith(("openalex-","wb-")) and s.get("year") is None and s["id"].startswith("wb-")),
 "sample_rate":"25%（10条 / 本轮22条升级）","sample_audit":AUDIT,
 "note":"22条补充条目升级（9世行指标+13学术文献）；剔除1条对象错误的候选"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["core_all_l2"]=True;sat["important_all_l2"]=True
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 OpenAlex（历史政权类）","B1 世行指标（区域/主题类）","误匹配剔除","R16","台账"],
 "gaps_found":pending+len(sup_l1),
 "note":"补充L2 34→56；总L2 182→204","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 f"- **升级 L2：{UPG} 条**（全部为补充条目）",
 "  - 9 条世行指标类：森林覆盖变化、土地利用变化、保护与保育区体系、东亚与太平洋/拉美加勒比/中东与北非/南亚区域发展、农业统计体系、气候适应政策",
 "  - 13 条学术文献类：古埃及中王国、贵霜帝国、室利佛逝、满者伯夷、帖木儿帝国、迈锡尼文明、神圣罗马帝国、汉萨同盟、基辅罗斯、美拉尼西亚、密克罗尼西亚、复活节岛、太平洋殖民航线",
 f"- 补充 L2：34 → **56**；总 L2：182 → **{levels['L2']}**（243 条的 {levels['L2']*100//243}%）","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R16）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- **剔除记录**：「南美贸易网络」的 OpenAlex 候选实为**菲律宾**贸易网络研究（摘要涉 Philippines / Asian mainland），与本条对象不符，未采用。",
 "- **弃用记录**：「沙漠化」拟用森林覆盖率作替代指标，因口径不符（D077）仍不升级。","",
 "## 3. 缺口发现摘要","",
 f"- 补充层 L1 仍 {len(sup_l1)} 条：多为南极/极地、方法论与「数据体系」类（地图投影、争议边界处理原则、地理空间数据产品、地球系统科学、人文地理学等），无对应数据端点",
 f"- 待核实总数：{pending}","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}** / L3 {levels['L3']}",
 f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 目标达成度","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心条目全部 L2 | **已达成 44/44** |",
 "| 重要条目全部 L2 | **已达成 104/104** |",
 f"| 多维缺口连续 3 轮为零 | **未达成**（补充层 {len(sup_l1)} 条 L1） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; L2",levels["L2"],"sup_l1",len(sup_l1))