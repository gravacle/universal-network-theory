"""Saved BBN-proxy arithmetic only; no table/spline evaluation or producer import."""
import hashlib,json,math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RESULT=HERE/'BBN_TABLE_PROXY_V001_RESULTS.json'
FREEZE=HERE/'BBN_TABLE_PROXY_V001_FROZEN.json'

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    seen=set();files={};occurrences=0
    def manifest(path):
        nonlocal occurrences
        path=path.resolve();path.relative_to(ROOT)
        if path in seen:return
        seen.add(path);files[str(path.relative_to(ROOT))]=sha(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            occurrences+=1;q=Path(name);candidates=[q] if q.is_absolute() else [ROOT/q,path.parent/q]
            candidates={p.resolve() for p in candidates if p.is_file() and p.resolve().is_relative_to(ROOT)}
            assert len(candidates)==1
            p=candidates.pop();assert sha(p)==digest;files[str(p.relative_to(ROOT))]=digest
            if p.name.endswith('_FROZEN.json'):manifest(p)
    manifest(FREEZE)
    payload_serialization=[]
    def wrapped(name):
        path=HERE/(name+'_RESULTS.json');w=json.loads(path.read_text())
        assert w['freeze_sha256']==sha(HERE/(name+'_FROZEN.json'))
        canonical=w['payload']
        if name=='BBN_TABLE_PROXY_V001':
            # The frozen producer constructs this one dictionary with integer
            # keys. JSON erases key types; canonical sort then changes order.
            # Restore ONLY this declared schema for exact producer-hash replay.
            assert set(canonical['matched_Delta0'])=={str(i) for i in range(18)}
            canonical=dict(canonical,matched_Delta0={int(k):v for k,v in canonical['matched_Delta0'].items()})
            payload_serialization.append(dict(file=path.name,
                original_loaded_key_hash=hashlib.sha256(encode(w['payload'])).hexdigest(),
                producer_key_types='matched_Delta0 keys are integers 0..17 before JSON encoding',
                typed_schema_hash=hashlib.sha256(encode(canonical)).hexdigest()))
        assert w['payload_sha256']==hashlib.sha256(encode(canonical)).hexdigest()
        return w['payload']
    p=wrapped('BBN_TABLE_PROXY_V001');old=wrapped('FINITE_GAP_PHOTON_BUDGET_V001');cal=wrapped('GLOBAL_GAP_LIMIT_CALIBRATION_V001')
    assert p['configuration']==json.loads(FREEZE.read_text())['configuration']
    config=p['configuration'];checks=0;maxerr=0.;fail=[]
    def check(name,got,wanted,scale=None,tol=2e-12):
        nonlocal checks,maxerr
        checks+=1;den=max(1.,abs(wanted)) if scale is None else max(abs(scale),1e-300)
        err=abs(got-wanted)/den;maxerr=max(maxerr,err)
        if not math.isfinite(err) or err>tol:fail.append(dict(name=name,error=err,tolerance=tol))
    obs=json.loads((HERE/'bbn_inputs_v001/BBN_OBSERVATIONS_V001.json').read_text());assert obs==p['observations']
    expected={(s,r,R) for s in range(4) for r in range(18) for R in [32,128,512,2048,8192]}
    assert len(p['rows'])==360 and {(r['spectrum_index'],r['reference'],r['R']) for r in p['rows']}==expected
    oldrows={r['source_row_index']:r for r in old['rows']};refs={r['reference']:r for r in cal['references']}
    assert len(p['matched_Delta0'])==18
    thermal=p['thermal_interface'];records=thermal['per_resolution'];fine=records[-1]
    ratio=thermal['endpoint_sigma_over_photon']
    check('endpoint_entropy',thermal['endpoint_extra_density_normalization'],ratio**(4/3))
    check('endpoint_scale',thermal['endpoint_scale_factor_fourth_power_normalization'],ratio**(-4/3))
    product=thermal['endpoint_extra_density_normalization']*thermal['endpoint_scale_factor_fourth_power_normalization']
    check('endpoint_product',thermal['endpoint_combined_late_normalization'],product)
    bounds=[max(r['log_ratio_all_T_bounds'][0] for r in records)+math.log(product),min(r['log_ratio_all_T_bounds'][1] for r in records)+math.log(product)]
    assert bounds[0]<=bounds[1]
    for i in range(2):check('history_intersection',thermal['log_ratio_all_T_intersection'][i],bounds[i])
    for r in records:
        assert r['log_ratio_end_bounds'][0]<=r['midpoint_readout']<=r['log_ratio_end_bounds'][1]
        for i in range(2):check('thermal_split',r['log_ratio_end_bounds'][i],r['heating_only_bounds'][i]+r['derivative_drift_bounds'][i])
    A=config['finite_gap_reference_temperature_MeV']*1e6*config['eV_J']/(config['k_B_J_K']*config['inherited_T0_K'])
    Amin=A*(fine['sigma_bounds'][0]/(4*math.pi**2/45))**(1/3)*math.exp(-bounds[1]/4)
    check('photon_A',p['photon_scale_reference_A_at_10keV'],A)
    check('history_A_lower',p['thermal_history_lower_bound_A_at_10keV'],Amin)
    def prediction(label,v):
        if v['status']!='TABLE_PROXY':return
        for key in ['helium','deuterium']:
            q=v['observables'][key];res=q['prediction']-obs[key]['value']
            check(label+':residual:'+key,q['signed_residual'],res)
            check(label+':obs_sigma:'+key,q['observational_sigma'],obs[key]['sigma'])
            check(label+':numerical_allowance:'+key,q['numerical_allowance'],config['interpolation_allowance'][key])
            check(label+':standardized:'+key,q['descriptive_marginal_standardized_residual'],res/math.hypot(q['table_theory_sigma'],obs[key]['sigma']))
            assert q['table_theory_sigma']>0
        Y=v['observables']['helium']['prediction'];D=v['observables']['deuterium']['prediction']
        check(label+':helium_D_convention',v['helium_D_only_denominator_correction'],Y*(1+2*D)/(1+2*Y*D)-Y)
        check(label+':helium_He3_coefficient',v['helium_linear_coefficient_unprovided_He3_over_H'],3*Y*(1-Y)/(1+2*Y*D)**2)
    for ref,base in p['matched_Delta0'].items():
        check('baseline_coordinate',base['omega_b'],refs[int(ref)]['bbn']['omega_b']);check('baseline_Delta',base['Delta'],0.)
        prediction('baseline'+ref,base)
    conversion=(7/8)*(4/11)**(4/3);supported=0;outside=0
    for row in p['rows']:
        source=oldrows[row['source_row_index']];ref=refs[row['reference']]
        assert (row['spectrum_index'],row['reference'],row['R'])==(source['spectrum_index'],source['reference'],source['R'])
        assert row['conditional_baryon_benchmark']==ref['bbn']
        assert row['conserved_scalar_abundance_status']=='NOT_YET_QUALIFIED'
        check('late_photon',row['late_photon_ratio'],source['asymptote_over_photons'])
        delta=source['asymptote_over_photons']/conversion;check('late_Delta',row['late_Delta_coordinate'],delta)
        v=row['proxy'];check('proxy_baryon',v['omega_b'],ref['bbn']['omega_b']);check('proxy_Delta',v['Delta'],delta)
        in_grid=(p['table_metadata']['omega_grid'][0]<=v['omega_b']<=p['table_metadata']['omega_grid'][-1] and p['table_metadata']['Delta_grid'][0]<=delta<=p['table_metadata']['Delta_grid'][-1])
        assert (v['status']=='TABLE_PROXY')==in_grid
        if in_grid:
            supported+=1;prediction(str(row['source_row_index']),v)
            base=p['matched_Delta0'][str(row['reference'])]
            for key in ['helium','deuterium']:
                check('matched_Delta0_difference',v['minus_matched_Delta0'][key],v['observables'][key]['prediction']-base['observables'][key]['prediction'])
        else:outside+=1
        x=delta*(7*math.pi**2/120)*(fine['sigma_bounds'][1]/(11*math.pi**2/45))**(4/3)/fine['plasma_rho_over_T4_bounds'][0]
        ratios=[math.sqrt((1+x)/(1+x*math.exp(-L)))-1 for L in bounds]
        expected_H=[min(0.,ratios[0]),max(0.,ratios[1])]
        for i in range(2):check('H_envelope',row['thermal_proxy_minus_conserved_fractional_H_bounds'][i],expected_H[i])
        check('gap_bound',row['scalar_fractional_energy_gap_bound_at_10keV'],source['D']/(source['Q']*Amin**2))
    for summary in p['summaries']:
        rr=[r for r in p['rows'] if r['R']==summary['R']];ok=[r for r in rr if r['proxy']['status']=='TABLE_PROXY']
        assert summary['rows']==len(rr)==72 and summary['table_supported']==len(ok)
        for i,f in enumerate([min,max]):check('Delta_range',summary['Delta_range'][i],f(r['late_Delta_coordinate'] for r in rr))
        if ok:
            for key in ['helium','deuterium']:
                for field,limits in summary['proxy_marginal_ranges'][key].items():
                    for i,f in enumerate([min,max]):check('proxy_summary',limits[i],f(r['proxy']['observables'][key][field] for r in ok))
    assert p['conserved_scalar_abundance_status']=='NOT_YET_QUALIFIED'
    supported_rows=[r for r in p['rows'] if r['proxy']['status']=='TABLE_PROXY']
    marginal_context={}
    for key in ['helium','deuterium']:
        marginal_context[key]={field:[f(b['observables'][key][field] for b in p['matched_Delta0'].values()) for f in [min,max]]
            for field in ['prediction','signed_residual','descriptive_marginal_standardized_residual']}
        marginal_context[key]['same_baryon_extra_component_effect']=[f(r['proxy']['minus_matched_Delta0'][key] for r in supported_rows) for f in [min,max]]
    thermal_ranges=[]
    for R in [32,128,512,2048,8192]:
        group=[r for r in p['rows'] if r['R']==R]
        thermal_ranges.append(dict(R=R,
            H_bounds=[min(r['thermal_proxy_minus_conserved_fractional_H_bounds'][0] for r in group),max(r['thermal_proxy_minus_conserved_fractional_H_bounds'][1] for r in group)],
            finite_gap_energy_bound_range=[f(r['scalar_fractional_energy_gap_bound_at_10keV'] for r in group) for f in [min,max]]))
    return dict(status='PASS' if not fail else 'FAIL',source_sha256=sha(Path(__file__)),result_sha256=sha(RESULT),
        freeze_sha256=sha(FREEZE),payload_sha256=json.loads(RESULT.read_text())['payload_sha256'],
        ancestry=dict(manifests=len(seen),unique_files=len(files),member_occurrences=occurrences,files=files),
        audit_checks=checks,max_scaled_error=maxerr,failures=fail,payload_serialization=payload_serialization,
        original_status=p['status'],original_checks=sum(p['counts'].values()),original_failures=p['failures'],
        supported_rows=supported,unsupported_rows=outside,thermal_interface=thermal,
        marginal_context=marginal_context,thermal_ranges=thermal_ranges,
        photon_A_10keV=A,thermal_history_A_10keV_lower_bound=Amin,
        summaries=p['summaries'],seconds=p['seconds'],peak_self_rss_bytes=p['peak_self_rss_bytes'],
        scope='Saved output arithmetic/custody only; no abundance interpolation, thermal bound integration, nuclear/oscillator ODE or production rerun. Shifted-T0 interpolation and underlying envelope construction remain source-reviewed, not independently reevaluated. All original qualifications retained.')

if __name__=='__main__':
    p=run();print(encode(dict(payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())
