# -*- coding: utf-8 -*-
"""第15轮第三批返工：
- 萨赫勒带：修正降水梯度方向、删无源句、改游牧表述、today 来源对齐；
- 山地农业：definition 去无源断言；
- 37 条 D041 前遗产 L2：加 status 后缀并在 coverage 标记；
- 人口迁移 theme 与 today 来源对齐。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 萨赫勒带正文修正
s=T["萨赫勒带"]
s["definition"]="萨赫勒带：撒哈拉南缘的半干旱过渡带，降水在南北向存在明显梯度且年际变率大。"
s["overview"]="撒哈拉南缘的半干旱过渡带，降水在南北向存在明显梯度且年际变率大。"
s["geo"]="萨赫勒位于撒哈拉南缘，向南过渡到稀树草原，降水随纬度南移而增加，年际波动明显。地表以草原与稀树草原为主。NASA 地球观测的萨赫勒与荒漠化专题记录了该区域干旱、沙尘输运与植被变化的研究脉络。"
s["influence"]="降水波动与过度放牧、农业扩张共同影响植被覆盖，是荒漠化研究的核心议题。相关研究强调气候波动与土地利用的共同作用，不宜归因于单一因素。"
s["connections"]="萨赫勒横贯非洲南北过渡带，西接大西洋沿岸、东抵红海方向，是撒哈拉与稀树草原之间的生态过渡带。"
s["today"]="荒漠化、粮食安全与人口增长是当代议题。降水距平、植被指数与人口数据需按年份从 NASA 机构页核验。"
s["pending_notes"]="第15轮三批返工：修正降水梯度方向（自北向南递增），删除「季节性水系/风蚀塑造景观」等无源句，把「游牧与定居交错」改为有 overgrazing/livestock 支撑的表述，today 来源与 sources 对齐（仅 NASA）。政权与年代不展开。"
s["last_update"]=TODAY

# 2) 山地农业 definition 去无源断言
m=T["山地农业"]
m["definition"]="山地农业：在高差大、坡度陡的地区进行的农业活动，耕作方式随海拔与坡面条件变化。"
m["overview"]="在高差大、坡度陡的地区进行的农业活动，耕作方式随海拔与坡面条件变化。"
m["pending_notes"]="二次返工：抽检 FAIL——fao-mountain-partnership 为门户首页（39 次 mountain 命中全来自导航，soil/erosion/terrace/slope/altitude 均为 0）。已降级 L1，并移除定义中「梯田与多样作物组合」这一无源断言。待 FAO 山地正文页到位后再升级。"
m["last_update"]=TODAY

# 3) 人口迁移：today 来源对齐（sources 无 NOAA），theme 保持枚举内并加注
p=T["人口迁移"]
p["today"]="城市化与国际迁移是当代主要趋势，统计口径因国家而异。净迁移率、城市化率与人口分布数据需按年份从 UN/OWID 机构页核验。"
p["pending_notes"]="第15轮按 D041 升级：专题页 owid-migration 正文含 migration/migrant 关键词，支撑迁移流与存量概述；s004 为 UN 人口司 WPP 机构页（首页为 JS 壳，无正文，仅作机构入口）。theme 受现有枚举限制标为「区域」，实指人口/迁移维度；数值待按年份核验。"
p["last_update"]=TODAY

# 4) D041 前遗产 L2 标记（仅加 status 后缀与 coverage 标记，不改 level、不动内容）
LEGACY_TAG="（D041 前遗产 L2·待补专题页）"
ALIAS={"britannica-regions","wikipedia-regions","un-m49","ap-human-geo"}
tagged=[]
for u,d in docs.items():
 for e in d["entries"]:
  if e["level"]!="L2": continue
  if e["title"] in ("五大湖","科罗拉多高原","格陵兰岛","人口迁移","萨赫勒带"): continue
  srcs=set(e.get("sources",[]))
  thematic=[x for x in srcs if x not in ALIAS]
  weak=(len(thematic)==0) or (len(thematic)==1 and any(k in (thematic[0] or "") for k in ("s056-earthquake","s057-databank","s011-unesco","s014-fao")))
  if weak:
   if LEGACY_TAG not in e["status"]:
    e["status"]=e["status"]+LEGACY_TAG
   e["pending_notes"]=(e.get("pending_notes") or "")+" 【D041 标记】本条为规则生效前的 L2，来源以数据层别名为主，未满足「一专题页+一机构页」，待补专题来源后重新校验。"
   e["last_update"]=TODAY
   tagged.append(e["title"])

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# coverage 加 legacy 标记位
cp=os.path.join(DATA,"coverage.json")
cov=json.load(open(cp,encoding="utf-8"))
bytitle={e["title"]:e["id"] for d in docs.values() for e in d["entries"]}
legacy_ids={bytitle[t] for t in tagged if t in bytitle}
for c in cov["entries"]:
 if c["id"] in legacy_ids: c["d041_legacy"]=True
cov["d041_legacy_count"]=len(legacy_ids)
json.dump(cov,open(cp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("萨赫勒/山地/人口 已修；遗产 L2 tagged:",len(tagged))