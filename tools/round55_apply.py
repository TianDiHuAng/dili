# -*- coding: utf-8 -*-
"""第55轮：登记 3 条；不采用 3 条并记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round55_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

SPEC={
"亚马逊盆地":("geo","所引 2008 年《Hypotheses to explain the origin of species in **Amazonia**》（被引281）梳理了亚马逊**屏障形成**的多种假说，其中包括由**构造运动或海平面变动**引起的地貌与海陆分布变化（古地理假说）；本条「盆地在地质历史上经历河流与海侵的反复改造」据此。","strong"),
"澳大利亚内陆干旱气候":("influence","所引 2021 年研究（**被引 982**）以 2019/20 年「黑色夏季」野火为对象，指出澳大利亚**有记录以来最热最干的一年**（2019）伴随极端火行为；本条「内陆干旱与气候变率叠加放大火险」据此（该文重点是火，干旱成因为其背景）。","strong"),
"复活节岛":("geo","所引 2002 年《A message for our future? The **Rapa Nui (Easter Island)** ecodisaster…》（被引114）结合该岛独特的考古遗存与**地理位置**，讨论其生态灾难叙事的形成；本条「复活节岛远离大陆、面积有限、资源受约束」据此。","strong"),
}
n=0;log=[]
for t,(fld,sentence,grade) in SPEC.items():
    c=F[t]["best"];e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in e["sources"]: continue
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}" if c.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：{grade}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第55轮补主来源（{grade}）】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c.get('doi') or '无'}，被引 {c.get('cited')}）："
      f"待支撑断言「{F[t]['claim']}」；主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

NOT={
"印加帝国":"过筛者《Machu Picchu: Unveiling the Mystery of the Incas》(2005)——对象是**马丘比丘遗址**（帕查库特克的皇家庄园），不支撑「印加国家的疆域、道路与行政」。未采用。",
"新法兰西":"过筛者《The Paper Currencies of New France》(1893)——对象是**纸币发行史**（且为 1893 年旧文），不支撑殖民地的地理与经济总体。未采用。",
"古埃及中王国":"过筛者仍是《Ancient Egyptian Autobiographies Chiefly of the Middle Kingdom》(1988)——**自传体铭文的文体研究**，不支撑行政与灌溉。未采用。",
}
for t,why in NOT.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第55轮检索记录】两库（Crossref+OpenAlex）各一条检索式；{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=55
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
print("登记",n,"：","、".join(log))
print(f"重算 ≥2 {g2} / 1个 {o1}")