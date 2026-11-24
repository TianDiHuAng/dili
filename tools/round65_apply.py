# -*- coding: utf-8 -*-
"""第65轮C：登记 4 条第二来源（3 条个案需限定范围）。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round65_second.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

SPEC={
"海洋生态系统":("influence","所引 2013 年《Current Status and Future Prospects for the Assessment of Marine and Coastal **Ecosystem Services**》（**被引 861**）系统评述海洋与沿海生态系统服务（MCES）的评估与制图现状，指出既有研究多集中于陆地、海洋部分存在明显知识缺口；本条「海洋生态系统服务在空间上分布不均、评估覆盖不足」据此。","strong","global"),
"保护与保育区体系":("influence","所引 2010 年研究评估**菲律宾海洋保护区**的养护成效与覆盖缺口（被引244），指出「量化既有保护区是否达成目标、识别覆盖空缺」是构建保护区网络的前提；本条「保护区体系需评估成效而非只看面积」据此。**注意：该文是菲律宾个案，不代全球**。","strong","case"),
"教育机会地域差异":("influence","所引 2023 年研究（被引53）以**中国**为例，指出高等教育进入普及阶段（入学率逾50%）后，**区域不平等仍是教育公平的主要障碍**；本条「教育机会的区域差异在普及之后依然显著」据此，**该文是中国个案**。","strong","case"),
"农业企业与价值链":("influence","所引 2004 年《Contract farming in Indonesia》（被引72）讨论**印尼**小农与农业企业的合同农业安排：大农可获资本、市场信息与制度支持，小农常被排除；本条「价值链的组织方式决定小农能否参与」据此，**该文是印尼个案**。","strong","case"),
}
n=0;log=[]
for t,(fld,sentence,grade,scope) in SPEC.items():
    c=F[t];e=T.get(t)
    if not c or not e: continue
    oid=c["oid"];sid=f"openalex-{oid}"
    if sid in e["sources"]: continue
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get("article","学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}" if c.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：{grade}。适用范围：{scope}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第65轮补第二来源（{grade}，{scope}）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c.get('cited')}，摘要 {c['abs_len']} 字符）：主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=65
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
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
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
one=[t for t,e in T.items() if sum(1 for s in e["sources"] if hb(s,e) is True)==1]
print("登记",n,"：","、".join(log))
print(f"重算 ≥2 {g2} / 1个 {len(one)}")
print("仍仅1源:",one)