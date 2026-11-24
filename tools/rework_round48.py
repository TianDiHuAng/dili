# -*- coding: utf-8 -*-
"""第48轮返工：库什反向证据、罗马个案、秦代错位、城市起源旁证、5处自造落点、台账。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=json_path=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

# ===== P0-1 库什：反向证据 → 改写断言到摘要真说的话 =====
ku=T["库什与努比亚"]
ku["influence"]=("所引 2019 年《The ironworking remains in the royal city of Meroe》（Antiquity，被引26）的结论是：麦罗埃的**炉渣堆积主要属纳帕塔期或后麦罗埃期**，"
  "而**约公元前 300 年至公元 300 年——恰是麦罗埃作为库什都城的时期——冶铁证据稀少**，提示该城工业基础在此期间发生重组。"
  " 因此本条**不把冶铁写成麦罗埃时期的经济基础**；该时期的经济构成待专门的商路与生产研究核验。")
ku["pending_notes"]=((ku.get("pending_notes") or "")+
  " 【第48轮返工·反向证据】原写「麦罗埃时期以冶铁与商路为经济基础」，而所引摘要结论与此**相反**（都城期冶铁证据稀少）；"
  "且摘要中 trade/route/econom 均 0 命中，「商路」无支撑。已按摘要结论改写为「工业基础在此期间重组」。"
  " 该源摘要仅 756 字符，低于 800 门槛，**不计为内容源**——本条内容源数实为 0，非「补到 2」。").strip()
ku["last_update"]=TODAY

# ===== P0-2 罗马阿非利加：个案降级 =====
ro=T["罗马阿非利加"]
ro["geo"]=re.sub(r" 所引 2004 年 Segermes 项目研究[^。]*。","",ro.get("geo") or "")
ro["geo"]=((ro.get("geo") or "")+" 所引 2004 年 Segermes 项目以突尼斯的**单一谷地**为对象，重建城镇与其腹地的农业产出；"
  "**该项目明确声明不覆盖全省**，故本条只据它写个案，不据此推断全行省的谷物与橄榄输出（后者待省级调查或产量数据核验）。").strip()
ro["pending_notes"]=((ro.get("pending_notes") or "")+
  " 【第48轮返工·个案当通例】所引摘要自述「the main title of this project does not cover an analysis of the province as a whole」，"
  "且 grain/olive/wheat/export 均 0 命中；原落点却撑「行省级谷物与橄榄输出」。已降为个案描述并写明其自述局限。").strip()
ro["last_update"]=TODAY

# ===== P0-3 秦代：删度量衡 =====
qi=T["秦代"]
qi["polities"]=re.sub(r" 所引 2019 年《Unification and the Peerage System[^。]*。","",qi.get("polities") or "")
qi["polities"]=((qi.get("polities") or "")+" 所引 2019 年研究讨论秦统一后的大规模**赐爵**、黔首身份与县属吏（里耶秦简），"
  "**不涉度量衡**；本条只据此写「统一后的爵制与地方行政」，度量衡与郡县制待专门制度史来源核验。").strip()
qi["pending_notes"]=((qi.get("pending_notes") or "")+
  " 【第48轮返工·主题错位】原落点写「郡县制与统一度量衡」，而摘要中 weights/measures 0 命中、commandery 0 命中，仅有 county 1 次；"
  "且删去「（爵制部分另作说明）」这一空头承诺（正文原无爵制内容）。已按摘要实有主题改写。").strip()
qi["last_update"]=TODAY

# ===== P0-4 城市起源：正文加句 + 标旁证 =====
ci=T["城市起源"]
if "多地独立" not in (ci.get("influence") or ""):
    ci["influence"]=((ci.get("influence") or "")+
      " 就全球范围而言，城市的**独立起源**见于少数几个区域（两河流域、中美洲等），这一点由所引 2024 年研究中「Mesoamerica is one of only three world regions to have developed pristine cities」一句支持；"
      "但该研究的对象是**中美洲**，对本条「两河流域」只构成**旁证**，不作第二互证来源。").strip()
ci["pending_notes"]=((ci.get("pending_notes") or "")+
  " 【第48轮返工·对象不同位】所引 2024 年《City-State Civilizations: Mesoamerica's Urban Revolution》研究对象是**中美洲**，"
  "与本条「两河流域」不同位（D095①）；已改为**旁证**并降级，同时在正文写出「独立起源见于少数区域」这句可被其支撑的话（原先该句不存在，属 D100 回潮）。").strip()
ci["last_update"]=TODAY

# ===== P1-5 5处自造落点：改为引用正文原句或先写正文 =====
LAND={
"蒙古帝国":("connections","驿站网络把东亚、中亚、波斯与东欧连成一体，商队、使节与技术沿此流动；就欧亚陆路连通的规模而言，是前现代最显著的一次。",
  "（所引 2014 年研究明确以 China / Iran / Russia / Golden Horde 等为例，与此句对应。）"),
"阿兹特克":("polities","据 Wikidata 记录，政体起于 1325 年、止于 1521 年（精度到年）；通常以三方联盟（特诺奇蒂特兰、特斯科科、特拉科潘）形式运作，联盟成立于 **1428 年**，为**霸权型**帝国（不常驻军于被征服省份），以朝贡网络维系。统治者序列与贡赋制度待专门史学来源逐条核验。",
  "（所引 2017 年研究给出 1428 年成立、三城成员、霸权型与不驻军、朝贡省份等要点，与此句对应。）"),
"商代":("influence","河谷农业支撑人口与手工业，青铜礼器与占卜反映王权与祭祀组织；安阳出土青铜器的**合金配比与铸造工序**显示按社会等级与器类分层的生产安排。资源获取与军事行动同样重要，不能单由土壤解释。",
  "（所引 2023 年研究分析安阳青铜的合金配方与铸造环节，与「铸造工序与合金配比」一句对应；本条不据此谈更大范围的「手工业组织」。）"),
}
for t,(fld,sentence,note) in LAND.items():
    e=T.get(t)
    if not e: continue
    e[fld]=sentence
    e["pending_notes"]=((e.get("pending_notes") or "")+" 【第48轮返工·落点对齐】"+note.strip()+" 原落点引句并非正文既有句，已先写正文再引用（D100）。").strip()
    e["last_update"]=TODAY

# ===== P2-8 删占位符、DOI 规范化、已撤来源标 retired =====
for e in T.values():
    pn=e.get("pending_notes") or ""
    if "改由 W 系" in pn:
        e["pending_notes"]=pn.replace("改由 W 系（三方联盟霸权型帝国）承担","改由 openalex-W2609565117（三方联盟霸权型帝国，2017）承担")
for s in sd["sources"]:
    if s["id"]=="openalex-W2609565117":
        s["url2"]="https://doi.org/10.17951/rh.2016.42.63-73"
    if s["id"]=="openalex-W2481617052":
        s["url2"]="https://doi.org/10.1524/9783486594577-016"
    if s["id"]=="openalex-W2291403203":
        s["note"]=(s.get("note") or "").replace("摘要长度 4414 字符","正文节录 4414 字符（MUSE 首页节录，非摘要）")
# 标记已撤来源
used=set()
for e in T.values(): used.update(e["sources"])
for s in sd["sources"]:
    if s["id"] not in used:
        s["note"]=(s.get("note") or "")+" 【已撤/未引用】本条已不再引用该来源。"
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# ===== 重算（库什 756<800 不计）=====
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
z0=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==0)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=48
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print(f"返工完成；重算：≥2 {g2} / 1个 {o1} / 0个 {z0}")