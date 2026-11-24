# -*- coding: utf-8 -*-
"""第80轮B：登记 7 条第二内容源；4 条如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round80_imp3.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"马其顿与亚历山大":("polities","所引 2010 年《Alexander the Great and His Empire: A Short Introduction》（**被引 107**）概述亚历山大帝国的建立与治理；本条「马其顿以军事征服建立跨欧亚帝国、死后迅速分裂」据此。"),
"特奥蒂瓦坎":("influence","所引 2005 年《Human Sacrifice, Militarism, and Rulership》（**被引 189**）以羽蛇神庙（约公元 200 年建）为对象，讨论特奥蒂瓦坎的**宗教含义与政治意涵**——该城是前哥伦布时期最早、人口最多的城市之一；本条「特奥蒂瓦坎以宗教与军事权威维系庞大人口」据此。"),
"十三殖民地":("influence","所引 2011 年《Colonial America: A History to 1763》（被引27，摘要 4,323 字符）综述英属北美殖民地至 1763 年的发展；本条「十三殖民地以农业与跨大西洋贸易成长、地方自治传统成形」据此。"),
"法兰克王国":("polities","所引 2008 年《Frankish military duty and the fate of Roman…》（被引28）讨论法兰克的**军事义务**与罗马遗产的关系；本条「法兰克以军事服务与土地授予维系王国」据此。"),
"奥尔梅克":("influence","所引 2014 年《Discovering the Olmecs》（被引15）综述奥尔梅克文明的研究；本条「奥尔梅克以巨型石雕头像与宗教中心影响中美洲后续文明」据此。"),
"加勒比海群岛":("influence","所引 2002 年《In the shadow of the plantation: Caribbean…》（被引75）讨论**种植园经济**对加勒比岛屿社会的塑造；本条「群岛经济以甘蔗种植园为主、人口结构由奴隶贸易重塑」据此。"),
"莱茵河":("geo","所引 2005 年《The Rhine: An Eco-Biography, 1815–2000》（摘要 4,440 字符）以**生态传记**方式叙述莱茵河两个世纪的环境变迁（含渠化、污染与治理）；本条「莱茵河为欧洲重要航运水道、人类工程深刻改造其河道」据此。"),
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
      f" 【第80轮补第二内容源（strong）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"十字军东征":"过筛候选《The Military Orders and Women of the Nobility in the Crusader States》(2023) 主题是**军事修会与贵族女性的互动**（性别侧面），不支撑十字军运动的整体。不采用。",
"威尼斯":"过筛候选《Negotiating Transcultural Relations in the Early Modern Mediterranean》(2014, 被引45) 时段是 **16–17 世纪**，而威尼斯本条叙述的是其**海上共和国鼎盛期（13–15 世纪）**，时期错配（D108）。不采用。",
"巴西高原":"过筛候选《GIS-Based Relief Compartment Mapping…central Brazilian highlands》(2020, 被引7) 只覆盖**里奥韦尔梅柳保护区的喀斯特地貌**（局部区域），不支撑高原的地质与地貌总体。不采用。",
"拉普拉塔平原":"过筛候选《Sustainable intensification of agriculture and economy》(2022, 被引3) 摘要以「任何人类活动都有影响」泛论开场，未见针对潘帕斯的具体结论。不采用。",
"大分水岭":"本轮**0 候选**（宽检索亦无过筛者）。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第80轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=80
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")