"""Post-execution independent saved-data audit; no solver imports or evolution.

Prints a JSON report. Does not modify evidence or claim preregistration.
"""
import bisect
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
G = 4.30091e-6
A0 = 1.2e-10 * 3.085677581491367e19 / 1e6
C = 1.2567828155112788
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
encode = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
freeze = ROOT / 'STELLAR_CALIBRATION_FROZEN.json'
fh = sha(freeze)
spec = json.loads(freeze.read_text())
for name, digest in spec['files'].items():
    assert sha(ROOT / name) == digest, name

def payload(name, expected=fh):
    o = json.loads((ROOT / name).read_text())
    assert o['freeze_sha256'] == expected
    assert o['payload_sha256'] == hashlib.sha256(encode(o['payload'])).hexdigest()
    return o['payload']

def interp(x, xs, ys):
    j = max(0, min(len(xs)-2, bisect.bisect_right(xs, x)-1))
    t = (x-xs[j])/(xs[j+1]-xs[j])
    return ys[j]*(1-t)+ys[j+1]*t

def slope(xs, ys, i):
    ids = (0, 1, 2) if i == 0 else ((len(xs)-3, len(xs)-2, len(xs)-1) if i == len(xs)-1 else (i-1, i, i+1))
    x = xs[i]
    return sum(ys[j]*(2*x-xs[k]-xs[l])/((xs[j]-xs[k])*(xs[j]-xs[l]))
               for j,k,l in (ids, (ids[1],ids[2],ids[0]), (ids[2],ids[0],ids[1])))

def close(a, b, tol=2e-10):
    e = abs(a-b)/max(1., abs(a), abs(b))
    assert e <= tol, (a,b,e)
    return e

maxima = {'field_absolute_a0': 0., 'scalar_scaled': 0., 'diagnostic_scaled': 0.}
cases, summary = {}, {}
oldfreeze = sha(ROOT / 'GALAXY_FIELD_FROZEN.json')
final = payload('STELLAR_CALIBRATION_RESULTS.json')
assert final['status'] == 'COMPLETE' and len(final['case_files_sha256']) == 4
for filename, digest in final['case_files_sha256'].items():
    assert sha(ROOT / filename) == digest
    p = payload(filename)
    assert p['case'] == Path(filename).stem and all(p['checks'].values())
    assert p['stellar_multiplier'] == C and p['hi_tail'] and p['h2_tail']
    old = payload(p['original_same_grid_case']+'.json', oldfreeze)
    xs = p['radii']
    mid = [r[0]-xs[0]*(r[1]-r[0])/(xs[1]-xs[0]) for r in p['phi']]
    radial = [slope(xs,mid,i) for i in range(len(xs))]
    maxima['field_absolute_a0'] = max(maxima['field_absolute_a0'], max(abs(a-b) for a,b in zip(radial,p['radial_force_a0'])))
    assert len(p['comparison']) == len(old['comparison']) == 43
    for a,b in zip(p['comparison'],old['comparison']):
        assert all(a[k] == b[k] for k in ('R','velocity','error'))
        x = interp(a['R'],xs,radial)
        expected = {'radial_force_a0': x, 'velocity_squared': a['R']*A0*x,
                    'prediction': math.sqrt(a['R']*A0*x)}
        expected.update(residual=expected['prediction']-a['velocity'],
                        old_radial_force_a0=b['radial_force_a0'],old_prediction=b['prediction'],old_residual=b['residual'],
                        force_change_a0=x-b['radial_force_a0'],velocity_squared_change=expected['velocity_squared']-b['velocity_squared'],
                        velocity_change=expected['prediction']-b['prediction'])
        for k,v in expected.items():
            maxima['scalar_scaled'] = max(maxima['scalar_scaled'],close(a[k],v))
    for k,mass in old['component_masses_Msun'].items():
        close(p['component_masses_Msun'][k], mass*(C if k == 'stars' else 1.), 1e-13)
    for low in (0,2,8):
        rows = [a for a in p['comparison'] if a['R'] >= low]
        s = p['summaries_descriptive_only'][f'R_ge_{low}_kpc']
        assert s['count'] == s['paired_real_velocity_count'] == len(rows) and s['omitted_negative_force_count'] == 0
        vals = {'rms_kms': math.sqrt(sum(a['residual']**2 for a in rows)/len(rows)),
                'mean_residual_kms':sum(a['residual'] for a in rows)/len(rows),
                'max_abs_residual_kms':max(abs(a['residual']) for a in rows),
                'nominal_sum_squared_error_units':sum((a['residual']/a['error'])**2 for a in rows),
                'mean_velocity_change_kms':sum(a['velocity_change'] for a in rows)/len(rows)}
        for k,v in vals.items(): maxima['scalar_scaled'] = max(maxima['scalar_scaled'],close(s[k],v))
    summary[p['case']] = {k:p[k] for k in ('checks','component_masses_Msun','numerical_comparison','summaries_descriptive_only','seconds_this_invocation','peak_self_rss_bytes')}
    summary[p['case']]['last_row'] = p['comparison'][-1]
    cases[(p['N'],p['extent'],p['newtonian'])] = p
