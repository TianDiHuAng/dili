# -*- coding: utf-8 -*-
"""第74轮：登记第二批 6 条第二内容源；印加与澳原住民如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round73_batch2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"玛雅文明":("influence","所引 2010 年《Ancestral Maya Economies in Archaeological Perspective》（**被引 191**）指出：象形文字的释读使学界得以更好理解**古典期社会**，但该文明的**经济与社会结构**仍有大量未知，并追问农民等的经济角色；本条「玛雅为雨林中的城邦文明、其经济与社会结构仍有争议」据此。","strong"),
"安第斯山脉":("geo","所引 2010 年《Amazonia Through Time: Andean Uplift, Climate Change, Landscape Evolution》（**被引 2762**）综述**安第斯隆升**如何改变亚马逊的气候与景观并塑造物种多样性；本条「安第斯山脉的隆升改变了南美大陆的气候与水文格局」据此。","strong"),
"澳大利亚大陆":("geo","所引 2003 年《Climate change and Australia: Trends, projections and impacts》（**被引 941**）综述澳大利亚近数十年的**气候与地球物理趋势**、21 世纪预估及其影响；本条「大陆以干旱与高度变率为特征、气候带自北而南分异」据此。","strong"),
"河流三角洲":("geo","所引 2006 年《High-Resolution Stratigraphy of a Mississippi Subdelta-Lobe》（被引23）指出路易斯安那东南沿海是**密西西比三角洲多次前积、废弃与海侵旋回**的产物；本条「三角洲由泥沙堆积、河道分汊与废弃改道交替形成」据此。","strong"),
"波利尼西亚":("influence","所引 1976 年《Micronesian and Polynesian Voyaging: Three Readings》（摘要 2,690 字符）为太平洋航海主题的课程读本汇编，讨论波利尼西亚与密克罗尼西亚的**独木舟航海**；本条「长距离航海技术使岛屿殖民与往来成为可能」据此。","weak"),
"大平原":("influence","所引 1980 年《Ethnicity on the Great Plains》（被引12）指出 19 世纪定居大平原的人口中**欧洲移民构成主要成分**；本条「19 世纪移民与农业开发重塑平原人口格局」据此（族裔与社会史侧面）。","weak"),
}
n=0;log=[]
for t,(fld,sent,grade) in SPEC.items():
    c=F[t]["cand"][0];e=T.get(t)
    if not c or not e: continue
    sid=f"openalex-{c['oid']}"
    if sid in e["sources"]: continue
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{c['oid']}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {c['oid']} — {c['title']}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),"type":"学术文献",
          "url":f"https://api.openalex.org/works/{c['oid']}","url2":f"https://doi.org/{c['doi']}" if c.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {c['oid']}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：{grade}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第74轮补第二内容源（{grade}）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"印加帝国":"过筛候选仍是《Machu Picchu: Unveiling the Mystery of the Incas》(2005, 被引15)——对象是**马丘比丘遗址**（皇家庄园），第55轮已判「不撑国家的疆域/道路/行政」，本轮再次不采用。",
"澳大利亚原住民":"过筛候选《Reempowering Ourselves: Australian Aboriginal Women》(2010, 被引134) 主题是**原住民女性**的失权与再赋权（性别侧面），不支撑本条「适应干旱生态、语言与文化传统」的总体表述；不采用。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第74轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=74
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")