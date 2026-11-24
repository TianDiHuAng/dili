# -*- coding: utf-8 -*-
"""第52轮 B1：按 D110（两库+两检索式+全记录）为侧面文献条目检索主来源。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"印加帝国":dict(claim="印加帝国的疆域、道路与行政",obj="inca",
  qs=["Inca empire road system administration","Inca state expansion territory Cusco"],
  slots=["empire","road","administrat","territor","state"]),
"文艺复兴意大利":dict(claim="城邦竞争、商业财富与艺术赞助",obj="renaissance",
  qs=["Italian Renaissance city-state economy","Renaissance Italy urban economy patronage"],
  slots=["city","econom","patron","state","urban"]),
"亚马逊盆地":dict(claim="亚马逊盆地的地貌、水文与生态",obj="amazon",
  qs=["Amazon basin geomorphology hydrology","Amazon basin landscape evolution"],
  slots=["basin","landscape","hydrolog","geomorph"]),
"库什与努比亚":dict(claim="库什的商路与商品结构",obj="kush",
  qs=["Meroe trade routes goods exchange","Kushite long-distance trade"],
  slots=["trade","route","exchange","good"]),
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
def try_one(t,spec,q):
    """用一个检索式跑 Crossref，返回合格候选列表与拒绝明细。"""
    ok=[];rej=[];n=0
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        n+=1
        doi=it.get("DOI"); typ=it.get("type")
        if not doi: continue
        if typ in ("book-review","component","dataset","peer-review","posted-content"):
            rej.append({"doi":doi,"title":(it.get("title") or [""])[0][:40],"why":f"type={typ}"});continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        ti=(oa.get("title") or "").lower(); al=a.lower()
        if len(a)<400:
            rej.append({"doi":doi,"title":ti[:40],"why":f"摘要{len(a)}字符<400"});continue
        if spec["obj"] not in ti:
            rej.append({"doi":doi,"title":ti[:40],"why":"标题无对象词"});continue
        hit=[s for s in spec["slots"] if s in al or s in ti]
        if len(hit)<2:
            rej.append({"doi":doi,"title":ti[:40],"why":f"主题槽仅{hit}"});continue
        ok.append({"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
          "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
          "type":oa.get("type"),"abs_len":len(a),"abstract":a,"slots":hit,
          "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    ok.sort(key=lambda x:-(x.get("cited") or 0))
    return {"query":q,"results":n,"passed":ok,"rejected":rej[:6]}

res={}
for t,spec in Q.items():
    recs=[]
    for q in spec["qs"]:
        r=try_one(t,spec,q);recs.append(r)
        time.sleep(1.5)
    allpass=[c for r in recs for c in r["passed"]]
    allpass.sort(key=lambda x:-(x.get("cited") or 0))
    res[t]={"claim":spec["claim"],"records":recs,"best":allpass[0] if allpass else None}
    b=allpass[0] if allpass else None
    print(f"{'OK' if b else '--'} {t:<12} {(b['title'][:46] if b else '-')} ({b.get('year') if b else ''}) cite={b.get('cited') if b else ''}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round52_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["best"]),"/",len(Q),flush=True)