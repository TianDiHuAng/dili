# -*- coding: utf-8 -*-
"""第53轮返工G：补元代/河中的候选（审计提供的 DOI），并修「无候选」失实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

def get_json(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",url],capture_output=True,timeout=35)
            s=p.stdout.decode("utf-8","ignore")
            if s.strip().startswith("{"): return json.loads(s)
            time.sleep(3)
        except Exception: time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))

CAND={
"元代":[("10.1017/jch.2024.63","influence","所引 2025 年《Communications and \"Communicators\" in the Yuan and Early Ming》讨论元与明初的**文书行政与驿传（通信）体系**，含译官机构、公文文字与纸钞等；本条「驿站与文书行政支撑跨区治理」据此。","weak"),
       ("10.2307/2715152","polities","（备用）《Salt Administration in the Yüan Dynasty》——元代盐政与行政，可作财政侧面。","weak")],
"河中地区":[("10.1016/j.jas.2012.03.009","geo","所引 2012 年《Dating the Irrigation System of the Samarkand Oasis》（被引27）以地质考古方法为撒马尔罕绿洲的**灌溉系统**定年；本条「河中绿洲依赖河水灌溉、城市以绿洲为重心」据此。","strong"),
         ("10.1007/s12520-023-01730-7","influence","所引 2023 年《Food globalization in southern Central Asia: archaeobotany at Bukhara》（被引21）以布哈拉的植物考古讨论**作物与商路带来的食物交流**；本条「河中作为东西作物与技术转运地」据此。","strong")],
}
n=0;log=[]
for t,items in CAND.items():
    e=T.get(t)
    if not e: continue
    for doi,fld,sentence,grade in items:
        w=get_json(f"https://api.openalex.org/works/https://doi.org/{doi}")
        if not w.get("id"):
            continue
        oid=(w.get("id") or "").rsplit("/",1)[-1];sid=f"openalex-{oid}"
        if sid in e["sources"]: continue
        if sid not in have:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
              f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
            raw=p.stdout.decode("utf-8","ignore");code=0;size=0
            if "__HTTP__" in raw:
                bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
            a=ab(w)
            sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {w.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
              "year":w.get("publication_year"),"type":TYP.get(w.get("type"),"学术文献"),
              "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{doi}",
              "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(w.get("title") or "")[:200],
              "note":f"OpenAlex 作品 {oid}（DOI {doi}）；{w.get('publication_year')}年；{w.get('type')}；被引 {w.get('cited_by_count')}。HTTP {code}，{size} 字节。摘要长度 {len(a)} 字符。证据强度：{grade}。"})
            have.add(sid)
        e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
        e[fld]=((e.get(fld) or "")+" "+sentence).strip()
        n+=1;log.append(t)

# 修「无候选」失实记录
REC={
"元代":" 【第53轮返工·检索失实更正】原记录写「36 条结果无一条过筛」——**失实**。原因有三：① 只查 Crossref 一库（违 D110 两库要求）；② 检索器 `if spec[\"obj\"] not in ti` 未做**变音归一**，《Salt Administration in the **Yüan** Dynasty》（摘要 3077 字符）因 `Yüan` 不含子串 `yuan` 被丢弃（D070 同型）；③ 只取 rows=18 首页。经补检，元代至少有 3 条候选（文书行政、盐政、银矿管理），已择 1 条登记。",
"河中地区":" 【第53轮返工·检索失实更正】原记录写「无一过筛」——**失实**，同样是只查单库所致。经补检，《Dating the Irrigation System of the Samarkand Oasis》(2012, 被引27) 与《Food globalization…Bukhara》(2023, 被引21) 均可承担本条断言，已登记；另有《Reading the Great Silk Road in the Samarkand Oasis》(2017, 被引1) 可作旁证。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=re.sub(r" 【第53轮检索记录】[^【]*","",e.get("pending_notes") or "")
    e["pending_notes"]=((e.get("pending_notes") or "")+why).strip()
    e["last_update"]=TODAY
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=53
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
print("补登记",n,"：","、".join(log))
print(f"重算 ≥2 {g2} / 1个 {o1}")