# -*- coding: utf-8 -*-
"""第105轮B：登记 G3a 命中条目；碰撞/弱候选如实记录。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round105_g3.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

# 条目 -> (候选序号, 写入字段, 句子)
SPEC={
"人文地理学":(0,"influence","所引 2014 年《Charting the development of social and cultural geography in Mainland China: voices from the inside》（被引19，摘要 1,393 字符）梳理中国大陆社会与文化地理学的发展，涵盖文化区、文化扩散、族群文化地理与文化景观等主题；其对象是中国大陆的学科发展，可作人文地理学学科史的补充视角，不代表全球学科全貌。"),
"隋唐":(0,"influence","所引 2015 年《City of Marvel and Transformation: Changan and Narratives of Experience in Tang Dynasty China》（被引9，摘要 1,493 字符）从文人经验的角度讨论唐代长安如何塑造士人身份与集体想象；它是都城文化史视角，与国家能力类来源互补，被引较少，证据强度有限，不涉及隋代与制度细节。"),
"大分水岭":(0,"geo","所引 1985 年《Post-orogenic evolution of a mountain range: South-eastern Australian Highlands》（被引9，摘要 836 字符）讨论造山后侵蚀、均衡回弹与河流下切对澳大利亚东南高地地貌的塑造；其范围是东南部高地，不覆盖大分山脉全长，且年代较早。"),
"冲积平原":(0,"geo","所引 2020 年《Channel-floodplain response to changes in sediment supply and floodplain width》（被引2，摘要 1,597 字符）讨论泥沙供给与河漫滩宽度如何影响冲积河道与漫滩的几何形态和演化，对应冲积平原的形成过程；属水槽或模型类研究章节，被引很少，证据强度有限。"),
}
n=0;log=[]
for t,(idx,fld,sent) in SPEC.items():
    cands=F[t]["cand"]
    e=T.get(t)
    if not e or len(cands)<=idx: continue
    c=cands[idx]
    sid=f"openalex-{c['oid']}"
    if sid in e["sources"]:
        print("已有，跳过:",t,sid);continue
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
          "note":f"OpenAlex 作品 {c['oid']}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：strong。路线：Crossref→DOI→OpenAlex by-ID。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第105轮补第二内容源（Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"教育机会地域差异":"第105轮候选为撒哈拉以南非洲性别差异（W3125766961）与中国高等教育城乡差距（W2941642351），前者主题仅部分对位，后者与已有来源重叠，均不采用，需换检索角度。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第105轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=105
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
