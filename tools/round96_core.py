# -*- coding: utf-8 -*-
"""第96轮：核心 G3a 9 条找第二对位来源（Crossref，D144 合规）。"""
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
# 排除已用过的 oid
USED={"撒哈拉沙漠":["W2794663306","W3077545719"],"马里帝国":["W2089041290","W1970609697"],
"苏美尔城邦":["W150669647","W4388058220"],"长江流域":["W2805650462"],"汉代":["W4403972561","W2113119651"],
"大平原":["W2992002638","W2186081253"],"澳大利亚大陆":["W2010976353","W2120218248"],
"波利尼西亚":["W1973139594","W2241623891"],"南极冰盖":["W196115473"]}
SPEC={
"撒哈拉沙漠":(["sahara","saharan"],["Sahara Quaternary palaeoclimate","Sahara desertification past climate"],["sahara","palaeoclimat","quaternary","desertif","climate"]),
"马里帝国":(["mali","mansa","sahel"],["Mali empire gold trade Sahel","medieval Mali state economy"],["mali","empire","gold","trade","sahel","state"]),
"苏美尔城邦":(["sumer","sumerian","uruk","mesopotamia"],["Mesopotamian urbanism state","Uruk settlement hierarchy"],["sumer","mesopotamia","urbanism","state","settlement"]),
"长江流域":(["yangtze","changjiang"],["Yangtze basin geography","Yangtze river civilization agriculture"],["yangtze","changjiang","basin","geograph","agricultur"]),
"汉代":(["han","china"],["Han dynasty state economy","Han empire administration society"],["han","dynasty","empire","state","econom"]),
"大平原":(["great plains"],["Great Plains environment agriculture","Great Plains grassland history"],["great plains","environment","grassland","agricultur","history"]),
"澳大利亚大陆":(["australia","australian"],["Australia continent geology","Australian environment climate"],["australia","geolog","environment","climate","continent"]),
"波利尼西亚":(["polynesia","polynesian"],["Polynesian dispersal settlement","Polynesia colonization archaeology"],["polynesia","polynesian","dispersal","coloniz","settlement"]),
"南极冰盖":(["antarctic ice sheet"],["Antarctic ice sheet dynamics","East Antarctic ice sheet history"],["antarctic","ice sheet","dynamic","history","mass"]),
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
            if w.get("type")=="book-review": continue
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
    print(f"{'OK' if u else '--'} {t:<10} {(u[0]['title'][:42] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round96_core.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)