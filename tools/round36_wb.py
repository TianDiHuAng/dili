# -*- coding: utf-8 -*-
"""第36轮：为全球主题类补充条目批量取世界银行指标。"""
import subprocess,json,os,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND={
"极端贫困空间分布":("SI.POV.DDAY","贫困人口比例（每日 2.15 美元以下，2017 PPP，%）"),
"能源转型":("EG.FEC.RNEW.ZS","可再生能源占最终能源消费比例（%）"),
"碳排放空间差异":("EN.GHG.CO2.MT.CE.AR5","CO₂ 排放总量（Mt CO₂e，不含 LULUCF）"),
"人口年龄结构":("SP.POP.0014.TO.ZS","0–14 岁人口占比（%）"),
"预期寿命空间差异":("SP.DYN.LE00.IN","出生时预期寿命（岁）"),
"人均产出空间差异":("NY.GDP.PCAP.CD","人均 GDP（现价美元）"),
"肥料使用与环境":("AG.CON.FERT.ZS","化肥消费强度（千克/公顷耕地）"),
"肉奶生产与土地":("AG.LND.AGRI.ZS","农业用地占土地面积（%）"),
"森林面积占比":("AG.LND.FRST.ZS","森林覆盖率（%）"),
"人口增长":("SP.POP.GROW","人口年增长率（%）"),
"城市化水平":("SP.URB.TOTL.IN.ZS","城市人口占比（%）"),
"土壤资源":("AG.LND.ARBL.ZS","可耕地占土地面积（%）"),
"海洋生态系统":("ER.FSH.PROD.MT","渔业总产量（吨）"),
"陆地保护区":("ER.LND.PTLD.ZS","陆地保护区占国土面积（%）"),
"全球营养状况":("SH.STA.MALN.ZS","5 岁以下儿童发育迟缓率（%）"),
"儿童发展地域差异":("SH.DYN.MORT","5 岁以下儿童死亡率（每千活产）"),
"全球人口规模":("SP.POP.TOTL","总人口（人）"),
"水资源供给概览":("ER.H2O.FWTL.ZS","年度淡水取用占内部可再生资源（%）"),
"作物单产差异":("AG.YLD.CREL.KG","谷物单产（千克/公顷）"),
"国家收入分类":("NY.GNP.PCAP.CD","人均 GNI（现价美元）"),
"教育机会地域差异":("SE.PRM.NENR","小学净入学率（%）"),
"健康地理数据":("SH.XPD.CHEX.GD.ZS","卫生支出占 GDP（%）"),
"气候与健康风险":("SH.DYN.LE00.FE.IN","女性出生时预期寿命（岁）"),
}
def get(u):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25",u],capture_output=True,timeout=35)
            s=p.stdout.decode("utf-8","ignore")
            if s.strip().startswith("["): return s
            time.sleep(3)
        except Exception: time.sleep(3)
    return ""
out={}
for name,(code,label) in IND.items():
    u=f"https://api.worldbank.org/v2/country/WLD/indicator/{code}?format=json&per_page=100&date=2015:2025"
    try:
        d=json.loads(get(u))
        rows=[r for r in d[1] if r.get("value") is not None] if len(d)>1 else []
        if rows:
            L=max(rows,key=lambda r:int(r["date"]))
            out[name]={"code":code,"label":label,"value":L["value"],"year":L["date"]}
            print(f"OK {name:<14} {code:<22} {L['date']} {L['value']}")
        else:
            print(f"-- {name:<14} {code:<22} 无值")
    except Exception as ex:
        print(f"ERR {name:<14} {code:<22} {type(ex).__name__}")
    time.sleep(1.5)
json.dump(out,open(os.path.join(ROOT,"reports","round36_wb.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n取得:",len(out),"/",len(IND))