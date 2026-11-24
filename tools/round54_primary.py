# -*- coding: utf-8 -*-
"""第54轮B：为 6 条剩余侧面条目检索主来源（D112：两库 + 变音归一 + 全记录）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(s):
    """变音归一：Yüan→yuan、Kōryŏ→koryo 等（D112/D070）。"""
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))
Q={
"古埃及中王国":dict(claim="中王国的行政与灌溉开发",obj="egypt",
  qs=["Middle Kingdom Egypt administration irrigation","Middle Kingdom Egypt state"],slots=["middle kingdom","administrat","irrigation","state"]),
"澳大利亚内陆干旱气候":dict(claim="澳大利亚内陆干旱气候的成因",obj="arid",
  qs=["Australian arid zone climate causes","Australia arid interior climate variability"],slots=["arid","climate","precipitation","variab"]),
"南极半岛":dict(claim="南极半岛的冰架与变暖响应",obj="peninsula",
  qs=["Antarctic Peninsula ice shelf warming","Antarctic Peninsula climate change ice"],slots=["peninsula","ice shelf","warming","climate"]),
"新法兰西":dict(claim="新法兰西殖民地的地理与经济",obj="france",
  qs=["New France colony geography economy","French colonial North America fur trade"],slots=["france","colony","fur","trade","geograph"]),
"古巴岛":dict(claim="古巴岛的地质与地形",obj="cuba",
  qs=["geology of Cuba island","Cuban geology tectonics"],slots=["geolog","tecton","stratigraph","island"]),
"巴塔哥尼亚":dict(claim="巴塔哥尼亚的地理与气候",obj="patagonia",
  qs=["Patagonia climate geography","Patagonian climate westerlies"],slots=["climate","westerl","geograph","precipitation"]),
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
def search_crossref(q,rows=18):
    return (cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+f"&rows={rows}&select=title,DOI,type").get("message") or {}).get("items") or []
def search_openalex(q,rows=15):
    for _ in range(3):
        d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+f"&per_page={rows}&mailto=geo-encyclopedia@example.com")
        if d.get("results") is not None: return d["results"]
        time.sleep(8)
    return []
res={}
for t,spec in Q.items():
    recs=[];passed=[]
    for q in spec["qs"]:
        items=search_crossref(q)
        n_cr=len(items)
        for it in items:
            doi=it.get("DOI")
            if not doi or it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
            a=ab(oa) or ""
            if len(a)<400: continue
            ti=norm(oa.get("title")); al=norm(a)
            if spec["obj"] not in ti: continue
            hit=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(hit)<2: continue
            passed.append({"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
              "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
              "type":oa.get("type"),"abs_len":len(a),"slots":hit,
              "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))})
        recs.append({"engine":"Crossref","query":q,"results":n_cr})
        time.sleep(1.2)
    # OpenAlex 第二库（D112）
    for q in spec["qs"][:1]:
        items=search_openalex(q)
        n_oa=len(items)
        for w in items:
            oid=(w.get("id") or "").rsplit("/",1)[-1]
            if any(p["oa_id"]==oid for p in passed): continue
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if spec["obj"] not in ti: continue
            hit=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(hit)<2: continue
            passed.append({"doi":w.get("doi",""),"title":w.get("title"),"year":w.get("publication_year"),
              "oa_id":oid,"cited":w.get("cited_by_count"),"type":w.get("type"),"abs_len":len(a),"slots":hit,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
        recs.append({"engine":"OpenAlex","query":q,"results":n_oa})
    passed.sort(key=lambda x:-(x.get("cited") or 0))
    res[t]={"claim":spec["claim"],"records":recs,"best":passed[0] if passed else None}
    b=passed[0] if passed else None
    print(f"{'OK' if b else '--'} {t:<14} {(b['title'][:42] if b else '-')} ({b.get('year') if b else ''}) cite={b.get('cited') if b else ''}",flush=True)
    time.sleep(1)
json.dump(res,open(os.path.join(ROOT,"reports","round54_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["best"]),"/",len(Q),flush=True)