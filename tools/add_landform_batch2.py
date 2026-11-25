# -*- coding: utf-8 -*-
"""批量新增 11 条中国地貌：类型化彩绘剖面 + NE 真实地图定位 + 2 篇对题来源。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, save_docs, update_coverage
import ne
from locator import map_svg
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")
CHINA_BB = (60, 146, 10, 58)

def L(x,y,s,c="lbl"): return f"<text x='{x}' y='{y}' class='{c}'>{s}</text>"
def P(pts,fill,stroke="#8a7452",op=None,sw=1.2):
    o=f" fill-opacity='{op}'" if op else ""
    return f"<polygon points='{pts}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{o}/>"
def R(x,y,w,h,fill,stroke="#8a7452",op=None):
    o=f" fill-opacity='{op}'" if op else ""
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{fill}' stroke='{stroke}'{o}/>"

def sch_basin(e):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>",
       "<rect x='21' y='21' width='858' height='90' fill='#eef3f6' opacity='.4'/>"]
    s.append(P("40,300 40,180 200,180 300,300 600,300 700,180 860,180 860,300","#c9b48c","#8a7452"))
    s.append(R(300,300,300,70,"#8f8a80","#5f5a52"))
    s.append(R(300,300,300,16,"#dcd2c0","#a08a5f"))
    s.append(L(330,342,"稳定基底",c="lbl-s")+L(90,214,"盆缘山地",c="lbl-s")+L(720,214,"盆缘山地",c="lbl-s"))
    s.append(L(360,238,"盆内充填（沉积盖层）",c="lbl-s"))
    s.append(f"<path d='M40 300 H860' stroke='#5b93b8' stroke-width='0'/>")
    s.append(L(40,430,"盆地剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def sch_plain(e, river=True):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>",
       "<rect x='21' y='21' width='858' height='80' fill='#eef3f6' opacity='.4'/>"]
    s.append(R(40,300,820,90,"#cbb98a","#a08a5f"))
    s.append(R(40,300,820,26,"#d9c9a6","#a08a5f",op=".9"))
    s.append("<g stroke='#8aa66a' stroke-width='1.3'>"+"".join(f"<path d='M{110+i*80} 320 v64'/>" for i in range(10))+"</g>")
    if river:
        s.append("<path d='M40 352 C300 344 600 366 860 348' fill='none' stroke='#5b93b8' stroke-width='5'/>"+L(600,338,"河流/灌渠",c="lbl-s"))
    s.append(L(90,292,"冲积层（河湖相沉积）",c="lbl-s")+L(90,410,"耕地/平原面",c="lbl-s"))
    s.append(L(40,430,"平原剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def sch_delta(e):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>"]
    s.append(R(40,300,520,90,"#cbb98a","#a08a5f"))
    s.append(P("560,300 860,300 860,390 620,390","#a9cbe0","#6f9db8",op=".9"))
    s.append("<path d='M60 340 C260 336 420 342 560 338' fill='none' stroke='#5b93b8' stroke-width='6'/>")
    for dy in (320,350,375):
        s.append(f"<path d='M560 338 C650 33{dy%10} 740 {dy} 860 {dy}' fill='none' stroke='#5b93b8' stroke-width='3'/>")
    s.append(L(80,292,"三角洲平原",c="lbl-s")+L(690,330,"分流河道",c="lbl-s")+L(760,410,"海（河口湾）",c="lbl-s"))
    s.append(L(40,430,"三角洲剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def sch_range(e, parallel=False):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>",
       "<rect x='21' y='21' width='858' height='80' fill='#eef3f6' opacity='.4'/>"]
    if parallel:
        s.append(P("40,360 150,180 240,240 340,150 440,240 540,170 640,250 740,190 860,360","#9fb2c8","#5c6d84"))
        for x in (240,440,640):
            s.append(f"<path d='M{x} 250 L{x-30} 360 L{x+30} 360 Z' fill='#cfd6cd' stroke='#5c6d84'/>")
        s.append(L(150,168,"平行岭谷（V 形谷）",c="lbl-s"))
    else:
        s.append(P("40,360 160,150 260,230 360,120 470,240 580,150 700,250 860,360","#b7a58c","#7a6a55"))
    s.append(P("330,150 360,120 395,152","#ffffff","#c3d3d9"))
    s.append(L(345,146,"雪线/高峰",c="lbl-s"))
    s.append(R(40,360,820,60,"#cbb98a","#a08a5f"))
    if not parallel:
        s.append("<path d='M60 400 C300 390 600 408 840 392' fill='none' stroke='#5b93b8' stroke-width='3'/>")
    s.append(L(60,410,"山前冲积/山麓带",c="lbl-s"))
    s.append(L(40,430,"山脉剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def sch_hills(e):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>",
       "<rect x='21' y='21' width='858' height='80' fill='#eef3f6' opacity='.4'/>"]
    s.append("<path d='M40 340 C120 270 200 300 280 260 C360 220 440 300 520 250 C600 200 700 300 780 250 C820 226 850 250 860 240 L860 340 Z' fill='#c9d6b0' stroke='#6f8a4a'/>")
    s.append(R(40,340,820,50,"#c08a5a","#8a5636"))
    s.append(R(40,356,820,10,"#b06b3a","#8a5636"))
    s.append(L(90,330,"红壤丘陵（缓丘起伏）",c="lbl-s")+L(90,402,"土层：红壤/富铁铝",c="lbl-s"))
    s.append(L(620,232,"侵蚀/梯田",c="lbl-s"))
    s.append(L(40,430,"丘陵剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def sch_line(e):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>"]
    s.append(R(40,300,380,90,"#e4cf94","#b99b4e"))  # 北：旱作/平原
    s.append(R(420,300,440,90,"#c9d6b0","#6f8a4a")) # 南：水田/丘陵
    s.append("<path d='M420 180 L420 390' stroke='#c0392b' stroke-width='2' stroke-dasharray='8 6'/>")
    s.append(L(300,190,"秦岭—淮河一线",c="lbl"))
    s.append(L(70,360,"北：温带、旱作（小麦），冬季结冰",c="lbl-s"))
    s.append(L(450,360,"南：亚热带、水田（水稻），湿润",c="lbl-s"))
    s.append(P("120,300 220,230 320,300","#b7a58c","#7a6a55"))
    s.append(L(120,220,"秦岭（东西向山地）",c="lbl-s"))
    s.append(L(40,430,"南北分界剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def sch_corridor(e):
    s=["<rect x='20' y='20' width='860' height='420' rx='10' fill='none' stroke='var(--line)'/>",
       "<rect x='21' y='21' width='858' height='80' fill='#eef3f6' opacity='.4'/>"]
    s.append(P("40,340 40,170 220,170 300,250 320,340","#9fb2c8","#5c6d84"))   # 北山
    s.append(P("520,340 540,250 620,170 860,170 860,340","#b0a08a","#7a6a55"))  # 南山（祁连）
    s.append(R(320,290,200,50,"#cbb98a","#a08a5f"))
    s.append("<path d='M330 320 C400 312 470 320 540 314' fill='none' stroke='#5b93b8' stroke-width='3'/>")
    for cx in (360,430,500):
        s.append(f"<circle cx='{cx}' cy='312' r='4' fill='#6f9a5a'/>")
    s.append(L(60,160,"北山/戈壁",c="lbl-s")+L(640,160,"祁连山（南）",c="lbl-s"))
    s.append(L(330,282,"走廊·绿洲串珠（沿河）",c="lbl-s"))
    s.append(L(40,430,"走廊剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

SCHEMA = {
 "准噶尔盆地":(sch_basin,(87,45)),"东北平原":(sch_plain,(125,45.5)),"华北平原":(sch_plain,(116.5,35.5)),
 "长江中下游平原":(sch_plain,(117,30.5)),"珠江三角洲":(sch_delta,(113.5,22.5)),
 "秦岭—淮河一线":(sch_line,(108,33.3)),"东南丘陵":(sch_hills,(118,26.5)),"河西走廊":(sch_corridor,(100,39.5)),
 "柴达木盆地":(sch_basin,(95,37.3)),"天山山脉":(sch_range,(84,42.5)),"横断山脉":(lambda e: sch_range(e,parallel=True),(99,28)),
}

def combine(inner, lon, lat, title):
    ov = ne.overlay((30,34,840,196), CHINA_BB, title)
    loc = map_svg((30,34,840,196), CHINA_BB, lon, lat, label=title, overlay=ov)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760' role='img' aria-label='位置图与剖面示意图'>"
            + loc + "<g transform='translate(0,258)'>" + inner + "</g></svg>")

# 元数据：title -> 字段 + 两来源
META = {
"准噶尔盆地":dict(tier="重要",theme="地形",coord=(87,45),
 defi="准噶尔盆地：天山以北、阿尔泰山以南的大型内陆盆地，位于中国新疆北部，盆内多戈壁与沙漠。",
 tp="古生代以来（晚古生代为板块汇聚带，中新生代成盆）",
 ov="准噶尔盆地：中国新疆北部、天山与阿尔泰山之间的内陆盆地。盆地北西侧为西准噶尔古生代褶皱带，内部充填中新生代沉积，中央有古尔班通古特沙漠。",
 geo="位于天山以北、阿尔泰山以南，是中国第二大内陆盆地。北西缘的西准噶尔为海西期褶皱带，处于西伯利亚、塔里木、哈萨克斯坦三大板块的晚古生代汇聚带；盆内充填中新生代沉积，中央为古尔班通古特沙漠。",
 infl="所引 1989 年研究指出西准噶尔是海西期褶皱带，位于西伯利亚、塔里木与哈萨克斯坦三大板块之间的晚古生代汇聚带；另一 1989 年同位素研究厘定了该褶皱带的构造演化时序与花岗岩成因。本条「准噶尔盆地北西缘为古生代板块汇聚带改造而成」据此。",
 pol="本条以自然地理与构造为主，不展开政权序列；历史游牧政权年代待专门来源核验。",
 conn="盆地四周山地提供冰雪融水，山前绿洲与内部戈壁沙漠对照；向西有阿拉山口等通道，是北疆交通与气候通道。",
 src=[("openalex-W2079767098","Tectonic evolution of the West Junggar Region, Xinjiang, China",1989,269,3257),
      ("openalex-W1992832689","Isotopic studies bearing on the tectonics of the West Junggar Region",1989,143,1217)],
 kw=["junggar"], rel=["asia-"+""]),
"东北平原":dict(tier="重要",theme="地形",coord=(125,45.5),
 defi="东北平原：中国东北由松嫩平原、辽河平原与三江平原等组成的最大平原，黑土广布、农业发达。",
 tp="中新生代以来（松辽盆地等断陷—坳陷，第四纪冲积成平原）",
 ov="东北平原：中国面积最大的平原，由松嫩平原、辽河平原和三江平原等组成，土层深厚（黑土），是中国重要商品粮基地。",
 geo="位于大兴安岭、小兴安岭与长白山之间，由松嫩、辽河、三江等平原组成；地势低平、土层深厚（黑土），湿地与耕地交错，是中国最大平原与商品粮基地。",
 infl="所引 2018 年研究指出三江平原近数十年以农业开垦为主要土地利用变化驱动力，湿地被大量开垦；所引 2023 年研究分析松嫩平原春玉米干旱的时空特征。本条「平原以农业开垦为主导、黑土与湿地资源突出、面临干旱风险」据此。",
 pol="本条以自然地理与农业为主，不展开政权序列；开发史年代待专门来源核验。",
 conn="黑土与湿地是核心资源；农业开垦改变湿地与景观格局，干旱与水资源是主要约束。",
 src=[("openalex-W2897721456","Land Use and Landscape Pattern Changes in the Sanjiang Plain, Northeast China",2018,18,1479),
      ("openalex-W4366772016","Spatial-Temporal Characteristics of Spring Maize Drought in Songnen Plain, Northeast China",2023,14,1413)],
 kw=["songliao","sanjiang","songnen","northeast china"], rel=[]),
"华北平原":dict(tier="重要",theme="地形",coord=(116.5,35.5),
 defi="华北平原：黄河、海河、淮河等冲积而成的中国第二大平原，地势低平、地下水超采问题突出。",
 tp="第四纪以来（河流冲积为主）",
 ov="华北平原：由黄河、海河、淮河等河流冲积形成的中国第二大平原，地势低平、耕地密集；地下水是主要供水来源，长期超采导致水位下降。",
 geo="由黄河、海河、淮河等冲积形成，地势低平、沉积层深厚，耕地密集；地表水不足，地下水为主要供水来源。",
 infl="所引 2013 年研究指出华北平原地下水是主要供水来源，大规模超采使地下水位下降并产生严重环境与生态影响；所引 2022 年研究用 GRACE 卫星监测该区地下水储量变化。本条「以地下水为主要供水、超采导致水位下降」据此。",
 pol="本条以自然地理与水文为主，不展开政权序列；开发史年代待专门来源核验。",
 conn="黄河等河流冲积造就平原与耕地；地下水超采与地面沉降、海水入侵等环境问题相连。",
 src=[("openalex-W1998321165","Characteristics of Groundwater Recharge on the North China Plain",2013,40,956),
      ("openalex-W4295350356","Using GRACE to Detect Groundwater Variation in North China Plain",2022,22,1847)],
 kw=["north china plain"], rel=[]),
"长江中下游平原":dict(tier="重要",theme="地形",coord=(117,30.5),
 defi="长江中下游平原：长江出三峡后沿江展开的冲积平原，湖泊密布、水网稠密。",
 tp="第四纪以来（河湖冲积）",
 ov="长江中下游平原：长江出三峡后形成的冲积平原，地势低平、湖泊与河网密布，是重要的农业与人口密集区。",
 geo="长江出三峡后沿江展开，地势低平、河网与湖泊（如洞庭、鄱阳等）密布；沉积以河湖相为主，汛期洪水与湖泊调蓄是核心水文特征。",
 infl="所引 2022 年研究分析该区连通湖泊中浮游植物群落的地理格局与驱动；所引 2024 年研究以热收支方程解析该区极端热浪的热力特征。本条「平原以河湖密布、水网稠密为特征，并面临高温热浪等气候风险」据此。",
 pol="本条以自然地理与水文为主，不展开政权序列；开发史年代待专门来源核验。",
 conn="湖泊调蓄与河网连通影响防洪与生态；农业、航运与城市沿江分布。",
 src=[("openalex-W4283764848","Geographic pattern of phytoplankton community and their drivers in lakes of the middle-lower Yangtze",2022,26,2032),
      ("openalex-W4391823149","Thermodynamic characteristics of extreme heat waves over the middle and lower reaches of the Yangtze River basin",2024,38,1617)],
 kw=["yangtze"], rel=[]),
"珠江三角洲":dict(tier="重要",theme="地形",coord=(113.5,22.5),
 defi="珠江三角洲：珠江在河口湾充填形成的复合三角洲，河网密布、地势低平，是中国重要经济区。",
 tp="全新世以来（河口湾充填、海陆相互作用）",
 ov="珠江三角洲：珠江口由河流—海洋相互作用充填形成的复合三角洲，河网密布、地势低平，是中国人口与经济高度密集的地区之一。",
 geo="位于珠江口，由西江、北江、东江等带来的泥沙在河口湾充填形成，属多岛断陷盆地背景下的复合三角洲；地势低平、河网与汊道密布，受潮汐与径流共同作用。",
 infl="所引 2023 年研究指出珠江三角洲是在多岛断陷盆地中、由区域构造、第四纪海平面波动与河流—海洋相互作用共同塑造的复合三角洲，并以等深线刻画其全新世演化；所引 2010 年研究讨论泛珠三角的区域合作。本条「三角洲由河海相互作用充填形成、且为高度一体化经济区」据此。",
 pol="本条以自然地理与经济区为主，不展开政权序列；开发史年代待专门来源核验。",
 conn="河网与港口支撑密集的城镇与制造业；地面沉降、咸潮上溯与防洪是主要环境约束。",
 src=[("openalex-W4387659191","Holocene Evolution of the Pearl River Delta: Mapping Integral Isobaths and Delta Progradation",2023,22,1568),
      ("openalex-W2475391560","Political Economy of Regional Cooperation in the Pan-Pearl River Delta",2010,15,477)],
 kw=["pearl river delta"], rel=[]),
"秦岭—淮河一线":dict(tier="重要",theme="地形",coord=(108,33.3),
 defi="秦岭—淮河一线：中国东部重要的南北地理分界，大致对应 1 月 0℃ 等温线与 800 毫米年等降水量线。",
 tp="地理分界（现代气候—地貌界线，非单一地质事件）",
 ov="秦岭—淮河一线：中国东部重要的南北分界，北侧为温带、旱作与冬季结冰，南侧为亚热带、水田与湿润区，常被视为暖温带与亚热带、湿润与半湿润的分界。",
 geo="秦岭东西横亘于中国中部，与淮河共同构成南北过渡带：北侧温带、旱作（小麦）、冬季河流结冰；南侧亚热带、水田（水稻）、降水更丰。该线大致对应 1 月 0℃ 等温线与 800mm 年等降水量线。",
 infl="所引 2022 年研究把秦岭—大巴山视为中国南北过渡带，分析其植被动态对气候变暖的响应；所引 2025 年研究分析秦岭这一气候敏感区景观生态对气候变化的响应。本条「秦岭—淮河一线是中国南北气候与植被的重要过渡带」据此。",
 pol="本条为地理分界说明，不涉政权序列。",
 conn="分界南北影响农业类型（旱作/水田）、作物熟制与水文（结冰与否）；也是生态与气候研究的敏感带。",
 src=[("openalex-W4293532135","Vegetation Dynamics in the Qinling-Daba Mountains through Climate Warming",2022,16,1793),
      ("openalex-W4410118893","Climate Change-Driven Spatiotemporal Dynamics of Landscape Ecological in the Qinling Mountains",2025,6,1124)],
 kw=["qinling"], rel=[]),
"东南丘陵":dict(tier="补充",theme="地形",coord=(118,26.5),
 defi="东南丘陵：中国东南部的低山丘陵区，红壤广布、水热丰沛，水土流失与红壤退化较突出。",
 tp="中生代以来（岩浆岩与红壤化，现代侵蚀活跃）",
 ov="东南丘陵：中国东南部以低山丘陵为主的地貌区，红壤广布、降水丰沛，坡地开垦后水土流失与红壤退化问题突出。",
 geo="中国东南部低山丘陵连绵、起伏和缓，红壤（富铁铝）广布，降水丰沛且集中；坡地开垦与降雨侵蚀导致水土流失与红壤退化。",
 infl="所引 2019 年研究以江西为代表分析南方丘陵红壤区土壤侵蚀变化中的人为影响；所引 2023 年研究评估不同耕作方式对红壤稳定性和可蚀性的影响。本条「红壤丘陵在降雨与人为扰动下水土流失突出」据此。",
 pol="本条以自然地理为主，不展开政权序列；开发史年代待专门来源核验。",
 conn="红壤酸性、易蚀；水土保持（梯田、退耕、植被恢复）是区域治理关键。",
 src=[("openalex-W2947473094","Identifying Human-Induced Spatial Differences of Soil Erosion Change in a Hilly Red Soil Region",2019,14,1404),
      ("openalex-W4382728222","Effects of Different Tillage Practices on Soil Stability and Erodibility for Red Soil",2023,29,1650)],
 kw=["hilly red soil","red soil","southeast china"], rel=[]),
"河西走廊":dict(tier="重要",theme="地形",coord=(100,39.5),
 defi="河西走廊：青藏高原东北缘、祁连山以北的狭长走廊式前陆盆地，靠祁连山冰雪融水串起绿洲。",
 tp="新生代以来（前陆盆地，现代仍在活动）",
 ov="河西走廊：位于青藏高原东北缘、祁连山以北的狭长走廊，是新生代前陆盆地系统；靠祁连山冰雪融水形成串珠状绿洲，是古丝绸之路要道。",
 geo="青藏高原东北缘、祁连山以北的狭长前陆盆地，南北两侧为活动断裂控制的山地；地貌自西南向东北分为数条平行带，绿洲依山前河流呈串珠状分布。",
 infl="所引 1998 年研究指出河西走廊是青藏高原东北缘的新生代前陆盆地系统，活动断裂以 NW 向逆—左行走滑与 NNW 向逆—右行走滑为主，地貌自西南向东北分三条平行带；所引 2017 年研究分析该区降水变率。本条「走廊由活动断裂控制、绿洲依赖山前水系」据此。",
 pol="本条以自然地理为主，不展开政权序列；丝路历史年代待专门来源核验。",
 conn="祁连山冰雪融水维系绿洲与丝路通道；断裂活动与地震、山前洪积相关。",
 src=[("openalex-W2110703516","Tectonic geomorphology in the Hexi Corridor, north-west China",1998,42,695),
      ("openalex-W2774167345","Entropy-Based Investigation on the Precipitation Variability over the Hexi Corridor",2017,22,1288)],
 kw=["hexi corridor"], rel=[]),
"柴达木盆地":dict(tier="补充",theme="地形",coord=(95,37.3),
 defi="柴达木盆地：青藏高原东北部的内陆高原盆地，海拔高、盐湖与戈壁广布，是著名的盐类矿产区。",
 tp="新生代以来（青藏高原东北部坳陷）",
 ov="柴达木盆地：位于青藏高原东北部的内陆盆地，海拔高、气候干旱，盐湖、戈壁与山前戈壁广布，以盐类矿产著称。",
 geo="青藏高原东北部的高海拔内陆盆地，四周为祁连山、阿尔金山、昆仑山环绕；气候干旱，盐湖与戈壁广布，山前冲积扇发育。",
 infl="所引 2021 年研究提出岩石圈挠曲（buckling）主导柴达木盆地新生代沉降；所引 2016 年研究讨论柴达木盆地与周边山地的源—汇（侵蚀—沉积）关系。本条「盆地沉降与周边山地隆升、物质源汇相关」据此。",
 pol="本条以自然地理与地质为主，不展开政权序列。",
 conn="封闭内流、蒸发强烈→盐湖与盐类矿产；山前冲积扇与绿洲农业。",
 src=[("openalex-W3154033814","Lithospheric buckling dominates the Cenozoic subsidence of the Qaidam Basin",2021,0,2356),
      ("openalex-W7147529769","Source to sink relations between the Qaidam basin and the surrounding mountains",2016,0,2661)],
 kw=["qaidam"], rel=[]),
"天山山脉":dict(tier="重要",theme="地形",coord=(84,42.5),
 defi="天山山脉：横贯中亚的巨大山系，将新疆分为南北，冰川与山前绿洲发育，构造活动强烈。",
 tp="古生代造山、新生代复活（印度—亚洲碰撞远程效应）",
 ov="天山山脉：横贯中亚的巨大山系，把新疆分为南疆与北疆；山脊冰川发育，山前绿洲依赖冰雪融水，是仍在活动的陆内造山带。",
 geo="横贯中亚、东西延展的巨大山系，分隔准噶尔盆地与塔里木盆地；山脊高、冰川与积雪发育，山前冲积扇与绿洲带发育，地震与活动断裂频繁。",
 infl="所引 2014 年研究以磁性地层与热年代学约束天山与西昆仑山的构造演化；所引 2024 年研究分析东天山戈壁—天山断裂的第四纪变形。本条「天山是受印度—亚洲碰撞驱动、仍在活动的陆内造山带」据此。",
 pol="本条以自然地理与构造为主，不展开政权序列。",
 conn="冰雪融水维系南北疆绿洲；山口是交通与气候通道，活动断裂带地震风险高。",
 src=[("openalex-W7143887305","Tectonic evolution of the Tian Shan and Western Kunlun Shan",2014,0,2944),
      ("openalex-W4402376020","Quaternary Deformation along the Gobi–Tian Shan Fault in the Easternmost Tian Shan",2024,8,1519)],
 kw=["tian shan"], rel=[]),
"横断山脉":dict(tier="重要",theme="地形",coord=(99,28),
 defi="横断山脉：青藏高原东南缘一系列南北走向的高山深谷，岭谷相间、垂直带谱完整、生物多样性极高。",
 tp="新生代以来（高原隆升与河流深切）",
 ov="横断山脉：青藏高原东南缘的南北向高山深谷区，岭谷相间、河谷深切，垂直气候与植被带谱完整，是全球生物多样性热点之一。",
 geo="青藏高原东南缘一系列近南北走向的高山与深谷，岭谷相间、河谷深切；海拔落差大，垂直气候—植被带谱完整，生物多样性极高。",
 infl="所引 2022 年研究讨论横断山脉形成对区域季风气候与生物多样性的影响；所引 2025 年研究分析末次盛冰期以来横断山植被变化，指出其地形包含高原面、高山与湖盆的多样组合。本条「横断山岭谷相间、垂直带谱完整、生物多样性高」据此。",
 pol="本条以自然地理为主，不展开政权序列。",
 conn="南北向河谷是物种迁移与民族走廊；水能与生物多样性资源丰富，山地灾害（滑坡、泥石流）多发。",
 src=[("openalex-W4221057355","The Impact of Hengduan Mountains Formation on the Regional Monsoon Climate",2022,1,2919),
      ("openalex-W4408444505","Vegetation changes in the Hengduan Mountains, China since the Last Glacial Maximum",2025,0,1676)],
 kw=["hengduan"], rel=[]),
}

P_asia = os.path.join(DATA, "asia.json"); doc = json.load(open(P_asia, encoding="utf-8"))
ids = {e["id"] for e in doc["entries"]}
sd = json.load(open(os.path.join(DATA, "sources.json"), encoding="utf-8")); have = {s["id"] for s in sd["sources"]}
ow = json.load(open(os.path.join(DATA, "object_words.json"), encoding="utf-8"))
ss = json.load(open(os.path.join(DATA, "semantic_scan.json"), encoding="utf-8"))
added = []
for title, m in META.items():
    eid = "asia-" + sid(title)
    fn, (lon, lat) = SCHEMA[title]
    entry = {"id": eid, "title": title, "tier": m["tier"], "unit_id": "asia", "region": "亚洲", "theme": m["theme"],
      "level": "L2", "status": "L2完成(新增·中国地貌)", "definition": m["defi"], "time_or_place": m["tp"],
      "overview": m["ov"], "related": [], "sources": [x[0] for x in m["src"]], "needs_verification": True,
      "pending_notes": "新增条目：地貌形态为教科书性常识；构造/机制据所引文献，具体年代与速率待专门核验。",
      "outlines": [title + "·中国地貌单元"], "last_update": "2026-11-25",
      "geo": m["geo"], "influence": m["infl"], "polities": m["pol"], "connections": m["conn"],
      "today": "（本条的当代指标不在本页展开。）", "svg": combine(fn(None), lon, lat, title)}
    # related 指向长江/黄河
    if title in ("长江中下游平原", "珠江三角洲"):
        entry["related"] = ["asia-" + sid("长江流域")]
    if title in ("华北平原",):
        entry["related"] = ["asia-" + sid("黄河流域")]
    if eid not in ids:
        doc["entries"].append(entry); added.append(title)
    for sid_, t, y, c, ln in m["src"]:
        if sid_ in have: continue
        sd["sources"].append({"id": sid_, "title": f"OpenAlex {sid_[9:]} — {t}", "author": "OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year": y, "type": "学术文献", "url": f"https://api.openalex.org/works/{sid_[9:]}", "url2": None,
          "link_ok": True, "verified": True, "page_title": t[:200],
          "note": f"OpenAlex 作品 {sid_[9:]}；{y}年；被引 {c}。摘要长度 {ln} 字符。经 Crossref 检索 + DOI 桥取得，摘要已人工阅读。证据强度：strong。"})
        have.add(sid_)
    ow[title] = m["kw"]
    ss["scanned_entries"] = sorted(set(ss["scanned_entries"]) | {title})

json.dump(doc, open(P_asia, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(sd, open(os.path.join(DATA, "sources.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(ow, open(os.path.join(DATA, "object_words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(ss, open(os.path.join(DATA, "semantic_scan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
docs = {u: json.load(open(os.path.join(DATA, u + ".json"), encoding="utf-8")) for u in
        ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]}
save_docs(docs); update_coverage(docs)
print("added", len(added), added)
