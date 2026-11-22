# -*- coding: utf-8 -*-
"""阶段1：来源库核验。用 curl 打开每个候选 URL，记录 HTTP 状态与页面标题。
verified=true 的条件：HTTP<400 且页面 <title> 非空且包含预期关键词（或允许的机构域名兜底）。
作者/年份缺失时写 null，并在 note 说明；不编造。
"""
import json, os, re, subprocess, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
TODAY = "2026-11-22"

# (id, title, author/institution, year|null, type, url, expect_keyword)
CANDIDATES = [
 ("un-m49","Standard country or area codes for statistical use (M49)","联合国统计司",2022,"官方机构","https://unstats.un.org/unsd/methodology/m49/","country or area codes"),
 ("un-m49-overview","M49 Overview","联合国统计司",2022,"官方机构","https://unstats.un.org/unsd/methodology/m49/overview/","M49"),
 ("britannica-regions","Continent | Definition, Facts, & Types","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/continent","Continent"),
 ("wikipedia-regions","List of regions of the world","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/List_of_regions_of_the_world"," regions of the world"),
 ("ap-human-geo","AP Human Geography Course and Exam Description","College Board",None,"课程大纲","https://apcentral.collegeboard.org/courses/ap-human-geography","AP Human Geography"),
 ("worldbank-data","World Bank Open Data","World Bank",None,"官方机构","https://data.worldbank.org/","World Bank"),
 ("who-data","WHO Data","World Health Organization",None,"官方机构","https://www.who.int/data","World Health Organization"),
 ("unesco-home","UNESCO","UNESCO",None,"官方机构","https://www.unesco.org/en","UNESCO"),
 ("fao-home","Food and Agriculture Organization","FAO",None,"官方机构","https://www.fao.org/home/en","Food and Agriculture"),
 ("ipcc-home","IPCC","IPCC",None,"官方机构","https://www.ipcc.ch/","IPCC"),
 ("noaa-home","NOAA","NOAA",None,"官方机构","https://www.noaa.gov/","NOAA"),
 ("nasa-earth","Earth Science Division","NASA",None,"官方机构","https://science.nasa.gov/earth/","Earth"),
 ("usgs-home","USGS","U.S. Geological Survey",None,"官方机构","https://www.usgs.gov/","USGS"),
 ("owid","Our World in Data","Our World in Data",None,"学术/数据机构","https://ourworldindata.org/","Our World in Data"),
 ("naturalearth","Natural Earth","Natural Earth",None,"数据集","https://www.naturalearthdata.com/","Natural Earth"),
 ("br-africa","Africa | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Africa","Africa"),
 ("br-asia","Asia | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Asia","Asia"),
 ("br-europe","Europe | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Europe","Europe"),
 ("br-north-america","North America | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/North-America","North America"),
 ("br-south-america","South America | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/South-America","South America"),
 ("br-oceania","Oceania | Definition, Geography, & Islands","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Oceania","Oceania"),
 ("br-antarctica","Antarctica | History, Geography, & Climate","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Antarctica","Antarctica"),
 ("wk-africa","Africa","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Africa","Africa"),
 ("wk-asia","Asia","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Asia","Asia"),
 ("wk-europe","Europe","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Europe","Europe"),
 ("wk-north-america","North America","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/North_America","North America"),
 ("wk-south-america","South America","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/South_America","South America"),
 ("wk-oceania","Oceania","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Oceania","Oceania"),
 ("wk-antarctica","Antarctica","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Antarctica","Antarctica"),
 ("br-nile","Nile River","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Nile-River","Nile"),
 ("wk-nile","Nile","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Nile","Nile"),
 ("br-sahara","Sahara | Desert, Africa","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Sahara","Sahara"),
 ("wk-sahara","Sahara","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Sahara","Sahara"),
 ("br-mesopotamia","Mesopotamia | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Mesopotamia","Mesopotamia"),
 ("wk-mesopotamia","Mesopotamia","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Mesopotamia","Mesopotamia"),
 ("br-himalayas","Himalayas | Mountains, Asia","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Himalayas","Himalayas"),
 ("wk-himalayas","Himalayas","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Himalayas","Himalayas"),
 ("br-tibet","Tibet | Plateau, China","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Tibet","Tibet"),
 ("wk-tibetan-plateau","Tibetan Plateau","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Tibetan_Plateau","Tibetan Plateau"),
 ("br-amazon","Amazon River","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Amazon-River","Amazon"),
 ("wk-amazon-rainforest","Amazon rainforest","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Amazon_rainforest","Amazon rainforest"),
 ("br-andes","Andes Mountains","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Andes-Mountains","Andes"),
 ("wk-andes","Andes","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Andes","Andes"),
 ("br-yellow-river","Huang He | River, China","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Huang-He","Huang He"),
 ("wk-yellow-river","Yellow River","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Yellow_River","Yellow River"),
 ("br-yangtze","Yangtze River","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Yangtze-River","Yangtze"),
 ("wk-yangtze","Yangtze","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Yangtze","Yangtze"),
 ("br-silk-road","Silk Road | Trade route, Asia","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/topic/Silk-Road-trade-route","Silk Road"),
 ("wk-silk-road","Silk Road","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Silk_Road","Silk Road"),
 ("br-mediterranean","Mediterranean Sea","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Mediterranean-Sea","Mediterranean"),
 ("wk-mediterranean","Mediterranean Sea","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Mediterranean_Sea","Mediterranean Sea"),
 ("br-sub-saharan-africa","Sub-Saharan Africa | Geography & History","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Sub-Saharan-Africa","Sub-Saharan Africa"),
 ("wk-sub-saharan-africa","Sub-Saharan Africa","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Sub-Saharan_Africa","Sub-Saharan Africa"),
 ("br-southeast-asia","Southeast Asia | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Southeast-Asia","Southeast Asia"),
 ("wk-southeast-asia","Southeast Asia","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Southeast_Asia","Southeast Asia"),
 ("br-central-asia","Central Asia | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Central-Asia","Central Asia"),
 ("wk-central-asia","Central Asia","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Central_Asia","Central Asia"),
 ("br-india","India | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/India","India"),
 ("wk-india","India","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/India","India"),
 ("br-china","China | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/China","China"),
 ("wk-china","China","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/China","China"),
 ("br-japan","Japan | History, Geography, & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Japan","Japan"),
 ("wk-japan","Japan","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Japan","Japan"),
 ("br-egypt","Egypt | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Egypt","Egypt"),
 ("wk-egypt","Egypt","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Egypt","Egypt"),
 ("br-great-rift-valley","Great Rift Valley","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Great-Rift-Valley","Rift Valley"),
 ("wk-great-rift-valley","Great Rift Valley","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Great_Rift_Valley","Rift Valley"),
 ("br-congo-basin","Congo River basin","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Congo-River","Congo"),
 ("wk-congo-basin","Congo Basin","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Congo_Basin","Congo Basin"),
 ("br-sahel","Sahel | Region, Africa","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Sahel","Sahel"),
 ("wk-sahel","Sahel","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Sahel","Sahel"),
 ("br-carthage","Carthage | Ancient City, Tunisia","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Carthage","Carthage"),
 ("wk-carthage","Carthage","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Carthage","Carthage"),
 ("br-mali-empire","Mali Empire","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Mali-Empire","Mali Empire"),
 ("wk-mali-empire","Mali Empire","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Mali_Empire","Mali Empire"),
 ("br-inca","Inca Empire","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Inca-Empire","Inca"),
 ("wk-inca","Inca Empire","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Inca_Empire","Inca"),
 ("br-maya","Maya civilization","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/topic/Maya-civilization","Maya"),
 ("wk-maya","Maya civilization","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Maya_civilization","Maya"),
 ("br-aztec","Aztec","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/topic/Aztec","Aztec"),
 ("wk-aztec","Aztec Empire","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Aztec_Empire","Aztec"),
 ("br-rome","Ancient Rome | History & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/topic/Ancient-Rome","Ancient Rome"),
 ("wk-rome","Ancient Rome","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Ancient_Rome","Ancient Rome"),
 ("br-greece","Ancient Greece | History & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Ancient-Greece","Ancient Greece"),
 ("wk-greece","Ancient Greece","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Ancient_Greece","Ancient Greece"),
 ("br-byzantium","Byzantine Empire","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Byzantine-Empire","Byzantine"),
 ("wk-byzantium","Byzantine Empire","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Byzantine_Empire","Byzantine"),
 ("br-viking","Vikings | History, Culture & Voyages","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/topic/Viking","Viking"),
 ("wk-viking","Vikings","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Vikings","Vikings"),
 ("br-australia","Australia | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Australia","Australia"),
 ("wk-australia","Australia","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Australia","Australia"),
 ("br-new-zealand","New Zealand | History, Geography, & People","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/New-Zealand","New Zealand"),
 ("wk-new-zealand","New Zealand","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/New_Zealand","New Zealand"),
 ("br-polynesia","Polynesia | Islands, Pacific","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/place/Polynesia","Polynesia"),
 ("wk-polynesia","Polynesia","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Polynesia","Polynesia"),
 ("br-antarctic-treaty","Antarctic Treaty","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/event/Antarctic-Treaty","Antarctic Treaty"),
 ("wk-antarctic-treaty","Antarctic Treaty System","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Antarctic_Treaty_System","Antarctic Treaty"),
 ("br-plate-tectonics","Plate tectonics | Theory, Earth & Geology","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/plate-tectonics","plate tectonics"),
 ("wk-plate-tectonics","Plate tectonics","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Plate_tectonics","Plate tectonics"),
 ("br-monsoon","Monsoon | Definition, Causes, & Seasons","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/monsoon","monsoon"),
 ("wk-monsoon","Monsoon","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Monsoon","Monsoon"),
 ("br-desertification","Desertification","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/desertification","desertification"),
 ("wk-desertification","Desertification","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Desertification","Desertification"),
 ("br-delta","River delta | Geography","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/delta","delta"),
 ("wk-delta","River delta","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/River_delta","River delta"),
 ("br-nomad","Nomad | People, Society & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/topic/nomad","Nomad"),
 ("wk-nomad","Nomad","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Nomad","Nomad"),
 ("unesco-wh","UNESCO World Heritage Centre","UNESCO",None,"官方机构","https://whc.unesco.org/en/list/","World Heritage"),
 ("fao-aquastat","FAO AQUASTAT","FAO",None,"官方机构","https://www.fao.org/aquastat/en/","AQUASTAT"),
 ("un-desa-pop","World Population Prospects","UN DESA",None,"官方机构","https://population.un.org/wpp/","World Population Prospects"),
 ("usgs-earthquakes","USGS Earthquakes","U.S. Geological Survey",None,"官方机构","https://earthquake.usgs.gov/","Earthquake"),
 ("noaa-climate","NOAA Climate.gov","NOAA",None,"官方机构","https://www.climate.gov/","climate"),
 ("nasa-earth-observatory","NASA Earth Observatory","NASA",None,"官方机构","https://earthobservatory.nasa.gov/","Earth Observatory"),
 ("ipcc-ar6","IPCC Sixth Assessment Report","IPCC",2021,"官方机构","https://www.ipcc.ch/report/ar6/wg1/","Sixth Assessment Report"),
 ("cbd-home","Convention on Biological Diversity","CBD",None,"官方机构","https://www.cbd.int/","Biological Diversity"),
 ("ramsar","Ramsar Convention on Wetlands","Ramsar Convention",None,"官方机构","https://www.ramsar.org/","Ramsar"),
 ("unfccc","UNFCCC","UNFCCC",None,"官方机构","https://unfccc.int/","UNFCCC"),
 ("worldbank-indicators","World Development Indicators","World Bank",None,"数据集","https://databank.worldbank.org/source/world-development-indicators","World Development Indicators"),
 ("britannica-geography-home","Geography | Science, History & Culture","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/geography","Geography"),
 ("wk-geography","Geography","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Geography","Geography"),
 ("br-continental-drift","Continental drift | Geology","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/continental-drift","continental drift"),
 ("wk-continental-drift","Continental drift","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Continental_drift","Continental drift"),
 ("br-ocean-current","Ocean current | Geology","Encyclopaedia Britannica",None,"权威百科","https://www.britannica.com/science/ocean-current","ocean current"),
 ("wk-ocean-current","Ocean current","Wikipedia contributors",None,"权威百科","https://en.wikipedia.org/wiki/Ocean_current","Ocean current"),
]


