"""HELD NEW shared-candidate contact/native/EH and weak assembly controls.
Root alone releases and executes. Three fresh manufactured inputs, no prior
fixture, source payload, coefficient, action, operator or solver replay.
Point tables retain all sixteen tests including time-primary coefficients.
The one-cell weak fixture is an implementation test, not a galaxy candidate.
Phase/ordinary zero placeholders are explicit; their mixed test is separate.
"""
from pathlib import Path
from fractions import Fraction
import ast,hashlib,json,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='FINITE_CANDIDATE_CONTACT_NORMAL_CONTROLS_V001'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'FINITE_CANDIDATE_CONFIGURATION_CONTACT_V001.md':'605d9c375c9a1a8b2e37ca8b221dc810c49573613f7886570ffb5e62aae54cd7',
 'author_fragment_finite_candidate_native_EH_normal_v001.py':'51947ffe86b0b2aa592ac331aaaca2323872249785268d0dbfc4dec662a79152',
 'FINITE_CANDIDATE_NATIVE_EH_NORMAL_V001.md':'f4a5a419ad720e7e11d31fb40d3c75109c4de11a873270e92a8c56876a3e70ab'}
DRIVER_PROTOCOL='FINITE_CANDIDATE_CONTACT_NORMAL_CONTROLS_V001.md'
DRIVER_PROTOCOL_SHA='85cfd608bc21b3f948a66eaf3571bf774d47e6a9736bcd4cedd1e4b7c069b5f6'
np=P=N=None;PROVIDER_SCOPE={};NORMAL_SCOPE={};RAW={};CASES=[];CONTROLS=[];EXACT_TARGETS={}

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def pair(high,low=None):
 h=np.asarray(high,dtype=np.float64);l=np.zeros_like(h) if low is None else np.asarray(low,dtype=np.float64)
 assert h.shape==l.shape;return h.copy(),l.copy()
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def capture_tree(prefix,value):
 if isinstance(value,dict):
  for n,x in value.items():capture_tree(prefix+'_'+n,x)
 elif isinstance(value,(tuple,list)):
  if len(value)==2 and all(isinstance(w,np.ndarray) for w in value):keep(prefix+'_hi',value[0]);keep(prefix+'_lo',value[1])
  else:
   for i,x in enumerate(value):capture_tree(prefix+'_'+str(i),x)
 elif isinstance(value,(np.ndarray,int,float,bool)):keep(prefix,value)
def fraction_pair(name,values,shape):
 values=[Fraction(x) for x in values];h=np.array([float(x) for x in values],dtype=np.float64)
 l=np.array([float(x-Fraction.from_float(float(a))) for x,a in zip(values,h)],dtype=np.float64)
 remainder=[x-Fraction.from_float(float(a))-Fraction.from_float(float(b)) for x,a,b in zip(values,h,l)]
 EXACT_TARGETS[name]=dict(shape=shape,numerators=[str(x.numerator) for x in values],denominators=[str(x.denominator) for x in values],pair_conversion_remainder_numerators=[str(x.numerator) for x in remainder],pair_conversion_remainder_denominators=[str(x.denominator) for x in remainder],exact_rational_not_exactly_two_word_representable=any(remainder))
 out=(h.reshape(shape),l.reshape(shape));capture_tree('independent_expected_'+name,out);return out
def fraction_tensor(name,shape,entries):
 values=[Fraction(0) for _ in range(int(np.prod(shape)))];index=np.arange(len(values)).reshape(shape)
 for key,value in entries.items():values[int(index[key])]=Fraction(value)
 return fraction_pair(name,values,shape)
def check_pair(name,actual,expected,bound,exact=False):
 assert actual[0].shape==actual[1].shape==expected[0].shape==expected[1].shape
 envelope=np.asarray(bound)+abs(expected[0])+abs(expected[1]);envelope=np.broadcast_to(envelope,actual[0].shape).copy();assert np.all(envelope>0)
 for n,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(name+'_'+n,x)
 gap=P.a_sub(actual,expected);capture_tree(name+'_gap',gap);error=float(np.max((abs(gap[0])+abs(gap[1]))/envelope,initial=0))
 word=not exact or all(np.array_equal(actual[i],expected[i]) for i in (0,1));keep(name+'_exact_word_predicate',np.asarray(word))
 CONTROLS.append(dict(name=name,error=error,tolerance=2e-11,exact_words=exact,word_predicate=word,passed=error<=2e-11 and word));assert error<=2e-11 and word,(name,error,word)
