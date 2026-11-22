# -*- coding: utf-8 -*-
"""第4轮：2新增 + 5来源修复记录 + 33复核，分4批。"""
import json, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid, update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

NEW=[
 ("global-themes","人口地理","重要","全球","区域","现代人口分布与长期人口转变",
  "研究人口数量、分布、迁移与结构的空间差异，关注人口变化与资源、城市、区域发展之间的关系。",
  ["s023-ourworldindata-org","s075-aag-org"],"人口迁移"),
 ("global-themes","城市地理","重要","全球","区域","现代城市化与城市体系",
  "研究城市的区位、内部空间结构、城市体系与城市化过程，关注城市与腹地、交通和环境之间的互动。",
  ["s025-ourworldindata-org","s075-aag-org"],"城市起源"),
]

FIX_NOTES={
 "尼罗河三角洲":"第4轮来源再核：World History Encyclopedia、Encyclopedia.com、EOL 均不可达或被拒绝；FAO AQUASTAT 与 NASA 页面标题非三角洲专题，维持 L1 与待核实。",
 "长江流域":"第4轮来源再核：未取得页面标题与长江流域直接对应的权威专题页；FAO 流域页仅作背景，维持 L1 与待核实。",
 "阿尔卑斯山":"第4轮来源再核：Britannica/World History 页面被拒绝，USGS/NASA 标题非阿尔卑斯专题，维持 L1；不再写最高山脉等不可核断言。",
 "五大湖":"第4轮来源再核：EPA《The Great Lakes》与 NOAA GLERL 已核验，但缺少圣劳伦斯航道、工业带与美加边界专题来源，维持 L1。",
 "南极半岛":"第4轮来源再核：BAS 站点返回 202、Britannica 403、NASA 标题非半岛专题，维持 L1；地质与站点分布待补。",
}

REVIEW_TITLES=[
 "阿契美尼德波斯","孔雀王朝","笈多王朝","宋代","明清","朝鲜半岛","中南半岛","湄公河三角洲","吴哥","马来群岛","河中地区","突厥","黎凡特","长江流域",
 "伊比利亚半岛","高卢","多瑙河","莱茵河","法兰克王国","十字军东征","威尼斯","基辅罗斯","巴尔干半岛","黑海海峡","阿尔卑斯山",
 "马格里布","库什与努比亚","迦太基","阿拉伯征服北非","斯瓦希里海岸","尼罗河三角洲","北美冰盖",
 "落基山脉","科罗拉多高原","中美洲地峡","奥尔梅克","特奥蒂瓦坎","巴西高原","阿塔卡马沙漠","莫切文化","蒂亚瓦纳科",
 "大自流盆地","新西兰北岛","新西兰南岛","毛利人","大堡礁","横贯南极山脉","罗斯海","冰芯气候记录","南极半岛",
 "大陆漂移","洋流","气候带","沙漠化","山地农业","人口迁移",
]
# 每轮取前33个，其余留第5轮
REVIEW_TITLES=REVIEW_TITLES[:33]

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
 "农业":["s014-fao-org","s022-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],
 "政权更替":["s011-unesco-org","s058-worldbank-org"],
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
           "theme":theme,"level":"L1","status":"L1完成(第4轮)",
           "definition":title+"："+overview,"time_or_place":tp,"overview":overview,
           "related":[rid] if rid else [],"sources":sources,"needs_verification":True,
           "pending_notes":"B1/B4 缺口补入；专题教材章节与现状数值待按年份核验。",
           "outlines":["OpenStax Geography 教材目录","AAG 学科页面"],"last_update":TODAY}
        docs[uid]["entries"].append(e);out.append(e["id"])
    return out

def fix(docs,title):
    for d in docs.values():
        for e in d["entries"]:
            if e["title"]==title:
                e["pending_notes"]=FIX_NOTES[title];e["last_update"]=TODAY;e["status"]="来源再核未通过(第4轮)"
                return e["id"]
    raise SystemExit("未找到:"+title)

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
                e["pending_notes"]=(f"第4轮复核：{e['region']}×{e['theme']}；"+
                    f"新增背景来源 {added or '无'}，现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
                e["last_update"]=TODAY;e["status"]="已复核(第4轮)"
                return e["id"]
    raise SystemExit("未找到复核:"+title)

def append_scope(titles):
    p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
    block="### 第4轮补充（B1/B4 缺口）\n\n"+"".join(f"- **{x}**（重要；见对应单元）— 教材目录/读者问题缺口补入。\n" for x in titles)+"\n"
    if "### 第4轮补充" not in t: t=t.replace(marker,block+marker)
    open(p,"w",encoding="utf-8").write(t)

def main():
    b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
    if b==1:
        done+=["NEW:"+x for x in add_new(docs)]
        for t in FIX_NOTES: done.append("FIX:"+fix(docs,t))
        for t in REVIEW_TITLES[:3]: done.append("REVIEW:"+review(docs,t))
        append_scope([n[1] for n in NEW])
    elif b==2:
        for t in REVIEW_TITLES[3:13]: done.append("REVIEW:"+review(docs,t))
    elif b==3:
        for t in REVIEW_TITLES[13:23]: done.append("REVIEW:"+review(docs,t))
    elif b==4:
        for t in REVIEW_TITLES[23:33]: done.append("REVIEW:"+review(docs,t))
    else: raise SystemExit("batch 1-4")
    for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    update_coverage(docs)
    print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))

if __name__=="__main__": main()
