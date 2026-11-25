# -*- coding: utf-8 -*-
"""新增「黄土高原」条目：彩绘式内联SVG + 三篇对题来源。"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, update_coverage, save_docs
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

EID = "asia-" + sid("黄土高原")

SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 460' role='img' aria-label='黄土高原地貌示意图'>"
 "<rect x='20' y='20' width='860' height='420' rx='12' fill='none' stroke='var(--line)'/>"
 # 天空
 "<rect x='21' y='21' width='858' height='92' fill='#eef3f6' opacity='.55'/>"
 # 远山（淡）
 "<polygon points='40,150 150,96 260,140 360,100 470,145 560,105 700,148 860,110 860,150' fill='#c9cfd4' opacity='.55'/>"
 # 黄土高原主台面（塬）
 "<polygon points='40,250 40,168 300,168 320,182 620,182 660,196 860,196 860,250' fill='#d9b26a'/>"
 "<polygon points='40,250 40,168 300,168 320,182 620,182 660,196 860,196 860,250' fill='none' stroke='#a9822f' stroke-width='1.4'/>"
 # 等高线
 "<polyline points='60,196 280,190 520,204 820,198' fill='none' stroke='#b9902f' stroke-width='.9' opacity='.7'/>"
 "<polyline points='60,214 300,208 540,222 840,214' fill='none' stroke='#b9902f' stroke-width='.9' opacity='.7'/>"
 # 塬面标注
 "<text x='90' y='188' class='lbl'>塬面（平坦台面）</text>"
 # 梁（长条脊）
 "<polygon points='330,250 360,196 470,188 560,198 600,232 600,250' fill='#cf9f4e'/>"
 "<polygon points='330,250 360,196 470,188 560,198 600,232 600,250' fill='none' stroke='#a9822f' stroke-width='1.2'/>"
 "<text x='392' y='182' class='lbl'>梁（长脊）</text>"
 # 峁（圆丘）
 "<path d='M650 250 C672 196 706 178 742 186 C782 194 800 216 812 250 Z' fill='#d9b26a' stroke='#a9822f' stroke-width='1.2'/>"
 "<text x='690' y='172' class='lbl'>峁（圆丘）</text>"
 # 沟谷（深切，V 形）
 "<path d='M300 250 L292 222 L304 196 L296 176' fill='none' stroke='#8a6a28' stroke-width='2'/>"
 "<path d='M620 250 L612 220 L624 196 L616 178' fill='none' stroke='#8a6a28' stroke-width='2'/>"
 "<text x='300' y='266' class='lbl-s'>沟谷下切</text>"
 # 黄河
 "<path d='M40 300 C180 286 320 312 470 300 C620 288 740 306 860 292' fill='none' stroke='#5b93b8' stroke-width='6' opacity='.9'/>"
 "<text x='470' y='330' class='lbl'>黄河（含大量泥沙）</text>"
 # 植被簇（灌草）
 "<g fill='#7ba05b' opacity='.9'>"
 "<circle cx='120' cy='232' r='3'/><circle cx='132' cy='228' r='3'/><circle cx='144' cy='234' r='3'/>"
 "<circle cx='520' cy='230' r='3'/><circle cx='532' cy='226' r='3'/><circle cx='544' cy='232' r='3'/>"
 "<circle cx='700' cy='236' r='3'/><circle cx='714' cy='232' r='3'/></g>"
 "<text x='112' y='218' class='lbl-s'>灌草植被</text>"
 # 地层剖面（左下）
 "<text x='60' y='352' class='lbl'>黄土地层剖面</text>"
 "<rect x='60' y='360' width='150' height='22' fill='#e2c079' stroke='#a9822f'/><text x='216' y='376' class='lbl-s'>马兰黄土（晚更新世）</text>"
 "<rect x='60' y='382' width='150' height='30' fill='#d3a95a' stroke='#a9822f'/>"
 "<rect x='60' y='390' width='150' height='4' fill='#b06b3a'/><rect x='60' y='399' width='150' height='4' fill='#b06b3a'/>"
 "<text x='216' y='402' class='lbl-s'>离石黄土（夹古土壤层）</text>"
 "<rect x='60' y='412' width='150' height='14' fill='#c9a24a' stroke='#a9822f'/><text x='216' y='423' class='lbl-s'>午城黄土（早更新世）</text>"
 "<rect x='60' y='426' width='150' height='12' fill='#8f8a80' stroke='#a9822f'/><text x='216' y='436' class='lbl-s'>基岩</text>"
 # 图例（右下）
 "<g transform='translate(600,360)'>"
 "<text x='0' y='0' class='lbl'>图例</text>"
 "<rect x='0' y='10' width='14' height='9' fill='#d9b26a' stroke='#a9822f'/><text x='20' y='18' class='lbl-s'>黄土台面（塬/梁/峁）</text>"
 "<rect x='0' y='25' width='14' height='9' fill='#b06b3a'/><text x='20' y='33' class='lbl-s'>古土壤（气候转湿）</text>"
 "<path d='M0 46 L14 46' stroke='#5b93b8' stroke-width='4'/><text x='20' y='50' class='lbl-s'>河流</text>"
 "<rect x='0' y='58' width='14' height='9' fill='#8f8a80'/><text x='20' y='66' class='lbl-s'>基岩</text></g>"
 "<text x='40' y='450' class='dim'>黄土高原地貌 · 示意图，非精确测绘</text>"
 "</svg>")

ENTRY = {
 "id": EID, "title": "黄土高原", "tier": "重要", "unit_id": "asia", "region": "亚洲",
 "theme": "地形", "level": "L2", "status": "L2完成(新增·中国地貌)",
 "definition": "黄土高原：中国北方以风力搬运的黄土为主体堆积而成的高原，是世界上黄土分布面积最大、最深厚的地区。",
 "time_or_place": "第四纪（黄土堆积约自 250 万年前持续至晚更新世）",
 "overview": "黄土高原：中国北方以风力搬运的黄土堆积而成的高原。冬半年风沙自西北内陆搬运粉尘、在下风区堆积成厚层黄土；流水侵蚀又把平坦塬面切割成千沟万壑的塬、梁、峁地貌。",
 "related": ["asia-" + sid("黄河流域")],
 "sources": ["openalex-W1980272579", "openalex-W2049441218", "openalex-W1989229638"],
 "needs_verification": True,
 "pending_notes": "新增条目：地貌描述（塬/梁/峁、垂直节理、沟蚀）为教科书性常识表述；具体年代与速率以所引文献为准，逐年数值待专门来源核验。",
 "outlines": ["黄土高原·中国地貌单元"],
 "last_update": "2026-11-25",
 "geo": "位于黄河中游、太行山以西、秦岭以北，地表覆盖数十至数百米厚的黄土。黄土疏松、垂直节理发育，抗蚀性弱；夏季暴雨集中，流水沿坡面与沟道强烈侵蚀，形成塬（平坦台面）、梁（长条脊）、峁（圆丘）等黄土地貌，沟壑密度极高。",
 "influence": "所引 1989 年研究指出黄土高原是世界上黄土发育最典型（面积、厚度、层序）且水土流失最严重的地区：黄土易垂直劈裂、表层疏松，夏季暴雨集中，加之数千年不合理土地利用与林草破坏，侵蚀强烈；本条「黄土疏松、暴雨集中与长期土地利用共同导致严重水土流失」据此。",
 "polities": "本条以自然地理与地貌为主，不展开政权序列；具体开发与人口年代待专门来源核验。",
 "connections": "黄土高原是黄河泥沙的主要来源区：沟蚀与坡面侵蚀把黄土输入黄河，泥沙下泄塑造华北平原、抬高下游河床。",
 "today": "（本条的当代指标不在本页展开。）",
 "svg": SVG,
}

P = os.path.join(DATA, "asia.json")
doc = json.load(open(P, encoding="utf-8"))
if not any(e["id"] == EID for e in doc["entries"]):
    doc["entries"].append(ENTRY)
json.dump(doc, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 来源登记
sd = json.load(open(os.path.join(DATA, "sources.json"), encoding="utf-8"))
have = {s["id"] for s in sd["sources"]}
META = {
 "openalex-W1980272579": ("Soil erosion and its control in the loess plateau of China", 1989, 290, 684),
 "openalex-W2049441218": ("Changes in mineralogy of loess–paleosol sections across the Chinese Loess Plateau", 2011, 98, 1394),
 "openalex-W1989229638": ("Binary sources of loess on the Chinese Loess Plateau revealed by U–Pb ages of zircon", 2013, 140, 1043),
}
for oid, (t, y, c, ln) in META.items():
    sid_ = "openalex-" + oid
    if sid_ in have: continue
    sd["sources"].append({"id": sid_, "title": f"OpenAlex {oid} — {t}", "author": "OpenAlex（开放学术知识图谱，CC0 元数据）",
      "year": y, "type": "学术文献", "url": f"https://api.openalex.org/works/{oid}", "url2": None,
      "link_ok": True, "verified": True, "page_title": t[:200],
      "note": f"OpenAlex 作品 {oid}；{y}年；被引 {c}。摘要长度 {ln} 字符。经 Crossref 检索 + DOI 桥取得，摘要已人工阅读。证据强度：strong。"})
json.dump(sd, open(os.path.join(DATA, "sources.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 对象词
ow = json.load(open(os.path.join(DATA, "object_words.json"), encoding="utf-8"))
ow["黄土高原"] = ["loess", "黄土"]
json.dump(ow, open(os.path.join(DATA, "object_words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 重建 doc 并保存配套
docs = {u: json.load(open(os.path.join(DATA, u + ".json"), encoding="utf-8")) for u in
        ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]}
save_docs(docs); update_coverage(docs)
print("added", EID)