def check_scatter(name,actual,expected,envelope):check_pair(name,pair(actual),pair(expected),np.asarray(envelope))

def independent_inputs(case):
 h0=16. if case in (1,2) else 1.;mu0=64. if case in (1,2) else 1.;N0=2. if case in (1,2) else 1.;h=np.eye(3)[None]*h0;I=np.eye(3)[None]/h0;e=2.**-60
 zi=np.zeros((32,1,3));zj=np.zeros((32,1,4,3));ht=np.zeros((1,3,3));htlo=np.zeros_like(ht);E0=np.zeros((1,4,4,4))
 if case==1:zi[0,0,0]=2.;zj[0,0,0,0]=3.
 if case==2:ht[0,0,2]=ht[0,2,0]=2.;htlo=ht*e
 if case==3:ht[0,1,1]=2.;E0[0,1,1,1]=1.
 geometry=dict(h=pair(h),ih=pair(I),mu=pair([mu0]),h_spatial_jets=pair(np.zeros((1,2,3,3))))
 gauge=dict(N=pair([N0]),beta=pair(np.zeros((1,3))),N_jets=pair(np.zeros((1,4))),beta_jets=pair(np.zeros((1,4,3))))
 covectors=dict(u=pair(np.zeros((1,3))),z=pair(zi),u_jets=pair(np.zeros((1,4,3))),z_jets=pair(zj));mechanical=dict(h_dot=pair(ht,htlo));phase=dict(phi=pair(np.zeros((1,4))))
 g=np.zeros((1,4,4));g[0,0,0]=-N0*N0;g[:,1:,1:]=h;hi=np.zeros_like(g);hi[0,0,0]=-1/(N0*N0);hi[:,1:,1:]=I
 U=np.array([[1/N0,0.,0.,0.]]);uc=np.array([[-N0,0.,0.,0.]]);z=np.concatenate((np.zeros((32,1,1)),zi),2);projector=np.diag([0.,1.,1.,1.])[None]
 dz=np.zeros((32,1,4,4));dz[:,:,:,1:]=zj;dg=np.zeros((1,4,4,4));dg[:,0,1:,1:]=ht;dglo=np.zeros_like(dg);dglo[:,0,1:,1:]=htlo;Ga=np.zeros_like(dg)
 if case==2:
  Ga[0,0,1,3]=Ga[0,0,3,1]=.25;Ga[0,1,0,3]=Ga[0,1,3,0]=Ga[0,3,0,1]=Ga[0,3,1,0]=1/16
 if case==3:Ga[0,0,2,2]=Ga[0,2,0,2]=Ga[0,2,2,0]=1.;Ga[0,1,1,1]=-.5
 value=dict(g=pair(g),hi=pair(hi),U=pair(U),z=pair(z),uc=pair(uc),P=pair(projector),up=pair(np.zeros((1,3))),gamma=pair([1.]),dens=pair([N0*mu0]),du=pair(np.zeros((1,4,4))),dz=pair(dz),dg=pair(dg,dglo),Ga=pair(Ga,Ga*e if case==2 else None))
 model=dict(value=value,delta={n:pair(np.zeros_like(x[0])) for n,x in value.items()})
 reference={n:value[n] for n in ('g','hi','U','z','du','dz','dg','Ga')};reference.update(E0=pair(E0),canonical_targets=dict(kind='fresh_manufactured_reference',physical_prior_selected=False),prior_bridge_references=dict(kind='fresh_manufactured_reference',physical_stationarity_admitted=False))
 w=np.zeros(32);w[0]=1. if case==1 else 0.;material=dict(omega=np.ones(32),xi=np.ones(32),w=w,B=1.,GC=1.,ALPHA=.02/1.98,ELL=.1,C=1.98,R=np.array([1.]),Z_coordinate=np.array([1.]))
 direction=dict(h=pair(4*h),h_spatial_jets=pair(np.zeros((1,2,3,3))),h_dot=pair(np.zeros((1,3,3))),u_jets=pair(np.zeros((1,4,3))),z_jets=pair(np.zeros((32,1,4,3))))
 return (geometry,model,gauge,covectors,mechanical,phase,material,reference),direction

