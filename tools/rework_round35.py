# -*- coding: utf-8 -*-
"""第35轮返工：修 4 FAIL + 2 P1 + P2，并诚实处理对象/时期错配。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== P0-1 北美原住民：文献对象＝巴西亚马孙 → 撤源，退回 L1 =====
n=T["北美原住民"]
n["sources"]=[s for s in n["sources"] if not s.startswith("openalex-W2020901419")]
n["level"]="L1"
n["status"]="L1·来源撤回(第35轮)"
n["pending_notes"]=("【第35轮返工·退回 L1】原第二来源 OpenAlex W2020901419（1996，《Paleoindian Cave Dwellers in the Amazon: The Peopling of the Americas》）"
  "的研究对象是**巴西亚马孙的 Monte Alegre 洞穴**，摘要自述其文化「distinct from North American cultures」，与本条「北美原住民」不同对象，已撤出。"
  " 原 geo 段「白令陆桥与沿海走廊两种假说」亦不在该文摘要内，属无源断言，已删。"
  " 本条现无学术第二来源，**退回 L1**；需补北美考古/民族史专题来源方可再升。其余来源为 UNSD/UNSDG 别名页与机构首页，无正文。")
n["geo"]="北美原住民的分布跨越北极、亚寒带、温带与干旱区，聚落形态随生态带变化显著。具体迁徙路线与年代属考古学议题，待专门来源核验。"
n["influence"]="本条不展开迁徙机制的具体断言；相关假说（白令陆桥、沿海走廊等）待专门考古与遗传学研究核验。"
n["last_update"]=TODAY

# ===== P0-2 朝鲜半岛：geo 剥离背书 =====
k=T["朝鲜半岛"]
k["geo"]=("半岛三面环海、北接大陆，地形以山地与丘陵为主，东部山脉陡降入海；季风气候带来夏季集中降水，冬季干冷。"
  "（本段为常识性地理描述，**未挂学术来源**；所引 2000 年研究仅涉植被史，不支撑地形与气候表述。）")
k["influence"]=("所引 2000 年研究以大型化石与孢粉重建半岛植被史（资料覆盖二叠纪至今）：现存针叶与阔叶类群自白垩纪以来"
  "连续出现，说明该区域未发生灾难性环境突变、长期气候具有连续性；期间仍有波动，更新世后出现喜冷针叶类群。"
  " 该研究**不涉及**地形、季风或气候型划分。")
k["pending_notes"]=((k.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】所引文献（Vegetational history of the Korean Peninsula）**只做植被史**，不含地形/季风表述；geo 段已剥离其背书并标为常识性描述，待补半岛地形与气候专题来源。").strip()
k["last_update"]=TODAY

# ===== P0-3 大津巴布韦：批评对象与臆造细节 =====
z=T["大津巴布韦"]
z["influence"]=("所引 1998 年研究批评的是**Huffman 式的认知考古重建**（认为其依赖「被误读的文献、可疑的口述传统与不当类比」），"
  "并主张以**绍纳（Shona）历史与人类学材料**重建该政体的政治过程，同时承认其模型「不企图解释每一处细节」。"
  " 该文讨论的是考古解释的方法问题，不是「殖民时代想象性历史」的一般批评。")
z["pending_notes"]=((z.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】原 influence 把批评对象写成「殖民时代对遗址的想象性历史」，实为批评 Huffman 的认知考古重建；"
  "并删除了「鸟形石雕、干砌技术」的错误归因（该文摘要未提）。").strip()
z["last_update"]=TODAY

# ===== P0-4 古巴比伦：时期错位 + 机制句臆造 =====
b=T["古巴比伦"]
b["influence"]=("所引 2017 年研究覆盖的是**晚期巴比伦（阿契美尼德末期与塞琉古时期，约前4–前1世纪）**，"
  "以档案楔形文书与天文日志中的价格数据重建经济：讨论帝国政治对价格的**外生冲击**、货币流通量，并做回归分析。"
  " 该文**不涉及**古巴比伦王国时期（约前2千纪）的神庙、土地与税收制度，两段时期的制度不能互推。")
b["pending_notes"]=((b.get("pending_notes") or "").replace("该文献与本条同一对象；","")+
  " 【第35轮返工】所引文献对象为**塞琉古时期巴比伦**，与条目「古巴比伦王国」同地区而不同时期；"
  "原 influence 的「神庙、王室与私人之间的土地与税收关系」不在摘要内，属臆造机制，已改为摘要实有内容（档案文书、价格序列、帝国冲击、货币量）。"
  " 古巴比伦王国时期的经济制度待专门亚述学来源核验。").strip()
b["last_update"]=TODAY

# ===== P1-5 吠陀时代：神名错字 + 补第二篇 =====
v=T["吠陀时代"]
v["influence"]=v["influence"].replace("印伽","因陀罗（Indra）")
v["pending_notes"]=((v.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】① 神名「印伽」为错字，摘要所列神祇为 Indra / Varuna / Mitra / Surya / Agni，已改为「因陀罗（Indra）」。"
  " ② 该文献刊于教育学院学报、被引 1，作为重要条目的唯一内容来源证据强度偏弱，需补第二篇同主题文献互证。"
  " ③ geo 段的「西北部与旁遮普、季风梯度」为常识性地理描述，不挂该文献。").strip()
v["last_update"]=TODAY

# ===== P1-6 匈奴：生态/继承句拆出 =====
h=T["匈奴"]
h["influence"]=("所引 2014 年研究依据中国史书与考古材料，指出匈奴的「王」与区域精英构成**分层联盟**，"
  "地方领袖的竞争导致草原精英的分裂，而非集权官僚制。"
  " （草原生态对政治组织的基础作用属本条常识性表述，不挂该文献。）")
h["pending_notes"]=((h.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】原句把「草原生态提供基础」与「继承安排」写在「所引 2014 年研究强调」之下——该文为纯政治史，摘要无生态或继承内容，已拆出并标为常识表述。").strip()
h["last_update"]=TODAY

# ===== P1-7 吴哥 =====
a=T["吴哥"]
a["influence"]=("所引 2010 年研究指出：14–15 世纪长期干旱与强季风事件交替，**与其他因素共同**促成吴哥的衰落；"
  "高强度季风年份损害了其水利控制设施。该研究把气候定位为促成因素之一（其他因素未具名），不是单一原因。")
a["time_or_place"]="鼎盛期约 9–15 世纪；本条所引研究覆盖的衰落期为 14–15 世纪（9 世纪起点待专门史学来源核验）"
a["pending_notes"]=((a.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】①「政治与战争因素同样关键」改为「其他因素（摘要未具名）」；② 9 世纪起点不在所引摘要覆盖范围内，已标待核。").strip()
a["last_update"]=TODAY

# ===== P2-8 马丘比丘 =====
m=T["马丘比丘"]
m["geo"]=("建于安第斯山脊，两侧为陡降的河谷；梯田与排水系统是维持建筑稳定与农业的关键工程措施。"
  "（具体海拔数值待专门来源核验，本条不写具体高度。）")
m["pending_notes"]=((m.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】删除「海拔约2400米」的具体数值——所引文献摘要未给该数字，已标待核。").strip()
m["last_update"]=TODAY

# ===== P2-9 斯堪的纳维亚 =====
s=T["斯堪的纳维亚"]
s["influence"]=("所引 2008 年综述指出，北欧在约 250–300 万年间经历**多次冰期与间冰期**：萨勒冰期（约 14 万年前）之后，"
  "末次间冰期（Eemian）早期格陵兰与波罗的海地区海面偏高；**Eemian 期间**气温比今天高约 5 °C，格陵兰冰盖缩减至约为现今的一半。"
  " 这为当前冰盖变化的量级提供了参照。")
s["pending_notes"]=((s.get("pending_notes") or "").replace("正文的地理与机制段落据其撰写；","")+
  " 【第35轮返工】+5 °C 改为归于「Eemian 期间」而非「早期」；geo 的峡湾/冰碛为常识性描述，不挂该文献。").strip()
s["last_update"]=TODAY

# ===== P2-10 全库模板句改写 =====
cnt=0
for e in T.values():
    pn=e.get("pending_notes") or ""
    if "正文的地理与机制段落据其撰写" in pn:
        pn=pn.replace("正文的地理与机制段落据其撰写，未外推。","机制/影响段据其撰写，geo 为常识性描述（未挂学术来源）。")
        pn=pn.replace("正文的地理与机制段落据其撰写","机制/影响段据其撰写，geo 为常识性描述（未挂学术来源）")
        e["pending_notes"]=pn;cnt+=1
    pn=e.get("pending_notes") or ""
    if " 该文献主题与本条同一对象" in pn:
        e["pending_notes"]=pn.replace(" 该文献主题与本条同一对象"," 该文献与本条对象一致（时期/范围见说明）")

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("返工完成；模板句改写",cnt)
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))