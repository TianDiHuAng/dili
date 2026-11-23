# -*- coding: utf-8 -*-
"""第39轮返工：罗斯海定义/科考站结论/横贯山脉期刊与方位/probe记录4处口径/探测留痕/台账。"""
import json,os,sys,re,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== 1 罗斯海：删「最深」，补冰架限定，补 D089 限定 =====
rs=T["罗斯海"]
rs["definition"]="罗斯海：南太平洋扇形海域，向南深深嵌入南极大陆轮廓，南接罗斯冰架。"
rs["overview"]=("罗斯海向南深深嵌入南极大陆轮廓，南接罗斯冰架，水域面积广大、以陆架为主（Britannica 记约 37 万平方英里，属较浅的边缘海）。"
  " 本条以海洋观测研究为机制依据，不据其推断地形。")
rs["influence"]=("所引 2002 年研究以近四十年的海洋观测（南极附近最长的记录之一）指出：陆架水盐度与罗斯环流表层盐度明显下降（淡化），"
  "同期罗斯岛大气增温、陆架以北约300米深处海水增温、南方涛动指数更偏负，并伴有**东南太平洋冰架**的减薄。"
  "原文认为淡化可能由多个因素共同造成；本条只陈述这些变化同向出现，不将其写作已确立的单一因果。")
rs["pending_notes"]=((rs.get("pending_notes") or "")+
  " 【第39轮返工·硬错】原 definition/overview 写「南极洲附近最深的边缘海」——Britannica 原文为 deep indentation（深入陆地的湾）"
  "与 shallow marine region（较浅边缘海），我把前者误读为「水深最深」，结论与来源相反，已改写。"
  "另「冰层减薄」补「东南太平洋冰架」限定（摘要原文 southeast Pacific ice shelves），避免读成罗斯海冰架。"
  " 【D089限定】本条 theme 为地形，所引文献为海洋水文观测，仅作该海域海洋侧面的一例，不作地形解释依据。").strip()
rs["last_update"]=TODAY

# ===== 2 南极科考站：结论纠反 =====
ks=T["南极科考站"]
ks["influence"]=("所引 2009 年研究由瑞典极地研究秘书处发起，就南极 28 国站点的废水与灰水处置实践做问卷普查（2005年秋发出）。"
  "其核心发现是：**37% 的常年站与 69% 的夏季站尚无任何形式的处理设施**。作者据此认为技术已具备、"
  "应全面采用处理设施并防止夏季站未经处理排放，即**治理仍是未完成的缺口**。")
ks["pending_notes"]=((ks.get("pending_notes") or "")+
  " 【第39轮返工·硬错】原稿写「科考站的环境管理已成为南极治理的一部分」——与摘要结论方向相反：摘要结论是多数站点仍无处理设施、"
  "治理属未完成缺口（37%/69%）。已按摘要改写并补入实数。"
  " 【D089限定】本条 theme 为贸易，所引文献领域为环境管理，仅作站点运营现状一例，不作贸易/定居解释依据。").strip()
ks["last_update"]=TODAY

# ===== 3 横贯南极山脉：期刊名、长度主体、方位 =====
tm=T["横贯南极山脉"]
tm["definition"]="横贯南极山脉：横贯南极大陆、分隔东南极与西南极的山脉。"
tm["geo"]=("山脉沿东南极与西南极的边界延伸。以罗斯海—罗斯冰架一侧与东南极冰盖一侧来定位更准确："
  "山脉构成东南极的东缘，其东侧与紧邻处为维多利亚地盆地；威尔克斯盆地位于山脉以西（后方）约400–500千米。"
  "山体被冰盖覆盖，仅山脊与少数冰原岛峰出露。")
tm["influence"]=("所引 1989 年研究指出，该山脉形成于东南极与西南极的陆—陆边界；高热流、薄地壳、正断层与火山活动表明"
  "这条边界具有张裂性质，并发育出横贯南极山脉、威尔克斯盆地与维多利亚地盆地三个主要构造。"
  "**长度口径**：该研究所称「约3000千米」是**这条边界**的长度；山脉本身的长度不同源表述不一（Britannica 记逾3200千米），本条不合并两者。")
