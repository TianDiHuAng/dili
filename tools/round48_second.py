# -*- coding: utf-8 -*-
"""第48轮 B1：为 14 条政权类仅1内容源条目按 D101 检索第二源（含替换错源）。"""
import subprocess,json,os,urllib.parse,time,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 条目: (待支撑断言, 检索式, 必须命中的槽位词, 标题须含的对象词)
Q={
"汉代":("汉代帝国的疆域与行政","Han empire territory administration",["han","empire"],"han"),
"蒙古帝国":("蒙古帝国的驿站与跨欧亚联系","Mongol empire postal relay yam system",["mongol","empire"],"mongol"),
"阿兹特克":("阿兹特克三方联盟与贡赋","Aztec empire triple alliance tribute",["aztec","alliance"],"aztec"),
"城市起源":("城市起源的机制解释","urban revolution earliest cities Mesopotamia",["urban","cit"],
        "city"),
"古埃及新王国":("新王国的帝国扩张与行政","New Kingdom Egypt empire administration",["new kingdom","egypt"],"egypt"),
"库什与努比亚":("库什王国的麦罗埃时期","kingdom of Kush Meroe",["kush","meroe"],"kush"),
"罗马阿非利加":("罗马阿非利加行省的粮食产出","Roman Africa province grain production",["africa","roman"],"africa"),
"加纳帝国":("加纳帝国的黄金贸易","Ghana empire trans-Saharan gold trade",["ghana","gold"],"ghana"),
"桑海帝国":("桑海帝国与尼日尔河航运","Songhai empire Niger river trade",["songhai","niger"],"songhai"),
"笈多王朝":("笈多王朝的政治与文教","Gupta empire polity culture",["gupta","empire"],"gupta"),
"商代":("商代的青铜与都邑","Shang dynasty bronze capital Anyang",["shang","bronze"],"shang"),
"周代":("周代的分封与宗法","Zhou dynasty feudal enfeoffment",["zhou","feudal"],"zhou"),
"秦代":("秦代的郡县与统一制度","Qin dynasty unification county system",["qin","unification"],"qin"),
"元代":("元代的驿站与海运","Yuan dynasty postal relay sea transport",["yuan","relay"],"yuan"),
}
def cj(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",url],capture_output=True,timeout=35)
            s=p.stdout.decode("utf-8","ignore")
            if s.strip().startswith("{"): return json.loads(s)
            time.sleep(3)
        except Exception: time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,(claim,q,slots,obj) in Q.items():
    best=None;seen=set();rej=[]
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=20&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<400: continue
        ti=(oa.get("title") or "").lower(); al=a.lower()
        # R19 精神：对象词必须出现在标题
        if obj not in ti:
            rej.append({"title":(oa.get("title") or "")[:50],"why":"标题无对象词","obj":obj});continue
        hit=[s for s in slots if s in al or s in ti]
        if len(hit)<len(slots):
            rej.append({"title":(oa.get("title") or "")[:50],"why":"缺槽","missing":sorted(set(slots)-set(hit))});continue
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,"claim":claim,"slots":hit,
             "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=16: break
    res[t]={"cand":best,"rejected":rej[:5]}
    print(f"{'OK' if best else '--'} {t:<12} {(best['title'][:46] if best else '-')} ({best.get('year') if best else ''}) cite={best.get('cited') if best else ''}",flush=True)
    time.sleep(1.2)
json.dump(res,open(os.path.join(ROOT,"reports","round48_second.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n成功:",sum(1 for v in res.values() if v["cand"]),"/",len(Q),flush=True)