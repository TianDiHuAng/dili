# -*- coding: utf-8 -*-
"""第23轮返工：实测 9 条复核条目的来源，生成逐条实证备注；修正 3 处矛盾与徽标。"""
import json,os,re,html,subprocess
from concurrent.futures import ThreadPoolExecutor
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
src={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

TARGETS={
 "夏威夷群岛":("hawaii|island",),
 "大堡礁":("reef|coral",),
 "澳大利亚内陆干旱气候":("arid|dry|drought",),
 "澳大利亚混合农业":("farm|agricultur|wheat",),
 "南极半岛":("peninsula|antarctic",),
 "松岛冰川退缩":("glacier|pine island|retreat",),
 "冲积平原":("alluvial|floodplain|sediment",),
 "山地农业":("mountain|terrace|slope",),
 "城市起源":("city|urban|settlement",),
}
def strip(h):
    for t in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{t}\b.*?</{t}>"," ",h,flags=re.I|re.S)
    return h
def measure(args):
    sid,rx=args
    s=src.get(sid)
    if not s: return sid,0,None,0,0
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",s["url"]],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return sid,0,s["url"],0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",strip(b)))).strip()
        return sid,int(c.strip() or 0),s.get("page_title"),len(txt),len(re.findall(rx,txt,re.I))
    except Exception:
        return sid,0,s.get("url"),0,0

jobs=[]
for t,(rx,) in TARGETS.items():
    for sid in T[t]["sources"]: jobs.append((sid,rx))
res={}
with ThreadPoolExecutor(max_workers=10) as ex:
    for sid,code,title,n,h in ex.map(measure,jobs):
        res[sid]=(code,n,h)
print("测量结果:")
for sid,(c,n,h) in res.items(): print(f"  {sid}: {c} body={n} hits={h}")
json.dump(res,open(os.path.join(ROOT,"reports","round23_measure.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)