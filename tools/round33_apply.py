# -*- coding: utf-8 -*-
"""第33轮：升级 10 条重要 L1 政权条目为 L2（Wikidata 年代 + 单源待互证标注）。"""
import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
W=json.load(open(os.path.join(ROOT,"reports","round33_wikidata.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

# 各条的专题内容（地理/influence/connections 差异化）
BODY={
"古埃及新王国":("period from 1570 to 1069 BC in Egypt",
 "尼罗河谷与三角洲的农业剩余支撑人口与工程能力；底比斯所在的上埃及河谷是宗教与政治重心。河流运输把南北连成整体，绿洲与红海通道通向外部。",
 "河谷农业与尼罗河运输是国家动员的基础；对外扩张与防务同样依赖组织与财政，地理条件提供约束与机会，不作单因解释。",
 "经三角洲连接地中海东岸，经红海与西奈连接西亚，经努比亚走廊向南接触非洲内陆。"),
"库什与努比亚":("c. 1070 BCE – c. CE 350 / kingdom in Nubia",
 "尼罗河上游的河谷与沙漠之间的绿洲带，河道险滩（cataract）分割区段，形成南北交通的天然节点与屏障。",
 "河谷农业与金矿资源支撑政权财富；商路控制与埃及的互动塑造了区域政治，资源禀赋是条件之一而非全部原因。",
 "沿尼罗河向北连接埃及，向东经沙漠通道通往红海，向南接触非洲内陆资源区。"),
"罗马阿非利加":("Roman province on the northern African coast",
 "地中海沿岸的狭长农耕地带，背靠阿特拉斯山地，海岸港口利于输运；冬季降水支撑谷物与橄榄。",
 "海岸与港口条件使该地区成为罗马的粮食与橄榄油供应地；行省治理与税收制度决定剩余如何被抽取，不能仅由土壤解释。",
 "经迦太基等港口连接意大利与地中海东部，经陆路连接努比亚与撒哈拉边缘。"),
"加纳帝国":("West African empire based in modern-day Mauritania and Mali",
 "萨赫勒草原与绿洲带交界处，跨撒哈拉商路的南端；季节性降水与井泉决定聚落与牧群分布。",
 "控制黄金与盐的南北向贸易是财富来源；王权与商路节点的关系塑造了政治结构，地理提供通道而非决定形态。",
 "北接撒哈拉商路通往马格里布，南连尼日尔河上游的农业区与黄金产地。"),
"桑海帝国":("former state located in western Africa",
 "尼日尔河中游的河湾与洪泛平原，河流提供运输与渔业，草原支持牧业；南北向商路穿过萨赫勒。",
 "河运与跨撒哈拉贸易支撑城市与王权；军事组织与行政安排决定扩张与维持，河网条件只是基础之一。",
 "沿尼日尔河连接西非内陆与贸易节点，北通撒哈拉至马格里布，东接豪萨地区。"),
"笈多王朝":("ancient Indian empire (c. 3rd century CE–575 CE)",
 "北印度恒河平原的冲积土与季风降水支撑密集农业，河谷是人口与城市重心；周边山地与森林提供资源与屏障。",
 "农业剩余与贸易网络支撑城市与文化繁荣；统一与分裂同地方势力与继承安排相关，地理条件提供基础而不决定政治周期。",
 "经陆路连接中亚与西北印度，经孟加拉湾港口接入印度洋贸易，与东南亚存在文化与商业往来。"),
"商代":("the first ancient Chinese dynasty to leave historical records",
 "黄河中下游的冲积平原与黄土台地，河谷农业与青铜资源分布决定聚落与都邑迁徙；气候较今温暖湿润。",
 "河谷农业支撑人口与手工业，青铜礼器与占卜反映王权与祭祀组织；资源获取与军事行动同样重要，不能单由土壤解释。",
 "经黄河支流网络连接关中与华北，向北接触草原地带，向南延伸至长江中游的铜矿带。"),
"周代":("dynasty of Ancient Chinese kings lasting from 1046 BC to 256 BC",
 "核心区在关中盆地与黄河中游，渭河谷地提供农业与防御条件；东向的华北平原则是封建诸侯的主要分布区。",
 "分封与宗法把亲属与功臣安置于要冲，地理距离与交通条件影响控制强度；制度设计是政治整合的主要机制，地理提供成本约束。",
 "以渭河—黄河轴心连接关中与中原，通过汉水与长江流域接触南方，向北与草原势力互动。"),
"秦代":("dynasty that ruled in China from 221 to 206 BC",
 "以关中为根据地，渭河平原与函谷关等隘口构成易守难攻的地理优势；统一后覆盖黄河与长江两大流域。",
 "关中的农业与地形优势利于积蓄力量，但统一后的整合依赖郡县制、统一度量衡与交通工程，地理只是起点条件。",
 "修驰道与直道连接关中、华北与北方边地，南向延伸至岭南，形成首次跨流域的行政交通网。"),
"元代":("Mongol-led imperial dynasty of China (1271–1368)",
 "以大都（今北京）为中枢，控制华北平原与蒙古高原的接合部；南北向的大运河与海运并用以输送南方粮赋。",
 "草原与农耕区的双重基础支撑统治，驿站与海运是关键基础设施；治理成效取决于制度与财政安排，不能仅由疆域解释。",
 "驿站网络连接漠北、中原与中亚，海路连接东南亚与印度洋，形成陆海并用的交通格局。"),
}
n=0;upgraded=[]
for title,(desc,geo,infl,conn) in BODY.items():
    e=T.get(title)
    if not e: continue
    w=W.get(title,{})
    if not (w.get("start") and w.get("end")): continue
    qid=w["qid"]; sid=f"wikidata-{qid.lower()}"
    if sid not in have:
        sd["sources"].append({"id":sid,"title":f"Wikidata {qid} — {w.get('label')}",
          "author":"Wikidata（Wikimedia 社区，CC0）","year":None,"type":"开放数据集",
          "url":f"https://www.wikidata.org/wiki/{qid}","url2":f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json",
          "link_ok":True,"verified":True,"page_title":f"Wikidata {qid} — {w.get('label')}",
          "note":f"Wikidata 实体 {qid}；英文描述「{desc}」；起止 {w['start']}–{w['end']}（精度=年）。第33轮 API 查询成功。众包数据，按 TASK 规则仅作双源之一。"})
        have.add(sid)
    span=f"{w['start']}–{w['end']}"
    e.update({"level":"L2","status":"L2完成(第33轮)-Wikidata年代","definition":f"{title}：据 Wikidata 结构化记录为 {span}。",
      "overview":f"据 Wikidata 结构化记录为 {span}；具体疆域与制度演变待专门史学来源核验。",
      "time_or_place":f"{span}（Wikidata P571/P576 或 P580/P582，精度=年）",
      "geo":geo,"influence":infl,
      "polities":f"据 Wikidata 记录，起于 {w['start']}、讫于 {w['end']}（精度=年）。具体统治者序列、年号与制度细节待专门史学来源逐条核验。",
      "connections":conn,
      "today":e.get("today") or "本条为历史条目，现状数据不在本页展开；相关国家或区域的当代指标见「区域发展」类条目。",
      "sources":[sid,"s010-unesco-org"],"needs_verification":True,
      "pending_notes":(f"第33轮升级：年代（{span}）来自 Wikidata {qid} 的结构化属性（精度=年）。"
        f" 【单源待互证】本条关键年代目前仅有 Wikidata 一处结构化来源（Britannica/Wikipedia/DBpedia 在本环境均不可达）；"
        f"UNESCO Culture 首页作机构背景，不构成第二独立印证。需补专题或学术来源后转为双源。"),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M80 260 C 200 220 320 200 460 205 C 570 210 650 235 690 260' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<text x='120' y='240' class='lbl'>{w['start']}</text>"
      f"<text x='560' y='252' class='lbl'>{w['end']}</text>"
      "<path d='M120 280 L560 285' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='6 4'/>"
      f"<text x='40' y='370' class='dim'>{title} · 简略时间轴示意，非精确测绘</text></svg>")
    n+=1;upgraded.append(title)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"条：","、".join(upgraded))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))