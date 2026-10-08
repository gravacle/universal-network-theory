"""Saved scalar response words only; no mass, EOS, FE, solver or jet replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PHASE_FIXED_WEAK_CHARGE_LINEAR_RESPONSE_V001'
OUT='READONLY_PHASE_LINEAR_RESPONSE_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='82f5d4ee170f0cf2b3cc2a17e38c93d810ba8416d6c8a823bbe7affe058b32ff'
PROTOCOL_SHA='816e73375cfdcbba92d4f7d913b4c76c03b6902bc908512898612dda3e741edf'
TERMINAL=dict(pid=59963,result_sha256='633bc7777a48549f37a1c74b7d699827249034c5500b5dd9100c7e973b6f5bd5',receipt_sha256='af1047d9fca4eaf59a7c78bd1d965622dce0168041637a1cb17c96476eccd363',error_sha256=None)
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists()
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_phase_fixed_weak_charge_linear_response_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['owner']['pid']==TERMINAL['pid'] and rc['owner']['source_sha256']==SOURCE_SHA
 r=load_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert r['owner']==rc['owner'] and rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256'] and load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')}
  assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and all(v['finite'] is True for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 import numpy as np
 identities=[];selected=[]
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms):
  arrays=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(arrays);bound=np.add.reduce([abs(v) for v in arrays]);e=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert e<=TOL,(label,e);identities.append(dict(name=label,error=e))
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,(c['ordinal'],names)
  witnesses=[read(q,names) for q in found];a=witnesses[0];assert all(all(np.array_equal(a[n],b[n]) for n in names) for b in witnesses)
  x,y,b=(a[n] for n in names);assert np.all(b>=0);e=float(np.max(abs(x-y)/np.maximum(b,1e-30),initial=0));assert e==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=e))
 if not closed:report=dict(status='SAVED_PHASE_LINEAR_RESPONSE_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  kinds=('earned_positive_literal_phase_mass_and_original_compact_minus_Q_RHS','independent_uniform_Q1_scalar_mass_solver_control','paired_scalar_3870_linearized_fixed_weak_charge_response','same_Q1_scalar_phase_velocity_increment_value_and_spatial_jets')
  roles=[]
  for kind in kinds:
   match=[q for q in records if q['metadata']['kind']==kind];assert len(match)==1,kind;roles.append(match[0])
  inp,fixture,sol,jets=roles;assert r['solution']==sol and r['rate_jets']==jets and len(controls)==2 and all(c['passed'] for c in controls)
  assert all(q in roles or q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' for q in records)
  assert r['actual_budget']==sol['metadata']['actual_budget']==dict(cycles=1,cap=160) and len(r['history'])==1 and r['history'][0]['cycle']==1 and r['history'][0]['cap']==160
  assert sol['metadata']['history']==r['history'] and sol['metadata']['response_admitted']==jets['metadata']['response_admitted']==r['response_rows_admitted']
  assert sol['metadata']['finite_charge_restored'] is False and sol['metadata']['configuration_updated'] is False and sol['metadata']['physical_adoption'] is False and jets['metadata']['baseline_phi_t_and_spatial_gradients_not_replaced'] is True and jets['metadata']['instantaneous_phi_i_unchanged'] is True
  assert all(r[n] is False for n in ('finite_phase_charge_restored','configuration_updated','physical_adoption'))
  mask=np.ones((87,45),bool);mask[0]=False;assert np.count_nonzero(mask)==3870
  ia=read(inp,tuple(n+'_'+w for n in ('fixed_weak_phase_velocity_rhs','new_phase_mass_diagonal','fixed_literal_weak_phase_charge') for w in ('hi','lo')))
  p='actual_phase_response';cy=p+'_cycle_001';up=cy+'_trial_update'
  names=tuple(sol['metadata']['schema']);a=read(sol,names);s=lambda n:pair(a,n)
  assert s('phase_velocity_nodal')[0].shape==s('phase_velocity_nodal')[1].shape==(87,45) and np.all(s('phase_velocity_nodal')[0][0]==0) and np.all(s('phase_velocity_nodal')[1][0]==0)
  for n in ('original_rhs','original_action','original_residual'):assert s(n)[0].shape==s(n)[1].shape==(3870,)
  for w in (0,1):
   assert np.array_equal(s('original_rhs')[w],pair(ia,'fixed_weak_phase_velocity_rhs')[w][mask])
   assert np.array_equal(s('phase_velocity_nodal')[w][mask],s(cy+'_final_nodes')[w]) and np.array_equal(s(cy+'_final_nodes')[w],s(up+'_updated_nodes')[w])
   for n in ('original_action','original_residual'):assert np.array_equal(s(n)[w],s(cy+'_final_'+n)[w])
  assert np.array_equal(a[cy+'_third_word_update_defect'],a[up+'_exact_update_minus_two_word_nodes']) and np.array_equal(a[cy+'_original_iterate'],a[up+'_float_correction'])
  update=[a[up+n] for n in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes')];assert all(v.shape==(3870,) for v in update) and np.all(update[0]==0) and np.all(update[1]==0)
  gaps=[math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5])) for v in zip(*update)];assert all(g==0 for g in gaps);identities.append(dict(name='exact_old_plus_correction_equals_pair_plus_third_word',error=0.))
  identity('original_rhs_minus_action_minus_residual',[(1,s('original_rhs')),(-1,s('original_action')),(-1,s('original_residual'))])
  identity('configuration_Q_plus_action_equals_linearized_total', [(-1,s('original_rhs')),(1,s('original_action')),(-1,s('linearized_total_weak_charge_contact'))])
  identity('linearized_total_plus_residual_equals_saved_gap',[(1,s('linearized_total_weak_charge_contact')),(1,s('original_residual')),(-1,s('linearized_charge_residual_identity_gap'))])
  scale=a['original_positive_scale'];assert scale.shape==(3870,) and np.all(scale>0) and np.array_equal(scale,a[p+'_new_phase_positive_scale'])
  identity('scale_squared_equals_saved_positive_diagonal',[(1,(scale*scale,np.zeros(3870))),(-1,tuple(v[mask] for v in pair(ia,'new_phase_mass_diagonal')))])
  f=total(s('original_rhs'));res=total(s('original_residual'));assert np.linalg.norm(f)>0;rat=np.array((np.linalg.norm(res)/np.linalg.norm(f),np.linalg.norm(res/scale)/np.linalg.norm(f/scale)))
  assert np.allclose(rat,a['original_raw_and_scaled_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(a['original_raw_and_scaled_ratios'],a[cy+'_trial_original_raw_and_scaled_ratios']) and np.array_equal(a['original_raw_and_scaled_ratios'],np.array(r['original_raw_and_scaled_ratios']))
  assert r['response_rows_admitted']==bool(np.all(a['original_raw_and_scaled_ratios']<=1e-10)) and r['history'][0]['admitted']==r['response_rows_admitted']
  ja=read(jets,tuple(jets['metadata']['schema']));assert set(ja)=={n+'_'+w for n in ('value','R','Z') for w in ('hi','lo')}
  for n,v in ja.items():assert v.shape==(15136,) and np.array_equal(v,a[p+'_phase_velocity_increment_'+n]),n
  assert jets['metadata']['solution']==sol and jets['metadata']['mixed_jet_rule']=='delta_partial_t_phi_i equals partial_i_delta_phi_t'
  norms={n:dict(L2=float(np.linalg.norm(total(s(n)))),Linf=float(np.max(abs(total(s(n))),initial=0))) for n in ('phase_velocity_nodal','original_rhs','original_action','original_residual','linearized_total_weak_charge_contact','linearized_charge_residual_identity_gap')}
  report=dict(status='SAVED_PHASE_LINEAR_RESPONSE_CLOSURE_PASS',controls=2,committed_pairs=len(records),roles={n:q['file'] for n,q in zip(('INPUT','FIXTURE','SOLUTION','RATE_JETS'),roles)},iteration_snapshots=len(records)-4,original_ratios=rat.tolist(),response_rows_admitted=r['response_rows_admitted'],norms_descriptive=norms,charge_contact_L2_over_original_RHS=norms['linearized_total_weak_charge_contact']['L2']/norms['original_rhs']['L2'],unchanged_prior_literal_weak_charge_L2=float(np.linalg.norm(total(pair(ia,'fixed_literal_weak_phase_charge')))),paired_jet_duplicate_ties_checked=True,independent_mixed_jet_or_mass_FE_recontraction=False,scope_limit='Saved word ties and signed arithmetic only; no functional, mass action, scatter, derivative, fixture or solver reconstruction',finite_phase_charge_restored=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,identities=identities,selected=selected,physical_adoption=False,EOS_FE_mass_operator_solver_or_fixture_replayed=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
