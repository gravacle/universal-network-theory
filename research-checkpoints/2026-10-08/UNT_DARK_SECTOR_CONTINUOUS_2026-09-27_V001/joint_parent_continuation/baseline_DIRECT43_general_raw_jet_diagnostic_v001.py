"""HELD closed baseline85 -> exact205 intervals -> general161 diagnostic.
Root alone releases/runs. No old producer/action, corrected geometry or circle.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
from math import isqrt
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='BASELINE_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V001'
PROTOCOL='BASELINE_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V001.md'
PROTOCOL_SHA=None
SOURCE=(None,None)
RESULT=(None,None,'DIRECT43_ORIGINAL_BASELINE_FIELDS_PREPARED_UNQUALIFIED')
RECEIPT=(None,None,'CLOSED')
PROOF=(None,None,'READONLY_NATURAL_CLOSED_DIRECT43_BASELINE_SUCCESS_SEALS_VERIFIED')
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_finite_conformal_circle_event_v001.py':'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_baseline_DIRECT43_raw_jet_pair_v001.py':'07cbcd0af964ba2531c12878e629b9c58ce56bff23fa94bd5471d83162ab2dd9',
 'author_fragment_conformal_DIRECT43_uncertainty_primitives_v003.py':'0027662008c236628ffd8b82e7202a24153ea6dadc8d1beeaeec9f7d2d31cd83',
 'author_fragment_general_raw_jet_instantaneous_geodesic_v001.py':'b357de459494d9bad5bb0963ee2c3236ca8265872ebaf583062e54b03b40602b',
 'direct43_original_baseline_preparation_v003.py':'68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336',
 'author_fragment_direct43_owned_baseline_field_law_v004.py':'99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1',
 'author_fragment_direct_TOTAL43_finite_event_v001.py':'9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'cross_u_full_metric_geodesic_and_rotating_material_v001.py':'53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa',
 'author_fragment_full_dynamic_metric_circle_v002.py':'3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};EVENT_CONTEXT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==set(names),file
 exec(compile(ast.Module(body=nodes,type_ignores=[]),file,'exec'),scope)

def constants(file,names):
 out={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse((BASE/file).read_text()).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names}
 assert set(out)==set(names),file;return out

def metadata(file,checksum):
 bind(file,checksum);p=P.path(file);assert p.stat().st_size<=16*1024*1024,file;return json.loads(p.read_text())

def retain(name,value):
 CONTEXT['active_capture']=name;return keep(name,value)

def initialize():
 global np,P
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','keep','read','thin','clear_current','initialize_io'},globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=retain)
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 definitions(list(PINS)[0],base,SCOPE)
 for n in base:setattr(P,n,SCOPE[n])
 definitions('author_fragment_exact_exponent_two_product_v003.py',{'exact_exponent_two_product','install_exact_exponent_product'},globals());install_exact_exponent_product(SCOPE,P,retain,'baseline_raw_shared_exact_product')
 definitions('author_fragment_finite_conformal_circle_event_v001.py',{'fce_pair','fce_block'},globals());definitions('author_fragment_finite_york_geometry_target_v001.py',{'fy_mv','fy_sum'},globals())
 helper='author_fragment_baseline_DIRECT43_raw_jet_pair_v001.py';definitions(helper,{'baseline_DIRECT43_raw_jet_require','baseline_DIRECT43_raw_jet_pair'},globals());globals().update(constants(helper,{'BASELINE_RAW_JET_SOURCE_PINS'}))
 globals().update(BASELINE_RAW_JET_AUTHOR_DRAFT=False,BASELINE_RAW_JET_AUTHORING_IN_PROGRESS=False,BASELINE_RAW_JET_SOURCE=SOURCE,BASELINE_RAW_JET_RESULT=RESULT,BASELINE_RAW_JET_RECEIPT=RECEIPT,BASELINE_RAW_JET_PROOF=PROOF)
 helper='author_fragment_conformal_DIRECT43_uncertainty_primitives_v003.py';names={n.name for n in ast.parse((BASE/helper).read_text()).body if isinstance(n,ast.FunctionDef)};assert len(names)==23;definitions(helper,names,globals());globals().update(constants(helper,{'CONFORMAL_UNCERTAINTY_SOURCE_PINS'}))
 globals().update(CONFORMAL_UNCERTAINTY_AUTHOR_DRAFT=False,CONFORMAL_UNCERTAINTY_AUTHORING_IN_PROGRESS=False,CONFORMAL_UNCERTAINTY_TERMINALS={n:(None,None,None,None) for n in ('direct_baseline','finite_trial','coupled_correction','selected_inputs')},CONFORMAL_UNCERTAINTY_BASELINE_TERMINALS=dict(source=SOURCE,result=RESULT,receipt=RECEIPT,proof=PROOF))
 helper='author_fragment_general_raw_jet_instantaneous_geodesic_v001.py';definitions(helper,{'grg_pair','grg_interval_event','general_raw_jet_instantaneous_geodesic'},globals());globals().update(constants(helper,{'GENERAL_RAW_GEODESIC_SOURCE_PINS','GENERAL_RAW_GEODESIC_ROOT_BITS'}))
 globals().update(GENERAL_RAW_GEODESIC_AUTHOR_DRAFT=False,GENERAL_RAW_GEODESIC_AUTHORING_IN_PROGRESS=False,GENERAL_RAW_GEODESIC_EVENT_SOURCE=SOURCE,GENERAL_RAW_GEODESIC_EVENT_RESULT=RESULT,GENERAL_RAW_GEODESIC_EVENT_RECEIPT=RECEIPT,GENERAL_RAW_GEODESIC_EVENT_PROOF=PROOF,GENERAL_RAW_GEODESIC_INTERVAL_SOURCE=(list(PINS)[7],PINS[list(PINS)[7]]))

def admission():
 for pin in (SOURCE,RESULT,RECEIPT,PROOF):assert all(v is not None for v in pin);bind(*pin[:2])
 result=metadata(*RESULT[:2]);receipt=metadata(*RECEIPT[:2]);proof=metadata(*PROOF[:2])
 assert SOURCE==(list(PINS)[9],PINS[list(PINS)[9]]) and result['status']==RESULT[2] and receipt['status']==RECEIPT[2] and proof['status']==PROOF[2]
 assert proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is proof['all_output_seals_verified'] is proof['all_success_role_seals_verified'] is True
 assert proof['source_sha256']==SOURCE[1] and proof['result_sha256']==RESULT[1] and proof['receipt_sha256']==RECEIPT[1]
 assert result['owner']==receipt['owner']==proof['owner'] and result['owner']['source_sha256']==SOURCE[1]
 assert receipt['error_sha256'] is None and receipt['result_sha256']==RESULT[1] and not result['controls'] and result['qualification']==receipt['qualification']==FLAGS
 assert result['case']['baseline_only'] is True and result['case']['physical_circle_or_new43_prediction_earned'] is False and result['case']['physical_adoption'] is False
 assert len(result['checkpoints'])==87 and result['case']['roles']==proof['science_role_count']==87 and result['case']['controls']==0 and len(result['case']['events'])==43
 return dict(result=result,receipt=receipt,proof=proof,terminal=dict(source=SOURCE,result=RESULT,receipt=RECEIPT,proof=PROOF,naturally_closed=True,exit_code=0,all_input_seals_verified=True,all_success_role_seals_verified=True,owner=result['owner']))

def record(ref,refs,ordinal,role,index):
 assert ref['file']==SOURCE[0].replace('direct43_original_baseline_preparation_v003.py','DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003')+'_%05d_%s.npz'%(ordinal,role)
 q=metadata(ref['commit_file'],ref['commit_sha256']);assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 md=q['metadata'];assert md['owner']==refs['result']['owner'] and md['failed'] is md['physical_adoption'] is False and md['qualification']==FLAGS and md['index']==index
 assert thin(refs['result']['checkpoints'][ordinal])==ref
 for f,h in (('file','sha256'),('commit_file','commit_sha256')):assert refs['receipt']['output_sha256'][ref[f]]==ref[h];bind(ref[f],ref[h])
 return dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def load(ref,names,label):
 assert all(n in ref['metadata']['schema'] for n in names);data=read(ref,names)
 for n,a in data.items():RAW[label+'_'+n]=a.copy();retain(label+'_'+n,a);s=ref['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True
 return data

def serial(value):
 if isinstance(value,Fraction):return dict(numerator=str(value.numerator),denominator=str(value.denominator))
 if isinstance(value,np.ndarray):return serial(value.tolist())
 if isinstance(value,np.generic):return serial(value.item())
 if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
 if isinstance(value,(tuple,list)):return [serial(v) for v in value]
 if value is None or type(value) in (str,bool,int) or type(value)is float and math.isfinite(value):return value
 raise TypeError(type(value).__name__)

def complete(role,data):
 def numeric(x,prefix):
  if isinstance(x,np.ndarray):return {prefix:x.copy()}
  if isinstance(x,dict):return {k:a for n,v in x.items() for k,a in numeric(v,prefix+str(n)+'_').items()}
  if isinstance(x,(tuple,list)):return {k:a for n,v in enumerate(x) for k,a in numeric(v,prefix+str(n)+'_').items()}
  return {}
 CONTEXT.update(EVENT_CONTEXT,stage=role);q=P.checkpoint(role,dict(RAW,**AVAILABLE,**numeric(data,'completed_')),dict(role=role,context=dict(CONTEXT),completed_payload=serial(data),baseline_only=True,physical_adoption=False))
 ref=thin(q);clear_current();CONTEXT.update(EVENT_CONTEXT,completed_stage=role);return ref

def word_tree(pair):
 hi,lo=pair;assert hi.shape==lo.shape and hi.dtype==lo.dtype==np.float64 and np.all(np.isfinite(hi)) and np.all(np.isfinite(lo))
 def build(a,b):
  if a.shape==():return (Fraction.from_float(float(a)),Fraction.from_float(float(b)))
  return [build(x,y) for x,y in zip(a,b)]
 return build(hi,lo)

def dyadic_tree(array):
 if array.shape==():return Fraction.from_float(float(array))
 return [dyadic_tree(a) for a in array]

def event_inputs(refs,event):
 i=event['index'];rr=record(event['reference_event'],refs,1+2*i,'REFERENCE_EVENT',i);br=record(event['baseline_event'],refs,2+2*i,'BASELINE_EVENT',i)
 shapes={'h':(3,3),'h_spatial_jets':(2,3,3),'N':(),'beta':(3,),'N_jets':(4,),'beta_jets':(4,3),'g':(4,4),'dg':(4,4,4)}
 d=load(rr,tuple(n+'_'+w for n in shapes for w in ('hi','lo')),'reference');reference={n:tuple(d[n+'_'+w] for w in ('hi','lo')) for n in shapes}
 md=rr['metadata'];reference.update(R=md['R'],Z=md['Z'],radial_side=md['radial_side'],provenance=md['reference_event_provenance'])
 assert md['R']==br['metadata']['R']==event['R']
 prefix='DIRECT_rate_%02d_original60363_increment_'%i
 names=['baseline_TOTAL_hdot_'+w for w in ('hi','lo')]+['original47969_hdot_'+w for w in ('hi','lo')]+[prefix+'positive_sheet_value_R_Z_weights']
 names+=[prefix+n+'_'+w for n in ['chi_corner%d'%c for c in range(4)]+['chi_jet%d_partial'%j for j in range(3)]+['CORRECTION_corner%d'%c for c in range(4)]+['CORRECTION_time_partial'] for w in ('hi','lo')]
 names+=[prefix+'original_rounded_Fhat_corner%d'%c for c in range(4)];b=load(br,tuple(names),'baseline')
 def pair(n):return tuple(b[n+'_'+w] for w in ('hi','lo'))
 for n in ['chi_corner%d'%c for c in range(4)]+['chi_jet%d_partial'%j for j in range(3)]:assert all(a.shape==() and a==0 for a in pair(prefix+n)),'Authentic saved zero chi/rho required'
 for n,shape in shapes.items():assert all(a.shape==shape for a in reference[n])
 ht=pair('baseline_TOTAL_hdot');assert all(a.shape==(3,3) for a in ht+pair('original47969_hdot')) and b[prefix+'positive_sheet_value_R_Z_weights'].shape==(3,4)
 sampling=dict(chi_corners=[word_tree(pair(prefix+'chi_corner%d'%c)) for c in range(4)],weights=dyadic_tree(b[prefix+'positive_sheet_value_R_Z_weights']),rho_words=[word_tree(pair(prefix+'chi_jet%d_partial'%j)) for j in range(3)],metric_corners=[word_tree(pair(prefix+'CORRECTION_corner%d'%c)) for c in range(4)],Fhat=[dyadic_tree(b[prefix+'original_rounded_Fhat_corner%d'%c]) for c in range(4)],delta_six_words=word_tree(pair(prefix+'CORRECTION_time_partial')),baseline_hdot_words=word_tree(pair('original47969_hdot')),total_hdot_words=word_tree(ht))
 adm=dict(source_pins=BASELINE_RAW_JET_SOURCE_PINS,baseline_terminal=refs['terminal'],reference_record=thin(rr),baseline_record=thin(br),reference_metadata=md,baseline_metadata=br['metadata'],selected_metadata_and_words_authenticated=True,same_geometry_baseline_not_new_coupled_trial=True)
 adm['original_input_word_hex']=dict(reference={n:{w:[float(x).hex() for x in a.flat] for w,a in zip(('hi','lo'),reference[n])} for n in shapes},baseline={n:[float(x).hex() for x in a.flat] for n,a in b.items()})
 return reference,ht,sampling,adm

def prepare(refs):
 header=complete('INPUT',dict(baseline_terminal=refs['terminal'],events=refs['result']['case']['events'],interval_limits=dict(bits=128,max_terms=256,max_squarings=16),orientation=1,new_coupled_or_finite_closure_used=False));events=[]
 for index,event in enumerate(refs['result']['case']['events']):
  assert event['index']==index;EVENT_CONTEXT.clear();EVENT_CONTEXT.update(index=index,R=event['R'],radial_side='left',vertical_side='upper',source_reference_event=event['reference_event'],source_baseline_event=event['baseline_event']);CONTEXT.update(EVENT_CONTEXT,stage='authentic_closed_event_words')
  reference,ht,sampling,adm=event_inputs(refs,event);before=len(RECORDS)
  raw=baseline_DIRECT43_raw_jet_pair(reference,ht,admission=adm,keep=retain,label='EVENT_%02d_RAW'%index,stage_complete=complete);assert len(RECORDS)-before==4
  interval_adm=dict(terminals=CONFORMAL_UNCERTAINTY_BASELINE_TERMINALS,source_pins=CONFORMAL_UNCERTAINTY_SOURCE_PINS,input_scope='closed_direct_baseline_evidence',baseline_naturally_closed=True,baseline_exit_code=0,baseline_selected_record_owner_and_seals_verified=True,same_geometry_baseline_not_new_coupled_trial=True,all_selected_dyadic_inputs_authenticated=True,original_masks_lifts_Fhat_corner_order_verified=True,point_TOTAL_addition_after_lift_verified=True,same_event_reference_and_radial_side_verified=True,all_original_word_hex_and_gauge_time_phi_retained=True,physical_metric_admitted=False,finite_constraint_solution_admitted=False,sampling_refs={n:adm[n] for n in ('reference_record','baseline_record')})
  before=len(RECORDS);box=conformal_DIRECT43_primitive_enclosure(dict(words={n:word_tree(reference[n]) for n in ('h','h_spatial_jets','N','beta','N_jets','beta_jets')}),sampling,interval_adm,dict(bits=128,max_terms=256,max_squarings=16),complete,'EVENT_%02d_INTERVAL'%index);assert len(RECORDS)-before==11
  words=dict(g=word_tree(raw['g']),dg=word_tree(raw['dg']),all_output_dyadic_words_authenticated=True,all_original_word_hex_preserved=True,word_hex={n:{w:[float(x).hex() for x in a.flat] for w,a in zip(('hi','lo'),raw[n])} for n in ('g','dg')},completed_raw_pair=raw['source_stage_refs']['raw_pair'])
  before=len(RECORDS);bounds=attach_completed_DIRECT43_words(box,words,complete,'EVENT_%02d_ATTACH'%index);assert len(RECORDS)-before==2
  interval_proof=box['completed'][-1];globals()['GENERAL_RAW_GEODESIC_INTERVAL_PROOF']=(interval_proof['commit_file'],interval_proof['commit_sha256'],'same_owner_completed_exact_primitive_box')
  grg_adm=dict(source=SOURCE,result=RESULT,receipt=RECEIPT,proof=PROOF,interval_source=GENERAL_RAW_GEODESIC_INTERVAL_SOURCE,interval_proof=GENERAL_RAW_GEODESIC_INTERVAL_PROOF,naturally_closed=True,exit_code=0,all_selected_byte_owner_and_header_seals_verified=True,physical_metric_admitted=False,input_scope='closed_direct_baseline_evidence',coordinate_event=raw['coordinate'],radial_side='left',vertical_side='upper',interval_event_provenance=box['provenance'],event_provenance=dict(ancestral_closed_baseline=refs['terminal'],same_owner_completed_raw_pair=raw['source_stage_refs']['raw_pair'],source_records=interval_adm['sampling_refs']))
  before=len(RECORDS);result=general_raw_jet_instantaneous_geodesic(raw['g'],raw['dg'],bounds=bounds,orientation=1,admission=grg_adm,keep=retain,label='EVENT_%02d_GENERAL'%index,stage_complete=complete);count=len(RECORDS)-before;assert 2<=count<=6
  events.append(dict(index=index,R=event['R'],raw_pair_stages=raw['source_stage_refs'],interval_stages=box['completed'],attachment_stages=bounds['completed'],general_stages=result['completed_stage_refs'],general_role_count=count,readout=serial(result),source_association_gaps=serial(raw['source_association_gaps']),physical_adoption=False))
 assert len(events)==43 and len(RECORDS)==1+43*17+sum(e['general_role_count'] for e in events) and not CHECKS
 return dict(status='BASELINE_DIRECT43_GENERAL_INSTANTANEOUS_RADIAL_DIAGNOSTICS_MEASURED',input=header,events=events,roles=len(RECORDS),controls=0,baseline_only=True,new_coupled_or_corrected_finite_metric_evaluated=False,source_or_installed_rounding_accuracy_admitted=False,full_circle_or_galaxy_prediction_admitted=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for pin in (SOURCE,RESULT,RECEIPT,PROOF) for v in pin),'Independent FULL review and actual closed baseline binding required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=dict(INPUTS),baseline_terminal=refs['terminal'],events=43,roles='1+43*(4raw+11primitive+2attachment)+sum(general2to6)',controls=0,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=prepare(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,checkpoints=RECORDS,controls=CHECKS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}),dict(kind='unfinished_baseline_general_raw_diagnostic',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
