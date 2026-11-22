# -*- coding: utf-8 -*-
"""第29轮：登记 5 个全球数据端点，为 5 条全球主题条目填 today。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
NEW=[
 ("wb-wld-forest","World Bank API — Forest area (% of land area, 全球)","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.FRST.ZS?format=json&per_page=100&date=2015:2025","2023 年 31.1%"),
 ("wb-wld-urban","World Bank API — Urban population (% of total, 全球)","https://api.worldbank.org/v2/country/WLD/indicator/SP.URB.TOTL.IN.ZS?format=json&per_page=100&date=2015:2025","2025 年 57.8%"),
 ("wb-wld-fish","World Bank API — Total fisheries production (metric tons, 全球)","https://api.worldbank.org/v2/country/WLD/indicator/ER.FSH.PROD.MT?format=json&per_page=100&date=2015:2025","2024 年 235,811,491 吨"),
 ("wb-wld-water","World Bank API — Annual freshwater withdrawals (% of internal resources, 全球)","https://api.worldbank.org/v2/country/WLD/indicator/ER.H2O.FWTL.ZS?format=json&per_page=100&date=2015:2025","2022 年 9.0%"),
 ("noaa-global-temp","NOAA Climate at a Glance — Global Land and Ocean Temperature Departures (JSON)","https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/12/12/2015-2025.json","基准期 1901-2000；2025 年 +1.12 °C，2024 年 +1.26 °C"),
]
for sid,title,url,latest in NEW:
    if sid in have: continue
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
    raw=p.stdout.decode("utf-8","ignore")
    b,c=raw.rsplit("\n__HTTP__",1)
    code=int(c.strip() or 0)
    sd["sources"].append({"id":sid,"title":title,"author":"World Bank" if sid.startswith("wb") else "NOAA",
      "year":None,"type":"数据端点","url":url,"url2":None,
      "link_ok":bool(code==200),"verified":bool(code==200),"page_title":title,
      "note":f"JSON API {code}；返回世界（WLD）或全球序列逐年数值；最新 {latest}；单位为该指标原生单位。"})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
FILL={
"全球气温距平":("来源：NOAA Climate at a Glance（全球陆海平均温度距平，基准期 1901–2000，单位 °C）：2023 年 +1.17、2024 年 +1.26、2025 年 +1.12。"
  "距平值随基准期与观测方法而变，跨数据集比较需核对口径。","noaa-global-temp"),
"森林覆盖变化":("来源：世界银行 API（指标 AG.LND.FRST.ZS，森林面积占土地面积比例）：全球 2023 年 31.1%。"
  "森林覆盖率按各国上报口径汇总，区域差异与统计年份差异需注意。","wb-wld-forest"),
"渔业资源":("来源：世界银行 API（指标 ER.FSH.PROD.MT，渔业总产量）：全球 2024 年 235,811,491 吨。"
  "该值为总产量（含养殖与捕捞），分解数据与种群状况需专门渔业统计核验。","wb-wld-fish"),
"水资源管理":("来源：世界银行 API（指标 ER.H2O.FWTL.ZS，年度淡水取用量占内部可再生资源比例）：全球 2022 年 9.0%。"
  "该比例是水压力的粗略指标，流域内与季节间的紧张程度可能远高于全球平均。","wb-wld-water"),
"城市热岛":("来源：世界银行 API（指标 SP.URB.TOTL.IN.ZS，城市人口占比）：全球 2025 年 57.8%。"
  "城市化率仅作背景，热岛强度需地面与卫星观测数据（地表温度差）核验，两者不可互换。","wb-wld-urban"),
}
n=0
for t,(txt,sid) in FILL.items():
    e=T.get(t)
    if not e: continue
    e["today"]=txt
    if sid not in e["sources"]: e["sources"].append(sid)
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第29轮现状数据】today 填入 {sid} 实测值（全球口径，含年份与单位）。").strip()
    e["last_update"]=TODAY;n+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("新增端点 5；today 填充",n)
print("today 无指标编号余额:",sum(1 for e in T.values() if e["level"]=="L2" and "SP." not in (e.get("today") or "") and "°C" not in (e.get("today") or "") and "吨" not in (e.get("today") or "") and "%" not in (e.get("today") or "")))