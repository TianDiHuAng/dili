# -*- coding: utf-8 -*-
"""第21轮定点返工：玛雅文明 influence/polities + 8 处分期词去年代化 + 编辑口径句移出正文。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 玛雅文明：influence 去「古典期」与单因断言；polities 去「殖民时期后」
m=T["玛雅文明"]
m["influence"]="农业与水利适应热带环境，城市中心在雨林中形成网络；干旱、政治冲突与贸易变化被视为城市中心衰落的相关因素，学界无定论，不能单因解释。"
m["polities"]="雨林中的城邦长期并立，中心兴衰更替；具体城邦名单与年代待专门史料核验。"
m["pending_notes"]=(m.get("pending_notes") or "")+" 【第21轮二次返工】删除 influence 的「古典期」考古分期与「衰落主因」单因断言；删除 polities 的「殖民时期后」时期标签。"

# 2) 8 处分期/事件词去年代化
FIX={
"大平原": [("原住民社会、殖民边疆与后来的农业经营先后改变土地利用格局",
            "原住民社会、外来定居者与后来的农业经营先后改变土地利用格局")],
"落基山脉": [("原住民、殖民边疆与国家公园体系先后塑造管理格局",
             "原住民、外来定居者与国家公园体系先后塑造管理格局")],
"澳大利亚大陆": [("原住民社会长期适应多样生态，殖民后形成新的政治与经济结构",
                "原住民社会长期适应多样生态，外来统治后形成新的政治与经济结构")],
"澳大利亚原住民": [("以族群与亲属组织为主的社会结构长期存在，殖民后经历剧烈变迁与权利运动",
                  "以族群与亲属组织为主的社会结构长期存在，外来统治后经历剧烈变迁与权利运动")],
"波利尼西亚": [("岛屿条件促成航海殖民与酋邦组织，接触欧洲后政治与人口结构显著变化",
               "岛屿条件促成远洋定居与酋邦组织，与外部世界接触后政治与人口结构显著变化")],
"亚马逊盆地": [("前殖民时期存在复杂的社群与区域网络，殖民与近代开发改变土地使用与族群关系",
                "外来统治之前已存在复杂的社群与区域网络，近代开发进一步改变土地使用与族群关系")],
"印加帝国": [("帝国依托高原道路与梯田组织资源，其后因内战与殖民征服而解体",
             "帝国依托高原道路与梯田组织资源，其后因内部冲突与外来征服而解体")],
"撒哈拉沙漠": [],
}
n2=0
for t,reps in FIX.items():
    e=T.get(t)
    if not e: continue
    for old,new in reps:
        for k in ("geo","influence","polities","connections","today"):
            v=e.get(k) or ""
            if old in v:
                e[k]=v.replace(old,new);n2+=1
    if reps: e["pending_notes"]=(e.get("pending_notes") or "")+" 【第21轮二次返工】polities/其余四段的分期标签（殖民/前殖民/接触欧洲）改为「外来统治/外来定居者/与外部世界接触」等去年代化表述。"

# 3) 编辑口径句移出正文
mf=T.get("季风系统")
if mf:
    mf["today"]="季风强度与降水数据需按年份从气象机构核验；具体数值待补。"
    mf["pending_notes"]=(mf.get("pending_notes") or "")+" 【第21轮二次返工】「本站不写未核验数值」编辑口径已移入本备注，正文不再出现编辑自述。"

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# D058 核对
chk=sum(1 for e in T.values() if "第21轮二次返工" in (e.get("pending_notes") or ""))
print("二次返工落盘:",chk,"条；分段替换",n2,"处")