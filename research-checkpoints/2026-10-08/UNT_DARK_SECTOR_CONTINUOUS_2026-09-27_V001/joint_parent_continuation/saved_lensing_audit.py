"""Post-execution audit and saved-node diagnosis; no worker imports or rays run."""
import bisect
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
enc=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
freeze=ROOT/'SAVED_POTENTIAL_LENSING_FROZEN.json'
spec=json.loads(freeze.read_text())
for name,h in spec['files'].items():assert sha(ROOT/name)==h,name
result=ROOT/'SAVED_POTENTIAL_LENSING_RESULTS.json'
obj=json.loads(result.read_text());d=obj['payload']
assert obj['freeze_sha256']==sha(freeze) and obj['payload_sha256']==hashlib.sha256(enc(d)).hexdigest()
assert len(d['cases'])==20 and len(d['checks'])==7645
assert d['failed_checks']==[c for c in d['checks'] if not c['passed']]
assert len(d['failed_checks'])==5 and d['status']=='FAILED_NUMERICAL_CONTROLS'
assert all(c['passed']==(math.isfinite(c['error']) and c['error']<=c['tolerance']) for c in d['checks'])
assert all(c['name']=='face_on:2.7:newtonian_projected_mass' and c['tolerance']==.01 for c in d['failed_checks'])
A0=1.2e-10*3.085677581491367e19/1e6;G=4.30091e-6;c_light=299792.458;factor=2*A0/c_light**2
maximum=0.
def close(a,b,tol=1e-11,unit_floor=1e-20):
    global maximum
    error=abs(a-b)/max(unit_floor,abs(a),abs(b))
    assert error<=tol,(a,b,error)
    maximum=max(maximum,error)

rows=json.loads((ROOT/'NGC3198_BARYON_INPUT.json').read_text())['rows']
hi_values=[3.17,3.88,4.53,4.97,5.24,5.19,4.73,3.95,3.26,2.94,2.66,2.29,2.12,1.98,1.62,1.27,1.14,1.11,1.01,.86,.72,.57,.36,.14]
hi_radii=[j*.5*13.8e3*math.pi/(180*60) for j in range(24)]
def enclosed(case,b):
    molecular=[r for r in rows if r['H2_Msun_pc2'] is not None]
    profiles=[(hi_radii,[1.36*v for v in hi_values],(hi_radii[-1]-hi_radii[-2])/math.log(hi_values[-2]/hi_values[-1]) if case['hi_tail'] else None),
              ([0.]+[r['radius_kpc'] for r in rows],[case['stellar_multiplier']*rows[0]['stars_Msun_pc2']]+[case['stellar_multiplier']*r['stars_Msun_pc2'] for r in rows],3.2),
              ([0.]+[r['radius_kpc'] for r in molecular],[molecular[0]['H2_Msun_pc2']]+[r['H2_Msun_pc2'] for r in molecular],2.7 if case['h2_tail'] else None)]
    total=0.
    for rs,ss,tail in profiles:
        for a,z,sa,sz in zip(rs,rs[1:],ss,ss[1:]):
            if b<=a:break
            t=min(b,z);m=(sz-sa)/(z-a)
            total+=(sa-m*a)*(t*t-a*a)/2+m*(t**3-a**3)/3
        if tail and b>rs[-1]:
            total+=ss[-1]*tail*((rs[-1]+tail)-(b+tail)*math.exp(-(b-rs[-1])/tail))
    return 2*math.pi*1e6*total

