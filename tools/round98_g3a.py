# -*- coding: utf-8 -*-
"""第98轮：G3a 重要剩余条目找第二对位来源（Crossref，D144 合规）。"""
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
"多瑙河":(["danube"],["Danube river hydrology","Danube basin environment history"],["danube","river","hydrolog","basin","environment"]),
"莱茵河":(["rhine"],["Rhine river history navigation","Rhine basin hydrology"],["rhine","river","history","navigat","hydrolog"]),
"维京时代":(["viking","norse"],["Viking Age Scandinavia society","Viking expansion trade"],["viking","norse","scandinavia","society","expansion","trade"]),
"巴尔干半岛":(["balkan"],["Balkan peninsula geography history","Balkans environment society"],["balkan","geograph","history","environment","society"]),
"落基山脉":(["rocky mountain"],["Rocky Mountains geology","Rocky Mountain orogeny evolution"],["rocky","mountain","geolog","orogen","evolution"]),
"格陵兰岛":(["greenland"],["Greenland ice sheet climate","Greenland geography environment"],["greenland","ice sheet","climate","geograph","environment"]),
"阿塔卡马沙漠":(["atacama"],["Atacama Desert aridity","Atacama hyperarid climate"],["atacama","desert","aridity","hyperarid","climate"]),
"马丘比丘":(["machu picchu"],["Machu Picchu archaeology construction","Machu Picchu Inca site"],["machu picchu","archaeolog","construction","inca","site"]),
"大自流盆地":(["great artesian basin","artesian"],["Great Artesian Basin hydrogeology","artesian basin groundwater"],["artesian","basin","hydrogeolog","groundwater"]),
"新西兰南岛":(["south island","new zealand"],["South Island New Zealand geology","New Zealand South Island environment"],["south island","new zealand","geolog","environment"]),
"大堡礁":(["great barrier reef"],["Great Barrier Reef ecology","Great Barrier Reef coral reef"],["great barrier","reef","ecolog","coral"]),
"元代":(["yuan dynasty","mongol yuan","karakorum"],["Yuan dynasty administration","Mongol Yuan China state"],["yuan dynasty","mongol","administrat","state","china"]),
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
    print(f"{'OK' if u else '--'} {t:<11} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round98_g3a2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)