# -*- coding: utf-8 -*-
"""第80轮：重要条目第三批 12 条检索。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
SPEC={
"马其顿与亚历山大":(["macedon","alexander"],["Macedonian empire Alexander","Alexander conquest administration"],["macedon","alexander","empire","conquest","administrat"]),
"莱茵河":(["rhine"],["Rhine river hydrology","Rhine navigation history"],["rhine","river","hydrolog","navigat","history"]),
"法兰克王国":(["frankish","francia","merovingian","carolingian"],["Frankish kingdom state","Carolingian empire administration"],["frankish","carolingian","kingdom","state","administrat"]),
"十字军东征":(["crusade","crusader"],["Crusades military orders","Crusader states administration"],["crusad","military order","state","administrat","levant"]),
"威尼斯":(["venice","venetian"],["Venice maritime empire trade","Venetian republic institutions"],["venice","venetian","maritime","trade","institution","republic"]),
"奥尔梅克":(["olmec"],["Olmec civilization society","Olmec Mesoamerica state"],["olmec","civiliz","society","state","mesoamerica"]),
"特奥蒂瓦坎":(["teotihuacan"],["Teotihuacan state society","Teotihuacan urbanism"],["teotihuacan","state","society","urban"]),
"十三殖民地":(["thirteen colonies","colonial america"],["Thirteen Colonies economy","British North America colonial society"],["colonies","colonial","econom","society","british"]),
"加勒比海群岛":(["caribbean"],["Caribbean islands history","Caribbean plantation society"],["caribbean","island","history","plantation","society"]),
"巴西高原":(["brazil","brazilian"],["Brazil highlands geology","Brazilian plateau geomorphology"],["brazil","highland","geolog","geomorph","plateau"]),
"拉普拉塔平原":(["plata","pampa"],["Pampas grassland agriculture","La Plata basin environment"],["pampa","plata","grassland","agricultur","environment"]),
"大分水岭":(["great dividing","dividing range"],["Great Dividing Range geology","eastern Australia highlands"],["dividing range","geolog","highland","australia"]),
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
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=20&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            if (w.get("type") or "")=="book-review": continue
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in objs): continue
            h=[s for s in slots if norm(s) in al or norm(s) in ti]
            if len(h)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10 and len(a)<800: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":cited,"abs_len":len(a),"slots":h,"doi":w.get("doi","")})
        time.sleep(0.7)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:42] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round80_imp3.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v["cand"]),"/",len(SPEC),flush=True)