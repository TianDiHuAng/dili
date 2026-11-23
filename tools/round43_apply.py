# -*- coding: utf-8 -*-
"""第43轮续：登记 0 源条目的学术来源（分级 + 剔除偏题）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round43_zerosrc.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文"}

REJECT={"马里帝国":"候选为《The Mande Creation Myth》的**书评**（book review），按 D082 不作内容来源",
"五大湖":"候选为《Hitchhiking Bats on the Great Lakes》，研究对象是**蝙蝠**而非湖泊本身，对象不符（D095）"}
GRADE={
"古希腊城邦":"strong","萨赫勒带":"strong","科罗拉多高原":"strong","安第斯山脉":"strong","洋流":"strong",
"板块构造":"strong","南极条约体系":"strong","亚马逊河":"strong","密西西比河":"strong","迦太基":"strong",
"阿契美尼德波斯":"partial","白令陆桥":"partial","中美洲地峡":"partial","黄河流域":"partial",
"游牧":"partial","澳大利亚原住民":"partial","尼罗河谷":"partial","亚马逊盆地":"partial",
"河流三角洲":"partial","北美冰盖":"partial","大分水岭":"partial","人口迁移":"partial","植物物候变化":"partial",
}
n=0;log=[]
for t,c in F.items():
    if not c or t in REJECT: continue
    e=T.get(t)
    if not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in [s for s in e["sources"]]: continue
    if sid not in have:
        code=0;size=0
        for _ in range(3):
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                    if code==200: break
                time.sleep(4)
            except Exception: time.sleep(4)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host')}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符，对象词命中 {c.get('hits')} 次。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys((e.get("sources") or [])+[sid]))
    g=GRADE.get(t,"partial")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第43轮补源（{g}）】{sid}（{c.get('year')}年，《{c['title']}》，{c.get('host')}，DOI {c['doi']}，被引 {c.get('cited')}，对象词命中 {c.get('hits')} 次）："
      + ("该文献与本条对象一致，可作相关断言的来源。" if g=="strong"
         else "该文献涉本条对象但聚焦某一侧面，仅支撑相应段落，其余段落仍为常识性地理描述。")).strip()
    e["last_update"]=TODAY
    n+=1;log.append((t,g))
for t,why in REJECT.items():
    e=T.get(t)
    if e: e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第43轮剔除】{why}。").strip()
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=43;cov["round_processed"]=n
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("登记",n,"条；",collections.Counter(g for _,g in log))
# 重算真实口径
SHELL={"britannica-regions","wikipedia-regions","un-m49","s010-unesco-org","s070-cbd-int","s071-cbd-int","ap-human-geo","s013-fao-org"}
def ac(e):
    return sum(1 for s in e["sources"] if s.startswith(("openalex-","livius-")) or s in ("nasa-ice-cores","usgs-glaciers-pdf","noaa-global-temp","nasa-pine-island"))
z=sum(1 for e in T.values() if ac(e)==0);o=sum(1 for e in T.values() if ac(e)==1);g2=sum(1 for e in T.values() if ac(e)>=2)
print(f"全站真实口径：0源 {z} / 1源 {o} / ≥2源 {g2}")