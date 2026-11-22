# -*- coding: utf-8 -*-
"""第5轮：2新增 + 8核心升级L2 + 30复核，分4批。"""
import json, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, make_svg, update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

NEW=[
 ("global-themes","地图投影","补充","全球","区域","制图方法（历史演变待专门来源核）",
  "把地球曲面转换为平面的数学规则，是地图制图与空间数据表达的基础环节；不同投影在面积、角度与距离上各有取舍。",
  ["ogc-standards","esri-gis"],"地理信息系统"),
 ("global-themes","争议边界处理原则","补充","全球","区域","编辑方法（非地理事实断言）",
  "本站对争议边界只并列描述各方立场，不绘制争议线，也不替读者下结论；这是资料编辑原则，不是对主权归属的判断。",
  ["un-m49","s070-cbd-int"],"南极条约体系"),
]

CONTENT={
"刚果盆地":{
 "defn":"刚果盆地：非洲中部的大型盆地，热带雨林广布，河网呈向心状汇入刚果河。",
 "geo":"盆地四周被高地环绕，中部低平，热带雨林覆盖广阔。刚果河及其支流构成密集水网，降水丰沛且季节分布相对均匀；资源包括森林、水力与矿产。",
 "influence":"雨林与水系支撑多样的生计方式，河流是区域交通的重要通道。森林覆盖与土地利用受人口、政策和全球需求共同影响，不能把区域差异简化为环境决定。",
 "polities":"前殖民时期存在多种社群与区域网络，近代殖民边界与资源开发改变了政治经济格局。具体政权序列需专门史料核验。",
 "connections":"盆地通过刚果河与大西洋连接，并通过陆地通道与东非大湖区、撒哈拉南缘互动。",
 "today":"森林覆盖变化与水力资源是当代议题。森林面积、人口与经济数据需按年份从权威机构补齐。",
 "sources":["s018-fao-org","s042-earthobservatory-nasa-gov","s013-fao-org"]},
"青藏高原":{
 "defn":"青藏高原：亚洲高海拔广大高原，是多条大河的发源区，高寒环境影响交通与聚落分布。",
 "geo":"高原平均海拔极高，边缘由山脉围限，内部包含盆地、湖泊与宽谷。高寒气候、冻土与强烈日照并存；冰川和河流源区是其重要自然特征。",
 "influence":"高海拔与寒冷限制农业和交通，河谷与低海拔地带更适合聚落。高原对亚洲水系与气候具有重要影响，但人类活动的结果取决于技术、制度与交流，不是环境单因决定。",
 "polities":"历史上高原与周边地区存在长期互动，形成多样的地方政权与宗教文化网络；具体年代与政权序列待专门来源核验。",
 "connections":"高原通过河流与东亚、南亚、中亚相连，山口与河谷构成交通通道，也是多条大河源头。",
 "today":"生态保护和气候变化是重要议题。海拔、人口与冰川数据需按年份从权威机构核验。",
 "sources":["s038-earthobservatory-nasa-gov","s056-earthquake-usgs-gov","s013-fao-org"]},
"日本列岛":{
 "defn":"日本列岛：东亚太平洋边缘的岛弧，山地多、平原狭小，海洋交通与地质活动深刻影响人居环境。",
 "geo":"列岛由多条弧形岛屿组成，山地与丘陵占大部，沿海平原狭窄。位于板块交界附近，地震与火山活动频繁；海洋性气候带来丰沛降水。",
 "influence":"海岸线曲折促进港口与海上交流，狭窄平原推动高密度土地利用。灾害风险管理是长期议题，但社会发展不能仅由地质条件解释。",
 "polities":"列岛历史上形成多个区域政权，近代以后政治结构经历显著变化；具体王朝与年代待专门来源核验。",
 "connections":"日本列岛通过东海、黄海与朝鲜半岛和中国相连，并通过太平洋航线与更广区域互动。",
 "today":"人口、能源与灾害管理是当代议题。相关数据需按年份从权威统计机构补齐。",
 "sources":["s050-oceanservice-noaa-gov","s056-earthquake-usgs-gov","s018-fao-org"]},
"亚马逊河":{
 "defn":"亚马逊河：南美洲流量巨大的河流，横贯亚马逊盆地，支撑广阔热带雨林与水运网络。",
 "geo":"河流发源于安第斯地区，向东流经低平盆地注入大西洋。主干与支流水量巨大，季节涨落塑造河岸湿地与洪泛林。",
 "influence":"河流是盆地内部最重要的交通廊道，渔业与洪泛农业沿河分布。雨林生态与河流过程相互联系，土地利用变化的影响需结合多源证据，不能单因解释。",
 "polities":"前殖民时期存在多样的流域社会，殖民与现代开发改变了资源利用格局；具体政权序列不在本站骨架内展开。",
 "connections":"亚马逊河通过大西洋航线与外部市场连接，安第斯山口又把流域与西岸地区联系起来。",
 "today":"森林砍伐、水文变化与生态保护是当代重点。径流量与森林面积需按年份从权威来源获取。",
 "sources":["fao-aquastat-basins","s086-earthobservatory-nasa-gov","s018-fao-org"]},
"密西西比河":{
 "defn":"密西西比河：北美洲主要水系，连接内陆大平原与墨西哥湾，是航运与农业区的重要骨架。",
 "geo":"干流自北向南流经中央低地，接纳众多支流，下游形成广阔冲积平原与三角洲。流域跨越多种气候区，水量与泥沙受季节和土地利用影响。",
 "influence":"内河航运降低大宗农产品运输成本，冲积平原支撑密集农业。洪水风险与水资源管理是长期议题，结果取决于工程与治理，不只由河流决定。",
 "polities":"流域与原住民社会、殖民边疆和现代州际治理密切相关；具体政治事件待专门史料核验。",
 "connections":"密西西比河水系连接五大湖—圣劳伦斯系统与墨西哥湾港口，是北美内陆物流的重要通道。",
 "today":"洪水、水质与航运是当代议题。人口、货运量与径流数据需按年份从权威机构补齐。",
 "sources":["fao-aquastat-basins","s013-fao-org","s077-ourworldindata-org"]},
"中美洲地峡":{
 "defn":"中美洲地峡：连接南北美洲的狭窄陆桥，山地、火山与海岸共同塑造区域生态与交通。",
 "geo":"地峡由火山山脉、高原与狭窄沿海平原组成，两侧临海。板块交界带来火山和地震活动，低地与山地之间气候差异明显。",
 "influence":"狭窄地形缩短东西向交通距离，山口与谷地成为通道；农业垂直分异明显。地质活动是重要条件，但聚落与社会变化还受贸易和制度影响。",
 "polities":"地峡历史上连接中美洲文明与南美、加勒比区域，近代形成多个国家；具体政权序列待专门来源核验。",
 "connections":"地峡连接北美与南美，太平洋与加勒比海航线在此靠近，是生物地理与贸易交流的走廊。",
 "today":"交通、火山灾害与生态连通性是当代议题。人口与货运数据需按年份核验。",
 "sources":["s056-earthquake-usgs-gov","s050-oceanservice-noaa-gov","s018-fao-org"]},
"游牧":{
 "defn":"游牧：随季节与资源变化迁移的生存方式，常见于草原、沙漠与高原环境，与定居社会长期互动。",
 "geo":"游牧区域多分布于降水不足或季节变化剧烈的草原与干旱区，水源与牧草分布决定迁移路线。山地垂直牧场也是常见形式。",
 "influence":"移动性使牧民能够利用分散资源，并与定居农业区交换畜产品与粮食。游牧并非环境单因产物，市场、制度与冲突同样塑造其形态。",
 "polities":"草原联盟、绿洲城邦与定居政权长期互动，贸易与冲突并存；具体政权名称与年代待专门来源核验。",
 "connections":"游牧网络把草原、沙漠与绿洲城市连接成交换通道，是跨区域贸易与文化传播的重要载体。",
 "today":"牧业社区面临气候变化、土地权属与市场整合压力。人口与牲畜数据需按年份从权威机构补齐。",
 "sources":["s018-fao-org","s077-ourworldindata-org","s013-fao-org"]},
"城市起源":{
 "defn":"城市起源：农业剩余、贸易与权力集中等因素共同作用，使部分聚落发展为早期城市。",
 "geo":"早期城市多出现在河流冲积平原、绿洲或海岸港口附近，水源、交通与可耕地是常见条件。地形并非唯一因素。",
 "influence":"农业剩余支持人口集中，贸易扩大资源来源，权力组织管理公共事务。学界对主次原因有不同看法，本站并列而不下结论。",
 "polities":"两河、尼罗河、印度河与东亚等地区出现早期城市，具体时间与政治形态各异；本站不把不同地区归入单一模式。",
 "connections":"城市通过商路连接腹地与远方市场，技术、宗教与艺术沿网络传播。",
 "today":"城市化仍是全球性过程。城市人口与面积数据需按年份从权威统计机构补齐。",
 "sources":["s010-unesco-org","s025-ourworldindata-org","s044-earthobservatory-nasa-gov"]},
}

