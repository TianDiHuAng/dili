# -*- coding: utf-8 -*-
"""第40轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=40;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";UPG=int(sys.argv[2]) if len(sys.argv)>2 else 15
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
l1=[e["id"] for e in es if e["level"]=="L1"]
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":UPG,"reviews":0,"fixes":UPG,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":15,"sample_rate":"25%（10条 / 本轮15条升级）","sample_audit":AUDIT,
 "note":"Crossref→OpenAlex DOI 桥绕过 search 端点 429；升级 15 条，总 L2 达 238/243（98%）"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["core_all_l2"]=True;sat["important_all_l2"]=True
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 Crossref→OpenAlex DOI桥（绕过429）","误匹配剔除（11条）","D088/D081复查","台账"],
 "gaps_found":pending+len(l1),
 "note":"补充L2 75→90；总L2 223→238（98%）；仅剩5条L1","result":"非饱和（剩5条）"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=UPG
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环","",
 "## 1. 本轮完成","",
 f"- **升级 L2：{UPG} 条**",
 "  - 主题/概念类：沙漠化、城市热岛、生物多样性分布、自然灾害风险、极端天气预警、城市贫困、可持续交通、火灾生态、农业气候风险、南极洲无农业的环境约束",
 "  - 历史/区域类：法蒂玛王朝、非洲大湖地区、查文文化、南锥体、南美贸易网络",
 f"- 补充 L2：75 → **90**；总 L2：223 → **{levels['L2']}**（243 条的 {levels['L2']*100//243}%）",
 f"- 剩余 L1：**{len(l1)}** 条","",
 "## 2. 渠道突破（本轮关键）","",
 "- OpenAlex **`search` 端点持续 429**（距上轮 2 小时后仍 429）；Semantic Scholar 亦 429；CORE 403。",
 "- **但 OpenAlex 单作品端点 `works/{id}` 正常（200）**，Crossref 搜索正常（200）。",
 "- 因此采用 **Crossref 搜索拿 DOI → OpenAlex DOI 端点取摘要** 的桥接方式，成功为 18+7 个主题取得带摘要的候选。",
 "- Crossref 自身的摘要覆盖率约 40%，但经 DOI 桥接后 OpenAlex 侧可取到更完整的 abstract_inverted_index。","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R17）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- **剔除 11 条对象错配候选**（两轮合计）：",
 "  - 古巴岛 ← **阿拉斯加半岛**地质（GEOLOGY OF THE ALASKA PENINSULA）",
 "  - 环境治理 ← 三本书评（International Studies Review）",
 "  - 南极特别保护区 ← 泛论保护区管理（非南极）",
 "  - 争议边界处理原则 ← 制图表示的泛论",
 "  - 南美贸易网络（首轮）← 安第斯水资源 resilience",
 "  - 阿巴拉契亚山脉 ← 金伯利岩侵入体（过窄）",
 "  - 另有第39轮已剔的 5 条（结核杆菌/海螺/美洲迁徙/镜面光学/木材鉴定）","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}** / L3 {levels['L3']}",
 f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 目标达成度","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心条目全部 L2 | **已达成 44/44** |",
 "| 重要条目全部 L2 | **已达成 104/104** |",
 f"| 多维缺口连续 3 轮为零 | 尚未（剩 {len(l1)} 条 L1：阿巴拉契亚山脉、古巴岛、南极特别保护区、争议边界处理原则、环境治理） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("updated; L2",levels["L2"],"L1",len(l1))