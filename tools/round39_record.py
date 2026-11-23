# -*- coding: utf-8 -*-
"""第39轮：为剩余 20 条补充 L1 记录探测证据（D062/D063：失败也必须留痕）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 每条的失败原因（第38–39轮实测）
WHY={
"南极特别保护区":"OpenAlex 检索「Antarctic Specially Protected Area」无标题含该短语且有摘要的记录；ATS 保护区名录为动态清单页，不宜作内容来源。",
"南极洲无农业的环境约束":"本轮候选为《Biological invasions in terrestrial Antarctica》（生物入侵），与「无农业」无逻辑关系，按 D081 剔除；「无农业」属该区域环境约束的常识推论，缺可核验端点。",
"沙漠化":"OpenAlex 检索「desertification」在限流前仅返回无摘要记录；世界银行无「荒漠化面积」指标（拟用 AG.LND.FRST.ZS 替代因口径不符按 D077 弃用）。",
"争议边界处理原则":"本条为编辑原则（本站如何处理争议边界的画法与表述），非地理实体；OpenAlex 的「boundary」候选均为管理学 boundary work 概念，按 D081 剔除。",
"生物多样性分布":"世界银行 ER.BDV.TOTL.ZS 返回无值；OpenAlex 检索在限流下未取得含摘要且标题匹配的记录。",
"城市热岛":"世界银行仅有 PM2.5（EN.ATM.PM25.MC.M3），与热岛强度口径不符（D077 弃用）；OpenAlex 检索「urban heat island」在限流下未返回。",
"自然灾害风险":"世界银行 EN.CLC.MDAT.ZS 返回无值；OpenAlex 检索在限流下未返回。",
"极端天气预警":"世界银行无对应指标；OpenAlex 检索在限流下未返回。",
"城市贫困":"世界银行 SI.POV.URBN.ZS 返回无值（该指标近年缺报）；OpenAlex 检索在限流下未返回。",
"可持续交通":"世界银行无对应指标（IS.ROD.TOTL.KM 已停更）；OpenAlex 检索在限流下未返回。",
"环境治理":"世界银行 IQ.CPA.ENVR.XQ 已停更；OpenAlex 检索在限流下未返回。",
"火灾生态":"世界银行仅有森林覆盖率，与火灾生态口径不符（D077 弃用）；OpenAlex 检索在限流下未返回。",
"法蒂玛王朝":"OpenAlex 两轮检索（Fatimid caliphate / Fatimid dynasty）均未取得标题匹配且有摘要的记录。",
"非洲大湖地区":"OpenAlex 候选为《A sister lineage of the Mycobacterium tuberculosis》（结核分枝杆菌谱系），对象为病原体而非区域，按 D081 剔除。",
"古巴岛":"OpenAlex 候选为女王凤凰螺（Aliger gigas）群体遗传研究，对象为海洋生物而非岛屿地理，按 D081 剔除。",
"查文文化":"OpenAlex 候选为《Ancient Peruvian optics... Chavin》(镜面光学)，主题过窄且非文化整体，按 D081 剔除。",
"南美贸易网络":"OpenAlex 候选为安第斯考古木材树种鉴定，非贸易网络，按 D081 剔除。",
"南锥体":"OpenAlex 候选为《Rapid coastal spread of First Americans》(人群迁徙)，与区域地理主题不符，按 D081 剔除（与巴塔哥尼亚处理口径一致，见 D089）。",
}
n=0
for t,why in WHY.items():
    e=T.get(t)
    if not e or e["level"]!="L1": continue
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第39轮渠道探测】{why} 本轮未升级；该条保持 L1 骨架。").strip()
    e["last_update"]=TODAY;n+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 写探测报告（可追溯）
rep={"round":39,"date":TODAY,
 "openalex_status":"429 rate-limited throughout (测试于 12:04 与 12:15 均返回 429)",
 "tested_queries":["urban heat island","desertification drylands","sustainable transport mobility"],
 "world_bank_tested":{"ER.BDV.TOTL.ZS":"无值","SI.POV.URBN.ZS":"无值","EN.CLC.MDAT.ZS":"无值",
   "EN.ATM.PM25.MC.M3":"有值但口径不符(热岛)","AG.LND.FRST.ZS":"有值但口径不符(火灾)",
   "IQ.CPA.ENVR.XQ":"已停更","IS.ROD.TOTL.KM":"已停更"},
 "kept_l1":sorted(WHY.keys()),
 "reasons":WHY}
json.dump(rep,open(os.path.join(ROOT,"reports","round39_probe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
import collections
print("记录探测失败",n,"条")
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))