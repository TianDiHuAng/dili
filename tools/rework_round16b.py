# -*- coding: utf-8 -*-
"""第16轮二次返工：
- 阿契美尼德波斯：状态改为 L2·D041配对缺口并加 coverage 标记；回填 outlines；措辞微调。
- livius-cyrus note 命中 69→62 并注明剥离规则。
- 删除自指句（theme 说明）。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 阿契美尼德波斯
a=T["阿契美尼德波斯"]
a["definition"]="阿契美尼德波斯：以波斯本土（安尚一带）为起家核心的古代帝国，居鲁士与大流士时期扩展到两河、安纳托利亚、埃及与中亚边缘。"
a["overview"]="以波斯本土（安尚一带）为起家核心的古代帝国，居鲁士与大流士时期扩展到两河、安纳托利亚、埃及与中亚边缘。"
a["polities"]="Livius 的居鲁士专题页记载其兴起、巴比伦与安纳托利亚等地的扩张，并述及被称为 satrap 的附庸王；王表与年代序列待专门史料逐条核验。"
a["connections"]="帝国与两河流域、安纳托利亚、埃及及中亚边缘存在军事联系，并通过附庸王安排维持地方统治；对印度河谷的控制不成立，相关说法已删除。"
a["outlines"]=["Livius: Cyrus the Great","Livius: Mesopotamia"]
a["status"]="L2·D041配对缺口(第16轮)"
a["pending_notes"]="第16轮二次返工：① 五段已收敛到 Livius Cyrus 实证范围（删驿道/行省制度/三大洲/度量衡/印度河征服等无源断言）；② 专题页 D044 口径：正文 9220 字符、正则 achaemenid|cyrus|persia 命中 62（剥离 nav/header/footer/aside/script/style/form/noscript）；③ **D041 配对缺口**：本机可达的机构页实测 8 个候选全部不可用（UNESCO WHC/Met/Smithsonian/Iranica/Britannica/British Museum 403 或不通，Penn Museum 0 命中），故本条暂标「配对缺口」，待可核验机构页到位后转正；④ livius-mesopotamia 正文 3630 字符（<8000），仅作区域背景。"
a["last_update"]=TODAY

# 2) 删除自指句
for t in ["拉丁美洲与加勒比区域发展","中东与北非区域发展","南亚区域发展","全球气温距平","二氧化碳排放清单","农业企业与价值链"]:
 e=T.get(t)
 if not e: continue
 e["pending_notes"]=(e["pending_notes"] or "").replace(" theme 受现有枚举限制，实际维度见 region/主题注释。","")

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# coverage 标记 d041_pairing_gap
cp=os.path.join(DATA,"coverage.json");cov=json.load(open(cp,encoding="utf-8"))
for c in cov["entries"]:
 if c["id"]==T["阿契美尼德波斯"]["id"]:
  c["d041_pairing_gap"]=True
  c.pop("d041_legacy",None)
cov["d041_pairing_gap_count"]=sum(1 for c in cov["entries"] if c.get("d041_pairing_gap"))
cov["d041_legacy_count"]=sum(1 for c in cov["entries"] if c.get("d041_legacy"))
json.dump(cov,open(cp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 3) livius-cyrus note 修正
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
 if s["id"]=="livius-cyrus":
  s["note"]=("curl 实测 HTTP 200；页面标题：Cyrus the Great - Livius；"
   "D044 剥离口径（去 nav/header/footer/aside/script/style/form/noscript）正文 9220 字符、"
   "正则 achaemenid|cyrus|persia 命中 62；未剥离 chrome 计数为 69，按 D044 不采用。")
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("阿契美尼德→配对缺口；自指句清理；note 62；legacy",cov["d041_legacy_count"],"pairing",cov["d041_pairing_gap_count"])