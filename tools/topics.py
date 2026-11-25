# -*- coding: utf-8 -*-
"""按条目内容细分的主题示意图：气候（按气候型）、农业（按农作制）、贸易（按路线型）、区域（按形态）。"""
from schematics import L, P, R

def _frame(): return "<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"

# ---------------- 气候 ----------------
CLIM = {
 "季风":   ([.05,.06,.10,.20,.30,.55,.85,1.0,.7,.35,.12,.06], [.15,.2,.35,.55,.7,.85,1.0,.95,.75,.55,.35,.2], "季风气候（夏雨集中，雨热同期）"),
 "地中海": ([.7,.65,.55,.4,.25,.1,.05,.08,.25,.5,.7,.75], [.35,.4,.5,.65,.8,.92,1.0,.98,.85,.65,.48,.38], "地中海气候（冬雨夏干）"),
 "海洋性": ([.55,.5,.55,.5,.55,.5,.55,.6,.6,.6,.62,.58], [.35,.36,.42,.5,.58,.65,.7,.7,.63,.54,.45,.38], "温带海洋性（全年温和湿润）"),
 "沙漠":   ([.05,.04,.05,.04,.03,.02,.02,.03,.02,.03,.04,.05], [.3,.35,.5,.65,.8,.92,1.0,.98,.85,.65,.45,.32], "热带/干旱沙漠（全年少雨）"),
 "雨林":   ([.8,.78,.82,.8,.78,.7,.65,.66,.7,.78,.82,.8], [.85,.86,.88,.88,.87,.85,.84,.84,.85,.86,.86,.85], "热带雨林（全年高温多雨）"),
 "极地":   ([.15,.12,.1,.08,.06,.05,.05,.06,.08,.1,.12,.15], [.05,.06,.12,.22,.35,.45,.5,.45,.35,.25,.15,.08], "极地/寒带（全年低温）"),
 "高原":   ([.12,.14,.2,.3,.4,.55,.7,.68,.5,.3,.18,.13], [.1,.14,.25,.4,.55,.68,.8,.78,.62,.42,.28,.16], "高原山地气候（低温、日较差大）"),
}
def _which(title):
    t=title
    for k in ("季风","地中海","海洋性","沙漠","雨林","极地","高原"):
        if k in t: return k
    if "干旱" in t or "荒漠" in t: return "沙漠"
    if "温带" in t: return "海洋性"
    if "热带" in t: return "雨林"
    if "寒" in t or "冰" in t: return "极地"
    return None

def climate(title):
    key=_which(title)
    s=[_frame(),"<path d='M80 520 L80 300 L840 300' fill='none' stroke='var(--line)' stroke-width='1.4'/>"]
    s.append(L(40,300,"气温",c="lbl-s")+L(830,520,"月份",c="lbl-s"))
    if key:
        pr,tp,name=CLIM[key]
        for i,v in enumerate(pr):
            x=95+i*61; h=v*160
            s.append(f"<rect x='{x}' y='{500-h:.0f}' width='30' height='{h:.0f}' fill='#5b93b8' opacity='.7'/>")
        pts=[]
        for i,v in enumerate(tp):
            x=110+i*61; y=470-v*150
            pts.append(f"{x:.0f} {y:.0f}")
        s.append("<polyline points='"+' '.join(pts)+"' fill='none' stroke='#c0392b' stroke-width='3'/>")
        s.append(L(90,286,"%s：%s（降水柱·气温线，定性示意，无数值）"%(title,name),c="lbl-s"))
    else:
        for i in range(12):
            x=95+i*61; h=(.4+.15*((i*7)%3))*120
            s.append(f"<rect x='{x}' y='{500-h:.0f}' width='30' height='{h:.0f}' fill='#5b93b8' opacity='.6'/>")
        s.append("<polyline points='110,420 232,400 354,440 476,410 598,430 720,405 842,420' fill='none' stroke='#c0392b' stroke-width='3'/>")
        s.append(L(90,286,"%s：气温与降水年内变化（定性示意，无数值）"%title,c="lbl-s"))
    return "".join(s)

