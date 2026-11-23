# -*- coding: utf-8 -*-
"""第40轮末批：农业气候风险、南美贸易网络 → L2。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
B=json.load(open(os.path.join(ROOT,"reports","round40_bridge2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

BODY={
"农业气候风险":dict(defn="农业气候风险：气候变率与变化对农业生产、收入与粮食安全的潜在损害。",
 geo="风险的空间分布由气候暴露（干旱、热浪、霜冻、暴雨）与农场脆弱性（灌溉条件、品种、资产）叠加决定；热带与雨养农业区风险最高，灌溉区与高纬度地区相对较低。",
 infl="所引 2019 年研究（PLoS ONE，被引 272）开发了一套可在**次国家尺度**复现的脆弱性评估方法，用于识别受气候影响最大的地区与社区。这说明气候风险无法由国家级平均值代表，需下推到地方单元才有政策意义。",
 conn="与水资源、作物单产、贫困、极端天气预警、气候适应政策相关。"),
"南美贸易网络":dict(defn="南美贸易网络：前西班牙时期安第斯与南美各地区之间的长距离交换体系。",
 geo="安第斯地区的交换沿垂直生态带展开：沿海提供鱼类与贝壳，高地提供马铃薯与藜麦，亚马逊东坡提供羽毛、木材与药材。这种「垂直群岛」格局使长距离交换成为生计必需。",
 infl="所引 2014 年研究以世界体系视角讨论**贵重贸易品**（如 Spondylus 马蹄螺贝壳）在安第斯社会再生产中的作用，并把它与安第斯主要语言的多次扩散相联系。这说明贸易品兼具经济与象征功能，可与语言与族群过程交织。",
 conn="连接沿海、高地与亚马逊东坡，并向北接入中美洲、向南接入南锥体方向的路线。"),
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
          "url":f"https://api.openalex.org/works/{oa}","url2":f"https://doi.org/{c['doi']}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oa}（经 Crossref DOI {c['doi']} 定位）；{c.get('year')}年；{c.get('host')}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符。"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第40轮)-学术文献","definition":b["defn"],
      "overview":b["defn"]+" 机制/影响段据所引研究撰写，geo 为常识性地理描述（未挂学术来源）。",
      "time_or_place":e.get("time_or_place") or "（本条为概念/网络主题条目，无单一时间跨度）",
      "geo":b["geo"],"influence":b["infl"],"connections":b["conn"],
      "polities":e.get("polities") or "本条为概念/区域主题条目，不展开具体政权序列。",
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第40轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}），经 Crossref→OpenAlex DOI 桥获取。"
        f" 【D081单源声明】britannica-regions/wikipedia-regions 为壳别名、s010-unesco-org 为 UNESCO Culture 首页，均不构成独立内容依据；本条实质为单源（OpenAlex）。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 275 L235 238 L375 218 L515 236 L645 270' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='375' cy='218' r='7' class='pt'/><text x='275' y='196' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
save_docs(docs);update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print("剔除5条：阿巴拉契亚(金伯利岩过窄)、古巴岛(命中阿拉斯加半岛)、南极特别保护区(泛论保护区非南极)、争议边界(制图表示泛论)、环境治理(三本书评)")
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))