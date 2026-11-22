# -*- coding: utf-8 -*-
"""第30轮返工：洋流时效表述、PM2.5 note、气候带无源断言、丝路指标编号、status 统一。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 洋流
oc=T["洋流"]
oc["today"]=("来源：NOAA CO-OPS 洋流观测站元数据 API（查询时点 2026-11-22）：当前登记 84 个洋流观测站。"
  "该站网仅覆盖美国沿岸水域，不代表全球洋流观测布局；全球洋流场的估算需结合卫星高度计与浮标阵列数据。"
  "站网目录为实时登记，数量随查询时刻变化，以查询返回为准。")
oc["pending_notes"]=((oc.get("pending_notes") or "")+
  " 【第30轮返工】删除「2025年查询」错误年份（实际查询时点 2026-11-22），补写实时目录的动态声明，并把「以美国沿岸为主」改为「仅覆盖美国沿岸水域，不代表全球布局」。").strip()
oc["last_update"]=TODAY

# 2) PM2.5 note
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
    if s["id"]=="wb-wld-pm25":
        s["note"]=("JSON API 200；2023 年 32.87 μg/m³（全球人口加权年均暴露）。"
                   "**世界银行年度指标**，随年度更新与历史修订变化，非实时目录。")
    if s["id"] in ("usgs-eq-m6","noaa-current-stations"):
        s["note"]=s["note"].replace("数值随查询时刻变化（USGS/NOAA 为实时目录），以查询返回为准。",
          "该端点为实时目录，数值随查询时刻变化，以查询返回为准。")
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 3) 气候带：删无源分布断言
cz=T["气候带"]
cz["today"]=("来源：世界银行 API（指标 AG.LND.ARBL.ZS，可耕地占土地面积比例）：全球 2023 年 10.67%。"
  "该指标反映土地利用强度，不区分气候带；气候带界线与各带面积需专门气候分类来源核验。")
cz["pending_notes"]=((cz.get("pending_notes") or "")+
  " 【第30轮返工】删除「温带与热带季风区占比高、干旱与寒带极低」等分布断言——该结论不来自所引指标（AG.LND.ARBL.ZS 仅给全球总量）。").strip()
cz["last_update"]=TODAY

# 4) 丝绸之路：UZB 补指标编号
sr=T["丝绸之路"]
sr["today"]=(sr["today"].replace("乌兹别克斯坦总人口 ",
  "乌兹别克斯坦总人口 ").replace("城市化率 51.0%（2025年）；",
  "城市化率 51.0%（2025年）；").strip())
# 若文本缺编号，重写
if "SP.POP.TOTL" not in sr["today"].split("乌兹别克斯坦")[1][:80]:
    D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
    def g(c,k):
        r=D[c][k]
        return f"{int(r['value']):,} 人（{r['year']}年）" if k=="pop_total" else f"{r['value']:.1f}%（{r['year']}年）"
    sr["today"]=(f"以哈萨克斯坦与乌兹别克斯坦为例，来源：世界银行 API。哈萨克斯坦总人口 {g('KAZ','pop_total')}（SP.POP.TOTL）、"
      f"城市化率 {g('KAZ','urban_pct')}（SP.URB.TOTL.IN.ZS）；乌兹别克斯坦总人口 {g('UZB','pop_total')}（SP.POP.TOTL）、"
      f"城市化率 {g('UZB','urban_pct')}（SP.URB.TOTL.IN.ZS）。上述为两国全国口径数据，仅示量级；"
      "丝路沿线货运量与过境流量需专门统计核验。")
sr["last_update"]=TODAY

# 6) status 标签统一：notes 写「命中0/未达标」的条目不用「实证」
for e in T.values():
    pn=e.get("pending_notes") or ""
    st=e.get("status") or ""
    if "·实证" in st and ("未达标" in pn or "命中 0" in pn or "命中0" in pn):
        e["status"]=re.sub(r"已复核\(第(\d+)轮·实证\)", r"已复核(第\1轮·无实证)", st)

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成")