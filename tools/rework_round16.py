# -*- coding: utf-8 -*-
"""第16轮返工：
1) 阿契美尼德波斯：五段收敛到 Livius Cyrus 实证范围，删驿道/三大洲/度量衡/印度河征服断言，移除无关 s013；
2) 命中数统一为 D044 剥离口径 62；
3) 8 条新增 L1：outlines 按实际来源回填；theme 保持枚举并在 pending 注明实际维度；
4) 壳页来源（s014/s057/wikipedia-regions）在 sources.json 加"仅作入口"标注。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条只写可核验的政治与地理背景；具体年代、王表与制度细节待专门史料核验。"
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 阿契美尼德波斯：收敛
a=T["阿契美尼德波斯"]
a.update({
 "definition":"阿契美尼德波斯：以伊朗高原为腹地的古代帝国，居鲁士与大流士时期扩展到两河、安纳托利亚、埃及与中亚边缘。",
 "overview":"以伊朗高原为腹地的古代帝国，居鲁士与大流士时期扩展到两河、安纳托利亚、埃及与中亚边缘。",
 "geo":"帝国腹地位于伊朗高原，与两河流域、安纳托利亚、埃及和中亚边缘相接。高原、沙漠与山口影响行军路线与区域联系，具体交通网络细节待专门史料核验。",
 "influence":"跨区域的整合依赖军事组织、地方统治安排与交通条件；地理距离与地形是重要约束，但政治制度与治理方式同样是关键变量。",
 "polities":"Livius 的居鲁士专题页记载其兴起、巴比伦与安纳托利亚等地的扩张，并述及地方统治者（satrap）的安排；王表与年代序列待专门史料逐条核验。",
 "connections":"帝国与两河流域、安纳托利亚、埃及及中亚边缘存在军事与行政联系；对印度河谷的控制不成立，相关说法已删除。",
 "sources":["livius-cyrus","livius-mesopotamia"],
 "status":"二次返工收敛(第16轮)",
 "pending_notes":"第16轮二次返工：原五段含「驿道与行省制度」「横跨三大洲」「度量衡交流」「连接印度河」等 Livius Cyrus 页无支撑（road/province/plateau/africa/europe 命中均为 0；indus 处原文明确未征服印度河谷），已删改；移除与主题无关的 s013（AQUASTAT）。专题页 D044 剥离口径：正文 9220 字符、正则 achaemenid|cyrus|persia 命中 62。政权年代与制度细节待专门史料。",
 "last_update":TODAY})

# 2) outlines 回填 + theme 说明（8 条新增）
OUT={
 "拉丁美洲与加勒比区域发展":["World Bank Latin America and the Caribbean 区域页","World Bank DataBank WDI"],
 "中东与北非区域发展":["World Bank MENA 区域页","World Bank DataBank WDI"],
 "南亚区域发展":["World Bank South Asia 区域页","World Bank DataBank WDI"],
 "全球气温距平":["NOAA Climate.gov 全球温度页","Our World in Data Climate Change"],
 "二氧化碳排放清单":["Our World in Data CO₂ emissions","Our World in Data Annual CO₂ emissions"],
 "保护与保育区体系":["CBD Protected and Conserved Areas","IUCN Protected areas and land use"],
 "农业企业与价值链":["World Bank Farming and Agribusiness","FAOSTAT"],
 "水资源供给概览":["FAO Water overview","FAO AQUASTAT"],
}
for t,ol in OUT.items():
 e=T[t]
 e["outlines"]=ol
 e["pending_notes"]=(e["pending_notes"] or "")+" 来源分级：首条为专题/主题页，次条为机构或数据入口页（部分为应用壳页，仅作入口）。theme 受现有枚举限制，实际维度见 region/主题注释。"

# theme 注释：水资源→地形、保护区→区域（枚举限制），写入 pending 说明
T["水资源供给概览"]["pending_notes"]=T["水资源供给概览"]["pending_notes"]+" 本条实际维度为水文/水资源，theme 因枚举限制标为「地形」。"
T["保护与保育区体系"]["pending_notes"]=T["保护与保育区体系"]["pending_notes"]+" 本条实际维度为生态/环境治理，theme 因枚举限制标为「区域」。"

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 3) 壳页标注
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
SHELL={'s014-fao-org':'第16轮核验补充：剥离 chrome 后可视正文约 9 字符，为应用壳页，仅作入口，不作正文依据。',
 's057-databank-worldbank-org':'第16轮核验补充：剥离 chrome 后可视正文约 41 字节，为应用壳页，仅作入口，不作正文依据。',
 'wikipedia-regions':'第16轮核验补充：该别名为 UN SDG 数据门户壳页（正文约 7 字节），仅作入口，不作正文依据。',
 's072-cbd-int':'第16轮核验补充：剥离 nav/footer 后正文约 176 字节，门户页形态，仅作入口，不作正文依据。',
 's013-fao-org':'第16轮核验补充：正文约 900 字节门户页，仅作入口；不用于跨主题断言（第16轮已从阿契美尼德波斯移除）。',
 's017-fao-org':'第16轮核验补充：正文约 3417 字节主题概览页；仅用于水资源相关条目，不得泛贴其他主题。'}
for s in sd["sources"]:
 if s["id"] in SHELL and "第16轮核验补充" not in (s.get("note") or ""):
  s["note"]=(s.get("note") or "")+" "+SHELL[s["id"]]
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("阿契美尼德收敛；outlines 回填 8 条；壳页标注",len(SHELL))