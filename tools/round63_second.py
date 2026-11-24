# -*- coding: utf-8 -*-
"""第63轮 B1：为 G3 中的政权类 9 条找第二学术来源（两库+变音归一+对象词）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))
Q={
"汉代":dict(objs=["han"],qs=["Han dynasty state economy society","Han empire administration"],
  slots=["han","dynasty","state","econom","administrat","society","empire"]),
"阿兹特克":dict(objs=["aztec","mexica"],qs=["Aztec state society tribute","Aztec empire Tenochtitlan"],
  slots=["aztec","state","tribute","society","empire","tenochtitlan"]),
"加纳帝国":dict(objs=["ghana","wagadu"],qs=["Ghana empire Wagadu state trade","Wagadu Ghana empire"],
  slots=["ghana","wagadu","state","trade","empire"]),
"古埃及新王国":dict(objs=["egypt"],qs=["New Kingdom Egypt empire administration","New Kingdom Egypt state society"],
  slots=["new kingdom","egypt","empire","administrat","state"]),
"周代":dict(objs=["zhou"],qs=["Zhou dynasty state enfeoffment","Zhou China feudal society"],
  slots=["zhou","dynasty","state","feudal","enfeoff"]),
"桑海帝国":dict(objs=["songhai"],qs=["Songhai empire state trade","Songhai Niger bend polity"],
  slots=["songhai","state","trade","empire","niger"]),
"笈多王朝":dict(objs=["gupta"],qs=["Gupta empire polity economy","Gupta dynasty administration"],
  slots=["gupta","empire","polity","econom","administrat"]),
"阿拉伯半岛":dict(objs=["arabian","arabia"],qs=["Arabian Peninsula geography climate","Arabian Peninsula physical geography"],
  slots=["arabian","peninsula","geograph","climate"]),
"马格里布":dict(objs=["maghreb","maghrib"],qs=["Maghreb region geography","Maghrib physical geography climate"],
  slots=["maghreb","maghrib","geograph","climate","region"]),
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
def run(spec,q,engine):
    out=[];n=0
    if engine=="Crossref":
        items=(cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type").get("message") or {}).get("items") or []
        n=len(items)
        for it in items:
            doi=it.get("DOI")
            if not doi or it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            w=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
            a=ab(w) or ""
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in spec["objs"]): continue
            hit=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(hit)<2: continue
            out.append({"doi":doi,"title":w.get("title"),"year":w.get("publication_year"),
              "oa_id":(w.get("id") or "").rsplit("/",1)[-1],"cited":w.get("cited_by_count"),
              "type":w.get("type"),"abs_len":len(a),"slots":hit})
    else:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=15&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        items=d.get("results") or [];n=len(items)
        for w in items:
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in spec["objs"]): continue
            hit=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(hit)<2: continue
            out.append({"doi":w.get("doi",""),"title":w.get("title"),"year":w.get("publication_year"),
              "oa_id":(w.get("id") or "").rsplit("/",1)[-1],"cited":w.get("cited_by_count"),
              "type":w.get("type"),"abs_len":len(a),"slots":hit})
    return {"engine":engine,"query":q,"results":n,"passed":out}
res={}
for t,spec in Q.items():
    recs=[]
    for q in spec["qs"]:
        recs.append(run(spec,q,"Crossref"));time.sleep(0.8)
        recs.append(run(spec,q,"OpenAlex"));time.sleep(0.8)
    allp=[c for r in recs for c in r["passed"]]
    seen=set();uniq=[]
    for c in allp:
        if c["oa_id"] in seen: continue
        seen.add(c["oa_id"]);uniq.append(c)
    # 优先被引≥10 且摘要≥800（强来源）
    strong=[c for c in uniq if (c.get("cited") or 0)>=10 and c["abs_len"]>=800]
    strong.sort(key=lambda x:-(x.get("cited") or 0))
    pick=strong[0] if strong else None
    res[t]={"records":recs,"best":pick,"candidates":len(uniq)}
    print(f"{'OK' if pick else '--'} {t:<12} {(pick['title'][:44] if pick else '-')} ({pick.get('year') if pick else ''}) cite={pick.get('cited') if pick else ''} 候选={len(uniq)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round63_second.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n强来源命中:",sum(1 for v in res.values() if v["best"]),"/",len(Q),flush=True)