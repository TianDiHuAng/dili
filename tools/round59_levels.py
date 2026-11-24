# -*- coding: utf-8 -*-
"""第59轮：计算每条目证据层级（A强/B中/C弱/D数据类），写入 data/evidence_level.json。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def grade_of(sid,e):
    """返回 'strong' / 'weak' / 'side' / 'data' / None"""
    if is_data(sid): return "data"
    s=S.get(sid) or {}
    note=s.get("note") or ""
    pn=e.get("pending_notes") or ""
    idx=pn.find(sid); seg=pn[max(0,idx-160):idx+90] if idx>=0 else ""
    # 备注中已标旁证/弱来源/剔除 → side
    if any(k in seg for k in ("旁证","剔除","不作","降级")):
        return "side"
    if "证据强度：weak" in note or "补弱来源" in seg:
        return "weak"
    if "证据强度：strong" in note or "补主来源" in seg:
        return "strong"
    # 未标注：按被引与摘要长度粗判
    m=re.search(r"被引\s*(\d+)",note); cited=int(m.group(1)) if m else None
    a=re.search(r"(?:摘要长度|正文|摘要)\s*\*{0,2}([\d,]+)\s*字符",note)
    abslen=int(a.group(1).replace(",","")) if a else None
    if cited is not None and cited>=10 and (abslen is None or abslen>=800):
        return "strong"
    if cited is not None and cited<10:
        return "weak"
    if abslen is not None and abslen>=800:
        return "strong"
    return None

out={}
summary={"A":[],"B":[],"C":[],"D":[]}
for t,e in T.items():
    counts={"strong":0,"weak":0,"side":0,"data":0,"unknown":0}
    for sid in e["sources"]:
        g=grade_of(sid,e)
        counts[g if g else "unknown"]+=1
    if counts["strong"]>=2: level="A"
    elif counts["strong"]==1: level="B"
    elif counts["data"]>0 and counts["strong"]==0 and counts["weak"]==0: level="D"
    else: level="C"
    out[t]={"level":level,"counts":counts,"tier":e["tier"]}
    summary[level].append(t)

json.dump({"round":59,"levels":out,"summary":{k:len(v) for k,v in summary.items()},
  "definition":{
   "A":"≥2 个强来源（被引≥10 且正文/摘要≥800 字符，或明确标 strong）",
   "B":"1 个强来源 + 旁证/弱来源",
   "C":"无强来源，仅弱来源或旁证",
   "D":"仅数据端点（世界银行/NOAA 等指标）与机构页——指标解读类"}},
  open(os.path.join(DATA,"evidence_level.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("证据层级分布:",{k:len(v) for k,v in summary.items()})
print("\nA 级示例:",summary["A"][:8])
print("C 级全部:",summary["C"])
print("D 级示例:",summary["D"][:10])