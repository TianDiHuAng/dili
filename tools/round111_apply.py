# -*- coding: utf-8 -*-
"""第111轮：Crossref 相关度检索 + DOI 桥，为 G3 条目登记第二内容源（摘要逐条阅读后接受）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
R=json.load(open(os.path.join(ROOT,"reports","round111_cr.json"),encoding="utf-8"))
C={x["id"]:x for v in R.values() for x in v}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

def add(t,oid,fld,sentence):
    b=C[oid];e=T[t];sid=f"openalex-{oid}"
    if sid not in have:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",
          f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore");code=0;size=0
        if "__HTTP__" in raw:
            bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {b['title']}",
          "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":b["year"],"type":"学术文献",
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{b['doi']}",
          "link_ok":code==200,"verified":code==200,"page_title":b["title"][:200],
          "note":f"OpenAlex 作品 {oid}（DOI {b['doi']}）；{b['year']}年；被引 {b['cited']}；类型 {b['type']}。HTTP {code}，{size} 字节。摘要长度 {b['chars']} 字符。经 Crossref query.bibliographic 相关度检索 + DOI 桥取得，摘要已人工阅读。"})
        have.add(sid)
        if code!=200: print("WARN",oid,code)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第111轮补第二内容源】{sid}（{b['year']}年，《{b['title']}》，被引 {b['cited']}，摘要 {b['chars']} 字符）：已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY

add("笈多王朝","W4231798191","polities","所引 2016 年百科条目《Gupta Empire》（摘要 933 字符）指出笈多王朝兴起于贵霜衰落后北印度的政治分裂之中，在约 50 年内升至帝国地位并主导北印度至 6 世纪中叶；旃陀罗笈多一世与离车公主鸠摩罗提毗联姻、其子沙摩陀罗笈多为最大的征服者；本条「统一与分裂同地方势力与继承安排相关」据此。")
add("笈多王朝","W4400658485","polities","所引 2024 年《Treasures of the Gupta Empire》（钱币学专著，摘要 1,356 字符）以钱币纪年把王朝起讫记为公元 319 年（旃陀罗笈多一世）至 543 年（毗湿奴笈多），与 Wikidata 属性 320/550 不完全一致，两说并列。")
add("冲积平原","W1755791855","geo","所引 2016 年《Alluvial plain dynamics in the southern Amazonian foreland basin》（被引33，摘要 1,804 字符）指出冲积平原由河流向邻近泛洪盆地堆积的沉积物构成，主要经决口扇与改道（crevasse splays and avulsions）实现；本条「由河道反复迁移与泛滥堆积形成」据此。")
add("卫星遥感地表观测","W4392872715","today","所引 GLC_FCS30D 数据集论文（被引612，摘要 2,829 字符）描述了覆盖 1985–2022 年、26 个时间步、35 个子类的全球 30 米土地覆盖动态监测产品；本条「用于监测土地覆盖」与「开源卫星与云平台扩大了数据可及性」据此举例。")
add("巴西高原","W7143967103","influence","所引 2026 年 SSRN 预印本《Fire History and Conservation Value of Open Ecosystems in South Brazilian Highlands》（被引0，摘要 1,635 字符）指出巴西南部高原草地历史上由火与放牧塑造，保护区排除干扰后出现高草优势与木本入侵；本条「植被分布随气候与人类活动的千年尺度变化而移动」据此补一例（火与放牧为人类活动一侧）。该文为未经同行评审的预印本，证据强度有限。")

T["拉普拉塔平原"]["pending_notes"]=((T["拉普拉塔平原"].get("pending_notes") or "")+" 【第111轮检索记录】Crossref 相关度检索（Pampas plain Argentina geomorphology / Rio de la Plata basin）12 条过筛候选，最接近者《Pliocene pedosedimentary cycles in the southern Pampas》(2000, 被引52) 讨论上新世古土壤，不支撑本条「黑土肥沃、农牧业」；其余为殖民史、鱼类生化等无关对象，全部拒收。").strip()
T["大分水岭"]["pending_notes"]=((T["大分水岭"].get("pending_notes") or "")+" 【第111轮】检索返回的两条最佳候选（W3153139914、W1990720532）已是本条现有来源，未新增。").strip()

ow=json.load(open(os.path.join(DATA,"object_words.json"),encoding="utf-8"))
ow["卫星遥感地表观测"]=["remote sensing","satellite","land cover","landsat","earth observation"]
ow["巴西高原"]=sorted(set(ow.get("巴西高原",[])+["brazilian highland"]))
json.dump(ow,open(os.path.join(DATA,"object_words.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));cov["updated"]=TODAY;cov["round"]=111
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("完成")
