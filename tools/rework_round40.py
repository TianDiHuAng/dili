# -*- coding: utf-8 -*-
"""第40轮返工：按摘要结论重写 5 条 FAIL + 4 条微调 + 未译词 + 台账。"""
import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== 1 城市热岛：按摘要结论重写 =====
uh=T["城市热岛"]
uh["influence"]=("所引 2005 年研究分析热岛强度（UHI）随**纬度**的变化：UHI 从低纬向高纬增强；"
  "但纬度只能解释约 **6%** 的方差，说明其他因子占主导。作者认为显著依赖主要来自**人为热排放与辐射平衡**的差异，"
  "而非单一的气候带位置。本条不据此讨论城市规模或形态的作用。")
uh["pending_notes"]=((uh.get("pending_notes") or "")+
  " 【第40轮返工·硬错】原稿写「分析热岛强度对城市人口规模的依赖、强度并非随规模线性增长、受形态调节」——"
  "所引摘要的主结论是**纬度梯度（仅解释约6%方差）与人为热/辐射平衡**，全无「城市规模非线性」「形态调节」；"
  "已按摘要结论重写（原写法属把个人推断挂到文献名下）。").strip()
uh["last_update"]=TODAY

# ===== 2 生物多样性分布：与结论相反 + 个案当通例 =====
bd=T["生物多样性分布"]
bd["influence"]=("所引 2021 年研究**以墨西哥的哺乳动物为例**，评估系统发育多样性（PD）的空间格局：东南部 PD 最高；"
  "**现有保护区网络已较好覆盖了系统发育树的广度**；保护区内外的 beta 多样性组成**十分相近**；"
  "保护区按近北极、新热带与墨西哥过渡带三类生物地理区聚类。"
  " 因此该研究并未主张「优先区划定会因指标选择而改变」，而是在既有网络基础上讨论 PD 的补充代表性。")
bd["pending_notes"]=((bd.get("pending_notes") or "")+
  " 【第40轮返工·硬错】原稿写「其与物种丰富度格局并不一致，保护优先区划定会因指标选择而改变」——"
  "与摘要结论**方向相反**（摘要明言保护区已较好代表 PD 广度、保护内外 beta 组成相近），且未标注研究对象为**墨西哥哺乳动物**（D083④个案当通例）。已按结论重写。").strip()
bd["last_update"]=TODAY

# ===== 3 极端天气预警：DOI 与结论句 =====
ew=T["极端天气预警"]
ew["influence"]=("所引 2022 年发表于 Climatic Change 的研究，检验区域气候模式与常用气象数据集在**肯尼亚北部**预测极端天气型的效力："
  "以人工神经网络结合站点数据的干旱预测准确率达 78–90%，隔离森林法在洪水识别上表现最优。"
  "作者的结论是：**这些模型与数据组合可作为肯尼亚农业部门早期预警系统的基础**。")
ew["pending_notes"]=((ew.get("pending_notes") or "")+
  " 【第40轮返工·硬错】① DOI 订正：原引 10.21203/rs.3.rs-1343486/v1 是**预印本**（题名为另一篇 «Enhancing Food Security in Africa…»），"
  "正式版为 Climatic Change **10.1007/s10584-022-03444-6**，已改。"
  "② 结论句原写「数据不完善会直接限制预警质量、瓶颈常在观测与数据」——是把标题里的 imperfect data 扩写成结论；"
  "摘要结论实为「这些模型与数据集可作为肯尼亚农业预警的基础」，已按结论改写。").strip()
ew["last_update"]=TODAY
for s in sd["sources"]:
    if s["id"].startswith("openalex-W4306771028"):
        s["url2"]="https://doi.org/10.1007/s10584-022-03444-6"
        s["note"]=(s.get("note") or "")+" 【第40轮订正】正式版 DOI 为 10.1007/s10584-022-03444-6（Climatic Change, 2022-10）；原记 10.21203/rs.3.rs-1343486/v1 系预印本，题名不同。"

# ===== 4 南极无农业：归因越界 =====
an=T["南极洲无农业的环境约束"]
an["influence"]=("所引 2014 年章节描述南极陆地环境：冰川与冰缘系统占绝对主导，**生命主要局限于大陆的边缘地带**，"
  "且存在显著的地理差异（半岛与内陆、露岩区与冰下环境）。"
  "**通用事实补充（非该章内容）**：南极露岩区占大陆面积不足 1%（通行估计约 0.3%），维管植物仅 2 种；"
  "这两项须以 SCAR 或南极条约体系的专门来源核验，本条暂不将其归因于所引章节。")
an["pending_notes"]=((an.get("pending_notes") or "")+
  " 【第40轮返工】原稿把「露岩区不足1%」「仅有两种维管植物」写在「所引 2014 年研究描述」之下——"
  "该章摘要并无这两项，属把通识归因给文献（D081/D083）；已拆出并标为「通用事实补充（非该章内容）」，待专门来源核验。").strip()
an["last_update"]=TODAY

