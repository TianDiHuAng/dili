import json,glob,os,re,subprocess,time,sys
F=['definition','overview','geo','influence','polities','connections','today','time_or_place']
ents={}
for f in glob.glob('data/*.json'):
    try: d=json.load(open(f,encoding='utf-8'))
    except Exception: continue
    if isinstance(d,dict) and isinstance(d.get('entries'),list):
        for e in d['entries']:
            if isinstance(e,dict) and 'title' in e: ents.setdefault(e['title'],e)
srcs={s['id']:s for s in json.load(open('data/sources.json',encoding='utf-8'))['sources']}
out={}
abs_cache={}
if os.path.exists('tmp/_scana_abs.json'): abs_cache=json.load(open('tmp/_scana_abs.json',encoding='utf-8'))
for n in (123,124,125):
    titles=json.load(open(f'reports/round{n}_batch.json',encoding='utf-8'))
    lst=[]
    for t in titles:
        e=ents.get(t)
        if not e: lst.append({'title':t,'missing':True});continue
        fields={k:e.get(k) for k in F if isinstance(e.get(k),str)}
        oa=[s for s in e.get('sources',[]) if s.startswith('openalex-W')]
        lst.append({'title':t,'fields':fields,'openalex':oa})
        for s in oa:
            if s in abs_cache: continue
            w=s.split('-',1)[1]
            for tr in range(4):
                time.sleep(1.2)
                r=subprocess.run(['curl','-L','-sS','--ssl-no-revoke','--compressed','-m','25','-A','Mozilla/5.0 (mailto:clientvip@zhuwyai.me)','-w','\n%{http_code}','https://api.openalex.org/works/'+w],capture_output=True)
                txt=r.stdout.decode('utf-8','replace'); body,_,code=txt.rpartition('\n')
                if code=='429': time.sleep(5*(tr+1)); continue
                break
            try:
                j=json.loads(body); inv=j.get('abstract_inverted_index')
                ab=None
                if inv:
                    pos=sorted((p,wd) for wd,ps in inv.items() for p in ps); ab=' '.join(wd for _,wd in pos)
                abs_cache[s]={'title':j.get('title'),'year':j.get('publication_year'),'abstract':ab,'local_title':srcs.get(s,{}).get('title')}
            except Exception as ex:
                abs_cache[s]={'error':code,'local_title':srcs.get(s,{}).get('title')}
    out[n]=lst
json.dump(abs_cache,open('tmp/_scana_abs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
json.dump(out,open('tmp/_scana_ents.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for n,l in out.items():
    print(n,[(x['title'],len(x.get('openalex',[])),x.get('missing')) for x in l])
