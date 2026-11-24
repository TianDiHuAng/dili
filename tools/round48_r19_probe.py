# -*- coding: utf-8 -*-
"""第48轮：实现 R19 的自洽性检验原型——检测「离群来源」（标题与同条其他来源无共同实词）。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
STOP=set("""a an the of in on at to for and or with from by as is are was were be been being
this that these those its their his her our your my it we they he she them us you i
new old first last early late history historical study studies review analysis
case evidence toward towards between among during after before under over
vol no pp eds ed university press journal science sciences research
proceedings transactions international national american european""".split())
def words(t):
    t=re.sub(r"[^A-Za-z ]"," ",(t or "").lower())
    return {w for w in t.split() if len(w)>2 and w not in STOP}
def content_src(e):
    out=[]
    for sid in e["sources"]:
        if not sid.startswith("openalex-"): continue
        s=S.get(sid) or {}
        out.append((sid,s.get("title") or ""))
    return out
suspects=[]
for t,e in T.items():
    srcs=content_src(e)
    if len(srcs)<2: continue
    ws=[words(ti) for _,ti in srcs]
    # 出现在 ≥ceil(n/2) 个来源标题中的词 = 该条目的「共识对象词」
    from collections import Counter
    cnt=Counter()
    for w in ws: cnt.update(w)
    need=max(1,(len(ws)+1)//2)
    consensus={w for w,c in cnt.items() if c>=need}
    if not consensus: continue
    for (sid,ti),wset in zip(srcs,ws):
        if not (wset & consensus):
            suspects.append((t,sid,ti[:70],sorted(list(consensus))[:6]))
print(f"检出离群来源: {len(suspects)}")
for s in suspects:
    print(f"  {s[0]:<14} {s[1]:<22} 标题「{s[2]}」")
    print(f"      同条共识词: {s[3]}")
json.dump({"round":48,"method":"R19原型：同条 openalex 来源标题的词集交集（出现于≥半数标题的实词为共识对象词）；不含任何共识词的来源判为离群",
 "suspects":[{"entry":a,"sid":b,"title":c,"consensus":d} for a,b,c,d in suspects]},
 open(os.path.join(ROOT,"reports","round48_r19_probe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)