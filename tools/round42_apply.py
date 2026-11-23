# -*- coding: utf-8 -*-
"""第42轮：为 46 条条目登记第二独立来源，按相关度分级标注支撑范围。"""
import json,os,sys,subprocess,time,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
SCR=json.load(open(os.path.join(ROOT,"reports","round42_screen.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

# 分级：strong=对象与主题一致；partial=主题一个侧面；core=仅支撑某句
GRADE={
"古埃及早王朝":"strong","古埃及古王国":"strong","苏美尔城邦":"strong","法兰克王国":"strong",
"莫斯科公国":"strong","奥尔梅克":"strong","玛雅文明":"strong","波利尼西亚":"strong",
"气候带":"strong","青藏高原":"strong","落基山脉":"strong","东非大裂谷":"strong",
"两河流域":"strong","爱琴海世界":"strong","罗马帝国":"strong","丝绸之路":"strong",
"克里特文明":"strong","斯瓦希里海岸":"strong","埃塞俄比亚高原":"strong","周代":"strong",
"宋代":"strong","十字军东征":"strong","黑海海峡":"strong","蒂亚瓦纳科":"strong",
"新西兰北岛":"strong","夏威夷群岛":"strong","拉普拉塔平原":"strong","撒哈拉沙漠":"strong",
"大平原":"strong","印加帝国":"strong","澳大利亚原住民":"strong","巴西殖民经济":"strong",
"澳大利亚大陆":"partial","南极大陆":"partial","季风系统":"partial","白令陆桥":"partial",
"文艺复兴意大利":"partial","维京时代":"partial","大分水岭":"partial","阿塔卡马沙漠":"partial",
"毛利人":"partial","加勒比海群岛":"partial","大自流盆地":"partial","新西兰南岛":"partial",
"马丘比丘":"partial","河流三角洲":"core",
}
WHY={"strong":"该文献与本条对象一致，可作年代/机制断言的第二独立来源",
"partial":"该文献涉本条对象但聚焦某一侧面，仅支撑相应段落，其余段落仍为常识性地理描述",
"core":"该文献仅与本条某一概念相关，作背景登记，不作事实断言依据"}
n=0;log=[]
for t,c in SCR["ok"].items():
    e=T.get(t)
    if not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
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
          "note":f"OpenAlex 作品 {oid}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host')}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符。"})
        have.add(sid)
    srcs=list(dict.fromkeys((e.get("sources") or [])+[sid]))
    e["sources"]=srcs
    g=GRADE.get(t,"partial")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第42轮第二来源（{g}）】{sid}（{c.get('year')}年，《{c['title'][:70]}》，{c.get('host')}，DOI {c['doi']}，被引 {c.get('cited')}）：{WHY[g]}。").strip()
    e["last_update"]=TODAY
    n+=1;log.append((t,g))
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=42;cov["round_processed"]=n
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("登记第二来源",n,"条；分级：",collections.Counter(g for _,g in log))
# 重新统计单源
SHELL={"britannica-regions","wikipedia-regions","un-m49","s010-unesco-org","s070-cbd-int","s071-cbd-int","ap-human-geo","s013-fao-org"}
multi=sum(1 for e in T.values() if e["level"]=="L2" and len([s for s in e["sources"] if s not in SHELL and not s.startswith("wb-")])>=2)
print("现有 ≥2 内容源的条目:",multi,"/",len(T))