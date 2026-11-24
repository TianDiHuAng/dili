# -*- coding: utf-8 -*-
"""第60轮B：修证据层级的「段污染」bug（按【】分段判定）+ 放宽 D 判据 + 重算。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def seg_for(sid,e):
    """按【】分段：返回包含该 sid 的那一段（避免相邻来源的字样污染）。"""
    pn=e.get("pending_notes") or ""
    for seg in re.split(r"【", pn):
        if sid in seg: return seg
    return ""
def grade_of(sid,e):
    if is_data(sid): return "data"
    s=S.get(sid) or {}
    note=s.get("note") or ""
    seg=seg_for(sid,e)
    # 只在该 sid 自己的段落里判断旁证/弱/强
    if any(k in seg for k in ("旁证","剔除","不作","降级")): return "side"
    if "证据强度：weak" in note: return "weak"
    if "证据强度：strong" in note: return "strong"
    m=re.search(r"被引\s*(\d+)",note); cited=int(m.group(1)) if m else None
    a=re.search(r"(?:摘要长度|正文节录|正文|摘要)\s*\*{0,2}([\d,]+)\s*字符",note)
    abslen=int(a.group(1).replace(",","")) if a else None
    b=re.search(r"(\d{3,7})\s*字节",note); bytelen=int(b.group(1)) if b else None
    body=abslen if abslen is not None else bytelen
    if (cited is not None and cited>=10) or (body is not None and body>=800): return "strong"
    if (cited is not None and cited<10) or (body is not None and body<800): return "weak"
    return None

out={};summary={"A":[],"B":[],"C":[],"D":[]}
for t,e in T.items():
    c={"strong":0,"weak":0,"side":0,"data":0,"unknown":0}
    for sid in e["sources"]:
        g=grade_of(sid,e); c[g if g else "unknown"]+=1
    # D 判据放宽：有数据端点、无强来源、无旁证 → 指标解读类（允许存在 weak 机构页）
    if c["strong"]>=2: lv="A"
    elif c["strong"]==1: lv="B"
    elif c["data"]>0 and c["side"]==0: lv="D"
    else: lv="C"
    out[t]={"level":lv,"counts":c,"tier":e["tier"]}
    summary[lv].append(t)
json.dump({"round":60,"levels":out,"summary":{k:len(v) for k,v in summary.items()},
 "definition":{"A":"≥2 强来源","B":"1 强来源","C":"无强来源","D":"仅数据端点+机构页（指标解读类）"},
 "fix":"第60轮修：层级判定按【】分段，避免相邻来源的『剔除/旁证』字样污染；D 判据放宽为 data>0 且 side==0"},
 open(os.path.join(DATA,"evidence_level.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("重算分布:",{k:len(v) for k,v in summary.items()})
print("C 级:",summary["C"])
print("D 级:",summary["D"])