# -*- coding: utf-8 -*-
"""第2轮抽检返工：移除新条目中无来源的具体年代，软化决定论表述。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TODAY = "2026-11-22"

FIX = {
 "东亚季风": {
   "time_or_place": "东亚季风区（现代观测与历史记载）",
   "overview": "海陆热力差异导致的季节性风向反转，显著影响稻作区降水节律与农业周期安排；具体影响程度还受地形、海洋温度与其他气候因子共同作用。",
   "definition": "东亚季风：海陆热力差异导致的季节性风向反转，显著影响东亚降水与农业节律；其强度变化受多因素共同作用，不作单因决定论解释。",
   "pending_notes": "抽检返工：已移除无来源的起始年代，软化决定论表述；季风起始时间与长期变化机制待专门来源核验。",
 },
 "欧洲温带海洋性气候": {
   "time_or_place": "西欧（常年气候特征）",
   "pending_notes": "抽检返工：已移除无来源的地质年代表述；气候分类与数据待权威气象来源核验。",
 },
 "中世纪欧洲庄园农业": {
   "time_or_place": "中世纪（起讫年代因地区而异）",
   "overview": "以庄园为单位的土地制度，敞田耕作与领主自营地并存，与封建秩序相互关联。",
   "pending_notes": "抽检返工：年代改为定性表述；庄园制度的区域差异待专门史料核验。",
 },
 "澳大利亚内陆干旱气候": {
   "time_or_place": "澳大利亚内陆（长期干旱环境）",
   "pending_notes": "抽检返工：已移除无来源的地质年代；干旱化过程待专门研究核验。",
 },
 "澳大利亚混合农业": {
   "time_or_place": "近现代（形成与发展时期待核）",
   "pending_notes": "抽检返工：已移除无来源年份；农业制度形成时间待专门来源核验。",
 },
 "南极洲无农业的环境约束": {
   "overview": "极端低温、极夜与缺乏可耕作土壤使大规模定居农业难以形成，食物主要依赖外部补给。",
   "pending_notes": "抽检返工：软化绝对表述；食物补给与人员规模数据待权威来源核验。",
 },
 "南极特别保护区": {
   "time_or_place": "南极条约体系建立后（年份待核）",
   "pending_notes": "抽检返工：已移除未经来源支持的年份；保护区名录与时间线待官方来源核验。",
 },
}

def main():
    fixed=[]
    for u in ["asia","europe","south-america","oceania","antarctica","global-themes","africa","north-america"]:
        p=os.path.join(DATA,u+".json")
        d=json.load(open(p,encoding="utf-8"))
        changed=False
        for e in d["entries"]:
            if e["title"] in FIX:
                e.update(FIX[e["title"]])
                e["last_update"]=TODAY
                e["status"]="抽检返工完成(第2轮)"
                fixed.append(e["title"])
                changed=True
        if changed:
            json.dump(d,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    # coverage 状态同步
    cp=os.path.join(DATA,"coverage.json")
    cov=json.load(open(cp,encoding="utf-8"))
    for c in cov["entries"]:
        if c["id"].split("-")[-1] in {f.split("-")[-1] for f in fixed} or c["id"] in fixed:
            pass
    # 用标题反查 id 更可靠
    titles={e["title"]:e["id"] for d in [json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]] for e in d["entries"]}
    idset={titles[t] for t in fixed}
    for c in cov["entries"]:
        if c["id"] in idset:
            c["status"]="抽检返工完成(第2轮)"
            c["last_update"]=TODAY
    json.dump(cov,open(cp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("返工条目",len(fixed),"：","、".join(fixed))

if __name__=="__main__":
    main()
