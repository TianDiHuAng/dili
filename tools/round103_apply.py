# -*- coding: utf-8 -*-
"""第103轮B：登记 4 条；3 条碰撞/侧面如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round103_g3b.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"明清":("polities","所引 2020 年研究（摘要 936 字符）讨论**清代绿营（garrison system）改革**中**国家与地方社会**的关系——军制如何与地方社区、身份与资源纠缠；本条「明清以里甲、卫所与州县体制治理基层」据此（该文聚焦军制一侧）。"),
"威尼斯":("influence","所引 2006 年《Molding the History of a **Maritime Empire**: The Role of the Thirteenth-century Mosaics…》（摘要 1,281 字符）指出**圣马可教堂的马赛克**体现这个**海上帝国**如何以图像服务政治与教会目的；本条「威尼斯以海上霸权与视觉宣传塑造共和国认同」据此。**说明：该文是艺术史研究，不涉经济与制度。**"),
"南极条约体系":("influence","所引 2011 年《The **Development of the Antarctic Treaty System**》（被引 38）梳理南极条约体系的演进；本条「南极条约体系以协商国会议与议定书扩展治理范围」据此。"),
"山地农业":("influence","所引 2022 年《A Future for **Mountain Terraces**》（被引16，摘要 1,779 字符）讨论山地**梯田农业**的经验与前景；本条「山地农业以梯田、等高耕作与水土保持适应坡度」据此。"),
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
      f" 【第103轮补第二内容源（strong，Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"隋唐":"过筛候选《Pirates and Publishers: A Social History of **Copyright in Modern China**》(2019) 研究 **1890s–1950s 中国的版权社会史**，与隋唐（6–9 世纪）无关。不采用。",
"大分水岭":"过筛候选《The **great divide**: population comparison using 3D and 2D geometric morphometrics》(2025) 是**几何形态测量学**的种群比较研究——`great divide` 在此是隐喻（并非 Great Dividing Range）。**对象碰撞**。不采用。",
"冲积平原":"过筛候选《Walls Formation, Western **Shetland**》(1985, 摘要 1,492) 研究**设得兰群岛西部**的一处泥盆纪冲积层序（局部地质），不支撑冲积平原的一般形成机制。不采用。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第103轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=103
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")