tm["connections"]=("山脉把东南极冰盖与西南极冰盖分隔，影响冰流路径；罗斯海一侧为罗斯冰架，是南极物质平衡研究的关键区。")
tm["pending_notes"]=((tm.get("pending_notes") or "")+
  " 【第39轮返工】① 期刊名订正：OpenAlex `display_name` 记「Journal of Geophysical Research Atmospheres」，"
  "但 Crossref container-title 与 raw_source_name 均为 **Journal of Geophysical Research: Solid Earth**（DOI 段 jb094ib08 亦属 JGR B），"
  "属 OpenAlex 字段缺陷，已按 Crossref 订正。② 「约3000千米」原写在 definition/geo 描述山脉全长，实为**边界**长度，已区分。"
  "③ 方位由「北侧/南侧」改为「罗斯海—罗斯冰架一侧／东南极冰盖一侧」，并补威尔克斯盆地位于山脉以西400–500千米。").strip()
tm["last_update"]=TODAY

# 来源 note 订正
for s in sd["sources"]:
    if s["id"]=="openalex-W2091566445":
        s["note"]=(s.get("note") or "").replace("Journal of Geophysical Research Atmospheres",
          "Journal of Geophysical Research: Solid Earth")
        s["note"]=(s.get("note") or "")+" 【第39轮订正】OpenAlex display_name 作「Atmospheres」系历史 ISSN 归并造成的字段缺陷；Crossref container-title 与 raw_source_name 均为 Solid Earth。"

# ===== 4 probe.json 4 处口径误述 =====
rp=os.path.join(ROOT,"reports","round39_probe.json")
rep=json.load(open(rp,encoding="utf-8"))
rep["world_bank_tested"]={
 "ER.BDV.TOTL.ZS":"**指标 ID 无效**（API 返回 Invalid value）；对应「受威胁鸟类种数」为 EN.BIR.THRD.NO（CHN 2022=94 有值）",
 "SI.POV.URBN.ZS":"**指标 ID 无效**；城市贫困在 1.2.HCount.* 系列有值",
 "EN.CLC.MDAT.ZS":"**有值**：仅 2009 年（口径为 1990–2009 年受灾人口平均占比），与当代风险口径不符，故不采用",
 "IQ.CPA.ENVR.XQ":"**仍在更新**（Kenya 2025=4、2024=3.5）；口径为 CPIA 国别评分，与「环境治理」综合口径不符，故不采用",
 "IS.ROD.TOTL.KM":"值域 1990–2010，停更成立",
 "EN.ATM.PM25.MC.M3":"有值；口径为 PM2.5 年均暴露，与热岛强度不符（D077）",
 "AG.LND.FRST.ZS":"有值；口径为森林覆盖率，与火灾生态不符（D077）"}
rep["openalex_status"]=("**搜索端点间歇 429**（12:04、12:15 实测 429；12:12 前后有 7 个主题取到结果并存于 round39_openalex.json）；"
  "单作品端点 works/{id} 正常（200）。其余 11 个主题未取得记录，且当时的取数脚本未落盘 HTTP 状态，故「429」与「返回但无标题匹配」在仓库内不可区分——下轮已加留痕。")
rep["corrections"]="本文件第39轮首版把 4 项世行指标误述为「无值」或「已停更」，经抽检核实后订正；错误已同步回改 4 条条目的 pending_notes。"
json.dump(rep,open(rp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 4 条条目 pending_notes 同步
FIX={"生物多样性分布":"世界银行无有效对应指标（ER.BDV.TOTL.ZS 为无效 ID；对应的 EN.BIR.THRD.NO 为物种数而非分布格局），故不采用。",
"城市贫困":"世界银行 SI.POV.URBN.ZS 为无效 ID（城市贫困实际在 1.2.HCount.* 系列），口径与「空间分布」亦不完全对应，故不采用。",
"自然灾害风险":"世界银行 EN.CLC.MDAT.ZS 有值但仅覆盖 2009 年（1990–2009 平均口径），与当代风险口径不符，故不采用。",
"环境治理":"世界银行 IQ.CPA.ENVR.XQ 仍在更新（2024/2025），但口径为 CPIA 国别评分，与「环境治理」综合口径不符，故不采用。"}
for t,txt in FIX.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    pn=re.sub(r"世界银行[^。]*。", "", pn, count=1)
    e["pending_notes"]=(pn+txt).strip()
    e["last_update"]=TODAY

# 补 D081 单源声明
for t in ("横贯南极山脉","罗斯海","南极科考站"):
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【D081单源声明】britannica-regions（UNSD M49）与 wikipedia-regions（UNSDG 门户壳页）为壳别名，s010-unesco-org 为 UNESCO Culture 首页、与本条无关；"
      "三者均不构成独立内容依据，本条实质为**单源（OpenAlex）**。").strip()

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=39;cov["round_processed"]=3
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("返工完成：罗斯海/科考站/横贯山脉/probe 4处/单源声明/台账")