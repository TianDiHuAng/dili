# -*- coding: utf-8 -*-
"""第34轮：升级「城市起源」（最后一条核心 L1）为 L2；登记其余学术第二来源。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
O=json.load(open(os.path.join(ROOT,"reports","round34_openalex2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

def chk(url):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return 0,0
        b,c=raw.rsplit("\n__HTTP__",1); return int(c.strip() or 0),len(b)
    except Exception: return 0,0

def add(t, c, kind="第二来源"):
    oa=(c.get("id") or "").rsplit("/",1)[-1]
    sid=f"openalex-{oa}"
    if sid not in have:
        code,size=chk(f"https://api.openalex.org/works/{oa}")
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),"type":"学术文献",
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":(c.get("title") or "")[:120],
          "note":(f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。"
                  f"JSON API HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:280]}…")})
        have.add(sid)
    return sid

# 1) 城市起源：核心 L1 → L2
co=T.get("城市起源")
if co:
    c=O.get("城市起源",[])
    if c:
        c=c[0]
        sid=add("城市起源",c)
        co.update({"level":"L2","status":"L2完成(第34轮)-学术专题",
          "definition":"城市起源：聚落向城市形态转变的过程。据 Cambridge Archaeological Journal 2014 年研究，世界最早的城市出现于两河流域平原（今伊拉克与叙利亚一带），时间在公元前第四千纪。",
          "overview":"据 Cambridge Archaeological Journal（2014）对美索不达米亚聚落过程的研究，世界最早的城市出现在两河流域平原，时间为公元前第四千纪。该研究同时指出，既有解释多假设「革命性的社会变化」「亲属关系作为组织原则的消失」与「理性官僚的出现」，并提出替代模型。起源机制本身是学术争论，不是定论。",
          "time_or_place":"公元前第四千纪（约前4000–前3000年），两河流域平原（据 Cambridge Archaeological Journal 2014）",
          "geo":"两河流域的冲积平原由底格里斯河与幼发拉底河的泥沙沉积形成，地势低平、灌溉便利。河流的不定期泛滥要求排水与蓄水安排，灌溉农业因此成为聚落密集的前提。平原缺乏石材与木材，建筑以泥砖为主，这一材料条件塑造了城市形态。",
          "influence":"灌溉农业带来的剩余、人口集中与专业分工是城市出现的条件；但把城市视为「为精英目标而作的功能性适应」只是其中一种解释，学术界另有强调家庭单位连续性与本土制度演化的模型。地理条件提供可能，制度与组织决定形态，不宜单因解释。",
          "polities":"本条不展开具体政权序列。起源时期的治理形态（神庙经济、城邦议事、家庭生产单位）存在竞争性解释，待专门考古与文献研究核验。",
          "connections":"乌鲁克等早期城市通过河道与陆路连接周边聚落，形成原料（木材、金属、石材）与农产品交换的网络；两河平原缺乏的物资须从周边山地与高地输入，这一结构性缺口推动了远距离交换。",
          "today":"来源：世界银行 API（指标 SP.URB.TOTL.IN.ZS，城市人口占比）：全球 2025年 57.8%。城市化率只反映居住形态的比例，不等于城市治理或生活质量；各国城镇化口径与城市定义差异较大，跨国比较须核对。",
          "sources":[sid,"wb-wld-urban"],
          "needs_verification":True,
          "pending_notes":(f"第34轮升级：由 L1 升 L2。第二来源为 OpenAlex 收录的 Cambridge Archaeological Journal 2014 年论文"
            f"（「Households and the Emergence of Cities in Ancient Mesopotamia」，DOI 10.1017/s095977431400047x），"
            f"其摘要明确给出「the world's first cities emerged on the plains of Mesopotamia … in the fourth millennium bc」，"
            f"可直接支撑本条的时间与地点断言。现状数据用世界银行 WLD 城市化率端点。"
            f" 机制解释部分已并列多种学说，未作单一归因。"),
          "last_update":TODAY})
        co["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
          "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
          "<path d='M80 300 C 200 285 320 275 470 270 C 580 266 650 262 690 258' fill='none' stroke='var(--accent)' stroke-width='3'/>"
          "<path d='M80 300 C 200 310 330 318 470 322' fill='none' stroke='var(--accent2)' stroke-width='3'/>"
          "<circle cx='240' cy='292' r='5' class='pt'/><circle cx='400' cy='278' r='7' class='pt'/>"
          "<circle cx='540' cy='268' r='9' class='pt'/>"
          "<text x='150' y='250' class='lbl'>聚落</text><text x='360' y='250' class='lbl'>镇</text><text x='520' y='240' class='lbl'>城市</text>"
          "<text x='40' y='370' class='dim'>城市起源 · 简笔示意，非精确测绘</text></svg>")
        print("城市起源 → L2 完成")

# 2) 其余条目登记第二来源（分级标注）
GRADE={"蒙古帝国":("强","摘要明确写「During the thirteenth century, the Mongols created the greatest empire in human history」，可证世纪与规模表述"),
 "罗马阿非利加":("强","专论「Land, city, and trade in the Roman Empire」，含北非行省土地与劳力章节"),
 "商代":("中","专著《China in the Early Bronze Age: Shang Civilization》，可证青铜时代商文明的存在与学术地位；摘要未给具体年代"),
 "长江流域":("中","《Water Research》2018 论文，主题为长江流域氮磷输运（1900–2010），可支撑「流域为完整水文单元」的表述；未涉河长"),
 "阿兹特克":("中","论前西班牙时期中墨西哥的政治权力与意识形态，可支撑政治组织表述；未给年代"),
 "加纳帝国":("中","世界史比较框架下的扩张与收缩研究，可支撑萨赫勒政权与跨撒哈拉贸易的一般表述"),
 "马格里布":("弱","西北非人群线粒体 DNA 研究，仅可支撑「区域人群存在长期连续性」；与地理/政权主题相关性弱")}
n=0
for t,(lv,why) in GRADE.items():
    e=T.get(t); c=(O.get(t) or [None])[0]
    if not e or not c: continue
    sid=add(t,c)
    srcs=e.get("sources") or []
    if sid not in srcs: srcs.append(sid)
    e["sources"]=srcs
    e["pending_notes"]=((e.get("pending_notes") or "").replace("【单源待互证】","【第34轮补第二来源】")+
      f" 【第34轮第二来源（{lv}）】OpenAlex {sid}（{c.get('year')}年，「{(c.get('title') or '')[:60]}」，DOI {c.get('doi') or '无'}）：{why}。").strip()
    e["last_update"]=TODAY; n+=1

json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("登记第二来源",n,"条；总来源",len(json.load(open(P,encoding='utf-8'))['sources']))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))