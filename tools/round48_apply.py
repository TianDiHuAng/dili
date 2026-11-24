# -*- coding: utf-8 -*-
"""第48轮：登记 7 条第二源；替换阿兹特克/库什的错源。"""
import json,os,sys,subprocess,time,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round48_second.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

OK={
"蒙古帝国":("influence","所引 2014 年《The Postal Roads of the Great Khans in Central…》（被引45）讨论**大汗驿道在欧亚内陆的走向与运作**；本条「驿站网络把东亚、中亚、波斯与东欧连成一体」据此。"),
"阿兹特克":("polities","所引 2017 年《Aztec Empire of the Triple Alliance as an Example of the Hegemonic Empire》明确三方联盟成立于**1428年**、由特诺奇蒂特兰、特斯科科与特拉科潘组成、1519 年西班牙人到来前扩张至中美洲广大地区，并指出其为**霸权型帝国**（不常驻军于被征服省份）。本条「三方联盟形式运作、以朝贡网络维系」据此。"),
"城市起源":("influence","所引 2024 年《City-State Civilizations: Mesoamerica's Urban Revolution》指出中美洲是全球**仅有的三个独立起源城市区之一**，并与两河流域研究的世界体系视角相互参照；本条「城市起源是多地独立发生的过程」据此。"),
"库什与努比亚":("influence","所引 2019 年《The ironworking remains in the royal city of Meroe》（被引26）以麦罗埃王城的**冶铁遗存**为对象；本条「麦罗埃时期以冶铁与商路为经济基础」据此。"),
"罗马阿非利加":("geo","所引 2004 年 Segermes 项目研究以突尼斯 Segermes 谷地的**人口与生产**为对象，重建罗马行省的农业产出与人地关系；本条「沿海农耕地带支撑谷物与橄榄输出」据此。"),
"商代":("geo","所引 2023 年《Bronze alloying recipes at Anyang during the Shang…》分析安阳出土青铜器的**合金配方**；本条「青铜礼器与手工业组织」据此。"),
"秦代":("polities","所引 2019 年《Unification and the Peerage System in Qin Dynasty》讨论秦的**统一与爵制**；本条「郡县制与统一度量衡」的表述据此（爵制部分另作说明）。"),
}
REJECT={
"古埃及新王国":"候选《Afterglow of Empire: Egypt from the Fall of the **New Kingdom** to the Saite…》研究对象是**新王国灭亡之后**（前11–前6世纪）的时期，与本条「新王国本身」时期错配（D081②），剔除。",
"加纳帝国":"候选《Youth entrepreneurship in a small-scale gold mining settlement in **Ghana**》研究的是**当代加纳北部 Kui 的小型金矿与青年创业**，与「加纳帝国」无历史关联（对象碰撞），剔除。",
}
n=0;log=[]
for t,(fld,sentence) in OK.items():
    c=F[t]["cand"];e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in e["sources"]: continue
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
          "note":f"OpenAlex 作品 {oid}（DOI {c['doi']}）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；标题含对象词（R19 精神），槽位命中 {c['slots']}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys((e["sources"] or [])+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第48轮第二源·D101】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
      f"待支撑断言「{c['claim']}」；对象词在标题、槽位命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

# 替换错源
if "openalex-W2331608140" in T["阿兹特克"]["sources"]:
    T["阿兹特克"]["sources"]=[s for s in T["阿兹特克"]["sources"] if s!="openalex-W2331608140"]
    T["阿兹特克"]["pending_notes"]=((T["阿兹特克"].get("pending_notes") or "")+
      " 【第48轮替换错源】原 W2331608140 研究的是 **Tlaxcallan（特拉斯卡拉）**——阿兹特克的敌对城邦，非本条对象；已撤出，改由 W 系（三方联盟霸权型帝国）承担。").strip()
if "openalex-W7169572344" in T["库什与努比亚"]["sources"]:
    T["库什与努比亚"]["sources"]=[s for s in T["库什与努比亚"]["sources"] if s!="openalex-W7169572344"]
    T["库什与努比亚"]["pending_notes"]=((T["库什与努比亚"].get("pending_notes") or "")+
      " 【第48轮替换错源】原 W7169572344 是 Educational Media Reviews Online 的**影像资料评介**，非研究论文；已撤出，改由麦罗埃冶铁研究承担。").strip()
for t,why in REJECT.items():
    e=T.get(t)
    if e: e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第48轮剔除】{why}").strip()
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=48
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
# 重算
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符",r"正文\s*\*{0,2}([\d,]+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
print("登记",n,"：","、".join(log))
print("剔除:",list(REJECT))
print(f"重算：≥2内容源 {g2} / 1个 {o1}")