census={c['case']:c for c in spec['case_census']};by_case={c['case']:c for c in d['cases']}
assert set(census)==set(by_case)
gates={(c['case'],c['name']):c for c in d['checks']}
assert len(gates)==7645
diagnosis=[];totals=[];projected=[]
for case in d['cases']:
    assert all(case[k]==v for k,v in census[case['case']].items())
    assert len(case['rays'])==15 and {(r['R_kpc'],r['projection']) for r in case['rays']}=={(b,label) for b in spec['radii_kpc'] for label in spec['projections']}
    assert case['reference_nodes']['maximum_batch_size']<=512
    q=G*case['total_mass_Msun']/A0;close(q,case['q_kpc2'])
    assert sum(c['case']==case['case'] for c in d['checks'])==(386 if case['newtonian'] else 381)
    for row in case['rays']:
        b=row['R_kpc'];entry,exit_=row['box_entry_exit_kpc'];aa,zz=math.atan(entry/b),math.atan(exit_/b)
        assert (row['X_kpc'],row['Y_kpc'])==((0.,b) if row['projection']=='minor_72' else (b,0.))
        axis=1 if row['projection']=='minor_72' else 0
        tag=f"{row['projection']}:{b}"
        for j in (0,1):
            raw=row['correction_raw_orders']
            for suffix,value in [(f'exact_segment:{j}',abs(raw['two'][j]-raw['four'][j])),
                                 (f'parity:{j}',abs(raw['two'][j]+raw['mirror_two'][j]))]:
                close(gates[case['case'],tag+':'+suffix]['error'],value)
        close(gates[case['case'],tag+':cross_axis']['error'],abs(raw['two'][1-axis]))
        for part in ('whole','interior','exterior'):
            value=max(abs(a-b_) for a,b_ in zip(row['spherical_orders_raw']['64'][part],row['spherical_orders_raw']['128'][part]))
            close(gates[case['case'],tag+':sphere_quadrature:'+part]['error'],value)
        for j in (0,1):
            close(row['total_rad'][j],math.fsum(v[j] for v in row['pieces_rad'].values()))
            close(row['total_arcsec'][j],row['total_rad'][j]*180*3600/math.pi)
            close(row['pieces_rad']['finite_box_correction'][j],factor*row['correction_raw_orders']['two'][j])
            close(row['reference_potential_effect_rad'][j],factor*(row['correction_raw_orders']['doubled_reference_two'][j]-row['correction_raw_orders']['two'][j]))
        for kind,control in row['analytic_monopole_controls'].items():
            whole=2*q/b**2 if kind=='newtonian' else math.pi*math.sqrt(q)/b
            inside=q/b**2*(math.sin(zz)-math.sin(aa)) if kind=='newtonian' else math.sqrt(q)/b*(zz-aa)
            for key,value in [('whole',whole),('interior',inside),('exterior',whole-inside)]:close(control['exact_scalar_integrals'][key],value)
            close(control['exact_whole_angle_rad'],factor*b*whole)
        if row['projection']=='face_on':close(row['faceon_trapezoid']['raw_integral'],row['correction_raw_orders']['two'][0],1e-9)
        if row['newtonian_projected_mass']:
            control=row['newtonian_projected_mass'];mass=enclosed(case,b);exact=4*G*mass/(c_light*c_light*b)
            close(control['enclosed_baryonic_mass_Msun'],mass)
            close(control['exact_angle_rad'],exact)
            close(control['fractional_error'],abs(row['total_rad'][0]/control['exact_angle_rad']-1))
            projected.append({'case':case['case'],'R_kpc':b,'signed_error':row['total_rad'][0]/exact-1})
        totals.append({'case':case['case'],'R_kpc':b,'projection':row['projection'],'main_angle_arcsec':row['total_arcsec'][axis],'cross_angle_arcsec':row['total_arcsec'][1-axis]})
    if case['newtonian']:
        original=json.loads((ROOT/(case['case']+'.json')).read_text())['payload'];centers=original['radii'];L=original['extent']
        for b in (2.7,8.7):
            i=bisect.bisect_right(centers,b)-1
            def saved_projection(spherical):
                values=[]
                for k in (i,i+1):
                    r=centers[k]
                    v=[q*(1-1/math.hypot(r,z)) for z in centers] if spherical else original['phi'][k].copy()
                    zero=v[0]-centers[0]*(v[1]-v[0])/(centers[1]-centers[0])
                    values.append([zero]+v+[q*(1-1/math.hypot(r,L))])
                nodes=[0.]+centers+[L]
                gradients=[2*b*(hi-lo)/(centers[i+1]**2-centers[i]**2) for lo,hi in zip(*values)]
                return factor*math.fsum((nodes[j+1]-nodes[j])*(gradients[j+1]+gradients[j]) for j in range(len(nodes)-1))
            row=next(r for r in case['rays'] if r['projection']=='face_on' and r['R_kpc']==b)
            direct=saved_projection(False);reference=saved_projection(True)
            sphere=row['pieces_rad']['spherical_interior'][0];outside=row['pieces_rad']['spherical_exterior'][0];target=row['newtonian_projected_mass']['exact_angle_rad']
            close(direct+sphere-reference+outside,row['total_rad'][0])
            diagnosis.append({'case':case['case'],'R_kpc':b,'radial_bracket_kpc':centers[i:i+2],
                'full_saved_interpolant_plus_exterior_fractional_error':(direct+outside)/target-1,
                'reference_interpolation_defect_rad':sphere-reference,
                'reference_interpolation_defect_fraction_of_target':(sphere-reference)/target,
                'reconstructed_total_rad':direct+sphere-reference+outside,
                'saved_total_rad':row['total_rad'][0]})
