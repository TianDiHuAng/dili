# -*- coding: utf-8 -*-
"""第82轮C：登记 Crossref 路线命中的 3 条；记录 OpenAlex 配额故障。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round82_crossref.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"赫梯王国":("polities","所引 2012 年《The Hittite Empire from Textual Evidence》（被引21）以赫梯文书为据重建帝国的行政与政治结构；本条「赫梯以文书行政与条约体系维系帝国」据此。"),
"神圣罗马帝国":("influence","所引 2018 年《Associative Political Culture in the Holy Roman Empire》（被引39）以「联合式政治文化」重新解释神圣罗马帝国的运作方式——它并非失败的国家，而是一种**以协商与联合为特征的政体**；本条「帝国权力分散、皇帝与诸侯共治」据此。"),
"汉萨同盟":("influence","所引 2024 年《The Hanseatic League》（摘要≥800 字符）综述汉萨同盟的组织与贸易网络；本条「汉萨以城市联盟形式垄断波罗的海贸易」据此。"),
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
          "note":f"OpenAlex 作品 {c['oid']}（DOI {c.get('doi') or '无'}）；{c.get('year')}年；被引 {c['cited']}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：strong。检索路线：Crossref bibliographic → DOI → OpenAlex by-ID。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sent).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第82轮补第二内容源（strong，Crossref 路线）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

# 撤销上批「0 候选」的错误记录
WRONG=("古埃及中王国","法蒂玛王朝","非洲大湖地区","赫梯王国","贵霜帝国","仰韶文化","室利佛逝","满者伯夷",
       "帖木儿帝国","迈锡尼文明","神圣罗马帝国","汉萨同盟")
for t in WRONG:
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    if "第82轮检索记录" in pn:
        pn=re.sub(r" 【第82轮检索记录】[^【]*","",pn)
    e["pending_notes"]=(pn+" 【第82轮·检索失败已撤销】本轮首次检索时 OpenAlex 的 search 端点返回 **HTTP 429（免费日配额耗尽，$0 remaining）**，"
      "脚本把失败静默当成「0 候选」。**该结论无效**——『没检索到』不等于『不存在』（D065/D110/D144）。"
      "改用 Crossref 路线（`query.bibliographic` → DOI → OpenAlex by-ID）后，赫梯、神圣罗马帝国、汉萨同盟三条均取到合格来源；"
      "其余条目待下一轮用 Crossref 路线重跑。").strip()
    e["last_update"]=TODAY
print("已撤销 12 条错误记录")

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=82
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")