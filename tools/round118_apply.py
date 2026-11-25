# -*- coding: utf-8 -*-
"""第111轮：Crossref 相关度检索 + DOI 桥，为 G3 条目登记第二内容源（摘要逐条阅读后接受）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-25"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

C={"W4392872715":{"title":"GLC_FCS30D: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985 to 2022 generated using dense-time-series Landsat imagery and the continuous change-detection method","year":2024,"cited":611,"chars":2829,"type":"article","doi":"10.5194/essd-16-1353-2024"}}
QUOTE={"W4392872715":"GLC_FCS30D has been developed using continuous change detection and all available Landsat imagery based on the Google Earth Engine platform."}
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
      f" 【第118轮 D150 回溯登记】{sid}（{b['year']}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['chars']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY

add("卫星遥感地表观测","W4392872715","today","所引 GLC_FCS30D 数据集论文（被引611，摘要 2,829 字符）描述了基于全部可用 Landsat 影像、覆盖 1985–2022 年 26 个时间步、35 个子类的全球 30 米土地覆盖动态监测产品；本条「用于监测土地覆盖」据此举例。")
T["大分水岭"]["pending_notes"]+=" 【第118轮 D150 回溯】W2077060230（2000，被引21）摘要写澳大利亚东北部 Laura/Carpentaria 盆地的 continental drainage divide 自中侏罗世以来未迁移；不含登记的等价词组（continental divide + eastern seaboard of australia），且仅涉东北段，维持不登记。"
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));cov["updated"]=TODAY;cov["round"]=118
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
