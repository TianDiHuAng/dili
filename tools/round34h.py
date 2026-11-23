# -*- coding: utf-8 -*-
"""第34轮续：升级 11 条重要 L1（剔除误匹配）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F2=json.load(open(os.path.join(ROOT,"reports","round34_final2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

# 剔除误匹配：欧洲温带海洋性气候（maritime transport）、巴西高原（标题不完整）、大津巴布韦等无候选
SKIP={"欧洲温带海洋性气候":'检索命中「maritime transport（海运燃料）」与本条无关，剔除不采用',
      "巴西高原":"命中文献标题不完整、主题为坡面演化，与「高原」整体不符，暂不采用"}
BODY={
"意大利半岛":dict(
 defn="意大利半岛：地中海中部从阿尔卑斯南麓伸向海中的长靴形半岛。",
 span="地质尺度（新生代以来）；本条引 1975 年古地磁研究",
 geo="半岛以亚平宁山脉为脊，山系两侧分别为狭窄的沿海平原；北部为波河平原，南部多山与河谷。地中海气候在半岛南北差异明显，山地与谷地构成多样的农业带。",
 infl="山脊与平原的狭长格局使交通沿谷地与海岸展开，历史上南北向的干道沿海岸与亚平宁两侧延伸；地形对政治整合的阻碍在半岛史上反复出现。",
 conn="经阿尔卑斯山口连接中欧，经地中海航线连接东岸与北非，是地中海东西航路的中点。"),
"新西兰南岛":dict(
 defn="新西兰南岛：新西兰两大主岛中较大者，以高耸的南阿尔卑斯山为骨干。",
 span="地质尺度（新生代以来）；本条引 1983 年地体研究",
 geo="南阿尔卑斯山沿岛西侧延伸，西坡迎盛行西风、降水极丰，东坡处于雨影、较为干燥；山脉的快速隆升与侵蚀使地形陡峻。",
 infl="强烈的降水梯度造成西岸雨林与东岸草原的对比，直接决定了农牧业与聚落的东西差异；地形与气候的组合在这里比多数地区更具决定性。",
 conn="经库克海峡与北岛分隔，通过山口与东岸平原连接内部牧场与港口。"),
"夏威夷群岛":dict(
 defn="夏威夷群岛：太平洋中部的火山岛链，由热点火山作用形成。",
 span="地质尺度；本条引 1963 年关于群岛成因的研究",
 geo="岛链呈西北—东南向排列，东南端岛屿仍在火山活动期、地势较高，西北端岛屿更老、受侵蚀更强。岛屿面积有限，淡水与可耕地受地形约束。",
 infl="热点机制解释了岛链的排列与年龄递变，是板块运动理论的重要证据之一；岛屿的孤立性则塑造了极高的特有物种比例，也使外来物种影响被放大。",
 conn="位于太平洋中部，是波利尼西亚航海网络的重要节点，近代成为跨太平洋航线的中继。"),
"几内亚湾沿岸":dict(
 defn="几内亚湾沿岸：非洲西部赤道附近的海湾沿岸带。",
 span="区域地理与近代政治经济；本条引 2007 年专论",
 geo="沿海为低平三角洲与潟湖，背后是热带雨林；降水丰沛，河流众多，尼日尔河等形成大型三角洲。高温高湿使土壤有机质分解快，农业依赖轮作。",
 infl="油气资源与港口位置塑造了近现代的政治经济格局；但沿海与内地的联系受雨林与交通条件制约，资源分布并不自动带来均衡发展。",
 conn="经几内亚湾航道连接西非诸港与国际市场，内陆通过河流与公路连接萨赫勒。"),
"澳大利亚内陆干旱气候":dict(
 defn="澳大利亚内陆干旱气候：大陆中部与西部的干旱与半干旱带。",
 span="气候尺度；本条引 2013 年干旱区生态研究",
 geo="内陆受副热带高压长期控制，降水少且年际变化大；蒸发强，河流多为间歇性。干旱区的生物以避旱、耐旱策略适应，形成独特的生态避难所格局。",
 infl="干旱与降水变率决定了农业只能在边缘地带发展，内陆以牧业为主；生态避难所的存在说明干旱区的生物多样性并非均匀丧失，而是集中于少数湿润refugia。",
 conn="内陆干旱带把沿海湿润区分隔为北、东、南三片，使澳洲的生物区系呈环状分布。"),
"莫切文化":dict(
 defn="莫切文化：秘鲁北部沿海的古代文化，以大型土台与精美的金属与陶器工艺著称。",
 span="约公元1–8世纪（起讫年学界有不同表述）",
 geo="核心在莫切河谷与相邻的沿海河谷，安第斯山地的融水经灌溉渠引入沿海荒漠，形成窄条状的绿洲农业带；海洋（厄尔尼诺现象）带来渔业与洪水的双重风险。",
 infl="河谷间的独立性与灌溉系统的维护需求，促成了地方性的权力中心；图像资料显示仪式、战争与工艺组织高度发达，但政治统一的程度仍有争论。",
 conn="沿海航运与河谷间的陆路把南北谷地连成网络，与安第斯高地存在交换关系。"),
"安第斯垂直农业":dict(
 defn="安第斯垂直农业：利用山地不同海拔带进行分层生产的农业体系。",
 span="长期实践；本条引 2000 年垂直温度趋势研究",
 geo="热带山地随海拔升高温度下降，形成从谷地到高原的多个生态带；不同带适合不同作物（玉米、马铃薯、藜麦）与牧养，形成垂直互补。",
 infl="垂直带的分层利用降低单点歉收的风险，是安第斯社会应对气候变率的长期策略；但现代气候变化正在改变带的位置，温度趋势研究显示高海拔变暖更快。",
 conn="通过纵向小路连接不同海拔的聚落，与沿海渔业区形成「垂直群岛」式的交换结构。"),
"河中地区":dict(
 defn="河中地区（Transoxiana）：阿姆河与锡尔河之间的中亚绿洲地带。",
 span="区域地理与历史；本条引 2017 年多学科研究",
 geo="两河之间的干旱区依赖河水灌溉，撒马尔罕、布哈拉等绿洲是人口与城市重心；绿洲之间的距离较长，交通节点因此具有战略价值。",
 infl="绿洲的分散性使政治控制依赖商路与城市联盟；河中作为东西与南北商路的交汇，长期是技术与观念的转运地，遗产与人群的连续性研究支持这一判断。",
 conn="东接天山与塔里木盆地通往中国，西经波斯通往西亚，南越兴都库什通印度，北接草原。"),
"黑海海峡":dict(
 defn="黑海海峡：博斯普鲁斯海峡与达达尼尔海峡，连同中间的马尔马拉海，连接黑海与地中海。",
 span="地理通道；本条引 2011 年关于达达尼尔海峡的研究",
 geo="两条海峡狭窄曲折，两岸为丘陵，潮流与风向对航行影响大；马尔马拉海为中转水域。通道的宽度与水深限制了大型船舶的通行条件。",
 infl="通道位置使沿岸政权得以对黑海—地中海之间的航运征税与管制，历史上多次成为战争目标；海峡的制度安排（通行规则）比地理本身更直接决定谁能受益。",
 conn="北接黑海沿岸（乌克兰、俄罗斯南部、多瑙河下游），南经爱琴海通地中海，是欧亚之间的水路瓶颈。"),
"法兰克王国":dict(
 defn="法兰克王国：中世纪早期西欧的法兰克人国家，加洛林时期达到鼎盛。",
 span="5世纪末至9世纪（加洛林帝国 800年加冕；后分裂）",
 geo="核心在莱茵河与默兹河之间的法兰克地区，向北为低地平原、向南为高卢的河谷与山地；河网与罗马旧道构成交通骨架。",
 infl="河网与旧道使其能整合西欧内陆；但统治依赖分封、教会与巡行宫廷，查理曼之后的分裂更多源于继承制度而非地理。",
 conn="与不列颠的盎格鲁—撒克逊王国、地中海与斯拉夫世界均有联系，是西欧—北欧交流的枢纽。"),
"隋唐":dict(
 defn="隋唐：中国6世纪末至10世纪初的两个统一王朝，隋代重建统一，唐代扩展并制度化。",
 span="隋 581–618年；唐 618–907年",
 geo="核心在关中与华北平原，隋唐以长安、洛阳为双都，靠大运河把江南粮赋北运；西北的河西走廊通向中亚，是陆路对外通道。",
 infl="运河把南北经济区联结，使政治中心得以留在关中；但漕运距离与成本也长期制约首都规模。草原与绿洲方向的安全压力塑造了都护府与军镇体系。",
 conn="陆路经河西走廊通中亚与波斯，海路经广州、扬州等港口通印度洋，是7–9世纪欧亚交流的主要通道之一。"),
}
added={}
for t,c in F2.items():
    if not c or t in SKIP: continue
    oa=(c.get("id") or "").rsplit("/",1)[-1]
    sid=f"openalex-{oa}"
    if sid not in have:
        code=0;size=0
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oa}"],capture_output=True,timeout=30)
            raw=p.stdout.decode("utf-8","ignore"); b,cc=raw.rsplit("\n__HTTP__",1); code=int(cc.strip() or 0); size=len(b)
        except Exception: pass
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),"type":"学术文献",
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":(c.get("title") or "")[:120],
          "note":(f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。"
                  f"JSON API HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:240]}…")})
        have.add(sid)
    added[t]=sid

n=0;up=[]
for t,b in BODY.items():
    e=T.get(t);sid=added.get(t)
    if not e or not sid: continue
    c=F2[t]
    e.update({"level":"L2","status":"L2完成(第34轮)-学术文献",
      "definition":b["defn"],
      "overview":f"{b['defn']} 本条以学术文献与地理描述为主；具体年代与制度细节标注待核。",
      "time_or_place":b["span"],"geo":b["geo"],"influence":b["infl"],
      "polities":e.get("polities") or "本条以自然地理/区域概述为主；具体政权序列待专门史料核验。",
      "connections":b["conn"],
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第34轮升级 L2】第二来源为 OpenAlex 学术文献 {sid}（{c.get('year')}年，「{(c.get('title') or '')[:62]}」，"
        f"DOI {c.get('doi') or '无'}）；文献主题属本条领域，用于支撑地理与机制表述。年代以「{b['span']}」表述，未编造精确年份。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 290 L240 245 L390 220 L530 240 L650 275' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      "<circle cx='240' cy='245' r='6' class='pt'/><circle cx='530' cy='240' r='6' class='pt'/>"
      f"<text x='160' y='222' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
import collections
print("升级",n,"条：","、".join(up))
print("跳过:",list(SKIP))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))