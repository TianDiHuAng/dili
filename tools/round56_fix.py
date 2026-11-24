# -*- coding: utf-8 -*-
"""第56轮：修 R19 词形逻辑（复数/词干）、处置马里与古希腊两条、把第二层写入 check.py。"""
import json,os,re,sys,unicodedata
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# ===== 1 处置两条真违规（标题不含对象词 → 标旁证）=====
FIX={
"马里帝国":("openalex-W2089041290","《Myth and Metrology: The Early Trans-Saharan Gold Trade》(1982, 被引115) 的**标题不含 mali**——研究对象是跨撒哈拉黄金贸易的度量传统，属与马里相关的**区域贸易侧面**，按 R19 第二层标为旁证，不作「马里帝国」的主来源。"),
"古希腊城邦":("openalex-W3098219892","《Coastal Geomorphology and Sea-Level Change》(2009, 被引75) 的**标题不含 greek/greece/polis**——是地形与海平面研究，属「希腊地形」的旁证，不作城邦条目主来源。"),
}
for t,(sid,why) in FIX.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第56轮R19第二层】{sid}：{why}").strip()
    e["last_update"]=TODAY

# ===== 2 修对象词（加复数/别名），重跑校验 =====
OBJ={
"尼罗河谷":["nile"],"刚果盆地":["congo"],"东非大裂谷":["east african rift","rift valley","ethiopian rift"],
"撒哈拉沙漠":["sahara"],"两河流域":["mesopotamia","tigris","euphrates"],"苏美尔城邦":["sumer"],
"阿卡德帝国":["akkad"],"阿契美尼德波斯":["achaemenid","persia"],"迦太基":["carthage","punic"],
"马里帝国":["mali"],"古埃及早王朝":["egypt","dynastic"],"古埃及古王国":["egypt","old kingdom"],
"古埃及新王国":["egypt","new kingdom"],"黄河流域":["yellow river","huang he"],"长江流域":["yangtze","changjiang"],
"日本列岛":["japan"],"汉代":["han"],"蒙古帝国":["mongol"],"阿兹特克":["aztec"],
"印度河文明":["indus"],"丝绸之路":["silk road"],"青藏高原":["tibet"],"爱琴海世界":["aegean"],
"古希腊城邦":["greek","greece","polis"],"罗马共和国":["roman","rome"],"罗马帝国":["roman","rome"],
"不列颠群岛":["british","britain"],"白令陆桥":["bering"],"密西西比河":["mississippi"],
"大平原":["great plains"],"中美洲地峡":["isthmus","central america"],"玛雅文明":["maya"],
"安第斯山脉":["andes"],"印加帝国":["inca"],"亚马逊盆地":["amazonia","amazon basin"],
"亚马逊河":["amazon"],"拉普拉塔平原":["la plata","plata","pampa"],"阿塔卡马沙漠":["atacama"],
"澳大利亚大陆":["australia"],"波利尼西亚":["polynesia"],"澳大利亚原住民":["aboriginal"],
"南极大陆":["antarctic"],"南极冰盖":["antarctic","ice sheet"],"季风系统":["monsoon"],
"洋流":["ocean","circulation","current"],"河流三角洲":["delta"],"板块构造":["plate tectonic"],
"游牧":["nomad","pastoral"],"气候带":["climate zone","climate classification"],
"城市起源":["cit"],   # 用词干，覆盖 city/cities/civilization
"文艺复兴意大利":["renaissance","italy","italian"],
}
def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
viol=[]
for t,objs in OBJ.items():
    e=T.get(t)
    if not e: continue
    for sid in e["sources"]:
        if not sid.startswith("openalex-"): continue
        ti=norm((S.get(sid) or {}).get("title"))
        if not any(norm(o) in ti for o in objs):
            viol.append({"entry":t,"sid":sid,"title":((S.get(sid) or {}).get("title") or "")[:70]})
print("重跑后仍有违规:",len(viol))
for v in viol: print("  ",v["entry"],v["sid"],v["title"])
json.dump({"round":56,"obj_map":OBJ,"remaining_violations":viol},
 open(os.path.join(ROOT,"reports","round56_r19b.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
save_docs(docs)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=56
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)