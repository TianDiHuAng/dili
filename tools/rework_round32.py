# -*- coding: utf-8 -*-
"""第32轮返工：修 5 条事实/口径/双源问题 + 渲染标签 + R15 扩词。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 阿兹特克：回填 verified + 精度 + 1367 说明
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
    if s["id"]=="wikidata-q2608489":
        s["verified"]=True; s["link_ok"]=True
        s["note"]=("Wikidata 实体 Q2608489；英文描述「former Mesoamerican empire」；"
          "P571=1325（精度=年）、P576=1521-08-13（精度=日）、P580=1367（精度=年）、P2046=300000 km²。"
          "第32轮返工复抓 HTTP 200 回填（此前 429 未核验）。众包数据，仅作双源之一。")
    if s["id"]=="wikidata-q7209":
        s["note"]=("Wikidata 实体 Q7209；英文描述「imperial dynasty in China from **202 BC** to 220 AD」；"
          "P571=-0206（精度=年）、P576=+0220（精度=年）。**注意：描述写 202 BC 与 P571 的 206 BC 不一致**（汉元年/受封汉王 vs 称帝）。"
          "第32轮复抓 HTTP 200。众包数据，仅作双源之一。")
    if s["id"]=="wikidata-q12557":
        s["note"]=("Wikidata 实体 Q12557；英文描述「13th- and 14th-century empire originating in Mongolia」；"
          "P571=1206（精度=年）、P576=1368（精度=年）。**1368 为元朝终年**；帝国自 1260 年起分裂、1294 年成四汗国。第32轮复抓 HTTP 200。")
    if s["id"]=="wikidata-q5413":
        s["note"]=("Wikidata 实体 Q5413（长江，非「长江流域」）；英文描述「longest river in Asia and third-longest in the world」；"
          "P2043=6300 千米（精度=1）。**该值为河流长度，不是流域面积**；流域实体 Q15758768 在 Wikidata 无面积属性。")
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 2) 印度河文明：数值订正（2025 = 255,219,554）
ind=T["印度河文明"]
ind["today"]=ind["today"].replace("251,269,164 人（2025年）","255,219,554 人（2025年）")
ind["pending_notes"]=((ind.get("pending_notes") or "")+
  " 【第32轮返工】today 巴基斯坦人口由 251,269,164 订正为 255,219,554（2025年）——原值实为 2024 年数据（来源 note 记的正是 255219554/2025）。").strip()
ind["last_update"]=TODAY

# 3) 汉代：年代口径
han=T["汉代"]
han["polities"]=("据 Wikidata 结构化记录，P571（成立）= 前206年、P576（解散）= 220年。"
  "**口径需说明**：前206 为汉元年（刘邦受封汉王）；秦亡于前207；通说以刘邦称帝（前202）为汉朝建立。"
  "同一 Wikidata 实体的英文描述写「from **202 BC** to 220 AD」，与 P571 的 206 BC 并不一致。"
  "西汉—新朝—东汉的帝系与年号待专门史学来源逐条核验。")
han["time_or_place"]="前206年–220年（Wikidata P571/P576，精度=年；通说建朝为前202年，口径差异见正文）"
han["pending_notes"]=((han.get("pending_notes") or "")+
  " 【第32轮返工】补年代口径：前206=汉元年/受封汉王、秦亡前207、通说建朝前202；并注明 Wikidata 自身描述写 202 BC 与 P571 的 206 BC 不一致。删除「中间有新朝中断」无源断言。").strip()
han["last_update"]=TODAY

# 4) 蒙古帝国：时序修正
mon=T["蒙古帝国"]
mon["polities"]=("据 Wikidata 记录，P571（成立）= 1206年、P576（解散）= 1368年。"
  "**时序需说明**：帝国自 1260 年忽必烈与阿里不哥之争后实际分裂，1294 年形成多个汗国；"
  "1368 年是元朝（中国部分）终结之年，并非全帝国同时终止。大汗世系与各汗国年代待专门史学来源核验。")
mon["connections"]="驿站网络把东亚、中亚、波斯与东欧连成一体，商队、使节与技术沿此流动；就欧亚陆路连通的规模而言，是前现代最显著的一次。"
mon["pending_notes"]=((mon.get("pending_notes") or "")+
  " 【第32轮返工】修时序：1368 为元朝终年，分裂起于 1260、四汗国成于 1294，原「其后分化为多个汗国」时序颠倒已改；「首次大规模连通」改为「前现代最显著的一次」（避免无源最高级断言）。").strip()
mon["last_update"]=TODAY

# 5) 阿兹特克：精度与 1325/1367/1430
az=T["阿兹特克"]
az["polities"]=("据 Wikidata 记录，P571（成立）= 1325年、P576（解散）= 1521年8月13日（精度到日）；同实体另记 P580（起始）= 1367年。"
  "**口径需说明**：1325 为特诺奇蒂特兰传统建城年，1367 为另一时间属性，三方联盟（特诺奇蒂特兰、特斯科科、特拉科潘）通常置于 15 世纪上半叶。"
  "三个时间点含义不同，不可互换；统治者序列与贡赋制度待专门史学来源核验。")
az["time_or_place"]="1325年–1521年8月13日（Wikidata P571/P576；P571 精度=年、P576 精度=日）"
az["pending_notes"]=((az.get("pending_notes") or "")+
  " 【第32轮返工】① 来源 wikidata-q2608489 原 verified=false（429），复抓 200 后回填；② 修正精度标注（P576 精度=日）；③ 补 P580=1367 与「1325 建城 / 1430 前后三方联盟」的口径关系。").strip()
az["last_update"]=TODAY

# 6) 长江流域：标明河长≠流域面积
yz=T["长江流域"]
yz["time_or_place"]="长江全长约6300千米（Wikidata P2043，精度=1千米；**该值为河流长度，非流域面积**）"
yz["geo"]=("流域自青藏高原发源，经四川盆地、长江中下游平原注入东海，跨越高原、盆地与平原多种地貌。"
  "水量丰沛、湖泊与支流众多，中下游形成密集水网与洪泛平原。"
  "**量值说明**：本条引用的 Wikidata 数值是长江**河流长度**（约6300千米），流域**面积**在本环境可获得的结构化数据中缺失，待专门水文来源核验。")
yz["pending_notes"]=((yz.get("pending_notes") or "")+
  " 【第32轮返工】① 明确标注所引 6300 千米为**河流长度**而非流域面积（流域实体 Q15758768 在 Wikidata 无面积属性）；② 删除「通过大运河与黄河流域整合」无源断言；③ fao-aquastat-basins 为流域目录页（无单流域正文），不作数值支撑。").strip()
yz["connections"]="通过长江口与沿海港口连接海上贸易网络，形成内陆—沿海双重联系；与黄河流域的历史联系待专门史料核验。"
yz["last_update"]=TODAY

# 7) 5 条统一标注「单源待互证」
for t in ("汉代","蒙古帝国","阿兹特克","长江流域","印度河文明"):
    e=T[t]
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【单源待互证】本条关键年代/量值目前**仅有 Wikidata 一处结构化来源**（DBpedia 与 Britannica/Wikipedia 在本环境均不可达），"
      "按 TASK 规则标为待核实；机构页（UNESCO Culture 首页、FAO 门户）与国情端点不构成第二独立印证。需补专题或学术来源后转为双源。").strip()
    e["needs_verification"]=True

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("5 条返工完成")