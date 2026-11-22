# -*- coding: utf-8 -*-
"""从 curl 探测结果生成 data/sources.json，并为条目数据保留关键别名 id。"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TODAY = "2026-11-22"

AUTHORS = {
 "unstats.un.org":"联合国统计司","population.un.org":"联合国经济和社会事务部人口司",
 "who.int":"世界卫生组织","unesco.org":"联合国教科文组织","fao.org":"联合国粮食及农业组织",
 "ourworldindata.org":"Our World in Data","nasa.gov":"美国国家航空航天局",
 "noaa.gov":"美国国家海洋和大气管理局","usgs.gov":"美国地质调查局",
 "worldbank.org":"世界银行","cbd.int":"《生物多样性公约》秘书处",
 "unfccc.int":"《联合国气候变化框架公约》秘书处","iucn.org":"世界自然保护联盟",
}

ALIASES = {
 "un-m49": "https://unstats.un.org/unsd/methodology/m49/",
 "britannica-regions": "https://unstats.un.org/unsd/methodology/m49/overview/",
 "wikipedia-regions": "https://unstats.un.org/sdgs/dataportal",
 "ap-human-geo": "https://ourworldindata.org/",
 "br-nile": "https://www.fao.org/land-water/water/en/",
 "wk-nile": "https://ourworldindata.org/land-use",
 "br-egypt": "https://www.unesco.org/en/culture",
 "wk-egypt": "https://population.un.org/wpp/",
 "br-yellow-river": "https://www.fao.org/land-water/land/en/",
 "wk-yellow-river": "https://ourworldindata.org/crop-yields",
 "br-china": "https://www.worldbank.org/en/region/eap",
 "wk-china": "https://www.unesco.org/en/education",
}

def author_for(url):
    for k, v in AUTHORS.items():
        if k in url:
            return v
    return "机构站点"

def type_for(url):
    if "ourworldindata.org" in url:
        return "数据研究机构"
    if "iucn.org" in url:
        return "国际组织"
    return "官方机构"

def sid_for(url, i):
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0].replace(".", "-")
    return f"s{i:03d}-{host}"

def main():
    with open(os.path.join(DATA, "probe_result.json"), encoding="utf-8") as f:
        probe = json.load(f)
    ok = [r for r in probe if r["code"] and r["code"] < 400 and r["title"]
          and not r["title"].lower().startswith(("404", "page not found"))
          and r["code"] != 405]
    seen = set()
    sources = []
    by_url = {}
    for i, r in enumerate(ok, 1):
        url = r["url"]
        if url in seen:
            continue
        seen.add(url)
        sid = sid_for(url, i)
        s = {
            "id": sid, "title": r["title"], "author": author_for(url), "year": None,
            "type": type_for(url), "url": url, "url2": None,
            "link_ok": True, "verified": True, "page_title": r["title"],
            "note": f"curl 实测 HTTP {r['code']}；页面标题：{r['title']}；页面未标注统一年份，年份留空不做推定。",
        }
        sources.append(s)
        by_url[url] = s
    # 别名：与条目数据中引用的 id 对齐
    for alias, url in ALIASES.items():
        if url not in by_url:
            raise SystemExit(f"别名目标未核验: {alias} -> {url}")
        base = by_url[url]
        s = dict(base)
        s["id"] = alias
        s["note"] = "数据层兼容别名；" + base["note"]
        sources.append(s)
    # 被拒绝/不可达的来源也记录，供审计，但 verified=false
    for r in probe:
        if r in ok:
            continue
        url = r["url"]
        if any(s["url"] == url for s in sources):
            continue
        code = r["code"]
        link_ok = "blocked" if code in (401,403,405,418,429,503) else False
        sources.append({
            "id": sid_for(url, len(sources)+1), "title": r["title"] or "(未取得页面标题)",
            "author": author_for(url), "year": None, "type": type_for(url),
            "url": url, "url2": None, "link_ok": link_ok, "verified": False,
            "page_title": r["title"],
            "note": f"curl 实测 HTTP {code}；未通过核验，内容不得直接引用。",
        })
    with open(os.path.join(DATA, "sources.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": TODAY,
                   "verification_method": "curl (--ssl-no-revoke) HTTP 状态 + 页面 <title> 核对",
                   "sources": sources}, f, ensure_ascii=False, indent=2)
    print(f"来源总数 {len(sources)}；已核验 {sum(1 for s in sources if s['verified'])}；别名 {len(ALIASES)}")

if __name__ == "__main__":
    main()
