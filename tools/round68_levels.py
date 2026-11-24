# -*- coding: utf-8 -*-
"""第68轮C：层级判定排除别名页/索引页（D071 的机器化）；重算真实层级。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

# 别名页/索引页：只提供「该对象存在」的入口，不含对象主题正文
ALIAS=("britannica-regions","wikipedia-regions","un-m49","ap-human-geo","s010-unesco-org")

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def grade(sid,e):
    if is_data(sid): return "data"
    if sid in ALIAS: return "alias"
    s=S.get(sid) or {}
    note=s.get("note") or ""
    seg=""
    for part in re.split(r"【", e.get("pending_notes") or ""):
        if sid in part: seg=part; break
    if any(k in seg for k in ("旁证","剔除","不作","降级")): return "side"
    if "证据强度：weak" in note: return "weak"
    if "证据强度：strong" in note: return "strong"
    mc=re.search(r"被引\s*(\d+)",note); cited=int(mc.group(1)) if mc else None
    ma=re.search(r"(?:摘要长度|正文节录|正文|摘要)\s*\*{0,2}([\d,]+)\s*字符",note)
    abslen=int(ma.group(1).replace(",","")) if ma else None
    mb=re.search(r"(\d{3,7})\s*字节",note); bytelen=int(mb.group(1)) if mb else None
    body=abslen if abslen is not None else bytelen
    if (cited is not None and cited>=10) or (body is not None and body>=800): return "strong"
    if (cited is not None and cited<10) or (body is not None and body<800): return "weak"
    return None

out={};summary={"A":[],"B":[],"C":[],"D":[]};alias_only=[]
for t,e in T.items():
    c={"strong":0,"weak":0,"side":0,"data":0,"alias":0,"unknown":0}
    for sid in e["sources"]: c[grade(sid,e) or "unknown"]+=1
    if c["strong"]>=2: lv="A"
    elif c["strong"]==1: lv="B"
    elif c["data"]>0 and c["side"]==0 and c["weak"]==0: lv="D"
    else: lv="C"
    out[t]={"level":lv,"counts":c,"tier":e["tier"]}
    summary[lv].append(t)
    if c["strong"]==0 and c["weak"]==0 and c["alias"]>0 and c["data"]==0:
        alias_only.append(t)
json.dump({"round":68,"levels":out,"summary":{k:len(v) for k,v in summary.items()},
 "alias_list":list(ALIAS),
 "fix":"第68轮：别名页/索引页（britannica-regions/wikipedia-regions/un-m49/ap-human-geo）不计为强来源——它们只证明对象存在，不含主题正文（D071 机器化,D135）",
 "alias_only_entries":alias_only},
 open(os.path.join(DATA,"evidence_level.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("修正后层级:",{k:len(v) for k,v in summary.items()})
print("仅别名页、无强/弱来源的条目:",len(alias_only))
for t in alias_only[:20]: print("  ",t)