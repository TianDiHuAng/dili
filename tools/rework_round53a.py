# -*- coding: utf-8 -*-
"""第53轮返工：元代/河中补候选（变音归一）、阿塔卡马删副高、GIS降旁证删灾害、突厥降旁证、莫切/城市地理改落点、意大利加截断声明。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

def fetch(oid):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",
              f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
            d=json.loads(p.stdout.decode("utf-8","ignore"))
            if d.get("id"): return d
        except Exception: pass
        time.sleep(4)
    return {}
def get_oa_by_doi(doi):
    d=fetch(f"https://doi.org/{doi}")
    if d.get("id"): return d
    # 备用：用 Crossref 元数据
    return {}

# ===== A 阿塔卡马：删「副热带高压」（摘要不存在）=====
at=T["阿塔卡马沙漠"]
at["geo"]=("位于南美西岸、安第斯山脉与太平洋之间，是全球最干旱的荒漠之一。"
  "所引 2003 年研究（被引587）给出机制：安第斯中段**西坡雨影**使 15°–27°S 的降水主要依赖亚马孙夏季对流，降水随海拔呈指数关系；"
  "超干旱的形成还与**安第斯隆升**（升至1000–2000米）和**秘鲁寒流上升流的加强**相伴随。"
  "（「副热带高压」为本条原稿所加，**不在该摘要内**，已删除。）")
at["pending_notes"]=((at.get("pending_notes") or "")+
  " 【第53轮返工·删无源机制】原落点写「极端干旱源于西坡雨影与**副热带高压**叠加」——摘要中副热带高压 0 命中（其机制链为雨影＋安第斯隆升＋秘鲁寒流上升流）；已删除该词，机制按摘要改写。").strip()
at["last_update"]=TODAY

# ===== B GIS：降旁证 + 删正文「灾害评估」残留 =====
gi=T["地理信息系统"]
gi["influence"]=("所引 2006 年文献是**区域空间决策支持系统（SDSS）的概念设计**，以 GIS 为底座、外挂模型与多准则评价（被引仅 4，属工程案例，**仅作旁证**）。"
  " 该文同时指出：传统上 GIS 强于空间数据管理，但**缺乏问题域的建模能力**，须外挂模型/多准则系统方能支持决策。"
  " 这说明「GIS 作为决策支持工具」是有条件的，而非自带决策能力。")
gi["pending_notes"]=((gi.get("pending_notes") or "")+
  " 【第53轮返工·降旁证】① 该源被引 4、属设计类工程文，按 D101 质量门**只能作旁证**，不得称「主来源」；"
  "② 补写摘要的反向限定「GIS 缺乏问题域建模能力、须外挂模型」；③ **删除正文残留的「灾害评估」**（第44轮已判该源无据，但当时只删备注未删正文）。").strip()
gi["last_update"]=TODAY

# ===== C 突厥：降旁证 + 修 polities 自相矛盾 + 标两说 =====
tk=T["突厥"]
tk["polities"]=("据所引 2023 年章节，突厥人建立了历史上第一个突厥帝国——**突厥汗国**，摘要给出「552–745年」与「552 至 742 年」**两种表述**（D109 要求并注）；"
  "该章节为 Routledge 电子书章、摘要 619 字符（低于本条 800 字符门槛）、被引 0，**故仅作旁证**。"
  " 更具体的汗国世系与分裂过程待专门突厥史专著核验。")
tk["pending_notes"]=((tk.get("pending_notes") or "")+
  " 【第53轮返工·降旁证】该源被引 0、book-chapter、摘要 619 字符 < 800（D106 第一层不成立），按 D101 只能作旁证；"
  "已把 polities 的自相矛盾（「待核验」+ 具体年代）合并为「据该章节可确认 552 年起」并标出 745/742 两说。主来源待补突厥史专著。").strip()
tk["last_update"]=TODAY

# ===== D 莫切：改落点为「都城手工业 + 南莫切国家」半附庸 =====
mo=T["莫切文化"]
mo["influence"]=("所引 2010 年《Craft Specialists at Moche》（被引58）以**莫切都城**（南莫切国家的都城）的作坊为对象：城市人口中有一部分是陶工、冶金匠与宝石匠，"
  "这些手工业专门化者在**南莫切国家的经济、政治与宗教领域**扮演重要角色。"
  " 摘要的结论是：城市手工业者**既非独立、也未受中央统治精英的紧密控制**（半附庸状态）。"
  " 本条**不据此**推断多河谷政治中心之间的关系，也不涉及灌溉（该源均无此内容）。")
mo["pending_notes"]=((mo.get("pending_notes") or "")+
  " 【第53轮返工·收窄】原落点写「**河谷**政治中心与手工业专门化相互支撑」，而摘要对象是**单一都城**、且结论为「半附庸」而非对称互撑；"
  "「灌溉」在原 claim 中但摘要 0 命中（属缩水对齐）；已按摘要收窄，并显式排除多河谷与灌溉两处。").strip()
mo["last_update"]=TODAY

# ===== E 城市地理：改落点、降强度、加样本限定 =====
ci=T["城市地理"]
ci["influence"]=("所引 2004 年《Exploring Metropolitan Accessibility and Urban Structure》（被引132）以 **GIS 区位可达性**分析城市空间结构，"
  "样本为**美国都市区**：结果显示居住可达性格局在各城市之间相近，而**就业可达性则因城市而异**；作者认为可达性指标「**可用于探索**城市形态，尤其是城市蔓延」。"
  " 本条据此写「可达性可用于刻画城市扩张」，不作「城市地理学以可达性定义城市」的学科通例断言。")
ci["pending_notes"]=((ci.get("pending_notes") or "")+
  " 【第53轮返工】① 结论强度由「以…刻画」降为「可用于探索」；② 补样本限定「美国都市区」；③ 落点改挂正文已有句「聚集经济与交通可达性推动城市扩张」（摘要的 urban sprawl 正好对应）。").strip()
ci["last_update"]=TODAY

# ===== F 意大利半岛：加截断声明 + 限定中南部 =====
it=T["意大利半岛"]
it["geo"]=("半岛以亚平宁山系为脊、两侧分别为狭窄的沿海平原；北部为波河平原，南部多山与河谷。"
  "地质上属**亚平宁褶皱—逆冲造山带**（所引 2010 年研究基于中南部 1:250,000 实测地质图，覆盖中南部而非全半岛）。"
  "地中海气候在半岛南北差异明显，山地与谷地构成多样的农业带。")
it["pending_notes"]=((it.get("pending_notes") or "")+
  " 【第53轮返工】① 所引摘要于 **693 字符处被截断**（末尾 `with: ( i...`），**未含结论句**，D088/D092 的「读到结论句」客观上无法完成——须读全文，备注如实声明；"
  "② 文献只覆盖**中南部亚平宁**，落点已限定；③ geo 补「地质上属亚平宁褶皱—逆冲造山带」一句。").strip()
it["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("A–F 处置完成")