# -*- coding: utf-8 -*-
"""第47轮B：口径修正——数据端点（wb-*）不计入「内容来源」；重算。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}
MIN=800

def is_data_source(sid):
    """数据端点：返回结构化数值，不能支撑文字断言。"""
    return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))

def has_body(sid,e=None):
    """内容源判定：非数据端点 + 实测字符数 ≥ MIN。"""
    if is_data_source(sid): return False          # 数据源永不计入内容源
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符",
                    r"正文\s*\*{0,2}([\d,]+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None

cat={"ge2_content":[],"one_content":[],"data_only":[],"unmeasured":[]}
for t,e in T.items():
    b=sum(1 for s in e["sources"] if has_body(s,e) is True)
    u=sum(1 for s in e["sources"] if has_body(s,e) is None)
    has_data=any(is_data_source(s) for s in e["sources"])
    if b>=2: cat["ge2_content"].append(t)
    elif b==1: cat["one_content"].append(t)
    elif u>0: cat["unmeasured"].append(t)
    else: cat["data_only"].append(t)
print("内容源分类：",{k:len(v) for k,v in cat.items()})
print("  data_only（仅数据端点+别名页）:",cat["data_only"][:15])
json.dump({"round":47,"date":TODAY,
 "definition":"内容来源 = 非数据端点（排除 wb-*/usgs-eq/noaa-current/ats-parties/wikidata-）且实测正文≥800字符；数据端点返回的是数值结构，不能支撑文字断言，单列",
 "categories":{k:len(v) for k,v in cat.items()},
 "data_only_list":cat["data_only"],"unmeasured_list":cat["unmeasured"]},
 open(os.path.join(ROOT,"reports","round47_content_sources.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 为 data_only 条目补「来源性质」说明（这些条目靠指标+别名页，正文为指标解读/常识）
n=0
for t in cat["data_only"]:
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    if "【第47轮来源性质】" in pn: continue
    e["pending_notes"]=(pn+" 【第47轮来源性质】本条内容来源为**数据端点**（世界银行/NOAA 等 JSON）与区域别名页："
      "数据端点支撑「今天的状况」中的数值，别名页不含本条主题正文；正文的文字部分为指标解读与常识性空间差异描述，"
      "不构成需学术文献支撑的具体事实断言（D103 要求分类基于实测，本条已实测确认）。").strip()
    e["last_update"]=TODAY;n+=1
print("已标注 data_only:",n)
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=47
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)