# -*- coding: utf-8 -*-
"""第34轮：为 重要 L1 批量检索 OpenAlex 学术来源（逐主题定向检索）。"""
import subprocess,json,os,urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
# 地形
"尼罗河三角洲":"Nile Delta geomorphology evolution","安纳托利亚":"Anatolia geography plateau history",
"意大利半岛":"Italian peninsula geography history","阿尔卑斯山":"Alps mountain range geology formation",
"斯堪的纳维亚":"Scandinavia geography glaciation","墨西哥湾":"Gulf of Mexico oceanography basin",
"巴西高原":"Brazilian Highlands geology","马丘比丘":"Machu Picchu Inca site",
"大自流盆地":"Great Artesian Basin Australia groundwater","新西兰北岛":"North Island New Zealand geology",
"新西兰南岛":"South Island New Zealand Southern Alps","夏威夷群岛":"Hawaiian Islands volcanism hotspot",
"大堡礁":"Great Barrier Reef coral reef ecology","南极半岛":"Antarctic Peninsula warming ice",
"松岛冰川退缩":"Pine Island Glacier retreat mass loss","大陆漂移":"continental drift plate tectonics Wegener",
# 气候
"几内亚湾沿岸":"Gulf of Guinea coast climate","东亚季风":"East Asian monsoon system variability",
"欧洲温带海洋性气候":"Western Europe temperate maritime climate","澳大利亚内陆干旱气候":"Australian arid interior climate",
# 农业
"湄公河三角洲":"Mekong Delta agriculture sediment","中世纪欧洲庄园农业":"medieval European manor agriculture",
"美国西进":"American westward expansion settlement","莫切文化":"Moche culture Andes",
"安第斯垂直农业":"Andean vertical agriculture zonation","澳大利亚混合农业":"Australian mixed farming wheat sheep",
"冲积平原":"alluvial plain formation agriculture","山地农业":"mountain agriculture terrace systems",
# 贸易
"大津巴布韦":"Great Zimbabwe trade Indian Ocean","帕提亚帝国":"Parthian empire trade Silk Road",
"隋唐":"Sui Tang China empire","明清":"Ming Qing China economy trade",
"马来群岛":"Malay Archipelago trade maritime","河中地区":"Transoxiana Central Asia trade",
"莱茵河":"Rhine river trade transport","十字军东征":"Crusades Mediterranean trade",
"威尼斯":"Venice maritime trade republic","黑海海峡":"Turkish Straits Bosporus Dardanelles",
"特奥蒂瓦坎":"Teotihuacan Mesoamerica city","加勒比海群岛":"Caribbean islands geography colonial",
# 政权
"阿拉伯征服北非":"Arab conquest North Africa","古巴比伦":"Babylonia ancient Mesopotamia",
"亚述帝国":"Neo-Assyrian empire","萨珊波斯":"Sasanian empire Iran","吠陀时代":"Vedic period India",
"孔雀王朝":"Maurya empire India","吴哥":"Angkor Khmer empire","匈奴":"Xiongnu steppe nomads",
"突厥":"Gokturk Turks Central Asia","马其顿与亚历山大":"Macedonia Alexander the Great",
"拜占庭帝国":"Byzantine empire","法兰克王国":"Frankish kingdom Francia",
"莫斯科公国":"Grand Duchy of Moscow","十三殖民地":"Thirteen Colonies British America",
"蒂亚瓦纳科":"Tiwanaku Andean state","巴西殖民经济":"colonial Brazil economy sugar",
# 区域
"朝鲜半岛":"Korean peninsula geography","中南半岛":"Indochina peninsula mainland Southeast Asia",
"黎凡特":"Levant region Middle East","伊比利亚半岛":"Iberian Peninsula geography history",
"高卢":"Gaul Roman provinces","多瑙河":"Danube river basin","巴尔干半岛":"Balkan peninsula geography",
"北美原住民":"Native American settlement North America",
}
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
out={}
for t,q in Q.items():
    u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+
       "&per_page=6&mailto=geo-encyclopedia@example.com")
    try: d=json.loads(get(u))
    except Exception: out[t]=[];print(f"{t:<14} ERR");continue
    good=[]
    for w in d.get("results",[]):
        a=ab_of(w)
        if not a or len(a)<300: continue
        good.append({"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
          "year":w.get("publication_year"),"doi":w.get("doi"),"cited":w.get("cited_by_count"),
          "abstract":a,"host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    good.sort(key=lambda x:-(x.get("cited") or 0))
    out[t]=good
    print(f"{t:<14} {len(good)} | {(good[0]['title'][:52] if good else '-')}")
json.dump(out,open(os.path.join(ROOT,"reports","round34_openalex3.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有候选:",sum(1 for v in out.values() if v),"/",len(Q))