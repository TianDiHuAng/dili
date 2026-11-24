# -*- coding: utf-8 -*-
"""第49轮：R19 人工扫描首批处置（5 条对象/学科错配）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

# ===== 1 罗马共和国：剔除（学科错配）=====
rr=T["罗马共和国"]
rid="openalex-W4408242507"
if rid in rr["sources"]: rr["sources"]=[s for s in rr["sources"] if s!=rid]
rr["geo"]=re.sub(r" 所引 2025 年《Integrating Sequence Stratigraphy[^。]*。","",rr.get("geo") or "")
rr["influence"]=re.sub(r" 所引 2025 年《Integrating Sequence Stratigraphy[^。]*。","",rr.get("influence") or "")
rr["pending_notes"]=re.sub(rf" 【第49轮[^】]*】{re.escape(rid)}[^【]*","",rr.get("pending_notes") or "")
rr["pending_notes"]=((rr.get("pending_notes") or "")+
  " 【第49轮剔除·学科错配】所引 W4408242507 是《Integrating Sequence Stratigraphy and Geostatistical Methods for 3D Lithofacies Modelling of the Tiber Alluvial Plain, Rome, Italy》（2025），"
  "研究对象是台伯河冲积平原的**三维岩相模型**（地质学），虽地理上在罗马，但学科与主题均不涉「罗马共和国的政体与扩张」。已剔除，相关落点句同删。").strip()
rr["last_update"]=TODAY

# ===== 2 汉代：降旁证 =====
ha=T["汉代"]
ha["pending_notes"]=((ha.get("pending_notes") or "")+
  " 【第49轮降旁证】所引 W4403972561 是《Dogs in Early Imperial China: Anthropo-Zoological Reading of Iconographic Sources from the Han Dynasty (206 BC-AD 220)》，"
  "标题含「汉代」与「前206–公元220」因而过了对象词检验，但主题是**汉代图像中的狗**（动物考古侧面），**不能支撑本条的疆域与行政叙述**。"
  "现降为**旁证**（仅可说明汉代有动物利用的图像材料），不作第二互证来源。").strip()
ha["last_update"]=TODAY

# ===== 3 植物物候变化：降旁证 =====
ph=T["植物物候变化"]
ph["pending_notes"]=((ph.get("pending_notes") or "")+
  " 【第49轮降旁证】所引 W7224996787 是《PhenoFECT: A Python package for forecasting and exploring plant phenology under climate change》，"
  "对象是**预测工具（软件包）**，不是物候变化的观测或机制。可作「已有工具化方法」的旁证，不作趋势断言的来源。").strip()
ph["last_update"]=TODAY

# ===== 4 北美冰盖：标明讨论通信 =====
na=T["北美冰盖"]
na["pending_notes"]=((na.get("pending_notes") or "")+
  " 【第49轮标明】所引 W2100185916 是《Comment and Reply on 'Keewatin Ice Sheet…'》（1980），属**学术讨论与答复**（Comment/Reply）而非研究论文；"
  "仅可说明「Keewatin 冰盖的范围存在学术争论」，不作冰盖范围的事实断言依据。").strip()
na["last_update"]=TODAY

# ===== 5 澳大利亚原住民：剔除 =====
ab=T["澳大利亚原住民"]
aid="openalex-W2260197586"
if aid in ab["sources"]: ab["sources"]=[s for s in ab["sources"] if s!=aid]
ab["pending_notes"]=re.sub(rf" 【第49轮[^】]*】{re.escape(aid)}[^【]*","",ab.get("pending_notes") or "")
ab["pending_notes"]=((ab.get("pending_notes") or "")+
  " 【第49轮剔除·对象错误】所引 W2260197586 是《Aboriginal Australians abroad 1606–1875》，对象是**19 世纪原住民板球队员的访英巡游**，"
  "与本条「适应干旱生态、语言与文化传统」无对应；已剔除。").strip()
ab["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=49
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
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
print(f"首批处置完成；重算 ≥2 {g2} / 1个 {o1} / 0个 {z0}")