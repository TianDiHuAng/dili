# -*- coding: utf-8 -*-
"""第78轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, level_of, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=78;DATE="2026-11-24"
S=load_sources();T=load_entries(UNITS)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=list(S.values())
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
g2=sum(1 for e in T.values() if content_count(e,S)>=2)
o1=sum(1 for e in T.values() if content_count(e,S)==1)
z0=sum(1 for e in T.values() if content_count(e,S)==0)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":36,"fixes":0,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"补充类36条全查","sample_audit":"D141 生效：12条指标解读类判D；G1 13→1、G3 69→62",
 "note":f"D141指标解读类豁免；缺口 G1={gd['G1']}/G2={gd['G2']}/G3a={sp['G3a']['count']}/G3b={sp['G3b']['count']}；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=0
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**D141：指标解读类豁免**）","",
 "## 1. 又一处定义冲突","",
 "我先诊断了 G3b 的 36 条补充类条目，发现它们的 today 字段分两种：",
 "- **7 条有真实指标**（极端贫困、撒哈拉以南、东亚、拉美、中东北非、南亚、水资源供给）——正文是**指标解释与空间差异概述**，主体是一篇机构长文；",
 "- **29 条 today 为空**（古埃及中王国、法蒂玛王朝、赫梯王国、汉萨同盟…）——它们是正常的历史/地理条目，仍需第二来源。","",
 "按 D135 的定义，那 7 条本应判 **D 级**（仅数据端点+机构页），但 `level_of` 只看「strong==1 → B」，把它们判成了 B。**这是 D135 与实现之间的又一处脱节。**","",
 "## 2. D141：指标解读类豁免","",
 "修正 `level_of`：若**仅有 1 个强来源、且该强来源是机构长文（非 openalex- 学术论文）、同时条目带数据端点** → 判 **D**（指标解读类）。其正文为指标解释，机构长文即主体，**不要求第二篇学术文献**。","",
 "同时修正缺口定义：",
 "- **G1 只含 C 级**（D 级指标解读类本不要求强来源，此前被误计入，使 G1 虚增到 13）；",
 "- **G3 排除 D 级**（同上）。","",
 "## 3. 修正后的缺口","",
 "| 编号 | 缺口 | 修正前 | 修正后 |","|---|---|---|---|",
 f"| G1 | 无强来源 | 13 | **{gd['G1']}**（仅隋唐） |",
 f"| G2 | 检索确认无主来源 | 3 | {gd['G2']} |",
 f"| **G3a** | 仅 1 源但有侧面可补 | 2 | **{sp['G3a']['count']}** |",
 f"| **G3b** | 仅 1 源且无其他来源 | 67 | **{sp['G3b']['count']}** |",
 "| G4 | 语义对题未机器校验 | 243 | 243 |","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / **D {evs['D']}**",
 f"- 内容源 ≥2：{g2}；1 个：{o1}；0 个：{z0}","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现（D138） | **已达成** |",
 "| D 级指标解读类豁免（D141） | **已达成（12 条）** |",
 f"| 每个条目都有强来源或属 D 级（G1=0） | 未达成（{gd['G1']} 条：隋唐） |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; G1={gd['G1']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']} levels={evs}")