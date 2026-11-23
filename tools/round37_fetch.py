# -*- coding: utf-8 -*-
"""第37轮 B1：历史/区域类补充条目的 OpenAlex 检索（带退避）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"古埃及中王国":[("Middle Kingdom Egypt","middle kingdom"),("Middle Kingdom ancient Egypt state","egypt")],
"法蒂玛王朝":[("Fatimid caliphate","fatimid"),("Fatimid state Egypt","fatimid")],
"赫梯王国":[("Hittite empire Anatolia","hittite"),("Hittite kingdom","hittite")],
"贵霜帝国":[("Kushan empire","kushan"),("Kushan Central Asia","kushan")],
"仰韶文化":[("Yangshao culture Neolithic China","yangshao"),("Yangshao","yangshao")],
"室利佛逝":[("Srivijaya maritime empire","srivijaya"),("Srivijaya Southeast Asia","srivijaya")],
"满者伯夷":[("Majapahit empire Java","majapahit"),("Majapahit","majapahit")],
"帖木儿帝国":[("Timurid empire","timurid"),("Timurid Central Asia","timur")],
"迈锡尼文明":[("Mycenaean civilization","mycenaean"),("Mycenaean Greece","mycenaean")],
"神圣罗马帝国":[("Holy Roman Empire","holy roman empire"),("Holy Roman Empire constitution","holy roman")],
"汉萨同盟":[("Hanseatic League trade","hanseatic"),("Hanseatic League Baltic","hanseatic")],
"基辅罗斯":[("Kyivan Rus medieval","rus"),("Kievan Rus state","kievan")],
"新法兰西":[("New France colonial North America","new france"),("New France","france")],
"查文文化":[("Chavin culture Andes","chavin"),("Chavin de Huantar","chavin")],
"纳斯卡文化":[("Nazca culture Peru","nazca"),("Nazca lines","nazca")],
"奇穆帝国":[("Chimu empire Peru","chimu"),("Chimu state","chimu")],
"非洲大湖地区":[("African Great Lakes region","great lakes"),("East African Great Lakes","great lakes")],
"西北海岸":[("Northwest Coast Pacific indigenous","northwest coast"),("Northwest Coast archaeology","northwest")],
"古巴岛":[("Cuba island geography","cuba"),("Cuba Caribbean island","cuba")],
"南锥体":[("Southern Cone South America","southern cone"),("Southern Cone geography","cone")],
"美拉尼西亚":[("Melanesia Pacific","melanesia"),("Melanesian islands","melanesia")],
"密克罗尼西亚":[("Micronesia Pacific islands","micronesia"),("Micronesia","micronesia")],
"复活节岛":[("Easter Island Rapa Nui","easter island"),("Rapa Nui","rapa nui")],
"太平洋殖民航线":[("Pacific colonization voyaging","pacific"),("Polynesian voyaging","voyaging")],
"南美贸易网络":[("South America trade network prehispanic","trade"),("Andean trade network","andean")],
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
    print(f"{'OK' if best else '--'} {t:<14} {(best['title'][:52] if best else '-')} ({best.get('year') if best else ''})")
    time.sleep(3)
json.dump(res,open(os.path.join(ROOT,"reports","round37_openalex.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q))