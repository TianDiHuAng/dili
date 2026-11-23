# -*- coding: utf-8 -*-
"""第37轮：14 条历史/区域类补充条目 → L2（OpenAlex 学术来源）。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round37_openalex.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述","dissertation":"学位论文"}

BODY={
"古埃及中王国":dict(span="约公元前1940–前1640年（据所引专著）",
 defn="古埃及中王国：古埃及的一个统一时期，约公元前1940–前1640年，以文学与行政的重建著称。",
 geo="核心仍在尼罗河谷与三角洲，法尤姆绿洲的灌溉开发扩大了耕地；河谷的南北轴线决定行政与运输的走向。",
 infl="所引 2010 年专著指出该时期是埃及书写的「黄金时代」，并重新评估文学作品的文化角色——此前常被视为王朝的宣传品。这说明文本的功能需具体分析，不能一概归为政治宣传。",
 conn="经努比亚走廊向南、经西奈与黎凡特向北、经红海通向蓬特，形成三向的外部联系。"),
"贵霜帝国":dict(span="约公元50–250年（据所引专著）",
 defn="贵霜帝国：内亚的古代帝国，约公元50–250年间支配中亚、南亚与东亚的部分地区。",
 geo="核心在中亚的巴克特里亚与犍陀罗（今阿富汗北部与巴基斯坦北部），处在印度、中亚与东亚之间的通道交汇处；山地与河谷控制商路节点。",
 infl="所引 2021 年研究称其为「欧亚的十字路口」：贵霜同时掌握政治军事控制与跨区域商路，成为文化（佛教艺术、钱币、文字）交流的枢纽。这说明过境位置在特定条件下可转化为制度性权力。",
 conn="南接印度河与恒河流域，东通塔里木盆地与中国，西连波斯与地中海东岸，是陆路丝绸之路的中段。"),
"室利佛逝":dict(span="7–13世纪（据所引 2021 年研究）",
 defn="室利佛逝：苏门答腊与马来半岛一带的海上城邦国家，7–13世纪间为印度洋与南海贸易的主要参与者。",
 geo="核心在苏门答腊东南部与马来半岛，扼马六甲海峡与巽他海峡的通道；季风风向决定帆船的往返季节，海峡位置因此具有枢纽价值。",
 infl="所引 2021 年研究强调其成长于「复杂网络」的中心：不是靠征服大片领土，而是靠对海峡通行与港口节点的控制。这说明海上政权可以不依赖陆地疆域而获得权力。",
 conn="西接印度洋航路（印度、阿拉伯），东连南海与中国港口，是两条海上贸易圈的交汇点。"),
"满者伯夷":dict(span="13–16世纪（满者伯夷；本条引 2022 年研究）",
 defn="满者伯夷：爪哇东部的古代帝国，被后世印尼民族运动视为国家荣光的象征。",
 geo="核心在爪哇东部布兰塔斯河下游的三角洲平原，火山土与季风降水支撑密集稻作；河网与港口连接内陆与外海。",
 infl="所引 2022 年研究讨论其社会政治史，并指出20世纪初印尼民族觉醒运动将其塑造为「过去荣光」的样板。这提示：历史叙述本身会被后世政治需要重新框架（D083 的立场问题）。",
 conn="经爪哇海连接苏门答腊、婆罗洲与马来半岛，经香料群岛通向东印尼的香料产地。"),
"帖木儿帝国":dict(span="14世纪末至15世纪（据所引 2025 年研究）",
 defn="帖木儿帝国：由阿米尔·帖木儿在14世纪末建立的中亚帝国，以撒马尔罕与赫拉特为中心。",
 geo="核心在河中地区（阿姆河与锡尔河之间）的绿洲带，撒马尔罕与赫拉特分别位于泽拉夫尚河与哈里河绿洲；绿洲之间的距离使城市成为控制点。",
 infl="所引 2025 年研究称该帝国在伊斯兰世界、蒙古遗产与波斯文化之间起**桥梁**作用，深刻影响中亚的建筑、文化与学术。这说明政权更替后文化生产可以延续并转型。",
 conn="东接天山与塔里木通中国，西经波斯通西亚，南越兴都库什通印度，北接草原。"),
"迈锡尼文明":dict(span="约公元前1600–前1100年（迈锡尼时期；所引研究聚焦前1400年后的扩张）",
 defn="迈锡尼文明：青铜时代晚期希腊大陆的文明，以城堡、线形文字 B 与广泛的贸易联系著称。",
 geo="核心在伯罗奔尼撒与希腊中部的山谷，城堡建于居高临下的丘陵；爱琴海的岛屿与航线提供交通，橄榄与葡萄适合山地。",
 infl="所引 1975 年研究指出，前1400年后迈锡尼文明有近两百年的繁荣期，部分建立在其已吸收的米诺斯文化之上；底比斯的陷落是该时期可确定的事件之一。这说明文明的扩张常以既有文化积累为基础。",
 conn="经爱琴海岛屿连接克里特与安纳托利亚西岸，经地中海东部航线通塞浦路斯、黎凡特与埃及。"),
"神圣罗马帝国":dict(span="约800/962年至1806年（所引专著称其延续千年）",
 defn="神圣罗马帝国：中欧的帝国体制，以「统一的基督教文明」为理念，延续约千年。",
 geo="覆盖今德国、奥地利、捷克、意大利北部与低地国家的广大区域，地形从阿尔卑斯山到北海沿岸；河流（莱茵、多瑙、易北）构成交通骨架。",
 infl="所引 2016 年专著（Peter Wilson）认为，帝国的连续性建立在理念而非集权行政之上，其遗产至今见于关于欧盟性质的讨论。这说明「帝国」可以是一种制度安排而非单一主权体。",
 conn="莱茵河与多瑙河分别通向北海与黑海，阿尔卑斯山口连接意大利，是中欧与地中海、东欧之间的枢纽。"),
"汉萨同盟":dict(span="13–17世纪（同盟 1669 年解散，据所引 2025 年研究）",
 defn="汉萨同盟：北德与波罗的海沿岸城市组成的商业同盟。",
 geo="核心在波罗的海与北海之间的低地平原与海峡城市（吕贝克、汉堡、但泽等），海运与河运交汇；鲱鱼与谷物是主要货类。",
 infl="所引 2025 年研究用 190 年的新贸易数据发现：1669 年同盟解散后，原汉萨航线的贸易量已回到引力模型的预测水平，但**同盟网络仍持续影响贸易构成**。这说明制度遗产可以在组织消亡后延续。",
 conn="经波罗的海通北欧与俄罗斯（诺夫哥罗德），经北海通英格兰与低地国家，是北欧贸易的骨干。"),
"基辅罗斯":dict(span="9–13世纪（基辅罗斯；所引 2025 年专著）",
 defn="基辅罗斯：中世纪东欧的政治体，以基辅为中心，连接北欧与拜占庭、东方。",
 geo="核心在第聂伯河与伏尔加河水系的上游，森林与森林草原交错；河流的南北走向使其成为「从瓦良格人到希腊人」的商路通道。",
 infl="所引 2025 年专著批评把罗斯简化为「拜占庭共同体」一部分的传统框架，认为这一框架**低估了与西欧的联系、放大了拜占庭影响**，并指出该叙事被民族主义修辞用于把俄罗斯与欧洲分隔。这属立场问题（D083）。",
 conn="北经波罗的海通斯堪的纳维亚，南沿第聂伯河通黑海与拜占庭，东经伏尔加河通伏尔加保加尔与东方。"),
"美拉尼西亚":dict(span="区域地理与近代史（所引 1985 年研究讨论「平定」过程）",
 defn="美拉尼西亚：太平洋西南部的岛群，包括新几内亚、所罗门、瓦努阿图、斐济等。",
 geo="岛屿多为大陆型与大岛，山地与雨林为主，语言与族群极度多样；火山与珊瑚礁并存，岛屿间的海距较短。",
 infl="所引 1985 年研究挑战「殖民统治与传教决定了平定进程」的通行看法，强调**岛民自身的利益与主动**在从部落战争走向持久和平中的作用。这提示外部力量并非唯一变量。",
 conn="经俾斯麦群岛与所罗门链连接新几内亚与波利尼西亚交界，是太平洋西南的航海与交换区。"),
"密克罗尼西亚":dict(span="区域地理与海洋生态（所引 2014 年研究）",
 defn="密克罗尼西亚：太平洋西部的众多小岛群，包括马里亚纳、加罗林、马绍尔等。",
 geo="岛屿多为珊瑚环礁与低平小岛，海拔极低、陆地面积小；海beyond为深海，淡水依赖降雨透镜，对海平面上升极为敏感。",
 infl="所引 2014 年研究讨论密克罗尼西亚岛屿在维持珊瑚礁遗传多样性中的作用，指出散布的小岛可能充当珊瑚三角区遗传多样性的**中转节点**。这说明小岛在生态网络中可以有超出其面积的重要性。",
 conn="位于珊瑚三角区以东，是太平洋生物扩散的踏脚石，也是近代跨太平洋航线的中继。"),
"复活节岛":dict(span="约公元1200年至历史时期（所引 2006 年研究：12世纪起清理棕榈）",
 defn="复活节岛（Rapa Nui）：东南太平洋的孤立火山岛，以巨型石像著称。",
 geo="面积小、远离大陆，火山土有限；淡水与海洋资源是生存基础，森林（棕榈）在12世纪起被清理。",
 infl="所引 2006 年研究以 Maunga Orito 的剖面揭示农业策略的序列：12世纪清理棕榈、开园种植薯蓣与芋，15世纪延续，17–19世纪出现覆土与石堆园。这说明岛屿社会长期**调整农业技术**以适应环境变化，而非单一崩溃叙事。",
 conn="与波利尼西亚东部群岛（马克萨斯、社会群岛）存在航海联系，是波利尼西亚三角的东南顶点。"),
"太平洋殖民航线":dict(span="约公元前1500年至公元后（Lapita 航海至东波利尼西亚）",
 defn="太平洋殖民航线：人类自东南亚向太平洋诸岛扩散的航海路线与技术水平。",
 geo="航线跨越从近大洋洲到远大洋洲的广阔海域，风向与洋流决定可行航向；岛屿间的距离逐步增大，对船只与导航的要求递增。",
 infl="所引 2008 年研究比较了不同阶段的海域难度：Lapita 航海者的海域**比近大洋洲更具挑战、但明显弱于后来东波利尼西亚人所面对的**；并据独木舟形制与性能估算航行能力。这说明「航海能力」应与具体海域条件匹配评估。",
 conn="从东南亚经近大洋洲到远大洋洲，最终抵达夏威夷、复活节岛与新西兰，构成地球史上最大规模的海洋扩散。"),
}
n=0;up=[];skip=[]
for t,b in BODY.items():
    e=T.get(t);c=F.get(t)
    if not e or not c: skip.append(t);continue
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
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c.get("title") or "")[:200],
          "note":f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:220]}…"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第37轮)-学术文献",
      "definition":b["defn"],"overview":b["defn"],
      "time_or_place":b["span"],"geo":b["geo"],"influence":b["infl"],
      "polities":e.get("polities") or "本条不展开完整统治者序列；具体世系与制度细节待专门史学来源核验。",
      "connections":b["conn"],
      "today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第37轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c.get('title')}》，DOI {c.get('doi') or '无'}，{c.get('host') or '出版方未标'}）。"
        f" 该文献与本条同一对象；机制/影响段据其撰写，geo 为常识性地理描述（未挂学术来源）。年代以「{b['span']}」表述。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 285 L235 245 L375 222 L515 238 L645 272' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='375' cy='222' r='7' class='pt'/><text x='285' y='200' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print("跳过",skip)
print("剔除：南美贸易网络（命中菲律宾文献，对象错误）")
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))