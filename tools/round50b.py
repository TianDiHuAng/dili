# -*- coding: utf-8 -*-
"""第50轮B：为核心 7 条侧面条目检索主来源（对象词+主题槽+时期槽）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"印加帝国":dict(claim="印加帝国的疆域、道路与行政",q="Inca empire roads administration territory",
  obj="inca",slots=["empire","road","administrat"],period=["15th","sixteenth","1438","1533"]),
"南极大陆":dict(claim="南极大陆的地貌与冰盖总体",q="Antarctica continent ice sheet geomorphology",
  obj="antarctic",slots=["ice sheet","continent"],period=["cenozoic","million","quaternary"]),
"密西西比河":dict(claim="密西西比河的水系与流域特征",q="Mississippi River basin hydrology geomorphology",
  obj="mississippi",slots=["river","basin","hydrolog"],period=["holocene","pleistocene","20th"]),
"亚马逊盆地":dict(claim="亚马逊盆地的地貌与水文",q="Amazon basin geomorphology hydrology landscape",
  obj="amazon",slots=["basin","geomorph","hydrolog"],period=["holocene","pleistocene","neogene"]),
"季风系统":dict(claim="季风系统的驱动与季节进退",q="monsoon system mechanism seasonal reversal circulation",
  obj="monsoon",slots=["circulation","seasonal","precipitation"],period=["holocene","modern","last"]),
"河流三角洲":dict(claim="三角洲的形成与沉积过程",q="river delta formation sediment progradation",
  obj="delta",slots=["sediment","prograd","formation"],period=["holocene","quaternary","modern"]),
"文艺复兴意大利":dict(claim="城邦竞争、商业财富与艺术赞助的整体格局",q="Italian Renaissance city-state economy patronage",
  obj="renaissance",slots=["city","econom","patron"],period=["14th","15th","16th","1300","1400","1500"]),
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
            rej.append({"t":(oa.get("title") or "")[:44],"w":"缺主题槽","miss":sorted(set(spec["slots"])-set(hit))});continue
        per=[p for p in spec["period"] if p in al or p in ti]
        if not per:
            rej.append({"t":(oa.get("title") or "")[:44],"w":"缺时期槽(降为可选)"});
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,"claim":spec["claim"],
             "slots":hit,"period":per,
             "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=18: break
    res[t]={"cand":best,"rejected":rej[:5]}
    print(f"{'OK' if best else '--'} {t:<12} {(best['title'][:44] if best else '-')} ({best.get('year') if best else ''}) cite={best.get('cited') if best else ''}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round50_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["cand"]),"/",len(Q),flush=True)