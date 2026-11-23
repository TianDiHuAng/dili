# -*- coding: utf-8 -*-
"""第35轮 B1：带退避重试的 OpenAlex 检索（处理剩余重要 L1）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(ROOT,"data",u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
LEFT=[t for t,e in T.items() if e["tier"]=="重要" and e["level"]=="L1"]
print("剩余重要L1:",len(LEFT))

Q={
"阿拉伯征服北非":[("Arab conquest North Africa","arab"),("Islamic conquest Maghrib","conquest")],
"大津巴布韦":[("Great Zimbabwe archaeology","zimbabwe"),("Great Zimbabwe stone walls trade","great zimbabwe")],
"古巴比伦":[("Babylonia ancient Near East","babylon"),("Babylon city Hammurabi","babylon")],
"吠陀时代":[("Vedic period India society","vedic"),("Rigvedic society early India","vedic")],
"明清":[("Ming Qing China economy","ming"),("late imperial China trade","qing")],
"朝鲜半岛":[("Korean Peninsula geography","korean"),("Korea peninsula physical geography","korea")],
"中南半岛":[("Indochina peninsula geography","indochina"),("Southeast Asia mainland geography","southeast asia")],
"吴哥":[("Angkor Khmer hydraulic city","angkor"),("Angkor water management","angkor")],
"马来群岛":[("Malay Archipelago biogeography","malay"),("Malay Archipelago maritime trade","archipelago")],
"匈奴":[("Xiongnu steppe empire","xiongnu"),("Xiongnu archaeology Mongolia","xiongnu")],
"突厥":[("Turkic Khaganate Central Asia","turkic"),("Göktürk empire steppe","khaganate")],
"黎凡特":[("Levant geography climate Holocene","levant"),("Levant region archaeology","levant")],
"安纳托利亚":[("Anatolia plateau climate history","anatolia"),("Anatolian peninsula geography","anatolia")],
"莫斯科公国":[("Muscovy rise Russian state","muscovy"),("Grand Duchy of Moscow","moscow")],
"巴尔干半岛":[("Balkan Peninsula geography","balkan"),("Balkans physical geography","balkans")],
"斯堪的纳维亚":[("Scandinavian Peninsula geography","scandinavia"),("Scandinavia glaciation landforms","scandinavia")],
"欧洲温带海洋性气候":[("Western Europe oceanic climate","oceanic climate"),("temperate maritime climate Europe","temperate")],
"中世纪欧洲庄园农业":[("medieval manor economy Europe","manor"),("open field system medieval agriculture","medieval agriculture")],
"墨西哥湾":[("Gulf of Mexico oceanography","gulf of mexico"),("Gulf of Mexico coastal ecology","gulf of mexico")],
"北美原住民":[("peopling of the Americas","americas"),("Native American settlement archaeology","native american")],
"美国西进":[("American westward expansion","westward"),("US frontier settlement history","frontier")],
"加勒比海群岛":[("Caribbean archipelago geography","caribbean"),("Caribbean islands colonial","caribbean")],
"巴西高原":[("Brazilian Highlands geology","brazilian highlands"),("Brazil plateau geomorphology","brazil")],
"马丘比丘":[("Machu Picchu Inca","machu picchu"),("Machu Picchu archaeology","machu picchu")],
"巴西殖民经济":[("colonial Brazil sugar economy","brazil"),("Brazil colonial society","brazil")],
"大自流盆地":[("Great Artesian Basin groundwater","artesian"),("Great Artesian Basin Australia","artesian")],
"新西兰北岛":[("North Island New Zealand volcanism","north island"),("North Island New Zealand geology","north island")],
"大堡礁":[("Great Barrier Reef ecology","great barrier reef"),("Great Barrier Reef bleaching","barrier reef")],
"澳大利亚混合农业":[("Australian wheat sheep zone","australia"),("mixed farming Australia","mixed farming")],
"冲积平原":[("alluvial plain formation","alluvial"),("floodplain alluvial deposits","floodplain")],
"山地农业":[("mountain agriculture terracing","mountain agriculture"),("highland agriculture Andes terrace","terrace")],
}
def get(u):
    for _ in range(4):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=40)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: time.sleep(5);continue
            b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
            if code==200: return b
            time.sleep(6)
        except Exception: time.sleep(5)
    return "{}"
def ab_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,pairs in Q.items():
    best=None
    for q,needle in pairs:
        u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+
           "&per_page=15&mailto=geo-encyclopedia@example.com")
        try: d=json.loads(get(u))
        except Exception: d={}
        for w in d.get("results",[]):
            a=ab_of(w)
            if not a or len(a)<250: continue
            ti=(w.get("title") or "").lower()
            if needle not in ti: continue
            cand={"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"doi":w.get("doi"),"cited":w.get("cited_by_count"),
              "type":w.get("type"),"abstract":a,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            if cand.get("type")=="book-review": continue
            if best is None or (cand.get("cited") or 0)>(best.get("cited") or 0): best=cand
        if best: break
        time.sleep(4)
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<14} {(best['title'][:52] if best else '-')} ({best.get('year') if best else ''})")
    time.sleep(3)
json.dump(res,open(os.path.join(ROOT,"reports","round35_openalex.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q))