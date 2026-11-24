# -*- coding: utf-8 -*-
"""第84轮：补充 G3b 12 条（D144 合规：Crossref 路线 + HTTP 状态统计）。"""
import subprocess,json,os,urllib.parse,time,unicodedata,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
STAT={"ok":0,"fail":0,"err":[]}
def get(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",
                              "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw:
                STAT["fail"]+=1; STAT["err"].append(("no-http",url[:50])); time.sleep(4); continue
            b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
            if code!=200:
                STAT["fail"]+=1; STAT["err"].append((code,url[:50])); time.sleep(4 if code in (429,503) else 2); continue
            STAT["ok"]+=1
            return json.loads(b) if b.strip().startswith("{") else {}
        except Exception as ex:
            STAT["fail"]+=1; STAT["err"].append(("exc",str(ex)[:40])); time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
SPEC={
"基辅罗斯":(["kyivan","kievan","rus"],["Kyivan Rus state","Kievan Rus society economy"],["kyivan","kievan","rus","state","society"]),
"欧洲冰期地貌":(["glacial","pleistocene"],["European glacial landforms","Pleistocene glaciation Europe"],["glacial","pleistocene","landform","europe"]),
"阿巴拉契亚山脉":(["appalachian"],["Appalachian orogeny geology","Appalachian mountains evolution"],["appalachian","orogen","geolog","evolution"]),
"西北海岸":(["northwest coast"],["Northwest Coast indigenous society","Pacific Northwest coast archaeology"],["northwest coast","indigenous","society","archaeolog"]),
"新法兰西":(["new france","nouvelle-france"],["New France colony economy","French colonial Canada society"],["new france","colony","econom","society","canada"]),
"的的喀喀湖":(["titicaca"],["Lake Titicaca basin society","Titicaca paleoclimate"],["titicaca","lake","basin","society","paleoclimat"]),
"查文文化":(["chavin","chavin de huantar"],["Chavin de Huantar society","Chavin culture Andes"],["chavin","society","culture","andes","huantar"]),
"纳斯卡文化":(["nazca","nasca"],["Nazca culture society","Nasca lines archaeology"],["nazca","nasca","culture","society","archaeolog"]),
"奇穆帝国":(["chimu"],["Chimu state administration","Chimu empire irrigation"],["chimu","state","administrat","empire","irrigation"]),
"南美贸易网络":(["andean","exchange"],["Andean exchange networks","prehispanic Andean trade"],["andean","exchange","trade","network","prehispanic"]),
"美拉尼西亚":(["melanesia","melanesian"],["Melanesian societies","Melanesia archaeology culture"],["melanesia","melanesian","societ","archaeolog","culture"]),
"密克罗尼西亚":(["micronesia","micronesian"],["Micronesian societies","Micronesia islands settlement"],["micronesia","micronesian","societ","settle","island"]),
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
    tot=STAT["ok"]+STAT["fail"]
    if tot>20 and STAT["fail"]/tot>0.5:
        print(f"⚠ 失败率超阈值，中止",flush=True); break
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"],"errors":STAT["err"][:8]}},
 open(os.path.join(ROOT,"reports","round84_sup3.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)
print("命中:",sum(1 for v in res.values() if v["cand"]),"/",len(res),flush=True)