ratios=[]
for case in d['cases']:
    if case['newtonian'] or case['N']!=512:continue
    newton=next(c for c in d['cases'] if c['source']==case['source'] and c['newtonian'])
    for a,b in zip(case['rays'],newton['rays']):
        assert (a['R_kpc'],a['projection'])==(b['R_kpc'],b['projection'])
        ratios.append({'case':case['case'],'R_kpc':a['R_kpc'],'projection':a['projection'],
                       'ratio':math.hypot(*a['total_rad'])/math.hypot(*b['total_rad'])})
for comparison in d['comparisons']['mesh_and_domain_descriptive_only']:
    current=next(r for r in by_case[comparison['case']]['rays'] if (r['R_kpc'],r['projection'])==(comparison['R_kpc'],comparison['projection']))
    old=next(r for r in by_case[comparison['baseline']]['rays'] if (r['R_kpc'],r['projection'])==(comparison['R_kpc'],comparison['projection']))
    delta=[a-b for a,b in zip(current['total_rad'],old['total_rad'])]
    for a,b in zip(delta,comparison['difference_rad']):close(a,b)
    close(math.hypot(*delta)/math.hypot(*current['total_rad']),comparison['fractional_vector_change'])
print(json.dumps({'status':'VERIFIED_FAILED_NUMERICAL_QUALIFICATION','source_sha256':sha(Path(__file__)),
    'freeze_sha256':sha(freeze),'result_sha256':sha(result),'frozen_member_count':len(spec['files']),
    'case_count':20,'ray_count':300,'check_count':7645,'failed_checks':d['failed_checks'],
    'independent_arithmetic_max_scaled':maximum,'diagnosis':diagnosis,'projected_mass_controls':projected,
    'raw_unqualified_fine_candidate_to_newtonian_ratio_range':[min(r['ratio'] for r in ratios),max(r['ratio'] for r in ratios)],
    'angle_ranges_arcsec':{mode:[min(r['main_angle_arcsec'] for r in totals if by_case[r['case']]['newtonian']==flag),max(r['main_angle_arcsec'] for r in totals if by_case[r['case']]['newtonian']==flag)] for mode,flag in [('candidate',False),('newtonian',True)]},
    'maximum_mesh_change':max((r for r in d['comparisons']['mesh_and_domain_descriptive_only'] if by_case[r['case']]['N']==512),key=lambda r:r['fractional_vector_change']),
    'maximum_domain_change':max((r for r in d['comparisons']['mesh_and_domain_descriptive_only'] if by_case[r['case']]['extent']==1023),key=lambda r:r['fractional_vector_change'])},indent=2,sort_keys=True))
