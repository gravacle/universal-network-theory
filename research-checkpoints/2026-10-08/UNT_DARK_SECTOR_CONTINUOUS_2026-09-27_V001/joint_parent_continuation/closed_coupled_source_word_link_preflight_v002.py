"""HELD root read-only completion of six deferred closed phase word links; no82-link replay."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,traceback,zipfile
import numpy as np
B=Path(__file__).resolve().parent
SELECTED=('NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_V003.json','7bceaa8396fed1f7635ddcaac194e3939f8fb21aef229d079f75e6b83e516f70')
STEM='ROOT_CLOSED_COUPLED_DEFERRED_PHASE_WORD_LINK_PREFLIGHT_V002'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
ROOT_PHASE_INPUT_RELEASE=None
PARENT_SOURCE=('closed_coupled_source_word_link_preflight_v001.py','7daf23d11fcdfd5d06faed1f2d07a24bc84a871b7acdd3ed458f0c3c9d022bbc')
PARENT_RESULT=('ROOT_CLOSED_COUPLED_SOURCE_WORD_LINK_PREFLIGHT_V001_RESULT.json','bbba9cb1960c35709ea41fa939a5473e2bb851806342ada1ad3ea93c217b65bd','CLOSED_SOURCE_WORD_LINK_PREFLIGHT_MEASURED')
PROTOCOL='CLOSED_COUPLED_DEFERRED_PHASE_WORD_LINK_PREFLIGHT_V002.md'
PROTOCOL_SHA=None
PHASE_LINKS=((5,'current_H'),(6,'current_p'),(9,'literal_phase_target'),(14,'original_phase_scale'),(15,'phase_adjoint_eL_rhs'),(17,'phase_lambda_argument'))
FUTURE_LINKS=((10,'mechanical_adjoint_eL_rhs'),(11,'mechanical_lambda_argument'))
VERIFIED={};STATS={};TERMINALS={};DONE=[];DEFERRED=[]
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
 with np.load(B/ref['file'],allow_pickle=False) as z:
  assert json.loads(str(z['metadata_json']))==md
  for key in e['$keys']:
   a=z[key];assert str(a.dtype)==e['$dtype']=='float64' and list(a.shape)==e['$shape'] and np.all(np.isfinite(a)),key
   schema=md['schema'][key];assert schema==dict(shape=list(a.shape),dtype='float64',finite=True)
   arrays.append(a)
 return arrays

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and ROOT_PHASE_INPUT_RELEASE is not None and PROTOCOL_SHA is not None
 assert not list(B.glob(STEM+'_*'));bind(Path(__file__).name,hashlib.sha256(Path(__file__).read_bytes()).hexdigest());bind(PROTOCOL,PROTOCOL_SHA);bind(*PARENT_SOURCE)
 prior=json.loads(bind(*PARENT_RESULT[:2]).read_bytes());v=json.loads(bind(*SELECTED).read_bytes());assert v['physical_adoption'] is False
 assert prior['status']==PARENT_RESULT[2] and prior['selected_assembly']==list(SELECTED) and prior['closed_links_checked']==82 and prior['checked_links_all_exact'] is True
 assert len(prior['links'])==82 and all(q['all_exact'] is True and all(q['exact_uint64_word_ties']) and q['mismatches']==[] for q in prior['links'])
 assert prior['all90_runtime_links_admitted'] is prior['all_four_fresh_component_ties_admitted'] is prior['original_numerical_actions_or_controls_replayed'] is prior['physical_adoption'] is False
 assert len(v['word_links'])==90 and {(q['ordinal'],q['name']) for q in prior['deferred'] if q['reason']=='closed_original_archive_dataless_no_payload_read'}==set(PHASE_LINKS)
 assert {(q['ordinal'],q['name']) for q in prior['deferred'] if q['reason']=='endpoint_unstarted_or_future'}==set(FUTURE_LINKS) and len(prior['deferred'])==8
 assert {q['ordinal'] for q in prior['links']}==set(range(90))-{i for i,n in PHASE_LINKS+FUTURE_LINKS}
 phase_records={}
 for i,name in PHASE_LINKS:
  w=v['word_links'][i];assert w['name']==name
  for side in ('left','right'):
   e=w[side];wrap=v['records'][e['$record']];assert wrap['terminal'] in ('updated_phase_mass','phase_adjoint') and wrap['scientific_owner']['pid'] in (19724,37373)
   phase_records[e['$record']]=wrap
 assert len(phase_records)==5
 expected={q['reference']['file']:q['reference']['sha256'] for q in phase_records.values()};release=ROOT_PHASE_INPUT_RELEASE
 assert release['original_archive_sha256']==expected and release['original_owners_absent']==[19724,37373]
 assert release['prior_natural_closure']==dict(session=52154,exit_code=0,source_sha256=PARENT_SOURCE[1],result_sha256=PARENT_RESULT[1])
 for wrap in phase_records.values():
  ref=wrap['reference'];assert not snapshot(B/ref['file'])['dataless'] and not snapshot(B/ref['commit_file'])['dataless'];record(wrap,v['terminals'])
 context={}
 try:
  for i,name in PHASE_LINKS:
   w=v['word_links'][i];context=dict(ordinal=i,name=name,left=w['left'],right=w['right'])
   endpoints=[w.get(n) for n in ('left','right')]
   (left, right) = [endpoint(e, v['records'], v['terminals']) for e in endpoints]
   assert len(left) == len(right)
   words = []
   mismatches = []
   for (j, (a, b)) in enumerate(zip(left, right)):
       assert a.shape == b.shape and a.dtype == b.dtype
       equal = np.equal(a.view(np.uint64), b.view(np.uint64))
       words.append(bool(np.all(equal)))
       if not words[-1]:
           flat = np.flatnonzero(~equal.ravel())
           k = int(flat[0])
           av = a.ravel()[k]
           bv = b.ravel()[k]
           mismatches.append(dict(word=j, count=int(flat.size), first_flat_index=k, left_hex=hex(int(a.view(np.uint64).ravel()[k])), right_hex=hex(int(b.view(np.uint64).ravel()[k])), left=float(av), right=float(bv)))
   row = dict(ordinal=i, name=w['name'], left=w['left'], right=w['right'], exact_uint64_word_ties=words, all_exact=all(words), mismatches=mismatches)
   DONE.append(row)
   seal(STEM + '_%03d_WORD_LINK.json' % i, row)
  for n,s in STATS.items():assert snapshot(Path(n))==s,n
  assert len(DONE)==6 and [(q['ordinal'],q['name']) for q in DONE]==list(PHASE_LINKS)
  remaining=[q for q in prior['deferred'] if (q['ordinal'],q['name']) in FUTURE_LINKS]
  result=dict(status='CLOSED_DEFERRED_PHASE_SOURCE_WORD_LINK_PREFLIGHT_MEASURED',observed_utc=datetime.now(timezone.utc).isoformat(),selected_assembly=list(SELECTED),parent_source=list(PARENT_SOURCE),inherited_preflight_result=list(PARENT_RESULT),inherited_closed_links_checked=82,inherited_checked_links_all_exact=True,inherited_link_outputs=[dict(file=PARENT_SOURCE[0].replace('closed_coupled_source_word_link_preflight_v001.py','ROOT_CLOSED_COUPLED_SOURCE_WORD_LINK_PREFLIGHT_V001')+'_%03d_WORD_LINK.json'%q['ordinal'],ordinal=q['ordinal'],name=q['name']) for q in prior['links']],first82_word_ties_recomputed=False,new_closed_phase_links_checked=6,new_phase_links_all_exact=all(q['all_exact'] for q in DONE),links=DONE,combined_closed_links_checked=88,combined_checked_links_all_exact=prior['checked_links_all_exact'] and all(q['all_exact'] for q in DONE),deferred=remaining,all90_runtime_links_admitted=False,all_four_fresh_component_ties_admitted=False,original_numerical_actions_or_controls_replayed=False,numeric_payloads_selected_only=True,physical_adoption=False,qualification_scope='Only six previously deferred closed phase word ties; prior82 result inherited verbatim by source/hash and never recomputed. Future mechanical ties and physical feedback remain unadmitted.',phase_input_release=release,verified_sha256=VERIFIED,stable_stats=STATS)
  h=seal(STEM+'_RESULT.json',result);print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,new_phase_checked=6,inherited_checked=82,all_closed_exact=result['combined_checked_links_all_exact'],future_deferred=len(remaining))))
 except BaseException:
  seal(STEM+'_ERROR.json',dict(status='FAILED_DEFERRED_PHASE_WORD_LINK_PREFIX_PRESERVED',context=context,completed_new_links=DONE,inherited_preflight_result=list(PARENT_RESULT),first82_word_ties_recomputed=False,traceback=traceback.format_exc(),verified_sha256=VERIFIED,stable_stats=STATS,physical_adoption=False));raise
if __name__=='__main__':main()
