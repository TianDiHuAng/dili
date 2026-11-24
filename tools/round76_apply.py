# -*- coding: utf-8 -*-
"""第76轮B：登记 5 条第二内容源；其余如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round76_imp2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"吴哥":("influence","所引 2020 年《Top-down and bottom-up water management: A diachronic model of the Greater **Angkor** region》（被引48）指出 9–15 世纪高棉帝国的连续都城发展出**大规模的农业与水资源管理系统**；本条「吴哥的水利网络支撑庞大人口与王权」据此。"),
"阿拉伯半岛":("geo","所引 2009 年《Chronology of the impact of Quaternary climate change…》（被引95）据古湖遗迹指出阿拉伯半岛**过去远比今天湿润**，最近的湿润期约在 10–5.5 ka 前；本条「半岛今日干旱、但在第四纪晚期经历湿润期」据此。"),
"匈奴":("influence","所引 2014 年《Iron Smelting in the Nomadic Empire of Xiongnu》（被引21）报告蒙古 Khustyn Bulag 的**匈奴时期冶铁遗址**（前209–公元155年），并指出匈奴是**东亚欧第一个游牧帝国**；本条「匈奴以游牧骑兵立国、兼有手工业」据此。"),
"周代":("polities","所引 2025 年研究（摘要 1,387 字符）讨论西周（约前1046–771）灭商后建立的**最早分封制**与燕国等封国的建立年代；本条「周代以分封与宗法组织政治秩序」据此。"),
"孔雀王朝":("polities","所引 2026 年《The Empire Under One **Umbrella**: Espionage, Reporting and the…》（摘要 3,665 字符）论证**孔雀帝国若无信息获取、传递与核验系统，便无法维系于单一权威之下**；本条「孔雀王朝靠行政与情报网络控制次大陆大部」据此。"),
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
          "note":f"OpenAlex 作品 {c['oid']}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：strong。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第76轮补第二内容源（strong）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"吠陀时代":"过筛候选《Status of Woman Reflected in Vedic Literature》(2023, 摘要2,167) 是**吠陀文献中的女性地位**（性别侧面），不支撑「吠陀时代的社会与宗教整体」。不采用。",
"笈多王朝":"过筛候选《Role of Coins in Reconstructing History》(2026, 摘要896) 是**钱币学**，物质文化侧面。不采用。",
"明清":"过筛候选《Organized Medicine in Ming-Qing China》(1987, 被引136) 是**医学制度**侧面，不支撑明清的国家与社会整体。不采用。",
"马来群岛":"过筛候选《Malay dialect research in Malaysia》(1989, 被引47) 是**方言语言学**研究，不支撑群岛的贸易与国家。不采用。",
"河中地区":"过筛候选《The Legacy of Sogdian Inscriptions》(2023, 摘要1,666) 是**粟特铭文**的文献学研究，不支撑绿洲灌溉与商路。不采用。",
"突厥":"过筛候选《Female burial of the Turkic period》(2023, 摘要1,197) 是**女性墓葬**（性别与考古侧面），不支撑突厥汗国的政治结构。不采用。",
"克里特文明":"宽检索本轮**0 候选**（前一阶段亦无合格者）。此条已多次检索无果。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第76轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=76
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")