def independent_targets(case):
 F=Fraction;C=F.from_float(1.98);e=F(1,2**60);x=1+e;prefix='case%d_'%case;native={};EH={}
 if case==1:native={(0,0,0):-F(27,2),(1,0,0):-F(23),(0,0,1):F(8),(1,0,1):F(16)}
 if case in (1,2):EH={(0,0,1):-4/C,(1,0,1):-8/C};theta=[F(-24),F(-144)];v=[F(8),F(16)]
 else:EH={(0,0,1):-1/C,(1,0,1):-2/C,(0,1,0):1/(2*C),(1,1,0):-1/C,(0,1,1):1/C,(1,1,1):2/C};theta=[F(5,8),-F(1,4)];v=[F(2),F(4)]
 if case==2:EH.update({(0,0,0):-x*x/(16*C),(1,0,0):x*x/(8*C),(0,3,1):-2*x/C,(1,3,1):-4*x/C})
 total=native.copy()
 for k,a in EH.items():total[k]=total.get(k,F(0))+a
 tables={n:fraction_tensor(prefix+n,(2,4,4),a) for n,a in (('native',native),('EH',EH),('action',total))}
 tables['theta']=fraction_pair(prefix+'theta',theta,(2,1));tables['Q']=fraction_tensor(prefix+'Q',(2,1),{});tables['V']=fraction_tensor(prefix+'V',(2,1,3),{(0,0,0):v[0],(1,0,0):v[1]})
 nd={};md={};ed={}
 if case==1:nd={(0,0,0):F(8),(1,0,0):F(16),(0,0,3):F(6),(1,0,3):F(12)};md={(0,0,0):-F(3,8),(1,0,0):F(3,4)}
 if case==2:ed={(0,0,4):x/(8*C),(1,0,4):-x/(4*C)}
 if case==3:ed={(0,0,0):-1/(2*C),(0,0,2):-1/(2*C),(1,0,0):1/C,(1,0,2):1/C}
 for n,shape,a in (('native_canonical',(2,1,99),nd),('metric_native_canonical',(2,1,6),md),('EH_canonical',(2,1,6),ed)):tables[n]=fraction_tensor(prefix+n,shape,a)
 # Independent exact corner integrals: N=1/4, NR=NZ=-1/2;
 # R*N=65/6, (R*N)_R=-43/2, (R*N)_Z=-65/3.
 functional=[]
 for direction in (0,1):
  def H(row,jet):return -total.get((direction,row,jet),F(0))
  rows=[H(0,0)/4-H(0,1)/2-H(0,2)/2,F(65,6)*H(1,0)-F(43,2)*H(1,1)-F(65,3)*H(1,2),H(2,0)/4-H(2,1)/2-H(2,2)/2,H(3,0)/4-H(3,1)/2-H(3,2)/2]
  functional.append(sum(F(i+1)*a for i,a in enumerate(rows)))
 tables['normal_integral']=fraction_pair(prefix+'normal_integral',functional,(2,));tables['CMC_integral']=fraction_pair(prefix+'CMC_integral',[a/4 for a in theta],(2,))
 tables['scope']=pair(np.asarray(1.));return tables

