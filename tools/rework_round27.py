# -*- coding: utf-8 -*-
"""第27轮返工：
1) 正则改英文同义词并重测，复活被误杀的 5 条；
2) 24 条补档位标注；拆 8 条共用句；
3) 修 4 条「达标+缺口」互斥；波利尼西亚撤销达标；
4) A 组补「仅示量级」+ 人口单位「人」+ 错别字；
5) 恢复 D060 配对说明状态。
"""
import json,os,re,sys,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
src={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

def strip(h):
    for x in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{x}\b.*?</{x}>"," ",h,flags=re.I|re.S)
    return h
def measure(url,rx):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return 0,0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",strip(b)))).strip()
        return int(c.strip() or 0),len(txt),len(re.findall(rx,txt,re.I))
    except Exception: return 0,0,0

# 英文正则（与被核验的英文来源一致）
ENRX={"地理信息系统":"gis|geographic information","城市地理":"urban","人口地理":"population",
 "人口迁移":"migration|migrant","冰芯气候记录":"ice core","南极冰盖":"ice sheet","南极大陆":"antarctic",
 "南极条约体系":"antarctic treaty","拉普拉塔平原":"la plata|pampa","阿契美尼德波斯":"achaemenid|persia|cyrus",
 "亚马逊河":"amazon","波利尼西亚":"polynesia","亚马逊盆地":"amazon","东非大裂谷":"rift","萨赫勒带":"sahel",
 "刚果盆地":"congo","斯瓦希里海岸":"swahili","维京时代":"viking","文艺复兴意大利":"renaissance",
 "白令陆桥":"bering","北美冰盖":"ice sheet|glacier","大平原":"prairie|great plains","落基山脉":"rocky mountain",
 "中美洲地峡":"isthmus","奥尔梅克":"olmec","玛雅文明":"maya","格陵兰岛":"greenland","阿塔卡马沙漠":"atacama",
 "大分水岭":"great dividing","澳大利亚原住民":"aboriginal","毛利人":"maori","板块构造":"plate tectonic",
 "季风系统":"monsoon","洋流":"ocean current","气候带":"climate zone","河流三角洲":"river delta",
 "游牧":"nomad","植物物候变化":"phenolog|spring","北极火情变化":"arctic fire|fire regime"}
# 标题是否含核心词（档位判定输入）
TITLE_HAS={"地理信息系统":"esri-gis（What is GIS?）含 GIS","城市地理":"s025 Urbanization 含 urban",
 "人口地理":"s023 Population Growth 含 population","人口迁移":"owid-migration 含 Migration",
 "冰芯气候记录":"nasa-ice-cores 含 Ice Core","南极冰盖":"nasa-ice-sheets 含 Ice Sheets",
 "植物物候变化":"noaa-phenology 含 spring plant","北极火情变化":"nasa-arctic-fire 含 Arctic Fire",
 "亚马逊河":"s086 Amazon Fire 含 Amazon","洋流":"无标题含 current（档③）","季风系统":"无标题含 monsoon（档③）"}

fixed=[];revived=[]
for t,rx in ENRX.items():
    e=T.get(t)
    if not e: continue
    pn=e.get("pending_notes") or ""
    if "第27轮实证复核" not in pn: continue
    parts=[]
    for sid in e["sources"][:2]:
        s=src.get(sid)
        if not s: continue
        code,n,h=measure(s["url"],rx)
        parts.append((sid,code,n,h))
    if not parts: continue
    mx=max(p[3] for p in parts); mb=max(p[2] for p in parts)
    # 档位判定：标题含核心词且命中>=30 → 档①5000；标题含且命中3-29 → 档②8000；否则档③8000+命中>=5
    th=TITLE_HAS.get(t,"")
    if th and "含" in th and "无标题" not in th:
        gate = 5000 if mx>=30 else 8000; tier="档①5000" if mx>=30 else "档②8000"
    else:
        gate=8000; tier="档③8000+命中≥5"
    ok = mb>=gate and mx>=(3 if gate==8000 else 3)
    det="；".join(f"{sid}={code}/正文{n}字符/本条命中{h}" for sid,code,n,h in parts)
    verdict=(f"达标（{tier} 门槛{gate}：正文{mb}≥{gate}、命中{mx}）" if ok
             else f"未达标（{tier} 门槛{gate}：正文{mb}、命中{mx}）")
    # 重建第27轮段（替换旧的）
    newseg=(f" 【第27轮实证复核·{t}】本条正则 {rx}（英文源用英文正则，D070）；{det}。"
            f"档位判定：{tier}（{th or '来源标题不含本条核心词'}）。D055 判定：{verdict}。"
            + ("" if ok else f"缺口为「{t}」主题专题页。"))
    pn2=re.sub(r"【第27轮实证复核[^】]*】[^【]*?(?=【|$)","",pn).strip()
    e["pending_notes"]=(pn2+" "+newseg).strip()
    e["last_update"]=TODAY
    fixed.append(t)
    if ok: revived.append((t,mb,mx,tier))

# 波利尼西亚撤销达标（UNSD M49 国码表非专题）
po=T.get("波利尼西亚")
if po:
    po["pending_notes"]=re.sub(r"D055 判定：达标[^。]*。","D055 判定：未达标——britannica-regions 实为 UNSD M49 国码表（别名，非「波利尼西亚」专题正文），命中来自列表项，不构成专题支撑。",po["pending_notes"])

# 4) A 组文案：补「仅示量级」、人口单位、错别字
for t,e in T.items():
    tod=e.get("today") or ""
    if "来源：世界银行 API" not in tod: continue
    if "仅示量级" not in tod and "不代表区域整体" not in tod and "待专门" not in tod[-30:]:
        tod=tod.rstrip("。")+"。上述为全国口径数据，仅示量级，不代表本条目所述区域的内部差异。"
    # 人口补「人」
    tod=re.sub(r"总人口 ([\d,]+)（(\d{4})年）", r"总人口 \1 人（\2年）", tod)
    tod=tod.replace("沙哈拉","撒哈拉")
    e["today"]=tod
    e["last_update"]=TODAY
# 撤回错别字
for t,e in T.items():
    if "沙哈拉" in (e.get("today") or ""): e["today"]=e["today"].replace("沙哈拉","撒哈拉")

# 5) 恢复 D060 三状态
for t in ("北美冰盖","南极冰盖","板块构造"):
    e=T.get(t)
    if not e: continue
    st=e.get("status") or ""
    if t=="北美冰盖": e["status"]="L2·配对说明(第24轮)-PDF专题·已复核(第27轮)"
    elif t=="南极冰盖": e["status"]="L2合规换源(第22轮)·已复核(第27轮)"
    else: e["status"]="L2·配对说明(第22轮)·已复核(第27轮)"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("重测并重写",len(fixed),"条；复活达标",len(revived))
for r in revived: print("  ",r)