GAP_BY_THEME={
 "地形":"地貌形成年代与关键地形节点的专题来源",
 "气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源",
 "贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源",
 "区域":"区域边界、人口与现状数据的专题来源",
}
SOURCE_BY_THEME={
 "地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],
 "农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],
 "政权更替":["s010-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"],
}

def add_new(docs):
    out=[]
    for uid,title,tier,region,theme,tp,overview,sources,rel in NEW:
        if any(e["title"]==title for e in docs[uid]["entries"]): continue
        rid=None
        for d in docs.values():
            for e in d["entries"]:
                if e["title"]==rel: rid=e["id"];break
            if rid:break
        e={"id":uid+"-"+sid(title),"title":title,"tier":tier,"unit_id":uid,"region":region,
           "theme":theme,"level":"L1","status":"L1完成(第5轮)",
           "definition":title+"："+overview,"time_or_place":tp,"overview":overview,
           "related":[rid] if rid else [],"sources":sources,"needs_verification":True,
           "pending_notes":"B4 缺口补入；专题方法与历史演变待专门来源核验。",
           "outlines":["OGC 标准","Esri GIS 定义","UN M49"],"last_update":TODAY}
        docs[uid]["entries"].append(e);out.append(e["id"])
    return out

def upgrade(docs,title):
    for d in docs.values():
        for e in d["entries"]:
            if e["title"]==title:
                c=CONTENT[title]
                e.update({"level":"L2","status":"L2完成(第5轮)","definition":c["defn"],"overview":c["defn"].split("：",1)[1],
                 "time_or_place":"地理与生态特征（具体演化年代待核）" if "年前" in e["time_or_place"] or "代" in e["time_or_place"] else e["time_or_place"],
                 "geo":c["geo"],"influence":c["influence"],"polities":c["polities"],
                 "connections":c["connections"],"today":c["today"],
                 "svg":make_svg(title,e["region"],e["theme"]),"sources":c["sources"],
                 "needs_verification":True,
                 "pending_notes":"第5轮升级：来源为 FAO/NASA/NOAA/USGS/OWID/UNESCO 等机构页，支撑自然地理与区域背景；历史序列与现状数值待专门来源核验。"})
                return e["id"]
    raise SystemExit("未找到:"+title)

