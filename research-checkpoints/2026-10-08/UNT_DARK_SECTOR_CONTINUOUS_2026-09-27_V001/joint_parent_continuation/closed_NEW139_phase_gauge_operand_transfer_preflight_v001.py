"""HELD exact saved-word phase-only transfer; root alone binds/runs this preflight."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,traceback
B=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='ROOT_CLOSED_NEW139_PHASE_GAUGE_OPERAND_TRANSFER_PREFLIGHT_V001'
PROTOCOL='CLOSED_NEW139_PHASE_GAUGE_OPERAND_TRANSFER_PREFLIGHT_V001.md'
PROTOCOL_SHA='b2d0316b1a7e165a1a90f8cb68b6bfc969a7f95376e5106a01131f0fbf9e929d'
TERMINAL_PINS={n:(None,None,None,None) for n in ('phase_gauge','updated_phase','finite139','mechanical_gauge')}
OLD30=('ROOT_CLOSED_GAUGE35734_PARTIAL_SUCCESS_BYTE_SEALS_V001.json','66eb1d867f22fa09ab51ee0b3e5690a3a77d7ba398a9af6d7369d3cc7fd87961')
SOURCE_PINS={'author_fragment_candidate_gauge_registered_current_contact_v001.py': 'ac0502f41c6ad04208f5ef5610d43b3e11064a4b66eb73d076d43c959ffb0cdd', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'cross_u_candidate_gauge_registered_current_controls_v002.py': 'e908868e63f2c2981b01a68bc1fdfd0fe063885ff6e4ed02b7f91d0eb7b5564c', 'saved_gauge35734_arithmetic_tail_recovery_v005.py': '6dcb4ac53f9597a848f1c2b7c26caf383ff63542dde4f229a882d83815b60d2a', 'cross_u_NEW139_mechanical_gauge_current_preparation_v005.py': 'e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222', 'author_fragment_NEW139_mechanical_gauge_preparation_v003.py': '244a0d50f89b72dbc2447eba66939ddcd5cd6a2b94483bb7595c0a1e41249dc7', 'cross_u_fixed_geometry_total_rate_state_evaluation_v004.py': '59f23b9476d38aadc8297c104d4cf8e5ab217ac1ce3a0bc077e34f2fec99b39f', 'author_fragment_candidate_gauge_fullweak_transpose_v003.py': 'a35bb8085710aff9ec5a88e44fe146cd6fe3fc700db485b44ab5aecea4ce35d7'}
RAW_S=('g','hi','U','uc','P')
RAW_C=('h','ih','N','beta','u','up','gamma','sqrt_h')
PAIRED_RAW={'hi':('s','hi'),'P':('s','P'),'U':('s','U'),'uc':('s','uc'),'N':('c','N'),'mu':('c','sqrt_h'),'ih':('c','ih'),'u':('c','u')}
DP_EOS_OPERANDS=('raised','X','q','X0','s','d','PX','PX_dimensionless','epnorm','clock','r','hi_r','density','J')
VERIFIED={};STATS={};TERMINALS={};RECORDS={};DONE=[];CONTEXT={};np=None
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
def thin(q):
 return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def terminal(name):
 if name in TERMINALS:return TERMINALS[name]
 t=TERMINAL_PINS[name];assert all(isinstance(q,(tuple,list)) and all(x is not None for x in q) for q in t),name
 source,result,receipt,proof=t
 for q in t:bind(*q[:2])
 assert (B/result[0]).stat().st_size<=128*1024*1024,'Larger RESULT requires separately reviewed bounded admission'
 r=json.loads((B/result[0]).read_bytes());rc=json.loads((B/receipt[0]).read_bytes());pr=json.loads((B/proof[0]).read_bytes())
 assert r['status']==result[2] and rc['status']==receipt[2]=='CLOSED' and pr['status']==proof[2]
 assert rc['result_sha256']==pr['result_sha256']==result[1] and rc['error_sha256'] is None
 assert pr['source_sha256']==source[1] and pr['receipt_sha256']==receipt[1] and r['owner']==rc['owner']==pr['owner']
 assert r['owner']['source_sha256']==source[1] and pr['naturally_closed'] is True and pr['exit_code']==0
 assert pr['all_input_seals_verified'] is True and pr['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification'] and r['qualification'] and all(x is False for x in r['qualification'].values())
 TERMINALS[name]=(r,rc,pr);return r,rc,pr
def record(ref,role,route,old):
 ref=thin(ref);key=(ref['file'],ref['sha256']);CONTEXT.update(record=ref,role=role,route=route)
 if key in RECORDS:return RECORDS[key]
 assert re.fullmatch(r'.+_[0-9]{5}_'+role+r'\.npz',ref['file']) and ref['commit_file']==ref['file']+'.COMMIT.json'
 for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):bind(n,h)
 q=json.loads((B/ref['commit_file']).read_bytes());md=q['metadata'];assert q['file']==ref['file'] and q['sha256']==ref['sha256']
 assert md['failed'] is False and md['qualification'] and all(x is False for x in md['qualification'].values()) and md.get('physical_adoption',False) is False
 if 'role' in md:assert md['role']==role
 if route=='original35734':
  rows=[x for x in old['records'] if x['file']==ref['file']];assert len(rows)==1 and thin(rows[0])==ref and rows[0]['role']==role
  assert md['owner']==old['owner'] and md['owner']['pid']==35734 and md['owner']['source_sha256']==SOURCE_PINS['cross_u_candidate_gauge_registered_current_controls_v002.py']
 else:
  r,rc,pr=terminal(route)
  if route=='cg_inherited_input':raise AssertionError('Use explicit finite139 inherited route')
  if md['owner']==r['owner']:
   assert all(rc['output_sha256'].get(n)==h for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])))
   assert any(thin(x)==ref for x in r['checkpoints'])
  else:
   assert route=='finite139' and pr['all_inherited_success_role_seals_verified'] is True
   for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):
    assert pr['inherited_readonly_seal_stats'][str((B/n).resolve())]['sha256']==h
   assert any(thin(x)==ref and x['metadata']['owner']==md['owner'] for x in r['checkpoints'])
 with np.load(B/ref['file'],allow_pickle=False) as z:assert json.loads(str(z['metadata_json']))==md
 RECORDS[key]=(ref,md);return ref,md
def words(q,keys):
 ref,md=q;out=[]
 with np.load(B/ref['file'],allow_pickle=False) as z:
  assert json.loads(str(z['metadata_json']))==md
  for key in keys:
   a=z[key];assert a.dtype==np.float64 and np.all(np.isfinite(a)) and md['schema'][key]==dict(dtype='float64',shape=list(a.shape),finite=True),key
   out.append(a)
 return out
def compare(name,left,right,provenance):
 assert len(left)==len(right) and left
 equal=[];mismatches=[]
 for w,(a,b) in enumerate(zip(left,right)):
  assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
  good=np.equal(a.view(np.uint64),b.view(np.uint64));equal.append(bool(np.all(good)))
  if not equal[-1]:
   ix=np.flatnonzero(~good.ravel());k=int(ix[0]);mismatches.append(dict(word=w,count=int(ix.size),first_flat_index=k,left_hex=hex(int(a.view(np.uint64).ravel()[k])),right_hex=hex(int(b.view(np.uint64).ravel()[k]))))
 row=dict(ordinal=len(DONE),name=name,word_ties=equal,all_exact=all(equal),mismatches=mismatches,provenance=provenance)
 DONE.append(row);seal(STEM+'_%03d_WORD_LINK.json'%row['ordinal'],row);return row['all_exact']
def preflight():
 old=json.loads(bind(*OLD30).read_bytes());assert old['status']=='ROOT_CLOSED_GAUGE35734_ALL30_SUCCESS_BYTE_SEALS_VERIFIED'
 assert old['naturally_closed'] is True and old['exit_code']==1 and old['all30_committed_role_seals_verified'] is True
 assert old['original80_controls_passed_and_preserved'] is True and old['numerical_arrays_decoded'] is False and old['original_files_mutated'] is False
 gr,gc,gp=terminal('phase_gauge');ur,uc,up=terminal('updated_phase');fr,fc,fp=terminal('finite139');mr,mc,mp=terminal('mechanical_gauge')
 assert TERMINAL_PINS['phase_gauge'][0]==('saved_gauge35734_arithmetic_tail_recovery_v005.py',SOURCE_PINS['saved_gauge35734_arithmetic_tail_recovery_v005.py'])
 assert TERMINAL_PINS['mechanical_gauge'][0]==('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py',SOURCE_PINS['cross_u_NEW139_mechanical_gauge_current_preparation_v005.py'])
 g=gr['case'];u=ur['case'];f=fr['case'];m=mr['case'];assert g['status']=='CANDIDATE_GAUGE_REGISTERED_CURRENT_FORWARD_CONTACTS_MEASURED'
 assert m['status']=='NEW139_MECHANICAL_GAUGE64_POINT_COEFFICIENTS_PREPARED_UNQUALIFIED' and m['new_ports']==64 and m['new_controls']==44
 assert m['phase_coefficients_inherited_only_by_future_exact_operand_proof'] is True and m['physical_adoption'] is False
 assert m['finite_terminal']==[list(q) for q in TERMINAL_PINS['finite139']]
 assert len(g['cache_columns'])==len(g['columns'])==len(m['prepared_inputs'])==len(u['columns'])==4
 oi=record(g['input'],'INPUT','original35734',old);ci=record(m['input'],'INPUT','mechanical_gauge',old)
 fi=record(ci[1]['finite_input'],'INPUT','finite139',old)
 assert thin(fi[0])==thin(f['input']) and fi[1]['original_input']==oi[1]['original_input']
 assert fi[1]['provenance']['updated_phase_closure']==oi[1]['finite_terminal']==[list(q) for q in TERMINAL_PINS['updated_phase']]
 assert oi[1]['gauge_row_order']==['N','beta_R','beta_Z','beta_phi'] and oi[1]['gauge_jet_order']==['value','R','Z','t']
 for n in ('R','dv','hats'):
  compare('original_basis_'+n,words(oi,['copied_original_basis_'+n]),words(fi,['completed_INPUT_basis_'+n]),dict(old_input=oi[0],new_finite_input=fi[0]))
 columns=[]
 for iq in range(4):
  CONTEXT.update(column=iq);cache=record(g['cache_columns'][iq],'CACHE_COLUMN','original35734',old);fresh=record(m['prepared_inputs'][iq],'MECHANICAL_GAUGE_INPUT','mechanical_gauge',old)
  cref=record(g['columns'][iq],'COLUMN','original35734' if iq==0 else 'phase_gauge',old)
  assert cache[1]['column']==fresh[1]['column']==cref[1]['column']==iq
  assert cref[1]['cache']==cache[0] and cache[1]['updated_phase']==thin(u['columns'][iq]) and cache[1]['input']==oi[0]
  assert cache[1]['EOS_primal_or_action_replayed'] is False and fresh[1]['prepared_before_any_gauge_port'] is True and fresh[1]['point_TOTAL_not_nodal_TOTAL'] is True
  assert fresh[1]['fixed_state']==cache[1]['state'] and fresh[1]['same_candidate_provenance']['finite_closure']==[list(q) for q in TERMINAL_PINS['finite139']]
  for w in ('hi','lo'):assert cref[1]['schema']['completed_NEW_gauge_column_coefficients_phase_'+w]==dict(dtype='float64',shape=[3784,4,4],finite=True)
  start=len(DONE);oldprefix='column%d_'%iq;newprefix='completed_MECHANICAL_GAUGE_INPUT_'
  for family,names in (('s',RAW_S),('c',RAW_C)):
   for n in names:
    compare('column%d_raw_%s_%s'%(iq,family,n),words(cache,[oldprefix+'copied_STATE_completed_candidate_'+family+'_'+n]),words(fresh,[newprefix+'candidate_'+family+'_'+n]),dict(old_cache=cache[0],new_prepared=fresh[0]))
  for n,(family,rawname) in PAIRED_RAW.items():
   a=words(fresh,[newprefix+'candidate_'+family+'_'+rawname])[0]
   compare('column%d_cached_supplied_%s'%(iq,n),words(cache,[oldprefix+'cached_EOS_same_candidate_'+n+'_'+w for w in ('hi','lo')]),[a,np.zeros_like(a)],dict(old_cache=cache[0],new_prepared=fresh[0],pair_policy='exact archived raw high plus source a_dd zero low'))
  phi=words(cache,[oldprefix+'cached_EOS_same_candidate_phi_'+w for w in ('hi','lo')])
  compare('column%d_updated_phase'%iq,phi,words(fresh,[newprefix+'updated_phase_pair_'+w for w in ('hi','lo')]),dict(old_cache=cache[0],new_prepared=fresh[0],updated_phase=cache[1]['updated_phase']))
  compare('column%d_old_phase_duplicate'%iq,words(cache,[oldprefix+'phase_updated_'+w for w in ('hi','lo')]),phi,dict(old_cache=cache[0]))
  admitted=all(x['all_exact'] for x in DONE[start:]);assert len(DONE)-start==23
  columns.append(dict(column=iq,invariant_phase_record=cref[0],old_cache=cache[0],current_prepared_input=fresh[0],frozen_EOS_record=cache[1]['updated_phase'],phase_branch_operand_transfer_verified=admitted,phase_coefficients_source_rate_independent=True,mechanical_gauge_coefficients_transferred=False))
 assert len(DONE)==95
 return dict(columns=columns,checked_links_all_exact=all(x['all_exact'] for x in DONE),frozen_EOS_operands_for_literal_dp=list(DP_EOS_OPERANDS),cached_EOS_recomputed=False,unchanged_EOS_stage_transaction=TERMINAL_PINS['updated_phase'],phase_scale_target_and_adjoint_admission_remain_external=True,original_scalar_and_normal_masks_source_pinned=True,one_dv_over_R_left_weight_and_original_betaR_Rhat_registration_preserved=True)
def main():
 global np
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and not list(B.glob(STEM+'_*'))
 import numpy as np
 try:
  bind(PROTOCOL,PROTOCOL_SHA)
  for n,h in SOURCE_PINS.items():bind(n,h)
  result=preflight()
  for n,s in STATS.items():assert snapshot(Path(n))==s,n
  result.update(status='CLOSED_NEW139_PHASE_GAUGE_OPERAND_TRANSFER_VERIFIED' if result['checked_links_all_exact'] else 'CLOSED_NEW139_PHASE_GAUGE_OPERAND_TRANSFER_REFUSED',observed_utc=datetime.now(timezone.utc).isoformat(),source_pins=SOURCE_PINS,terminals=TERMINAL_PINS,original30_proof=OLD30,word_links=DONE,verified_sha256=VERIFIED,stable_stats=STATS,old_phase_gauge_actions_or_controls_replayed=False,physical_adoption=False,normal_feedback_or_stationarity_admitted=False,arbitrary_DD_coefficient_linearity_or_global_inverse_qualified=False,original_targets_scales_and_masks_modified=False)
  h=seal(STEM+'_RESULT.json',result);print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,all_exact=result['checked_links_all_exact'],comparisons=len(DONE))))
 except BaseException:
  seal(STEM+'_ERROR.json',dict(status='CLOSED_PHASE_GAUGE_PREFLIGHT_REFUSED',traceback=traceback.format_exc(),context=CONTEXT,completed_links=DONE,verified_sha256=VERIFIED,stable_stats=STATS,phase_branch_operand_transfer_verified=False,physical_adoption=False));raise
if __name__=='__main__':main()
