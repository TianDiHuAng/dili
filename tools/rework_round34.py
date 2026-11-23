# -*- coding: utf-8 -*-
"""第34轮返工：修 3 FAIL、8 处误匹配措辞、模板化引用、截断标题、wikidata 状态。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
SRC={s["id"]:s for s in sd["sources"]}

# ===== 1) 三个 FAIL =====
# 威尼斯
v=T.get("威尼斯")
if v:
    v["time_or_place"]="中世纪至近代；本条所引 QJE 2014 研究覆盖约公元 800–1600 年。共和国终结于 1797 年（待专门史学来源核验）"
    v["influence"]=("所引 QJE 2014 研究的论证方向是：长程贸易扩大 → 商人家族财富与政治参与变化 → 1297 年后转向寡头化的制度安排。"
      "**即制度由贸易扩张塑造，而非「地理约束直接塑造制度」**；潟湖环境提供航运条件，但因果链需要制度中介。")
    v["geo"]="建在潟湖岛屿上，浅水与沙洲提供天然防护；缺乏淡水与耕地，这一环境约束迫使居民依赖海运与贸易。（本段为常识性地理描述，未引专门来源）"
    v["pending_notes"]=((v.get("pending_notes") or "")+
      " 【第34轮返工】① 1797 年不在所引文献摘要内，已改「待专门史学来源核验」；② influence 因果方向纠正为「贸易扩张→制度变迁」，原文并非「地理约束塑造制度」；③ geo 标注为常识性描述。").strip()
    v["last_update"]=TODAY

# 十三殖民地
s13=T.get("十三殖民地")
if s13:
    bad=[s for s in s13["sources"] if s.startswith("openalex-W2491281325")]
    s13["sources"]=[s for s in s13["sources"] if not s.startswith("openalex-W2491281325")]
    s13["time_or_place"]="17世纪初至1783年（巴黎条约承认独立）；本条原引文献仅覆盖**1763年断面**，1783 年待专门来源核验"
    s13["overview"]=("十三殖民地：北美东岸自新英格兰到乔治亚的十三个英属殖民地，1763年是常被用作断面的时点。"
      "本条以地理描述为主；政治与制度细节待专门史学来源核验。")
    s13["pending_notes"]=((s13.get("pending_notes") or "")+
      " 【第34轮返工】原第二来源（OpenAlex W2491281325，《The American Revolution》全书简介）摘要是独立战争通史，**不含十三殖民地地理或制度内容**，属「只沾边当全面来源」，已撤出。"
      " 1783 年不在任何现存来源中，已标待核。本条关键年代现无学术第二来源支撑，证据强度下调，需补专门来源方可确认 L2。").strip()
    s13["status"]="L2完成(第34轮)-来源撤出待补"
    s13["last_update"]=TODAY

# 松岛冰川
pig=T.get("松岛冰川退缩")
if pig:
    pig["influence"]=("所引 2002 年《Annals of Glaciology》研究显示：1990 年代该冰川与思韦茨冰川加速、8 年内冰流速度增加约 18±2%，"
      "并明确指出当时的观测**尚不足以确定原因**。海洋暖水入侵作为机制属于后续研究的方向，本条不将其写作已由该文献证实的结论。")
    pig["pending_notes"]=((pig.get("pending_notes") or "")+
      " 【第34轮返工】① 原 influence 把「暖深层海水入侵」写成由卫星观测支持的机制，而所引文献摘要明说「were not sufficient to determine the cause」，属无源归因，已改。"
      " ② 来源 nasa-pine-island 复测已无可剥离正文（仅导航样板），其早年记录的正文与命中数不可复现，已在该源 note 标注。").strip()
    for s in sd["sources"]:
        if s["id"]=="nasa-pine-island":
            s["note"]=(s.get("note") or "")+" 【第34轮复测】剥离后正文仅约 9450 字符且为导航样板，warm/melt/Circumpolar 命中 0；第23轮记录的「7719 字符/命中 25」当前不可复现。"
            s["link_ok"]=False; s["verified"]=False
    pig["last_update"]=TODAY

# ===== 2) 8 处残留误匹配：改措辞 / 降级说明 =====
MISMATCH={
"阿拉伯半岛":"所引文献为单峰驼群体遗传结构研究，**仅涉该半岛的骆驼种群**，不含年代或面积信息；本条面积数值依赖的 Wikidata 端点当前不可达，故该数值标为待核。",
"马格里布":"所引文献为西北非人群线粒体 DNA 研究，仅涉人群遗传连续性，**不支撑面积或地理概况**；本条面积数值依赖的 Wikidata 端点当前不可达，标为待核。",
"伊比利亚半岛":"所引文献为野生食用植物民族植物学研究，仅涉传统植物利用知识，**不支撑半岛整体地理**；正文已限域表述，geo 段属常识性描述。",
"阿兹特克":"所引文献研究的是 **Tlaxcallan（特拉斯卡拉）**——阿兹特克的敌对城邦，不能代表阿兹特克本身；本条年代依赖 Wikidata（当前不可达），标为待核。",
"澳大利亚内陆干旱气候":"所引文献讨论干旱区生态避难所与保护，**不支撑干旱气候的整体特征**；正文已限域为生态适应与避难所格局。",
"长江流域":"所引文献为长江氮磷污染来源解析，**不支撑河长数值**；河长 6300 千米仅来自 Wikidata（当前不可达），标为待核。",
"库什与努比亚":"所引文献为 Educational Media Reviews Online 的**影像资料评介**，非研究论文，不能支撑年代；本条年代依赖 Wikidata（当前不可达），标为待核。",
"尼罗河三角洲":"所引文献为三角洲地表水重金属浓度研究，仅涉水质空间分布；正文已加限域句，未外推为整体概况。",
}
for t,why in MISMATCH.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    pn=pn.replace("该文献主题属本条领域，用于支撑地理与制度表述。","")
    pn=pn.replace("文献主题属本条领域，支撑地理与机制表述。","")
    pn=pn.replace("文献主题属本条领域，用于支撑地理与机制表述。","")
    e["pending_notes"]=(pn+
      f" 【第34轮返工·引用范围澄清】{why}").strip()
    e["last_update"]=TODAY

# ===== 3) 模板化引用清理：去掉"制度表述"套话 =====
for e in T.values():
    pn=e.get("pending_notes") or ""
    for pat in ["本条以学术文献与地理描述为主；具体年代与制度细节标注待核。",
                " 本条以学术文献与地理描述为主；具体年代与制度细节标注待核。"]:
        pn=pn.replace(pat,"")
    pn=re.sub(r"该文献主题属本条领域，[^；。]*。","",pn)
    pn=re.sub(r"文献主题属本条领域，[^；。]*。","",pn)
    e["pending_notes"]=re.sub(r"\s{2,}"," ",pn).strip()

# overview 去模板
for e in T.values():
    ov=e.get("overview") or ""
    if "本条以学术文献与地理描述为主" in ov:
        e["overview"]=ov.replace(" 本条以学术文献与地理描述为主；具体年代与制度细节标注待核。","").replace("本条以学术文献与地理描述为主；具体年代与制度细节标注待核。","").strip()

# ===== 4) 60 字符截断标题复原 =====
def full_title(sid):
    oa=sid.split("openalex-")[-1]
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",
          f"https://api.openalex.org/works/{oa}?select=title,type,publication_year,doi"],capture_output=True,timeout=30)
        d=json.loads(p.stdout.decode("utf-8","ignore"))
        return d.get("title"), d.get("type")
    except Exception: return None,None
fixed=0
for e in T.values():
    pn=e.get("pending_notes") or ""
    for sid in re.findall(r"openalex-(W\d+)",pn):
        full,typ=full_title("openalex-"+sid)
        if not full: continue
        # 替换 pending 中被截断的标题
        short=re.search(r"「([^」]{20,60})」",pn)
        if short and len(full)>len(short.group(1)) and full.startswith(short.group(1)[:40]):
            pn=pn.replace(short.group(1),full)
            e["pending_notes"]=pn;fixed+=1
            break

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("三个FAIL修复；误匹配澄清",len(MISMATCH),"；标题复原",fixed)