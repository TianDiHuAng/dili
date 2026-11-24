# -*- coding: utf-8 -*-
"""第52轮B：为 8 条侧面条目检索主来源（D110 两检索式）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"拜占庭帝国":dict(claim="拜占庭帝国的行政、经济与长期延续",obj="byzantine",
  qs=["Byzantine Empire administration economy state","Byzantine state institutions fiscal"],
  slots=["administration","econom","state","fiscal","institution"]),
"元代":dict(claim="元代的行政、驿站与海运",obj="yuan",
  qs=["Yuan dynasty administration postal relay","Yuan China transport sea grain"],
  slots=["administrat","relay","transport","grain","postal"]),
"维京时代":dict(claim="维京时代的扩张与贸易",obj="viking",
  qs=["Viking Age expansion trade network","Viking maritime trade routes"],
  slots=["expansion","trade","route","maritime","network"]),
"美国西进":dict(claim="美国向西部扩张的定居与边疆过程",obj="west",
  qs=["American westward expansion settlement frontier","United States westward migration land"],
  slots=["westward","settle","frontier","expansion","migration"]),
"大自流盆地":dict(claim="大自流盆地的地下水与自流机制",obj="artesian",
  qs=["Great Artesian Basin groundwater hydrogeology","Great Artesian Basin recharge discharge"],
  slots=["groundwater","recharge","aquifer","hydrogeolog","discharge"]),
"古埃及新王国":dict(claim="新王国的帝国扩张与行政",obj="egypt",
  qs=["New Kingdom Egypt empire administration","New Kingdom Egypt state expansion"],
  slots=["new kingdom","empire","administrat","state","expansion"]),
"意大利半岛":dict(claim="意大利半岛的地质与地形",obj="italian peninsula",
  qs=["Italian peninsula geology tectonics","geology of Italy Apennines"],
  slots=["geolog","tecton","apenning","structur"]),
"落基山脉":dict(claim="落基山脉的地质与隆升",obj="rocky mountain",
  qs=["Rocky Mountains geology orogeny uplift","Rocky Mountain orogenic belt"],
  slots=["geolog","orogen","uplift","tecton"]),
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
def try_one(spec,q):
    ok=[];n=0
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=18&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        n+=1
        doi=it.get("DOI")
        if not doi or it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<400: continue
        ti=(oa.get("title") or "").lower(); al=a.lower()
        if spec["obj"] not in ti: continue
        hit=[s for s in spec["slots"] if s in al or s in ti]
        if len(hit)<2: continue
        ok.append({"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
          "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
          "type":oa.get("type"),"abs_len":len(a),"abstract":a,"slots":hit,
          "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    ok.sort(key=lambda x:-(x.get("cited") or 0))
    return {"query":q,"results":n,"passed":ok}
res={}
for t,spec in Q.items():
    recs=[try_one(spec,q) for q in spec["qs"]]
    allp=[c for r in recs for c in r["passed"]];allp.sort(key=lambda x:-(x.get("cited") or 0))
    res[t]={"claim":spec["claim"],"records":recs,"best":allp[0] if allp else None}
    b=allp[0] if allp else None
    print(f"{'OK' if b else '--'} {t:<12} {(b['title'][:44] if b else '-')} ({b.get('year') if b else ''}) cite={b.get('cited') if b else ''}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round52b_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["best"]),"/",len(Q),flush=True)