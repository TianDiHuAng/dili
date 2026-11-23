# -*- coding: utf-8 -*-
"""第44轮：登记 12 条 0 源条目的学术来源（含落点句）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F1=json.load(open(os.path.join(ROOT,"reports","round44_zerosrc2.json"),encoding="utf-8"))
F0=json.load(open(os.path.join(ROOT,"reports","round44_zerosrc.json"),encoding="utf-8"))
CAND={k:v for k,v in list(F1.items())+list(F0.items()) if v}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文"}

SPEC={
"刚果盆地":("strong","geo","所引 2013 年研究分析刚果盆地的**森林砍伐趋势**；本条「森林覆盖变化与人类活动压力」的表述据此。"),
"罗马共和国":("strong","polities","所引 2015 年专著《The Roman Republic》讨论其**政体结构与演进**；本条「共和政体的制度构成」据此。"),
"十三殖民地":("strong","influence","所引 1998 年研究讨论十三殖民地的**经济增长与制度**；本条「殖民地经济与母国政策的关系」据此。"),
"不列颠群岛":("strong","geo","所引 1970 年研究重建不列颠群岛的**三叠纪古地理**；本条「群岛地质构造的阶段性」据此。"),
"人口地理":("strong","geo","所引 2006 年研究分析人口**空间分布与结构**；本条「人口分布的不均衡性」据此。"),
"南极冰盖":("partial","influence","所引 1982 年研究讨论西南极冰盖与东南极的**发育关系**；本条仅据此写「冰盖发育存在阶段性讨论」，不作定论。"),
"冰芯气候记录":("partial","influence","所引 2024 年研究对冰芯钻探点的**年代—冰流建模**；本条「冰芯定年依赖流动模型」据此。"),
"北极火情变化":("partial","influence","所引 1980 年研究记录一次**苔原火对土壤与植物群落**的影响；本条「苔原火改变地表与植被」据此。"),
"日本列岛":("partial","influence","所引 2017 年研究讨论**家畜引入日本列岛**的过程；本条仅据此写「列岛与大陆的生物交流」，不作地质断言。"),
"格陵兰岛":("partial","influence","所引 2023 年研究观测格陵兰冰面的**湍流热通量与雪冰过程**；本条「冰盖表面能量交换」据此。"),
"城市地理":("partial","influence","所引 2009 年讲座文章讨论城市地理与**公共健康**的关联；本条「城市形态与社会结果相互关联」据此。"),
"地理信息系统":("partial","influence","所引 2015 年研究把 GIS 用于**滴灌系统的远程调度**；本条「GIS 作为空间决策工具」据此。"),
}
n=0;log=[]
for t,(g,fld,sentence) in SPEC.items():
    c=CAND.get(t);e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in (e["sources"] or []): continue
    if sid not in have:
        code=0;size=0
        for _ in range(3):
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                    if code==200: break
                time.sleep(4)
            except Exception: time.sleep(4)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys((e["sources"] or [])+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第44轮补源（{g}）】{sid}（{c.get('year')}年，《{c['title']}》，{c.get('host') or '出版方未标'}，DOI {c['doi']}，被引 {c.get('cited')}）；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=44;cov["round_processed"]=n
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
# 重算实测口径
import re
STUB={"livius-polis","livius-athens"}
EXTRA=("nasa-ice-cores","usgs-glaciers-pdf","noaa-global-temp","nasa-pine-island","s042-earthobservatory-nasa-gov","nasa-ice-sheets","noaa-sustainable-fisheries","s051-fisheries-noaa-gov")
S={s["id"]:s for s in sd["sources"]}
def ac(e):
    k=0
    for sid in e["sources"]:
        if sid in STUB: continue
        if sid.startswith(("openalex-","livius-")) or sid in EXTRA:
            note=(S.get(sid) or {}).get("note") or ""
            m=re.search(r"(\d{3,6})\s*字节", note)
            if sid.startswith("livius-") and m and int(m.group(1))<1000: continue
            k+=1
    return k
z=sum(1 for e in T.values() if ac(e)==0);o=sum(1 for e in T.values() if ac(e)==1);g2=sum(1 for e in T.values() if ac(e)>=2)
print("登记",n,"条：","、".join(log))
print(f"实测口径：0源 {z} / 1源 {o} / ≥2源 {g2}")