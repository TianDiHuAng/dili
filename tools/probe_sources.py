# -*- coding: utf-8 -*-
"""并发探测权威站点可达性，输出 JSON 供来源库使用。
用法：python -X utf8 tools/probe_sources.py > data/probe_result.json
"""
import json, re, html, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

URLS = [
 "https://unstats.un.org/unsd/methodology/m49/",
 "https://unstats.un.org/unsd/methodology/m49/overview/",
 "https://unstats.un.org/unsd/methodology/m49/notes/",
 "https://unstats.un.org/sdgs/dataportal",
 "https://unstats.un.org/unsd/statcom/",
 "https://unstats.un.org/home/",
 "https://population.un.org/wpp/",
 "https://population.un.org/wpp/Download/Standard/Population/",
 "https://www.who.int/data",
 "https://www.who.int/data/gho",
 "https://www.who.int/health-topics/climate-change",
 "https://www.unesco.org/en",
 "https://www.unesco.org/en/education",
 "https://www.unesco.org/en/natural-sciences",
 "https://www.unesco.org/en/social-human-sciences",
 "https://www.unesco.org/en/culture",
 "https://www.unesco.org/en/communication-information",
 "https://www.unesco.org/en/sustainable-development",
 "https://www.unesco.org/en/water",
 "https://www.unesco.org/en/climate-change",
 "https://www.unesco.org/en/biosphere-reserves",
 "https://whc.unesco.org/en/list/",
 "https://www.fao.org/home/en",
 "https://www.fao.org/aquastat/en/",
 "https://www.fao.org/faostat/en/",
 "https://www.fao.org/land-water/en/",
 "https://www.fao.org/land-water/land/en/",
 "https://www.fao.org/land-water/water/en/",
 "https://www.fao.org/forestry/en/",
 "https://www.fao.org/fishery/en",
 "https://www.fao.org/climate-change/en/",
 "https://www.fao.org/natural-resources/en/",
 "https://www.fao.org/agriculture/en/",
 "https://www.fao.org/food/en/",
 "https://www.fao.org/documents/en/",
 "https://www.fao.org/statistics/en/",
 "https://www.fao.org/economic/en/",
 "https://www.fao.org/in-action/en/",
 "https://ourworldindata.org/",
 "https://ourworldindata.org/population-growth",
 "https://ourworldindata.org/world-population-growth",
 "https://ourworldindata.org/urbanization",
 "https://ourworldindata.org/climate-change",
 "https://ourworldindata.org/co2-emissions",
 "https://ourworldindata.org/energy",
 "https://ourworldindata.org/food",
 "https://ourworldindata.org/agriculture",
 "https://ourworldindata.org/water",
 "https://ourworldindata.org/forests",
 "https://ourworldindata.org/biodiversity",
 "https://ourworldindata.org/natural-disasters",
 "https://ourworldindata.org/grapher/population",
 "https://ourworldindata.org/grapher/life-expectancy",
 "https://ourworldindata.org/grapher/gdp-per-capita-worldbank",
 "https://ourworldindata.org/grapher/annual-co2-emissions-per-country",
 "https://ourworldindata.org/grapher/urban-population-wb",
 "https://ourworldindata.org/grapher/forest-area-as-share-of-land-area",
 "https://ourworldindata.org/grapher/water-withdrawals-annual-total",
 "https://science.nasa.gov/earth/",
 "https://earthobservatory.nasa.gov/",
 "https://climate.nasa.gov/",
 "https://www.nasa.gov/",
 "https://science.nasa.gov/earth/earth-observatory/",
 "https://science.nasa.gov/mission/landsat/",
 "https://earthobservatory.nasa.gov/features/Deforestation",
 "https://earthobservatory.nasa.gov/features/WorldOfChange",
 "https://earthobservatory.nasa.gov/features/Urbanization",
 "https://earthobservatory.nasa.gov/features/Desertification",
 "https://earthobservatory.nasa.gov/features/DustBowl",
 "https://science.nasa.gov/earth/faq/what-is-earth-science/",
 "https://www.noaa.gov/",
 "https://www.climate.gov/",
 "https://www.ncei.noaa.gov/",
 "https://oceanservice.noaa.gov/",
 "https://www.fisheries.noaa.gov/",
 "https://www.weather.gov/",
 "https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature",
 "https://oceanservice.noaa.gov/facts/ocean-currents.html",
 "https://oceanservice.noaa.gov/facts/el-nino-la-nina.html",
 "https://www.ncei.noaa.gov/access/",
 "https://www.ncei.noaa.gov/products/",
 "https://www.usgs.gov/",
 "https://earthquake.usgs.gov/",
 "https://water.usgs.gov/",
 "https://www.usgs.gov/programs/earthquake-hazards",
 "https://www.usgs.gov/programs/national-cooperative-geologic-mapping-program",
 "https://www.usgs.gov/centers/eros",
 "https://www.usgs.gov/programs/mineral-resources-program",
 "https://www.usgs.gov/programs/national-water-quality-program",
 "https://databank.worldbank.org/source/world-development-indicators",
 "https://www.worldbank.org/en/topic/urbanization",
 "https://www.worldbank.org/en/topic/agriculture",
 "https://www.worldbank.org/en/topic/climatechange",
 "https://www.worldbank.org/en/topic/water",
 "https://www.worldbank.org/en/topic/environment",
 "https://www.worldbank.org/en/topic/transport",
 "https://www.worldbank.org/en/region/afr",
 "https://www.worldbank.org/en/region/eap",
 "https://www.worldbank.org/en/region/eur",
 "https://www.worldbank.org/en/region/lac",
 "https://www.worldbank.org/en/region/mena",
 "https://www.worldbank.org/en/region/sar",
 "https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups",
 "https://www.cbd.int/",
 "https://www.cbd.int/convention/",
 "https://www.cbd.int/protected/",
 "https://unfccc.int/",
 "https://unfccc.int/topics",
 "https://www.iucn.org/",
 "https://www.unep.org/",
 "https://www.un-habitat.org/",
 "https://www.unicef.org/",
 "https://www.iau-aiu.net/",
 "https://www.igc.org.uk/",
 "https://www.geolsoc.org.uk/",
 "https://www.aag.org/",
 "https://www.nationalacademies.org/",
 "https://www.sciencedirect.com/",
 "https://www.springer.com/",
 "https://www.tandfonline.com/",
 "https://www.sAGEpub.com/",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

def probe(url):
    try:
        p = subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","18",
                            "-A",UA,"-o","-","-w","\n__HTTP__%{http_code}",url],
                           capture_output=True, timeout=25)
        raw = p.stdout.decode("utf-8", "ignore")
        if "__HTTP__" not in raw:
            return {"url":url,"code":0,"title":None}
        body, code = raw.rsplit("\n__HTTP__",1)
        m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I|re.S)
        title = re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
        return {"url":url,"code":int(code.strip()),"title":title}
    except Exception:
        return {"url":url,"code":0,"title":None}

def main():
    with ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(probe, URLS))
    ok = [r for r in results if r["code"] and r["code"] < 400 and r["title"]]
    print(f"OK {len(ok)}/{len(URLS)}", file=sys.stderr)
    for r in results:
        print(f"{r['code']:>4} {r['title'] or '-'} | {r['url']}", file=sys.stderr)
    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
