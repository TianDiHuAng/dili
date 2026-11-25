# -*- coding: utf-8 -*-
"""类型化地貌剖面库：按关键词选择剖面（彩绘式，内联 SVG，900x460 区域内）。"""
def L(x,y,s,c="lbl"): return f"<text x='{x}' y='{y}' class='{c}'>{s}</text>"
def P(pts,fill,stroke="#8a7452",op=None,sw=1.2):
    o=f" fill-opacity='{op}'" if op else ""
    return f"<polygon points='{pts}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{o}/>"
def R(x,y,w,h,fill,stroke="#8a7452",op=None):
    o=f" fill-opacity='{op}'" if op else ""
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{fill}' stroke='{stroke}'{o}/>"

def basin(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,300 40,180 200,180 300,300 600,300 700,180 860,180 860,300","#c9b48c","#8a7452"),
       R(300,300,300,70,"#8f8a80","#5f5a52"), R(300,300,300,16,"#dcd2c0","#a08a5f"),
       L(330,342,"稳定基底",c="lbl-s"),L(90,214,"盆缘山地",c="lbl-s"),L(720,214,"盆缘山地",c="lbl-s"),
       L(360,238,"盆内充填（沉积盖层）",c="lbl-s"),L(40,430,"盆地剖面 · 示意图，非精确测绘",c="dim")]
    return "".join(s)

def plain(title,river=True):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       R(40,300,820,90,"#cbb98a","#a08a5f"), R(40,300,820,26,"#d9c9a6","#a08a5f",op=".9"),
       "<g stroke='#8aa66a' stroke-width='1.3'>"+"".join(f"<path d='M{110+i*80} 320 v64'/>" for i in range(10))+"</g>"]
    if river: s.append("<path d='M40 352 C300 344 600 366 860 348' fill='none' stroke='#5b93b8' stroke-width='5'/>"+L(600,338,"河流/灌渠",c="lbl-s"))
    s += [L(90,292,"冲积层（河湖相沉积）",c="lbl-s"),L(90,410,"耕地/平原面",c="lbl-s"),L(40,430,"平原剖面 · 示意图，非精确测绘",c="dim")]
    return "".join(s)

def delta(title):
    s=[R(40,300,520,90,"#cbb98a","#a08a5f"), P("560,300 860,300 860,390 620,390","#a9cbe0","#6f9db8",op=".9"),
       "<path d='M60 340 C260 336 420 342 560 338' fill='none' stroke='#5b93b8' stroke-width='6'/>"]
    for dy in (320,350,375):
        s.append(f"<path d='M560 338 C650 33{dy%10} 740 {dy} 860 {dy}' fill='none' stroke='#5b93b8' stroke-width='3'/>")
    s += [L(80,292,"三角洲平原",c="lbl-s"),L(690,330,"分流河道",c="lbl-s"),L(760,410,"海（河口湾）",c="lbl-s"),L(40,430,"三角洲剖面 · 示意图，非精确测绘",c="dim")]
    return "".join(s)

def range_(title,parallel=False):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"]
    if parallel:
        s.append(P("40,360 150,180 240,240 340,150 440,240 540,170 640,250 740,190 860,360","#9fb2c8","#5c6d84"))
        for x in (240,440,640): s.append(f"<path d='M{x} 250 L{x-30} 360 L{x+30} 360 Z' fill='#cfd6cd' stroke='#5c6d84'/>")
        s.append(L(150,168,"平行岭谷（V 形谷）",c="lbl-s"))
    else:
        s.append(P("40,360 160,150 260,230 360,120 470,240 580,150 700,250 860,360","#b7a58c","#7a6a55"))
        s.append(P("330,150 360,120 395,152","#ffffff","#c3d3d9")); s.append(L(345,146,"雪线/高峰",c="lbl-s"))
    s += [R(40,360,820,60,"#cbb98a","#a08a5f")]
    if not parallel: s.append("<path d='M60 400 C300 390 600 408 840 392' fill='none' stroke='#5b93b8' stroke-width='3'/>")
    s += [L(60,410,"山前冲积/山麓带",c="lbl-s"),L(40,430,"山脉剖面 · 示意图，非精确测绘",c="dim")]
    return "".join(s)

def hills(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      "<path d='M40 340 C120 270 200 300 280 260 C360 220 440 300 520 250 C600 200 700 300 780 250 C820 226 850 250 860 240 L860 340 Z' fill='#c9d6b0' stroke='#6f8a4a'/>"
      + R(40,340,820,50,"#c08a5a","#8a5636") + R(40,356,820,10,"#b06b3a","#8a5636")
      + L(90,330,"丘陵（缓丘起伏）",c="lbl-s")+L(90,402,"土层/风化壳",c="lbl-s")+L(620,232,"侵蚀/梯田",c="lbl-s")
      + L(40,430,"丘陵剖面 · 示意图，非精确测绘",c="dim"))

def plateau(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + P("40,360 40,220 300,220 360,180 700,180 760,220 860,220 860,360","#d9b26a","#a9822f")
      + R(40,360,820,60,"#8f8a80","#5f5a52")
      + L(120,210,"高原面（顶面平缓）",c="lbl-s")+L(560,172,"边缘陡坎/断崖",c="lbl-s")
      + "<path d='M60 330 C300 320 600 340 840 326' fill='none' stroke='#5b93b8' stroke-width='2' opacity='.6'/>"
      + L(40,430,"高原剖面 · 示意图，非精确测绘",c="dim"))

