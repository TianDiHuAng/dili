# -*- coding: utf-8 -*-
"""第51轮：登记季风系统/南极大陆主来源；库什如实记录无合格候选；收尾。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round51_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

OK={
"季风系统":("geo","所引 2010 年《Understanding the Predictability of East Asian Summer Monsoon…》（被引97）以**海陆热力差异变化**解释东亚夏季风环流的可预测性，指出对流层增温对季风环流的支配作用；本条「海陆热力差异驱动季风、夏季风随季节推进」据此。"),
"南极大陆":("geo","所引 2024 年研究以**甘布尔采夫冰下山脉**（东南极中部）为例，讨论被冰盖掩埋的景观如何保存**大陆在 3400 万年前大规模 glaciation 之前与之后**的地质与地貌演化信息；本条「南极大陆以冰盖覆盖为主体、露岩区极少、地貌演化史古老」据此（以该区为实例，不代整大陆的地形细节）。"),
}
n=0;log=[]
for t,(fld,sentence) in OK.items():
    c=F[t]["cand"];e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in e["sources"]: continue
    if sid not in have:
        code=0;size=0
        for _ in range(3):
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                    if code==200: break
                time.sleep(4)
            except Exception: time.sleep(4)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {c['doi']}）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys((e["sources"] or [])+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第51轮补主来源】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
      f"待支撑断言「{c['claim']}」；主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

# 库什：如实记录无合格候选（唯一候选是已判定的反向证据文献）
ku=T["库什与努比亚"]
ku["pending_notes"]=((ku.get("pending_notes") or "")+
  " 【第51轮检索无果】再以「kingdom of Kush Napata Meroe trade」检索，Crossref 20 条结果中**唯一过对象词与主题槽者仍是 2019 年那篇麦罗埃冶铁研究**——"
  "而该文摘要已判定为**反向证据**（麦罗埃作为都城期间冶铁证据稀少），按 D101② 不得采用。"
  " 故本条目前**无合格内容来源**（0 个）；宁可留空，不以反证文献充数（D103）。待专门的库什商路/纳帕塔期考古研究。").strip()
ku["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=51
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
print("登记:",n,"、".join(log))
print(f"重算 ≥2 {g2} / 1个 {o1} / 0个 {z0}")