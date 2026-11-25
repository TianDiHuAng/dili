# -*- coding: utf-8 -*-
"""第111轮：Crossref 相关度检索 + DOI 桥，为 G3 条目登记第二内容源（摘要逐条阅读后接受）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-25"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

C={"W3121385383":{"title":"Spatial variation of erosion rates and passive margin escarpment embayment from New England, NSW and Bellenden Ker, Queensland","year":2020,"cited":0,"chars":3246,"type":"conference-abstract","doi":"10.5194/egusphere-egu2020-10431"}}
QUOTE={"W3121385383":"The eastern seaboard of Australia is characterized by a passive margin and a continental divide that separates the inland-draining rivers from those that drain to the Coral and Tasman seas."}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

def add(t,oid,fld,sentence):
    b=C[oid];e=T[t];sid=f"openalex-{oid}"
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {b['title']}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":b["year"],"type":"学术文献",
          "url":f"https://api.openalex.org/works/{oid}","url2":(f"https://doi.org/{b['doi']}" if b['doi'] else None),
          "link_ok":code==200,"verified":code==200,"page_title":b["title"][:200],"abstract_quote":QUOTE.get(oid),
          "note":f"OpenAlex 作品 {oid}（DOI {b['doi']}）；{b['year']}年；被引 {b['cited']}；类型 {b['type']}。HTTP {code}，{size} 字节。摘要长度 {b['chars']} 字符。经 Crossref query.bibliographic 相关度检索 + DOI 桥取得，摘要已人工阅读。"})
        have.add(sid)
        if code!=200: print("WARN",oid,code)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第117轮补第二内容源（D141）】{sid}（{b['year']}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['chars']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY

add("大分水岭","W3121385383","geo","所引 2020 年 EGU 会议摘要（被引0，摘要 3,246 字符，经 D140 摘要通道登记）指出澳大利亚东岸为被动大陆边缘，其大陆分水岭把内流河与流向珊瑚海、塔斯曼海的河流分开，分水岭向海一侧为分隔沿海平原与高原的大断崖；本条「河流向东或向西流」据此。该文为会议摘要、被引为零，证据强度有限。")
T["大分水岭"]["pending_notes"]+=" 【第117轮】W2105767775（1996，被引112）摘要只写 SE Australia 被动陆缘与新英格兰台地，不含对象词或登记的等价词组，D140 通道仍不放行，未登记。"
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));cov["updated"]=TODAY;cov["round"]=117
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
