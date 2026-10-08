"""New h=g local reference only; not a finite-gradient disk prediction."""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parent
STEM='LINEAR_SOURCE_GALAXY_REFERENCE_V001'
PRIOR='GALAXY_RADIAL_TRANSFER_V001_RESULT.json'
PRIOR_SHA='77883bc7e0da4ceaf1d623ba835be6dc3c0666dd0b56d0b00aa36e551247f7c0'
A0=1.0059833281731022e-10
INTERNAL=8/(3*math.pi)
PC=648000*149597870700/math.pi
CONV=1e6/(1000*PC)
ELL_PC=100.
GM_SUN=1.32712440018e20


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def theta_from_x(x):
    h=INTERNAL*np.asarray(x,dtype=float)
    t=2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    return h,np.arctan2(1.,t)


def flux(x,order=None):
    h,theta=theta_from_x(x)
    if order is not None:
        z,w=np.polynomial.legendre.leggauss(order)
        u=theta[...,None]*(z+1)/2
        si=np.sin(u)**2
        bracket=theta/2*np.sum(w*2*si*(3-2*si),axis=-1)
    else:
        bracket=1.5*theta-.5*np.sin(2*theta)-np.sin(4*theta)/8
        small=theta<.2
        ts=theta[small]
        series=np.zeros_like(ts)
        for n in range(1,13):
            coefficient=(-1)**(n+1)*(2.**(2*n)+2.**(4*n-1))/math.factorial(2*n+1)
            series+=coefficient*ts**(2*n+1)
        bracket=np.array(bracket,copy=True)
        bracket[small]=series
    return h*h*bracket/(2*INTERNAL)


def inverse(d,iterations):
    d=np.asarray(d,dtype=float)
    if np.any(~np.isfinite(d)) or np.any(d<=0):
        raise ValueError('Positive finite source required; no clipping')
    lo=np.zeros_like(d)
    hi=4*(d+np.sqrt(d)+1)
    if np.any(flux(hi)<d):
        raise ValueError('Predeclared inverse bracket failed')
    for _ in range(iterations):
        mid=(lo+hi)/2
        less=flux(mid)<d
        lo=np.where(less,mid,lo)
        hi=np.where(less,hi,mid)
    return (lo+hi)/2


def readout(pred,observed,error,outer):
    dv=pred-observed
    lg=2*np.log10(pred/observed)
    return dict(prediction_kms=pred.tolist(),residual_kms=dv.tolist(),
                residual_dex=lg.tolist(),quoted_error_residual=(dv/error).tolist(),
                outer=dict(velocity_mse=float(np.mean(dv[outer]**2)),
                           logg_mse=float(np.mean(lg[outer]**2))))


