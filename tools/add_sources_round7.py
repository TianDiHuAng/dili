# -*- coding: utf-8 -*-
"""第7轮新增并核验 Livius 专题来源。"""
import json,os,re,html,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=os.path.join(ROOT,"data","sources.json")
NEW=[
 ("livius-carthage","Punic Carthage - Livius","Livius.org",None,"学术百科","https://www.livius.org/articles/place/carthage/"),
 ("livius-roman-republic","Roman Republic - Livius","Livius.org",None,"学术百科","https://www.livius.org/category/roman-republic/"),
 ("livius-italy","Italy - Livius","Livius.org",None,"学术百科","https://www.livius.org/category/italy/"),
]
def fetch(u):
 p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","18","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=28)
 raw=p.stdout.decode("utf-8","ignore")
 if "__HTTP__" not in raw: return 0,None
 b,c=raw.rsplit("\n__HTTP__",1)
 m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
 t=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
 return int(c.strip()),t
def main():
 d=json.load(open(P,encoding="utf-8"));have={s["url"] for s in d["sources"]}
 for sid,title,author,year,typ,url in NEW:
  code,pt=fetch(url);verified=bool(code and code<400 and pt)
  if url in have: continue
  d["sources"].append({"id":sid,"title":title,"author":author,"year":year,"type":typ,"url":url,
   "url2":None,"link_ok":True if verified else False,"verified":verified,"page_title":pt,
   "note":f"curl 实测 HTTP {code}；页面标题：{pt or '未取得'}；年份未标注。"})
  print(sid,code,pt,verified)
 json.dump(d,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 print("已核验总数",sum(1 for s in d["sources"] if s["verified"]))
if __name__=="__main__": main()
