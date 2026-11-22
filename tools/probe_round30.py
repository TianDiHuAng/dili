# -*- coding: utf-8 -*-
"""第30轮 B1 探测：宋代专题页（多域名）＋全球观测数据端点。"""
import subprocess,re,json,os,html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C=[
 # 宋代（Song dynasty）专题
 ("宋代","https://www.openstax.org/books/world-history-volume-1/pages/13-1-song-dynasty",r"song"),
 ("宋代","https://www.livius.org/articles/place/china/",r"china|song"),
 ("宋代","https://www.metmuseum.org/toah/hd/nsong/hd_nsong.htm",r"song"),
 ("宋代","https://www.archives.gov/research/",r"song"),
 ("宋代","https://openstax.org/details/books/world-history-volume-1",r"world history"),
 # 全球观测数据
 ("板块构造","https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-01&endtime=2025-12-31&minmagnitude=6&limit=20",r"features|magnitude"),
 ("板块构造","https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2025-01-01&endtime=2025-12-31",r"count"),
 ("洋流","https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=currents",r"stations"),
 ("河流三角洲","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.IRIG.AG.ZS?format=json&per_page=100&date=2015:2025",r"irrig|value"),
 ("气候带","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.ARBL.ZS?format=json&per_page=100&date=2015:2025",r"arable|value"),
 ("季风系统","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.CROP.ZS?format=json&per_page=100&date=2015:2025",r"crop|value"),
 ("沙尘暴","https://api.worldbank.org/v2/country/WLD/indicator/EN.ATM.PM25.MC.M3?format=json&per_page=100&date=2015:2025",r"pm25|value"),
 ("荒漠化","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.FRST.ZS?format=json&per_page=100&date=2015:2025",r"forest|value"),
]
def strip(h):
    for x in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{x}\b.*?</{x}>"," ",h,flags=re.I|re.S)
    return h
rows=[]
for topic,u,rx in C:
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw:
            rows.append({"topic":topic,"url":u,"http":0,"len":0,"hits":0,"reason":"连接失败"});continue
        b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
        is_json = b.strip().startswith(("{","["))
        txt = b if is_json else re.sub(r"\s+"," ",H.unescape(re.sub(r"<[^>]+>"," ",strip(b))))
        n=len(txt); h=len(re.findall(rx,txt,re.I))
        if code>=400: reason=f"HTTP {code}"
        elif n<300: reason=f"内容过短 {n}"
        elif h<1: reason=f"命中 0"
        else: reason="达标"
        rows.append({"topic":topic,"url":u,"http":code,"len":n,"hits":h,"reason":reason,"json":is_json})
        print(f"{'OK' if reason=='达标' else '--'} {code:>3} len={n:>7} hits={h:>4} | {topic:<10} | {reason} | {u[:70]}")
    except Exception as ex:
        rows.append({"topic":topic,"url":u,"http":0,"len":0,"hits":0,"reason":f"异常 {type(ex).__name__}"})
json.dump({"round":30,"rows":rows,"usable":sum(1 for x in rows if x.get("reason")=="达标")},
  open(os.path.join(ROOT,"reports","round30_probe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("可用",sum(1 for x in rows if x.get("reason")=="达标"),"/",len(rows))