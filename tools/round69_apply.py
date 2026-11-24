# -*- coding: utf-8 -*-
"""第69轮B：登记 6 条强来源；4 条不匹配的另找或记录。"""
import json,os,re,sys,subprocess,time,urllib.parse,unicodedata
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round69_g1.json"),encoding="utf-8"))
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
      f" 【第69轮补强来源（{grade}）】{sid}（{b.get('year')}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['abs_len']} 字符）：主题槽命中 {b['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY
    return True

OK={
"玛雅文明":("influence","所引 2003 年《Climate and the Collapse of Maya Civilization》（**被引 1145**）以古气候记录讨论**古典期崩溃**与干旱的关系；本条「干旱、政治冲突与贸易变化被视为城市中心衰落的相关因素，学界无定论」据此——该文是「干旱说」的代表性研究，不等于定论。"),
"印加帝国":("influence","所引 1993 年《Segmentary State Formation and the Ritual Control of Water》（被引162）指出印加史研究中存在一个悖论：一般承认其为神权古国（王为太阳之子），但标准描述却很少提及**水与灌溉的仪式性控制**在政治结构中的作用；该文据此论证**水的仪式控制是国家形成的一部分**。本条「国家通过道路、仓储与劳役组织资源，并以仪式维系权威」据此。"),
"澳大利亚原住民":("influence","所引 2002 年《Visions from the Past: The Archaeology of Australian Aboriginal Art》（被引169）系统讨论澳大利亚原住民**岩画艺术**的考古；本条「原住民以岩画与口传维系与土地的联系」据此（艺术与信仰侧面，社会制度另需来源）。"),
"孔雀王朝":("polities","所引 2006 年《The Mauryan empire in early India》（被引24）讨论孔雀帝国的**政体与治理**；本条「孔雀王朝以行政与军事控制印度次大陆大部」据此。"),
"隋唐":("polities","所引 1999 年《Son of Heaven and Heavenly Qaghan: Sui-Tang China and Its Neighbors》（被引82）讨论隋唐的**天下秩序与对外关系**（皇帝同时称「天子」与「天可汗」）；本条「隋唐以朝贡与羁縻体系处理周边关系」据此。"),
"维京时代":("influence","所引 2020 年《Population genomics of the Viking world》（**被引 398**）以全基因组数据重构**维京人的流动与混合**；本条「维京时代的扩张伴随人群交流而非单向劫掠」据此。"),
}
n=0;log=[]
for t,(fld,sent) in OK.items():
    b=F[t]["cand"]
    if add(t,b,fld,sent): n+=1;log.append(t)
print("登记:",n,"、".join(log))

REC={
"澳大利亚大陆":"过筛候选《Refining Rodinia: Geologic Evidence for the Australia–Western U.S. connection》(1999, 被引668) 讲的是**前寒武纪超大陆（Rodinia）的拼合**，属深部地质史，不支撑「大陆的地形与气候总体」；本轮不采用，主来源仍缺。",
"十字军东征":"过筛候选《Patterns in Medieval Trade: The Commerce of Amalfi **Before the Crusades**》(1968, 被引155) 的时段是「十字军**之前**」，与本条 11–13 世纪不重叠（D108 时期槽否决）；不采用。",
"大平原":"过筛候选《Effects of agriculture, urbanization, and climate on water quality in the **Canadian** Great Plains》(1999, 被引407) 只涉加拿大段**水质**，与本条农业/野牛/交通/沙尘暴诸断言无对应；不采用。",
"克里特文明":"过筛候选《The Volcanic Destruction of Minoan Crete》(**1939**, 被引224) 对象对位（米诺斯文明），但为 1939 年的**火山摧毁说**，学界其后多有修正；本轮不登记为主来源，仅记录为可引的早期假说（如需可降为旁证）。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第69轮检索记录】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=69
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")