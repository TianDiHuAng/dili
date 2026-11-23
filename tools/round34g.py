# -*- coding: utf-8 -*-
"""第34轮续：为剩余 46 条重要 L1 定向检索 OpenAlex。"""
import subprocess,json,os,urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"尼罗河三角洲":["nile delta"],"安纳托利亚":["anatolia"],"意大利半岛":["italian peninsula"],
"斯堪的纳维亚":["scandinavia","scandinavian peninsula"],"墨西哥湾":["gulf of mexico"],
"巴西高原":["brazilian highlands","brazil plateau"],"马丘比丘":["machu picchu"],
"大自流盆地":["artesian basin","great artesian"],"新西兰北岛":["north island new zealand"],
"新西兰南岛":["south island new zealand","southern alps"],"夏威夷群岛":["hawaiian islands","hawaii volcanism"],
"大堡礁":["great barrier reef"],
"几内亚湾沿岸":["gulf of guinea"],"东亚季风":["east asian monsoon"],"欧洲温带海洋性气候":["maritime climate europe","western europe climate"],
"澳大利亚内陆干旱气候":["australian arid","arid australia climate"],
"湄公河三角洲":["mekong delta"],"中世纪欧洲庄园农业":["medieval manor","open field agriculture medieval"],
"美国西进":["westward expansion","american frontier"],"莫切文化":["moche"],
"安第斯垂直农业":["andean agriculture","vertical zonation andes"],"澳大利亚混合农业":["australian wheat sheep","mixed farming australia"],
"冲积平原":["alluvial plain"],"山地农业":["mountain agriculture","terracing"],
"大津巴布韦":["great zimbabwe"],"隋唐":["sui tang"],"明清":["ming qing economy","late imperial china"],
"马来群岛":["malay archipelago"],"河中地区":["transoxiana","central asia samarkand"],
"黑海海峡":["bosporus","dardanelles"],"加勒比海群岛":["caribbean islands"],
"阿拉伯征服北非":["arab conquest","islamic conquest north africa"],"古巴比伦":["babylonia","babylon mesopotamia"],
"吠陀时代":["vedic period","rigveda"],"吴哥":["angkor","khmer empire"],
"匈奴":["xiongnu"],"突厥":["gokturk","turkic khaganate"],"法兰克王国":["frankish","francia carolingian"],
"莫斯科公国":["muscovy","grand duchy of moscow"],"巴西殖民经济":["colonial brazil","brazil sugar economy"],
"朝鲜半岛":["korean peninsula"],"中南半岛":["indochina","mainland southeast asia"],
"黎凡特":["levant"],"伊比利亚半岛":["iberian peninsula"],"巴尔干半岛":["balkan peninsula"],
"北美原住民":["native north america","peopling of the americas"],
}
CORE={
"尼罗河三角洲":["nile delta"],"安纳托利亚":["anatolia"],"意大利半岛":["italian peninsula","italy"],
"斯堪的纳维亚":["scandinavia"],"墨西哥湾":["gulf of mexico"],"巴西高原":["brazil"],
"马丘比丘":["machu picchu"],"大自流盆地":["artesian"],"新西兰北岛":["north island"],
"新西兰南岛":["south island","southern alps"],"夏威夷群岛":["hawai"],"大堡礁":["great barrier reef","coral reef"],
"几内亚湾沿岸":["gulf of guinea"],"东亚季风":["monsoon"],"欧洲温带海洋性气候":["maritime","oceanic climate"],
"澳大利亚内陆干旱气候":["arid","australia"],"湄公河三角洲":["mekong"],"中世纪欧洲庄园农业":["manor","medieval"],
"美国西进":["westward","frontier"],"莫切文化":["moche"],"安第斯垂直农业":["andean","andes"],
"澳大利亚混合农业":["australia"],"冲积平原":["alluvial"],"山地农业":["mountain agriculture","terrace"],
"大津巴布韦":["zimbabwe"],"隋唐":["sui","tang"],"明清":["ming","qing"],"马来群岛":["malay"],
"河中地区":["transoxiana","central asia"],"黑海海峡":["bosporus","dardanelles","strait"],
"加勒比海群岛":["caribbean"],"阿拉伯征服北非":["arab","islamic conquest"],"古巴比伦":["babylon"],
"吠陀时代":["vedic"],"吴哥":["angkor","khmer"],"匈奴":["xiongnu","steppe nomad"],
"突厥":["turk","gokturk"],"法兰克王国":["frankish","francia"],"莫斯科公国":["moscow","muscovy"],
"巴西殖民经济":["brazil","colonial"],"朝鲜半岛":["korea"],"中南半岛":["southeast asia","indochina"],
"黎凡特":["levant","eastern mediterranean"],"伊比利亚半岛":["iberian"],"巴尔干半岛":["balkan"],
"北美原住民":["native","americas","indigenous"],
}
def get(u):
    return subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",u],
                          capture_output=True,timeout=40).stdout.decode("utf-8","ignore")
def ab_of(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for word,idxs in inv.items():
        for i in idxs: pos[i]=word
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,qs in Q.items():
    got=None
    for q in qs:
        u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+
           "&per_page=8&mailto=geo-encyclopedia@example.com")
        try: d=json.loads(get(u))
        except Exception: continue
        good=[]
        for w in d.get("results",[]):
            a=ab_of(w)
            if not a or len(a)<300: continue
            ti=(w.get("title") or "").lower()
            if not any(k in ti for k in CORE.get(t,[q])): continue
            good.append({"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"doi":w.get("doi"),"cited":w.get("cited_by_count"),
              "abstract":a,"host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))})
        if good:
            good.sort(key=lambda x:-(x.get("cited") or 0)); got=good[0]; break
    res[t]=got
    print(f"{'OK' if got else '--'} {t:<14} {(got['title'][:50] if got else '-')} ({got['year'] if got else ''})")
json.dump(res,open(os.path.join(ROOT,"reports","round34_final2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q))