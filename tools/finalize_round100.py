# -*- coding: utf-8 -*-
"""第100轮收尾（第100轮总结）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=100;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
nref=sat["evidence"]["sources_referenced"];nunref=sat["evidence"]["sources_unreferenced"];nfail=sat["evidence"]["sources_fetch_failed"]
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":243,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"41项边界用例 + 6项交叉一致性 + 全量来源引用核查",
 "sample_audit":"边界用例0失败、一致性0问题；新发现777登记中139未引用（D154）",
 "note":f"D154：来源登记数≠引用数（{nref} 引用/{nunref} 未引用）；缺口 G1=0/G3a={sp['G3a']['count']}/G3b={sp['G3b']['count']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**第 100 轮判据复核：全部通过，另发现一处数字口径问题**）","",
 "## 1. 判据复核（D143 周期点）","",
 "### 41 项边界用例：0 失败","",
 "重跑第90轮写的用例集，覆盖 is_data / is_alias / is_bad_type / _nums / has_content / strength / level_of / count_entry / content_count 的各类边界（多值 note、空壳页、书评、首页、被引门槛、D141 指标类豁免）。**全部通过。**","",
 "### 6 项交叉一致性：0 问题","",
 "| 检查 | 内容 | 结果 |","|---|---|---|",
 "| 1 | `content_count ≤ strong 数` | ✅ |",
 "| 2 | `content_count` = 去重后的域数 | ✅ |",
 "| 3 | `level_of` 与 strong/content_count 对应 | ✅ |",
 "| 4 | G3 分类与 `content_count==1 且非 D` 一致 | ✅ |",
 "| 5 | `evidence_level.json` 与实时重算一致 | ✅ |",
 "| 6 | 来源引用核查 | ⚠ **见下** |","",
 "**这是本项目第一次「边界用例 + 交叉一致性」全过。** 前几轮（90/92/93/94）每次都能查出新问题，这次没有。",
 "判断依据不是「我觉得收敛了」，而是：**D146（side）、D150（域名）、D151（层级口径）、D152（多段扫描）四条修复之后，同一个事实在 strength/content_count/level_of 三处给出的结论一致。**","",
 "## 2. 新发现：来源数一直在虚报","",
 "交叉检查第 6 项暴露了一个口径问题：**sources.json 登记 777 条，但实际被条目引用的只有 638 条**。",
 "139 条未被引用，其中 **48 条是抓取失败记录**（「404 - File or directory not found」「(未取得页面标题)」「Just a moment...」），另 53 条是补源时登记但最终未采用的 openalex 候选。","",
 "**这意味着我此前每一轮报告里的「777 来源」都偏高 139 条。**",
 "这些记录不该删除（它们证明了哪些 URL 抓不到，是可复现的证据），但**必须与引用数分开报告**。","",
 "已做：在 `sources.json` 给未引用来源加 `referenced=false`、抓取失败者加 `fetch_failed=true`；SATURATION 中区分 `sources_registered`（777）、`sources_referenced`（638）、`sources_unreferenced`（139）、`sources_fetch_failed`（48）。","",
 "## 3. 第 100 轮的账","",
 "| 指标 | 值 |","|---|---|",
 "| 条目 | 243（全部 L2） |",
 f"| 层级 | A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']} |",
 f"| 来源（登记 / 引用） | **777 / {nref}** |",
 f"| 缺口 | G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4={gd['G4']} |",
 f"| 内容源 ≥2 | **{g2}**（{g2*100//243}%） |",
 f"| 判据 | 41 项用例 + 6 项一致性，**全过** |",
 "| 机器闸 | `check.py` R1–R25，0 错误；`check_links.py` 4,940 链接，0 断链 |","",
 "## 4. 一百轮里最重要的一件事","",
 "不是「G3 从 91 降到 31」，而是：**有 9 轮（77、78、79、82、90、91、92、93、94）的主要工作是推翻自己上一轮的数字。**",
 "| 那 9 轮在做什么 | 推翻了什么 |","|---|---|",
 "| 77 | G3 拆分 | 发现 69 条里只有 2 条「有侧面可补」，67 条是无任何第二来源 |",
 "| 78 | D141 指标类豁免 | G1 虚增到 13，修正为 1 |",
 "| 79 | 审计 assess.py | `_nums` 取大值、空壳页未排除 |",
 "| 82 | 识别 API 故障 | 12 条「0 候选」是 429 造成的假象 |",
 "| 90 | 审计判据一致性 | `content_count` 不认 side → **G3 由 14 修正为 45** |",
 "| 91 | A 级抽样 | 城市化水平错挂气候页、双耳瓶 |",
 "| 92 | A 级全量 | **Home-AAG 首页被当 12 条的强来源** → A 由 183 修正为 171 |",
 "| 93 | A 级全量 | 同域名多页当独立来源 |",
 "| 94 | A 级全量 | `for…break` 忽略降级记录 → **撤销「G1 清零」里程碑** |","",
 "**如果没有这 9 轮，我现在会宣称「G3=14、G1=0、A=213」——三个数字全是错的。**",
 "第 100 轮能做出「用例全过 + 一致性全过」的结论，正是因为这 9 轮把判据磨到了一致。","",
 "## 5. 下一阶段","",
 "剩余 31 条：G3a 14（核心 1）、G3b 17（核心 3）。**核心 4 条**是真正的硬骨头。",
 "继续补源时，每个新来源仍须过：对象词匹配 → 摘要对读 → 落点句。**判据已收敛，补进来的就是真的。**",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} 引用={nref}/登记={len(src)}")