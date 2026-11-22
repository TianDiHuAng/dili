# -*- coding: utf-8 -*-
"""缺口发现：覆盖矩阵、悬空引用、读者问题、待核实、深度缺口。输出 reports/gap_roundN.json。"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UNITS = ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAMES = {"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
THEMES = ["地形","气候","农业","贸易","政权更替","区域"]

QUESTIONS = {
 "地形":"为什么山脉/河流/盆地会影响人类定居？",
 "气候":"季风和干旱区如何改变农业与贸易？",
 "农业":"哪些自然条件决定稻作、粟作或游牧？",
 "贸易":"河流、海岸和山口如何形成商路？",
 "政权更替":"地理条件如何影响国家兴起与衰落？",
 "区域":"相邻区域之间如何互相影响？",
}

def main():
    round_no = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    cov = json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
    entries = cov["entries"]
    by_id = {e["id"]: e for e in entries}
    docs = {u: json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
    all_es = [e for d in docs.values() for e in d["entries"]]
    gaps = {}

    # B2 覆盖矩阵
    matrix = cov.get("matrix", {})
    blanks, sparse = [], []
    for u in UNITS:
        for t in THEMES:
            n = matrix.get(u,{}).get(t,0)
            if n == 0: blanks.append(f"{NAMES[u]}×{t}")
            elif n == 1: sparse.append(f"{NAMES[u]}×{t}")
    gaps["B2_matrix"] = {"blanks": blanks, "sparse": sparse}

    # B3 悬空引用
    dangling = []
    for e in all_es:
        for rid in e.get("related",[]):
            if rid not in by_id:
                dangling.append(f"{e['id']} -> {rid}")
    text = " ".join(e.get("overview","")+" "+e.get("definition","") for e in all_es)
    for name in re.findall(r"另见[：:]([\u4e00-\u9fff、，, ]+)", text):
        for nm in re.split(r"[、，, ]+", name.strip()):
            if nm and nm not in {e["title"] for e in all_es}:
                dangling.append(f"另见 {nm}")
    gaps["B3_dangling"] = dangling

    # B4 读者问题：按主题检查是否有标题/概述覆盖
    qgap = []
    for t,q in QUESTIONS.items():
        hits = [e for e in all_es if e["theme"]==t and any(k in e["overview"] for k in ("影响","形成","塑造","决定","连接"))]
        if len(hits) < 3:
            qgap.append({"theme":t, "question":q, "hits":len(hits)})
    gaps["B4_reader_questions"] = qgap

    # B5 待核实
    pend = [e for e in entries if e["pending_count"]>0]
    gaps["B5_pending"] = {
        "total": len(pend),
        "by_unit": dict(collections.Counter(NAMES[next((u for u in UNITS if e["id"].startswith(u+"-")),"其他")] for e in pend)),
        "core": sum(1 for e in pend if e["tier"]=="核心"),
        "important": sum(1 for e in pend if e["tier"]=="重要"),
    }

    # B7 深度缺口
    deep = [e["id"] for e in entries if e["tier"] in ("核心","重要") and e["level"]=="L1"]
    gaps["B7_depth"] = {"core_l1": sum(1 for i in deep if by_id[i]["tier"]=="核心"),
                        "important_l1": sum(1 for i in deep if by_id[i]["tier"]=="重要"),
                        "ids": deep}

    out = os.path.join(ROOT,"reports",f"gap_round{round_no}.json")
    json.dump({"round":round_no,"gaps":gaps}, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("矩阵空白",len(blanks),"稀疏",len(sparse),"悬空",len(dangling),"读者问题缺口",len(qgap),"待核实",len(pend),"深度缺口",len(deep))
    print("空白格子:", "、".join(blanks))
    print("报告:",out)

if __name__=="__main__":
    main()
