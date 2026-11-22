# -*- coding: utf-8 -*-
"""第3轮抽检返工：7条 FAIL 条目的专题来源替换、无源年代移除与措辞修正。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

FIX={
"地理信息系统":{
 "time_or_place":"空间数据方法（形成年代待专门来源核）",
 "definition":"地理信息系统：通过采集、存储、分析与展示空间数据来支撑制图与区域研究的方法体系；其形成年代与学科谱系待专门来源核验。",
 "sources":["ogc-standards","esri-gis","s075-aag-org"],
 "pending_notes":"返工：已移除无源年代；OGC 标准页与 Esri GIS 定义页支撑方法概述，OpenStax 页面标题仅为站点名，未作为专题依据。学科形成年代待专门史料核验。"},
"尼罗河三角洲":{
 "time_or_place":"埃及北部（地貌演化年代待核）",
 "polities":"历史上多个政权把三角洲与河谷作为经济重心；具体王朝序列需专门史料核验。",
 "sources":["fao-aquastat-basins","br-nile","wk-nile"],
 "pending_notes":"返工：已移除全新世与王朝具体序列；FAO AQUASTAT 流域页支撑水资源背景，三角洲演化年代待专门地貌来源核验。"},
"长江流域":{
 "time_or_place":"长江流域（农业与城市密集区）",
 "polities":"中古以后经济重心逐渐南移，具体时期与政权序列待专门来源核验。",
 "sources":["fao-aquastat-basins","s022-ourworldindata-org","un-m49"],
 "pending_notes":"返工：已移除约前5000年与王朝序列；FAO 流域页支撑水系背景，稻作起源与年代待专门来源核验。"},
"阿尔卑斯山":{
 "time_or_place":"中欧山地（形成年代待核）",
 "geo":"阿尔卑斯山横贯中欧，冰川与河谷塑造地形，山口为南北交通提供可能通道。海拔差异形成明显垂直气候带。",
 "sources":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "pending_notes":"返工：已移除约3000万年前与欧洲最高山脉表述；山口表述改为提供通道而非决定交通；山地形成年代待专门地质来源核验。"},
"五大湖":{
 "time_or_place":"北美中东部（湖群形成细节待核）",
 "geo":"五大湖位于北美中东部，由地质与冰川过程塑造，湖群通过圣劳伦斯河通向大西洋。湖岸平原与港口条件优越。",
 "sources":["noaa-glerl","s050-oceanservice-noaa-gov"],
 "pending_notes":"返工：已移除冰后期与具体成因断言；NOAA GLERL 支撑湖泊研究背景，形成过程与年代待专门来源核验。"},
"南极半岛":{
 "time_or_place":"南极洲北部（地质年代待核）",
 "influence":"相对可达性使半岛成为科考密集区，区域升温与海洋过程共同影响冰架和生态。人类活动受限，变化原因需结合观测与模型，不作单因解释。",
 "sources":["s038-earthobservatory-nasa-gov","s049-ncei-noaa-gov"],
 "pending_notes":"返工：已移除约中生代与科考站密集的具体断言；原因表述改为多因素；半岛地质年代与站点数量待专门来源核验。"},
"大陆漂移":{
 "time_or_place":"20世纪初（具体年份待专门来源核）",
 "sources":["usgs-dynamic-earth","s056-earthquake-usgs-gov"],
 "status":"待复核(第3轮返工)",
 "pending_notes":"返工：USGS《This Dynamic Earth》已加入并核验，可支撑漂移与板块理论概述；魏格纳提出年份仍待专门史料核验，故状态回到待复核。"},
}

def main():
    docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
    done=[]
    for d in docs.values():
        for e in d["entries"]:
            if e["title"] in FIX:
                e.update(FIX[e["title"]])
                e["last_update"]=TODAY
                if e["title"]!="大陆漂移": e["status"]="抽检返工完成(第3轮)"
                done.append(e["title"])
    for u,d in docs.items():
        json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    update_coverage(docs)
    print("返工",len(done),"条：","、".join(done))

if __name__=="__main__": main()
