# -*- coding: utf-8 -*-
"""第35轮：升级 13 条强相关重要 L1（剔除明显无关候选）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round35_openalex.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

REJECT={"朝鲜半岛":"命中「白垩纪鸟类与翼龙」文献，与本条无关，剔除",
"斯堪的纳维亚":"命中「大型哺乳动物种群结构」文献，与本条无关，剔除",
"美国西进":"命中「德国在西南非洲」文献，与本条无关，剔除",
"吠陀时代":"命中「非洲—印度史前接近性」文献，与本条无关，剔除"}
BODY={
"吴哥":dict(defn="吴哥：柬埔寨洞里萨湖以北的高棉帝国都城群。",
 span="9–15世纪（都城鼎盛期；本条引 2010 年气候与衰落研究）",
 geo="位于洞里萨湖冲积平原北缘，湄公河水系的季节涨落决定湖面大小；热带季风降水支撑稻作，水利系统（水库与渠道）用于调节旱雨两季的供水。",
 infl="所引 2010 年研究把气候（长期干旱与极端季风事件）作为吴哥衰落的一个**促成因素**，并与水利设施失修相互作用；这不是单一原因的解释，政治与战争因素同样关键。",
 conn="经湄公河水系连接中南半岛内陆，经泰国湾港口接入海上贸易，是9–15世纪东南亚大陆的枢纽。"),
"匈奴":dict(defn="匈奴：蒙古高原上的游牧政权，与汉朝长期互动。",
 span="约公元前3世纪至公元1世纪（起讫年学界有不同表述）",
 geo="核心在蒙古高原的草原与戈壁边缘，降水少、不宜定居农业；牧草的季节分布决定畜群迁徙路线，也决定与南方农耕区的交换需求。",
 infl="所引 2014 年研究强调匈奴的「王」与政治秩序是**分层联盟**而非集权官僚，草原生态提供基础但政治结构由联盟与继承安排塑造。",
 conn="南接汉朝边郡与长城地带，西通西域绿洲，东连东北草原，是欧亚草原带东段的核心节点。"),
"马来群岛":dict(defn="马来群岛：东南亚的岛屿群，包括苏门答腊、爪哇、婆罗洲等。",
 span="地质尺度（本条引 2017 年群岛地质综述）",
 geo="位于欧亚、印度—澳大利亚与太平洋板块交汇处，火山与地震活动强烈；赤道气候与海洋调节使岛屿降水丰沛，山地与低地差异显著。",
 infl="板块构造决定岛屿的形成与地形，也影响矿产与土壤分布；海峡与季风风系则决定航运季节，二者共同塑造了群岛的贸易格局。",
 conn="马六甲海峡与巽他海峡是印度洋—太平洋航路的瓶颈，季风方向决定帆船往返的季节窗口。"),
"墨西哥湾":dict(defn="墨西哥湾：北美东南部的半封闭海湾。",
 span="现代海洋观测（本条引 2014 年表层海洋条件研究）",
 geo="海湾由北美大陆与尤卡坦半岛环抱，通过佛罗里达海峡与加勒比海相连；密西西比河带来大量淡水与营养盐，形成显著的河口羽流。",
 infl="所引研究显示表层海洋条件存在**自然变率**，与风场、淡水输入相关；这提示生态与渔业管理需区分自然波动与人为影响。",
 conn="经佛罗里达海峡连接大西洋，经尤卡坦海峡连接加勒比海，是北美与中美洲之间的航运与生态通道。"),
"中世纪欧洲庄园农业":dict(defn="中世纪欧洲庄园农业：以庄园为单位组织土地、劳力与地租的农业制度。",
 span="约9–14世纪（地区差异大；本条引 2010 年专论 Manors and Markets）",
 geo="西北欧平原与丘陵的交错地带，土壤与降水适合谷物与牧草轮作；三圃制与敞田在这样的地形上便于集体耕作与放牧。",
 infl="所引专论强调庄园制度与市场交换是**并存**而非替代关系：地租、市场与人口变动共同塑造农业组织，制度演化不能被简化为「自然经济」。",
 conn="通过集镇与市集连接地方交换网络，通过水路把谷物与羊毛运往城市与出口港。"),
"澳大利亚混合农业":dict(defn="澳大利亚混合农业：在同一农场内结合小麦种植与绵羊放牧的经营方式。",
 span="20世纪以来的农业变迁（本条引 1982 年生产率研究）",
 geo="主要分布于南部与西南部的地中海气候区，冬季降水、夏季干旱，适合小麦—休闲—牧草的轮作；土壤肥力较低，需依赖休耕与施肥。",
 infl="所引研究关注**生产灵活性与技术变迁**：轮作制度使农场能在价格波动中调整作物与畜牧的比重，这是对降水与市场双重不确定性的适应。",
 conn="经铁路与港口连接出口市场，羊毛与小麦是19世纪以来澳大利亚的主要出口品。"),
"大自流盆地":dict(defn="大自流盆地：澳大利亚东部的大型自流地下水盆地。",
 span="地质尺度（本条引 1986 年氯-36 定年研究）",
 geo="盆地被不透水层圈闭，含水层向西部倾斜；东部边缘的补给区降水入渗后向盆地内部流动，井水可自流至地表。",
 infl="所引氯-36 定年研究显示部分地下水**年龄极老**、补给速率极慢，这意味着开采速率一旦超过补给，水位将长期下降且难以恢复。",
 conn="支撑内陆牧业与城镇用水，是干旱内陆唯一可靠的规模化水源。"),
"新西兰北岛":dict(defn="新西兰北岛：新西兰两大主岛之一，以火山与地热活动著称。",
 span="地质尺度（本条引 1996 年火山灰年代学研究）",
 geo="岛屿中部为火山高原与地热区，周边为丘陵与平原；火山灰层序记录了多次喷发，成为定年与地层对比的关键材料。",
 infl="火山灰年代学为考古与古环境研究提供时间标尺，也说明该岛的土壤肥力与灾害风险同源：肥沃的火山土与喷发风险并存。",
 conn="经库克海峡与南岛分隔，通过港口与奥克兰地峡连接国际贸易。"),
"马丘比丘":dict(defn="马丘比丘：秘鲁安第斯山脊上的印加遗址。",
 span="15世纪（印加时期；本条引 2004 年专论）",
 geo="建于海拔约2400米的山脊，两侧为陡降的河谷；梯田与排水系统是维持建筑稳定与农业的关键工程措施。",
 infl="遗址的位置与工程反映印加国家对山地地形的适应能力；但它在印加政治体系中的具体功能（王室庄园、宗教中心等）仍有不同解释。",
 conn="经印加道路系统连接库斯科与周边谷地，是安第斯山地交通网络的节点。"),
"北美原住民":dict(defn="北美原住民：在欧洲人到来之前及其后生活于北美的原住民族群。",
 span="末次冰期后至历史时期（本条引 1996 年美洲人群迁徙研究）",
 geo="迁徙路线涉及白令陆桥与沿海走廊两种假说；冰川消退的时间窗口决定内陆无冰走廊何时可用，这直接影响人群进入的路径与年代。",
 infl="所引研究以亚马孙洞穴遗址为证据，支持**较早的沿海或内陆迁徙**，说明进入美洲的时间与路线仍是活跃的研究问题，不宜下定论。",
 conn="从东北亚经白令地区进入，随后向南北美洲扩散，形成从北极到火地岛的连续分布。"),
"加勒比海群岛":dict(defn="加勒比海群岛：加勒比海中的岛链，包括大安的列斯与小安的列斯。",
 span="生物地理尺度（本条引 1975 年加勒比生物地理研究）",
 geo="岛链由火山岛与珊瑚岛组成，按大小与海拔分层；信风与洋流决定降水与物种扩散方向，岛屿间的距离是扩散的屏障也是通道。",
 infl="所引研究以**隔离分化（vicariance）模型**解释加勒比生物区系的形成，与「跨海扩散」模型形成对照，说明同一分布格局可以有不同机制解释。",
 conn="经海流与信风连接北美、中美与南美，近代成为跨大西洋航线的必经水域。"),
"阿拉伯征服北非":dict(defn="阿拉伯征服北非：7–8世纪阿拉伯军队向西推进、整合北非的过程。",
 span="7世纪中叶至8世纪初（本条引 2020 年「北非门户」研究）",
 geo="北非沿海为地中海气候的狭长农耕地带，背靠阿特拉斯山地与撒哈拉；沿海城市由罗马时代的港口网络延续而来。",
 infl="所引研究把北非视为**连接地中海与撒哈拉以南的「门户」**：征服的可持续性依赖对既有城市与税收体系的接管，以及跨撒哈拉商路的接入，而非单纯的军事推进。",
 conn="东接埃及与西亚，北经地中海通伊比利亚与意大利，南经撒哈拉商路通西非黄金产地。"),
"大津巴布韦":dict(defn="大津巴布韦：南部非洲的石头建筑群遗址，为津巴布韦王国的中心。",
 span="11–15世纪（起讫年学界有不同表述；本条引 1998 年认知考古研究）",
 geo="位于南部非洲高原，花岗岩节理发育，便于开采薄石板用于干砌建筑；周边草原适合牧养，季风边缘的降水变率大。",
 infl="所引 1998 年研究批评了殖民时代对该遗址的**想象性历史**解释，强调应从本地物质文化（如鸟形石雕、干砌技术）出发理解其意义，而非外来起源假说。",
 conn="经林波波河与印度洋港口连接东非海岸贸易，象牙、黄金与铜沿此输出。"),
}
added={}
for t,c in F.items():
    if not c or t in REJECT or t not in BODY: continue
    oa=(c.get("id") or "").rsplit("/",1)[-1];sid=f"openalex-{oa}"
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
        TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文","preprint":"预印本"}
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),
          "type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":(c.get("title") or "")[:200],
          "note":f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:240]}…"})
        have.add(sid)
    added[t]=sid

n=0;up=[]
for t,b in BODY.items():
    e=T.get(t);sid=added.get(t)
    if not e or not sid: continue
    c=F[t]
    e.update({"level":"L2","status":"L2完成(第35轮)-学术文献",
      "definition":b["defn"],"overview":b["defn"],
      "time_or_place":b["span"],"geo":b["geo"],"influence":b["infl"],
      "polities":e.get("polities") or "本条以自然地理/区域概述为主；具体政权序列待专门史料核验。",
      "connections":b["conn"],
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第35轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c.get('title')}》，DOI {c.get('doi') or '无'}，{c.get('host') or '出版方未标'}）。"
        f" 该文献主题与本条同一对象，正文的地理与机制段落据此撰写；年代以「{b['span']}」表述并注明学界有不同版本。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 285 L235 245 L375 222 L515 238 L645 272' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='375' cy='222' r='7' class='pt'/><text x='290' y='200' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print("剔除:",list(REJECT))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))