"""Guarded saved-only D0 audit. Definitions/compile only in authoring."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='ROOT_SAVED_WEAK_CANONICAL_MOMENTUM_TIME_DERIVATIVE_V001_AUDIT'
PARENT='CROSS_U_WEAK_CANONICAL_MOMENTUM_TIME_DERIVATIVE_V001'
AUTHOR_DRAFT=True
PROTOCOL_SHA=None
TERMINAL=dict(pid=38115,source_sha256='c653708fb4e86057fe589c24c5cf3902ada0f53ac76e9023de6e16e04407ed7b',protocol_sha256='8da1c2e485b7769ace5d6ca50d6703720f3e5c5db9c4fc01f156aa2114b41ad7',result_sha256=None,receipt_sha256=None)
TOL=2e-11;C=1.98
np=None;OWNER=None;INPUTS={};OUTPUTS={};TESTS=[];CONTEXT={}
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def publish(n,v):
 raw=(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[n]=sha(p);return OUTPUTS[n]
def identity(name,a,b,e):
 CONTEXT.update(identity=name);assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 ratio=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));TESTS.append(dict(name=name,entries=int(a.size),error=ratio,tolerance=TOL,passed=ratio<=TOL));assert ratio<=TOL,(name,ratio)
def read(rec,names):
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json']))==rec['metadata'];return {k:f[k].copy() for k in names}
def admit():
 assert type(TERMINAL['pid']) is int and all(type(TERMINAL[k]) is str and len(TERMINAL[k])==64 for k in ('source_sha256','protocol_sha256','result_sha256','receipt_sha256')),'Natural parent CLOSED terminal must be bound.'
 names={'cross_u_weak_canonical_momentum_time_derivative_v001.py':TERMINAL['source_sha256'],PARENT+'.md':TERMINAL['protocol_sha256'],PARENT+'_RESULT.json':TERMINAL['result_sha256'],PARENT+'_RECEIPT.json':TERMINAL['receipt_sha256']}
 for n,h in names.items():assert sha(path(n))==h
 rr=json.loads(path(PARENT+'_RESULT.json').read_text());rc=json.loads(path(PARENT+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==TERMINAL['result_sha256'] and rr['owner']==rc['owner'] and rr['owner']['pid']==TERMINAL['pid'] and rr['owner']['source_sha256']==TERMINAL['source_sha256']
 assert rr['status']=='CONDITIONAL_D0_KNOWN_FORCE_WEAK_ARITHMETIC_PASS' and len(rr['controls'])==33 and len(rr['checkpoints'])==8 and all(v is False for v in rr['qualification'].values())
 assert len(rr['cases'])==1 and rr['cases'][0]['sigma']==1. and rr['cases'][0]['qualification']==rr['qualification']
 # One complete terminal admission, one hash per unique path. No nested rewalk.
 for mapping in (rc['input_sha256'],rc['output_sha256'],names):
  for n,h in mapping.items():
   key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h;INPUTS[key]=h
 for n,h in INPUTS.items():assert sha(n)==h,n
 recs=rr['checkpoints']
 for rec in recs:
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
  assert rec['metadata']['owner']==rr['owner'] and rec['metadata']['failed'] is False
 assert [r['file'].rsplit('_',1)[-1] for r in recs]==['INPUT.npz','FIXTURE.npz','BASIS.npz','COLUMN.npz','COLUMN.npz','COLUMN.npz','COLUMN.npz','LOADS.npz']
 assert {p.name for p in BASE.glob(PARENT+'_*.npz')}=={r['file'] for r in recs} and {p.name for p in BASE.glob(PARENT+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in recs}
 return rr,recs

def census_and_controls(rr,recs):
 count=entries=negative=0;seen={}
 for rec in recs:
  CONTEXT.update(file=rec['file'],stage='saved_schema_finite_control_census')
  with np.load(path(rec['file']),allow_pickle=False) as f:
   schema=rec['metadata']['schema'];assert set(f.files)==set(schema)|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata']
   for k,desc in schema.items():
    a=f[k];assert list(a.shape)==desc['shape'] and str(a.dtype)==desc['dtype'] and bool(np.all(np.isfinite(a)))==desc['finite'] and desc['finite'] is True
    assert a.dtype.kind in 'fiub';count+=1;entries+=int(a.size);negative+=int(np.count_nonzero(a<0))
   for row in rec['metadata'].get('controls',[]):
    i=row['ordinal'];assert i not in seen and row==rr['controls'][i] and row['passed'] is True and row['tolerance']==TOL
    key=f"control_{i:03d}_{row['name']}_";a,b,e=(f[key+x] for x in ('actual','expected','envelope'))
    identity('original_raw_gate_'+str(i),a,b,e);assert TESTS[-1]['error']==row['error'];seen[i]=row
 assert set(seen)==set(range(33))
 return dict(pairs=8,numeric_arrays=count,numeric_entries=entries,signed_negative_entries=negative,controls=33)

def audit_column(iq,rec):
 CONTEXT.update(column=iq,stage='new_saved_derivative_identities');parent=rec['metadata']['parent'];fr=json.loads(path(parent['commit_file']).read_text())
 assert fr['file']==parent['file'] and fr['sha256']==parent['sha256']
 names=('seed_Pi','seed_PiU','seed_connection_momentum','seed_chart_dens','seed_chart_JU','seed_chart_JzU','seed_chart_Jzz','seed_chart_Uh','seed_chart_zh','seed_chart_embed','seed_chart_h','seed_chart_ih','seed_chart_N','seed_chart_K','seed_chart_Ktrace','seed_chart_sqrt_h','seed_chart_u','seed_chart_up','seed_phase_PX','seed_phase_PXX','seed_phase_X','seed_nodal_native_rate','seed_metric_L2_rate','new_native_momentum','new_metric_native_momentum','new_metric_EH_momentum','new_phase_canonical_density')
 a=read(fr,names)
 with np.load(path(rec['file']),allow_pickle=False) as f:
  def q(n):return f[n]
  dl=q('D0_intercept_D0_chart_log_dens');ds=a['seed_chart_dens'];Pi,PU=a['seed_Pi'],a['seed_PiU'];dPi=q('D0_intercept_D0_native_Pi');dPU=q('D0_intercept_D0_native_PiU')
  du=np.einsum('pa,pai->pi',dPU[:,0],a['seed_chart_JU'])+np.einsum('pa,pai->pi',PU[:,0],q('D0_intercept_D0_chart_JU'))+np.einsum('jp,jpi->pi',dPi[:,:,0,0],a['seed_chart_JzU'])+np.einsum('jp,jpi->pi',Pi[:,:,0,0],q('D0_intercept_D0_chart_JzU'))
  dz=dPi[:,:,0,1:]+dPi[:,:,0,0,None]*a['seed_chart_Jzz'][None]+Pi[:,:,0,0,None]*q('D0_intercept_D0_chart_Jzz')[None]
  dn=dl[:,None]*a['new_native_momentum']+ds[:,None]*np.concatenate((du,dz.transpose(1,0,2).reshape(3784,96)),axis=1)
  identity('column_'+str(iq)+'_native_direct_canonical_chain',dn,q('D0_native_intercept'),q('D0_native_intercept_envelope'))
  CT=a['seed_connection_momentum'][:,0];dCT=q('D0_intercept_D0_native_connection_momentum')[:,0]
  dm=np.einsum('pmn,pkmn->pk',dCT,a['seed_chart_embed'])+np.einsum('pmn,pkmn->pk',CT,q('D0_intercept_D0_chart_embed'))+np.einsum('pa,pka->pk',dPU[:,0],a['seed_chart_Uh'])+np.einsum('pa,pka->pk',PU[:,0],q('D0_intercept_D0_chart_Uh'))+np.einsum('jp,jpk->pk',dPi[:,:,0,0],a['seed_chart_zh'])+np.einsum('jp,jpk->pk',Pi[:,:,0,0],q('D0_intercept_D0_chart_zh'))
  dm=dl[:,None]*a['new_metric_native_momentum']+ds[:,None]*dm
  identity('column_'+str(iq)+'_native_metric_direct_canonical_chain',dm,q('D0_metric_native_intercept'),q('D0_intercept_metric_native_envelope'))
  for field in ('native','metric_native'):
   identity('column_'+str(iq)+'_intercept_'+field+'_product_sum',q('D0_intercept_'+field+'_terms').sum(axis=-1),q('D0_intercept_'+field),q('D0_intercept_'+field+'_envelope'))
   identity('column_'+str(iq)+'_twelve_gauge_'+field+'_product_sum',q('first_gauge_'+field+'_product_terms').sum(axis=-1),q('first_gauge_'+field+'_coefficients'),q('first_gauge_'+field+'_envelope'))
  owned=q('owned_gauge_value_jets');gn=q('first_gauge_native_coefficients');gm=q('first_gauge_metric_native_coefficients')+q('first_gauge_metric_EH_coefficients')
  identity('column_'+str(iq)+'_owned_native_gauge_values',q('D0_native_intercept')+np.einsum('pa,api->pi',owned,gn[:4]),q('D0_native_registered_gauge_values'),q('D0_native_registered_gauge_values_envelope'))
  identity('column_'+str(iq)+'_owned_metric_gauge_values',q('D0_metric_total_intercept')+np.einsum('pa,api->pi',owned,gm[:4]),q('D0_metric_registered_gauge_values'),q('D0_metric_registered_gauge_values_envelope'))
  k=a['seed_metric_L2_rate'];ih=a['seed_chart_ih'];v=a['seed_nodal_native_rate'];up=a['seed_chart_up'];u=a['seed_chart_u'];mu=a['seed_chart_sqrt_h'];N=a['seed_chart_N'];X=a['seed_phase_X'];PX=a['seed_phase_PX'];PXX=a['seed_phase_PXX']
  b=np.einsum('pi,pi->p',u,up);theta=np.einsum('pij,pij->p',ih,k)/2;bdot=2*np.einsum('pi,pi->p',up,v[:,:3])-np.einsum('pi,pij,pj->p',up,k,up);slope=PXX-b;assert np.all(slope>0)
  expected=np.column_stack((mu*(PX-X*b),mu*(theta*(PX-X*b)-X*bdot),-mu*slope*X/N,mu*slope/N))
  actual=np.column_stack((q('phase_registered_charge_density'),q('phase_mechanical_charge_rate'),q('phase_lapse_velocity_coefficient'),q('phase_phi_tt_coefficient')))
  bound=np.column_stack((mu*(abs(PX)+abs(X)*np.einsum('pi,pi->p',abs(u),abs(up))),mu*((np.einsum('pij,pij->p',abs(ih),abs(k))/2)*(abs(PX)+abs(X)*np.einsum('pi,pi->p',abs(u),abs(up)))+abs(X)*(2*np.einsum('pi,pi->p',abs(up),abs(v[:,:3]))+np.einsum('pi,pij,pj->p',abs(up),abs(k),abs(up)))),mu*(abs(PXX)+abs(b))*abs(X)/N,mu*(abs(PXX)+abs(b))/N))
  identity('column_'+str(iq)+'_exact_phase_charge_coefficients',actual,expected,bound)
  return dict(native=q('D0_native_registered_gauge_values').copy(),metric=q('D0_metric_registered_gauge_values').copy(),native_envelope=q('D0_native_registered_gauge_values_envelope').copy(),metric_envelope=q('D0_metric_registered_gauge_values_envelope').copy())

def audit_loads(rec):
 parent='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RESULT.json';rr=json.loads(path(parent).read_text());old=rr['checkpoints'][-1]
 a=read(old,('native_spatial_Euler_load','native_spatial_Euler_envelope','complete_known_metric_spatial_Euler_load','complete_known_metric_spatial_Euler_envelope'))
 with np.load(path(rec['file']),allow_pickle=False) as f:
  for field,key in (('native','native_spatial_Euler'),('metric','complete_known_metric_spatial_Euler')):
   expected=a[key+'_load']-f['D0_'+field+'_registered_gauge_values_load'];identity('new_weak_'+field+'_E_minus_D0p',f['known_'+field+'_E_minus_D0p_load'],expected,f['known_'+field+'_E_minus_D0p_envelope'])
  phase=f['current_phase_current_density'];assert phase.shape==(15136,4) and np.all(np.isfinite(phase))

def main():
 global np,OWNER
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args();assert args.root_run and not AUTHOR_DRAFT
 assert PROTOCOL_SHA and sha(path(STEM+'.md'))==PROTOCOL_SHA and not list(BASE.glob(STEM+'_*'))
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(__file__));publish(STEM+'_OWNER_START.json',OWNER)
 try:
  import numpy as np_local
  np=np_local;rr,recs=admit();cen=census_and_controls(rr,recs)
  for iq,rec in enumerate(recs[3:7]):audit_column(iq,rec)
  audit_loads(recs[7]);assert len(TESTS)==71 and all(x['passed'] for x in TESTS)
  for n,h in INPUTS.items():assert sha(n)==h
  out=dict(status='SAVED_D0_PACKET_AUDIT_PASS',owner=OWNER,terminal=TERMINAL,census=cen,identities=TESTS,input_sha256=INPUTS,scope='saved contractions only; no producer/helper/feature/velocity/operator/Gram/solve/eigen/evolution replay',physical_qualification=rr['qualification'])
  result=publish(STEM+'.json',out);publish(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=datetime.now(timezone.utc).isoformat(),result_sha256=result,input_sha256=INPUTS,output_sha256=OUTPUTS));return 0
 except BaseException:
  error=publish(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=traceback.format_exc(),context=CONTEXT,identities=TESTS,input_sha256=INPUTS,output_sha256=OUTPUTS));publish(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=datetime.now(timezone.utc).isoformat(),error_sha256=error,input_sha256=INPUTS,output_sha256=OUTPUTS));return 1
if __name__=='__main__':raise SystemExit(main())
