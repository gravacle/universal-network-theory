"""Guarded saved-only arithmetic; no mean law, angular rule or FE replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_ONCE_COUNTED_ORDINARY_MEAN_WEAK_LOADS_V001'
OUT='READONLY_ONCE_COUNTED_MEAN_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='6c6f31a382f884e84d303aa617788eb90f46c78c44ebcfb789499a1771ff2cc9'
PROTOCOL_SHA='7a405ed8fa42c79073cce5adce0dd4081469d21615b8147190c49baf5b5286ec'
TERMINAL=dict(pid=56727,result_sha256='2b8d9e27d7fdafad1ce6369e5c9c01ad87bd1cff2880f57e053c6ca4e6eb5f8e',receipt_sha256='9238701c16c637216c4d775bc74f8e2d66e578d5cc03fe3c9e6062ca97ca1120',error_sha256=None)
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def read_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert not path(OUT).exists()
 import numpy as np
 assert sha('cross_u_once_counted_ordinary_mean_weak_loads_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=read_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=read_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'])
 assert rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA and rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 records=r['checkpoints'];assert len({x['file'] for x in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={x['file'] for x in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={x['commit_file'] for x in records}
 data=[];array_count=elements=0
 for rec in records:
  assert rc['output_sha256'][rec['file']]==rec['sha256'] and rc['output_sha256'][rec['commit_file']]==rec['commit_sha256']
  assert read_json(rec['commit_file'],rec['commit_sha256'])=={k:rec[k] for k in ('file','sha256','metadata')}
  assert rec['metadata']['owner']==r['owner'] and rec['metadata']['qualification']==r['qualification']
  with np.load(path(rec['file']),allow_pickle=False) as f:
   sc=rec['metadata']['schema'];assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata'];raw={}
   for n,s in sc.items():
    a=f[n].copy();assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and a.dtype.kind in 'fiub' and bool(np.all(np.isfinite(a)))==s['finite'];raw[n]=a;array_count+=1;elements+=a.size
   data.append(raw)
 controls=r['controls'];assert [c['ordinal'] for c in controls]==list(range(len(controls)))
 control_errors=[]
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);found=[q for q in data if prefix+'actual' in q];assert len(found)==1;q=found[0];a,e,b=(q[prefix+n] for n in ('actual','expected','envelope'))
  assert a.shape==e.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(e)) and np.all(np.isfinite(b)) and np.all(b>=0)
  error=float(np.max(abs(a-e)/np.maximum(b,1e-30),initial=0));assert c['error']==error and c['tolerance']==TOL and c['passed']==(error<=TOL);control_errors.append(error)
 identities=[]
 def eq(name,a,e,extra=0):
  assert a.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(e));b=abs(a)+abs(e)+extra;error=float(np.max(abs(a-e)/np.maximum(b,1e-30),initial=0));assert error<=TOL,(name,error);identities.append(dict(name=name,error=error))
 if closed:
  assert len(records)==6 and len(controls)==12 and all(c['passed'] for c in controls) and r['conditional_source_branch_assembled'] is True and r['original_state_changed'] is False and r['original_primitive_bridge_admitted'] is False and r['mean_inventory_overlap_proven'] is False and r['physical_adoption'] is False
  inp=data[0];rhoB,rhoR=inp['mean_densities'];assert np.isfinite(rhoB) and np.isfinite(rhoR) and rhoB>0 and rhoR>0
  eq('saved_mass_sum',inp['current_mass_weight_full_sum'],np.array(math.fsum(map(float,inp['source_mass_weights']))));eq('saved_mass_conversion',inp['label_mass_radius'][1:2],np.array([float(inp['current_mass_weight_full_sum'])*float(inp['registered_weight_to_Msun_conversion'])]))
  for iq,q in enumerate(data[1:5]):
   md=records[iq+1]['metadata'];assert md['column']==iq and md['canonical_momentum_density_exact_zero_by_antipodal_symmetry'] is True and md['finite_compensation_selected'] is False and md['physical_preparation_admitted'] is False
   R=q['current_R'];N=q['current_N'];mu=q['current_sqrt_h'];assert R.shape==N.shape==mu.shape==(3784,) and np.all(R>0) and np.all(N>0) and np.all(mu>0)
   DB=q['reference_coordinate_dust_density'];DR=q['reference_radiation_energy_measure'];EB=q['dust_coordinate_energy'];ER=q['radiation_coordinate_energy'];S=q['radiation_contravariant_stress_density']
   eq('column_%d_saved_D_B'%iq,DB,rhoB*R);eq('column_%d_saved_radiation_measure'%iq,DR,rhoR*R);eq('column_%d_dust_energy'%iq,EB,DB);eq('column_%d_radiation_energy'%iq,ER,DR*q['angular_energy_fine']);eq('column_%d_radiation_stress'%iq,S,DR[:,None,None]*q['angular_stress_fine'])
   eq('column_%d_dust_density'%iq,q['dust_physical_energy']*mu,EB);eq('column_%d_radiation_density'%iq,q['radiation_physical_energy']*mu,ER)
   normal=q['mean_normal_coordinate_densities'];assert normal.shape==(3784,4);eq('column_%d_lapse_energy'%iq,normal[:,0],EB+ER);assert np.all(normal[:,1:]==0)
   tensor=N[:,None,None]*S/2;expected=np.stack([tensor[:,a,b]*(1 if a==b else 2) for a,b in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=1);eq('column_%d_positive_N_stress_metric_force'%iq,q['mean_metric_configuration_force'],expected)
   assert np.all(q['normal_envelope']>=0) and np.all(q['metric_envelope']>=0)
  q=data[5];md=records[5]['metadata'];assert md['original_state_changed'] is False and md['physical_exterior'] is None and md['finite_pure_FLRW_wall'] is False and md['physical_history'] is None and md['activity_outside_0_3_to_15_1'] is None
  old=q['original_normal_rows_hi']+q['original_normal_rows_lo'];branch=q['branch_normal_rows_hi']+q['branch_normal_rows_lo'];mean=q['mean_normal_rows'];eq('preserved_old_plus_new_conditional_rows',branch,old+mean,abs(q['original_normal_rows_hi'])+abs(q['original_normal_rows_lo']))
  eq('fixed_D_dust_Q1_saved_analytic_identity',q['fixed_reference_dust_normal_rows'],q['analytic_fixed_reference_dust_rows'])
  summary={}
  for name,a in (('original_normal',old),('new_mean_normal',mean),('conditional_branch_normal',branch),('mean_metric_configuration_force',q['mean_metric_configuration_force_rows'])):
   summary[name]=[dict(L2=float(np.linalg.norm(x)),Linf=float(np.max(abs(x),initial=0)),signed_min=float(np.min(x,initial=0)),signed_max=float(np.max(x,initial=0))) for x in a]
  report=dict(status='SAVED_ONCE_COUNTED_MEAN_CLOSURE_PASS',parent_status=r['status'],owner_pid=os.getpid(),parent=TERMINAL,controls=12,committed_pairs=6,arrays=array_count,elements=elements,identities=identities,maximum_control_error=max(control_errors),row_norms_descriptive=summary,copied_Mgal_Msun=r['copied_Mgal_Msun'],conditional_label_RL_kpc=r['conditional_label_RL_kpc'],original_primitive_bridge_admitted=False,mean_inventory_overlap_proven=False,physical_adoption=False,mean_law_angular_fixture_FE_or_operator_replayed=False)
 else:report=dict(status='SAVED_ONCE_COUNTED_MEAN_FAILURE_PRESERVED',owner_pid=os.getpid(),parent=TERMINAL,controls=controls,committed_pairs=len(records),arrays=array_count,elements=elements,physical_adoption=False,mean_law_angular_fixture_FE_or_operator_replayed=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
