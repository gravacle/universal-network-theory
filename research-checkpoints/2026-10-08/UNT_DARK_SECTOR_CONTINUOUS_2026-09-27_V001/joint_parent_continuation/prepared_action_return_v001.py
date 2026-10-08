"""Same prepared actions determine zero-source energy and pressure; no fit."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import disk_solver as law

ROOT=Path(__file__).resolve().parent
PHASE=ROOT/'COMMON_HISTORY_PHASE_MEAN_V003_RESULTS.json'
STATES=ROOT/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'
FREEZE=ROOT/'PREPARED_ACTION_RETURN_V001_FROZEN.json'
OUTPUT=ROOT/'PREPARED_ACTION_RETURN_V001_RESULTS.json'


def solve_actions(delta, lower, upper, order):
    x,w=leggauss(order)
    theta=(x+1)*math.pi/2
    center=(lower+upper)/2
    radius=(upper-lower)/2
    y=center[:,None]+radius[:,None]*np.cos(theta)
    q=y*y+(lower+upper)[:,None]*y+(2*delta*delta+lower*lower+lower*upper+upper*upper)[:,None]
    action=radius**2/(math.sqrt(2)*math.pi)*np.sum(w*math.pi/2*np.sin(theta)**2*np.sqrt(q),axis=-1)
    assert np.all(action>=0)
    angle=(x+1)*math.pi/4
    weight=w*math.pi/4
    sn2=np.sin(angle)**2
    cs2=np.cos(angle)**2

    def zero_action(b):
        stiff=delta[:,None]**2+b[:,None]**2*(1+sn2)/2
        return 2/math.pi*b*b*np.sum(weight*cs2*np.sqrt(stiff),axis=-1)

    lo=np.zeros_like(delta)
    hi=np.sqrt(2*action/delta)
    assert np.all(zero_action(hi)>=action*(1-1e-13))
    for _ in range(75):
        mid=(lo+hi)/2
        below=zero_action(mid)<action
        lo=np.where(below,mid,lo)
        hi=np.where(below,hi,mid)
    b=(lo+hi)/2
    stiff=delta[:,None]**2+b[:,None]**2*(1+sn2)/2
    measure=weight/np.sqrt(stiff)
    norm=np.sum(measure,axis=-1)
    period=4*norm
    energy=delta*delta*b*b/2+b**4/4
    pressure=action*(2*math.pi/period)-energy
    quartic_mean=b**4/4*np.sum(measure*sn2**2,axis=-1)/norm
    positive=action>0
    action_error=float(np.max(abs(zero_action(b)[positive]/action[positive]-1))) if np.any(positive) else 0.
    active=energy>0
    virial_error=float(np.max(abs(pressure[active]-quartic_mean[active])/energy[active])) if np.any(active) else 0.
    ratio=np.divide(pressure,energy,out=np.zeros_like(energy),where=active)
    return {'action':action.tolist(),'zero_source_turning_amplitude':b.tolist(),
        'zero_source_energy':energy.tolist(),'zero_source_pressure':pressure.tolist(),
        'zero_source_period':period.tolist(),'quartic_mean':quartic_mean.tolist(),
        'action_relative_error':action_error,'pressure_virial_scaled_error':virial_error,
        'min_modal_pressure_ratio':float(np.min(ratio)),'max_modal_pressure_ratio':float(np.max(ratio)),
        'checks':{'action_conserved':action_error<=2e-8,'pressure_virial':virial_error<=2e-8,
            'pressure_range':bool(np.all(ratio>=-2e-8) and np.all(ratio<=1/3+2e-8))}}


def sources():
    paths=[Path(__file__),ROOT/'PREPARED_ACTION_RETURN_PROTOCOL_V001.md',
        ROOT/'FIXED_ACTION_MODE_INTERFACE_V001.md',PHASE,STATES,
        ROOT/'COMMON_HISTORY_PHASE_MEAN_V003_FROZEN.json',
        ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json',ROOT/'disk_solver.py',law.SHAPE_PATH]
    return {str(p):law.sha(p) for p in paths}


def authenticate(path,freeze):
    r=json.loads(path.read_text())
    assert r['freeze_sha256']==law.sha(freeze)
    assert r['payload_sha256']==hashlib.sha256(law.encode(r['payload'])).hexdigest()
    assert all(r['payload']['checks'].values())
    return r['payload']


def main():
    import sys
    if sys.argv[1:]==['freeze']:
        law.save_new(FREEZE,{'files':sources()})
        print('FROZEN; no action return calculated.')
        return
    assert not sys.argv[1:] and not OUTPUT.exists()
    assert json.loads(FREEZE.read_text())['files']==sources()
    phase=authenticate(PHASE,ROOT/'COMMON_HISTORY_PHASE_MEAN_V003_FROZEN.json')
    states=authenticate(STATES,ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json')
    indexed={}
    for c in states['cases']:
        for o in c['observations']:
            if o['hold']==0:
                indexed[(c['gap'],c['order'],c['dt'],c['duration'],o['g_over_a0'])]=(c,o)
    start=time.perf_counter()
    rows=[]
    for row in phase['rows']:
        c,o=indexed[(row['gap'],row['mode_order'],row['dt'],row['duration'],row['g_over_a0'])]
        delta=np.array(c['delta'])
        weights=np.array(c['weights'])
        md=row['mode_data']
        calculated=[solve_actions(delta,np.array(md['turning_low']),np.array(md['turning_high']),n)
                    for n in (64,128)]
        low,high=calculated
        action=np.array(high['action'])
        force_period=np.array(md['periods'])
        oldkin=np.array(md['mean_kinetic'])
        original_identity_error=float(np.max(abs(action*2*math.pi/force_period-2*oldkin)
            /np.array(md['mode_excitation'])))
        energy=np.array(high['zero_source_energy'])
        pressure=np.array(high['zero_source_pressure'])
        eq=float(np.sum(weights*energy))
        pq=float(np.sum(weights*pressure))
        error=max(float(np.max(abs(np.array(low['action'])/action-1))),
            float(np.max(abs(np.array(low['zero_source_energy'])/energy-1))),
            float(np.max(abs(np.array(low['zero_source_pressure'])-pressure)/energy)))
        g=row['g']
        gs=states['parameters']['gs_internal']
        h=g/math.sqrt(1+(g/gs)**2)
        y=np.array(o['y']);v=np.array(o['v'])
        held_intrinsic=float(np.sum(weights*(v*v/2+delta*delta*y*y/2+y**4/4-delta*h*y)))
        preparation=c['Kb']*g*g/2+held_intrinsic
        preparation_error=abs(preparation-o['energy'])/(c['Kb']*g*g)
        returned=eq-preparation
        checks={'both_quadrature_identities':all(all(v['checks'].values()) for v in calculated),
            'original_action_kinetic_identity':original_identity_error<=2e-8,
            'cross_quadrature':error<=2e-8,'preparation_energy_ledger':preparation_error<=2e-8,
            'cycle_ledger':abs((preparation+returned)-eq)<=2e-8*eq,
            'positive_remaining_energy':eq>0}
        rows.append({'gap':row['gap'],'mode_order':row['mode_order'],'dt':row['dt'],
            'duration':row['duration'],'g':g,'g_over_a0':row['g_over_a0'],
            'prepared_action_sum':float(np.sum(weights*action)),
            'return_energy':eq,'return_pressure':pq,'return_w':pq/eq,
            'preparation_work':preparation,'adiabatic_return_work':returned,
            'complete_cycle_work':preparation+returned,'held_intrinsic_energy':held_intrinsic,
            'original_action_kinetic_error':original_identity_error,'cross_quadrature_error':error,
            'preparation_ledger_error':preparation_error,'mode_data':high,'checks':checks})
    payload={'role':'Ideal fixed-volume adiabatic return of actual prepared scalar actions; not an observed cosmic history.',
        'baseline':'Same unchanged DeltaU cancels at both cycle endpoints; no vacuum rematching.',
        'rows':rows,'checks':{'all_36_rows':len(rows)==36,'all_checks':all(all(r['checks'].values()) for r in rows)},
        'seconds':time.perf_counter()-start}
    law.save_new(OUTPUT,{'freeze_sha256':law.sha(FREEZE),'payload':payload,
        'payload_sha256':hashlib.sha256(law.encode(payload)).hexdigest()})
    print(json.dumps({'checks':payload['checks'],'seconds':payload['seconds'],
        'main_rows':[{k:v for k,v in r.items() if k not in ('mode_data',)}
            for r in rows if r['dt']==.005 and r['gap']==.001]},indent=2))


if __name__=='__main__':
    main()
