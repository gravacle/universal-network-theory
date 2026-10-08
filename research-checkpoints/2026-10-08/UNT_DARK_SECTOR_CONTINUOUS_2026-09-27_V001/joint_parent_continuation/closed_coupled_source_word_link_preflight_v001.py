"""Root read-only preflight of closed88 selector word links; no physical admission."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,zipfile
import numpy as np
B=Path(__file__).resolve().parent
SELECTED=('NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_V003.json','7bceaa8396fed1f7635ddcaac194e3939f8fb21aef229d079f75e6b83e516f70')
STEM='ROOT_CLOSED_COUPLED_SOURCE_WORD_LINK_PREFLIGHT_V001'
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
 assert not list(B.glob(STEM+'_*'));v=json.loads(bind(*SELECTED).read_bytes());assert v['physical_adoption'] is False
 for i,w in enumerate(v['word_links']):
  endpoints=[w.get(n) for n in ('left','right')]
  reason=None
  if not all(isinstance(e,dict) and isinstance(v['records'].get(e.get('$record')),dict) and isinstance(v['records'][e['$record']].get('reference'),dict) for e in endpoints):reason='endpoint_unstarted_or_future'
  elif any(snapshot(B/v['records'][e['$record']]['reference']['file'])['dataless'] for e in endpoints):reason='closed_original_archive_dataless_no_payload_read'
  if reason:DEFERRED.append(dict(ordinal=i,name=w['name'],reason=reason));continue
  left,right=[endpoint(e,v['records'],v['terminals']) for e in endpoints]
  assert len(left)==len(right)
  words=[];mismatches=[]
  for j,(a,b) in enumerate(zip(left,right)):
   assert a.shape==b.shape and a.dtype==b.dtype
   equal=np.equal(a.view(np.uint64),b.view(np.uint64));words.append(bool(np.all(equal)))
   if not words[-1]:
    flat=np.flatnonzero(~equal.ravel());k=int(flat[0]);av=a.ravel()[k];bv=b.ravel()[k]
    mismatches.append(dict(word=j,count=int(flat.size),first_flat_index=k,left_hex=hex(int(a.view(np.uint64).ravel()[k])),right_hex=hex(int(b.view(np.uint64).ravel()[k])),left=float(av),right=float(bv)))
  row=dict(ordinal=i,name=w['name'],left=w['left'],right=w['right'],exact_uint64_word_ties=words,all_exact=all(words),mismatches=mismatches)
  DONE.append(row);seal(STEM+'_%03d_WORD_LINK.json'%i,row)
 for n,s in STATS.items():assert snapshot(Path(n))==s,n
 result=dict(status='CLOSED_SOURCE_WORD_LINK_PREFLIGHT_MEASURED',observed_utc=datetime.now(timezone.utc).isoformat(),selected_assembly=list(SELECTED),closed_links_checked=len(DONE),checked_links_all_exact=all(q['all_exact'] for q in DONE),links= DONE,deferred=DEFERRED,all90_runtime_links_admitted=False,all_four_fresh_component_ties_admitted=False,original_numerical_actions_or_controls_replayed=False,numeric_payloads_selected_only=True,physical_adoption=False,qualification_scope='saved closed selected byte words only; no changed-state transfer or physical/source inverse admission',verified_sha256=VERIFIED,stable_stats=STATS)
 h=seal(STEM+'_RESULT.json',result);print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,checked=len(DONE),all_exact=result['checked_links_all_exact'],deferred=len(DEFERRED))))
if __name__=='__main__':main()
