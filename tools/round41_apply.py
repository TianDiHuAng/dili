# -*- coding: utf-8 -*-
"""第41轮：最后 5 条补充 L1 → L2（全部条目达到 L2）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
B=json.load(open(os.path.join(ROOT,"reports","round41_pick.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

BODY={
"阿巴拉契亚山脉":dict(
 defn="阿巴拉契亚山脉：北美东部的山系，由古生代多次造山事件叠加形成。",
 geo="山系自加拿大东南部延伸至美国阿拉巴马，由谷岭区（褶皱与推覆构造）、蓝岭、阿巴拉契亚高原等平行带组成；东侧为山麓与海岸平原，西侧为密西西比河流域。",
 infl=("所引 2002 年研究（被引 163）指出：阿巴拉契亚造山带形成于**早古生代开始、以阿勒格尼造山运动（Alleghanian，320–260 Ma）结束**的过程，"
   "由大陆—大陆碰撞与 Theic 洋最终闭合驱动。作者以阿勒格尼造山作为「拉链式构造（zipper tectonics）」的例证：斜向碰撞后板块旋转、"
   "洋盆自一端向另一端逐步闭合。这说明同一山系可由多期、不同机制的造山事件叠加而成。"),
 conn="西侧经阿巴拉契亚高原与密西西比水系相连，东侧经山麓与海岸平原通向大西洋，是北美东部南北向的天然分界与通道。"),
"古巴岛":dict(
 defn="古巴岛：加勒比海最大的岛屿，位于佛罗里达半岛以南、尤卡坦半岛以东。",
 geo="岛屿呈西北—东南走向，地貌以平原与丘陵为主，东南部为马埃斯特腊山脉；北部为石灰岩台地与喀斯特，海岸多珊瑚礁与海湾。",
 infl=("所引 2004 年研究以古巴中部 Camagüey 地区的 Ar/Ar 定年约束该区构造事件：火山岩全岩年龄为 **74–72 Ma**，"
   "比夹层沉积岩中化石指示的 100–80 Ma 明显年轻；侵入其中的正长岩与花岗闪长岩给出 **75–72 Ma**。"
   "作者把这一年龄解释为火山—侵入弧的**较快抬升与冷却**，并用于约束古巴向北迁移进入加勒比及随后与巴哈马台地碰撞的时间。"
   " 这说明岛屿的现今位置是板块迁移与碰撞的结果。"),
 conn="北隔佛罗里达海峡与美国相望，西隔尤卡坦海峡与墨西哥相望，东经向风海峡接伊斯帕尼奥拉岛，是加勒比海北部航路的中枢。"),
"南极特别保护区":dict(
 defn="南极特别保护区（ASPA）：南极条约区域内保护级别最高的陆域保护区类别。",
 geo="ASPA 分布于南极大陆与亚南极岛屿，选址以代表性生态系统、特有物种与长期监测价值为依据；多数面积很小，位于沿岸露岩区与企鹅、海豹繁殖地附近。",
 infl=("所引 2013 年研究说明制度安排：访客须遵守该区管理计划并取得国家主管机关的**进入许可**；南极条约环境议定书缔约方须交换"
   "①下一季的许可发放数与②上一季的实际访问数。作者以 2008/09–2010/11 提交至电子信息交换系统的数据评估现行许可与信息交换实践，"
   "发现各方对义务的**解释与执行并不一致**。这提示「划定保护区」与「管理到位」之间存在制度执行差距。"),
 conn="经电子信息交换系统在缔约方之间共享许可与访问数据；与南极科考站、旅游活动及环境保护议定书的履约机制相连。"),
"争议边界处理原则":dict(
 defn="争议边界处理原则：在制图与条文中如何处理存在主权争议的边界与领土的表达规则。",
 geo="争议边界分布集中于陆地与海洋主张重叠处：陆地争议常牵动其外缘海域主张，从而形成「陆地—海洋」两层重叠；制图上的线型（实线/虚线）、留白与注记都构成立场表达。",
 infl=("所引 2021 年研究指出：当高潮线地物或大陆领土的主权存在争议时，通常会出现**两组重叠主张**——一组针对陆地本身，"
   "另一组针对该陆地所享有的海域；国家在提出陆地主张后几乎必然随之提出海域主张，形成第二层重叠。"
   "该章讨论争议陆域外接争议水域中各方的权利与义务。这为制图时区分「陆地争议」与「由此衍生的海域争议」提供了框架。"),
 conn="与地图投影、地理空间数据产品、海洋划界与国际法体系相关；制图表达须与实际法律状态区分开。"),
"环境治理":dict(
 defn="环境治理：为解决生态退化而建立的制度、组织与规则体系，含国内与国际两个层面。",
 geo="治理体制的密度与效力在区域间不均衡：国际环境机构多设于发达国家，履约与监测能力在低收入国家较弱；跨界问题（气候、渔业、河流）须跨辖区协调。",
 infl=("所引 2011 年研究评估环境治理体制的**有效性**：既有研究已在较严格的方法框架下审视这类组织的绩效，"
   "但对两类问题关注有限——①组织**学习与创新能力**，②组织与相关**社会政治环境的契合度**。"
   "作者以后社会主义国家（中国与欧洲）的经验说明，修补这一缺口有助于理解治理成效为何差异巨大。"
   " 这说明有效性不只取决于规则文本，也取决于制度学习与情境匹配（D092：以摘要结论为准）。"),
 conn="与气候适应政策、可持续交通、保护与保育区体系、环境数据访问相关；治理成效依赖数据与监测能力。"),
}
n=0;up=[]
for t,b in BODY.items():
    e=T.get(t);c=B.get(t)
    if not e or not c: continue
    oa=c["oa_id"];sid=f"openalex-{oa}"
    if sid not in have:
        code=0;size=0
        for _ in range(3):
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oa}"],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                    if code==200: break
                time.sleep(5)
            except Exception: time.sleep(5)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oa}","url2":f"https://doi.org/{c['doi']}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oa}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host')}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符。"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第41轮)-学术文献","definition":b["defn"],
      "overview":b["defn"]+" 机制/影响段据所引研究撰写，geo 为常识性地理描述（未挂学术来源）。",
      "geo":b["geo"],"influence":b["infl"],"connections":b["conn"],
      "polities":e.get("polities") or "本条为自然地理/概念主题条目，不展开具体政权序列。",
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第41轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c['title']}》，{c.get('host')}，DOI {c['doi']}，被引 {c.get('cited')}），经 Crossref→OpenAlex DOI 桥获取。"
        f" 机制/影响段按摘要结论句撰写（D092），geo 为常识性地理描述。"
        f" 【D081单源声明】britannica-regions/wikipedia-regions 为壳别名、s010-unesco-org 为 UNESCO Culture 首页，均不构成独立内容依据；本条实质为单源（OpenAlex）。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 275 L235 238 L375 218 L515 236 L645 270' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='375' cy='218' r='7' class='pt'/><text x='275' y='196' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
save_docs(docs);update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))
print("剩余L1:",[t for t,e in T.items() if e["level"]=="L1"])