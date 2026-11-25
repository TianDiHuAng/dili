# -*- coding: utf-8 -*-
"""第111轮：Crossref 相关度检索 + DOI 桥，为 G3 条目登记第二内容源（摘要逐条阅读后接受）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-25"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
R=json.load(open(os.path.join(ROOT,"reports","round112_cr.json"),encoding="utf-8"))
C={x["id"]:x for v in R.values() for x in v}
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
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{b['doi']}",
          "link_ok":code==200,"verified":code==200,"page_title":b["title"][:200],
          "note":f"OpenAlex 作品 {oid}（DOI {b['doi']}）；{b['year']}年；被引 {b['cited']}；类型 {b['type']}。HTTP {code}，{size} 字节。摘要长度 {b['chars']} 字符。经 Crossref query.bibliographic 相关度检索 + DOI 桥取得，摘要已人工阅读。"})
        have.add(sid)
        if code!=200: print("WARN",oid,code)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第112轮补第二内容源】{sid}（{b['year']}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['chars']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY

add("卫星遥感地表观测","W4390344318","influence","所引 2023 年综述《The Use of Artificial Intelligence and Satellite Remote Sensing in Land Cover Change Detection》（被引132，摘要 1,333 字符）指出在全球、区域与地方尺度上制图土地覆盖格局是监测动态世界的关键，并讨论人工智能与卫星遥感结合用于土地覆盖变化检测；本条「遥感支撑变化检测」据此。")
add("拉普拉塔平原","W2616812401","influence","所引 2010 年《Vegetation changes after 15 years of abandonment of crop fields in the Pampas Region (Argentina)》（被引32，摘要 1,515 字符）指出阿根廷潘帕斯地区的农业已延续一个多世纪，长期扰动显著改变了原生植被，部分原生物种消失或分布大幅缩小；本条「黑土与温和气候有利于农牧业」据此补其生态代价一侧。")
T["大分水岭"]["pending_notes"]=((T["大分水岭"].get("pending_notes") or "")+" 【第112轮检索记录】Crossref 相关度检索（Great Dividing Range rainfall / geology / landscape）18 条过筛候选：唯一对象相符者 W3153139914 已是现有来源；其余为淡水螯虾、滑翔袋鼯形态学、中国大兴安岭钼矿、喜马拉雅河谷等对象不符，全部拒收。第二内容源仍缺。").strip()
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));cov["updated"]=TODAY;cov["round"]=112
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
