"""Saved phase pairs/controls only; no phase, mass, geometry or EOS replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003'
OUT='READONLY_LITERAL_PHASE_PREPARATION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='ed18caa749cbbfef40956ee4764390d688aaf6a1567912317d6cc81c9851d079'
PROTOCOL_SHA='a1f9b46ddb29879633eb38b099671ad762f0a8d4bcb8a4d12297035d586c111f'
TERMINAL=dict(pid=59190,result_sha256='fefe9a83c871577653a3965d0c61ff869f6786ff0b1c9a943d9abf4fd6ee79d7',receipt_sha256='9d2fb6e0a649976167144b0d428bc730800844d78670587ad8891b11ddfcca90',error_sha256=None)
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
 assert sha('cross_u_phase_fixed_weak_charge_preparation_v003.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['owner']['pid']==TERMINAL['pid'] and rc['owner']['source_sha256']==SOURCE_SHA
 r=load_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert r['owner']==rc['owner'] and rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256'] and load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')}
  assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and all(v['finite'] is True for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 if not closed:report=dict(status='SAVED_LITERAL_PHASE_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  import numpy as np
  assert len(records)==7 and len(controls)==6 and all(c['passed'] for c in controls) and r['phase_velocity_solved'] is False and r['phase_charge_restored'] is False and r['configuration_updated'] is False and r['physical_adoption'] is False and r['phase_velocity_space_dimension']==3870
  selected=[];identities=[];columns=[]
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
   a=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(a);bound=np.add.reduce([abs(v) for v in a]);e=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert e<=TOL,(label,e);identities.append(dict(name=label,error=e))
  def control(q,a,c):
   prefix='control_%03d_%s_'%(c['ordinal'],c['name']);x,y,b=(a[prefix+n] for n in ('actual','expected','envelope'));assert np.all(b>=0);e=float(np.max(abs(x-y)/np.maximum(b,1e-30),initial=0));assert e==c['error'] and e<=TOL
  inp=records[0];geo=read(inp,tuple(inp['metadata']['schema']));old=inp['metadata']['recovered_geometry_ref'];assert old['metadata']['owner']['pid']==58418 and inp['metadata']['original_basis_payload_reloaded'] is False and inp['metadata']['completed_fixture_replayed'] is False
  for n,h in ((old['file'],old['sha256']),(old['commit_file'],old['commit_sha256'])):assert rc['input_sha256'].get(n,rc['input_sha256'].get(str(path(n).resolve())))==h and sha(n)==h
  assert load_json(old['commit_file'],old['commit_sha256'])=={k:old[k] for k in ('file','sha256','metadata')};cached=read(old,tuple(geo));assert all(np.array_equal(geo[n],cached[n]) for n in geo)
  assert np.all(geo['R']>0) and np.all(geo['dv']>0);fixture=records[1];f=read(fixture,tuple(n for n in fixture['metadata']['schema'] if n.startswith('control_')));control(fixture,f,controls[0])
  eps=inp['metadata']['phase_refs']['fixed']['eps'];H=[];sign_margin=[];clock=[];gaps={}
  for iq,q in enumerate(records[2:6]):
   assert q['metadata']['column']==iq and q['metadata']['controls']==[controls[iq+1]] and q['metadata']['registered_current_gap_retained'] is True
   a=read(q,tuple(q['metadata']['schema']));control(q,a,controls[iq+1]);p=lambda n:pair(a,n)
   for lhs,rhs,gap in (('action_current','registered_current','current_gap'),('action_canonical_density','registered_canonical_density','density_gap'),('literal_hessian','registered_hessian','hessian_gap'),('literal_hessian','reduced_hessian','reduced_gap'),('registered_canonical_density','owned_registered_density','registered_minus_owned_density'),('action_canonical_density','owned_registered_density','action_minus_owned_density')):identity('q%d_%s'%(iq,gap),[(1,p(lhs)),(-1,p(rhs)),(-1,p(gap))])
   identity('q%d_owned_clock_gap'%iq,[(1,p('clock_pressure_argument')),(-1,(a['owned_pressure_argument_u'],np.zeros(3784))),(-1,p('clock_minus_owned_pressure_argument_gap'))])
   lower=p('literal_hessian')[0]-abs(p('literal_hessian')[1]);eH=a['hessian_envelope'];assert np.all(eH>=0) and np.array_equal(lower,a['literal_Hessian_pair_lower_bound']) and np.all(lower>TOL*eH)
   margin=lower/np.maximum(eH,1e-30);assert np.array_equal(margin,a['literal_Hessian_construction_margin']);u=p('clock_pressure_argument');domain=(u[0]>abs(u[1]))&((eps-u[0])>abs(u[1]));assert np.array_equal(domain,a['clock_argument_pair_domain_test']) and np.all(domain) and np.all((a['owned_pressure_argument_u']>0)&(a['owned_pressure_argument_u']<eps))
   assert np.all(p('owned_registered_density')[1]==0)
   H.append(p('literal_hessian'));sign_margin.append(margin);clock.append(total(u))
   for n in ('current_gap','density_gap','hessian_gap','reduced_gap','clock_gap','clock_minus_owned_pressure_argument_gap','registered_minus_owned_density','action_minus_owned_density'):gaps.setdefault(n,[]).append(total(p(n)))
   columns.append(q['file'])
  loads=r['loads'];assert loads==records[6] and loads['metadata']['phase_velocity_solve'] is None and loads['metadata']['phase_velocity_space_dimension']==3870 and loads['metadata']['global_I0_profile_determined'] is False
  a=read(loads,tuple(loads['metadata']['schema']));control(loads,a,controls[5]);p=lambda n:pair(a,n)
  for w in (0,1):assert np.array_equal(p('literal_Hessian')[w],np.concatenate([h[w] for h in H]))
  identity('literal_registered_weak_charge_gap',[(1,p('fixed_literal_weak_phase_charge')),(-1,p('registered_weak_phase_charge')),(-1,p('literal_minus_registered_weak_gap'))]);identity('registered_owned_weak_charge_gap',[(1,p('registered_weak_phase_charge')),(-1,p('owned_registered_weak_phase_charge')),(-1,p('registered_minus_owned_weak_gap'))])
  for w in (0,1):assert np.array_equal(p('fixed_weak_phase_velocity_rhs')[w],-p('compact_literal_phase_configuration_contact')[w])
  mask=np.ones((87,45),bool);mask[0]=False;assert np.count_nonzero(mask)==3870 and np.all(p('new_phase_mass_diagonal')[0][mask]>abs(p('new_phase_mass_diagonal')[1][mask]))
  for n in ('new_phase_mass_diagonal','new_phase_mass_test_response','fixed_literal_weak_phase_charge','registered_weak_phase_charge','owned_registered_weak_phase_charge','compact_literal_phase_configuration_contact','fixed_weak_phase_velocity_rhs'):
   assert p(n)[0].shape==p(n)[1].shape==(87,45) and np.all(p(n)[0][0]==0) and np.all(p(n)[1][0]==0)
  desc={n:dict(L2=float(np.linalg.norm(np.concatenate(v))),Linf=float(np.max(abs(np.concatenate(v)),initial=0))) for n,v in gaps.items()}
  report=dict(status='SAVED_LITERAL_PHASE_PREPARATION_CLOSURE_PASS',controls=6,committed_pairs=7,identities=identities,selected=selected,point_H_min=float(np.min(np.concatenate([total(h) for h in H]))),point_H_max=float(np.max(np.concatenate([total(h) for h in H]))),resolved_H_margin_min=float(np.min(np.concatenate(sign_margin))),clock_u_min=float(np.min(np.concatenate(clock))),clock_u_max=float(np.max(np.concatenate(clock))),finite_current_density_H_and_clock_gap_norms_descriptive=desc,scalar_dimension=3870,positive_diagonal_and_weak_restrictions_checked=True,mass_functional_stored_triplet_checked=True,independent_mass_functional_recontraction=False,functional_scope_limit='Test/direct/nodal functional operands were not published; no test or operator reconstruction',literal_Hessian_positive=True,phase_mass_positive=r['phase_mass_positive'],phase_charge_restored=False,phase_velocity_solved=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,physical_adoption=False,phase_EOS_geometry_FE_operator_or_fixture_replayed=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
