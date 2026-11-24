# -*- coding: utf-8 -*-
"""第62轮：建立 data/side_evidence.json（侧面文献结构化）+ 重定义缺口维度。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}

def segs(e):
    return [s for s in re.split(r"【", e.get("pending_notes") or "") if s.strip()]

side=[];dropped=[];weakclaim=[]
for t,e in T.items():
    for seg in segs(e):
        head=seg.split("】")[0] if "】" in seg else seg[:30]
        body=seg.split("】",1)[1] if "】" in seg else seg
        sids=re.findall(r"(openalex-[A-Za-z0-9]+|[a-z]{2,10}-[a-z0-9\-]{2,})", body)
        rec={"entry":t,"kind":None,"sids":sids,"note":body.strip()[:260]}
        if any(k in head for k in ("旁证认定","侧面","降旁证")):
            rec["kind"]="side"; side.append(rec)
        elif any(k in head for k in ("剔除","对象碰撞","错源","撤回","学科错配")):
            rec["kind"]="dropped"; dropped.append(rec)
        elif any(k in head for k in ("补弱来源","D112降级")):
            rec["kind"]="weak_claim"; weakclaim.append(rec)
out={"round":62,"date":TODAY,
 "definition":{"side":"对象同一但只涉一个侧面的来源（降为旁证）",
   "dropped":"对象/时期/学科错配，已撤出的来源",
   "weak_claim":"被引≤5 或 正文<800 的来源（不得称主来源）"},
 "counts":{"side":len(side),"dropped":len(dropped),"weak_claim":len(weakclaim)},
 "side":side,"dropped":dropped,"weak_claim":weakclaim}
json.dump(out,open(os.path.join(DATA,"side_evidence.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("side_evidence.json:",out["counts"])

# 重定义缺口维度：只保留「仍未达成且可陈述」的项
gaps=[]
# 1 主来源缺口：A/B 级为有强来源；C/D 或已记录无合格主来源者
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
for t,v in ev["levels"].items():
    if v["level"] in ("C","D"):
        gaps.append({"entry":t,"gap":"主来源","detail":f"层级 {v['level']}（{v['counts']}）"})
# 2 已记录无合格主来源者
NOFIX=("河中地区","库什与努比亚","莫切文化")
for t in NOFIX:
    e=T.get(t)
    if not e: continue
    if not any(g["entry"]==t for g in gaps):
        gaps.append({"entry":t,"gap":"主来源（检索确认无解）","detail":"见 limits.html"})
# 3 内容源仅 1 个者
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or "", e.get("pending_notes") or ""]
    for note in notes:
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
one=[t for t,e in T.items() if sum(1 for s in e["sources"] if hb(s,e) is True)==1]
out2={"round":62,"date":TODAY,
 "gap_definitions":[
   {"id":"G1","name":"无强来源（C/D 级）","count":len([g for g in gaps if g["gap"]=="主来源"]),
    "fixed_by":"补一条被引≥10 或正文≥800 的来源"},
   {"id":"G2","name":"检索确认无合格主来源","count":len(NOFIX),
    "fixed_by":"仅待新文献出现；不再重试同类检索"},
   {"id":"G3","name":"内容源仅 1 个（需第二互证）","count":len(one),
    "fixed_by":"补第二内容源，须过 R19/R20/R22"},
   {"id":"G4","name":"语义对题未经机器校验","count":243,
    "fixed_by":"人工逐条扫描（不可自动化）"}],
 "gaps":gaps,"one_source_entries":one}
json.dump(out2,open(os.path.join(ROOT,"reports","round62_gaps.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("缺口定义：",{d["id"]:d["count"] for d in out2["gap_definitions"]})
print("G1 明细:",[g["entry"] for g in gaps if g["gap"]=="主来源"])