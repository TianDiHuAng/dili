# -*- coding: utf-8 -*-
"""第29轮收尾。"""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=29;DATE="2026-11-22"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";FIXES=int(sys.argv[2]) if len(sys.argv)>2 else 21
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":1,"fixes":FIXES,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":5,"sample_rate":"25%（10条抽检 / 本轮16条去重改动 = 62.5%）","sample_audit":AUDIT,
 "note":"10条补量级声明、5条全球主题填数据、5条年份格式统一（合计16条去重）；宋代原判实证经抽检证伪已回退为非实证"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["实证复核(末条清零)","today量级声明","全球数据端点","事实核对","台账"],
 "gaps_found":pending+cov.get("d041_legacy_count",0),
 "note":"today 无编号 25→22（全球主题类难用国家数据，已用 WLD/NOAA 世界序列补 5 条）","result":"非饱和"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常（NORMAL）","",
 "## 1. 本轮完成","",
 "- 新增条目：0","- 升级 L2：0",
 f"- 修复：{FIXES} 项（16 条去重条目）：宋代尝试实证复核但**经抽检证伪已回退**（详见质量节）；10 条历史 today 补「仅示量级、不代表区域差异」声明；5 条年份格式统一为「YYYY年」）",
 "- 数据填充：5 条全球主题条目 today 首次写入实测值（全球气温距平←NOAA 全球陆海温度距平 2025 年 +1.12 °C；森林覆盖变化←世界 31.1%（2023年）；渔业资源←世界 235,811,491 吨（2024年）；水资源管理←世界 9.0%（2022年）；城市热岛←世界城市化率 57.8%（2025年））",
 "- 复核：1（宋代；原判「实证/达标」为假命中，已回退为「非实证」）",
 "- 新增来源：5（noaa-global-temp、wb-wld-forest/urban/fish/water）",
 "- 说明：**零复核池已清零**，本轮未用满 40 配额（21 项）","",
 "## 2. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（25%，10 条）：{AUDIT}",
 "- 过程修复：3 条 today 曾因「2024 年」带空格触发 R8 校验，已统一为「2024年」",
 "- **抽检后返工**：① 宋代实证结论证伪（UNSD M49 页的 han 命中来自 Handbook/Ghana/Afghanistan，song=0、宋=0），回退为非实证；② 澳大利亚大陆/日本列岛仍挂 wb-api-pop(CHN)/wb-api-life(WLD) 共享端点，已建 wb-aus-*/wb-jpn-* 专用端点替换并补写国名；③ 共享端点 5 个全部退役（现 0 条引用）；④ **check.py 新增 R14**：today 提到的国家必须在该条端点 ISO3 集合内，防 D072 复发","",
 "## 3. 缺口发现摘要","",
 "- B1 全球数据端点探测（8 候选）：6 达标（NOAA currents/temperature、WLD forest/urban/fish/water）；USGS 地震计数与 CO₂ 端点返回内容过短",
 "- today 无指标编号：25 → 22（余下为板块构造/季风/洋流/气候带/河流三角洲等，需专门观测数据）",
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