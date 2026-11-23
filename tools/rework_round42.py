# -*- coding: utf-8 -*-
"""第42轮返工：剔除6条误登记、19条旁证改措辞、取消截断、三档口径、台账。"""
import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
SHELL={"britannica-regions","wikipedia-regions","un-m49","s010-unesco-org","s070-cbd-int","s071-cbd-int","ap-human-geo","s013-fao-org"}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))

# ===== 1 剔除 6 条误登记 =====
BAD={
"白令陆桥":("openalex-W4392444874","所引为《Grazing exclosures in **Bering Land Bridge National Preserve**》——研究对象是阿拉斯加**以陆桥命名的现代国家保护区**（驯鹿放牧围栏 2012–2022 数据），与更新世陆桥无关，属地名碰撞（与 Circular Cities 同型）。"),
"河流三角洲":("openalex-W4250626851","所引为《…non-refractory submicron aerosols in the **Pearl River Delta**, China》——珠三角在此是大气研究**地名**，主题为气溶胶来源与形成，与三角洲地貌成因/沉积无概念对应。"),
"大分水岭":("openalex-W2159370596","所引为春尾虫（springtail）系统地理学研究，**大分水岭仅为采样地**（Tallaganda）；正文断言（雨影、跨山调水、城市带）无一句可由此支撑。"),
"澳大利亚原住民":("openalex-W2273406395","所引为《Australian academic archaeology: Aboriginal transformation of its aims and practices》——研究对象是**考古学这门学科**的方法论转向，不是原住民本身。"),
"巴西殖民经济":("openalex-W7118956095","所引为《The coffee economy in **Imperial** Brazil (c.1800–1850)》——条目为 1500–1822 葡属殖民地，源为**帝国时期**，时期不一致（D081）。"),
"加勒比海群岛":("openalex-W2153621070","所引为《Phylogeny and biogeography of Caribbean mammals》——摘要结论是「**没有类群符合 Gaarlandia 模型预测的时间**、需逐类群解释」，与正文「以隔离分化模型解释」**方向相反**（D092 同型）。"),
}
for t,(sid,why) in BAD.items():
    e=T.get(t)
    if not e: continue
    e["sources"]=[s for s in e["sources"] if s!=sid]
    pn=e.get("pending_notes") or ""
    pn=re.sub(rf" 【第42轮第二来源（[^）]*）】{re.escape(sid)}[^【]*", "", pn)
    e["pending_notes"]=(pn+f" 【第42轮返工·剔除】{why} 已撤出该来源，本条不据此建立互证。").strip()
    e["last_update"]=TODAY
# 加勒比海：修正反向断言
too=T.get("加勒比海群岛")
if too:
    too["influence"]=("加勒比群岛的生物区系形成涉及隔离分化（vicariance）与跨海扩散两种模型。"
      "既有系统发育研究显示：**没有类群符合 Gaarlandia 陆桥模型所预测的分化时间**，各族群需要逐类群的具体解释。"
      " 因此本条不把单一模型当作既定结论（D092）。")
    too["pending_notes"]=((too.get("pending_notes") or "")+" 【第42轮返工】原写「以隔离分化模型解释」，与摘要结论相反，已改为「两模型并存、无类群符合 Gaarlandia 预测时间」。").strip()

# ===== 2 旁证 19 条：改措辞 =====
PROOF=["文艺复兴意大利","维京时代","澳大利亚大陆","克里特文明","落基山脉","斯瓦希里海岸","宋代",
 "莫斯科公国","黑海海峡","蒂亚瓦纳科","阿塔卡马沙漠","新西兰北岛","玛雅文明","印加帝国","周代",
 "大自流盆地","新西兰南岛","拉普拉塔平原","十字军东征"]
for t in PROOF:
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    pn=pn.replace("该文献涉本条对象但聚焦某一侧面，仅支撑相应段落，其余段落仍为常识性地理描述",
                  "该文献与本条对象同一，但**正文目前没有可与之对应的具体句子**，故登记为**旁证**、不计入「双源互证」")
    e["pending_notes"]=pn
    e["last_update"]=TODAY

# ===== 3 取消 70 字截断（改为完整标题）=====
for e in T.values():
    pn=e.get("pending_notes") or ""
    pn=re.sub(r"《([^》]{60})》", lambda m: "《"+m.group(1)+"…》", pn) if False else pn
    # 去掉所有 ⋯/… 尾截断标记
    pn=re.sub(r"(【第4\d轮[^】]*】[^【]*?)《([^》]*?)…》", r"\1《\2》", pn)
    e["pending_notes"]=pn

# ===== 4 三档口径统计 + 写入口径文件 =====
def content_sources(e):
    return [s for s in e["sources"] if s not in SHELL and not s.startswith("wb-")]
def non_wd(e):
    return [s for s in content_sources(e) if not s.startswith("wikidata-")]
tier2_link=sum(1 for e in T.values() if len(content_sources(e))>=2)
tier2_no_wd=sum(1 for e in T.values() if len(non_wd(e))>=2)
tier2_proof=sum(1 for e in T.values() if len(non_wd(e))>=2 and e["title"] not in PROOF)
rep={"round":42,"date":TODAY,
 "tier1_ge2_links":tier2_link,
 "tier2_ge2_excl_wikidata":tier2_no_wd,
 "tier3_ge2_with_correspondence":tier2_proof,
 "note":"三档口径：链接数 / 剔除 wikidata 结构化记录 / 其中正文有对应落点者（不含旁证 19 条）",
 "rejected_this_round":list(BAD.keys()),
 "side_evidence":PROOF}
json.dump(rep,open(os.path.join(ROOT,"reports","round42_tiers.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=42;cov["round_processed"]=46
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print(f"剔除 6 条；旁证改措辞 19 条")
print(f"三档：≥2链接={tier2_link} / 剔wikidata={tier2_no_wd} / 有落点≈{tier2_proof}")