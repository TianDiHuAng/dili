# -*- coding: utf-8 -*-
"""第19轮返工。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 地理信息系统：改 geo 表述 + 修错字 + ogc 壳页标注
g=T["地理信息系统"]
g["geo"]="空间数据以坐标与属性记录地表要素，GIS 把位置数据与描述性信息连到地图上，用于查询、空间分析与制图可视化，从而比较不同区域的区位关系。"
g["time_or_place"]="方法体系（形成年代待专门来源核验）"
g["pending_notes"]=((g.get("pending_notes") or "")+
 " 【第19轮返工】geo 已改为来源页实有表述（把位置数据与描述信息连到地图、空间分析与制图），删「叠加分析/缓冲区/网络分析」等无源列举；修正 time_or_place 错字。"
 " D053：第二源 ogc-standards 剥离后正文仅约 73 字符（内容在 script/nav 内），不构成独立依据。")

# 2) 植物物候变化：删无源断言
ph=T["植物物候变化"]
ph["influence"]="物候改变影响展叶与开花期的同步性，也影响农事时序安排；观测到的变化幅度因物种与地区而异，不作单一结论。"
ph["pending_notes"]=((ph.get("pending_notes") or "")+
 " 【第19轮返工】删除「传粉者/植食者错配」「生态系统碳交换」等无源断言（NOAA 页 pollinat/insect/mismatch/carbon 命中均为 0），改为正文可支撑的同步性与农事时序。"
 " D053：第二源 s026（OWID Climate Change）正文 phenolog/plant 命中 0，不构成独立依据。")

# 3) 北极火情变化：删反照率/烟雾输送
af=T["北极火情变化"]
af["influence"]="火灾燃烧深入富碳土层，改变地表水文与融雪过程，并产生影响居民健康的烟雾；对生态与社区的影响取决于火季长度与管理能力。"
af["connections"]="火情改变地表状态与碳库，是北极系统变化的一部分；跨区域影响需结合监测数据评估。"
af["pending_notes"]=((af.get("pending_notes") or "")+
 " 【第19轮返工】删除「改变地表反照率并形成正反馈」「烟雾与碳输送到中纬度」等无源断言（albedo/feedback 命中为 0，smoke 仅健康风险语境），改为正文可支撑的富碳土层燃烧、水文改变、融雪加速与烟雾健康风险。")

# 4) 城市化水平 / 城市热岛：恢复 s025 到正确主题
for t,tag in [("城市化水平","城市化水平"),("城市热岛","城市热岛")]:
 e=T.get(t)
 if not e: continue
 if "s025-ourworldindata-org" not in e["sources"]:
  e["sources"].insert(0,"s025-ourworldindata-org")
  e["pending_notes"]=((e.get("pending_notes") or "")+
   f" 【第19轮返工】恢复 s025（OWID Urbanization）为本条专题来源——第19轮批次2 清理时按「本轮主题」误移，实际{tag}正是其主题；D055 留痕：来源是否错配按**条目主题**判定，非按全局。")

# 5) 名义双源标注
D053={"南锥体":"s026（OWID Climate Change，正文 urban/population 命中 0）与 un-m49（M49 分组表，urban 命中 0）对「南锥体」均无主题支撑",
 "城市热岛":"s044（Earth Observatory 首页）与 s039（气候总览）为机构入口级",
 "人口地理":"s004（UN Population Prospects 首页，剥离后约 26 字符 JS 壳页）"}
for t,desc in D053.items():
 e=T.get(t)
 if e and "D053" not in (e.get("pending_notes") or ""):
  e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第19轮 D053 标注】{desc}，不构成第二独立依据；已列入下轮换源清单。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 6) sources note: ogc / s004 壳页
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
 if s["id"]=="ogc-standards" and "73 字符" not in (s.get("note") or ""):
  s["note"]=(s.get("note") or "")+" 第19轮核验补充：raw 约 1.25MB 但剥离 nav/header/script 后正文仅约 73 字符，内容主要在脚本与导航内；仅作入口，不构成独立依据。"
 if s["id"]=="s004-population-un-org" and "26 字符" in (s.get("note") or ""):
  pass
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("返工完成：GIS/植物物候/北极火情/城市化水平/城市热岛/D053标注/ogc note")