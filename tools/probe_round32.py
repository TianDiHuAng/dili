# -*- coding: utf-8 -*-
"""第32轮 B1：Wikidata / 其他结构化渠道探测（用于古代政权条目）。"""
import subprocess,re,json,os,html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C=[
 ("汉代","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Han%20dynasty&language=en&format=json",r"Han"),
 ("宋代","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Song%20dynasty&language=en&format=json",r"Song"),
 ("蒙古帝国","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Mongol%20Empire&language=en&format=json",r"Mongol"),
 ("阿兹特克","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Aztec&language=en&format=json",r"Aztec"),
 ("城市起源","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=city&language=en&format=json",r"city"),
 ("汉代","https://dbpedia.org/data/Han_dynasty.json",r"Han"),
 ("宋代","https://dbpedia.org/data/Song_dynasty.json",r"Song"),
 ("丝绸之路","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Silk%20Road&language=en&format=json",r"Silk"),
 ("长江流域","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Yangtze&language=en&format=json",r"Yangtze"),
 ("印度河文明","https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Indus%20Valley%20Civilisation&language=en&format=json",r"Indus"),
]
def probe(topic,u,rx):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return topic,u,0,0,0,"连接失败"
        b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
        n=len(b); h=len(re.findall(rx,b,re.I))
        reason=("HTTP %d"%code if code>=400 else ("内容过短 %d"%n if n<300 else ("命中 0" if h<1 else "达标")))
        return topic,u,code,n,h,reason
    except Exception as ex:
        return topic,u,0,0,0,f"异常 {type(ex).__name__}"
rows=[]
for topic,u,rx in C:
    t,uu,code,n,h,reason=probe(topic,u,rx)
    rows.append({"topic":t,"url":uu,"http":code,"len":n,"hits":h,"reason":reason})
    print(f"{'OK' if reason=='达标' else '--'} {code:>3} len={n:>7} hits={h:>3} | {topic:<10} | {reason}")
json.dump({"round":32,"rows":rows,"usable":sum(1 for x in rows if x["reason"]=="达标")},
  open(os.path.join(ROOT,"reports","round32_probe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("可用",sum(1 for x in rows if x["reason"]=="达标"),"/",len(rows))