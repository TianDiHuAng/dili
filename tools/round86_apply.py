# -*- coding: utf-8 -*-
"""第86轮B：登记 6 条；4 条侧面/不相关如实记录。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round86_imp4.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

SPEC={
"阿拉伯征服北非":("influence","所引 1987 年《A History of the Maghrib in the Islamic Period》（**被引 400**）是伊斯兰时期马格里布的通史；本条「7–8 世纪的阿拉伯征服重塑北非的语言、宗教与行政格局」据此。"),
"桑海帝国":("polities","所引 2018 年《The Fall of the Songhai Empire》（摘要 937 字符）讨论桑海北疆**图阿雷格人**的失控与帝国覆亡的直接后果；本条「桑海在 1591 年遭摩洛哥入侵后解体」据此。"),
"萨珊波斯":("polities","所引 2016 年《Sasanian Empire》（摘要 800 字符）概述萨珊帝国的制度与地位；本条「萨珊以琐罗亚斯德教为国教、与罗马—拜占庭长期对峙」据此。"),
"克里特文明":("influence","所引 2017 年研究（摘要 2,001 字符）以**房屋、空间与建筑**为切入点研究晚青铜时代米诺斯的**家庭内关系**与身份实践；本条「米诺斯社会关系通过居住空间与物质实践再生产」据此。"),
"河中地区":("influence","所引 2022 年《Mongol invasion of Transoxiana 1219–1221》（摘要 1,310 字符）讨论蒙古对**河中地区**的入侵；本条「河中作为东西商路枢纽、屡遭北方游牧势力冲击」据此。"),
"十字军东征":("polities","所引 2016 年《The Fifth Crusade in Context: The Crusading Movement…》（摘要 1,247 字符）把第五次十字军置于**十字军运动的整体脉络**中讨论；本条「十字军是持续两个世纪的运动、非单一事件」据此。"),
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
      f" 【第86轮补第二内容源（strong，Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"笈多王朝":"过筛候选《Treasures of the Gupta **Empire**》(2024, 摘要 1,356) 主题是**笈多王朝的钱币之美与复杂性**（钱币学）——与第76轮命中的「Role of Coins」同类。笈多条的文献面确实以钱币学为主。",
"吠陀时代":"过筛候选《Pre-Historic Intra-Continental Africa-India Proximity Series》(2023, 摘要 1,679) 讨论**非洲与印度的史前邻近性**（泛论），不涉吠陀时代的社会与宗教。",
"明清":"过筛候选《Editing, Circulating, and Reading Huang Zhong's Hai yu》(2019, 摘要 927) 是**一本书的编辑、流传与阅读史**（书籍史侧面），不支撑明清的国家与社会整体。",
"马来群岛":"本轮 **0 候选**（检索成功，HTTP 失败率 1%）。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第86轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=86
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")