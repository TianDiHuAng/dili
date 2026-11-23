# -*- coding: utf-8 -*-
"""第36轮返工：修 fmt 解包序（22条 today 写成指标编号）、POV 口径、能源转型 geo、未译句等。"""
import json,os,sys,re,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
W=json.load(open(os.path.join(ROOT,"reports","round36_wb.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
SRC={s["id"]:s for s in sd["sources"]}

def disp(name):
    d=W[name];v=float(d["value"]);c=d["code"]
    if c=="SP.POP.TOTL": return f"{int(v):,} 人"
    if c=="SP.DYN.LE00.IN": return f"{v:.1f} 岁"
    if c in ("NY.GDP.PCAP.CD","NY.GNP.PCAP.CD"): return f"{v:,.0f} 美元"
    if c=="EN.GHG.CO2.MT.CE.AR5": return f"{v:,.2f} Mt CO₂e"
    if c=="ER.FSH.PROD.MT": return f"{v:,.0f} 吨"
    if c in ("AG.YLD.CREL.KG","AG.CON.FERT.ZS"): return f"{v:,.1f} 千克/公顷"
    if c=="SH.DYN.MORT": return f"{v:.1f}‰"
    if c=="SP.POP.GROW": return f"{v:.2f}%"
    return f"{v:.1f}%"

# 修正 POV 口径（官方：$3.00/2021 PPP）
POV_FIX={"title":"World Bank API — 贫困人口比例（$3.00/日，2021 PPP）(SI.POV.DDAY, 全球)",
         "label":"贫困人口比例（每日 3.00 美元以下，2021 PPP，%）"}
n=0;fixed=[]
for name,d in W.items():
    e=T.get(name)
    if not e: continue
    if name not in T: continue
    code=d["code"];v=disp(name)
    label=d["label"]
    if code=="SI.POV.DDAY": label=POV_FIX["label"]
    # 重写 today
    if name=="全球气温变化":
        e["today"]=("来源：NOAA Climate at a Glance（全球陆海平均温度距平，基准期 1901–2000，单位 °C）："
          "2023年 +1.17、2024年 +1.26、2025年 +1.12。距平值随基准期与观测方法而变，跨数据集比较须核对口径；"
          "单年数值受自然变率影响，不应直接当作长期趋势。")
    elif name=="撒哈拉以南非洲发展数据":
        v2=f"{int(d['value']):,} 人"
        e["today"]=(f"来源：世界银行 API（指标 {code}，总人口）：撒哈拉以南非洲 {v2}（{d['year']}年）。"
          "该值为区域合计，掩盖区域内部差异（沿海与矿产国、内陆萨赫勒国家、岛国相距悬殊），跨国/跨区比较须核对口径。")
    else:
        e["today"]=(f"来源：世界银行 API（指标 {code}，{label}）：全球 {v}（{d['year']}年）。"
          "该值为全球合计或均值，掩盖国家与区域间的巨大差异，跨国比较须核对口径。")
    # 重写 pending 中的「实测 …」
    pn=e.get("pending_notes") or ""
    pn=re.sub(r"实测 \S+（\d{4}年）", f"实测 {v}（{d['year']}年）", pn)
    pn=pn.replace("实测 wb", "实测 ")
    e["pending_notes"]=pn.replace(f"实测 {code}（{d['year']}年）", f"实测 {v}（{d['year']}年）")
    e["last_update"]=TODAY;n+=1;fixed.append(name)

# 源 note 里的值
for s in sd["sources"]:
    if s["id"].startswith("wb-wld-") or s["id"].startswith("wb-ssf-"):
        for name,d in W.items():
            if d["code"].lower().replace(".","-") in s["id"]:
                s["note"]=re.sub(r"最新 \S+（\d{4}年）", f"最新 {disp(name)}（{d['year']}年）", s.get("note") or "")
                break
# POV 源标题/口径
for s in sd["sources"]:
    if s["id"]=="wb-wld-si-pov-dday":
        s["title"]=POV_FIX["title"];s["page_title"]=POV_FIX["title"]
        s["note"]=(s.get("note") or "")+" 【口径】该指标官方名为「Poverty headcount ratio at $3.00 a day (2021 PPP)」；2021 PPP 修订后与旧版（$2.15/2017 PPP）贫困率不可直接比较。"

# 能源转型 geo 与指标矛盾修正
en=T.get("能源转型")
if en:
    en["geo"]=("转型速度在地区间差异极大，但**「可再生能源占比」不能区分传统生物质与现代可再生能源**："
      "撒哈拉以南非洲的高占比主要来自薪柴与木炭等传统生物质，欧洲的高占比主要来自水、风、太阳能等现代来源。"
      "因此本指标不宜直接用作「转型速度」的排序依据；需同时看现代可再生能源的绝对量与电力部门结构。")
    en["pending_notes"]=((en.get("pending_notes") or "")+
      " 【第36轮返工】原 geo 称「撒南仍以生物质为主」易被读成其占比低——实测 SSF 该指标 2020 年为 70.3%，高于欧盟 21.1% 与全球 19.7%；"
      "已改写为「高占比不等于现代可再生能源占比高」，避免与指标直接矛盾。").strip()

# 海洋保护区未译句
mp_=T.get("海洋保护区")
if mp_:
    mp_["geo"]=(mp_.get("geo") or "").replace("高 seas","高公海（high seas）").replace("公海与高公海（high seas）","公海（high seas）")
    mp_["pending_notes"]=((mp_.get("pending_notes") or "")+" 【第36轮返工】geo 残留未译「high seas」，已改为「公海（high seas）」。").strip()

# 湿地补 internal 口径
wl=T.get("湿地与水资源")
if wl:
    W2=json.load(open(os.path.join(ROOT,"reports","round36_wb2.json"),encoding="utf-8"))
    d=[x for x in W2.values() if x["code"]=="ER.H2O.INTR.PC"]
    wl["today"]=("来源：世界银行 API（指标 ER.H2O.INTR.PC，人均**内部**可再生淡水资源，单位立方米）："
      f"全球 {d[0]['value']:,.0f} 立方米（{d[0]['year']}年）。该口径为「内部」可再生资源，不含境外来水；"
      "跨国比较须核对是否含跨境水量。")

# 北美原住民补 2017 文结论
na=T.get("北美原住民")
if na:
    na["influence"]=(na["influence"]+
      " 关于首次进入的时间，该 2017 年研究指出：就现有证据的总体权重而言，人类首次进入北美约在 **14,000 cal BP**，"
      "即末次盛冰期之后——Bluefish Caves 更早的测年因此仍属存疑证据，而非定论。")

for u,dd in docs.items(): json.dump(dd,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("修复 today:",n,"条；含能源转型geo/海洋保护区/湿地/北美原住民")
print("样例 极端贫困:",T["极端贫困空间分布"]["today"][:110])
print("样例 全球人口规模:",T["全球人口规模"]["today"][:110])