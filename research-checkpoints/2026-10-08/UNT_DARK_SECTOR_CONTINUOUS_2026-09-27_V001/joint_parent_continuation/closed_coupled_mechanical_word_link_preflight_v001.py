"""HELD completion of two mechanical source-link families; no88-link replay or norm/action arithmetic."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,traceback
import numpy as np
B=Path(__file__).resolve().parent
STEM='ROOT_CLOSED_COUPLED_MECHANICAL_WORD_LINK_PREFLIGHT_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
ROOT_EXECUTOR_RELEASE=None
PROTOCOL='CLOSED_COUPLED_MECHANICAL_WORD_LINK_PREFLIGHT_V001.md'
PROTOCOL_SHA=None
PARENT_SOURCE=('closed_coupled_source_word_link_preflight_v001.py','7daf23d11fcdfd5d06faed1f2d07a24bc84a871b7acdd3ed458f0c3c9d022bbc')
SELECTED=('NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_V003.json','7bceaa8396fed1f7635ddcaac194e3939f8fb21aef229d079f75e6b83e516f70')
MECHANICAL=('ROOT_ACTUAL_CLOSED_SECOND_CYCLE_MECHANICAL_SELECTORS_V001.json','27c6d4dae409839e6abb7160bea2d8ef201a87c1a0e43ccf08eb648bb4241fbb')
PRIOR82=('ROOT_CLOSED_COUPLED_SOURCE_WORD_LINK_PREFLIGHT_V001_RESULT.json','bbba9cb1960c35709ea41fa939a5473e2bb851806342ada1ad3ea93c217b65bd')
PRIOR88=('ROOT_CLOSED_COUPLED_DEFERRED_PHASE_WORD_LINK_PREFLIGHT_V002_RESULT.json','71bbd6cd71c3f7c7bd7071560aaff8890318be9d4b7f799efdf25df3d2c29f3c')
SOURCE53=('author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py','25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c')
FAMILIES=((10,'mechanical_adjoint_eL_rhs'),(11,'mechanical_lambda_argument'))
VERIFIED={};STATS={};TERMINALS={};DONE=[];CONTEXT={}
def snapshot(p):
 s=p.stat();return dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777),dataless=bool(s.st_flags&0x40000000))
def bind(n,h):
 p=B/n;key=str(p.resolve());before=snapshot(p);assert not before['dataless'],n
 if key not in VERIFIED:
  H=hashlib.sha256()
  with p.open('rb') as f:
   while a:=f.read(1024*1024):H.update(a)
  assert H.hexdigest()==h,n;assert snapshot(p)==before,n
  VERIFIED[key]=h;STATS[key]=before
 else:assert VERIFIED[key]==h and STATS[key]==before,n
 return p
def seal(n,v):
 raw=(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();p=B/n
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);return hashlib.sha256(raw).hexdigest()
def terminal(name,t):
 if name in TERMINALS:return TERMINALS[name]
 source,result,receipt,proof=t
 for r in t:bind(*r[:2])
 rc=json.loads((B/receipt[0]).read_bytes());pr=json.loads((B/proof[0]).read_bytes())
 assert rc['status']==receipt[2]=='CLOSED' and rc['result_sha256']==result[1] and rc['error_sha256'] is None
 assert pr['status']==proof[2] and pr['source_sha256']==source[1] and pr['result_sha256']==result[1] and pr['receipt_sha256']==receipt[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_success_role_seals_verified'] is True
 assert rc['owner']==pr['owner'] and rc['owner']['source_sha256']==source[1]
 TERMINALS[name]=(rc,pr);return rc,pr
def record(wrap,terminals):
 ref=wrap['reference'];rc,pr=terminal(wrap['terminal'],terminals[wrap['terminal']])
 for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):
  bind(n,h)
  if rc['output_sha256'].get(n)!=h:
   assert wrap['terminal']=='finite139' and pr['all_inherited_success_role_seals_verified'] is True
   ancestor=wrap['ancestor_seal_proof'];bind(*ancestor[:2])
   inherited=pr['inherited_readonly_seal_stats'][str((B/n).resolve())]
   assert inherited['sha256']==h,n
 c=json.loads((B/ref['commit_file']).read_bytes());assert c['file']==ref['file'] and c['sha256']==ref['sha256'] and c['metadata']['owner']==wrap['scientific_owner']
 assert c['metadata']['failed'] is False and all(a is False for a in c['metadata']['qualification'].values())
 return ref,c['metadata']

def endpoint(e,records,terminals):
 wrap=records[e['$record']];ref,md=record(wrap,terminals);arrays=[]
 assert e['$dtype'] in ('float64','bool')
 with np.load(B/ref['file'],allow_pickle=False) as z:
  assert json.loads(str(z['metadata_json']))==md
  for key in e['$keys']:
   a=z[key];assert str(a.dtype)==e['$dtype'] and list(a.shape)==e['$shape'] and np.all(np.isfinite(a)),key
   assert md['schema'][key]==dict(shape=list(a.shape),dtype=e['$dtype'],finite=True),key
   arrays.append(a)
 return arrays

def compare(name,left,right,records,terminals,family=None):
 CONTEXT.clear();CONTEXT.update(name=name,left=left,right=right,family=family)
 a=endpoint(left,records,terminals);b=endpoint(right,records,terminals);assert len(a)==len(b)
 words=[];mismatches=[]
 for j,(x,y) in enumerate(zip(a,b)):
  assert x.shape==y.shape and x.dtype==y.dtype
  bits=np.uint64 if x.dtype==np.float64 else np.uint8;equal=np.equal(x.view(bits),y.view(bits));words.append(bool(np.all(equal)))
  if not words[-1]:
   f=np.flatnonzero(~equal.ravel());k=int(f[0]);mismatches.append(dict(word=j,count=int(f.size),first_flat_index=k,left_bits=hex(int(x.view(bits).ravel()[k])),right_bits=hex(int(y.view(bits).ravel()[k]))))
 row=dict(name=name,family=family,left=left,right=right,exact_word_ties=words,all_exact=all(words),mismatches=mismatches)
 DONE.append(row);seal(STEM+'_%02d_WORD_LINK.json'%(len(DONE)-1),row);assert row['all_exact'],name
 return row

def member(record_name,keys,shape,dtype='float64'):
 return {'$record':record_name,'$keys':list(keys),'$shape':list(shape),'$dtype':dtype}

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and ROOT_EXECUTOR_RELEASE is not None and PROTOCOL_SHA is not None
 assert not list(B.glob(STEM+'_*'));bind(Path(__file__).name,hashlib.sha256(Path(__file__).read_bytes()).hexdigest());bind(PROTOCOL,PROTOCOL_SHA);bind(*PARENT_SOURCE);bind(*SOURCE53)
 try:
  prior=json.loads(bind(*PRIOR88).read_bytes());first=json.loads(bind(*PRIOR82).read_bytes());v=json.loads(bind(*SELECTED).read_bytes());m=json.loads(bind(*MECHANICAL).read_bytes());c=m['component']
  assert prior['status']=='CLOSED_DEFERRED_PHASE_SOURCE_WORD_LINK_PREFLIGHT_MEASURED' and prior['selected_assembly']==list(SELECTED)
  assert prior['inherited_preflight_result'][:2]==list(PRIOR82) and prior['combined_closed_links_checked']==88 and prior['combined_checked_links_all_exact'] is True
  assert prior['first82_word_ties_recomputed'] is prior['physical_adoption'] is prior['all90_runtime_links_admitted'] is False
  assert first['closed_links_checked']==82 and first['checked_links_all_exact'] is True and len(first['links'])==82
  assert len(prior['links'])==6 and all(q['all_exact'] is True for q in prior['links'])
  assert {(q['ordinal'],q['name']) for q in prior['deferred']}==set(FAMILIES) and len(v['word_links'])==90
  assert {(i,v['word_links'][i]['name']) for i,n in FAMILIES}==set(FAMILIES)
  assert m['status']=='ACTUAL_CLOSED_SECOND_CYCLE_MECHANICAL_SELECTORS_PREPARED_HELD' and m['numerical_arrays_decoded'] is m['physical_adoption'] is m['all13group_runtime_map_admitted'] is False
  assert c['cycle_number']==2 and c['same_NEW_eL_source_and_original53_reference'] is c['current_cycle_fresh_basis'] is True and c['physical_adoption'] is False
  assert c['operator']=='represented_directed_original244_coefficient_Astar'
  t=m['actual_terminal'];assert t[1][2]=='SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_ADMITTED'
  terminals=dict(mechanical_adjoint=t,inherited_warm=c['inherited_RHS_terminal'],literal220=v['terminals']['literal220'])
  rc,proof=terminal('mechanical_adjoint',t);warm_rc,warm_proof=terminal('inherited_warm',terminals['inherited_warm']);terminal('literal220',terminals['literal220'])
  assert proof['source_relative_adjoint_rows_admitted'] is proof['all_original_construction_controls_passed'] is True and proof['measurement_status']==t[1][2]
  assert proof['case_history']['same_NEW_eL_source_and_original53_reference'] is True and proof['case_history']['new_rhs'] is False and proof['cycle_number']==2
  assert warm_rc['owner']['pid']==89302 and terminals['inherited_warm'][1][2]=='NEW_E_L_SAVED_WARM_RESIDUAL_MEASURED_REFINEMENT_REQUIRED'
  required=('mech_solution','mech_candidate','mech_warm_reference','mech_additional_context');records={n:c['records'][n] for n in required};metadata={}
  for n in required:
   assert records[n]['terminal']=='mechanical_adjoint' and records[n]['success_role_membership_verified'] is True;_,metadata[n]=record(records[n],terminals)
  assert proof['total_lambda_source_certificate']==records['mech_solution']['reference'] and proof['warm_reference_context']==records['mech_warm_reference']['reference'] and proof['additional_cycle_context']==records['mech_additional_context']['reference']
  wr=metadata['mech_warm_reference'];assert wr['source_records']['WARMSTART_CONTEXT']==c['inherited_RHS_context'] and wr['warm_terminal']==terminals['inherited_warm']
  records['warm_rhs']=dict(reference=c['inherited_RHS_context'],terminal='inherited_warm',scientific_owner=warm_rc['owner'])
  records['warm_measured']=dict(reference=wr['source_records']['MEASURED_ADMISSION'],terminal='inherited_warm',scientific_owner=warm_rc['owner'])
  records['literal220_weak_bridge']=v['records']['literal220_weak_bridge']
  for n in ('warm_rhs','warm_measured','literal220_weak_bridge'):_,metadata[n]=record(records[n],terminals)
  assert metadata['warm_rhs']['fresh_eL']==records['literal220_weak_bridge']['reference'] and metadata['warm_rhs']['NEW_initial_source_rows_admitted'] is False
  assert metadata['warm_measured']['source_relative_adjoint_rows_admitted'] is False and metadata['warm_measured']['refinement_required'] is True
  assert metadata['literal220_weak_bridge']['eL_sign']=='epsilon minus (literal minus registered)' and metadata['literal220_weak_bridge']['stationarity_or_feedback_zero_assumed'] is False
  assert metadata['mech_solution']['NEW_RHS_feedback_admission'] is metadata['mech_candidate']['admitted'] is True
  assert metadata['mech_candidate']['iteration']==proof['iterations'] and metadata['mech_solution']['history']['same_NEW_eL_source_and_original53_reference'] is True
  rhs=c['same_NEW_eL_current_cycle_RHS'];scale=c['same_NEW_eL_original_scale'];norms=c['selectors']['source_norms'];zero=c['selectors']['zero_source']
  assert rhs==member('mech_additional_context',('rhs_hi','rhs_lo'),(403340,)) and scale==member('mech_additional_context',('original_scale',),(403340,))
  assert norms==member('mech_warm_reference',('norms',),(3,2)) and zero==member('mech_warm_reference',('zero_source_both_words',),(3,),'bool')
  assert c['selectors']['lambda_mechanical']==member('mech_solution',('lambda_hi','lambda_lo'),(403340,)) and c['selectors']['residual']==member('mech_solution',('residual_hi','residual_lo'),(403340,)) and c['selectors']['scores']==member('mech_solution',('scores',),(3,2))
  expected_arguments=[dict(name='mechanical_lambda_argument',left=c['selectors']['lambda_mechanical'],right=member('mech_candidate',('lambda_hi','lambda_lo'),(403340,)),verified=False),dict(name='same_NEW_eL_source_norms',left=norms,right=member('mech_additional_context',('source_norms',),(3,2)),verified=False),dict(name='same_NEW_eL_zero_source',left=zero,right=member('mech_additional_context',('zero_source_both_words',),(3,),'bool'),verified=False)]
  assert c['argument_word_links']==expected_arguments
  links=[('mechanical_adjoint_eL_rhs_to_89302',rhs,member('warm_rhs',('rhs_hi','rhs_lo'),(403340,)),10),('mechanical_adjoint_eL_rhs_to_fresh220',rhs,member('literal220_weak_bridge',('NEW_literal_stationarity_eL_packed_hi','NEW_literal_stationarity_eL_packed_lo'),(403340,)),10)]
  links.extend((q['name'],q['left'],q['right'],11 if q['name']=='mechanical_lambda_argument' else None) for q in c['argument_word_links'])
  links.extend([('original53_norms_to_89302',norms,member('warm_measured',('new_source_norms',),(3,2)),None),('original53_zero_flags_to_89302',zero,member('warm_measured',('new_source_exact_both_word_zero',),(3,),'bool'),None),('original_scale_to_89302',scale,member('warm_rhs',('original_scale',),(403340,)),None),('original_scale_to_fresh220',scale,member('literal220_weak_bridge',('NEW_literal_original_scale_packed',),(403340,)),None),('total_lambda_source_scores',c['selectors']['scores'],member('mech_candidate',('scores',),(3,2)),None)])
  for name,left,right,family in links:compare(name,left,right,records,terminals,family)
  CONTEXT.clear();CONTEXT.update(stage='original53_source_zero_norm_and_saved_certificate_predicates')
  R=endpoint(rhs,records,terminals);N=endpoint(norms,records,terminals)[0];Z=endpoint(zero,records,terminals)[0];S=endpoint(scale,records,terminals)[0];E=endpoint(c['selectors']['residual'],records,terminals);scores=endpoint(c['selectors']['scores'],records,terminals)[0]
  assert N.shape==scores.shape==(3,2) and Z.shape==(3,) and np.all(S>0) and np.all(N>=0) and np.all(scores>=0) and np.all(scores<=1e-10)
  assert np.array_equal(scores.view(np.uint64),np.asarray(proof['source_relative_scores'],dtype=np.float64).view(np.uint64))
  groups=(('native',slice(0,380292)),('metric',slice(380292,None)),('packed',slice(None)));checks=[]
  for row,(name,selection) in enumerate(groups):
   source_zero=bool(all(np.all(a[selection]==0) for a in R));residual_zero=bool(all(np.all(a[selection]==0) for a in E));assert bool(Z[row])==source_zero
   assert bool(np.all(N[row]==0)) if source_zero else bool(np.all(N[row]>0))
   if source_zero:assert residual_zero and np.all(scores[row]==0)
   checks.append(dict(group=name,source_both_words_zero=source_zero,residual_both_words_zero=residual_zero,source_norms=N[row].tolist(),saved_scores=scores[row].tolist(),norms_recomputed=False))
  predicate=dict(status='ORIGINAL53_SAVED_SOURCE_CERTIFICATE_PREDICATES_PASS',group_order=['native','metric','packed'],versions=['raw','coordinate_scaled'],native_slice=[0,380292],metric_slice=[380292,403340],positive_original_scale=True,threshold=1e-10,checks=checks,norm_arithmetic_replayed=False,operator_evaluated=False,physical_adoption=False);seal(STEM+'_SOURCE_CERTIFICATE.json',predicate)
  assert len(DONE)==10 and all(q['all_exact'] for q in DONE) and {q['family'] for q in DONE if q['family'] is not None}=={10,11}
  for n,s in STATS.items():assert snapshot(Path(n))==s,n
  result=dict(status='CLOSED_MECHANICAL_SOURCE_WORD_LINK_PREFLIGHT_PASS',observed_utc=datetime.now(timezone.utc).isoformat(),selected_assembly=list(SELECTED),mechanical_selectors=list(MECHANICAL),inherited_preflight_results=[list(PRIOR82),list(PRIOR88)],inherited_closed_links_checked=88,first88_word_ties_recomputed=False,new_mechanical_families=list(FAMILIES),new_exact_comparisons=len(DONE),links=DONE,combined_declared_word_families_checked=90,combined_declared_word_families_all_exact=True,source_certificate=predicate,actual_mechanical_terminal=t,inherited_warm_measured_only=True,source_sign='target minus literal current; epsilon minus (literal minus registered)',all90_runtime_links_admitted=False,all13group_runtime_map_admitted=False,operator_actions_or_norms_replayed=False,uniform_adjoint_or_original147_association_qualified=False,physical_adoption=False,verified_sha256=VERIFIED,stable_stats=STATS,scope='Two final mechanical source/lambda families and explicit same-NEW-eL reference word predicates only. Completed88 result inherited by exact hashes; no physical feedback or coupled runtime admission.')
  h=seal(STEM+'_RESULT.json',result);print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,inherited=88,new_families=2,new_word_comparisons=10,all_exact=True,physical_adoption=False)))
 except BaseException:
  seal(STEM+'_ERROR.json',dict(status='FAILED_MECHANICAL_WORD_LINK_PREFIX_PRESERVED',context=CONTEXT,completed_new_links=DONE,inherited_preflight_result=list(PRIOR88),first88_word_ties_recomputed=False,traceback=traceback.format_exc(),verified_sha256=VERIFIED,stable_stats=STATS,physical_adoption=False));raise
if __name__=='__main__':main()
