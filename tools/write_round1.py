# -*- coding: utf-8 -*-
"""阶段3/4 第1轮：把 40 条骨架标为 L1 完成；把 2 个样板升级到 L2；填充相关条目。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UNITS = ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

with open(os.path.join(DATA, "sources.json"), encoding="utf-8") as f:
    sources = {s["id"]: s for s in json.load(f)["sources"]}

docs = {}
for uid in UNITS:
    with open(os.path.join(DATA, uid + ".json"), encoding="utf-8") as f:
        docs[uid] = json.load(f)

entries = {e["id"]: e for d in docs.values() for e in d["entries"]}
by_title = {e["title"]: e for e in entries.values()}

# 相关条目：同单元同主题优先，补足同单元其他条目，最多3条
for uid, d in docs.items():
    es = d["entries"]
    for e in es:
        same_theme = [x["id"] for x in es if x["id"] != e["id"] and x["theme"] == e["theme"]][:2]
        others = [x["id"] for x in es if x["id"] != e["id"] and x["id"] not in same_theme][:2]
        e["related"] = (same_theme + others)[:3]

# 第1轮处理配额：按 核心→重要 顺序取前 40 条（跨单元轮转，保证覆盖面）
order = {"核心":0,"重要":1,"补充":2}
pool = sorted(entries.values(), key=lambda e: (order[e["tier"]], UNITS.index(e["unit_id"]), e["title"]))
round1 = pool[:40]
for e in round1:
    e["status"] = "L1完成"

# ---- L2 样板 1：尼罗河谷 ----
nile = next(e for e in entries.values() if e["title"] == "尼罗河谷")
nile["level"] = "L2"
nile["status"] = "L2完成"
nile["geo"] = "尼罗河谷沿尼罗河两岸展开，上游为狭窄的侵蚀谷，下游为广阔的冲积平原与三角洲。流域跨越东非高原与撒哈拉沙漠边缘，气候从热带草原过渡到干旱沙漠，降水高度季节化。水系以尼罗河干流为轴，支流与泛滥平原构成灌溉与交通基础；资源包括肥沃冲积土、芦苇、鱼类与石材。"
nile["influence"] = "学界较普遍的看法是，尼罗河季节性泛滥带来的肥沃淤泥与可预测的耕作周期，降低了早期定居农业的风险，支撑人口密集与剩余产品积累，进而有利于国家组织与大型工程。需要强调的是，这是地理条件影响社会发展的一种解释方式，不是地理决定论式定论；灌溉管理到底是原因还是结果，学界仍有讨论。"
nile["polities"] = "早王朝与古王国以孟菲斯为中心，中王国与新王国先后兴起，底比斯成为南部宗教与政治重心；其后努比亚、托勒密与罗马时期延续了对河谷与三角洲的控制。政权更替与尼罗河运输、灌溉和粮税体系密切相关。"
nile["connections"] = "尼罗河谷通过三角洲与地中海世界相连，通过上游努比亚与中非的黄金、象牙贸易通道相接，并经红海与西奈通向西亚。交流内容包括石材、金属、粮食、宗教观念与工艺技术。"
nile["today"] = "今天河谷与三角洲仍是埃及人口与农业最密集的区域。具体人口、耕地面积与用水数据随年份变化，本站不在此写具体数值，待以权威统计机构数据补齐并标注年份与来源。"
nile_svg = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='尼罗河谷示意图'>
<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>
<path d='M60 90 C 170 70 260 110 340 150 C 430 195 500 240 560 300 C 600 335 650 350 700 350' fill='none' stroke='var(--accent)' stroke-width='3' stroke-dasharray='6 5'/>
<path d='M300 45 C 310 110 330 160 340 210 C 350 260 360 300 365 352' fill='none' stroke='var(--accent)' stroke-width='6'/>
<path d='M365 352 L 340 382 M365 352 L 390 382 M365 352 L 365 385' fill='none' stroke='var(--accent)' stroke-width='4'/>
<circle cx='345' cy='205' r='6' class='pt'/><text x='360' y='210' class='lbl'>底比斯</text>
<circle cx='360' cy='300' r='6' class='pt'/><text x='375' y='305' class='lbl'>孟菲斯</text>
<circle cx='365' cy='365' r='5' class='pt'/><text x='380' y='370' class='lbl'>三角洲</text>
<text x='55' y='60' class='lbl'>撒哈拉</text><text x='600' y='70' class='lbl'>红海</text>
<text x='40' y='385' class='dim'>示意图，非精确测绘</text>
</svg>"""
nile["svg"] = nile_svg
nile_sources = ["br-nile","wk-nile","br-egypt","wk-egypt"]
nile["sources"] = [s for s in nile_sources if s in sources]
nile["needs_verification"] = any(not sources[s]["verified"] for s in nile["sources"])
nile["pending_notes"] = "暂无待核实关键事实；具体人口与耕地数值待按年份与权威统计来源补齐。" if not nile["needs_verification"] else "部分来源未通过联网核验；具体人口与耕地数值待权威统计机构补齐。"

