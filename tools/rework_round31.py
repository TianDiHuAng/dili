# -*- coding: utf-8 -*-
"""第31轮返工：CO2 口径纠反、查询时点格式、D076 全库扫尾、R15 机器化。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) CO2 口径纠反
co=T["二氧化碳排放清单"]
co["today"]=("来源：世界银行 API（指标 EN.GHG.CO2.MT.CE.AR5，官方名为 "
  "「Carbon dioxide (CO2) emissions (total) **excluding LULUCF**」，单位 Mt CO₂e）：全球 2024 年约 39,632.66 Mt CO₂e。"
  "该口径**不含土地利用变化与林业（LULUCF）**；与含 LULUCF 的清单、以及仅计能源燃烧的口径均不可直接比较，跨国比较须先核对核算范围。")
co["pending_notes"]=((co.get("pending_notes") or "")+
  " 【第31轮返工】口径纠反：该指标为「不含 LULUCF（土地利用变化与林业）」，此前误写为「含土地利用」，已订正 today 与来源 note。").strip()
co["last_update"]=TODAY

# sources note 同步
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
    if s["id"]=="wb-wld-co2":
        s["note"]=("JSON API 200；2024 年 39,632.66 Mt CO₂e。"
          "官方指标名为「CO2 emissions (total) **excluding LULUCF**」——**不含土地利用变化与林业**；"
          "年度指标，随年度更新与历史修订变化。此前 note 误写为「含土地利用口径 AR5」，已订正。")
    if s["id"]=="ats-parties":
        s["note"]=s["note"].replace("以页面当前状态为准。","以页面当前状态为准；查询时点 2026年11月22日。")
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 2) A1 查询时点格式
at=T["南极条约体系"]
at["today"]=at["today"].replace("（2026年查询）","（查询时点 2026年11月22日）")

# 3) 板块构造补查询时点
pt=T["板块构造"]
pt["today"]=pt["today"].replace("（M≥6 事件，2025年 1–12 月）","（M≥6 事件，2025年 1–12 月；查询时点 2026年11月22日）")
if "查询时点" not in pt["today"]:
    pt["today"]=pt["today"].replace("来源：USGS 地震目录 API","来源：USGS 地震目录 API（查询时点 2026年11月22日）")

# 4) D076 全库扫尾
fixed=[]
for e in T.values():
    pn=e.get("pending_notes") or ""
    st=e.get("status") or ""
    if "·实证" not in st: continue
    bad = ("未达标" in pn) or ("命中 0" in pn) or ("命中0" in pn) or ("维持 L1" in pn)
    if bad:
        e["status"]=re.sub(r"已复核\(第(\d+)轮·实证\)", r"已复核(第\1轮·无实证)", st)
        e["last_update"]=TODAY;fixed.append(e["title"])

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 5) R15：D075 机器化
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R15" not in t:
    t=t.replace('            if e.get("today"):\n                check_today_sources(e)',
'''            if e.get("today"):
                check_today_sources(e)
                check_dynamic_source(e)''')
    t=t.replace("def check_today_sources(e):",
'''DYN_WORDS = ("实时", "随查询", "随…变化", "名录", "目录为实时")

def check_dynamic_source(e):
    """R15：动态/名录类来源必须写明「查询时点 YYYY年MM月DD日」（D075）。"""
    today = e.get("today") or ""
    if not any(w in today for w in DYN_WORDS):
        return
    if not re.search(r"查询时点\\s*\\d{4}年\\d{1,2}月\\d{1,2}日", today):
        err(f"R15 {e['id']}: today 描述了动态/名录类来源，但缺「查询时点 YYYY年MM月DD日」")


def check_today_sources(e):''')
    open(p,"w",encoding="utf-8").write(t)
    print("R15 已加入")
print("返工：CO2 口径、查询时点、D076 扫尾",len(fixed),fixed)