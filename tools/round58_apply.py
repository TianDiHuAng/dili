# -*- coding: utf-8 -*-
"""第58轮：如实记录3处无合格主来源；R20 扩展到补充条目。"""
import json,os,re,sys,unicodedata
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

REC={
"河中地区":"过筛者《The Sogdians and Their Religions in Turfan》（2021, 被引23）——研究对象是**吐鲁番出土的粟特语宗教文本目录**，虽涉粟特人（河中商路的主体人群），但主题是宗教文献学，**不支撑「绿洲灌溉与商路网络」**。主来源仍缺。",
"库什与努比亚":"两库、两条检索式（Meroe trade network commodities／Kushite Red Sea trade）均无一条同时满足「标题含 kush/meroe/nubia」与「两个商路主题槽」。**商路与商品结构确无合格主来源**。",
"莫切文化":"过筛者《A mass sacrifice of children and camelids at the Huanchaquito-Las Llamas》（2019, 被引78）——研究对象是**奇穆（Chimú）国家约公元 1450 年的儿童与骆驼科献祭**，与莫切文化既非同一政体、时期亦相差数百年（对象与时期双错）。不采用。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第58轮检索记录】{why}").strip()
    e["last_update"]=TODAY

# ===== R20 扩展到补充条目（为有 openalex 来源者建映射）=====
objpath=os.path.join(DATA,"object_words.json")
obj=json.load(open(objpath,encoding="utf-8"))
ADD={
"仰韶文化":["yangshao"],"古埃及中王国":["egypt","middle kingdom"],"法蒂玛王朝":["fatimid"],
"赫梯王国":["hittite"],"贵霜帝国":["kushan"],"室利佛逝":["srivijaya"],"满者伯夷":["majapahit"],
"帖木儿帝国":["timurid"],"迈锡尼文明":["mycenaean"],"神圣罗马帝国":["holy roman"],
"汉萨同盟":["hanseatic"],"基辅罗斯":["kyivan","kievan","rus"],"非洲大湖地区":["great lakes"],
"西北海岸":["northwest coast"],"新法兰西":["new france"],"古巴岛":["cuba"],"巴塔哥尼亚":["patagonia"],
"的的喀喀湖":["titicaca"],"查文文化":["chavin"],"纳斯卡文化":["nazca"],"奇穆帝国":["chimu"],
"南美贸易网络":["andean","exchange"],"南锥体":["southern cone","cone"],"美拉尼西亚":["melanesia"],
"密克罗尼西亚":["micronesia"],"复活节岛":["easter island","rapa nui"],"太平洋殖民航线":["lapita","pacific","voyaging"],
"横贯南极山脉":["transantarctic"],"罗斯海":["ross sea"],"南极科考站":["antarctic","station"],
"南极特别保护区":["antarctic","protected area"],"争议边界处理原则":["disputed","boundary"],
"人文地理学":["human geography"],"可持续交通":["sustainable transport","car sharing"],
"地图投影":["map projection"],"地球系统科学":["earth system"],"地理空间数据产品":["laserfarm","lidar"],
"环境数据访问":["ecodatacube","environmental data"],"城市热岛":["heat island"],"城市贫困":["urban","poverty"],
"沙漠化":["desertification","dryland"],"自然灾害风险":["hazard","disaster"],"火灾生态":["fire regime","bark"],
"生物多样性分布":["biodiversity","phylogenetic"],"极端天气预警":["monsoon","climate model","warning"],
"玛雅研究新进展":["maya","lidar"],"欧洲冰期地貌":["glacial","map"],"环境治理":["environmental governance"],
"农业气候风险":["agricultural","climate","vulnerab"],"巴塔哥尼亚高原":["patagonia"],
}
n=0
for t,w in ADD.items():
    if t in obj: continue
    obj[t]=w;n+=1
json.dump(obj,open(objpath,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"R20 映射新增 {n} 条，总 {len(obj)} 条")

def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))
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
            viol.append({"entry":t,"sid":sid,"title":((S.get(sid) or {}).get("title") or "")[:60],"objs":objs[:2]})
print(f"R20 全量（{len(obj)} 条）检出 {len(viol)} 条")
from collections import Counter
for en,k in Counter(v["entry"] for v in viol).most_common(20):
    print(f"  {en:<16} ×{k}")
json.dump({"round":58,"obj_total":len(obj),"violations":viol},
 open(os.path.join(ROOT,"reports","round58_r20.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
save_docs(docs)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=58
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)