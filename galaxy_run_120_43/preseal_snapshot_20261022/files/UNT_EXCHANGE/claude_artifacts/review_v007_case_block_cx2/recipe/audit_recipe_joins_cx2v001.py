"""A99 candidate recipe/source joins, own JSON checks only; no project execution."""
from pathlib import Path
import json,hashlib

A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
O=A/'review_v007_case_block_cx2/recipe'
pins={};raw={}
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def eq(a,b):return canon(a)==canon(b)
def read(p,h,asjson=True):
 p=Path(p);assert not any(v in ('runs','runs_ext') for v in p.parts)
 assert not any(v in ('runs','runs_ext') for v in p.resolve(strict=True).parts)
 b=p.read_bytes();assert sha(b)==h,str(p);pins[str(p)]=h;raw[str(p)]=b
 return parse(b) if asjson else b.decode()
prep_path=A/'review_v007_case_block_cx2/prep_recipe/SOURCE_BINDING_CHECKLIST_CX2V001.json'
prep=read(prep_path,'b56626d73ff25484a1dd057ffa3c8ace2036225e4c903a07a4740c218f5e1a2a')
for p,h in prep['pins_start'].items():read(p,h,Path(p).suffix=='.json')
cp=A/'v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json'
C=read(cp,'76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
B=read(A/'v007_final_prereg_c4/r5/out/CASE_BLOCK_BUILD_C4V001.json','bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad')
draft=read(A/'tail_scheme_impl_c2/driver/out/CASE_BLOCK_V007_DRAFT_C2V001.json','6bf4ce5a4219d281fa480d4249e818e8d9fc39779b3ad605e1a069f42e0da4c1')
pre=parse(raw[str(A/'kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json')])
ext=parse(raw[str(A/'kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json')])
grids={k:v['composite_grid_spec'] for k,v in pre['grids'].items()};grids.update({k:ext['grids'][k]['composite_grid_spec'] for k in ('G5','G6')})
checks=[]
def ck(n,b):checks.append({'name':n,'pass':bool(b)})
ck('eleven exact entries',set(C['cases'])=={x['case'] for x in prep['cases']}|{'C5H'})
ck('schema/mode/empty key map',C['schema']=='UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003' and C['route_a_mode']=='parallel8' and C['key_equivalence_map']==[])
ck('build output exact identity',B['case_block']=={'path':str(cp),'sha256':pins[str(cp)],'bytes':len(raw[str(cp)])})
ck('build provenance ten exact cases',set(B['provenance_per_case'])=={x['case'] for x in prep['cases']})
norms={}
for p in prep['cases']:
 lab=p['case'];e=C['cases'][lab];s=parse(raw[p['filled_spec']['path']]);r=parse(raw[p['dry_report']['path']]);n=r['normalized_spec'];num=n['numerics'];uv=num['uv_tail'];bp=B['provenance_per_case'][lab];norms[lab]=num
 ck(lab+' whole normalized numerics exact',eq(e['normalized_spec_equal'],{'/numerics':num}))
 ck(lab+' filled/report join',r['call_spec']==p['filled_spec']['path'] and r['call_spec_sha256']==p['filled_spec']['sha256'])
 ck(lab+' named filled and report pins in note',all(v in e['note'] for ref in (p['filled_spec'],p['dry_report']) for v in ref.values()))
 ck(lab+' build provenance exact refs',bp['filled_spec']==p['filled_spec'] and bp['dry_report']==p['dry_report'])
 ck(lab+' entry grid',e['grid']==p['expected_grid'])
 ck(lab+' full registered grid object',eq(num['composite_grid_spec'],grids[e['grid']]))
 ck(lab+' entry and normalized truncation',eq(e['truncation'],p['truncation']) and eq(num['truncation'],p['truncation']))
 ck(lab+' tail and RO1',e['tail'] is True and e['ro1_required'] is True)
 ck(lab+' sole r5 driver',e['drivers_allowed']==['b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'])
 ck(lab+' reported uv digest join only',e['uv_tail_config_sha256']==bp['uv_tail_config_sha256']==r['uv_tail']['config']['normalized_sha256'])
 ck(lab+' raw and normalized physical exact anchor',eq(s['physical'],pre['anchor']['physical']) and eq(n['physical'],pre['anchor']['physical']))
 ck(lab+' raw and normalized coefficient object exact anchor',eq(s['coefficients'],pre['anchor']['coefficients']) and eq(n['coefficients'],pre['anchor']['coefficients']))
 ck(lab+' DDO galaxy',s['galaxy']==n['galaxy']=='DDO154')
 ck(lab+' physical not unsupported entry keys',not ({'physical','coefficients'}&set(e)))
 ck(lab+' N8/M32/P6',num['route_a']['column_workers']==8 and num['route_a']['max_iterations']==32 and eq(num['picard'],pre['anchor']['picard']))
 ck(lab+' outer exactly registered distinction',eq(uv['outer'],p['outer']))
 sr={'rule':'nodes_v001','ext_grid':grids['G5']} if lab=='C4T-D5' else 'continuum_v001'
 ck(lab+' source rule exactly registered distinction',eq(uv['source_rule'],sr))
 ck(lab+' lambda exactly registered distinction',eq(uv['lambda_scale'],p['lambda_scale']))
 ck(lab+' gas128 and lapse-only',type(uv['gas']['M_s']) is int and uv['gas']['M_s']==128 and uv['enabled'] is True and uv['lapse_only'] is True)
 ck(lab+' recorded normalization changes',bp['dry_normalization_added_leaves']==p['raw_vs_normalized_numerics_difference_paths'])
 ck(lab+' remainder UV same as C4T',eq({k:v for k,v in uv.items() if k not in ('outer','lambda_scale','source_rule')},{k:v for k,v in C['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail'].items() if k not in ('outer','lambda_scale','source_rule')}))
ck('all ten whole numerics pairwise distinct',len({canon(n) for n in norms.values()})==10)
for a,b in [('C4T','C4T-KLO'),('C4T','C4T-KHI'),('C4T-KLO','C4T-KHI'),('C4T','C4T-A'),('C4T-D5','C4T-C5c')]:
 ck(a+'/'+b+' UV distinctions',not eq(norms[a]['uv_tail'],norms[b]['uv_tail']) and C['cases'][a]['uv_tail_config_sha256']!=C['cases'][b]['uv_tail_config_sha256'])
c5=C['cases']['C5H']
ck('C5H constants only',c5['grid']=='G5' and eq(c5['truncation'],{'shape':'cube','kmax_inverse_kpc':None}) and c5['normalized_spec_equal']=={} and c5['tail'] is False and c5['ro1_required'] is False and c5['call_spec_sha256']=='60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e' and c5['drivers_allowed']==['999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6'])
ck('old draft obsolete schema',draft['schema']=='UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V002')
ck('old draft retired labels','C4T-K16' in draft['cases'] and 'C4T-K64' in draft['cases'] and 'C4T-KLO' not in draft['cases'])
oldnum=draft['cases']['C4T']['normalized_spec_equal']['/numerics']
ck('old draft P32Ms64',oldnum['uv_tail']['outer']['K_big_inverse_kpc']==32 and oldnum['uv_tail']['gas']['M_s']==64)
ck('old draft driver differs',draft['cases']['C4T']['drivers_allowed']!=C['cases']['C4T']['drivers_allowed'])
ck('old draft D5 missing whole numerics','/numerics' not in draft['cases']['C4T-D5']['normalized_spec_equal'])
end={p:sha(Path(p).read_bytes()) for p in pins};changed=[p for p,h in pins.items() if end[p]!=h]
ck('all input bytes stable',not changed)
out={'schema':'CX2_A99_CASE_BLOCK_RECIPE_JOINS_V001','date_u':'Sun Oct 18 20:40:34 UTC 2026','policy':'nice unavailable (sandbox); 0514 waiver','verdict':'PASS','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'findings':[],
 'TESTED':'Own strict JSON and canonical whole-numerics equality, ten filled/report joins, build-record provenance joins, registered physical/coefficient object identity, distinctions, old draft static diagnosis, before/after byte pins. No project module imported or executed.',
 'UNTESTED':'Fresh driver normalization and uv digest recomputation, complete comparator validator, protected C5H normalized-reference equivalence, underlying coefficient archive bytes, production run acceptance, final prereg binding. Other lanes own structural/normalizer work.',
 'pins_start':pins,'pins_end':end,'changed':changed}
assert all(x['pass'] for x in checks)
p=O/'RECIPE_JOIN_RESULTS_CX2V001.json'
with p.open('x') as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'verdict':out['verdict'],'passed':out['passed'],'total':out['total'],'sources':len(pins),'sha256':sha(p.read_bytes())}))
