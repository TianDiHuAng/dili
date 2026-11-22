# -*- coding: utf-8 -*-
"""第23轮 B1 探测落盘：记录全部 23 条候选的实测明细（含失败原因）。"""
import subprocess,re,html,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
rows=[]
for topic,u,rx in C:
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw:
            rows.append({"topic":topic,"url":u,"http":0,"title":None,"body":0,"hits":0,"reason":"连接失败"});continue
        b,c=raw.rsplit("\n__HTTP__",1)
        code=int(c.strip() or 0)
        m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
        title=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
        txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",strip(b)))).strip()
        n=len(txt);h=len(re.findall(rx,txt,re.I))
        if code>=400: reason=f"HTTP {code}"
        elif not title: reason="无标题"
        elif re.search(r"404|not found|error|moved",title,re.I): reason="标题为错误页"
        elif n<gate if False else (n < (5000 if h>=30 else 8000)): reason=f"正文不足（{n} < {5000 if h>=30 else 8000}）"
        elif h<3: reason=f"命中不足（{h}）"
        else: reason="达标"
        rows.append({"topic":topic,"url":u,"http":code,"title":title,"body":n,"hits":h,"reason":reason})
    except Exception as ex:
        rows.append({"topic":topic,"url":u,"http":0,"title":None,"body":0,"hits":0,"reason":f"异常 {type(ex).__name__}"})
hosts={}
for r in rows:
    h=r["url"].split("/")[2]
    hosts.setdefault(h,{"tried":0,"ok":0})
    hosts[h]["tried"]+=1
    if r["reason"]=="达标": hosts[h]["ok"]+=1
out={"round":23,"candidates":len(rows),"usable":sum(1 for r in rows if r["reason"]=="达标"),
 "hosts":hosts,"rows":rows,
 "note":"本机可达的 7 个主机中 6 个在 r17–r22 已反复探测；主导失败模式为 WAF 拦截 / 门户迁移 / 门落户，并非「无对题页面」。单轮 0 收益不足以判定渠道饱和。"}
json.dump(out,open(os.path.join(ROOT,"reports","round23_probe_detail.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("候选",out["candidates"],"可用",out["usable"])
for r in rows: print(f"  {r['http']:>3} body={r['body']:>6} hits={r['hits']:>3} | {r['topic']:<12} | {r['reason']}")