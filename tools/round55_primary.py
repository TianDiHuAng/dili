# -*- coding: utf-8 -*-
"""第55轮 B1：剩余缺主来源条目的精确检索（对象词用完整短语，D112 两库+变音归一）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))
Q={
"印加帝国":dict(claim="印加国家的疆域、道路与行政",objs=["inca","tawantinsuyu"],
  qs=["Inca state administration roads","Tawantinsuyu empire organization"],slots=["state","administrat","road","empire","organiz"]),
"亚马逊盆地":dict(claim="亚马逊盆地的地貌、水文与生态总体",objs=["amazonia","amazon basin"],
  qs=["Amazonia landscape ecology overview","Amazon basin geology hydrology"],slots=["landscape","ecolog","geolog","hydrolog"]),
"新法兰西":dict(claim="新法兰西殖民地的地理与经济",objs=["new france"],
  qs=["New France colony economy","French colonial empire North America trade"],slots=["colony","trade","econom","settlement"]),
"古埃及中王国":dict(claim="中王国的行政与灌溉开发",objs=["middle kingdom"],
  qs=["Middle Kingdom Egypt state","Middle Kingdom Egypt administration economy"],slots=["middle kingdom","state","administrat","econom"]),
"澳大利亚内陆干旱气候":dict(claim="澳大利亚内陆干旱的成因与变率",objs=["australia","australian"],
  qs=["Australian arid interior climate variability","Australia desert climate causes"],slots=["arid","desert","climate","variab"]),
"复活节岛":dict(claim="复活节岛的环境与孤立性",objs=["easter island","rapa nui"],
  qs=["Rapa Nui island environment","Easter Island landscape prehistory"],slots=["island","landscape","environment","prehistor"]),
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
def collect(spec,q,engine):
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
              "type":w.get("type"),"abs_len":len(a),"slots":hit,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    else:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=15&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        items=d.get("results") or []
        n=len(items)
        for w in items:
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in spec["objs"]): continue
            hit=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(hit)<2: continue
            out.append({"doi":w.get("doi",""),"title":w.get("title"),"year":w.get("publication_year"),
              "oa_id":(w.get("id") or "").rsplit("/",1)[-1],"cited":w.get("cited_by_count"),
              "type":w.get("type"),"abs_len":len(a),"slots":hit,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    return {"engine":engine,"query":q,"results":n,"passed":out}
res={}
for t,spec in Q.items():
    recs=[collect(spec,spec["qs"][0],"Crossref"),collect(spec,spec["qs"][0],"OpenAlex")]
    allp=[c for r in recs for c in r["passed"]]
    # 去重
    seen=set();uniq=[]
    for c in allp:
        if c["oa_id"] in seen: continue
        seen.add(c["oa_id"]);uniq.append(c)
    uniq.sort(key=lambda x:-(x.get("cited") or 0))
    res[t]={"claim":spec["claim"],"records":recs,"best":uniq[0] if uniq else None}
    b=uniq[0] if uniq else None
    print(f"{'OK' if b else '--'} {t:<14} {(b['title'][:44] if b else '-')} ({b.get('year') if b else ''}) cite={b.get('cited') if b else ''}",flush=True)
    time.sleep(1)
json.dump(res,open(os.path.join(ROOT,"reports","round55_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["best"]),"/",len(Q),flush=True)