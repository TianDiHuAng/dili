# -*- coding: utf-8 -*-
"""第50轮C：登记 2 条主来源、剔除 2 条不匹配、收尾。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round50_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

OK={
"密西西比河":("geo","所引 2004 年《Tritium hydrology of the Mississippi River basin》（被引57）以氚示踪分析**流域干支流的水文过程**（密西西比干流与俄亥俄、密苏里等支流采样点）；本条「水系由干流与多条支流构成、水量季节变化显著」据此。"),
"河流三角洲":("geo","所引 2008 年研究以数学模型讨论**河口沙坝的形成与前积（progradation）**，并以多瑙河三角洲的波塔波夫与贝斯特里支流为例；本条「三角洲由泥沙堆积与河道分汊形成」据此。"),
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
      f" 【第50轮补主来源】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
      f"待支撑断言「{c['claim']}」；主题槽命中 {c['slots']}；已在本条 {fld} 段落点。此前该条的侧面文献（另见旁证认定）仍保留作旁证。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

REJECT={
"季风系统":"候选《Eddy-Mediated Regime Transitions in the Seasonal Cycle of a **Hadley Circulation**》研究的是**哈德莱环流的季节循环**（理想化 GCM 模拟），与季风（海陆热力差异驱动的季节性风向反转）不是同一对象，剔除。",
"南极大陆":"候选《Deglacial climate and ice sheet evolution of the **Ross Embayment**, Antarctica》只覆盖**罗斯海湾这一扇区**，不支撑「南极大陆」的地貌与冰盖总体，仅可作扇区旁证，未登记为主来源。",
}
for t,why in REJECT.items():
    e=T.get(t)
    if e: e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第50轮未采用】{why}").strip()

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=50
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
print("登记主来源:",n,"、".join(log))
print(f"重算 ≥2 {g2} / 1个 {o1} / 0个 {z0}")