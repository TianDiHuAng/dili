# -*- coding: utf-8 -*-
"""第104轮：G3a 剩余 7 条找互补来源（D156 已查现有强源）。"""
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
USED={"朝鲜半岛":["W2020449353"],"中南半岛":["W1935059050"],"黎凡特":["W2884062598"],
"古埃及中王国":["W2339022878"],"争议边界处理原则":["W3216751933"],
"教育机会地域差异":["W4317206970"],"人文地理学":["W2038018335"]}
SPEC={
"朝鲜半岛":(["korea","korean"],["Korean peninsula geology geography","Korea topography environment"],["korea","korean","geolog","geograph","topograph","environment"]),
"中南半岛":(["indochina","mainland southeast asia"],["Mainland Southeast Asia states history","Indochina peninsula society"],["indochina","mainland","state","history","society"]),
"黎凡特":(["levant"],["Levant geography corridor","Levant archaeology settlement"],["levant","geograph","corridor","archaeolog","settlement"]),
"古埃及中王国":(["middle kingdom","egypt"],["Middle Kingdom Egypt economy society","Egypt Middle Kingdom literature culture"],["middle kingdom","egypt","econom","society","culture"]),
"争议边界处理原则":(["boundary dispute","delimitation"],["Boundary delimitation principles international law","territorial dispute settlement"],["boundary","delimitation","dispute","settlement","territorial"]),
"教育机会地域差异":(["education inequality","regional education"],["Regional inequality education access","education opportunity geography"],["educat","inequal","regional","access","opportunit"]),
"人文地理学":(["human geography"],["Human geography discipline review","human geography development field"],["human geography","discipline","review","development","field"]),
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
            oid=(w.get("id") or "").rsplit("/",1)[-1]
            if oid in USED.get(t,[]): continue
            cands.append({"oid":oid,"title":w.get("title"),"year":w.get("publication_year"),
              "cited":cited,"abs_len":len(a),"slots":h,"doi":doi})
            time.sleep(0.3)
        time.sleep(0.6)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<13} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round104_g3a.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)