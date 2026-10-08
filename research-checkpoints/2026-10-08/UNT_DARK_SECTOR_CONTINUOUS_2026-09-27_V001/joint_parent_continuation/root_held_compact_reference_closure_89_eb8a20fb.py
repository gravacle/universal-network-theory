"""Guarded saved operands only; no producer, formula, feature or FE replay."""
from pathlib import Path
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='READONLY_COMPACT_CONTACT_AND_REFERENCE_CLOSURE_V001'
AUTHOR_DRAFT=True
TOL=2e-11
TERMINALS={
'CROSS_U_COMPACT_METRIC_CONFIGURATION_CONTACT_V001':dict(pid=54248,source='cross_u_compact_metric_configuration_contact_v001.py',source_sha256='8b2c335221d300a4e1a44da30c5f6bddd1fbf3bc99f7b8ae8b7bdce4c60164bd',protocol_sha256='a286661036905627aa53f8a40acb4bdaeab926ec88f49ae9cc33d164800b9138',result_sha256='2815aed3a61e64a39c10bf6ea5e723533aa341d8cfdb6c06eb2c5c432ba6115b',receipt_sha256='a851e4c176325c0a80202291bde3f63ad403271e6613e7fbb0c4158225321060'),
'CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001':dict(pid=54328,source='cross_u_owned_flrw_ordinary_reference_benchmark_v001.py',source_sha256='1d97d883b370c73bdd0a24ac09815a78f4ae690ed0357ed51ab57688ca2a45e9',protocol_sha256='700c85f9d09af983b92d629559d78762c31f311fccd3e601cba6b85ada7faf9d',result_sha256='d279da68cbf50ebbeae62021cb39333cc986abda54f467df71eecc5791358502',receipt_sha256='5c21282863bbbfb129ce59fa0cf861d18c6f0fe77af16a62a2a3c3fd3fe1f243')}
INPUTS={};IDENTITIES=[];np=None
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def bind(n,h):
 p=BASE/n;assert h is not None and sha(p)==h,n;key=str(p.resolve());assert key not in INPUTS or INPUTS[key]==h;INPUTS[key]=h
def mapped(mapping,n):return mapping[n] if n in mapping else mapping[str((BASE/n).resolve())]
def auth(stem,t):
 for n,h in ((t['source'],t['source_sha256']),(stem+'.md',t['protocol_sha256']),(stem+'_RESULT.json',t['result_sha256']),(stem+'_RECEIPT.json',t['receipt_sha256'])):bind(n,h)
 r=json.loads((BASE/(stem+'_RESULT.json')).read_text());c=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
 assert c['status']=='CLOSED' and c['error_sha256'] is None and c['result_sha256']==t['result_sha256'] and c['owner']==r['owner']
 assert r['owner']['pid']==t['pid'] and r['owner']['source_sha256']==t['source_sha256'] and c['qualification']==r['qualification'] and all(v is False for v in r['qualification'].values())
 return r,c
def read(ref,mapping,names=None):
 for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert mapped(mapping,n)==h;bind(n,h)
 rec=json.loads((BASE/ref['commit_file']).read_text());assert rec=={k:ref[k] for k in ('file','sha256','metadata')}
 schema=ref['metadata']['schema'];names=tuple(schema) if names is None else tuple(names)
 with np.load(BASE/ref['file'],allow_pickle=False) as f:
  assert set(f.files)==set(schema)|{'metadata_json'} and json.loads(str(f['metadata_json'].item()))==ref['metadata'];out={n:f[n].copy() for n in names}
 for n,a in out.items():assert list(a.shape)==schema[n]['shape'] and str(a.dtype)==schema[n]['dtype'] and a.dtype.kind in 'fiub' and np.all(np.isfinite(a))
 return out
def identity(name,a,e,v):
 a,e,v=np.broadcast_arrays(np.asarray(a,dtype=float),np.asarray(e,dtype=float),np.asarray(v,dtype=float));assert np.all(np.isfinite(a)) and np.all(np.isfinite(e)) and np.all(np.isfinite(v)) and np.all(v>=0)
 rat=abs(a-e)/np.maximum(v,1e-30);idx=np.unravel_index(int(np.argmax(rat)),rat.shape);error=float(rat[idx]);IDENTITIES.append(dict(name=name,error=error,actual=float(a[idx]),expected=float(e[idx]),envelope=float(v[idx]),index=list(map(int,idx))));assert error<=TOL,(name,IDENTITIES[-1]);return error
