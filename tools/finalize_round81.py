# -*- coding: utf-8 -*-
"""第81轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=81;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":12,"fixes":4,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":4,"sample_rate":"核心5+重要7全查","sample_audit":"核心命中4/5（含印加终于找到）、重要7条0候选",
 "note":f"补4条→G3 57→{gd['G3']}、核心G3b 5→1；层级 A{evs['A']}/B{evs['B']}/C{evs['C']}/D{evs['D']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=4
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**核心 G3b：5 → 1**）","",
 "## 1. 4 条核心条目全部找到对位来源","",
 "| 条目 | 新第二来源 | 被引 | 摘要 |","|---|---|---|---|",
 "| 东非大裂谷 | Evolution of the East African Rift System from trap- to plate-scale rifting (2022) | **101** | 2,889 |",
 "| 印加帝国 | Imperial Expansion and Local Agency: A Case Study of Labor Organization (2017) | **43** | 1,411 |",
 "| 撒哈拉沙漠 | Late–Mesozoic and Tertiary palaeoenvironments of the Sahara region (2020) | 5 | 1,905 |",
 "| 印度河文明 | Origin and Growth of the Principal Elements of the Harappan Civilization (2025) | 0 | 862 |","",
 "**印加终于找到了**——此前三次检索都只命中「马丘比丘遗址」或「玉米酒器物」，这两条都是遗址/器物层面。这次换成「帝国扩张 + 劳役组织」对象词，命中一篇**直接讨论行省经济集约化与地方能动性**的研究，正是本条要的国家层面。","",
 "**东非大裂谷**此前命中「死海裂谷」（地名碰撞），这次加了 `great rift` 与 `plume` 等词，找到裂谷系统演化的综述（被引 101）。","",
 "## 2. 重要条目 7 条全部 0 候选","",
 "萨珊波斯、吠陀时代、明清、马来群岛、河中地区、洋流、气候带——本轮宽检索**均无过筛者**。这些条目前几轮命中的都是侧面（钱币学、女性地位、医学制度、方言、铭文），说明**该主题的英文学术文献确实以侧面研究为主**。","",
 "## 3. 一个校验修复","",
 "R20 报错：印度河文明的新来源标题用的是 **HARAPPAN**（不是 INDUS），对象词表缺 `harappan`。已补 → 对象词变为 `['indus','harappan','indus valley']`。",
 "这也是 R20 的价值：**它逼我为每个条目想清「这个对象还有哪些别名」**。","",
 "## 4. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 层级：**A {evs['A']}** / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 内容源 ≥2：**{g2}**；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / **G3b={sp['G3b']['count']}**（核心仅 1） / G4=243","",
 "| 条件 | 状态 |","|---|---|",
 "| 全部 243 条 L2 | **已达成** |",
 "| 判据单一实现 + 经主动审计 | **已达成** |",
 "| R19–R25 七道机器校验 | 已上线，0 违规 |",
 f"| 每个条目都有强来源或属 D 级 | 未达成（{gd['G1']} 条：隋唐） |",
 f"| 每条（非 D 级）都有 ≥2 内容源 | 未达成（{sp['G3a']['count']+sp['G3b']['count']} 条，其中核心仅 1 条） |",
 "| G4 语义对题 | 50/243 已扫描 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} G3={gd['G3']} G3b={sp['G3b']['count']}")