# ---------------- 农业 ----------------
def agriculture(title):
    t=title; s=[_frame()]
    if any(k in t for k in ("水稻","水田","稻作")):
        s.append(R(60,320,780,200,"#bcd6e8","#6f9db8")); 
        s.append("<g stroke='#8aa66a' stroke-width='1.5'>"+"".join(f"<path d='M{100+i*80} 330 v80'/>" for i in range(9))+"</g>")
        s.append("<path d='M60 350 C300 344 600 360 840 350' fill='none' stroke='#5b93b8' stroke-width='4'/>"+L(600,340,"水田/灌溉",c="lbl-s"))
        s.append(L(90,312,"%s · 稻作水田系统（蓄水—插秧—排水，示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("小麦","旱作","谷物","单产")):
        s.append(R(60,320,780,200,"#dcc9a0","#a08a5f"))
        s.append("<g stroke='#b79b5c' stroke-width='1.6'>"+"".join(f"<path d='M{100+i*70} 400 v70'/>" for i in range(10))+"</g>")
        s.append(L(90,312,"%s · 旱作农田（条播—轮作，示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("绿洲","灌溉","河谷")):
        s.append(R(60,320,780,200,"#e4cf94","#b99b4e")); s.append("<path d='M250 360 C350 352 500 372 650 360' fill='none' stroke='#5b93b8' stroke-width='5'/>")
        s.append("<g fill='#6f9a5a'>"+"".join(f"<circle cx='{c_}' cy='{y_}' r='6'/>" for c_,y_ in ((320,420),(420,440),(520,420),(620,440)))+"</g>")
        s.append(L(90,312,"%s · 绿洲灌溉农业（渠系—耕地，示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("游牧","畜牧","肉奶")):
        s.append(R(60,340,780,180,"#cfe0c0","#6f8a4a"))
        s.append("<g fill='#7a6a55'>"+"".join(f"<circle cx='{200+i*60}' cy='430' r='7'/>" for i in range(6))+"</g>")
        s.append(L(90,312,"%s · 游牧/草地畜牧（示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("种植园","殖民","企业","价值链")):
        s.append(R(60,320,780,200,"#d9c9a6","#a08a5f"))
        for r in range(3):
            s.append("<g stroke='#6f8a4a' stroke-width='2'>"+"".join(f"<path d='M{110+i*90} {350+r*50} v34'/>" for i in range(9))+"</g>")
        s.append(L(90,312,"%s · 种植园/商品农业（成行作物，示意）"%t,c="lbl-s"))
    else:
        s.append(R(60,320,780,200,"#dcc9a0","#a08a5f"))
        s.append("<g stroke='#8aa66a' stroke-width='1.6'>"+"".join(f"<path d='M{100+i*80} 330 v170'/>" for i in range(10))+"</g>")
        s.append("<path d='M60 360 C300 352 600 372 840 360' fill='none' stroke='#5b93b8' stroke-width='4'/>"+L(600,350,"灌溉渠",c="lbl-s"))
        s.append(L(90,312,"%s · 农业系统（耕地—灌排—作物，示意）"%t,c="lbl-s"))
    return "".join(s)

# ---------------- 贸易 ----------------
def _nodes_routes(s, nodes, color="#a4501a", curve=True):
    for i in range(len(nodes)-1):
        x1,y1=nodes[i]; x2,y2=nodes[i+1]
        if curve:
            s.append(f"<path d='M{x1} {y1} Q {(x1+x2)//2} {min(y1,y2)-40} {x2} {y2}' fill='none' stroke='{color}' stroke-width='2' stroke-dasharray='6 4'/>")
        else:
            s.append(f"<path d='M{x1} {y1} L{x2} {y2}' fill='none' stroke='{color}' stroke-width='2' stroke-dasharray='6 4'/>")
    for (x,y) in nodes:
        s.append(f"<circle cx='{x}' cy='{y}' r='7' fill='#2f6f8f'/>")

def trade(title):
    t=title; s=[_frame()]
    if any(k in t for k in ("海","航","港","殖民航线","海上")):
        s.append(R(60,310,780,220,"#cfe0ea","#6f9db8"))
        nodes=[(150,470),(330,420),(520,380),(700,340)]
        for i in range(len(nodes)-1):
            x1,y1=nodes[i]; x2,y2=nodes[i+1]
            s.append(f"<path d='M{x1} {y1} Q {(x1+x2)//2} {min(y1,y2)-50} {x2} {y2}' fill='none' stroke='#a4501a' stroke-width='2' stroke-dasharray='6 4'/>")
        for (x,y) in nodes:
            s.append(f"<path d='M{x-10} {y} l20 0 l-10 -14 Z' fill='#2f6f8f'/>")
        s.append(L(90,300,"%s · 海上航线（港口—航路，示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("丝","陆","路")):
        s.append(R(60,310,780,220,"#e7e0cf","#a08a5f"))
        nodes=[(140,460),(320,410),(500,360),(680,330),(800,360)]
        s.append("<path d='M140 460 C320 420 500 370 680 330 C740 322 780 340 800 360' fill='none' stroke='#a4501a' stroke-width='2.4' stroke-dasharray='7 5'/>")
        for (x,y) in nodes: s.append(f"<circle cx='{x}' cy='{y}' r='6' fill='#8a5636'/>")
        s.append(L(90,300,"%s · 陆上商路（节点—驿路，示意）"%t,c="lbl-s"))
    else:
        s.append(R(60,310,780,220,"#e7ecf0","var(--line)"))
        _nodes_routes(s,[(150,470),(320,400),(500,450),(680,380),(800,430)])
        s.append(L(90,300,"%s · 贸易网络（节点—路线，示意）"%t,c="lbl-s"))
    return "".join(s)

# ---------------- 区域 ----------------
def region(title):
    t=title; s=[_frame()]
    if any(k in t for k in ("群岛","岛")):
        s.append(R(60,310,780,220,"#cfe0ea","#6f9db8"))
        for (x,y,r) in ((200,420,16),(320,380,12),(430,440,18),(560,400,10),(680,430,14),(760,380,9)):
            s.append(f"<circle cx='{x}' cy='{y}' r='{r}' fill='#c6cdc4' stroke='#6f7a6c'/>")
        s.append(L(90,300,"%s · 群岛分布（示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("半岛",)):
        s.append(R(60,310,780,220,"#cfe0ea","#6f9db8"))
        s.append(P("120,330 520,360 560,420 520,480 120,510","#cbb98a","#a08a5f")+L(200,420,"半岛主体",c="lbl-s"))
        s.append(L(90,300,"%s · 半岛形态（三面临海，示意）"%t,c="lbl-s"))
    elif any(k in t for k in ("流域","河","江")):
        s.append(R(60,310,780,220,"#eef4f6","var(--line)"))
        s.append("<path d='M90 480 C260 380 420 380 500 430 C580 480 700 440 800 470' fill='none' stroke='#8a8272' stroke-width='1.4' stroke-dasharray='8 6'/>"+L(96,360,"分水岭",c="lbl-s"))
        s.append("<path d='M500 430 C600 436 700 440 800 452' fill='none' stroke='#5b93b8' stroke-width='4'/>")
        s.append(L(90,300,"%s · 流域范围（分水岭—干流，示意）"%t,c="lbl-s"))
    else:
        s.append(R(60,310,780,220,"#eef1f3","var(--line)"))
        s.append("<path d='M90 470 C300 420 520 500 800 440' fill='none' stroke='#2f6f8f' stroke-width='2' stroke-dasharray='7 5'/>")
        s.append("<rect x='330' y='360' width='240' height='120' fill='none' stroke='#a4501a' stroke-width='2' stroke-dasharray='8 6'/>")
        s.append("<circle cx='450' cy='420' r='6' fill='#c0392b'/>")
        s.append(L(90,300,"%s · 区域范围与对外联系（示意）"%t,c="lbl-s"))
    return "".join(s)

def draw(theme, title):
    return {"气候":climate,"农业":agriculture,"贸易":trade,"区域":region}.get(theme, region)(title)
