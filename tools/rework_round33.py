# -*- coding: utf-8 -*-
"""第33轮返工：恢复审计轨迹、补口径句、修精度、更正单源理由、来源留痕、today 处理。"""
import json,os,re,subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

# 1) 从 git 恢复第33轮前的 pending_notes
OLD={}
for u in UNITS:
    try:
        out=subprocess.run(["git","show",f"01a99f0:data/{u}.json"],cwd=ROOT,capture_output=True,timeout=60).stdout.decode("utf-8","ignore")
        d=json.loads(out)
        for e in d["entries"]: OLD[e["title"]]=e.get("pending_notes") or ""
    except Exception: pass

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 2) 逐条口径 / 精度 / 引文 / today
DETAIL={
"古埃及新王国":dict(
 span="前1550年–前1070年",
 caliper="**口径需说明**：同一 Wikidata 实体的英文描述写「period from **1570 to 1069 BC**」，而其 P580/P582 属性值为 1550/1070 BC；两者相差约 20 年，属年代划分不同版本。本条取属性值（1550–1070），并注明描述值以供比对。",
 src_desc="period from 1570 to 1069 BC in Egypt"),
"库什与努比亚":dict(
 span="前1070年–350年",
 caliper="**口径需说明**：实体英文描述为「c. 1070 BCE – c. CE 350」，P571 属性值为 2180 BC。2,180 与 1070 相差逾千年，很可能指不同阶段的库什政体（早期与纳帕塔/麦罗埃期）。本条**取描述值 1070–350**，并声明属性值 2180 属另一口径。",
 src_desc="c. 1070 BCE – c. CE 350 / kingdom in Nubia (modern-day Sudan), northeast Africa"),
"加纳帝国":dict(
 span="约100年–约12世纪",
 caliper="**口径需说明**：实体描述为「…(c. 200–c. 1200s)」，P571=100（精度=年）、P576=1200（**精度=世纪**）。描述起点 c.200 与属性 100 不一致；终点因 P576 为世纪精度，只能写「约12世纪」。本条并列两种口径。",
 src_desc="West African empire based in modern-day Mauritania and Mali (c. 200–c. 1200s)"),
"桑海帝国":dict(
 span="1464年–1591年3月12日",
 caliper="**精度说明**：P571=1464（精度=年）、P576=1591-03-12（**精度=日**）。故终点可精确到日，起点仅到年。",
 src_desc="former state located in western Africa"),
"笈多王朝":dict(
 span="320年–550年",
 caliper="**口径需说明**：实体描述为「ancient Indian empire (c. 3rd century CE–575 CE)」，P571=320、P576=550。描述以世纪表述且终年作 575，与属性 320/550 不一致。本条取属性值并注明。",
 src_desc="ancient Indian empire (c. 3rd century CE–575 CE)"),
"商代":dict(span="前1600年–前1046年",
 caliper="属性与描述一致（1600–1046 BC）。",
 src_desc="the first ancient Chinese dynasty to leave historical records (1600-1046 BC)"),
"周代":dict(span="前1046年–前256年",
 caliper="P571 存在多个值（-1046 preferred、-1027、-1100 精度=世纪）；本条取 preferred rank 的 1046，与描述「c. 1046 to 256 BC」一致。",
 src_desc="dynasty of Ancient Chinese kings lasting from c. 1046 to 256 BC"),
"秦代":dict(span="前221年–前206年",
 caliper="属性与描述一致（221–206 BC）。**另有口径差异**：秦亡常系于前207年（见本书「汉代」条）；Wikidata 记 P576=206 BC。两说并存，本条取属性值并注明。",
 src_desc="dynasty that ruled in China from 221 to 206 BC"),
"元代":dict(span="1271年–1368年",
 caliper="属性与描述一致（1271–1368）。",
 src_desc="Mongol-led imperial dynasty of China (1271–1368)"),
"罗马阿非利加":dict(span="前146年–439年",
 caliper="属性 P571=-146、P576=+439；描述未给年代（仅述及今突尼斯/阿尔及利亚/利比亚沿海）。",
 src_desc="Roman province on the northern African coast"),
}
SINGLE_REASON=(" 【单源待互证】本条关键年代/量值目前仅有 Wikidata 一处**内容性**结构化来源。"
 "可达性实况（第33轮复测）：Britannica 403、Wikipedia 无响应；**DBpedia HTTP 可达（200，资源页 136–217 KB）**，"
 "但其英文 abstract 字段为空、内容派生自 Wikipedia，不构成独立内容来源。"
 "UNESCO Culture 首页与 UNSD M49 为区域/机构框架页，亦不构成第二独立印证。需补学术或专题来源后转为双源。")

