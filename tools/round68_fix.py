# -*- coding: utf-8 -*-
"""第68轮B：处置 5 FAIL + 8 SOFT；修正 book-review 类型；重算层级与缺口。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

def setf(t,fld,text):
    e=T.get(t)
    if not e: return False
    e[fld]=text; e["last_update"]=TODAY; return True
def note(t,text):
    e=T.get(t)
    if not e: return False
    e["pending_notes"]=((e.get("pending_notes") or "")+" "+text).strip(); e["last_update"]=TODAY; return True
def drop(t,sid,why):
    e=T.get(t)
    if not e: return False
    if sid in e["sources"]: e["sources"]=[x for x in e["sources"] if x!=sid]
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第68轮剔除】{why}").strip()
    e["last_update"]=TODAY; return True

# ===== 0 修 book-review 类型（玛雅那条 sources.type 记错）=====
for sid,t in (("openalex-W2910624658","玛雅文明"),("openalex-W1977985637","萨克森王朝"),
              ("openalex-W2325759714","宋代"),("openalex-W617733386","法兰克王国")):
    s=S.get(sid)
    if s and "书评" not in (s.get("type") or ""):
        s["type"]="书评（不作内容来源）"
        s["note"]=(s.get("note") or "")+" 【第68轮类型更正】OpenAlex type=book-review，按 D082 仅登记备查，不得作内容来源。"
print("已修正 4 条 book-review 类型")

# ===== 1 剔除 5 条 FAIL 的来源 =====
n=0
n+=drop("玛雅文明","openalex-W2910624658",
 "该书评（Choice Reviews Online 49-0460）按 D082 不作内容来源；且其所述为**形成期（前古典期）兴起**（Nakbe/El Mirador/Cival），与「古典期衰落」断言时段错配。剔除后本条学术内容源归零。")
n+=drop("大平原","openalex-W2333116877",
 "该文为**加拿大冰碛大平原 96 样地植被顶极群落分类**（1961），仅涉植被侧面，空间亦不及美国大平原主体；与本条农业/野牛/铁路/沙尘暴诸断言无对应（适用范围 case，D128）。")
n+=drop("印加帝国","openalex-W2504408383",
 "该文为**玉米酒（chicha）器物的分布研究**（aríbalos），属仪式性再分配侧面；第50轮已判旁证，但第42轮 strong 标签未撤，本条直接剔除以免冲突残留。")
n+=drop("克里特文明","openalex-W576397603",
 "该文为米诺斯**印章学**专著（类型学/沉积/图像与宗教含义），摘要 725 字符 <800（D112①），且与本条「海上贸易与宫殿再分配」无对应——与第45轮已剔除的《The artistic reception of Minoan Crete》同判据。")
n+=drop("十字军东征","openalex-W561167263",
 "该文为**纪念文集（John Pryor）导言**，摘要 793 字符 <800（D112①）、被引 6，属卷级书目介绍而非实证结论；第34轮曾据此升级 L2，依据不成立。")
n+=drop("十字军东征","openalex-W4249644002",
 "该文覆盖 **1305–1352**（阿维尼翁教廷的布道组织），**落在本条「11世纪末至13世纪末」时段之外**（D108 时期槽否决），且属布道与宣传侧面。")
print("剔除:",n)

# ===== 2 修 8 条 SOFT 措辞 =====
setf("撒哈拉沙漠","influence",
"沙漠既阻隔也连接：它分隔南北，却也通过跨撒哈拉商路把西非黄金与地中海市场联系起来（商路部分为常识性叙述，未挂该文）。"
" 所引 2018 年研究（被引 181）覆盖 **20 世纪（1902–2013）**的季节降水趋势，指出撒哈拉沙漠在此期间**扩张 11%–18%（随季节与时段而异）**，成因与萨赫勒降水带北缘退却、热带带扩张有关；"
"本条「扩张与收缩与降水带移动相关」据此。**该文不涉地貌、矿产与商路**，不得作全条目的第二来源。")
setf("东非大裂谷","influence",
"裂谷湖盆提供水源与渔业，高地降雨与火山土有利于农业；但学界对其在人类演化中的作用仍有讨论（生态与农业部分为常识性叙述）。"
" 所引 2002 年研究（被引 150）给出的是**裂谷发育的运动学框架**——前寒武岩石圈对东非裂谷系的控制、东支抵达坦桑尼亚克拉通约 **12–10 Ma**；"
"该文支撑的是构造机制与这一年代节点，**不涉湖泊链、气候、农业与人类演化**。")
setf("两河流域","influence",
"灌溉农业支撑城市与人口密集，渠网维护需要协作与行政组织（机制性常识表述，未挂专门来源）；"
"土壤盐渍化与水量变化**是否**削弱政权稳定，学界在 1960 年代以后已有修正与争议，本条标为**待核**。"
" 所引 1960 年研究（Helbaek，*Iraq* 22）讨论的是早期作物扩散与农业起源，**摘要未涉及两河灌溉的盐渍化结论**。")
setf("青藏高原","geo",
re.sub(r"所引 1985 年研究[^。]*。","",
 (T.get("青藏高原") or {}).get("geo","")) +
" 所引 1985 年研究是以**运动学模型推算**的隆升史（45 Ma 碰撞以来；中新世早期仍低于 1 千米，中中新世起稳定抬升至现今高度）——可支撑「隆升年代框架（模型）」一句，"
"**不支撑水系源区与亚洲气候影响**；模型推算非实测年代，不得作实测年代的互证。")
setf("爱琴海世界","influence",
"海洋交通降低了远距离交流成本，山地与海湾促成聚落分立与海上贸易并存（地理机制部分为常识性叙述）。"
" 所引 1996 年研究（被引 42）把爱琴海青铜时代经济视为**东地中海世界体系的附属**，并主张重视生产而非仅交换；"
"该文支撑「海上交换网络」与「体系层级」判断，**不支撑「地理条件促成城邦分立」**。关于该体系是否属核心—边缘依附关系，学界有修正（文献指出青铜时代缺少近代意义上的边缘依附）。")
setf("罗马帝国","influence",
"道路与海上运输网络支撑帝国的**行政与军事调度**（御用驿传 cursus publicus、征服与治理中的后勤），并降低人员与物资移动成本。"
" 所引 2012 年《Travel and Geography in the Roman Empire》（被引 293）为**论文集**，编者导言综述的正是运输通信对统治的必要性；"
"**「统一市场」「法律」「城市化」「尼罗河与北非粮食供应」四项不在该摘要内**，市场整合程度与城市化水平待专门研究核验。")
setf("埃塞俄比亚高原","geo",
"高原由火山岩与断崖构成、海拔多在 2000 米以上、为青尼罗河等河流发源地、裂谷纵切——**以上为常识性地理描述，未挂专门来源**。"
" 所引 2000 年研究（被引 115）只覆盖**东北部 Wollo 与 Tigray** 的降水变率（仅三站有 1950 年代以来的较完整记录），"
"作者明言「无长期趋势或变化的证据」；该文**不支撑「降水较周边丰沛」**（无周边对比），亦不涉地质与河源。")
setf("落基山脉","geo",
re.sub(r"本条「落基山脉主要由晚白垩世至早第三纪的造山运动抬升」据此。","",
 (T.get("落基山脉") or {}).get("geo","")) +
" 本条「**南部落基山**主要由晚白垩世至早第三纪的拉拉米造山运动抬升」据此（所引 1975 年研究的对象是 Southern Rocky Mountain province，不覆盖北部落基山；全山脉的隆升序列须另配来源）。")

# ===== 3 补登 side_evidence =====
sep=os.path.join(DATA,"side_evidence.json");sed=json.load(open(sep,encoding="utf-8"))
already={r["entry"]+r["sids"][0] if r["sids"] else r["entry"] for r in sed["side"]}
adds=[
 ("撒哈拉沙漠","openalex-W2794663306","仅覆盖20世纪降水趋势与沙漠扩张，不涉地貌/矿产/商路"),
 ("东非大裂谷","openalex-W2004908009","构造运动学框架，不涉湖泊链/气候/农业/人类演化"),
 ("两河流域","openalex-W1982150356","讨论作物扩散与农业起源，摘要未涉灌溉盐渍化"),
 ("青藏高原","openalex-W1997020239","1985年运动学模型推算隆升史，不涉水系与气候影响"),
 ("爱琴海世界","openalex-W2209715977","世界体系层级分析，不涉地理条件促成城邦分立"),
 ("罗马帝国","openalex-W378444792","论文集编者导言，仅涉运输通信对统治的必要性"),
 ("埃塞俄比亚高原","openalex-W2168645999","仅东北部两省降水变率，不涉地质/河源/防御性"),
 ("落基山脉","openalex-W2087734990","南部落基山前寒武地壳边界，且作者明言无共识"),
]
for t,sid,why in adds:
    if t+sid in already: continue
    sed["side"].append({"entry":t,"kind":"side","sids":[sid],"note":why})
sed["counts"]["side"]=len(sed["side"])
sed["counts"]["dropped"]=len(sed["dropped"])
json.dump(sed,open(sep,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("side_evidence 补登 8 条")

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=68
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")