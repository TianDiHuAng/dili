# -*- coding: utf-8 -*-
"""第35轮续：为剩余 18 条做精筛检索（要求标题同时含对象词与主题词）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"古巴比伦":[("Babylonia state formation Mesopotamia","babylon"),("Babylon city urbanism","babylon")],
"吠陀时代":[("Vedic period society India","vedic"),("Vedic literature Indo-Aryan","vedic")],
"明清":[("Ming Qing China economy trade","ming"),("Ming dynasty state","ming")],
"朝鲜半岛":[("Korean Peninsula geography climate","korean peninsula"),("Korea physical geography","korea")],
"中南半岛":[("Indochina Peninsula geography geology","indochina"),("Southeast Asia monsoon geography","southeast asia")],
"突厥":[("Turkic khaganate empire steppe","turkic"),("Turkic peoples Central Asia history","turkic")],
"黎凡特":[("Levant region geography climate","levant"),("Levant coastal plain geography","levant")],
"安纳托利亚":[("Anatolian plateau geography","anatolia"),("Anatolia land use history","anatolia")],
"莫斯科公国":[("Muscovy state formation","muscovy"),("Muscovy Russian lands","muscovy")],
"巴尔干半岛":[("Balkan Peninsula physical geography","balkan"),("Balkans climate geography","balkans")],
"斯堪的纳维亚":[("Scandinavian Peninsula geography","scandinavia"),("Scandinavia landforms glaciation","scandinavia")],
"欧洲温带海洋性气候":[("oceanic climate Europe","oceanic climate"),("maritime climate western europe","maritime climate")],
"美国西进":[("westward expansion United States","westward"),("American frontier settlement","frontier")],
"巴西高原":[("Brazilian Highlands","brazilian highlands"),("Brazil plateau geomorphology","plateau")],
"巴西殖民经济":[("colonial Brazil economy","colonial brazil"),("Brazil sugar plantation colonial","brazil")],
"大堡礁":[("Great Barrier Reef coral ecology","great barrier reef"),("Great Barrier Reef","barrier reef")],
"冲积平原":[("alluvial plain floodplain formation","alluvial"),("alluvial fan plain sediment","alluvial")],
"山地农业":[("mountain agriculture terrace","mountain agriculture"),("highland farming systems","highland")],
}
def get(u):
    for _ in range(4):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=40)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: time.sleep(4);continue
            b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip() or 0)
            if code==200: return b
            time.sleep(6)
        except Exception: time.sleep(4)
    return "{}"
def ab_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,pairs in Q.items():
    best=None
    for q,needle in pairs:
        u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=15&mailto=geo-encyclopedia@example.com")
        try: d=json.loads(get(u))
        except Exception: d={}
        for w in d.get("results",[]):
            a=ab_of(w)
            if not a or len(a)<300: continue
            ti=(w.get("title") or "").lower()
            if needle not in ti: continue
            if w.get("type") in ("book-review","paratext","editorial","letter"): continue
            cand={"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),"year":w.get("publication_year"),
              "doi":w.get("doi"),"cited":w.get("cited_by_count"),"type":w.get("type"),"abstract":a,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            if best is None or (cand.get("cited") or 0)>(best.get("cited") or 0): best=cand
        if best: break
        time.sleep(4)
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<14} {(best['title'][:54] if best else '-')} ({best.get('year') if best else ''})")
    time.sleep(3)
json.dump(res,open(os.path.join(ROOT,"reports","round35_openalex2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q))