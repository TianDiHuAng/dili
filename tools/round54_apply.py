# -*- coding: utf-8 -*-
"""第54轮C：登记 3 条主来源；3 条错配按 D112 记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round54_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

SPEC={
"南极半岛":("influence","所引 2000 年《The link between climate warming and break-up of ice shelves in the Antarctic Peninsula》（**被引 873**）综述原位与遥感数据，指出与冰架快速退缩相关的特征：深凹的冰前缘、大量细长冰山的分裂事件、流速加快、以及冰面融水塘的出现；本条「半岛冰架崩解与变暖相关」据此。","strong"),
"古巴岛":("geo","所引 2016 年《The geology of Cuba: A brief overview and synthesis》（被引81）指出古巴的地质记录包含三个重要阶段：侏罗纪北美与南美（Pangea）裂解及被动陆缘演化、白垩纪—古近纪大洋内弧的沉积—岩浆—变质演化，以及与巴哈马台地的碰撞；本条「岛屿由多期构造拼合而成」据此。","strong"),
"巴塔哥尼亚":("geo","所引 2013 年《Large-Scale Control on the Patagonian Climate》（**被引 668**）指出巴塔哥尼亚降水主要由**西风气流中的扰动**产生，并被**南安第斯山**强烈改造；本条「西风带与安第斯雨影共同决定其干旱格局」据此。","strong"),
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
      f" 【第54轮补主来源（{grade}）】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c.get('doi') or '无'}，被引 {c.get('cited')}）："
      f"待支撑断言「{F[t]['claim']}」；主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

REC={
"古埃及中王国":"过筛者为《Ancient Egyptian Autobiographies Chiefly of the Middle Kingdom》（1988, 被引172）——主题是**自传体铭文的文体发展**（铭文学侧面），不支撑「行政与灌溉开发」。主来源仍缺。",
"澳大利亚内陆干旱气候":"过筛者为《Salinity Stress in Arid and Semi-Arid Climates》（2019, 被引304）——主题是**盐胁迫对作物的影响**（农学），不涉干旱气候的成因。主来源仍缺。",
"新法兰西":"过筛者为《Driven by drink: The role of drinking in the political economy…》（1990, 被引489）——主题是**跨文化饮酒习俗的政治经济学**，与「新法兰西殖民地的地理与经济」无关（对象词 `france` 过宽导致误中）。主来源仍缺。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第54轮检索记录】引擎 Crossref+OpenAlex 两库、各两条检索式；{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=54
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