# ===== 5 查文文化：时期分开 + 删无源物证 =====
cv=T["查文文化"]
cv["time_or_place"]="查文文化通行跨度约公元前900–前200年；**所引研究覆盖的是更早的初始期晚期至早地平线期（约前1300–前600年）**，两段不可互推"
cv["influence"]=("所引 2004 年研究讨论查文德万塔尔**权威与权力的演化**，其材料包括石雕、切石建筑、地下廊道、地形改造，"
  "以及声光环境与致幻物的使用。作者据此论证仪式中心同时是政治权威形成的场所。"
  "（研究对象的时间段为约前1300–前600年，早于查文文化的通行跨度；本条不据此推断后段的制度。）")
cv["pending_notes"]=((cv.get("pending_notes") or "")+
  " 【第40轮返工】① 时期分开：所引研究覆盖约前1300–前600年，条目文化跨度约前900–前200年，已在 time_or_place 与正文分列（D083②）。"
  "② 删除「热带贝壳、黑曜石」——摘要未列这些物证，属常识补充，已移除。"
  "③ 年份差异说明：Crossref 记 2005-01、OpenAlex 记 2004，属出版与收录时间差。").strip()
cv["last_update"]=TODAY

# ===== 6 可持续交通：未译硬伤 =====
st=T["可持续交通"]
st["influence"]=("所引 2015 年研究以共享汽车（car sharing）作为可持续交通政策的案例，指出道路运输在客运与货运上的主导地位"
  "已带来显著的环境与社会成本；要扭转该趋势，需技术手段与行为改变并行。欧洲的实践显示共享汽车可使**汽车保有量**下降。"
  "这说明单靠技术替代不足，政策与行为同样关键。")
st["pending_notes"]=((st.get("pending_notes") or "")+" 【第40轮返工】未译硬伤「车ownnership」已改为「汽车保有量」。").strip()
st["last_update"]=TODAY

# ===== 7 沙漠化 / 8 自然灾害风险 / 9 城市贫困 / 10 火灾生态 / 非洲大湖 =====
ds=T["沙漠化"]
ds["influence"]=("所引 1998 年研究讨论全球变化对旱地生态系统的冲击：气候变率与土地利用等**干扰事件**叠加，"
  "可把系统推过韧性阈值而造成非线性退化；低复发频率的干扰尤为关键。"
  "（本条把沙漠化理解为「过程而非边界推移」属解释性表述，非该文献的原话。）")
ds["last_update"]=TODAY

nr=T["自然灾害风险"]
nr["influence"]=("所引 2016 年文献为 Oxford Research Encyclopedia 的**预发表摘要（advance summary）**，讨论空间规划与自然灾害风险管理的关系，"
  "涉及把风险信息纳入土地利用决策的必要性。因所引为摘要，本条不将其表述为该文的完整主张。")
nr["pending_notes"]=((nr.get("pending_notes") or "")+" 【第40轮返工】所引为 advance summary（预发表摘要），已标注；「主张把风险信息纳入土地利用决策」弱化为「涉及…的必要性」。").strip()
nr["last_update"]=TODAY

up_=T["城市贫困"]
up_["definition"]="城市贫困：城市居民在社会与经济参与上的匮乏及其空间聚集，常以社会排斥（social exclusion）的框架刻画。"
up_["overview"]=up_["definition"]+" 本条以社会排斥的空间维度为概念框架。"
up_["influence"]=("所引 2006 年章节以「社会排斥／整合」为概念框架，强调**空间本身有其作用**：贫困的空间聚集与邻里效应相互作用。"
  " 本条不据此主张「服务获取」的具体结论——该章节摘要未展开服务可及性。")
up_["pending_notes"]=((up_.get("pending_notes") or "")+" 【第40轮返工】① 按 social exclusion 概念改写；② 弱化「服务获取」（摘要未述）；③ 未译词「inner-city」改为「内城」。").strip()
up_["last_update"]=TODAY

fe=T["火灾生态"]
fe["influence"]=("所引 2014 年研究（被引 506）分析全球树皮厚度的变异，指出**火 regime 是选择与塑造树皮厚度的关键因子**："
  "火既是干扰也是选择压力。作者同时说明，现有数据的不足限制了对该关系的完全精确分析。"
  " 本条不把 regime 窄化为「频率」，也不称两者「共同演化」。")
fe["pending_notes"]=((fe.get("pending_notes") or "")+" 【第40轮返工】① 「共同演化」改为「受火 regime 选择/塑造」；② 补摘要自述局限「数据不足限制精确分析」；③ 「火 regime」保留原术语并加注（强度与频次）。").strip()
fe["last_update"]=TODAY

gl=T["非洲大湖地区"]
gl["influence"]=("所引 2019 年研究比较该区域各湖的水文与物理湖沼学特征，指出**湖盆形态与水量平衡**的差异使各湖表现不同，不能一概而论。"
  " 本条不据该文献推断分层、营养循环或渔业的具体机制。")
gl["pending_notes"]=((gl.get("pending_notes") or "")+" 【第40轮返工】删除「分层与混合→营养循环与渔业」——所引摘要只讲湖盆形态与水量平衡，该推链条属摘要外推。").strip()
gl["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=40;cov["round_processed"]=15
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成：5 FAIL 重写 + 4 微调 + 未译词 + 台账")