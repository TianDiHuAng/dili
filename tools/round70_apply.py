# -*- coding: utf-8 -*-
"""第70轮B：登记 3 条强来源（十字军/大平原/克里特）；澳大利亚大陆与隋唐记录。"""
import json,os,re,sys,subprocess,time,urllib.parse,unicodedata
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round70_wide.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

def add(t,b,fld,sentence,grade="strong"):
    e=T.get(t)
    if not e or not b: return False
    sid=f"openalex-{b['oid']}"
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{b['oid']}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {b['oid']} — {b['title']}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":b.get("year"),"type":"学术文献",
          "url":f"https://api.openalex.org/works/{b['oid']}","url2":f"https://doi.org/{b['doi']}" if b.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(b["title"] or "")[:200],
          "note":f"OpenAlex 作品 {b['oid']}（DOI {b.get('doi') or '无'}）；{b.get('year')}年；被引 {b['cited']}。HTTP {code}，{size} 字节。摘要长度 {b['abs_len']} 字符；主题槽命中 {b['slots']}。证据强度：{grade}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第70轮补强来源（{grade}）】{sid}（{b.get('year')}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['abs_len']} 字符）：主题槽命中 {b['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY
    return True

OK={
"十字军东征":("polities","所引 2020 年《Settlement, Identity, and Memory in the Latin East》（被引29）指出第一次十字军后在黎凡特与叙利亚形成了**四个政体**——耶路撒冷王国、安条克公国、埃德萨伯国与的黎波里伯国，并讨论「crusader states」这一术语本身是否恰当（MacEvitt 主张弃用）；本条「十字军在东地中海建立若干拉丁政权」据此。"),
"大平原":("influence","所引 2019 年《Decadal heat and drought drive body size of North American bison》（被引27）指出**大平原草原自史前以来一直支撑着数量最多的野牛**，并以数十年尺度的热与干旱检验其体型变化；本条「草原广布、历史上野牛群与游猎并存」及「干旱构成长期约束」据此。"),
"克里特文明":("polities","所引 2016 年《Seals, Craft, and Community in Bronze Age Crete》（被引31）讨论米诺斯克里特**「宫殿社会」的起源**——把宫殿出现之前的阶段识别为一次异常活跃的社会文化创新期；本条「宫殿中心由更早的社区与手工业分化中生成」据此。"),
}
n=0;log=[]
for t,(fld,sent) in OK.items():
    b=F[t]["cand"][0]
    if add(t,b,fld,sent): n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"隋唐":"宽检索（Tang dynasty China society / medieval China state administration / Tang China economy）得 42 条候选，过筛者为《Maintaining Gods in Medieval China: Temple Worship》(2010, 被引5, 摘要4313字符) 与《Dressing for the Times: Fashion in Tang Dynasty China》(2013, 被引8, 摘要3818字符)——前者是**寺庙崇拜**、后者是**服饰**，均属隋唐社会的侧面，不支撑「政体与制度」。主来源仍缺。",
"澳大利亚大陆":"宽检索得 27 条候选，最强者《Land surface phenological response to decadal climate variability》(2014, 被引143, 摘要2386字符) 讨论地表物候与气候变率，**未明确覆盖澳大利亚全境**（摘要未出现 Australia），不支撑「大陆的地形与气候总体」。主来源仍缺。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第70轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=70
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")