# -*- coding: utf-8 -*-
"""第108轮：G3b 三条找互补来源（D156 已查现有强源）。"""
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
USED={"非洲大湖地区":["W2967976954"],"西北海岸":["W2163451848"],"卫星遥感地表观测":[]}
SPEC={
"非洲大湖地区":(["african great lakes","great lakes of africa","east african lakes","african lakes","lake victoria","lake tanganyika","lake malawi","east african rift lakes"],["African Great Lakes","African Great Lakes fisheries","African Great Lakes region","East African Great Lakes","Lake Victoria Lake Tanganyika Lake Malawi","Great Lakes region Africa ecology","East African rift lakes","African Great Lakes climate"],["lake","africa","rift","fish","basin","tanganyika","victoria","malawi"]),
"西北海岸":(["northwest coast","north-west coast","pacific northwest","northwest pacific coast","northwest coast indians"],["Northwest Coast","Northwest Coast peoples","Northwest Coast archaeology","Pacific Northwest Coast indigenous","Northwest Coast potlatch","Northwest Coast salmon fishing","Pacific Northwest coast Indigenous peoples","Northwest Coast economy trade"],["coast","indigenous","salmon","archaeolog","northwest","pacific","trade","potlatch"]),
"卫星遥感地表观测":(["remote sensing","satellite remote sensing","earth observation","land cover","landsat"],["satellite remote sensing land surface","satellite remote sensing land cover","satellite remote sensing vegetation monitoring","satellite remote sensing urban expansion","remote sensing of land surface","Landsat land cover change","earth observation land surface monitoring","satellite remote sensing water bodies"],["satellite","land","vegetation","urban","water","cover","monitor","sensor"]),
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
            oid=(w.get("id") or "").rsplit("/",1)[-1]
            if oid in USED.get(t,[]): continue
            cands.append({"oid":oid,"title":w.get("title"),"year":w.get("publication_year"),
              "cited":cited,"abs_len":len(a),"slots":h,"doi":doi})
            time.sleep(0.3)
        time.sleep(0.6)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:5],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<13} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round108_g3.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)