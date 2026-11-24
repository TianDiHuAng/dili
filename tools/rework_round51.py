# -*- coding: utf-8 -*-
"""第51轮返工：季风换主来源、南极降个案、库什补2条、修硬编码TODAY。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","report":"技术报告"}

def fetch(oid):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",
              f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
            d=json.loads(p.stdout.decode("utf-8","ignore"))
            if d.get("id"): return d
        except Exception: pass
        time.sleep(4)
    return {}

# ===== 1 修 round2_apply.py 硬编码 TODAY =====
p2=os.path.join(ROOT,"tools","round2_apply.py")
t2=open(p2,encoding="utf-8").read()
if 'TODAY = "2026-11-22"' in t2:
    t2=t2.replace('TODAY = "2026-11-22"','TODAY = os.environ.get("DILI_TODAY", "2026-11-24")')
    open(p2,"w",encoding="utf-8").write(t2)
    print("已修 round2_apply.py 的 TODAY 硬编码")

# ===== 2 季风系统：换主来源 + 删零支撑成分 =====
mo=T["季风系统"]
mo["geo"]=("海陆热力差异与青藏高原、西太平洋副热带高压共同决定季风的进退；雨带随季节自南向北推进，形成华南前汛期、江淮梅雨与华北雨季。"
  "（「雨带随季节推进」为本条常识性气候描述，**不挂具体文献**。）")
NEW_MO=("W2046274250","Thermal Controls on the Asian Summer Monsoon")
d=fetch(NEW_MO[0])
sid=f"openalex-{NEW_MO[0]}"
if sid not in have and d:
    code=200;size=0
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
      f"https://api.openalex.org/works/{NEW_MO[0]}"],capture_output=True,timeout=30)
    raw=p.stdout.decode("utf-8","ignore")
    if "__HTTP__" in raw:
        bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
    sd["sources"].append({"id":sid,"title":f"OpenAlex {NEW_MO[0]} — {d.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
      "year":d.get("publication_year"),"type":TYP.get(d.get("type"),"学术文献"),
      "url":f"https://api.openalex.org/works/{NEW_MO[0]}","url2":f"https://doi.org/{d.get('doi')}",
      "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(d.get("title") or "")[:200],
      "note":f"OpenAlex 作品 {NEW_MO[0]}（DOI {d.get('doi')}）；{d.get('publication_year')}年；Scientific Reports；被引 {d.get('cited_by_count')}。HTTP {code}，{size} 字节。摘要结论句：「the Asian summer monsoon systems are controlled mainly by thermal forcing… the South Asian monsoon south of 20°N by land-sea thermal contrast」。"})
    have.add(sid)
mo["influence"]=("所引 2012 年《Thermal Controls on the Asian Summer Monsoon》（Scientific Reports，**被引 915**）指出：**亚洲夏季风系统主要由热力强迫控制**，"
  "其中**20°N 以南的南亚季风由海陆热力差异控制**。本条据此写「海陆热力差异是季风的主要驱动之一」，"
  "并保留青藏高原与副热带高压的作用（后者为常识性补充，未挂该文）。")
mo["sources"]=[s for s in mo["sources"] if s!="openalex-W2124570107"]
mo["sources"]=list(dict.fromkeys(mo["sources"]+[sid]))
mo["pending_notes"]=((mo.get("pending_notes") or "")+
  " 【第51轮返工·换主来源】原用 2010 年《Understanding the Predictability of East Asian Summer Monsoon…》——该文是**可预测性技巧研究**，"
  "摘要中 season/advance/driv/mechan **均为 0 命中**，「驱动」「随季节推进」属越界（D083④）。已换用 2012 年《Thermal Controls on the Asian Summer Monsoon》（被引915），"
  "其结论句明写「主要由热力强迫控制…南亚 20°N 以南由海陆热力差异控制」；同时删除「随季节推进」这一零支撑成分并标为常识。").strip()
mo["last_update"]=TODAY

# ===== 3 南极大陆：删零支撑成分，降个案 =====
an=T["南极大陆"]
an["geo"]=("南极大陆约 98% 的面积被冰盖覆盖，露岩区面积比例极小（属常识性量级表述，本条的学术来源未测该比例）。"
  "冰盖之下保存着古老的冰下地貌：所引 2024 年研究以**甘布尔采夫冰下山脉**为例，指出该区自约 3400 万年前大规模 glaciation 以来长期处于**冷基、非侵蚀**状态，"
  "因而保存了古老的树枝状谷网。这一发现是**个案保存性证据**，不等同于大陆地貌的总体描述。")
an["influence"]=("冰盖的存在使南极的地貌演化史与其它大陆显著不同：冰下景观在长时间尺度上被「冻结」保存，而非被流水持续改造。"
  " 所引 2024 年研究据甘布尔采夫冰下山脉保存的（>34 Ma）树枝状谷网论证这一点；该论证的适用范围是**保存性**，不是露岩比例或大陆地形统计。")
an["pending_notes"]=((an.get("pending_notes") or "")+
  " 【第51轮返工】① 删除「露岩区极少」——所引摘要中 exposed/nunatak/bedrock **均 0 命中**，该文未测大陆露岩比例；现标为常识性量级表述并注明来源未测。"
  "② 原以摘**要首句**（讨论大陆演化的背景框架句）支撑通例，属 D092+D083④ 叠加；已降为**个案保存性证据**，限定语与断言同宽。").strip()
an["last_update"]=TODAY

# ===== 4 库什：补 2 条（纳帕塔政体 + 冶铁生产），两说并陈 =====
ku=T["库什与努比亚"]
for oid,why,fld,sentence in [
 ("W2507574122","纳帕塔期政体形成","polities",
  "所引 2016 年《Entanglement and the Formation of the Ancient Nubian Napatan State》（American Anthropologist，被引65）讨论**纳帕塔国家的形成**（约前750–前656年），"
  "强调其与埃及的纠缠关系；本条「库什作为独立政体在纳帕塔期形成」据此。"),
 ("W2894840915","麦罗埃冶铁传统","influence",
  "所引 2018 年《The ancient iron mines of Meroe》（Azania，被引34）指出麦罗埃的**冶铁传统延续一千余年**（约前7世纪至公元6世纪），并认为该地曾产出可观数量的铁。"
  " 须并陈的是：同组 2019 年炉渣测年研究认为麦罗埃作为都城期间（前300–公元300）堆积稀少、工业组织重组——**两说并存**，本条不作单一定论。"),
]:
    d=fetch(oid);sid=f"openalex-{oid}"
    if sid not in have and d:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {d.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":d.get("publication_year"),"type":TYP.get(d.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{d.get('doi')}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(d.get("title") or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {d.get('doi')}）；{d.get('publication_year')}年；被引 {d.get('cited_by_count')}。HTTP {code}，{size} 字节。用途：{why}。"})
        have.add(sid)
    ku["sources"]=list(dict.fromkeys(ku["sources"]+[sid]))
    ku[fld]=((ku.get(fld) or "")+" "+sentence).strip()
ku["influence"]=("麦罗埃时期的**冶铁**是长期讨论的问题，现有研究结论不一：2018 年矿冶研究认为冶铁传统延续千余年、产出可观；"
  "而 2019 年炉渣测年研究认为都城期（前300–公元300）堆积稀少、工业组织发生重组。**两说并存**，本条不作单一定论。"
  " 商路与商品结构目前**无合格主来源**（唯一候选被引 0，仅列旁证）。")
ku["pending_notes"]=re.sub(r" 【第51轮检索无果】[^【]*","",ku.get("pending_notes") or "")
ku["pending_notes"]=((ku.get("pending_notes") or "")+
  " 【第51轮返工·检索记录更正】原写「唯一过筛候选仍是 2019 年那篇…故无合格来源」——这是**只查了 Crossref 一条检索式**（且绑了 trade 一词）就下的结论，违反 D099「无来源≠未检索」。"
  " 经 OpenAlex 补充检索，**纳帕塔政体**（W2507574122, 被引65）与**麦罗埃冶铁**（W2894840915, 被引34）均有可用文献，已登记并写落点；"
  "仅**商路与商品结构**确无合格主来源。另：原「反向证据」标签失准——2019 说的是「都城期堆积稀少、组织重组」，非「冶铁不存在」；已改为两说并陈。").strip()
ku["time_or_place"]="约公元前2180年起（Wikidata P571，精度=年）；英文描述另作「c. 1070 BCE – c. CE 350」；本条取后者作为王国主体跨度，两说并注"
ku["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=51
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
z0=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==0)
print(f"返工完成；重算 ≥2 {g2} / 1个 {o1} / 0个 {z0}")