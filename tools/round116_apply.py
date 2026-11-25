# -*- coding: utf-8 -*-
"""第111轮：Crossref 相关度检索 + DOI 桥，为 G3 条目登记第二内容源（摘要逐条阅读后接受）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-25"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

C={"W3036819405":{"title":"The history of the Notion of the State in West Africa: from the destruction of empires to the emergence of the modern state resulting from colonization (the case of the Mali Empire)","year":2020,"cited":5,"chars":1515,"type":"article","doi":"10.22363/2312-8127-2020-12-1-28-34"},
"W2967453577":{"title":"Beyond the Mali Empire – A New Paradigm for the Sunjata Epic.","year":2018,"cited":42,"chars":989,"type":"article","doi":None}}
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
          "link_ok":code==200,"verified":code==200,"page_title":b["title"][:200],
          "note":f"OpenAlex 作品 {oid}（DOI {b['doi']}）；{b['year']}年；被引 {b['cited']}；类型 {b['type']}。HTTP {code}，{size} 字节。摘要长度 {b['chars']} 字符。经 Crossref query.bibliographic 相关度检索 + DOI 桥取得，摘要已人工阅读。"})
        have.add(sid)
        if code!=200: print("WARN",oid,code)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第116轮补第二内容源】{sid}（{b['year']}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['chars']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY

add("马里帝国","W3036819405","polities","所引 2020 年《The history of the Notion of the State in West Africa…(the case of the Mali Empire)》（被引5，摘要 1,515 字符）指出今马里境内最大、最著名的帝国是 9 世纪的加纳帝国，13 世纪由马里（曼德）帝国继之，其范围涉及今马里、毛里塔尼亚及几内亚、塞内加尔等西非国家；本条「马里帝国承接加纳帝国、为西非萨赫勒的大型政体」据此。")
add("马里帝国","W2967453577","polities","所引 2018 年《Beyond the Mali Empire – A New Paradigm for the Sunjata Epic》（被引42，摘要 989 字符）提醒：松迪亚塔史诗的主题远早于 13 世纪，史诗中的谱系应读作治理之道的教谕而非历史人物的记录；因此本条不据史诗确定马里帝国的建立者与年代细节。")
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));cov["updated"]=TODAY;cov["round"]=116
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
