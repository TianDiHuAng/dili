# -*- coding: utf-8 -*-
"""第76轮：重要条目第二批 12 条检索。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
SPEC={
"吠陀时代":(["vedic"],["Vedic period society","Vedic India religion society"],["vedic","society","religion","india","period"]),
"孔雀王朝":(["maurya","mauryan","asoka","ashoka"],["Mauryan empire administration","Ashoka Maurya policy"],["maurya","empire","administrat","state","asoka"]),
"笈多王朝":(["gupta"],["Gupta empire polity","Gupta dynasty culture economy"],["gupta","empire","polity","econom","culture"]),
"周代":(["zhou"],["Zhou dynasty state","Zhou China feudal system"],["zhou","dynasty","state","feudal","system"]),
"明清":(["ming","qing"],["Ming Qing state society","late imperial China economy"],["ming","qing","state","society","econom"]),
"吴哥":(["angkor","khmer"],["Angkor state hydraulic","Khmer empire administration"],["angkor","khmer","state","hydraul","administrat"]),
"马来群岛":(["malay","archipelago","srivijaya","majapahit"],["Malay archipelago trade states","Srivijaya maritime state"],["malay","archipelago","trade","state","maritime"]),
"河中地区":(["transoxiana","samarkand","sogdian"],["Transoxiana cities trade","Sogdian merchants Central Asia"],["transoxiana","samarkand","sogdian","trade","city"]),
"匈奴":(["xiongnu"],["Xiongnu state steppe","Xiongnu empire organization"],["xiongnu","state","steppe","empire","organiz"]),
"突厥":(["turk","turkic"],["Turkic khaganate steppe state","Turkic empires Central Asia"],["turk","turkic","khaganate","state","steppe"]),
"阿拉伯半岛":(["arabian peninsula","arabia"],["Arabian Peninsula geography","Arabia climate environment"],["arabian","arabia","geograph","climate","environment"]),
"克里特文明":(["minoan","crete"],["Minoan palace society","Minoan Crete state"],["minoan","crete","palace","society","state"]),
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
    print(f"{'OK' if u else '--'} {t:<10} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round76_imp2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v["cand"]),"/",len(SPEC),flush=True)