# -*- coding: utf-8 -*-
"""第69轮：为 G1 十条检索强来源（被引≥10 或摘要≥800，两库+对象词+主题槽）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
Q={
"玛雅文明":dict(objs=["maya"],qs=["Maya civilization state society","Classic Maya collapse drought"],
  slots=["maya","state","society","collapse","classic","polit"]),
"印加帝国":dict(objs=["inca","tawantinsuyu"],qs=["Inca empire roads administration","Inca state organization"],
  slots=["inca","empire","road","administrat","state","organiz"]),
"澳大利亚大陆":dict(objs=["australia"],qs=["Australia continent geology geography","Australia physical geography climate"],
  slots=["australia","geolog","geograph","climate","continent"]),
"澳大利亚原住民":dict(objs=["aboriginal","indigenous australian"],qs=["Aboriginal Australia archaeology","Australian indigenous society land"],
  slots=["aboriginal","indigenous","archaeolog","society","land"]),
"孔雀王朝":dict(objs=["maurya","mauryan","asoka","ashoka"],qs=["Mauryan empire administration","Ashoka Maurya state"],
  slots=["maurya","empire","administrat","state","asoka"]),
"隋唐":dict(objs=["sui","tang"],qs=["Tang dynasty state administration","Sui Tang China empire"],
  slots=["tang","sui","state","administrat","empire"]),
"克里特文明":dict(objs=["minoan","crete"],qs=["Minoan palace economy","Minoan civilization Crete"],
  slots=["minoan","crete","palace","econom","civiliz"]),
"维京时代":dict(objs=["viking"],qs=["Viking Age expansion society","Viking Scandinavia state"],
  slots=["viking","expansion","society","state","scandinav"]),
"十字军东征":dict(objs=["crusade"],qs=["Crusades Mediterranean trade","Crusade state institutions"],
  slots=["crusade","trade","state","institution","mediterran"]),
"大平原":dict(objs=["great plains"],qs=["Great Plains agriculture settlement","North American Great Plains environment"],
  slots=["great plains","agricultur","settle","environment","grassland"]),
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
def hit(spec,w):
    a=ab(w)
    if len(a)<400: return None
    ti=norm(w.get("title")); al=norm(a)
    if not any(norm(o) in ti for o in spec["objs"]): return None
    h=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
    if len(h)<2: return None
    return {"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
            "year":w.get("publication_year"),"cited":w.get("cited_by_count") or 0,
            "abs_len":len(a),"slots":h,"doi":w.get("doi",""),"type":w.get("type")}
res={}
for t,spec in Q.items():
    cands=[]
    for q in spec["qs"]:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=15&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            r=hit(spec,w)
            if r: cands.append(r)
        time.sleep(0.8)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    strong=[c for c in u if c["cited"]>=10 or c["abs_len"]>=800]
    strong.sort(key=lambda x:-(x["cited"]*1000+x["abs_len"]))
    res[t]={"cand":strong[0] if strong else None,"n":len(u),"nstrong":len(strong)}
    b=res[t]["cand"]
    print(f"{'OK' if b else '--'} {t:<12} {(b['title'][:42] if b else '-')} ({b.get('year') if b else ''}) cite={b.get('cited') if b else ''} abs={b.get('abs_len') if b else ''} [候选{len(u)}/强{len(strong)}]",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round69_g1.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v["cand"]),"/",len(Q),flush=True)