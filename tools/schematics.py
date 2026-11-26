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


def biome(title):
    bands=[("极地苔原/冰原","#dfe8ea"),("亚寒带针叶林","#9fb8a8"),("温带落叶林","#a9d0a0"),
           ("温带草原","#cfe0c0"),("亚热带常绿林","#7fbf6a"),("热带雨林","#4f9a4a"),("干旱荒漠","#e0c078")]
    s=["<rect x='60' y='180' width='780' height='230' fill='none' stroke='var(--line)'/>"]
    y=180
    for i,(nm,col) in enumerate(bands):
        h=230/len(bands)
        s.append(f"<rect x='60' y='{y:.0f}' width='780' height='{h:.0f}' fill='{col}' stroke='#ffffff' stroke-width='1'/>")
        s.append(L(72,int(y+h/2)+4,nm,c="lbl-s"))
        y+=h
    s.append(L(60,170,"%s · 纬度—气候—植被地带性（示意，由赤道向两极）"%title,c="lbl-s"))
    return "".join(s)

def cycle(title):
    s=["<rect x='60' y='150' width='780' height='280' rx='10' fill='#eef4f6' stroke='var(--line)'/>"]
    box=[(120,200,"海洋"),(360,200,"大气"),(600,200,"陆地"),(360,340,"地下水/土壤")]
    for x,y,nm in box:
        s.append(f"<rect x='{x-50}' y='{y-26}' width='100' height='52' rx='8' fill='#ffffff' stroke='#6f9db8'/>"+L(x-24,y+5,nm,c="lbl-s"))
    def arrow(x1,y1,x2,y2):
        return f"<path d='M{x1} {y1} L{x2} {y2}' stroke='#2f6f8f' stroke-width='2' marker-end=''/>"+f"<polygon points='{x2},{y2} {x2-8},{y2-4} {x2-8},{y2+4}' fill='#2f6f8f'/>"
    s.append(arrow(170,200,310,200)+L(210,190,"蒸发",c="lbl-s"))
    s.append(arrow(410,200,550,200)+L(455,190,"降水",c="lbl-s"))
    s.append(arrow(600,226,410,340)+L(470,300,"径流/下渗",c="lbl-s"))
    s.append(arrow(330,340,150,226)+L(210,300,"地下汇流",c="lbl-s"))
    s.append(L(60,140,"%s · 海陆间水循环（蒸发—水汽输送—降水—径流/下渗，示意）"%title,c="lbl-s"))
    return "".join(s)


def lake(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + P("40,360 40,240 260,240 340,320 560,320 640,240 860,240 860,360","#cbb98a","#a08a5f")
      + "<path d='M340 300 C420 292 500 308 560 300 L560 320 L340 320 Z' fill='#a9cbe0' stroke='#6f9db8'/>"
      + "<path d='M120 250 C200 246 300 252 340 260' fill='none' stroke='#5b93b8' stroke-width='4'/>"
      + "<path d='M560 262 C640 258 740 252 820 248' fill='none' stroke='#5b93b8' stroke-width='4'/>"
      + L(90,232,"入湖河",c="lbl-s")+L(700,232,"出湖河",c="lbl-s")+L(400,290,"湖面/水体",c="lbl-s")
      + R(340,320,220,10,"#8f8a80","#5f5a52")+L(360,344,"湖底沉积",c="lbl-s")
      + L(40,430,"湖泊剖面 · 示意图，非精确测绘",c="dim"))

def aquifer(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + R(40,220,820,44,"#cbb98a","#a08a5f")+L(60,248,"地表/包气带",c="lbl-s")
      + R(40,264,820,60,"#a9cbe0","#6f9db8")+L(60,300,"含水层（饱和带）",c="lbl-s")
      + "<path d='M40 264 H860' stroke='#2f6f8f' stroke-width='2' stroke-dasharray='7 5'/>"+L(700,258,"潜水面",c="lbl-s")
      + R(40,324,820,30,"#8f8a80","#5f5a52")+L(60,344,"隔水层",c="lbl-s")
      + R(600,180,18,144,"#ffffff","#5f5a52")+L(560,176,"井",c="lbl-s")
      + "<path d='M609 264 L609 210' stroke='#5b93b8' stroke-width='3'/>"
      + L(40,430,"地下水/含水层剖面 · 示意图，非精确测绘",c="dim"))

