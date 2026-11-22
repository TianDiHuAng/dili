# -*- coding: utf-8 -*-
"""第19轮 B1 复核：对已有来源做「标题即主题 + 正文长度 + 命中」三项验证，
找出可直接升级 L2 的条目（主题匹配型专题页）。"""
import json,os,re,html,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
src={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

# 候选：条目 → (专题来源, 关键词正则)
CAND={
 "人口地理":("s023-ourworldindata-org",r"population"),
 "城市地理":("s025-ourworldindata-org",r"urban"),
 "地理信息系统":("esri-gis",r"gis|geographic information"),
 "荒漠化":("s045-earthobservatory-nasa-gov",r"desertif"),
 "沙尘暴":("s046-earthobservatory-nasa-gov",r"dust|sahel"),
 "陆地保护区":("s091-iucn-org",r"protected area"),
 "农业企业与价值链":("s059-worldbank-org",r"agribusiness|farm"),
 "全球气温距平":("s053-climate-gov",r"temperature"),
 "二氧化碳排放清单":("s027-ourworldindata-org",r"co2|emission"),
 "植物物候变化":("noaa-phenology",r"spring|plant|phenolog"),
 "北极火情变化":("nasa-arctic-fire",r"fire|arctic"),
 "松岛冰川退缩":("nasa-pine-island",r"glacier|pine island"),
 "土壤资源":("s083-fao-org",r"soil"),
 "渔业资源":("s051-fisheries-noaa-gov",r"fish"),
 "海洋生态系统":("s085-unesco-org",r"ocean"),
 "卫星遥感地表观测":("s041-science-nasa-gov",r"landsat|satellite"),
 "水资源管理":("s061-worldbank-org",r"water"),
 "湿地与水资源":("fao-aquastat-basins",r"water|basin"),
}
def strip(h):
    for t in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{t}\b.*?</{t}>"," ",h,flags=re.I|re.S)
    return h
def measure(url,rx):
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
    raw=p.stdout.decode("utf-8","ignore")
    if "__HTTP__" not in raw: return 0,0,0
    b,c=raw.rsplit("\n__HTTP__",1)
    txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",strip(b))))
    return int(c.strip() or 0),len(txt),len(re.findall(rx,txt,re.I))

ok=[]
for title,(sid,rx) in CAND.items():
    e=next((x for x in (v for d in docs.values() for v in d["entries"]) if x["title"]==title),None)
    if not e: continue
    s=src.get(sid)
    if not s: continue
    code,n,h=measure(s["url"],rx)
    okflag = code and code<400 and s.get("verified") and h>=3 and n>=1500
    print(f"{'OK ' if okflag else '-- '} {title:<16} {e['tier']:<2} {e['level']} | {sid} | {code} body={n:>6} hits={h:>3}")
    if okflag: ok.append({"title":title,"sid":sid,"tier":e["tier"],"level":e["level"],"body":n,"hits":h,"rx":rx})
json.dump(ok,open(os.path.join(ROOT,"reports","round19_candidates.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可升级:",len(ok))
print("其中 重要:",[x["title"] for x in ok if x["tier"]=="重要"])
print("其中 核心:",[x["title"] for x in ok if x["tier"]=="核心"])