def new_basis():
 i,j=np.meshgrid(np.arange(86),np.arange(44),indexing='ij');gauss=((1-1/np.sqrt(3))/2,(1+1/np.sqrt(3))/2);R=np.empty((4,3784));hats=np.empty((4,4,3,86,44))
 for iq,(x,y) in enumerate(((gauss[0],gauss[0]),(gauss[1],gauss[0]),(gauss[0],gauss[1]),(gauss[1],gauss[1]))):
  R[iq]=(i+x).reshape(3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   a=x if di else 1-x;b=y if dj else 1-y;hats[iq,corner,0]=a*b;hats[iq,corner,1]=(1. if di else -1.)*b;hats[iq,corner,2]=(1. if dj else -1.)*a
 basis=dict(R=R,dv=R/4,hats=hats,cell_i=i.reshape(3784),cell_j=j.reshape(3784));normal=np.zeros((4,87,45));normal[:,43,22]=(1.,2.,3.,4.);scalar=np.zeros((87,45));scalar[43,22]=1.
 return basis,normal,scalar

def new_point_case(case,inputs,direction,known):
 candidate=finite_candidate_raw_action_adapter(*inputs,P.paired_current_affine_features,P.paired_current_affine_momenta,keep,'fresh_case%d_raw'%case)
 capture_tree('completed_candidate',candidate)
 contact=finite_candidate_configuration_contact(candidate,inputs[0],inputs[2],inputs[3],inputs[4],direction,inputs[7],keep,'fresh_case%d_contact'%case);capture_tree('completed_contact',contact)
 curvature=finite_candidate_intrinsic_curvature(candidate,contact,keep,'fresh_case%d_curvature'%case);capture_tree('completed_curvature',curvature)
 tables={n:pair(np.zeros((2,4,4))) for n in ('native','EH','action')};theta=None
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   f=np.zeros(1);df=np.zeros((1,4));b=np.zeros((1,3));db=np.zeros((1,4,3))
   if row==0:
    if coordinate is None:f[0]=1.
    else:df[0,coordinate]=1.
   elif coordinate is None:b[0,row-1]=1.
   else:db[0,coordinate,row-1]=1.
   label='fresh_case%d_row%d_jet%d'%(case,row,jet)
   out=finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,1/8,inputs[7],keep,label);capture_tree('completed_'+label,out)
   for n in tables:
    for k,family in enumerate(('value','delta')):
     for word in (0,1):tables[n][word][k,row,jet]=out[family][n][word][0]
    capture_tree('completed_sixteen_'+n,tables[n])
   theta=P.a_stack([out['value']['initial_CMC_density'],out['delta']['initial_CMC_density']],0);capture_tree('completed_initial_CMC',theta)
 for n,actual in tables.items():check_pair('case%d_all_sixteen_%s'%(case,n),actual,known[n],512)
 check_pair('case%d_initial_CMC'%case,theta,known['theta'],256)
 for n in ('Q','V'):check_pair('case%d_intrinsic_%s'%(case,n),P.a_stack([curvature[n][0],curvature[n][1]],0),known[n],256)
 for n,key in (('native_canonical','native_density'),('metric_native_canonical','metric_native_density'),('EH_canonical','metric_EH_density')):
  check_pair('case%d_%s'%(case,n),P.a_stack([candidate['momenta'][key],contact['delta_momenta'][key]],0),known[n],512)
 preserved=not candidate['physical_adoption'] and not contact['physical_adoption'] and candidate['canonical_target_references'] is inputs[7]['canonical_targets'] and candidate['prior_bridge_references'] is inputs[7]['prior_bridge_references']
 check_pair('case%d_unchanged_prior_scope'%case,pair(np.asarray(float(preserved))),known['scope'],1,True)
 return tables,theta

def new_global_case(case,tables,theta,known):
 basis,nt,st=new_basis();capture_tree('fresh_basis',basis);keep('fresh_normal_test',nt);keep('fresh_CMC_test',st);columns=[];index=43*44+22
 for iq in range(4):
  q=dict(normal_coordinate_order=('value','R','Z','t'),relative_phase_count=1,ordinary_label_count=1,phase_and_ordinary_zero_placeholder_only=True)
  for k,family in enumerate(('value','delta')):
   coeff=pair(np.zeros((3784,4,4)));trace=pair(np.zeros(3784))
   for word in (0,1):coeff[word][index]=-tables['action'][word][k];trace[word][index]=theta[word][k,0]
   q[family]=dict(normal_coefficients=coeff,initial_CMC_density=trace)
  columns.append(q);capture_tree('completed_NEW_fixture_column%d'%iq,q)
 out=finite_candidate_global_normal_CMC(columns,basis,nt,st,keep,check_scatter,'case%d_NEW_global'%case);capture_tree('completed_global',out)
 for n,key in (('normal_integral','normal_functional_nodal'),('CMC_integral','CMC_functional_nodal')):
  actual=P.a_stack([out['value'][key],out['delta'][key]],0);check_pair('case%d_independent_%s'%(case,n),actual,known[n],512)
 assert out['all_time_primary_coefficients_retained'] and not out['finite_candidate_physically_admitted'];return out

