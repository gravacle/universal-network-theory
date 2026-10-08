"""Recover V001 accepted fields and unfinished linear directions; same physics."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,time
import numpy as np
import cross_u_ngc3198_nonlinear_disk_v001 as core

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_PARTIAL_RECOVERY_V002'
ANCESTOR='CROSS_U_NGC3198_NONLINEAR_DISK_V001'
ANCESTOR_SOURCE='ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1'
PROTOCOL_SHA='c236db1e798d4df086460e880d3515612dea127335eb85c4defde842e4589400'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def auth():
    assert PROTOCOL_SHA and sha(BASE/(STEM+'.md'))==PROTOCOL_SHA
    assert sha(BASE/'cross_u_ngc3198_nonlinear_disk_v001.py')==ANCESTOR_SOURCE
    core.authenticate()
def write(name,obj):return core.publish(name,obj)
def state(name,step,x,history,identity,partial=None):
    tail=f'STEP_{step:03d}' if partial is None else f'LINEAR_FAILED_{step:03d}'
    namefile=f'{STEM}_{name}_{tail}.npz';p=BASE/namefile
    ht=json.dumps(history,allow_nan=False);it=json.dumps(identity,sort_keys=True,allow_nan=False)
    with p.open('xb') as f:
        fields=dict(state=x,history=ht,identity=it)
        if partial is not None:fields['unaccepted_linear_partial']=partial
        np.savez_compressed(f,**fields);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);write(namefile+'.commit.json',dict(file=namefile,sha256=sha(p),identity=identity))

def recover_input(case,receipt):
    name=case['identity']['case'];files=receipt['output_sha256']
    failed=sorted(BASE.glob(f'{ANCESTOR}_{name}_LINEAR_FAILED_*.npz'))
    completed=sorted(BASE.glob(f'{ANCESTOR}_{name}_STEP_*.npz'))
    path=failed[-1] if failed else completed[-1]
    commit=path.with_name(path.name+'.commit.json')
    assert files[path.name]==sha(path) and files[commit.name]==sha(commit)
    c=json.loads(commit.read_text());assert c['sha256']==sha(path) and c['identity']==case['identity']
    with np.load(path,allow_pickle=False) as npz:
        x=npz['state'].copy();history=json.loads(str(npz['history']));identity=json.loads(str(npz['identity']))
        partial=npz['unaccepted_linear_partial'].copy() if 'unaccepted_linear_partial' in npz else None
    assert identity==case['identity'] and np.all(np.isfinite(x))
    return x,partial,history,dict(file=path.name,sha256=sha(path),commit_sha256=sha(commit))

def solve(model,name,identity,x,partial,old_history):
    tick=time.monotonic();history=[];state(name,0,x,history,identity)
    r0,p0,_=model.residual(np.zeros(model.shape));scale=float(np.linalg.norm(model.rhs/np.sqrt(p0)))
    status='NEWTON_ALLOWANCE';used_partial=False
    for outer in range(40):
        r,pre,H=model.residual(x);root=np.sqrt(pre);rhs=-r/root
        error=float(np.linalg.norm(rhs)/scale)
        if error<=1e-8:status='CONVERGED';break
        tolerance=min(.5,max(1e-6,.5*math.sqrt(error)))
        def A(v):return H(v/root)/root
        seed_rejection=None
        valid=outer==0 and partial is not None and partial.shape==rhs.shape and np.all(np.isfinite(partial)) and np.all(partial[~model.mask]==0)
        seed=partial if valid else np.zeros_like(rhs)
        if outer==0 and partial is not None and not valid:seed_rejection='partial_shape_mask_or_finite_guard'
        action=A(seed)
        seed_error=float(np.linalg.norm(rhs-action)/np.linalg.norm(rhs))
        if not np.all(np.isfinite(action)) or not math.isfinite(seed_error):
            seed_rejection='nonfinite_partial_action';seed=np.zeros_like(rhs);action=np.zeros_like(rhs);seed_error=1.
        if seed_error<=tolerance:
            delta=seed.copy();details=dict(ok=True,iterations=0,error=seed_error,reason='authenticated_partial_recovered')
            used_partial=True
        else:
            rem=rhs-action;ratio=float(np.linalg.norm(rhs)/np.linalg.norm(rem))
            correction,details=core.bicgstab(A,rem,tolerance*ratio,600)
            delta=seed+correction
            true_error=float(np.linalg.norm(rhs-A(delta))/np.linalg.norm(rhs)) if np.all(np.isfinite(delta)) else math.inf
            details=dict(details,ok=math.isfinite(true_error) and true_error<=tolerance,
                         error=true_error if math.isfinite(true_error) else None,seed_error=seed_error)
        row=dict(outer=outer,error=error,inexact_target=tolerance,linear=details,partial_rejection=seed_rejection)
        if not details['ok']:
            history.append(row);state(name,outer,x,history,identity,delta);status='LINEAR_FAILED';break
        delta/=root;accepted=False
        for back in range(32):
            step=2.**(-back);candidate=x+step*delta
            try:
                cr,_=model.residual(candidate,False);candidate_error=float(np.linalg.norm(cr/root)/scale)
            except ValueError:continue
            if math.isfinite(candidate_error) and candidate_error<=(1-1e-4*step)*error:
                x=candidate;accepted=True;row.update(step=step,candidate_error=candidate_error);break
        row['accepted']=accepted;history.append(row)
        if not accepted:status='GLOBALIZATION_FAILED';break
        state(name,outer+1,x,history,identity)
        print('RECOVERY',name,'NEWTON',outer+1,'ERROR',candidate_error,'STEP',step,flush=True)
    r,pre,_=model.residual(x);error=float(np.linalg.norm(r/np.sqrt(pre))/scale)
    if error<=1e-8:status='CONVERGED'
    force=np.gradient(x[0,:,0],model.r,edge_order=2);rows=[]
    for obs in core.observation_rows():
        g=float(np.interp(obs['R'],model.r,force));v2=obs['R']*core.A0_V*g
        v=math.sqrt(v2) if v2>=0 else None
        rows.append(dict(obs,radial_force_a0=g,velocity_squared=v2,model_velocity=v,
                         residual=None if v is None else v-obs['velocity']))
    return dict(identity=identity,status=status,numerical_residual=error,history=history,ancestral_history=old_history,
                unfinished_partial_used=used_partial,rows=rows,elapsed_seconds=time.monotonic()-tick,
                physical_flags=dict(refinement_qualified=False,full_metric_qualified=False,
                                    FLRW_junction_qualified=False,formation_qualified=False,joint_superiority_qualified=False))

def main():
    auth();source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing recovery preserved'
    rp=BASE/(ANCESTOR+'_RECEIPT.json');receipt=json.loads(rp.read_text())
    assert receipt['source_sha256']==ANCESTOR_SOURCE
    for n,h in receipt['output_sha256'].items():assert sha(BASE/n)==h,('changed ancestor output',n)
    parent=json.loads((BASE/(ANCESTOR+'_RESULT.json')).read_text())
    assert receipt['result_sha256']==sha(BASE/(ANCESTOR+'_RESULT.json')) and len(parent['cases'])==16
    fixed=parent['manifest']['fixed']
    manifest=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=source,
                  ancestor_receipt_sha256=sha(rp),ancestor_result_sha256=receipt['result_sha256'],
                  ancestor_source_sha256=ANCESTOR_SOURCE,protocol_sha256=PROTOCOL_SHA,
                  physics_changes=[],numerical_change='Authenticated incomplete direction and inexact Newton forcing eta<=.5',
                  no_automatic_resume=True,old_completed_cases_not_repeated=True)
    mh=write(STEM+'_MANIFEST.json',manifest);results=[]
    for case in parent['cases']:
        name=case['identity']['case']
        if case['status']=='CONVERGED':
            result=dict(case,completed_ancestor_copied=True)
        else:
            x,partial,old_history,inputseal=recover_input(case,receipt)
            old=case['identity'];r=np.array(old['r_kpc']);z=np.array(old['z_kpc'])
            model=core.Model(r,z,32,old['eps'],fixed,core.density.profiles(old['hi_tail'],old['h2_tail']))
            assert x.shape==model.shape and np.all(x[~model.mask]==0)
            identity=dict(old,recovery_manifest_sha256=mh,recovery_source_sha256=source,ancestral_state=inputseal)
            result=solve(model,name,identity,x,partial,case['history'])
            result['ancestral_checkpoint_history']=old_history
        auth();assert sha(__file__)==source
        write(STEM+'_'+name+'_CASE.json',result);results.append(result)
        print('RECOVERY_CASE',name,result['status'],flush=True)
    passed=all(r['status']=='CONVERGED' for r in results)
    status='RESIDUALS_PASS_UNQUALIFIED' if passed else 'RECOVERY_FAILURES_RETAINED'
    rh=write(STEM+'_RESULT.json',dict(status=status,manifest=manifest,cases=results,joint_superiority_qualified=False))
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    write(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),source_sha256=source,started=manifest['started'],
                                 closed=now(),result_sha256=rh,output_sha256=outputs))
    print('RECOVERY_BATCH_CLOSED',status,flush=True);return 0 if passed else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    raise SystemExit(main())
