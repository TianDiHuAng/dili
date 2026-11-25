# -*- coding: utf-8 -*-
"""全量汇总字段自检：evidence_level / round62_gaps / SATURATION / no_solution / semantic_scan 互相对齐。"""
import json, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, level_of, UNITS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = load_sources(); T = load_entries(UNITS)
g = json.load(open(os.path.join(ROOT,'reports','round62_gaps.json'),encoding='utf-8'))
sat = json.load(open(os.path.join(ROOT,'SATURATION.json'),encoding='utf-8'))
ev = json.load(open(os.path.join(ROOT,'data','evidence_level.json'),encoding='utf-8'))
lvl = collections.Counter(level_of(e,S) for e in T.values()); lvmap={t:level_of(e,S) for t,e in T.items()}
errs=[]
for t,l in lvmap.items():
    if ev['levels'].get(t,{}).get('level')!=l: errs.append(f'ev {t}')
gd={d['id']:d['count'] for d in g['gap_definitions']}
calc_g1=sum(1 for t in T if lvmap[t]=='C')
calc_g3=sum(1 for t,e in T.items() if content_count(e,S)==1 and lvmap[t]!='D')
if gd['G1']!=calc_g1: errs.append(f'G1 {gd["G1"]} vs {calc_g1}')
if gd['G3']!=calc_g3: errs.append(f'G3 {gd["G3"]} vs {calc_g3}')
sdef={d['id']:d['count'] for d in sat['gap_model']['definitions']}
if sdef!=gd: errs.append('sat.definitions')
scnt=sat['gap_model'].get('counts',{})
if scnt and scnt!=gd: errs.append('sat.counts')
if sat['evidence']['levels']!={k:lvl.get(k,0) for k in 'ABCD'}: errs.append('sat.levels')
g2=sum(1 for e in T.values() if content_count(e,S)>=2); o1=sum(1 for e in T.values() if content_count(e,S)==1); z0=sum(1 for e in T.values() if content_count(e,S)==0)
if (sat['evidence'].get('ge2_content'),sat['evidence'].get('one_content'),sat['evidence'].get('zero_content'))!=(g2,o1,z0): errs.append('sat.content')
if sat.get('unsolvable'): errs.append('sat.unsolvable')
ns=json.load(open(os.path.join(ROOT,'data','no_solution.json'),encoding='utf-8'))['entries']
if ns: errs.append('no_solution非空')
if gd['G2']!=len(ns): errs.append('G2 vs no_solution')
ss=json.load(open(os.path.join(ROOT,'data','semantic_scan.json'),encoding='utf-8'))
if ss['unresolved']['entries']: errs.append('unresolved非空')
if len(ss['scanned_entries'])!=len(T): errs.append('scanned!=243')
print(('ALL CONSISTENT' if not errs else 'ERRORS'), len(errs)); [print(' -',e) for e in errs]
print('levels',dict(lvl),'content',g2,o1,z0,'gaps',gd)
