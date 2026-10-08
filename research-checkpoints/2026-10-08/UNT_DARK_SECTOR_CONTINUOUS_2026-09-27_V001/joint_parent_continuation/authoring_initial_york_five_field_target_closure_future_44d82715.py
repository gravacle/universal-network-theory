"""Selected saved five-field target words; no helper, L, FE or producer replay."""
from pathlib import Path
from decimal import Decimal,localcontext
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_INITIAL_YORK_FIVE_FIELD_TARGET_CONTACTS_V001'
SOURCE='cross_u_initial_york_five_field_target_contacts_v001.py'
SOURCE_SHA='063c5248f3b0ce0bd0190289e1715a5c4083b9a1075fe73d56d6fed08360eaa5'
PROTOCOL_SHA='ab2742209785d3e374a0d6f22d2ccc5949eeca771a157c7e93ad86af93e2ad4b'
OUT='READONLY_INITIAL_YORK_FIVE_FIELD_TARGET_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None)
FIELDS=('a','W_R','W_Z','W_phi','t')
TOL=2e-11

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def main():
 assert AUTHOR_DRAFT is False and all(v is not None for v in TERMINAL.values()),'Root release and actual natural CLOSED terminal required before I/O'
 assert not path(OUT).exists();seals={};selected=[];identities=[]
 def seal(n,h):assert sha(n)==h,n;seals[n]=h
 for n,h in ((STEM+'_RESULT.json',TERMINAL['result_sha256']),(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']),(SOURCE,SOURCE_SHA),(STEM+'.md',PROTOCOL_SHA)):seal(n,h)
 r=json.loads(path(STEM+'_RESULT.json').read_text());rc=json.loads(path(STEM+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==TERMINAL['result_sha256'] and rc['owner']==r['owner']
 assert r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_file']==SOURCE and r['owner']['source_sha256']==SOURCE_SHA
 assert r['status']=='INITIAL_YORK_FIVE_FIELD_TARGET_CONTACTS_MEASURED' and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 assert r['owned_PiTF_as_current_S_test_only'] is True and all(r[n] is False for n in ('auxiliary_W_state_admitted','canonical_primitive_bridge_resolved','physical_adoption'))
 records=r['checkpoints'];controls=r['controls'];assert len(records)==7 and len({q['file'] for q in records})==7 and len(controls)==2
 assert r['input']==records[0] and r['fixture']==records[1] and r['columns']==records[2:6] and r['loads']==records[6]
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,k in ((q['file'],'sha256'),(q['commit_file'],'commit_sha256')):assert rc['output_sha256'][n]==q[k];seal(n,q[k])
  assert json.loads(path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')}
  assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False and all(s['finite'] is True for s in q['metadata']['schema'].values())
 assert r['input']['metadata']['node']==[43,22] and r['input']['metadata']['fields']==list(FIELDS) and r['input']['metadata']['W_state_admitted'] is False and r['input']['metadata']['physical_ports'] is None
 assert r['fixture']['metadata']['controls']==controls[:1] and r['loads']['metadata']['controls']==controls
 assert [c['ordinal'] for c in controls]==[0,1] and all(c['passed'] is True and c['tolerance']==TOL and math.isfinite(c['error']) and c['error']<=TOL for c in controls)
 import numpy as np
 def read(q,names):
  out={};schema=q['metadata']['schema']
  with np.load(path(q['file']),allow_pickle=False) as z:
   assert set(z.files)==set(schema)|{'metadata_json'} and json.loads(str(z['metadata_json']))==q['metadata']
   for n in names:
    x=z[n].copy();assert list(x.shape)==schema[n]['shape'] and str(x.dtype)==schema[n]['dtype'] and schema[n]['finite'] is True and np.all(np.isfinite(x)),n;out[n]=x
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def stats(x):return dict(L2=float(np.linalg.norm(x)),Linf=float(np.max(abs(x),initial=0)),nonzero=int(np.count_nonzero(x)))
 triplets=[]
 for c,q in zip(controls,(r['fixture'],r['loads'])):
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);a=read(q,tuple(prefix+n for n in ('actual','expected','envelope')));x,y,e=(a[prefix+n] for n in ('actual','expected','envelope'))
  assert x.shape==y.shape==e.shape and np.all(e>=0);err=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert np.isclose(err,c['error'],rtol=TOL,atol=1e-300) and err<=TOL
  identities.append(dict(name=c['name'],error=err));triplets.append((x,y,e))
 assert triplets[0][0].shape==(16,) and triplets[1][0].shape==(5,) and np.all(triplets[1][1]==0)
 loads=r['loads'];assert loads['metadata']['fields']==list(FIELDS) and loads['metadata']['coupled_coordinates']==403340 and loads['metadata']['metric_coordinates']==23048
 assert loads['metadata']['columns']==[{n:q[n] for n in ('file','sha256','commit_file','commit_sha256')} for q in r['columns']] and loads['metadata']['physical_ports'] is None and loads['metadata']['ordinary_and_phase_targets_unchanged'] is True
 assert loads['metadata']['global_rate_response_computed'] is False and loads['metadata']['canonical_primitive_bridge_resolved'] is False
 names=tuple(field+'_'+part+'_'+word for field in FIELDS for part in ('weak_metric_target','full_coupled_target_RHS','nodal_functional','direct_functional','functional_gap') for word in ('hi','lo'))
 a=read(loads,names);mask=np.ones((6,87,45),dtype=bool);mask[:,0]=False;mask[3:5,:,0]=False;assert np.count_nonzero(mask)==23048
 weak_norms={};functional_words={}
 for i,field in enumerate(FIELDS):
  weak=pair(a,field+'_weak_metric_target');packed=pair(a,field+'_full_coupled_target_RHS')
  for w in (0,1):
   assert weak[w].shape==(6,87,45) and packed[w].shape==(403340,) and np.all(packed[w][:380292]==0) and np.array_equal(packed[w][380292:],weak[w][mask])
   identities.append(dict(name=field+'_exact_saved_metric_RHS_pack_'+('hi' if w==0 else 'lo'),error=0.))
  scalar=[pair(a,field+'_'+p) for p in ('nodal_functional','direct_functional','functional_gap')];assert all(x.shape==() for pair_words in scalar for x in pair_words)
  with localcontext() as ctx:
   ctx.prec=80;terms=[Decimal.from_float(float(v))*s for pair_words,s in zip(scalar,(1,-1,-1)) for v in pair_words];gap=sum(terms);bound=sum(abs(v) for v in terms);error=float(abs(gap)/max(bound,Decimal('1e-30')))
  assert error<=TOL,(field,error);identities.append(dict(name=field+'_stored_nodal_minus_direct_minus_gap',error=error))
  assert float(scalar[2][0]+scalar[2][1])==float(triplets[1][0][i])
  weak_norms[field]=dict(readout=stats(weak[0]+weak[1]),high_word=stats(weak[0]),low_word=stats(weak[1]));functional_words[field]={p:[float(v) for v in words] for p,words in zip(('nodal','direct','gap'),scalar)}
 point_norms={field:[] for field in FIELDS}
 for iq,q in enumerate(r['columns']):
  md=q['metadata'];assert md['column']==iq and md['node']==[43,22] and md['fields']==list(FIELDS) and md['reference_mu_held_fixed'] is True and md['all_map_cross_terms_retained'] is True and md['S_is_owned_PiTF_test_only'] is True and md['TT_free_prior_admitted'] is False and md['physical_ports'] is None
  b=read(q,tuple(field+'_delta_target_six_coordinate_density_'+word for field in FIELDS for word in ('hi','lo')))
  for field in FIELDS:
   x=pair(b,field+'_delta_target_six_coordinate_density');assert x[0].shape==x[1].shape==(4,6);point_norms[field].append(stats(x[0]+x[1]))
 for n,h in seals.items():assert sha(n)==h,n
 proof=dict(status='SAVED_INITIAL_YORK_FIVE_FIELD_TARGET_CLOSURE_PASS',owner_pid=os.getpid(),parent=TERMINAL,controls=2,committed_pairs=7,identities=identities,maximum_error=max(x['error'] for x in identities),arithmetic_tolerance=TOL,selected=selected,weak_target_norms=weak_norms,compact_column_target_norms=point_norms,saved_functional_words=functional_words,packing_coordinates=dict(native=380292,metric=23048,total=403340),canonical_primitive_bridge_resolved=False,TT_free_prior_admitted=False,global_rate_response_computed=False,global_rank_claimed=False,physical_adoption=False,old_target_helper_L_map_FE_scatter_fixture_or_producer_replayed=False,old_input_maps_rehashed=False,scope_limit='Seven sealed records, stored triplets, exact saved RHS word packing, scalar-word identities and descriptive target norms only.')
 with path(OUT).open('x') as f:json.dump(proof,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=proof['status'],owner_pid=os.getpid(),sha256=sha(OUT))),flush=True)

if __name__=='__main__':main()
