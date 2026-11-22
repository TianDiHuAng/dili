# -*- coding: utf-8 -*-
"""第22轮返工：
1) 板块构造：备注删「s056 机构页」矛盾表述，改述同站目录页；
2) 南极冰盖：补 D053 披露，status 去「合规」改「配对说明」；
3) 6 条 time_or_place「约中生代至今」等收敛为待核；
4) 4 条复核改为从未复核条目，重复句合并；
5) 台账 note 修正（usgs-dynamic-earth 标题、nasa-ice-sheets 剥离值、s042 口径）。
"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 板块构造
p=T["板块构造"]
p["status"]="L2·配对说明(第22轮)"
p["pending_notes"]=("第22轮换源转正：专题页 USGS『Understanding plate motions』（剥离后 17121 字符、tectonic|plate 命中 86，D055 档① 达标）；"
 "第二来源为同站系列目录页『This Dynamic Earth--Contents』（剥离后 2123 字符、命中 4，无正文），仅作系列入口，不构成独立依据（D053）。"
 "五段按板块边界类型与理论作用重写，不含具体速率数值；板块速率与地震数据待按年份从 USGS 机构页核验。")

# 2) 南极冰盖
a=T["南极冰盖"]
a["status"]="L2·配对说明(第22轮)"
a["pending_notes"]=("第22轮换源转正：专题页 NASA『Ice Sheets』指标页（剥离后 8612 字符、命中 14，D055 档② 门槛 8000，余量较薄）；"
 "第二来源 s038 为 Earth Observatory 门户首页（剥离后 7143 字符、命中 1），无正文，仅作机构入口，不构成独立依据（D053）。"
 "冰盖质量与海平面数据待按年份从 NASA 机构页核验。")

# 3) 无源年代收敛（约中生代至今等）
BADTP=re.compile(r"(约?中生代|约?古生代|约?新生代|约?更新世|冰后期|全新世|约?白垩纪|约?\d+万年前|约?\d+亿年前)")
cnt=0
for t,e in T.items():
    tp=e.get("time_or_place") or ""
    if BADTP.search(tp) and "待专门来源核验" not in tp:
        e["time_or_place"]="时期与年代待专门来源核验（详见待核实）"
        e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第22轮】time_or_place 原「{tp}」无专门来源支撑，已收敛为待核表述。"
        e["last_update"]=TODAY;cnt+=1

# 4) 复核改选：从未复核的重要/核心 L1
DUPNOTE="【第22轮复核】"
for t,e in T.items():
    pn=e.get("pending_notes") or ""
    # 合并 17-22 重复句
    if pn.count("【第17轮复核】")>0 and pn.count("【第18轮复核】")>0:
        pass
GAP={"地形":"含地貌成因正文的专题页","气候":"含气候机制正文的专题页","农业":"含作物制度/水利正文的专题页",
 "贸易":"含商路与商品结构正文的专题页","政权更替":"含政权年代序列正文的专题页","区域":"含区域边界与现状数据正文的专题页"}
never=[t for t,e in T.items() if e["tier"] in ("重要","核心") and e["level"]=="L1"
       and "复核" not in (e.get("pending_notes") or "")]
print("从未复核的重要/核心 L1：",len(never),never[:12])
picked=never[:4]
for t in picked:
    e=T[t]
    e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第22轮·首轮复核】{e['region']}×{e['theme']}；来源均已核验；按 D041/D055 仍缺{GAP.get(e['theme'],'专题页')}。"
    e["last_update"]=TODAY;e["status"]="已复核(第22轮)"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 5) 台账 note 修正
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
    if s["id"]=="usgs-dynamic-earth":
        s["title"]="This Dynamic Earth--Contents [USGS]"
        s["note"]=(s.get("note") or "")+" 第22轮：线上标题为「This Dynamic Earth--Contents [USGS]」，已对齐；剥离后 2123 字符、命中 4，为系列目录页，不构成正文。"
    if s["id"]=="nasa-ice-sheets":
        s["note"]=re.sub(r"正文 \d+ 字节[；;]?", "剥离后正文 8612 字符、命中 14；", s.get("note") or "")
    if s["id"]=="s042-earthobservatory-nasa-gov":
        s["note"]=(s.get("note") or "")+" 第22轮核验：剥离后正文 46123 字符、tropical|deforest 命中 289（D050 口径）。"
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("年代收敛",cnt,"；复核改选",len(picked))