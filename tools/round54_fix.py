# -*- coding: utf-8 -*-
"""第54轮：修 R19 抓出的 6 条（弱来源被称主来源）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
sd=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

FIX={
"突厥":("openalex-W4384485896","旁证（被引0、摘要619字符<800）",
  "该章节只能说明「有研究给出 552–745 这一年代区间」，不能作为年代断言的唯一依据；具体的汗国世系与分裂过程仍待突厥史专著（如 Golden 的通史类著作）。"),
"意大利半岛":("openalex-W4298223504","旁证（摘要693字符截断、无结论句）",
  "该摘要于 693 字符处截断，未含结论句；仅可说明「有基于 1:250,000 实测图的中南部亚平宁构造研究」，全半岛的地质结论须读全文或另引综述。"),
"文艺复兴意大利":("openalex-W2487072270","旁证（摘要660字符<800）",
  "该摘要较短（660 字符），仅可作「城邦危机与区域国家形成」的提示，不能作为本条政治背景的唯一依据。"),
"美国西进":("openalex-W3023324006","旁证（被引0）",
  "该文被引 0，仅可作「西进使版图从大西洋岸延伸至太平洋岸」这一概述的旁证。"),
"河流三角洲":("openalex-W2034581965","旁证（被引5、摘要661字符<800）",
  "该摘要较短，仅支撑「河口沙坝形成与前积」的模型讨论，不作三角洲成因的定论。"),
"地理信息系统":("openalex-W4230464905","旁证（被引4、设计类工程文）",
  "该文属 SDSS 概念设计（被引4），仅作「以 GIS 为底座的空间决策支持系统一例」，不作 GIS 能力的通例断言；主来源待补 GIS 综述类文献。"),
}
n=0
for t,(sid,newtail,why) in FIX.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    # 把该段里的「补主来源」改为「补弱来源」
    pn=re.sub(rf"(【[^】]*)补主来源([^】]*】{re.escape(sid)})", r"\1补弱来源\2", pn)
    pn=re.sub(rf"(【[^】]*)补主来源([^】]*?{re.escape(sid)})", r"\1补弱来源\2", pn)
    # 若仍未改（段落顺序不同），做全局替换该 sid 前的「补主来源」
    if f"补主来源" in pn and sid in pn:
        idx=pn.find(sid)
        head=pn[:idx]; tail=pn[idx:]
        head=head.replace("补主来源","补弱来源")
        pn=head+tail
    e["pending_notes"]=(pn+f" 【第54轮D112降级】{sid} 为**{newtail}**，不得称「主来源」；{why}").strip()
    e["last_update"]=TODAY;n+=1
save_docs(docs)
json.dump(sd,open(os.path.join(DATA,"sources.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=54
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("降级",n,"条")