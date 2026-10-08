"""Guarded new compact configuration + global rate + phase normal derivative."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMBINED_CONFIGURATION_NORMAL_DERIVATIVE_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='4d49c10d595c2642d41d4fb7a8bb3a833660b86b911a81756a5b575f9e02718a'
PROVIDERS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18','cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40','cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19'}
FRAGMENTS={'author_fragment_combined_normal_derivative_admission_v003.txt':'e1ab622f6453569f655380d8b548628a54c54a35b7bfd49496b8cc5be65f480f','author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd','author_fragment_differentiated_normal_test_lift_v001.py':'9a30c1a6ba93efd0a04107ab92456f946028b6f97418fe1ac16c1599acf5fed8','author_fragment_combined_normal_stress_contact_v001.py':'e44f1ebba987c2567b7a95afacaee5f867384c9b0574bb5dbe78b9544aea4b22','author_fragment_combined_normal_curvature_contact_v002.py':'897de8d1a49316c73a1d0b3f38652a228393497219b9f211611116400dc739de','author_fragment_combined_normal_contact_controls_v001.py':'f88ba07f907e769350a98b74a313fa7809f450686083ebd18735c43cd8697e6a'}
P=N=A=np=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())

def pair(n,x):normal_keep_pair(n,x,keep);return x

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def initialize():
 global P,N,A,np,ORIGINAL_CAPTURE,C,ALPHA,ELL,B,GC
 modules=[]
 for n,h in PROVIDERS.items():
  assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
  spec=importlib.util.spec_from_file_location('combined_'+n.removesuffix('.py'),BASE/n);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);modules.append(m)
 P,N,A=modules
 import numpy as numpy_module
 np=numpy_module;P.np=N.np=A.np=np;ORIGINAL_CAPTURE=P.capture;P.capture=keep
 C,ALPHA,ELL,GC=N.C,N.ALPHA,N.ELL,N.GC;B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2;N.B=A.B=B
 P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(physical_configuration_prepared=False,finite_phase_charge_restored=False,normal_constraints_qualified=False,primitive_legendre_bridge_resolved=False,physical_exterior_adopted=False,evolution_qualified=False,galaxy_velocity_qualified=False)
 for n in ('RAW','AVAILABLE','DD_ARRAY_CURRENT','INPUTS','CONTEXT'):setattr(N,n,getattr(P,n));setattr(A,n,getattr(P,n))
 N.capture=A.capture=keep
 for n in ('a_dd','a_add','a_sub','a_mul','a_mul64','a_prod','a_matvec','a_stack','a_slice','a_transpose','a_reshape','a_div64'):
  globals()[n]=getattr(P,n);setattr(N,n,getattr(P,n));setattr(A,n,getattr(P,n))
 for n in ('normal_keep_pair','normal_pair_sum','normal_action_dot','normal_action_reduce','paired_normal_chart_jets','paired_normal_lift','paired_normal_metric_delta','normal_test_mask','evaluate_normal_test','scatter_normal_envelope','paired_scatter_normal'):globals()[n]=getattr(N,n)
 globals().update(path=P.path,INPUTS=P.INPUTS)
 for n,h in {**PROVIDERS,**FRAGMENTS,STEM+'.md':PROTOCOL_SHA,__file__:P.sha(__file__)}.items():bind(n,h)
 for n in FRAGMENTS:exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def scratch(stage,preserved=None,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)
 if preserved:P.AVAILABLE.update(preserved)

def emit_pair(data,n,x):
 pair(n,x);data[n+'_hi']=x[0].copy();data[n+'_lo']=x[1].copy()

def take_point_fields(s,c,jets,feature,moments,op,take):
 mode_s={'z','z2','f','dz'};mode_c={'JzU','zh'};mode_f={'nz','q','V','D','V_raised','D_raised','Pi','dz'};constants={'omega','xi','w'}
 ss={n:(v if n in constants else np.take(v,take,axis=1 if n in mode_s else 0)) for n,v in s.items()}
 cc={n:np.take(v,take,axis=1 if n in mode_c else 0) for n,v in c.items()}
 def pp(x,mode):return {n:(np.take(v[0],take,axis=1 if n in mode else 0),np.take(v[1],take,axis=1 if n in mode else 0)) for n,v in x.items()}
 return ss,cc,pp(jets,{'dz'}),dict(paired=pp(feature['paired'],mode_f)),pp(moments,set()),{n:np.take(v,take,axis=1 if n=='dz' else 0) for n,v in op.items()}

def read_contact(ref):
 names=tuple(n for n in ref['metadata']['schema'] if n in ('indices','Q','Q_jet') or n.startswith(('delta_primitive_','delta_chart_','delta_feature_','delta_configuration_','delta_momentum_')))
 raw=P.read_pair(ref,names)
 def family(prefix):return {n[len(prefix):-3]:(raw[n],raw[n[:-3]+'_lo']) for n in names if n.startswith(prefix) and n.endswith('_hi')}
 return raw['indices'],raw['Q'],raw['Q_jet'],family('delta_primitive_'),family('delta_chart_'),dict(paired=family('delta_feature_'),configuration=family('delta_configuration_')),family('delta_momentum_')

def read_normal_base(ref,take=None):
 names=tuple(n for n in ref['metadata']['schema'] if n.startswith(('native_metric_terms_','mode_compensation_terms_','absolute_phase_terms_','curvature_')))
 raw=P.read_pair(ref,names)
 if take is not None:raw={n:np.take(v,take,axis=0) for n,v in raw.items()}
 terms={n:(raw[n+'_hi'],raw[n+'_lo']) for n in ('native_metric_terms','mode_compensation_terms','absolute_phase_terms')}
 curvature={n.removeprefix('curvature_'):v for n,v in raw.items() if n.startswith('curvature_')}
 return terms,curvature

def zero_configuration(s,c,jets,df):
 z=lambda a:a_dd(np.zeros_like(a));d={n:z(s[n]) for n in ('g','hi','U','z')};d.update(jets)
 dc={n:z(c[n]) for n in ('ih','dens','sqrt_h')};dc['log_dens']=a_dd(np.zeros(len(s['U'])))
 cfg={n:z(s[n]) for n in ('uc','P','r','z2')}
 return d,dc,dict(paired=df['paired'],configuration=cfg)

def direction_test(p,row,jet):
 axis=(None,1,2,0)[jet]
 f=np.zeros(p);dt=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
 if row==0:
  if axis is None:f[:]=1
  else:dt[:,axis]=1
 elif axis is None:b[:,row-1]=1
 else:db[:,axis,row-1]=1
 return f,dt,b,db

def derivative_direction(s,c,jets,feature,moments,base,d,dc,df,dm,dcurvature,row,jet,label):
 f,dt,b,db=direction_test(len(s['U']),row,jet)
 lift,test,dlift,dtest,cj,dcj=normal_contact_test_derivatives(s,c,jets,feature,d,dc,df,f,dt,b,db,keep,label+'_test')
 native=combined_normal_native_contact(s,feature,test,d,df,dtest,keep,label+'_native')
 mode=combined_normal_z0_contact(s,jets,feature,lift,d,df,dlift,keep,label+'_mode')
 phase=combined_normal_absolute_phase_contact(s,c,test,d,dc,dtest,keep,label+'_phase')
 EH=combined_normal_EH_contact(s,c,cj,moments,base['curvature'],d,dc,dcj,dm,dcurvature,f,dt,b,db,keep,label+'_EH')
 values={n:a_slice(base['terms'][n],(slice(None),row,jet,slice(None))) for n in base['terms']}
 out=combined_normal_density_contact(c,dc,values,native,mode,phase,EH,keep,label+'_density')
 names=('test_Gamma_construction_gap','raw_test_duc_construction_gap','raw_test_projector_construction_gap','raw_test_inverse_construction_gap')
 out['test_construction_gaps']={name:(P.AVAILABLE[label+'_test_'+name+'_hi'],P.AVAILABLE[label+'_test_'+name+'_lo']) for name in names}
 return out

def compact_curvature(s,c,jets,op,Q,Qa,d,dc,curvature,label):
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_base_chart');dcj=dict(dh=a_slice(d['dg'],(slice(None),slice(None),slice(1,None),slice(1,None))))
 eI=np.einsum('pij,pjk,pkl->pil',abs(c['ih']),abs(Q),abs(c['ih']))
 eQa=abs(Qa[:,1:]).copy();eQa[:,0,2,2]=abs(Qa[:,1,0,0])*s['R']**2+2*s['R']*abs(Q[:,0,0])
 eMu=.5*c['sqrt_h']*np.einsum('pij,pij->p',abs(c['ih']),abs(Q))
 env=dict(delta_ih=eI,dh=op['dg'][:,1:,1:,1:],delta_dh=eQa,delta_sqrt_h=eMu)
 return combined_curvature_contact(s,c,cj,curvature,dc,dcj,env,keep,label)

def column_packet(iq,admitted,y,k):
 scratch('new_combined_normal_column',column=iq);s,c,jets,F,moments,op,_=N.load_pilot_column(admitted['pilot_columns'][iq]);s['du']=jets['du'][0];s['dz']=jets['dz'][0]
 terms,curvature=read_normal_base(admitted['normal_base_columns'][iq]);base=dict(terms=terms,curvature=curvature)
 sl=slice(iq*3784,(iq+1)*3784);yy=a_reshape(a_transpose(a_slice(y,(slice(None),sl,slice(None))),(1,0,2)),(3784,99));kk=a_slice(k,(sl,slice(None)))
 rate_jets=A.paired_fixed_chart_velocity_increment(s,c,yy,kk,keep,'new_rate_firstjets');tangent_s=dict(s,Z=np.zeros_like(s['Z']))
 rate_feature=A.paired_current_affine_features(tangent_s,c,rate_jets,keep,'new_rate_feature');rate_moments=A.paired_current_affine_momenta(tangent_s,c,rate_feature,rate_jets,keep,'new_rate_moments')
 d,dc,df=zero_configuration(s,c,rate_jets,rate_feature);zero_curvature=dict(Q=a_dd(np.zeros(3784)),V=a_dd(np.zeros((3784,3))))
 rate=a_dd(np.zeros((3784,4,4)));config=a_dd(np.zeros((3784,4,4)));data={};preserved={}
 for family,values in (('new_rate_first_jet',rate_jets),('new_rate_feature',rate_feature['paired']),('new_rate_momentum',rate_moments)):
  for n,x in values.items():
   for word,suffix in enumerate(('hi','lo')):preserved[family+'_'+n+'_'+suffix]=x[word]
 preserved.update(completed_rate_normal_coefficients_hi=rate[0],completed_rate_normal_coefficients_lo=rate[1],completed_compact_normal_coefficients_hi=config[0],completed_compact_normal_coefficients_lo=config[1])
 for row in range(4):
  for jet in range(4):
   scratch('new_rate_normal_direction',preserved,column=iq,row=row,test_jet=jet);out=derivative_direction(s,c,jets,F,moments,base,d,dc,df,rate_moments,zero_curvature,row,jet,'rate_direction')
   for word in (0,1):rate[word][:,row,jet]=out['coefficient'][word]
   pair('completed_rate_normal_coefficients',rate);data['rate_direction_%d_%d_component_L2'% (row,jet)]=np.linalg.norm(out['component_densities'][0]+out['component_densities'][1],axis=0)
   keep('completed_rate_direction_component_L2',data['rate_direction_%d_%d_component_L2'%(row,jet)])
   for n,x in out['test_construction_gaps'].items():emit_pair(data,'rate_direction_%d_%d_%s'%(row,jet,n),x)
   preserved.update(data)
 take,Q,Qa,dq,dcq,dfq,dmq=read_contact(admitted['contact_columns'][iq]);ss,cc,jj,ff,mm,oo=take_point_fields(s,c,jets,F,moments,op,take)
 bt={n:(x[0][take],x[1][take]) for n,x in terms.items()};cur={n:v[take] for n,v in curvature.items()};compact_base=dict(terms=bt,curvature=cur)
 dcv=compact_curvature(ss,cc,jj,oo,Q,Qa,dq,dcq,cur,'new_compact_curvature')
 for n in ('Gamma3','Q','V'):emit_pair(data,'new_compact_curvature_contact_'+n,dcv[n])
 for n in ('envelope_Gamma3','envelope_Q','envelope_V'):data['new_compact_curvature_contact_'+n]=dcv[n].copy()
 name='new_compact_curvature_spatial_minus_4D_density_fraction_gap'
 for suffix in ('hi','lo'):data[name+'_'+suffix]=P.AVAILABLE[name+'_'+suffix].copy()
 preserved.update(data)
 for row in range(4):
  for jet in range(4):
   scratch('new_compact_normal_direction',preserved,column=iq,row=row,test_jet=jet);out=derivative_direction(ss,cc,jj,ff,mm,compact_base,dq,dcq,dfq,dmq,dcv,row,jet,'compact_direction')
   for word in (0,1):config[word][take,row,jet]=out['coefficient'][word]
   pair('completed_compact_normal_coefficients',config);data['compact_direction_%d_%d_component_L2'%(row,jet)]=np.linalg.norm(out['component_densities'][0]+out['component_densities'][1],axis=0)
   keep('completed_compact_direction_component_L2',data['compact_direction_%d_%d_component_L2'%(row,jet)])
   for n,x in out['test_construction_gaps'].items():emit_pair(data,'compact_direction_%d_%d_%s'%(row,jet,n),x)
   preserved.update(data)
 mean=P.read_pair(admitted['mean_base_columns'][iq],('radiation_contravariant_stress_density',));mean_contact=combined_mean_lapse_contact(a_dd(Q),mean['radiation_contravariant_stress_density'][take],keep,'once_counted_mean')
 m=a_dd(np.zeros((3784,4,4)));m[0][take,0,0]=mean_contact[0];m[1][take,0,0]=mean_contact[1]
 for name,x in (('configuration_action_coefficients',config),('rate_action_coefficients',rate),('mean_Hamiltonian_coefficients',m)):emit_pair(data,name,x)
 data['compact_point_indices']=take.copy();data['ordinary_sheet_contact']=np.zeros(4)
 for n,x in rate_jets.items():emit_pair(data,'new_rate_first_jet_'+n,x)
 for n,x in rate_feature['paired'].items():emit_pair(data,'new_rate_feature_'+n,x)
 for n,x in rate_moments.items():emit_pair(data,'new_rate_momentum_'+n,x)
 rec=P.checkpoint('COLUMN',data,dict(kind='new_same_action_combined_configuration_and_induced_rate_normal_derivative',column=iq,pilot_ref=thin(admitted['pilot_columns'][iq]),compact_ref=thin(admitted['contact_columns'][iq]),base_normal_ref=thin(admitted['normal_base_columns'][iq]),once_counted_mean_ref=thin(admitted['mean_base_columns'][iq]),config_and_rate_parts_kept_separate=True,ordinary_sheet_contact_zero_offsheet=True,temporal_primary_contacts_retained=True,physical_ports=None,physical_adoption=False))
 return config,rate,m,rec

def read_earned_phase_rows(ref,names):
 # The saved closure authenticated the large publication. Only six final words
 # are read; no scalar-prefix schema/payload sweep or metadata replay occurs.
 assert P.sha(P.path(ref['file']))==ref['sha256'] and P.sha(P.path(ref['commit_file']))==ref['commit_sha256']
 out={}
 with np.load(P.path(ref['file']),allow_pickle=False) as z:
  for n in names:
   x=z[n].copy();schema=ref['metadata']['schema'][n];assert list(x.shape)==schema['shape'] and str(x.dtype)==schema['dtype'] and schema['finite'] is True and np.all(np.isfinite(x));out[n]=x;keep('copied_'+n,x)
 return out

def combined_packet(admitted):
 scratch('copy_earned_nodal_response_and_fixed_basis');geo=P.read_pair(admitted['basis'],('R','dv','hats','cell_i','cell_j','r','z'));response=P.read_pair(admitted['warm_response'],('native_rate_response_hi','native_rate_response_lo','metric_rate_response_hi','metric_rate_response_lo'))
 assert geo['R'].shape==geo['dv'].shape==(4,3784) and geo['hats'].shape==(4,4,3,86,44)
 nodes={n:(response[n+'_rate_response_hi'],response[n+'_rate_response_lo']) for n in ('native','metric')}
 y=P.dd_native_node_value(nodes['native'],geo,keep);k=P.dd_metric_node_value(nodes['metric'],geo,keep)
 data=dict(geo)
 for n,x in (('new_native_response_values',y),('new_metric_response_values',k)):emit_pair(data,n,x)
 inp=P.checkpoint('INPUT',data,dict(kind='new_value_evaluation_of_earned_warm_nodal_response',admitted_refs={n:[thin(q) for q in v] if isinstance(v,list) else thin(v) for n,v in admitted.items() if n in ('contact_columns','pilot_columns','normal_base_columns','mean_base_columns','basis','warm_response','warm_readout','phase_normal_loads')},fixed=admitted['fixed'],owned_background=admitted['owned_background'],finite_configuration_adopted=False,primitive_bridge_resolved=False))
 scratch('new_independent_derivative_controls');fixture=fresh_combined_normal_contact_controls();fr=P.checkpoint('FIXTURE',{**P.AVAILABLE,**P.RAW},dict(fixture,controls=P.CHECKS.copy()))
 columns=[];refs=[]
 for iq in range(4):
  q,v,m,rec=column_packet(iq,admitted,y,k);columns.append((q,v,m));refs.append(rec)
 scratch('new_combined_weak_normal_derivative');fields={};coefs={};rows={}
 for part,index in (('configuration',0),('rate',1),('mean',2)):
  coefficients=tuple(np.concatenate([x[index][word] for x in columns],axis=0) for word in (0,1));coefs[part]=coefficients
  point=a_slice(coefficients,(slice(None),slice(None),slice(1,None)));val=a_dd(np.zeros((15136,4,3)))
  for word in (0,1):val[word][:,:,0]=coefficients[word][:,:,0];val[word][:,:,1:]=point[word][:,:,:2]
  action=paired_scatter_normal(val,geo,part+'_new_action');rows[part]=action if part=='mean' else (-action[0],-action[1]);emit_pair(fields,part+'_weak_Hamiltonian_contact',rows[part])
 phase=read_earned_phase_rows(admitted['phase_normal_loads'],('registered_normal_weak_Hamiltonian_rows_hi','registered_normal_weak_Hamiltonian_rows_lo','literal_action_weak_Hamiltonian_rows_hi','literal_action_weak_Hamiltonian_rows_lo','literal_minus_registered_weak_normal_gap_hi','literal_minus_registered_weak_normal_gap_lo'))
 phase_rows=(phase['registered_normal_weak_Hamiltonian_rows_hi'],phase['registered_normal_weak_Hamiltonian_rows_lo']);emit_pair(fields,'earned_phase_registered_weak_Hamiltonian_contact',phase_rows)
 combined=a_add(a_add(rows['configuration'],rows['rate']),a_add(rows['mean'],phase_rows));emit_pair(fields,'combined_weak_Hamiltonian_contact',combined)
 for n,a in phase.items():fields['copied_'+n]=a.copy();keep('copied_'+n,a)
 test=(np.arange(4*87*45)%17-8).reshape(4,87,45)/31.;test*=normal_test_mask();testjets=evaluate_normal_test(test,geo);weight=(geo['dv']/geo['R']).reshape(15136)
 differences=[];bounds=[]
 for part in ('configuration','rate','mean'):
  signed=coefs[part] if part=='mean' else (-coefs[part][0],-coefs[part][1]);nodal=normal_action_reduce(a_mul64(test,rows[part]),(0,1,2));point=a_dd(np.zeros(15136))
  for row in range(4):
   for jet,cjet in ((0,0),(1,1),(2,2)):point=a_add(point,a_mul64(testjets[:,row,jet],a_slice(signed,(slice(None),row,cjet))))
  direct=normal_action_reduce(a_mul64(weight,point),(0,));gap=a_sub(nodal,direct)
  for name,x in (('nodal',nodal),('direct',direct),('gap',gap)):emit_pair(fields,part+'_new_functional_'+name,x)
  ec=abs(signed[0][:,:,:3])+abs(signed[1][:,:,:3]);en=scatter_normal_envelope(ec,geo);bound=np.sum(abs(test)*en)+np.sum(weight[:,None,None]*abs(testjets)*ec)
  differences.append(float(gap[0]+gap[1]));bounds.append(float(bound))
 P.check('new_combined_contact_normal_Q1_functionals',np.array(differences),np.zeros(3),np.array(bounds));fields.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 loads=P.checkpoint('LOADS',fields,dict(kind='new_combined_configuration_rate_phase_and_once_counted_mean_normal_derivative',columns=[thin(q) for q in refs],warm_signed_bridge_ref=thin(admitted['warm_readout']),earned_phase_contact_ref=thin(admitted['phase_normal_loads']),physical_ports=None,temporal_improvement_ports=None,old_normal_or_mean_rows_added=False,original_primitive_bridge_resolved=False,configuration_updated=False,controls=P.CHECKS[-1:]))
 assert len(P.CHECKS)==4 and len(P.RECORDS)==7
 return dict(status='COMBINED_SAME_ACTION_NORMAL_CONFIGURATION_DERIVATIVE_MEASURED',input=inp,fixture=fr,columns=refs,loads=loads,controls=P.CHECKS,checkpoints=P.RECORDS,phase_charge_linear_response_admitted=True,global_frozen_rate_response_admitted=True,primitive_bridge_resolved=False,normal_constraints_qualified=False,finite_configuration_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root and distinct FULL review required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_combined_normal_derivative');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,admitted=combined_normal_derivative_admission();case=combined_packet(admitted);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=4,pairs=7)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})};arrays={n:np.asarray(x).copy() for n,x in arrays.items()}
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='current_new_combined_normal_derivative_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
