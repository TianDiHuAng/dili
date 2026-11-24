# -*- coding: utf-8 -*-
"""第87轮：重要 G3b 剩余条目检索（综述性检索词，D144 合规）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
STAT={"ok":0,"fail":0}
def get(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",
                              "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: STAT["fail"]+=1; time.sleep(4); continue
            b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
            if code!=200: STAT["fail"]+=1; time.sleep(4 if code in (429,503) else 2); continue
            STAT["ok"]+=1
            return json.loads(b) if b.strip().startswith("{") else {}
        except Exception: STAT["fail"]+=1; time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
SPEC={
"威尼斯":(["venice","venetian"],["Venice history republic","Venetian economy society"],["venice","venetian","history","republic","econom","society"]),
"毛利人":(["maori"],["Maori society history","Maori New Zealand culture"],["maori","societ","history","culture","new zealand"]),
"南极条约体系":(["antarctic treaty"],["Antarctic Treaty System governance","Antarctic treaty regime history"],["antarctic treaty","system","governance","regime","history"]),
"洋流":(["ocean circulation","thermohaline"],["ocean circulation review","global ocean overturning"],["circulation","ocean","overturning","global","review"]),
"气候带":(["climate zone","koppen"],["Koppen climate classification review","global climate classification"],["climate","classification","koppen","global","zone"]),
"大分水岭":(["great dividing range","dividing range"],["Great Dividing Range geology","eastern Australia highlands uplift"],["dividing","range","geolog","highland","uplift","australia"]),
"巴西高原":(["brazil","brazilian"],["Brazilian highlands geology","Brazil plateau geomorphology"],["brazil","highland","geolog","geomorph","plateau"]),
"拉普拉塔平原":(["pampa","plata"],["Pampas grasslands history","La Plata basin environment"],["pampa","plata","grassland","environment","basin"]),
"巴西殖民经济":(["brazil","colonial"],["colonial Brazil economy","Brazil sugar plantation colonial"],["brazil","colonial","econom","sugar","plantation"]),
"马来群岛":(["malay","archipelago","southeast asia"],["Malay archipelago history","island Southeast Asia states"],["malay","archipelago","island","history","state"]),
}
res={}
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        cr=get("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
        for it in ((cr.get("message") or {}).get("items") or []):
            doi=it.get("DOI")
            if not doi or it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            w=get(f"https://api.openalex.org/works/https://doi.org/{doi}")
            a=ab(w) or ""
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in objs): continue
            h=[s for s in slots if norm(s) in al or norm(s) in ti]
            if len(h)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10 and len(a)<800: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":cited,"abs_len":len(a),"slots":h,"doi":doi})
            time.sleep(0.3)
        time.sleep(0.6)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:42] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round87_imp5.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)
print("命中:",sum(1 for v in res.values() if v["cand"]),"/",len(res),flush=True)