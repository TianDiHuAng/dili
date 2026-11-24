# -*- coding: utf-8 -*-
"""第83轮：D144 合规检索——Crossref 路线，记录 HTTP 状态，区分「无结果」与「请求失败」。"""
import subprocess,json,os,urllib.parse,time,unicodedata,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))

STAT={"ok":0,"fail":0,"err":[]}
def get(url,expect_json=True):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",
                              "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw:
                STAT["fail"]+=1; STAT["err"].append(("no-http", url[:60])); time.sleep(4); continue
            b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
            if code!=200:
                STAT["fail"]+=1; STAT["err"].append((code, url[:60])); time.sleep(4 if code in (429,503) else 2); continue
            STAT["ok"]+=1
            return json.loads(b) if expect_json and b.strip().startswith("{") else b
        except Exception as ex:
            STAT["fail"]+=1; STAT["err"].append(("exc", str(ex)[:40])); time.sleep(3)
    return {}

def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))

SPEC={
"古埃及中王国":(["middle kingdom","egypt"],["Middle Kingdom Egypt state administration"],["middle kingdom","egypt","state","administrat"]),
"法蒂玛王朝":(["fatimid"],["Fatimid caliphate state administration"],["fatimid","state","administrat","caliphate"]),
"非洲大湖地区":(["great lakes"],["African Great Lakes region states"],["great lakes","region","state","africa"]),
"贵霜帝国":(["kushan"],["Kushan empire state administration"],["kushan","empire","state","administrat"]),
"仰韶文化":(["yangshao"],["Yangshao culture Neolithic society"],["yangshao","culture","neolithic","society"]),
"室利佛逝":(["srivijaya"],["Srivijaya maritime state trade"],["srivijaya","maritime","state","trade"]),
"满者伯夷":(["majapahit"],["Majapahit empire state administration"],["majapahit","empire","state","administrat"]),
"帖木儿帝国":(["timurid"],["Timurid empire state economy"],["timurid","empire","state","econom"]),
"迈锡尼文明":(["mycenaean"],["Mycenaean palace state society"],["mycenaean","palace","state","society"]),
}
res={}
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        cr=get("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
        items=(cr.get("message") or {}).get("items") or []
        for it in items:
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
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
    # D144：失败率阈值
    tot=STAT["ok"]+STAT["fail"]
    if tot>20 and STAT["fail"]/tot>0.5:
        print(f"⚠ 失败率 {STAT['fail']}/{tot} 超阈值，中止",flush=True); break

json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"],"errors":STAT["err"][:10]}},
 open(os.path.join(ROOT,"reports","round83_sup2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP 统计：成功 {STAT['ok']} / 失败 {STAT['fail']}（失败率 {STAT['fail']/max(tot,1):.0%}）",flush=True)
print("命中:",sum(1 for v in res.values() if v["cand"]),"/",len(res),flush=True)