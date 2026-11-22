# -*- coding: utf-8 -*-
"""第17轮 B1 探测：针对降级条目与核心 L1 的专题页（D044 判据）。"""
import subprocess,re,html,json
C=[
 ("北美冰盖","https://earthobservatory.nasa.gov/features/Paleoclimatology_IceCores",r"ice"),
 ("北美冰盖","https://www.nps.gov/subjects/geology/glacial-landforms.htm",r"glacial"),
 ("山地农业","https://www.fao.org/3/y4252e/y4252e00.htm",r"mountain"),
 ("印度河文明","https://www.metmuseum.org/toah/hd/indu/hd_indu.htm",r"indus"),
 ("印度河文明","https://www.si.edu/spotlight/indus-valley",r"indus"),
 ("大堡礁","https://oceanservice.noaa.gov/facts/coral.html",r"coral"),
 ("大堡礁","https://oceanservice.noaa.gov/facts/coralreef-climate.html",r"coral"),
 ("墨西哥湾","https://oceanservice.noaa.gov/facts/hypoxia.html",r"hypox|gulf"),
 ("长江流域","https://earthobservatory.nasa.gov/features/ThreeGorges",r"yangtze|three gorges"),
 ("城市起源","https://www.loc.gov/collections/",r"city"),
 ("城市起源","https://www.si.edu/spotlight/cities",r"city"),
 ("汉代","https://www.metmuseum.org/toah/hd/hand/hd_hand.htm",r"han"),
 ("蒙古帝国","https://www.metmuseum.org/toah/hd/mong/hd_mong.htm",r"mongol"),
 ("阿兹特克","https://www.metmuseum.org/toah/hd/azte/hd_azte.htm",r"aztec"),
]
def strip(h):
 for t in ("nav","header","footer","aside","script","style","form"): h=re.sub(rf"<{t}\b.*?</{t}>"," ",h,flags=re.I|re.S)
 return h
def f(it):
 topic,u,rx=it
 try:
  p=subprocess.run(['curl','-L','-sS','--ssl-no-revoke','--compressed','-m','20','-A','Mozilla/5.0','-o','-','-w','\n__HTTP__%{http_code}',u],capture_output=True,timeout=30)
  raw=p.stdout.decode('utf-8','ignore')
  if '__HTTP__' not in raw: return topic,u,0,None,0,0
  b,c=raw.rsplit('\n__HTTP__',1)
  m=re.search(r'<title[^>]*>(.*?)</title>',b,re.I|re.S)
  t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',m.group(1)))).strip() if m else None
  txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',strip(b))))
  return topic,u,int(c.strip()),t,len(txt),len(re.findall(rx,txt,re.I))
 except Exception: return topic,u,0,None,0,0
ok=[]
for r in [f(x) for x in C]:
 topic,u,code,t,n,h=r
 good=code and code<400 and t and n>=8000 and h>=5 and not re.search(r"404|not found|error",(t or ""),re.I)
 print(f"{'OK' if good else 'no':>3} {code:>3} body={n:>7} hits={h:>4} | {topic} | {u}")
 if good: ok.append({"topic":topic,"url":u,"title":t,"body":n,"hits":h})
json.dump(ok,open("reports/round17_candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("USABLE",len(ok))