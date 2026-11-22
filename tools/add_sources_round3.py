# -*- coding: utf-8 -*-
"""第3轮 B1/B6 新增来源核验并追加到 sources.json。"""
import json, os, re, html, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT,"data","sources.json")
UA = "Mozilla/5.0"
NEW = [
 ("noaa-phenology","How spring plant milestones are shifting in response to changing climate","NOAA Climate.gov",None,"官方机构","https://www.climate.gov/news-features/event-tracker/how-spring-plant-milestones-are-shifting-response-changing-climate"),
 ("nasa-arctic-fire","Fire on Ice: The Arctic’s Changing Fire Regime","NASA Earth Observatory",None,"官方机构","https://science.nasa.gov/earth/earth-observatory/fire-on-ice-the-arctics-changing-fire-regime/"),
 ("nasa-pine-island","Retreat at Pine Island Glacier","NASA Earth Observatory",None,"官方机构","https://science.nasa.gov/earth/earth-observatory/retreat-at-pine-island-glacier/"),
 ("openstax-intro-geo","Introduction to Geography","OpenStax",None,"教材目录","https://openstax.org/details/books/introduction-geography"),
 ("openstax-human-geo","Human Geography","OpenStax",None,"教材目录","https://openstax.org/details/books/human-geography"),
]

def fetch(url):
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A",UA,
                      "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=40)
    raw=p.stdout.decode("utf-8","ignore")
    if "__HTTP__" not in raw: return 0,None
    body,code=raw.rsplit("\n__HTTP__",1)
    m=re.search(r"<title[^>]*>(.*?)</title>",body,re.I|re.S)
    title=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
    return int(code.strip()),title

def main():
    doc=json.load(open(P,encoding="utf-8"))
    have={s["url"] for s in doc["sources"]}
    added=[]
    for sid,title,author,year,typ,url in NEW:
        code,ptitle=fetch(url)
        if code and code<400 and ptitle:
            verified=True; link_ok=True; note=f"curl 实测 HTTP {code}；页面标题：{ptitle}；年份未标注。"
        else:
            verified=False; link_ok=("blocked" if code in (401,403,429,503) else False); note=f"curl 实测 HTTP {code}；未核验。"
        if url in have:
            continue
        doc["sources"].append({"id":sid,"title":title,"author":author,"year":year,"type":typ,
            "url":url,"url2":None,"link_ok":link_ok,"verified":verified,"page_title":ptitle,
            "note":note+("；页面为前端渲染，静态标题为站点名，需浏览器复核目录。" if sid.startswith("openstax") else "")})
        added.append((sid,code,ptitle,verified))
    json.dump(doc,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    for a in added: print(a)
    print("新增来源",len(added),"；已核验总数",sum(1 for s in doc["sources"] if s["verified"]))

if __name__=="__main__": main()
