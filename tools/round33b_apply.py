# -*- coding: utf-8 -*-
"""第33轮续：升级 马格里布/阿拉伯半岛/埃塞俄比亚高原（Wikidata 面积/海拔）。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
G=json.load(open(os.path.join(ROOT,"reports","round33_wikidata_geo.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

SPEC={
"马格里布":("mass","面积","6,045,741 km²",
 "地中海沿岸与阿特拉斯山脉之间的区域，北缘冬季降水支撑谷物与橄榄，南缘过渡为干旱草原；山脉与海岸决定交通与聚落分布。",
 "沿海降水与港口条件支撑农业与贸易；内陆干旱与山地阻隔使区域内部差异显著，政治整合受地形与距离制约。",
 "经地中海港口连接南欧，经撒哈拉通道连接西非与萨赫勒，是南北与东西商路的交汇区。"),
"阿拉伯半岛":("mass","面积","3,200,000 km²",
 "干旱高原与沙漠为主，边缘山地与沿海平原降水稍多；绿洲、井泉与沿海港口决定人口与商路节点分布。",
 "干旱条件限制定居农业，绿洲与商路位置成为政治经济重心；半岛的边缘性（红海与波斯湾两翼）使其长期充当东西方贸易中介。",
 "西临红海连接埃及与东非，东临波斯湾连接美索不达米亚与印度洋航线，南北向商路贯穿绿洲带。"),
"埃塞俄比亚高原":("elev","最高海拔","4,550 m",
 "高原由火山岩与断崖构成，海拔多在 2,000 米以上，降水较周边丰沛，是青尼罗河等河流的发源地；裂谷纵切高原。",
 "高海拔带来较温和的气候与农业条件，也造成交通阻隔；高原的防御性与农业基础支撑了独立政权的延续，但具体政治形态由制度与历史塑造。",
 "通过青尼罗河连接尼罗河流域，经红海港口连接阿拉伯半岛与印度洋贸易。"),
}
n=0;up=[]
for t,(key,lab,disp,geo,infl,conn) in SPEC.items():
    e=T.get(t);w=G.get(t)
    if not e or not w or key not in w["vals"]: continue
    qid=w["qid"];sid=f"wikidata-{qid.lower()}"
    if sid not in have:
        sd["sources"].append({"id":sid,"title":f"Wikidata {qid} — {t}",
          "author":"Wikidata（Wikimedia 社区，CC0）","year":None,"type":"开放数据集",
          "url":f"https://www.wikidata.org/wiki/{qid}",
          "url2":f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json",
          "link_ok":True,"verified":True,"page_title":f"Wikidata {qid} — {t}",
          "note":f"Wikidata 实体 {qid}；英文描述「{w.get('desc','')}」；{lab} = {disp}（属性 {'P2046' if key=='mass' else 'P2044'}）。第33轮 API 成功。众包数据，仅作双源之一。"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第33轮)-Wikidata量值",
      "definition":f"{t}：据 Wikidata 结构化记录，{lab}为 {disp}。",
      "overview":f"据 Wikidata 结构化记录，{lab}为 {disp}；具体边界与内部差异待专门地理来源核验。",
      "time_or_place":f"{lab} {disp}（Wikidata {'P2046' if key=='mass' else 'P2044'}）",
      "geo":geo,"influence":infl,
      "polities":e.get("polities") or "本条以自然地理与区域概述为主；具体政权序列待专门史料核验。",
      "connections":conn,
      "today":e.get("today") or "本条以地理与区域概述为主，当代指标见相关「区域发展」类条目。",
      "sources":[sid,"un-m49"],"needs_verification":True,
      "pending_notes":(f"第33轮升级：{lab}（{disp}）来自 Wikidata {qid} 的结构化属性。"
        f" 【单源待互证】该量值目前仅一处结构化来源；UNSD M49 作区域框架，不构成第二独立印证。具体边界与统计口径待专门地理来源核验。"),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<ellipse cx='380' cy='200' rx='230' ry='105' fill='none' stroke='var(--accent)' stroke-width='3'/>"
      f"<text x='300' y='205' class='lbl'>{t}</text>"
      f"<text x='450' y='235' class='dim'>{disp}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"条：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))