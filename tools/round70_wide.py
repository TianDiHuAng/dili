# -*- coding: utf-8 -*-
"""第70轮：为 G1 五条用宽检索重试（对象词放宽、槽位≥1、两库）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
Q={
"隋唐":dict(objs=["tang","sui","china","chinese"],qs=["Tang dynasty China society","medieval China state administration","Tang China economy"],
  slots=["tang","sui","dynasty","china","state","administrat","econom","society"]),
"十字军东征":dict(objs=["crusad","crusader"],qs=["Crusades Levant states","crusader states Latin East","Crusading movement Mediterranean"],
  slots=["crusad","levant","latin east","mediterran","state","movement"]),
"克里特文明":dict(objs=["minoan","crete","aegean"],qs=["Minoan Bronze Age Aegean","Cretan Bronze Age society","Aegean Bronze Age palace"],
  slots=["minoan","crete","aegean","bronze age","palace","society"]),
"大平原":dict(objs=["great plains","plains"],qs=["Great Plains bison grassland","North American plains agriculture drought","US Great Plains settlement"],
  slots=["great plains","plains","bison","grassland","agricultur","drought","settle"]),
"澳大利亚大陆":dict(objs=["australia","australian"],qs=["Australia geology continent","Australia climate arid interior","Australian landform geography"],
  slots=["australia","geolog","climate","arid","landform","geograph","continent"]),
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
    cands=[]
    for q in spec["qs"]:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=20&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            if (w.get("type") or "")=="book-review": continue
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in spec["objs"]): continue
            h=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(h)<1: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":w.get("cited_by_count") or 0,
              "abs_len":len(a),"slots":h,"doi":w.get("doi",""),"type":w.get("type")})
        time.sleep(0.8)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    # 只留强（被引≥10 或摘要≥800）
    strong=[c for c in u if c["cited"]>=10 or c["abs_len"]>=800]
    strong.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":strong[:3],"n":len(u),"nstrong":len(strong)}
    print(f"== {t}: 候选{len(u)} 强{len(strong)}")
    for c in strong[:3]:
        print(f"     {c['cited']:>5}引 {c['abs_len']:>5}字 {c['year']} 《{c['title'][:56]}》 槽{c['slots'][:3]}")
json.dump(res,open(os.path.join(ROOT,"reports","round70_wide.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)