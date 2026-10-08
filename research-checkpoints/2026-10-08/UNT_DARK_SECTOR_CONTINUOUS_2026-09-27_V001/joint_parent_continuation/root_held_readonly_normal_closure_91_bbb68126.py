"""Guarded saved-only paired normal identities and descriptive residual scales.
No action/feature/scatter/operator/fixture/solver replay; no physical-zero gate.
Root binds actual natural terminal, reviews, releases and executes this reader.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002'
OUT='READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json'
AUTHOR_DRAFT=True
TERMINAL=dict(pid=None,source_sha256=None,protocol_sha256=None,result_sha256=None,receipt_sha256=None)
TOL=2e-11
BOUND={};np=None;IDENTITIES=[]
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def bind(n,h):
 p=path(n);assert sha(p)==h,n;key=str(p.resolve());assert key not in BOUND or BOUND[key]==h;BOUND[key]=h;return p
def pair_record(r,receipt):
 for n,h in ((r['file'],r['sha256']),(r['commit_file'],r['commit_sha256'])):assert receipt['output_sha256'][n]==h;bind(n,h)
 assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
 assert r['metadata']['owner']['pid']==TERMINAL['pid'] and r['metadata']['failed'] is False
 assert all(v is False for v in r['metadata']['qualification'].values())
 return r
def read_saved(r,names):
 out={}
 with np.load(path(r['file']),allow_pickle=False) as f:
  assert set(f.files)==set(r['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==r['metadata']
  for n in names:
   a=f[n].copy();s=r['metadata']['schema'][n]
   assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True and np.all(np.isfinite(a)),n
   out[n]=a
 return out
def word(d,n):return d[n+'_hi']+d[n+'_lo']
def word_bound(d,n):return abs(d[n+'_hi'])+abs(d[n+'_lo'])
def identity(n,a,b,e):
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));IDENTITIES.append(dict(name=n,error=error,tolerance=TOL));assert error<=TOL,(n,error)
def original_control(c,d):
 prefix=f"control_{c['ordinal']:03d}_{c['name']}_";a,b,e=(d[prefix+n] for n in ('actual','expected','envelope'))
 assert a.shape==b.shape==e.shape and np.all(e>=0)
 value=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));assert value<=c['tolerance']==TOL and math.isclose(value,c['error'],rel_tol=2e-13,abs_tol=1e-30),(c['name'],value,c['error'])
def summary(d):
 h=word(d,'normal_Hamiltonian_rows');comp=word(d,'normal_Hamiltonian_components');den=np.sum(abs(comp),axis=-1);rows=[]
 for i,n in enumerate(('lapse','shift_R','shift_Z','shift_phi')):
  l2=float(np.linalg.norm(h[i]));inf=float(np.max(abs(h[i]),initial=0));dl2=float(np.linalg.norm(den[i]));dinf=float(np.max(den[i],initial=0))
  rows.append(dict(row=n,absolute_L2=l2,absolute_Linf=inf,absolute_component_sum_L2=dl2,absolute_component_sum_Linf=dinf,relative_L2_to_absolute_component_sum=l2/dl2 if dl2 else None,relative_Linf_to_absolute_component_sum=inf/dinf if dinf else None))
 return rows
def main():
 global np
 assert not AUTHOR_DRAFT and all(v is not None for v in TERMINAL.values()),'Actual CLOSED bindings/root release required before I/O'
 assert not path(OUT).exists();source_sha=sha(__file__);t=TERMINAL
 result=json.loads(bind(STEM+'_RESULT.json',t['result_sha256']).read_text());receipt=json.loads(bind(STEM+'_RECEIPT.json',t['receipt_sha256']).read_text())
 bind('cross_u_paired_current_normal_constraints_v002.py',t['source_sha256']);bind(STEM+'.md',t['protocol_sha256'])
 assert receipt['status']=='CLOSED' and receipt['error_sha256'] is None and receipt['result_sha256']==t['result_sha256']
 assert result['owner']==receipt['owner'] and result['owner']['pid']==t['pid'] and result['owner']['source_sha256']==t['source_sha256']
 assert result['status']=='CONDITIONAL_PAIRED_NORMAL_CONSTRAINTS_MEASURED' and all(v is False for v in result['qualification'].values())
 controls=result['controls'];records=result['checkpoints'];assert len(controls)==12 and len(records)==8 and all(c['passed'] is True and c['tolerance']==TOL for c in controls) and [c['ordinal'] for c in controls]==list(range(12))
 records=[pair_record(r,receipt) for r in records];assert [r['file'].rsplit('_',1)[-1] for r in records]==['INPUT.npz','FIXTURE.npz','BASIS.npz']+['COLUMN.npz']*4+['LOADS.npz']
 assert set(p.name for p in BASE.glob(STEM+'_*.npz'))==set(r['file'] for r in records) and set(p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json'))==set(r['commit_file'] for r in records)
 assert records[1]['metadata']['controls']==controls[:3] and records[1]['metadata']['fixture_equations_replayed'] is False
 for i,r in enumerate(records[3:7]):assert r['metadata']['column']==i and r['metadata']['controls']==controls[3+2*i:5+2*i] and r['metadata']['primitive_momentum_replayed'] is False
 assert records[-1]['metadata']['controls']==controls[-1:] and records[-1]['metadata']['primitive_readout_recomputed'] is False
 import numpy as _np
 np=_np
 for r in records[3:]:
  selected=tuple(n for n in r['metadata']['schema'] if n.startswith('control_'));raw=read_saved(r,selected)
  for c in r['metadata']['controls']:original_control(c,raw)
 loads=records[-1];names=tuple(n for n in loads['metadata']['schema'] if n.startswith(('normal_action_','normal_Hamiltonian_rows_','normal_Hamiltonian_components_','ordinary_Hamiltonian_rows_','functional_nodal_','functional_direct_','functional_difference_','EH_isotropic_Hamiltonian_alias_','EH_full_minus_isotropic_remainder_','pilot_saved_readout_')) and not n.startswith('control_'))
 d=read_saved(loads,names);a,h,ordinary,components=(word(d,n) for n in ('normal_action','normal_Hamiltonian_rows','ordinary_Hamiltonian_rows','normal_Hamiltonian_components'))
 assert a.shape==h.shape==ordinary.shape==(4,87,45) and components.shape==(4,87,45,5)
 identity('minus_action_plus_ordinary',h,-a+ordinary,word_bound(d,'normal_Hamiltonian_rows')+word_bound(d,'normal_action')+word_bound(d,'ordinary_Hamiltonian_rows'))
 identity('five_component_row_sum',h,np.sum(components,axis=-1),word_bound(d,'normal_Hamiltonian_rows')+np.sum(word_bound(d,'normal_Hamiltonian_components'),axis=-1))
 fd=word(d,'functional_difference');fn=word(d,'functional_nodal');fp=word(d,'functional_direct');identity('functional_difference',fd,fn-fp,word_bound(d,'functional_difference')+word_bound(d,'functional_nodal')+word_bound(d,'functional_direct'))
 iso=word(d,'EH_isotropic_Hamiltonian_alias');rem=word(d,'EH_full_minus_isotropic_remainder');identity('full_EH_equals_isotropic_plus_remainder',components[...,3],iso+rem,word_bound(d,'normal_Hamiltonian_components')[...,3]+word_bound(d,'EH_isotropic_Hamiltonian_alias')+word_bound(d,'EH_full_minus_isotropic_remainder'))
 pilot_name='CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002_RESULT.json';pilot_sha=result['case']['pilot_result_sha256'];assert receipt['input_sha256'][str(path(pilot_name).resolve())]==pilot_sha;pilot=json.loads(bind(pilot_name,pilot_sha).read_text())
 assert np.array_equal(d['pilot_saved_readout_original_affine_and_actual_target_ratios'],np.array(pilot['case']['original_affine_and_actual_target_ratios'])) and np.array_equal(d['pilot_saved_readout_bridge_rhs_and_target_ratios'],np.array(pilot['case']['bridge_rhs_and_target_ratios']))
 assert result['case']['original_affine_readout_ratios']==pilot['case']['original_affine_and_actual_target_ratios'] and result['case']['bridge_ratios']==pilot['case']['bridge_rhs_and_target_ratios'] and result['case']['primitive_canonical_readout_admitted']==pilot['case']['canonical_primitive_readout_admitted']
 assert result['case']['physical_adoption'] is False and result['case']['normal_constraint_solution'] is False and result['case']['finite_Legendre_stationarity_remainder_retained'] is True
 rows=summary(d)
 for n,v in BOUND.items():assert sha(n)==v,n
 assert sha(__file__)==source_sha
 out=dict(status='SAVED_PAIRED_NORMAL_CLOSURE_PASS',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=source_sha,parent_terminal=t,controls=12,inherited_controls_checked_metadata_only=3,new_controls_recontracted=9,committed_pairs=8,identities=IDENTITIES,per_row_diagnostic_scales=rows,ratio_definition='norm residual / norm of pointwise sum of absolute five stored component contributions; descriptive only',physical_zero_acceptance_gate=False,qualification=result['qualification'],primitive_canonical_readout_admitted=result['case']['primitive_canonical_readout_admitted'],original_affine_and_actual_target_ratios=pilot['case']['original_affine_and_actual_target_ratios'],bridge_rhs_and_target_ratios=pilot['case']['bridge_rhs_and_target_ratios'],EFT_feature_scatter_operator_fixture_solver_or_evolution_replayed=False)
 with path(OUT).open('x') as f:json.dump(out,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 path(OUT).chmod(0o444);print('SAVED_PAIRED_NORMAL_CLOSURE_PASS',os.getpid(),sha(path(OUT)))
if __name__=='__main__':main()
