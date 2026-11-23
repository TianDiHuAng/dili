# -*- coding: utf-8 -*-
"""第34轮 B1：用 OpenAlex 学术 API 为「单源待互证」条目寻找第二来源。"""
import subprocess,json,os,re,urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUERIES={
"汉代":"Han dynasty China imperial","蒙古帝国":"Mongol Empire expansion","阿兹特克":"Aztec Empire Mesoamerica",
"长江流域":"Yangtze River basin China","印度河文明":"Indus Valley Civilization",
"古埃及新王国":"New Kingdom Egypt","库什与努比亚":"kingdom of Kush Nubia","罗马阿非利加":"Roman Africa province",
"加纳帝国":"Ghana Empire West Africa","桑海帝国":"Songhai Empire","笈多王朝":"Gupta Empire India",
"商代":"Shang dynasty China","周代":"Zhou dynasty China","秦代":"Qin dynasty China","元代":"Yuan dynasty China",
"马格里布":"Maghreb North Africa region","阿拉伯半岛":"Arabian Peninsula geography","埃塞俄比亚高原":"Ethiopian Highlands",
"城市起源":"origin of cities urbanization ancient","丝绸之路":"Silk Road trade",
}
def get(u):
    return subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",u],
                          capture_output=True,timeout=40).stdout.decode("utf-8","ignore")
def abstract_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))
out={}
for title,q in QUERIES.items():
    u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+
       "&per_page=8&mailto=geo-encyclopedia@example.com")
    try: d=json.loads(get(u))
    except Exception as e:
        out[title]={"err":type(e).__name__};print(f"{title:<12} ERR");continue
    cands=[]
    for w in d.get("results",[]):
        ab=abstract_of(w)
        if not ab: continue
        if len(ab)<200: continue
        cands.append({"title":w.get("title"),"year":w.get("publication_year"),
                      "doi":w.get("doi"),"cited":w.get("cited_by_count"),
                      "abstract":ab,"type":w.get("type"),
                      "id":w.get("id"),"host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
    out[title]=cands
    print(f"{title:<12} 候选 {len(cands):>2} | 首条: {(cands[0]['title'][:52] if cands else '-')} ({cands[0]['year'] if cands else ''})")
json.dump(out,open(os.path.join(ROOT,"reports","round34_openalex.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有可用候选条目:",sum(1 for v in out.values() if isinstance(v,list) and v))