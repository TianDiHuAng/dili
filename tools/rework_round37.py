# -*- coding: utf-8 -*-
"""第37轮返工：去星号（含R17）、口径照抄、断言边界、重复端点合并、台账。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# 1) 去星号（正文段 + pending）
FIELDS=("definition","overview","geo","influence","polities","connections","today","time_or_place")
n=0
for d in docs.values():
    for e in d["entries"]:
        for f in FIELDS+("pending_notes",):
            v=e.get(f)
            if isinstance(v,str) and "**" in v:
                e[f]=v.replace("**","");n+=1
print("去星号字段:",n)

# 2) P2 口径照抄官方名
fw=T.get("森林覆盖变化")
if fw:
    fw["today"]=(fw["today"] or "").replace("森林覆盖率（%）","森林面积占土地面积（%）")
    fw["definition"]="森林覆盖变化：森林面积占土地面积的百分比及其随时间的变化。"
pa=T.get("保护与保育区体系")
if pa:
    pa["today"]=(pa["today"] or "").replace("陆地保护区占比（%）","陆地保护区占总土地面积（%）")
    pa["influence"]=(pa["influence"] or "").replace("海洋保护区覆盖低于陆地。","")
    pa["pending_notes"]=((pa.get("pending_notes") or "")+" 【第37轮返工】删除「海洋保护区覆盖低于陆地」——本条仅引陆地指标，该比较无来源支撑。").strip()

# 3) 室利佛逝否定断言
sf=T.get("室利佛逝")
if sf:
    sf["influence"]=("所引 2021 年研究强调其成长于「复杂网络」的中心：通过对海峡通行与港口节点的控制获得权力，"
      "而非依赖大片陆地疆域。这说明海上政权可以在陆地领土有限的情况下取得区域影响力。")
    sf["pending_notes"]=((sf.get("pending_notes") or "")+
      " 【第37轮返工】原句「不是靠征服大片领土」属摘要未作的否定断言，已改为「通过控制海峡与港口节点获得权力、而非依赖大片陆地疆域」的正面表述。").strip()

# 4) 贵霜/神圣罗马 归属收窄
ks=T.get("贵霜帝国")
if ks:
    ks["influence"]=("所引 2021 年研究称其为「欧亚的十字路口」：贵霜同时掌握政治军事控制与跨区域商路。"
      "（佛教艺术、钱币与文字的交流属本条对贵霜时期文化面貌的常识性补充，不挂该研究。）")
sr=T.get("神圣罗马帝国")
if sr:
    sr["influence"]=("所引 2016 年专著（Peter Wilson）认为，帝国的连续性建立在「统一基督教文明」的理念之上，"
      "其遗产至今见于关于欧盟性质的讨论。这说明「帝国」可以是一种以理念维系的制度安排。"
      "（「而非集权行政」属本条补充说明，不挂该专著。）")

# 5) 重复端点合并
DUP={"wb-wld-ag-lnd-frst-zs":"wb-wld-forest"}
for s in sd["sources"]:
    if s["id"] in DUP:
        s["note"]=(s.get("note") or "")+" 【第37轮】与 wb-wld-forest 同指 AG.LND.FRST.ZS，已合并引用。"
for e in T.values():
    e["sources"]=[DUP.get(s,s) for s in (e.get("sources") or [])]
seen=set();out=[]
for s in sd["sources"]:
    if s["id"] in seen: continue
    seen.add(s["id"]);out.append(s)
sd["sources"]=out

# 6) 农业统计补关联
ag=T.get("农业统计体系")
if ag:
    ag["today"]=(ag["today"] or "").replace("：全球 3,130,499,027 吨（2024年）",
      "：以该系统所统计的谷物产量为例，全球 3,130,499,027 吨（2024年）")

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=37;cov["round_processed"]=22
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成；来源数",len(sd["sources"]))