# ---- L2 样板 2：黄河流域 ----
yellow = next(e for e in entries.values() if e["title"] == "黄河流域")
yellow["level"] = "L2"
yellow["status"] = "L2完成"
yellow["geo"] = "黄河发源于青藏高原，东流经过黄土高原与华北平原，最终注入渤海。中游流经黄土区，河流含沙量高，下游形成地上河与冲积平原。流域跨越干旱、半干旱与温带季风气候区，降水集中于夏季，水旱灾害风险长期存在。"
yellow["influence"] = "一种常见解释认为，黄土易于耕作、河谷与平原适宜粟作农业，加上对治水与灌溉的协作需求，有利于早期聚落密集与政权组织。这是影响机制的一种分析框架，不能据此断定环境必然导致特定政治形态；治水与国家形成的关系在学界仍有争论。"
yellow["polities"] = "仰韶、龙山等史前文化之后，商周在黄河中下游兴起；秦汉以降，长安—洛阳一线长期是政治重心。中古以后经济重心逐渐南移，但黄河流域仍具政治与交通意义。"
yellow["connections"] = "黄河流域通过河西走廊与中亚相连，通过大运河与长江流域整合，并通过陆上与海上交通同朝鲜半岛、日本及东南亚互动。技术、作物、宗教与制度沿这些通道传播。"
yellow["today"] = "黄河流域如今仍是重要农业与人口密集区。水资源分配、泥沙治理与生态修复是长期议题；具体人口、灌溉面积与径流量数据待按年份和权威来源补齐。"
yellow_svg = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='黄河流域示意图'>
<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>
<path d='M70 120 C 140 110 200 150 270 175 C 350 205 420 230 500 250 C 570 268 630 285 690 300' fill='none' stroke='var(--accent)' stroke-width='5'/>
<path d='M270 175 C 300 210 330 250 350 300 C 370 340 390 360 420 370' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='5 4'/>
<circle cx='100' cy='122' r='6' class='pt'/><text x='115' y='126' class='lbl'>上游源区</text>
<circle cx='320' cy='195' r='6' class='pt'/><text x='335' y='200' class='lbl'>长安</text>
<circle cx='480' cy='247' r='6' class='pt'/><text x='495' y='251' class='lbl'>洛阳</text>
<circle cx='675' cy='297' r='6' class='pt'/><text x='620' y='285' class='lbl'>渤海</text>
<text x='45' y='60' class='lbl'>青藏高原</text><text x='330' y='345' class='lbl'>黄土高原</text>
<text x='40' y='385' class='dim'>示意图，非精确测绘</text>
</svg>"""
yellow["svg"] = yellow_svg
yellow_sources = ["br-yellow-river","wk-yellow-river","br-china","wk-china"]
yellow["sources"] = [s for s in yellow_sources if s in sources]
yellow["needs_verification"] = any(not sources[s]["verified"] for s in yellow["sources"])
yellow["pending_notes"] = "暂无待核实关键事实；具体人口、径流量与灌溉面积待按年份与权威来源补齐。" if not yellow["needs_verification"] else "部分来源未通过联网核验；具体数据待权威统计机构补齐。"

# 保存单元文件
for uid, d in docs.items():
    with open(os.path.join(DATA, uid + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# 更新 coverage.json
with open(os.path.join(DATA, "coverage.json"), encoding="utf-8") as f:
    cov = json.load(f)
for c in cov["entries"]:
    e = entries[c["id"]]
    c["level"] = e["level"]
    c["status"] = e["status"]
    c["source_count"] = len(e["sources"])
    c["pending_count"] = 1 if e.get("needs_verification") else 0
    c["last_update"] = "2026-11-22"
cov["updated"] = "2026-11-22"
cov["round"] = 1
cov["round_processed"] = len(round1)
with open(os.path.join(DATA, "coverage.json"), "w", encoding="utf-8") as f:
    json.dump(cov, f, ensure_ascii=False, indent=2)

print(f"第1轮处理 {len(round1)} 条；L2 样板 2 条；相关链接已填充")
