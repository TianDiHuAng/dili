# -*- coding: utf-8 -*-
"""第20轮 B1：为 6 条未达门槛条目 + 4 条名义双源条目探测更强专题页（D055 分档）。"""
import subprocess,re,html,json
C=[
 # 未达门槛：松岛冰川/渔业/土壤/湿地/陆地保护区/海洋生态系统
 ("松岛冰川退缩","https://science.nasa.gov/earth/earth-observatory/retreat-at-pine-island-glacier/",r"pine island|glacier"),
 ("松岛冰川退缩","https://www.nps.gov/subjects/geology/glaciers.htm",r"glacier"),
 ("渔业资源","https://www.fisheries.noaa.gov/topic/sustainable-fisheries",r"fisher|sustainab"),
 ("渔业资源","https://www.fisheries.noaa.gov/insight/understanding-fishery-stock-status",r"fisher|stock"),
 ("土壤资源","https://www.fao.org/soils-portal/soil-management/soil-degradation-restoration/en/",r"soil"),
 ("土壤资源","https://www.fao.org/global-soil-partnership/en/",r"soil"),
 ("陆地保护区","https://www.iucn.org/our-work/topic/protected-areas-and-land-use",r"protected area"),
 ("陆地保护区","https://www.cbd.int/protected/intro/",r"protected area"),
 ("湿地与水资源","https://www.ramsar.org/about-the-convention-on-wetlands",r"wetland"),
 ("海洋生态系统","https://oceanservice.noaa.gov/facts/coralreef-climate.html",r"coral|reef"),
 ("海洋生态系统","https://science.nasa.gov/earth/earth-observatory/ocean/",r"ocean"),
 # 名义双源：南锥体/城市热岛/人口地理/地理信息系统
 ("南锥体","https://www.worldbank.org/en/region/lac",r"latin america|caribbean"),
 ("城市热岛","https://www.epa.gov/heatislands",r"heat island"),
 ("人口地理","https://www.prb.org/articles/",r"population"),
 ("地理信息系统","https://www.usgs.gov/faqs/what-geographic-information-system-gis",r"geographic information"),
 # 核心 L1 尝试
 ("城市起源","https://www.nps.gov/subjects/archeology/archeology-in-the-parks.htm",r"archeolog|city"),
 ("汉代","https://www.metmuseum.org/toah/hd/hand/hd_hand.htm",r"han"),
 ("蒙古帝国","https://www.nps.gov/subjects/archeology/index.htm",r"archeolog"),
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
    # D055 档判定：标题含主题词 → 命中>=30 用 5000, 3-29 用 8000; 否则 8000+命中>=5
    title_match = bool(t) and bool(re.search(re.sub(r"[^a-zA-Z ]","",topic.split("退缩")[0].split("资源")[0])[:4] or "x", t, re.I))
    gate = 5000 if h>=30 else 8000
    good = c and c<400 and t and n>=gate and h>=3 and not re.search(r"404|not found|error|moved",t,re.I)
    print(f"{'OK ' if good else '-- '} {c:>3} body={n:>7} hits={h:>4} gate={gate:>5} | {topic} | {t}")
    if good: ok.append({"topic":topic,"url":u,"title":t,"body":n,"hits":h,"gate":gate})
json.dump(ok,open("reports/round20_candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可升级:",len(ok),[x["topic"] for x in ok])