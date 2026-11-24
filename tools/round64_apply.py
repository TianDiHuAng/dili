# -*- coding: utf-8 -*-
"""第64轮B：标记空壳页（不作正文依据），重算 G3；为可复用条目挂上真长文。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

SHELL={"s004-population-un-org":26,"s008-unesco-org":218,"s014-fao-org":7,"s085-unesco-org":218,
 "s072-cbd-int":172,"s074-unicef-org":750}   # <800 → 仅入口页
for sid,n in SHELL.items():
    s=S.get(sid)
    if not s: continue
    if "【空壳页判定】" in (s.get("note") or ""): continue
    s["note"]=(s.get("note") or "")+f" 【空壳页判定】strip 后仅 {n} 字符（多为 JS 应用壳或导航条），**仅作入口页，不作正文依据**（D125）。"
print("标记空壳页:",len(SHELL))

# 重算 G3
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    if is_data(sid): return False
    for note in [(S.get(sid) or {}).get("note") or "", e.get("pending_notes") or ""]:
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
one=[(t,e) for t,e in T.items() if sum(1 for s in e["sources"] if hb(s,e) is True)==1]
print("G3 现状:",len(one))

# 为这些条目挂上可复用的真长文（OWID / World Bank / NOAA / IUCN 等已实测≥800）
CAND={
"人口增长":["s023-ourworldindata-org","s032-ourworldindata-org"],
"人口年龄结构":["s032-ourworldindata-org","s023-ourworldindata-org"],
"全球人口规模":["s023-ourworldindata-org"],
"预期寿命空间差异":["s032-ourworldindata-org"],
"作物单产差异":["s019-fao-org"],
"农业统计体系":["s059-worldbank-org"],
"农业企业与价值链":["s059-worldbank-org"],
"保护与保育区体系":["s091-iucn-org"],
"海洋生态系统":["s050-oceanservice-noaa-gov"],
"教育机会地域差异":["s085-unesco-org"],
}
addn=0
for t,sids in CAND.items():
    e=T.get(t)
    if not e: continue
    for sid in sids:
        if sid in e["sources"]: continue
        n=hb(sid,e)
        if n is not True: continue
        e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
        e["pending_notes"]=((e.get("pending_notes") or "")+
          f" 【第64轮补第二来源】{sid}（已实测正文≥800 字符的机构/数据长文）：作用是为本条的空间差异描述提供第二个独立来源，不作因果断言依据。").strip()
        e["last_update"]=TODAY;addn+=1
print("挂接第二来源:",addn)

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=64
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
one2=[t for t,e in T.items() if sum(1 for s in e["sources"] if hb(s,e) is True)==1]
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
print(f"重算：≥2 {g2} / 1个 {len(one2)}")
print("仍仅1源:",one2)