def fetch(url):
    try:
        p = subprocess.run(["curl","-L","-sS","-m","25","-A",UA,"-o","-","-w","\n__HTTP__%{http_code}",url],
                           capture_output=True, timeout=35)
        raw = p.stdout.decode("utf-8", "ignore")
        if "__HTTP__" not in raw:
            return None, None
        body, code = raw.rsplit("\n__HTTP__", 1)
        return int(code.strip()), body
    except Exception:
        return None, None


def parse_title(body):
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    if not m:
        return None
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()
    return t or None


def main():
    sources = []
    ok = 0
    for i, (sid, title, author, year, typ, url, expect) in enumerate(CANDIDATES, 1):
        code, body = fetch(url)
        ptitle = parse_title(body) if body else None
        if code is None:
            link_ok = False
        elif code < 400:
            link_ok = True
        elif code in (401, 403, 429, 503):
            link_ok = "blocked"
        else:
            link_ok = False
        verified = bool(link_ok is True and ptitle and expect.lower() in ptitle.lower())
        note = "curl 实测 HTTP %s；页面标题：%s" % (code, ptitle or "未取得")
        if year is None:
            note += "；网页动态更新，年份未标注，不做推定。"
        sources.append({
            "id": sid, "title": title, "author": author, "year": year,
            "type": typ, "url": url, "url2": None,
            "link_ok": link_ok, "verified": verified,
            "page_title": ptitle, "note": note,
        })
        if verified:
            ok += 1
        print(f"[{i}/{len(CANDIDATES)}] {sid}: {'OK' if verified else 'NO'} ({code}) {ptitle}")
    with open(os.path.join(ROOT, "data", "sources.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": TODAY, "verification_method": "curl HTTP + <title> 关键词比对", "sources": sources}, f, ensure_ascii=False, indent=2)
    print(f"VERIFIED {ok}/{len(CANDIDATES)}")

if __name__ == "__main__":
    main()