assert set(cases) == {(256,255,False),(320,1023,False),(512,255,False),(512,255,True)}
for key,label in (((320,1023,False),'remote_domain'),((512,255,False),'mesh_refinement')):
    p,base = cases[key], cases[(256,255,False)]
    e = max(abs(a['radial_force_a0']-b['radial_force_a0'])/max(abs(a['radial_force_a0']),1e-12)
            for a,b in zip(p['comparison'],base['comparison']) if a['R'] >= 2)
    close(e,p['numerical_comparison'][label+'_max_force_change'],1e-13)

oracle = payload('STELLAR_CALIBRATION_ORACLE.json')
assert sha(ROOT/'STELLAR_CALIBRATION_ORACLE.json') == final['oracle_sha256']
assert oracle['status'] == 'COMPLETE' and all(c['passed'] and c['error']<=c['tolerance'] for c in oracle['checks'])
prior = payload('RING_ORACLE_RESULTS.json',sha(ROOT/'RING_ORACLE_FROZEN.json'))
oldrings = [r for r in prior['cases'] if r['hi_tail'] and r['h2_tail']]
maxring = 0.
for new,old,comparison in zip(oracle['cases'],oldrings,cases[(512,255,True)]['independent_newtonian_force_comparison']):
    assert new['R_kpc'] == old['R_kpc'] == comparison['R_kpc']
    for a,b in zip(new['heights'],old['heights']):
        assert a['z_kpc'] == b['z_kpc']
        for order in ('48','96'):
            ao,bo = a['orders'][order],b['orders'][order]
            for name,piece in bo['components'].items():
                for k,v in piece.items(): close(ao['components'][name][k],v*(C if name == 'stars' else 1.),1e-13)
            for k in ('gR_kms2_per_kpc','potential_kms2'):
                close(ao[k],sum(piece[k] for piece in ao['components'].values()),1e-13)
            missing = sum(piece['omitted_mass_Msun'] for piece in ao['components'].values())
            close(ao['force_tail_bound_kms2_per_kpc'],G*missing/(ao['cutoff_kpc']-new['R_kpc'])**2,1e-13)
            close(ao['potential_tail_bound_kms2'],G*missing/(ao['cutoff_kpc']-new['R_kpc']),1e-13)
    extrap = [2*new['heights'][j+1]['orders']['96']['gR_kms2_per_kpc']-new['heights'][j]['orders']['96']['gR_kms2_per_kpc'] for j in (0,1)]
    for a,b in zip(extrap,new['extrapolated_gR_kms2_per_kpc']): close(a,b,1e-13)
    force=interp(new['R_kpc'],cases[(512,255,True)]['radii'],cases[(512,255,True)]['radial_force_a0'])*A0
    close(comparison['grid_gR_kms2_per_kpc'],force,1e-13)
    close(comparison['oracle_extrapolated_gR_kms2_per_kpc'],extrap[-1],1e-13)
    maxring=max(maxring,abs(force-extrap[-1])/abs(extrap[-1]))
    assert comparison['passed'] and abs(force-extrap[-1])<=comparison['numerical_allowance']

r=spec['r']; ai=8/(3*math.pi)
def flux(g):
    v=g*ai; z=(g/r)**2; h=v/math.sqrt(1+z)
    y=2/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*h/2)/3)
    t=math.atan2(1.,y)
    e=h*h/4*(1.5*t-.5*math.sin(2*t)-math.sin(4*t)/8)
    return (2*e*(1+z)**(-1.5)+v*z*(2+z)/(1+z)**2)/ai
def inverse(d):
    lo,hi=0.,2*(d+math.sqrt(d)+r)
    for _ in range(80):
        mid=(lo+hi)/2
        if flux(mid)<d: lo=mid
        else: hi=mid
    return (lo+hi)/2
