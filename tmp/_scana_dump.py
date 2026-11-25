import json,re,sys
ab=json.load(open('tmp/_scana_abs.json',encoding='utf-8'))
ents=json.load(open('tmp/_scana_ents.json',encoding='utf-8'))
n=sys.argv[1]
for e in ents[n]:
    print('=====',e['title'],e.get('openalex'))
    for k,v in e.get('fields',{}).items():
        for m in re.finditer(r'所引[^。]*。',v): print(' [%s] %s'%(k,m.group(0)))
        for m in re.finditer(r'[^。]*(研究|文献|学者|论文)[^。]*。',v):
            if '所引' not in m.group(0): print(' (%s?) %s'%(k,m.group(0).strip()[:200]))
    for s in e.get('openalex',[]):
        a=ab.get(s,{})
        print(' --',s,'|',a.get('title'),'|',a.get('year'),'| local:',a.get('local_title'),'| err:',a.get('error'))
        print('    ABS:',(a.get('abstract') or '摘要缺失')[:900])
