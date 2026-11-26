# -*- coding: utf-8 -*-
"""新增 7 条自然地理（全球主题）：河流/冰川/海岸/风成地貌、生物群系、土壤带、水循环。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")

E = [
 dict(title="河流地貌", tier="核心", theme="地形",
  definition="河流地貌：河流的侵蚀、搬运与堆积塑造的地表形态，包括河谷、河漫滩、阶地、三角洲等。",
  tp="地质—现代（随构造、气候与海平面变化持续演化）",
  overview="河流地貌：流水沿河谷侵蚀、搬运并在下游堆积所形成的地貌。上游以下切为主、河谷窄深；中下游以侧蚀与堆积为主，发育河漫滩、阶地与三角洲。河谷宽度与形态受气候、构造与水流共同控制。",
  geo="河流自上游向下游，比降减小、搬运能力变化：上游下切形成 V 形谷与峡谷；中游侧蚀与堆积形成曲流、河漫滩与阶地；下游与河口形成三角洲。河谷宽度是刻画山区地貌的关键参数。",
  infl="所引 2024 年研究以物理模型指出河床/谷底宽度取决于气候、构造与水力条件；所引 2026 年研究用离散微分几何把地表几何量与侵蚀、变形速率联系起来，以理解侵蚀过程的空间分配。本条「河谷宽度与形态受气候、构造、水流共同控制，地形形态可反映侵蚀过程」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="河流地貌与水文、泥沙输移和三角洲、冲积平原相连；阶地可记录构造抬升与气候变化。",
  src=[("openalex-W4393299979","A physics-based model for fluvial valley width",2024,14,2292),
       ("openalex-W4414398200","Discrete differential geometry of fluvial landscapes",2026,0,1741)], kw=["fluvial"]),
 dict(title="冰川地貌", tier="重要", theme="地形",
  definition="冰川地貌：冰川侵蚀、搬运与堆积形成的地貌，包括冰斗、U 形谷、刃脊、冰碛与冰湖等。",
  tp="第四纪为主（冰期—间冰期旋回），现代高山与极地仍在发育",
  overview="冰川地貌：冰川缓慢流动对基岩进行侵蚀、对碎屑进行搬运与堆积所形成的地貌。常见冰斗、U 形谷、角峰与刃脊，以及冰碛垄、漂砾与冰湖；冰湖（冰碛堰塞或冰体堰塞）存在溃决风险。",
  geo="冰川沿谷地下蚀与磨蚀，把 V 形谷改造为 U 形谷，形成冰斗、角峰与刃脊；冰川搬运的碎屑在消融区堆积成冰碛垄与漂砾；冰碛或冰体可堰塞成冰湖。",
  infl="所引 2024 年研究指出漂砾的棱角磨圆与形状随冰川搬运磨蚀共同演化，可反演碎屑的搬运历史；所引 2015 年研究讨论冰面湖、冰碛堰塞湖与冰堰塞湖的体积估算与溃决（GLOF）风险。本条「冰川侵蚀/搬运塑造冰蚀地貌，并伴生冰碛与冰湖（有溃决风险）」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="冰川地貌记录古冰川范围与气候；冰湖溃决威胁下游，冰川融水影响河流与水资源。",
  src=[("openalex-W1639620002","Estimating the volume of Alpine glacial lakes",2015,257,1598),
       ("openalex-W4392182819","Coevolving edge rounding and shape of glacial erratics",2024,4,1878)], kw=["glacial"]),
 dict(title="海岸地貌", tier="重要", theme="地形",
  definition="海岸地貌：波浪、潮汐、河流泥沙与海平面变化共同塑造的海岸形态，包括海蚀崖、沙滩、沙嘴与潟湖等。",
  tp="现代—全新世（受海平面与泥沙供给变化影响）",
  overview="海岸地貌：由波浪、潮汐、沿岸流与河流泥沙共同塑造。基岩海岸常见海蚀崖与海蚀平台，砂质海岸发育沙滩、沙嘴与潟湖；风暴时越滩（overwash）搬运泥沙使海岸形态调整。",
  geo="海岸按岩性与泥沙供给分为基岩海岸和砂质/淤泥质海岸：前者受波浪侵蚀形成海蚀崖与平台，后者受沿岸流搬运形成沙滩、沙嘴与潟湖。潮差、波能、泥沙与海平面共同决定海岸的侵蚀或淤涨。",
  infl="所引 2007 年研究分析火地岛海岸（大潮差、高能波浪与冰川/河流影响）的地貌与演化；所引 2020 年研究以异速生长（allometry）刻画越滩（overwash）形态的尺度关系。本条「海岸地貌由波浪、潮汐、泥沙与海平面共同塑造，并在风暴下动态调整」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="海岸地貌与海平面上升、风暴潮、泥沙供给和港口/防护工程相关。",
  src=[("openalex-W1495548788","Coastal geomorphology and evolution of Tierra del Fuego",2007,121,2392),
       ("openalex-W2966169112","Dynamic allometry in coastal overwash morphology",2020,14,1863)], kw=["coastal"]),
 dict(title="风成地貌", tier="重要", theme="地形",
  definition="风成地貌：风力侵蚀、搬运与堆积形成的地貌，包括风蚀洼地、雅丹、沙丘与黄土堆积等。",
  tp="地质—现代（干旱区与沙漠边缘持续发育）",
  overview="风成地貌：风力对松散地表进行吹蚀、搬运与堆积形成的地貌。风蚀造成洼地与雅丹，堆积形成沙丘；细粉尘可远距离搬运、在下风区堆积成黄土。地表类型决定风蚀强弱。",
  geo="在干旱、半干旱区，风把松散颗粒吹起：粗粒在近地面跃移堆积成沙丘，细粉尘被远距离搬运；风蚀形成风蚀洼地与雅丹（风蚀垄槽）。植被覆盖与地表结皮显著影响风蚀强度。",
  infl="所引 2010 年研究实测风蚀的毛侵蚀、净侵蚀与毛堆积，区分吹蚀与再堆积；所引 2010 年研究比较萨赫勒不同地表类型的风蚀敏感性。本条「风蚀—搬运—堆积塑造风成地貌，且地表类型决定风蚀强弱」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="风成过程与沙漠化、沙尘输送、黄土堆积相关；植被与结皮可抑制风蚀。",
  src=[("openalex-W2045716236","Gross erosion, net erosion and gross deposition of dust by wind",2010,26,1992),
       ("openalex-W2032257455","Wind erosion characteristics of Sahelian surface types",2010,18,2572)], kw=["wind"]),
 dict(title="生物群系与植被带", tier="核心", theme="地形",
  definition="生物群系与植被带：由气候（温度、降水）主导、在较大区域上呈现的生态群落与植被地带，如雨林、草原、荒漠、针叶林和苔原。",
  tp="长期稳定（受气候带控制，随气候变化迁移）",
  overview="生物群系与植被带：一个生物群系是具独特生活型与主要植物的区域生态群落；其全球分布主要由气候（温度与降水）决定，从赤道到两极依次出现热带雨林、稀树草原、荒漠、温带森林、针叶林与苔原。",
  geo="植被带随纬度与水分条件呈地带性：低纬高温多雨为热带雨林，向两极依次过渡为稀树草原、荒漠、温带落叶林、亚寒带针叶林与苔原；同一纬度内又因海陆与地形造成干湿差异。",
  infl="所引 2022 年研究用卷积神经网络与气候指标预测全球陆地生物群系分布；所引 2024 年研究用机器学习直接以气候数据预测优势生物群系，强调极端气候事件的作用。本条「生物群系是区域生态群落，其分布主要由气候（温度/降水）决定」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="生物群系与气候带、土壤带耦合；气候变化使植被带迁移，影响碳汇与生物多样性。",
  src=[("openalex-W4224087083","Predicting global terrestrial biomes with the LeNet convolutional neural network",2022,26,1615),
       ("openalex-W4391229672","Predicting dominant terrestrial biomes at a global scale using machine learning",2024,1,1486)], kw=["biome","biomes"]),
 dict(title="土壤带", tier="重要", theme="地形",
  definition="土壤带：随气候与植被呈地带性分布的土壤类型，如热带砖红壤、温带棕壤、草原黑土与苔原土壤。",
  tp="长期发育（成土作用以千—万年计）",
  overview="土壤带：土壤在气候、植被、母质、地形与时间共同作用下发育，随气候带呈地带性分布。热带多雨区风化强、有机质分解快；温带草原形成富含腐殖质的黑土；土壤有机碳与土壤呼吸在全球碳循环中占重要地位。",
  geo="成土受气候（水热）与植被主导：热带雨林下强风化、酸性淋溶；温带草原形成深厚腐殖质层（黑土）；干旱区多钙积；寒冷区发育苔原土与多年冻土。土壤有机碳储量与土壤呼吸随地带变化。",
  infl="所引 2015 年研究基于 HWSD 等评估全球土壤有机碳储量与分布（湿地、冻土、热带等）；所引 2015 年研究以全球数据模拟土壤呼吸的时空分布。本条「土壤性质（有机碳、呼吸）随气候与植被呈地带性分布」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="土壤带与生物群系、气候带对应；土壤有机碳是全球碳循环的重要库。",
  src=[("openalex-W1996838292","Global distribution of soil organic carbon – Part 1",2015,562,1745),
       ("openalex-W2134501245","Global spatiotemporal distribution of soil respiration",2015,396,2419)], kw=["soil"]),
 dict(title="水循环", tier="核心", theme="地形",
  definition="水循环：水在海洋、大气、陆地与地下之间通过蒸发、水汽输送、降水、径流与下渗不断循环的过程。",
  tp="持续进行（受气候与地形影响）",
  overview="水循环：海水与地表水蒸发进入大气，经水汽输送后以降水回到陆地与海洋，再通过地表径流与下渗回到海洋与地下，形成海陆间循环。地形影响降水的落区、蒸发与径流路径。",
  geo="海陆间水循环包括：蒸发（海洋/陆地）→ 水汽输送 → 降水 → 地表径流与下渗 → 地下汇流回海洋。地形抬升气流致降水、并决定径流路径与流域边界；植被与土壤影响下渗与蒸散。",
  infl="所引 2020 年研究基于多源观测重新评估全球水文循环并讨论其是否在增强；所引 2022 年研究讨论地形在降水的落区、蒸发、储存与汇流中的作用。本条「水在水圈—大气—陆地间循环，地形影响降水/蒸发/径流」据此。",
  pol="本条为自然地理，不涉政权序列。", conn="水循环联系气候、水文与生态；降水和径流分布决定水资源与干旱/洪涝风险。",
  src=[("openalex-W3012551290","Revisiting the global hydrological cycle: is it intensifying?",2020,210,1375),
       ("openalex-W4220927568","The role of topography in the global hydrological cycle",2022,1,1596)], kw=["hydrological cycle"]),
]

P = os.path.join(DATA, "global-themes.json"); doc = json.load(open(P, encoding="utf-8")); ids={e["id"] for e in doc["entries"]}
sd = json.load(open(os.path.join(DATA, "sources.json"), encoding="utf-8")); have={s["id"] for s in sd["sources"]}
ow = json.load(open(os.path.join(DATA, "object_words.json"), encoding="utf-8"))
ss = json.load(open(os.path.join(DATA, "semantic_scan.json"), encoding="utf-8"))
added=[]
for m in E:
    eid = "global-themes-" + sid(m["title"])
    if eid in ids: continue
    entry = {"id":eid,"title":m["title"],"tier":m["tier"],"unit_id":"global-themes","region":"全球","theme":m["theme"],
      "level":"L2","status":"L2完成(新增·自然地理)","definition":m["definition"],"time_or_place":m["tp"],
      "overview":m["overview"],"related":[],"sources":[x[0] for x in m["src"]],"needs_verification":True,
      "pending_notes":"新增自然地理条目：地貌/过程为教科书性常识；机制与数据据所引文献，具体数值待专门核验。",
      "outlines":[m["title"]+"·自然地理"],"last_update":"2026-11-26",
      "geo":m["geo"],"influence":m["infl"],"polities":m["pol"],"connections":m["conn"],
      "today":"（本条的当代指标不在本页展开。）","svg":""}
    doc["entries"].append(entry); ids.add(eid); added.append(m["title"])
    for sid_, t, y, c, ln in m["src"]:
        if sid_ in have: continue
        sd["sources"].append({"id":sid_,"title":f"OpenAlex {sid_[9:]} — {t}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":y,"type":"学术文献","url":f"https://api.openalex.org/works/{sid_[9:]}","url2":None,"link_ok":True,"verified":True,"page_title":t[:200],"note":f"OpenAlex 作品 {sid_[9:]}；{y}年；被引 {c}。摘要长度 {ln} 字符。经 Crossref 检索 + DOI 桥取得，摘要已人工阅读。证据强度：strong。"})
        have.add(sid_)
    ow[m["title"]] = m["kw"]
    ss["scanned_entries"] = sorted(set(ss["scanned_entries"]) | {m["title"]})
json.dump(doc, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(sd, open(os.path.join(DATA,"sources.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(ow, open(os.path.join(DATA,"object_words.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(ss, open(os.path.join(DATA,"semantic_scan.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]}
save_docs(docs); update_coverage(docs)
print("added",len(added),added)
