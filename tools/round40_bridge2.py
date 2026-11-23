# -*- coding: utf-8 -*-
"""第40轮续：剩余 7 条用 DOI 桥精确检索。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"阿巴拉契亚山脉":["Appalachian Mountains geology tectonic","Appalachian orogen geology"],
"古巴岛":["Cuba geology island arc","Cuban geology stratigraphy"],
"南美贸易网络":["prehispanic trade networks Andes","Andean exchange networks prehispanic"],
"南极特别保护区":["Antarctic protected area management","Antarctic conservation area designation"],
"争议边界处理原则":["cartographic representation disputed boundaries","map boundary ambiguity cartography"],
"环境治理":["environmental governance review","environmental governance institutions effectiveness"],
"农业气候风险":["agricultural climate risk vulnerability","climate risk agriculture adaptation"],
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
    if not inv: return None
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for topic,qs in Q.items():
    seen=set();best=None
    for q in qs:
        cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=15&select=title,DOI,type")
        for it in (cr.get("message") or {}).get("items") or []:
            doi=it.get("DOI")
            if not doi or doi in seen: continue
            seen.add(doi)
            if it.get("type") in ("book-review","component","dataset","peer-review"): continue
            oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
            a=ab(oa) or ""
            if len(a)<300: continue
            rec={"doi":doi,"title":oa.get("title") or "","year":oa.get("publication_year"),
                 "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
                 "type":oa.get("type"),"abs_len":len(a),"abstract":a,
                 "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if best: break
        time.sleep(1.5)
    res[topic]=best
    print(f"{'OK' if best else '--'} {topic:<16} {(best['title'][:52] if best else '-')} ({best.get('year') if best else ''})",flush=True)
    time.sleep(1.5)
json.dump(res,open(os.path.join(ROOT,"reports","round40_bridge2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)