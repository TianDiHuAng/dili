# -*- coding: utf-8 -*-
"""第87轮B：登记 4 条；6 条侧面/碰撞如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round87_imp5.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"洋流":("geo","所引 1969 年《Climate and the Ocean Circulation》（**被引 120**）讨论海洋环流与气候的关系；本条「洋流通过热量再分配影响大陆气候」据此。"),
"气候带":("geo","所引 2021 年《Observed and projected changes in global climate zones》（**被引 224**）报告全球**气候带**已观测到的位移与未来预估；本条「气候带随全球变暖发生位移、边界并非固定」据此。"),
"巴西殖民经济":("influence","所引 2019 年《Sugar and the Formation of Colonial Brazil》（摘要 842 字符）以**蔗糖**为轴讨论殖民巴西的形成；本条「殖民经济以甘蔗种植园与奴隶劳动为基础」据此。"),
"毛利人":("influence","所引 2012 年研究（摘要 **6,902 字符**）讨论传统毛利哲学中的**价值观**及其在今日新西兰的可见性；本条「毛利人以 whakapapa（谱系）与 mana（威望）组织社会关系」据此。"),
}
n=0;log=[]
for t,(fld,sent) in SPEC.items():
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
          "note":f"OpenAlex 作品 {c['oid']}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：strong。路线：Crossref→DOI→OpenAlex by-ID。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第87轮补第二内容源（strong，Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"大分水岭":"过筛候选《Euastacus vesper sp. nov., a new giant spiny **crayfish**》(2017) 描述的是**新种螯虾**，只因标本产地在「Great Dividing Range 西部水系」而命中——**纯产地碰撞**，与山脉本身无关。不采用。",
"威尼斯":"过筛候选《Venice Incognito: **Masks** in the Serene Republic》(2011) 主题是**威尼斯的面具文化**，社会习俗侧面。不采用。",
"马来群岛":"过筛候选《The Biological History of Homo sapiens in Island Southeast Asia》(2017) 是**颅测量学**的人群迁移史，属体质人类学侧面，不支撑群岛的贸易与国家。不采用。",
"巴西高原":"候选仍是《GIS-Based Relief Compartment Mapping…central Brazilian highlands》(2020)——只覆盖**里奥韦尔梅柳保护区的喀斯特地貌**（局部），第80轮已拒。",
"拉普拉塔平原":"候选仍是《Sustainable intensification of agriculture》(2022)——泛论，第80轮已拒。",
"南极条约体系":"本轮命中的来源**已登记**（第39轮），无新增。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第87轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=87
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")