# -*- coding: utf-8 -*-
"""第3轮返工：新增5个专题来源并核验。"""
import json, os, re, html, subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=os.path.join(ROOT,"data","sources.json")
NEW=[
 ("usgs-dynamic-earth","This Dynamic Earth: The Story of Plate Tectonics","U.S. Geological Survey",None,"官方机构","https://pubs.usgs.gov/gip/dynamic/dynamic.html"),
 ("ogc-standards","OGC Standards","Open Geospatial Consortium",None,"标准组织","https://www.ogc.org/standards/"),
 ("esri-gis","What is GIS?","Esri",None,"行业机构","https://www.esri.com/en-us/what-is-gis/overview"),
 ("fao-aquastat-basins","AQUASTAT — Countries and Basins","FAO",None,"官方机构","https://www.fao.org/aquastat/en/countries-and-basins"),
 ("noaa-glerl","NOAA Great Lakes Environmental Research Laboratory","NOAA",None,"官方机构","https://www.glerl.noaa.gov/"),
]
def fetch(u):
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
    raw=p.stdout.decode("utf-8","ignore")
    if "__HTTP__" not in raw: return 0,None
    b,c=raw.rsplit("\n__HTTP__",1)
    m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
    t=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
    return int(c.strip()),t
def main():
    d=json.load(open(P,encoding="utf-8")); have={s["url"] for s in d["sources"]}
    for sid,title,author,year,typ,url in NEW:
        code,pt=fetch(url)
        verified=bool(code and code<400 and pt)
        note=f"curl 实测 HTTP {code}；页面标题：{pt or '未取得'}；年份未标注。"
        if url in have: continue
        d["sources"].append({"id":sid,"title":title,"author":author,"year":year,"type":typ,"url":url,
          "url2":None,"link_ok":(True if verified else False),"verified":verified,"page_title":pt,"note":note})
        print(sid,code,pt,verified)
    json.dump(d,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("已核验总数",sum(1 for s in d["sources"] if s["verified"]))
if __name__=="__main__": main()
