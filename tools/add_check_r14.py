# -*- coding: utf-8 -*-
"""向 check.py 追加 R14：today 国名必须与端点 ISO3 一致（D072 防复发）。"""
import re,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R14" in t:
    print("已存在 R14");raise SystemExit
# 1) 在 main() 里，all_entries.append 之前加调用
t=t.replace("            all_entries.append(e)",
"""            if e.get("today"):
                check_today_sources(e)
            all_entries.append(e)""")
# 2) 追加函数与国名映射
t=t.replace("def check_today(eid, text):",
'''CN2ISO = {
 "中国":"CHN","印度":"IND","尼日利亚":"NGA","巴西":"BRA","美国":"USA","埃及":"EGY","印度尼西亚":"IDN",
 "日本":"JPN","伊拉克":"IRQ","巴基斯坦":"PAK","越南":"VNM","澳大利亚":"AUS","阿尔及利亚":"DZA",
 "南非":"ZAF","土耳其":"TUR","德国":"DEU","法国":"FRA","俄罗斯":"RUS","坦桑尼亚":"TZA","肯尼亚":"KEN",
 "阿根廷":"ARG","乌拉圭":"URY","加拿大":"CAN","突尼斯":"TUN","伊朗":"IRN","希腊":"GRC","意大利":"ITA",
 "英国":"GBR","挪威":"NOR","危地马拉":"GTM","墨西哥":"MEX","秘鲁":"PER","智利":"CHL","新西兰":"NZL",
 "斐济":"FJI","埃塞俄比亚":"ETH","马里":"MLI","哈萨克斯坦":"KAZ","韩国":"KOR",
 "刚果民主共和国":"COD","乌兹别克斯坦":"UZB","格陵兰":"GRL","巴布亚新几内亚":"PNG","尼日尔":"NER",
 "塞内加尔":"SEN","加纳":"GHA","乍得":"TCD","蒙古":"MNG","孟加拉国":"BGD","斯里兰卡":"LKA","尼泊尔":"NPL",
}

def check_today_sources(e):
    """R14：today 中提到的国家，必须在该条 sources 的端点里有对应 ISO3（D072）。"""
    today = e.get("today") or ""
    if "世界银行 API" not in today:
        return
    named = {CN2ISO[n] for n in CN2ISO if n in today}
    if not named:
        return
    endpoint_isos = set()
    for sid in e.get("sources", []):
        m = re.match(r"wb-([a-z]{3})-(pop|urban|life|forest|agri)$", sid)
        if m:
            endpoint_isos.add(m.group(1).upper())
    if not endpoint_isos:
        err(f"R14 {e['id']}: today 引用世界银行数据，但无国别专用端点（D072）")
        return
    missing = named - endpoint_isos
    if missing:
        err(f"R14 {e['id']}: today 提到 {sorted(named)} 但端点仅覆盖 {sorted(endpoint_isos)}（缺 {sorted(missing)}，D072）")


def check_today(eid, text):''')
open(p,"w",encoding="utf-8").write(t)
print("R14 已加入 check.py")