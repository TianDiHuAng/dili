# -*- coding: utf-8 -*-
"""第15轮 B1 缺口发现：按 D041 规则探测专题页，并用主题关键词验证正文支撑。"""
import subprocess,re,html,json,os
from concurrent.futures import ThreadPoolExecutor

CANDIDATES=[
 # (主题, url, 关键词正则)
 ("大堡礁","https://oceanservice.noaa.gov/facts/coral_reef.html",r"coral|reef"),
 ("大堡礁","https://www.noaa.gov/education/resource-collections/ocean-coasts/coral-reef-ecosystems",r"coral|reef"),
 ("格陵兰岛","https://science.nasa.gov/earth/earth-observatory/greenland/",r"greenland|ice sheet"),
 ("格陵兰岛","https://climate.nasa.gov/vital-signs/ice-sheets/",r"ice sheet|greenland"),
 ("北美冰盖","https://www.usgs.gov/programs/climate-research-and-development-program/science/glaciers",r"glacier|ice"),
 ("北美冰盖","https://pubs.usgs.gov/gip/glaciers/",r"glacier|ice"),
 ("墨西哥湾","https://www.noaa.gov/education/resource-collections/ocean-coasts/gulf-of-mexico",r"gulf of mexico"),
 ("墨西哥湾","https://oceanservice.noaa.gov/facts/deadzone.html",r"dead zone|hypoxia|gulf"),
 ("尼罗河三角洲","https://www.fao.org/aquastat/en/countries-and-basins/basins/nile",r"nile"),
 ("尼罗河三角洲","https://earthobservatory.nasa.gov/images/event/83656",r"nile|delta"),
 ("湄公河三角洲","https://www.fao.org/aquastat/en/countries-and-basins/basins/mekong",r"mekong"),
 ("冲积平原","https://www.nps.gov/subjects/geology/fluvial-processes.htm",r"fluvial|alluvial|floodplain"),
 ("山地农业","https://www.fao.org/mountain-partnership/en/",r"mountain"),
 ("人口迁移","https://www.un.org/development/desa/pd/themes/migration",r"migration"),
 ("人口迁移","https://ourworldindata.org/migration",r"migration"),
 ("城市起源","https://www.nps.gov/subjects/archeology/index.htm",r"archeolog"),
 ("阿兹特克","https://www.nps.gov/subjects/internationalcapacitybuilding/index.htm",r"."),
 ("长江流域","https://www.fao.org/aquastat/en/countries-and-basins/basins/yangtze",r"yangtze"),
 ("科罗拉多高原","https://www.nps.gov/subjects/geology/plateaus.htm",r"plateau"),
 ("五大湖","https://www.epa.gov/greatlakes/great-lakes-atlas",r"great lakes"),
]
UA="Mozilla/5.0"

def probe(item):
    topic,url,rx=item
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A",UA,"-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return topic,url,0,None,0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
        t=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
        text=re.sub(r"<[^>]+>"," ",b)
        text=re.sub(r"\s+"," ",html.unescape(text))
        hits=len(re.findall(rx,text,re.I))
        return topic,url,int(c.strip()),t,len(b),hits
    except Exception:
        return topic,url,0,None,0,0

def main():
    with ThreadPoolExecutor(max_workers=10) as ex:
        res=list(ex.map(probe,CANDIDATES))
    ok=[]
    for topic,url,code,title,n,hits in res:
        verdict="OK" if (code and code<400 and title and hits>=3 and n>8000) else ("weak" if code and code<400 else "no")
        print(f"{verdict:>5} code={code:>3} len={n:>7} hits={hits:>3} | {topic} | {title} | {url}")
        if verdict=="OK": ok.append({"topic":topic,"url":url,"title":title,"hits":hits,"len":n})
    json.dump(ok,open("reports/round15_topic_candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("USABLE",len(ok))

if __name__=="__main__": main()