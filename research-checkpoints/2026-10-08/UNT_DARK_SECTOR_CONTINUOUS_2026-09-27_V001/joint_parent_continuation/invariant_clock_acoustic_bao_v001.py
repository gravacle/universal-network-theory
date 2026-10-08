"""Predicted-ruler DESI development test, not a new calibration or holdout.

Reuse completed measured-temperature K(X) recombination and physical drag
interval. No atomic rerun or model/ruler fit for the primary prediction.
Keep supplied13x13 covariance and final DH,DM ordering. An explicitly
counterfactual one-ruler profile diagnoses scale versus shape, not native
proof or a revised candidate. Numerical gates inherited from DESI_BAO_SHAPE:
2e-12 quadrature,2e-11 independent integration,2e-8 score arithmetic,
2e-12 covariance. No observational pass threshold, p-value or sigma claim.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_acoustic_v001 as acoustic
import desi_bao_shape_v001 as old

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_ACOUSTIC_BAO_V001_RESULT.json'
PARENT_SHA='29807e6a6dd8d4aa0b3cbfb26b4ba94a4ea9c8ecd20b74ec5e8669c535acf2ea'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def vector(bg,order,simpson=False):
    values=[]
    for z,kind in old.ORDER:
        dh=bg.unit/float(bg.E(1/(1+z)))
        if simpson:
            zz=np.linspace(0,z,2049);fun=1/bg.E(1/(1+zz))
            dm=bg.unit*z/2048/3*(fun[0]+fun[-1]+4*np.sum(fun[1:-1:2])+2*np.sum(fun[2:-1:2]))
        else:dm=bg.unit*acoustic.quad(lambda zz:1/bg.E(1/(1+zz)),0,z,order)
        dv=(z*dm*dm*dh)**(1/3)
        values.append({'DM_over_rs':dm,'DH_over_rs':dh,'DV_over_rs':dv}[kind])
    return np.array(values)


def main():
    start=time.monotonic();controls=[]
    def check(name,value,tol):
        controls.append(dict(name=name,error=float(value),tolerance=tol,passed=bool(value<=tol)))
    if sha(acoustic.OUT)!=PARENT_SHA:raise ValueError('Changed acoustic receipt')
    parent=json.loads(acoustic.OUT.read_text())
    if not parent['all_controls_passed']:raise ValueError('Unqualified acoustic input')
    for name,digest in parent['hashes'].items():
        p=BASE/name
        if name=='HYREC_LOCAL_BUILD_V001.json':p=BASE/'hyrec_inputs_v001'/name
        if sha(p)!=digest:raise ValueError('Changed acoustic ancestor '+name)
    mean=BASE/old.DATA/'desi_gaussian_bao_ALL_GCcomb_mean.txt'
    covfile=BASE/old.DATA/'desi_gaussian_bao_ALL_GCcomb_cov.txt'
    for p in (mean,covfile):
        if sha(p)!=old.PINS[old.DATA+p.name]:raise ValueError('Changed DESI input')
    lines=[s.split() for s in mean.read_text().splitlines() if s.strip() and not s.startswith('#')]
    if [(float(r[0]),r[2]) for r in lines]!=old.ORDER:raise ValueError('Changed data order')
    obs=np.array([float(r[1]) for r in lines]);cov=np.loadtxt(covfile)
    if cov.shape!=(13,13):raise ValueError('Wrong covariance shape')
    check('covariance_symmetry',np.max(abs(cov-cov.T)),2e-12)
    chol=np.linalg.cholesky(cov);ci=np.linalg.solve(cov,np.eye(13))
    check('covariance_inverse',np.max(abs(cov@ci-np.eye(13))),2e-12)
    saved=json.loads(acoustic.plasma.prior.old.base.SOURCE.read_text())
    saved['inherited']['Q0_over_H0']=100.;model=acoustic.plasma.prior.old.base.Model(saved,1)
    rows=[]
    for dust in (False,True):
        bg=acoustic.Background(model,dust);kind='REFERENCE' if dust else 'CANDIDATE'
        p=next(r for r in parent['rows'] if r['kind']==kind)
        f=vector(bg,96);co=vector(bg,48);si=vector(bg,96,True)
        check(kind+'_quadrature',np.max(abs(co/f-1)),2e-12)
        check(kind+'_independent_integration',np.max(abs(si/f-1)),2e-11)
        A=float(f@ci@f);B=float(f@ci@obs);C=float(obs@ci@obs)
        yopt=B/A
        def score(y):
            residual=f*y-obs;w=np.linalg.solve(chol,residual)
            direct=float(w@w);polynomial=A*y*y-2*B*y+C
            check(kind+'_quadratic_score',abs(direct-polynomial),2e-8)
            return direct
        lo,hi=p['observables']['half']['drag_ruler_Mpc_interval']
        candidates=[1/hi,1/lo]
        if candidates[0]<yopt<candidates[1]:candidates.append(yopt)
        scores=[score(y) for y in candidates]
        yd=2/(lo+hi);residual=f*yd-obs;shape=score(yopt)
        rows.append(dict(kind=kind,predicted_ruler_Mpc_interval=[lo,hi],
            score_interval=[min(scores),max(scores)],
            score_witnesses=[dict(ruler_Mpc=1/y,score=s) for y,s in zip(candidates,scores)],
            midpoint_prediction=(f*yd).tolist(),midpoint_residual=residual.tolist(),
            midpoint_whitened_residual=np.linalg.solve(chol,residual).tolist(),
            counterfactual_profile=dict(fitted_freedoms=1,ruler_Mpc=1/yopt,score=shape,
                scope='Development common-scale fit, not the physical ruler or a revised candidate'),
            midpoint_scale_penalty=A*(yd-yopt)**2,
            Hunit_times_predicted_ruler_interval=[model.p['H0_km_s_Mpc']*lo,model.p['H0_km_s_Mpc']*hi]))
    result=dict(protocol=__doc__,data_order=old.ORDER,data=obs.tolist(),covariance=cov.tolist(),
        rows=rows,controls=controls,all_controls_passed=all(c['passed'] for c in controls),
        elapsed_seconds=time.monotonic()-start,hashes={p.name:sha(p) for p in
            (Path(__file__),Path(acoustic.__file__),acoustic.OUT,Path(old.__file__),mean,covfile)})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
