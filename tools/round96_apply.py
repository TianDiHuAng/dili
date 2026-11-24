# -*- coding: utf-8 -*-
"""第96轮B：登记核心 G3a 6 条第二对位来源。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round96_core.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"撒哈拉沙漠":("geo","所引 2015 年《The impact of **Sahara desertification** on Arctic cooling during the Holocene》（被引21）讨论撒哈拉沙漠化如何影响**全新世北极的降温**；本条「撒哈拉的干旱化是长期环境变迁的结果、并与全球气候耦合」据此。"),
"马里帝国":("polities","所引 2025 年《The Grand Empires of the **Sahel**: Gold, Trade…》（摘要 935 字符）讨论萨赫勒大帝国以**黄金与贸易**为基础的政治经济；本条「马里帝国以黄金与盐的贸易支撑政治中心」据此。"),
"苏美尔城邦":("polities","所引 2007 年《Early Mesopotamian urbanism: a new view》（**被引 244**）以新的考古材料重新审视**早期美索不达米亚的城市化**；本条「苏美尔以城邦与神庙中心组织人口与生产」据此。"),
"汉代":("polities","所引 2019 年《**War economy** during the Western Han Dynasty》（摘要 945 字符）讨论西汉的**战争经济**（军需与财政动员）；本条「汉代以编户齐民与财政动员支撑大规模军事行动」据此。"),
"大平原":("geo","所引 2001 年《The Great Plains: **Agriculture and the Environment**》（摘要 999 字符）讨论大平原的农业与环境关系；本条「大平原以草原与旱作农业为特征、受干旱周期制约」据此。"),
"南极冰盖":("geo","所引 2023 年《Present and future **Ross Ice Shelf** dynamics》（摘要 **3,172 字符**）指出近数十年全球变暖已驱动**南极冰盖显著质量损失**，并预估 1.5℃/2℃ 升温情景下的后果；本条「南极冰盖的稳定性受海洋与大气升温影响」据此。"),
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
      f" 【第96轮补第二内容源（strong，Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"长江流域":"候选《Geographic patterns of **industrial water consumption** in the Yangtze River》(2025) 研究**工业用水**的地理格局（现代经济地理），不支撑本条的流域地形与农业史。不采用。",
"澳大利亚大陆":"候选《Australian Participation in the **IPCC**》(2008, 被引14) 是**澳大利亚参与政府间气候变化专门委员会**的政策史，属国际治理侧面，不支撑大陆的自然地理。不采用。",
"波利尼西亚":"候选《Southeast **Solomon Islands** in regional perspective》(2022, 被引46) 研究对象是**所罗门群岛**（属美拉尼西亚），与波利尼西亚的文化圈不同（D105 对象偏差）。不采用。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第96轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=96
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")