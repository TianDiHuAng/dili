# -*- coding: utf-8 -*-
"""第103轮：G3b 重要 7 条（跳过 3 条无解）——按 D156 找互补来源。"""
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
# 排除已有
USED={"隋唐":["W4304193318"],"明清":["W2081119930"],"威尼斯":["W2104329013"],
"大分水岭":["W3153139914"],"南极条约体系":["W4387309994"],
"冲积平原":["W2154930938"],"山地农业":["W1972724176"]}
SPEC={
"隋唐":(["tang","sui","china"],["Tang dynasty society economy","Tang China social history"],["tang","society","econom","social","history"]),
"明清":(["ming","qing","china"],["Ming Qing state and society","late imperial China economy society"],["ming","qing","state","society","econom"]),
"威尼斯":(["venice","venetian"],["Venetian maritime empire","Venice republic politics society"],["venice","venetian","maritime","empire","politic"]),
"大分水岭":(["great dividing range","dividing range"],["Great Dividing Range geology uplift","eastern Australia highlands geology"],["dividing","range","geolog","uplift","highland"]),
"南极条约体系":(["antarctic treaty"],["Antarctic Treaty System governance","Antarctic treaty regime evolution"],["antarctic treaty","governance","regime","evolution","system"]),
"冲积平原":(["alluvial plain","floodplain"],["alluvial plain formation","floodplain sedimentation dynamics"],["alluvial","floodplain","formation","sediment","plain"]),
"山地农业":(["mountain agriculture","terrace"],["mountain agriculture terraces farming","highland agriculture systems"],["mountain","agricultur","terrace","farming","highland"]),
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
    print(f"{'OK' if u else '--'} {t:<11} {(u[0]['title'][:46] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round103_g3b.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
tot=STAT["ok"]+STAT["fail"]
print(f"\nHTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}（{STAT['fail']/max(tot,1):.0%}）",flush=True)