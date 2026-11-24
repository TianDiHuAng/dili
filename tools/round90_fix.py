# -*- coding: utf-8 -*-
"""第90轮B：修正汉代虚高（Dogs 标旁证）；撒哈拉加限定。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 汉代：Dogs 降旁证
e=T["汉代"]
if "openalex-W4403972561" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第90轮审计修正·虚高】openalex-W4403972561（《Dogs in Early Imperial China: Anthropo-Zoological Reading of "
      "Iconographic Sources from the **Han Dynasty** (206 BC-AD 220)》, 2019, 被引0）——**标题含 Han Dynasty，"
      "因而通过了 R20 的对象词检验**，但主题是**汉代图像中的狗（动物考古/图像学侧面）**，不支撑本条的疆域与行政叙述。"
      "**现降为旁证**。此条是「R20 拦不住的那一层」的实例：标题含对象词而主题无关。本条的 A 级随之降为 B。").strip()
    e["last_update"]=TODAY
    print("汉代：Dogs 已降旁证")

# 2) 撒哈拉：加限定（来源保留，但正文说明其时段）
e=T["撒哈拉沙漠"]
sid="openalex-W2794663306"
if sid in e["sources"] and "第90轮审计限定" not in (e.get("pending_notes") or ""):
    e["geo"]=((e.get("geo") or "")+
      " 关于本条气候变化的第二来源（2018 年《Twentieth-Century Climate Change over Africa》，被引181）"
      "讨论的是**20 世纪**非洲的**季节性水文气候变化**，属现代气候记录；**本条不以其作为地质时期干旱化的定论**，"
      "只用于说明撒哈拉周边的气候变率仍在持续。").strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第90轮审计限定】{sid} 的时段是 **20 世纪**、范围是**整个非洲**的季节性水文气候，"
      "与本条的**地质时期干旱化**不同层；已在 geo 段加写限定，不作地质定论。").strip()
    e["last_update"]=TODAY
    print("撒哈拉：已加时段限定")

save_docs(docs); update_coverage(docs)
print("完成")