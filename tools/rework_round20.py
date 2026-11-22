# -*- coding: utf-8 -*-
"""第20轮返工：
1) 渔业资源：五段收敛到 NOAA Sustainable Fisheries 页可支撑的管理表述，补 D053 标注；
2) 土壤资源：GSP 页实质正文仅 2076 字符，档①不成立 → 不升级，保持 L1 并记录；
3) 宋代分级改写；4) 蒙古帝国/黎凡特补壳别名说明。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 渔业资源：管理导向的五段（来源页为 Sustainable Fisheries：stock assessment/bycatch/overfishing/rebuild/Magnuson）
f=T["渔业资源"]
f.update({
 "level":"L2","status":"L2完成(第20轮)-主题页",
 "definition":"渔业资源：可被捕捞利用的鱼类与无脊椎动物种群，其状况由种群评估判断，并受捕捞压力与管理措施影响。",
 "overview":"可被捕捞利用的鱼类与无脊椎动物种群，其状况由种群评估判断，并受捕捞压力与管理措施影响。",
 "time_or_place":"现代渔业管理实践（年份以来源页面为准）",
 "geo":"渔业资源分布于海洋与内陆水域，资源状况需按种群分别评估。种群评估以渔获、调查与生物学数据推算资源量与可持续捕捞水平，是管理决策的技术基础。",
 "influence":"过度捕捞会削弱种群的生产力与恢复能力，兼捕则影响非目标物种与栖息地。限额管理、兼捕减少措施与种群重建计划是主要应对手段，成效取决于监测与执行。",
 "polities":"本条不展开政权序列；配额分配、渔业权属与执法属治理议题，具体制度待专门资料核验。",
 "connections":"渔业通过贸易与加工链连接产地与消费市场；共享种群与洄游物种使邻国间的管理协作成为必要。",
 "today":"多国依据法定框架实施种群评估与捕捞限额。资源量、上岸量与配额数据需按年份从 NOAA/FAO 机构页核验。",
 "sources":["noaa-sustainable-fisheries","s051-fisheries-noaa-gov"],
 "needs_verification":True,
 "pending_notes":"第20轮按 D055 档①升级：专题页 noaa-sustainable-fisheries 标题即主题、剥离后 19729 字符、fisher|sustainab 命中 165。五段已收敛到该页可支撑的管理内容（种群评估/限额/兼捕/重建），删除「上升流/大陆架/河口/水温饵料」等生态分布断言（该页 habitat/continental shelf/upwelling 命中为 0）。D053：第二源 s051 为 NOAA Fisheries 门户首页，不构成独立正文依据。"})
f["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='渔业管理示意图'>"
 "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
 "<ellipse cx='300' cy='190' rx='130' ry='62' fill='none' stroke='var(--accent)' stroke-width='3'/>"
 "<ellipse cx='520' cy='240' rx='90' ry='45' fill='none' stroke='var(--accent)' stroke-width='3'/>"
 "<path d='M300 190 L520 240' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='5 4'/>"
 "<circle cx='300' cy='190' r='5' class='pt'/><text x='250' y='165' class='lbl'>种群评估</text>"
 "<circle cx='520' cy='240' r='5' class='pt'/><text x='500' y='290' class='lbl'>限额管理</text>"
 "<text x='40' y='370' class='dim'>渔业管理 · 简笔示意，非精确测绘</text></svg>")

# 2) 土壤资源：不升级，记录原因
s=T["土壤资源"]
s["pending_notes"]=((s.get("pending_notes") or "")+
 " 【第20轮】拟按 D055 升级未成立：fao-global-soil-partnership 剥离后 5215 字符，但剔除新闻块与视频列表后实质正文约 2076 字符（<5000 门槛），页面主体为伙伴关系治理而非土壤本体；相应五段（盐渍化/有机质/固碳/保护性耕作/母质/地带性）在该页命中为 0。保持 L1，待土壤本体专题页（≥5000 实质字符）到位后再升级。")

# 3) 宋代分级改写
song=T.get("宋代")
if song:
 song["pending_notes"]=(song.get("pending_notes") or "").replace(
  "【第20轮来源分级】别名 4 + 机构 1（专题页缺失）",
  "【第20轮来源分级】全别名（其中 s014-fao-org 为 FAOSTAT 壳页，可视正文约 7 字符，不构成正文依据）")

# 4) 蒙古帝国/黎凡特补说明
for t in ["蒙古帝国","黎凡特"]:
 e=T.get(t)
 if e:
  e["pending_notes"]=(e.get("pending_notes") or "")+" D053：现有来源含壳别名（wikipedia-regions 约 5 字符）与门户首页（s075 AAG），均不构成独立正文依据。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))