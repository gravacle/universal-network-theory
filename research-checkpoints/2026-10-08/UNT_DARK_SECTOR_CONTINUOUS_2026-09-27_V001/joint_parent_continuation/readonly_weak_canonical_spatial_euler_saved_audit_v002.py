"""Prospective saved-only audit. Root must bind authentic CLOSED terminal pins.
No producer/helper import, force/field/99-operator/kinetic replay, solve or evolution.
Only stored coefficient, chart, momentum, incidence and component contractions.
"""
from pathlib import Path
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V002'
AUTHOR_DRAFT=True
AUDIT='READONLY_'+STEM+'_SAVED_AUDIT'
HELD_BLUEPRINT=dict(source_sha256='648d5a62f0a3958e02d917356820f5d6fb541aa8151ab5c52c9fc3f946768a1f',protocol_sha256='ae50d65afc3790d2a5fd41dc13d6352fe5b53181f7cb8fffc88690c4937344d0')
TERMINAL=dict(owner_pid=None,source_sha256=None,protocol_sha256=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
np=None;IDENTITIES=0;MAX_ERROR=0.;COUNTS=dict(pairs=0,numeric_arrays=0,numeric_entries=0,negative_entries=0,nonfinite_entries=0,metadata_arrays=0)

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def read_json(n):return json.loads(path(n).read_text())

def false_flags(v):assert v and all(x is False for x in v.values())

def identity(label,a,b,envelope=None):
 global IDENTITIES,MAX_ERROR
 a=np.asarray(a);b=np.asarray(b);e=abs(a)+abs(b) if envelope is None else np.asarray(envelope)
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0),label
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));assert error<=2e-11,(label,error)
 IDENTITIES+=1;MAX_ERROR=max(MAX_ERROR,error)

def control(row,d):
 prefix=f"control_{row['ordinal']:03d}_{row['name']}_"
 a,b,e=[d[prefix+x] for x in ('actual','expected','envelope')]
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0))
 assert row['tolerance']==2e-11 and abs(error-row['error'])<=2e-13*max(1.,abs(error),abs(row['error']))
 assert (error<=row['tolerance']) is row['passed']