def danxia(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + P("40,360 40,220 200,220 200,180 360,180 360,240 520,240 520,200 700,200 700,260 860,260 860,360","#c06a48","#8a3f26")
      + "<g stroke='#8a3f26' stroke-width='1.2' opacity='.8'><path d='M200 180 V360'/><path d='M360 180 V360'/><path d='M520 200 V360'/><path d='M700 260 V360'/></g>"
      + L(200,168,"陡崖/方山（红色砂砾岩）",c="lbl-s")+L(60,410,"红层+垂直节理→陡崖、峰林",c="lbl-s")
      + L(40,430,"丹霞地貌剖面 · 示意图，非精确测绘",c="dim"))

def coral(title):
    return ("<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"
      + R(40,300,820,90,"#a9cbe0","#6f9db8")+L(60,320,"海面",c="lbl-s")
      + P("160,340 260,250 380,340","#e2b98f","#a06a3a")+L(200,240,"礁脊",c="lbl-s")
      + "<path d='M120 340 C220 300 320 300 420 340' fill='none' stroke='#5b93b8' stroke-width='2'/>"
      + P("420,340 520,300 640,340","#cfa77a","#8a5a30")+L(470,292,"礁前斜坡",c="lbl-s")
      + "<g fill='#d98f6a'><circle cx='200' cy='320' r='4'/><circle cx='230' cy='330' r='4'/><circle cx='300' cy='322' r='4'/><circle cx='480' cy='330' r='4'/></g>"
      + L(80,410,"潟湖",c="lbl-s")+L(700,320,"外海",c="lbl-s")
      + L(40,430,"珊瑚礁剖面 · 示意图，非精确测绘",c="dim"))


