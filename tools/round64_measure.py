# -*- coding: utf-8 -*-
"""第64轮：实测补充类条目涉及的机构页字符数（补齐 D104 之后的测量缺口）。"""
import json,os,re,sys,subprocess,html as H,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}
TARGET=["s004-population-un-org","s008-unesco-org","s014-fao-org","s085-unesco-org","s072-cbd-int",
 "s021-fao-org","s074-unicef-org","s050-oceanservice-noaa-gov","s091-iucn-org","s059-worldbank-org",
 "s078-ourworldindata-org","s081-ourworldindata-org","s023-ourworldindata-org","s032-ourworldindata-org",
 "s033-ourworldindata-org","s019-fao-org","s037-science-nasa-gov","s054-ncei-noaa-gov","s064-worldbank-org",
 "s065-worldbank-org","s066-worldbank-org","s067-worldbank-org","s068-worldbank-org","s010-unesco-org"]
def strip_tags(h):
    for x in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{x}\b.*?</{x}>"," ",h,flags=re.I|re.S)
    return h
def measure(url):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",
          "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return 0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        txt=re.sub(r"\s+"," ",H.unescape(re.sub(r"<[^>]+>"," ",strip_tags(b)))).strip()
        return int(c.strip() or 0),len(txt)
    except Exception: return 0,0
done=0
for sid in TARGET:
    s=S.get(sid)
    if not s or not s.get("url"): continue
    if "第64轮实测" in (s.get("note") or ""):
        continue
    code,n=measure(s["url"])
    if code!=200 or n==0:
        print(f"  跳过 {sid}: HTTP {code} 正文 {n}")
        time.sleep(1.2); continue
    s["note"]=(s.get("note") or "")+f" 【第64轮实测】strip 后正文 {n:,} 字符（HTTP {code}）。"
    print(f"  {sid:<30} HTTP {code} 正文 {n:>7} 字符")
    done+=1
    time.sleep(0.8)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("实测完成:",done,"条")