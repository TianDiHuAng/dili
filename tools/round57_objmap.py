# -*- coding: utf-8 -*-
"""第57轮：为 97 条重要条目补建对象词映射，并跑 R20 全量校验。"""
import json,os,re,sys,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

ADD={
"尼罗河三角洲":["nile delta","delta"],"埃塞俄比亚高原":["ethiopia","ethiopian"],
"几内亚湾沿岸":["guinea"],"萨赫勒带":["sahel"],"马格里布":["maghreb","maghrib"],
"古埃及古王国":["egypt","old kingdom"],"古埃及新王国":["egypt","new kingdom"],
"库什与努比亚":["kush","nubia","meroe","napata"],"罗马阿非利加":["africa","roman"],
"阿拉伯征服北非":["arab","islamic conquest","north africa"],"加纳帝国":["ghana"],"桑海帝国":["songhai"],
"大津巴布韦":["zimbabwe"],"斯瓦希里海岸":["swahili"],"阿卡德帝国":["akkad"],
"古巴比伦":["babylon"],"亚述帝国":["assyria"],"帕提亚帝国":["parthia"],"萨珊波斯":["sasanian","sassanian"],
"吠陀时代":["vedic"],"孔雀王朝":["maurya","asoka","ashoka"],"笈多王朝":["gupta"],
"商代":["shang"],"周代":["zhou"],"秦代":["qin"],"隋唐":["sui","tang"],"宋代":["song"],"元代":["yuan"],
"明清":["ming","qing"],"朝鲜半岛":["korea"],"中南半岛":["indochina","southeast asia"],
"湄公河三角洲":["mekong"],"吴哥":["angkor","khmer"],"马来群岛":["malay","archipelago"],
"河中地区":["transoxiana","samarkand","bukhara","central asia"],
"匈奴":["xiongnu"],"突厥":["turk"],"阿拉伯半岛":["arabian peninsula","arabia"],
"黎凡特":["levant"],"安纳托利亚":["anatolia"],"东亚季风":["east asian monsoon","monsoon"],
"克里特文明":["minoan","crete"],"马其顿与亚历山大":["macedon","alexander"],
"拜占庭帝国":["byzantine"],"意大利半岛":["italy","italian peninsula","apennine"],
"伊比利亚半岛":["iberia","iberian"],"高卢":["gaul"],"阿尔卑斯山":["alps","alpine"],
"多瑙河":["danube"],"莱茵河":["rhine"],"维京时代":["viking"],"法兰克王国":["frankish","francia","merovingian","carolingian"],
"十字军东征":["crusade"],"威尼斯":["venice","venetian"],"莫斯科公国":["muscovy","moscow"],
"巴尔干半岛":["balkan"],"斯堪的纳维亚":["scandinavia"],"黑海海峡":["bosporus","dardanelles","strait"],
"欧洲温带海洋性气候":["oceanic climate","maritime climate","thermohaline"],
"中世纪欧洲庄园农业":["manor","medieval agricultur"],"北美冰盖":["laurentide","ice sheet","keewatin"],
"落基山脉":["rocky mountain"],"五大湖":["great lakes"],"科罗拉多高原":["colorado plateau"],
"墨西哥湾":["gulf of mexico"],"奥尔梅克":["olmec"],"特奥蒂瓦坎":["teotihuacan"],
"北美原住民":["native american","peopling","beringia"],"格陵兰岛":["greenland"],
"十三殖民地":["thirteen colonies","colonial"],"美国西进":["westward","frontier"],
"加勒比海群岛":["caribbean"],"巴西高原":["brazil"],"拉普拉塔平原":["la plata","plata","pampa"],
"阿塔卡马沙漠":["atacama"],"莫切文化":["moche"],"蒂亚瓦纳科":["tiwanaku"],"马丘比丘":["machu picchu"],
"安第斯垂直农业":["andean","altitudinal"],"巴西殖民经济":["brazil","colonial"],
"大分水岭":["great dividing","dividing range"],"大自流盆地":["artesian"],
"新西兰北岛":["north island"],"新西兰南岛":["south island","southern alps","torlesse"],
"毛利人":["maori"],"夏威夷群岛":["hawai"],"大堡礁":["great barrier reef","coral"],
"澳大利亚内陆干旱气候":["australia","arid"],"澳大利亚混合农业":["australia","wheat","mixed farming"],
"南极半岛":["antarctic peninsula","antarctic"],"南极条约体系":["antarctic treaty"],
"冰芯气候记录":["ice core"],"松岛冰川退缩":["pine island","thwaites","glacier"],
"大陆漂移":["continental drift","wegener","plate tectonic"],"洋流":["ocean","circulation","current"],
"气候带":["climate zone","climate classification"],"冲积平原":["alluvial"],
"山地农业":["mountain agriculture","highland","terrace"],"人口迁移":["migration"],
"植物物候变化":["phenolog"],"北极火情变化":["tundra fire","arctic fire"],
"地理信息系统":["gis","geographic information"],"人口地理":["population"],
"城市地理":["urban","city"],
}

objpath=os.path.join(DATA,"object_words.json")
obj=json.load(open(objpath,encoding="utf-8"))
n=0
for t,words in ADD.items():
    if t in obj: continue
    obj[t]=words;n+=1
json.dump(obj,open(objpath,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"新增映射 {n} 条，总 {len(obj)} 条")

def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))

# R20 全量校验（豁免已标旁证/弱来源）
viol=[]
for t,objs in obj.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    for sid in e["sources"]:
        if not sid.startswith("openalex-"): continue
        idx=pn.find(sid); seg=pn[max(0,idx-150):idx+80] if idx>=0 else ""
        if any(k in seg for k in ("旁证","弱来源","剔除","降级","不作")): continue
        ti=norm((S.get(sid) or {}).get("title"))
        if not any(norm(o) in ti for o in objs):
            viol.append({"entry":t,"sid":sid,"title":((S.get(sid) or {}).get("title") or "")[:66],"objs":objs[:2]})
print(f"R20 全量检出 {len(viol)} 条")
from collections import Counter
c=Counter(v["entry"] for v in viol)
for e,k in c.most_common(25):
    print(f"  {e:<14} ×{k}")
json.dump({"round":57,"obj_total":len(obj),"violations":viol},
 open(os.path.join(ROOT,"reports","round57_r20.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)