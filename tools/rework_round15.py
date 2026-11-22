# -*- coding: utf-8 -*-
"""第15轮抽检返工：
- 北美冰盖、山地农业降级 L1（专题页为 PDF 门落户 / 门户首页，不满足 D041）；
- 格陵兰岛、人口迁移逐条化 pending_notes；
- sources.json 补 URL 漂移与可达性说明。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

DOWN={
"北美冰盖":("北美冰盖：地质历史时期覆盖北美北部的巨大冰体，对当地地形与水系留下深远影响。",
 ["s038-earthobservatory-nasa-gov","s056-earthquake-usgs-gov"],
 "二次返工：抽检 FAIL——usgs-glaciers 实为 PDF 下载门落户（正文仅冰川定义），nps-grand-canyon-geology 为大峡谷地层页（冰川关键词 0），属跨条目凑数；geo 的「侵蚀基岩/冰碛/冰川湖/覆盖北美北部」无源。已降级 L1。待含 Laurentide / continental ice sheet 正文的专题页到位后再升级。"),
"山地农业":("山地农业：在高差大、坡度陡的地区进行的农业活动，常以梯田与多样作物组合适应环境。",
 ["s016-fao-org","s083-fao-org"],
 "二次返工：抽检 FAIL——fao-mountain-partnership 为门户首页，39 次 mountain 命中全部来自导航菜单与新闻标题，soil/erosion/terrace/slope/altitude 命中均为 0；「垂直气候带/土层薄/易侵蚀/梯田」无源。已降级 L1。待 FAO 山地正文页（山地生态系统或山地农业专文）到位后再升级。"),
}

for t,(defn,srcs,note) in DOWN.items():
 e=T[t]
 for k in ["geo","influence","polities","connections","today","svg"]:
  e.pop(k,None)
 e.update({"level":"L1","status":"二次返工降级L1(第15轮)","definition":defn,
  "overview":defn.split("：",1)[1],"time_or_place":"时期与年代待专门来源核验（详见待核实）",
  "sources":srcs,"needs_verification":True,"pending_notes":note,"last_update":TODAY})

# 保留的两条 L2：逐条化 pending_notes
T["格陵兰岛"]["pending_notes"]="第15轮按 D041 升级：专题页 nasa-ice-sheets（Earth Indicator: Ice Sheets）正文含 greenland/ice sheet 关键词，支撑冰体质量变化与海平面关联的概述；s039 为 NASA 气候机构页。政权与年代不展开；冰量、气温与融水数值待按年份从 NASA 冰盖指标页核验。"
T["人口迁移"]["pending_notes"]="第15轮按 D041 升级：专题页 owid-migration 正文含 migration/migrant 关键词，支撑迁移流与存量概述；s004 为 UN 人口司 WPP 机构页（首页为 JS 壳，无正文，仅作机构入口）。城市化与国际迁移口径因国家而异，净迁移率等数值待按年份核验。"

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# sources.json 补记
P=os.path.join(DATA,"sources.json")
sd=json.load(open(P,encoding="utf-8"))
DRIFT={
 'nasa-ice-sheets':'第15轮核验补充：现跳转至 science.nasa.gov/earth/explore/earth-indicators/ice-sheets/，标题一致；正文含 greenland/ice sheet 关键词，可作专题支撑。',
 's039-climate-nasa-gov':'第15轮核验补充：现跳转至 science.nasa.gov/climate-change/，标题一致。',
 's083-fao-org':'第15轮核验补充：现跳转至 fao.org/global-soil-partnership/soil-data/en，标题一致；mountain 命中 0，不用于山地条目。',
 's038-earthobservatory-nasa-gov':'第15轮核验补充：/features 与根路径均跳转至 science.nasa.gov/earth/earth-observatory/，专题正文不再在该 URL 提供，按机构页级别使用。',
 'fao-aquastat-basins':'第15轮核验补充：现跳转至 /countries-and-basins/index.html，为流域目录页，无单流域正文。',
 's058-worldbank-org':'第15轮核验补充：现 301 至 worldbank.org/ext/en/development-topics，为泛化 topics 索引，内容已漂，不用于具体专题断言。',
 's011-unesco-org':'第15轮核验补充：存在间歇性 connection reset（3 次 curl 中 2 次失败），间歇可达，不作内容依据。',
 's004-population-un-org':'第15轮核验补充：首页为 JS 壳（正文约 26 字符），仅作机构入口，不含数据正文。',
 'usgs-glaciers':'第15轮核验补充：该页为 PDF 下载门落户（正文仅冰川定义），不满足 D041 专题页要求，未用于升级。',
 'fao-mountain-partnership':'第15轮核验补充：该页为 Mountain Partnership 门户首页，关键词命中来自导航与新闻标题，不满足 D041 专题页要求，未用于升级。',
}
for s in sd["sources"]:
 if s["id"] in DRIFT: s["note"]=s["note"]+" "+DRIFT[s["id"]]
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("降级:",list(DOWN))
print("sources 补记:",len(DRIFT))