import json,glob,subprocess,time,re,sys,os
os.chdir('E:/ai_project/dili')
entries={}
for f in glob.glob('data/*.json'):
    try: d=json.load(open(f,encoding='utf-8'))
    except: continue
    if isinstance(d,dict) and 'entries' in d:
        for e in d['entries']: entries[e.get('title')]=e
src={s['id']:s for s in json.load(open('data/sources.json',encoding='utf-8'))['sources']}
F=['definition','overview','geo','influence','polities','connections','today','time_or_place']
cache={}
if os.path.exists('tmp/_scanb_cache.json'): cache=json.load(open('tmp/_scanb_cache.json',encoding='utf-8'))
def fetch(w):
    if w in cache: return cache[w]
    for i in range(5):
        time.sleep(1.2)
        r=subprocess.run(['curl','-L','-sS','--ssl-no-revoke','--compressed','-m','25','-A','Mozilla/5.0 (mailto:clientvip@zhuwyai.me)','-w','\n%{http_code}','https://api.openalex.org/works/'+w],capture_output=True)
        out=r.stdout.decode('utf-8','replace'); body,_,code=out.rpartition('\n')
        if code=='429': time.sleep(5*(i+1)); continue
        try:
            j=json.loads(body); inv=j.get('abstract_inverted_index')
            ab=None
            if inv:
                pos=sorted((p,k) for k,v in inv.items() for p in v); ab=' '.join(k for p,k in pos)
            cache[w]={'title':j.get('title'),'year':j.get('publication_year'),'abstract':ab}
        except Exception as ex: cache[w]={'title':None,'abstract':None,'err':code}
        break
    json.dump(cache,open('tmp/_scanb_cache.json','w',encoding='utf-8'),ensure_ascii=False)
    return cache.get(w,{'abstract':None})
n=sys.argv[1]
titles=json.load(open(f'reports/round{n}_batch.json',encoding='utf-8'))
out=[]
for t in titles:
    e=entries.get(t)
    if not e: out.append({'title':t,'missing':True}); continue
    ss=e.get('sources',[])
    rec={'title':t,'fields':{k:e.get(k) for k in F if e.get(k)},'sources':[]}
    for s in ss:
        sid=s if isinstance(s,str) else s.get('id')
        m=re.search(r'openalex-(W\d+)',sid or '')
        info={'id':sid,'title':src.get(sid,{}).get('title')}
        if m: info['oa']=fetch(m.group(1))
        rec['sources'].append(info)
    out.append(rec)
json.dump(out,open(f'tmp/_scanb_{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('done',n)
