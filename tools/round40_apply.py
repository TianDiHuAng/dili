# -*- coding: utf-8 -*-
"""第40轮：13 条补充条目 → L2（Crossref→OpenAlex DOI 桥获取的学术来源）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
B=json.load(open(os.path.join(ROOT,"reports","round40_bridge.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

BODY={
"沙漠化":dict(defn="沙漠化：干旱、半干旱与半湿润偏干地区的土地退化过程。",
 geo="干旱区分布在副热带高压带与雨影区，降水少且年际变率大；过度放牧、不合理灌溉与植被清除会加速退化，土壤盐渍化在灌溉农区尤为突出。",
 infl="所引 1998 年研究讨论全球变化对旱地生态系统的冲击：气候变率与土地利用叠加造成植被与土壤属性的退化，而退化程度受降水事件的大小与频次调控。这说明沙漠化是过程而非边界推移。",
 conn="与粮食安全、水资源、沙尘输送、生物多样性相关。"),
"城市热岛":dict(defn="城市热岛：城市区域气温高于周边乡村的现象。",
 geo="热岛强度在夜间与静风条件下最显著；城市规模、建成区密度、绿地与水体比例决定强度分布，高密度中心与裸露铺装区最强。",
 infl="所引 2005 年研究分析热岛强度对城市人口规模等的依赖关系，指出强度并非随城市规模线性增长，而受形态与气候背景调节。这说明「越大越热」的直觉需要条件限定。",
 conn="与能源消耗（制冷）、空气污染、居民健康、城市规划相关。"),
"生物多样性分布":dict(defn="生物多样性分布：物种丰富度与系统发育多样性在地理空间上的格局。",
 geo="多样性在热带最高、向极地递减；山地与岛屿因地形与隔离形成高特有性。海洋的多样性中心（珊瑚三角区）与陆地热点并不重合。",
 infl="所引 2021 年研究评估系统发育多样性的空间格局，指出其与物种丰富度格局并不一致，保护优先区的划定会因指标选择而改变。这说明「多样性」是一组指标而非单一量。",
 conn="与保护区体系、森林覆盖、气候带、岛屿生物地理相关。"),
"自然灾害风险":dict(defn="自然灾害风险：致灾因子、暴露度与脆弱性共同决定的潜在损失。",
 geo="风险高值出现在灾害频发且人口密集的地带：环太平洋火山地震带、季风洪泛平原、干旱区与海岸低地。暴露度与脆弱性共同放大致灾因子的后果。",
 infl="所引 2016 年研究讨论空间规划在自然灾害风险管理中的作用，主张把风险信息纳入土地利用决策。这说明风险不只由自然过程决定，规划与制度同样改变结果。",
 conn="与城市化、气候适应、贫困、基础设施相关。"),
"极端天气预警":dict(defn="极端天气预警：对可能造成损失的极端天气事件进行预测并向公众与部门发布警报的体系。",
 geo="预警的价值取决于事件的时空尺度与人口分布：热带气旋与暴雨需沿海与流域尺度的监测网，干旱则需季节尺度的预测。观测稀疏区（如非洲部分地区）预警能力受限。",
 infl="所引 2022 年研究以肯尼亚为例，检验区域气候模式与常用气象数据集对极端天气型的预测效力，指出**数据不完善**会直接限制预警质量。这说明预警能力的瓶颈常在观测与数据，而非仅模型。",
 conn="与气候与健康风险、农业气候风险、自然灾害风险相关。"),
"城市贫困":dict(defn="城市贫困：城市居民在收入、住房与服务可及性上的匮乏及其空间聚集。",
 geo="城市贫困常集中于非正式聚落、inner-city 衰退区与边缘地带；其空间分布与住房市场、就业可达性、基础设施覆盖相互作用。",
 infl="所引 2006 年研究讨论城市社会排斥的空间维度，指出贫困不只是收入不足，还包括空间上的隔离与服务获取的障碍。这说明城市贫困需用空间指标衡量。",
 conn="与城市化、非正规经济、健康与教育机会相关。"),
"可持续交通":dict(defn="可持续交通：在满足可达性需求的同时降低资源消耗与环境影响的交通系统。",
 geo="交通模式与密度、地形、城市形态相关：高密度城市适合公共交通与非机动车，低密度地区依赖小汽车，二者碳强度差异显著。",
 infl="所引 2015 年研究以共享汽车（car sharing）作为可持续交通政策的案例，指出车ownnership 下降与环境收益需要行为改变与技术手段并行。这说明单靠技术替代不足。",
 conn="与城市化、能源转型、碳排放、健康相关。"),
"火灾生态":dict(defn="火灾生态：火作为生态过程对植被、土壤与生物多样性的作用。",
 geo="火 regime 随气候与植被类型变化：地中海气候区与针叶林带火频繁，湿润热带雨林自然火少；干季长度与燃料连续性决定火险。",
 infl="所引 2014 年研究以树皮厚度与火 regime 的关系为例，说明植被性状与火频率共同演化——火既是干扰也是选择压力。这修正了「火纯属灾害」的看法。",
 conn="与森林覆盖变化、碳排放、土地利用、生物多样性相关。"),
"南极洲无农业的环境约束":dict(defn="南极洲无农业的环境约束：使南极不具备农业可能性的自然条件组合。",
 geo="南极大陆几乎全被冰盖覆盖，露岩区不足 1%；即使露岩区，生长期极短、土壤发育极弱（多为粗骨土）、降水以雪为主，缺乏可耕作土壤与稳定液态水。",
 infl="所引 2014 年研究描述南极陆地环境：极端低温、干旱（尽管冰多而可用水少）、强风与短生长季共同限制维管植物的分布，仅有两种维管植物见于南极半岛。这一环境组合使农业不可行。",
 conn="与冰盖、气候带、生物多样性（特有种与简单群落结构）相关。"),
"法蒂玛王朝":dict(span="909–1171年（法蒂玛哈里发国家）",
 defn="法蒂玛王朝：以伊斯玛仪派哈里发为统治者的北非—埃及政权，909–1171年。",
 geo="核心先在北非马格里布（今突尼斯一带），后移治开罗；尼罗河谷的灌溉农业与地中海—红海商路是财政基础。",
 infl="所引 2020 年研究以「建设哈里发国家」为题，讨论其建筑与城市工程如何在**建设与破坏**之间体现政权合法性。这说明纪念性建筑是政治表达的手段，而非仅是工程活动。",
 conn="西接马格里布与西西里，东经红海通也门与印度洋，北临地中海通拜占庭与意大利。"),
"非洲大湖地区":dict(defn="非洲大湖地区：东非裂谷带上的湖泊群及其周边区域，包括维多利亚湖、坦噶尼喀湖等。",
 geo="湖泊位于东非裂谷带的构造洼地，深度大、水体分层明显；周边高原降水较丰，农业与渔业支撑密集人口。湖泊之间的海拔与连通性差异极大。",
 infl="所引 2019 年研究比较该区域各湖的水文与物理湖沼学特征，指出**湖盆形态与深度**决定分层与混合方式，进而影响营养循环与渔业。这说明同一区域内的湖泊不能一概而论。",
 conn="经尼罗河、刚果河与赞比西河等水系连接外部，湖泊本身构成内河航运与渔业的中心。"),
"查文文化":dict(span="约公元前900–前200年（查文文化；所引研究讨论其权威演化）",
 defn="查文文化：安第斯中部的早期文化，以查文德万塔尔遗址与大型石构建筑著称。",
 geo="核心在安第斯中部的高山谷地（今秘鲁安卡什），海拔约3000米；河谷是南北与东西通道的交汇，石料与水源决定选址。",
 infl="所引 2004 年研究讨论查文德万塔尔**权威与权力的演化**，指出其仪式性建筑与外来物（如热带贝壳、黑曜石）的集中反映跨区域联系与地方权威的形成。这说明早期宗教中心同时是政治经济节点。",
 conn="连接沿海（获取贝壳与鱼类）与亚马逊东坡（获取羽毛与植物），是安第斯垂直交换网络的枢纽。"),
"南锥体":dict(defn="南锥体：南美洲南部的锥形区域，通常包括阿根廷、智利、乌拉圭，有时含巴拉圭与巴西南部。",
 geo="安第斯山脉在西缘，东侧为潘帕斯草原与巴塔哥尼亚台地；西风带使智利南部多雨、阿根廷侧干旱。气候自北向南由亚热带过渡到冷温带。",
 infl="所引 2022 年研究考察 1946–1960 年西班牙向该区域的战后移民，涉西班牙与阿根廷的移民协定、巴西1950年代初的经济繁荣等。这说明区域的人口构成受跨大西洋政策与经济的共同影响；本条仅以此为区域研究现状的一例，不作地理成因解释。",
 conn="东临大西洋、西临太平洋，南隔德雷克海峡与南极相望，是南美与南极之间的门户。"),
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
          "url":f"https://api.openalex.org/works/{oa}","url2":f"https://doi.org/{c['doi']}" if c.get("doi") else None,
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oa}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符，节录：{(c.get('abstract') or '')[:240]}…"})
        have.add(sid)
    e["level"]="L2";e["status"]="L2完成(第40轮)-学术文献"
    e["definition"]=b["defn"];e["overview"]=b["defn"]+" 机制/影响段据所引研究撰写，geo 为常识性地理描述（未挂学术来源）。"
    e["time_or_place"]=b.get("span","（本条为概念/主题条目，无单一时间跨度）")
    e["geo"]=b["geo"];e["influence"]=b["infl"];e["connections"]=b["conn"]
    e["polities"]=e.get("polities") or "本条为概念/区域主题条目，不展开具体政权序列。"
    e["today"]=e.get("today") or "（本条的当代指标不在本页展开。）"
    e["sources"]=list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"]))
    e["needs_verification"]=True
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第40轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}），经 Crossref→OpenAlex DOI 桥获取（当日 search 端点 429 限流）。"
      f" 【D081单源声明】britannica-regions/wikipedia-regions 为壳别名、s010-unesco-org 为 UNESCO Culture 首页，均不构成独立内容依据；本条实质为单源（OpenAlex）。").strip()
    e["last_update"]=TODAY
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 275 L235 238 L375 218 L515 236 L645 270' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='375' cy='218' r='7' class='pt'/><text x='275' y='196' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)

json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
save_docs(docs)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print("剔除5条：环境治理(移民治理)、南极特别保护区(苔藓)、争议边界(制图系列)、南美贸易(水资源)、古巴岛(艺术)")
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))