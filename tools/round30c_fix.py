# -*- coding: utf-8 -*-
"""第30轮修复：补缺失端点 + 年份格式。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
MET={"pop":"SP.POP.TOTL","urban":"SP.URB.TOTL.IN.ZS","life":"SP.DYN.LE00.IN","forest":"AG.LND.FRST.ZS"}
LAB={"pop":"总人口","urban":"城市化率","life":"预期寿命","forest":"森林覆盖率"}
NAM={"UZB":"乌兹别克斯坦","MNG":"蒙古","KAZ":"哈萨克斯坦"}
NEED=[("UZB","urban"),("MNG","pop"),("MNG","urban"),("KAZ","pop"),("KAZ","urban")]
for iso,mk in NEED:
    sid=f"wb-{iso.lower()}-{mk}"
    if sid in have: continue
    u=f"https://api.worldbank.org/v2/country/{iso}/indicator/{MET[mk]}?format=json&per_page=100&date=2015:2025"
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
    raw=p.stdout.decode("utf-8","ignore");b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip() or 0)
    val=yr=None
    try:
        d=json.loads(b);rows=[r for r in d[1] if r.get("value") is not None]
        if rows: L=max(rows,key=lambda r:int(r["date"]));val=L["value"];yr=L["date"]
    except Exception: pass
    sd["sources"].append({"id":sid,"title":f"World Bank API — {LAB[mk]} ({MET[mk]}, {NAM[iso]})",
      "author":"World Bank","year":None,"type":"数据端点","url":u,"url2":None,"link_ok":bool(code==200),
      "verified":bool(code==200),"page_title":f"World Bank API — {LAB[mk]} ({MET[mk]}, {NAM[iso]})",
      "note":f"JSON API {code}；国家 {iso}（{NAM[iso]}）＋指标 {MET[mk]}；最新值 {val}（{yr} 年）。"})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
n=0
for d in docs.values():
    for e in d["entries"]:
        tod=e.get("today") or ""
        if not tod: continue
        new=re.sub(r"(\d{4}) 年",r"\1年",tod)
        if new!=tod: e["today"]=new;e["last_update"]=TODAY;n+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("补端点",len(NEED),"；年份修正",n)