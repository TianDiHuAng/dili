# -*- coding: utf-8 -*-
"""第34轮：严格筛标题相关性，选出可用条目。"""
import json,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O=json.load(open(os.path.join(ROOT,"reports","round34_openalex3.json"),encoding="utf-8"))
# 每条的核心英文词（须出现在标题中）
CORE={
"尼罗河三角洲":["nile delta","nile"],
"安纳托利亚":["anatolia","byzantine anatolia"],
"阿尔卑斯山":["alps","alpine"],
"墨西哥湾":["gulf of mexico"],
"巴西高原":["brazil","brazilian"],
"新西兰北岛":["north island"],
"新西兰南岛":["southern alps","south island"],
"大堡礁":["great barrier reef","coral reef"],
"南极半岛":["antarctic peninsula","antarctic"],
"松岛冰川退缩":["pine island","thwaites","glacier retreat"],
"大陆漂移":["continental drift","wegener","plate tectonics"],
"几内亚湾沿岸":["gulf of guinea"],
"湄公河三角洲":["mekong"],
"美国西进":["westward","american west","frontier"],
"大津巴布韦":["great zimbabwe","zimbabwe"],
"帕提亚帝国":["parthian"],
"隋唐":["sui-tang","tang","sui dynasty"],
"明清":["ming","qing"],
"马来群岛":["malay archipelago","malay"],
"莱茵河":["rhine"],
"十字军东征":["crusade","crusades"],
"威尼斯":["venice","venetian"],
"黑海海峡":["strait","bosporus","dardanelles"],
"特奥蒂瓦坎":["teotihuacan"],
"亚述帝国":["assyrian","assyria"],
"萨珊波斯":["sasanian","sassanian"],
"孔雀王朝":["maurya","asoka","ashoka"],
"匈奴":["xiongnu","steppe nomad","nomads of the eastern steppe"],
"马其顿与亚历山大":["alexander","macedon"],
"拜占庭帝国":["byzantine"],
"莫斯科公国":["moscow","muscovy"],
"十三殖民地":["thirteen colonies","colonial america"],
"蒂亚瓦纳科":["tiwanaku"],
"中南半岛":["southeast asia","indochina"],
"黎凡特":["levant","eastern mediterranean"],
"高卢":["gaul"],
"多瑙河":["danube"],
"北美原住民":["native american","americas migration","peopling of the americas"],
"吠陀时代":["vedic"],
"古巴比伦":["babylon","babylonia"],
}
res={}
for t,cands in O.items():
    if not cands: continue
    keys=CORE.get(t,[])
    if not keys: continue
    good=[]
    for c in cands:
        ti=(c.get("title") or "").lower()
        if any(k in ti for k in keys):
            good.append(c)
    if good:
        # 优先被引多、年份新
        good.sort(key=lambda x:(-(x.get("cited") or 0)))
        res[t]=good[0]
        print(f"OK {t:<14} {good[0].get('year')} 「{(good[0].get('title') or '')[:58]}」")
    else:
        print(f"-- {t:<14} 标题不含核心词，剔除 {len(cands)} 条")
json.dump(res,open(os.path.join(ROOT,"reports","round34_final.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",len(res),"条")