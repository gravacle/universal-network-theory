"""Same saved actions: exact radiation moment and finite-gap certificates."""
import sys
sys.dont_write_bytecode=True
import hashlib
import json
import math
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.resolve()
FREEZE=HERE/'SAME_ACTION_RADIATION_V001_FROZEN.json'
NOTE='SAME_ACTION_RADIATION_ASYMPTOTE_V001.md'
PINS={
    'PREPARED_ACTION_RETURN_V001_RESULTS.json':'b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678',
    'COMMON_HISTORY_MECHANISM_V001_RESULTS.json':'e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a',
    'HIGH_GAP_PULSE_V001_RESULTS.json':'3ff381351716259c36d3ef1cca01431e40a73c3deeabcf0bb24df27696617140',
    'HOMOGENEOUS_DILUTION_V001_RESULTS.json':'779ea9498572dc8bcbd3f9dc40b7610b097427dde9eb534dcb14345e1d8beb58',
    'ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json':'1b155c6caf7ceb721db2f8766fa282b456b8c5f40d49555052ab4b0dc9a06abd',
    'COSMOLOGY_CLOSURE_ARITHMETIC.json':'258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153',
    NOTE:'913160e3e485d3b6ddc64a66a47a0c06c40b6cd350bb8764df5629f848b49002'}