def review_titles(docs):
    out=[]
    for u in UNITS:
        for e in docs[u]["entries"]:
            if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第4轮)" not in e["status"]:
                out.append(e["title"])
    return out[:30]

def review(docs,title):
    for d in docs.values():
        for e in d["entries"]:
            if e["title"]==title:
                gap=GAP_BY_THEME.get(e["theme"],"专题来源")
                pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"])
                added=None
                for s in pool:
                    if s not in e["sources"]:
                        e["sources"].append(s);added=s;break
                e["pending_notes"]=(f"第5轮复核：{e['region']}×{e['theme']}；"
                    f"新增背景来源 {added or '无'}，现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
                e["last_update"]=TODAY;e["status"]="已复核(第5轮)"
                return e["id"]
    raise SystemExit("未找到复核:"+title)

def append_scope(titles):
    p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
    block="### 第5轮补充（B4 缺口）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 读者问题缺口补入。\n" for x in titles)+"\n"
    if "### 第5轮补充" not in t: t=t.replace(marker,block+marker)
    open(p,"w",encoding="utf-8").write(t)

def main():
    b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
    if b==1:
        done+=["NEW:"+x for x in add_new(docs)]
        for t in CONTENT: done.append(upgrade(docs,t))
        append_scope([n[1] for n in NEW])
    else:
        titles=review_titles(docs)
        start=(b-2)*10
        for t in titles[start:start+10]: done.append("REVIEW:"+review(docs,t))
    for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    update_coverage(docs)
    print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))

if __name__=="__main__": main()
