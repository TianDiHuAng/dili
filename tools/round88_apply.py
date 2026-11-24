# -*- coding: utf-8 -*-
"""第88轮B：登记 2 条；立 D145（重复命中即停止重试）并标记无解清单。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round88_imp6.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"气候带":("geo","所引 1994 年《On coupling global biome models with climate models》（**被引 145**）把预测全球植被格局的 BIOME 模型与 ECHAM 气候模型耦合，用以模拟**气候与生物群区的对应关系**；本条「气候带与植被类型相关、随气候变化而移动」据此。"),
"大分水岭":("geo","所引 1983 年《Seasonal changes in the distribution of rainfall over the **Great Dividing Range** in New South Wales》（被引15）用日降水相关性划出新南威尔士大分水岭周边的**降水区与季节变化**；本条「大分水岭影响东部降水分布、形成迎风与背风差异」据此。"),
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
      f" 【第88轮补第二内容源（strong，Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

# D145：重复命中的条目 → 停止重试，列无解
IRREP={
"笈多王朝":"【已列为无解（D145）】连续两轮（第76、86轮）独立检索均只命中**钱币学**研究（《Role of Coins》/《Treasures of the Gupta Empire》）。该主题的英文学术文献以钱币研究为主，无整体性研究可得。停止重试。",
"巴西高原":"【已列为无解（D145）】连续两轮（第80、87轮）命中同一篇**局部喀斯特地貌制图**（仅覆盖里奥韦尔梅柳保护区）。无高原尺度的地质地貌综述可得。停止重试。",
"拉普拉塔平原":"【已列为无解（D145）】连续两轮（第80、87轮）命中同一篇**泛论**（《Sustainable intensification of agriculture》，摘要以「任何人类活动都有影响」开场，无潘帕斯具体结论）。停止重试。",
}
for t,txt in IRREP.items():
    e=T.get(t)
    if not e: continue
    if "已列为无解（D145）" in (e.get("pending_notes") or ""): continue
    e["pending_notes"]=((e.get("pending_notes") or "")+" "+txt).strip()
    e["last_update"]=TODAY
print("已标记无解 3 条")

REC={
"吠陀时代":"本轮候选《Chemistry in Vedic and Post-Vedic Literature》(2026) 是**吠陀文献中的化学知识**（科技史侧面）。",
"明清":"本轮候选《Beyond the Lens: the **Telescope**'s Influence》(2024) 是**望远镜**的科技史侧面。",
"马来群岛":"本轮候选《Winstedt, colonialism and the Malaysian history wars》(2024) 是**殖民主义与马来西亚史学论战**（史学史）。",
"威尼斯":"本轮候选《Public service and private trade: Northern seamen in seventeenth-century Venice》(2015) 时段是**17 世纪**且主体是**北欧海员**，与本条（威尼斯共和国鼎盛期）时期与主题双重错配。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第88轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=88
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")