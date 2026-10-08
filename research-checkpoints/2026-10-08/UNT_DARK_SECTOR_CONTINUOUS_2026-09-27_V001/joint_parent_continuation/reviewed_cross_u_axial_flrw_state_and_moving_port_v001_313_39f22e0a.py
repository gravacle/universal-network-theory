"""Root-only reusable axial FLRW pointwise RHS/ports; fixed arithmetic, no history."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, traceback

AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_AXIAL_FLRW_STATE_AND_MOVING_PORT_V001'
PARENT='CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001'
PROTOCOL_SHA='f772429c75535c94e94edc3cf6e20b9b409460a1108b3eb617714846ad1a44f3'
PINS={
 'CROSS_U_EPS5_TRANSVERSE_AXIAL_CAUSAL_EXTERIOR_AND_PORTS_V001.md':'47ab4d4281345ea69c01e3d063d63c05cbdd56706aa4920c02ddf6d0418e841b',
 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md':'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0',
 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md':'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986',
 'cross_u_saved_native_local_temporal_curvature_v001.py':'96e73bafada42c134bf84bada1a9f3414921c196f2a5f0ff18265b203a54e8d6',
 'CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001.md':'7e5f08b5b34b67188eba1fdb7c741a1d788ffe12db30da46758d646c46e3e904',
 'CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_RECEIPT.json':'ebe0d2051f46349cc16f0b6cb4d918131c4a9f85e16e26bba96eafcd3ae9c660',
 'CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_OWNER_START.json':'4c05d0e1e1583161912bc3284130275133eebd706a0a8140029f5acf02167aff',
 'CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_00000_INPUT.npz':'af1280ff9879d15409a4f3840134ea52e1428025b43d194ab50a6e21ede11c21',
 'CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_00000_INPUT.npz.COMMIT.json':'bfaf01a0a6cb8e1a2334dc02773a3f0243eac8d994e94f92862b1197e5b2f3f7',
 'CROSS_U_SAVED_NATIVE_LOCAL_TEMPORAL_CURVATURE_V001_00001_LOCAL_CURVATURE.npz.COMMIT.json':'62954f53a29cf7f56821572eca914d09f5306abef390d82681768cde26066dce'}
KB=.02; C=1.98; ELL=.1; L0=3.085677581491367e19; CP=299792458.
SIGMAS=(.1,1.,10.,100.); TOL=2e-11; CONTROL_COUNT=24; PAIR_COUNT=5
np=None; OWNER=None; INPUTS={}; OUTPUTS={}; RECORDS=[]; RAW={}; CONTEXT={}; CHECKS=[]
FLAGS={k:False for k in ('physical_temporal_spectrum_qualified','physical_Cauchy_state_qualified',
 'physical_boundary_history_qualified','physical_exterior_qualified','full_coupled_characteristics_qualified',
 'full_galaxy_junction_qualified','active_source_mapping_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}

def now():return datetime.now(timezone.utc).isoformat()
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Nonfinite or unsupported metadata: '+type(v).__name__)
def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def publish(n,b):
 p=path(n)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==b;OUTPUTS[n]=sha(p);return OUTPUTS[n]
def json_file(n,v):return publish(n,encode(v))
def scalar(v,name):
 x=float(v)
 if not math.isfinite(x):raise ValueError(name+' must be finite.')
 return x
def array(v,name):
 a=np.asarray(v)
 if a.dtype.kind not in 'fiu' or not np.all(np.isfinite(a)):raise ValueError(name+' must be finite real numeric data.')
 return a.astype(np.float64,copy=False)
def finite_math(f):
 def wrapped(*args,**kw):
  with np.errstate(over='raise',divide='raise',invalid='raise'):
   try:return f(*args,**kw)
   except (FloatingPointError,OverflowError,ZeroDivisionError) as e:raise ValueError('Invalid derived axial arithmetic.') from e
 return wrapped

class AxialFLRW:
 """c=1, lengths in L0 and time in L0/cp; caller supplies H,Q and spatial jets.

 State columns: u, p=P/M^2, z[32], v=D_t z[32], each in this geometric chart.
 No propagator, ordinary-current model, exterior inverse or initial state is selected.
 """
 def __init__(self,xi,w,eta,sigma,ell=ELL):
  global np
  if np is None:
   import numpy as _np
   np=_np
  self.available={};self.xi=array(xi,'xi').copy();self.w=array(w,'weights').copy()
  if self.xi.shape!=(32,) or self.w.shape!=(32,) or not np.all((self.xi>0)&(self.xi<=1)) or not np.all(self.w>0):raise ValueError('Actual positive 32-mode layout required.')
  self.eta=scalar(eta,'eta');self.sigma=scalar(sigma,'sigma');self.ell=scalar(ell,'ell')
  if self.eta<=0 or self.ell<=0 or self.sigma not in SIGMAS:raise ValueError('Positive proper eta/ell and one declared sigma required.')
  with np.errstate(over='raise',divide='raise',invalid='raise'):
   self.omega=self.sigma*self.xi*self.eta;self.omega2=self.omega**2
  if not np.all(np.isfinite(self.omega2)) or not np.all(self.omega2>0):raise ValueError('Derived frequencies must be positive finite.')
 def inputs(self,R,l,y,yr,yrr,H,Q):
  R=array(R,'R');y=array(y,'state');yr=array(yr,'state_R');yrr=array(yrr,'state_RR')
  if R.ndim!=1 or not np.all(R>0) or type(l) is not int or l<1:raise ValueError('R>0 and integer harmonic l>=1 required.')
  if y.shape!=(len(R),66) or yr.shape!=y.shape or yrr.shape!=y.shape:raise ValueError('State and both spatial jets must be N by 66.')
  return R,l,y,yr,yrr,scalar(H,'H'),scalar(Q,'Q')
 @finite_math
 def radial_operator(self,R,l,f,fr,frr):
  R=array(R,'R');f=array(f,'f');fr=array(fr,'f_R');frr=array(frr,'f_RR')
  if R.ndim!=1 or not np.all(R>0) or type(l) is not int or l<1 or f.ndim<1 or f.shape[0]!=len(R) or fr.shape!=f.shape or frr.shape!=f.shape:raise ValueError('Invalid radial operator data.')
  self.available.update(current_R=R,current_operator_f=f,current_operator_f_R=fr,current_operator_f_RR=frr)
  r=R.reshape((len(R),)+(1,)*(f.ndim-1));out=-frr-2*fr/r+l*(l+1)*f/r**2
  self.available['current_K']=out
  if not np.all(np.isfinite(out)):raise ValueError('Nonfinite K_l output.')
  return out
 @finite_math
 def rhs(self,R,l,y,yr,yrr,H,Q):
  R,l,y,yr,yrr,H,Q=self.inputs(R,l,y,yr,yrr,H,Q)
  u,p=y[:,0],y[:,1];z,v=y[:,2:34],y[:,34:66]
  Z=z@self.w;E=(p-C*Z)/KB;K=self.radial_operator(R,l,y,yr,yrr)
  self.available.update(current_state=y,current_state_R=yr,current_state_RR=yrr,current_Z=Z,current_E=E)
  intrinsic=np.column_stack((E-H*u,-2*H*p-KB*K[:,0]-C*Q**2*u,v,
   -3*H*v-self.omega2*(z+self.ell**2*K[:,2:34])+self.omega2*E[:,None]))
  advection=H*R[:,None]*yr;out=intrinsic-advection
  self.available.update(current_D_t_state=intrinsic,current_advection=advection,current_rhs=out)
  if not all(np.all(np.isfinite(a)) for a in (Z,E,K,intrinsic,advection,out)):raise ValueError('Nonfinite axial RHS.')
  return dict(rhs=out,D_t_state=intrinsic,advection=advection,E=E,Z=Z,K_state=K)
 @finite_math
 def moving_ports(self,R,l,y,yr,yrr,H,Q,Vb):
  R,l,y,yr,yrr,H,Q=self.inputs(R,l,y,yr,yrr,H,Q);Vb=array(Vb,'tube peculiar velocity')
  if Vb.shape!=R.shape or not np.all(abs(Vb)<1):raise ValueError('Timelike tube requires |Vb|<1.')
  gamma=1/np.sqrt(1-Vb**2);p=y[:,1];v=y[:,34:66];zr=yr[:,2:34]
  self.available.update(current_port_state=y,current_port_state_R=yr,current_Vb=Vb,current_gamma=gamma)
  curl=yr[:,0]+y[:,0]/R
  Pu=np.column_stack((p,-KB*curl))
  Pz=np.stack((C*self.w*v/self.omega2,-C*self.w*self.ell**2*zr),axis=-1)
  normal=np.column_stack((-gamma*Vb,gamma))
  outU=np.sum(normal*Pu,axis=-1);outz=np.sum(normal[:,None,:]*Pz,axis=-1)
  self.available.update(current_conormal=normal,current_U_momentum=Pu,current_mode_momenta=Pz,current_U_port=outU,current_mode_ports=outz)
  if not all(np.all(np.isfinite(a)) for a in (gamma,Pu,Pz,normal,outU,outz)):raise ValueError('Nonfinite conormal data.')
  return dict(U_port_over_Msq=outU,mode_ports_over_Msq=outz,conormal=normal,U_momentum_over_Msq=Pu,mode_momenta_over_Msq=Pz,gamma=gamma,Vb=Vb,curl_radial=curl)
 @finite_math
 def work_ledger(self,R,l,y,yr,yrr,H,Q,Qdot):
  R,l,y,yr,yrr,H,Q=self.inputs(R,l,y,yr,yrr,H,Q);Qdot=scalar(Qdot,'Qdot')
  data=self.rhs(R,l,y,yr,yrr,H,Q);dt=data['D_t_state'];E=data['E'];L=l*(l+1);r=R[:,None]
  u,p=y[:,0],y[:,1];z,v=y[:,2:34],y[:,34:66];zr,vr=yr[:,2:34],yr[:,34:66]
  Er=(yr[:,1]-C*(zr@self.w))/KB;curl=yr[:,0]+u/R;curlR=yrr[:,0]+yr[:,0]/R-u/R**2
  dtE=(dt[:,1]-C*(v@self.w))/KB;dtcurl=Er+E/R-2*H*curl
  energy_terms=np.column_stack((KB*E**2/2,KB*(curl**2+L*u**2/R**2)/2,C*Q**2*u**2/2,
   C*(v**2/self.omega2)@self.w/2,C*(z**2)@self.w/2,C*self.ell**2*(zr**2+L*z**2/r**2)@self.w/2))
  self.available['current_energy_terms']=energy_terms
  flux_terms=np.column_stack((KB*E*curl,C*self.ell**2*(v*zr)@self.w))
  self.available['current_flux_terms']=flux_terms
  Dt_terms=np.column_stack((KB*E*dtE,KB*curl*dtcurl,KB*L*u*(E-2*H*u)/R**2,
   C*Q*Qdot*u**2,C*Q**2*u*dt[:,0],C*(v*dt[:,34:66]/self.omega2)@self.w,
   C*(z*v)@self.w,C*self.ell**2*(zr*(vr-H*zr)+L*z*(v-H*z)/r**2)@self.w))
  self.available['current_Dt_energy_terms']=Dt_terms
  div_terms=np.column_stack((KB*Er*curl,KB*E*(curlR+2*curl/R),
   C*self.ell**2*(vr*zr+v*yrr[:,2:34]+2*v*zr/r)@self.w))
  self.available['current_div_flux_terms']=div_terms
  work_terms=np.column_stack((-2*H*E*p,-2*H*KB*(curl**2+L*u**2/R**2),C*(Q*Qdot-H*Q**2)*u**2,
   -3*H*C*(v**2/self.omega2)@self.w,-H*C*self.ell**2*(zr**2+L*z**2/r**2)@self.w))
  self.available['current_background_work_terms']=work_terms
  Dt_energy=Dt_terms.sum(axis=1);div_flux=div_terms.sum(axis=1);work=work_terms.sum(axis=1)
  balance=Dt_energy-div_flux-work;env=abs(Dt_terms).sum(axis=1)+abs(div_terms).sum(axis=1)+abs(work_terms).sum(axis=1)
  out=dict(energy=energy_terms.sum(axis=1),flux=flux_terms.sum(axis=1),energy_terms=energy_terms,flux_terms=flux_terms,
   Dt_energy_terms=Dt_terms,div_flux_terms=div_terms,background_work_terms=work_terms,Dt_energy=Dt_energy,div_flux=div_flux,background_work=work,balance=balance,absolute_envelope=env)
  if not all(np.all(np.isfinite(a)) for a in out.values()):raise ValueError('Nonfinite inclusive work ledger.')
  return out

def authenticate():
 ins=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});r=json.loads(path(PARENT+'_RECEIPT.json').read_text());o=json.loads(path(PARENT+'_OWNER_START.json').read_text())
 assert r['status']=='CLOSED' and r['owner']==o and o['owner']=='root' and o['pid']==95397 and r['closed']>o['started']
 assert o['source_sha256']==PINS['cross_u_saved_native_local_temporal_curvature_v001.py']
 for k,h in dict(r['input_sha256'],**r['output_sha256']).items():
  assert k not in ins or ins[k]==h,('Input seal conflict',k);ins[k]=h
 for k,h in ins.items():assert sha(path(k))==h,('Input changed',k)
 rec=json.loads(path(PARENT+'_00000_INPUT.npz.COMMIT.json').read_text());hm=json.loads(path(PARENT+'_00001_LOCAL_CURVATURE.npz.COMMIT.json').read_text())
 for c in (rec,hm):
  assert set(c)=={'file','sha256','metadata'} and c['metadata']['owner']==o and r['output_sha256'][c['file']]==c['sha256']
 assert rec['file']==PARENT+'_00000_INPUT.npz' and rec['metadata']['kind']=='authentic_closed_FINE_Q3_input'
 for k in ('current_xi','current_weights'):assert rec['metadata']['schema'][k]==dict(shape=[32],dtype='float64',finite=True)
 assert hm['metadata']['kind']=='conditional_local_q_zero_curvatures'
 tree=ast.parse(path('cross_u_saved_native_local_temporal_curvature_v001.py').read_text())
 hs=[ast.literal_eval(a.value) for a in tree.body if isinstance(a,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HUNIT' for t in a.targets)]
 assert len(hs)==1 and hs[0]==hm['metadata']['Hunit']
 return ins,rec,scalar(hs[0],'owned Hunit')
def load_layout(rec):
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata']))==rec['metadata'];xi=f['current_xi'].copy();RAW['current_xi']=xi
  w=f['current_weights'].copy();RAW['current_weights']=w
 RAW.update(current_xi=xi,current_weights=w)
 assert xi.shape==w.shape==(32,) and xi.dtype==w.dtype==np.dtype('float64')
 assert np.all(np.isfinite(xi)) and np.all(np.isfinite(w)) and np.all((xi>0)&(xi<=1)) and np.all(w>0)
 return xi,w
def check(name,actual,expected,envelope=None):
 ordinal=len(CHECKS);CONTEXT.update(current_control=name,current_control_ordinal=ordinal)
 a=np.asarray(actual);b=np.asarray(expected);prefix=f'control_{ordinal:03d}_{name}'
 RAW[prefix+'_actual']=a.copy();RAW[prefix+'_expected']=b.copy()
 if envelope is not None:RAW[prefix+'_envelope']=np.asarray(envelope).copy()
 assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
 env=max(1e-30,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0))) if envelope is None else max(1e-30,float(np.max(array(envelope,'control envelope'),initial=0)))
 gap=float(np.max(abs(a-b),initial=0));err=gap/env;assert all(math.isfinite(x) for x in (env,gap,err))
 row=dict(ordinal=ordinal,name=name,absolute_gap=gap,envelope=env,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row)
 return row
def checkpoint(tag,arrays,meta):
 md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
 text=encode(md).decode();md=json.loads(text);name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);rec=dict(file=name,sha256=sha(p),metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);OUTPUTS[name]=rec['sha256'];RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert set(f.files)==set(arrays)|{'metadata_json'} and str(f['metadata_json'])==text
  for k,a in arrays.items():assert f[k].dtype==a.dtype and f[k].shape==a.shape and np.array_equal(f[k],a,equal_nan=True)
 return rec
def seal_created():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)
def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('Input changed',n)
 assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER) and sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('Output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for k,s in r['metadata']['schema'].items():assert f[k].shape==tuple(s['shape']) and str(f[k].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[k])))==s['finite']
 if strict:
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}
def fixture(xi,w):
 R=np.array([.8,1.3,2.1]);c=np.zeros((66,4));c[0]=[0,1,.25,0]
 c[2:34]=xi[:,None]*np.array([1,1,.5,0])[None,:]/10
 c[34:66]=xi[:,None]*np.array([2,-1,0,1/6])[None,:]/7
 c[1]=KB*np.array([2,0,1/3,0])+C*(w@c[2:34])
 y=sum(c[:,n][None,:]*R[:,None]**n for n in range(4))
 yr=sum(n*c[:,n][None,:]*R[:,None]**(n-1) for n in range(1,4))
 yrr=sum(n*(n-1)*c[:,n][None,:]*R[:,None]**(n-2) for n in range(2,4))
 return R,c,y,yr,yrr
def global_controls(comp,hunit):
 R,c,y,yr,yrr=fixture(comp.xi,comp.w);RAW.update(fixture_R=R,polynomial_coefficients=c,fixture_state=y,fixture_state_R=yr,fixture_state_RR=yrr)
 check('proper_eta_units',np.array(comp.eta),np.array((hunit*1000/(1000*L0))*L0/CP))
 ks=[];ex=[]
 for l in (1,3):
  L=l*(l+1);ks.append(comp.radial_operator(R,l,y,yr,yrr));ex.append(sum((L-n*(n+1))*c[:,n][None,:]*R[:,None]**(n-2) for n in range(4)))
 check('K_monomials_l1_l3',np.stack(ks),np.stack(ex))
 f=1+R**2/3;fr=2*R/3;frr=np.full(R.shape,2/3);h=R+R**3/5;hr=1+3*R**2/5;hrr=6*R/5
 Kg=comp.radial_operator(R,3,h,hr,hrr);Kf=comp.radial_operator(R,3,f,fr,frr)
 RAW.update(green_f=f,green_f_R=fr,green_f_RR=frr,green_g=h,green_g_R=hr,green_g_RR=hrr,K_green_f=Kf,K_green_g=Kg)
 check('radial_Green_boundary',R**2*(f*Kg-h*Kf),2*R*(h*fr-f*hr)+R**2*(h*frr-f*hrr))
 u=y[:,0];ur=yr[:,0]
 check('curl_actual_boundary',R**2*((ur+u/R)**2-ur**2),u**2+2*R*u*ur)
 return R,c,y,yr,yrr
def arm_controls(comp,R,c,y,yr,yrr):
 H=1/32;Q=3/20;Qdot=-1/70;l=3;L=l*(l+1)
 RAW.update(fixture_R=R,polynomial_coefficients=c,fixture_state=y,fixture_state_R=yr,fixture_state_RR=yrr,omega=comp.omega,omega_squared=comp.omega2,
  supplied_artificial_H=np.array(H),supplied_artificial_Q=np.array(Q),supplied_artificial_Qdot=np.array(Qdot))
 a=comp.rhs(R,l,y,yr,yrr,H,Q)
 for k,v in a.items():RAW['rhs_'+k]=v.copy()
 Kclosed=sum((L-n*(n+1))*c[:,n][None,:]*R[:,None]**(n-2) for n in range(4));Eclosed=2+R**2/3
 dt=np.column_stack((Eclosed-H*y[:,0],-2*H*y[:,1]-KB*Kclosed[:,0]-C*Q**2*y[:,0],y[:,34:66],
  -3*H*y[:,34:66]+comp.omega2*(Eclosed[:,None]-y[:,2:34]-ELL**2*Kclosed[:,2:34])))
 RAW.update(closed_monomial_K=Kclosed,independent_E=Eclosed,independent_D_t_state=dt)
 check('sigma_'+str(comp.sigma)+'_comoving_rows',a['D_t_state'],dt)
 check('sigma_'+str(comp.sigma)+'_Eulerian_advection',a['rhs'],dt-H*R[:,None]*yr)
 ports=[];expected=[]
 for Vb in (-H*R,np.full(R.shape,.25),np.full(R.shape,-.3)):
  port=comp.moving_ports(R,l,y,yr,yrr,H,Q,Vb);ports.append(np.column_stack((port['U_port_over_Msq'],port['mode_ports_over_Msq'])))
  gb=1/np.sqrt(1-Vb**2);expected.append(np.column_stack((-gb*(KB*(yr[:,0]+y[:,0]/R)+Vb*y[:,1]),
   -C*comp.w*gb[:,None]*(Vb[:,None]*y[:,34:66]/comp.omega2+ELL**2*yr[:,2:34]))))
  for k,v in port.items():RAW[f'port_{len(ports)-1}_'+k]=v.copy()
 check('sigma_'+str(comp.sigma)+'_moving_conormal',np.stack(ports),np.stack(expected))
 for tag,h,qd in [('flat',0.,0.),('FLRW_work',H,Qdot)]:
  e=comp.work_ledger(R,l,y,yr,yrr,h,Q,qd)
  for k,v in e.items():RAW[tag+'_'+k]=v.copy()
  check('sigma_'+str(comp.sigma)+'_'+tag+'_inclusive_energy',e['balance'],np.zeros_like(R),e['absolute_envelope'])

def main():
 global np,OWNER,INPUTS
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64,'Guarded author draft: root review/freeze required.'
 assert not list(BASE.glob(STEM+'_*')),'Unused exclusive namespace required; no replay.'
 INPUTS,rec,hunit=authenticate();sh=sha(__file__);INPUTS[str(Path(__file__).resolve())]=sh
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sh);arms=[];comp=None
 try:
  json_file(STEM+'_OWNER_START.json',OWNER)
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_layout_file=rec['file'],sigmas=SIGMAS,controls=CONTROL_COUNT,pairs=PAIR_COUNT,
   geometric_units=dict(length_m=L0,time_seconds=L0/CP,light_speed=1,H_and_Q='caller supplied geometric phase-background fields'),
   state_order=['u','p=P/Msq','z[32]','v=D_t_z[32]'],qualification=FLAGS))
  import numpy as _np
  np=_np
  xi,w=load_layout(rec);eta=hunit/CP;RAW.update(owned_Hunit=np.array(hunit),eta=np.array(eta))
  comp=AxialFLRW(xi,w,eta,SIGMAS[0]);fixture_data=global_controls(comp,hunit)
  checkpoint('LAYOUT_AND_CONTROLS',dict(RAW),dict(kind='unchanged_owned_layout_and_fixed_analytic_controls',controls=list(CHECKS),weights_sum=float(w.sum()),weights_renormalized=False,Hunit=hunit,eta=eta))
  for sigma in SIGMAS:
   RAW.clear();start=len(CHECKS);CONTEXT.update(stage='fixed_artificial_arm',sigma=sigma)
   comp=AxialFLRW(xi,w,eta,sigma);arm_controls(comp,*fixture_data)
   cp=checkpoint('SIGMA_'+str(sigma),dict(RAW),dict(kind='pointwise_operator_advection_conormal_and_work_controls',sigma=sigma,controls=CHECKS[start:],background='explicit artificial supplied fields; no physical history'))
   arms.append(dict(sigma=sigma,status='ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS[start:]) else 'ARITHMETIC_FAILED',checkpoint_file=cp['file'],checkpoint_sha256=cp['sha256']))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT
  status='COMPONENT_ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS) else 'ARITHMETIC_FAILED'
  result=dict(owner=OWNER,status=status,controls=CHECKS,checkpoints=RECORDS,arms=arms,expected_controls=CONTROL_COUNT,expected_pairs=PAIR_COUNT,qualification=FLAGS,
   unknown_inputs={k:None for k in ('actual_phase_background_H_Q_history','boundary_worldtube_history','ordinary_current_and_stress','Cauchy_and_incoming_state','metric_vector_constraint_solution','physical_inertia_and_graph_map','active_source_outside_measured_support','scalar_TT_and_full_galaxy_junction')})
  recheck();rh=json_file(STEM+'_RESULT.json',result)
  publish(STEM+'_REPORT.md',('# '+STEM+'\n\n'+status+'. Pointwise 66-field RHS and moving weak-port component; 24 artificial implementation controls, no trajectory or physical initial/exterior state.\n\nThe positive quadratic work ledger is not the full normal source or coordinate Legendre energy. Unknown active support remains unknown; no final orbital force is computed.\n').encode());recheck()
  receipt=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS)
  json_file(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads(path(STEM+'_RECEIPT.json').read_text())==receipt
  print(json.dumps(dict(status=status,controls=len(CHECKS),pairs=len(RECORDS),result_sha256=rh),sort_keys=True));return 0 if status=='COMPONENT_ARITHMETIC_PASS' else 3
 except BaseException:
  failure=traceback.format_exc();raw_failure=None;closing_failure=None;prior=path(STEM+'_RECEIPT.json');prior_sha=sha(prior) if prior.exists() else None
  if comp is not None:RAW.update(comp.available)
  try:
   if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_current_operands',context=CONTEXT,traceback=failure))
  except BaseException:raw_failure=traceback.format_exc()
  seal_created()
  try:
   if path(STEM+'_OWNER_START.json').exists():recheck(strict=False)
  except BaseException:closing_failure=traceback.format_exc()
  unpaired=sorted(({p.name for p in BASE.glob(STEM+'_*.npz')}|{p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')})-{r['file'] for r in RECORDS}-{r['commit_file'] for r in RECORDS})
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,failed=now(),traceback=failure,raw_preservation_traceback=raw_failure,closing_preservation_traceback=closing_failure,context=CONTEXT,controls=CHECKS,
   checkpoints=RECORDS,completed_arms=arms,unqualified_partial_pair_files=unpaired,preserved_outputs=dict(OUTPUTS),existing_receipt_sha256=prior_sha,qualification=FLAGS))
  if prior_sha is None:
   receipt=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS)
   json_file(STEM+'_RECEIPT.json',receipt)
   if closing_failure is None and path(STEM+'_OWNER_START.json').exists():recheck(strict=False)
   assert json.loads(prior.read_text())==receipt
  else:
   if closing_failure is None and path(STEM+'_OWNER_START.json').exists():recheck(strict=False)
   assert sha(prior)==prior_sha
  raise

if __name__=='__main__':raise SystemExit(main())
