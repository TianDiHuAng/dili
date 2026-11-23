# -*- coding: utf-8 -*-
"""第34轮第三批：放宽参数的 OpenAlex 检索。"""
import subprocess,json,os,urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"尼罗河三角洲":"Nile Delta Egypt sediment","阿拉伯征服北非":"Arab conquest Ifriqiya Maghrib",
"大津巴布韦":"Great Zimbabwe stone enclosures","古巴比伦":"Babylon city Mesopotamia",
"吠陀时代":"Vedic India Indo-Aryan","明清":"Ming Qing China trade silver",
"朝鲜半岛":"Korean peninsula geography","中南半岛":"mainland Southeast Asia peninsula",
"湄公河三角洲":"Mekong Delta Vietnam","吴哥":"Angkor Khmer Cambodia",
"马来群岛":"Malay Archipelago Southeast Asia","匈奴":"Xiongnu empire Han",
"突厥":"Turkic khaganate steppe","黎凡特":"Levant region Syria Palestine",
"安纳托利亚":"Anatolia plateau Turkey","东亚季风":"East Asian summer monsoon",
"伊比利亚半岛":"Iberian Peninsula Spain Portugal","莫斯科公国":"Muscovy Russia state",
"巴尔干半岛":"Balkans peninsula Southeast Europe","斯堪的纳维亚":"Scandinavian peninsula Nordic",
"欧洲温带海洋性气候":"oceanic climate Western Europe","中世纪欧洲庄园农业":"manor medieval agrarian Europe",
"墨西哥湾":"Gulf of Mexico coastal","北美原住民":"indigenous peoples North America",
"美国西进":"westward expansion United States frontier","加勒比海群岛":"Caribbean archipelago islands",
"巴西高原":"Brazilian Highlands plateau","马丘比丘":"Machu Picchu Peru Inca citadel",
"巴西殖民经济":"colonial Brazil plantation economy","大自流盆地":"Great Artesian Basin groundwater Australia",
"新西兰北岛":"North Island New Zealand volcanic","大堡礁":"Great Barrier Reef Australia",
"澳大利亚混合农业":"Australian agriculture wheat sheep zone","冲积平原":"alluvial plains rivers",
"山地农业":"mountain agriculture highland farming",
}
CORE={t:[w for w in q.lower().split() if len(w)>3] for t,q in Q.items()}
def get(u):
    return subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",u],
                          capture_output=True,timeout=40).stdout.decode("utf-8","ignore")
def ab_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,q in Q.items():
    u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+
       "&per_page=25&mailto=geo-encyclopedia@example.com")
    try: d=json.loads(get(u))
    except Exception: res[t]=None;print(f"-- {t}");continue
    best=None
    for w in d.get("results",[]):
        a=ab_of(w)
        if not a or len(a)<250: continue
        ti=(w.get("title") or "").lower()
        need=CORE.get(t,[])
        if need and not any(k in ti for k in need): continue
        cand={"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
          "year":w.get("publication_year"),"doi":w.get("doi"),"cited":w.get("cited_by_count"),
          "abstract":a,"host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (cand.get("cited") or 0)>(best.get("cited") or 0): best=cand
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<14} {(best['title'][:54] if best else '-')} ({best.get('year') if best else ''})")
json.dump(res,open(os.path.join(ROOT,"reports","round34_final3.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q))