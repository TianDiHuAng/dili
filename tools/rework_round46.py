# -*- coding: utf-8 -*-
"""第46轮返工A：撤回日本列岛错源、回写实测字符数、hb 双读、重算五分类。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

# ===== A 撤回日本列岛错源（哥伦比亚侏罗纪火山） =====
jp=T["日本列岛"]
BAD="openalex-W2319079898"
if BAD in jp["sources"]: jp["sources"]=[s for s in jp["sources"] if s!=BAD]
jp["influence"]=re.sub(r" [^。]*所引[^。]*第46轮补源[^。]*。","",jp.get("influence") or "")
jp["pending_notes"]=re.sub(rf" 【第46轮补源[^】]*】{re.escape(BAD)}[^【]*","",jp.get("pending_notes") or "")
jp["pending_notes"]=((jp.get("pending_notes") or "")+
  " 【第46轮返工·撤回错源】所引 W2319079898 实为《Jurassic Silicic Volcanism…in **Northwestern Colombia**》（2016，被引27）——研究对象是**哥伦比亚**的侏罗纪（180 Ma）陆弧，"
  "既非日本列岛（对象碰撞，与第45轮「阿根廷 Pampean」同型），也不涉「现在位于板块交界」这一现在时断言（时期错配）。已撤回该来源与落点句。"
  " 现仅保留「位于板块交界附近」的常识性表述，具体地震/火山频度待引日弧专题文献。").strip()
jp["last_update"]=TODAY

# ===== B 回写实测字符数（审计现场抓取的数值，可复现）=====
MEASURED={
"s045-desertification":(24305,42),
"s041-nasa-landsat":(23448,112),
"epa-great-lakes":(2624,11),
"noaa-glerl":(2804,9),
"s025-ourworldindata-org":(39569,None),
"s082-ourworldindata-org":(19408,None),
"s035":(10903,None),
"s039-climate-nasa-gov":(12407,None),
"s074-unicef-org":(5455,None),
}
n=0
for sid,(chars,hits) in MEASURED.items():
    s=S.get(sid)
    if not s: continue
    note=s.get("note") or ""
    if "正文" in note and f"{chars}" in note: continue
    tail=f" 【第46轮实测】strip 后正文 {chars:,} 字符" + (f"，本条正则命中 {hits}" if hits else "") + "（现场抓取，可复现）。"
    if "第46轮实测" not in note:
        s["note"]=note+tail;n+=1
print("回写实测:",n)

# ===== C hb() 双读：sources.note ∪ entry.pending_notes =====
MIN=800
def hb(sid, e=None):
    notes=[]
    s=S.get(sid) or {}
    notes.append(s.get("note") or "")
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符",
                    r"正文\s*\*{0,2}(\d[\d,]*)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None

# 重算五分类
cat={"ge2":[],"one":[],"indicator":[],"terrain_common":[],"unmeasured_or_alias":[]}
for t,e in T.items():
    b=sum(1 for s in e["sources"] if hb(s,e) is True)
    unk=sum(1 for s in e["sources"] if hb(s,e) is None)
    pn=e.get("pending_notes") or ""
    if b>=2: cat["ge2"].append(t)
    elif b==1: cat["one"].append(t)
    elif unk>0: cat["unmeasured_or_alias"].append(t)
    elif "指标解读类" in pn: cat["indicator"].append(t)
    elif "常识性地理描述" in pn: cat["terrain_common"].append(t)
    else: cat["unmeasured_or_alias"].append(t)
print("新五分类：",{k:len(v) for k,v in cat.items()})
print("  unmeasured/alias 明细:",cat["unmeasured_or_alias"][:12])

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=46
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
json.dump({"round":46,"date":TODAY,"categories":{k:len(v) for k,v in cat.items()},
 "unmeasured_list":cat["unmeasured_or_alias"],
 "note":"hb() 改为双读 sources.note ∪ entry.pending_notes；回写 9 条实测；日本列岛错源已撤回"},
 open(os.path.join(ROOT,"reports","round46_recount.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)