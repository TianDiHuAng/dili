# -*- coding: utf-8 -*-
"""通用：把 reports/roundNNN_scan.json 的 SOFT/FAIL 整句替换写回正文，NA/NOACAD 记录，更新 scanned_entries。用法：python tools/apply_scan.py 123 124 ..."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import save_docs, update_coverage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = ['africa','asia','europe','north-america','south-america','oceania','antarctica','global-themes']
docs = {u: json.load(open(os.path.join(ROOT,'data',u+'.json'), encoding='utf-8')) for u in U}
T = {e['title']: e for d in docs.values() for e in d['entries']}
sp = os.path.join(ROOT,'data','semantic_scan.json'); S = json.load(open(sp, encoding='utf-8'))
tot = {}
for r in sys.argv[1:]:
    p = os.path.join(ROOT,'reports',f'round{r}_scan.json')
    scan = json.load(open(p, encoding='utf-8'))
    n = {'SOFT':0,'FAIL':0,'NA':0,'NOACAD':0,'miss':0}
    for en in scan['entries']:
        e = T.get(en['title'])
        if not e: print('NO ENTRY', en['title']); continue
        if en.get('verdict') == 'NOACAD':
            n['NOACAD'] += 1
            e['pending_notes'] = (e.get('pending_notes') or '') + f' 【第{r}轮语义扫描】无学术来源，正文无学术落点句；本条依赖机构/数据/常识来源，语义对题无需逐句对读。'
        for i in en.get('items', []):
            v = i.get('verdict'); sid = i.get('source'); f = i.get('field')
            if v == 'NA':
                n['NA'] += 1
                e['pending_notes'] = (e.get('pending_notes') or '') + f' 【第{r}轮语义扫描】{sid} 在正文中无对应落点句，仅作登记，不支撑任何断言。'
                continue
            if v not in ('SOFT','FAIL') or i.get('fix') is None: continue
            c = i.get('claim') or ''
            if not (f and c and c in (e.get(f) or '')):
                n['miss'] += 1; print('MISS', r, en['title'], sid); continue
            e[f] = e[f].replace(c, i['fix'], 1).replace('  ',' ').strip(); n[v] += 1
            e['pending_notes'] = (e.get('pending_notes') or '') + f' 【第{r}轮语义扫描 {v}】{sid}：{(i.get("reason") or "")[:120]}'
        e['last_update'] = '2026-11-25'
    S['scanned_entries'] = sorted(set(S['scanned_entries']) | {x['title'] for x in scan['entries']})
    S['scans_done'].append({'round': int(r), 'scope': f'{len(scan["entries"])} 条逐条语义扫描',
        'result': {k: sum(1 for x in scan['entries'] if x.get('verdict')==k) for k in ('PASS','SOFT','FAIL','NA','NOACAD')},
        'file': f'reports/round{r}_scan.json'})
    print(r, n); tot[r] = n
save_docs(docs); update_coverage(docs)
json.dump(S, open(sp,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(tot, open(os.path.join(ROOT,'reports','apply_scan_last.json'),'w',encoding='utf-8'), ensure_ascii=False)
