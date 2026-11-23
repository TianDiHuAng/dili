# -*- coding: utf-8 -*-
"""第44轮 B1：52 条 0 源条目重试检索（放宽标题要求，以摘要对象词命中≥3次为准）。"""
import subprocess,json,os,urllib.parse,time,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
STUB={"livius-polis","livius-athens"}
EXTRA=("nasa-ice-cores","usgs-glaciers-pdf","noaa-global-temp","nasa-pine-island",
       "s042-earthobservatory-nasa-gov","nasa-ice-sheets","noaa-sustainable-fisheries","s051-fisheries-noaa-gov")
docs={u:json.load(open(os.path.join(ROOT,"data",u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(ROOT,"data","sources.json"),encoding="utf-8"))["sources"]}
def ac(e):
    n=0
    for sid in e["sources"]:
        if sid in STUB: continue
        if sid.startswith(("openalex-","livius-")) or sid in EXTRA:
            note=(S.get(sid) or {}).get("note") or ""
            m=re.search(r"(\d{3,6})\s*字节", note)
            if sid.startswith("livius-") and m and int(m.group(1))<1000: continue
            n+=1
    return n
ZERO=[t for t,e in T.items() if ac(e)==0]
print("0 源条目:",len(ZERO),flush=True)

Q={
"刚果盆地":("Congo basin peat swamp forest","congo"),
"日本列岛":("Japanese archipelago tectonics subduction","japan"),
"罗马共和国":("Roman Republic constitutional","roman republic"),
"不列颠群岛":("British Isles stratigraphy palaeogeography","british"),
"南极冰盖":("Antarctic ice sheet dynamics","antarctic ice"),
"格陵兰岛":("Greenland ice sheet mass","greenland"),
"十三殖民地":("British North American colonies settlement","thirteen colonies"),
"冰芯气候记录":("ice core climate record","ice core"),
"北极火情变化":("Arctic tundra fire","tundra fire"),
"地理信息系统":("geographic information system spatial analysis","geographic information"),
"人口地理":("population distribution geography spatial","population"),
"城市地理":("urban geography morphology","urban structure"),
"罗马帝国":("Roman Empire provincial","roman empire"),
"日本列岛古":("Japanese Islands geology","japanese islands"),
"大平原农业":("Great Plains agriculture land use","great plains"),
"意大利半岛":("Italian peninsula geology","italian peninsula"),
}
def cj(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",url],capture_output=True,timeout=35)
            s=p.stdout.decode("utf-8","ignore")
            if s.strip().startswith("{"): return json.loads(s)
            time.sleep(3)
        except Exception: time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,q in Q.items():
    if t not in T or t not in ZERO: continue
    best=None;seen=set()
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q[0])+"&rows=20&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<400: continue
        al=a.lower()
        if al.count(q[1].lower())<3: continue     # 摘要对象词 ≥3 次
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,"hits":al.count(q[1].lower()),
             "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=10: break
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<14} {(best['title'][:50] if best else '-')} ({best.get('year') if best else ''}) hits={best['hits'] if best else 0}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round44_zerosrc.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有候选:",sum(1 for v in res.values() if v),"/",len([t for t in Q if t in ZERO]),flush=True)