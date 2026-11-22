# -*- coding: utf-8 -*-
"""第24轮 B1：试取数层（JSON API / PDF 直链 / 数据端点），不再只抓 HTML。"""
import subprocess,re,html,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C=[
 # (主题, url, 期望内容类型, 关键词)
 ("世界银行国家数据","https://api.worldbank.org/v2/country/CHN?format=json",r"China|CHN",100),
 ("世界银行指标","https://api.worldbank.org/v2/country/CHN/indicator/SP.POP.TOTL?format=json",r"Population|value",100),
 ("USGS 地震目录","https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=5",r"features|metadata",200),
 ("NASA 图像库","https://images-api.nasa.gov/search?q=amazon%20deforestation",r"collection|items",200),
 ("NPS 公园数据","https://developer.nps.gov/api/v1/parks?limit=2&api_key=DEMO_KEY",r"parks|data",200),
 ("OWID 图表数据","https://ourworldindata.org/grapher/population.csv",r"population|Entity",200),
 ("USGS 冰川 PDF","https://pubs.usgs.gov/gip/glaciers/glaciers.pdf",r"glacier",1000),
 ("IPCC 报告","https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf",r"climate",1000),
 ("FAO 统计 API","https://fenixservices.fao.org/faostat/api/v1/en/data/QCL?area=351&item=15&element=5510&year=2022",r"data|value",100),
]
def probe(topic,u,rx,minlen):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return topic,u,0,0,0,"连接失败"
        b,c=raw.rsplit("\n__HTTP__",1)
        code=int(c.strip() or 0)
        size=len(b)
        hits=len(re.findall(rx,b,re.I))
        if code>=400: reason=f"HTTP {code}"
        elif size<minlen: reason=f"内容过短 {size}<{minlen}"
        elif hits<1: reason=f"关键词未命中 {hits}"
        else: reason="达标"
        return topic,u,code,size,hits,reason
    except Exception as ex:
        return topic,u,0,0,0,f"异常 {type(ex).__name__}"
rows=[]
for topic,u,rx,minlen in C:
    r=probe(topic,u,rx,minlen)
    rows.append({"topic":r[0],"url":r[1],"http":r[2],"bytes":r[3],"hits":r[4],"reason":r[5]})
    print(f"{'OK' if r[5]=='达标' else '--'} {r[2]:>3} bytes={r[3]:>8} hits={r[4]:>4} | {r[0]:<14} | {r[5]} | {r[1]}")
json.dump({"round":24,"layer":"api/pdf","rows":rows,"usable":sum(1 for x in rows if x['reason']=='达标')},
  open(os.path.join(ROOT,"reports","round24_probe_detail.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("可用",sum(1 for x in rows if x['reason']=='达标'),"/",len(rows))