# -*- coding: utf-8 -*-
"""第24轮：登记 API/PDF 来源 + 北美冰盖用 USGS 冰川 PDF 升级 L2 + 3 条补 API 数据来源。"""
import json,os,re,sys,subprocess,zlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
have={s["id"] for s in sd["sources"]}
NEW=[
 ("usgs-glaciers-pdf","Glaciers: Clues to Future Climate (PDF)","U.S. Geological Survey",None,"官方文档",
  "https://pubs.usgs.gov/gip/glaciers/glaciers.pdf",
  "PDF 777779 字节；解压后文本 284151 字节、约 3583 词；glacier 命中 58、moraine 1。第24轮按 D064 作 PDF 专题文档使用。"),
 ("wb-api-country","World Bank Country API (CHN)","World Bank",None,"数据端点",
  "https://api.worldbank.org/v2/country/CHN?format=json",
  "JSON API 457 字节；返回国家元数据（iso2/iso3、region、incomeLevel）。用于现状数据的机构口径核对。"),
 ("wb-api-pop","World Bank Indicator API — Population (SP.POP.TOTL, CHN)","World Bank",None,"数据端点",
  "https://api.worldbank.org/v2/country/CHN/indicator/SP.POP.TOTL?format=json",
  "JSON API 9885 字节；返回逐年人口数值与 year 字段（命中 200）。可作现状数据的年份-数值核对入口。"),
 ("usgs-eq-api","USGS Earthquake Catalog API (GeoJSON)","U.S. Geological Survey",None,"数据端点",
  "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=5",
  "GeoJSON API 3885 字节；含 features/metadata，可核验地震事件的时刻与震级字段。"),
 ("nps-api-parks","NPS Data API — Parks","U.S. National Park Service",None,"数据端点",
  "https://developer.nps.gov/api/v1/parks?limit=2&api_key=DEMO_KEY",
  "JSON API 23293 字节；返回公园名录与描述字段（命中 15）。用于地名/机构口径核对。"),
]
for sid,title,author,year,typ,url,note in NEW:
    if sid in have: continue
    sd["sources"].append({"id":sid,"title":title,"author":author,"year":year,"type":typ,"url":url,"url2":None,
      "link_ok":True,"verified":True,"page_title":title,"note":note})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 北美冰盖：PDF 专题 + NASA 机构页，升级 L2
n=T["北美冰盖"]
n.update({
 "level":"L2","status":"L2完成(第24轮)-PDF专题",
 "definition":"北美冰盖：地质历史时期覆盖北美北部的巨大冰体，其进退塑造了当地地形、水系与沉积物分布。",
 "overview":"地质历史时期覆盖北美北部的巨大冰体，其进退塑造了当地地形、水系与沉积物分布。",
 "time_or_place":"时期与年代待专门来源核验（详见待核实）",
 "geo":"冰体由积雪压实形成并缓慢流动，运动过程中侵蚀基岩、搬运碎屑，退却后留下冰碛与冰川湖等堆积地貌。USGS《Glaciers: Clues to Future Climate》以冰川为气候指示物，说明冰川的形成、运动与地貌作用。",
 "influence":"冰川作用塑造盆地、丘陵与河谷，影响后来的水系与土壤分布；冰川规模变化与气候条件相联系，具体时序需区域资料细化。",
 "polities":"本条不展开具体政权序列；冰盖范围变化影响生物迁移与后续人类活动的地理条件。",
 "connections":"冰盖进退改变水系与海岸线，把北美内陆与大西洋、北冰洋的水文过程联系起来。",
 "today":"古冰盖范围与消退时间由地质与湖泊沉积记录重建；年代与范围数据需按年份从 USGS/NASA 机构页核验。",
 "sources":["usgs-glaciers-pdf","s038-earthobservatory-nasa-gov"],
 "needs_verification":True,
 "pending_notes":"第24轮按 D064 升级：专题文档为 USGS《Glaciers: Clues to Future Climate》PDF（777779 字节；解压文本 284151 字节；glacier 命中 58）。此前第15轮曾把该来源的**网页入口**（4962 字节目录页）误判为「PDF 门落户」，实际 PDF 本体是真文档——判断已纠正。第二来源 NASA Earth Observatory 为机构入口（7143 字符、命中 1），按 D053 不构成独立正文。"})
n["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='冰盖进退与冰川地貌示意图'>"
 "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
 "<path d='M80 250 C 200 170 340 160 460 190 C 560 215 640 240 690 258' fill='none' stroke='var(--accent)' stroke-width='4'/>"
 "<path d='M100 300 C 210 240 350 232 470 258' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='5 4'/>"
 "<circle cx='210' cy='200' r='5' class='pt'/><text x='180' y='180' class='lbl'>冰体</text>"
 "<circle cx='380' cy='172' r='5' class='pt'/><text x='345' y='152' class='lbl'>冰流</text>"
 "<circle cx='560' cy='232' r='5' class='pt'/><text x='540' y='212' class='lbl'>冰碛</text>"
 "<text x='40' y='370' class='dim'>北美冰盖 · 简笔示意，非精确测绘</text></svg>")

# 2) 三条现状类条目补 API 数据端点（不改正文数值，只加来源 + 注记）
for t,sid,why in [("人口地理","wb-api-pop","世界银行人口指标 API 提供逐年数值与 year 字段"),
                  ("城市化水平","wb-api-country","世界银行国家 API 提供收入分组与区域归属"),
                  ("板块构造","usgs-eq-api","USGS 地震目录 API 提供事件时刻与震级字段")]:
    e=T.get(t)
    if not e: continue
    if sid not in e["sources"]:
        e["sources"].append(sid)
        e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第24轮数据端点】新增 {sid}（{why}），用于按年份核对数值口径；本条正文未写入具体数值。"
        e["last_update"]=TODAY

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("新来源",len(NEW),"；北美冰盖 level:",T["北美冰盖"]["level"],"sources:",T["北美冰盖"]["sources"])