def yardang(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       R(40,300,820,90,"#e4cf94","#b99b4e")]
    for x in (140,320,500,680):
        s.append(f"<path d='M{x} 300 C{x+30} 250 {x+80} 250 {x+110} 300 Z' fill='#c9ab63' stroke='#98874f'/>")
    s.append("<path d='M60 220 L260 220' stroke='#a4501a' stroke-width='2'/><polygon points='260,216 260,224 272,220' fill='#a4501a'/>"+L(70,212,"风向",c="lbl-s"))
    s.append(L(150,250,"流线型风蚀垄（雅丹）",c="lbl-s")+L(150,410,"风蚀垄间槽",c="lbl-s"))
    s.append(L(40,430,"雅丹地貌剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def fjord(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,360 40,140 220,140 320,300 320,360","#9fb2c8","#5c6d84"),
       P("860,360 860,140 680,140 580,300 580,360","#9fb2c8","#5c6d84"),
       R(320,300,260,60,"#a9cbe0","#6f9db8")]
    s.append("<path d='M320 300 C380 340 500 340 580 300' fill='none' stroke='#5b93b8' stroke-width='2'/>")
    s.append(L(120,132,"陡峭谷壁（冰蚀 U 形谷）",c="lbl-s")+L(400,330,"海水侵入（峡湾）",c="lbl-s")+L(420,292,"冰蚀槛",c="lbl-s"))
    s.append(L(40,430,"峡湾剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def oxbow(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       R(40,240,820,150,"#cbb98a","#a08a5f")]
    s.append("<path d='M80 320 C220 260 340 320 420 320 C560 320 640 250 780 300' fill='none' stroke='#5b93b8' stroke-width='6'/>")
    s.append("<path d='M300 300 C340 230 460 230 500 300 C460 268 340 268 300 300 Z' fill='#a9cbe0' stroke='#6f9db8'/>")
    s.append(L(340,222,"牛轭湖（截弯取直后遗留）",c="lbl-s")+L(90,300,"主河道",c="lbl-s"))
    s.append("<path d='M600 300 C660 270 720 274 760 292' fill='none' stroke='#a4501a' stroke-width='1.6' stroke-dasharray='6 4'/>"+L(620,264,"截弯取直",c="lbl-s"))
    s.append(L(40,430,"曲流与牛轭湖 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def faultblock(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,360 40,300 220,300 300,220 460,220 540,300 720,300 800,240 860,240 860,360","#b7a58c","#7a6a55")]
    s.append("<path d='M260 220 L200 360' stroke='#7a3b16' stroke-width='2'/>"+L(196,214,"正断层",c="lbl-s"))
    s.append("<path d='M600 220 L660 360' stroke='#7a3b16' stroke-width='2'/>")
    s.append("<path d='M380 300 L380 268' stroke='#a4501a' stroke-width='2'/><polygon points='376,272 384,272 380,262' fill='#a4501a'/>"+L(320,296,"山块抬升",c="lbl-s"))
    s.append("<path d='M500 268 L500 300' stroke='#2f6f8f' stroke-width='2'/><polygon points='496,296 504,296 500,306' fill='#2f6f8f'/>"+L(510,290,"盆地下陷",c="lbl-s"))
    s.append(L(40,430,"断块山剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)

def terrace(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>"]
    steps=[(40,360,220,300),(220,300,380,250),(380,250,520,210),(520,210,700,180)]
    for x0,y0,x1,y1 in steps:
        s.append(P(f"{x0},{y0} {x0},{y1} {x1},{y1} {x1},{y0}","#cbb98a","#a08a5f"))
        s.append(L(x0+8,y1+16,"阶地面",c="lbl-s"))
    s.append("<path d='M40 360 L860 360' stroke='#5b93b8' stroke-width='3'/>"+L(60,382,"河水面",c="lbl-s"))
    s.append(L(120,420,"多级阶地（河流下切形成，越上越老）",c="lbl-s"))
    s.append(L(40,440,"河流阶地剖面 · 示意图，非精确测绘",c="dim"))
    return "".join(s)


def moraine(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",R(40,300,820,90,"#cbb98a","#a08a5f")]
    for x in (120,240,360,480,600,720):
        s.append(f"<path d='M{x} 300 C{x+20} 254 {x+60} 254 {x+80} 300 Z' fill='#b9a98a' stroke='#7a6a55'/>")
    s.append("<path d='M80 230 L300 230' stroke='#2f6f8f' stroke-width='2'/><polygon points='300,226 300,234 312,230' fill='#2f6f8f'/>"+L(90,222,"冰流向",c="lbl-s"))
    s.append(L(120,264,"冰碛丘陵（冰碛物堆积成的丘岗）",c="lbl-s")+L(120,410,"底碛/终碛",c="lbl-s"))
    s.append(L(40,430,"冰碛丘陵剖面 · 示意图，非精确测绘",c="dim"));return "".join(s)

def seacliff(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,150 320,150 340,300 60,300","#b7a58c","#7a6a55"),
       R(60,300,760,90,"#a9cbe0","#6f9db8")]
    s.append("<path d='M320 220 C360 250 340 280 300 290' fill='none' stroke='#7a6a55' stroke-width='2'/>"+L(250,214,"海蚀崖",c="lbl-s"))
    s.append("<path d='M340 300 L560 316' stroke='#98874f' stroke-width='3'/>"+L(380,338,"海蚀平台",c="lbl-s"))
    s.append("<path d='M600 300 q20 -10 40 0 t40 0' stroke='#5b93b8' stroke-width='2' fill='none'/>"+L(640,290,"波浪侵蚀",c="lbl-s"))
    s.append(L(40,430,"海蚀崖剖面 · 示意图，非精确测绘",c="dim"));return "".join(s)

def tidalflat(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,260 860,300 860,360 40,360","#cbb98a","#a08a5f"),
       R(40,300,820,60,"#a9cbe0","#6f9db8",op=".5")]
    s.append("<path d='M40 284 H860' stroke='#2f6f8f' stroke-width='2' stroke-dasharray='8 6'/>"+L(700,278,"高潮线",c="lbl-s"))
    s.append("<path d='M120 330 C260 326 360 334 480 330' fill='none' stroke='#5b93b8' stroke-width='2'/>"+L(200,324,"潮沟",c="lbl-s"))
    s.append(L(120,250,"潮滩（粉砂/淤泥质，坡度极缓）",c="lbl-s"))
    s.append(L(40,430,"潮滩剖面 · 示意图，非精确测绘",c="dim"));return "".join(s)

def soilerosion(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,240 400,240 480,360 40,360","#b98a52","#8a5636"),
       R(40,360,820,30,"#e4cf94","#b99b4e")]
    for x in (140,220,300):
        s.append(f"<path d='M{x} 250 L{x+40} 356' stroke='#8a5636' stroke-width='2' fill='none'/>")
    s.append(L(150,232,"坡面细沟/切沟侵蚀",c="lbl-s")+L(500,388,"坡脚堆积泥沙",c="lbl-s"))
    s.append("<g stroke='#5b93b8' stroke-width='1.4'><path d='M320 200 l-6 14'/><path d='M360 200 l-6 14'/></g>"+L(300,192,"降雨溅蚀",c="lbl-s"))
    s.append(L(40,430,"土壤侵蚀剖面 · 示意图，非精确测绘",c="dim"));return "".join(s)


def floodplain(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,300 40,250 320,250 340,300 340,360 40,360","#cbb98a","#a08a5f"),
       P("860,300 860,250 580,250 560,300 560,360 860,360","#cbb98a","#a08a5f"),
       R(340,330,220,30,"#a9cbe0","#6f9db8")]
    s.append("<path d='M340 300 C360 270 520 270 560 300' fill='#a9cbe0' stroke='#6f9db8'/>")
    s.append("<path d='M40 268 H860' stroke='#2f6f8f' stroke-width='1.6' stroke-dasharray='8 6'/>"+L(600,262,"洪水位",c="lbl-s"))
    s.append(L(110,242,"天然堤",c="lbl-s")+L(740,242,"天然堤",c="lbl-s")+L(380,352,"河道",c="lbl-s"))
    s.append(L(60,410,"河漫滩（洪水泛滥淤积的平坦谷底）",c="lbl-s"))
    s.append(L(40,430,"河漫滩剖面 · 示意图，非精确测绘",c="dim"));return "".join(s)

def alluvialfan(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       P("40,150 40,360 200,300 200,150","#9fb2c8","#5c6d84")]
    s.append("<path d='M200 220 L760 150 L760 340 L200 300 Z' fill='#d9b26a' stroke='#a9822f'/>")
    for i in range(5):
        s.append(f"<path d='M210 {230+i*15} C400 {210+i*10} 560 {190+i*12} 750 {165+i*30}' fill='none' stroke='#a9822f' stroke-width='1'/>")
    s.append(L(120,142,"山口（扇顶）",c="lbl-s")+L(520,250,"扇面（坡度变缓、颗粒变细）",c="lbl-s"))
    s.append(L(280,300,"粗砾",c="lbl-s")+L(700,330,"砂/粉砂",c="lbl-s"))
    s.append(L(40,430,"冲积扇平面 · 示意图，非精确测绘",c="dim"));return "".join(s)

def permafrost(title):
    s=["<rect x='21' y='21' width='858' height='70' fill='#eef3f6' opacity='.4'/>",
       R(40,220,820,30,"#c9b48c","#8a7452")+L(60,240,"地表/活动层（季节性冻融）",c="lbl-s"),
       R(40,250,820,110,"#bcd0e0","#6f9db8")+L(60,320,"多年冻土（常年冻结）",c="lbl-s")]
    s.append("<path d='M400 250 L430 330 L400 360 L370 330 Z' fill='#ffffff' stroke='#6f9db8'/>"+L(360,232,"冰楔",c="lbl-s"))
    s.append("<path d='M600 250 C640 290 600 330 640 360' fill='none' stroke='#5b93b8' stroke-width='2'/>"+L(650,300,"热喀斯特（冻融塌陷）",c="lbl-s"))
    s.append(L(40,430,"多年冻土剖面 · 示意图，非精确测绘",c="dim"));return "".join(s)

KINDS = {"basin":basin,"plain":plain,"delta":delta,"range":range_,"hills":hills,"plateau":plateau,
         "desert":desert,"rift":rift,"coast":coast,"river":river,"island":island,"ice":ice,"biome":biome,"cycle":cycle,"lake":lake,"aquifer":aquifer,"danxia":danxia,"coral":coral,"yardang":yardang,"fjord":fjord,"oxbow":oxbow,"faultblock":faultblock,"terrace":terrace,"moraine":moraine,"seacliff":seacliff,"tidalflat":tidalflat,"soilerosion":soilerosion,"floodplain":floodplain,"alluvialfan":alluvialfan,"permafrost":permafrost}

def pick(title):
    t = title
    if "冰川湖" in t: return "lake"
    if any(k in t for k in ("冰盖","冰川","冰架","南极大陆","罗斯海","冰芯")): return "ice"
    if "河漫滩" in t: return "floodplain"
    if "冲积扇" in t: return "alluvialfan"
    if "冻土" in t: return "permafrost"
    if "冰碛" in t: return "moraine"
    if "海蚀" in t: return "seacliff"
    if "潮滩" in t: return "tidalflat"
    if "土壤侵蚀" in t: return "soilerosion"
    if "冰川湖" in t: return "lake"
    if "雅丹" in t: return "yardang"
    if "峡湾" in t: return "fjord"
    if "牛轭" in t: return "oxbow"
    if "断块" in t: return "faultblock"
    if "阶地" in t: return "terrace"
    if "地下水" in t: return "aquifer"
    if "丹霞" in t: return "danxia"
    if "珊瑚" in t: return "coral"
    if "湖" in t: return "lake"
    if any(k in t for k in ("裂谷",)): return "rift"
    if any(k in t for k in ("三角洲",)): return "delta"
    if any(k in t for k in ("盆地","平原")) and "平原" in t: return "plain"
    if any(k in t for k in ("盆地",)): return "basin"
    if any(k in t for k in ("平原",)): return "plain"
    if any(k in t for k in ("沙漠","戈壁","荒漠","风成","风蚀","沙丘")): return "desert"
    if any(k in t for k in ("生物群系","植被带","生物群落")): return "biome"
    if any(k in t for k in ("水循环",)): return "cycle"
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
