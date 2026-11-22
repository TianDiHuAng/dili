# -*- coding: utf-8 -*-
"""第16轮 B1 缺口发现：D044 判据探测（剥离 nav/header/footer/aside 后计关键词密度）。"""
import subprocess,re,html,json

CANDIDATES=[
 ("落基山脉","https://www.nps.gov/subjects/geology/mountain-building.htm",r"mountain"),
 ("落基山脉","https://www.usgs.gov/geology-and-ecology-of-national-parks/rocky-mountain-national-park",r"rocky mountain"),
 ("落基山脉","https://www.nps.gov/romo/learn/nature/geology.htm",r"rocky|mountain"),
 ("北美冰盖","https://www.usgs.gov/programs/climate-research-and-development-program/science/glaciers-and-ice-caps",r"ice sheet"),
 ("北美冰盖","https://pubs.usgs.gov/gip/dynamic/glaciers.html",r"glacier"),
 ("北美冰盖","https://www.nps.gov/subjects/geology/glacial-landforms.htm",r"glacial|glacier"),
 ("山地农业","https://www.fao.org/mountain-partnership/our-work/en/",r"mountain"),
 ("山地农业","https://www.fao.org/3/i9993en/i9993en.pdf",r"mountain"),
 ("印度河文明","https://www.harappa.com/",r"harappa|indus"),
 ("印度河文明","https://whc.unesco.org/en/list/138",r"mohenjo"),
 ("大堡礁","https://www.gbrmpa.gov.au/",r"reef"),
 ("大堡礁","https://www.aims.gov.au/",r"reef"),
 ("墨西哥湾","https://www.nps.gov/subjects/geology/index.htm",r"geolog"),
 ("墨西哥湾","https://www.epa.gov/gulfofmexico",r"gulf"),
 ("尼罗河三角洲","https://www.fao.org/aquastat/en/geospatial-information/",r"nile"),
 ("湄公河三角洲","https://www.fao.org/aquastat/en/countries-and-basins/basins/",r"mekong"),
 ("冲积平原","https://www.usgs.gov/special-topics/water-science-school/science/rivers-and-streams",r"alluvial|floodplain"),
 ("阿契美尼德波斯","https://www.livius.org/category/achaemenid/",r"achaemenid"),
 ("阿契美尼德波斯","https://www.livius.org/articles/dynasty/achaemenid/",r"achaemenid"),
 ("阿契美尼德波斯","https://www.livius.org/articles/person/cyrus-the-great/",r"cyrus|achaemenid"),
]
UA="Mozilla/5.0"

def strip_chrome(h):
    for tag in ("nav","header","footer","aside","script","style","form"):
        h=re.sub(rf"<{tag}\b.*?</{tag}>"," ",h,flags=re.I|re.S)
    return h

def probe(item):
    topic,url,rx=item
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","22","-A",UA,"-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=32)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return topic,url,0,None,0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
        t=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
        body=strip_chrome(b)
        txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",body)))
        return topic,url,int(c.strip()),t,len(txt),len(re.findall(rx,txt,re.I))
    except Exception:
        return topic,url,0,None,0,0

def main():
    res=[probe(c) for c in CANDIDATES]
    ok=[]
    for topic,url,code,title,n,hits in res:
        good = code and code<400 and title and n>=8000 and hits>=5 and not re.search(r"404|not found|error|moved",(title or "")+url,re.I)
        print(f"{'OK' if good else 'no':>3} code={code:>3} body={n:>7} hits={hits:>4} | {topic} | {url}")
        if good: ok.append({"topic":topic,"url":url,"title":title,"body":n,"hits":hits})
    json.dump(ok,open("reports/round16_candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("USABLE",len(ok),json.dumps(ok,ensure_ascii=False,indent=1))

if __name__=="__main__": main()