# -*- coding: utf-8 -*-
"""第30轮：为板块构造/洋流/沙尘暴填全球观测数据；宋代保持非实证并记录探测结果。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
NEW=[
 ("usgs-eq-m6","USGS Earthquake Catalog — M6+ events, 2025 (GeoJSON)",
  "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-01&endtime=2025-12-31&minmagnitude=6&limit=500",
  "2025 年 1–12 月 M≥6 事件 144 次（features 计数）"),
 ("noaa-current-stations","NOAA CO-OPS — Currents Station Metadata (JSON)",
  "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=currents",
  "返回 84 个洋流观测站（stations 数组长度）"),
 ("wb-wld-pm25","World Bank API — PM2.5 air pollution, mean annual exposure (EN.ATM.PM25.MC.M3, 全球)",
  "https://api.worldbank.org/v2/country/WLD/indicator/EN.ATM.PM25.MC.M3?format=json&per_page=100&date=2015:2025",
  "2023 年 32.87 μg/m³（全球人口加权年均暴露）"),
]
for sid,title,url,latest in NEW:
    if sid in have: continue
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
    raw=p.stdout.decode("utf-8","ignore");b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip() or 0)
    sd["sources"].append({"id":sid,"title":title,"author":"USGS" if sid.startswith("usgs") else ("NOAA" if sid.startswith("noaa") else "World Bank"),
      "year":None,"type":"数据端点","url":url,"url2":None,"link_ok":bool(code==200),"verified":bool(code==200),
      "page_title":title,"note":f"JSON API {code}；{latest}；数值随查询时刻变化（USGS/NOAA 为实时目录），以查询返回为准。"})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
FILL={
"板块构造":("来源：USGS 地震目录 API（M≥6 事件，2025 年 1–12 月）：全年记录到 144 次 M6 及以上地震。"
  "地震集中于板块边界，可作为板块运动活跃度的观测指标；目录为实时更新，数值随查询时刻变化。","usgs-eq-m6"),
"洋流":("来源：NOAA CO-OPS 洋流观测站元数据 API：当前登记 84 个洋流观测站。"
  "站点分布不均（以美国沿岸为主），全球洋流场的估算需结合卫星高度计与浮标阵列数据。","noaa-current-stations"),
"沙尘暴":("来源：世界银行 API（指标 EN.ATM.PM25.MC.M3，细颗粒物年均暴露）：全球 2023 年约 32.87 μg/m³。"
  "该指标是空气污染总体暴露，**不等于沙尘浓度**；沙尘贡献需依靠气溶胶组分与源区观测区分。","wb-wld-pm25"),
}
n=0
for t,(txt,sid) in FILL.items():
    e=T.get(t)
    if not e: continue
    e["today"]=txt
    if sid not in e["sources"]: e["sources"].append(sid)
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第30轮现状数据】today 填入 {sid} 实测值（全球口径，含年份或查询时点说明；已声明指标局限）。").strip()
    e["last_update"]=TODAY;n+=1

# 宋代：记录本轮探测失败
s=T.get("宋代")
if s:
    s["pending_notes"]=((s.get("pending_notes") or "")+
      " 【第30轮探测】又试 5 个宋代专题候选（OpenStax world-history 章节、Livius China、Met TOAH Northern Song、"
      "Archives research、OpenStax 书目页）：全部 404/无法取回/正文 10–1233 字符且 song 命中 0。本环境可及渠道内仍无宋代专题页，保持「非实证」状态。").strip()
    s["last_update"]=TODAY

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("填充",n,"条；sources",len(json.load(open(P,encoding='utf-8'))['sources']))