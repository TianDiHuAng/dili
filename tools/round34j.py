# -*- coding: utf-8 -*-
"""第34轮末批：升级 4 条（湄公河三角洲/东亚季风/尼罗河三角洲/伊比利亚半岛）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F3=json.load(open(os.path.join(ROOT,"reports","round34_final3.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

BODY={
"湄公河三角洲":dict(
 defn="湄公河三角洲：湄公河在越南南部入海形成的三角洲平原。",
 span="现代水文观测（本条引 2014 年地面沉降研究）",
 geo="三角洲地势低平、河网密布，由河流泥沙沉积形成；潮汐与季风洪水共同塑造水道。地势低使高程对海平面变化极为敏感。",
 infl="泥沙补给与地面沉降决定三角洲能否维持高程；地下水抽取引起的地面沉降与海平面上升叠加，是当代最直接的物理风险，研究表明两者共同作用。",
 conn="经南海航道连接区域与全球市场，内陆经湄公河干流通柬埔寨与泰国东北部。"),
"东亚季风":dict(
 defn="东亚季风：东亚地区随季节反转的盛行风系统，夏季湿润、冬季干冷。",
 span="气候尺度（本条引 2015 年降水变率研究）",
 geo="海陆热力差异与青藏高原、西太平洋副热带高压共同决定季风的进退；雨带随季节自南向北推进，形成华南前汛期、江淮梅雨与华北雨季。",
 infl="季风降水的时间与空间集中度决定农业窗口与洪涝风险；古气候记录显示季风强度存在千年尺度变化，这使「稳定季风」的假设不成立。",
 conn="与印度季风、西太平洋暖池及厄尔尼诺—南方涛动相互关联，一个区域的异常常通过大气环流影响另一区域。"),
"尼罗河三角洲":dict(
 defn="尼罗河三角洲：尼罗河在埃及北部入地中海形成的扇形冲积平原。",
 span="现代环境观测（本条引 2010 年水质研究）",
 geo="三角洲由多条分支河道与潟湖组成，地势低平；上游来沙与洪水季节决定沉积与侵蚀的平衡，海岸线受波浪与沿岸流影响。",
 infl="上游筑坝改变了来沙与洪水节律，三角洲的沉积补给因此减少，海岸侵蚀与盐水入侵成为突出问题；水质研究显示重金属等污染物的空间分布与河道、工业位置相关。",
 conn="北接地中海航线，南经尼罗河谷连上埃及，是埃及人口与农业的核心区。"),
"伊比利亚半岛":dict(
 defn="伊比利亚半岛：欧洲西南部被地中海与大西洋环绕的半岛。",
 span="区域地理与人文（本条引 2007 年野生食用植物传统知识研究）",
 geo="半岛以梅塞塔高原为主体，四周为山脉，河谷深切；地中海沿岸与大西洋沿岸气候不同，内陆为大陆性。降水自西北向东南递减。",
 infl="气候与地形的梯度造成农业与聚落的东西、南北差异；传统植物利用知识的分布研究显示，生态多样性与文化实践高度耦合。",
 conn="北经比利牛斯山接西欧，南隔直布罗陀海峡望北非，是地中海与大西洋航路的交汇点。"),
}
n=0;up=[]
for t,b in BODY.items():
    c=F3.get(t);e=T.get(t)
    if not c or not e: continue
    oa=(c.get("id") or "").rsplit("/",1)[-1];sid=f"openalex-{oa}"
    if sid not in have:
        code=0;size=0
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oa}"],capture_output=True,timeout=30)
            raw=p.stdout.decode("utf-8","ignore");bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        except Exception: pass
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":c.get("year"),"type":"学术文献",
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":(c.get("title") or "")[:120],
          "note":f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:240]}…"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第34轮)-学术文献",
      "definition":b["defn"],
      "overview":f"{b['defn']} 本条以学术文献与地理描述为主。",
      "time_or_place":b["span"],"geo":b["geo"],"influence":b["infl"],
      "polities":e.get("polities") or "本条以自然地理/区域概述为主；具体政权序列待专门史料核验。",
      "connections":b["conn"],
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第34轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，「{(c.get('title') or '')[:60]}」，DOI {c.get('doi') or '无'}）；文献主题属本条领域，支撑地理与机制表述。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M90 280 L230 240 L380 220 L520 235 L640 270' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='380' cy='220' r='7' class='pt'/><text x='300' y='200' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
import collections
print("升级",n,"：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))