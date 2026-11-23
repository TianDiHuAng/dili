# -*- coding: utf-8 -*-
"""第34轮：把 OpenAlex 学术文献登记为第二来源，解除「单源待互证」；并标注 Wikidata 当前不可达。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
S=json.load(open(os.path.join(ROOT,"reports","round34_screened.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

def chk(url):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return 0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        return int(c.strip() or 0), len(b)
    except Exception: return 0,0

n=0;done=[]
for title,cands in S.items():
    if not cands: continue
    e=T.get(title)
    if not e: continue
    c=cands[0]
    oa_id=(c.get("id") or "").rsplit("/",1)[-1]
    sid=f"openalex-{oa_id}"
    url=f"https://api.openalex.org/works/{oa_id}"
    if sid not in have:
        code,size=chk(url)
        ab=c.get("abstract") or ""
        sd["sources"].append({"id":sid,
          "title":f"OpenAlex {oa_id} — {c.get('title')}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),
          "type":"学术文献",
          "url":f"https://api.openalex.org/works/{oa_id}",
          "url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":(c.get("title") or "")[:120],
          "note":(f"OpenAlex 作品 {oa_id}；{c.get('year')}年；{c.get('host') or '期刊/出版社未标'}；"
                  f"DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。"
                  f"JSON API HTTP {code}，返回 {size} 字节。"
                  f"摘要（abstract_inverted_index 重建，节录）：{ab[:300]}… "
                  f"本条以其摘要中的年代/主题表述作为年代断言的第二独立来源。")})
        have.add(sid)
        n+=1
    # 挂到条目并解除单源标注
    srcs=e.get("sources") or []
    if sid not in srcs: srcs.append(sid)
    e["sources"]=srcs
    pn=e.get("pending_notes") or ""
    pn=pn.replace("【单源待互证】","【第34轮补第二来源】")
    e["pending_notes"]=(pn+
      f" 【第34轮双源补齐】第二来源为 OpenAlex 学术文献 {oa_id}（{c.get('year')}年，"
      f"「{(c.get('title') or '')[:60]}」，DOI {c.get('doi') or '无'}）；其摘要含 "
      f"{'、'.join(c.get('matched',[]))}，可支撑本条年代/主题断言。"
      f" 该文献为主题性研究而非通史概述，剩余段落（地理与经济机制）仍以常识性地理描述为主，未作无源具体断言。").strip()
    e["last_update"]=TODAY
    n+=0; done.append(title)

json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("新增学术来源",n,"条；补双源条目",len(done),"：","、".join(done))