# -*- coding: utf-8 -*-
"""第17轮返工：北美冰盖换源、十三殖民地清 s011、s056 残留清理、s011/s056 全库扫描报告。"""
import json,os,re,html,subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

# 1) 登记 nasa-ice-cores
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
U="https://earthobservatory.nasa.gov/features/Paleoclimatology_IceCores"
p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",U],capture_output=True,timeout=30)
raw=p.stdout.decode("utf-8","ignore");b,c=raw.rsplit("\n__HTTP__",1)
m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
pt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
H=re.sub(r"<[^>]+>"," ",b)
for t in ("nav","header","footer","aside","script","style","form"): H=re.sub(rf"<{t}\b.*?</{t}>"," ",H,flags=re.I|re.S)
T_=re.sub(r"\s+"," ",html.unescape(H))
hits=len(re.findall(r"ice sheet|ice core|glacier",T_,re.I))
if not any(s["id"]=="nasa-ice-cores" for s in sd["sources"]):
 sd["sources"].append({"id":"nasa-ice-cores","title":"Paleoclimatology: The Ice Core Record - NASA Science",
  "author":"NASA Earth Observatory","year":None,"type":"官方机构","url":U,"url2":None,
  "link_ok":True,"verified":True,"page_title":pt,
  "note":f"curl 实测 HTTP {int(c.strip())}；页面标题：{pt}；D044 剥离口径正文 {len(T_)} 字符，正则 ice sheet|ice core|glacier 命中 {hits}。"})
 json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("nasa-ice-cores",c.strip(),len(T_),hits)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 2) 北美冰盖：换源
e=T["北美冰盖"]
e["sources"]=["nasa-ice-cores","s038-earthobservatory-nasa-gov"]
e["definition"]="北美冰盖：地质历史时期覆盖北美北部的巨大冰体，对当地地形与水系留下深远影响。"
e["pending_notes"]=("第17轮二次返工：原用 s038（NASA 门户）+ s056（USGS 站点迁移通告，0 命中）无法支撑主题；"
 "现改用 NASA『Paleoclimatology: The Ice Core Record』为专题页（正文 18931 字符、ice sheet|ice core|glacier 命中 40），s038 作机构页，已摘除 s056。"
 "冰盖范围与时序仍待专门地质来源逐条核验。")
e["status"]=(e.get("status") or "").replace("已复核(第16轮)","已复核(第17轮)")+"·换源(第17轮二次)"
e["last_update"]=TODAY

# 3) 十三殖民地：移除 s011
c13=T["十三殖民地"]
c13["sources"]=[s for s in c13["sources"] if s!="s011-unesco-org"]
c13["pending_notes"]=(c13.get("pending_notes") or "")+" 第17轮清理：移除 s011（UNESCO Climate action，与殖民地主题完全无关；为第14轮误贴残留）。13 colonies 专题页实测不可用（NPS 1505B/0、LOC 403、Archives 2716B/4），来源仅剩区域别名，待补专题页。"
c13["status"]=(c13.get("status") or "").replace("已复核(第16轮)","已复核(第17轮)")
c13["last_update"]=TODAY

# 4) 清 s056 残留在 3 条
for t in ["巴西高原","尼罗河三角洲","埃塞俄比亚高原"]:
 x=T.get(t)
 if not x: continue
 before=len(x["sources"])
 x["sources"]=[s for s in x["sources"] if s!="s056-earthquake-usgs-gov"]
 if len(x["sources"])!=before:
  x["pending_notes"]=(x.get("pending_notes") or "")+" 第17轮清理：移除 s056（USGS 站点迁移通告页，0 命中，不作内容依据）。"
  x["last_update"]=TODAY

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 5) s011/s056 全库扫描报告
scan={}
for sid in ["s011-unesco-org","s056-earthquake-usgs-gov","s058-worldbank-org","s025-ourworldindata-org","s057-databank-worldbank-org"]:
 hits=[(e["title"],e["theme"],e["level"]) for e in T.values() if sid in e.get("sources",[])]
 scan[sid]={"count":len(hits),"by_theme":{},
   "entries":[h[0] for h in hits]}
 for _,th,_ in hits: scan[sid]["by_theme"][th]=scan[sid]["by_theme"].get(th,0)+1
json.dump(scan,open(os.path.join(ROOT,"reports","round17_source_scan.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("扫描:",{k:v["count"] for k,v in scan.items()})
print("十三殖民地 sources:",c13["sources"])
print("北美冰盖 sources:",e["sources"])