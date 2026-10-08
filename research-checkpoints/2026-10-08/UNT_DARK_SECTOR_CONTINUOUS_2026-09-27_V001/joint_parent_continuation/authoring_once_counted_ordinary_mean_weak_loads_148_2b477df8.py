"""Guarded once-counted ordinary mean branch; new source loads, no old law replay."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_ONCE_COUNTED_ORDINARY_MEAN_WEAK_LOADS_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
PROVIDER='cross_u_paired_current_normal_constraints_v002.py'
PROVIDER_SHA='a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40'
NORMAL='CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002'
BENCH='CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001'
FORCE='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RESULT.json'
REG='CROSS_U_ONCE_COUNTED_ORDINARY_EXCESS_LABEL_REGISTRATION_V001.json'
PINS={NORMAL+'_RESULT.json':'ca1056f8798864eb7ae86c61812379ad8be46c4586560bf832f308fb79242158',NORMAL+'_RECEIPT.json':'00a630bd20e5ac06ce3dcc63dd4187c6d82b8ea73989274b0d105157cfee25b2','READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json':'1e3b72fee21d3ec31335a02ae814d74c982d2970c39c9fb0575f28589ba2442b',BENCH+'_RESULT.json':'d279da68cbf50ebbeae62021cb39333cc986abda54f467df71eecc5791358502',BENCH+'_RECEIPT.json':'5c21282863bbbfb129ce59fa0cf861d18c6f0fe77af16a62a2a3c3fd3fe1f243',FORCE:'981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770',REG:'6bf78e13e4099d7a13988237658a81ad90ea975ab0b3f18c0e4446206d411f05','CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00000_REUSED_SOURCE_FOOTPRINTS.npz.COMMIT.json':'b8061d69f72302d923a45a4a8875cb687188eb3a4a9ebf13801c92eebbcd4dc7'}
P=None;np=None

def initialize():
 global P,np
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('mean_load_custody_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS={n:False for n in ('original_state_changed','physical_label_preparation_admitted','canonical_bridge_admitted','normal_constraint_zero','evolution_qualified','physical_exterior_qualified','orbital_or_observational_prediction','background_overlap_explanation_adopted')}
 bind(PROVIDER,PROVIDER_SHA)
 for n,h in PINS.items():bind(n,h)
 bind(STEM+'.md',PROTOCOL_SHA);bind(Path(__file__).name,P.sha(__file__))

def bind(n,h):
 p=BASE/n;assert h is not None and P.sha(p)==h,n;key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def record(ref,mapping):
 ref=P.resolve_record(ref)
 for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):
  assert mapping[n if n in mapping else str((BASE/n).resolve())]==h;bind(n,h)
 return ref

def load(ref,mapping,names,label):
 ref=record(ref,mapping);raw=P.read_pair(ref,names)
 for n,a in raw.items():P.capture(label+'_'+n,a)
 return raw

def restrict_normal(x):
 y=x.copy()
 for row in (0,2,3):y[row,1]+=y[row,0]
 y[:,0]=0;y[2,:,0]=0;y[:,-1]=0;y[:,:,-1]=0;return y

def lift_normal(x):
 y=x.copy()
 for row in (0,2,3):y[row,0]=y[row,1]
 y[1,0]=0;y[2,:,0]=0;y[:,-1]=0;y[:,:,-1]=0;return y

def restrict_metric(x):
 y=x.copy();y[:,1]+=y[:,0];y[:,0]=0;y[3:5,:,0]=0;return y

def lift_metric(x):
 y=x.copy();y[:,0]=y[:,1];y[3:5,:,0]=0;return y

def metric_F(R):
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2;return F

def direction_rule(order,nphi):
 mu,w=np.polynomial.legendre.leggauss(order);directions=[];weights=[]
 # One hemisphere plus exact antipodes: odd canonical momentum cancels exactly.
 for t,wt in zip(mu[mu>0],w[mu>0]):
  for k in range(nphi):
   ph=2*math.pi*k/nphi;s=math.sqrt(1-t*t);directions.append((s*math.cos(ph),t,s*math.sin(ph)));weights.append(wt/nphi)
 return np.asarray(directions),np.asarray(weights)

def angular_moments(ih,R,directions,weights,label):
 p=len(R);energy=np.zeros(p);stress=np.zeros((p,3,3));envE=np.zeros(p);envS=np.zeros_like(stress)
 for k,(n,w) in enumerate(zip(directions,weights)):
  cov=np.broadcast_to(n,(p,3)).copy();cov[:,2]*=R;up=np.einsum('pij,pj->pi',ih,cov);sq=np.sum(cov*up,axis=1)
  P.capture(label+'_current_canonical_direction',cov);P.capture(label+'_current_raised_direction',up);P.capture(label+'_current_energy_squared',sq);assert np.all(np.isfinite(sq)) and np.all(sq>0)
  eps=np.sqrt(sq);termE=w*eps;termS=w*up[:,:,None]*up[:,None,:]/eps[:,None,None]
  energy+=termE;P.capture(label+'_energy_partial',energy);stress+=termS;P.capture(label+'_stress_partial',stress)
  envE+=abs(termE);envS+=abs(termS);P.capture(label+'_energy_envelope_partial',envE);P.capture(label+'_stress_envelope_partial',envS)
 return energy,stress,envE,envS

def mean_column(iq,ref,mapping,geo,rhoB,rhoR,rules):
 P.RAW={};P.AVAILABLE={};P.CONTEXT.update(stage='new_fixed_canonical_mean_column',column=iq)
 raw=load(ref,mapping,('config_R','config_phi','chart_h','chart_ih','chart_N','chart_sqrt_h'),'current');R=raw['config_R'];h=raw['chart_h'];ih=raw['chart_ih'];N=raw['chart_N'];mu=raw['chart_sqrt_h'];phi=raw['config_phi'];p=len(R)
 assert p==3784 and h.shape==ih.shape==(p,3,3) and np.array_equal(R,geo['R'][iq].reshape(p)) and np.all((N>0)&(mu>0)) and np.all(phi[:,0]>0) and np.all(phi[:,1:]==0)
 inv=np.einsum('pij,pjk->pik',h,ih);refinv=np.broadcast_to(np.eye(3),inv.shape);einv=np.einsum('pij,pjk->pik',abs(h),abs(ih))+abs(refinv)
 scale=h[:,0,0];conformal=np.zeros_like(h);conformal[:,0,0]=scale;conformal[:,1,1]=scale;conformal[:,2,2]=scale*R**2
 a=np.concatenate((inv.reshape(p,9),h.reshape(p,9)),axis=1);e=np.concatenate((refinv.reshape(p,9),conformal.reshape(p,9)),axis=1);v=np.concatenate((einv.reshape(p,9),(abs(h)+abs(conformal)).reshape(p,9)),axis=1)
 P.check('mean_column_%d_current_inverse_and_conformal_domain'%iq,a,e,v)
 coarse=angular_moments(ih,R,*rules[0],'coarse');fine=angular_moments(ih,R,*rules[1],'fine')
 ca=np.concatenate((coarse[0][:,None],coarse[1].reshape(p,9)),axis=1);fa=np.concatenate((fine[0][:,None],fine[1].reshape(p,9)),axis=1);ve=np.concatenate(((coarse[2]+fine[2])[:,None],(coarse[3]+fine[3]).reshape(p,9)),axis=1)
 P.check('mean_column_%d_fixed_isotropic_angular_accuracy'%iq,ca,fa,ve)
 E0,S0,eE,eS=fine;DB=rhoB*R;DR=rhoR*R;EB=DB;ER=DR*E0;Srad=DR[:,None,None]*S0
 normal=np.zeros((p,4));normal[:,0]=EB+ER;metric_tensor=N[:,None,None]*Srad/2;metric=np.stack([metric_tensor[:,a,b]*(1 if a==b else 2) for a,b in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=1)
 enormal=np.zeros_like(normal);enormal[:,0]=abs(DB)+abs(DR)*eE;emetric=np.stack([abs(N)*abs(DR)*eS[:,a,b]*(.5 if a==b else 1.) for a,b in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=1)
 data=dict(reference_coordinate_dust_density=DB,reference_radiation_energy_measure=DR,dust_coordinate_energy=EB,radiation_coordinate_energy=ER,dust_physical_energy=EB/mu,radiation_physical_energy=ER/mu,radiation_contravariant_stress_density=Srad,mean_normal_coordinate_densities=normal,mean_metric_configuration_force=metric,normal_envelope=enormal,metric_envelope=emetric,angular_energy_coarse=coarse[0],angular_energy_fine=E0,angular_stress_coarse=coarse[1],angular_stress_fine=S0,current_R=R,current_h=h,current_ih=ih,current_N=N,current_sqrt_h=mu)
 for n,a in data.items():P.capture('completed_'+n,a)
 data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 rec=P.checkpoint('COLUMN',data,dict(kind='new_once_counted_fixed_canonical_mean_ordinary_densities',column=iq,configuration_parent=ref,angular_rules=[{'mu':4,'phi':8,'antipodal_directions':32},{'mu':8,'phi':16,'antipodal_directions':128}],production_rule='fine',canonical_reference_frame='EPS5 phase-normal at this phi_i0 slice',canonical_momentum_density_exact_zero_by_antipodal_symmetry=True,ordinary_configuration_force_is_positive_N_stress_over_two=True,controls=P.CHECKS[-2:],finite_compensation_selected=False,physical_preparation_admitted=False))
 return normal,metric,enormal,emetric,DB,rec

def scatter_new(columns,geo):
 normal=np.zeros((4,87,45));metric=np.zeros((6,87,45));en=np.zeros_like(normal);em=np.zeros_like(metric);dust=np.zeros((87,45));direct=np.zeros(2);directenv=np.zeros(2)
 tn=lift_normal(((np.arange(4*87*45)%17)-8).reshape(4,87,45)/29);tm=lift_metric(((np.arange(6*87*45)%19)-9).reshape(6,87,45)/31)
 for iq,(pn,pm,pne,pme,DB,_) in enumerate(columns):
  R=geo['R'][iq];dv=geo['dv'][iq];weight=dv/R;F=metric_F(R);pnc=pn.reshape(86,44,4).transpose(2,0,1);pmc=np.einsum('...ta,...t->...a',F,pm.reshape(86,44,6)).transpose(2,0,1);ne=pne.reshape(86,44,4).transpose(2,0,1);me=np.einsum('...ta,...t->...a',abs(F),pme.reshape(86,44,6)).transpose(2,0,1)
  factors=np.ones((4,86,44));factors[1]=R;pnc*=factors;ne*=abs(factors);testn=np.zeros_like(pnc);testm=np.zeros_like(pmc)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=geo['hats'][iq,corner,0];key=(slice(None),slice(di,86+di),slice(dj,44+dj));normal[key]+=pnc*(weight*hat)[None];metric[key]+=pmc*(weight*hat)[None];en[key]+=ne*abs(weight*hat)[None];em[key]+=me*abs(weight*hat)[None];dust[di:86+di,dj:44+dj]+=(DB.reshape(86,44)*weight*hat);testn+=tn[key]*hat[None];testm+=tm[key]*hat[None]
   for name,a in (('new_mean_normal_partial',normal),('new_mean_metric_partial',metric),('new_mean_normal_envelope_partial',en),('new_mean_metric_envelope_partial',em),('new_mean_dust_partial',dust)):P.capture(name,a)
  direct+=np.array((np.sum(testn*pnc*weight[None]),np.sum(testm*pmc*weight[None])));directenv+=np.array((np.sum(abs(testn)*ne*abs(weight)[None]),np.sum(abs(testm)*me*abs(weight)[None])))
 normal=restrict_normal(normal);en=restrict_normal(en);metric=restrict_metric(metric);em=restrict_metric(em);d=restrict_normal(np.stack((dust,np.zeros_like(dust),np.zeros_like(dust),np.zeros_like(dust))))[0]
 P.capture('new_mean_normal_rows',normal);P.capture('new_mean_metric_configuration_rows',metric);P.capture('new_mean_dust_rows',d)
 nodal=np.array((np.sum(normal*tn),np.sum(metric*tm)));ev=directenv+np.array((np.sum(en*abs(tn)),np.sum(em*abs(tm))))
 P.check('new_mean_genuine_normal_metric_Q1_functional',nodal,direct,ev)
 return normal,metric,en,em,d

def packet():
 nr=json.loads((BASE/(NORMAL+'_RESULT.json')).read_text());rc=json.loads((BASE/(NORMAL+'_RECEIPT.json')).read_text());proof=json.loads((BASE/'READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json').read_text());br=json.loads((BASE/(BENCH+'_RESULT.json')).read_text());bc=json.loads((BASE/(BENCH+'_RECEIPT.json')).read_text())
 for result,receipt,name,pid in ((nr,rc,NORMAL,51682),(br,bc,BENCH,54328)):
  assert receipt['status']=='CLOSED' and receipt['error_sha256'] is None and receipt['result_sha256']==PINS[name+'_RESULT.json'] and result['owner']==receipt['owner'] and result['owner']['pid']==pid and result['qualification']==receipt['qualification'] and all(v is False for v in result['qualification'].values())
 assert proof['status']=='SAVED_PAIRED_NORMAL_CLOSURE_PASS' and proof['parent_terminal']['result_sha256']==PINS[NORMAL+'_RESULT.json']
 reg=json.loads((BASE/REG).read_text());assert reg['branch_adopted'] is False and reg['ordinary_source_appended'] is False and reg['branch']=='absolute_condensed_sheet_plus_disjoint_diffuse_cosmic_labels_with_asymptotic_excess'
 inp=nr['checkpoints'][0];fixed=inp['metadata']['fixed'];assert fixed['rG']==.98989898989899 and fixed['eps']==1e-5 and fixed['Hunit']==67.49711988577813 and fixed['OB']==.04659233656879551 and fixed['OR']==8.996751426107524e-5
 geo=load(nr['checkpoints'][2],rc['output_sha256'],('R','dv','hats','cell_i','cell_j','r','z'),'geometry');assert geo['R'].shape==geo['dv'].shape==(4,86,44) and geo['hats'].shape==(4,4,3,86,44)
 force=json.loads((BASE/FORCE).read_text());assert force['owner']['pid']==36387 and force['cases'][0]['sigma']==1.;oref=force['cases'][0]['loads'];src=load(oref,rc['input_sha256'],('ordinary_input_source_mass_weight','ordinary_input_source_R','ordinary_input_source_Z'),'source');m=src['ordinary_input_source_mass_weight'];Rsrc=src['ordinary_input_source_R'];assert m.shape==Rsrc.shape==(4832,) and np.all(m>=0) and np.all((Rsrc>0)&(Rsrc<=geo['r'][-1])) and np.all(src['ordinary_input_source_Z']==0)
 summary=json.loads((BASE/'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00000_REUSED_SOURCE_FOOTPRINTS.npz.COMMIT.json').read_text())['metadata']['summaries']['EXP24'];Mgal=summary['total_mass_Msun'];converted=math.fsum(map(float,m))*(299792458./1000)**2/4.30091e-6;P.capture('converted_current_mass_weight_Msun',np.array(converted));P.capture('copied_EXP24_total_rest_mass_Msun',np.array(Mgal));P.check('current_full_annular_weight_physical_mass',np.array(converted),np.array(Mgal),np.array(abs(converted)+abs(Mgal)))
 eta=fixed['Hunit']/299792458.;rhoB=3*eta*eta*fixed['OB']/(1.98*fixed['rG']);rhoR=3*eta*eta*fixed['OR']/(1.98*fixed['rG']);rho_phys=3*(fixed['Hunit']/1000)**2*fixed['OB']/(8*math.pi*.99*4.30091e-6*fixed['rG']);RL=(3*Mgal/(4*math.pi*rho_phys))**(1/3)
 rules=(direction_rule(4,8),direction_rule(8,16));mom=np.einsum('n,ni,nj->ij',rules[1][1],rules[1][0],rules[1][0]);actual=np.r_[np.sum(rules[1][1]),mom.ravel()];expected=np.r_[1.,(np.eye(3)/3).ravel()];env=np.r_[np.sum(abs(rules[1][1]))+1.,(np.einsum('n,ni,nj->ij',abs(rules[1][1]),abs(rules[1][0]),abs(rules[1][0]))+np.eye(3)/3).ravel()];P.check('fresh_antipodal_isotropic_reference_moments',actual,expected,env)
 data=dict(source_mass_weights=m,source_R=Rsrc,source_Z=src['ordinary_input_source_Z'],mean_densities=np.array((rhoB,rhoR)),label_mass_radius=np.array((Mgal,converted,RL)),fine_reference_directions=rules[1][0],fine_reference_weights=rules[1][1]);data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 P.checkpoint('INPUT',data,dict(kind='separate_conditional_once_counted_excess_ordinary_mean_branch',registration_file=REG,registration_sha256=PINS[REG],fixed=fixed,owned_background=inp['metadata']['owned_background'],original_normal_result_sha256=PINS[NORMAL+'_RESULT.json'],full_source_ref=oref,source_support='only authentic source r[-1]',reference_D_B_fixed=True,canonical_radiation_fixed=True,phase_first_jets_held=True,finite_compensation_selected=False,physical_prior='once-counted absolute condensed labels plus diffuse complementary labels q^3=r^3+RL^3',controls=P.CHECKS.copy()))
 columns=[]
 for iq,ref in enumerate(inp['metadata']['pilot_columns']):columns.append(mean_column(iq,ref,rc['input_sha256'],geo,rhoB,rhoR,rules))
 P.RAW={};P.AVAILABLE={};P.CONTEXT.update(stage='new_mean_weak_load_branch');normal,metric,en,em,dust=scatter_new(columns,geo)
 bench=load(br['checkpoint'],bc['output_sha256'],('restricted_analytic_volume',),'earned_reference');expected_dust=rhoB*bench['restricted_analytic_volume'];P.check('new_fixed_D_dust_matches_earned_analytic_Q1_volume',dust,expected_dust,abs(dust)+abs(expected_dust))
 old=load(nr['checkpoints'][-1],rc['output_sha256'],('normal_Hamiltonian_rows_hi','normal_Hamiltonian_rows_lo'),'original');new=P.a_add((old['normal_Hamiltonian_rows_hi'],old['normal_Hamiltonian_rows_lo']),P.a_dd(normal));P.capture('new_branch_normal_rows_hi',new[0]);P.capture('new_branch_normal_rows_lo',new[1])
 out=dict(mean_normal_rows=normal,mean_metric_configuration_force_rows=metric,mean_normal_envelope=en,mean_metric_envelope=em,fixed_reference_dust_normal_rows=dust,analytic_fixed_reference_dust_rows=expected_dust,original_normal_rows_hi=old['normal_Hamiltonian_rows_hi'],original_normal_rows_lo=old['normal_Hamiltonian_rows_lo'],branch_normal_rows_hi=new[0],branch_normal_rows_lo=new[1]);out.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 loads=P.checkpoint('LOADS',out,dict(kind='new_ordinary_mean_branch_with_original_rows_preserved',rows=['lapse','shift_R','shift_Z','shift_phi'],metric_force_basis=['a','b','c','d','e','f'],original_state_changed=False,ordinary_labels_disjoint_by_declared_registration=True,mean_is_not_uniform_physical_energy=True,physical_exterior=None,finite_pure_FLRW_wall=False,physical_history=None,activity_outside_0_3_to_15_1=None,controls=P.CHECKS[-2:]))
 assert len(P.CHECKS)==12 and len(P.RECORDS)==6 and all(c['passed'] for c in P.CHECKS)
 return dict(status='CONDITIONAL_ONCE_COUNTED_ORDINARY_MEAN_WEAK_LOADS_MEASURED',loads=loads,controls=P.CHECKS,checkpoints=P.RECORDS,copied_Mgal_Msun=Mgal,current_weight_converted_Mgal_Msun=converted,conditional_label_RL_kpc=RL,conditional_source_branch_assembled=True,original_state_changed=False,original_primitive_bridge_admitted=False,mean_inventory_overlap_proven=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and '--root-run' in sys.argv,'Root review/release required';assert not list(BASE.glob(STEM+'_*')),'Preserve existing namespace';initialize();P.OWNER=dict(owner='root',pid=os.getpid(),started=P.now(),source_file=Path(__file__).name,source_sha256=P.sha(__file__))
 try:
  case=packet();P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=P.OWNER,status='CLOSED',closed=P.now(),result_sha256=rh,error_sha256=None,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),qualification=P.FLAGS));P.recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True)
 except BaseException:
  failure=traceback.format_exc();arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_unqualified_new_ordinary_mean_branch_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(owner=P.OWNER,status='FAILED',traceback=failure,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=P.OWNER,status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),qualification=P.FLAGS));raise
if __name__=='__main__':main()
