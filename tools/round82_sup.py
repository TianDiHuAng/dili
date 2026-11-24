# -*- coding: utf-8 -*-
"""第82轮：补充条目 G3b 前 12 条检索。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
SPEC={
"古埃及中王国":(["middle kingdom","egypt"],["Middle Kingdom Egypt state","Egypt Middle Kingdom administration economy"],["middle kingdom","egypt","state","administrat","econom"]),
"法蒂玛王朝":(["fatimid"],["Fatimid state administration","Fatimid caliphate economy"],["fatimid","state","administrat","caliphate","econom"]),
"非洲大湖地区":(["great lakes","africa"],["African Great Lakes region","East African Great Lakes states"],["great lakes","region","africa","state","lake"]),
"赫梯王国":(["hittite"],["Hittite empire administration","Hittite state society"],["hittite","empire","administrat","state","society"]),
"贵霜帝国":(["kushan"],["Kushan empire state","Kushan administration economy"],["kushan","empire","state","administrat","econom"]),
"仰韶文化":(["yangshao"],["Yangshao culture society","Yangshao Neolithic China"],["yangshao","culture","society","neolithic","china"]),
"室利佛逝":(["srivijaya"],["Srivijaya state maritime","Srivijaya trade empire"],["srivijaya","state","maritime","trade","empire"]),
"满者伯夷":(["majapahit"],["Majapahit empire state","Majapahit Java administration"],["majapahit","empire","state","administrat","java"]),
"帖木儿帝国":(["timurid"],["Timurid empire state","Timurid administration economy"],["timurid","empire","state","administrat","econom"]),
"迈锡尼文明":(["mycenaean"],["Mycenaean palace state","Mycenaean Greece society"],["mycenaean","palace","state","society","greece"]),
"神圣罗马帝国":(["holy roman empire"],["Holy Roman Empire institutions","Holy Roman Empire constitution"],["holy roman","empire","institution","constitution","state"]),
"汉萨同盟":(["hanseatic","hansa"],["Hanseatic League trade","Hansa network cities"],["hanseatic","hansa","trade","network","city"]),
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
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=20&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            if (w.get("type") or "")=="book-review": continue
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in objs): continue
            h=[s for s in slots if norm(s) in al or norm(s) in ti]
            if len(h)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10 and len(a)<800: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":cited,"abs_len":len(a),"slots":h,"doi":w.get("doi","")})
        time.sleep(0.7)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:42] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round82_sup1.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v["cand"]),"/",len(SPEC),flush=True)