def main():
    destination=ROOT/(STEM+'_RESULT.json')
    if destination.exists():
        raise FileExistsError(destination)
    start=time.perf_counter()
    out=dict(status='started',controls=[],cases=[],excluded=[],inputs=dict(
        a0_si=A0,ell_pc_development_choice=ELL_PC,GM_sun=GM_SUN,
        per_galaxy_fits=0,new_global_fits=0,
        scored_model='h=g zero-gradient local algebraic reference; ell absent'))
    def check(name,error,limit):
        out['controls'].append(dict(name=name,error=float(error),limit=limit,
                                   passed=bool(math.isfinite(error) and error<=limit)))
    try:
        paths=(Path(__file__),ROOT/(STEM+'.md'),ROOT/PRIOR)
        out['custody']={p.name:sha(p) for p in paths}
        if out['custody'][PRIOR]!=PRIOR_SHA:
            raise ValueError('Prior radial result changed')
        prior=json.loads((ROOT/PRIOR).read_text())
        if prior['status']!='QUALIFIED_COMPLETE_CENSUS' or prior['census']!=100 or prior['eligible']!=94:
            raise ValueError('Prior census/qualification differs')
        x=np.logspace(-12,12,241)
        f,f32,f64=flux(x),flux(x,32),flux(x,64)
        check('positive_flux_oracle',float(np.max(abs(f/f64-1))),1e-11)
        check('positive_quadrature_refinement',float(np.max(abs(f32/f64-1))),1e-11)
        check('positive_monotone',0 if np.all(f>0) and np.all(np.diff(f)>0) else 1,0)
        check('deep_limit',abs(float(flux(np.array([1e-8]))[0])/1e-16-1),1e-6)
        beta=32/(9*math.pi**2)
        mcrit=A0*(ELL_PC*PC)**2/(beta*GM_SUN)
        out['separate_spherical_asymptotic']=dict(
            beta=beta,ell_pc=ELL_PC,Mcrit_Msun=mcrit,
            acceleration='sqrt(G M a0)/R + (beta G M-a0 ell^2)/R^2',
            validity=['rM/R << 1','ell^2/(rM R) << 1','outside ordinary source',
                      'negligible external field','isolated settled spherical response'],
            scored_against_disk_rows=False)
        check('critical_mass_identity',abs(beta*GM_SUN*mcrit/(A0*(ELL_PC*PC)**2)-1),1e-12)
        for filename,expected in sorted(prior['case_sha256'].items()):
            path=ROOT/'GALAXY_RADIAL_TRANSFER_V001_CASES'/filename
            if sha(path)!=expected:
                raise ValueError('Case hash changed: '+filename)
            case=json.loads(path.read_text())
            if case['n']<6:
                out['excluded'].append(dict(name=case['name'],reason=case['reason'],n=case['n'],case_sha256=expected))
                continue
            if case['status']!='QUALIFIED':
                raise ValueError('Unqualified source case: '+filename)
            rows=case['rows']
            radius,obs,err,gb,go=(np.asarray([r[k] for r in rows]) for k in
                                ('R_kpc','vobs_kms','evobs_kms','gbar_si','gobs_si'))
            outer=np.asarray(case['outer_indices'],dtype=int)
            if len(rows)!=case['n'] or outer.tolist()!=list(range(case['n_inner'],case['n'])):
                raise ValueError('Saved outer mask differs')
            if any(np.any(~np.isfinite(a)) or np.any(a<=0) for a in (radius,obs,err,gb,go)):
                raise ValueError('Invalid saved row; no exclusion/repair')
            d=gb/A0
            g72=inverse(d,72)
            g88=inverse(d,88)
            name=case['name']
            check(name+'_inverse',float(np.max(abs(flux(g88)/d-1))),1e-11)
            check(name+'_inverse_refinement',float(np.max(abs(g72/g88-1))),1e-11)
            check(name+'_SI_identity',float(np.max(abs(CONV*obs*obs/radius/go-1))),1e-10)
            pred=np.sqrt(A0*g88*radius/CONV)
            new=readout(pred,obs,err,outer)
            references={key:value for key,value in case['fixed'].items()}
            for halo in ('NFW','ISO'):
                references[halo+'_513']=next(v['readout'] for v in case['halo_fits'][halo] if v['grid_count']==513)
            pair={}
            for label,old in references.items():
                saved=np.asarray(old['prediction_kms'])
                again=readout(saved,obs,err,outer)['outer']
                for metric in ('velocity_mse','logg_mse'):
                    check(name+'_'+label+'_'+metric,abs(again[metric]-old['outer'][metric])/
                          max(1.,abs(old['outer'][metric])),1e-10)
                pair[label]={k:new['outer'][k]-again[k] for k in again}
            out['cases'].append(dict(name=name,case_sha256=expected,
                source_lines=[r['source_line'] for r in rows],R_kpc=radius.tolist(),
                gbar_si=gb.tolist(),outer_indices=outer.tolist(),
                gpred_si=(A0*g88).tolist(),new_local_reference=new,
                paired_outer_differences=pair))
            peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            peak=peak if sys.platform=='darwin' else 1024*peak
            if time.perf_counter()-start>120 or peak>256*1024**2:
                raise RuntimeError('Declared resource ceiling')
        check('same_94_6_census',0 if len(out['cases'])==94 and len(out['excluded'])==6 else 1,0)
        out['new_galaxy_balanced_outer_MSE']={k:float(np.mean([c['new_local_reference']['outer'][k]
                                                            for c in out['cases']]))
                                             for k in ('velocity_mse','logg_mse')}
        out['saved_reference_outer_MSE']=prior['outer_galaxy_balanced_MSE']
        out['all_controls_pass']=all(c['passed'] for c in out['controls'])
        out['status']='QUALIFIED_LOCAL_REFERENCE_ONLY' if out['all_controls_pass'] else 'UNQUALIFIED_CONTROLS'
        out['scope']='New exposed no-fit local shape screen; no finite-ell disk prediction, native derivation, cosmology, or model-superiority claim.'
    except Exception as exc:
        out['status']='failed'
        out['failure']=repr(exc)
        out['all_controls_pass']=False
    out['elapsed_seconds']=time.perf_counter()-start
    with destination.open('x') as stream:
        json.dump(out,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(status=out['status'],galaxies=len(out['cases']),
                         elapsed_seconds=out['elapsed_seconds'],result=str(destination))))
    return 0 if out['all_controls_pass'] else 2


if __name__=='__main__':
    if sys.argv[1:]!=['--run']:
        raise SystemExit('Explicit --run required; no producer is imported.')
    raise SystemExit(main())