diag=final['matched_diagnostic']; assert diag['status']=='COMPLETE' and len(diag['rows'])==43 and len(diag['checks'])==172
assert all(c['passed'] and c['error']<=c['tolerance'] for c in diag['checks'])
actual,newton=cases[(512,255,False)],cases[(512,255,True)]
inputs=json.loads((ROOT/'NGC3198_BARYON_INPUT.json').read_text())['rows']
hi=[3.17,3.88,4.53,4.97,5.24,5.19,4.73,3.95,3.26,2.94,2.66,2.29,2.12,1.98,1.62,1.27,1.14,1.11,1.01,.86,.72,.57,.36,.14]
hir=[i*.5*13.8*1000*math.pi/(180*60) for i in range(24)]
profiles=[(hir,[1.36*s for s in hi],(hir[-1]-hir[-2])/math.log(hi[-2]/hi[-1])),
          ([0.]+[a['radius_kpc'] for a in inputs],[C*inputs[0]['stars_Msun_pc2']]+[C*a['stars_Msun_pc2'] for a in inputs],3.2)]
h2=[a for a in inputs if a['H2_Msun_pc2'] is not None]
profiles.append(([0.]+[a['radius_kpc'] for a in h2],[h2[0]['H2_Msun_pc2']]+[a['H2_Msun_pc2'] for a in h2],2.7))
def sigma(radius):
    return sum(interp(radius,rs,ss) if radius <= rs[-1] else ss[-1]*math.exp(-(radius-rs[-1])/tail)
               for rs,ss,tail in profiles)
for row,a,n in zip(diag['rows'],actual['comparison'],newton['comparison']):
    radius,x,nr=a['R'],a['radial_force_a0'],n['radial_force_a0']
    assert row['R_kpc']==radius and row['hard_edge_warning'] is False
    b,z=row['sheet_flux_a0'],row['reconstructed_vertical_a0']
    coefficient=flux(math.hypot(x,z))/math.hypot(x,z)
    vector=nr/math.hypot(nr,b)*inverse(math.hypot(nr,b))
    radial=math.copysign(inverse(abs(nr)),nr); deep=math.copysign(math.sqrt(abs(nr)),nr)
    flat=math.sqrt(G*sum(actual['component_masses_Msun'].values())/A0)/radius
    terms={'remaining_field':x-vector,'vertical_projection':vector-radial,'law_shape_vs_deep':radial-deep,'newtonian_disk_vs_monopole':deep-flat}
    vals={'true_radial_a0':x,'newtonian_radial_a0':nr,'mu':coefficient,'radial_solenoidal_flux_a0':coefficient*x-nr,
          'reference_residual_v2_kms2':radius*A0*flat-a['velocity']**2,'true_residual_v2_kms2':radius*A0*x-a['velocity']**2}
    maxima['diagnostic_scaled']=max(maxima['diagnostic_scaled'],close(coefficient*z,b))
    for k,v in vals.items(): maxima['diagnostic_scaled']=max(maxima['diagnostic_scaled'],close(row[k],v))
    for k,v in terms.items():
        maxima['diagnostic_scaled']=max(maxima['diagnostic_scaled'],close(row['force_terms_a0'][k],v),close(row['signed_v2_terms_kms2'][k],v*radius*A0))
    close(sum(row['signed_v2_terms_kms2'].values())+row['reference_residual_v2_kms2'],row['true_residual_v2_kms2'])
    close(b,2*math.pi*G*1e6*row['sigma_Msun_pc2']/A0)
    close(row['sigma_Msun_pc2'],sigma(radius),1e-13)
regions=[]
for lower,upper in ((0,2),(2,8),(8,20),(20,50)):
    rows=[a for a in actual['comparison'] if lower <= a['R'] < upper]
    regions.append({'lower_kpc':lower,'upper_exclusive_kpc':upper,'count':len(rows),
                    'old_rms_kms':math.sqrt(sum(a['old_residual']**2 for a in rows)/len(rows)),
                    'new_rms_kms':math.sqrt(sum(a['residual']**2 for a in rows)/len(rows))})
result={'mode':'independent post-execution saved-data arithmetic only; no propagation/PDE',
        'status':'PASS','source_sha256':sha(Path(__file__)),'freeze_sha256':fh,'freeze_file_count':len(spec['files']),
        'case_file_sha256':final['case_files_sha256'],'oracle_sha256':final['oracle_sha256'],
        'result_sha256':sha(ROOT/'STELLAR_CALIBRATION_RESULTS.json'),
        'case_checks':sum(len(p['checks']) for p in cases.values()),'oracle_checks':len(oracle['checks']),
        'diagnostic_checks':len(diag['checks']),'audit_maxima':maxima,'max_ring_relative_discrepancy':maxring,
        'cases':summary,'posthoc_descriptive_regions_not_acceptance_gates':regions,'last_diagnostic':diag['rows'][-1]}
print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
