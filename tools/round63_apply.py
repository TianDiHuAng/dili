# -*- coding: utf-8 -*-
"""第63轮：登记 4 条第二来源；3 条未命中与 1 条部分适配如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round63_second.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

SPEC={
"阿兹特克":("polities","所引 2008 年《Aztec city-state capitals》（**被引 202**）指出：阿兹特克人自 13 世纪起统治墨西哥大部至 1521 年西班牙征服；除帝都特诺奇蒂特兰之外，**若干城市中心统治着中部墨西哥众多的城邦**。本条「三方联盟之下仍保留大量城邦单元」据此。","strong"),
"阿拉伯半岛":("geo","所引 2012 年《Recent climate change in the Arabian Peninsula》（**被引 396**）以网格数据与沙特 27 个地面站（1978–2009）分析半岛的年降雨与气温气候学；沙特一国即占半岛近 80%。本条「半岛以干旱气候为主、降水与温度年际变率大」据此。","strong"),
"马格里布":("influence","所引 2021 年《The Invention of the Maghreb: Between Africa and the Middle East》（被引62）论证「马格里布」作为一个地理实体，是在**法国殖民统治下**才与「中东」「非洲」这两个同样属殖民构造的实体区分开来的；本条「马格里布是历史形成的区域概念而非天然界线」据此。","strong"),
"汉代":("influence","所引 2014 年《Fortified settlements and the settlement system in the Northern Zone…》（被引17）以帝国行政与防御体系如何影响聚落格局为问题，指出大型territorial国家与帝国需要复杂的治理与防御系统；本条「边地设防与行政控制塑造聚落分布」据此（该文以北方地带为个案）。","strong"),
}
n=0;log=[]
for t,(fld,sentence,grade) in SPEC.items():
    c=F[t]["best"];e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in e["sources"]: continue
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}" if c.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：{grade}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第63轮补第二来源（{grade}）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c.get('cited')}，摘要 {c['abs_len']} 字符）：主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

REC={
"古埃及新王国":"过筛候选《Literacy and Ancient Egyptian Society》（1983, 被引333）讨论**埃及文字与社会**（自前3000年），不专指新王国，仅可作背景；本条第二来源仍缺。",
"周代":"11 条候选中无一同时满足「标题含 zhou」与「两个主题槽（state/feudal/enfeoff）」。第二来源缺。",
"桑海帝国":"3 条候选中无过筛者。第二来源缺。",
"笈多王朝":"7 条候选中无过筛者。第二来源缺。",
"加纳帝国":"检索命中的仍是已登记的 W2010072736（被引107），非第二来源；需另找。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第63轮检索记录】两库（Crossref+OpenAlex）、两条检索式；{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=63
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    if is_data(sid): return False
    for note in [(S.get(sid) or {}).get("note") or "", e.get("pending_notes") or ""]:
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
print("登记",n,"：","、".join(log))
print(f"重算 ≥2 {g2} / 1个 {o1}")