"""Saved physical fields, fixed symmetric whitening, true-residual MINRES."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,time
import numpy as np
import cross_u_ngc3198_nonlinear_disk_v001 as core

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_MINRES_RECOVERY_V003'
PARENT='CROSS_U_NGC3198_PARTIAL_RECOVERY_V002'
PINS={
    'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md':'91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8',
    'cross_u_ngc3198_nonlinear_disk_v001.py':'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1',
    'cross_u_ngc3198_partial_recovery_v002.py':'6f52dddd8ec0fbf844f9174c92e80d3700b51dcc8432709cd1d88c81811b1925',
    'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002.md':'c236db1e798d4df086460e880d3515612dea127335eb85c4defde842e4589400',
    'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_MANIFEST.json':'a1756ed9cec5bff2273088008ca6410c9c9a6f769f0fb92c6750c2601a89f687',
    'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json':'c72830fb31defeae5443beed55eec910b08c2bf520a45f14853c9cdfe59950a1',
    'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json':'720cbaf0902285d35dc3a50d59f81d266431c7d91b4985eb19ab822b0b14413b',
    'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RESULT.json':'eb99696cfc5ff635cc56dbe3dd128f7ce7032529ff62f0c4037f0b3cfc346300'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def finite(v):return float(v) if math.isfinite(v) else None
def auth():
    for n,h in PINS.items():assert sha(BASE/n)==h,('changed input',n)
    core.authenticate()
def write(n,o):return core.publish(n,o)

def minres(A,b,seed,tolerance,cap=600):
    """M=None, shift0; accepts only original-denominator true residual."""
    x=seed.copy();norm=float(np.linalg.norm(b));checks=[];it=0
    def close(reason):
        error=None
        if math.isfinite(norm) and norm>0 and np.all(np.isfinite(b)) and np.all(np.isfinite(x)):
            action=A(x)
            if np.all(np.isfinite(action)):error=finite(float(np.linalg.norm(b-action)/norm))
        return x,dict(ok=error is not None and error<=tolerance,error=error,
                      iterations=it,reason=reason,true_checks=checks)
    if norm==0:
        if np.all(b==0):return np.zeros_like(b),dict(ok=True,error=0.,iterations=0,reason='zero_rhs',true_checks=[])
        return close('underflowed_nonzero_rhs_norm')
    if not math.isfinite(norm) or not np.all(np.isfinite(x)):return close('nonfinite_initial_state')
    action=A(x)
    if not np.all(np.isfinite(action)):return close('nonfinite_seed_action')
    r=b-action;beta=float(np.linalg.norm(r))
    initial=finite(beta/norm);checks.append(dict(iteration=0,error=initial))
    if initial is not None and initial<=tolerance:return close('authenticated_seed_true_residual')
    if not math.isfinite(beta) or beta<=0:return close('initial_norm_breakdown')
    v=r/beta;previous_v=np.zeros_like(v)
    older_w=np.zeros_like(v);previous_w=np.zeros_like(v)
    cs=-1.;sn=0.;dbar=eps=0.;phibar=beta
    for it in range(1,cap+1):
        if not np.all(np.isfinite(v)):return close('nonfinite_lanczos_direction')
        q=A(v)
        if not np.all(np.isfinite(q)):return close('nonfinite_lanczos_action')
        q-=beta*previous_v;alpha=float(np.sum(v*q));q-=alpha*v
        next_beta=float(np.linalg.norm(q))
        oldeps=eps;delta=cs*dbar+sn*alpha;gbar=sn*dbar-cs*alpha
        eps=sn*next_beta;dbar=-cs*next_beta;gamma=math.hypot(gbar,next_beta)
        if not all(math.isfinite(t) for t in (alpha,next_beta,delta,gbar,eps,dbar,gamma)) or gamma==0:
            return close('givens_or_lanczos_breakdown')
        cs=gbar/gamma;sn=next_beta/gamma;phi=cs*phibar;phibar=sn*phibar
        w=(v-oldeps*older_w-delta*previous_w)/gamma
        x+=phi*w
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(w)):return close('nonfinite_linear_state')
        if abs(phibar)/norm<=tolerance or it%25==0 or next_beta==0:
            action=A(x)
            error=finite(float(np.linalg.norm(b-action)/norm)) if np.all(np.isfinite(action)) else None
            checks.append(dict(iteration=it,error=error))
            if error is not None and error<=tolerance:return close('true_residual')
        if next_beta==0:return close('lanczos_terminal_true_residual_failed')
        older_w=previous_w;previous_w=w;previous_v=v;v=q/next_beta;beta=next_beta
    return close('iteration_allowance')

def controls():
    cases=[('positive',np.array([[4.,1.],[1.,3.]]),np.array([1.,2.]),np.array([.3,-.2]),np.array([1/11,7/11])),
           ('indefinite',np.array([[2.,3.],[3.,-1.]]),np.array([1.,2.]),np.zeros(2),np.array([7/11,-1/11])),
           ('compatible_singular',np.ones((2,2)),np.array([2.,2.]),np.array([.2,.3]),np.array([.95,1.05])),
           ('incompatible_singular',np.diag([1.,0.]),np.ones(2),np.zeros(2),None)]
    rows=[]
    for name,mat,b,seed,exact in cases:
        x,info=minres(lambda y:mat@y,b,seed,1e-10 if exact is None else 1e-12,20)
        error=None if exact is None else finite(float(np.max(abs(x-exact))))
        passed=(not info['ok'] and info['error'] is not None and info['error']>1e-10) if exact is None else info['ok'] and error is not None and error<=2e-12
        row=dict(name=name,linear=info,solution_error=error,passed=passed)
        path=BASE/f'{STEM}_CONTROL_{name}.npz'
        with path.open('xb') as f:
            np.savez_compressed(f,state=x,seed=seed,rhs=b,matrix=mat);f.flush();os.fsync(f.fileno())
        path.chmod(0o444);row.update(file=path.name,sha256=sha(path))
        write(f'{STEM}_CONTROL_{name}.json',row);rows.append(row)
    return rows

def state(name,step,x,history,identity,partial=None):
    suffix=f'STEP_{step:03d}' if partial is None else f'LINEAR_FAILED_{step:03d}'
    path=BASE/f'{STEM}_{name}_{suffix}.npz'
    ht=json.dumps(history,allow_nan=False);it=json.dumps(identity,sort_keys=True,allow_nan=False)
    with path.open('xb') as f:
        fields=dict(state=x,history=ht,identity=it)
        if partial is not None:fields['unaccepted_linear_partial']=partial
        np.savez_compressed(f,**fields);f.flush();os.fsync(f.fileno())
    path.chmod(0o444);write(path.name+'.commit.json',dict(file=path.name,sha256=sha(path),identity=identity))

def recover(case,receipt):
    name=case['identity']['case'];outputs=receipt['output_sha256']
    paths=sorted(BASE.glob(f'{PARENT}_{name}_LINEAR_FAILED_*.npz')) or sorted(BASE.glob(f'{PARENT}_{name}_STEP_*.npz'))
    p=paths[-1];cp=p.with_name(p.name+'.commit.json')
    assert outputs[p.name]==sha(p) and outputs[cp.name]==sha(cp)
    commit=json.loads(cp.read_text());assert commit['sha256']==sha(p) and commit['identity']==case['identity']
    with np.load(p,allow_pickle=False) as n:
        x=n['state'].copy();history=json.loads(str(n['history']));identity=json.loads(str(n['identity']))
        partial=n['unaccepted_linear_partial'].copy() if 'unaccepted_linear_partial' in n else None
    assert identity==case['identity'] and np.all(np.isfinite(x))
    return x,partial,history,dict(file=p.name,sha256=sha(p),commit_sha256=sha(cp))

def solve(model,name,identity,x,partial):
    started=time.monotonic();history=[];state(name,0,x,history,identity)
    _,pre0,_=model.residual(np.zeros(model.shape));scale=float(np.linalg.norm(model.rhs/np.sqrt(pre0)))
    status='NEWTON_ALLOWANCE'
    for outer in range(40):
        r,pre,H=model.residual(x);root=np.sqrt(pre);b=-r/root;error=float(np.linalg.norm(b)/scale)
        if error<=1e-8:status='CONVERGED';break
        target=min(.5,max(1e-6,.5*math.sqrt(error)))
        def A(v):
            with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
                physical=v/root
                if not np.all(np.isfinite(physical)):return np.full_like(v,np.nan)
                return H(physical)/root
        valid=outer==0 and partial is not None and partial.shape==b.shape and np.all(np.isfinite(partial)) and np.all(partial[~model.mask]==0)
        seed=partial if valid else np.zeros_like(b)
        delta,linear=minres(A,b,seed,target)
        row=dict(outer=outer,error=error,inexact_target=target,linear=linear,
                 parent_partial_used=bool(valid),parent_partial_rejected=bool(outer==0 and partial is not None and not valid))
        if not linear['ok']:
            history.append(row);state(name,outer,x,history,identity,delta);status='LINEAR_FAILED';break
        delta=delta/root;accepted=False;guard_rejections=merit_rejections=0
        for back in range(32):
            step=2.**(-back);candidate=x+step*delta
            try:cr,_=model.residual(candidate,False);candidate_error=float(np.linalg.norm(cr/root)/scale)
            except ValueError:guard_rejections+=1;continue
            if math.isfinite(candidate_error) and candidate_error<=(1-1e-4*step)*error:
                x=candidate;accepted=True;row.update(step=step,candidate_error=candidate_error);break
            merit_rejections+=1
        row.update(accepted=accepted,domain_or_finite_rejections=guard_rejections,merit_rejections=merit_rejections);history.append(row)
        if not accepted:status='GLOBALIZATION_FAILED';break
        state(name,outer+1,x,history,identity)
        print('MINRES_RECOVERY',name,'NEWTON',outer+1,'ERROR',candidate_error,'STEP',step,flush=True)
    r,pre,_=model.residual(x);error=float(np.linalg.norm(r/np.sqrt(pre))/scale)
    if error<=1e-8:status='CONVERGED'
    force=np.gradient(x[0,:,0],model.r,edge_order=2);rows=[]
    for obs in core.observation_rows():
        g=float(np.interp(obs['R'],model.r,force));v2=obs['R']*core.A0_V*g;v=math.sqrt(v2) if v2>=0 else None
        rows.append(dict(obs,radial_force_a0=g,velocity_squared=v2,model_velocity=v,residual=None if v is None else v-obs['velocity']))
    return dict(identity=identity,status=status,numerical_residual=error,history=history,rows=rows,
                elapsed_seconds=time.monotonic()-started,readout_qualified=False,
                physical_flags=dict(refinement_qualified=False,full_metric_qualified=False,FLRW_junction_qualified=False,
                                    formation_qualified=False,stability_qualified=False,joint_superiority_qualified=False))

def close(source,manifest,result):
    auth();assert source==sha(__file__)
    result['manifest']=manifest;rh=write(STEM+'_RESULT.json',result)
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    write(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),source_sha256=source,started=manifest['started'],
                                  closed=now(),result_sha256=rh,output_sha256=outputs))
    print('MINRES_BATCH_CLOSED',result['status'],flush=True)

def main():
    auth();source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing recovery preserved'
    receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    assert receipt['source_sha256']==PINS['cross_u_ngc3198_partial_recovery_v002.py']
    for n,h in receipt['output_sha256'].items():assert sha(BASE/n)==h,('changed parent output',n)
    parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());assert receipt['result_sha256']==sha(BASE/(PARENT+'_RESULT.json')) and len(parent['cases'])==16
    original=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text());fixed=original['manifest']['fixed']
    screen=json.loads((BASE/'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text())
    counts={r['eps']:r['compatible_count'] for r in screen['rows']};assert counts=={1e-6:0,1e-5:18,1e-4:18,1e-3:18}
    manifest=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=source,input_sha256=PINS,
                  inherited_input_sha256=core.PINS,physics_changes=[],no_automatic_resume=True,
                  numerical_change='True-residual MINRES on frozen symmetric diagonal whitening',stationary_screen_counts=list(counts.items()))
    mh=write(STEM+'_MANIFEST.json',manifest);control=controls()
    if not all(t['passed'] for t in control):
        close(source,manifest,dict(status='IMPLEMENTATION_CONTROL_FAILED',controls=control,cases=[],joint_superiority_qualified=False));return 3
    results=[]
    for case in parent['cases']:
        old=case['identity'];name=old['case']
        if case['status']=='CONVERGED' or old['eps']==1e-6:
            result=dict(case,parent_copied_exactly=True,recovery_disposition='completed' if case['status']=='CONVERGED' else 'ineligible_necessary_stationary_width')
        else:
            x,partial,checkpoint_history,inputseal=recover(case,receipt)
            model=core.Model(np.array(old['r_kpc']),np.array(old['z_kpc']),32,old['eps'],fixed,core.density.profiles(old['hi_tail'],old['h2_tail']))
            assert x.shape==model.shape and np.all(x[~model.mask]==0)
            identity=dict(old,minres_manifest_sha256=mh,minres_source_sha256=source,parent_state=inputseal)
            result=solve(model,name,identity,x,partial)
            result.update(parent_case_history=case['history'],parent_checkpoint_history=checkpoint_history,
                          ancestral_history=case['ancestral_history'],ancestral_checkpoint_history=case['ancestral_checkpoint_history'])
        auth();assert source==sha(__file__);write(f'{STEM}_{name}_CASE.json',result);results.append(result)
        print('MINRES_CASE',name,result['status'],flush=True)
    close(source,manifest,dict(status='RECOVERY_OUTCOMES_RETAINED',controls=control,cases=results,joint_superiority_qualified=False))
    return 0 if all(c['status']=='CONVERGED' for c in results) else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    raise SystemExit(main())
