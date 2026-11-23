# -*- coding: utf-8 -*-
"""第34轮：筛选 OpenAlex 候选中「摘要明确含该条年代/量值」的文献。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O=json.load(open(os.path.join(ROOT,"reports","round34_openalex.json"),encoding="utf-8"))
# 各条的年代/量值关键词（须在摘要中出现其一）
NEED={
"蒙古帝国":["1206","1368","13th","14th"],
"阿兹特克":["1325","1521","Aztec empire","Triple Alliance"],
"印度河文明":["Indus","3000","2600","1900","1800","Bronze Age"],
"库什与努比亚":["Kush","Nubia","Meroe","Napata"],
"桑海帝国":["Songhai","1464","1591"],
"笈多王朝":["Gupta","320","550"],
"丝绸之路":["Silk Road","trade"],
"汉代":["Han dynasty","206 BC","202 BC","220"],
"秦代":["Qin","221","206"],
"元代":["Yuan","1271","1368"],
"古埃及新王国":["New Kingdom","1550","1570","1070"],
"罗马阿非利加":["Roman Africa","province","Carthage"],
"阿拉伯半岛":["Arabian Peninsula"],
}
def norm(s): return (s or "").lower()
res={}
for title,cands in O.items():
    if not isinstance(cands,list) or not cands: continue
    keys=NEED.get(title,[])
    good=[]
    for c in cands:
        ab=norm(c.get("abstract"));ti=norm(c.get("title"))
        hit=[k for k in keys if norm(k) in ab or norm(k) in ti]
        # 标题须含条目核心词，且摘要命中至少 1 个年代/主题词
        core=norm(keys[0]) if keys else ""
        if not core: continue
        if core in ti and len(hit)>=1 and len(c.get("abstract") or "")>=300:
            good.append({**c,"matched":hit,"score":(2 if core in ti else 0)+len(hit)})
    good.sort(key=lambda x:-x["score"])
    res[title]=good
    if good:
        g=good[0]
        print(f"OK {title:<12} {len(good)}条 | {g['year']} 「{(g['title'] or '')[:56]}」 matched={g['matched']}")
    else:
        print(f"-- {title:<12} 无合格候选（标题含核心词且摘要含年代者）")
json.dump(res,open(os.path.join(ROOT,"reports","round34_screened.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n合格条目:",sum(1 for v in res.values() if v))