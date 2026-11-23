# -*- coding: utf-8 -*-
"""第44轮续：对失败条目用「标题含对象词」为主判据重试。"""
import subprocess,json,os,urllib.parse,time,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"刚果盆地":("Congo Basin","congo basin"),
"日本列岛":("Japanese archipelago","japanese archipelago"),
"罗马共和国":("Roman Republic","roman republic"),
"南极冰盖":("Antarctic ice sheet","antarctic ice sheet"),
"格陵兰岛":("Greenland ice sheet","greenland"),
"十三殖民地":("Thirteen Colonies","thirteen colonies"),
"冰芯气候记录":("ice core","ice core"),
"北极火情变化":("tundra fire","tundra fire"),
"地理信息系统":("Geographic Information System","geographic information system"),
"城市地理":("urban geography","urban geography"),
"尼罗河谷":"skip",
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
for t,v in Q.items():
    if v=="skip": continue
    q,needle=v
    best=None;seen=set()
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<300: continue
        ti=(oa.get("title") or "").lower()
        if needle not in ti: continue            # 标题必须含对象词（主判据）
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,
             "hits":a.lower().count(needle),"host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=12: break
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<14} {(best['title'][:52] if best else '-')} ({best.get('year') if best else ''})",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round44_zerosrc2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有候选:",sum(1 for v in res.values() if v),"/",len(res),flush=True)