def control(raw,c,prefix):
 a,e,v=(raw[prefix+n] for n in ('actual','expected','envelope'));err=identity(c['name'],a,e,v)
 assert c['passed'] is True and c['tolerance']==TOL and math.isclose(err,c['error'],rel_tol=2e-13,abs_tol=1e-30)
def pair(raw,name):return raw[name+'_hi'],raw[name+'_lo']
def bound(x):return abs(x[0])+abs(x[1])
def gap(raw,name,left,right):
 a,b,g=pair(raw,left),pair(raw,right),pair(raw,name);identity(name,(a[0]+a[1])-(b[0]+b[1]),g[0]+g[1],bound(a)+bound(b)+bound(g))
def norms(x):
 a=x[0]+x[1];return dict(L2=float(np.linalg.norm(a)),Linf=float(np.max(abs(a))),signed_sum=float(np.sum(a)),hi_L2=float(np.linalg.norm(x[0])),lo_L2=float(np.linalg.norm(x[1])))
def packet():
 global np
 results=[auth(s,t) for s,t in TERMINALS.items()]
 import numpy as numpy_module
 np=numpy_module;(r,c),(b,bc)=results;assert len(r['controls'])==12 and len(r['checkpoints'])==6 and len(b['controls'])==2
 assert r['contact_refs']==r['checkpoints'][1:5] and r['loads']==r['checkpoints'][5] and r['quadrature_contacts']==16
 assert all(r[k] is False for k in ('configuration_updated','global_induced_rate_computed','normal_rank_qualified','original_affine_bridge_admitted','physical_adoption'))
 assert all(b[k] is False for k in ('local_source_added','original_state_changed','physical_zero_gate','velocity_bound'))
 refs=r['checkpoints'];new=[read(q,c['output_sha256']) for q in refs];bench=read(b['checkpoint'],bc['output_sha256'])
 for stem,rr in ((list(TERMINALS)[0],refs),(list(TERMINALS)[1],[b['checkpoint']])):
  assert {p.name for p in BASE.glob(stem+'*.npz')}=={q['file'] for q in rr}
 phase={};phase_names=('delta_canonical_density_action','delta_canonical_density_registered_literal','delta_canonical_density_registered_owned','delta_action_minus_owned_registered_density')
 for iq,(ref,raw) in enumerate(zip(r['contact_refs'],new[1:5])):
  assert ref['metadata']['column']==iq and ref['metadata']['controls']==r['controls'][3*iq:3*iq+3]
  for k in range(3):ctl=r['controls'][3*iq+k];control(raw,ctl,'control_%03d_%s_'%(3*iq+k,ctl['name']))
  for n,left,right in [('base_action_minus_registered_current','base_current_action','base_current_registered_literal'),('delta_action_minus_registered_current','delta_current_action','delta_current_registered'),('base_action_minus_owned_density','base_canonical_density_action','owned_canonical_density'),('base_registered_literal_minus_owned_density','base_canonical_density_registered_literal','owned_canonical_density'),('delta_action_minus_owned_registered_density','delta_canonical_density_action','delta_canonical_density_registered_owned')]:gap(raw,'delta_phase_'+n,'delta_phase_'+left,'delta_phase_'+right)
  parent=ref['metadata']['parent'];owned=read(parent,c['input_sha256'],('unchanged_new_phase_current','unchanged_new_phase_canonical_density'));indices=raw['indices'];assert indices.dtype==np.int64 and indices.shape==(4,) and np.all((indices>=0)&(indices<3784))
  literal=pair(raw,'delta_phase_base_current_registered_literal');g=pair(raw,'delta_phase_base_registered_literal_minus_owned_current');J=owned['unchanged_new_phase_current'][indices]
  identity('column_%d_registered_minus_owned_current'%iq,literal[0]+literal[1]-J,g[0]+g[1],bound(literal)+abs(J)+bound(g));p=pair(raw,'delta_phase_owned_canonical_density');assert np.array_equal(p[0],owned['unchanged_new_phase_canonical_density'][indices]) and np.all(p[1]==0)
  for total,left,right in [('metric_total_density','metric_native_density','metric_EH_density'),('connection_momentum','connection_D','connection_Maxwell')]:
   a,l,h=(pair(raw,'delta_momentum_'+n) for n in (total,left,right));identity('column_%d_'%iq+total,a[0]+a[1],l[0]+l[1]+h[0]+h[1],bound(a)+bound(l)+bound(h))
  for name in phase_names:phase.setdefault(name,[]).append(pair(raw,'delta_phase_'+name))
 for ctl in b['controls']:control(bench,ctl,'control_'+ctl['name']+'_')
 saved,negative,diff=(bench[n] for n in ('saved_lapse_rounded','negative_homogeneous_shortfall','descriptive_difference_from_negative_reference'))
 assert np.array_equal(bench['saved_lapse_hi'],bench['loaded_normal_Hamiltonian_rows_hi'][0]) and np.array_equal(bench['saved_lapse_lo'],bench['loaded_normal_Hamiltonian_rows_lo'][0]) and b['reference_sign']=='negative'
 identity('benchmark_reference_density',b['reference_density'],bench['reference_scalars_eta_C_ordinary_phase_EH'][2],abs(b['reference_density'])+abs(bench['reference_scalars_eta_C_ordinary_phase_EH'][2]))
 phase_scalar,EH_scalar=bench['reference_scalars_eta_C_ordinary_phase_EH'][3:5];identity('benchmark_phase_EH_shortfall',b['reference_phase_EH_shortfall'],phase_scalar+EH_scalar,abs(b['reference_phase_EH_shortfall'])+abs(phase_scalar)+abs(EH_scalar))
 identity('benchmark_saved_lapse_words',saved,bench['saved_lapse_hi']+bench['saved_lapse_lo'],abs(saved)+abs(bench['saved_lapse_hi'])+abs(bench['saved_lapse_lo']))
 identity('benchmark_difference',diff,saved-negative,abs(diff)+abs(saved)+abs(negative))
 sn,rn,dn=(float(np.linalg.norm(x)) for x in (saved,negative,diff));rm=float(np.max(abs(negative)));assert rn>0 and rm>0
 expected=dict(saved_lapse_L2=sn,negative_reference_L2=rn,difference_L2=dn,difference_L2_over_reference=dn/rn,difference_Linf_over_reference=float(np.max(abs(diff)))/rm,unrestricted_volume=float(np.sum(bench['analytic_volume'])),restricted_volume=float(np.sum(bench['restricted_analytic_volume'])))
 for n,v in expected.items():identity('benchmark_'+n,b[n],v,abs(b[n])+abs(v))
 node=tuple(b['largest_saved_node']['indices']);assert node==np.unravel_index(int(np.argmax(abs(saved))),saved.shape)
 for n,a in (('saved',saved),('negative_reference',negative),('difference',diff)):assert b['largest_saved_node'][n]==float(a[node])
 assert b['largest_saved_node']['R_kpc']==float(bench['loaded_r'][node[0]]) and b['largest_saved_node']['Z_kpc']==float(bench['loaded_z'][node[1]])
 for n,v in INPUTS.items():assert sha(n)==v
 return dict(status='SAVED_COMPACT_CONTACT_AND_REFERENCE_CLOSURE_PASS',pid=os.getpid(),parent_terminals=TERMINALS,controls=14,committed_pairs=7,identities=len(IDENTITIES),maximum_identity_error=max(x['error'] for x in IDENTITIES),identities_detail=IDENTITIES,compact_patch_norms={n:norms(pair(new[-1],'weak_'+n)) for n in ('native','metric','trace_Gamma','trace_ADM')},phase_density_contact_point_norms={n:norms((np.concatenate([x[0] for x in a]),np.concatenate([x[1] for x in a]))) for n,a in phase.items()},benchmark_descriptive_norms=expected,original_affine_and_actual_target_ratios=r['original_affine_and_actual_target_ratios'],qualification=dict(compact=r['qualification'],reference=b['qualification']),phase_norms_are_unintegrated_16_point_contacts=True,physical_zero_gate=False,physical_state_or_source_adopted=False,producer_formula_helper_FE_operator_or_solver_replayed=False)
def main():
 assert AUTHOR_DRAFT is False,'Root review/release required';assert not list(BASE.glob(STEM+'_*')),'Prior verifier outputs preserved';own=sha(__file__)
 try:
  result=packet();assert sha(__file__)==own;result['audit_source_sha256']=own;out=BASE/(STEM+'_RESULT.json');out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n');out.chmod(0o444);print(json.dumps(dict(status=result['status'],pid=os.getpid(),sha256=sha(out))),flush=True)
 except BaseException:
  out=BASE/(STEM+'_ERROR.json');out.write_text(json.dumps(dict(pid=os.getpid(),source_sha256=own,identities=IDENTITIES,traceback=traceback.format_exc()),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n');out.chmod(0o444);raise
if __name__=='__main__':main()
