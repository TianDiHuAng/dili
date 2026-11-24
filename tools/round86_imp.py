# -*- coding: utf-8 -*-
"""第86轮：重要 G3b 前 10 条，改用综述性检索词（D144 合规）。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
STAT={"ok":0,"fail":0}
def get(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",
                              "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: STAT["fail"]+=1; time.sleep(4); continue
            b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
            if code!=200: STAT["fail"]+=1; time.sleep(4 if code in (429,503) else 2); continue
            STAT["ok"]+=1
            return json.loads(b) if b.strip().startswith("{") else {}
        except Exception: STAT["fail"]+=1; time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
# 综述性检索词：history / historiography / state formation / political economy
SPEC={
"阿拉伯征服北非":(["conquest","north africa","maghrib","islamic"],["Arab conquest North Africa history","Islamic conquest Maghrib"],["conquest","maghrib","north africa","islamic","arab"]),
"桑海帝国":(["songhai","songhay"],["Songhai empire history","Songhay state formation"],["songhai","songhay","empire","history","state"]),
"萨珊波斯":(["sasanian","sassanian"],["Sasanian empire history","Sasanian Iran political economy"],["sasanian","empire","history","politic","econom"]),
"吠陀时代":(["vedic"],["Vedic period history","Vedic India society economy"],["vedic","history","society","econom","period"]),
"笈多王朝":(["gupta"],["Gupta empire history","Gupta dynasty political economy"],["gupta","empire","history","politic","econom"]),
"明清":(["ming","qing"],["Ming Qing history","late imperial China political economy"],["ming","qing","history","politic","econom"]),
"马来群岛":(["malay","srivijaya","majapahit","archipelago"],["Malay archipelago history","Southeast Asia island states economy"],["malay","archipelago","history","state","econom"]),
"河中地区":(["transoxiana","sogdian"],["Transoxiana history","Central Asia Sogdian economy society"],["transoxiana","sogdian","history","econom","society"]),
"克里特文明":(["minoan","crete"],["Minoan civilization history","Minoan Crete economy society"],["minoan","crete","history","econom","society"]),
"十字军东征":(["crusade","crusader"],["Crusades history crusader states","crusading movement economy"],["crusad","history","state","econom","movement"]),
}
res={}
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        cr=get("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
        for it in ((cr.get("message") or {}).get("items") or []):
            doi=it.get("DOI")
            if not doi or it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            w=get(f"https://api.openalex.org/works/https://doi.org/{doi}")
            a=ab(w) or ""
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in objs): continue
            h=[s for s in slots if norm(s) in al or norm(s) in ti]
            if len(h)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10 and len(a)<800: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":cited,"abs_len":len(a),"slots":h,"doi":doi})
            time.sleep(0.3)
        time.sleep(0.6)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:42] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round86_imp4.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)
print("命中:",sum(1 for v in res.values() if v["cand"]),"/",len(res),flush=True)