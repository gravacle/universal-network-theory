"""One counted physical Hunit calibration against exposed CMB theta.

All dimensionless model parameters, physical a0,T0,Neff,YHe held fixed.
Radiation Omega and physical baryon density change consistently with Hunit.
Not a unit rescaling, new held-out evidence, native parameter derivation,
or a fit of the BAO ruler. Preserve the failed73.6 development point.
Bracketing endpoint60, saved73.6; max12 secants, theta relative1e-6.
Existing HYREC binaries only, serial. Frozen numerical gates in thermal note.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_acoustic_v001 as acoustic
import invariant_clock_acoustic_bao_v001 as bao

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_CMB_CALIBRATION_V001_RESULT.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    start=time.monotonic();builds=acoustic.authenticate();controls=[];trials=[]
    def check(name,value,tol):
        controls.append(dict(name=name,error=float(value),tolerance=tol,passed=bool(value<=tol)))
    if sha(acoustic.OUT)!=bao.PARENT_SHA:raise ValueError('Changed prior acoustic result')
    parent=json.loads(acoustic.OUT.read_text())
    for name,digest in parent['hashes'].items():
        p=BASE/name if name!='HYREC_LOCAL_BUILD_V001.json' else BASE/'hyrec_inputs_v001'/name
        if sha(p)!=digest:raise ValueError('Changed parent '+name)
    seed=json.loads(acoustic.plasma.prior.old.base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0']=100.
    def model_at(h):
        saved=json.loads(json.dumps(seed));saved['inherited']['H0_km_s_Mpc']=h
        return acoustic.plasma.prior.old.base.Model(saved,1)
    old=parent['rows'][0]
    path=BASE/old['invocations']['default']['output_path']
    if sha(path)!=old['invocations']['default']['output_sha256']:raise ValueError('Changed reusable endpoint')
    reused=dict(Hunit=73.6,residual=old['observables']['default']['theta100']/acoustic.PLANCK_THETA100-1,
        invocation=old['invocations']['default'],observables=old['observables']['default'],reused_without_execution=True)
    trials.append(reused)
    def evaluate(h,index):
        bg=acoustic.Background(model_at(h))
        atom,inv=acoustic.invoke(bg,'default',f'CMB_CAL_{index:02d}',builds)
        obs=acoustic.observables(bg,atom)
        trial=dict(Hunit=h,residual=obs['theta100']/acoustic.PLANCK_THETA100-1,
            invocation=inv,observables=obs,reused_without_execution=False)
        trials.append(trial)
        print(json.dumps(dict(trial=index,Hunit=h,theta100=obs['theta100'],residual=trial['residual'])),flush=True)
        return trial,atom
    lower,latom=evaluate(60.,0);upper=reused
    if lower['residual']*upper['residual']>=0:
        result=dict(protocol=__doc__,status='FAILED_PREDECLARED_BRACKET',trials=trials,
                    source_sha256=sha(Path(__file__)))
        with OUT.open('x') as stream:json.dump(result,stream,indent=2)
        return
    selected=None;atom=None
    for iteration in range(1,13):
        lo,hi=lower['Hunit'],upper['Hunit'];fl,fu=lower['residual'],upper['residual']
        proposal=(lo*fu-hi*fl)/(fu-fl)
        if not lo<proposal<hi:proposal=(lo+hi)/2
        trial,ta=evaluate(proposal,iteration)
        if abs(trial['residual'])<=1e-6:selected,atom=trial,ta;break
        if trial['residual']*fl>0:lower=trial
        else:upper=trial
    if selected is None:
        result=dict(protocol=__doc__,status='FAILED_DECLARED_ROOT_BUDGET',trials=trials,
                    source_sha256=sha(Path(__file__)))
        with OUT.open('x') as stream:json.dump(result,stream,indent=2)
        return
    model=model_at(selected['Hunit']);bg=acoustic.Background(model)
    half,hcall=acoustic.invoke(bg,'half','CMB_CAL_FINE',builds)
    alternate,acall=acoustic.invoke(bg,'default','CMB_CAL_HGRID',builds,alternate=True)
    fine=acoustic.observables(bg,half);aobs=acoustic.observables(bg,alternate)
    thin=acoustic.observables(bg,half,thinning=2);quad=acoustic.observables(bg,half,nquad=128)
    check('calibration_residual_half',abs(fine['theta100']/acoustic.PLANCK_THETA100-1),2e-6)
    co=np.array(atom['rows'],float);fi=np.array(half['rows'],float)[::2]
    if co.shape!=fi.shape or np.max(abs(co[:,0]-fi[:,0]))>1e-12:raise ValueError('Atomic output grids differ')
    check('xe_refinement',np.max(abs(co[:,1]-fi[:,1])/np.maximum(1e-3,abs(fi[:,1]))),2e-3)
    check('Tm_refinement',np.max(abs(co[:,2]/fi[:,2]-1)),2e-3)
    check('H_grid_pointwise',acall['native_alternate_H_relative_error'],2e-7)
    for name in ('zstar','rs_Mpc','DM_Mpc','theta100','drag_redshift_interval','drag_ruler_Mpc_interval'):
        v=np.array(fine[name]);dv=np.array(selected['observables'][name])
        check(name+'_atomic',np.max(abs(dv/v-1)),2e-4)
        check(name+'_thinning',np.max(abs(np.array(thin[name])/v-1)),1e-4)
        check(name+'_quadrature',np.max(abs(np.array(quad[name])/v-1)),2e-8)
        check(name+'_H_grid',np.max(abs(np.array(aobs[name])/dv-1)),1e-5)
    oldbao=json.loads(bao.OUT.read_text())
    expected='684da639c34341ba965f06f4b695e9a8f6b3b30e06a47385e92c2bae9b95f4f8'
    if sha(bao.OUT)!=expected:raise ValueError('Changed BAO receipt')
    obs=np.array(oldbao['data']);cov=np.array(oldbao['covariance']);chol=np.linalg.cholesky(cov)
    rows=[]
    for dust in (False,True):
        bb=acoustic.Background(model,dust);kind='REFERENCE' if dust else 'CANDIDATE'
        inv={}
        if dust:
            ca,di=acoustic.invoke(bb,'default','CMB_CAL_REF_DEFAULT',builds)
            fa,hi=acoustic.invoke(bb,'half','CMB_CAL_REF_HALF',builds)
            ob=acoustic.observables(bb,fa);oc=acoustic.observables(bb,ca)
            inv=dict(default=di,half=hi)
            crows=np.array(ca['rows'],float);frows=np.array(fa['rows'],float)[::2]
            check('reference_xe',np.max(abs(crows[:,1]-frows[:,1])/np.maximum(1e-3,abs(frows[:,1]))),2e-3)
            check('reference_Tm',np.max(abs(crows[:,2]/frows[:,2]-1)),2e-3)
            for key in ('zstar','rs_Mpc','theta100','drag_ruler_Mpc_interval'):
                check('reference_'+key,np.max(abs(np.array(oc[key])/np.array(ob[key])-1)),2e-4)
        else:ob=fine;inv=dict(default=selected['invocation'],half=hcall,alternate=acall)
        physical=bao.vector(bb,96);coarse=bao.vector(bb,48);si=bao.vector(bb,96,True)
        check(kind+'_BAO_gauss',np.max(abs(coarse/physical-1)),2e-12)
        check(kind+'_BAO_independent',np.max(abs(si/physical-1)),2e-11)
        w=np.linalg.solve(chol,physical);wd=np.linalg.solve(chol,obs)
        lo,up=ob['drag_ruler_Mpc_interval'];ymin=float(w@wd/(w@w))
        ys=[1/up,1/lo]
        if ys[0]<ymin<ys[1]:ys.append(ymin)
        scores=[float((y*w-wd)@(y*w-wd)) for y in ys]
        rows.append(dict(kind=kind,observables=ob,invocations=inv,DESI_score_interval=[min(scores),max(scores)],
            actual_H_today=selected['Hunit']*float(bb.E(1.)),omega_gamma=bb.og,omega_radiation=bb.OR,
            physical_omega_b=bb.omega_b,galaxy_a0_Hunit_ratio=model.p['a0']/(acoustic.S['c']*bb.hunit)))
    result=dict(protocol=__doc__,status='COMPLETED_ONE_PARAMETER_DEVELOPMENT_CALIBRATION',
        fitted_freedoms=1,calibration_observable='Published compressed100theta1.0411',
        selected_Hunit=selected['Hunit'],fixed=model.p,trials=trials,rows=rows,controls=controls,
        all_controls_passed=all(c['passed'] for c in controls),elapsed_seconds=time.monotonic()-start,
        hashes={p.name:sha(p) for p in (Path(__file__),Path(acoustic.__file__),Path(bao.__file__),acoustic.OUT,bao.OUT)})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(status=result['status'],Hunit=selected['Hunit'],all_controls_passed=result['all_controls_passed'],
        rows=[{k:v for k,v in r.items() if k!='invocations'} for r in rows],controls=controls,
        elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
