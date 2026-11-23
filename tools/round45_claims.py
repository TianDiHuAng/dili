# -*- coding: utf-8 -*-
"""第45轮 B1（D100 顺序）：按正文待支撑句的关键词检索，并逐条核对摘要是否支撑该句。"""
import subprocess,json,os,urllib.parse,time,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (条目, 待支撑句的中文要点, 检索词, 摘要须出现的关键词组)
TARGET={
"马里帝国":("控制跨撒哈拉黄金与盐贸易是帝国财富与权力的重要来源",
  "trans-Saharan gold trade Mali empire","gold","trans-saharan"),
"日本列岛":("位于板块交界附近，地震与火山活动频繁",
  "Japan subduction zone volcanism seismicity","subduction","volcan"),
"古希腊城邦":("山地分割与海上通道并存",
  "Greek landscape mountains sea city-state","greek","landscape"),
"罗马共和国":("台伯河畔的拉丁姆平原提供农业与交通基础",
  "Tiber river Rome Latium settlement","tiber","latium"),
"文艺复兴意大利":("城邦竞争、商业财富与城市赞助为艺术与学术提供条件",
  "Italian Renaissance city-state patronage economy","renaissance","patronage"),
"白令陆桥":("冰期海平面下降时出露为连接亚洲与北美的宽阔陆地",
  "Beringia sea level lowstand land bridge","beringia","sea level"),
"安第斯山脉":("海拔差异形成垂直气候带",
  "Andean vertical climate zones altitudinal","andean","altitudinal"),
"克里特文明":("海上贸易与宫殿再分配体系相互支撑",
  "Minoan palace economy redistribution","minoan","palace"),
"五大湖":("季节水位变化是重要水文特征",
  "Great Lakes water level variability","great lakes","water level"),
"洋流":("由风、密度差与地转偏向力驱动",
  "ocean circulation wind stress density Coriolis","circulation","wind"),
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
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t in TARGET:
    claim,q,k1,k2=TARGET[t]
    best=None;seen=set();notes=[]
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<400: continue
        al=a.lower()
        # D100：摘要须同时命中两个关键词组（即支撑该具体断言）
        if k1.lower() not in al or k2.lower() not in al: continue
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,"claim":claim,
             "k1":k1,"k2":k2,"host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=14: break
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<12} {(best['title'][:46] if best else '-')} ({best.get('year') if best else ''})",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round45_claims.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n按断言匹配成功:",sum(1 for v in res.values() if v),"/",len(TARGET),flush=True)