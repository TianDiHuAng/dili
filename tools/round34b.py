# -*- coding: utf-8 -*-
"""第34轮续：标注 Wikidata 不可达 + 为剩余条目换词检索 OpenAlex。"""
import subprocess,json,os,urllib.parse,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 1) 标注 wikidata 来源当前不可达
P=os.path.join(ROOT,"data","sources.json");sd=json.load(open(P,encoding="utf-8"))
cnt=0
for s in sd["sources"]:
    if s["id"].startswith("wikidata-") and s.get("link_ok"):
        s["link_ok"]=False
        s["note"]=(s.get("note") or "")+" 【第34轮复测 2026-11-23】www.wikidata.org 连接被重置/超时（api.php 与 /entity/ 均 000），当前不可达；第33轮核验时可用，内容记录保留。"
        cnt+=1
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("标注 wikidata 不可达:",cnt)

# 2) 换词检索剩余条目
Q2={
"蒙古帝国":"Mongol empire thirteenth century Eurasia review",
"阿兹特克":"Aztec state formation central Mexico",
"罗马阿非利加":"Roman North Africa provinces economy",
"加纳帝国":"Ghana empire Wagadu Sudanic West Africa",
"商代":"Shang civilization bronze age China",
"周代":"Zhou dynasty Western Zhou China",
"马格里布":"Maghreb regional geography northwest Africa",
"埃塞俄比亚高原":"Ethiopian plateau highlands climate",
"城市起源":"urban revolution first cities Mesopotamia",
"长江流域":"Yangtze River basin hydrology China",
}
def get(u):
    return subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",u],
                          capture_output=True,timeout=40).stdout.decode("utf-8","ignore")
def ab_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))
out={}
for t,q in Q2.items():
    u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+
       "&per_page=10&mailto=geo-encyclopedia@example.com")
    try: d=json.loads(get(u))
    except Exception: out[t]=[];print(f"{t:<10} ERR");continue
    good=[]
    for w in d.get("results",[]):
        a=ab_of(w)
        if not a or len(a)<300: continue
        if w.get("type") not in ("article","book","review","book-chapter","proceedings-article"): continue
        good.append({"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
          "year":w.get("publication_year"),"doi":w.get("doi"),"cited":w.get("cited_by_count"),
          "abstract":a,"host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    good.sort(key=lambda x:-(x.get("cited") or 0))
    out[t]=good
    print(f"{t:<10} {len(good)}条 | {(good[0]['title'][:56] if good else '-')} ({good[0]['year'] if good else ''})")
json.dump(out,open(os.path.join(ROOT,"reports","round34_openalex2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有候选:",sum(1 for v in out.values() if v))