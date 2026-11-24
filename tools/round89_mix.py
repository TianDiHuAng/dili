# -*- coding: utf-8 -*-
"""第89轮：G3a 4 条按 D140 写明限定；试 3 条重要级。"""
import subprocess,json,os,urllib.parse,time,unicodedata,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
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

# 1) 3 条重要级新尝试（换更宽的综述词）
SPEC={
"吠陀时代":(["vedic","arya"],["Vedic society religion economy","early India vedic period state"],["vedic","society","religion","econom","state"]),
"明清":(["ming","qing","china"],["Ming Qing China economy society","late imperial China history"],["ming","qing","econom","society","history","china"]),
"马来群岛":(["malay","southeast asia","nusantara"],["Malay world trade states","Southeast Asian maritime polities"],["malay","trade","state","maritime","polities"]),
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
    print(f"{'OK' if u else '--'} {t:<10} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} 候选{len(u)}",flush=True)
json.dump({"results":res,"http":{"ok":STAT["ok"],"fail":STAT["fail"]}},
 open(os.path.join(ROOT,"reports","round89_imp7.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 2) G3a 4 条按 D140 写明
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
G3A={
"宋代":"【第89轮·G3a 说明（D140）】本条现有 1 个整体性内容来源，另有**弱来源**（摘要/正文不足或主题偏侧）已登记并降为旁证。按 D140 归入「G3a：有侧面/弱来源可补充，缺整体研究」。",
"突厥":"【第89轮·G3a 复核（D140）】本条现有 1 个整体性内容来源，另有**侧面向文献**（突厥时期女性墓葬等）已降旁证——只研究其中一个侧面，不计为第二内容源。",
"马丘比丘":"【第89轮·G3a 复核（D140）】本条现有 1 个整体性内容来源，另有**侧面向文献**（建筑艺术等）已降旁证。",
"教育机会地域差异":"【第89轮·G3a 说明（D140）】本条属**指标解读类**但强来源仅 1 个、另有 2 个弱来源：正文以指标解释与空间差异为主，弱来源（统计口径说明等）已降旁证。按 D140 归入 G3a。",
}
for t,txt in G3A.items():
    e=T.get(t)
    if not e: continue
    if "G3a" in (e.get("pending_notes") or ""): continue
    e["pending_notes"]=((e.get("pending_notes") or "")+" "+txt).strip()
    e["last_update"]=TODAY
save_docs(docs); update_coverage(docs)
print("G3a 已写明 4 条")
print(f"HTTP：成功 {STAT['ok']} / 失败 {STAT['fail']}")