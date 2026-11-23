# -*- coding: utf-8 -*-
"""第41轮 B1：剩余 5 条精确检索（DOI 桥，多轮换词）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"阿巴拉契亚山脉":["Appalachian orogeny geology","Appalachian Mountains physiography relief",
                "Appalachian plateau geologic structure"],
"古巴岛":["Cuba Greater Antilles geology","Cuban archipelago geology tectonic",
         "geology of Cuba island"],
"南极特别保护区":["Antarctic Specially Protected Area management","ASPA Antarctic conservation",
              "Antarctic protected areas designation management"],
"争议边界处理原则":["disputed territory cartographic representation","boundary representation maps political",
             "uncertain boundaries mapping"],
"环境治理":["environmental governance effectiveness institutions review",
        "global environmental governance assessment"],
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
    if not inv: return None
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={};detail={}
for topic,qs in Q.items():
    seen=set();cands=[];tries=[]
    for q in qs:
        cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+
              "&rows=15&select=title,DOI,type")
        for it in (cr.get("message") or {}).get("items") or []:
            doi=it.get("DOI")
            if not doi or doi in seen: continue
            seen.add(doi)
            if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
            a=ab(oa) or ""
            ttl=oa.get("title") or ""
            tries.append({"doi":doi,"title":ttl[:70],"abs_len":len(a),"type":oa.get("type")})
            if len(a)<300: continue
            cands.append({"doi":doi,"title":ttl,"year":oa.get("publication_year"),
              "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
              "type":oa.get("type"),"abs_len":len(a),"abstract":a,
              "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))})
        if len(cands)>=3: break
        time.sleep(1.5)
    cands.sort(key=lambda x:-(x.get("cited") or 0))
    res[topic]=cands
    detail[topic]=tries[:15]
    print(f"=== {topic}（{len(cands)} 个有摘要候选）",flush=True)
    for c in cands[:3]:
        print(f"   [{c['year']}] cite {c.get('cited')} | {c['title'][:64]}",flush=True)
    time.sleep(1.5)
json.dump(res,open(os.path.join(ROOT,"reports","round41_bridge.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(detail,open(os.path.join(ROOT,"reports","round41_bridge_detail.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有候选条目:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)