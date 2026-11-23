# -*- coding: utf-8 -*-
"""第41轮返工：环境治理越界、time_or_place、D081声明id、CBD链接、徽标白名单、台账。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== 1 环境治理：末两句越界（把研究缺口当结论）=====
eg=T["环境治理"]
eg["influence"]=("所引 2011 年研究评估环境治理体制的**有效性**：既有研究已在较严格的方法框架下审视这类组织的绩效，"
  "但对两类问题关注有限——①组织**学习与创新能力**，②组织与相关**社会政治环境的契合度**。"
  "作者的结论是：系统性地修补这一缺口是值得推进的工作，并以中国与欧洲的后社会主义国家经验作为例示。"
  "（这两项是作者指出的**研究缺口**，不是已确立的成因。）")
eg["pending_notes"]=((eg.get("pending_notes") or "")+
  " 【第41轮返工】原末两句「有助于理解治理成效为何差异巨大」「有效性不取决于规则文本也取决于制度学习与情境匹配」——"
  "摘要明说这两项是 accorded limited attention（尚未被充分研究），被写成已确定的成因，属把研究缺口当结论（D092）。已改写。").strip()
eg["last_update"]=TODAY

# ===== 2 阿巴拉契亚：time_or_place + 末句 =====
ap=T["阿巴拉契亚山脉"]
ap["time_or_place"]="晚古生代阿勒格尼造山期（320–260 Ma，据 2002 年 GSA 研究）；更早的造山事件始于早古生代"
ap["influence"]=("所引 2002 年研究（被引 163）指出：阿巴拉契亚造山带形成于**早古生代开始、以阿勒格尼造山运动（Alleghanian，320–260 Ma）结束**的过程，"
  "由大陆—大陆碰撞与 Theic 洋最终闭合驱动。作者以阿勒格尼造山作为「拉链式构造（zipper tectonics）」的例证：斜向碰撞后板块旋转、"
  "洋盆自一端向另一端逐步闭合。就本条所引研究而言，它支持「同一山系由多期事件叠加而成」，阿勒格尼期为斜向旋转碰撞机制。")
ap["pending_notes"]=((ap.get("pending_notes") or "")+
  " 【第41轮返工】① time_or_place 原写「时期与年代待专门来源核验」，与 influence 已给出的 320–260 Ma 矛盾，已同步；"
  "② 末句「不同机制」收紧为「多期事件叠加，阿勒格尼期为斜向旋转碰撞机制」——摘要只支持多期，未对早期事件断言机制。").strip()
ap["last_update"]=TODAY

# ===== 3 D081 声明 id 校正（3 条按实际 sources 重写）=====
def fix_d081(title):
    e=T.get(title)
    if not e: return
    actual=[s for s in e["sources"] if s.startswith(("s0","un-","britannica","wikipedia","ap-"))]
    pn=e.get("pending_notes") or ""
    new=(" 【D081单源声明】本条除 OpenAlex 文献外的来源为 "
         + "、".join(actual) + "，其中 britannica-regions/wikipedia-regions 为壳别名、un-m49 为区域框架、"
         "s070/s071-cbd-int 为《生物多样性公约》首页、s010-unesco-org 为 UNESCO Culture 首页——"
         "均与条目主题不同类或不含正文，不构成独立内容依据；本条实质为**单源（OpenAlex）**，"
         "coverage 中的 source_count 应理解为「链接数」而非「可互证来源数」。")
    pn=re.sub(r" 【D081单源声明】[^【]*", "", pn)
    e["pending_notes"]=(pn+new).strip()
    e["last_update"]=TODAY
for t in ("南极特别保护区","争议边界处理原则","环境治理"): fix_d081(t)

# ===== 4 南极特别保护区：CBD 链接标注 =====
for s in sd["sources"]:
    if s["id"] in ("s070-cbd-int","s071-cbd-int"):
        s["note"]=(s.get("note") or "")+" 【第41轮标注】《生物多样性公约》首页，与南极条约体系口径相邻但非同一制度，不含本条主题正文，不作内容依据。"

# ===== 5 gen_site.py 徽标白名单 =====
gp=os.path.join(ROOT,"tools","gen_site.py")
gt=open(gp,encoding="utf-8").read()
if "学术文献" not in gt:
    gt=gt.replace('''    if "Wikidata" in st:''',
'''    if "-学术文献" in st or "-指标数据" in st:
        return '<span class="tag">来源：学术文献（单源待互证）</span>'
    if "Wikidata" in st:''')
    open(gp,"w",encoding="utf-8").write(gt)
    print("徽标白名单已补")

# ===== 6 台账 =====
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=41;cov["round_processed"]=5
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成")