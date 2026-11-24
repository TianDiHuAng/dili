# -*- coding: utf-8 -*-
"""第67轮B：落实语义抽检的 11 条修改（1 FAIL + 10 SOFT）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

def setf(t,fld,text):
    e=T.get(t)
    if not e: return False
    e[fld]=text; e["last_update"]=TODAY; return True
def note(t,text):
    e=T.get(t)
    if not e: return False
    e["pending_notes"]=((e.get("pending_notes") or "")+" "+text).strip(); e["last_update"]=TODAY; return True

n=0
# ===== #12 丝绸之路（FAIL：降级）=====
if setf("丝绸之路","influence",
"陆路商队依赖绿洲补给与季节通行条件，海路则依赖季风与港口；商品与观念的流动沿这些通道发生，但「丝绸之路」作为一个整体网络，"
"学界更倾向于把它看作**多段、多主体、非连续**的交换体系，而非单一商道。"
" 所引 2008 年研究是**拉达克（Ladakh）商埠的民族史个案**：该地曾为中亚—南亚商路要冲，20 世纪中叶国界划定后与中亚贸易中断、当地社会随之改变——"
"**只能支撑「南亚—中亚段商路在近代国家边界形成后衰退」这一**段**级判断，不作整条「丝绸之路」的第二独立来源**。"):
    n+=1
note("丝绸之路"," 【第67轮语义抽检·FAIL降级】W4249333639 为拉达克单点商埠个案（且断代在 20 世纪边界划定），W1520501027 为大英图书馆特展图录（Aurel Stein 藏品），"
 "两者均不覆盖「陆海网络整体」与「绿洲补给机制」；第42轮把它们记为「年代/机制断言的第二独立来源」属模板化登记，已改为段级线索。")

# ===== #1 苏美尔城邦（题目级错位）=====
note("苏美尔城邦"," 【第67轮语义抽检·题目级错位】openalex-W150669647 的记录题名是章节《Sumerian Agriculture and Land Management》，"
 "而 OpenAlex 返回的摘要是**整卷《The Sumerian World》导论**（南部美索不达米亚考古/历史/艺术、与邻邦关系、约前3000–2000年），"
 "**不含「城邦制度」「灌溉—协作」机制**。仅可作对象与大致年代的旁证，不作机制断言的第二来源。")
su=T.get("苏美尔城邦")
if su and "本段为机制性常识表述" not in (su.get("influence") or ""):
    su["influence"]=(su.get("influence") or "")+" （本段机制表述为常识性概括，未挂专门来源。）"
    su["last_update"]=TODAY; n+=1

# ===== #2 黄河流域（删「地上河」）=====
if setf("黄河流域","geo",
(yellow:=T.get("黄河流域")).get("geo","").split("所引 2004 年研究")[0].strip()+
" 所引 2004 年研究以水深平均二维模型模拟**花园口—夹河滩约 100 公里河段**的洪水演进与泥沙输运，可佐证该河段**含沙量高、河床冲淤与游荡性显著**；"
"**该文自陈含沙量 >200 kg/m³ 情形的适用性尚待研究**，故不支撑「全流域多沙」与「淤积抬升形成地上河」的结论。"
" 流域的气候、农业与王朝历史为本条常识性叙述，未挂该文。"):
    n+=1

# ===== #3 蒂亚瓦纳科（删冻害、改因果）=====
tv=T.get("蒂亚瓦纳科")
if tv:
    inf=tv.get("influence") or ""
    inf=inf.replace("冻害规避技术","抬升田的排水与保温效应（摘要未涉冻害，待专门来源核验）")
    inf=re.sub(r"这一技术—组织组合是国家形成的重要条件","该文讨论的是**国家内部**的组织形态，并未论断这些技术是国家形成的原因",inf)
    tv["influence"]=inf
    tv["time_or_place"]="约公元400–1000年（学界有不同表述）"
    tv["last_update"]=TODAY; n+=1
    note("蒂亚瓦纳科"," 【第67轮语义抽检】删去「冻害规避技术」（摘要无）；把「技术—组织是国家形成的条件」（因果反转）改为「该文讨论国家内部的组织形态」；年代按摘要 ca. AD 400–1000 调整为「约400–1000」并注明学界有异说。geo 中「海拔约3800米」加待核标记。")

# ===== #4 澳大利亚内陆干旱气候（删「决定」）=====
if setf("澳大利亚内陆干旱气候","influence",
"（本段两组地理—农业断言为常识性表述，未引专门来源。）"
" 所引 2021 年研究以 **2019/20 年「黑色夏季」** 为对象，可支撑「**极端干旱年份（2019 年为有记录以来最热最干年）与气候变率叠加，放大澳大利亚东南部森林火险**」；"
"**该文区域为东南澳、主题为火险，不支持以内陆干旱区为主语的表述**。"):
    n+=1

# ===== #5 马丘比丘（删「适应能力」）=====
if setf("马丘比丘","influence",
"所引专论将该遗址定位为**云雾林中的王室庄园**——印加皇帝与宾客避离都城压力之所；其在印加政治体系中的具体功能（王室庄园、宗教中心等）仍有不同解释。"
" 「遗址反映国家对山地地形的适应能力」一类引申**不在该摘要内**。 梯田与排水系统为常识性工程描述，摘要未涉，待专门来源核验。"):
    n+=1

# ===== #6 维京时代（删「劫掠」）=====
if setf("维京时代","influence",
"所引 2020 年研究讨论**9–10 世纪迪拉姆银币向波罗的海的流入（哥特兰窖藏最集中）以及奴隶贸易驱动的跨大陆交换网络**；"
"本条「维京人的贸易网络连接北欧与欧亚（中亚铸币—罗斯—不列颠）」据此。"
" **该摘要不涉「劫掠」「航海技术」与「拜占庭」**——这些为常识性表述，未挂该文。"):
    n+=1

# ===== #10 安纳托利亚（中→早全新世）=====
an=T.get("安纳托利亚")
if an and "中全新世" in (an.get("influence") or ""):
    an["influence"]=(an.get("influence") or "").replace("中全新世","早全新世")
    an["last_update"]=TODAY; n+=1
    note("安纳托利亚"," 【第67轮语义抽检】「中全新世」改为「早全新世」——约前 9 千纪中叶（≈8500 cal BC）属早全新世，中全新世约在前 5–2 千纪；括号内年份正确，仅地层词错。")

# ===== #11 古埃及古王国（改登记语）=====
note("古埃及古王国"," 【第67轮语义抽检】openalex-W2021390023 仅涉**古王国金字塔选址**（经济/地貌/社会政治/宗教因素、孟菲斯为金字塔区中心地），"
 "**摘要不含任何年代**；第42轮「可作年代/机制断言的第二独立来源」不成立，改记为「孟菲斯中心性」的旁证。")

# ===== #13 莫斯科公国（改归因）=====
if setf("莫斯科公国","influence",
"所引 2017 年研究讨论莫斯科为何未参与早期印刷革命，作者的回答是「**没有参与**」：主因**不是技术落后，而是缺乏对印刷品的公共需求**；"
"俄国的信息结构先围绕**教会**、后围绕**国家**组织，印刷长期主要服务于此二者。"):
    n+=1

# ===== #14 马格里布（加常识标注）=====
mg=T.get("马格里布")
if mg:
    inf=mg.get("influence") or ""
    if "常识性地理表述" not in inf:
        inf=inf.replace("政治整合受地形与距离制约。","政治整合受地形与距离制约。（**以上为常识性地理表述，未引专门来源**。）")
    inf=re.sub(r"才与「中东」「非洲」这两个同样属殖民构造的实体区分开来",
               "被建构为独立于「非洲」与「中东」（两者同为殖民构造）的单一区域类别，该建构延续至后殖民时代", inf)
    mg["influence"]=inf; mg["last_update"]=TODAY; n+=1

# ===== #15 中南半岛（改「景观」）=====
if setf("中南半岛","influence",
"所引 2007 年研究（被引397）对东南亚多条河流沉积物分析后指出：**在气候条件相近的情况下，流域的化学风化程度差异显著，构造与岩性起主导作用**。"
" 这说明**同一气候带内各流域的风化强度并不一致**——该文测的是流域风化强度，**不涉及「景观」整体**（原表述「同一气候带内景观一致不成立」为术语溢出）。"):
    n+=1

save_docs(docs)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=67
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("修改条目数:",n)