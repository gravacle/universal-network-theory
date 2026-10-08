"""HELD original4832 sheet/masks/weights prerequisite checks; no90-link or operator replay."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,traceback,zipfile
import numpy as np
B=Path(__file__).resolve().parent
STEM='ROOT_CLOSED_COUPLED_FIXED_SHEET_MASK_WEIGHT_PREFLIGHT_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
ROOT_EXECUTOR_RELEASE=None
PROTOCOL='CLOSED_COUPLED_FIXED_SHEET_MASK_WEIGHT_PREFLIGHT_V001.md'
PROTOCOL_SHA=None
PRIOR90=None
SELECTED=('NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_V003.json','7bceaa8396fed1f7635ddcaac194e3939f8fb21aef229d079f75e6b83e516f70')
SHEET_MAP=('NATIVE_CLOSED_ORIGINAL_SHEET_SELECTOR_SCHEMA_ADDENDUM_V001.json','1c40eca2a438acdb13c4c91a1f6998df2827e6172dcccf106153ddb06f0c7ddd')
PARENT_SOURCE=('closed_coupled_mechanical_word_link_preflight_v001.py','9132f2777c95aaeac850a2c20ac2612ab132cd2a14b059844cc3bae38d394049')
SOURCE_PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18','cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40','author_fragment_fixed_label_finite_sheet_geometry_v002.py':'556bac0713c74947b0abece865bf7e74c3d3b212029af1248aa7dd0af525a661','author_fragment_candidate_configuration_coefficient_wholeweak_v002.py':'fa55addae8e9bfe19d2f60628b5ba1776889b452902e4b3ae4ddaf893c62d122','cross_u_finite0_candidate_action_residual_v007.py':'ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58','cross_u_NEW139_coupled425955_correction_v004.py':'1bc5750730ec571c3ed9a7396058d7eb714ddefd540ef078479f4d3cc7e890ee'}
ORIGINAL_SHEET_SOURCE=('cross_u_finite0_state_normal_recovery_v005.py','8f9b528e1da5114b148585799e902cdaaa14a6ac2af60e7deff9a85375792be2')
ORIGINAL_SHEET_RECEIPT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RECEIPT.json','9e26a9c77d2ec7f023344c8399645cb94dc3252f2ab0dd744e14469050a30955')
ORIGINAL_SHEET_PROOF=('ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_V001.json','47ea566a93b34846c5861f7b184f80a73ac1ddd74f52bc891a7160b0a57fdab1','ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED')
ORIGINAL_LABEL_REFERENCE={'file':'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_00007_LOADS.npz','sha256':'4b6b6db0ccdc7b678c43150fa55d9eab5c54d09eabe6a71254e5986b4f0fa9cc','commit_file':'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_00007_LOADS.npz.COMMIT.json','commit_sha256':'f81ae230cfb2712438b52da727d7f636f05d0422ab30ee098ddc864447ebd349'}
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
def check(name,passed,evidence):
 CONTEXT.clear();CONTEXT.update(predicate=name);row=dict(name=name,passed=bool(passed),evidence=evidence)
 DONE.append(row);seal(STEM+'_%02d_PREDICATE.json'%(len(DONE)-1),row);assert row['passed'],name

def masks():
 scope={'np':np};names={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':{'native_mask','metric_mask','scalar_mask'},'cross_u_paired_current_normal_constraints_v002.py':{'normal_test_mask'}}
 for n,wanted in names.items():
  tree=ast.parse(bind(n,SOURCE_PINS[n]).read_text());defs=[a for a in tree.body if isinstance(a,ast.FunctionDef) and a.name in wanted];assert {a.name for a in defs}==wanted
  exec(compile(ast.Module(body=defs,type_ignores=[]),n,'exec'),scope)
 return np.broadcast_to(scope['native_mask'](),(33,3,87,45)),scope['metric_mask'](),scope['scalar_mask'](),scope['normal_test_mask']()

def archive(ref,owner,receipt):
 CONTEXT.clear();CONTEXT.update(record=ref)
 for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):bind(n,h);assert receipt['output_sha256'][n]==h,n
 c=json.loads((B/ref['commit_file']).read_bytes());md=c['metadata'];assert c['file']==ref['file'] and c['sha256']==ref['sha256'] and md['owner']==owner and md['failed'] is False
 assert all(x is False for x in md['qualification'].values()) and md.get('physical_adoption',False) is False
 with zipfile.ZipFile(B/ref['file']) as z:
  assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())=={k+'.npy'for k in md['schema']}|{'metadata_json.npy'}
  for k,e in md['schema'].items():
   with z.open(k+'.npy')as f:
    version=np.lib.format.read_magic(f);assert version in ((1,0),(2,0));reader=np.lib.format.read_array_header_1_0 if version==(1,0) else np.lib.format.read_array_header_2_0;shape,order,dtype=reader(f,max_header_size=10000000)
    assert list(shape)==e['shape'] and str(dtype)==e['dtype'] and not dtype.hasobject and e['finite'] is True
    assert z.getinfo(k+'.npy').file_size==f.tell()+int(np.prod(shape,dtype=object))*dtype.itemsize
 with np.load(B/ref['file'],allow_pickle=False)as z:assert json.loads(str(z['metadata_json']))==md
 return md

def member(ref,md,key,shape,dtype='float64'):
 CONTEXT.clear();CONTEXT.update(record=ref['file'],member=key)
 assert md['schema'][key]==dict(shape=list(shape),dtype=dtype,finite=True)
 with np.load(B/ref['file'],allow_pickle=False)as z:a=z[key]
 assert str(a.dtype)==dtype and list(a.shape)==list(shape) and np.all(np.isfinite(a));return a

def pair(ref,md,prefix,shape):return tuple(member(ref,md,prefix+'_'+w,shape)for w in ('hi','lo'))

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and ROOT_EXECUTOR_RELEASE is not None and PROTOCOL_SHA is not None and PRIOR90 is not None
 assert not list(B.glob(STEM+'_*'));bind(Path(__file__).name,hashlib.sha256(Path(__file__).read_bytes()).hexdigest());bind(PROTOCOL,PROTOCOL_SHA);bind(*PARENT_SOURCE)
 try:
  for n,h in SOURCE_PINS.items():bind(n,h)
  prior=json.loads(bind(*PRIOR90).read_bytes());v=json.loads(bind(*SELECTED).read_bytes());s=json.loads(bind(*SHEET_MAP).read_bytes())
  assert prior['status']=='CLOSED_MECHANICAL_SOURCE_WORD_LINK_PREFLIGHT_PASS' and prior['selected_assembly']==list(SELECTED) and prior['combined_declared_word_families_checked']==90 and prior['combined_declared_word_families_all_exact'] is True
  assert prior['first88_word_ties_recomputed'] is prior['all13group_runtime_map_admitted'] is prior['physical_adoption'] is False and len(prior['links'])==10
  assert s['closed9_unchanged_sha256']==SELECTED[1] and s['sheet_nodes']==4832 and s['sheet_radiation_count']==0 and s['physical_adoption'] is False
  for a in (ORIGINAL_SHEET_SOURCE,ORIGINAL_SHEET_RECEIPT,ORIGINAL_SHEET_PROOF):bind(*a[:2])
  old=json.loads((B/ORIGINAL_SHEET_RECEIPT[0]).read_bytes());proof=json.loads((B/ORIGINAL_SHEET_PROOF[0]).read_bytes())
  assert old['status']=='CLOSED' and old['error_sha256'] is None and old['owner']==proof['owner'] and old['owner']['source_sha256']==ORIGINAL_SHEET_SOURCE[1]
  assert proof['status']==ORIGINAL_SHEET_PROOF[2] and proof['receipt_sha256']==ORIGINAL_SHEET_RECEIPT[1] and proof['result_sha256']==old['result_sha256'] and proof['source_sha256']==ORIGINAL_SHEET_SOURCE[1]
  assert proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is proof['all_success_role_seals_verified'] is True and proof['owner']['pid']==97585 and all(x is False for x in proof['qualification'].values())
  w=s['records']['fixed_sheet_original'];sheet=w['reference'];assert w['scientific_owner']==proof['owner'] and w['ancestor_seal_proof']==list(ORIGINAL_SHEET_PROOF) and w['explicit_inherited_success_refs']==[sheet]
  sm=archive(sheet,proof['owner'],old);assert sm['reference']==ORIGINAL_LABEL_REFERENCE and sm['finite_rho']==0. and sm['labels_and_locations_unchanged'] is sm['no_candidate_volume_or_budget_subtraction'] is True
  assert sm['mapping_proof_retained']=='SAVED_ORDINARY_MAPPING_PASS' and sm['reference_lineage_admitted_by_helper'] is False
  assert [(q['name'],q['tolerance'],q['passed'])for q in sm['completed_controls']]==[('sheet_value_polynomial_transpose',2e-11,True),('sheet_delta_polynomial_transpose',2e-11,True)]
  check('original_sheet_owner_seals_and_fixed_label_source',True,dict(owner=proof['owner'],sheet=sheet,original_reference=sm['reference'],original_controls_inherited=2,no_original_LOADS_payload_opened=True))
  tr=v['records']['original_targets_input'];rc,pr=terminal('original_targets',v['terminals']['original_targets']);tm=archive(tr['reference'],tr['scientific_owner'],rc)
  fr=v['records']['finite_readout'];rc,pr=terminal('finite139',v['terminals']['finite139']);fm=archive(fr['reference'],fr['scientific_owner'],rc)
  assert tm['basis']==v['original_basis_source_ref'] and tm['rho_W_t_all_exact_zero'] is True and tm['TT_or_exterior_prior_refitted'] is False
  fp=fm['provenance'];assert fp['baseline_closure'][0]==list(ORIGINAL_SHEET_SOURCE) and fp['baseline_closure'][2][:2]==list(ORIGINAL_SHEET_RECEIPT) and fp['baseline_closure'][3]==list(ORIGINAL_SHEET_PROOF)
  assert fp['original_fixed_references_verified'] is fp['unchanged_sheet_value_identity_verified'] is True and fp['physical_adoption'] is False
  check('same_fixed_basis_and_sheet_ancestry',True,dict(basis=tm['basis'],readout=fr['reference'],baseline_closure=fp['baseline_closure'],sheet_invariance_source_scoped=True))
  native,metric,scalar,normal=masks();counts=[int(np.count_nonzero(a))for a in (native,metric,scalar,normal)]
  check('original_masks_and_packed_sizes',counts==[380292,23048,3870,14875] and sum(counts)==425955,dict(native=counts[0],metric=counts[1],mechanical=counts[0]+counts[1],scalar=counts[2],normal=counts[3],configuration=counts[2]+counts[3],normal_row_counts=[int(np.count_nonzero(a))for a in normal],source_functions_only=['native_mask','metric_mask','scalar_mask','normal_test_mask']))
  R=member(tr['reference'],tm,'original_basis_R',(4,3784));dv=member(tr['reference'],tm,'original_basis_dv',(4,3784));member(tr['reference'],tm,'original_basis_hats',(4,4,3,86,44))
  check('original_volume_weights_and_basis_shapes',np.all(R>0)&np.all(dv>0),dict(columns=4,points_per_column=3784,hats_shape=[4,4,3,86,44],volume_weight='original dv/R once',sheet_weight='unweighted original two-side incidence; beta_R has original R factor',new_weight_contractions_performed=False))
  for name,mask,shape,prefix in [('native',native,(33,3,87,45),'completed_READOUT_current_native'),('metric',metric,(6,87,45),'completed_READOUT_current_metric'),('normal',normal,(4,87,45),'completed_READOUT_weak_normal'),('CMC',scalar,(87,45),'completed_READOUT_weak_initial_CMC')]:
   p=pair(fr['reference'],fm,prefix,shape);check('original_inactive_'+name+'_words',all(np.all(a[~mask]==0)for a in p),dict(mask_source_pinned=True,both_words_checked=True,reference_equality_replayed=False))
  for name,mask,shape in [('native',native,(33,3,87,45)),('metric',metric,(6,87,45))]:
   scale=member(tr['reference'],tm,'original_reference_'+name+'_scale',shape);check('original_active_'+name+'_scale',np.all(scale[mask]>0),dict(active_count=int(np.count_nonzero(mask)),inactive_scale_floor_not_introduced=True))
  def get(k,shape,dtype='float64'):return member(sheet,sm,k,shape,dtype)
  sr=get('fixed_label_sheet_fixed_R',(4832,));sz=get('fixed_label_sheet_fixed_Z',(4832,));indices=get('fixed_label_sheet_rho_fixed_indices',(4832,),'int64');right=get('fixed_label_sheet_rho_fixed_right_weight',(4832,))
  check('original_sheet_domain_and_two_side_incidence',np.all(sr>0)&np.all(sz==0)&np.all(indices>=0)&np.all(indices<86)&np.all(right>0)&np.all(right<1),dict(nodes=4832,indices_dtype='int64',right_weight_open_interval=[0,1],Z_both_side_sheet=0,volume_dv_over_R_not_applied_to_sheet=True))
  rawg=get('fixed_label_sheet_authentic_reference_g',(4832,4,4));h=pair(sheet,sm,'fixed_label_sheet_reference_h',(4832,3,3));weight=pair(sheet,sm,'fixed_label_sheet_conformal_weight',(4832,));rho=pair(sheet,sm,'fixed_label_sheet_rho_sample',(4832,));candidate=pair(sheet,sm,'completed_sheet_geometry_geometry_h',(4832,3,3))
  check('original_rho_zero_reference_spatial_geometry',np.array_equal(h[0].view(np.uint64),rawg[:,1:,1:].view(np.uint64)) and np.all(h[1]==0) and np.all(weight[0]==1) and np.all(weight[1]==0) and all(np.all(a==0)for a in rho) and all(np.array_equal(a.view(np.uint64),b.view(np.uint64))for a,b in zip(h,candidate)),dict(finite_rho=0,reference_h_raw_word_tie=True,conformal_weight=[1,0],candidate_spatial_words_tied=True,inverse_root_and_location_contacts_not_zero_assumed=True))
  for path,e in [('gauge.N',s['data_q_sheet']['gauge']['N']),('gauge.beta',s['data_q_sheet']['gauge']['beta'])]+[(n,e)for n,e in s['data_q_sheet']['labels'].items()if isinstance(e,dict)and '$record'in e and '$keys'in e]:
   assert e['$record']=='fixed_sheet_original'
   for key in e['$keys']:get(key,e['$shape'],e['$dtype'])
  contact=pair(sheet,sm,'fixed_label_sheet_fixed_label_location_contact',(4832,));check('original_sheet_labels_gauge_and_contacts_retained',True,dict(radiation_rows=0,gauge_shapes={'N':[4832],'beta':[4832,3]},labels_once=True,reference=sm['reference'],location_contact_nonzero_word_counts=[int(np.count_nonzero(a))for a in contact],location_contact_forced_zero=False,ordinary_or_sheet_derivative_replayed=False))
  for n,snap in STATS.items():assert snapshot(Path(n))==snap,n
  result=dict(status='CLOSED_FIXED_SHEET_MASK_WEIGHT_PREREQUISITES_PASS',observed_utc=datetime.now(timezone.utc).isoformat(),selected_assembly=list(SELECTED),sheet_selector=list(SHEET_MAP),inherited90_result=list(PRIOR90),inherited_word_families=90,prior90_word_links_replayed=False,predicates=DONE,sheet=sheet,sheet_owner=proof['owner'],readout=fr['reference'],readout_owner=fm['owner'],original_basis=tm['basis'],registered_sheet_once=True,new_qwc_sheet_unit_preparation_performed=False,original_LOADS_archive_bytes_reauthenticated=False,coefficient_240_archives_read_or_hashed=False,all13group_runtime_admitted=False,physical_adoption=False,verified_sha256=VERIFIED,stable_stats=STATS,scope='Only three archive pairs: original sheet, saved fixed basis/scales, recovered current masked words. Inherited90 exact links are not recalculated. Missing whole13 runtime leases and fresh response gates remain external.')
  h=seal(STEM+'_RESULT.json',result);print(json.dumps(dict(file=STEM+'_RESULT.json',sha256=h,predicates=len(DONE),prior90_replayed=False,physical_adoption=False)))
 except BaseException:
  seal(STEM+'_ERROR.json',dict(status='FAILED_FIXED_SHEET_MASK_WEIGHT_PREFIX_PRESERVED',context=CONTEXT,completed_predicates=DONE,inherited90_result=PRIOR90,traceback=traceback.format_exc(),verified_sha256=VERIFIED,stable_stats=STATS,physical_adoption=False));raise
if __name__=='__main__':main()
