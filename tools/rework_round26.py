# -*- coding: utf-8 -*-
"""第26轮返工：修寿命单位、斯瓦希里换TZA/KEN、拉普拉塔补ARG/URY、刚果盆地判定、撤连批复核、补档位判定。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
def y(c,k,unit="pct"):
    r=D[c][k]
    return f"{r['value']:.1f}%（{r['year']}年）" if unit=="pct" else f"{int(r['value']):,}（{r['year']}年）"
def yr(c,k): 
    r=D[c][k]; return f"{r['value']:.1f} 岁（{r['year']}年）"

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 寿命单位修正
T["尼罗河谷"]["today"]=T["尼罗河谷"]["today"].replace(
  [x for x in [T["尼罗河谷"]["today"]] if "预期寿命" in x][0].split("预期寿命")[1].split("（")[0],
  " "+yr("EGY","life_exp").rstrip("（2024年）")+"（2024年）") if "预期寿命" in T["尼罗河谷"]["today"] else T["尼罗河谷"]["today"]
# 更稳妥：整段重写含寿命的两条
T["尼罗河谷"]["today"]=(f"以埃及为例，来源：世界银行 API。总人口 {y('EGY','pop_total','int')}（SP.POP.TOTL）、"
  f"城市化率 {y('EGY','urban_pct')}（SP.URB.TOTL.IN.ZS）、预期寿命 {yr('EGY','life_exp')}（SP.DYN.LE00.IN）。"
  "河谷与三角洲仍是人口与农业最密集的区域，具体流域内分布数据需专门统计源核验。")
T["日本列岛"]["today"]=(f"来源：世界银行 API。总人口 {y('JPN','pop_total','int')}（SP.POP.TOTL）、"
  f"城市化率 {y('JPN','urban_pct')}（SP.URB.TOTL.IN.ZS）、森林覆盖率 {y('JPN','forest_pct')}（AG.LND.FRST.ZS）、"
  f"预期寿命 {yr('JPN','life_exp')}（SP.DYN.LE00.IN）。列岛人口集中于沿海平原，具体分布数据待专门来源核验。")

# 2) 斯瓦希里海岸：改 TZA/KEN
T["斯瓦希里海岸"]["today"]=(f"以坦桑尼亚与肯尼亚为例，来源：世界银行 API。坦桑尼亚总人口 {y('TZA','pop_total','int')}（SP.POP.TOTL）、"
  f"城市化率 {y('TZA','urban_pct')}（SP.URB.TOTL.IN.ZS）；肯尼亚总人口 {y('KEN','pop_total','int')}、城市化率 {y('KEN','urban_pct')}。"
  "东非海岸港口吞吐与城市人口数据需专门来源核验。")
T["斯瓦希里海岸"]["pending_notes"]=(T["斯瓦希里海岸"].get("pending_notes") or "")+" 【第26轮返工】原用南非（ZAF）作「区域参照」属国家错配，已改为坦桑尼亚/肯尼亚实测值。"

# 3) 拉普拉塔平原：补 ARG/URY，纠正归因
T["拉普拉塔平原"]["today"]=(f"以阿根廷与乌拉圭为例，来源：世界银行 API。阿根廷总人口 {y('ARG','pop_total','int')}（SP.POP.TOTL）、"
  f"城市化率 {y('ARG','urban_pct')}（SP.URB.TOTL.IN.ZS）；乌拉圭总人口 {y('URY','pop_total','int')}、城市化率 {y('URY','urban_pct')}。"
  "两国农牧业产值与播种面积数据待专门统计来源核验。")
for s in ("wb-api-pop","wb-api-urban"):
    if s not in T["拉普拉塔平原"]["sources"]: T["拉普拉塔平原"]["sources"].append(s)
T["拉普拉塔平原"]["pending_notes"]=(T["拉普拉塔平原"].get("pending_notes") or "")+" 【第26轮】昨日因 ARG/URY **未纳入采集名单**（非数据缺失）而未填，已补实测值并挂 wb-api 源（D065 同型问题已纠正）。"

# 4) 刚果盆地：判定改为未达标
cg=T.get("刚果盆地")
if cg:
    pn=cg.get("pending_notes") or ""
    pn=re.sub(r"D055 判定：达标（可升级候选）；缺口为「刚果盆地」主题专题页。",
      "D055 判定：**未达标**——档③（标题不含本条核心词）要求正文≥8000 且命中≥5，实测最高命中 3 < 5；缺口为刚果盆地主题专题页。",pn)
    cg["pending_notes"]=pn

# 5) 撤连批复核 6 条（第25轮刚复核）
WITHDRAW=["东非大裂谷","大平原","澳大利亚大陆","大自流盆地","新西兰北岛","新西兰南岛"]
for t in WITHDRAW:
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    pn=re.sub(r"【第26轮实证复核[^】]*】[^【]*?(?=【|$)","",pn).strip()
    e["pending_notes"]=pn+" 【第26轮】按 D059 撤回本轮复核标记（该条第25轮刚复核，避免连轮复检）。"
    e["status"]="已复核(第25轮·实证)"

# 6) 7 条"达标/缺口"互斥修正 + 补档位判定
CONFLICT=["萨赫勒带","古埃及早王朝","古埃及古王国","马里帝国","罗马共和国"]
for t in CONFLICT:
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    pn=pn.replace("D055 判定：达标（可升级候选）；缺口为","D055 判定：未达标（实测未同时满足「正文≥门槛」与「命中≥3」，详见上句数字）；缺口为")
    e["pending_notes"]=pn

# 7) 补档位判定行（所有含第26轮实证的条目）
for e in T.values():
    pn=e.get("pending_notes") or ""
    if "第26轮实证复核" not in pn or "档位" in pn: continue
    m=re.search(r"本条正则 ([^；]+)；",pn)
    rx=m.group(1) if m else "?"
    e["pending_notes"]=pn+f" 档位判定：本条标题为「{e['title']}」，正则 {rx} 是否出现在来源标题需逐页确认；未确认时按档③（8000字+命中≥5）从严。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
n26=sum(1 for e in T.values() if "第26轮实证复核" in (e.get("pending_notes") or ""))
print("剩余第26轮实证复核:",n26,"；撤回 6 条")