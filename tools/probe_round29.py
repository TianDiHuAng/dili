# -*- coding: utf-8 -*-
"""第29轮 B1：为全球主题条目探测数据端点（JSON/CSV），补「现状数据」。"""
import subprocess,json,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C=[("板块构造","https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2025-01-01&endtime=2025-12-31&minmagnitude=6",r"count|features"),
 ("洋流","https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=currents",r"stations|currents"),
 ("全球气温距平","https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/12/12/2015-2025.json",r"data|anomaly|global"),
 ("二氧化碳排放清单","https://api.worldbank.org/v2/country/WLD/indicator/EN.ATM.CO2E.KT?format=json&per_page=100&date=2015:2025",r"co2|value"),
 ("森林覆盖变化","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.FRST.ZS?format=json&per_page=100&date=2015:2025",r"forest|value"),
 ("城市热岛","https://api.worldbank.org/v2/country/WLD/indicator/SP.URB.TOTL.IN.ZS?format=json&per_page=100&date=2015:2025",r"urban|value"),
 ("渔业资源","https://api.worldbank.org/v2/country/WLD/indicator/ER.FSH.PROD.MT?format=json&per_page=100&date=2015:2025",r"fish|value"),
 ("水资源管理","https://api.worldbank.org/v2/country/WLD/indicator/ER.H2O.FWTL.ZS?format=json&per_page=100&date=2015:2025",r"water|value"),
]
def probe(topic,u,rx,minlen=200):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw:
            return topic,u,0,0,0,"连接失败"
        b,cs=raw.rsplit("\n__HTTP__",1)
        c=int(cs.strip() or 0)
        hits=len(re.findall(rx,b,re.I))
        size=len(b)
        if c!=200: return topic,u,c,size,hits,f"非 JSON/HTTP 失败"
        if size<minlen: return topic,u,c,size,hits,f"内容过短 {size}"
        if hits<1: return topic,u,c,size,hits,"关键词未命中"
        return topic,u,c,size,hits,"达标"
    except Exception as ex:
        return topic,u,0,0,0,f"异常 {type(ex).__name__}"
rows=[]
for topic,u,rx in C:
    r=probe(topic,u,rx)
    rows.append({"topic":r[0],"url":r[1],"http":r[2],"bytes":r[3],"hits":r[4],"reason":r[5]})
    print(f"{'OK' if r[5]=='达标' else '--'} {r[2]:>3} bytes={r[3]:>8} hits={r[4]:>3} | {topic:<12} | {r[5]}")
json.dump({"round":29,"rows":rows,"usable":sum(1 for x in rows if x['reason']=='达标')},
  open(os.path.join(ROOT,"reports","round29_probe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("可用",sum(1 for x in rows if x['reason']=='达标'),"/",len(rows))