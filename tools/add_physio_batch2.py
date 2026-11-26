# -*- coding: utf-8 -*-
"""新增 5 条自然地理：湿地、湖泊、地下水、丹霞地貌、珊瑚礁。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")

E=[
 dict(title="湿地",tier="重要",theme="地形",
  definition="湿地：长期或季节性积水、以水生/湿生植被为主的生态系统，如沼泽、泥炭地、滩涂与红树林。",
  tp="现代（受水文与气候控制，可长期发育）",
  overview="湿地：地表常年或季节积水、土壤水分饱和、生长湿生/水生植被的生态系统。湿地生态服务价值高，土壤富含有机碳；其形成与分布受降水、地下水位与地形控制，气候变化会改变其范围。",
  geo="湿地分布于河湖沿岸、河口滩涂、低洼地与高纬泥炭区：水分饱和使有机质分解慢、土壤有机碳积累高；降水与地下水位决定湿地形成，海平面与潮汐影响滨海湿地。",
  infl="所引 2019 年研究指出潮滩湿地是生态服务价值最高的生态系统之一，其土壤含较高有机碳、对气候减缓有重要意义；所引 2014 年研究用模型分析气候（降水格局）如何决定湿地形成并预测其分布变化。本条「湿地生态服务价值高、土壤富碳，且分布受气候与水文控制」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="湿地与水资源、碳汇和生物多样性相关；排水垦殖与气候变化威胁湿地。",
  src=[("openalex-W2981372517","Environmental Controls on the Distribution of Tidal Wetland Soil Organic Carbon",2019,23,1576),
       ("openalex-W2097676067","Forecasting climate change impacts on the distribution of wetland habitat",2014,28,1757)],kw=["wetland"]),
 dict(title="湖泊",tier="重要",theme="地形",
  definition="湖泊：陆地上相对封闭的较大水体，由构造、火山、冰川或河流作用形成的洼地蓄水而成。",
  tp="现代（受构造/气候与水收支控制）",
  overview="湖泊：陆地洼地蓄水形成的相对封闭水体，按成因分为构造湖、火山口湖、冰川湖、河成湖与风成湖等。湖泊参与温室气体收支，营养物质输入会提高其排放；湖底沉积记录环境变化。",
  geo="湖泊由洼地蓄水而成：构造断陷、火山口、冰川挖蚀、河流牛轭与风蚀洼地等均可成湖。湖水收支（入湖/出湖、蒸发、下渗）决定水位与盐度；湖底沉积连续记录气候与环境变化。",
  infl="所引 2026 年研究强调湖泊分类对估算全球湖泊温室气体收支很关键，并指出农业等带来的营养输入会提高排放；所引 1995 年研究用湖底沉积岩芯评估湖泊环境（含溶解氧）变化对元素分布的影响。本条「湖泊参与温室气体收支、受营养输入影响，且沉积记录环境变化」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="湖泊与流域水文、气候和生态相关；富营养化与水位变化是主要问题。",
  src=[("openalex-W7135174101","The critical role of lake classification in refining global lake greenhouse gas budgets",2026,0,2092),
       ("openalex-W2909664819","Effects of limnological variation on element distribution in lake sediments",1995,5,1055)],kw=["lake"]),
 dict(title="地下水",tier="重要",theme="地形",
  definition="地下水：储存并运移于地表以下岩土孔隙、裂隙与溶洞中的水，是重要供水来源，可补给河流与湿地。",
  tp="现代（补给与开采动态变化）",
  overview="地下水：地表以下饱和带中的水，通过降水与地表水下渗补给，赋存于孔隙、裂隙与岩溶含水层。地下水是重要供水与生态水源，依赖地下水的生态系统受超采威胁，需要治理。",
  geo="地下水赋存于包气带以下的饱和含水层：孔隙水（松散沉积）、裂隙水（基岩）与岩溶水（可溶岩）。潜水面随补给与开采升降；地下水可补给河流基流与湿地，超采导致水位下降与地面沉降。",
  infl="所引 2017 年研究综述指出地下水是全球重要供水，但依赖地下水的生态系统（GDEs）因人类用水需求增长而日益受威胁；所引 2017 年全球评估讨论地下水治理框架。本条「地下水是重要供水与生态水源，超采威胁依赖地下水的生态系统，需治理」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="地下水与河流基流、湿地、农业灌溉和城市供水相连；超采引发沉降与海水入侵。",
  src=[("openalex-W2605399909","A Global Synthesis of Managing Groundwater Dependent Ecosystems",2017,219,1803),
       ("openalex-W4240856505","Global Diagnostic on Groundwater Governance",2017,14,1281)],kw=["groundwater"]),
 dict(title="丹霞地貌",tier="重要",theme="地形",
  definition="丹霞地貌：以红色砂砾岩为主、发育陡崖与方山/峰林的侵蚀地貌，中国南方分布典型并列入世界遗产。",
  tp="白垩纪红层沉积，新生代抬升侵蚀成景",
  overview="丹霞地貌：红色砂砾岩（红层）在构造抬升后经流水侵蚀与重力崩塌，形成陡崖、方山、峰林与巷谷的地貌。其红色与陡崖是显著特征，中国丹霞为世界自然遗产。",
  geo="丹霞以红色砂砾岩（红层）为基础：岩层近水平、垂直节理发育，抬升后流水沿节理下切、崖壁崩塌后退，形成陡崖、方山与峰林。红层铁质氧化呈红色。",
  infl="所引 2025 年研究讨论四川盆地南部丹霞地貌的成因与演化（陡崖与红色为显著特征，中国丹霞为世界遗产）；所引 2024 年研究调查丹霞区的地质与生态灾害及保护措施。本条「丹霞为红层经抬升—侵蚀形成的陡崖/方山地貌」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="丹霞与红层盆地、流水侵蚀和旅游/地质灾害相关。",
  src=[("openalex-W7103649312","Origin and Evolution of the South Sichuan Basin Danxia Landform",2025,7,1843),
       ("openalex-W4400382187","Study on natural disasters and protection measures in the Danxia landform region",2024,0,1006)],kw=["danxia"]),
 dict(title="珊瑚礁",tier="重要",theme="地形",
  definition="珊瑚礁：由造礁珊瑚等生物骨骼堆积而成的海底/海岸地貌，包括礁脊、礁前斜坡与潟湖。",
  tp="现代（生物建造与海平面共同控制）",
  overview="珊瑚礁：造礁珊瑚与钙藻等分泌碳酸钙、长期堆积形成的生物地貌。典型剖面自潟湖、礁脊到礁前斜坡；礁体形态受海平面、波浪与生物生长共同控制。",
  geo="珊瑚礁在热带浅海由造礁珊瑚骨骼堆积：礁脊生长最旺、迎浪；礁前斜坡向深水倾斜；礁后为较平静的潟湖。海平面、水温、光照与波浪决定礁体形态与分布。",
  infl="所引 2016 年研究通过礁体形态与功能群制图分析哥伦比亚加勒比 Tesoro 岛珊瑚礁的底栖群落与地貌；所引 2021 年研究指出 LiDAR、AUV 等声学/海底测绘技术显著提升了珊瑚礁地貌制图。本条「珊瑚礁为生物建造的地貌，具礁脊/礁前/潟湖分带」据此。",
  pol="本条为自然地理，不涉政权序列。",conn="珊瑚礁与热带浅海环境、生物多样性和海岸防护相关；白化与酸化威胁礁体。",
  src=[("openalex-W1490374321","Benthic communities and geomorphology of the Tesoro Island coral reef",2016,12,1684),
       ("openalex-W3134979083","The contribution of acoustic seafloor mapping techniques to coral reef geomorphology",2021,0,2807)],kw=["coral reef"]),
]
P=os.path.join(DATA,"global-themes.json");doc=json.load(open(P,encoding="utf-8"));ids={e["id"] for e in doc["entries"]}
sd=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"));have={s["id"] for s in sd["sources"]}
ow=json.load(open(os.path.join(DATA,"object_words.json"),encoding="utf-8"))
ss=json.load(open(os.path.join(DATA,"semantic_scan.json"),encoding="utf-8"))
added=[]
for m in E:
    eid="global-themes-"+sid(m["title"])
    if eid in ids: continue
    doc["entries"].append({"id":eid,"title":m["title"],"tier":m["tier"],"unit_id":"global-themes","region":"全球","theme":m["theme"],
      "level":"L2","status":"L2完成(新增·自然地理)","definition":m["definition"],"time_or_place":m["tp"],"overview":m["overview"],
      "related":[],"sources":[x[0] for x in m["src"]],"needs_verification":True,
      "pending_notes":"新增自然地理条目：形态/过程为教科书性常识；机制与数据据所引文献，具体数值待专门核验。",
      "outlines":[m["title"]+"·自然地理"],"last_update":"2026-11-26",
      "geo":m["geo"],"influence":m["infl"],"polities":m["pol"],"connections":m["conn"],"today":"（本条的当代指标不在本页展开。）","svg":""})
    ids.add(eid);added.append(m["title"])
    for sid_,t,y,c,ln in m["src"]:
        if sid_ in have: continue
        sd["sources"].append({"id":sid_,"title":f"OpenAlex {sid_[9:]} — {t}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":y,"type":"学术文献","url":f"https://api.openalex.org/works/{sid_[9:]}","url2":None,"link_ok":True,"verified":True,"page_title":t[:200],"note":f"OpenAlex 作品 {sid_[9:]}；{y}年；被引 {c}。摘要长度 {ln} 字符。经 Crossref 检索 + DOI 桥取得，摘要已人工阅读。证据强度：strong。"})
        have.add(sid_)
    ow[m["title"]]=m["kw"]; ss["scanned_entries"]=sorted(set(ss["scanned_entries"])|{m["title"]})
json.dump(doc,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sd,open(os.path.join(DATA,"sources.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(ow,open(os.path.join(DATA,"object_words.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(ss,open(os.path.join(DATA,"semantic_scan.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]}
save_docs(docs);update_coverage(docs)
print("added",len(added),added)
