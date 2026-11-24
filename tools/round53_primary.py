# -*- coding: utf-8 -*-
"""第53轮 B1：为 8 条侧面条目检索主来源（D110 两检索式 + 全记录）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"莫切文化":dict(claim="莫切文化的河谷政治与灌溉社会",obj="moche",
  qs=["Moche society irrigation politics","Moche state organization valleys"],
  slots=["irrigation","politic","state","society","valley"]),
"阿塔卡马沙漠":dict(claim="阿塔卡马沙漠的极端干旱与形成机制",obj="atacama",
  qs=["Atacama Desert hyperaridity climate","Atacama Desert formation aridity"],
  slots=["hyperarid","arid","climate","precipitation","formation"]),
"元代":dict(claim="元代的行政、驿站与海运",obj="yuan",
  qs=["Yuan dynasty state administration","Yuan empire transport communications"],
  slots=["administrat","state","transport","relay","communication"]),
"意大利半岛":dict(claim="意大利半岛的地质构造与地形",obj="italy",
  qs=["geology of Italy Apennines tectonics","Italian peninsula geomorphology"],
  slots=["geolog","tecton","apenning","geomorph"]),
"河中地区":dict(claim="河中地区的绿洲、灌溉与商路",obj="transoxiana",
  qs=["Transoxiana oasis irrigation trade","Central Asia Samarkand Bukhara irrigation"],
  slots=["irrigation","oasis","trade","samarkand","bukhara"]),
"突厥":dict(claim="突厥汗国的草原政治与扩张",obj="turk",
  qs=["Turkic khaganate steppe polity","Gokturk empire expansion"],
  slots=["khaganate","steppe","empire","expansion"]),
"城市地理":dict(claim="城市地理学的城市形态与结构研究",obj="urban",
  qs=["urban geography morphology structure","urban morphology city structure"],
  slots=["morpholog","structure","city","urban"]),
"地理信息系统":dict(claim="GIS 的空间分析与决策支持",obj="gis",
  qs=["geographic information system spatial analysis","GIS spatial decision support"],
  slots=["spatial","analysis","decision","information system"]),
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
json.dump(res,open(os.path.join(ROOT,"reports","round53_primary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["best"]),"/",len(Q),flush=True)