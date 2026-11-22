# -*- coding: utf-8 -*-
"""第33轮：批量查询 Wikidata 实体年代，为重要 L1 政权条目升级做准备。"""
import subprocess,json,os,re,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP={
"古埃及新王国":"New Kingdom of Egypt","库什与努比亚":"Kingdom of Kush","罗马阿非利加":"Africa (Roman province)",
"加纳帝国":"Ghana Empire","桑海帝国":"Songhai Empire","大津巴布韦":"Kingdom of Zimbabwe",
"古巴比伦":"Babylonia","亚述帝国":"Neo-Assyrian Empire","帕提亚帝国":"Parthian Empire",
"萨珊波斯":"Sasanian Empire","吠陀时代":"Vedic period","孔雀王朝":"Maurya Empire",
"笈多王朝":"Gupta Empire","商代":"Shang dynasty","周代":"Zhou dynasty","秦代":"Qin dynasty",
"元代":"Yuan dynasty","明清":"Ming dynasty","吴哥":"Khmer Empire","河中地区":"Transoxiana",
"匈奴":"Xiongnu","突厥":"Göktürks","马其顿与亚历山大":"Macedonia (ancient kingdom)",
"拜占庭帝国":"Byzantine Empire","法兰克王国":"Francia","十字军东征":"Crusades",
"威尼斯":"Republic of Venice","莫斯科公国":"Grand Duchy of Moscow","特奥蒂瓦坎":"Teotihuacan",
"十三殖民地":"Thirteen Colonies","蒂亚瓦纳科":"Tiwanaku",
}
def get(u):
    return subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",u],
                          capture_output=True,timeout=35).stdout.decode("utf-8","ignore")
def fmt(t):
    if not t: return None
    neg=t.startswith("-"); s=t.lstrip("-").split("T")[0]
    y=s.split("-")[0]
    return ("前%d年" % int(y)) if neg else ("%d年" % int(y))
out={}
for cn,en in MAP.items():
    su=f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={en.replace(' ','%20')}&language=en&format=json&limit=3"
    try:
        d=json.loads(get(su))
    except Exception:
        out[cn]={"err":"search_fail"};continue
    cand=[s for s in d.get("search",[]) if s.get("id","").startswith("Q")]
    if not cand:
        out[cn]={"err":"no_entity"};print(f"{cn:<14} NO_ENTITY");continue
    qid=cand[0]["id"]; label=cand[0].get("label"); desc=cand[0].get("description") or ""
    eu=f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json"
    try:
        e=json.loads(get(eu)); cl=e["entities"][qid].get("claims",{})
    except Exception:
        out[cn]={"err":"entity_fail"};continue
    def val(pid):
        if pid not in cl: return None,None
        try:
            v=cl[pid][0]["mainsnak"]["datavalue"]["value"]
            return v.get("time"), v.get("precision")
        except Exception: return None,None
    t1,p1=val("P571"); t2,p2=val("P576"); t3,p3=val("P580"); t4,p4=val("P582")
    start=fmt(t3 or t1); end=fmt(t4 or t2)
    out[cn]={"qid":qid,"label":label,"desc":desc,"start":start,"end":end,
             "prec_start":p3 or p1,"prec_end":p4 or p2}
    print(f"{cn:<14} {qid:<9} {start or '-':<10}–{end or '-':<10} | {desc[:44]}")
json.dump(out,open(os.path.join(ROOT,"reports","round33_wikidata.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
ok=[k for k,v in out.items() if v.get("start") and v.get("end")]
print("\n有完整起止年代:",len(ok),"→","、".join(ok))