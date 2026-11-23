# -*- coding: utf-8 -*-
"""第43轮 B1：对已登记的多源条目逐条做「对象同一」复核（取各源摘要并检索对象词）。"""
import subprocess,json,os,time,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
SHELL={"britannica-regions","wikipedia-regions","un-m49","s010-unesco-org","s070-cbd-int","s071-cbd-int","ap-human-geo","s013-fao-org"}
docs={u:json.load(open(os.path.join(ROOT,"data",u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
sd={s["id"]:s for s in json.load(open(os.path.join(ROOT,"data","sources.json"),encoding="utf-8"))["sources"]}

# 待复核：≥2 内容源（剔 wikidata）的条目
TARGET=[]
for t,e in T.items():
    cs=[s for s in e["sources"] if s not in SHELL and not s.startswith("wb-") and not s.startswith("wikidata-")]
    if len(cs)>=2: TARGET.append((t,cs))
print("待复核条目:",len(TARGET),flush=True)

def get(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",url],capture_output=True,timeout=30)
            s=p.stdout.decode("utf-8","ignore")
            if s.strip().startswith("{"): return json.loads(s)
            time.sleep(2)
        except Exception: time.sleep(2)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))

out={}
for t,cs in TARGET:
    rows=[]
    for sid in cs:
        if sid.startswith("openalex-"):
            oid=sid.replace("openalex-","")
            w=get(f"https://api.openalex.org/works/{oid}?select=title,publication_year,abstract_inverted_index,type")
            rows.append({"sid":sid,"title":w.get("title"),"year":w.get("publication_year"),
                         "type":w.get("type"),"abs":ab(w)})
            time.sleep(1.2)
        else:
            rows.append({"sid":sid,"title":(sd.get(sid) or {}).get("title"),"year":None,"type":"非openalex","abs":""})
    out[t]=rows
    print(f"  {t}: {len(rows)} 源",flush=True)
json.dump(out,open(os.path.join(ROOT,"reports","round43_review.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n完成",len(out),"条",flush=True)