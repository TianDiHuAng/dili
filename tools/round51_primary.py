# -*- coding: utf-8 -*-
"""第51轮 B1：库什 + 5 条核心侧面条目补主来源（三端口径，含时期槽可选）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"库什与努比亚":dict(claim="库什王国的商路与纳帕塔/麦罗埃时期的政治经济",q="kingdom of Kush Napata Meroe trade",
  obj="kush",slots=["napata","meroe","trade","kingdom"],period=["bc","bce","first millennium"]),
"印加帝国":dict(claim="印加帝国的疆域、道路系统与行政",q="Inca empire road system administration territory",
  obj="inca",slots=["empire","road","administrat","territor"],period=["15th","sixteenth","1438","1533","century"]),
"文艺复兴意大利":dict(claim="城邦竞争、商业财富与艺术赞助的整体格局",q="Italian Renaissance city states economy art patronage",
  obj="renaissance",slots=["city","econom","patron","art"],period=["14th","15th","16th","century"]),
"亚马逊盆地":dict(claim="亚马逊盆地的地貌、水文与生态总体",q="Amazon basin landscape hydrology geomorphology overview",
  obj="amazon",slots=["basin","landscape","hydrolog","geomorph"],period=["holocene","pleistocene","neogene"]),
"季风系统":dict(claim="季风系统由海陆热力差异驱动、随季节进退",q="monsoon system land sea thermal contrast seasonal reversal",
  obj="monsoon",slots=["land","sea","seasonal","circulation","precipitation"],period=["holocene","modern","last"]),
"南极大陆":dict(claim="南极大陆的地貌与冰盖总体",q="Antarctica continent ice sheet topography overview",
  obj="antarctic",slots=["continent","ice sheet","topograph","geolog"],period=["cenozoic","million","quaternary"]),
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
for t,spec in Q.items():
    best=None;seen=set();rej=[]
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(spec["q"])+"&rows=20&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<400: continue
        ti=(oa.get("title") or "").lower(); al=a.lower()
        if spec["obj"] not in ti:
            rej.append({"t":(oa.get("title") or "")[:44],"w":"标题无对象词"});continue
        hit=[s for s in spec["slots"] if s in al or s in ti]
        if len(hit)<max(2,len(spec["slots"])-1):
            rej.append({"t":(oa.get("title") or "")[:44],"w":"主题槽不足","hit":hit});continue
        per=[p for p in spec["period"] if p in al or p in ti]
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,"claim":spec["claim"],
             "slots":hit,"period":per,
             "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=18: break
    res[t]={"cand":best,"rejected":rej[:4]}
    print(f"{'OK' if best else '--'} {t:<12} {(best['title'][:46] if best else '-')} ({best.get('year') if best else ''}) cite={best.get('cited') if best else ''}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round51_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["cand"]),"/",len(Q),flush=True)