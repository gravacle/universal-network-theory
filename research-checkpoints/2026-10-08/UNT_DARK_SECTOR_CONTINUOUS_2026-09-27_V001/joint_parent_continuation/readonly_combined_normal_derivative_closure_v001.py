"""Guarded selected saved words only; no contact/feature/FE/operator replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMBINED_CONFIGURATION_NORMAL_DERIVATIVE_V001'
OUT='READONLY_COMBINED_NORMAL_DERIVATIVE_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='e139a418838005d8db5498ccacca6afeed0092628a96886d61d7b5f3a86d49d0'
PROTOCOL_SHA='4d49c10d595c2642d41d4fb7a8bb3a833660b86b911a81756a5b575f9e02718a'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def saved_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists()
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_combined_configuration_normal_derivative_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=saved_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=saved_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'])
 assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,k in ((q['file'],'sha256'),(q['commit_file'],'commit_sha256')):assert rc['output_sha256'][n]==q[k] and sha(n)==q[k]
  assert saved_json(q['commit_file'],q['commit_sha256'])=={n:q[n] for n in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False and all(s['finite'] is True for s in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=4 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 import numpy as np
 selected=[];identities=[]
 def read(q,names):
  schema=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as z:
   assert set(z.files)==set(schema)|{'metadata_json'} and json.loads(str(z['metadata_json']))==q['metadata']
   for n in names:
    x=z[n].copy();assert list(x.shape)==schema[n]['shape'] and str(x.dtype)==schema[n]['dtype'] and schema[n]['finite'] is True and np.all(np.isfinite(x)),n;out[n]=x
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(x):return x[0]+x[1]
 def identity(name,terms):
  values=[sign*v for sign,x in terms for v in x];gap=np.add.reduce(values);bound=np.add.reduce([abs(v) for v in values]);error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0))
  assert error<=TOL,(name,error);identities.append(dict(name=name,error=error))
 def norms(x):
  assert x.shape==(4,87,45);return [dict(L2=float(np.linalg.norm(v)),Linf=float(np.max(abs(v),initial=0)),nonzero=int(np.count_nonzero(v))) for v in x]
 triplets={}
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found
  rows=[read(q,names) for q in found];a=rows[0];assert all(all(np.array_equal(a[n],b[n]) for n in names) for b in rows)
  x,y,e=(a[n] for n in names);assert x.shape==y.shape==e.shape and np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];triplets[c['ordinal']]=(x,y,e);identities.append(dict(name=c['name'],error=error))
 if not closed:report=dict(status='SAVED_COMBINED_NORMAL_DERIVATIVE_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  assert r['status']=='COMBINED_SAME_ACTION_NORMAL_CONFIGURATION_DERIVATIVE_MEASURED' and len(controls)==4 and all(c['passed'] for c in controls) and len(records)==7
  assert all(r[n] is False for n in ('primitive_bridge_resolved','normal_constraints_qualified','finite_configuration_adopted','physical_adoption'))
  inp,fixture,columns,loads=r['input'],r['fixture'],r['columns'],r['loads'];assert inp in records and fixture in records and loads in records and len(columns)==4 and all(q in records for q in columns)
  assert fixture['metadata']['controls']==controls[:3] and loads['metadata']['controls']==controls[3:] and loads['metadata']['configuration_updated'] is False and loads['metadata']['old_normal_or_mean_rows_added'] is False and loads['metadata']['original_primitive_bridge_resolved'] is False
  phase_names=tuple(n+'_'+w for n in ('registered_normal_weak_Hamiltonian_rows','literal_action_weak_Hamiltonian_rows','literal_minus_registered_weak_normal_gap') for w in ('hi','lo'))
  families=('configuration','rate','mean');bases=tuple(n+'_weak_Hamiltonian_contact' for n in families)+('earned_phase_registered_weak_Hamiltonian_contact','combined_weak_Hamiltonian_contact')
  functionals=tuple(part+'_new_functional_'+kind for part in families for kind in ('nodal','direct','gap'))
  names=tuple(n+'_'+w for n in bases+functionals for w in ('hi','lo'))+tuple('copied_'+n for n in phase_names);a=read(loads,names)
  for n in bases:assert pair(a,n)[0].shape==pair(a,n)[1].shape==(4,87,45)
  identity('combined_configuration_rate_mean_phase_sum',[(1,pair(a,n)) for n in bases[:-1]]+[(-1,pair(a,bases[-1]))])
  for part in families:identity(part+'_stored_nodal_direct_difference',[(1,pair(a,part+'_new_functional_nodal')),(-1,pair(a,part+'_new_functional_direct')),(-1,pair(a,part+'_new_functional_gap'))])
  gaps=np.asarray([float(total(pair(a,part+'_new_functional_gap'))) for part in families]);assert np.array_equal(gaps,triplets[3][0]) and np.all(triplets[3][1]==0)
  ref=loads['metadata']['earned_phase_contact_ref'];assert inp['metadata']['admitted_refs']['phase_normal_loads']==ref
  for n,k in ((ref['file'],'sha256'),(ref['commit_file'],'commit_sha256')):assert rc['input_sha256'][n if n in rc['input_sha256'] else str(path(n).resolve())]==ref[k] and sha(n)==ref[k]
  # Read only six earned phase words, without loading or traversing its large
  # metadata/scalar-prefix inventory or reconstructing any old contraction.
  with np.load(path(ref['file']),allow_pickle=False) as z:
   for n in phase_names:
    x=z[n];assert x.shape==(4,87,45) and x.dtype==np.float64 and np.all(np.isfinite(x)) and np.array_equal(x,a['copied_'+n]),n
  for w in ('hi','lo'):assert np.array_equal(a['earned_phase_registered_weak_Hamiltonian_contact_'+w],a['copied_registered_normal_weak_Hamiltonian_rows_'+w])
  identity('copied_literal_registered_phase_gap',[(1,pair(a,'copied_literal_action_weak_Hamiltonian_rows')),(-1,pair(a,'copied_registered_normal_weak_Hamiltonian_rows')),(-1,pair(a,'copied_literal_minus_registered_weak_normal_gap'))])
  time_norms=[]
  for iq,q in enumerate(columns):
   assert q['metadata']['column']==iq and q['metadata']['config_and_rate_parts_kept_separate'] is True and q['metadata']['ordinary_sheet_contact_zero_offsheet'] is True and q['metadata']['temporal_primary_contacts_retained'] is True
   bs=('configuration_action_coefficients','rate_action_coefficients','mean_Hamiltonian_coefficients');b=read(q,tuple(n+'_'+w for n in bs for w in ('hi','lo')))
   stats={}
   for n in bs:
    x=total(pair(b,n));assert x.shape==(3784,4,4);stats[n]=[dict(L2=float(np.linalg.norm(v)),Linf=float(np.max(abs(v),initial=0))) for v in x[:,:,3].T]
   time_norms.append(dict(column=iq,per_row_time_coefficient_norms=stats))
  report=dict(status='SAVED_COMBINED_NORMAL_DERIVATIVE_CLOSURE_PASS',controls=4,committed_pairs=7,component_weak_norms={n:norms(total(pair(a,n))) for n in bases},time_coefficient_norms=time_norms,original_primitive_bridge_resolved=False,normal_constraints_qualified=False,reachable_rank_or_five_field_admission_claimed=False,phase_time_coefficient_norms_independently_measured=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_tolerance=TOL,old_input_maps_rehashed=False,scope_limit='Selected saved words, triplets, sums and descriptive norms; no point contact, feature, phase formula, FE scatter, operator or fixture replay',old_contact_feature_FE_operator_solver_or_fixture_replayed=False,physical_adoption=False)
 for q in records:
  assert sha(q['file'])==q['sha256'] and sha(q['commit_file'])==q['commit_sha256']
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha('cross_u_combined_configuration_normal_derivative_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
