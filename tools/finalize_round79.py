# -*- coding: utf-8 -*-
"""第79轮收尾。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, level_of, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=79;DATE="2026-11-24"
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":2,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"—","sample_audit":"审计 assess.py 本身：查出2处偏离（多值取大/空壳页未排除）并修复",
 "note":f"D142：_nums取严格值+空壳页排除；A 137→{evs['A']}、G3 62→{gd['G3']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=ROUND;sat["gap_model"]["definitions"]=g["gap_definitions"];sat["evidence"]["levels"]=evs
sat["evidence"].update({"ge2_content":g2,"one_content":o1,"zero_content":z0})
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=2
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**审计判据本身，查出 2 处漏洞**）","",
 "## 1. 这轮没有补来源，而是审计 `assess.py`","",
 "上轮结尾我写道：「与其等它暴露，不如先审一遍」。本轮就做了这件事——对 `tools/assess.py` 的四个函数逐个设计边界用例。","",
 "**测试方法**：直接 import 模块，喂人造数据（多值 note、空壳页 note、不同措辞的备注段），看返回值是否符合预期。","",
 "| 测试项 | 结果 |","|---|---|",
 "| `has_content` 调用点是否漏传 `entry` | ✅ 全部传入（不会漏读 pending_notes） |",
 "| `strength` 的 side 判定（7 种措辞） | ✅ 7/7 正确 |",
 "| 机构长文（NOAA/IUCN/World Bank）判 strong | ✅ 正确 |",
 "| **note 中并存多个字符数** | ❌ **取第一个（5,455），应取严格值（750）** |",
 "| **空壳页是否被排除** | ❌ **未排除**——`is_alias` 不认，`has_content` 也不查「空壳页判定」 |","",
 "## 2. 两处漏洞的具体后果","",
 "**漏洞一（多值取大）**：UNICEF 那条 note 里并存「文本提取 5,455 字符」与「strip 后 750 字符」。`_nums` 取第一个匹配 → 5,455 ≥ 800 → 判有正文。**这与 D127「以更严格者为准」直接矛盾**。",
 "**漏洞二（空壳页未排除）**：`s008-unesco-org`、`s085-unesco-org`、`s004-population-un-org` 已被标「空壳页判定」，但 `assess.py` 只排除 `is_alias` 名单内的 5 个 id，**这三个不在名单里**，它们若 note 含大数字仍会被算作内容源。","",
 "## 3. 修复（D142）","",
 "- `_nums`：收集所有字符数匹配，**取最小值**；","",
 "- `has_content` / `strength`：note 含「空壳页判定」者，分别返回 `False` / `weak`。","",
 "修复后重测：`_nums` 返回 750 ✅、`has_content` 返回 False ✅、空壳页 strength 返回 weak ✅。","",
 "## 4. 数字的变化（都是往严的方向）","",
 "| 指标 | 修复前 | 修复后 |","|---|---|---|",
 f"| A 级 | 137 | **{evs['A']}** |",
 f"| D 级 | 12 | **{evs['D']}** |",
 f"| G3 | 62 | **{gd['G3']}** |",
 f"| G3a / G3b | 2 / 60 | **{sp['G3a']['count']} / {sp['G3b']['count']}** |","",
 "## 5. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；R1–R25）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 内容源 ≥2：{g2}；1 个：{o1}；0 个：{z0}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3a={sp['G3a']['count']} / G3b={sp['G3b']['count']} / G4=243","",
 "## 6. 为什么这轮值","",
 "此前三次「定义脱节」（D135 别名页、D138 双标准、D141 指标类）都是**事后**发现的——先跑出数字，再看数字不对劲。",
 "这轮换了顺序：**先审判据，再信数字**。两个漏洞都在它们污染数字之前被拦住。",
 "而且这两个漏洞的形态相同：**assess.py 的实现只覆盖了「我知道的情况」，没覆盖「我不知道的情况」**——别名页只写了 5 个、字符数只取了第一个。",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} D={evs['D']} G3={gd['G3']} G3a={sp['G3a']['count']} G3b={sp['G3b']['count']}")