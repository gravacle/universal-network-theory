"""Guarded same-action phase-charge initial Euler rate from stored native jets."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import argparse, hashlib, json, math, os, traceback

AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_COUPLED_PHASE_INITIAL_RATE_V001'
PARENT='CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002'
PROTOCOL_SHA='6f23a33650973e777bbe334485845e0eb6b436b6fbe8e6249d26486e334b67d5'
PINS={
 'authoring_cross_u_saved_coupled_phase_initial_rate_v001_227_8feed4b2.py':'8feed4b26a769e8a6b12757f86c6d95917fa61a987decc15bb1b281e0fa4d0a0',
 PARENT+'_RESULT.json':'4d4c9e89520390db932b66548aed361607abcc70b48d422502a3f53af9d06fb6',
 PARENT+'_RECEIPT.json':'4a21c59742252d7fcaaccfd7b9371fa846bc1d248579ae9408a9838ae971b99e',
 'cross_u_saved_full_native_adm_legendre_v002.py':'9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002.md':'e8529df3d5c3997f3120a0d483e035493517514ddeaaa3e55834e811006d81e3',
 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json':'3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c',
 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md':'087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523',
 'CROSS_U_CONSTRAINED_CANONICAL_CHART_AND_CMC_ADMISSION_V001.md':'872ca230d040bfca08ac127c117e741e81549a4316e62dd5de8df8e8732f7e98'}
SIGMAS=(.1,1.,10.,100.)
TOL=2e-11
CONTROL_COUNT=20
PAIR_COUNT=6
np=None
OWNER=None
INPUTS={}
OUTPUTS={}
RECORDS=[]
CHECKS=[]
RAW={}
CONTEXT={}
FLAGS={k:False for k in ('full_Cauchy_slice_qualified','global_constraint_solution_qualified','physical_initial_state_qualified','formation_history_qualified','quantum_origin_qualified','physical_junction_qualified','active_source_mapping_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def encode(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def publish(n,b):
 p=path(n)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[n]=sha(p);assert p.read_bytes()==b
 return OUTPUTS[n]
def json_file(n,v):return publish(n,encode(v))
def check(label,a,b,envelope):
 a=np.asarray(a);b=np.asarray(b);e=np.asarray(envelope)
 k=len(CHECKS);CONTEXT.update(control=label,ordinal=k)
 for n,v in (('actual',a),('expected',b),('envelope',e)):RAW[f'control_{k:03d}_{label}_{n}']=v.copy()
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 err=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0))
 row=dict(ordinal=k,name=label,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row)
 assert row['passed'],(label,err)
def checkpoint(tag,arrays,meta,allow_failed=False):
 for k,a in arrays.items():assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiu' and (allow_failed or np.all(np.isfinite(a))),k
 md=dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for k,a in arrays.items()})
 text=encode(md).decode();n=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(n)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);r=dict(file=n,sha256=sha(p),metadata=md);c=n+'.COMMIT.json';ch=json_file(c,r)
 OUTPUTS[n]=r['sha256'];r=dict(r,commit_file=c,commit_sha256=ch);RECORDS.append(r)
 with np.load(p,allow_pickle=False) as f:
  assert str(f['metadata_json'])==text and set(f.files)==set(arrays)|{'metadata_json'}
  for k,a in arrays.items():assert np.array_equal(f[k],a,equal_nan=True)
 return r
def recheck():
 for n,h in INPUTS.items():assert sha(path(n))==h,('input changed',n)
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('output changed',n)
 assert sha(__file__)==OWNER['source_sha256']
def read_arrays(r,names):
 assert sha(path(r['file']))==r['sha256'] and sha(path(r['commit_file']))==r['commit_sha256']
 assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
 out={}
 with np.load(path(r['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json']))==r['metadata']
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a;s=r['metadata']['schema'][n]
   assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a));out[n]=a
 return out

def phase_rate(g,hi,U,Udot,phi,gdot,udot,N,beta,u,PX,PXX):
 """Exact circular initial charge equation and independent four-tensor derivative."""
 h=g[:,1:,1:];ih=hi[:,1:,1:]+beta[:,:,None]*beta[:,None,:]/N[:,None,None]**2
 hdot=gdot[:,1:,1:];up=np.einsum('pij,pj->pi',ih,u)
 b=np.einsum('pi,pi->p',u,up)
 theta=np.einsum('pij,pji->p',ih,hdot)/2
 bdot_terms=np.column_stack((2*np.einsum('pi,pi->p',up,udot),-np.einsum('pi,pij,pj->p',up,hdot,up)))
 bdot=bdot_terms.sum(axis=1)
 raised=np.einsum('pab,pb->pa',hi,phi);X=np.sqrt(-np.einsum('pa,pa->p',phi,raised))
 denominator=PXX-b
 for n,a in dict(b=b,theta=theta,bdot=bdot,bdot_terms=bdot_terms,X=X,denominator=denominator).items():RAW['current_rate_'+n]=a.copy()
 assert np.all(X>0) and np.all(b>=0) and np.all(np.isfinite(denominator)) and np.all(denominator!=0),'Strict finite phase velocity map refusal.'
 numerator_terms=np.column_stack((theta*PX,-theta*X*b,-X*bdot))
 numerator=numerator_terms.sum(axis=1);phi_tt=-N*numerator/denominator
 RAW['current_rate_numerator_terms']=numerator_terms.copy();RAW['current_rate_phi_tt']=phi_tt.copy()
 dphi=np.zeros_like(phi);dphi[:,0]=phi_tt
 dhi=-np.einsum('pac,pcd,pdb->pab',hi,gdot,hi)
 dhi_env=np.einsum('pac,pcd,pdb->pab',abs(hi),abs(gdot),abs(hi))
 dX_terms=np.column_stack((np.einsum('pa,pab,pb->p',phi,dhi,phi),2*np.einsum('pa,pa->p',raised,dphi)))
 dX=-dX_terms.sum(axis=1)/(2*X)
 dX_env=(np.einsum('pa,pab,pb->p',abs(phi),dhi_env,abs(phi))+2*np.einsum('pa,pa->p',abs(raised),abs(dphi)))/(2*X)
 v=-raised/X[:,None]
 drphi=np.einsum('pab,pb->pa',dhi,phi)+np.einsum('pab,pb->pa',hi,dphi)
 drphi_env=np.einsum('pab,pb->pa',dhi_env,abs(phi))+np.einsum('pab,pb->pa',abs(hi),abs(dphi))
 dv=-drphi/X[:,None]-v*dX[:,None]/X[:,None]
 dv_env=drphi_env/X[:,None]+abs(v)*dX_env[:,None]/X[:,None]
 QU=np.einsum('pa,pa->p',U,phi);dQU=np.einsum('pa,pa->p',Udot,phi)+np.einsum('pa,pa->p',U,dphi)
 dQU_env=np.einsum('pa,pa->p',abs(Udot),abs(phi))+np.einsum('pa,pa->p',abs(U),abs(dphi))
 r_raised=raised+U*QU[:,None]
 dr_raised=drphi+Udot*QU[:,None]+U*dQU[:,None]
 dr_raised_env=drphi_env+abs(Udot)*abs(QU[:,None])+abs(U)*dQU_env[:,None]
 J=PX[:,None]*v-r_raised
 dJ=PXX[:,None]*dX[:,None]*v+PX[:,None]*dv-dr_raised
 dJ_env=abs(PXX[:,None])*dX_env[:,None]*abs(v)+abs(PX[:,None])*dv_env+dr_raised_env
 density=np.sqrt(-np.linalg.det(g));sqrt_h=density/N
 logdensity=np.einsum('pab,pba->p',hi,gdot)/2
 logdensity_env=np.einsum('pab,pba->p',abs(hi),abs(gdot))/2
 charge_rate=density*(logdensity*J[:,0]+dJ[:,0])
 charge_rate_env=density*(logdensity_env*(abs(PX*v[:,0])+abs(r_raised[:,0]))+dJ_env[:,0])
 closed_rate=sqrt_h*(numerator+denominator*phi_tt/N)
 closed_env=sqrt_h*(abs(numerator_terms).sum(axis=1)+abs(denominator*phi_tt/N))
 return dict(h_inverse=ih,u_raised=up,b=b,theta=theta,bdot_terms=bdot_terms,bdot=bdot,X=X,P_X=PX,P_XX=PXX,denominator=denominator,numerator_terms=numerator_terms,numerator=numerator,phi_tt=phi_tt,dphi=dphi,delta_inverse=dhi,delta_X_terms=dX_terms,delta_X=dX,v_phase=v,relative_raised=r_raised,J_phi=J,delta_J_phi=dJ,charge_rate=charge_rate,charge_rate_envelope=charge_rate_env,closed_charge_rate=closed_rate,closed_charge_rate_envelope=closed_env,density=density,sqrt_h=sqrt_h)

def fixture(N,beta,u,hdot,udot,PX,PXX,X):
 h=np.diag([4.,9.,16.]);ih=np.diag([.25,1/9,1/16]);g=np.zeros((1,4,4));hi=np.zeros_like(g)
 g[0,1:,1:]=h;g[0,0,1:]=h@beta;g[0,1:,0]=g[0,0,1:];g[0,0,0]=-N*N+beta@h@beta
 hi[0,0,0]=-1/N**2;hi[0,0,1:]=beta/N**2;hi[0,1:,0]=hi[0,0,1:];hi[0,1:,1:]=ih-np.outer(beta,beta)/N**2
 up=ih@u;gamma=math.sqrt(1+u@up);U=np.r_[gamma/N,up-beta*gamma/N][None]
 dgamma=(up@udot-up@hdot@up/2)/gamma;dup=ih@udot-ih@hdot@up
 Udot=np.r_[dgamma/N,dup-beta*dgamma/N][None]
 gd=np.zeros_like(g);gd[0,1:,1:]=hdot;gd[0,0,1:]=hdot@beta;gd[0,1:,0]=gd[0,0,1:];gd[0,0,0]=beta@hdot@beta
 phi=np.array([[N*X,0.,0.,0.]])
 return phase_rate(g,hi,U,Udot,phi,gd,udot[None],np.array([N]),beta[None],u[None],np.array([PX]),np.array([PXX]))

def fixtures(fixed,cp):
 eta=fixed['Hunit']/299792458.;back=cp['background'];H=eta*back['h'];Q=100*eta*back['q'];cs2=back['cs']
 ep=fixed['eps'];s=back['s'];u=ep*s/(1+s);norm=1/ep-math.log1p(1/ep)
 ownedPX=(2*eta*eta/1.98)*back['w']/Q
 ownedPXX=(2*eta*eta/1.98)*back['A']*(2*s/(ep*norm)+4*back['q']**2/(norm*(ep-u)**2))/(100*eta)**2
 # This exact homogeneous control is the owned clock equation, with cs already c_s^2.
 a=fixture(1.,np.zeros(3),np.zeros(3),2*H*np.diag([4.,9.,16.]),np.zeros(3),ownedPX,ownedPXX,Q)
 qdot=-3*H*cs2*Q
 RAW.update({'fixture_homogeneous_'+k:v.copy() for k,v in a.items()})
 check('owned_homogeneous_charge_clock',np.array([a['phi_tt'][0],a['charge_rate'][0]]),np.array([qdot,0.]),np.array([abs(qdot),a['charge_rate_envelope'][0]]))
 F=Fraction;N=F(7,5);X=F(15,119);PX=F(2,7);PXX=F(7,3);b=F(9,16)
 beta=np.array([1/7,-1/11,1/13]);u=np.array([1.5,0.,0.])
 for name,Hf,duf in (('volume',F(1,13),F(0)),('native',F(0),F(2,19)),('mixed',F(1,13),F(2,19))):
  theta=3*Hf;bdot=F(3,4)*duf-2*Hf*b;exact=-N*(theta*(PX-X*b)-X*bdot)/(PXX-b)
  d=fixture(float(N),beta,u,2*float(Hf)*np.diag([4.,9.,16.]),np.array([float(duf),0.,0.]),float(PX),float(PXX),float(X))
  target=np.array([float(exact),0.,0.]);actual=np.array([d['phi_tt'][0],d['charge_rate'][0],d['closed_charge_rate'][0]])
  env=np.array([max(abs(float(exact)),float(N)*abs(d['numerator_terms'][0]).sum()/abs(float(PXX-b))),d['charge_rate_envelope'][0],d['closed_charge_rate_envelope'][0]])
  RAW.update({f'fixture_{name}_'+k:v.copy() for k,v in d.items()})
  check('independent_rational_phase_'+name,actual,target,env)

def arm(case):
 global RAW
 RAW={};start=len(CHECKS);CONTEXT.update(sigma=case['sigma'],stage='phase_initial_Euler_rate')
 names=('sample_indices','sample_g','sample_hi','sample_Ga','sample_U','sample_du','sample_phi','chart_Ui','chart_N','chart_beta','P_X','P_XX','p_phi','J_phi','chart_velocity','all_velocity_response','reconstructed_du','reconstructed_dg','owned_isotropic_hdot','phase_u')
 v=read_arrays(case['checkpoint'],names);RAW.update({'input_'+k:a.copy() for k,a in v.items()})
 ix=v['sample_indices'];g=v['sample_g'];hi=v['sample_hi'];U=v['sample_U'];phi=v['sample_phi'];N=v['chart_N'][ix];beta=v['chart_beta'][ix];u=v['chart_Ui'][ix]
 assert g.shape==(8,4,4) and len(ix)==8 and np.array_equal(phi[:,1:],np.zeros((8,3)))
 assert np.array_equal(U[:,1:3],np.zeros((8,2))) and np.array_equal(v['J_phi'][:,1:3],np.zeros((1972,2)))
 assert np.all((v['phase_u'][ix]>0)&(v['phase_u'][ix]<1e-5))
 # The registered seed is stationary and axisymmetric: its old coordinate time jets vanish.
 ga=v['sample_Ga'];left=np.einsum('plm,pln->pmn',ga[:,:,0,:],g);oldgd=left+left.transpose(0,2,1)
 le=np.einsum('plm,pln->pmn',abs(ga[:,:,0,:]),abs(g));oldgd_env=le+le.transpose(0,2,1)
 oldudot=v['chart_velocity'][ix,:3]
 oldudot_env=np.einsum('pia,pa->pi',oldgd_env[:,1:,:],abs(U))+np.einsum('pia,pa->pi',abs(g[:,1:,:]),abs(v['sample_du'][:,0]))
 actual=np.r_[oldgd.ravel(),v['sample_du'][:,0].ravel(),oldudot.ravel()];expected=np.zeros_like(actual)
 env=np.r_[oldgd_env.ravel(),abs(v['sample_du'][:,0]).ravel(),oldudot_env.ravel()]
 check(f's{case["sigma"]}_stationary_circular_initial_charge_subchart',actual,expected,env)
 assert np.array_equal(v['sample_du'][:,0],np.zeros((8,4)))
 values=[]
 for k in range(7):
  gd=v['reconstructed_dg'][k,:,0];Ud=v['sample_du'][:,0]+v['reconstructed_du'][k,:,0]
  ud=v['all_velocity_response'][:,:3,k]
  CONTEXT['direction']=k
  d=phase_rate(g,hi,U,Ud,phi,gd,ud,N,beta,u,v['P_X'][ix],v['P_XX'][ix]);values.append(d)
  RAW.update({f'direction_{k}_'+n:a.copy() for n,a in d.items()})
 out={k:np.stack([d[k] for d in values]) for k in values[0]}
 RAW.update(out)
 charge=out['density']*out['J_phi'][:,:,0];target=np.broadcast_to(v['p_phi'][ix],(7,8))
 pe=out['density']*(abs(out['P_X'][:,:,None]*out['v_phase'])[:,:,0]+abs(out['relative_raised'][:,:,0]))
 check(f's{case["sigma"]}_unchanged_full_pressure_relative_charge',charge,target,pe+abs(target))
 check(f's{case["sigma"]}_independent_four_tensor_initial_current_derivative',out['charge_rate'],np.zeros((7,8)),out['charge_rate_envelope'])
 check(f's{case["sigma"]}_closed_full_charge_Euler_rate',out['closed_charge_rate'],np.zeros((7,8)),out['closed_charge_rate_envelope'])
 r=checkpoint('ARM',RAW,dict(kind='conditional_same_charge_initial_phase_Euler_rate',sigma=case['sigma'],controls=CHECKS[start:],parent_file=case['checkpoint']['file'],parent_sha256=case['checkpoint']['sha256'],directions=['RR','ZZ','phiphi','RZ','Rphi','Zphi','owned_Hbar_isotropic'],gauge='Ndot=betadot=0; stationary circular seed, phi_i=0; first six columns are unit responses, seventh is owned physical expansion increment',unknowns=dict(physical_initial_history=None,whole_slice_constraints=None,metric_exterior=None,activity_outside_support=None),physical_changes=[]))
 return dict(sigma=case['sigma'],status='CONDITIONAL_INITIAL_PHASE_RATE',checkpoint=r)

def admission():
 inputs={}
 for n,h in PINS.items():assert isinstance(h,str) and sha(path(n))==h,n;inputs[n]=h
 assert isinstance(PROTOCOL_SHA,str) and sha(path(STEM+'.md'))==PROTOCOL_SHA
 inputs[STEM+'.md']=PROTOCOL_SHA
 parent=json.loads(path(PARENT+'_RESULT.json').read_text());rc=json.loads(path(PARENT+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==PINS[PARENT+'_RESULT.json'] and parent['status']=='CONDITIONAL_COMPACT_LEGENDRE_ARITHMETIC_PASS'
 assert [c['sigma'] for c in parent['cases']]==list(SIGMAS) and len(parent['controls'])==60 and all(c['passed'] for c in parent['controls'])
 for n,h in rc['input_sha256'].items():assert sha(path(n))==h,n;inputs[n]=h
 for n,h in rc['output_sha256'].items():assert sha(path(n))==h,n;inputs[n]=h
 assert all(v is False for v in parent['qualification'].values())
 fixed=parent['checkpoints'][0]['metadata']['fixed'];cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 return inputs,parent,fixed,cp

def main():
 global np,OWNER,INPUTS,RAW
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Held incomplete root-only phase-rate source; source/protocol admission required.')
 assert not list(BASE.glob(STEM+'_*')),'Own namespace occupied.'
 INPUTS,parent,fixed,cp=admission();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__))
 cases=[]
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(controls=CONTROL_COUNT,pairs=PAIR_COUNT,sigma=list(SIGMAS),local_points=8,directions=7,tolerance=TOL),qualification=FLAGS))
  import numpy as _np
  np=_np
  checkpoint('INPUT',dict(sigma=np.array(SIGMAS)),dict(kind='unchanged_parent_refs',fixed=fixed,owned_EPS5_background=cp['background'],physical_changes=[]))
  RAW={};fixtures(fixed,cp);checkpoint('FIXTURES',RAW,dict(kind='four_independent_phase_charge_controls',controls=list(CHECKS),physical_changes=[]))
  for case in parent['cases']:cases.append(arm(case))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_INITIAL_PHASE_EULER_RATE_PASS',cases=cases,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  recheck();json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS));recheck()
  print('CONDITIONAL_INITIAL_PHASE_EULER_RATE_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_failure=None;closing_failure=None
  if np is not None and RAW:
   try:checkpoint('ERROR_RAW',RAW,dict(kind='unaccepted_available_phase_rate_operands',context=dict(CONTEXT)),allow_failed=True)
   except BaseException:raw_failure=traceback.format_exc()
  try:
   for p in sorted(BASE.glob(STEM+'_*')):
    if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)
   recheck()
  except BaseException:closing_failure=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  orphan_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}]
  orphan_commits=[p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json') if p.name not in {r['commit_file'] for r in RECORDS}]
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_failure,closing_traceback=closing_failure,context=dict(CONTEXT),controls=CHECKS,completed_cases=cases,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=orphan_npz,unqualified_commits=orphan_commits,qualification=FLAGS))
  if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS))
  raise
if __name__=='__main__':main()
