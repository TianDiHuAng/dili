# -*- coding: utf-8 -*-
"""第56轮：为核心条目建立「条目→对象词」映射，并做对象词校验（R19 第二层）。"""
import json,os,re,sys,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))

# 核心条目 → 对象词（英文，可多个别名）
OBJ={
"尼罗河谷":["nile"],"刚果盆地":["congo"],"东非大裂谷":["east african rift","rift valley","ethiopian rift"],
"撒哈拉沙漠":["sahara"],"两河流域":["mesopotamia","tigris","euphrates"],"苏美尔城邦":["sumer","sumerian"],
"阿卡德帝国":["akkad","akkadian"],"阿契美尼德波斯":["achaemenid","persia","persian"],"迦太基":["carthage","punic"],
"马里帝国":["mali"],"古埃及早王朝":["egypt","dynastic"],"古埃及古王国":["egypt","old kingdom"],
"古埃及新王国":["egypt","new kingdom"],"黄河流域":["yellow river","huang he"],"长江流域":["yangtze","changjiang"],
"日本列岛":["japan","japanese"],"汉代":["han"],"蒙古帝国":["mongol"],"阿兹特克":["aztec"],
"印度河文明":["indus"],"丝绸之路":["silk road"],"青藏高原":["tibet","tibetan"],"爱琴海世界":["aegean"],
"古希腊城邦":["greek","greece","polis"],"罗马共和国":["roman","rome"],"罗马帝国":["roman","rome"],
"不列颠群岛":["british","britain","britain"],"白令陆桥":["bering","beringia"],"密西西比河":["mississippi"],
"大平原":["great plains","plains"],"中美洲地峡":["isthmus","central america"],"玛雅文明":["maya"],
"安第斯山脉":["andes","andean"],"印加帝国":["inca"],"亚马逊盆地":["amazon","amazonia"],
"亚马逊河":["amazon"],"拉普拉塔平原":["la plata","plata","pampa"],"阿塔卡马沙漠":["atacama"],
"澳大利亚大陆":["australia","australian"],"波利尼西亚":["polynesia","polynesian"],
"澳大利亚原住民":["aboriginal","australian"],"南极大陆":["antarctic","antarctica"],
"南极冰盖":["antarctic","ice sheet"],"季风系统":["monsoon"],"洋流":["ocean","circulation","current"],
"河流三角洲":["delta"],"板块构造":["plate tectonic","tectonic"],"游牧":["nomad","pastoral"],
"气候带":["climate zone","climate classification"],"城市起源":["city","urban"],
}
# 核心条目集合
core=[t for t,e in T.items() if e["tier"]=="核心"]
missing_obj=[t for t in core if t not in OBJ]

print(f"核心条目 {len(core)} 条；已建映射 {len(core)-len(missing_obj)} 条")
if missing_obj: print("缺映射:",missing_obj)

# 校验：每条核心条目的 openalex 来源标题是否含对象词
viol=[]
for t in core:
    objs=OBJ.get(t)
    if not objs: continue
    for sid in T[t]["sources"]:
        if not sid.startswith("openalex-"): continue
        s=S.get(sid) or {}
        ti=norm(s.get("title"))
        if not any(norm(o) in ti for o in objs):
            viol.append({"entry":t,"sid":sid,"title":(s.get("title") or "")[:70],"objs":objs})
print(f"\n对象词校验：检出 {len(viol)} 条标题不含对象词")
for v in viol:
    print(f"  {v['entry']:<12} {v['sid']:<22} 「{v['title']}」")
    print(f"      期望对象词: {v['objs']}")
json.dump({"round":56,"core_count":len(core),"mapped":len(core)-len(missing_obj),
 "violations":viol,"obj_map":{k:v for k,v in OBJ.items()}},
 open(os.path.join(ROOT,"reports","round56_r19b.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)