# -*- coding: utf-8 -*-
"""第43轮续：为 37 条 0 源核心/重要条目检索学术来源（摘要多次命中筛选，避免地名碰撞）。"""
import subprocess,json,os,urllib.parse,time,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"尼罗河谷":("Nile Valley Egypt predynastic","nile valley"),
"刚果盆地":("Congo Basin rainforest peatland","congo basin"),
"迦太基":("Carthage Punic city","carthage"),
"马里帝国":("Mali empire West African","mali empire"),
"阿契美尼德波斯":("Achaemenid empire Persia","achaemenid"),
"黄河流域":("Yellow River basin China sediment","yellow river"),
"日本列岛":("Japanese archipelago tectonics","japanese archipelago"),
"古希腊城邦":("Greek polis city-state","polis"),
"罗马共和国":("Roman Republic politics","roman republic"),
"不列颠群岛":("British Isles geology","british isles"),
"白令陆桥":("Beringia land bridge Pleistocene","beringia"),
"密西西比河":("Mississippi River basin","mississippi river"),
"中美洲地峡":("Central America isthmus geology","isthmus"),
"安第斯山脉":("Andean cordillera uplift","andean"),
"亚马逊盆地":("Amazon basin rainforest hydrology","amazon basin"),
"亚马逊河":("Amazon River hydrology","amazon river"),
"澳大利亚原住民":("Aboriginal Australians land management","aboriginal"),
"南极冰盖":("Antarctic ice sheet mass balance","antarctic ice sheet"),
"板块构造":("plate tectonics theory","plate tectonics"),
"河流三角洲":("river delta morphology sediment","river delta"),
"游牧":("pastoral nomadism steppe","nomad"),
"萨赫勒带":("Sahel rainfall variability","sahel"),
"北美冰盖":("Laurentide ice sheet","laurentide"),
"五大湖":("Great Lakes North America","great lakes"),
"科罗拉多高原":("Colorado Plateau geology","colorado plateau"),
"格陵兰岛":("Greenland ice sheet","greenland"),
"十三殖民地":("Thirteen Colonies British North America","thirteen colonies"),
"大分水岭":("Great Dividing Range Australia","great dividing"),
"南极条约体系":("Antarctic Treaty System governance","antarctic treaty"),
"冰芯气候记录":("ice core paleoclimate record","ice core"),
"洋流":("ocean circulation currents","ocean circulation"),
"人口迁移":("migration geography patterns","migration"),
"植物物候变化":("plant phenology climate change","phenology"),
"北极火情变化":("Arctic fire regime tundra","arctic fire"),
"地理信息系统":("geographic information systems","gis"),
"人口地理":("population geography distribution","population geography"),
"城市地理":("urban geography city structure","urban geography"),
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
for title,(q,needle) in Q.items():
    best=None;seen=set()
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=15&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<300: continue
        ti=(oa.get("title") or "").lower(); al=a.lower()
        # 改进筛选：标题含对象词 且 摘要中出现对象词 ≥2 次
        if needle not in ti: continue
        if al.count(needle)<2: continue
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,"hits":al.count(needle),
             "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=8: break
    res[title]=best
    print(f"{'OK' if best else '--'} {title:<14} {(best['title'][:48] if best else '-')} ({best.get('year') if best else ''}) hits={best['hits'] if best else 0}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round43_zerosrc.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有候选:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)