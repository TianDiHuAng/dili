# -*- coding: utf-8 -*-
"""第42轮：按核心对象词严格筛选第二来源候选。"""
import json,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=json.load(open(os.path.join(ROOT,"reports","round42_second.json"),encoding="utf-8"))
CORE={
"撒哈拉沙漠":["sahara"],"东非大裂谷":["east african rift","rift"],"两河流域":["mesopotamia","tigris","euphrates"],
"马里帝国":["mali"],"爱琴海世界":["aegean"],"罗马帝国":["roman empire","rome"],
"文艺复兴意大利":["renaissance","italy","italian"],"白令陆桥":["bering"],"大平原":["great plains","grassland"],
"玛雅文明":["maya"],"安第斯山脉":["andes","andean"],"印加帝国":["inca"],"澳大利亚大陆":["australia"],
"澳大利亚原住民":["aboriginal","australian"],"波利尼西亚":["polynesia","polynesian","voyaging"],
"南极大陆":["antarctic","antarctica"],"季风系统":["monsoon"],"气候带":["climate zone","climate classification"],
"河流三角洲":["delta"],"青藏高原":["tibet","tibetan"],"丝绸之路":["silk road"],"城市起源":["urban revolution","origin of cities","first cities","early cities"],
"克里特文明":["minoan","crete"],"维京时代":["viking","norse"],"落基山脉":["rocky mountain"],
"奥尔梅克":["olmec"],"十三殖民地":["thirteen colonies","colonial"],"拉普拉塔平原":["la plata","pampa","plata"],
"阿塔卡马沙漠":["atacama"],"大分水岭":["great dividing","dividing range"],"毛利人":["maori","aotearoa"],
"斯瓦希里海岸":["swahili"],"埃塞俄比亚高原":["ethiopia","ethiopian"],"古埃及早王朝":["early dynastic","dynastic egypt"],
"古埃及古王国":["old kingdom"],"苏美尔城邦":["sumer","sumerian"],"周代":["zhou"],"宋代":["song"],
"法兰克王国":["frankish","merovingian","francia"],"十字军东征":["crusade","crusades"],
"莫斯科公国":["muscovy","moscow"],"黑海海峡":["strait","bosporus","dardanelles"],
"加勒比海群岛":["caribbean"],"蒂亚瓦纳科":["tiwanaku"],"马丘比丘":["machu picchu"],
"巴西殖民经济":["brazil"],"大自流盆地":["artesian"],"新西兰北岛":["north island"],
"新西兰南岛":["south island","southern alps"],"夏威夷群岛":["hawai"],
}
ok={};rej={}
for t,v in S.items():
    c=v.get("cand")
    if not c: rej[t]="无候选";continue
    ti=(c["title"] or "").lower()
    keys=CORE.get(t,[])
    if any(k in ti for k in keys):
        ok[t]=c
    else:
        rej[t]=f"标题不含核心词「{c['title'][:56]}」"
print("通过:",len(ok),"/",len(S))
for t in ok: print("  OK",t,"|",ok[t]["year"],"|",ok[t]["title"][:58])
print("\n剔除:")
for t,r in rej.items(): print("  --",t,"|",r)
json.dump({"ok":ok,"rej":rej},open(os.path.join(ROOT,"reports","round42_screen.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)