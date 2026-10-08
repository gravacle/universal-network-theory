"""Saved orbit audit, independent periodic midpoint quadrature, analytic limit controls."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/'COMMON_HISTORY_PHASE_MEAN_V002_RESULTS.json'
FREEZE=ROOT/'COMMON_HISTORY_PHASE_MEAN_V002_FROZEN.json'
SOURCE=ROOT/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def unseal(path,freeze):
    o=json.loads(path.read_text());assert o['freeze_sha256']==sha(freeze)
    encoded=json.dumps(o['payload'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    assert hashlib.sha256(encoded).hexdigest()==o['payload_sha256']
    return o['payload']


def periodic_mean(delta,a,b,n):
    theta=(np.arange(n)+.5)*(2*math.pi/n)
    q=(a+b)[:,None]/2+(b-a)[:,None]/2*np.cos(theta)
    polynomial=q*q+(a+b)[:,None]*q+(2*delta*delta+a*a+a*b+b*b)[:,None]
    assert np.all(polynomial>0)
    measure=1/np.sqrt(polynomial);norm=np.sum(measure,axis=1)
    return np.sum(q*measure,axis=1)/norm,math.sqrt(2)*(2*math.pi/n)*norm


def main():
    f=json.loads(FREEZE.read_text())
    for name,digest in f['files'].items():assert sha(ROOT/name)==digest,name
    src=unseal(SOURCE,ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json')
    result=unseal(INPUT,FREEZE);assert all(result['checks'].values())
    assert len(result['rows'])==36
    gs=src['parameters']['gs_internal'];a0=src['parameters']['a0_internal']
    records=[];seen=set();worst_mean=0.;worst_period=0.;worst_energy=0.
    for row in result['rows']:
        identity=(row['gap'],row['duration'],row['mode_order'],row['dt'],row['g'])
        assert identity not in seen;seen.add(identity)
        case=next(c for c in src['cases'] if(c['gap'],c['duration'],c['order'],c['dt'])==identity[:4])
        obs=next(r for r in case['observations'] if r['hold']==0 and abs(r['g_over_a0']*a0-row['g'])<1e-16)
        d=np.array(case['delta']);w=np.array(case['weights']);g=row['g'];h=g/math.sqrt(1+(g/gs)**2)
        hp=(1+(g/gs)**2)**-1.5;kb=case['Kb'];md=row['mode_data']
        assert all(row['checks'].values()) and all(all(c.values()) for c in row['all_quadrature_checks'])
        lo=np.array(md['turning_low']);hi=np.array(md['turning_high']);y=np.array(obs['y']);v=np.array(obs['v'])
        # Expanded unweighted energy, independent of the relative-minimum representation.
        E=.5*v*v+.5*d*d*y*y+.25*y**4-d*h*y
        V=lambda z:.5*d*d*z*z+.25*z**4-d*h*z
        exc=np.array(md['mode_excitation']);assert np.all(exc>0)
        endpoint=float(np.max(np.maximum(abs(V(lo)-E),abs(V(hi)-E))/exc))
        assert endpoint<2e-8;worst_energy=max(worst_energy,endpoint)
        coarse,coarseperiod=periodic_mean(d,lo,hi,1024)
        mean,period=periodic_mean(d,lo,hi,2048)
        D=g-hp*math.fsum(float(a*b*c) for a,b,c in zip(w,d,mean))/kb
        mean_error=abs(D-row['phase_mean_D'])/g
        period_error=float(np.max(abs(period-np.array(md['periods']))/period))
        assert mean_error<2e-10 and period_error<2e-10
        worst_mean=max(worst_mean,mean_error);worst_period=max(worst_period,period_error)
        energy=math.fsum(float(a*b) for a,b in zip(w,exc))
        assert abs(energy-obs['excitation'])/(kb*g*g)<2e-8
        records.append(dict(identity=identity,D_over_g=D/g,relaxed_D_over_g=row['relaxed_D_over_g'],
            departure_over_g=D/g-row['relaxed_D_over_g'],independent_force_error_over_g=mean_error,
            independent_period_relative_error=period_error,expanded_energy_endpoint_error=endpoint,
            periodic_resolution_mean_y_max_abs=float(np.max(abs(mean-coarse))),
            period_min=float(np.min(period)),period_max=float(np.max(period))))
    # Synthetic limiting identities only, not a new preparation used in the result above.
    import common_history_phase_mean_v001 as frozen_function
    delta=np.array([.3]);h=.02;lo=0.;hi=1.
    for _ in range(80):
        mid=(lo+hi)/2
        if mid**3+delta[0]**2*mid<delta[0]*h:lo=mid
        else:hi=mid
    star=(lo+hi)/2;k=delta[0]**2+3*star**2;period0=2*math.pi/math.sqrt(k)
    controls=[]
    for relative_amplitude in (.1,.03,.01,.003):
        y=np.array([star*(1+relative_amplitude)]);v=np.array([0.])
        out=frozen_function.phase_mean(delta,y,v,h,256)
        energy=float(out['mode_excitation'][0]);mean=float(out['mean_y'][0]);period=float(out['periods'][0])
        # From averaged equation k<x>+3ystar<x²>+<x³>=0 and <x²>=E/k+O(E²).
        leading_shift=-3*star*energy/k**2
        controls.append(dict(relative_amplitude=relative_amplitude,ystar=star,stiffness=k,
            energy=energy,mean=mean,period=period,harmonic_period=period0,
            relative_period_departure=period/period0-1,
            mean_shift_over_leading_small_energy_shift=(mean-star)/leading_shift))
    assert abs(controls[-1]['relative_period_departure'])<abs(controls[0]['relative_period_departure'])
    assert abs(controls[-1]['mean_shift_over_leading_small_energy_shift']-1)<1e-4
    print(json.dumps(dict(role='Independent saved-energy phase quadrature and analytic limit controls; no new propagation or galaxy fit.',
        source_sha256=sha(Path(__file__)),input_sha256=sha(INPUT),freeze_sha256=sha(FREEZE),
        original_trajectory_result_sha256=sha(SOURCE),phase_row_count=len(records),records=records,
        maximum_independent_force_error_over_g=worst_mean,
        maximum_independent_period_relative_error=worst_period,
        maximum_expanded_endpoint_energy_relative_error=worst_energy,
        harmonic_limit_controls=controls),indent=2,sort_keys=True,allow_nan=False))


if __name__=='__main__':main()
