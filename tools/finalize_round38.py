# -*- coding: utf-8 -*-
"""第38轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=38;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";UPG=int(sys.argv[2]) if len(sys.argv)>2 else 16
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
 "new_sources":len(src)-484,"sample_rate":"25%（10条 / 本轮16条升级）","sample_audit":AUDIT,
 "note":"16条补充条目升级（15学术+1指标）；剔除6条对象错配候选；R17首日即抓到7处星号"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["core_all_l2"]=True;sat["important_all_l2"]=True
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 OpenAlex（历史/方法论类）","B1 世行指标","误匹配剔除（6条）","R16/R17","台账"],
 "gaps_found":pending+len(sup_l1),
 "note":"补充L2 56→72；总L2 204→220（90.5%）","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=UPG
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 f"- **升级 L2：{UPG} 条**（15 条学术文献 + 1 条世行指标）",
 "  - 历史/区域：赫梯王国、仰韶文化、西北海岸、新法兰西、巴塔哥尼亚、的的喀喀湖、纳斯卡文化、奇穆帝国、玛雅研究新进展",
 "  - 方法论/数据：欧洲冰期地貌、地图投影、地理空间数据产品、地球系统科学、环境数据访问、人文地理学",
 "  - 指标类：气候与健康风险",
 f"- 补充 L2：56 → **72**；总 L2：204 → **{levels['L2']}**（243 条的 {levels['L2']*100//243}%）","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R17）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- **R17 首日即生效**：我在本轮脚本里又写了 7 处 `**`，被 R17 当场拦下并清理——证明把缺陷做成机器规则比人工记忆可靠。",
 "- **剔除 6 条对象错配的候选**：",
 "  - 非洲大湖地区 ← 结核分枝杆菌谱系研究",
 "  - 古巴岛 ← 女王海螺群体遗传",
 "  - 南锥体 ← 美洲人类迁徙",
 "  - 查文文化 ← 安第斯古代镜面光学",
 "  - 南美贸易网络 ← 安第斯木材鉴定",
 "  - 争议边界处理原则 ← 管理学「boundary work」概念（学科/职业边界，非国界）",
 "- **按 D077 弃用 3 个替代指标**：城市热岛←PM2.5、火灾生态←森林覆盖率、农业气候风险←耕地占比（口径与主题不符）。","",
 "## 3. 缺口发现摘要","",
 f"- 补充层 L1 仍 {len(sup_l1)} 条：多为南极/极地（横贯南极山脉、罗斯海、南极科考站、无农业约束、特别保护区）、少数方法论与主题条目（沙漠化、生物多样性分布、城市贫困、自然灾害风险、极端天气预警、可持续交通、环境治理、火灾生态、法蒂玛王朝、非洲大湖地区、古巴岛、查文文化、南美贸易网络、南锥体、争议边界处理原则）",
 "- 这些条目普遍缺「可核验的对应端点」，且 OpenAlex 的候选多为对象错配（已逐条剔除）","",
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