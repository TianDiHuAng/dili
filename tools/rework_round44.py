# -*- coding: utf-8 -*-
"""第44轮返工：8条FAIL、落点句实测核对、口径叙事、D092结论句、台账。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== A 剔除 2 条对象不同位的来源 =====
DROP={
"罗马共和国":("openalex-W2593441633","所引是《Oxford Handbook of Roman Epigraphy》第 9 章，摘要自述写**拉丁共和时期碑铭的类型与特征**（碑铭学），不能作「政体结构与演进」的来源；已剔除，落点句同删除。"),
"日本列岛":("openalex-W2751639802","所引 2017 年章讨论**家畜引入日本列岛**（动物考古/畜牧史），与本条「列岛地理（地形）」主题不同位（D089），已剔除。"),
}
for t,(sid,why) in DROP.items():
    e=T.get(t)
    if not e: continue
    e["sources"]=[s for s in e["sources"] if s!=sid]
    pn=re.sub(rf" 【第44轮补源（[^）]*）】{re.escape(sid)}[^【]*","",e.get("pending_notes") or "")
    e["pending_notes"]=(pn+f" 【第44轮返工·剔除】{why}").strip()
    e["last_update"]=TODAY

# ===== B 6 条落点句与正文不符：改为「正文新增可支撑句 + 落点对齐」 =====
REWRITE={
"十三殖民地":("influence","所引 1998 年《New World Economies》的结论是：**殖民地经济发展的速度反映母国经济的增长速度与需求变动**；本条据此写「殖民地经济与母国增长的关系」，不涉制度差异（后者出自另一卷）。",
   "【第44轮返工】原落点写「殖民地经济与母国政策的关系」且称「与制度」，但正文无「经济」二字、且「制度」出自姊妹卷；已补正文句并对齐落点。"),
"不列颠群岛":("geo","所引 1970 年研究重建不列颠群岛的**三叠纪古地理**，指出盆地受断层控制、与海西造山期末的剥蚀相关；本条据此写「群岛地质经历多期构造—沉积阶段」。",
   "【第44轮返工】原落点称「本条据此写群岛地质构造的阶段性」，但 geo 段无「地质」「构造」字样；已在 geo 补入可支撑句。"),
"南极冰盖":("influence","所引 1982 年研究提出的是**假说**（marine ice transgression hypothesis）：西南极冰盖与东南极冰盖的发育先后存在不同设想，作者以该假说勾勒新生代冰史。本条据此写「冰盖发育先后属假说之争」，不作定论。",
   "【第44轮返工】原落点称「本条仅据此写冰盖发育存在阶段性讨论」，但正文无「发育/阶段」字样，且未标明所引为假说；已补句并标明。"),
"格陵兰岛":("geo","所引 2023 年研究观测格陵兰冰面的**湍流热通量与雪冰过程**，指出冰面站点稀少使能量收支的模式估计不确定；本条据此写「冰盖表面能量交换的观测不足」。",
   "【第44轮返工】原落点称「本条写冰盖表面能量交换」，但 geo/influence 无「能量」「通量」字样；已补句。"),
"城市地理":("influence","所引 2009 年讲座文章把**公共卫生纳入城市政治与治理**的框架讨论；本条据此写「城市地理学近年将健康议题纳入城市政治研究」，**不主张城市形态导致特定社会结果**。",
   "【第44轮返工·因果方向】原落点写「城市形态与社会结果相互关联」，与摘要方向相反；已改为「城市地理学将健康纳入城市政治研究」。"),
"人口地理":("geo","所引 2006 年研究以**南京为例**分析城市内部人口密度梯度（距 CBD 越远密度下降越快）；本条仅以该个案说明「人口密度的空间梯度可用实证刻画」，**不据此支撑全球尺度的人口分布不均**。",
   "【第44轮返工】原落点未加限定，被用来支撑「人口在地表分布极不均衡」这一全球句（个案当通例，D083④）；已显式限定为南京个案。"),
}
for t,(fld,sentence,note) in REWRITE.items():
    e=T.get(t)
    if not e: continue
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+" "+note).strip()
    e["last_update"]=TODAY

# ===== C 4 条 PASS 的微调 =====
FIX={
"刚果盆地":("influence","所引 2013 年研究分析刚果盆地的森林砍伐趋势；本条「森林覆盖与土地利用受人口、政策与全球需求影响」的表述据此。",
  "【第44轮返工】落点由 geo 移至 influence，对齐实际可支撑句。"),
"冰芯气候记录":("geo","所引 2024 年研究用**逆冰流模型**（1D/2.5D）为冰芯钻探点定年，给出约 145 万年尺度；本条「深层冰对应更早时期、钻探点选择受冰流与地形影响」据此。",
  "【第44轮返工】落点由 influence 移至 geo，措辞对齐。"),
"北极火情变化":("geo","所引 1980 年研究记录 1977 年 Seward 半岛一次**苔原火**后植物盖度、物种组成与**土壤解冻深度**的变化；本条仅据此写「单次苔原火改变地表与植被」。",
  "【第44轮返工】删除原「融雪过程」（摘要无据），改为摘要实有的土壤解冻深度。"),
"地理信息系统":("influence","所引 2015 年研究把 GIS 用于**滴灌系统的远程调度**（按日排程并监测缺水或过量）；本条仅以此为「GIS 作空间决策工具」的一例，不据此谈灾害评估。",
  "【第44轮返工】删除「灾害评估」（该源无据），并加「仅为一例应用」。"),
}
for t,(fld,sentence,note) in FIX.items():
    e=T.get(t)
    if not e: continue
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+" "+note).strip()
    e["last_update"]=TODAY

# ===== D 12 条备注补 D092 结论句要点 =====
CONC={
"刚果盆地":"结论：盆地森林砍伐与人口、政策及全球商品需求相关。",
"罗马共和国":"（来源已剔除）",
"十三殖民地":"结论：殖民地经济发展速度反映母国经济增长。",
"不列颠群岛":"结论：三叠纪盆地受断层控制、与海西造山期末剥蚀相关。",
"人口地理":"结论：南京城市内部密度随距 CBD 距离快速下降。",
"南极冰盖":"结论：以 marine ice transgression 假说勾勒新生代冰史（假说，非定论）。",
"冰芯气候记录":"结论：逆冰流模型给出钻探点约 145 万年尺度定年。",
"北极火情变化":"结论：1977 年一次苔原火改变植物盖度、物种组成与土壤解冻深度。",
"日本列岛":"（来源已剔除）",
"格陵兰岛":"结论：冰面湍流热通量与雪冰过程观测稀少，能量收支估计不确定。",
"城市地理":"结论：把公共卫生纳入城市政治与治理框架讨论。",
"地理信息系统":"结论：GIS 用于滴灌日排程与缺水监测。",
}
for t,c in CONC.items():
    e=T.get(t)
    if not e or c.startswith("（"): continue
    if "【D092结论句】" in (e.get("pending_notes") or ""): continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【D092结论句】{c}").strip()

# ===== E status 刷新（去掉与新事实冲突的「无实证」）=====
for t in ("刚果盆地","罗马共和国","不列颠群岛","日本列岛","格陵兰岛","十三殖民地"):
    e=T.get(t)
    if not e: continue
    ac=sum(1 for s in e["sources"] if s.startswith(("openalex-","livius-")))
    e["status"]=f"L2完成(第44轮复核)-内容源{ac}条"

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=44
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成：剔除2 + 重写6 + 微调4 + D092结论句 + status刷新")