# 重写第33轮的 10 条政权条目
for t,d in DETAIL.items():
    e=T.get(t)
    if not e: continue
    base=OLD.get(t,"")
    span=d["span"]
    e["time_or_place"]=f"{span}（Wikidata 属性值；口径差异见正文）"
    e["polities"]=(f"据 Wikidata 记录，{span}。{d['caliper']}"
      f" 具体统治者序列、年号与制度细节待专门史学来源逐条核验。")
    e["pending_notes"]=(base+
      f" 【第33轮升级】年代（{span}）来自 Wikidata {e['sources'][0]} 的属性值；引文照录实体描述：「{d['src_desc']}」。"
      + SINGLE_REASON).strip()

# 3) 来源 note：引文照录 + 标题可辨
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
TITLE_FIX={"wikidata-q181238":"Wikidata Q181238 — Africa (Roman province)",
 "wikidata-q28227":"Wikidata Q28227 — Maghreb","wikidata-q31945":"Wikidata Q31945 — Arabian Peninsula",
 "wikidata-q319288":"Wikidata Q319288 — Ethiopian Highlands"}
for s in sd["sources"]:
    if s["id"] in TITLE_FIX:
        s["title"]=TITLE_FIX[s["id"]];s["page_title"]=TITLE_FIX[s["id"]]
    if s["id"].startswith("wikidata-"):
        s["note"]=(s["note"].replace("Britannica/Wikipedia/DBpedia 在本环境均不可达","") or "")
        if "DBpedia" not in (s.get("note") or ""):
            s["note"]=(s.get("note") or "")+" 第33轮复测：DBpedia 资源页 HTTP 200 可达，但 abstract 为空且派生自 Wikipedia，不作独立内容来源。"
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 4) 来源替换留痕 + today 处理（13 条）
for t in ("古埃及新王国","库什与努比亚","罗马阿非利加","加纳帝国","桑海帝国","笈多王朝","商代","周代","秦代","元代",
          "马格里布","阿拉伯半岛","埃塞俄比亚高原"):
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第33轮来源留痕】升级时 sources 收敛为「Wikidata + 机构框架页」两条；"
      "原别名页（britannica-regions/wikipedia-regions）及部分机构页（s038 NASA EO、s075 AAG、ap-human-geo）随之移除——"
      "因其对本报关键年代/量值不构成独立印证。埃塞俄比亚高原另注：4,550 m 为实体自身 P2044，其 P610 最高点 Ras Dashen 为 4,533 m。").strip()
    if not e.get("today") or "本条为历史条目" in (e.get("today") or "") or "本条以地理" in (e.get("today") or ""):
        e["today"]="（本条的当代指标不在本页展开。）"
        e["pending_notes"]+= " 【第33轮】today 为占位而非实测数据，已显式声明。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 5) 清理探测残留
gp=os.path.join(ROOT,"reports","round33_wikidata_geo.json")
gj=json.load(open(gp,encoding="utf-8"))
if "黎凡特" in gj:
    gj["黎凡特"]={"qid":"Q15761348","desc":"academic journal","vals":{},"error":"错命中：实体为学术期刊，已标注不用于条目"}
    json.dump(gj,open(gp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("返工完成：口径/精度/引文/单源理由/留痕/today/残留")