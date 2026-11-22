# -*- coding: utf-8 -*-
"""第28轮返工 R3-R6。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
def f(c,k):
    r=D.get(c,{}).get(k)
    if not r: return None
    if k=="pop_total": return f"{int(r['value']):,} 人（{r['year']}年）"
    if k=="life_exp": return f"{r['value']:.1f} 岁（{r['year']}年）"
    return f"{r['value']:.1f}%（{r['year']}年）"

# R3 白令陆桥：补 RUS 数据，删悬空引用
b=T.get("白令陆桥")
if b and "俄罗斯一侧数据见下" in (b.get("today") or ""):
    rp=f("RUS","pop_total"); ru=f("RUS","urban_pct")
    b["today"]=(f"以俄罗斯与美国为例，来源：世界银行 API。俄罗斯总人口 {rp}（SP.POP.TOTL）、城市化率 {ru}（SP.URB.TOTL.IN.ZS）；"
      f"美国总人口 {f('USA','pop_total')}（SP.POP.TOTL）。上述为两国全国口径数据，仅示量级，不代表白令海峡区域的内部差异；"
      "该区域人口与生态数据待专门统计与机构来源核验。")
    for s in ("wb-rus-pop","wb-rus-urban"):
        if s not in b["sources"]: b["sources"].append(s)
    b["pending_notes"]=((b.get("pending_notes") or "")+" 【第28轮返工】删除「俄罗斯一侧数据见下」悬空引用，补俄美两国实测值。").strip()

# R4 沙尘暴：拆拼接证据句
d=T.get("沙尘暴")
if d:
    pn=d.get("pending_notes") or ""
    pn=re.sub(r"D055 判定：达标（[^）]*）。",
      "证据分开：s046（NASA Dust Bowl-to-Sahel）=200/正文10327/命中20（档②门槛8000，正文达标且命中≥3 → 本条达标依据）；s045（NASA Desertification）=200/正文22413/命中0（本条正则未命中，不构成依据）。",pn)
    d["pending_notes"]=pn;d["last_update"]=TODAY

# R5 DN068 / 单位失真
for e in T.values():
    pn=e.get("pending_notes") or ""
    if "DN068" in pn:
        pn=pn.replace("DN068","D068")
    if "单位含「人/岁/%」" in pn:
        tod=e.get("today") or ""
        units=[]
        if " 人（" in tod: units.append("人")
        if "%（" in tod: units.append("%")
        if " 岁（" in tod: units.append("岁")
        pn=pn.replace("单位含「人/岁/%」", "单位"+("、".join(units) if units else "（本条无数据单位）"))
    e["pending_notes"]=pn

# R6 斐济 M49 说明 + 荒漠化第二源标注
po=T.get("波利尼西亚")
if po:
    po["today"]=(po.get("today") or "").replace("（岛群差异大）",
      "（斐济按 UNSD M49 归美拉尼西亚，位于波利尼西亚西缘，此处作代表示意而非归属说明）")
de=T.get("荒漠化")
if de:
    de["pending_notes"]=((de.get("pending_notes") or "")+
      " D053：第二源 s018（FAO Forestry）与本条主题错配（正文 4707 字符、本条正则命中 1），不构成独立依据。").strip()

for u,dd in docs.items(): json.dump(dd,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("R3-R6 完成")