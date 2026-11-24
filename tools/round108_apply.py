# -*- coding: utf-8 -*-
"""第108轮：登记 G3b 两条互补内容源（非洲大湖地区、西北海岸）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY=os.environ.get("DILI_TODAY","2026-11-24")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round108_g3.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

SPEC={
"非洲大湖地区":("W2899960445","influence",
 "另据所引 2018 年《Prognosis for long-term sustainable fisheries in the African Great Lakes》（被引35，摘要 1,476 字符）：坦噶尼喀湖、马拉维湖与维多利亚湖的渔业仍为开放准入，渔获量下降、物种组成发生变化；作者认为可持续管理需转向更强的社会—生态路径，并称若无相应行动，长期可持续渔业的前景「黯淡」。此为该文的评估与论断，本条不据此推断各湖渔获的具体数值或成因分解。"),
"西北海岸":("W1581636576","influence",
 "另据所引 2009 年《Salmon, Science, and Reciprocity on the Northwest Coast》（被引62，摘要 859 字符）：作者论证该沿岸的部落在近代商业捕捞之前的数千年间管理鲑鱼种群，并拥有对终端渔场的排他权利、由互惠关系维系；作者称现有证据「令人信服」地表明其主动维护了鲑鱼的持续丰度。此为单篇研究的论证，摘要之外的具体机制与数据本条不引用。"),
}
n=0;log=[]
for t,(oid,fld,sent) in SPEC.items():
    e=T.get(t)
    cs=[c for c in F[t]["cand"] if c["oid"]==oid]
    if not e or not cs: print("缺失:",t);continue
    c=cs[0];sid=f"openalex-{oid}"
    if sid in e["sources"]: print("已有:",t);continue
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),"type":"学术文献",
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}" if c.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：strong。路线：Crossref→DOI→OpenAlex by-ID。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第108轮补第二内容源（Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=108
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
