"""HELD root-owned43 diagnostic of fixed configuration plus nonconverged rates.
No EOS/native-action/field solve, Gauss interpolation, fit or physical adoption.
All43 supplied new event metrics/jets are published before any circle readout.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import argparse,ast,hashlib,json,math,os,statistics,sys,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_NONCONVERGED_CURRENT_METRIC_43_DIAGNOSTIC_V002'
ROTATION_ORIENTATION=1 # Declared coordinate orientation, fixed independently of Vobs.
RADIAL_SIDE='left';SHEET_SIDE='positive'
PINS={
 'author_fragment_nonconverged_current_metric_event_sampler_v002.py':'43f7a3c6f7bd13d1b94f3207d2c671c5c3282ab2c98195481a1d20940ec608a5',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'author_fragment_full_dynamic_metric_circle_v002.py':'3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b',
 'author_fragment_revised_43_observer_report_v002.py':'0cab1853d083239175943a4765101a95104949bb14f13ca1eb9902713df92843',
 'cross_u_full_metric_geodesic_and_rotating_material_v001.py':'53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa',
 'cross_u_whole_slice_cauchy_data_v002.py':'6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_native_metric_star_paired_trace_gmres_v002.py':'091a6d1303bf8c75160a0472af6e88688b89be4e6ba6b770310b280125350871',
 'NGC3198_FINE_Q3_43_POINT_SAVED_RECAP_V001.json':'ea6e41a879bab1ed43fa556031ad96ae3535779707af62d30eff061b191fc024',
 'sparc_official_NGC3198_rotmod.dat':'17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953',
 'READONLY_CURRENT_METRIC_EVENT_SELECTED_PROVENANCE_V001.json':'f849cd1fa76d400e0858f45673e062a33a1a63ea8c4c838bd8e71bc513742808'}
TERMINALS=(
 ('CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002',24903,'af0365e378a46c727108c7df57f527994a22b7428d72b1f67c6f1bbac93667ed','88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9'),
 ('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001',47969,'6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc','a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d'),
 ('CROSS_U_NATIVE_METRIC_STAR_PAIRED_TRACE_GMRES_V002',83768,'131981ac294b722c8d50ec82bafdb643fb5425a734d2f33b868245deffe822f8','bc9546a41af95ed6612284709899cacd88167b1bf876da8b49575f3dff9c5c7f'))
DRIVER_PROTOCOL='CROSS_U_NONCONVERGED_CURRENT_METRIC_43_DIAGNOSTIC_V001.md';DRIVER_PROTOCOL_SHA='c4cf63a2fff32f8f776e6ad5d5fb2df5cba63891014cc8ac4819f48dcc3ceac0'
np=P=H=G=CIRCLE=REPORT=SAMPLE=None
RAW={};INPUTS={};OUTPUTS={};RECORDS=[];EVENTS=[];SCOPE={};OWNER=None

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def bind(name,expected):
 assert expected and sha(name)==expected,(name,'SHA mismatch');INPUTS[name]=expected;return BASE/name
def keep(name,value):
 a=np.asarray(value).copy();RAW[name]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name;return a
def clean(value):
 if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
 if isinstance(value,(tuple,list)):return [clean(v) for v in value]
 if hasattr(value,'tolist'):return clean(value.tolist())
 if isinstance(value,float) and not math.isfinite(value):return dict(nonfinite_value=repr(value))
 return value
def write_json(name,value):
 with (BASE/name).open('x') as f:json.dump(clean(value),f,sort_keys=True,indent=2,allow_nan=False)
 (BASE/name).chmod(0o444);OUTPUTS[name]=sha(name);return OUTPUTS[name]
def snapshot(role):
 name=STEM+'_'+role+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/name).chmod(0o444);OUTPUTS[name]=sha(name);record=dict(role=role,file=name,sha256=OUTPUTS[name],fields=len(RAW));RECORDS.append(record);return record
def definitions(name,names,extras=None):
 source=bind(name,PINS[name]);tree=ast.parse(source.read_text());all_defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 scope=dict(np=np,math=math,json=json,statistics=statistics,Fraction=Fraction,EPS=sys.float_info.epsilon,DD_ARRAY_CURRENT={});scope.update(extras or {})
 exec(compile(ast.Module(body=[all_defs[n] for n in names],type_ignores=[]),str(source),'exec'),scope);return types.SimpleNamespace(**{n:scope[n] for n in names}),scope
def initialize():
 global P,H,G,CIRCLE,REPORT,SAMPLE,SCOPE
 P,SCOPE=definitions('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py',('a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_mul','a_mul64','a_matvec','a_slice'))
 G,_=definitions('cross_u_full_metric_geodesic_and_rotating_material_v001.py',('floating_refusal','finite_result','real','metric_geometry','normal_observer','geodesic_rhs','dynamic_circle_residual'))
 CIRCLE,_=definitions('author_fragment_full_dynamic_metric_circle_v002.py',('full_dynamic_circle_coefficients','full_dynamic_polynomial_roots','full_dynamic_circle_candidates'),dict(G=G))
 unit_source=ast.parse((BASE/'author_fragment_model_metric_si_circle_readout_v002.py').read_text())
 unit_pins=next(ast.literal_eval(n.value) for n in unit_source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODEL_SI_UNIT_SOURCE_PINS' for t in n.targets))
 for n,h in unit_pins.items():bind(n,h)
 H,_=definitions('author_fragment_model_metric_si_circle_readout_v002.py',('native_313_si_registration','affine_metric_unit_pullback','q1_radial_readout_contact','orient_dynamic_circle_candidates'),dict(MODEL_SI_UNIT_SOURCE_PINS=unit_pins))
 REPORT,_=definitions('author_fragment_revised_43_observer_report_v002.py',('report43_path','report43_number','report43_statistics','revised_43_observer_report'))
 SAMPLE,_=definitions('author_fragment_nonconverged_current_metric_event_sampler_v002.py',('diagnostic_event_pair_keep','diagnostic_current_metric_event'),dict(P=P,H=H))
def selected_pair(ref,fields,receipt=None):
 bind(ref['commit_file'],ref['commit_sha256']);c=json.loads((BASE/ref['commit_file']).read_text());assert c['file']==ref['file'] and c['sha256']==ref['sha256']
 if receipt is not None:assert receipt['output_sha256'].get(ref['file'])==ref['sha256'] and receipt['output_sha256'].get(ref['commit_file'])==ref['commit_sha256']
 bind(ref['file'],ref['sha256'])
 with np.load(BASE/ref['file'],allow_pickle=False) as f:out={n:f[n].copy() for n in fields}
 for n,a in out.items():keep('selected_'+ref['file'].split('_000')[0]+'_'+n,a)
 return out,c
def admission():
 docs=[];receipts=[]
 for stem,pid,rh,ch in TERMINALS:
  rc=json.loads(bind(stem+'_RECEIPT.json',ch).read_text());assert rc['status']=='CLOSED' and rc['owner']['pid']==pid and rc['result_sha256']==rh
  result=json.loads(bind(stem+'_RESULT.json',rh).read_text());assert result['owner']==rc['owner'];docs.append(result);receipts.append(rc)
 refs=[]
 for d,tail in zip(docs,('_00000_INPUT.npz','_00007_SOLUTION.npz','_00006_RESPONSE.npz')):
  found=[r for r in d['checkpoints'] if r['file'].endswith(tail)];assert len(found)==1;refs.append(found[0])
 assert docs[2]['response']==refs[2] and docs[2]['status']=='STAR_GMRES_LITERAL_TRACE_RESPONSE_NOT_ADMITTED'
 assert docs[2]['frozen_original_response_admitted'] is False and docs[2]['literal_original_response_admitted'] is False and docs[2]['physical_adoption'] is False
 conf,_=selected_pair(refs[0],('final_state','sigma1_physical_beta_chi','r_kpc','z_kpc'),receipts[0])
 rates,rc=selected_pair(refs[1],('metric_nodal_rate_hi','metric_nodal_rate_lo'),receipts[1])
 response,_=selected_pair(refs[2],('final_paired_response_hi','final_paired_response_lo'),receipts[2])
 basis=rc['metadata']['basis_ref'];grid,_=selected_pair(basis,('r','z'))
 assert np.array_equal(conf['r_kpc'],grid['r']) and np.array_equal(conf['z_kpc'],grid['z'])
 assert conf['final_state'].shape==(65,87,45) and conf['sigma1_physical_beta_chi'].shape==(2,87,45)
 mask=np.ones((6,87,45),dtype=bool);mask[:,0,:]=False;mask[3:5,:,0]=False;keep('unchanged_independent_metric_mask',mask)
 response_nodes=[]
 for word in ('hi','lo'):
  x=response['final_paired_response_'+word];assert x.shape==(403340,);y=np.zeros((6,87,45));y[mask]=x[380292:];keep('full_nonconverged_metric_response_'+word,y);response_nodes.append(y)
 provenance=dict(terminals=[dict(stem=s,pid=p,result_sha256=r,receipt_sha256=c) for s,p,r,c in TERMINALS],configuration_source=refs[0],current_rate_source=refs[1],response_source=refs[2],shared_rate_basis=basis,
  gauge_time_policy='original_stationary_seed_plus_fixed_N_beta_owned_K_lift',configuration_changed=False,nonconverged_response_adopted_as_physical_solution=False,
  original_primitive_mismatch_preserved=True,original_GMRES_six_gates_admitted=False,source_chain_static_proof=PINS['READONLY_CURRENT_METRIC_EVENT_SELECTED_PROVENANCE_V001.json'])
 return conf,tuple(rates['metric_nodal_rate_'+w] for w in ('hi','lo')),tuple(response_nodes),provenance
def sample_all(conf,current,response,baseline,provenance):
 B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2;keep('source_literal_B',np.array(B))
 for index,row in enumerate(baseline['rows']):
  label='event_%02d'%index;event=dict(index=index,R_kpc=row['R_kpc'],Vobs_kms=row['observed_velocity_kms'],measured_sigma_kms=row['quoted_error_kms'],declared_orientation=ROTATION_ORIENTATION);EVENTS.append(event)
  try:
   event['sample']=SAMPLE.diagnostic_current_metric_event(conf['r_kpc'],conf['z_kpc'],conf['final_state'][0],conf['sigma1_physical_beta_chi'][0],current,response,potential_normalization=B,R=row['R_kpc'],radial_side=RADIAL_SIDE,sheet_side=SHEET_SIDE,provenance=provenance,keep=keep,label=label)
  except (AssertionError,ValueError,TypeError,KeyError,ArithmeticError) as error:event['sampling_refusal']=type(error).__name__+': '+str(error)
 assert len(EVENTS)==43;snapshot('ALL43_EVENTS_BEFORE_READOUT');write_json(STEM+'_ALL43_EVENT_REGISTRATION.json',dict(events=EVENTS,provenance=provenance,physical_adoption=False))
def readout_all(baseline,provenance):
 units=H.native_313_si_registration();rows=[]
 for event in EVENTS:
  index=event['index'];v=None;note='';flags=dict(nonconverged_state=True,physical_metric_admitted=False,finite_constraint_solution_admitted=False,readout_precision_admitted=False,unique_oriented_radial_root=False,full_instantaneous_circle_admitted=False)
  try:
   sample=event['sample'];pulled=H.affine_metric_unit_pullback(sample['g_model'],sample['dg_model_binary64'],units['dmodel_dSI'],units['metric_length_unit_m']);event['SI_pullback']=pulled
   geo=G.metric_geometry(pulled['g'],pulled['dg'],units['cp_m_per_s']);event['geometry']=geo
   dynamic=CIRCLE.full_dynamic_circle_candidates(geo,azimuth=3,meridional=(1,2),radial=1);event['all_dynamic_candidates']=dynamic
   oriented=H.orient_dynamic_circle_candidates(dynamic,ROTATION_ORIENTATION);event['orientation_selection']=oriented;choice=oriented['selected_index'];flags['unique_oriented_radial_root']=choice is not None
   for candidate in oriented['candidates']:
    target=np.array((0.,0.,candidate['Omega_dot']));candidate['coordinate_circle_acceleration']=target;candidate['geodesic_rhs_minus_circle_acceleration']=candidate['geodesic']['dw_dt']-target;candidate['clock_construction_gap']=candidate['circle']['f']-candidate['derived_f']
   if choice is not None:v=oriented['candidates'][choice]['declared_orientation_speed_kms'];note='Nonconverged fixed-configuration radial-balance diagnostic; all circle/geodesic defects retained. Binary64 readout is unqualified.'
   else:note=oriented['orientation_status']
  except (AssertionError,ValueError,TypeError,KeyError,ArithmeticError) as error:note='READOUT_REFUSED: '+type(error).__name__+': '+str(error);event['readout_refusal']=note
  event.update(radial_candidate_velocity_kms=v,physical_admitted_report_velocity_kms=None,interval_flags=flags,note=note)
  rows.append(dict(R_kpc=event['R_kpc'],velocity_kms=v,interval_flags=flags,note=note))
 status=dict(diagnostic_current_configuration_with_rate_correction=True,nonconverged_diagnostic_only=True,all43_radial_candidates_available=all(r['velocity_kms'] is not None for r in rows),original_GMRES_six_gates_admitted=False,physical_metric_admitted=False,finite_constraint_solution_admitted=False,readout_precision_admitted=False)
 scope=dict(motion_scope='radial_balance_diagnostic',state='current47969_absolute_rates_plus_full_nonconverged83768_response',configuration_changed=False,orientation=ROTATION_ORIENTATION,orientation_selected_using_Vobs=False,radial_side=RADIAL_SIDE,sheet_side=SHEET_SIDE,sheet_junction='one_sided_reflected_half_plane_only',gauge_time_policy=provenance['gauge_time_policy'],time_jets_zeroed=False,Gauss_tensor_interpolation=False,persistent_orbit_or_stability_admitted=False,synthetic_observation_or_physical_curve_admitted=False)
 return REPORT.revised_43_observer_report(baseline,rows,baseline_row_path=('rows',),baseline_fields=dict(radius=('R_kpc',),observed=('observed_velocity_kms',),sigma=('quoted_error_kms',),model=('Q1_predicted_velocity_kms',)),provenance=provenance,admission_status=status,prediction_kind='local_metric_circular_snapshot',prediction_scope=scope)
def main():
 global np,OWNER
 parser=argparse.ArgumentParser();parser.add_argument('--root-run',action='store_true');args=parser.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('HELD_DRAFT_NO_NUMERICAL_EXECUTION')
 assert type(ROTATION_ORIENTATION) is int and ROTATION_ORIENTATION in (-1,1)
 assert not list(BASE.glob(STEM+'_*')),'Exclusive new numerical namespace required'
 for name,h in PINS.items():bind(name,h)
 bind(DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA)
 import numpy as numpy_module
 np=numpy_module;OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=sha(Path(__file__).name),started_utc=datetime.now(timezone.utc).isoformat(),execution='root_owned_new_nonconverged43_diagnostic')
 write_json(STEM+'_OWNER_START.json',OWNER)
 try:
  initialize();conf,current,response,provenance=admission();baseline=json.loads((BASE/'NGC3198_FINE_Q3_43_POINT_SAVED_RECAP_V001.json').read_text());assert len(baseline['rows'])==43
  snapshot('INPUT');sample_all(conf,current,response,baseline,provenance);report=readout_all(baseline,provenance)
  write_json(STEM+'_EVENT_READOUT.json',dict(events=EVENTS,physical_adoption=False));report_name=STEM+'_REPORT.md'
  with (BASE/report_name).open('x') as f:f.write(report['markdown'])
  (BASE/report_name).chmod(0o444);OUTPUTS[report_name]=sha(report_name)
  for name,h in INPUTS.items():assert sha(name)==h
  result=dict(status='NONCONVERGED_CURRENT_CONFIGURATION_43_RADIAL_DIAGNOSTIC_COMPLETED',owner=OWNER,records=RECORDS,report=report,physical_adoption=False);rh=write_json(STEM+'_RESULT.json',result)
  write_json(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=OWNER,closed_utc=datetime.now(timezone.utc).isoformat(),result_sha256=rh,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),physical_adoption=False))
 except Exception:
  if SCOPE:RAW.update({STEM+'_last_DD_'+n:np.asarray(a).copy() for n,a in SCOPE['DD_ARRAY_CURRENT'].get('arrays',{}).items()})
  snapshot('ERROR_RAW');eh=write_json(STEM+'_ERROR.json',dict(status='CLOSED_ERROR',owner=OWNER,traceback=traceback.format_exc(),events=EVENTS,records=RECORDS,physical_adoption=False))
  receipt='_ERROR_RECEIPT.json' if (BASE/(STEM+'_RECEIPT.json')).exists() else '_RECEIPT.json';write_json(STEM+receipt,dict(status='CLOSED_ERROR',owner=OWNER,error_sha256=eh,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),physical_adoption=False));raise
if __name__=='__main__':main()
