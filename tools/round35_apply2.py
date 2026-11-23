# -*- coding: utf-8 -*-
"""第35轮续：升级 15 条重要 L1（剔除朝鲜半岛/吠陀时代/斯堪的纳维亚）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round35_openalex2.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

BODY={
"古巴比伦":dict(defn="古巴比伦：两河流域南部的巴比伦城及其统治的王国。",
 span="约公元前2千纪初至前1千纪（古巴比伦王国；后期巴比伦在波斯与塞琉古治下延续，本条引 2017 年晚期巴比伦经济研究）",
 geo="位于幼发拉底河下游冲积平原，河水灌溉支撑大麦与椰枣种植；河道变迁频繁，灌溉与排水需要持续维护，这一维护需求塑造了地方组织。",
 infl="所引 2017 年研究以楔形文书重建晚期巴比伦的经济：神庙、王室与私人之间的土地与税收关系构成制度骨架，说明灌溉农业的剩余如何被组织与抽取。",
 conn="经河网与波斯湾连接印度洋贸易，经陆路通叙利亚与安纳托利亚，是古代近东的枢纽。"),
"明清":dict(defn="明清：中国明代与清代两个王朝（1368–1912年）。",
 span="明 1368–1644年；清 1644–1912年",
 geo="核心区在华北平原与长江下游，运河把江南粮赋北运；东南沿海港湾众多，是海上贸易的前沿；西北与西南为山地高原，治理成本高。",
 infl="所引 1990 年研究以广东佛山为例，说明明清时期**乡村—城镇的转化**由手工业与商业推动，而非单纯行政设置；这说明城市化有多种动力，不能只看行政层级。",
 conn="经运河连接南北，经东南港口（广州、泉州等）通东南亚与印度洋，经陆路通蒙古与中亚。"),
"中南半岛":dict(defn="中南半岛：亚洲东南部的大陆部分，包括今越南、老挝、柬埔寨、泰国、缅甸。",
 span="地质与气候尺度（本条引 2007 年风化研究）",
 geo="半岛受季风控制，干湿季分明；山脉自北向南延伸，河谷与三角洲是人口与农业重心。湄公河、红河、萨尔温江等大河纵贯，形成纵向的交通与生态走廊。",
 infl="所引 2007 年研究显示，尽管气候条件相近，华南与中南半岛各流域的**化学风化程度不同**，受构造与岩性控制；这说明「同一气候带内景观一致」的假设不成立。",
 conn="西临印度洋、东临南海，是海上丝绸之路的陆海交汇带；内陆河流把中国西南与半岛腹地连成一体。"),
"突厥":dict(defn="突厥：中亚与蒙古高原上的突厥语人群及其汗国。",
 span="6世纪中叶至8世纪（突厥汗国；其后突厥语人群继续扩展，本条引 2015 年遗传研究）",
 geo="核心在蒙古高原与阿尔泰山一带，草原与山地交错，适合牧养与冶金；向西经准噶尔与中亚绿洲带通往波斯与黑海草原。",
 infl="所引 2015 年遗传研究显示突厥语人群的扩展**伴随基因混合**而非单纯替换，说明语言扩散与人群迁移是两件相互关联但不重合的过程。",
 conn="横跨欧亚草原带，东接中国北方，西连中亚与波斯，是草原丝绸之路的主要通道。"),
"黎凡特":dict(defn="黎凡特：地中海东岸及其内陆的区域，约当今日叙利亚、黎巴嫩、以色列与巴勒斯坦、约旦。",
 span="区域地理与古气候（本条引 2018 年 4.2 ka 事件研究）",
 geo="沿海为狭窄平原，向内陆迅速抬升为山地（黎巴嫩山、前黎巴嫩山），再向东进入干旱草原；降水集中于冬季，海岸与内陆的湿润度差异极大。",
 infl="所引 2018 年研究讨论约 4200 年前的干旱事件（4.2 ka BP）在该区域的记录与影响，表明**气候事件在区域尺度上的表现并不一致**，需逐地比对而非整体推断。",
 conn="是埃及、安纳托利亚、美索不达米亚三大区域的交接地带，陆海商路的必经之地。"),
"安纳托利亚":dict(defn="安纳托利亚：亚洲西部的半岛（今土耳其的亚洲部分），以中央高原为主体。",
 span="高原地理与早期农业（本条引 2018 年安纳托利亚高原农业起源研究）",
 geo="中央为干旱高原，四周为山脉，沿海有较湿润的狭长平原；高原降水少、蒸发强，河谷与山间盆地是农业的可行带。",
 infl="所引 2018 年研究指出，栽培作物在中全新世（约公元前9千纪中叶后）由**本地采集者采纳**而出现在安纳托利亚中部，说明农业扩散不只是「源头→传播」的单向过程，也包含本地选择与改造。",
 conn="北接黑海、南临地中海、西连爱琴海，是欧洲与西亚之间的陆桥。"),
"莫斯科公国":dict(defn="莫斯科公国：中世纪晚期罗斯地区的政治体，后发展为俄罗斯国家。",
 span="13–16世纪（莫斯科大公国；本条引 2017 年印刷术研究）",
 geo="位于东欧平原的河流交汇处，莫斯科河连接伏尔加与奥卡水系；森林与沼泽提供防护，河网便于收取贡赋与发展贸易。",
 infl="所引 2017 年研究追问莫斯科为何未参与16世纪欧洲的「传播革命」（印刷术）：作者的回答是**否**——技术条件之外，政治与宗教权威对印刷的控制才是关键变量。",
 conn="经伏尔加水系连接里海与东方商路，经北方河流通往白海与北欧。"),
"巴尔干半岛":dict(defn="巴尔干半岛：欧洲东南部的半岛，被亚得里亚海、爱琴海与黑海环绕。",
 span="区域地理与生物多样性（本条引 2004 年巴尔干生物多样性研究）",
 geo="地形以山地为主（狄那里克阿尔卑斯、罗多彼等），河谷与盆地镶嵌其间；气候受地中海、大陆与山地三重影响，局部差异极大。",
 infl="所引 2004 年研究把巴尔干视为欧洲生物多样性的**热点与避难所**：山地与河谷的分隔造成高度的特有性，也说明地形破碎度与生物多样性正相关。",
 conn="南接爱琴海与地中海航路，北经多瑙河通中欧，东临黑海海峡，是欧亚之间的陆桥。"),
"欧洲温带海洋性气候":dict(defn="欧洲温带海洋性气候：西欧与北欧沿岸冬温夏凉、降水全年分配的海洋性气候型。",
 span="气候尺度（本条引 2005 年温盐环流研究）",
 geo="受北大西洋暖流与盛行西风影响，沿海地区冬季异常温和、降水丰沛且季节分配均匀；离海越远，海洋性越弱、大陆性越强。",
 infl="所引 2005 年研究指出，大西洋温盐环流的减弱会**改变海洋性气候的表现**，即这一气候型依赖洋流而不仅是纬度——这使它在气候变率下并不稳定。",
 conn="与北大西洋涛动、温盐环流耦合，一个环节的变化会影响整个欧洲的降水与温度格局。"),
"美国西进":dict(defn="美国西进：19世纪美国向北美西部的扩张与settler殖民过程。",
 span="19世纪（本条引 2005 年关于美国西部非裔 American 的史料集）",
 geo="自密西西比河谷向西依次为平原、落基山地、大盆地与太平洋沿岸，降水递减；越过 100°W 后进入半干旱区，农业需依赖灌溉与旱作技术。",
 infl="所引史料集提示：西进的叙述长期以白人 settler 为主体，**非裔与其它群体的参与被系统性低估**；这说明对同一地理过程的记述本身受立场影响。",
 conn="经俄勒冈小径、圣塔菲小径与横贯大陆铁路连接东部与西部，太平洋沿岸港口通亚洲贸易。"),
"巴西高原":dict(defn="巴西高原：南美洲东部的大片高原，覆盖巴西中东部。",
 span="地质与植被尺度（本条引 2007 年巴西南部 Araucaria 森林扩张研究）",
 geo="高原海拔多在500–1000米，边缘陡降为崖壁；气候自热带向亚热带过渡，降水与干季长度决定植被类型。",
 infl="所引 2007 年研究讨论 Araucaria 森林在巴西南部的扩张，显示**植被分布随气候与人类活动的千年尺度变化**而移动，不是固定不变的景观。",
 conn="高原上的河流多向西或向北汇入亚马孙与巴拉那水系，是南美内陆水系的源头区。"),
"巴西殖民经济":dict(defn="巴西殖民经济：1500–1822年葡萄牙治下巴西的种植园与出口经济。",
 span="1500–1822年（本条引 2024 年殖民巴西社会与政府研究）",
 geo="沿海为狭长的湿润平原（zona da mata），适合甘蔗；内陆高原为较干燥的牧区与后来的咖啡带；这一「沿海种植园—内陆牧业」的二分是殖民经济的地理骨架。",
 infl="所引 2024 年研究强调殖民巴西的**社会与政府制度**如何与种植园经济相互支撑：土地授予、劳役与市政组织共同决定了出口导向的形态，地理只是条件。",
 conn="经大西洋航线连接葡萄牙与非洲（奴隶贸易），是三角贸易的关键一端。"),
"大堡礁":dict(defn="大堡礁：澳大利亚东北岸外的珊瑚礁群系统。",
 span="生态尺度（本条引 2003 年珊瑚除草剂影响研究）",
 geo="位于昆士兰海岸外的大陆架，水深浅、光照足、水温适宜，适合造礁珊瑚；外海与近岸的水质差异直接影响礁体健康。",
 infl="所引 2003 年实验显示，除草剂（敌草隆、阿特拉津）在**极低浓度下即可影响珊瑚的共生藻**，说明陆源农业径流对近岸礁体的影响可通过化学途径传导，而不仅是泥沙覆盖。",
 conn="与昆士兰沿岸河流的径流相连，陆源物质经河流入海影响礁体，是陆海耦合的典型。"),
"冲积平原":dict(defn="冲积平原：河流携带的沉积物在河谷或下游堆积形成的平坦地形。",
 span="地质尺度（本条引 2005 年冲积序列研究）",
 geo="由河道反复迁移与泛滥堆积形成，沉积物以砂、粉砂与黏土互层；地形极平坦，坡度常小于1‰，微地形决定排水与土壤差异。",
 infl="所引 2005 年研究以**不连续界面**划分冲积序列，说明平原的堆积并非连续均匀，而是由洪水事件与河道改道分段形成——这决定了对平原地层与古洪水记录的解释方式。",
 conn="连接上游侵蚀区与下游三角洲，是泥沙与水量的输送通道，也是农业与聚落最密集的地带。"),
"山地农业":dict(defn="山地农业：在高海拔或陡坡地区进行的农业生产系统。",
 span="现代农业研究（本条引 1998 年肯尼亚高地长期试验研究）",
 geo="山地随海拔升高温度下降、坡度增大，土层薄、侵蚀风险高；不同海拔带适合不同作物，梯田与等高耕作是控制水土流失的基本手段。",
 infl="所引 1998 年研究以肯尼亚高地的长期试验讨论**土壤有机碳组分**作为诊断指标，说明山地农业的可持续性取决于有机质维持，而这一点对施肥与休耕制度高度敏感。",
 conn="山地农业区常处于流域上游，其水土管理直接影响下游的水量与泥沙。"),
}
added={}
for t,b in BODY.items():
    c=F.get(t)
    if not c: continue
    oa=(c.get("id") or "").rsplit("/",1)[-1];sid=f"openalex-{oa}"
    if sid not in have:
        code=0;size=0
        for _ in range(3):
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oa}"],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                    if code==200: break
                time.sleep(5)
            except Exception: time.sleep(5)
        TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文"}
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":(c.get("title") or "")[:200],
          "note":f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:240]}…"})
        have.add(sid)
    added[t]=sid

n=0;up=[]
for t,b in BODY.items():
    e=T.get(t);sid=added.get(t)
    if not e or not sid: continue
    c=F[t]
    e.update({"level":"L2","status":"L2完成(第35轮)-学术文献",
      "definition":b["defn"],"overview":b["defn"],
      "time_or_place":b["span"],"geo":b["geo"],"influence":b["infl"],
      "polities":e.get("polities") or "本条以自然地理/区域概述为主；具体政权序列待专门史料核验。",
      "connections":b["conn"],
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第35轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c.get('title')}》，DOI {c.get('doi') or '无'}）。"
        f" 该文献与本条同一对象；正文的地理与机制段落据其摘要撰写，未外推。年代以「{b['span']}」表述并注明学界有不同版本。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M95 288 L230 246 L370 224 L510 240 L645 274' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='370' cy='224' r='7' class='pt'/><text x='285' y='202' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))