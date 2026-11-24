# -*- coding: utf-8 -*-
"""第97轮：G3a 重要前 12 条找第二对位来源（Crossref，D144 合规）。"""
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
SPEC={
"尼罗河三角洲":(["nile delta","delta"],["Nile Delta sediment evolution","Nile Delta subsidence erosion"],["nile","delta","sediment","subsid","erosion"]),
"古埃及古王国":(["old kingdom","egypt","giza"],["Old Kingdom Egypt society economy","Giza pyramids labour organization"],["old kingdom","egypt","society","econom","pyramid","labour"]),
"古埃及新王国":(["new kingdom","egypt"],["New Kingdom Egypt empire administration","Egypt New Kingdom economy society"],["new kingdom","egypt","empire","administrat","econom"]),
"宋代":(["song","southern song","northern song"],["Song dynasty China economy","Song China state society"],["song","dynasty","econom","state","society","china"]),
"元代":(["yuan","mongol","china"],["Yuan dynasty China administration","Yuan China economy society"],["yuan","mongol","dynasty","administrat","econom","society"]),
"朝鲜半岛":(["korea","korean"],["Korean peninsula history","Korea geography environment"],["korea","korean","history","geograph","environment"]),
"中南半岛":(["indochina","mainland southeast asia"],["Indochina peninsula geography","mainland Southeast Asia states"],["indochina","mainland","geograph","state","peninsula"]),
"突厥":(["turk","turkic","khaganate"],["Turkic khaganate state","Turkic empires steppe politics"],["turk","turkic","khaganate","state","steppe","politic"]),
"黎凡特":(["levant"],["Levant history geography","Levant archaeology society"],["levant","history","geograph","archaeolog","society"]),
"拜占庭帝国":(["byzantine"],["Byzantine empire administration","Byzantine state economy society"],["byzantine","empire","administrat","econom","society"]),
"伊比利亚半岛":(["iberia","iberian peninsula"],["Iberian Peninsula geography","Iberia history environment"],["iberia","iberian","geograph","history","environment"]),
"高卢":(["gaul","gaulish"],["Roman Gaul society economy","Gaul geography history"],["gaul","gaulish","society","econom","geograph"]),
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
    print(f"{'OK' if u else '--'} {t:<11} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round97_g3a.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)