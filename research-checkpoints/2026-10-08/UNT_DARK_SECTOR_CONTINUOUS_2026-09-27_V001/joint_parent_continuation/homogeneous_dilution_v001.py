"""Same saved actions under homogeneous dilution; stdout-only freeze/run."""
import os
import sys
sys.dont_write_bytecode = True
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import prepared_susceptibility_v001 as saved

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE/'HOMOGENEOUS_DILUTION_V001_FROZEN.json'
PULSE = HERE/'HIGH_GAP_PULSE_V001_RESULTS.json'
PULSE_SHA = '3ff381351716259c36d3ef1cca01431e40a73c3deeabcf0bb24df27696617140'
PULSE_FREEZE_SHA = '1f78119c2b20516e7fa6de9586acd8e58817d489c029f8564982ab4aeb639435'
CONFIG = dict(inverse_scale_factors=[1.,2.,4.,11.,101.,1101.],orders=[64,128],
    bisections=72,orbit_tolerance=2e-8,algebra_tolerance=2e-12,
    derivative_tolerance=2e-7,difference_steps=[1e-3,5e-4],
    synthetic_delta=[.1,1.,128.],synthetic_b=[0.,.01,1.,100.],
    output_target_bytes=2097152)


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    returned,history,ancestor = saved.inputs()
    files,seen = dict(ancestor['files']),set()

    def add(path,expected=None):
        path=path.resolve(strict=True)
        path.relative_to(ROOT)
        digest=sha(path)
        if expected is not None and digest != expected:
            raise RuntimeError('Input hash differs: '+str(path))
        files[str(path.relative_to(ROOT))]=digest
        return path

    def manifest(path):
        path=add(path)
        if path in seen:
            return
        seen.add(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            member=Path(name)
            if member.is_absolute():
                child=add(member,digest)
            else:
                # The pulse freeze uses workspace-relative paths; older ones
                # use absolute or manifest-relative paths. Reject ambiguity.
                candidates=set()
                for base in (path.parent,ROOT):
                    candidate=(base/member).resolve()
                    candidate.relative_to(ROOT)
                    if candidate.is_file():
                        candidates.add(candidate)
                if len(candidates)!=1:
                    raise RuntimeError('Missing/ambiguous frozen member: '+name)
                child=add(candidates.pop(),digest)
            if child.name.endswith('_FROZEN.json'):
                manifest(child)

    add(PULSE,PULSE_SHA)
    pf=add(HERE/'HIGH_GAP_PULSE_V001_FROZEN.json',PULSE_FREEZE_SHA)
    manifest(pf)
    pulse=json.loads(PULSE.read_text())
    if (pulse['status']!='COMPLETE' or pulse['freeze_sha256']!=sha(pf)
            or pulse['payload_sha256']!=hashlib.sha256(encode(pulse['payload'])).hexdigest()
            or not all(c['passed'] for c in pulse['payload']['checks'])):
        raise RuntimeError('Pulse result is not authenticated and qualified')
    for name in ('homogeneous_dilution_v001.py','HOMOGENEOUS_DILUTION_PROTOCOL_V001.md',
                 'FIXED_ACTION_MODE_INTERFACE_V001.md','prepared_action_return_v001.py',
                 'prepared_compression_v001.py','high_gap_pulse_v001.py'):
        add(HERE/name)
    lookup={(c['gap'],c['order'],c['dt'],c['duration']):c for c in history['cases']}
    templates=[]
    for index,row in enumerate(returned['rows']):
        old=lookup[(row['gap'],row['mode_order'],row['dt'],row['duration'])]
        md=row['mode_data']
        templates.append(dict(family='original_soft',input_index=index,
            identity={k:row[k] for k in ('gap','mode_order','dt','duration','g')},
            delta=old['delta'],weights=old['weights'],action=md['action'],
            saved_energy=md['zero_source_energy'],saved_pressure=md['zero_source_pressure'],
            saved_frequency=[2*math.pi/t for t in md['zero_source_period']],
            Kb=old['Kb'],DeltaU=None))
    cases=pulse['payload']['cases']
    if len(cases)!=6 or {(c['gap'],c['amplitude']) for c in cases}!={(r,a) for r in (32.,64.,128.) for a in (1.,4.)}:
        raise RuntimeError('Pulse census differs')
    for index,row in enumerate(cases):
        md=row['fine_end_state']
        if len(md['delta'])!=129:
            raise RuntimeError('Pulse fine spectrum differs')
        templates.append(dict(family='soft_plus_hard_pulse',input_index=index,
            identity={k:row[k] for k in ('gap','amplitude','cycles')},
            delta=md['delta'],weights=md['weights'],action=md['action'],
            saved_energy=md['energy'],saved_pressure=md['pressure'],
            saved_frequency=md['frequency'],Kb=row['finite_spectrum']['Kb'],
            DeltaU=row['finite_spectrum']['DeltaU']))
    for t in templates:
        count=len(t['delta'])
        if not all(len(t[k])==count for k in ('weights','action','saved_energy','saved_pressure','saved_frequency')):
            raise RuntimeError('Modal array length differs')
        for key in ('delta','weights','action','saved_energy','saved_frequency'):
            if not all(math.isfinite(x) and x>0 for x in t[key]):
                raise RuntimeError('Nonpositive/nonfinite saved mode '+key)
    return templates,dict(configuration=CONFIG,files=files,
        old_baseline=returned['baseline'],pulse_payload_sha256=pulse['payload_sha256'])


def rule(order):
    x,w=leggauss(order)
    theta=(x+1)*math.pi/4
    return w*math.pi/4,np.sin(theta)**2,np.cos(theta)**2


def at_amplitude(delta,b,quadrature,u=1.):
    weight,sine,cosine=quadrature
    q=delta[:,None]**2+u*b[:,None]**2*(1+sine)/2
    measure=weight/np.sqrt(q)
    j=np.sum(measure,axis=1)
    action=2/math.pi*b*b*np.sum(weight*cosine*np.sqrt(q),axis=1)
    omega=math.pi/(2*j)
    mean2=b*b*np.sum(measure*sine,axis=1)/j
    pressure=u*b**4/4*np.sum(measure*sine*sine,axis=1)/j
    energy=delta*delta*b*b/2+u*b**4/4
    curvature=omega*omega*u*np.sum(weight*(1+sine)/q**1.5,axis=1)/(2*j*(delta*delta+u*b*b))
    return dict(b=b,action=action,energy=energy,pressure=pressure,omega=omega,
                mean2=mean2,curvature=curvature,zeta=action*curvature/omega)


def action_at(delta,b,quadrature):
    weight,sine,cosine=quadrature
    q=delta[:,None]**2+b[:,None]**2*(1+sine)/2
    return 2/math.pi*b*b*np.sum(weight*cosine*np.sqrt(q),axis=1)


def inverse(delta,target,quadrature):
    lo=np.zeros_like(delta)
    hi=np.minimum(np.sqrt(2*target/delta),np.cbrt(2*math.sqrt(2)*target))
    bracket=action_at(delta,hi,quadrature)
    for _ in range(CONFIG['bisections']):
        mid=(lo+hi)/2
        below=action_at(delta,mid,quadrature)<target
        lo=np.where(below,mid,lo)
        hi=np.where(below,hi,mid)
    result=at_amplitude(delta,(lo+hi)/2,quadrature)
    result['bracket_action']=bracket
    return result


def run():
    start=time.perf_counter()
    templates,snapshot=inputs()
    if json.loads(FREEZE.read_text())!=snapshot:
        raise RuntimeError('Prospective freeze differs')
    rules={q:rule(q) for q in CONFIG['orders']}
    maxima,counts,failures={},{},[]

    def check(name,left,right=0.,scale=1.,upper=False,tolerance=None,tag=''):
        tolerance=CONFIG['orbit_tolerance'] if tolerance is None else tolerance
        difference=np.asarray(left)-np.asarray(right)
        error=float(np.max((np.maximum(difference,0) if upper else np.abs(difference))/np.asarray(scale)))
        maxima[name]=max(maxima.get(name,0.),error)
        counts[name]=counts.get(name,0)+int(np.size(difference))
        if not math.isfinite(error) or error>tolerance:
            failures.append(dict(check=name,tag=tag,error=error,tolerance=tolerance))

    for d in CONFIG['synthetic_delta']:
        for b in CONFIG['synthetic_b']:
            delta=np.array([d]);amp=np.array([b])
            known=at_amplitude(delta,amp,rules[128])
            solved=inverse(delta,known['action'],rules[128])
            check('synthetic_inverse',solved['b'],amp,max(b,1.),tolerance=2e-12,tag=f'{d}:{b}')
    beta=math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)
    for A in CONFIG['inverse_scale_factors']:
        harmonic=at_amplitude(np.array([.7]),np.array([.3*A**1.5]),rules[128],u=0.)
        quartic=at_amplitude(np.array([0.]),np.array([.3*A]),rules[128])
        check('synthetic_harmonic_energy',harmonic['energy'],.5*.7**2*.3**2*A**3,
              float(harmonic['energy'][0]),tolerance=2e-12)
        check('synthetic_harmonic_pressure',harmonic['pressure'],0.,tolerance=2e-12)
        check('synthetic_harmonic_frequency',harmonic['omega'],.7,tolerance=2e-12)
        expected_action=math.sqrt(2)/(4*math.pi)*beta*(.3*A)**3
        check('synthetic_quartic_action',quartic['action'],expected_action,expected_action,tolerance=2e-12)
        check('synthetic_quartic_pressure',quartic['pressure'],quartic['energy']/3,
              quartic['energy'],tolerance=2e-12)
        check('synthetic_quartic_enthalpy',quartic['action']*quartic['omega'],4*quartic['energy']/3,
              quartic['energy'],tolerance=2e-12)
    rows=[]
    for ti,t in enumerate(templates):
        delta=np.asarray(t['delta']);weights=np.asarray(t['weights']);initial=np.asarray(t['action'])
        saved_e=np.asarray(t['saved_energy']);saved_p=np.asarray(t['saved_pressure'])
        saved_omega=np.asarray(t['saved_frequency']);E1=float(weights@saved_e)
        check('contact_weight',float(np.sum(weights)),t['Kb'],t['Kb'],tolerance=2e-12,tag=str(ti))
        for A in CONFIG['inverse_scale_factors']:
            tag=f'{ti}:{A}'
            target=initial*A**3
            low,high=[inverse(delta,target,rules[q]) for q in CONFIG['orders']]
            e,p,omega=high['energy'],high['pressure'],high['omega']
            for order,out in ((64,low),(128,high)):
                label=f'{tag}:q{order}'
                check('target_action',out['action'],target,target,tag=label)
                check('upper_bracket',target,out['bracket_action'],target,True,tag=label)
                check('virial_energy',delta**2*out['mean2']+3*out['pressure'],out['energy'],out['energy'],tag=label)
                check('action_enthalpy',out['action']*out['omega'],out['energy']+out['pressure'],out['energy'],tag=label)
                check('pressure_nonnegative',0.,out['pressure'],out['energy'],True,tag=label)
                check('pressure_upper',out['pressure'],out['energy']/3,out['energy'],True,tag=label)
                check('zeta_nonnegative',0.,out['zeta'],upper=True,tag=label)
                check('zeta_upper',out['zeta'],1/3,upper=True,tag=label)
            check('quadrature_energy',low['energy'],e,e,tag=tag)
            check('quadrature_pressure',low['pressure'],p,e,tag=tag)
            check('quadrature_frequency',low['omega'],omega,omega,tag=tag)
            if A==1:
                check('saved_energy',e,saved_e,saved_e,tag=tag)
                check('saved_pressure',p,saved_p,saved_e,tag=tag)
                check('saved_frequency',omega,saved_omega,saved_omega,tag=tag)
            E=float(weights@e);P=float(weights@p);W=E+P
            check('dust_energy_lower',E1*A**3,E,E,True,tag=tag)
            check('radiation_energy_upper',E,E1*A**4,E,True,tag=tag)
            derivatives=[]
            for eps in CONFIG['difference_steps']:
                plus=inverse(delta,target*math.exp(3*eps),rules[128])['energy']
                minus=inverse(delta,target*math.exp(-3*eps),rules[128])['energy']
                derivatives.append((plus-minus)/(2*eps))
            deriv=(4*derivatives[1]-derivatives[0])/3
            check('continuity_derivative',deriv,3*(e+p),3*(e+p),
                  tolerance=CONFIG['derivative_tolerance'],tag=tag)
            aggregate_curvature=float(weights@(target*target*high['curvature']))
            rows.append(dict(template_index=ti,family=t['family'],input_index=t['input_index'],
                identity=t['identity'],inverse_scale_factor=A,Kb=t['Kb'],unchanged_DeltaU=t['DeltaU'],
                E=E,P=P,P_over_E=P/E,E_over_present_dust=E/(E1*A**3),
                common_compression_coefficient=aggregate_curvature/W,
                modal_frequency=omega.tolist(),minimum_frequency=float(np.min(omega)),
                maximum_frequency=float(np.max(omega)),
                clock_coefficients=dict(H_over_omega=float(np.max(1/omega)),
                    fractional_action_change_per_period=float(np.max(6*math.pi/omega)),
                    frequency_adiabaticity=float(np.max(3*high['zeta']/omega))),
                quadrature_max_relative_energy=float(np.max(abs(low['energy']/e-1))),
                quadrature_max_energy_scaled_pressure=float(np.max(abs(low['pressure']-p)/e)),
                quadrature_max_relative_frequency=float(np.max(abs(low['omega']/omega-1)))))
    indexed={(r['identity']['gap'],r['identity'].get('duration'),r['identity'].get('g'),
              r['identity'].get('mode_order'),r['identity'].get('dt'),r['inverse_scale_factor']):r
             for r in rows if r['family']=='original_soft'}
    comparisons=[]
    for gap in (.001,.002):
        for duration in (8,16):
            for g in (.0025,.01,.04):
                for A in CONFIG['inverse_scale_factors']:
                    for left,right,name in (((64,.01),(128,.01),'old_spectral_order'),
                                            ((128,.01),(128,.005),'old_time_step')):
                        x=indexed[(gap,duration,g,*left,A)];y=indexed[(gap,duration,g,*right,A)]
                        comparisons.append(dict(gap=gap,duration=duration,g=g,inverse_scale_factor=A,
                            label=name,signed_right_minus_left={k:y[k]-x[k] for k in ('E','P','P_over_E','E_over_present_dust')},
                            energy_relative_to_right=(y['E']-x['E'])/y['E']))
    check('row_census',len(rows),252,tolerance=2e-12)
    check('comparison_census',len(comparisons),144,tolerance=2e-12)
    check('modal_frequency_census',sum(len(r['modal_frequency']) for r in rows),27684,tolerance=2e-12)
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':
        peak*=1024
    payload=dict(configuration=CONFIG,rows=rows,resolution_comparisons=comparisons,
        check_counts=counts,maximum_errors=maxima,failures=failures,
        excitation_only=True,unchanged_original_baseline=snapshot['old_baseline'],
        scope='Conditional isotropic/triad homogeneous orbit readout; no preparation, physical clock, H(a), observed-redshift mapping, fit, or metric evolution.',
        seconds=time.perf_counter()-start,peak_rss_bytes=int(peak))
    payload['output_target_exceeded']=len(encode(payload))>CONFIG['output_target_bytes']
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS',freeze_sha256=sha(FREEZE),
                payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)


def main():
    if sys.argv[1:]==['freeze']:
        output=inputs()[1]
    elif sys.argv[1:]==['run']:
        output=run()
    else:
        raise ValueError('usage: homogeneous_dilution_v001.py freeze|run')
    print(encode(output).decode())


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status='ERROR',error_type=type(exc).__name__,error=str(exc))))
        sys.exit(1)
