# -*- coding: utf-8 -*-
"""第23轮 B1：探测剩余遗产 L2 与核心 L1 的专题页（D055 分档）。"""
import subprocess,re,html,json
C=[
 ("洋流","https://oceanservice.noaa.gov/facts/current.html",r"current"),
 ("洋流","https://www.noaa.gov/jetstream/ocean/ocean-currents",r"current"),
 ("季风系统","https://www.noaa.gov/jetstream/global/monsoon",r"monsoon"),
 ("气候带","https://www.noaa.gov/jetstream/global/climate-zones",r"climate zone|climate"),
 ("河流三角洲","https://oceanservice.noaa.gov/facts/river-delta.html",r"delta"),
 ("河流三角洲","https://www.nps.gov/subjects/geology/deltas.htm",r"delta"),
 ("撒哈拉沙漠","https://earthobservatory.nasa.gov/features/Sahara",r"sahara"),
 ("东非大裂谷","https://earthobservatory.nasa.gov/features/EastAfricanRift",r"rift"),
 ("东非大裂谷","https://www.nps.gov/subjects/geology/rift-valleys.htm",r"rift"),
 ("两河流域","https://www.nps.gov/subjects/archeology/mesopotamia.htm",r"mesopotamia"),
 ("丝绸之路","https://www.nps.gov/subjects/internationalcapacitybuilding/silk-road.htm",r"silk road"),
 ("罗马帝国","https://www.nps.gov/subjects/archeology/roman-empire.htm",r"roman"),
 ("玛雅文明","https://www.nps.gov/subjects/archeology/maya.htm",r"maya"),
 ("安第斯山脉","https://earthobservatory.nasa.gov/features/AndesMountains",r"andes"),
 ("大平原","https://www.nps.gov/subjects/grasslands/index.htm",r"grassland|prairie"),
 ("大平原","https://www.usda.gov/oce/grassland",r"grassland"),
 ("白令陆桥","https://www.nps.gov/subjects/beringia/index.htm",r"beringia|bering"),
 ("大分水岭","https://www.bom.gov.au/climate/about-australian-weather",r"divide|australia"),
 ("澳大利亚大陆","https://www.bom.gov.au/climate/about-australian-weather",r"australia|climate"),
 ("长江流域","https://earthobservatory.nasa.gov/features/YangtzeRiver",r"yangtze"),
 ("汉代","https://www.metmuseum.org/toah/hd/hand/hd_hand.htm",r"han"),
 ("阿兹特克","https://www.metmuseum.org/toah/hd/azte/hd_azte.htm",r"aztec"),
 ("城市起源","https://www.nps.gov/subjects/archeology/cities.htm",r"city"),
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
json.dump(ok,open("reports/round23_candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",len(ok),[x["topic"] for x in ok])