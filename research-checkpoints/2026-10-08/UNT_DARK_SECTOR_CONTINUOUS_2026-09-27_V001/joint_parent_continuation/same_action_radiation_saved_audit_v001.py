"""Independent saved-action sums; no producer import, roots or dynamics."""
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run():
    path=HERE/'SAME_ACTION_RADIATION_V001_RESULTS.json'
    freeze=HERE/'SAME_ACTION_RADIATION_V001_FROZEN.json'
    assert sha(path)=='b01ba51bcfb8793fbaed3a3626e797a6b24b4d86c98bc15f9e6bef92a66a39f5'
    assert sha(freeze)=='def953b318cbfb18068eda55481067281e0ba1d8f237e338082826b8d02c76b3'
    result=json.loads(path.read_text());p=result['payload'];f=json.loads(freeze.read_text())
    assert result['status']=='COMPLETE' and not p['failures']
    assert result['freeze_sha256']==sha(freeze)
    assert result['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    for name,digest in f['files'].items():
        target=Path(name) if Path(name).is_absolute() else ROOT/name
        target.resolve().relative_to(ROOT.resolve())
        assert sha(target)==digest,name
    original=json.loads((HERE/'PREPARED_ACTION_RETURN_V001_RESULTS.json').read_text())['payload']
    hist=json.loads((HERE/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json').read_text())['payload']
    pulse=json.loads((HERE/'HIGH_GAP_PULSE_V001_RESULTS.json').read_text())['payload']
    dilution=json.loads((HERE/'HOMOGENEOUS_DILUTION_V001_RESULTS.json').read_text())['payload']
    calibration=json.loads((HERE/'ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json').read_text())['payload']
    closure=json.loads((HERE/'COSMOLOGY_CLOSURE_ARITHMETIC.json').read_text())
    assert p['reference_scope']==closure['scope'] and p['reference_assumptions']==closure['assumptions']
    assert p['references']==calibration['references']
    assert p['inherited_calibration_scope']==calibration['scope']
    assert p['inherited_calibration_qualifications']==calibration['qualifications']
    assert p['unchanged_original_baseline']==original['baseline']
    cases={(c['gap'],c['order'],c['dt'],c['duration']):c for c in hist['cases']}
    states=[]
    for i,r in enumerate(original['rows']):
        c=cases[(r['gap'],r['mode_order'],r['dt'],r['duration'])];m=r['mode_data']
        states.append(dict(family='original_soft',index=i,
            identity={k:r[k] for k in ('gap','mode_order','dt','duration','g')},
            delta=c['delta'],weight=c['weights'],I=m['action'],e=m['zero_source_energy'],
            pressure=m['zero_source_pressure'],Kb=c['Kb'],baseline=None,hard=None))
    for i,r in enumerate(pulse['cases']):
        m=r['fine_end_state'];s=r['finite_spectrum']
        states.append(dict(family='soft_plus_hard_pulse',index=i,
            identity={k:r[k] for k in ('gap','amplitude','cycles')},delta=m['delta'],weight=m['weights'],
            I=m['action'],e=m['energy'],pressure=m['pressure'],Kb=s['Kb'],baseline=s['DeltaU'],hard=128))
    assert len(states)==len(p['templates'])==42
    C=math.exp((4/3)*(math.log(1.5)+.5*math.log(math.pi)+math.lgamma(.75)-math.lgamma(.25)))
    count=0;maxima={}

    def check(label,a,b,scale=None,tol=2e-12):
        nonlocal count
        error=abs(a-b)/(max(abs(b),1e-300) if scale is None else scale)
        assert math.isfinite(error) and error<=tol,(label,error)
        maxima[label]=max(maxima.get(label,0.),error);count+=1

    check('Gamma_constant',p['Gamma_constant'],C)
    computed=[]
    for i,(s,r) in enumerate(zip(states,p['templates'])):
        assert r['template_index']==i and r['family']==s['family'] and r['input_index']==s['index']
        assert r['identity']==s['identity'] and r['unchanged_DeltaU']==s['baseline']
        q=[C*math.exp((4/3)*math.log(I)) if I else 0. for I in s['I']]
        qc=[w*v for w,v in zip(s['weight'],q)]
        dc=[w*d*d*math.sqrt(v) for w,d,v in zip(s['weight'],s['delta'],q)]
        Q=math.fsum(qc);D=math.fsum(dc)
        E=math.fsum(w*e for w,e in zip(s['weight'],s['e']))
        P=math.fsum(w*v for w,v in zip(s['weight'],s['pressure']))
        S4=math.fsum(w*d**4 for w,d in zip(s['weight'],s['delta']))
        for name,values in (('modal_q',q),('modal_Q_contribution',qc),('modal_D_contribution',dc)):
            assert len(r[name])==len(values)
            for a,b in zip(r[name],values):check(name,a,b)
        for name,v in dict(E1=E,P1=P,Q=Q,D=D,S4=S4,Kb=s['Kb'],Q_over_E1=Q/E).items():
            check(name,r[name],v)
        assert r['zero_action_modes']==[dict(mode=j,reason='ZERO_ACTION: q and D contribution retained as zero') for j,I in enumerate(s['I']) if I==0]
        assert r['ratio_reason'] is None and D*D<=Q*S4*(1+2e-12)
        for cert,eps in zip(r['asymptote_certificates'],(.01,.1)):
            assert cert['relative_energy_error']==eps and cert['reason'] is None
            check('sufficient_A',cert['sufficient_A'],max(1.,math.sqrt(D/(eps*Q))))
        for group in ('soft','hard'):
            js=[j for j in range(len(q)) if (j==s['hard'])==(group=='hard')]
            sums=dict(E1=math.fsum(s['weight'][j]*s['e'][j] for j in js),
                      Q=math.fsum(qc[j] for j in js),D=math.fsum(dc[j] for j in js))
            for name,v in sums.items():check('split_'+name,r['component_splits'][group][name],v)
        computed.append(dict(Q=Q,D=D,E=E,P=P))
    assert sum(len(r['modal_q']) for r in p['templates'])==4614
    factors=(1.,2.,4.,11.,101.,1101.)
    oldidx={(r['template_index'],r['inverse_scale_factor']):r for r in dilution['rows']}
    idx={(r['template_index'],r['inverse_scale_factor']):r for r in p['finite_gap_rows']}
    assert len(idx)==len(p['finite_gap_rows'])==252 and set(idx)==set(oldidx)=={(i,A) for i in range(42) for A in factors}
    for (i,A),r in idx.items():
        old=oldidx[(i,A)];s=computed[i];E=old['E'];P=old['P'];Q=s['Q'];D=s['D']
        assert r['E']==E and r['P']==P and r['inherited_clock_coefficients']==old['clock_coefficients']
        residuals=dict(energy_above_quartic=E-A**4*Q,energy_below_upper=A**4*Q+A*A*D-E,
                       nonnegative_quadratic_trace=E-3*P,quadratic_trace_below_upper=2*A*A*D-E+3*P)
        for name,v in residuals.items():
            check('residual_'+name,r['signed_residuals'][name],v,scale=max(E,A**4*Q+A*A*D))
            assert v>=-2e-8*max(E,A**4*Q+A*A*D)
        values=dict(E_over_A4=E/A**4,asymptotic_Q=Q,energy_error_upper=D/A**2,
                    relative_energy_error_upper=D/(A*A*Q),one_third_minus_w_upper=2*D/(3*A*A*Q),
                    E_over_E1_A4=E/(s['E']*A**4))
        for name,v in values.items():check(name,r[name],v)
        assert r['normalization_reason'] is None
    refs={r['reference']:r for r in calibration['references']}
    calidx={(r['template'],r['reference']):r for r in calibration['rows']}
    for name,n,ts,status in (('original_calibration_mappings',648,range(36),'INHERITED_ORIGINAL_CALIBRATION'),
                             ('conditional_extended_mappings',108,range(36,42),'CONDITIONAL_EXTENDED_REFERENCE_ONLY')):
        rows=p[name];assert len(rows)==n and {(r['template_index'],r['reference']) for r in rows}=={(i,j) for i in ts for j in range(18)}
        for r in rows:
            i,j=r['template_index'],r['reference'];s=computed[i];omega=refs[j]['Omega_exc']
            assert r['status']==status and r['reason'] is None and r['inverse_scale_factors']==list(factors)
            check('reference_Omega',r['Omega_exc_reference'],omega)
            check('asymptotic_density',r['Omega_extra_rad_asympt'],omega*s['Q']/s['E'])
            for A,finite,err in zip(factors,r['finite_A_Omega_coefficient'],r['finite_A_upper_errors']):
                check('finite_density',finite,omega*oldidx[(i,A)]['E']/(s['E']*A**4))
                check('finite_density_bound',err,omega*s['D']/(s['E']*A*A))
            if i<36:
                cr=calidx[(i,j)];assert r['inherited_calibration_status']==cr['status']=='POSITIVE_CALIBRATION'
                physical=2*cr['gstar_m_s2']**2*s['Q']/(3*states[i]['Kb']*(299792458.*refs[j]['H0_s_inverse'])**2)
                check('independent_gstar_density',r['Omega_asympt_from_frozen_gstar'],physical,tol=2e-11)
    summaries=[]
    for name,lo,hi in (('original_soft',0,36),('soft_plus_hard_pulse',36,42)):
        rows=p['templates'][lo:hi]
        mappings=p['original_calibration_mappings'] if lo==0 else p['conditional_extended_mappings']
        summaries.append(dict(family=name,template_count=len(rows),
            ranges={key:[min(r[key] for r in rows),max(r[key] for r in rows)] for key in ('E1','Q','D','Q_over_E1')},
            Omega_asympt_range=[min(r['Omega_extra_rad_asympt'] for r in mappings),max(r['Omega_extra_rad_asympt'] for r in mappings)],
            A_1percent_range=[min(r['asymptote_certificates'][0]['sufficient_A'] for r in rows),max(r['asymptote_certificates'][0]['sufficient_A'] for r in rows)]))
    representatives=[]
    for i in (6,36,37,38,39,40,41):
        r=p['templates'][i]
        representatives.append({k:v for k,v in r.items() if not k.startswith('modal_')})
    return dict(status='ACCEPTED_SAVED_ARITHMETIC',script_sha256=sha(Path(__file__)),
        result_sha256=sha(path),freeze_sha256=sha(freeze),payload_sha256=result['payload_sha256'],
        frozen_members=len(f['files']),producer_checks=sum(p['check_counts'].values()),
        independent_arithmetic_checks=count,maximum_relative_errors=maxima,
        census=dict(states=42,modes=4614,finite_A=252,original_mappings=648,conditional_mappings=108),
        Gamma_constant_independent=C,summary=summaries,representatives=representatives,
        producer_seconds=p['seconds'],producer_peak_self_RSS_bytes=p['peak_rss_bytes'],
        limits=['No new action roots, quadrature, propagation, state, fitting or observed-data inference.',
                'All radiation moments independently recombined from existing actual modal actions.',
                'Formal adiabatic/isotropic same-state scaling is not automatically qualified at arbitrarily early epochs.',
                'Ordinary photons and uncertainties are not inputs to this producer.'])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
