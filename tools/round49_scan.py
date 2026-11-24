# -*- coding: utf-8 -*-
"""第49轮：导出所有含 openalex 来源的条目及其来源标题，供对象同一性人工扫描。"""
import json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
rows=[]
for t,e in T.items():
    srcs=[]
    for sid in e["sources"]:
        if not sid.startswith("openalex-"): continue
        s=S.get(sid) or {}
        srcs.append({"sid":sid,"title":s.get("title") or "","year":s.get("year")})
    if srcs: rows.append({"entry":t,"tier":e["tier"],"sources":srcs})
rows.sort(key=lambda r:({"核心":0,"重要":1}.get(r["tier"],2),r["entry"]))
json.dump(rows,open(os.path.join(ROOT,"reports","round49_titles.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("含学术来源条目:",len(rows))
for r in rows[:70]:
    print(f"\n== {r['entry']} [{r['tier']}]")
    for s in r["sources"]:
        print(f"   [{s['year']}] {s['title'][:78]}")