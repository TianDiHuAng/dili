# -*- coding: utf-8 -*-
"""补充探测：把结果追加到 data/probe_result.json。"""
import json, re, html, subprocess, os
from concurrent.futures import ThreadPoolExecutor

URLS = [
 "https://ourworldindata.org/land-use",
 "https://ourworldindata.org/crop-yields",
 "https://ourworldindata.org/fertilizers",
 "https://ourworldindata.org/meat-production",
 "https://ourworldindata.org/grapher/urban-population-percent-wb",
 "https://ourworldindata.org/grapher/rural-population",
 "https://ourworldindata.org/grapher/population-by-age-group",
 "https://ourworldindata.org/grapher/number-of-people-in-extreme-poverty",
 "https://www.fao.org/soils-portal/en/",
 "https://www.fao.org/land-water/land/land-governance/en/",
 "https://www.fao.org/climate-change/climate-change-and-food-security/en/",
 "https://www.fao.org/nr/water/aquastat/main/index.stm",
 "https://unstats.un.org/unsd/methodology/m49/aggregate/",
 "https://unstats.un.org/unsd/methodology/m49/structure/",
 "https://www.unesco.org/en/memory-of-the-world",
 "https://www.unesco.org/en/igcp",
 "https://www.unesco.org/en/ocean",
 "https://science.nasa.gov/earth/earth-observatory/earth-matters/",
 "https://science.nasa.gov/earth/faq/how-do-we-study-earth-from-space/",
 "https://earthobservatory.nasa.gov/features/AmazonFire",
 "https://www.ncei.noaa.gov/maps-and-geospatial-products/",
 "https://oceanservice.noaa.gov/facts/coralreef.html",
 "https://www.usgs.gov/news/",
 "https://www.usgs.gov/programs/volcano-hazards",
 "https://www.worldbank.org/en/topic/poverty",
 "https://www.worldbank.org/en/topic/health",
 "https://www.worldbank.org/en/topic/energy",
 "https://www.iucn.org/theme/protected-areas",
 "https://www.unep.org/resources/report",
 "https://www.un-habitat.org/urbanization/",
]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

def probe(url):
    try:
        p = subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","18","-A",UA,
                            "-o","-","-w","\n__HTTP__%{http_code}",url], capture_output=True, timeout=25)
        raw = p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw:
            return {"url":url,"code":0,"title":None}
        body, code = raw.rsplit("\n__HTTP__",1)
        m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I|re.S)
        title = re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
        return {"url":url,"code":int(code.strip()),"title":title}
    except Exception:
        return {"url":url,"code":0,"title":None}

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "data", "probe_result.json")
    with open(path, encoding="utf-8") as f:
        existing = json.load(f)
    have = {r["url"] for r in existing}
    with ThreadPoolExecutor(max_workers=12) as ex:
        new = list(ex.map(probe, [u for u in URLS if u not in have]))
    existing.extend(new)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    ok = [r for r in existing if r["code"] and r["code"] < 400 and r["title"]]
    print(f"NEW_OK {sum(1 for r in new if r['code'] and r['code']<400 and r['title'])} TOTAL_OK {len(ok)}")
    for r in new:
        print(r["code"], r["title"], "|", r["url"])

if __name__ == "__main__":
    main()
