# -*- coding: utf-8 -*-
"""第15轮第二批返工：萨赫勒带换用真实专题来源；印度河文明降级 L1。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条只写自然地理与生态背景，不叙述具体政权、王朝与年代序列（相关历史条目待专门史料核验）。"
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 萨赫勒带：改用 NASA 萨赫勒/荒漠化专题页（实测 sahel=20/31、desertification=7/60、vegetation=47）
s=T["萨赫勒带"]
s.update({
 "level":"L2","status":"L2合规换源(第15轮)",
 "definition":"萨赫勒带：撒哈拉南缘的半干旱过渡带，降水年际变率大，植被由荒漠草原向稀树草原过渡。",
 "overview":"撒哈拉南缘的半干旱过渡带，降水年际变率大，植被由荒漠草原向稀树草原过渡。",
 "time_or_place":"时期与年代待专门来源核验（详见待核实）",
 "geo":"萨赫勒位于撒哈拉南缘，降水自北向南递减且年际波动明显。地表覆盖以草原与稀树草原为主，季节性水系与风蚀过程共同塑造景观。NASA 地球观测的萨赫勒与荒漠化专题记录了该区域降水与植被变化的研究脉络。",
 "influence":"降水波动使游牧与定居农业长期交错，植被覆盖对放牧压力与降雨变化敏感。荒漠化研究强调气候波动与土地利用的共同作用，不宜归因于单一因素。",
 "polities":NAT,
 "connections":"萨赫勒横贯非洲南北过渡带，西接大西洋沿岸、东抵红海方向，是撒哈拉与稀树草原之间的生态走廊。",
 "today":"荒漠化、粮食安全与人口增长是当代议题。降水距平、植被指数与人口数据需按年份从 NASA/FAO 机构页核验。",
 "sources":["s046-earthobservatory-nasa-gov","s045-earthobservatory-nasa-gov"],
 "needs_verification":True,
 "pending_notes":"第15轮合规换源：原用 4 个数据层别名为唯一来源，不满足 D041；现改用 NASA 萨赫勒（Dust Bowl to the Sahel）与荒漠化（Defining Desertification）两个专题页，正文含 sahel/desertification/vegetation 关键词。政权与年代不展开，现状数值待按年份核验。",
 "last_update":TODAY})

# 印度河文明：无专题来源 → 降级 L1
i=T["印度河文明"]
for k in ["geo","influence","polities","connections","today","svg"]:
 i.pop(k,None)
i.update({
 "level":"L1","status":"D041合规降级L1(第15轮)",
 "definition":"印度河文明：印度河及其支流沿岸的早期城市文明，以规划城市与灌溉农业著称。",
 "overview":"印度河及其支流沿岸的早期城市文明，以规划城市与灌溉农业著称。",
 "time_or_place":"时期与年代待专门来源核验（详见待核实）",
 "sources":["s010-unesco-org","s013-fao-org"],
 "needs_verification":True,
 "pending_notes":"第15轮 D041 合规检查：原 L2 仅以 4 个数据层别名页为来源，不符合「一专题页 + 一机构页」；现无可用印度河考古专题页（Livius 无对应分类、UNESCO WHC 403），降级 L1。待哈拉帕/摩亨佐达罗考古专题来源到位后再升级。",
 "last_update":TODAY})

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("萨赫勒带 → L2 换源完成；印度河文明 → L1")