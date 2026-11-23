# -*- coding: utf-8 -*-
"""第38轮返工：仰韶BP/BC、奇穆结论反向、4处归属越界、悬空引用、巴塔哥尼亚、台账。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== A1 仰韶：BP → BC 换算错 =====
ys=T["仰韶文化"]
ys["influence"]=("所引 2001 年研究以陕西仰韶时期人骨的饮食与健康变化为线索，指出在**距今约5000年（约公元前3000年）**之后出现降温，"
  "若干指标随之变化；作者把这一转折与仰韶晚期至龙山过渡的社会变化相联系。"
  " 这说明农业社会的生计与社会组织对气候波动敏感，但因果关系仍需具体证据（D081）。")
ys["time_or_place"]="约公元前5000–前3000年（仰韶文化；所引研究覆盖距今7000–4000年，即约前5000–前2000年）"
ys["pending_notes"]=((ys.get("pending_notes") or "")+
  " 【第38轮返工·硬错】原稿把摘要的「the fifth millennium **BP**」（距今约5000年≈前3000年）写成「公元前第五千纪」（前5000年），差约2000年，且与条目自身年代矛盾；已改为「距今约5000年（约公元前3000年）」。").strip()

# ===== A2 奇穆：结论与摘要相反 =====
cm=T["奇穆帝国"]
cm["influence"]=("所引 1982 年研究分析的是**奇卡马—莫切跨谷运河（La Cumbre）**：以明渠流设计的计算机分析结合实地测量，"
  "探讨把奇卡马谷的水引至莫切谷的可行性。研究的结论是**该运河在完工前即被放弃、从未向莫切谷输水**——"
  "沿线比降受断层影响，试挖多条渠线仍难以克服。这一案例说明大规模跨谷水利在技术上与政治上都有失败的可能，"
  "不能一概读作「权力集中的成功机制」。")
cm["pending_notes"]=((cm.get("pending_notes") or "")+
  " 【第38轮返工·硬错】原稿①把对象写成「奇卡马谷的水利工程」（实为奇卡马—莫切跨谷运河 La Cumbre）；"
  "②漏掉摘要的关键结论「运河完工前即废弃、从未输水」；③并据此反向推出「灌溉是权力集中机制」。"
  "三点已全部改正——原文是**失败工程**的案例研究，不是成功例证。").strip()

# ===== B3 新法兰西：删「宣传」 =====
nf=T["新法兰西"]
nf["influence"]=("所引 2012 年研究以耶稣会《Relations》为对象，指出这些文本在巴黎编辑后又被送回殖民地供对照与删改，"
  "因此其作为「旅行写作」与「民族志首要资料」的可靠性须重新评估。这提示**《Relations》这一特定文本**的成书过程"
  "影响其证据价值；本条不据此推断所有殖民文献的性质。")
nf["pending_notes"]=((nf.get("pending_notes") or "")+
  " 【第38轮返工】删去「殖民文献本身是宣传工具」——摘要只讨论《Relations》的编辑—回流—复核过程，未作「宣传」判断，"
  "亦不应由个案外推至全部殖民文献（D083④）。").strip()

# ===== B4 的的喀喀湖：删「政治边界」 =====
tt=T["的的喀喀湖"]
tt["influence"]=("所引 2002 年研究以「水中的界线」为题，讨论湖泊作为渔业与芦苇资源、交通通道以及**文化认同载体**的多重角色，"
  "并涉及现代技术、市场压力与文化自主之间的张力。正文不据该研究主张「政治边界」的判断。")
tt["pending_notes"]=((tt.get("pending_notes") or "")+
  " 【第38轮返工】删去「政治边界」——摘要无此内容（原句系把书名双关当作论点）；改为「资源、交通与文化认同的载体」。").strip()

# ===== B5 玛雅：删「社区返还」 =====
my=T["玛雅研究新进展"]
my["influence"]=("所引 2020 年研究讨论 LiDAR 带来的认知突破，同时提出伦理与新殖民主义问题：数据的**长周期存储与管理**、"
  "**科学开放获取与国家保护之间的分歧**（部分国家因盗掘与军事安全不愿完全公开），以及**卫星技术对民族国家物理边界与主权**的挑战。"
  "这说明技术进展与数据治理是同一议题的两面。")
my["pending_notes"]=((my.get("pending_notes") or "")+
  " 【第38轮返工】删除「对当地社区的返还」——摘要框架是国家保护/主权/盗掘，未涉社区返还；已改为摘要实有的三项张力。").strip()

# ===== B6 地图投影：删「学生态度」 =====
mp=T["地图投影"]
mp["influence"]=("所引 2018 年研究对 24 本普通制图学教科书做内容分析，结论是：投影性质各书都讲，但**变形图示方法**与**基准面**的"
  "讲解不一致或很少提及；作者据此提出三项改进建议（坐标系统、读者理解实验、Web Mercator 等技术影响）。"
  "这说明投影在教学中常被当作技术细节处理，而其表达后果的讲解并不统一。")
mp["pending_notes"]=((mp.get("pending_notes") or "")+
  " 【第38轮返工】删除「学生常把投影视为技术细节」（摘要未做学生实证）；改为对 24 本教科书内容分析的结论转述。").strip()

# ===== C7 欧洲冰期地貌：限定 =====
eu=T["欧洲冰期地貌"]
eu["influence"]=("所引 2004 年研究以 150 年积累的已发表文献与 BGS 测绘记录为基础，编成「Glacial Map」（1:625,000）与 GIS 数据库，"
  "**覆盖末次（Devensian）不列颠冰盖**，逾 2 万个地貌要素按主题分层、可回溯到原始来源；作者自陈主要限制是数据一致性与可靠性。"
  "这说明「地貌知识」也依赖数据组织方式。")
eu["pending_notes"]=((eu.get("pending_notes") or "")+
  " 【第38轮返工】补限定「末次（Devensian）不列颠冰盖、1:625,000、逾2万要素」；「野外观测」改为「已发表文献与 BGS 测绘记录」。").strip()

# ===== C8 人文地理学：删悬空引用 =====
hg=T["人文地理学"]
hg["influence"]=re.sub(r"（与「争议边界处理原则」中的[^）]*）","",hg.get("influence") or "")
hg["pending_notes"]=((hg.get("pending_notes") or "")+
  " 【第38轮返工】删除末句对「boundary work」的悬空引用——本条正文无该概念（且该概念属管理学同名陷阱，已在本轮剔除）。").strip()

# ===== C9 巴塔哥尼亚：主题与内容对齐 =====
pt=T["巴塔哥尼亚"]
pt["influence"]=("所引 2020 年研究以古基因组揭示南巴塔哥尼亚的**人群历史**，显示流动与替代过程比单一「沿海扩张」模型更复杂。"
  "（本条主题为区域地理，人口史仅作为该区域研究现状的一例，不代表对气候或地貌的解释。）")
pt["pending_notes"]=((pt.get("pending_notes") or "")+
  " 【第38轮返工】本条 theme 为「气候」，所引文献为古基因组人群史——已在正文显式限定为「区域研究现状的一例」，"
  "不作气候或地貌的解释依据。").strip()

# ===== C10 赫梯：拆归属 =====
ht=T["赫梯王国"]
ht["influence"]=("所引 2022 年专著讨论其国家形态：档案文书显示王权与**条约体系**并重，并涉及权力的委任安排。"
  "（与埃及的卡叠什对峙是古代近东外交的著名事件，属本条补充的史实，不挂该专著。）")

# ===== D14 source note 修正 =====
for s in sd["sources"]:
    if s["id"]=="openalex-W4297537764":
        s["note"]=re.sub(r"HTTP 200，368 字节。", "HTTP 200，36,869 字节。", s.get("note") or "")
        if "摘要节录" not in (s.get("note") or ""):
            s["note"]=(s.get("note") or "")+" 摘要字段为空，故无节录。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=38;cov["round_processed"]=16
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成：硬错2 + 越界4 + 限定3 + 台账")