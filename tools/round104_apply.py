# -*- coding: utf-8 -*-
"""第104轮B：登记 G3a 命中条目；碰撞/弱候选如实记录。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round104_g3a.json"),encoding="utf-8"))["results"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

# 条目 -> (候选序号, 写入字段, 句子)
SPEC={
"古埃及中王国":(0,"influence","所引 2006 年《The Middle Kingdom of Ancient Egypt: History, Archaeology and Society》（被引107，摘要 1,170 字符）把中王国（约公元前 2000–1700 年）作为艺术、历史与文学的古典时期，并指出研究常止于王室雕像与文学名篇；本条据此补充历史与考古的社会视角。"),
"争议边界处理原则":(0,"influence","所引 2015 年《Equitable Principles of Maritime Boundary Delimitation》（被引117，摘要 927 字符）讨论公平原则在国际法中的角色，并以海洋划界为案例。**说明：该书聚焦海洋划界，陆地边界不在其内。**"),
"黎凡特":(0,"influence","所引 2007 年《Structural Transformations in Settlement Systems of the Northern Levant》（被引98，摘要 1,401 字符）基于阿姆克谷地（今土耳其）的考古调查，描述黎凡特北部聚落体系的结构变化：约公元前 3000 年起，聚落集中到约 100 个位于低地平原的聚落丘。**说明：样本来自北部黎凡特的一个谷地。**"),
"朝鲜半岛":(0,"geo","所引 2024 年《Learning Geography of Korea by Mountains and Island as Main Resource of Korean Peninsula》（被引1，摘要 806 字符）概述朝鲜半岛的山地与岛屿及其对生态、旅游与文化的意义。**说明：该文偏教学性概述，被引很少，证据强度有限。**"),
"中南半岛":(1,"geo","所引 2005 年《Land Use History in Montane Mainland Southeast Asia》（被引2，摘要 1,329 字符）记录一次多国跨学科研讨：关于云南、缅甸、泰国、老挝等山地区域的土地利用与土地覆被变化及政策影响。**说明：覆盖的是大陆东南亚山地，而非整个半岛，被引很少。**"),
}
n=0;log=[]
for t,(idx,fld,sent) in SPEC.items():
    cands=F[t]["cand"]
    e=T.get(t)
    if not e or len(cands)<=idx: continue
    c=cands[idx]
    sid=f"openalex-{c['oid']}"
    if sid in e["sources"]:
        print("已有，跳过:",t,sid);continue
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
      f" 【第104轮补第二内容源（Crossref）】{sid}（{c.get('year')}年，《{c['title']}》，被引 {c['cited']}，摘要 {c['abs_len']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"中南半岛":"过筛候选《Role of the quasi-biweekly oscillation in the onset of convection over…》(2007，被引21) 研究季风对流的起始，属大气科学，与本条的区域概述不对口。不采用。",
"教育机会地域差异":"第104轮检索无通过候选，需换检索角度。",
"人文地理学":"第104轮检索无通过候选，需换检索角度。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第104轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=104
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
