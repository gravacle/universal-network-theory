"""Guarded selected saved operands only; no phase/FE/scatter/operator replay."""
from pathlib import Path
import hashlib,json,os
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
PARENT='CROSS_U_PHASE_VELOCITY_FOUR_NORMAL_CONTACTS_V002'
OWNER_PID=63089
SOURCE_SHA='78635ea928f73efa71a9ead61ef21c84a0701018e56815a7d8501e0ab4a6112c'
PROTOCOL_SHA='b9cf8e400e79d91009b5d0c860b959008b775895222c224170332e6be13d7737'
RESULT_SHA='9756f561266938f7c8037449f2dd3a7e745230d705cd21a067c7605bdd9d6683'
RECEIPT_SHA='9e63853d14d73eb19dfaa8b5c6ceba1ac0424e751c2dcd531be4098a0ceb7d49'
FAILED_PROOF=('ROOT_PHASE_FOUR_NORMAL_V001_FAILED_OWNER_RECOVERY_V001.json','d202e3b3d48031574cf32ae1d8a9ad16b38300dbd704051bdb539825ef143a59')
OUT='READONLY_PHASE_FOUR_NORMAL_RECOVERY_CLOSURE_V001_RESULT.json'
TOL=2e-11
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def main():
 assert AUTHOR_DRAFT is False and all(x is not None for x in (OWNER_PID,SOURCE_SHA,PROTOCOL_SHA,RESULT_SHA,RECEIPT_SHA)),'Root FULL review/release and authentic terminal required'
 assert not (BASE/OUT).exists()
 seals={};identities=[];np=None
 def sealed(n,h):
  assert h is not None
  if n not in seals:assert digest(BASE/n)==h;seals[n]=h
  else:assert seals[n]==h
  return BASE/n
 for n,h in ((PARENT+'_RESULT.json',RESULT_SHA),(PARENT+'_RECEIPT.json',RECEIPT_SHA),('cross_u_phase_velocity_four_normal_contacts_v002.py',SOURCE_SHA),(PARENT+'.md',PROTOCOL_SHA),FAILED_PROOF):sealed(n,h)
 r=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());rc=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());failed=json.loads((BASE/FAILED_PROOF[0]).read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==RESULT_SHA and r['owner']==rc['owner'] and r['owner']['pid']==OWNER_PID and r['owner']['source_sha256']==SOURCE_SHA
 assert r['physical_adoption'] is False and r['normal_constraints_qualified'] is False and all(v is False for v in r['qualification'].values()) and r['completed_fixture_and_four_point_columns_replayed'] is False
 records=r['checkpoints'];assert len(records)==8 and len(r['columns'])==4 and len(r['controls'])==2 and [q['ordinal'] for q in r['controls']]==[0,1]
 assert all(q['passed'] is True and q['tolerance']==TOL and q['error']<=TOL for q in r['controls'])
 assert failed['owner']['pid']==61274 and failed['terminal_receipt_present'] is False and len(failed['checkpoints'])==7
 assert r['recovered_failed_owner_proof']==dict(file=FAILED_PROOF[0],sha256=FAILED_PROOF[1])
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;sealed(n,h)
  assert json.loads((BASE/q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['failed'] is False
 assert {p.name for p in BASE.glob(PARENT+'*.npz')}=={q['file'] for q in records}
 import numpy as numpy_module
 np=numpy_module
 def read(q,names):
  out={}
  with np.load(BASE/q['file'],allow_pickle=False) as z:
   for n in names:
    a=z[n];sc=q['metadata']['schema'][n];assert list(a.shape)==sc['shape'] and str(a.dtype)==sc['dtype'] and sc['finite'] is True and a.dtype.kind in 'fiub' and np.all(np.isfinite(a));out[n]=a
  return out
 def identity(name,a,b,e):
  assert a.shape==b.shape==e.shape and np.all(np.isfinite(e)) and np.all(e>=0)
  error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));assert error<=TOL,(name,error)
  identities.append(dict(name=name,error=error));return error
 def pair(data,n):return data[n+'_hi']+data[n+'_lo']
 copied=0;direction_diagnostics=0
 for iq,(q,old) in enumerate(zip(records[:7],failed['checkpoints'])):
  assert q['metadata']['recovered_completed_parent']=={n:old[n] for n in ('file','sha256','commit_file','commit_sha256')} and q['metadata']['schema']==old['metadata']['schema']
  for n,h in ((old['file'],old['sha256']),(old['commit_file'],old['commit_sha256'])):sealed(n,h)
  assert json.loads((BASE/old['commit_file']).read_text())=={n:old[n] for n in ('file','sha256','metadata')}
  names=tuple(q['metadata']['schema']) if iq!=1 else tuple('control_000_new_tilted_phase_velocity_four_normal_contact_'+s for s in ('actual','expected','envelope'))+('fixture_completed_contacts','fixture_completed_envelope')
  new=read(q,names);prior=read(old,names)
  for n in names:assert new[n].dtype==prior[n].dtype and new[n].shape==prior[n].shape and new[n].tobytes()==prior[n].tobytes();copied+=1;direction_diagnostics+=int(n.startswith('direction_'))
 assert direction_diagnostics==400 and records[1]['metadata']['controls']==failed['checkpoints'][1]['metadata']['controls']==r['controls'][:1]
 loads=r['loads'];assert loads==records[-1] and loads['metadata']['baseline_rows_added_or_subtracted'] is False and loads['metadata']['primitive_legendre_bridge_resolved'] is False
 families=('registered_normal','literal_action');names=[]
 for fam in families:
  for part in ('weak_action','weak_Hamiltonian_rows','functional_difference','nodal_functional_through15659','direct_functional_through60543'):
   names.extend(fam+'_'+part+'_'+word for word in ('hi','lo'))
 names.extend('literal_minus_registered_weak_normal_gap_'+word for word in ('hi','lo'))
 stem='control_001_new_phase_contact_regular_normal_Q1_functional';names.extend(stem+'_'+x for x in ('actual','expected','envelope'))
 data=read(loads,names);functional=[];norms={}
 for fam in families:
  action=pair(data,fam+'_weak_action');ham=pair(data,fam+'_weak_Hamiltonian_rows');e=sum(abs(data[fam+'_'+part+'_'+word]) for part in ('weak_action','weak_Hamiltonian_rows') for word in ('hi','lo'))
  identity(fam+'_Hamiltonian_equals_minus_action',ham,-action,e)
  nodal=pair(data,fam+'_nodal_functional_through15659');direct=pair(data,fam+'_direct_functional_through60543');gap=pair(data,fam+'_functional_difference')
  identity(fam+'_saved_functional_difference',gap,nodal-direct,abs(nodal)+abs(direct)+abs(gap));functional.append(float(gap))
  norms[fam]=[dict(row=i,L2=float(np.sqrt(np.sum(ham[i]**2))),Linf=float(np.max(abs(ham[i]),initial=0)),nonzero_nodes=int(np.count_nonzero(ham[i]))) for i in range(4)]
 gap=pair(data,'literal_minus_registered_weak_normal_gap');lit=pair(data,'literal_action_weak_Hamiltonian_rows');reg=pair(data,'registered_normal_weak_Hamiltonian_rows')
 identity('literal_minus_registered_weak_rows',gap,lit-reg,abs(lit)+abs(reg)+abs(gap))
 identity('functional_control_actual_is_saved_differences',data[stem+'_actual'],np.array(functional),abs(data[stem+'_actual'])+abs(np.array(functional)))
 triplets=[]
 for q,row in ((records[1],r['controls'][0]),(loads,r['controls'][1])):
  prefix='control_%03d_'%row['ordinal']+row['name'];v=read(q,tuple(prefix+'_'+x for x in ('actual','expected','envelope')))
  error=identity(row['name'],v[prefix+'_actual'],v[prefix+'_expected'],v[prefix+'_envelope']);assert np.isclose(error,row['error'],rtol=TOL,atol=1e-300);triplets.append(error)
 for n,h in seals.items():assert digest(BASE/n)==h
 result=dict(status='SAVED_PHASE_FOUR_NORMAL_RECOVERY_CLOSURE_PASS',owner_pid=os.getpid(),parent=dict(pid=OWNER_PID,result_sha256=RESULT_SHA,receipt_sha256=RECEIPT_SHA),controls=2,committed_pairs=8,selected_bitcopied_fields=copied,direction_diagnostic_fields=direction_diagnostics,identities=identities,maximum_error=max(q['error'] for q in identities),four_row_unweighted_nodal_norms_descriptive=norms,literal_minus_registered_gap_norms=[dict(L2=float(np.sqrt(np.sum(gap[i]**2))),Linf=float(np.max(abs(gap[i]),initial=0))) for i in range(4)],physical_adoption=False,normal_constraints_qualified=False,old_phase_normal_FE_scatter_operator_or_fixture_replayed=False,scope_limit='Final saved words and seven selected copied payload witnesses only. Intermediate LOADS summation prefixes, point formulas, FE/scatter and functional recontractions are not replayed; no residual-zero or physical acceptance gate.')
 with (BASE/OUT).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 (BASE/OUT).chmod(0o444);print(json.dumps(dict(status=result['status'],owner_pid=os.getpid(),sha256=digest(BASE/OUT))),flush=True)
if __name__=='__main__':main()