CONFIG=dict(inverse_scale_factors=[1.,2.,4.,11.,101.,1101.],certificate_errors=[.01,.1],
    algebra_tolerance=2e-12,inherited_orbit_tolerance=2e-8,
    inherited_calibration_tolerance=2e-11,output_target_bytes=2097152,
    synthetic_actions=[0.,1e-6,.1,1.,10.],synthetic_k=[1e-6,1.,16384.],
    synthetic_b=[.01,1.,10.],synthetic_fraction=[0.,.5,1.],c_m_s=299792458.)


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate():
    files,seen={},set()

    def add(path,expected=None):
        path=path.resolve(strict=True);path.relative_to(ROOT)
        value=sha(path)
        if expected is not None and value!=expected:
            raise RuntimeError('Input hash mismatch: '+str(path))
        files[str(path.relative_to(ROOT))]=value
        return path

    def resolve(name,parent):
        p=Path(name)
        if p.is_absolute():
            return add(p)
        candidates=set()
        for base in (parent,ROOT):
            candidate=(base/p).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                continue
            if candidate.is_file():
                candidates.add(candidate)
        if len(candidates)!=1:
            raise RuntimeError('Missing or ambiguous frozen input: '+name)
        return candidates.pop()

    def manifest(path):
        path=add(path)
        if path in seen:
            return
        seen.add(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            child=add(resolve(name,path.parent),digest)
            if child.name.endswith('_FROZEN.json'):
                manifest(child)

    def wrapper(name):
        path=add(HERE/name,PINS[name]);value=json.loads(path.read_text())
        freeze=path.with_name(name.replace('_RESULTS.json','_FROZEN.json'))
        manifest(freeze)
        if (value['freeze_sha256']!=sha(freeze) or value['payload_sha256']!=
                hashlib.sha256(encode(value['payload'])).hexdigest()):
            raise RuntimeError('Result custody mismatch: '+name)
        p=value['payload']
        if value.get('status','COMPLETE')!='COMPLETE' or p.get('status','COMPLETE')!='COMPLETE':
            raise RuntimeError('Unqualified result status: '+name)
        checks=p.get('checks')
        if isinstance(checks,list):
            valid=all(c['passed'] for c in checks)
        elif isinstance(checks,dict) and 'failed' in checks:
            valid=checks['failed']==0 and not checks['failure_names']
        elif isinstance(checks,dict):
            valid=all(isinstance(v,bool) and v for v in checks.values())
        else:
            valid='failures' in p and not p['failures']
        if not valid:
            raise RuntimeError('Unqualified numerical controls: '+name)
        return p

    returned=wrapper('PREPARED_ACTION_RETURN_V001_RESULTS.json')
    history=wrapper('COMMON_HISTORY_MECHANISM_V001_RESULTS.json')
    pulse=wrapper('HIGH_GAP_PULSE_V001_RESULTS.json')
    dilution=wrapper('HOMOGENEOUS_DILUTION_V001_RESULTS.json')
    calibration=wrapper('ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json')
    closure=json.loads(add(HERE/'COSMOLOGY_CLOSURE_ARITHMETIC.json',PINS['COSMOLOGY_CLOSURE_ARITHMETIC.json']).read_text())
    if closure['status']!='AUTHENTICATED_REFERENCE_CLOSURE_DIAGNOSTIC':
        raise RuntimeError('Unexpected historical closure identity')
    add(HERE/'cosmology_closure_arithmetic.py',closure['script_sha256'])
    for name,digest in closure['input_sha256'].items():
        path=add(HERE.parent/name,digest)
        if path.name.endswith('_FROZEN.json'):
            manifest(path)
    for name in (Path(__file__).name,'SAME_ACTION_RADIATION_PROTOCOL_V001.md',NOTE):
        add(HERE/name,PINS.get(name))
    expected={(gap,n,dt,t,g) for gap in (.001,.002) for n,dt in ((64,.01),(128,.01),(128,.005))
              for t in (8,16) for g in (.0025,.01,.04)}
    actual=[(r['gap'],r['mode_order'],r['dt'],r['duration'],r['g']) for r in returned['rows']]
    if len(actual)!=36 or set(actual)!=expected:
        raise RuntimeError('Original state census differs')
    lookup={(c['gap'],c['order'],c['dt'],c['duration']):c for c in history['cases']}
    templates=[]
    for i,row in enumerate(returned['rows']):
        h=lookup[actual[i][:4]];md=row['mode_data']
        templates.append(dict(family='original_soft',input_index=i,
            identity={k:row[k] for k in ('gap','mode_order','dt','duration','g')},
            delta=h['delta'],weights=h['weights'],action=md['action'],energy=md['zero_source_energy'],
            pressure=md['zero_source_pressure'],saved_E1=row['return_energy'],Kb=h['Kb'],
            saved_P1=row['return_pressure'],DeltaU=None,hard_index=None))
    pc=pulse['cases']
    if len(pc)!=6 or {(r['gap'],r['amplitude']) for r in pc}!={(g,a) for g in (32.,64.,128.) for a in (1.,4.)}:
        raise RuntimeError('Pulse state census differs')
    for i,row in enumerate(pc):
        md=row['fine_end_state']
        if len(md['delta'])!=129:
            raise RuntimeError('Pulse fine mode count differs')
        templates.append(dict(family='soft_plus_hard_pulse',input_index=i,
            identity={k:row[k] for k in ('gap','amplitude','cycles')},
            delta=md['delta'],weights=md['weights'],action=md['action'],energy=md['energy'],
            pressure=md['pressure'],saved_E1=row['controls'][2]['total_energy'],
            saved_P1=row['orbit_averaged']['total_pressure'],Kb=row['finite_spectrum']['Kb'],
            DeltaU=row['finite_spectrum']['DeltaU'],hard_index=128))
    for t in templates:
        n=len(t['delta'])
        if not all(len(t[k])==n for k in ('weights','action','energy','pressure')):
            raise RuntimeError('Modal input lengths differ')
        if not all(math.isfinite(x) and x>0 for k in ('delta','weights') for x in t[k]):
            raise RuntimeError('Invalid spectrum')
        if not all(math.isfinite(x) and x>=0 for k in ('action','energy') for x in t[k]):
            raise RuntimeError('Invalid action or energy')
    dr=dilution['rows']
    if len(dr)!=252 or {(r['template_index'],r['inverse_scale_factor']) for r in dr}!={(i,A) for i in range(42) for A in CONFIG['inverse_scale_factors']}:
        raise RuntimeError('Dilution census differs')
    for r in dr:
        t=templates[r['template_index']]
        if (r['family']!=t['family'] or r['input_index']!=t['input_index'] or r['identity']!=t['identity']):
            raise RuntimeError('Dilution state identity differs')
    refs=calibration['references'];cr=calibration['rows'];ct=calibration['templates']
    if (len(refs)!=18 or {r['reference'] for r in refs}!=set(range(18)) or len(cr)!=648
            or {(r['template'],r['reference']) for r in cr}!={(i,j) for i in range(36) for j in range(18)}
            or len(ct)!=36 or {r['template'] for r in ct}!=set(range(36))):
        raise RuntimeError('Calibration census differs')
    for c in ct:
        t=templates[c['template']]
        if (c['actions_sha256']!=hashlib.sha256(encode(t['action'])).hexdigest()
                or c['spectrum_sha256']!=hashlib.sha256(encode(dict(delta=t['delta'],weights=t['weights']))).hexdigest()):
            raise RuntimeError('Calibrated state/spectrum differs')
    snapshot=dict(configuration=CONFIG,files=files,reference_scope=closure['scope'],
                  reference_assumptions=closure['assumptions'])
    return templates,dilution,calibration,closure,returned['baseline'],snapshot


def run():
    start=time.perf_counter()
    templates,dilution,calibration,closure,baseline,snapshot=authenticate()
    if json.loads(FREEZE.read_text())!=snapshot:
        raise RuntimeError('Prospective freeze differs')
    maxima,counts,failures={},{},[]

    def check(name,left,right=0.,scale=1.,upper=False,tolerance=None,tag=''):
        tol=CONFIG['algebra_tolerance'] if tolerance is None else tolerance
        difference=left-right
        error=(max(0.,difference) if upper else abs(difference))/(scale if scale else 1.)
        maxima[name]=max(maxima.get(name,0.),error);counts[name]=counts.get(name,0)+1
        if not math.isfinite(error) or error>tol:
            failures.append(dict(check=name,tag=tag,normalized_error=error,tolerance=tol))

    beta=math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)
    C=(math.pi/beta)**(4/3)
    other=(1.5*math.sqrt(math.pi)*math.gamma(.75)/math.gamma(.25))**(4/3)
    check('dual_Gamma_constant',C,other,C)
    for I in CONFIG['synthetic_actions']:
        for A in CONFIG['inverse_scale_factors']:
            q=C*I**(4/3)
            check('synthetic_quartic_scaling',C*(A**3*I)**(4/3),A**4*q,A**4*q)
    for k in CONFIG['synthetic_k']:
        for b in CONFIG['synthetic_b']:
            for fraction in CONFIG['synthetic_fraction']:
                y=b*fraction;e0=b**4/4;trial=e0+k*b*b/2
                lhs=(trial-k*y*y/2-y**4/4)-(e0-y**4/4)
                rhs=k*(b*b-y*y)/2
                check('synthetic_trial_radicand',lhs,rhs,max(1.,trial))
                check('synthetic_trial_nonnegative',0.,rhs,max(1.,trial),True)
    rows=[]
    for index,t in enumerate(templates):
        q=[C*I**(4/3) for I in t['action']]
        qc=[w*z for w,z in zip(t['weights'],q)]
        dc=[w*d*d*math.sqrt(z) for w,d,z in zip(t['weights'],t['delta'],q)]
        Q=math.fsum(qc);D=math.fsum(dc)
        E1=math.fsum(w*e for w,e in zip(t['weights'],t['energy']))
        P1=math.fsum(w*p for w,p in zip(t['weights'],t['pressure']))
        S4=math.fsum(w*d**4 for w,d in zip(t['weights'],t['delta']))
        zero=[]
        for j,(I,e,w,z,dpart) in enumerate(zip(t['action'],t['energy'],t['weights'],q,dc)):
            tag=f'{index}:{j}'
            if I==0:
                zero.append(dict(mode=j,reason='ZERO_ACTION: q and D contribution retained as zero'))
                check('zero_action_energy',e,0.,max(E1,1.),tolerance=CONFIG['inherited_orbit_tolerance'],tag=tag)
            dj=dpart/w
            check('present_modal_lower',z,e,max(e,z),True,CONFIG['inherited_orbit_tolerance'],tag)
            check('present_modal_upper',e,z+dj,max(e,z+dj),True,CONFIG['inherited_orbit_tolerance'],tag)
        check('saved_present_energy',E1,t['saved_E1'],max(E1,t['saved_E1']),tag=str(index))
        check('saved_present_pressure',P1,t['saved_P1'],max(E1,1e-300),tolerance=CONFIG['inherited_orbit_tolerance'],tag=str(index))
        check('Cauchy_moment_bound',D*D,S4*Q,max(D*D,S4*Q),True,tag=str(index))
        positive=E1>0 and Q>0
        cert=[dict(relative_energy_error=eps,sufficient_A=max(1.,math.sqrt(D/(eps*Q))) if positive else None,
                   reason=None if positive else 'ZERO_EXCITATION: relative asymptote undefined')
              for eps in CONFIG['certificate_errors']]
        hi=t['hard_index'];indices=range(len(q))
        splits={}
        for name,selected in (('soft',[j for j in indices if j!=hi]),('hard',[] if hi is None else [hi])):
            splits[name]=dict(E1=math.fsum(t['weights'][j]*t['energy'][j] for j in selected),
                Q=math.fsum(qc[j] for j in selected),D=math.fsum(dc[j] for j in selected))
        rows.append(dict(template_index=index,family=t['family'],input_index=t['input_index'],identity=t['identity'],
            E1=E1,P1=P1,Kb=t['Kb'],unchanged_DeltaU=t['DeltaU'],Q=Q,D=D,S4=S4,
            Q_over_E1=Q/E1 if positive else None,
            ratio_reason=None if positive else 'ZERO_EXCITATION: cannot normalize a positive present excitation',
            modal_q=q,modal_Q_contribution=qc,modal_D_contribution=dc,zero_action_modes=zero,
            component_splits=splits,asymptote_certificates=cert))
    finite=[];by_template={i:[] for i in range(42)}
    for old in dilution['rows']:
        i=old['template_index'];r=rows[i];A=old['inverse_scale_factor'];E=old['E'];P=old['P']
        leading=A**4*r['Q'];upper=leading+A*A*r['D'];gap=E-3*P;gapupper=2*A*A*r['D']
        residuals=dict(energy_above_quartic=E-leading,energy_below_upper=upper-E,
                       nonnegative_quadratic_trace=gap,quadratic_trace_below_upper=gapupper-gap)
        for name,value in residuals.items():
            check('finite_gap:'+name,0.,value,max(E,upper),True,
                  CONFIG['inherited_orbit_tolerance'],f'{i}:{A}')
        positive=r['Q']>0 and r['E1']>0
        out=dict(template_index=i,inverse_scale_factor=A,E=E,P=P,signed_residuals=residuals,
            E_over_A4=E/A**4,asymptotic_Q=r['Q'],energy_error_upper=r['D']/A**2,
            relative_energy_error_upper=r['D']/(A*A*r['Q']) if positive else None,
            one_third_minus_w_upper=2*r['D']/(3*A*A*r['Q']) if positive else None,
            E_over_E1_A4=E/(r['E1']*A**4) if positive else None,
            normalization_reason=None if positive else 'ZERO_EXCITATION',
            inherited_clock_coefficients=old['clock_coefficients'])
        finite.append(out);by_template[i].append(out)
    for values in by_template.values():
        values.sort(key=lambda r:r['inverse_scale_factor'])
    refs={r['reference']:r for r in calibration['references']}
    original=[];extended=[]

    def mapping(index,reference,status):
        state=rows[index];ref=refs[reference];omega=ref['Omega_exc']
        valid=state['E1']>0 and state['Q']>0 and omega>0
        result=dict(template_index=index,reference=reference,status=status if valid else 'NONPOSITIVE_NORMALIZATION_DOMAIN',
            Omega_exc_reference=omega,Omega_extra_rad_asympt=omega*state['Q']/state['E1'] if valid else None,
            inverse_scale_factors=CONFIG['inverse_scale_factors'],
            finite_A_Omega_coefficient=[omega*f['E_over_E1_A4'] for f in by_template[index]] if valid else None,
            finite_A_upper_errors=[omega*state['D']/(state['E1']*A*A) for A in CONFIG['inverse_scale_factors']] if valid else None,
            reason=None if valid else 'Zero template excitation or nonpositive inherited reference; no ratio fabricated')
        return result

    for old in calibration['rows']:
        i=old['template'];j=old['reference'];state=rows[i];ref=refs[j]
        result=mapping(i,j,'INHERITED_ORIGINAL_CALIBRATION')
        result['inherited_calibration_status']=old['status']
        if old['status']=='POSITIVE_CALIBRATION' and state['E1']>0:
            factor=2*old['gstar_m_s2']**2/(3*state['Kb']*(CONFIG['c_m_s']*ref['H0_s_inverse'])**2)
            check('calibration_present_density',factor*state['E1'],ref['Omega_exc'],ref['Omega_exc'],
                  tolerance=CONFIG['inherited_calibration_tolerance'],tag=f'{i}:{j}')
            reconstructed=factor*state['Q']
            check('calibration_radiation_normalization',reconstructed,result['Omega_extra_rad_asympt'],
                  result['Omega_extra_rad_asympt'],tolerance=CONFIG['inherited_calibration_tolerance'],tag=f'{i}:{j}')
            result['Omega_asympt_from_frozen_gstar']=reconstructed
        else:
            result['Omega_asympt_from_frozen_gstar']=None
            result['status']='INHERITED_CALIBRATION_DOMAIN_UNAVAILABLE'
        original.append(result)
    for i in range(36,42):
        for j in range(18):
            extended.append(mapping(i,j,'CONDITIONAL_EXTENDED_REFERENCE_ONLY'))
    for name,actual,expected in (('templates',len(rows),42),('modal_entries',sum(len(r['modal_q']) for r in rows),4614),
                                 ('finite_gap_rows',len(finite),252),('original_mappings',len(original),648),
                                 ('conditional_extended_mappings',len(extended),108)):
        check('census:'+name,actual,expected)
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':
        peak*=1024
    payload=dict(configuration=CONFIG,Gamma_constant=C,beta_function=beta,templates=rows,
        finite_gap_rows=finite,original_calibration_mappings=original,conditional_extended_mappings=extended,
        references=calibration['references'],reference_scope=closure['scope'],reference_assumptions=closure['assumptions'],
        inherited_calibration_scope=calibration['scope'],inherited_calibration_qualifications=calibration['qualifications'],
        unchanged_original_baseline=baseline,maximum_errors=maxima,check_counts=counts,failures=failures,
        scope='Conditional same-action adiabatic isotropic/triad radiation coefficient; no photon/neutrino inputs, new state, fit, physical clock, or observed-redshift proof.',
        seconds=time.perf_counter()-start,peak_rss_bytes=int(peak))
    payload['bytes_before_size_fields']=len(encode(payload))
    payload['output_target_exceeded']=payload['bytes_before_size_fields']>CONFIG['output_target_bytes']
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS',freeze_sha256=sha(FREEZE),
                payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)


def main():
    if sys.argv[1:]==['freeze']:
        output=authenticate()[-1]
    elif sys.argv[1:]==['run']:
        output=run()
    else:
        raise ValueError('usage: same_action_radiation_v001.py freeze|run')
    print(encode(output).decode())


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status='ERROR',error_type=type(exc).__name__,error=str(exc))))
        sys.exit(1)
