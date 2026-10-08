"""HELD actual reference-candidate current/normal/initial-CMC measurement.
Root alone releases and executes after complete source/contract review.
No old coefficient/feature/momentum/normal/operator/solver producer is replayed.
All candidate coefficients and invariant EOS are rebuilt on one225 raw chart.
The inherited primitive epsilon, reference compatibility and physical ports
remain explicit; this is not a finite projection or a prepared galaxy state.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V001'
DRIVER_PROTOCOL='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V001.md'
PROTOCOL_SHA='253f43b95c8029d0f54b7e38082771bad2e6080f7288e076bcdea36c73e0235b'
ADMISSION_FILE='author_fragment_finite0_reference_admission_v002.py'
ADMISSION_SHA='90695639545a693297610567a0779f6812d0e9c2eda87722730680dd3bdfb2ae'
CONTROL_PROOF=('FINITE_CANDIDATE_CONTACT_NORMAL_CONTROLS_V002_RESULT.json','390aa856e2794239790e59a922b26f3eac2ba80163ad1497a1c758ec9315bce3','NEW_CANDIDATE_CONTACT_NATIVE_EH_GLOBAL_CONTROLS_PASS')
MIXED_CONTROL_PROOF=('FINITE_MIXED_PHASE_ORDINARY_EH_NORMAL_CONTROLS_V002_RESULT.json','6920e447997f77a05eda1a2b8d74d8f985371e133b780269a2d2fc48a0bbc711','NEW_SHARED_CANDIDATE_MIXED_FOUR_NORMAL_CONTROL_PASS')
SHEET_CONTROL_PROOF=('FIXED_LABEL_FINITE_SHEET_GEOMETRY_CONTROLS_V002_RESULT.json','dcd07b86af968316fe2563f34ad6cc729d71e31b46f7f648d96501a9991f7a5f','NEW_FIXED_LABEL_Q1_REFERENCE_CONFORMAL_CONTROLS_PASS')
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_finite_candidate_native_EH_normal_v001.py':'51947ffe86b0b2aa592ac331aaaca2323872249785268d0dbfc4dec662a79152',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_candidate_phase_normal_stress_v001.py':'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_fixed_label_finite_sheet_geometry_v002.py':'556bac0713c74947b0abece865bf7e74c3d3b212029af1248aa7dd0af525a661'}
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def bind(name,checksum):
 assert checksum is not None and P.sha(P.path(name))==checksum,name
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==checksum;INPUTS[key]=checksum;return checksum
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));AVAILABLE[name]=a;return a
def pair_from(data,name):return data[name+'_hi'],data[name+'_lo']
def read(ref,names):return P.read_pair(P.resolve_record(ref),tuple(names))
def arrays(values):return {n:np.asarray(x).copy() for n,x in values.items()}
def thin(ref):return {n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')}
def put_pair(data,name,value):
 for word,w in zip(('hi','lo'),value):data[name+'_'+word]=keep(name+'_'+word,w)
 return value
def capture_families(prefix,values):
 for n,x in values.items():
  if isinstance(x,dict):capture_families(prefix+n+'_',x)
  elif isinstance(x,tuple) and len(x)==2 and all(isinstance(w,np.ndarray) for w in x):put_pair(AVAILABLE,prefix+n,x)
  elif isinstance(x,tuple) and len(x)==2 and all(isinstance(w,tuple) for w in x):capture_families(prefix+n+'_',dict(value=x[0],delta=x[1]))
  elif isinstance(x,np.ndarray):keep(prefix+n,x)
def clear_current():
 RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear();CONTEXT.clear()

def initialize_io():
 global P,SCOPE
 file=list(PINS)[1];tree=ast.parse((BASE/file).read_text());wanted={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted];assert len(defs)==13
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),SCOPE);P=types.SimpleNamespace(**{n:SCOPE[n] for n in wanted},INPUTS=INPUTS)

def initialize_arithmetic():
 global np,P,N
 import numpy as numpy
 np=numpy;SCOPE['np']=np;names=list(PINS);trees=[ast.parse((BASE/f).read_text()) for f in names[:3]];maps=[{n.name:n for n in t.body if isinstance(n,ast.FunctionDef)} for t in trees]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','paired_current_affine_features','paired_current_affine_momenta','native_mask','metric_mask','dd_native_scatter','dd_metric_F','dd_metric_scatter'}
 scalar={'a_reshape','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter'}
 for n in base:assert ast.dump(maps[0][n],include_attributes=False)==ast.dump(maps[1][n],include_attributes=False),n
 defs=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base|scalar]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(defs)==31
 SCOPE.update(capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 exec(compile(ast.Module(body=defs,type_ignores=[]),names[1],'exec'),SCOPE)
 for n in base|primitive|scalar|{'B','GC','ALPHA','ELL','C'}:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|scalar|{'B','GC','ALPHA','ELL','C'}})
 normal={'normal_test_mask','extend_normal_tests','restrict_normal_rows','normal_hat_jet','normal_hat_operation_envelope','scatter_normal_envelope','paired_restrict_normal_rows','paired_scatter_normal'}
 normal_scope=dict(SCOPE);defs=[n for n in trees[2].body if isinstance(n,ast.FunctionDef) and n.name in normal];assert len(defs)==8;exec(compile(ast.Module(body=defs,type_ignores=[]),names[2],'exec'),normal_scope);N=types.SimpleNamespace(**{n:normal_scope[n] for n in normal})
 for file,count in zip(names[3:],(11,20,8,7,5,8,3,1,1,2)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count,file;exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())

def compact_direction(basis,iq,h,h_spatial):
 # Genuine true-conformal reference tangent, not the registered additive-a contact.
 chi=np.zeros(3784);grad=np.zeros((3784,2));node=(43,22)
 for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  take=(basis['cell_i']+di==node[0])&(basis['cell_j']+dj==node[1])
  for jet in range(3):
   value=basis['hats'][iq,corner,jet].reshape(3784)
   if jet==0:chi[take]+=value[take]
   else:grad[take,jet-1]+=value[take]
 keep('predeclared_true_conformal_chi',chi);keep('predeclared_true_conformal_gradient',grad)
 dh=P.a_mul64(4*chi[:,None,None],h);dhs=P.a_add(P.a_mul64(4*chi[:,None,None,None],h_spatial),P.a_mul64(4*grad[:,:,None,None],(h[0][:,None],h[1][:,None])))
 return dict(h=dh,h_spatial_jets=dhs,h_dot=P.a_dd(np.zeros((3784,3,3))),u_jets=P.a_dd(np.zeros((3784,4,3))),z_jets=P.a_dd(np.zeros((32,3784,4,3)))),chi,grad

def finite0_inputs(refs,iq,basis,rate_words):
 p=3784;pilot=refs['pilots'][iq];names=tuple(n for n in pilot['metadata']['schema'] if n.startswith('config_') or n in ('chart_h','chart_ih','chart_sqrt_h','chart_N','chart_beta','chart_u','chart_up','chart_gamma','chart_dens','seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot') or n.startswith('first_jet_'))
 old=read(pilot,names);s={n.removeprefix('config_'):v for n,v in old.items() if n.startswith('config_')};c={n.removeprefix('chart_'):v for n,v in old.items() if n.startswith('chart_')}
 force=read(refs['forces'][iq],('seed_chart_derivative_dN','seed_chart_derivative_dbeta','seed_chart_derivative_dh','seed_chart_derivative_du_cov','seed_dz'))
 sl=slice(iq*p,(iq+1)*p);y=tuple(rate_words['native_jet_value_'+word][:,sl].copy() for word in ('hi','lo'));k=tuple(rate_words['metric_jet_value_'+word][sl].copy() for word in ('hi','lo'))
 ht=P.a_dd(np.zeros((p,3,3)))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for word in (0,1):ht[word][:,i,j]=ht[word][:,j,i]=k[word][:,a]
 Na=P.a_dd(force['seed_chart_derivative_dN']);ba=P.a_dd(force['seed_chart_derivative_dbeta']);ua=P.a_dd(force['seed_chart_derivative_du_cov']);za=P.a_dd(force['seed_dz'][:,:,:,1:])
 Na[0][:,0]=old['seed_owned_coordinate_Ndot'];Na[1][:,0]=0.;ba[0][:,0]=old['seed_owned_coordinate_betadot'];ba[1][:,0]=0.
 for word in (0,1):ua[word][:,0]=y[word][0];za[word][:,:,0]=y[word][1:]
 geometry=dict(h=P.a_dd(c['h']),ih=P.a_dd(c['ih']),mu=P.a_dd(c['sqrt_h']),h_spatial_jets=P.a_dd(force['seed_chart_derivative_dh'][:,1:3]))
 gauge=dict(N=P.a_dd(c['N']),beta=P.a_dd(c['beta']),N_jets=Na,beta_jets=ba);covectors=dict(u=P.a_dd(c['u']),z=P.a_dd(s['z'][:,:,1:]),u_jets=ua,z_jets=za);mechanical=dict(h_dot=ht);phase=dict(phi=P.a_dd(s['phi']))
 jets={n:pair_from(old,'first_jet_'+n) for n in ('du','dz','dg','Ga')};g=P.a_dd(s['g']);compatibility=[]
 for a in range(4):
  G=P.a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)));reaction=P.a_add(fy_mm(P.a_transpose(G,(0,2,1)),g),fy_mm(g,G));compatibility.append(P.a_sub(P.a_slice(jets['dg'],(slice(None),a)),reaction));put_pair(AVAILABLE,'current_owned_E0',P.a_stack(compatibility,1))
 E0=P.a_stack(compatibility,1);reference=dict(E0=E0,canonical_targets=refs['canonical_columns'][iq],prior_bridge_references=refs['prior_readout'],**{n:P.a_dd(s[n]) for n in ('g','hi','U','z')},**jets)
 value=dict(**{n:P.a_dd(s[n]) for n in ('g','hi','U','z','uc','P')},**{n:P.a_dd(c[n]) for n in ('up','gamma','dens')},**jets);model=dict(value=value,delta={})
 material=dict(omega=s['omega'],xi=s['xi'],w=s['w'],B=P.B,GC=P.GC,ALPHA=P.ALPHA,ELL=P.ELL,C=P.C,R=s['R'],Z_coordinate=s['Z_coordinate'])
 assert np.array_equal(material['R'],basis['R'][iq])
 direction,chi,grad=compact_direction(basis,iq,geometry['h'],geometry['h_spatial_jets']);capture_families('NEW_reference_input_',dict(geometry=geometry,gauge=gauge,covectors=covectors,mechanical=mechanical,phase=phase,material=material,reference=reference,direction=direction))
 return (geometry,model,gauge,covectors,mechanical,phase,material,reference),direction

def mean_labels(refs,iq,R,directions,weights):
 raw=read(refs['mean_columns'][iq],('reference_coordinate_dust_density','reference_radiation_energy_measure'));p=len(R);ray=np.broadcast_to(directions[:,None,:],(64,p,3)).copy();ray[:,:,2]*=R[None]
 # Same registered128 full rule: explicit fixed antipodes for49 momentum rows.
 ray=np.concatenate((ray,-ray),0);w=.5*np.concatenate((weights,weights))[:,None]*raw['reference_radiation_energy_measure'][None]
 labels=dict(galaxy_mass_weight=P.a_dd(np.zeros(p)),galaxy_specific_covector=P.a_dd(np.zeros((p,3))),reference_dust_energy_weight=P.a_dd(raw['reference_coordinate_dust_density']),radiation_weights=P.a_dd(w),radiation_covectors=P.a_dd(ray),existing_once_counted_branch_registered=True,provenance=dict(reference=refs['mean_columns'][iq],same_registered_antipodal_rule=True,candidate_volume_or_radial_rescale=False))
 capture_families('unchanged_mean_labels_',labels);return labels

def candidate_column(refs,iq,basis,rate_words,directions,weights,Hbar,constants):
 clear_current();CONTEXT.update(stage='NEW_candidate_column',column=iq);inputs,direction=finite0_inputs(refs,iq,basis,rate_words)
 candidate=finite_candidate_raw_action_adapter(*inputs,P.paired_current_affine_features,P.paired_current_affine_momenta,keep,'candidate_raw');capture_families('completed_candidate_',dict(s=candidate['s'],c=candidate['c'],jets=candidate['jets'],features=candidate['features']['paired'],momenta=candidate['momenta'],KADM=candidate['KADM']))
 contact=finite_candidate_configuration_contact(candidate,inputs[0],inputs[2],inputs[3],inputs[4],direction,inputs[7],keep,'candidate_contact');capture_families('completed_contact_',contact)
 curvature=finite_candidate_intrinsic_curvature(candidate,contact,keep,'candidate_curvature');capture_families('completed_curvature_',curvature)
 s={n:P.a_dd(candidate['s'][n]) for n in ('g','hi','U','uc','P','phi')};c={n:P.a_dd(candidate['c'][n]) for n in ('N','beta','h','ih','u')};c['mu']=P.a_dd(candidate['c']['sqrt_h']);D={**contact['d'],**contact['dc']};D['mu']=contact['dc']['sqrt_h']
 eos=candidate_invariant_phase_eos_current(s,c,D,constants,keep,'candidate_phase');capture_families('completed_phase_',eos)
 ordinary=finite_fixed_canonical_ordinary_point(dict(h=c['h'],ih=c['ih'],delta_h=D['h'],delta_ih=D['ih']),dict(N=c['N'],beta=c['beta']),mean_labels(refs,iq,basis['R'][iq],directions,weights),keep,'candidate_mean');capture_families('completed_mean_',ordinary)
 state_ref=P.checkpoint('STATE',arrays(AVAILABLE),dict(kind='NEW_candidate_completed_configuration_features_momenta_EOS_and_mean',column=iq,pilot_reference=thin(refs['pilots'][iq]),owned_spatial_reference=thin(refs['forces'][iq]),current_time_words=thin(refs['current_jets']),new_candidate_coefficients_and_EOS_evaluated=True,all_configuration_inverse_E0_and_chart_gaps_retained=True,physical_adoption=False))
 coeff={family:P.a_dd(np.zeros((3784,4,4))) for family in ('value','delta')};theta={};point_outputs={};test_refs=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   clear_current();CONTEXT.update(stage='NEW_candidate_normal_test',column=iq,row=row,jet=jet,state=thin(state_ref),completed_test_refs=list(test_refs))
   f=np.zeros(3784);df=np.zeros((3784,4));b=np.zeros((3784,3));db=np.zeros((3784,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   label='row%d_jet%d'%(row,jet);native=finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,Hbar,inputs[7],keep,label+'_native_EH');capture_families('completed_'+label+'_native_EH_',native)
   phase=candidate_phase_normal_stress(s,c,D,eos,f,b,keep,label+'_phase') if coordinate is None else dict(value={n:P.a_dd(np.zeros(3784)) for n in ('action','absolute','relative')},delta={n:P.a_dd(np.zeros(3784)) for n in ('action','absolute','relative')},relative_phase_included_once=True)
   # Phase and ordinary action have no test-firstjet coefficient; their value
   # calls are skipped for jet directions by the exact declared local action.
   own=ordinary if coordinate is None else dict(value=dict(normal_density=P.a_dd(np.zeros((3784,4)))),delta=dict(normal_density=P.a_dd(np.zeros((3784,4)))))
   total=finite_candidate_total_normal(native,phase,own,f,b,keep,label+'_total');capture_families('completed_'+label+'_total_',total)
   for family in ('value','delta'):
    for word in (0,1):coeff[family][word][:,row,jet]=total[family]['hamiltonian'][word]
    theta[family]=native[family]['initial_CMC_density'];put_pair(point_outputs,family+'_current_Hamiltonian_coefficients',coeff[family])
   test_ref=P.checkpoint('NORMAL_TEST',arrays(AVAILABLE),dict(kind='NEW_completed_normal_test_and_primary_comparison_contacts',column=iq,row=row,jet=jet,normal_coordinate_order=['value','R','Z','t'],candidate_state=thin(state_ref),relative_phase_count=1,ordinary_mean_count=1,physical_ports_admitted=False,physical_adoption=False));test_refs.append(thin(test_ref))
 clear_current();CONTEXT.update(stage='NEW_candidate_column_publication',column=iq,state=thin(state_ref),completed_test_refs=list(test_refs))
 for family in ('value','delta'):put_pair(point_outputs,family+'_normal_coefficients',coeff[family]);put_pair(point_outputs,family+'_initial_CMC_density',theta[family]);put_pair(point_outputs,family+'_phase_density',eos[family]['p'])
 for n,x in candidate['momenta'].items():put_pair(point_outputs,'NEW_current_momentum_'+n,x)
 for n,x in contact['delta_momenta'].items():put_pair(point_outputs,'NEW_delta_momentum_'+n,x)
 data=arrays({**AVAILABLE,**point_outputs});record=P.checkpoint('COLUMN',data,dict(kind='NEW_finite0_candidate_coefficients_current_and_normal_rows',column=iq,candidate_state=thin(state_ref),normal_test_refs=test_refs,pilot_reference=thin(refs['pilots'][iq]),owned_spatial_reference=thin(refs['forces'][iq]),current_time_words=thin(refs['current_jets']),geometry_reference_rho=0.,direction='true_conformal_scalar_hat43_22_at_reference_mechanical_rates_fixed',phase_charge_direction_restored=False,normal_coordinate_order=['value','R','Z','t'],all_primary_comparison_gaps_retained=True,relative_phase_count=1,ordinary_mean_count=1,old_coefficients_features_momenta_or_normals_reused=False,original_target_or_epsilon_refitted=False,physical_adoption=False));clear_current()
 compact=dict(value=dict(normal_coefficients=coeff['value'],initial_CMC_density=theta['value']),delta=dict(normal_coefficients=coeff['delta'],initial_CMC_density=theta['delta']),normal_coordinate_order=('value','R','Z','t'),relative_phase_count=1,ordinary_label_count=1)
 return compact,record,dict(value=dict(native=candidate['momenta']['native_density'],metric=candidate['momenta']['metric_total_density'],phase=eos['value']['p']),delta=dict(native=contact['delta_momenta']['native_density'],metric=contact['delta_momenta']['metric_total_density'],phase=eos['delta']['p']))

def sheet_rows(refs,basis,normal_test):
 clear_current();CONTEXT.update(stage='NEW_fixed_label_sheet');names=('g','R','Z','mass_weight','right_weight','specific_covariant_p','indices');raw=read(refs['ordinary_loads'],('ordinary_input_source_'+n for n in names));src={n:raw['ordinary_input_source_'+n] for n in names};rho=P.a_dd(np.zeros((87,45)));drho=P.a_dd(np.zeros((87,45)));drho[0][43,22]=1.
 sheet=fixed_label_finite_sheet_geometry(src['g'],src['R'],src['Z'],basis['r'],src['indices'],src['right_weight'],rho,drho,keep,'fixed_label_sheet');capture_families('completed_sheet_geometry_',sheet)
 keep('predeclared_sheet_polynomial_test',normal_test);n=len(src['R']);labels=dict(galaxy_mass_weight=P.a_dd(src['mass_weight']),galaxy_specific_covector=P.a_dd(src['specific_covariant_p']),reference_dust_energy_weight=P.a_dd(np.zeros(n)),radiation_weights=P.a_dd(np.zeros((0,n))),radiation_covectors=P.a_dd(np.zeros((0,n,3))),existing_once_counted_branch_registered=True,provenance=refs['ordinary_loads'])
 ordinary=finite_fixed_canonical_ordinary_point(sheet['geometry'],sheet['gauge'],labels,keep,'fixed_label_ordinary');capture_families('completed_sheet_ordinary_',ordinary);result={}
 for family in ('value','delta'):
  force=ordinary[family]['normal_density'];out=P.a_dd(np.zeros((4,87,45)));env=np.zeros((4,87,45));test_value=np.zeros((n,4))
  if family=='delta':assert all(np.array_equal(w,np.zeros_like(w)) for w in force),'Declared off-sheet compact direction must leave every fixed-label force word zero'
  for side,hat in ((0,1-src['right_weight']),(1,src['right_weight'])):
   for row in range(4):
    scale=src['R'] if row==1 else np.ones(n);val=P.a_mul64(hat,P.a_mul64(scale,P.a_slice(force,(slice(None),row))));fy_keep('sheet_current_force',val,keep);ev=abs(hat*scale)*(abs(force[0][:,row])+abs(force[1][:,row]));test_value[:,row]+=hat*scale*normal_test[row,src['indices']+side,0]
    for node in range(87):
     take=np.flatnonzero(src['indices']+side==node)
     if len(take):
      subtotal=normal_pair_sum((val[0][take],val[1][take]),0);joined=P.a_add(P.a_slice(out,(row,node,0)),subtotal)
      for word in (0,1):out[word][row,node,0]=joined[word]
      env[row,node,0]+=np.sum(ev[take]);fy_keep('sheet_current_nodal',out,keep)
  out=N.paired_restrict_normal_rows(out);env=N.restrict_normal_rows(env);nodal=fy_sum(fy_sum(fy_sum(P.a_mul64(normal_test,out),2),1),0);direct=fy_sum(fy_sum(P.a_mul64(test_value,force),1),0);bound=np.asarray(np.sum(abs(normal_test)*env)+np.sum(abs(test_value)*(abs(force[0])+abs(force[1]))))
  if family=='delta':assert all(np.array_equal(w,np.zeros_like(w)) for w in out),'Declared off-sheet compact direction must leave all sheet nodal words zero'
  for name,x in (('weak_normal',out),('functional_nodal',nodal),('functional_direct',direct),('functional_gap',P.a_sub(nodal,direct))):put_pair(AVAILABLE,'sheet_'+family+'_'+name,x)
  keep('sheet_'+family+'_functional_envelope',bound);P.check('sheet_'+family+'_polynomial_transpose',np.asarray(nodal[0]+nodal[1]).copy(),np.asarray(direct[0]+direct[1]).copy(),bound)
  result[family]=out
 record=P.checkpoint('SHEET',arrays({**AVAILABLE,**{n:x for n,x in RAW.items() if n.startswith('control_')}}),dict(kind='NEW_same_position_fixed_canonical_sheet_geometry_energy_and_incidence',reference=thin(refs['ordinary_loads']),mapping_proof_retained=refs['ordinary_mapping_proof']['status'],labels_and_locations_unchanged=True,no_candidate_volume_or_budget_subtraction=True,finite_rho=0.,compact_direction_off_sheet=True,reference_lineage_admitted_by_helper=False,completed_controls=CHECKS[-2:],physical_adoption=False));return result,record

def canonical_functional_contact(kind,field,weak,test,basis,label):
 # Independent coefficient-polynomial contraction of the NEW point currents.
 # Positive corner bounds precede all cancellations. They certify the scatter
 # arithmetic, not upstream action accuracy or canonical target restoration.
 u=test.copy();shape=field[0].shape;polynomial=P.a_dd(np.zeros(shape));envelope=np.zeros(shape)
 if kind=='native':
  assert shape==(33,15136,3) and u.shape==(33,3,87,45) and np.all(u[:,~P.native_mask()]==0)
  u[:,0,0,:]=0.;u[:,1,0,:]=u[:,1,1,:];u[:,1,:,0]=0.;u[:,2,0,:]=u[:,2,1,:]
 elif kind=='metric':
  assert shape==(15136,6) and u.shape==(6,87,45) and np.all(u[~P.metric_mask()]==0)
  u[:,0,:]=u[:,1,:];u[3:5,:,0]=0.
 else:
  assert kind=='phase' and shape==(15136,) and u.shape==(87,45) and np.all(u[~P.scalar_mask()]==0);u[0]=u[1]
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);R=basis['R'][iq]
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0].reshape(3784)
   if kind=='native':
    local=u[:,:,di:86+di,dj:44+dj].reshape(33,3,3784).transpose(0,2,1);factor=np.ones((3784,3));factor[:,2]=R**2
    term=P.a_mul64(factor,P.a_prod(hat[:,None],local));key=(slice(None),sl);eb=abs(local)*abs(hat[:,None])*abs(factor)
   elif kind=='metric':
    a,b,c,d,e,f=u[:,di:86+di,dj:44+dj].reshape(6,3784)
    local=P.a_stack([P.a_add(P.a_dd(a),P.a_prod(R**2,b)),P.a_dd(f),P.a_prod(R**2,a),P.a_prod(R,d),P.a_prod(R**3,c),P.a_prod(R**2,e)],1)
    term=P.a_mul64(hat[:,None],local);key=sl;eb=abs(hat[:,None])*np.stack((abs(a)+abs(R**2*b),abs(f),abs(R**2*a),abs(R*d),abs(R**3*c),abs(R**2*e)),1)
   else:
    local=u[di:86+di,dj:44+dj].reshape(3784);term=P.a_prod(hat,local);key=sl;eb=abs(hat*local)
   update=P.a_add(P.a_slice(polynomial,key),term)
   for word in (0,1):polynomial[word][key]=update[word]
   envelope[key]+=eb;fy_keep(label+'_current_independent_test_polynomial',polynomial,keep);keep(label+'_current_test_operation_envelope',envelope)
 weight=(basis['dv']/basis['R']).reshape(15136);scale=weight[None,:,None] if kind=='native' else weight[:,None] if kind=='metric' else weight
 # Only predeclared coefficient-test support is reduced; identically zero
 # multipliers outside this support cannot contribute to the polynomial.
 nodal_terms=P.a_mul64(test,weak);direct_terms=P.a_mul64(scale,P.a_mul(polynomial,field));nodal_support=test!=0;point_support=envelope>0
 nodal=fy_sum((nodal_terms[0][nodal_support],nodal_terms[1][nodal_support]),0);direct=fy_sum((direct_terms[0][point_support],direct_terms[1][point_support]),0);gap=P.a_sub(nodal,direct)
 bound=np.asarray(np.sum(abs(test)*(abs(weak[0])+abs(weak[1])))+np.sum(scale*envelope*(abs(field[0])+abs(field[1])))).copy()
 for n,x in (('nodal',nodal),('direct',direct),('gap',gap)):put_pair(AVAILABLE,label+'_'+n,x)
 keep(label+'_operation_envelope',bound);P.check(label,np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),bound)

def packet(refs):
 basis=read(refs['basis'],('R','dv','hats','cell_i','cell_j','r','z'));rate=read(refs['current_jets'],('native_jet_value_hi','native_jet_value_lo','metric_jet_value_hi','metric_jet_value_lo'));mean=read(refs['mean_input'],('fine_reference_directions','fine_reference_weights'));assert np.all(mean['fine_reference_weights']>0)
 Hbar=refs['owned_background']['h']*refs['fixed']['Hunit']/299792458.;assert math.isfinite(Hbar) and Hbar>0;constants=candidate_phase_registered_constants(refs['fixed']);nt=np.zeros((4,87,45));nt[:,43,22]=(1.,2.,3.,4.);st=np.zeros((87,45));st[43,22]=1.;native_test=np.zeros((33,3,87,45));native_test[0,0,43,22]=1.;native_test[1,1,43,22]=2.;native_test[2,2,43,22]=3.;metric_test=np.zeros((6,87,45));metric_test[:,43,22]=np.arange(1.,7.)
 P.checkpoint('INPUT',arrays(rate),dict(kind='owned_current_mechanical_time_words_reference_finite_candidate',refs=refs,fixed=refs['fixed'],owned_background=refs['owned_background'],rho=0.,compact_direction_node=[43,22],inherited_primitive_nonadmission=True,physical_adoption=False));P.checkpoint('BASIS',arrays(basis),dict(kind='unchanged_registered_E_F_normal_scalar_basis',reference=refs['basis'],old_operator_or_action_replayed=False));columns=[];records=[];moments=[]
 for iq in range(4):
  q,record,m=candidate_column(refs,iq,basis,rate,mean['fine_reference_directions'],mean['fine_reference_weights'],Hbar,constants);columns.append(q);records.append(record);moments.append(m)
 sheet_test=np.zeros((4,87,45));sheet_test[:,43,0]=(1.,2.,0.,4.);sheet,sheet_ref=sheet_rows(refs,basis,sheet_test);clear_current();CONTEXT.update(stage='NEW_global_current_normal_CMC_residual');global_rows=finite_candidate_global_normal_CMC(columns,basis,nt,st,keep,P.check,'candidate_global');prior=read(refs['prior_readout'],('native_original_target','metric_original_target')+tuple(family+'_'+n+'_'+word for family in ('native','metric') for n in ('frozen_rhs_defect','primitive_minus_earned_bridge','actual_target_residual') for word in ('hi','lo')));phase_prior=read(refs['phase_loads'],tuple(n+'_'+word for n in ('fixed_literal_weak_phase_charge','registered_weak_phase_charge','owned_registered_weak_phase_charge','literal_minus_registered_weak_gap','registered_minus_owned_weak_gap') for word in ('hi','lo')));data={};norms={}
 for family in ('value','delta'):
  native=P.a_stack([m[family]['native'] for m in moments],0);native=(native[0].reshape(15136,33,3).transpose(1,0,2),native[1].reshape(15136,33,3).transpose(1,0,2));metric=(np.concatenate([m[family]['metric'][0] for m in moments]),np.concatenate([m[family]['metric'][1] for m in moments]));phase=(np.concatenate([m[family]['phase'][0] for m in moments]),np.concatenate([m[family]['phase'][1] for m in moments]))
  nweak=P.dd_native_scatter(native,basis,keep);mweak=P.dd_metric_scatter(metric,basis,keep);pweak=P.dd_scalar_scatter(phase,basis,keep,'candidate_'+family+'_phase_charge');normal=P.a_add(global_rows[family]['weak_normal'],sheet[family]);trace=global_rows[family]['weak_initial_CMC']
  for n,x in (('native_current',nweak),('metric_current',mweak),('literal_phase_current',pweak),('total_weak_normal',normal),('initial_weak_CMC',trace)):put_pair(data,family+'_'+n,x)
  for kind,point,weak,test in (('native',native,nweak,native_test),('metric',metric,mweak,metric_test),('phase',phase,pweak,st)):canonical_functional_contact(kind,point,weak,test,basis,'candidate_'+family+'_'+kind+'_current_polynomial_transpose')
  if family=='value':
   target_norms={}
   for n,x,target in (('native',nweak,P.a_dd(prior['native_original_target'])),('metric',mweak,P.a_dd(prior['metric_original_target'])),('phase',pweak,pair_from(phase_prior,'fixed_literal_weak_phase_charge'))):
    residual=put_pair(data,'actual_'+n+'_canonical_target_residual',P.a_sub(x,target));target_norms[n]=float(np.linalg.norm(residual[0]+residual[1]))
   norms['actual_canonical_target_residuals_L2']=target_norms
  norms[family]=dict(normal_L2=[float(np.linalg.norm((normal[0]+normal[1])[row])) for row in range(4)],initial_CMC_L2=float(np.linalg.norm(trace[0]+trace[1])),native_current_L2=float(np.linalg.norm(nweak[0]+nweak[1])),metric_current_L2=float(np.linalg.norm(mweak[0]+mweak[1])),literal_phase_current_L2=float(np.linalg.norm(pweak[0]+pweak[1])))
 capture_families('prior_signed_bridge_',prior);capture_families('prior_phase_current_',phase_prior);data.update(arrays(AVAILABLE));data.update(arrays({n:x for n,x in RAW.items() if n.startswith('control_')}));loads=P.checkpoint('LOADS',arrays(data),dict(kind='NEW_candidate_current_and_full_normal_initial_CMC_measurement',columns=[thin(q) for q in records],sheet=thin(sheet_ref),norms=norms,completed_controls=CHECKS[2:],original_native_metric_and_literal_weak_phase_targets_unchanged=True,inherited_frozen_primitive_epsilon_and_phase_registration_gaps_retained=True,compact_direction_is_unqualified_charge_and_canonical_partial=True,relative_phase_count=1,ordinary_sheet_and_reference_mean_counted_once=True,no_offset_gain_or_source_refit=True,physical_ports=None,physical_adoption=False))
 assert len(RECORDS)==76 and len(CHECKS)==12 and all(x['passed'] for x in CHECKS)
 return dict(status='FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED',columns=records,sheet=sheet_ref,loads=loads,norms=norms,finite_configuration_rho=0.,direction_node=[43,22],original_native_metric_and_phase_targets_retained=True,primitive_bridge_resolved=False,physical_normal_CMC_or_charge_solved=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(x is not None for x in (CONTROL_PROOF,MIXED_CONTROL_PROOF,SHEET_CONTROL_PROOF)),'Root reviewed release and earned fresh component controls required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER'])
  for n,h in tuple(PINS.items())+((ADMISSION_FILE,ADMISSION_SHA),(DRIVER_PROTOCOL,PROTOCOL_SHA)):bind(n,h)
  for name,h,status in (CONTROL_PROOF,MIXED_CONTROL_PROOF,SHEET_CONTROL_PROOF):bind(name,h);proof=json.loads(P.path(name).read_text());assert proof['status']==status,name
  tree=ast.parse((BASE/ADMISSION_FILE).read_text());defs=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.Assign))];globals().update(path=P.path);exec(compile(ast.Module(body=defs,type_ignores=[]),ADMISSION_FILE,'exec'),globals());pins,refs=finite0_reference_admission();assert pins==INPUTS
  INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256'];P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,scope='NEW finite0 reference candidate coefficients action currents four normals initial CMC and true-conformal compact partial',component_control_proofs=[CONTROL_PROOF,MIXED_CONTROL_PROOF,SHEET_CONTROL_PROOF],qualification=FLAGS));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   available={**AVAILABLE,**RAW,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if available:
    try:P.checkpoint('ERROR_RAW',arrays(available),dict(context=dict(CONTEXT),kind='available_new_finite_candidate_operands'),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
