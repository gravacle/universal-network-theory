import importlib.util, json, hashlib, math, sys, os
A='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_freeze_0462'
R='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1'
REG=R+'/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json'; REGSHA='13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d'
MAN=R+'/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json'; MANSHA='a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'
OUT=sys.argv[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,f'{A}/{name}.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
E=load('calibration_region_engine_c3v001'); F=load('prediction_freeze_c3v001')
reg=json.load(open(REG)); rows=reg['rows']; ids=[r['id'] for r in rows]
obs={r['id']:r['observed_speed_km_s'] for r in rows}; rect={r['id']:(r['conditional_random_acceptance_low_km_s'],r['conditional_random_acceptance_high_km_s']) for r in rows}
# toy: 3 varying coords (a: log free, b: linear free, D: linear nuisance with zero effect) + fixed c; speeds = obs + slope*(u-0.5)
coords=[{'name':'a','transform':'log','lower':0.5,'upper':2.0,'role':'free','trial_value':1.0},
        {'name':'b','transform':'linear','lower':-1.0,'upper':1.0,'role':'free','trial_value':0.0},
        {'name':'D','transform':'linear','lower':3.9,'upper':4.2,'role':'nuisance','trial_value':4.04},
        {'name':'c','transform':'linear','lower':0.0,'upper':1.0,'role':'fixed','trial_value':0.3}]
def u_of(theta):
    ua=(math.log(theta['a'])-math.log(0.5))/(math.log(2.0)-math.log(0.5)); ub=(theta['b']+1.0)/2.0; return ua,ub
calls={'n':0}
def toy(theta):
    calls['n']+=1; ua,ub=u_of(theta)
    sp={rid: obs[rid]+ 4.0*(ua-0.5)*(i%3+1) - 3.0*(ub-0.5)*(i%2+1) for i,rid in enumerate(ids)}
    return {'speeds_km_s':sp,'valid':True,'reasons':[]}
res=E.run_calibration_region(forward=toy,coordinates=coords,observation_region_path=REG,observation_region_sha256=REGSHA,
    u_seed=None,budget=400,rel_step=0.05,min_step=1e-4,max_halvings=3,null_tolerance=1e-6,repair_iterations=10,
    max_repair_step=0.25,march_step=0.05,bisection_steps=6,design_count=24,rng_seed=3)
print('engine status',res['status'],'ok',res['ok'],'evals',res['evaluations_used'],'calls',calls['n'])
idn=res['identifiability']; print('identified',idn['identified'],'near_null',idn['near_null'],'sv',[round(s,4) for s in idn['singular_values']])
ex=res['exploration']; adm=ex['admitted_points']; rej=ex['rejected_points']
# independent recheck of every classification
bad=0
for p in adm:
    sp=toy(p['theta_natural'])['speeds_km_s']
    if not all(rect[r][0]<=sp[r]<=rect[r][1] for r in ids): bad+=1
for p in rej:
    sp=toy(p['theta_natural'])['speeds_km_s']
    if all(rect[r][0]<=sp[r]<=rect[r][1] for r in ids): bad+=1
print('admitted',len(adm),'rejected',len(rej),'misclassified',bad)
print('hull_box',{k:(round(v['min'],4),round(v['max'],4)) for k,v in ex['hull_box'].items()})
print('unidentified', [(d['index'], [round(x,3) for x in d['vector_u']], d['sensitivity']) for d in ex['unidentified_directions']])
assert bad==0 and res['status']=='COMPLETE'
# freeze
man=F.load_query_manifest(path=MAN,expected_sha256=MANSHA); assert man['ok'],man['reasons']; qids=man['query_ids']
sel=F.select_representative_points(exploration=res,interior_count=4); assert sel['ok'],sel['reasons']
print('representatives',len(sel['points']),[p['role'] for p in sel['points']])
def toy_ngc(theta):
    ua,ub=u_of(theta); return {'speeds_km_s':{q: 100.0+20.0*(ua-0.5)*(j%4+1)-10.0*(ub-0.5) for j,q in enumerate(qids)},'valid':True,'reasons':[]}
env=F.evaluate_envelopes(forward_ngc=toy_ngc,points=sel['points'],query_ids=qids,budget=100); assert env['ok'],env['reasons']
# independent envelope recheck for Q01
vals=[toy_ngc(p['theta_natural'])['speeds_km_s'][qids[0]] for p in sel['points']]
e0=env['envelopes'][qids[0]]; assert abs(e0['min']-min(vals))<1e-12 and abs(e0['max']-max(vals))<1e-12, (e0,min(vals),max(vals))
mp=OUT+'/FREEZE_MANIFEST_leadcheck.json'
w=F.write_freeze_manifest(out_path=mp,parameter_region={'hull_box':ex['hull_box'],'identified':idn['identified'],'near_null':idn['near_null'],'bounds_semantics':res['bounds_semantics']},
    alternatives={'state':'toy','source':'toy','approximation':'toy'},observation_rule=reg['statistical_choice'],envelopes=env['envelopes'],query_ids=qids,
    code_files=[f'{A}/calibration_region_engine_c3v001.py',f'{A}/prediction_freeze_c3v001.py'],input_files=[REG,MAN],notes={'lead_check':True})
assert w['ok'],w['reasons']; print('manifest',w['manifest_sha256'][:16],w['bytes_written'])
doc=json.load(open(mp)); body={k:v for k,v in doc.items() if k!='manifest_sha256'}
assert hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==doc['manifest_sha256']
assert 'vobs' not in json.dumps(doc).lower() and doc['target_velocities_included'] is False
v=F.verify_freeze_manifest(freeze_manifest_path=mp); assert v['ok'],v['reasons']
# synthetic targets: 40 within 0.5 sigma, 3 outside
tr=[{'id':q,'velocity':doc['predictions'][i]['velocity']+(0.5 if i<40 else 3.0),'sigma':1.0} for i,q in enumerate(qids)]
sc=F.score_after_freeze(freeze_manifest_path=mp,target_rows=tr); assert sc['ok'] and not sc['refused'],sc['reasons']
print('score within',sc['within_error_count'],'overlap',sc['band_overlap_count'],'invalid',sc['invalid_count'],'rows',len(sc['rows']))
assert sc['within_error_count']==40
# tamper
raw=open(mp,'rb').read(); tp=OUT+'/FREEZE_MANIFEST_tampered.json'
i=raw.index(b'"velocity":'); open(tp,'wb').write(raw[:i+12]+ (b'9' if raw[i+12:i+13]!=b'9' else b'8') + raw[i+13:])
sc2=F.score_after_freeze(freeze_manifest_path=tp,target_rows=tr); print('tampered refused',sc2['refused'],sc2['reasons'][:1])
assert sc2['refused']
# wrong order refuses
sc3=F.score_after_freeze(freeze_manifest_path=mp,target_rows=list(reversed(tr))); assert sc3['refused']
# empty region toy
def toy_empty(theta):
    d=toy(theta); d['speeds_km_s'][ids[0]]+=50.0; return d
r2=E.run_calibration_region(forward=toy_empty,coordinates=coords,observation_region_path=REG,observation_region_sha256=REGSHA,u_seed=None,budget=60,rel_step=0.05,min_step=1e-4,max_halvings=3,null_tolerance=1e-6,repair_iterations=5,max_repair_step=0.25,march_step=0.05,bisection_steps=4,design_count=8,rng_seed=1)
print('empty status',r2['status'],'empty_region',r2['exploration']['empty_region'],'evals',r2['evaluations_used'])
assert r2['status']=='NO_ADMITTED_POINT'
print('LEAD CHECK 0462: ALL PASSED')
