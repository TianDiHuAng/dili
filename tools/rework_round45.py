# -*- coding: utf-8 -*-
"""第45轮返工：4条语义FAIL、白令/洋流、孤儿引文全库扫描、台账。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
S={s["id"]:s for s in sd["sources"]}

# ===== P0-1 安第斯山脉：撤落点，降旁证 =====
an=T["安第斯山脉"]
an["geo"]=re.sub(r" 所引 2008 年研究综述[^。]*。","",an.get("geo") or "")
an["pending_notes"]=((an.get("pending_notes") or "")+
  " 【第45轮返工·撤回】所引 2008 年《Review and analysis of altitudinal distribution…》摘要中 climate/zone/vertical/temperature **均为 0 次命中**，"
  "全文是哥伦比亚安第斯**无尾类（蛙类）的海拔分布与特有种**，不支撑「垂直气候带」断言。已撤下落点句，该源降为**旁证**（不作特征描述依据）；"
  "「垂直气候带」待引气候/地貌专题文献。").strip()
an["last_update"]=TODAY

# ===== P0-2 五大湖：改用 NOAA GLERL（现成页面） =====
gl=T["五大湖"]
gl["geo"]=re.sub(r" 所引 2024 年研究以优化方法讨论[^。]*。","",gl.get("geo") or "")
gl["sources"]=[s for s in gl["sources"] if not s.startswith("openalex-")]
for s in ("noaa-glerl","epa-great-lakes"):
    if s in S and s not in gl["sources"]: gl["sources"].append(s)
gl["pending_notes"]=((gl.get("pending_notes") or "")+
  " 【第45轮返工·撤回】所引 2024 年《Optimal Water Level Study Based on Great Lakes》为**水位优化建模**（AHP/SQP/模拟退火/水坝出流），"
  "摘要中 season/seasonal/hydrolog **0 次命中**，不描述水文特征；且 cited 1、Clausius Press，质量门不足。已撤下该源与落点句。"
  " 改以机构来源（NOAA GLERL、EPA 五大湖页）作背景，具体水文特征待专门水文学来源。").strip()
gl["last_update"]=TODAY

# ===== P0-3 马里帝国：正文收窄（去掉「盐」与「财富权力」的无据部分） =====
ml=T["马里帝国"]
ml["influence"]=("所引 1982 年《Myth and Metrology: The Early Trans-Saharan Gold Trade》讨论跨撒哈拉**黄金贸易的早期存在与其度量（称量）标准的源流**；"
  "本条据此只写「跨撒哈拉黄金贸易长期存在并有其度量传统」，**不据此推断其与政治权力的关系**。贸易对帝国财政的作用待专门研究核验。")
ml["pending_notes"]=((ml.get("pending_notes") or "")+
  " 【第45轮返工·收紧】原 influence 写「控制黄金**与盐**贸易是**财富与权力**的重要来源」，而摘要中 salt/power/wealth/control 均为 0 次命中，"
  "仅支持「黄金贸易的早期存在与度量标准」；已把正文收窄到摘要可支撑的范围（禁止「缩水对齐」——落点句不得窄于正文断言，故同步收窄正文）。").strip()
ml["last_update"]=TODAY

# ===== P0-4 文艺复兴意大利：删无据分句 =====
rn=T["文艺复兴意大利"]
rn["influence"]=("所引 2017 年研究《Patronage and Italian Renaissance Sculpture》讨论**私人公民对雕塑的赞助及其对公共空间的僭越**；"
  "本条据此只写「赞助制度为艺术生产提供条件」，**不据此写城邦竞争、商业财富或学术**。后者待专门经济社会史来源。")
rn["pending_notes"]=((rn.get("pending_notes") or "")+
  " 【第45轮返工·收紧】原 influence 写「城邦竞争、商业财富与城市赞助为艺术与**学术**提供条件」，而摘要中 city-state/competition/commercial/wealth/learn 均为 0 次命中；"
  "已收窄为「赞助制度为艺术生产提供条件」；该专著 cited 0 且只谈雕塑，证据强度有限。").strip()
rn["last_update"]=TODAY

# ===== P1-5 白令陆桥：删「宽阔」+ 加反向证据 =====
bl=T["白令陆桥"]
bl["geo"]=("白令陆桥位于今白令海峡一带。所引 1973 年研究重建白令地区海平面历史，给出末次冰期低海平面幅度（约 −90 至 −135 米）"
  "与陆桥出露的时段；**该研究同时指出末次冰期时外陆架仍有部分没入水下**，故陆桥为**部分出露**、宽度随低海平面幅度而变化，而非固定「宽阔陆地」。"
  " 当时气候寒冷干燥，草原与苔原提供动物迁徙通道（后者为常识性描述）。")
bl["pending_notes"]=((bl.get("pending_notes") or "")+
  " 【第45轮返工】删除「宽阔陆地」——摘要明写末次冰期外陆架 remained submerged（反向证据）；已改为「部分出露、宽度随低海平面幅度变化」。").strip()
bl["last_update"]=TODAY

# ===== P1-6 洋流：第二句标常识 =====
oc=T["洋流"]
oc["geo"]=("洋流由风应力与密度差驱动、并受地转平衡约束（所引 2001 年研究以海洋边缘密度约束环流结构，支持「密度差驱动」这一环节）；"
  "形成表层环流与深层翻转环流。（「海盆形状与海峡决定路径」为本条常识性表述，未挂该文献。）")
oc["pending_notes"]=((oc.get("pending_notes") or "")+
  " 【第45轮返工】geo 第二句「海盆形状与海峡决定路径」无源，已标为常识性表述；「驱动」表述改为「风应力与密度差驱动、受地转平衡约束」。").strip()
oc["last_update"]=TODAY

# ===== P1-7 孤儿引文全库扫描 =====
def years_in_sources(e):
    ys=set()
    for sid in e["sources"]:
        s=S.get(sid) or {}
        if s.get("year"): ys.add(str(s["year"]))
        m=re.search(r"（(\d{4})年）|(\d{4})年", s.get("note") or "")
        if m: ys.add(m.group(1) or m.group(2))
    return ys
FIELDS=("definition","overview","geo","influence","polities","connections","today","time_or_place")
orphans=[]
for t,e in T.items():
    ys=years_in_sources(e)
    for f in FIELDS:
        v=e.get(f) or ""
        for m in re.finditer(r"所引\s*(\d{4})\s*年", v):
            if m.group(1) not in ys:
                orphans.append((t,f,m.group(1)))
print("孤儿引文:",len(orphans))
for o in orphans[:20]: print("  ",o)
# 清理：删除含孤儿年份的整句
for t,f,yr in orphans:
    e=T[t]
    v=e[f]
    v=re.sub(rf"[^。]*所引\s*{yr}\s*年[^。]*。","",v)
    e[f]=re.sub(r"\s{2,}"," ",v).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第45轮孤儿清理】删除 {f} 段中引用 {yr} 年来源的句子——该年份在本条 sources 中无对应记录。").strip()
    e["last_update"]=TODAY
print("已清理",len(orphans),"处")

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=45
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
json.dump({"round":45,"orphans_found":len(orphans),"orphans":orphans,
 "note":"扫描全部正文段的「所引YYYY年」，与 sources 的 year/note 年份比对；不符者视为孤儿引文并删句"},
 open(os.path.join(ROOT,"reports","round45_orphans.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)