def record_read(r,owner):
 assert sha(r['file'])==r['sha256'] and sha(r['commit_file'])==r['commit_sha256']
 assert read_json(r['commit_file'])=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
 md=r['metadata'];assert md['owner']==owner;false_flags(md['qualification']);out={}
 with np.load(path(r['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for k,s in md['schema'].items():
   a=f[k];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and a.dtype.kind in 'fiub',k
   finite=np.isfinite(a);assert bool(np.all(finite))==s['finite'] and (md['failed'] or s['finite']),k
   COUNTS['numeric_arrays']+=1;COUNTS['numeric_entries']+=a.size;COUNTS['negative_entries']+=int(np.count_nonzero(a<0));COUNTS['nonfinite_entries']+=int(a.size-np.count_nonzero(finite));out[k]=a.copy()
 COUNTS['pairs']+=1;COUNTS['metadata_arrays']+=1;return out

def point_momentum_identities(d):
 den=d['seed_chart_dens'];PU=d['seed_PiU'];P=d['seed_Pi'];JU=d['seed_chart_JU'];Jzu=d['seed_chart_JzU'];Jzz=d['seed_chart_Jzz']
 u=np.einsum('pa,pai->pi',PU[:,0],JU)+np.einsum('jp,jpi->pi',P[:,:,0,0],Jzu)
 z=P[:,:,0,1:]+P[:,:,0,0,None]*Jzz[None]
 ue=np.einsum('pa,pai->pi',abs(PU[:,0]),abs(JU))+np.einsum('jp,jpi->pi',abs(P[:,:,0,0]),abs(Jzu));ze=abs(P[:,:,0,1:])+abs(P[:,:,0,0,None]*Jzz[None])
 calc=den[:,None]*np.concatenate((u,z.transpose(1,0,2).reshape(3784,96)),axis=1);bound=den[:,None]*np.concatenate((ue,ze.transpose(1,0,2).reshape(3784,96)),axis=1)
 identity('current_native_momentum',d['new_native_momentum'],calc,d['momentum_operation_current_native_density']+abs(d['new_native_momentum']))
 C=d['seed_connection_momentum'][:,0];embed=d['seed_chart_embed'];Uh=d['seed_chart_Uh'];zh=d['seed_chart_zh']
 pm=den[:,None]*(np.einsum('pmn,pkmn->pk',C,embed)+np.einsum('pa,pka->pk',PU[:,0],Uh)+np.einsum('jp,jpk->pk',P[:,:,0,0],zh))
 em=den[:,None]*(np.einsum('pmn,pkmn->pk',abs(C),abs(embed))+np.einsum('pa,pka->pk',abs(PU[:,0]),abs(Uh))+np.einsum('jp,jpk->pk',abs(P[:,:,0,0]),abs(zh)))
 identity('current_native_metric_momentum',d['new_metric_native_momentum'],pm,em+abs(d['new_metric_native_momentum']))
 eh=d['new_metric_EH_momentum'];six=np.stack((eh[:,0,0],eh[:,1,1],eh[:,2,2],2*eh[:,0,1],2*eh[:,0,2],2*eh[:,1,2]),axis=1)
 identity('current_total_metric_momentum',d['new_metric_total_momentum'],pm+six,em+abs(six)+abs(d['new_metric_total_momentum']))
 identity('connection_component_sum',d['seed_connection_momentum'],d['seed_connection_D']+d['seed_connection_Maxwell'])
 identity('native_rate_difference',d['seed_native_rate_delta'],d['seed_nodal_native_rate']-d['seed_old_L2_native_rate'],abs(d['seed_nodal_native_rate'])+abs(d['seed_old_L2_native_rate']))
 identity('actual_native_target_gap',d['new_native_minus_old_target'],d['new_native_momentum']-d['old_native_target'],abs(d['new_native_momentum'])+abs(d['old_native_target']))
 identity('phase_current_density',d['new_phase_canonical_density'],den*d['new_phase_current'][:,0])
 tc=d['metric_Euler_component_coefficients'];te=d['metric_Euler_component_envelope']
 identity('signed_metric_point_component_sum',d['metric_Euler_coefficient'],tc.sum(axis=-1),te.sum(axis=-1))
 identity('metric_point_envelope_sum',d['metric_Euler_envelope'],te.sum(axis=-1))
 # D0 caller usability: actual stored primitives, jets, chart and tensor EH operand.
 required=('uc','V_raised','connection_Klo','connection_momentum','g','hi','Ga','U','du','z','dz','phi','Pi','PiU','nu','nz','P','q','V','D','F','Fup','Z','A','mu','a','r','f','z2')
 assert all('seed_'+k in d for k in required)
 assert d['seed_z'].shape==(32,3784,4) and d['seed_chart_JzU'].shape==(32,3784,3) and eh.shape==(3784,3,3)
 for k in ('dg','dhi','dN','dbeta','dh','dih','du_cov','dup','dgamma','dJU','dJzU','dJzz','dUh','dzh','dembed'):assert 'seed_chart_derivative_'+k in d
 for k in ('seed_covariant_native_rate_R','seed_covariant_native_rate_Z'):assert d[k].shape==(33,3784,3)
 for k in ('seed_metric_L2_rate','seed_metric_L2_rate_R','seed_metric_L2_rate_Z'):assert d[k].shape==(3784,3,3)

def saved_incidence(cols,basis,kind):
 # Fixed incidence of stored coefficient value/R/Z jets and saved hats only.
 out=np.zeros((33,3,87,45)) if kind=='native' else np.zeros((6,87,45));ci=basis['geometry_cell_i'];cj=basis['geometry_cell_j']
 assert ci.dtype==cj.dtype==np.dtype('int64') and np.all((ci>=0)&(ci<86)) and np.all((cj>=0)&(cj<44))
 links=((0,0,0),(0,1,2),(1,5,0),(2,0,2),(3,3,1),(4,2,3),(5,4,2))
 for iq,d in enumerate(cols):
  co=d[kind+'_Euler_coefficient'];R=basis['geometry_R'][iq];weight=basis['geometry_dv'][iq]/R
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hats=basis['geometry_hats'][iq,a].reshape(3,3784)
   if kind=='native':
    q=co.reshape(3784,33,3,3)
    for c in range(3):
     power=2 if c==2 else 0;factor=hats*R[None]**power
     if power:factor[1]+=power*R**(power-1)*hats[0]
     values=np.einsum('pgj,jp->gp',q[:,:,c,:],factor)*weight
     for g in range(33):np.add.at(out[g,c],(ci+di,cj+dj),values[g])
   else:
    for local,regular,power in links:
     factor=hats*R[None]**power
     if power:factor[1]+=power*R**(power-1)*hats[0]
     values=np.sum(co[:,local,:]*factor.T,axis=1)*weight;np.add.at(out[regular],(ci+di,cj+dj),values)
 if kind=='native':out[:,1,1]+=out[:,1,0];out[:,2,1]+=out[:,2,0];out[:,:,0]=0;out[:,1,:,0]=0
 else:out[:,1]+=out[:,0];out[:,0]=0;out[3:5,:,0]=0
 return out

def ordinary_saved_incidence(d,r):
 i=d['ordinary_input_source_indices'];t=d['ordinary_input_source_right_weight'];R=d['ordinary_input_source_R']
 assert i.dtype==np.dtype('int64') and np.all((i>=0)&(i<86)) and np.all((t>0)&(t<1)) and np.all(d['ordinary_input_source_Z']==0)
 identity('annular_radius',R,(1-t)*r[i]+t*r[i+1],abs((1-t)*r[i])+abs(t*r[i+1])+abs(R))
 local=d['ordinary_metric_local_force'];regular=d['ordinary_metric_regular_point_force'];calc=np.zeros_like(regular)
 for a,b,power in ((0,0,0),(0,1,2),(1,5,0),(2,0,2),(3,3,1),(4,2,3),(5,4,2)):calc[:,b]+=local[:,a]*R**power
 identity('ordinary_regular_component_transform',regular,calc,abs(regular)+abs(calc))
 out=np.zeros((6,87,45))
 for offset,w in ((0,1-t),(1,t)):
  for k in range(6):np.add.at(out[k,:,0],i+offset,regular[:,k]*w)
 out[:,1]+=out[:,0];out[:,0]=0;out[3:5,:,0]=0
 identity('ordinary_saved_sheet_incidence',d['ordinary_metric_spatial_Euler_load'],out,d['ordinary_metric_spatial_Euler_envelope']+abs(out))

def publish(n,v):
 raw=(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;print('READONLY_AUDIT_SHA256',sha(n),flush=True)

FAILED='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001'
FAILED_PINS=dict(error='8abfa418e010ebd5728845461e3391a73064925015537bdaa88643202e8d0c83',receipt='fd79952cefba089c86568c8641e88df1a9df50a8ef3c1935a5e6a3490b300b85')

def exact_old_pair(old,new,prefix=''):
 assert sha(old['file'])==old['sha256'] and sha(old['commit_file'])==old['commit_sha256']
 assert read_json(old['commit_file'])=={k:v for k,v in old.items() if k not in ('commit_file','commit_sha256')}
 with np.load(path(old['file']),allow_pickle=False) as z:
  assert json.loads(str(z['metadata_json']))==old['metadata'] and set(z.files)==set(old['metadata']['schema'])|{'metadata_json'}
  for k,desc in old['metadata']['schema'].items():
   a=z[k];b=new[prefix+k];assert a.dtype==b.dtype and a.shape==b.shape and a.tobytes(order='C')==b.tobytes(order='C'),('exact_failed_parent_reuse',k)


def saved_positive_bound_identities(d):
 # Contractions of stored positive intermediates only; no bound helper replay.
 for k,a in d.items():
  if k.startswith('momentum_operation_'):assert a.dtype.kind=='f' and np.all(a>=0),k
 base='momentum_operation_saved_affine_'
 identity('stored_expected_bound_sum',d[base+'expected_density'],d[base+'old_pointstar']+d[base+'action'])
 modes=d[base+'modes'];u=d[base+'native_U']
 action=np.concatenate((u,modes.transpose(1,0,2).reshape(3784,96)),axis=1)
 identity('stored_affine_positive_block_order',d[base+'action'],action)
 identity('stored_new_full_readout_bound',d['new_full_native_readout_envelope'],d['momentum_operation_current_native_density']+d[base+'expected_density'])
 assert d['original_postcancel_native_momentum_envelope'].shape==(3784,99)


def main():
 global np
 if AUTHOR_DRAFT:raise SystemExit('HELD: root FULL review and audit release required.')
 if any(TERMINAL[k] is None for k in ('owner_pid','source_sha256','protocol_sha256','receipt_sha256')) or (TERMINAL['result_sha256'] is None and TERMINAL['error_sha256'] is None):raise SystemExit('HELD: authentic root CLOSED bindings and audit authorization required.')
 print('READONLY_SPATIAL_EULER_AUDIT_PID',os.getpid(),flush=True)
 assert sha('cross_u_weak_canonical_spatial_euler_loads_v002.py')==TERMINAL['source_sha256'] and sha(STEM+'.md')==TERMINAL['protocol_sha256'] and sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 rc=read_json(STEM+'_RECEIPT.json');assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['closed'] and rc['owner']['owner']=='root' and rc['owner']['pid']==TERMINAL['owner_pid'] and rc['owner']['source_sha256']==TERMINAL['source_sha256'];false_flags(rc['qualification'])
 hashes={}
 for group in ('input_sha256','output_sha256'):
  for n,h in rc[group].items():assert n not in hashes or hashes[n]==h;hashes[n]=h;assert sha(n)==h,n
 for n in rc['output_sha256']:assert path(n).stat().st_mode&0o777==0o444
 assert path(STEM+'_RECEIPT.json').stat().st_mode&0o777==0o444
 success=TERMINAL['error_sha256'] is None
 if success:
  assert sha(STEM+'_RESULT.json')==TERMINAL['result_sha256']==rc['result_sha256'];doc=read_json(STEM+'_RESULT.json');assert doc['status']=='CONDITIONAL_WEAK_CANONICAL_SPATIAL_EULER_ARITHMETIC_PASS' and len(doc['cases'])==1
 else:
  assert sha(STEM+'_ERROR.json')==TERMINAL['error_sha256'];doc=read_json(STEM+'_ERROR.json');assert doc['status']=='FAILED'
  if rc['status']=='CLOSED_ERROR':assert rc['error_sha256']==TERMINAL['error_sha256']
  else:assert doc['prior_receipt_sha256']==TERMINAL['receipt_sha256']
  for n,h in doc['preserved_outputs'].items():assert sha(n)==h
 assert doc['owner']==rc['owner'];false_flags(doc['qualification']);records=doc['checkpoints'];controls=doc['controls']
 assert [r['ordinal'] for r in controls]==list(range(len(controls)))
 if success:assert len(records)==8 and len(controls)==36 and all(r['passed'] for r in controls)
 else:assert len(controls)<=36 and len(records)<=9
 actual={p.name for p in BASE.glob(STEM+'_*.npz')};commits={p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')};expected={r['file'] for r in records};ec={r['commit_file'] for r in records}
 if success:assert actual==expected and commits==ec
 else:
  assert actual==expected|set(doc['unqualified_npz']) and ec<=commits
  for n in actual|commits:assert n in doc['preserved_outputs'] and sha(n)==doc['preserved_outputs'][n]
 import numpy as _np
 np=_np;groups={};witness=set();cols=[]
 assert sha(FAILED+'_ERROR.json')==FAILED_PINS['error'] and sha(FAILED+'_RECEIPT.json')==FAILED_PINS['receipt']
 old=read_json(FAILED+'_ERROR.json');oldrc=read_json(FAILED+'_RECEIPT.json');assert oldrc['status']=='CLOSED_ERROR' and old['owner']==oldrc['owner'] and old['owner']['pid']==34079
 assert len(old['controls'])==8 and all(x['passed'] for x in old['controls'][:7]) and old['controls'][7]['passed'] is False and len(old['checkpoints'])==4
 if success:assert doc['checkpoints'][0]['metadata']['original_controls']==old['controls'] and doc['checkpoints'][0]['metadata']['original_failure_retained'] is True
 for rec in records:
  d=record_read(rec,rc['owner']);md=rec['metadata'];kind=md['kind']
  for row in controls:
   if f"control_{row['ordinal']:03d}_{row['name']}_actual" in d:control(row,d);witness.add(row['ordinal'])
  for row in md.get('controls',[]):assert row==controls[row['ordinal']] and row['ordinal'] in witness
  if not md['failed'] and kind=='new_sigma1_canonical_spatial_Euler_coefficients_on_explicit_mixed_seed':
   assert md['sigma']==1. and md['column']==len(cols) and md['points']==3784 and len(md['controls'])==6 and md['physical_changes']==[] and all(x is None for x in md['unknown_ports'].values())
   if md['column']==0:exact_old_pair(old['checkpoints'][3],d,'failed_V001_')
   saved_positive_bound_identities(d);point_momentum_identities(d);cols.append({k:d[k] for k in ('native_Euler_coefficient','metric_Euler_coefficient')})
  elif not md['failed']:groups[kind]=(rec,d)
 if success:
  assert witness==set(range(36)) and len(cols)==4
  for ordinal,newrec in enumerate(records[:3]):
   with np.load(path(newrec['file']),allow_pickle=False) as z:newdata={k:z[k] for k in newrec['metadata']['schema']}
   exact_old_pair(old['checkpoints'][ordinal],newdata)
  assert records[1]['metadata']['controls']==old['controls'][:7] and records[1]['metadata']['no_fixture_replay'] is True
  assert records[2]['metadata']['basis_replay'] is False
  inp=groups['unchanged_sigma1_configuration_spectrum_and_owned_seed_references'][1];basis=groups['unchanged_genuine_native_and_regular_six_metric_configuration_basis'][1];md,d=groups['genuine_weak_native99_and_six_metric_spatial_Euler_loads']
  assert inp['xi'].shape==inp['weights'].shape==(32,) and np.all(inp['xi']>0) and np.all(np.diff(inp['xi'])>0) and np.all(inp['weights']>0)
  for kind,key in (('native','native_spatial_Euler_load'),('metric','metric_spatial_Euler_bulk_load')):
   calc=saved_incidence(cols,basis,kind);en=d['native_spatial_Euler_envelope'] if kind=='native' else d['metric_spatial_Euler_bulk_envelope'];identity(kind+'_stored_coefficient_incidence',d[key],calc,en+abs(calc))
  loads=d['metric_spatial_Euler_component_loads'];bounds=d['metric_spatial_Euler_component_envelope'];assert loads.shape==(16,6,87,45)
  identity('signed_metric_bulk_components',loads[:15].sum(axis=0),d['metric_spatial_Euler_bulk_load'],bounds[:15].sum(axis=0)+d['metric_spatial_Euler_bulk_envelope'])
  identity('ordinary_component_copy',loads[15],d['ordinary_metric_spatial_Euler_load']);ordinary_saved_incidence(d,inp['r_kpc'])
  identity('complete_known_metric_load',d['complete_known_metric_spatial_Euler_load'],d['metric_spatial_Euler_bulk_load']+d['ordinary_metric_spatial_Euler_load'],d['complete_known_metric_spatial_Euler_envelope'])
  identity('weak_native_functional',np.array(np.sum(d['native_spatial_Euler_load']*d['weak_force_native_test'])),d['weak_force_direct_functional'][0],np.array(np.sum(d['native_spatial_Euler_envelope']*abs(d['weak_force_native_test']))+abs(d['weak_force_direct_functional'][0])))
  identity('weak_metric_functional',np.array(np.sum(d['metric_spatial_Euler_bulk_load']*d['weak_force_metric_test'])),d['weak_force_direct_functional'][1],np.array(np.sum(d['metric_spatial_Euler_bulk_envelope']*abs(d['weak_force_metric_test']))+abs(d['weak_force_direct_functional'][1])))
  assert md['metadata']['quadrature_points']==15136 and all(x is None for x in md['metadata']['unknowns'].values())
 for n,h in hashes.items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha('cross_u_weak_canonical_spatial_euler_loads_v002.py')==TERMINAL['source_sha256']
 report=dict(status='SAVED_PACKET_AUDIT_PASS' if success else 'SAVED_CLOSED_FAILURE_CUSTODY_AUDIT_PASS',terminal=TERMINAL,audit_pid=os.getpid(),census=COUNTS,control_count=len(controls),witnessed_control_ordinals=sorted(witness),unwitnessed_control_ordinals=sorted(set(range(len(controls)))-witness),failed_controls=[r for r in controls if not r['passed']],input_bindings=len(rc['input_sha256']),output_bindings=len(rc['output_sha256']),identity_count=IDENTITIES,max_identity_error=MAX_ERROR,D0_seed_operands_admitted=success,original_failed_controls=old['controls'],original_failed_gate_preserved=True,cached_column0_exact_reuse=success,qualification=doc['qualification'],scientific_operator_or_producer_replay=False,scope='Stored spatial Euler arithmetic and D0 operand availability only; no pdot, acceleration, CMC, physical ports/history or calculated galaxy velocity qualification.')
 publish(AUDIT+'.json',report);print(json.dumps({k:report[k] for k in ('status','audit_pid','census','control_count','identity_count','max_identity_error')},sort_keys=True),flush=True)

if __name__=='__main__':
 try:main()
 except BaseException:
  if TERMINAL['owner_pid'] is not None and TERMINAL['receipt_sha256'] is not None:publish(AUDIT+'_READER_REFUSAL.json',dict(status='READER_REFUSAL',terminal=TERMINAL,audit_pid=os.getpid(),traceback=traceback.format_exc(),audit_source_sha256=sha(__file__)))
  raise
