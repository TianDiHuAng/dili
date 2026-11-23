# -*- coding: utf-8 -*-
"""第42轮 B1：为核心/重要单源条目寻找第二篇独立文献（DOI 桥，排除已有）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
SHELL={"britannica-regions","wikipedia-regions","un-m49","s010-unesco-org","s070-cbd-int","s071-cbd-int","ap-human-geo","s013-fao-org"}
docs={u:json.load(open(os.path.join(ROOT,"data",u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
# 核心 + 重要单源（含 0 源）
TARGETS=[]
for t,e in T.items():
    if e["level"]!="L2" or e["tier"] not in ("核心","重要"): continue
    content=[s for s in e["sources"] if s not in SHELL and not s.startswith("wb-")]
    if len(content)<=1: TARGETS.append((t,e["tier"],content))

Q={
"撒哈拉沙漠":["Sahara desert climate history","Sahara aridification"],
"东非大裂谷":["East African Rift System geology","East African Rift evolution"],
"两河流域":["Mesopotamia rivers irrigation history","Tigris Euphrates plain"],
"马里帝国":["Mali empire West Africa history","Mali empire Sundiata"],
"爱琴海世界":["Aegean Bronze Age world","Aegean sea archaeology Bronze"],
"罗马帝国":["Roman Empire economy geography","Roman Empire provinces"],
"文艺复兴意大利":["Italian Renaissance cities economy","Renaissance Italy urban"],
"白令陆桥":["Bering Land Bridge","Beringia Pleistocene"],
"大平原":["Great Plains North America grassland","Great Plains physiography"],
"玛雅文明":["Maya civilization Classic period","Maya lowlands society"],
"安第斯山脉":["Andes mountain range geology","Andean cordillera uplift"],
"印加帝国":["Inca empire Andes state","Inca administration"],
"澳大利亚大陆":["Australia continent geology","Australian landforms"],
"澳大利亚原住民":["Australian Aboriginal archaeology","Aboriginal Australia settlement"],
"波利尼西亚":["Polynesia Pacific settlement","Polynesian societies"],
"南极大陆":["Antarctica continent ice sheet","Antarctic continent geology"],
"季风系统":["monsoon system dynamics","global monsoon circulation"],
"气候带":["climate zones classification","Koppen climate classification"],
"河流三角洲":["river delta formation","delta morphology sediment"],
"青藏高原":["Tibetan Plateau uplift","Tibetan Plateau climate"],
"丝绸之路":["Silk Road trade networks","Silk Road history exchange"],
"城市起源":["urban revolution first cities","origin of cities Mesopotamia"],
"克里特文明":["Minoan Crete civilization","Crete Bronze Age"],
"维京时代":["Viking Age Scandinavia","Viking expansion"],
"落基山脉":["Rocky Mountains geology","Rocky Mountain orogeny"],
"奥尔梅克":["Olmec Mesoamerica","Olmec civilization"],
"十三殖民地":["Thirteen Colonies British America","colonial America settlement"],
"拉普拉塔平原":["La Plata basin pampas","Rio de la Plata region"],
"阿塔卡马沙漠":["Atacama Desert hyperarid","Atacama climate"],
"大分水岭":["Great Dividing Range Australia","Great Dividing Range geology"],
"毛利人":["Maori New Zealand","Maori settlement Aotearoa"],
"斯瓦希里海岸":["Swahili coast trade","Swahili city-states"],
"埃塞俄比亚高原":["Ethiopian Highlands geology","Ethiopian plateau climate"],
"古埃及早王朝":["Early Dynastic Egypt","Egyptian early dynastic state"],
"古埃及古王国":["Old Kingdom Egypt pyramids","Old Kingdom Egypt state"],
"苏美尔城邦":["Sumerian city-states","Sumer urbanism"],
"周代":["Zhou dynasty Western Zhou","Zhou China feudal"],
"宋代":["Song dynasty China economy","Song China urbanization"],
"法兰克王国":["Frankish kingdom Merovingian","Frankish realm"],
"十字军东征":["Crusades Mediterranean trade","Crusader states"],
"莫斯科公国":["Muscovy Russian state formation","Grand Duchy Moscow"],
"黑海海峡":["Bosporus Dardanelles straits","Turkish straits regime"],
"加勒比海群岛":["Caribbean islands biogeography","Caribbean archipelago"],
"蒂亚瓦纳科":["Tiwanaku Andean state","Tiwanaku archaeology"],
"马丘比丘":["Machu Picchu Inca","Machu Picchu archaeology"],
"巴西殖民经济":["colonial Brazil economy","Brazil sugar colonial"],
"大自流盆地":["Great Artesian Basin","Artesian Basin Australia"],
"新西兰北岛":["North Island New Zealand geology","North Island volcanism"],
"新西兰南岛":["South Island New Zealand","Southern Alps geology"],
"夏威夷群岛":["Hawaiian Islands geology","Hawaii volcanism hotspot"],
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
    if not inv: return None
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for title,qs in Q.items():
    e=T.get(title)
    if not e: continue
    have_ids={s.replace("openalex-","") for s in e["sources"] if s.startswith("openalex-")}
    have_dois=set()
    best=None;tries=[]
    for q in qs:
        cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=15&select=title,DOI,type")
        for it in (cr.get("message") or {}).get("items") or []:
            doi=it.get("DOI")
            if not doi or doi in have_dois: continue
            have_dois.add(doi)
            if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
            oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
            oid=(oa.get("id") or "").rsplit("/",1)[-1]
            if not oid or oid in have_ids: continue
            a=ab(oa) or ""
            ttl=oa.get("title") or ""
            tries.append({"doi":doi,"title":ttl[:60],"abs_len":len(a)})
            if len(a)<300: continue
            rec={"doi":doi,"title":ttl,"year":oa.get("publication_year"),"oa_id":oid,
                 "cited":oa.get("cited_by_count"),"type":oa.get("type"),"abs_len":len(a),
                 "abstract":a,"host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if best: break
        time.sleep(1.2)
    res[title]={"cand":best,"tries":tries[:12]}
    print(f"{'OK' if best else '--'} {title:<14} {(best['title'][:50] if best else '-')} ({best.get('year') if best else ''}) cite={best.get('cited') if best else ''}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round42_second.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有第二来源候选:",sum(1 for v in res.values() if v["cand"]),"/",len(Q),flush=True)