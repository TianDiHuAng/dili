# -*- coding: utf-8 -*-
"""第38轮 B1：16 条历史/区域类 + 6 条方法论类 OpenAlex 检索。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"法蒂玛王朝":[("Fatimid caliphate Egypt","fatimid"),("Fatimid","fatimid")],
"非洲大湖地区":[("African Great Lakes region","great lakes"),("East African Great Lakes","great lakes")],
"赫梯王国":[("Hittite empire","hittite"),("Hittite state Anatolia","hittite")],
"仰韶文化":[("Yangshao Neolithic China","yangshao"),("Yangshao culture","yangshao")],
"西北海岸":[("Northwest Coast indigenous","northwest coast"),("Northwest Coast archaeology","northwest")],
"新法兰西":[("New France colony","new france"),("New France North America","france")],
"古巴岛":[("Cuba island","cuba"),("Cuba geography","cuba")],
"巴塔哥尼亚":[("Patagonia geography","patagonia"),("Patagonia","patagonia")],
"的的喀喀湖":[("Lake Titicaca","titicaca"),("Titicaca basin","titicaca")],
"查文文化":[("Chavin culture","chavin"),("Chavin","chavin")],
"纳斯卡文化":[("Nazca culture","nazca"),("Nazca","nazca")],
"奇穆帝国":[("Chimu empire","chimu"),("Chimu","chimu")],
"南美贸易网络":[("Andean trade prehispanic","andean"),("South American trade network","trade")],
"南锥体":[("Southern Cone South America","southern cone"),("Southern Cone","cone")],
"玛雅研究新进展":[("Maya archaeology advances","maya"),("Maya civilization research","maya")],
"欧洲冰期地貌":[("European glacial landforms Pleistocene","glacial"),("glacial geomorphology Europe","glacial")],
"地图投影":[("map projection cartography","projection"),("map projection distortion","projection")],
"争议边界处理原则":[("boundary dispute cartography","boundary"),("territorial dispute mapping","boundary")],
"地理空间数据产品":[("geospatial data products","geospatial"),("geospatial data infrastructure","geospatial")],
"地球系统科学":[("Earth system science","earth system"),("Earth system science framework","earth system")],
"环境数据访问":[("environmental data access open","environmental data"),("open environmental data","data")],
"人文地理学":[("human geography discipline","human geography"),("human geography theory","human geography")],
}
def get(u):
    for _ in range(4):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=40)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: time.sleep(4);continue
            b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip() or 0)
            if code==200: return b
            time.sleep(6)
        except Exception: time.sleep(4)
    return "{}"
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,pairs in Q.items():
    best=None
    for q,needle in pairs:
        u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=12&mailto=geo-encyclopedia@example.com")
        try: d=json.loads(get(u))
        except Exception: d={}
        for w in d.get("results",[]):
            a=ab(w)
            if not a or len(a)<300: continue
            ti=(w.get("title") or "").lower()
            if needle not in ti: continue
            if w.get("type") in ("book-review","paratext","editorial","letter","erratum"): continue
            cand={"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),"year":w.get("publication_year"),
              "doi":w.get("doi"),"cited":w.get("cited_by_count"),"type":w.get("type"),"abstract":a,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            if best is None or (cand.get("cited") or 0)>(best.get("cited") or 0): best=cand
        if best: break
        time.sleep(3)
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<16} {(best['title'][:50] if best else '-')} ({best.get('year') if best else ''})",flush=True)
    time.sleep(2.5)
json.dump(res,open(os.path.join(ROOT,"reports","round38_openalex.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)