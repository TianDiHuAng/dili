# -*- coding: utf-8 -*-
"""第33轮续：为重要 L1 的地形/区域类条目查询 Wikidata 面积/长度/海拔。"""
import subprocess,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP={
"埃塞俄比亚高原":"Ethiopian Highlands","几内亚湾沿岸":"Gulf of Guinea","马格里布":"Maghreb",
"阿拉伯半岛":"Arabian Peninsula","黎凡特":"Levant","安纳托利亚":"Anatolia","意大利半岛":"Italian Peninsula",
"伊比利亚半岛":"Iberian Peninsula","高卢":"Gaul","多瑙河":"Danube","莱茵河":"Rhine",
"巴尔干半岛":"Balkans","斯堪的纳维亚":"Scandinavia","黑海海峡":"Turkish Straits",
"墨西哥湾":"Gulf of Mexico","格陵兰岛":"Greenland","加勒比海群岛":"Caribbean","巴西高原":"Brazilian Highlands",
"新西兰北岛":"North Island","新西兰南岛":"South Island","夏威夷群岛":"Hawaiian Islands","大堡礁":"Great Barrier Reef",
"大自流盆地":"Great Artesian Basin","澳大利亚内陆干旱气候":"Outback",
}
UNITS={"mass":"P2046","len":"P2043","elev":"P2044"}
def get(u):
    return subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",u],
                          capture_output=True,timeout=35).stdout.decode("utf-8","ignore")
UNIT={"http://www.wikidata.org/entity/Q712226":"km²","http://www.wikidata.org/entity/Q828224":"km",
      "http://www.wikidata.org/entity/Q11573":"m"}
out={}
for cn,en in MAP.items():
    su=f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={en.replace(' ','%20')}&language=en&format=json&limit=2"
    try: d=json.loads(get(su))
    except Exception: continue
    cand=[s for s in d.get("search",[]) if s.get("id","").startswith("Q")]
    if not cand: print(f"{cn:<16} NO_ENTITY");continue
    qid=cand[0]["id"];desc=cand[0].get("description") or ""
    eu=f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json"
    try: cl=json.loads(get(eu))["entities"][qid].get("claims",{})
    except Exception: continue
    vals={}
    for k,pid in UNITS.items():
        if pid in cl:
            try:
                v=cl[pid][0]["mainsnak"]["datavalue"]["value"]
                vals[k]=(v.get("amount"),UNIT.get(v.get("unit"),v.get("unit","")))
            except Exception: pass
    out[cn]={"qid":qid,"desc":desc,"vals":vals}
    print(f"{cn:<16} {qid:<9} {vals} | {desc[:40]}")
json.dump(out,open(os.path.join(ROOT,"reports","round33_wikidata_geo.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有量值:",sum(1 for v in out.values() if v["vals"]))