def desert(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + R(40,300,820,90,"#e4cf94","#b99b4e")
      + "<g fill='none' stroke='#c2a45c' stroke-width='1.6'>"+"".join(f"<path d='M{110+i*95} 360 q22 -22 44 0'/>" for i in range(8))+"</g>"
      + "<path d='M110 344 L150 344' stroke='#a4501a' stroke-width='1.4'/><polygon points='150,341 150,347 160,344' fill='#a4501a'/>"
      + L(90,292,"沙丘（风向自左向右）",c="lbl-s")+L(600,410,"砾漠/戈壁",c="lbl-s")
      + L(40,430,"沙漠剖面 · 示意图，非精确测绘",c="dim"))

def rift(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + P("40,360 40,220 300,220 400,360","#b7a58c","#7a6a55") + P("860,360 860,220 600,220 500,360","#b7a58c","#7a6a55")
      + R(400,300,100,60,"#c98a6a","#8a5636") + "<path d='M420 330 L480 330' stroke='#c0392b' stroke-width='2'/>"
      + L(120,210,"断块山地",c="lbl-s")+L(430,352,"裂谷/地堑（下陷）",c="lbl-s")+L(700,210,"断块山地",c="lbl-s")
      + L(40,430,"裂谷剖面 · 示意图，非精确测绘",c="dim"))

def coast(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + R(40,300,480,90,"#cbb98a","#a08a5f") + R(520,300,340,90,"#a9cbe0","#6f9db8")
      + "<path d='M520 300 C560 330 540 360 520 390' fill='none' stroke='#5b93b8' stroke-width='3'/>"
      + "<g stroke='#7fb0cf' stroke-width='2' fill='none'><path d='M600 340 q10 -8 20 0 t20 0'/><path d='M640 360 q10 -8 20 0 t20 0'/></g>"
      + L(120,292,"陆地",c="lbl-s")+L(700,292,"海/湾",c="lbl-s")+L(500,412,"海岸线/海滩",c="lbl-s")
      + L(40,430,"海岸剖面 · 示意图，非精确测绘",c="dim"))

def river(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + P("40,340 40,200 260,200 320,250 320,340","#b7a58c","#7a6a55")
      + R(320,300,520,60,"#cbb98a","#a08a5f")
      + "<path d='M140 210 C220 260 300 300 360 340 C520 348 700 344 820 336' fill='none' stroke='#5b93b8' stroke-width='6'/>"
      + L(80,190,"山地/源头",c="lbl-s")+L(520,332,"河漫滩/冲积平原",c="lbl-s")+L(760,322,"河口",c="lbl-s")
      + L(40,430,"河流剖面 · 示意图，非精确测绘",c="dim"))

def island(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + R(40,320,820,70,"#a9cbe0","#6f9db8")
      + P("300,320 360,220 420,320","#c6cdc4","#6f7a6c") + P("470,320 520,250 570,320","#cfd6cd","#6f7a6c")
      + L(340,210,"火山岛/主岛",c="lbl-s")+L(600,352,"环礁/浅海",c="lbl-s")
      + L(40,430,"岛屿剖面 · 示意图，非精确测绘",c="dim"))

def ice(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + R(40,300,820,90,"#8f8a80","#5f5a52")
      + P("40,300 120,240 300,220 520,210 700,225 860,250 860,300","#eef4f6","#c3d3d9")
      + "<path d='M120 300 C200 290 260 296 320 288' fill='none' stroke='#5b93b8' stroke-width='2' opacity='.7'/>"
      + L(120,205,"冰盖/冰川",c="lbl-s")+L(360,330,"冰下基岩",c="lbl-s")+L(300,278,"冰流/融水",c="lbl-s")
      + L(40,430,"冰盖剖面 · 示意图，非精确测绘",c="dim"))

KINDS = {"basin":basin,"plain":plain,"delta":delta,"range":range_,"hills":hills,"plateau":plateau,
         "desert":desert,"rift":rift,"coast":coast,"river":river,"island":island,"ice":ice}

def pick(title):
    t = title
    if any(k in t for k in ("冰盖","冰川","冰架","南极大陆","罗斯海","冰芯")): return "ice"
    if any(k in t for k in ("裂谷",)): return "rift"
    if any(k in t for k in ("三角洲",)): return "delta"
    if any(k in t for k in ("盆地","平原")) and "平原" in t: return "plain"
    if any(k in t for k in ("盆地",)): return "basin"
    if any(k in t for k in ("平原",)): return "plain"
    if any(k in t for k in ("沙漠","戈壁","荒漠")): return "desert"
    if any(k in t for k in ("高原",)): return "plateau"
    if any(k in t for k in ("丘陵",)): return "hills"
    if any(k in t for k in ("山脉","山","岭")): return "range"
    if any(k in t for k in ("海","湾","海峡","半岛","海岸")): return "coast"
    if any(k in t for k in ("群岛","岛")): return "island"
    if any(k in t for k in ("河","江","湖","流域")): return "river"
    return "range"

def draw(title):
    k = pick(title)
    return KINDS[k](title)
