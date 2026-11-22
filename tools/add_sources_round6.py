# -*- coding: utf-8 -*-
"""第6轮：新增并核验 Livius / NatGeo 专题来源。"""
import json, os, re, html, subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=os.path.join(ROOT,"data","sources.json")
NEW=[
 ("livius-egypt","Egypt - Livius","Livius.org",None,"学术百科","https://www.livius.org/category/egypt/"),
 ("livius-mesopotamia","Mesopotamia - Livius","Livius.org",None,"学术百科","https://www.livius.org/articles/place/mesopotamia/"),
 ("livius-polis","Polis - Livius","Livius.org",None,"学术百科","https://www.livius.org/articles/concept/polis/"),
 ("livius-athens","Athens - Livius","Livius.org",None,"学术百科","https://www.livius.org/articles/place/athens/"),
 ("livius-greece","Greece - Livius","Livius.org",None,"学术百科","https://www.livius.org/category/greece/"),
 ("natgeo-maya","New research challenges the idea that the Maya civilization collapsed","National Geographic",None,"权威媒体","https://www.nationalgeographic.com/history/article/maya"),
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
 d=json.load(open(P,encoding="utf-8"));have={s["url"] for s in d["sources"]}
 for sid,title,author,year,typ,url in NEW:
  code,pt=fetch(url)
  verified=bool(code and code<400 and pt)
  d["sources"].append({"id":sid,"title":title,"author":author,"year":year,"type":typ,
   "url":url,"url2":None,"link_ok":True if verified else False,"verified":verified,"page_title":pt,
   "note":f"curl 实测 HTTP {code}；页面标题：{pt or '未取得'}；年份未标注。"})
  print(sid,code,pt,verified)
 json.dump(d,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 print("已核验总数",sum(1 for s in d["sources"] if s["verified"]))
if __name__=="__main__": main()
