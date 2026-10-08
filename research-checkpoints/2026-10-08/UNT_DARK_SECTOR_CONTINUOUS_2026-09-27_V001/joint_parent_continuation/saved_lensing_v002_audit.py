"""Independent saved-data V002 audit; no numerical-worker imports or new rays."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
encode=lambda p:json.dumps(p,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
freeze=ROOT/'SAVED_POTENTIAL_LENSING_V002_FROZEN.json'
spec=json.loads(freeze.read_text())
for name,digest in spec['files'].items():assert sha(ROOT/name)==digest,name
def load(name,frozen):
    obj=json.loads((ROOT/name).read_text());p=obj['payload']
    assert obj['freeze_sha256']==sha(ROOT/frozen)
    assert obj['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    return p
old=load('SAVED_POTENTIAL_LENSING_RESULTS.json','SAVED_POTENTIAL_LENSING_FROZEN.json')
d=load('SAVED_POTENTIAL_LENSING_V002_RESULTS.json',freeze.name)
assert d['previous_result_sha256']==sha(ROOT/'SAVED_POTENTIAL_LENSING_RESULTS.json')
assert len(old['failed_checks'])==5
assert d['failed_checks']==[c for c in d['checks'] if not c['passed']]
assert all(c['passed']==(math.isfinite(c['error']) and c['error']<=c['tolerance']) for c in d['checks'])
assert d['status']==('COMPLETE' if not d['failed_checks'] else 'FAILED_NUMERICAL_CONTROLS')
synthetic=[c for c in d['checks'] if c['case']=='synthetic_cubic']
assert len(synthetic)==246
assert len({c['name'] for c in synthetic})==246
old_gates={(c['case'],c['name']):c for c in old['checks']}
inherited=[c for c in d['checks'] if 'inherited_unchanged_from' in c]
for check in inherited:
    assert check['inherited_unchanged_from']=='SAVED_POTENTIAL_LENSING_RESULTS.json'
    assert {k:v for k,v in check.items() if k!='inherited_unchanged_from'}==old_gates[check['case'],check['name']]
old_cases={c['case']:c for c in old['cases']};cases={c['case']:c for c in d['cases']}
if d['cases']:
    assert set(cases)==set(old_cases) and len(inherited)==5400 and len(d['checks'])==7891
gates={(c['case'],c['name']):c for c in d['checks']}
assert len(gates)==len(d['checks'])
A0=1.2e-10*3.085677581491367e19/1e6;factor=2*A0/299792.458**2
maximum=0.
def close(a,b,tol=2e-11,floor=1e-20):
    global maximum
    e=abs(a-b)/max(floor,abs(a),abs(b));assert e<=tol,(a,b,e)
    maximum=max(maximum,e)
projected=[];angles=[];changes=[]
for name,c in cases.items():
    before=old_cases[name]
    for key in ('case','freeze','source','hi_tail','h2_tail','stellar_multiplier','N','extent','newtonian','q_kpc2','total_mass_Msun'):
        assert c[key]==before[key]
    assert len(c['rays'])==15 and c['reference_nodes']['maximum_batch_size']<=512
    assert c['reference_nodes']['positive_saved_center_count']>=before['reference_nodes']['positive_saved_center_count']
    for r,prior in zip(c['rays'],before['rays']):
        for key in ('R_kpc','projection','X_kpc','Y_kpc','inclination_deg','box_entry_exit_kpc',
                    'whole_spherical_rad','spherical_orders_raw','analytic_monopole_controls'):
            assert r[key]==prior[key]
        assert r['spherical_parts_reused_from_authenticated_V001']
        assert r['V001_total_rad']==prior['total_rad']
        for key in ('spherical_interior','spherical_exterior'):assert r['pieces_rad'][key]==prior['pieces_rad'][key]
        raw=r['correction_raw_orders'];tag=f"{r['projection']}:{r['R_kpc']}"
        axis=1 if r['projection']=='minor_72' else 0
        for i in (0,1):
            close(r['total_rad'][i],math.fsum(v[i] for v in r['pieces_rad'].values()))
            close(r['total_arcsec'][i],r['total_rad'][i]*180*3600/math.pi)
            close(r['pieces_rad']['finite_box_correction'][i],factor*raw['four'][i])
            close(r['reference_potential_effect_rad'][i],factor*(raw['doubled_reference_four'][i]-raw['four'][i]))
            close(r['V002_minus_V001_rad'][i],r['total_rad'][i]-prior['total_rad'][i])
            for key,value in [(f'exact_cubic_segment:{i}',abs(raw['four'][i]-raw['eight'][i])),
                              (f'parity:{i}',abs(raw['four'][i]+raw['mirror_four'][i]))]:
                close(gates[name,tag+':'+key]['error'],value)
        close(gates[name,tag+':cross_axis']['error'],abs(raw['four'][1-axis]))
        if r['projection']=='face_on':
            close(gates[name,tag+':faceon_trapezoid']['error'],abs(raw['four'][0]-r['faceon_trapezoid']['raw_integral']))
        if r['newtonian_projected_mass']:
            a,b=r['newtonian_projected_mass'],prior['newtonian_projected_mass']
            for key in ('enclosed_baryonic_mass_Msun','exact_angle_rad','target','scope'):assert a[key]==b[key]
            assert a['target']==.01
            signed=r['total_rad'][0]/a['exact_angle_rad']-1
            close(a['fractional_error'],abs(signed))
            assert gates[name,tag+':newtonian_projected_mass']['tolerance']==.01
            close(gates[name,tag+':newtonian_projected_mass']['error'],abs(signed))
            projected.append({'case':name,'R_kpc':r['R_kpc'],'signed_error':signed,'V001_absolute_error':b['fractional_error']})
        angles.append({'case':name,'R_kpc':r['R_kpc'],'projection':r['projection'],
                       'angle_arcsec':r['total_arcsec'][axis],'newtonian':c['newtonian']})
        changes.append({'case':name,'R_kpc':r['R_kpc'],'projection':r['projection'],
                        'relative_change_from_V001':math.hypot(*r['V002_minus_V001_rad'])/math.hypot(*r['total_rad'])})
for comp in d['comparisons'].get('mesh_and_domain_descriptive_only',[]):
    get=lambda name:next(r for r in cases[name]['rays'] if (r['R_kpc'],r['projection'])==(comp['R_kpc'],comp['projection']))
    a,b=get(comp['case']),get(comp['baseline']);change=[x-y for x,y in zip(a['total_rad'],b['total_rad'])]
    for x,y in zip(change,comp['difference_rad']):close(x,y)
    close(comp['fractional_vector_change'],math.hypot(*change)/math.hypot(*a['total_rad']))
for comp in d['comparisons'].get('fixed_stellar_calibration_changes',[]):
    get=lambda name:next(r for r in cases[name]['rays'] if (r['R_kpc'],r['projection'])==(comp['R_kpc'],comp['projection']))
    a,b=get(comp['case']),get(comp['original'])
    for x,y in zip([x-y for x,y in zip(a['total_rad'],b['total_rad'])],comp['difference_rad']):close(x,y)
ratios=[]
for c in d['cases']:
    if c['newtonian'] or c['N']!=512:continue
    newton=next(x for x in d['cases'] if x['source']==c['source'] and x['newtonian'])
    for a,b in zip(c['rays'],newton['rays']):
        assert (a['R_kpc'],a['projection'])==(b['R_kpc'],b['projection'])
        ratios.append({'case':c['case'],'R_kpc':a['R_kpc'],'projection':a['projection'],
                       'ratio':math.hypot(*a['total_rad'])/math.hypot(*b['total_rad'])})
numerical=d['comparisons'].get('mesh_and_domain_descriptive_only',[])
print(json.dumps({'status':d['status'],'source_sha256':sha(Path(__file__)),
    'result_sha256':sha(ROOT/'SAVED_POTENTIAL_LENSING_V002_RESULTS.json'),'freeze_sha256':sha(freeze),
    'previous_result_sha256':d['previous_result_sha256'],'frozen_members':len(spec['files']),
    'case_count':len(cases),'ray_count':len(angles),'checks':len(d['checks']),
    'synthetic_checks':len(synthetic),'inherited_checks':len(inherited),
    'new_real_field_checks':len(d['checks'])-len(synthetic)-len(inherited),
    'failed_checks':d['failed_checks'],'arithmetic_max_scaled':maximum,'projected_controls':projected,
    'angle_ranges_arcsec':{label:[min(r['angle_arcsec'] for r in angles if r['newtonian']==flag),max(r['angle_arcsec'] for r in angles if r['newtonian']==flag)] for label,flag in [('candidate',False),('newtonian',True)]} if angles else {},
    'fine_candidate_to_newtonian_ratios':ratios,
    'maximum_V002_V001_change':max(changes,key=lambda r:r['relative_change_from_V001']) if changes else None,
    'maximum_mesh_change':max((r for r in numerical if cases[r['case']]['N']==512),key=lambda r:r['fractional_vector_change']) if numerical else None,
    'maximum_domain_change':max((r for r in numerical if cases[r['case']]['extent']==1023),key=lambda r:r['fractional_vector_change']) if numerical else None,
    'seconds':d['seconds'],'peak_self_rss_bytes':d['peak_self_rss_bytes']},indent=2,sort_keys=True))
