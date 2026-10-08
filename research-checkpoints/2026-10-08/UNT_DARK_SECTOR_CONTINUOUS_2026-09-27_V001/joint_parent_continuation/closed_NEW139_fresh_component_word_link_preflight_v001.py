"""HELD selected-word NEW139 Cg/config preflight; root alone releases."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,traceback
B=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
COMPONENT=None
STEM='ROOT_CLOSED_NEW139_FRESH_COMPONENT_WORD_LINK_PREFLIGHT_V001'
PROTOCOL='CLOSED_NEW139_FRESH_COMPONENT_WORD_LINK_PREFLIGHT_V001.md'
PROTOCOL_SHA='23c3379b3b35123afd257a85c065f968501721292763acfc4edbd7cb4b276a31'
PARENT_SOURCE=('closed_coupled_mechanical_word_link_preflight_v002.py','ccb3d1a665a432520f34d43d84481d1a4e54c60ef073d603eff9e8aca9a14696')
RECIPE=('NATIVE_HELD_COUPLED13_FINAL_ADMISSION_AND_FRESH_COMPONENT_LINK_RECIPE_V001.json','58d3b692318ae11b1d33e4da99d118029370b5636177321e295bba0c828b7dd8')
CLOSED9=('NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_V003.json','7bceaa8396fed1f7635ddcaac194e3939f8fb21aef229d079f75e6b83e516f70')
CG_SELECTORS=('ROOT_ACTUAL_CLOSED_NEW139_MECHANICAL_GAUGE_SELECTORS_V001.json','5649a0e17718be135a21ef9c3be08882a413ee0b6c6373432130cbae22a675d5')
CONFIGURATION_SELECTORS=(None,None)
PRIOR_CG_PROOF=(None,None,None)
PRIOR90=('ROOT_CLOSED_COUPLED_MECHANICAL_WORD_LINK_PREFLIGHT_V001_RESULT.json','8cf0ea08adec78c014e173fb616bb3e3dce567f0b8f90c36ac77f42a199dcdb6')
SHEET13=('ROOT_CLOSED_COUPLED_FIXED_SHEET_MASK_WEIGHT_PREFLIGHT_V003_RESULT.json','6d9a6d24ca6a1cc2ac59087609d0a9446ae4b709af09f1ca9c23cb077acf5196')
ORIGINAL606=('ROOT_CLOSED9_SELECTED_BYTE_CUSTODY_RESIDENT_PREFIX_V002.json','377b60d18017059f4a5d7dd75ae6513ca4cac4ddadbc40c241403621031caba3')
RV_SELECTORS=('ROOT_ACTUAL_CLOSED_NEW139_NORMAL_RESPONSE_SELECTORS_V001.json','57330c46ceb54161e51b6d50e75b6edf8582dd163de758735ea88721541c58e2')
CG_PROOF=('READONLY_PERSISTENCE_COMPLETE_NEW139_MECHANICAL_GAUGE_SUCCESS_SEALS_V001.json','209cbfa3bae3abe0df8ce29ab4e2dafdc45e5fa55c46c7d1a0875bc2839a9823')
SOURCE_PINS={'gauge':('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py','e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222'),'configuration':('cross_u_NEW139_configuration_three_unit_preparation_v006.py','6789a603ca989f27ac97f0e91f69902b29d6e4899012931d9ccbe89de451dfbe')}
VERIFIED={};STATS={};TERMINALS={};DONE=[];CONTEXT={};LEASES={};np=None


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
 if name=='mechanical_gauge64':
  assert tuple(source)==SOURCE_PINS['gauge'] and tuple(proof[:2])==CG_PROOF and proof[2]==pr['status']=='READONLY_PERSISTENCE_COMPLETE_NEW139_COMPONENT_SUCCESS_SEALS_VERIFIED'
  assert pr['owner']['pid']==89675 and pr['kind']=='gauge' and pr['outcome']=='SUCCESS'
  assert pr['exit_code'] is None and pr['naturally_closed'] is False and pr['producer_exit_observed'] is pr['post_receipt_recheck_observed'] is False
  assert pr['persistence_complete'] is pr['process_absent'] is pr['session_retired'] is pr['all_input_seals_verified'] is pr['all_output_seals_verified'] is pr['all_success_role_seals_verified'] is pr['planned_role_and_control_census_complete'] is True
  c=pr['observed_closure'];assert c['pid']==89675 and c['session_id']==42171 and c['exit_code'] is None and c['naturally_closed'] is False and c['persistence_complete'] is c['process_absent'] is c['session_retired'] is True and c['producer_exit_observed'] is c['post_receipt_recheck_observed'] is False
  assert all(isinstance(c[n],str) and c[n] for n in ('observed_utc','process_absent_evidence','session_retired_evidence'))
  assert pr['input_count']==len(rc['input_sha256'])==109 and pr['output_count']==len(rc['output_sha256'])==151 and pr['success_roles']==pr['planned_roles']==len(pr['records'])==74 and pr['failed_roles']==0 and pr['actual_control_count']==pr['planned_controls']==len(pr['controls'])==44
 else:
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
 if '$copy_finite_h_spatial' in e:
  assert set(e)=={'$copy_finite_h_spatial'};leaf=e['$copy_finite_h_spatial'];name=leaf['$record']
  assert name in ('finite_rate_state_input0','finite_rate_state_input1','finite_rate_state_input2','finite_rate_state_input3') and leaf==member(name,('completed_RATE_STATE_INPUT_h_first_hi','completed_RATE_STATE_INPUT_h_first_lo'),(3784,4,3,3))
  ref,md=record(records[name],terminals);iq=int(name[-1]);assert records[name]['terminal']=='finite139' and md['owner']['pid']==65759 and md['owner']['source_sha256']=='59f23b9476d38aadc8297c104d4cf8e5ab217ac1ce3a0bc077e34f2fec99b39f' and md['column']==iq and ref['file'].endswith('_%05d_RATE_STATE_INPUT.npz'%(3+22*iq))
  return [a[:,1:3].copy() for a in endpoint(leaf,records,terminals)]
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

def inherit_leases(rows,hashes=None):
 for item in rows:
  name,h,expected=item['file'],item['sha256'],item['stable_stats'];p=B/name;key=str(p.resolve());now=snapshot(p)
  assert not now['dataless'] and all(now[n]==expected[n] for n in ('inode','size','mtime_ns','mode')) and now['mode']=='0o444',name
  if hashes is not None:assert hashes[key]==h
  if key in VERIFIED:assert VERIFIED[key]==h and STATS[key]==now
  else:VERIFIED[key]=h;STATS[key]=now;LEASES[key]=dict(sha256=h,stable_stats=expected)

def finite_refs(closed9,iq):
 return {r:closed9['records'][n+str(iq)]['reference'] for r,n in (('BASELINE_COLUMN_INPUT','finite_baseline_column_input'),('RATE_STATE_INPUT','finite_rate_state_input'),('RATE_STATE_FIRST_JETS','finite_rate_state_first_jets'),('RATE_STATE_FEATURES','finite_rate_state_features'),('RATE_STATE_MOMENTA','finite_rate_state_momenta'),('RATE_STATE_COLUMN','finite_rate_state_column'))}

def Rv_metadata_routes(closed9):
 packet=json.loads(bind(*RV_SELECTORS).read_bytes());c=packet['component'];assert len(c['columns'])==4 and len(c['descriptors'])==len(c['chunks'])==120 and c['data_word_equalities_verified'] is False
 rows=[]
 for iq,col in enumerate(c['columns']):
  prov=col['same_candidate_provenance'];assert prov['fresh_stages']==finite_refs(closed9,iq) and prov['finite_terminal']==closed9['terminals']['finite139'] and prov['point_TOTAL_time_words']==prov['fresh_stages']['RATE_STATE_INPUT'] and prov['nodal_TOTAL_equivalence_earned'] is False
  for serial in range(30*iq,30*(iq+1)):assert c['descriptors'][serial]['same_candidate_provenance']==c['chunks'][str(serial)]['same_candidate_provenance']==prov
  rows.append(dict(column=iq,same_candidate_provenance=prov,exact_six_finite_stage_refs=True,all30chunk_provenances_same=True,Rv_arrays_recompared=False))
 return rows

def prepare_links(packet,closed9,recipe,group):
 component=packet['component'];t=packet['actual_terminal'];assert tuple(t[0])==SOURCE_PINS[group] and t[2][2]=='CLOSED' and component['not_runtime_selected_map'] is True and component['data_word_equalities_verified'] is component['physical_adoption'] is False
 key='mechanical_gauge64' if group=='gauge' else 'configuration_three_chi';terminals={**closed9['terminals'],key:t};records={**closed9['records'],**component['records']};rc,pr=terminal(key,t);assert len(component['columns'])==4
 links=json.loads(json.dumps(recipe['Cg_new_word_links' if group=='gauge' else 'configuration_existing_overlay_word_links']))
 for iq,col in enumerate(component['columns']):
  assert col['column']==iq if group=='gauge' else col['same_candidate_provenance']['NEW139_point_TOTAL_input']
  target=pr['case']['prepared_inputs'][iq] if group=='gauge' else col['configuration_cache'];hits=[n for n,q in component['records'].items() if q['reference']==target];assert len(hits)==1;name=hits[0]
  _,md=record(records[name],terminals);assert md['column']==iq and md['source_records']==finite_refs(closed9,iq)
  if group=='gauge':
   assert md['kind']=='NEW139_MECHANICAL_GAUGE_INPUT' and md['point_TOTAL_not_nodal_TOTAL'] is True and md['same_candidate_provenance']['finite_closure']==closed9['terminals']['finite139'] and col['source_records']==md['source_records']
   _,cm=record(next(q for q in component['records'].values() if q['reference']==col['fresh_mechanical_record']),terminals);assert cm['input']==target and cm['source_records']==md['source_records'] and len(cm['tests'])==16
  else:assert md['role']=='NEW139_CONFIGURATION_CACHE' and md['fresh_mechanical_input']==col['same_candidate_provenance']['NEW139_point_TOTAL_input']
  for link in links:
   if link['column']==iq:link['right']['$record']=name
 assert len(links)==28 and len({q['name'] for q in links})==28
 return links,records,terminals

def main():
 global np
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and COMPONENT in ('gauge','configuration') and not list(B.glob(STEM+'_*'))
 import numpy as np
 try:
  bind(Path(__file__).name,hashlib.sha256(Path(__file__).read_bytes()).hexdigest());bind(PROTOCOL,PROTOCOL_SHA);bind(*PARENT_SOURCE)
  recipe=json.loads(bind(*RECIPE).read_bytes());closed9=json.loads(bind(*CLOSED9).read_bytes());old90=json.loads(bind(*PRIOR90).read_bytes());sheet=json.loads(bind(*SHEET13).read_bytes());leases=json.loads(bind(*ORIGINAL606).read_bytes())
  assert recipe['AUTHOR_DRAFT'] is True and all(q['value'] is None for q in recipe['six_final_predicates'].values())
  assert old90['combined_declared_word_families_checked']==90 and old90['combined_declared_word_families_all_exact'] is True and old90['operator_actions_or_norms_replayed'] is old90['all13group_runtime_map_admitted'] is False
  assert len(sheet['predicates'])==13 and all(q['passed'] is True for q in sheet['predicates']) and sheet['registered_sheet_once'] is True and sheet['prior90_word_links_replayed'] is False
  assert leases['all_selected_original_bytes_verified'] is True and leases['selected_unique_file_count']==leases['verified_resident_file_count']==len(leases['verified'])==606 and leases['pending_dataless']==[];inherit_leases(leases['verified'])
  cgproof=json.loads(bind(*CG_PROOF).read_bytes());inherit_leases([dict(file=n,sha256=cgproof['verified_sha256'][n],stable_stats=s) for n,s in cgproof['stable_stats'].items()],cgproof['verified_sha256'])
  rv=Rv_metadata_routes(closed9);prior=None
  if COMPONENT=='gauge':packet=json.loads(bind(*CG_SELECTORS).read_bytes())
  else:
   assert all(q is not None for q in CONFIGURATION_SELECTORS+PRIOR_CG_PROOF);prior=json.loads(bind(*PRIOR_CG_PROOF[:2]).read_bytes());assert prior['status']==PRIOR_CG_PROOF[2]=='CLOSED_NEW139_GAUGE28_SOURCE_WORD_LINKS_PASS' and prior['component']=='gauge' and prior['checked_links_all_exact'] is True and prior['new_comparisons']==len(prior['links'])==28 and prior['Cg_selectors']==list(CG_SELECTORS) and prior['recipe']==list(RECIPE)
   inherit_leases([dict(file=n,sha256=prior['verified_sha256'][n],stable_stats=s) for n,s in prior['stable_stats'].items()],prior['verified_sha256']);packet=json.loads(bind(*CONFIGURATION_SELECTORS).read_bytes())
  links,records,terminals=prepare_links(packet,closed9,recipe,COMPONENT)
  for row in links:compare(row['name'],row['left'],row['right'],records,terminals,row['family'])
  assert len(DONE)==28 and all(q['all_exact'] for q in DONE)
  for n,s in STATS.items():assert snapshot(Path(n))==s,n
  result=dict(status='CLOSED_NEW139_'+('GAUGE28' if COMPONENT=='gauge' else 'CONFIGURATION28')+'_SOURCE_WORD_LINKS_PASS',component=COMPONENT,observed_utc=datetime.now(timezone.utc).isoformat(),recipe=list(RECIPE),Cg_selectors=list(CG_SELECTORS),configuration_selectors=list(CONFIGURATION_SELECTORS),prior_Cg28_result=list(PRIOR_CG_PROOF) if prior else None,inherited_Cg28_comparisons=28 if prior else 0,Cg28_word_ties_replayed=False,prior90=list(PRIOR90),sheet13=list(SHEET13),original606=list(ORIGINAL606),old90_or_sheet13_word_tests_replayed=False,new_comparisons=28,links=DONE,checked_links_all_exact=True,Rv_six_ref_metadata_routes=rv,Cg_exit_observed=False,Cg_post_receipt_recheck_observed=False,Cg_naturally_closed=False,Cg_persistence_complete=True,operator_actions_units_controls_or_norms_evaluated=False,all13group_runtime_map_admitted=False,final_six_map_predicates_promoted=False,phase95_operand_transfer_admitted=False,physical_adoption=False,source_unsigned_and_wholeweak_qualifications_external=True,verified_sha256=VERIFIED,stable_stats=STATS,inherited_byte_leases=LEASES)
  h=seal(STEM+'_RESULT.json',result);print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,component=COMPONENT,checked=28,all_exact=True)))
 except BaseException:
  seal(STEM+'_ERROR.json',dict(status='FAILED_NEW139_COMPONENT_WORD_LINK_PREFIX_PRESERVED',component=COMPONENT,context=CONTEXT,completed_links=DONE,traceback=traceback.format_exc(),recipe=list(RECIPE),prior90=list(PRIOR90),sheet13=list(SHEET13),old_word_or_operator_replay=False,verified_sha256=VERIFIED,stable_stats=STATS,physical_adoption=False));raise
if __name__=='__main__':main()
