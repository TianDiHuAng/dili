# -*- coding: utf-8 -*-
"""第49轮B：处理第二批（阿拉伯半岛←骆驼、马格里布←人群基因）+ 记录扫描结论。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

DROPS={
"阿拉伯半岛":("openalex-W3217685633","《Genetic structure of Arabian Peninsula dromedary camels》——研究对象是**单峰驼**的群体遗传结构，不是半岛的地理与面积；第41轮曾加说明但未剔除，本轮按 R19 剔除。"),
"马格里布":("openalex-W2008635858","《Mitochondrial DNA analysis of Northwest African populations》——研究对象是**人群的线粒体 DNA**，不是区域地理；仅可作「人群连续性」的旁证，不作地理来源。"),
}
for t,(sid,why) in DROPS.items():
    e=T.get(t)
    if not e: continue
    e["sources"]=[s for s in e["sources"] if s!=sid]
    e["pending_notes"]=re.sub(rf" 【[^】]*】{re.escape(sid)}[^【]*","",e.get("pending_notes") or "")
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第49轮剔除·对象错误】{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=49
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 记录 R19 扫描结论
rows=json.load(open(os.path.join(ROOT,"reports","round49_titles.json"),encoding="utf-8"))
SIDE=["维京时代","美国西进","莫切文化","阿塔卡马沙漠","南锥体","新法兰西","古埃及中王国","古巴岛",
 "巴塔哥尼亚","复活节岛","密克罗尼西亚","印加帝国","元代","拜占庭帝国","大自流盆地","新西兰南岛",
 "古埃及新王国","南极大陆","密西西比河","亚马逊盆地","季风系统","河流三角洲","地理信息系统","城市地理",
 "意大利半岛","文艺复兴意大利","澳大利亚内陆干旱气候","落基山脉","河中地区","突厥","萨哈拉以南发展数据"]
rep={"round":49,"scanned_entries":len(rows),
 "dropped":[{"entry":t,"sid":s,"why":w} for t,(s,w) in DROPS.items()],
 "dropped_earlier_this_round":[
   {"entry":"罗马共和国","sid":"openalex-W4408242507","why":"学科错配：台伯河冲积平原三维岩相建模（地质学）"},
   {"entry":"澳大利亚原住民","sid":"openalex-W2260197586","why":"对象错误：19世纪原住民板球队员访英史"},
   {"entry":"汉代","sid":"openalex-W4403972561","why":"降旁证：汉代图像中的狗（动物考古侧面）"},
   {"entry":"植物物候变化","sid":"openalex-W7224996787","why":"降旁证：PhenoFECT 预测软件包"},
   {"entry":"北美冰盖","sid":"openalex-W2100185916","why":"标明：Comment/Reply 学术讨论通信"}],
 "side_evidence_note":"另有约 30 条属「侧面文献」（如拜占庭←医院史、元代←高丽青瓷、印加←玉米酒、莫切←艺术图像），"
   "对象同一但只涉一个侧面；已在本轮扫描中识别，须逐条降为旁证或补主来源——留待下一轮处理。",
 "method":"导出全部 196 条含学术来源条目及其来源标题，人工逐条核对对象同一性（R19 的人工执行形式）"}
json.dump(rep,open(os.path.join(ROOT,"reports","round49_r19_scan.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("已剔除:",list(DROPS))
print("扫描条目:",len(rows),"；识别侧面文献约 30 条待下轮处理")