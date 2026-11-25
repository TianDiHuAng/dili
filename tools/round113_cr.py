import json, subprocess, sys, time, urllib.parse
Q = {
 'great_dividing': ['eastern Australian highlands', 'southeastern Australian highlands geomorphology', 'eastern Australia passive margin escarpment', 'New England tableland', 'Australian Alps'],
}
def curl(url):
    r = subprocess.run(['curl','-L','-sS','--ssl-no-revoke','--compressed','-m','25','-A','Mozilla/5.0 (mailto:clientvip@zhuwyai.me)',url],capture_output=True,text=True,encoding='utf-8',errors='replace')
    return r.stdout
def abstract(doi):
    t = curl('https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(doi))
    try: d = json.loads(t)
    except Exception: return None, 0
    inv = d.get('abstract_inverted_index') or {}
    pos = sorted((p,w) for w,ps in inv.items() for p in ps)
    return d, ' '.join(w for _,w in pos)
out = {}
for k, qs in Q.items():
    out[k] = []
    for q in qs:
        u = 'https://api.crossref.org/works?rows=8&filter=has-abstract:true&query.bibliographic='+urllib.parse.quote(q)
        try: items = json.loads(curl(u))['message']['items']
        except Exception as e:
            print(k, q, 'CR_FAIL'); continue
        for it in items:
            doi = it.get('DOI'); title = (it.get('title') or [''])[0]
            d, ab = abstract(doi); time.sleep(0.3)
            if not d: continue
            c = d.get('cited_by_count', 0); n = len(ab)
            if c >= 10 or n >= 800:
                out[k].append({'q':q,'doi':doi,'id':d.get('id','').rsplit('/',1)[-1],'title':title[:110],'year':d.get('publication_year'),'cited':c,'chars':n,'type':d.get('type'),'abstract':ab[:600]})
    print(k, len(out[k]))
json.dump(out, open('reports/round113_cr.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
