# -*- coding: utf-8 -*-
"""第45轮：按 D100 登记 6 条（断言已匹配），剔除 3 条偏题，清理残留句。"""
import json,os,sys,subprocess,time,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round45_claims.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文"}

OK={"马里帝国":("influence","所引 1982 年《Myth and Metrology: The Early Trans-Saharan Gold Trade》讨论跨撒哈拉**黄金贸易的早期度量与流通**；本条「控制黄金贸易是财富与权力的重要来源」据此。"),
"文艺复兴意大利":("influence","所引 2017 年研究讨论**意大利文艺复兴时期的艺术赞助**；本条「城市赞助为艺术与学术提供条件」据此。"),
"白令陆桥":("geo","所引 1973 年研究重建**白令地区的海平面历史**，说明陆桥出露与淹没的时段；本条「冰期海平面下降时出露」据此。"),
"安第斯山脉":("geo","所引 2008 年研究综述**安第斯海拔分布的生物地理格局**；本条「海拔差异形成垂直气候带」据此。"),
"五大湖":("geo","所引 2024 年研究以优化方法讨论**五大湖水位**；本条「季节水位变化是重要水文特征」据此。"),
"洋流":("geo","所引 2001 年研究用海洋边缘密度约束**环流结构**；本条「密度差驱动环流」据此。"),
}
REJECT={"日本列岛":"候选为《Seismic tomography of the **Pampean** flat-slab subduction》（阿根廷潘帕地区），对象不是日本列岛，已剔除（同为地名碰撞）。",
"古希腊城邦":"候选为《Mountains in **Greek and Roman Art**》，主题是艺术中的山，不支撑「山地分割与海上通道并存」这一地形断言，已剔除。",
"克里特文明":"候选为《The artistic reception of Minoan Crete》，主题是**艺术接受史**，不支撑「海上贸易与宫殿再分配体系」，已剔除。"}
n=0;log=[]
for t,(fld,sentence) in OK.items():
    c=F.get(t);e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in (e["sources"] or []): continue
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
          "note":f"OpenAlex 作品 {oid}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；摘要同时命中「{c['k1']}」与「{c['k2']}」，对应待支撑断言。",
        })
        have.add(sid)
    e["sources"]=list(dict.fromkeys((e["sources"] or [])+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第45轮补源·按断言选文献（D100）】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}）：先在正文定位待支撑句「{c['claim']}」，再选此文献；摘要命中「{c['k1']}」「{c['k2']}」，已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

# 清理日本列岛残留句（来源已剔除但落点句仍在）
jp=T.get("日本列岛")
if jp:
    jp["influence"]=re.sub(r" 所引 2017 年研究讨论家畜引入日本列岛的过程；本条仅据此写「列岛与大陆的生物交流」，不作地质断言。","",jp.get("influence") or "")
    jp["pending_notes"]=((jp.get("pending_notes") or "")+" 【第45轮清理】原 influence 残留已被剔除来源的落点句（家畜引入），已删除。").strip()
for t,why in REJECT.items():
    e=T.get(t)
    if e: e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第45轮剔除】{why}").strip()

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=45;cov["round_processed"]=n
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
# 重算四分类
MIN=800
S={s["id"]:s for s in sd["sources"]}
def hb(sid):
    note=(S.get(sid) or {}).get("note") or ""
    if "stub" in note.lower(): return False
    m=re.search(r"摘要长度\s*(\d+)\s*字符",note) or re.search(r"正文\s*(\d+)\s*字符",note) or re.search(r"摘要\s*(\d+)\s*字符",note)
    if m: return int(m.group(1))>=MIN
    m=re.search(r"(\d{3,7})\s*字节",note)
    if m: return int(m.group(1))>=MIN
    return None
a1=a2=a3=0
for e in T.values():
    b=sum(1 for s in e["sources"] if hb(s) is True)
    if b>=2: a3+=1
    elif b==1: a2+=1
    else: a1+=1
print("登记",n,"：","、".join(log))
print("剔除:",list(REJECT))
print(f"四分类：别名页only {a1} / 1源 {a2} / ≥2源 {a3}")