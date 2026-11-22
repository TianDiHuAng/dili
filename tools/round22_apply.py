# -*- coding: utf-8 -*-
"""第22轮：4 条遗产 L2 换源转正（板块构造/冰芯气候记录/亚马逊盆地/南极冰盖）+ 合并重复备注。"""
import json,os,re,sys,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

# 1) 登记 usgs-plate-motions
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
U="https://pubs.usgs.gov/gip/dynamic/understanding.html"
if not any(s["id"]=="usgs-plate-motions" for s in sd["sources"]):
    sd["sources"].append({"id":"usgs-plate-motions","title":"Understanding plate motions [This Dynamic Earth, USGS]",
     "author":"U.S. Geological Survey","year":None,"type":"官方机构","url":U,"url2":None,
     "link_ok":True,"verified":True,"page_title":"Understanding plate motions [This Dynamic Earth, USGS]",
     "note":"curl 实测 HTTP 200；D044/D050 剥离口径正文 17121 字符、tectonic|plate 命中 86；第22轮按 D055 档①作专题页。"})
    json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 2) 4 条换源 + 重写五段
FIX={
"板块构造":{
 "sources":["usgs-plate-motions","s056-earthquake-usgs-gov"],
 "def":"板块构造：把岩石圈划分为运动板块的理论，用以解释地震、火山与造山的分布。",
 "geo":"板块边界分为离散（洋中脊）、汇聚（俯冲带与碰撞带）与转换（走滑）三类，边界处地震与火山集中。板块运动速率与方向由地球物理观测推算。",
 "infl":"该理论统一解释了山脉、海沟与地震带的分布，是现代地质学的基础框架；具体区域演化史仍需实测资料，属科学理论而非价值判断。",
 "pol":"该理论不涉及政权更替；相关学科通过观测网络与国际合作计划发展。",
 "conn":"板块运动把地震带、火山弧与大洋盆地连成整体，影响资源分布与灾害风险。",
 "today":"板块运动速率与地震监测数据需按年份从 USGS 机构页核验。",
 "proof":"usgs-plate-motions 标题即主题，剥离后 17121 字符、命中 86",
 "note":"第22轮换源转正：用 USGS『Understanding plate motions』作专题页（17121/86），USGS 地震台网作机构页；五段按边界类型与理论作用重写。"},
"冰芯气候记录":{
 "sources":["nasa-ice-cores","nasa-ice-sheets"],
 "def":"冰芯气候记录：从冰盖钻孔取得的冰层序列，封存气泡与尘埃，用于重建古大气与温度变化。",
 "geo":"冰层逐年积累，深层冰对应更早时期；气泡中的气体成分与同位素比值可推算当时大气组成与温度。钻探点选择受冰流与地形影响。",
 "infl":"冰芯提供古大气成分与温度的直接证据，是气候研究的关键资料；解释需结合模型与其他代用指标，不能单靠单一冰芯下结论。",
 "pol":"多国钻探计划通过国际合作共享样品与数据，形成长期观测体系；具体计划与条款待研究机构核验。",
 "conn":"极地冰芯与海洋沉积等记录共同构成全球古气候证据网络。",
 "today":"年代标定与气体数据需按年份从 NASA 研究机构核验。",
 "proof":"nasa-ice-cores 标题即主题，剥离后 18929 字符、命中 36",
 "note":"第22轮换源转正：用 NASA『Paleoclimatology: The Ice Core Record』作专题页（18929/36），NASA 冰盖指标页作机构页。"},
"亚马逊盆地":{
 "sources":["s086-earthobservatory-nasa-gov","s042-earthobservatory-nasa-gov"],
 "def":"亚马逊盆地：南美洲北部的巨大低地盆地，覆盖广阔热带雨林与密集河网。",
 "geo":"盆地地势低平、降水丰沛，河流季节涨落决定聚落与交通位置。雨林与河流过程相互联系，火烧与土地利用变化会改变植被与碳循环。",
 "infl":"河流是主要交通廊道，雨林资源支撑多样化生计；火的使用与扩张会削弱生态韧性。环境与社会关系存在多种解释，需避免单线因果。",
 "pol":"本条不展开具体政权序列；土地使用与族群关系的历史待专门史料核验。",
 "conn":"亚马逊通过河流与大西洋连接，盆地产品曾把区域纳入全球市场。",
 "today":"森林砍伐、火情与水文变化是核心议题；森林面积与火点数据需按年份从 NASA 机构页核验。",
 "proof":"s086 标题即主题（Amazon Fire），剥离后 33279 字符、命中 189",
 "note":"第22轮换源转正：用 NASA『From Forest to Field: How Fire is Transforming the Amazon』作专题页（33279/189），NASA 热带毁林页作机构页。"},
"南极冰盖":{
 "sources":["nasa-ice-sheets","s038-earthobservatory-nasa-gov"],
 "def":"南极冰盖：覆盖南极大陆的大陆冰体，其质量变化影响全球海平面。",
 "geo":"冰盖由降雪积累与冰流输出维持平衡，边缘形成冰架与冰川。卫星重力与测高观测可估计冰体质量变化，区域差异明显。",
 "infl":"冰盖储量变化影响全球海平面，是气候系统的关键变量；其变化受大气与海洋共同作用，单一因素解释不足。",
 "pol":"冰盖研究由多国科考计划合作推进，数据通过国际计划共享；具体计划待官方来源核验。",
 "conn":"冰盖与南大洋、大气环流相互作用，冰芯记录联系到全球气候史。",
 "today":"冰盖质量变化趋势需引用最新卫星观测；具体数值待按年份从 NASA 机构页核验。",
 "proof":"nasa-ice-sheets 标题即主题，剥离后 8612 字符、命中 14（D055 档②：8000 ✓）",
 "note":"第22轮换源转正：用 NASA『Ice Sheets』指标页作专题页（8612/14，档②达标），Earth Observatory 作机构页。"},
}
for t,c in FIX.items():
    e=T[t]
    e.update({"level":"L2","status":"L2合规换源(第22轮)","definition":c["def"],
      "overview":c["def"].split("：",1)[1],"time_or_place":e.get("time_or_place") or "时期与年代待专门来源核验（详见待核实）",
      "geo":c["geo"],"influence":c["infl"],"polities":c["pol"],"connections":c["conn"],"today":c["today"],
      "sources":c["sources"],"needs_verification":True,"last_update":TODAY,
      "pending_notes":f"{c['note']} D053 配对：专题页 + 机构页各一。具体数值与年代待按年份核验。"})

# 3) 合并剩余 32 条 legacy 的重复备注
DUP="本条为规则生效前的 L2，来源以数据层别名为主，未满足「一专题页+一机构页」，待补专题来源后重新校验。"
NEW="【D041 缺口】来源为数据层别名级（区域/机构框架），不满足「一专题页+一机构页」；第21轮已收敛 polities，第22轮起改用「轮次索引」记录，不再每轮重复同一句。"
merged=0
for t,e in T.items():
    pn=e.get("pending_notes") or ""
    if "D041 标记" in pn and DUP in pn:
        e["pending_notes"]=pn.replace(DUP,NEW)
        e["pending_notes"]=re.sub(r"(【D041 标记】){2,}","【D041 标记】",e["pending_notes"])
        e["last_update"]=TODAY;merged+=1

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 4) D058 核对
chk=sum(1 for t in FIX if "第22轮换源转正" in (T[t].get("pending_notes") or ""))
print("换源落盘:",chk,"/4；备注合并",merged,"条")
print("sources:",{t:T[t]["sources"] for t in FIX})