"""Independent post-execution arithmetic audit; no physical modules or solvers.

Prints a snapshot of currently published evidence, without modifying anything.
This is a post-exposure check, not a preregistered experiment.
"""
import bisect
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
encode = lambda p: json.dumps(p, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
freeze = ROOT / 'HALOGAS_FIELD_FROZEN.json'
fh = sha(freeze)
spec = json.loads(freeze.read_text())
for name, digest in spec['files'].items():
    assert sha(ROOT/name) == digest, name
G, A0 = 4.30091e-6, 1.2e-10*3.085677581491367e19/1e6
maxima = {}
hashes = {freeze.name: fh}


def close(a, b, category='arithmetic', tolerance=2e-10):
    error = abs(a-b)/max(1., abs(a), abs(b))
    assert math.isfinite(error) and error <= tolerance, (category, a, b, error)
    maxima[category] = max(maxima.get(category, 0.), error)
    return error


def payload(name, expected=fh):
    path = ROOT/name
    record = json.loads(path.read_text())
    assert record['freeze_sha256'] == expected, name
    assert record['payload_sha256'] == hashlib.sha256(encode(record['payload'])).hexdigest(), name
    hashes[name] = sha(path)
    return record['payload']


def interp(x, xs, ys):
    assert xs[0] <= x <= xs[-1]
    i = max(0, min(len(xs)-2, bisect.bisect_right(xs, x)-1))
    t = (x-xs[i])/(xs[i+1]-xs[i])
    return (1-t)*ys[i]+t*ys[i+1]


def slope(xs, ys, i):
    ids = (0, 1, 2) if i == 0 else ((len(xs)-3, len(xs)-2, len(xs)-1) if i == len(xs)-1 else (i-1, i, i+1))
    x = xs[i]
    return sum(ys[j]*(2*x-xs[k]-xs[l])/((xs[j]-xs[k])*(xs[j]-xs[l]))
               for j, k, l in (ids, (ids[1], ids[2], ids[0]), (ids[2], ids[0], ids[1])))


qualified = payload('HALOGAS_FIELD_SOURCE_QUALIFICATION.json')
assert qualified['status'] == 'COMPLETE' and all(qualified['checks'].values())
extraction = json.loads((ROOT/'halogas_source_candidate/PLANAR_SOURCE_RESULTS.json').read_text())
order = next(o for o in extraction['orders'] if o['subpixels_per_axis'] == 8)
source_summaries, source_by_model = {}, {}
for q in qualified['models']:
    width, bins = q['width_arcsec'], q['bins']
    assert q['model'] == spec['models'][str(width)] and len(bins) == {40: 51, 120: 17}[width]
    assert q['stellar_multiplier'] == spec['stellar_multiplier'] and q['helium_factor_applied_once'] == 1.36
    assert q['status'] == 'COMPLETE' and all(c['passed'] and math.isfinite(c['error']) and c['error'] <= c['tolerance'] for c in q['checks'])
    p = order[f'profile_{width}arcsec']
    assert p['complete_by_conservative_chord_bound'] == [i < len(bins) for i in range(len(p['r_lo_kpc']))]
    means = [1.36*b['bare_HI_mass_Msun']/(math.pi*1e6*(b['R_hi_kpc']**2-b['R_lo_kpc']**2)) for b in bins]
    ends = [means[0]]+[min(a,b) for a,b in zip(means,means[1:])]+[0.]
    for i, b in enumerate(bins):
        assert b['R_lo_kpc'] == p['r_lo_kpc'][i] and b['R_hi_kpc'] == p['r_hi_kpc'][i]
        assert b['bare_HI_mass_Msun'] == p['groups']['full']['mass_Msun'][i]
        controls = [ends[i], 3*means[i]-ends[i]-ends[i+1], ends[i+1]]
        for a, v in zip(controls, b['controls_HI_He_Msun_pc2']): close(a,v,'source_controls',1e-13)
        close(b['mean_HI_He_Msun_pc2'], means[i], 'source_controls', 1e-13)
        assert min(controls) >= 0 and max(controls) <= 3*means[i]+1e-14*max(1., means[i])
        ds = b['R_hi_kpc']**2-b['R_lo_kpc']**2
        mass = math.pi*1e6*ds*sum(controls)/3
        for key in ('HI_He_mass_Msun','analytic_mass_Msun','gauss_mass_Msun'):
            close(b[key],mass,'source_full_integral',1e-12)
        left,right=b['R_lo_kpc'],b['R_hi_kpc']
        aa,bb=left+(right-left)/8,right-(right-left)/8
        ta,tb=(aa*aa-left*left)/ds,(bb*bb-left*left)/ds
        def primitive(t):
            d,e,f=controls
            return d*t+(e-d)*t*t+(d-2*e+f)*t**3/3
        partial=math.pi*1e6*ds*(primitive(tb)-primitive(ta))
        for key in ('partial_analytic_Msun','partial_gauss_Msun'):
            close(b[key],partial,'source_partial_integral',1e-12)
    masses=p['groups']['full']['mass_Msun']
    included,excluded=math.fsum(masses[:len(bins)]),math.fsum(masses[len(bins):])
    for key,value in [('included_retained_bare_HI_Msun',included),('excluded_retained_bare_HI_Msun',excluded),
                      ('full_map_retained_bare_HI_Msun',included+excluded),('excluded_fraction',excluded/(included+excluded)),
                      ('included_negative_pixel_contribution_Msun',math.fsum(p['groups']['full']['negative_mass_Msun'][:len(bins)]))]:
        close(q[key],value,'source_ledger',1e-13)
    close(q['component_masses_Msun']['HI_He'],1.36*included,'source_ledger',1e-13)
    assert q['zero_retention_bin_indices']==[i for i,b in enumerate(bins) if b['bare_HI_mass_Msun']==0]
    source_by_model[q['model']]=q
    source_summaries[q['model']]={k:v for k,v in q.items() if k not in ('bins','checks','scope','exterior_assumption')}
    source_summaries[q['model']]['passed_check_count']=len(q['checks'])
assert set(source_by_model)==set(spec['models'].values())
close(qualified['models'][0]['included_retained_bare_HI_Msun'],qualified['models'][1]['included_retained_bare_HI_Msun'],'same_mass',1e-13)

oracle=payload('HALOGAS_FIELD_ORACLE.json')
assert oracle['status']=='COMPLETE' and len(oracle['cases'])==10 and len(oracle['checks'])==170
assert all(c['passed'] and math.isfinite(c['error']) and c['error']<=c['tolerance'] for c in oracle['checks'])
recorded_checks={c['name']:c for c in oracle['checks']}
seen_checks=set()
def oracle_check(name,value,tolerance):
    c=recorded_checks[name];seen_checks.add(name)
    close(c['error'],value,'oracle_gate_arithmetic',1e-13)
    assert c['tolerance']==tolerance and value<=tolerance
rows=json.loads((ROOT/'NGC3198_BARYON_INPUT.json').read_text())['rows']
inherited_knots=[0.]+[r['radius_kpc'] for r in rows]
oracle_summaries=[]
for o in oracle['cases']:
    model,R=o['model'],o['R_kpc'];q=source_by_model[model]
    assert R in spec['oracle_radii_kpc'] and o['width_arcsec']==q['width_arcsec']
    assert o['component_masses_Msun']==q['component_masses_Msun']
    distance=min(abs(v-R) for v in inherited_knots+[b['R_hi_kpc'] for b in q['bins']])
    close(distance,o['nearest_knot_distance_kpc'],'oracle_geometry',1e-13)
    assert distance>1e-10
    for j,h in enumerate(o['heights']):
        height=min(.2,distance/4)/2**j;assert h['z_kpc']==height
        for key in ('gR_kms2_per_kpc','potential_kms2'):
            a,b=h['orders']['48'][key],h['orders']['96'][key]
            oracle_check(f'quadrature:{model}:{R}:{height}:{key}',abs(a-b)/max(1.,abs(b)),1e-8)
        for order,out in h['orders'].items():
            assert int(order) in spec['oracle_orders'] and out['cutoff_kpc']==q['support_kpc']
            for key in ('gR_kms2_per_kpc','potential_kms2'):
                close(out[key],sum(c[key] for c in out['components'].values()),'oracle_sum',1e-13)
            missing=sum(c['omitted_mass_Msun'] for c in out['components'].values())
            close(out['force_tail_bound_kms2_per_kpc'],G*missing/(out['cutoff_kpc']-R)**2,'oracle_tail',1e-13)
            close(out['potential_tail_bound_kms2'],G*missing/(out['cutoff_kpc']-R),'oracle_tail',1e-13)
            assert out['components']['HI_He']['omitted_mass_Msun']==0
            for name,c in out['components'].items():
                mass=q['component_masses_Msun'][name]
                error=abs(c['quadrature_mass_Msun']+c['omitted_mass_Msun']-mass)/mass
                assert error<=1e-9
                if order=='96': oracle_check(f'mass:{model}:{R}:{height}:{name}',error,1e-9)
    values=[h['orders']['96']['gR_kms2_per_kpc'] for h in o['heights']]
    extrap=[2*values[i+1]-values[i] for i in (0,1)]
    for a,b in zip(extrap,o['extrapolated_gR_kms2_per_kpc']):close(a,b,'oracle_extrap',1e-13)
    oracle_check(f'height:{model}:{R}',abs(extrap[0]-extrap[1])/max(1.,abs(extrap[1])),1e-3)
    oracle_check(f'tail:{model}:{R}',o['heights'][-1]['orders']['96']['force_tail_bound_kms2_per_kpc']/max(1.,abs(extrap[1])),1e-10)
    oracle_summaries.append({'model':model,'R_kpc':R,'force_kms2_kpc':extrap[1],
                            'height_relative_change':recorded_checks[f'height:{model}:{R}']['error'],
                            'HI_force_final_height':o['heights'][-1]['orders']['96']['components']['HI_He']['gR_kms2_per_kpc']})
assert seen_checks==set(recorded_checks)
assert {(o['model'],o['R_kpc']) for o in oracle['cases']}=={(m,R) for m in source_by_model for R in spec['oracle_radii_kpc']}

control_hash=sha(ROOT/'STELLAR_CALIBRATION_FROZEN.json')
cases,case_summaries={},{}
for width in (40,120):
    model=spec['models'][str(width)]
    for n,extent,newton in spec['jobs_per_source']:
        name=f'{model}_N{n}_L{extent}_Newton{int(newton)}'
        if not (ROOT/(name+'.json')).exists(): continue
        p=payload(name+'.json');cases[(model,n,extent,newton)]=p
        assert (p['case'],p['model'],p['width_arcsec'],p['N'],p['extent'],p['newtonian'])==(name,model,width,n,extent,newton)
        assert all(p['checks'].values()) and len(p['comparison'])==43 and len(p['radii'])==n
        assert p['stellar_multiplier']==spec['stellar_multiplier']
        assert len(p['phi'])==n and all(len(r)==n and all(math.isfinite(x) for x in r) for r in p['phi'])
        assert all(b>a for a,b in zip(p['radii'],p['radii'][1:]))
        q=source_by_model[model]
        for k,v in q['component_masses_Msun'].items():close(p['component_masses_Msun'][k],v,'field_mass',1e-13)
        close(p['total_mass_Msun'],sum(q['component_masses_Msun'].values()),'field_mass',1e-13)
        xs=p['radii'];mid=[v[0]-xs[0]*(v[1]-v[0])/(xs[1]-xs[0]) for v in p['phi']]
        radial=[slope(xs,mid,i) for i in range(n)]
        for a,b in zip(radial,p['radial_force_a0']):close(a,b,'saved_phi_derivative',2e-10)
        control_name=f'ML36_CAL_HI1_H21_V001_N{n}_L{extent}_Newton{int(newton)}'
        assert p['paired_calibrated_control_case']==control_name
        control=payload(control_name+'.json',control_hash)
        for k in ('stars','H2_He'):assert p['component_masses_Msun'][k]==control['component_masses_Msun'][k]
        for a,b in zip(p['comparison'],control['comparison']):
            assert all(a[k]==b[k] for k in ('R','velocity','error'))
            force=interp(a['R'],xs,radial);v2=A0*a['R']*force
            for k,v in [('radial_force_a0',force),('velocity_squared',v2),('signed_force_change_a0',force-b['radial_force_a0']),
                        ('signed_v2_change_kms2',v2-b['velocity_squared']),('control_radial_force_a0',b['radial_force_a0']),('control_prediction',b['prediction'])]:
                close(a[k],v,'field_rows',2e-9)
            if v2>=0:
                velocity=math.sqrt(v2)
                for k,v in [('prediction',velocity),('residual',velocity-a['velocity']),('velocity_change_kms',velocity-b['prediction'])]:
                    close(a[k],v,'field_rows',2e-9)
            else:assert a['prediction'] is None and a['residual'] is None and a['velocity_change_kms'] is None
        for low in (0,2,8):
            selected=[r for r in p['comparison'] if r['R']>=low and r['residual'] is not None]
            summary=p['summaries_descriptive_only'][f'R_ge_{low}_kpc']
            assert summary['count']==len(selected) and summary['omitted_negative_force_count']==sum(r['R']>=low and r['residual'] is None for r in p['comparison'])
            expected={'rms_kms':math.sqrt(math.fsum(r['residual']**2 for r in selected)/len(selected)),
                      'mean_residual_kms':math.fsum(r['residual'] for r in selected)/len(selected),
                      'max_abs_residual_kms':max(abs(r['residual']) for r in selected),
                      'nominal_sum_squared_error_units':math.fsum((r['residual']/r['error'])**2 for r in selected),
                      'mean_change_from_calibrated_control_kms':math.fsum(r['velocity_change_kms'] for r in selected)/len(selected)}
            for k,v in expected.items():close(summary[k],v,'field_summary',1e-13)
        last=p['history'][-1]
        assert len(p['history'])<=300 and all(h['outer']==i and not h.get('linear_failed',False) for i,h in enumerate(p['history']))
        assert last['flux_balance_error']<=2e-6 and last['nonlinear_error']<=1e-9 and last['clipped_faces']==0
        assert p['source_mass_relative_error']<=1e-13 and p['qualified_source_relative_error']<=1e-13
        if not newton and (extent==1023 or n==512):
            base=cases[(model,256,255,False)]
            error=max(abs(a['radial_force_a0']-b['radial_force_a0'])/max(abs(a['radial_force_a0']),1e-12)
                      for a,b in zip(p['comparison'],base['comparison']) if a['R']>=2)
            label='remote_domain' if extent==1023 else 'mesh_refinement'
            close(p['numerical_comparison'][label+'_max_force_change'],error,'field_refinement',1e-13)
            assert error<.02
        ring_errors=[]
        if newton:
            matches=[o for o in oracle['cases'] if o['model']==model]
            assert len(p['independent_newtonian_force_comparison'])==5
            for c,o in zip(p['independent_newtonian_force_comparison'],matches):
                assert c['R_kpc']==o['R_kpc']
                force=A0*interp(o['R_kpc'],xs,p['radial_force_a0']);ref=o['extrapolated_gR_kms2_per_kpc'][-1]
                heights=abs(ref-o['extrapolated_gR_kms2_per_kpc'][0]);lastorders=o['heights'][-1]['orders']
                quad=abs(lastorders['96']['gR_kms2_per_kpc']-lastorders['48']['gR_kms2_per_kpc'])
                allowance=.02*max(1.,abs(ref))+heights+quad
                for k,v in [('grid_gR_kms2_per_kpc',force),('oracle_extrapolated_gR_kms2_per_kpc',ref),
                            ('oracle_extrapolation_difference',heights),('oracle_quadrature_difference',quad),
                            ('absolute_discrepancy',abs(force-ref)),('numerical_allowance',allowance)]:close(c[k],v,'field_ring',1e-13)
                assert c['passed'] and abs(force-ref)<=allowance
                ring_errors.append(abs(force-ref)/abs(ref))
        case_summaries[name]={k:p[k] for k in ('checks','numerical_comparison','summaries_descriptive_only','seconds_this_invocation','peak_self_rss_bytes')}
        case_summaries[name].update(last_row=p['comparison'][-1],last_history=last,outer_updates=len(p['history']),maximum_relative_ring_discrepancy=max(ring_errors,default=None))

final_path=ROOT/'HALOGAS_FIELD_RESULTS.json'
complete=final_path.exists()
if complete:
    final=payload(final_path.name)
    assert final['status']=='COMPLETE' and len(cases)==len(final['case_files_sha256'])==8
    assert set(final['models'])==set(source_by_model)
    for name,digest in final['case_files_sha256'].items():assert hashes[name]==digest
    assert final['oracle_sha256']==hashes['HALOGAS_FIELD_ORACLE.json']
    assert final['source_qualification_sha256']==hashes['HALOGAS_FIELD_SOURCE_QUALIFICATION.json']
print(json.dumps({'status':'COMPLETE' if complete else 'PARTIAL_CASE_SNAPSHOT',
                  'role':'Independent post-execution saved-data arithmetic; no new PDE or ring quadrature.',
                  'audit_source_sha256':sha(Path(__file__)), 'input_sha256':hashes,
                  'authenticated_manifest_members':len(spec['files']),
                  'qualification_check_count':sum(len(q['checks']) for q in qualified['models'])+len(qualified['checks']),
                  'oracle_check_count':len(oracle['checks']),'source_summaries':source_summaries,
                  'oracle_summaries':oracle_summaries,'arithmetic_maxima_scaled':maxima,
                  'published_cases':len(cases),'case_summaries':case_summaries},indent=2,sort_keys=True,allow_nan=False))
