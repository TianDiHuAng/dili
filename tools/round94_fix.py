# -*- coding: utf-8 -*-
"""第94轮：修南锥体（两条均不对位）、大堡礁除草剂、南极科考站污水。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 南锥体：两条强来源均不对位
e=T["南锥体"]
e["pending_notes"]=((e.get("pending_notes") or "")+
  " 【第94轮审计修正·双条不对位】本条原 A 级的两个强来源**都不支撑条目**："
  "① `s026-ourworldindata-org`（《**Climate Change** | Our World in Data》）是**全球气候变化**页，与「南锥体」的区域地理无关；"
  "② `openalex-W4224441281`（《The **Spanish postwar emigration** to the Southern Cone》, 2022, 被引3）研究的是"
  "**二战后西班牙向南锥体的移民**，属 20 世纪人口史侧面。两条现均降为旁证。"
  "**本条因此失去全部强来源（C 级）——这是如实反映，不是退步。**").strip()
e["last_update"]=TODAY
print("南锥体：两条已降旁证 → C 级")

# 2) 大堡礁
e=T["大堡礁"]
if "openalex-W2020216779" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第94轮审计修正·侧面】`openalex-W2020216779`（《Effects of **herbicides** diuron and atrazine on corals》, 2003）"
      "是**除草剂对珊瑚的毒理学**研究，属污染生态侧面，不支撑「大堡礁的生态格局与保护」。现降为旁证。").strip()
    e["last_update"]=TODAY; print("大堡礁：除草剂已降旁证")

# 3) 南极科考站
e=T["南极科考站"]
if "openalex-W2135820861" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第94轮审计修正·侧面】`openalex-W2135820861`（《Survey of **waste water** disposal practices at Antarctic stations》, 2009, 被引138）"
      "研究的是科考站的**污水处理做法**，属设施管理侧面，不支撑「科考站体系的科学合作框架」。现降为旁证。").strip()
    e["last_update"]=TODAY; print("南极科考站：污水已降旁证")

save_docs(docs); update_coverage(docs)
print("完成")