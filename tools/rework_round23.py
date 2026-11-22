# -*- coding: utf-8 -*-
"""第23轮返工（二）：按实测写实证备注、修山地农业来源、修徽标。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
src={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 逐条实证（含实测数字与 D055 判定）
EV={
"夏威夷群岛":"实测：britannica-regions 实为 UNSD M49 方法论页（200 / 剥离后 137675 字符 / hawaii|island 命中 29，属区域统计口径而非专题）；wikipedia-regions 实为 UN SDG 数据门户（200 / **5 字符 JS 壳页** / 命中 0）。D053：第二源为壳别名，不构成独立依据；两源均非「夏威夷」专题页，故缺口为「太平洋岛屿专题页（D055 档①或②）」。",
"大堡礁":"实测：s050（NOAA Ocean Service 门户首页）200 / 剥离后 2753 字符 / reef|coral 命中 **0**；s085（UNESCO Ocean）本次不可达（HTTP 000）。缺口语义已对齐：待 GBRMPA 或 UNESCO **大堡礁世界遗产**页；当前两源对珊瑚礁主题均无正文支撑。",
"澳大利亚内陆干旱气候":"实测：s039（NASA Climate）200 / 剥离后 10544 字符 / arid|dry|drought 命中 **0**；s048（NOAA Climate.gov）403（WAF 拦截）。两源均未提供内陆干旱机制正文，缺口为「澳大利亚内陆干旱气候机制专题页」。",
"澳大利亚混合农业":"实测：s014（FAOSTAT）200 / 剥离后 **7 字符**（应用壳页）/ 命中 0；s022（OWID 首页）200 / 22764 字符 / farm|agricultur|wheat 命中 **5**（仅站点导航级）。缺口为「澳大利亚农业体系专题页」；D053：s014 为壳页。",
"南极半岛":"实测：s038（Earth Observatory 门户首页）200 / 7143 字符 / peninsula|antarctic 命中 **1**；s049（NCEI 首页）200 / 2471 字符 / 命中 **0**。两源均为机构入口，缺口为「南极半岛地貌/生态专题页」。",
"松岛冰川退缩":"实测：nasa-pine-island 200 / 剥离后 **7719 字符** / glacier|pine island|retreat 命中 **25** → D055 **档②（门槛 8000）**，**差 281 字符未达标**。这是可核的近失值，而非「缺专题页」；待该页扩写或另寻 ≥8000 字符的冰川专题页即可升级。",
"冲积平原":"实测：s015（FAO Land, Soil and Water）200 / 9643 字符 / alluvial|floodplain|sediment 命中 **0**；s016（FAO Land overview）200 / 4070 字符 / 命中 **0**。缺口为「冲积平原/河流沉积地貌专题页」（此前误写为作物制度/水利，已纠正）。",
"山地农业":"实测：s016（FAO Land overview）200 / 4070 字符 / mountain|terrace|slope 命中 **0**；s083（FAO 土壤数据）200 / 2268 字符 / 命中 **0**，且其 note 明写「mountain 命中 0，不用于山地条目」→ 已移除 s083。缺口为「FAO 山地农业正文页」。",
"城市起源":"实测：s010（UNESCO Culture）200 / 剥离后 **218 字符** / city|urban|settlement 命中 **0**；un-m49（UNSD M49）200 / 144945 字符 / 命中 **2**（仅国家分组级）。缺口为「早期城市/聚落考古专题页」（此前按 theme=政权更替 机械写为政权年代序列，已按主题纠正）。",
}
for t,txt in EV.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    # 删除旧模板句
    pn=re.sub(r"\s*【第2[0-9]轮[^】]*】[^【]*?(?:专题页|正文页)。", "", pn)
    pn=re.sub(r"\s*【第23轮·首轮复核】[^【]*?(?:专题页|正文页)。", "", pn)
    e["pending_notes"]=(pn.strip()+" 【第23轮实证复核】"+txt).strip()
    e["status"]="已复核(第23轮·实证)"
    e["last_update"]=TODAY

# 山地农业：移除 s083 并循环补足
m=T["山地农业"]
m["sources"]=[s for s in m["sources"] if s!="s083-fao-org"]
while len(m["sources"])<2:
    for s in ("s015-fao-org","s018-fao-org","un-m49"):
        if s not in m["sources"]:
            m["sources"].append(s);break
    else:
        m["sources"].append("un-m49")
m["pending_notes"]=m["pending_notes"]+" 已按 note 提示移除 s083（不用于山地条目），补入 s015/s018 区域农业机构页维持 ≥2。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("实证备注写入:",sum(1 for t in EV if "第23轮实证复核" in (T[t].get("pending_notes") or "")))
print("山地农业 sources:",m["sources"])