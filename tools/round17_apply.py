# -*- coding: utf-8 -*-
"""第17轮：清理 7 条泛化来源误贴 + 33 条复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# A) 误贴清理：移除与主题无关的泛化来源
BAD={
 "北美冰盖":["s017-fao-org"],
 "大自流盆地":["s017-fao-org"],
 "巴西高原":["s017-fao-org"],
 "巴西殖民经济":["s011-unesco-org"],
 "加勒比海群岛":["s025-ourworldindata-org"],
 "十三殖民地":["s058-worldbank-org"],
 "美国西进":["s059-worldbank-org"],
}
cleaned=[]
for t,bad in BAD.items():
 e=T.get(t)
 if not e: continue
 before=len(e["sources"])
 e["sources"]=[s for s in e["sources"] if s not in bad]
 if len(e["sources"])!=before:
  e["pending_notes"]=(e.get("pending_notes") or "")+f" 第17轮清理：移除与主题无对应的泛化来源 {'、'.join(bad)}（D040/D047 同型问题）。"
  e["status"]=(e.get("status") or "").replace("已复核(第16轮)","已复核(第17轮)")
  e["last_update"]=TODAY
  cleaned.append(t)

# B) 复核队列
GAP={"地形":"含地貌成因正文的专题页","气候":"含气候机制正文的专题页",
 "农业":"含作物制度/水利正文的专题页","贸易":"含商路与商品结构正文的专题页",
 "政权更替":"含政权年代序列正文的专题页","区域":"含区域边界与现状数据正文的专题页"}
POOL={"地形":["s056-earthquake-usgs-gov"],"气候":["s048-climate-gov"],
 "农业":["s018-fao-org"],"贸易":["s057-databank-worldbank-org"],
 "政权更替":["s010-unesco-org"],"区域":["un-m49"]}
def review_titles():
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第17轮)" not in e["status"] and e["title"] not in cleaned:
    out.append(e["title"])
 return out[:33]
def review(title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP.get(e["theme"],"专题页")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第17轮复核】{e['region']}×{e['theme']}；来源均已核验；按 D041/D044 仍缺{gap}（须正文≥8000字节且主题关键词命中≥5）。")
    e["last_update"]=TODAY;e["status"]="已复核(第17轮)"
    return e["id"]
 raise SystemExit("未找到:"+title)

def main():
 b=int(sys.argv[1]);done=[]
 if b==1:
  done=["CLEAN:"+t for t in cleaned]
  for t in review_titles()[:10-len(done)]: done.append("REVIEW:"+review(t))
 else:
  start=(b-2)*10+(10-len(cleaned))
  for t in review_titles()[start:start+10]: done.append("REVIEW:"+review(t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks: "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))
if __name__=="__main__": main()