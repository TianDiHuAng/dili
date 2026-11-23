# -*- coding: utf-8 -*-
"""第44轮返工（口径）：统一 ac() 实现——读 note 实测正文字符/字节，不用 id 前缀；重算 baseline 与 after。"""
import json,os,re,subprocess,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

MIN_CHARS=800   # 判定「有正文」的最小字符/字节阈值

def load(unit, rev=None):
    if rev is None:
        return json.load(open(os.path.join(DATA,unit+".json"),encoding="utf-8"))
    raw=subprocess.run(["git","show",f"{rev}:data/{unit}.json"],cwd=ROOT,capture_output=True).stdout.decode("utf-8","ignore")
    return json.loads(raw) if raw.strip() else {"entries":[]}

def load_sources(rev=None):
    if rev is None:
        d=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))
    else:
        raw=subprocess.run(["git","show",f"{rev}:data/sources.json"],cwd=ROOT,capture_output=True).stdout.decode("utf-8","ignore")
        d=json.loads(raw)
    return {s["id"]:s for s in d["sources"]}

def is_stub(sid, note):
    """自称 stub 的页面不计。"""
    return "stub" in (note or "").lower()

def has_body(sid, s):
    """判定该来源是否有实际正文：读 note 中的实测字符/字节数。"""
    note=(s.get("note") or "")
    if is_stub(sid,note): return False
    # 优先取「摘要长度 N 字符」「正文 N 字符」
    m=re.search(r"摘要长度\s*(\d+)\s*字符", note) or re.search(r"正文\s*(\d+)\s*字符", note) \
      or re.search(r"摘要\s*(\d+)\s*字符", note)
    if m: return int(m.group(1))>=MIN_CHARS
    # 其次取「N 字节」
    m=re.search(r"(\d{3,7})\s*字节", note)
    if m: return int(m.group(1))>=MIN_CHARS
    # 无实测记录 → 无法判定，保守计为「未知」，不计入
    return None

def stats(rev=None):
    S=load_sources(rev)
    res={"zero":0,"one":0,"ge2":0,"unknown":0}
    for u in UNITS:
        for e in load(u,rev)["entries"]:
            n=0;unk=0
            for sid in e["sources"]:
                s=S.get(sid)
                if not s: continue
                hb=has_body(sid,s)
                if hb is True: n+=1
                elif hb is None: unk+=1
            if n==0:
                if unk>0: res["unknown"]+=1
                else: res["zero"]+=1
            elif n==1: res["one"]+=1
            else: res["ge2"]+=1
    return res

base=stats("be07fc1")   # 第43轮返工后的状态
cur=stats(None)
print("同一实现下：")
print(f"  baseline(第43轮末) 0源 {base['zero']} / 1源 {base['one']} / ≥2源 {base['ge2']} / 无实测记录 {base['unknown']}")
print(f"  当前               0源 {cur['zero']} / 1源 {cur['one']} / ≥2源 {cur['ge2']} / 无实测记录 {cur['unknown']}")
out={"round":44,"date":TODAY,
 "implementation":"统一 ac()：读 note 中实测的「摘要长度/正文字符」或「字节」，阈值 800；stub 不计；无实测记录者计入 unknown 单列（不再用 id 前缀猜测）",
 "baseline_be07fc1":base,"current":cur,
 "note":"第43轮曾用 id 前缀白名单，导致基线 52/167/24 与另一实现 77/154/12 不可比；本文件为统一口径重算"}
json.dump(out,open(os.path.join(ROOT,"reports","round44_recount.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n已写入 reports/round44_recount.json")