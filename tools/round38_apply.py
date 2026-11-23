# -*- coding: utf-8 -*-
"""第38轮：15 条补充条目 → L2（OpenAlex 学术来源 + 1 条世行指标）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round38_openalex.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文"}

BODY={
"赫梯王国":dict(span="约公元前17–前12世纪（赫梯古王国至帝国期；具体起讫年学界有不同表述）",
 defn="赫梯王国：安纳托利亚高原上的古代国家，以楔形文字档案与铁器技术著称。",
 geo="核心在安纳托利亚高原中部的哈图沙一带，高原干旱、河谷适合农业；四周山地提供木材与矿料，北向黑海、南向叙利亚的通道决定其对外方向。",
 infl="所引 2022 年专著《The Hittite Empire》讨论其国家形态：档案文书显示王权与条约体系并重，与埃及的卡叠什对峙是古代近东外交的典型案例。",
 conn="南经托罗斯山口通叙利亚与美索不达米亚，西接爱琴海沿岸（与迈锡尼世界有接触），北向黑海沿岸。"),
"仰韶文化":dict(span="约公元前5000–前3000年（仰韶文化；所引研究覆盖 7000–4000 BP）",
 defn="仰韶文化：中国新石器时代中期的考古文化，以彩陶与粟作农业为特征。",
 geo="核心在黄河中游（陕西、河南、山西）的黄土台地与河谷，黄土肥沃、易于耕作；气候较今温暖湿润，粟与黍是主要作物。",
 infl="所引 2001 年研究以陕西仰韶时期人骨的饮食与健康变化为线索，指出公元前第五千纪前后的气候波动之后进入较冷期，与聚落平等性的变化相伴随。这说明农业社会的社会结构与气候—生计条件相互关联，但非单一决定。",
 conn="沿黄河及其支流扩散至华北与西北，与长江中游的稻作文化区存在交流。"),
"西北海岸":dict(span="长期延续至历史时期（所引研究为民族志与考古综合）",
 defn="西北海岸：北美太平洋西北沿岸的原住民文化区，从阿拉斯加东南延伸至华盛顿州。",
 geo="海岸为峡湾与岛屿交错，冷温带雨林提供雪松与鲑鱼；海洋生产力高，河流的鲑鱼洄游形成季节性资源脉冲。",
 infl="所引 2013 年研究指出，该区域原住民**主动管理**陆域与海洋资源（如贝类床、火控促进资源植物），其管理实践嵌入复杂的社会经济网络。这修正了「采集者被动适应」的印象。",
 conn="沿岸航线连接南北，与内陆高原文化区通过河流与山口交换。"),
"新法兰西":dict(span="16–18世纪（新法兰西殖民地，1534–1763年）",
 defn="新法兰西：法国在北美东北部的殖民地，沿圣劳伦斯河与密西西比河流域展开。",
 geo="核心在圣劳伦斯河谷，水路直通五大湖；北方森林与毛皮资源是经济基础，河谷平原可耕作但生长季短。",
 infl="所引 2012 年研究以耶稣会《Relations》为对象，指出这些文本需放在**殖民地内部循环**（而非仅「冒险家的记述」）的语境中理解。这提示殖民文献本身是宣传与知识生产的工具，不能直接当作客观记录。",
 conn="经圣劳伦斯河口通大西洋，经五大湖与密西西比水系深入北美内陆，与英国殖民地及原住民诸族交织。"),
"巴塔哥尼亚":dict(span="区域地理与人群史（所引研究为古基因组）",
 defn="巴塔哥尼亚：南美洲南端的广大区域，以干旱草原、冰川与强风著称。",
 geo="安第斯山脉在西部，向东过渡为台地草原；西风带带来降水集中于山地，东侧处于雨影。南部为冰川区与峡湾。",
 infl="所引 2020 年研究以古基因组揭示南巴塔哥尼亚的人群历史，显示该区域人群的流动与替代过程比单一「沿海扩张」模型更复杂。这说明区域人群史需要多点证据，而非单一路线推断。",
 conn="北接潘帕斯草原，南隔麦哲伦海峡与火地岛相望，两侧分别为太平洋与大西洋。"),
"的的喀喀湖":dict(span="湖泊与区域文明（长期延续）",
 defn="的的喀喀湖：南美洲安第斯高原上的大型高原湖泊，位于秘鲁与玻利维亚交界。",
 geo="湖面海拔约3800米，面积大而水深；湖水调节局地温度，湖岸与岛屿在高寒环境中提供相对温和的小气候。周围为干旱高原。",
 infl="所引 2002 年研究以「水中的界线」为题，讨论湖泊如何同时作为资源、交通与**文化与政治边界**。这提示水域不仅提供生计，也参与社会边界的形成。",
 conn="经湖泊与高原道路连接秘鲁南部、玻利维亚与智利北部，是安第斯南部交换网络的中心。"),
"纳斯卡文化":dict(span="约公元前1世纪至公元8世纪（纳斯卡文化；所引研究为该区地质考古）",
 defn="纳斯卡文化：秘鲁南部沿海与内陆谷地的古代文化，以地画与精细陶器著称。",
 geo="位于阿塔卡马沙漠北缘的干旱谷地，河流的季节水量决定农业的可能；沙漠表面（pampa）覆盖石砾，地画即通过移除表层砾石形成。",
 infl="所引 2005 年研究以沙漠黄土与地貌分析建立该区环境演化的初步年代序列，说明景观本身在长期气候波动中变化——地画的「持久可见」依赖于极端干旱这一条件。",
 conn="经沿海航运与谷地间的陆路连接帕拉卡斯、伊卡与高地。"),
"奇穆帝国":dict(span="约公元900–1470年（奇穆国家；所引研究为水利工程）",
 defn="奇穆帝国：秘鲁北部沿海的古代国家，以大规模灌溉与土台都城昌昌著称。",
 geo="核心在莫切河谷下游的沿海荒漠，依赖安第斯融水的灌溉渠；地下水与河道比降决定渠线，沿海的海洋资源补充生计。",
 infl="所引 1982 年研究分析奇穆在奇卡马谷的水利工程，指出渠道的设计与维护需要跨谷的组织协调。这说明大规模灌溉可以成为权力集中的一个机制，而非仅仅是地理条件的产物。",
 conn="沿南北谷地构成的海岸走廊连接北部诸谷，与高地之间存在交换关系。"),
"玛雅研究新进展":dict(span="2010年代以来的 LiDAR 应用（所引 2020 年综述）",
 defn="玛雅研究新进展：2010年代起，机载 LiDAR 测绘对玛雅低地聚落认识的改写。",
 geo="玛雅低地（危地马拉佩滕、墨西哥坎佩切、伯利兹）为热带雨林覆盖的喀斯特台地，地面调查困难；LiDAR 可穿透林冠读出地形与建筑。",
 infl="所引 2020 年研究讨论 LiDAR 带来的认知突破，同时提出**伦理与新殖民主义**问题：数据的获取、所有权与对当地社区的返还。这说明技术进展与知识正义是同一议题的两面。",
 conn="与中美洲各地的聚落网络研究相连，并与当代考古数据治理的讨论挂钩。"),
"欧洲冰期地貌":dict(span="第四纪（约258万年以来；所引研究为冰川地貌数据库）",
 defn="欧洲冰期地貌：末次冰期及更早冰期在欧洲留下的地貌与沉积组合。",
 geo="斯堪的纳维亚冰盖与阿尔卑斯山地冰川分别塑造了不同的地貌：前者形成冰蚀湖、鼓丘与冰碛平原，后者形成冰斗、U 形谷与冰碛垄。",
 infl="所引 2004 年研究建立冰川地貌的**地图与 GIS 数据库**，把零散的野外观测整合为可比较的空间数据。这说明「地貌知识」本身也依赖数据组织方式。",
 conn="与北欧、阿尔卑斯与不列颠的第四纪研究相连，并为古气候重建提供地面证据。"),
"地图投影":dict(span="制图学基础（长期发展）",
 defn="地图投影：把球面（椭球面）坐标转换为平面坐标的数学方法。",
 geo="球面不可展为平面，任何投影都会在保形、保面积、保距离之间取舍；高纬度与全球尺度上的变形尤为显著。",
 infl="所引 2018 年研究讨论制图教学中投影的选择与讲解，指出学生常把投影视为技术细节而忽略其**表达后果**（面积、形状的失真会影响判断）。这说明「中性地图」不存在，投影本身是一种选择。",
 conn="与 GIS、坐标系统、面积统计（如森林与冰川面积）直接相关；不同投影会改变同一区域的多边形面积计算。"),
"地理空间数据产品":dict(span="技术现状（所引 2022 年工作流研究）",
 defn="地理空间数据产品：由原始观测加工而成、可直接用于分析的空间数据集。",
 geo="产品覆盖范围从全球栅格（高程、土地覆盖）到城市级三维数据；分辨率与覆盖范围往往成反比，全球产品在局部精度有限。",
 infl="所引 2022 年研究以 LiDAR 点云为例，提出高通量工作流把原始点云转为可分析的栅格产品（如冠层高度），这使大范围三维数据产品成为可能。这说明产品化的关键在流程与标准化，而非单次测量。",
 conn="与地球系统科学、环境数据访问、制图可视化相互依赖。"),
"地球系统科学":dict(span="学科框架（20世纪后期以来）",
 defn="地球系统科学：把大气、海洋、陆地、冰盖与生物作为相互作用的分系统来研究的框架。",
 geo="各分系统在不同尺度上耦合：如海冰—反照率—温度的正反馈、季风—植被—水循环的联动；空间上的差异决定耦合的强度。",
 infl="所引 2019 年研究讨论如何从时间序列**推断因果**，指出地球系统数据的高维、非线性与反馈使相关不等于因果，需专门方法（如收敛交叉映射）。这提醒把「趋势相关」当作机制是常见错误。",
 conn="与气候学、生态学、水文与经济系统相互嵌套，是当代全球变化研究的组织框架。"),
"环境数据访问":dict(span="数据基础设施现状（所引 2023 年平台论文）",
 defn="环境数据访问：研究者获取、共享与复用环境观测数据的渠道与制度。",
 geo="观测站点分布极不均：高收入国家的监测密度远高于非洲与南美部分地区，形成「数据地理」的不对称。",
 infl="所引 2023 年研究介绍 Ecodatacube 平台，把开放的遥感与气象数据预加工为「analysis-ready」立方体，降低使用门槛。这说明数据的可用性不止取决于有无，也取决于加工与接口。",
 conn="与地球系统科学、地理空间数据产品、农业与水资源的模型输入相关。"),
"人文地理学":dict(span="学科史（19世纪至今）",
 defn="人文地理学：研究人类活动空间组织与文化—环境关系的学科分支。",
 geo="研究对象覆盖聚落、经济、政治与文化景观；尺度从社区到全球，方法从田野到定量。",
 infl="所引 1987 年研究以法国某研究机构的学科建制为例，讨论人文地理学作为「新学科」的建立过程。这说明学科的边界与合法性并非自然生成，而由机构、期刊与人才培训共同确立（与「争议边界处理原则」中的 boundary work 概念相关但不同）。",
 conn="与经济学、社会学、生态学交叉，为区域研究与规划提供空间视角。"),
"气候与健康风险":dict(wb=("SH.DYN.MORT","5 岁以下儿童死亡率（每千活产）"),
 defn="气候与健康风险：气候变化通过热浪、病媒传播、粮食与水资源影响人群健康的途径与分布。",
 geo="风险分布与气候带、贫困水平和公共卫生能力叠加：热带与亚热带低收入地区的暴露与脆弱性同时较高。",
 infl="气候通过多条路径影响健康（直接伤害、病媒、食物与水的安全），其效应被卫生系统能力放大或削弱；单一指标只能反映结果的一部分。",
 conn="与营养状况、水资源、极端天气、贫困相互关联。"),
}
n=0;up=[]
for t,b in BODY.items():
    e=T.get(t)
    if not e: continue
    if "wb" in b:
        code,label=b["wb"];W=json.load(open(os.path.join(ROOT,"reports","round38_wb.json"),encoding="utf-8"))
        d=[x for x in W.values() if x["code"]==code]
        if not d: continue
        d=d[0];v=f"{float(d['value']):.1f}‰";yr=d["year"]
        sid="wb-wld-sh-dyn-mort"
        if sid not in have:
            u=f"https://api.worldbank.org/v2/country/WLD/indicator/{code}?format=json&per_page=100&date=2015:2025"
            c2=0;size=0
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);c2=int(cc.strip() or 0);size=len(bb)
            except Exception: pass
            sd["sources"].append({"id":sid,"title":f"World Bank API — {label} ({code}, 全球)","author":"World Bank","year":None,
              "type":"数据端点","url":u,"url2":None,"link_ok":bool(c2==200),"verified":bool(c2==200),
              "page_title":f"World Bank API — {code} (WLD)",
              "note":f"JSON API {c2}；WLD＋{code}；最新 {v}（{yr}年）。年度指标，随年度更新与历史修订变化。"})
            have.add(sid)
        e.update({"level":"L2","status":"L2完成(第38轮)-指标数据","definition":b["defn"],
          "overview":b["defn"]+" 本条以可核验的指标为数据基础。","time_or_place":f"全球口径（{yr}年数据）",
          "geo":b["geo"],"influence":b["infl"],"connections":b["conn"],
          "polities":e.get("polities") or "本条为全球主题条目，不展开具体政权序列。",
          "today":f"来源：世界银行 API（指标 {code}，{label}）：全球 {v}（{yr}年）。该值为全球合计或均值，掩盖国家与区域间的巨大差异。",
          "sources":list(dict.fromkeys((e.get("sources") or [])+[sid])),"needs_verification":True,
          "pending_notes":((e.get("pending_notes") or "")+f" 【第38轮升级 L2】数据来源 {sid}，实测 {v}（{yr}年）。").strip(),
          "last_update":TODAY})
    else:
        c=F.get(t)
        if not c: continue
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
            sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
              "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
              "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
              "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c.get("title") or "")[:200],
              "note":f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:220]}…"})
            have.add(sid)
        e.update({"level":"L2","status":"L2完成(第38轮)-学术文献",
          "definition":b["defn"],"overview":b["defn"],"time_or_place":b["span"],
          "geo":b["geo"],"influence":b["infl"],
          "polities":e.get("polities") or "本条不展开完整政权序列；具体世系与制度细节待专门史学来源核验。",
          "connections":b["conn"],"today":e.get("today") or "（本条的当代指标不在本页展开。）",
          "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),"needs_verification":True,
          "pending_notes":((e.get("pending_notes") or "")+
            f" 【第38轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c.get('title')}》，DOI {c.get('doi') or '无'}）。"
            f" 机制/影响段据其撰写，geo 为常识性地理描述（未挂学术来源）。").strip(),
          "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 280 L240 240 L380 220 L520 238 L645 272' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='380' cy='220' r='7' class='pt'/><text x='290' y='198' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))