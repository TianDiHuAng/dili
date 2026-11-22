# -*- coding: utf-8 -*-
"""第22轮 B1：为 36 条遗产 L2 探测主题页（D055 分档）。"""
import subprocess,re,html,json
C=[
 ("板块构造","https://pubs.usgs.gov/gip/dynamic/dynamic.html",r"plate tectonics|tectonic"),
 ("板块构造","https://pubs.usgs.gov/gip/dynamic/understanding.html",r"tectonic|plate"),
 ("冰芯气候记录","https://earthobservatory.nasa.gov/features/Paleoclimatology_IceCores",r"ice core|climate"),
 ("亚马逊盆地","https://earthobservatory.nasa.gov/features/AmazonFire",r"amazon|forest"),
 ("南极冰盖","https://climate.nasa.gov/vital-signs/ice-sheets/",r"ice sheet|antarctic"),
 ("洋流","https://oceanservice.noaa.gov/facts/current.html",r"current"),
 ("洋流","https://oceanservice.noaa.gov/education/tutorial_currents/welcome.html",r"current"),
 ("季风系统","https://www.climate.gov/news-features/understanding-climate/monsoon",r"monsoon"),
 ("气候带","https://www.climate.gov/maps-data/dataset/climate-zones",r"climate zone"),
 ("河流三角洲","https://oceanservice.noaa.gov/facts/delta.html",r"delta"),
 ("撒哈拉沙漠","https://earthobservatory.nasa.gov/features/DustBowl",r"sahara|sahel"),
 ("安第斯山脉","https://earthobservatory.nasa.gov/features/Andes",r"andes"),
 ("大平原","https://www.nps.gov/subjects/grasslands/index.htm",r"grassland|prairie"),
 ("落基山脉","https://www.nps.gov/subjects/geology/mountain-building.htm",r"mountain"),
 ("东非大裂谷","https://earthobservatory.nasa.gov/features/RiftValley",r"rift"),
 ("澳大利亚大陆","https://www.bom.gov.au/climate/about/",r"australia"),
 ("白令陆桥","https://www.nps.gov/subjects/beringia/index.htm",r"beringia"),
 ("大分水岭","https://www.bom.gov.au/climate/about/?bookmark=gridded",r"divide"),
]
def strip(h):
    for t in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{t}\b.*?</{t}>"," ",h,flags=re.I|re.S)
    return h
def m(it):
    topic,u,rx=it
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return topic,u,0,None,0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        mm=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
        t=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",mm.group(1)))).strip() if mm else None
        txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",strip(b)))).strip()
        return topic,u,int(c.strip()),t,len(txt),len(re.findall(rx,txt,re.I))
    except Exception: return topic,u,0,None,0,0
ok=[]
for topic,u,c,t,n,h in [m(x) for x in C]:
    gate = 5000 if h>=30 else 8000
    good = c and c<400 and t and n>=gate and h>=3 and not re.search(r"404|not found|error|moved",t,re.I)
    print(f"{'OK ' if good else '-- '} {c:>3} body={n:>7} hits={h:>4} gate={gate:>5} | {topic} | {t}")
    if good: ok.append({"topic":topic,"url":u,"title":t,"body":n,"hits":h,"gate":gate})
json.dump(ok,open("reports/round22_candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",len(ok),[x["topic"] for x in ok])