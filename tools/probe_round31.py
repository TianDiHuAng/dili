# -*- coding: utf-8 -*-
"""第31轮 B1：南极/观测类数据端点探测。"""
import subprocess,re,json,os,html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C=[
 ("南极冰盖","https://climate.nasa.gov/vital-signs/ice-sheets/",r"ice sheet|greenland|antarctic"),
 ("南极冰盖","https://sealevel.nasa.gov/understanding-sea-level/global-sea-level/overview",r"sea level"),
 ("南极冰盖","https://earth.gsfc.nasa.gov/cryo/data/ice-sheet-mass-balance",r"mass|balance|ice"),
 ("南极大陆","https://nsidc.org/antarctica-today",r"antarctic"),
 ("南极大陆","https://www.antarctica.gov.au/about-antarctica/",r"antarctic"),
 ("南极条约体系","https://www.ats.aq/devAS/Parties?lang=e",r"parties|antarctic"),
 ("冰芯气候记录","https://www.ncdc.noaa.gov/icecore",r"ice core"),
 ("冰芯气候记录","https://climate.nasa.gov/vital-signs/carbon-dioxide/",r"co2|carbon"),
 ("植物物候变化","https://www.usanpn.org/data/observations",r"phenolog|observation"),
 ("北极火情变化","https://www.noaa.gov/news-release/arctic-report-card-2025",r"arctic"),
 ("卫星遥感地表观测","https://api.nasa.gov/planetary/earth/assets?lon=0&lat=0&date=2020-01-01&api_key=DEMO_KEY",r"url|date"),
 ("二氧化碳排放清单","https://api.worldbank.org/v2/country/WLD/indicator/EN.GHG.CO2.MT.CE.AR5?format=json&per_page=100&date=2015:2022",r"co2|value"),
 ("二氧化碳排放清单","https://api.worldbank.org/v2/country/WLD/indicator/EN.ATM.CO2E.PC?format=json&per_page=100&date=2015:2025",r"co2|value"),
 ("农业企业与价值链","https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.AGRI.ZS?format=json&per_page=100&date=2015:2025",r"agric|value"),
 ("地理信息系统","https://api.nasa.gov/",r"api|nasa"),
 ("城市地理","https://api.worldbank.org/v2/country/WLD/indicator/SP.URB.GROW?format=json&per_page=100&date=2015:2025",r"urban|value"),
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
        isj=b.strip().startswith(("{","["))
        txt=b if isj else re.sub(r"\s+"," ",H.unescape(re.sub(r"<[^>]+>"," ",strip(b))))
        n=len(txt);h=len(re.findall(rx,txt,re.I))
        reason=("HTTP %d"%code if code>=400 else ("内容过短 %d"%n if n<300 else ("命中 0" if h<1 else "达标")))
        rows.append({"topic":topic,"url":u,"http":code,"len":n,"hits":h,"reason":reason})
        print(f"{'OK' if reason=='达标' else '--'} {code:>3} len={n:>7} hits={h:>4} | {topic:<12} | {reason}")
    except Exception as ex:
        rows.append({"topic":topic,"url":u,"http":0,"len":0,"hits":0,"reason":f"异常 {type(ex).__name__}"})
        print("ERR",topic,type(ex).__name__)
json.dump({"round":31,"rows":rows,"usable":sum(1 for x in rows if x["reason"]=="达标")},
  open(os.path.join(ROOT,"reports","round31_probe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("可用",sum(1 for x in rows if x["reason"]=="达标"),"/",len(rows))