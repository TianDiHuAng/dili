# -*- coding: utf-8 -*-
"""第82轮B：OpenAlex search 配额耗尽后的替代检索路线（Crossref bibliographic → DOI → OpenAlex by-ID）。"""
import subprocess,json,os,urllib.parse,time,unicodedata,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
def cj(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: time.sleep(4); continue
            b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
            if code==200 and b.strip().startswith("{"): return json.loads(b)
            time.sleep(4)
        except Exception: time.sleep(4)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))

SPEC={
"赫梯王国":(["hittite"],["Hittite empire administration"],["hittite","empire","administrat","state"]),
"神圣罗马帝国":(["holy roman"],["Holy Roman Empire institutions"],["holy roman","empire","institution","constitution"]),
"汉萨同盟":(["hanseatic","hansa"],["Hanseatic League trade"],["hanseatic","hansa","trade","city"]),
}
res={}
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
        items=(cr.get("message") or {}).get("items") or []
        print(f"  {t}: Crossref「{q}」返回 {len(items)} 条")
        for it in items:
            doi=it.get("DOI")
            if not doi or it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            w=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
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
            time.sleep(0.4)
        time.sleep(0.8)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} 候选{len(u)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round82_crossref.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\nCrossref 路线命中:",sum(1 for v in res.values() if v["cand"]),"/",len(SPEC),flush=True)