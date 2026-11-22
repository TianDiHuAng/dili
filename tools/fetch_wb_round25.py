# -*- coding: utf-8 -*-
"""第25轮：从世界银行 API 取带年份的现状数值（JSON，可复核）。"""
import subprocess,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE="https://api.worldbank.org/v2"
IND={
 "urban_pct":"SP.URB.TOTL.IN.ZS",
 "pop_total":"SP.POP.TOTL",
 "life_exp":"SP.DYN.LE00.IN",
 "forest_pct":"AG.LND.FRST.ZS",
 "agri_pct_gdp":"NV.AGR.TOTL.ZS",
}
COUNTRIES=["CHN","IND","NGA","BRA","USA","EGY","IDN","MEX"]
def fetch(c,ind):
    u=f"{BASE}/country/{c}/indicator/{ind}?format=json&per_page=100&date=2015:2025"
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25",u],capture_output=True,timeout=35)
    try:
        d=json.loads(p.stdout.decode("utf-8","ignore"))
        if not isinstance(d,list) or len(d)<2: return None
        rows=[r for r in d[1] if r.get("value") is not None]
        if not rows: return None
        latest=max(rows,key=lambda r:int(r["date"]))
        return {"value":latest["value"],"year":latest["date"],"country":latest["country"]["value"]}
    except Exception:
        return None
out={}
for c in COUNTRIES:
    out[c]={}
    for k,ind in IND.items():
        r=fetch(c,ind)
        if r: out[c][k]=r
        print(f"{c} {k}: {r['year'] if r else '-'} {r['value'] if r else '-'}")
json.dump(out,open(os.path.join(ROOT,"reports","round25_wb_data.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("样本数",len(out))