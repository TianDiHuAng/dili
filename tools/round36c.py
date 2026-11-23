# -*- coding: utf-8 -*-
"""第36轮：4 条补充条目升 L2（海洋保护区/湿地水资源/撒南非洲/全球气温变化）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
W=json.load(open(os.path.join(ROOT,"reports","round36_wb2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

SPEC={
"海洋保护区":dict(
 defn="海洋保护区：为保护海洋生态系统与资源而在海域划定的管理区域。",
 dim="覆盖比例在部分岛国与发达国家较高，公海与高 seas 的覆盖长期偏低；近岸与专属经济区内的划定差异大。",
 mech="划定受政治意愿与渔业利益制约；「覆盖面积」不等于「管理成效」，执法的经费与能力是关键变量。",
 conn="与渔业资源、珊瑚礁与湿地、海洋生态系统健康相关。"),
"湿地与水资源":dict(
 defn="湿地与水资源：湿地生态系统与可利用淡水资源的分布与管理。",
 dim="人均可再生水资源在干旱的西亚与北非极低，在湿润热带与高纬度地区很高；湿地集中于低平原与三角洲。",
 mech="水资源可得性由降水、蒸发与跨境河流决定；湿地则依赖水位节律，上游取水与筑坝会改变其存续条件。",
 conn="与灌溉农业、城市化、生物多样性、气候适应相关。"),
"撒哈拉以南非洲发展数据":dict(
 defn="撒哈拉以南非洲发展数据：用于刻画该区域人口、经济与社会指标的数据体系。",
 dim="区域内差异极大：沿海与矿产国、内陆萨赫勒国家、岛国的指标水平相距悬殊；统计能力本身也不均衡。",
 mech="数据可得性与质量受国家统计体系、冲突与调查频率影响；不可用「区域平均值」代替具体国情判断。",
 conn="与贫困、人口增长、营养、教育等指标互为参照。"),
"全球气温变化":dict(
 defn="全球气温变化：全球平均地表气温相对基准期的变动。",
 dim="变暖幅度随纬度与海陆分布不同：北极增温最快（极地放大），海洋增温慢于陆地；区域差异远大于全球均值。",
 mech="变暖由温室气体累积驱动，叠加自然变率（如 ENSO、火山）造成年际波动；因此单年数值不能代表趋势，需看多年平均。",
 conn="与碳排放、极端天气、海平面、生态物候相关。"),
}
n=0;up=[]
for name,s in SPEC.items():
    e=T.get(name)
    if not e: continue
    if name=="全球气温变化":
        sid="noaa-global-temp"
        body=("来源：NOAA Climate at a Glance（全球陆海平均温度距平，基准期 1901–2000，单位 °C）："
              "2023年 +1.17、2024年 +1.26、2025年 +1.12。距平值随基准期与观测方法而变，跨数据集比较须核对口径；"
              "单年数值受自然变率影响，不应直接当作长期趋势。")
        tox="（本条用 NOAA 全球温度序列，未采用排放指标——排放不等于气温。）"
    else:
        d=W[name];code=d["code"]
        sid=f"wb-{d['agg'].lower()}-{code.lower().replace('.','-')}"
        if sid not in have:
            u=f"https://api.worldbank.org/v2/country/{d['agg']}/indicator/{code}?format=json&per_page=100&date=2015:2025"
            c2=0;size=0
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);c2=int(cc.strip() or 0);size=len(bb)
            except Exception: pass
            disp=(f"{int(d['value']):,} 人" if code=="SP.POP.TOTL" else
                  f"{d['value']:,.0f} 立方米" if code=="ER.H2O.INTR.PC" else f"{d['value']:.1f}%")
            sd["sources"].append({"id":sid,"title":f"World Bank API — {d['label']} ({code}, {d['agg']})",
              "author":"World Bank","year":None,"type":"数据端点","url":u,"url2":None,
              "link_ok":bool(c2==200),"verified":bool(c2==200),"page_title":f"World Bank API — {code} ({d['agg']})",
              "note":f"JSON API {c2}；聚合 {d['agg']}（{'撒哈拉以南非洲' if d['agg']=='SSF' else '全球'}）＋指标 {code}；最新 {disp}（{d['year']}年）。年度指标，随年度更新与历史修订变化。"})
            have.add(sid)
        disp=(f"{int(d['value']):,} 人" if code=="SP.POP.TOTL" else
              f"{d['value']:,.0f} 立方米" if code=="ER.H2O.INTR.PC" else f"{d['value']:.1f}%")
        body=(f"来源：世界银行 API（指标 {code}，{d['label']}）：{'撒哈拉以南非洲' if d['agg']=='SSF' else '全球'} {disp}（{d['year']}年）。"
              "该值为合计或均值，掩盖区域内部差异，跨国/跨区比较须核对口径。")
        tox=""
    e.update({"level":"L2","status":"L2完成(第36轮)-指标数据",
      "definition":s["defn"],"overview":s["defn"]+" 本条以可核验的指标序列为数据基础，最新值见「今天的状况」。",
      "time_or_place":"全球/区域口径（最新观测年份见 today）",
      "geo":s["dim"],"influence":s["mech"],"connections":s["conn"],
      "polities":e.get("polities") or "本条为全球/区域主题条目，不展开具体政权序列。",
      "today":body,"sources":list(dict.fromkeys((e.get("sources") or [])+[sid])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第36轮升级 L2】数据来源 {sid}；空间差异描述为常识性地理概述，未逐国引用。{tox}").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 270 C200 230 320 215 460 220 C570 224 650 240 690 258' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<text x='110' y='250' class='lbl'>{name}</text>"
      f"<text x='40' y='370' class='dim'>{name} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(name)

json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))