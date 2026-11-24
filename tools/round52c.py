# -*- coding: utf-8 -*-
"""第52轮C：登记 5 条主来源；明确排除古埃及「新王国之后」重复命中。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round52b_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

SPEC={
"拜占庭帝国":("influence","所引 2009 年《The Middle Byzantine Economy (600–1204)》（被引21）讨论中期拜占庭经济的结构，并把它视为理解拜占庭国家、社会与文化的关键；本条「农业、税收与军区制相互支撑」据此（军区制部分为常识性补充）。","strong"),
"维京时代":("influence","所引 2020 年《Viking-Age Trade: Silver, Slaves and Gotland》（被引13）以哥特兰岛为中心讨论维京时代的**白银、奴隶与贸易网络**；本条「维京人以海上贸易与劫掠并行的方式连接北欧与欧亚商路」据此。","strong"),
"大自流盆地":("geo","所引 1968 年研究分析大自流盆地的**构造、地层与水文地质**；本条「盆地被不透水层圈闭、含水层向西部倾斜、井水可自流」据此。","strong"),
"落基山脉":("geo","所引 1975 年《Laramide (Late Cretaceous-Early Tertiary) Orogeny》（被引223）讨论**拉拉米造山运动**对落基山脉形成的控制；本条「落基山脉主要由晚白垩世至早第三纪的造山运动抬升」据此。","strong"),
"美国西进":("influence","所引 2020 年研究讨论内战时期美国**东西部之间**的分隔与向西扩张的推进过程；本条「西进使联邦版图从大西洋岸延伸至太平洋岸」据此。（该文被引 0，证据强度有限，仅作辅助。）","weak"),
}
n=0;log=[]
for t,(fld,sentence,grade) in SPEC.items():
    c=F[t]["best"];e=T.get(t)
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
          "note":f"OpenAlex 作品 {oid}（DOI {c['doi']}）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：{grade}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第52轮补主来源（{grade}）】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
      f"待支撑断言「{F[t]['claim']}」；主题槽命中 {c['slots']}；已在本条 {fld} 段落点。此前的侧面文献仍保留为旁证。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

# 古埃及新王国：明确排除（第二次命中「之后」时期）
eg=T["古埃及新王国"]
eg["pending_notes"]=((eg.get("pending_notes") or "")+
  " 【第52轮检索记录·重复命中】以「New Kingdom Egypt empire administration」检索，Crossref 结果中过筛者仍是《Afterglow of Empire: Egypt from the **Fall** of the New Kingdom to the Saite…》(2012)——"
  "该文研究对象是新王国**灭亡之后**（前11–前6世纪），第48轮已判定时期错配并剔除。**书名含 New Kingdom 但主题在其之后**，属 D108「同名不同时」的典型，故本轮再次排除。"
  " 本条主来源仍缺，需题为「New Kingdom」且讨论帝国行政的专题研究。").strip()
eg["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=52
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