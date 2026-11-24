# -*- coding: utf-8 -*-
"""第91轮：修正 2 处虚高——城市化水平错挂气候页；古埃及新王国双耳瓶降旁证。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 城市化水平：Climate Change 页明显错挂
e=T["城市化水平"]
if "s026-ourworldindata-org" in e["sources"]:
    e["sources"]=[s for s in e["sources"] if s!="s026-ourworldindata-org"]
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第91轮审计修正·错挂来源】`s026-ourworldindata-org`（《**Climate Change** | Our World in Data》）"
      "此前被登记为本条的第二强来源，但该页主题是**气候变化**，与「城市化水平」无关——**属明显错挂**"
      "（疑似为凑 A 级而误挂）。现已从本条 sources 移除。本条降为 **B 级**。").strip()
    e["last_update"]=TODAY
    print("城市化水平：已移除 Climate Change 页")

# 2) 古埃及新王国：Amphorae 降旁证
e=T["古埃及新王国"]
if "openalex-W197188726" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第91轮审计修正·器物层面】`openalex-W197188726`（《**Amphorae** in New Kingdom Egypt》, 2005, 被引45）"
      "研究的是新王国的**双耳陶瓶**（器物类型学），属物质文化层面，"
      "不能支撑本条「以文书与官僚体系治理」的行政叙述。**现降为旁证**。本条降为 **B 级**。").strip()
    e["last_update"]=TODAY
    print("古埃及新王国：Amphorae 已降旁证")

save_docs(docs); update_coverage(docs)
print("完成")