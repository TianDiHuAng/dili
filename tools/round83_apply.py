# -*- coding: utf-8 -*-
"""第83轮B：登记 6 条；非洲大湖地区查 type 后决定。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round83_sup2.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"古埃及中王国":("polities","所引 2013 年《Setting a State Anew: The Central Administration from the End of the Old Kingdom to the End of the Middle Kingdom》（被引52）指出中王国的行政与古王国**显著不同**，并划分出三个阶段；本条「中王国重建中央官僚体系、与古王国制度有别」据此。"),
"法蒂玛王朝":("influence","所引 2023 年《The Fatimid Caliphate》（摘要 876 字符）讨论 1050–1128 年间**法蒂玛在沙姆地区权威的衰退**及其地方因素；本条「法蒂玛以哈里发—军队—地方势力的平衡维系政权、后期失衡」据此。"),
"贵霜帝国":("polities","所引 2020 年《The Kushan Empire》（摘要 1,598 字符）指出贵霜原为中亚草原的**游牧部族**，后在南亚与中亚建立**定居国家**；本条「贵霜由游牧转定居、控制中亚—南亚商路」据此。"),
"帖木儿帝国":("polities","所引 2026 年《Diplomacy of The Timurid Empire》（摘要 1,610 字符）分析帖木儿及其后继者时期的**外交体系与对外政策**原则；本条「帖木儿以军事征服与外交并重建国」据此。"),
"迈锡尼文明":("influence","所引 2008 年《Beyond the Palace: Mycenaean East Lokris》（被引39）以希腊中部的考古材料讨论**宫殿之外的迈锡尼社会**；本条「迈锡尼以宫殿中心组织社会、但地方聚落亦具自主性」据此。"),
"仰韶文化":("influence","所引 2025 年研究（摘要 1,194 字符）讨论**仰韶彩陶纹饰的社会功能**；本条「仰韶以彩陶与聚落形态体现新石器时代的社会组织」据此（该文聚焦彩陶一侧，不涉农业与聚落总体）。"),
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
          "note":f"OpenAlex 作品 {c['oid']}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：strong。路线：Crossref→DOI→OpenAlex by-ID（D144）。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第83轮补第二内容源（strong，Crossref 路线）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

# 非洲大湖地区：查 type
c=F["非洲大湖地区"]["cand"][0]
w={}
for _ in range(3):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",
          f"https://api.openalex.org/works/{c['oid']}?select=title,type"],capture_output=True,timeout=30)
        w=json.loads(p.stdout.decode("utf-8","ignore"))
        if w.get("title"): break
    except Exception: pass
    time.sleep(4)
print("非洲大湖地区候选 type:",w.get("type"))
e=T.get("非洲大湖地区")
if e:
    if w.get("type")=="book-review":
        e["pending_notes"]=((e.get("pending_notes") or "")+
          f" 【第83轮剔除·书评】{c['oid']}（《Conflict and Peacebuilding in the African Great Lakes Region》）经 OpenAlex 实测 **type=book-review**，"
          "摘要是「Edited by… Pp. xiii, 245; index, bibliography. $28.00」的书评格式，按 D082/R25 不作内容来源。").strip()
    else:
        e["pending_notes"]=((e.get("pending_notes") or "")+
          f" 【第83轮检索记录】候选 {c['oid']}（type={w.get('type')}）主题为冲突与和平建设，属当代政治侧面，不支撑「大湖地区的自然地理与人口分布」。不采用。").strip()
    e["last_update"]=TODAY

REC={
"室利佛逝":"Crossref 路线**检索成功**（HTTP 失败率 2%，非故障），20 条结果中无一条同时满足「标题含 srivijaya」与「两主题槽」。本轮结论为**真实的无过筛结果**。",
"满者伯夷":"同上，检索成功、无过筛者。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第83轮检索记录·D144 合规】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=83
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")