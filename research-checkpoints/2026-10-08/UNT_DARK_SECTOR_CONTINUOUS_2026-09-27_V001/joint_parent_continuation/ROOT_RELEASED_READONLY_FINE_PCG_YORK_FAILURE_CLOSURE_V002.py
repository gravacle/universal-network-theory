"""Held stored fine-PCG words/contacts only; no producer or operator replay."""
from pathlib import Path
import ast,hashlib,json,math,os,struct,zipfile
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V006'
OUT='READONLY_FINE_PCG_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='a4c442fa10a50fe63e5cc5c70984786d23e171cd936b5aa6f7313f4ac412b6ef'
PROTOCOL_SHA='5ecfa2446693b60e669a16e6cf2dfb954fd4b67731a30b1a98c412b676287f2d'
TERMINAL={'pid': 74275, 'result_sha256': None, 'receipt_sha256': '73db4994b09f24d11b6d7aa4951c5e320ae7fb97fe372a825908df6119e05860', 'error_sha256': '3b0418ecfc32f540e50bc7220c5f4748e5e16b910dfedaf273789c2c0449b627'}
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V005'
PARENT_RESULT_SHA='a3aaf3f4b938b621d6491d3fc9fcc4b4a5d2b05e71bf0b4a588eab08d8547ccb'
PARENT_RECEIPT_SHA='eefef813468b05e23aa47a872c3128916d3a93cb45fc55b10cf180244aa3ff5c'
PARENT_PROOF=('READONLY_WARM_TWOLEVEL_YORK_PROJECTION_CLOSURE_V001_RESULT.json','9ba456c04cb20263bf43a5a04325531a727ae5f93a04bbe5608b1deb6c53771b')
TOL=2e-11;ROW_TOL=1e-10

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def js(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists(),'Reviewed actual natural closure required before I/O'
 assert TERMINAL['result_sha256'] is None and TERMINAL['error_sha256'] is not None
 assert sha('cross_u_compact_york_longitudinal_projection_v006.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=False;assert rc['status']=='CLOSED_ERROR'
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 import numpy as np
 selected=[];identities=[]
 def seal(q,output=True):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert (rc['output_sha256'][n] if output else rc['input_sha256'][str(path(n).resolve())])==h and sha(n)==h,n
  committed=js(q['commit_file'],q['commit_sha256']);assert committed['file']==q['file'] and committed['sha256']==q['sha256']
  if 'metadata' in q:assert committed['metadata']==q['metadata']
 def headers(q):
  with zipfile.ZipFile(path(q['file'])) as z:
   assert set(z.namelist())=={n+'.npy' for n in q['metadata']['schema']}|{'metadata_json.npy'}
   for n,s in q['metadata']['schema'].items():
    with z.open(n+'.npy') as f:
     assert f.read(6)==b'\x93NUMPY';v=f.read(2);assert v in (b'\x01\x00',b'\x02\x00',b'\x03\x00');h=struct.unpack('<H' if v[0]==1 else '<I',f.read(2 if v[0]==1 else 4))[0];hd=ast.literal_eval(f.read(h).decode('utf8' if v[0]==3 else 'latin1'))
    assert list(hd['shape'])==s['shape'] and str(np.dtype(hd['descr']))==s['dtype'] and np.dtype(hd['descr']).kind in 'fiub',n
  if closed:assert all(s['finite'] is True for s in q['metadata']['schema'].values())
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms,envelope=None):
  parts=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(parts);bound=np.add.reduce([abs(v) for v in parts]) if envelope is None else envelope
  assert gap.shape==bound.shape and np.all(bound>=0);error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def row_ratios(res,rhs,scale):
  cuts=(0,3740,7395,11135);out=[]
  for i in range(3):
   s=slice(cuts[i],cuts[i+1]);a=np.linalg.norm(rhs[s]);b=np.linalg.norm(rhs[s]/scale[s]);assert a>0 and b>0;out.append((np.linalg.norm(res[s])/a,np.linalg.norm(res[s]/scale[s])/b))
  return np.asarray(out)
 for q in records:
  seal(q);headers(q);assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=3 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 for c in controls:
  p='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(p+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 assert r['status']=='FAILED' and r['owner']['pid']==74275 and len(controls)==2 and all(c['passed'] for c in controls) and len(records)==3 and not path(STEM+'_RESULT.json').exists()
 kinds=('all_V005_INPUT_and_latest_paired_seed_for_direct_fine_PCG','fresh_coupled_anisotropic_fine_PCG_with_same_generic_loop','available_NEW_fine_PCG_vectors_contacts_and_history')
 assert tuple(q['metadata']['kind'] for q in records)==kinds
 inp,fixture,raw=records;assert not inp['metadata']['failed'] and not fixture['metadata']['failed'] and raw['metadata']['failed'] and len(inp['metadata']['schema'])==478 and len(fixture['metadata']['schema'])==178 and len(raw['metadata']['schema'])==59
 assert r['context']['stage']=='new_fine_paired_PCG' and r['context']['iteration']==1 and r['context']['cap']==512 and raw['metadata']['context']==r['context']
 assert 'york_fine_pcg_action' in r['traceback'] and not any(n.startswith('fine_york_PCG_node_update_') for n in raw['metadata']['schema'])
 assert fixture['metadata']['cap']==12 and fixture['metadata']['original_rows_admitted'] and fixture['metadata']['old_York_or_twolevel_fixture_replayed'] is False
 for n,h in ((PARENT+'_RESULT.json',PARENT_RESULT_SHA),(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA),PARENT_PROOF):assert rc['input_sha256'][str(path(n).resolve())]==h
 previous=js(PARENT+'_RESULT.json',PARENT_RESULT_SHA);proof=js(*PARENT_PROOF)
 assert previous['owner']['pid']==71992 and previous['original_rows_admitted'] is False and proof['status']=='SAVED_WARM_TWOLEVEL_YORK_CLOSURE_PASS' and proof['parent']==dict(pid=71992,result_sha256=PARENT_RESULT_SHA,receipt_sha256=PARENT_RECEIPT_SHA,error_sha256=None)
 assert inp['metadata']['parent_input']==thin(previous['input']) and inp['metadata']['parent_solution']==thin(previous['solution']) and inp['metadata']['earned_coarse_ref']==previous['earned_coarse_ref']
 assert inp['metadata']['all_360_parent_input_fields_bitcopied'] and inp['metadata']['new_latest_solution_prefix']=='fine_pcg_seed_' and inp['metadata']['latest_SOLUTION_loaded_before_INPUT'] and inp['metadata']['coarse_Gram_factor_fixture_or_old_iterations_replayed'] is False
 assert inp['metadata']['preserved_parent_controls']==previous['controls'] and inp['metadata']['preserved_parent_checkpoints']==previous['checkpoints'] and fixture['metadata']['controls']==controls
 for q in (previous['input'],previous['solution'],previous['earned_coarse_ref']):seal(q,False)
 warm=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale')
 coarse=tuple('new_coarse_'+n for n in ('fine_to_coarse_i','fine_to_coarse_j','physical_node_interpolation_weights','coarse_hat_values_at_fine_cell_corners','coarse_global_local_indices','coarse_mask','coarse_positive_scale','normalized_coarse_Cholesky'))
 assert len(previous['input']['metadata']['schema'])==360
 with np.load(path(inp['file']),allow_pickle=False) as new,np.load(path(previous['input']['file']),allow_pickle=False) as original,np.load(path(previous['solution']['file']),allow_pickle=False) as latest,np.load(path(previous['earned_coarse_ref']['file']),allow_pickle=False) as factor:
  for n,sc in previous['input']['metadata']['schema'].items():assert inp['metadata']['schema'][n]==sc and original[n].tobytes()==new[n].tobytes(),n
  assert {n for n in inp['metadata']['schema'] if n.startswith('fine_pcg_seed_')}=={'fine_pcg_seed_'+n for n in warm}
  for n in warm:assert inp['metadata']['schema']['fine_pcg_seed_'+n]==previous['solution']['metadata']['schema'][n] and latest[n].tobytes()==new['fine_pcg_seed_'+n].tobytes(),n
  for n in coarse:assert factor[n].tobytes()==new['continued_coarse_'+n].tobytes(),n
 report=dict(status='SAVED_FINE_PCG_YORK_FAILURE_PRESERVED',producer_status=r['status'],original_terminal_status='CLOSED_ERROR',controls=2,committed_pairs=3,failed_raw_fields=59,immutable_parent_INPUT_fields=360,all_immutable_parent_INPUT_fields_bitcopied=True,distinct_latest_final_solution_fields=11,selected_earned_coarse_fields_bitcopied=8,earned_fresh_fixture_preserved=True,actual_node_update_earned=False,original_rows_admitted=False,compact_weak_TT_original_rows_admitted=False,context=r['context'])
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_identity_tolerance=TOL,original_row_tolerance=ROW_TOL,L_point_energy_Gram_triangle_preconditioner_operator_PCG_FE_or_fixture_replayed=False,physical_adoption=False,scope_limit='Authentic failed publication and earned INPUT/FIXTURE words, bitcopies and triplets only. The first actual direction action/tensors/bounds survive in ERROR_RAW; no independent contraction, actual node update or original-row admission is claimed. No replacement producer packet is created.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v006.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