def save_case(case):
 name=STEM+'_CASE'+str(case)+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
 (BASE/name).chmod(0o444);CASES.append(dict(case=case,file=name,sha256=sha(name),fields=len(RAW),physical_adoption=False));RAW.clear()

def initialize():
 global np,P,N,PROVIDER_SCOPE,NORMAL_SCOPE
 import numpy as numpy
 np=numpy;names=list(PINS);trees=[ast.parse((BASE/f).read_text()) for f in names[:3]];maps=[{n.name:n for n in t.body if isinstance(n,ast.FunctionDef)} for t in trees]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','paired_current_affine_features','paired_current_affine_momenta'}
 scalar={'a_reshape','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter'}
 for n in base:assert ast.dump(maps[0][n],include_attributes=False)==ast.dump(maps[1][n],include_attributes=False),n
 selected=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base|scalar]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(selected)==26
 PROVIDER_SCOPE=dict(np=np,DD_ARRAY_CURRENT={},capture=keep,B=1.,GC=1.,ALPHA=.02/1.98,ELL=.1,C=1.98);exec(compile(ast.Module(body=selected,type_ignores=[]),names[1],'exec'),PROVIDER_SCOPE)
 P=types.SimpleNamespace(**{n:PROVIDER_SCOPE[n] for n in base|primitive|scalar|{'B','GC','ALPHA','ELL','C'}})
 # Literal123 calls aliases directly: all of them and the constants are explicit.
 globals().update({n:PROVIDER_SCOPE[n] for n in base|primitive|scalar|{'B','GC','ALPHA','ELL','C'}})
 normal={'normal_test_mask','extend_normal_tests','restrict_normal_rows','normal_hat_jet','normal_hat_operation_envelope','scatter_normal_envelope','paired_restrict_normal_rows','paired_scatter_normal'}
 NORMAL_SCOPE=dict(PROVIDER_SCOPE);defs=[n for n in trees[2].body if isinstance(n,ast.FunctionDef) and n.name in normal];assert len(defs)==8
 exec(compile(ast.Module(body=defs,type_ignores=[]),names[2],'exec'),NORMAL_SCOPE);N=types.SimpleNamespace(**{n:NORMAL_SCOPE[n] for n in normal})
 counts=(11,20,8,7,5,8);files=(names[3],names[4],names[5],names[6],names[7],names[9])
 for file,count in zip(files,counts):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and DRIVER_PROTOCOL_SHA is not None and not list(BASE.glob(STEM+'_*')),'Root exclusive reviewed release required'
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 initialize()
 for case in (1,2,3):
  inputs,direction=independent_inputs(case);known=independent_targets(case);capture_tree('fresh_input',dict(zip(('geometry','spacetime','gauge','covectors','mechanical','phase','material','reference'),inputs)));capture_tree('fresh_input_direction',direction)
  targetfile=STEM+'_CASE'+str(case)+'_EXACT_TARGETS.json'
  with (BASE/targetfile).open('x') as f:json.dump(dict(case=case,targets={n:x for n,x in EXACT_TARGETS.items() if n.startswith('case%d_'%case)},two_words_are_rounded_target_comparisons_not_exact_rational_representation=True),f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
  (BASE/targetfile).chmod(0o444)
  tables,theta=new_point_case(case,inputs,direction,known);new_global_case(case,tables,theta,known);save_case(case)
 assert len(CONTROLS)==48 and all(x['passed'] for x in CONTROLS)
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 report=dict(status='NEW_CANDIDATE_CONTACT_NATIVE_EH_GLOBAL_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),pins=PINS,driver_protocol_sha256=DRIVER_PROTOCOL_SHA,controls=CONTROLS,cases=CASES,only_three_new_inputs_evaluated=True,all_sixteen_test_and_time_primary_contacts_preserved=True,phase_ordinary_mixed_integration_control_separate=True,global_fixture_is_one_predeclared_cell_implementation_only=True,original_targets_and_offsets_refitted=False,old_fixture_coefficient_payload_operator_solver_replayed=False,physical_normal_CMC_or_finite_preparation_admitted=False)
 name=STEM+'_RESULT.json'
 with (BASE/name).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=len(CONTROLS),sha256=sha(name))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for name,value in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+name]=np.asarray(value).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,exact_targets=EXACT_TARGETS,traceback=traceback.format_exc()),f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
