# -*- coding: utf-8 -*-
"""第5轮抽检返工：无源年代全局清理、城市起源降级、新L1来源说明修正。"""
import json, os, re, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
PAT=re.compile(r"\d|万年前|亿年前|世纪|冰期")

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
changed=[]
for d in docs.values():
    for e in d["entries"]:
        # 1) L2/L3 全局无源年代清理
        if e["level"] in ("L2","L3") and PAT.search(e.get("time_or_place","")):
            e["time_or_place"]="时期与年代待专门来源核验（详见待核实）"
            e["pending_notes"]=e.get("pending_notes","")+" 第5轮返工：已移除无专门来源的具体年代表述。"
            changed.append(e["title"])
        # 2) 本批新增 L1 的背景来源与 outlines 修正
        if e["title"]=="地图投影":
            e["outlines"]=["OGC 标准","Esri GIS 定义"]
            e["pending_notes"]="背景来源 OGC 标准页与 Esri GIS 定义页已核验；投影分类与历史演变待专题来源核验。"
        if e["title"]=="争议边界处理原则":
            e["outlines"]=["UN M49","CBD 公约页面"]
            e["pending_notes"]="背景来源 UN M49 与 CBD 页面已核验；本站只描述立场、不画线的编辑原则非事实断言，专题方法来源待补。"
        # 3) 城市起源降级 L1
        if e["title"]=="城市起源":
            for k in ["geo","influence","polities","connections","today","svg"]: e.pop(k,None)
            e["level"]="L1";e["status"]="二次返工降级L1(第5轮)"
            e["definition"]="城市起源：农业剩余、贸易与权力集中等因素共同作用，使部分聚落发展为早期城市。"
            e["overview"]="农业剩余、贸易与权力集中等因素共同作用，使部分聚落发展为早期城市。"
            e["time_or_place"]="时期与年代待专门来源核验（详见待核实）"
            e["sources"]=["s010-unesco-org","s025-ourworldindata-org"]
            e["pending_notes"]="第5轮返工：现有 UNESCO 文化页与 OWID 城市化页为背景来源，不能支撑早期城市具体年代与地区序列，故降级 L1。"
            changed.append(e["title"])

for u,d in docs.items():
    json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# scope.md 增加年代口径说明
p=os.path.join(ROOT,"scope.md")
t=open(p,encoding="utf-8").read()
note="> 年代口径：本清单中的年代为选题阶段的候选标记，不构成站点事实断言。自第5轮起，L2 条目的无专门来源年代已从站点页面移除并统一标为待核；详见 DECISIONS.md。\n\n"
if "年代口径：本清单中的年代为选题阶段" not in t:
    t=t.replace("# scope.md — 《地理与文明百科》入选清单\n","# scope.md — 《地理与文明百科》入选清单\n\n"+note,1)
open(p,"w",encoding="utf-8").write(t)
print("返工：清理年代",len(changed),"条；城市起源降级；scope.md 增加年代口径说明")
