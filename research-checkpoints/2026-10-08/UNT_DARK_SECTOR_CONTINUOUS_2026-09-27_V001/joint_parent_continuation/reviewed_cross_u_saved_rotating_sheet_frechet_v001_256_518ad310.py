"""Guarded saved ordinary rotating-sheet Frechet block; no correction applied."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001'
PARENT='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
PROTOCOL_SHA='e1ea987af25cf02dab2460e555f59b13691fefee254e83e1789a1c3a28281f05'
PINS={'cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68','CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001.md':'88fbf64e1568af3f47f1346b809c6d8a35fe7b685a73817938616b9056068e24','CROSS_U_FULL_METRIC_CONSTRAINED_WEAK_VARIATION_SCOPE_V001.md':'2b927d54354eec7f8e8018960c7920c12d8099c070c42c2577cae1af8fe4dad7',PARENT+'_RESULT.json':'ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798',PARENT+'_RECEIPT.json':'eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde'}
PARENT_PID=13990
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10;B=A0*KPC/LIGHT**2
SIGMAS=(.1,1.,10.,100.);TOL=2e-11;CONTROL_COUNT=19;PAIR_COUNT=6
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];RAW={};ARM_AVAILABLE={};CONTEXT={};CHECKS=[]
FLAGS={k:False for k in ('correction_applied','stationary_Euler_solution_qualified','angular_momentum_history_qualified','full_coupled_Hessian_qualified','full_metric_solution_qualified','physical_junction_qualified','active_source_mapping_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}

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


def array(v,name):
 a=np.asarray(v)
 if a.dtype.kind not in 'fiu' or not np.all(np.isfinite(a)):raise ValueError(name+' must be finite real numeric data.')
 return a.astype(np.float64,copy=False)


def check(name,actual,expected,envelope=None):
 ordinal=len(CHECKS);CONTEXT.update(current_control=name,current_control_ordinal=ordinal)
 a=np.asarray(actual);b=np.asarray(expected);prefix=f'control_{ordinal:03d}_{name}'
 RAW[prefix+'_actual']=a.copy();RAW[prefix+'_expected']=b.copy()
 if envelope is not None:RAW[prefix+'_envelope']=np.asarray(envelope).copy()
 assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
 env=max(1e-30,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0))) if envelope is None else max(1e-30,float(np.max(array(envelope,'control envelope'),initial=0)))
 gap=float(np.max(abs(a-b),initial=0));err=gap/env;assert all(math.isfinite(x) for x in (env,gap,err))
 row=dict(ordinal=ordinal,name=name,absolute_gap=gap,envelope=env,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row)
 assert row['passed'],name
 return row


def checkpoint(tag,arrays,meta):
 md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
 text=encode(md).decode();md=json.loads(text);name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
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
 assert sha(__file__)==OWNER['source_sha256']
 if strict:assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('Output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for k,s in r['metadata']['schema'].items():assert f[k].shape==tuple(s['shape']) and str(f[k].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[k])))==s['finite']
 if strict:
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}


def selected_arrays(file,names):
 out={}
 with np.load(path(file),allow_pickle=False) as f:
  for k in names:
   a=f[k].copy();RAW['loaded_'+k]=a
   assert a.dtype==np.dtype('float64') and np.all(np.isfinite(a));out[k]=a
 return out


def metric_partial(g,Ga):
 a=np.einsum('plam,pln->pamn',Ga,g)
 return a+np.swapaxes(a,2,3)

def block(g,dg,k,D,q,dq,weight):
 # q_i and its coordinate jet are held numeric tensors, not retetraded.
 g=array(g,'metric');dg=array(dg,'metric jet');k=array(k,'worldline');D=array(D,'worldline D');q=array(q,'metric directions');dq=array(dq,'metric direction jets');weight=array(weight,'mass weights')
 p=len(D);m=len(q);assert g.shape==(p,4,4) and dg.shape==(p,4,4,4) and k.shape==(p,4) and q.shape==(m,p,4,4) and dq.shape==(m,p,4,4,4) and weight.shape==(p,)
 assert np.all(D>0) and np.all(g[:,3,3]>0) and np.all(weight>=0) and np.all(k[:,0]==1) and np.all(k[:,1:3]==0)
 RAW.update(current_metric=g,current_metric_jet=dg,current_worldline_k=k,current_D=D,current_mass_weight=weight,current_metric_directions=q,current_metric_direction_jets=dq)
 sd=np.sqrt(D);A=np.einsum('pa,ipab,pb->ip',k,q,k);Ar=np.einsum('pa,ipab,pb->ip',k,dq[:,:,1],k)
 RAW.update(current_sqrtD=sd,current_qkk=A,current_dR_qkk=Ar)
 J=np.einsum('pa,pa->p',g[:,3,:],k);Jr=np.einsum('pa,pa->p',dg[:,1,3,:],k);Ji=np.einsum('ipa,pa->ip',q[:,:,3,:],k)
 RAW.update(current_J=J,current_dR_J=Jr,current_delta_J=Ji)
 N=-np.einsum('pa,pab,pb->p',k,dg[:,1],k)/2;a=N/D
 Di=-A;Ni=-Ar/2;DO=-2*J;NO=-Jr
 RAW.update(current_N_R=N,current_radial_Euler=a,current_delta_D=Di,current_delta_N_R=Ni,current_D_Omega=DO,current_N_R_Omega=NO)
 ai=Ni/D[None,:]-a[None,:]*Di/D[None,:];aO=NO/D-a*DO/D
 RAW.update(current_delta_radial_Euler=ai,current_radial_Euler_Omega=aO)
 momentum=J/sd;pi=Ji/sd[None,:]-J[None,:]*Di/(2*D[None,:]**1.5);pO=g[:,3,3]/sd-J*DO/(2*D**1.5)
 RAW.update(current_p_phi=momentum,current_delta_p_phi=pi,current_p_phi_Omega=pO)
 first=weight[None,:]*A/(2*sd[None,:]);mixed=weight[None,:]*(Ji/sd[None,:]+A*J[None,:]/(2*D[None,:]**1.5))
 RAW.update(current_source_first=first,current_source_metric_Omega=mixed)
 curvature_weight=weight/(4*D**1.5);H=np.einsum('ip,p,jp->ij',A,curvature_weight,A)
 Henv=np.einsum('ip,p,jp->ij',abs(A),curvature_weight,abs(A));RAW.update(current_curvature_weight=curvature_weight,current_metric_Hessian=H,current_metric_Hessian_envelope=Henv)
 angular_first=weight*momentum;angular_second=weight*(g[:,3,3]/sd+J*J/D**1.5)
 RAW.update(current_source_Omega=angular_first,current_source_Omega_Omega=angular_second)
 env_aO=abs(NO)/D+abs(a*DO)/D;nondegenerate=aO!=0
 conditioning=np.zeros(p);np.divide(abs(aO),env_aO,out=conditioning,where=env_aO>0)
 # No inversion, Omega step, orbit root choice, displaced annulus or new state.
 out=dict(metric=g,metric_jet=dg,worldline_k=k,D=D,mass_weight=weight,metric_directions=q,metric_direction_jets=dq,qkk=A,dR_qkk=Ar,J=J,dR_J=Jr,delta_J=Ji,N_R=N,radial_Euler=a,delta_D=Di,delta_N_R=Ni,delta_radial_Euler=ai,D_Omega=DO,N_R_Omega=NO,radial_Euler_Omega=aO,radial_Euler_Omega_envelope=env_aO,Omega_nondegenerate=nondegenerate,Omega_reciprocal_condition=conditioning,p_phi=momentum,delta_p_phi=pi,p_phi_Omega=pO,source_first=first,source_metric_Omega=mixed,source_Omega=angular_first,source_Omega_Omega=angular_second,metric_Hessian=H,metric_Hessian_envelope=Henv,curvature_weight=curvature_weight)
 for name,v in out.items():
  RAW['current_'+name]=v
  assert np.all(np.isfinite(v)),name
 return out

def scaled_check(name,actual,expected,envelope):
 a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);assert a.shape==b.shape==e.shape
 scale=np.maximum(e,1e-30);label=f'raw_{len(CHECKS):03d}_{name}'
 RAW[label+'_actual']=a.copy();RAW[label+'_expected']=b.copy();RAW[label+'_envelope']=e.copy();RAW[label+'_scale']=scale.copy()
 return check(name,a/scale,b/scale,np.ones_like(a))

def fixtures():
 R=3.;O=1/5;g=np.diag([-1.,1.,1.,R*R])[None,:,:];dg=np.zeros((1,4,4,4));dg[:,1,3,3]=2*R;k=np.array([[1.,0.,0.,O]]);D=np.array([16/25]);q=np.zeros((3,1,4,4));dq=np.zeros((3,1,4,4,4))
 q[0,:,0,0]=1/7;q[1,:,3,3]=R*R/13;q[2,:,0,3]=q[2,:,3,0]=R/11
 dq[1,:,1,3,3]=2*R/13;dq[2,:,1,0,3]=dq[2,:,1,3,0]=1/11
 v=block(g,dg,k,D,q,dq,np.ones(1));ARM_AVAILABLE.update({'fixture_'+n:a.copy() for n,a in v.items()})
 actual=np.array([v['radial_Euler'][0],v['radial_Euler_Omega'][0],v['p_phi'][0],v['p_phi_Omega'][0]]);expected=np.array([-3/16,-375/128,9/4,1125/64])
 scaled_check('independent_flat_rotating_Euler_and_momentum',actual,expected,np.maximum(abs(actual),abs(expected)))
 A=np.array([[1/7],[9/325],[6/55]]);Ar=np.array([[0.],[6/325],[2/55]]);Ji=np.array([[0.],[9/65],[3/11]])
 ai=-25*Ar/32-75*A/256;pi=5*Ji/4+225*A/128
 actual=np.concatenate((v['delta_radial_Euler'].ravel(),v['delta_p_phi'].ravel()));expected=np.concatenate((ai.ravel(),pi.ravel()))
 RAW.update(flat_fixture_qkk_independent=A,flat_fixture_dR_qkk_independent=Ar,flat_fixture_delta_J_independent=Ji)
 scaled_check('independent_flat_metric_Euler_and_momentum_jets',actual,expected,np.maximum(abs(actual),abs(expected)))
 H=125*A@A.T/256;actual=np.concatenate((v['metric_Hessian'].ravel(),v['source_metric_Omega'].ravel(),v['source_first'].ravel()));expected=np.concatenate((H.ravel(),pi.ravel(),(5*A/8).ravel()))
 scaled_check('independent_flat_worldline_second_contacts',actual,expected,np.maximum(abs(actual),abs(expected)))

def admission():
 pins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64 and (n not in pins or pins[n]==h);pins[n]=h
 for n,h in PINS.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA);add(__file__,sha(__file__))
 rc=json.loads(path(PARENT+'_RECEIPT.json').read_text());assert rc['status']=='CLOSED' and rc['closed'] and rc['owner']['owner']=='root' and rc['owner']['pid']==PARENT_PID
 for field in ('input_sha256','output_sha256'):
  for n,h in rc[field].items():add(n,h)
 for n,h in pins.items():assert sha(path(n))==h,('input seal',n)
 assert rc['owner']['source_sha256']==PINS['cross_u_saved_full_metric_native_source_residual_v001.py'] and rc['result_sha256']==PINS[PARENT+'_RESULT.json']
 assert path(PARENT+'_RESULT.json').stat().st_size<32*1024*1024
 result=json.loads(path(PARENT+'_RESULT.json').read_text());assert result['owner']==rc['owner'] and result['status']=='CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS'
 assert len(result['controls'])==36 and all(c['passed'] for c in result['controls']) and [c['sigma'] for c in result['cases']]==list(SIGMAS)
 assert len(result['checkpoints'])==6 and all(v is False for v in result['qualification'].values())
 for rec in result['checkpoints']:
  assert pins[str(path(rec['file']).resolve())]==rec['sha256'] and pins[str(path(rec['commit_file']).resolve())]==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
  assert rec['metadata']['owner']==rc['owner'] and all(v is False for v in rec['metadata']['qualification'].values()) and all(v['finite'] for v in rec['metadata']['schema'].values())
 assert result['checkpoints'][0]['metadata']['schema']['source_samples32']==dict(shape=[4832,9],dtype='float64',finite=True)
 for case in result['cases']:assert case['checkpoint'] in result['checkpoints'] and case['checkpoint']['metadata']['sigma']==case['sigma'] and case['status']=='CONDITIONAL_FULL_METRIC_WEAK_MEASURES'
 return pins,result

def arm(case,source):
 global RAW,ARM_AVAILABLE
 RAW={};ARM_AVAILABLE={};start=len(CHECKS);sig=case['sigma'];CONTEXT.update(stage='ordinary_source_Frechet',sigma=sig)
 names=['source_g','source_Ga','source_k','source_D','source_radial_material_Euler']
 names += [f'b{b}_d{i}_source_{suffix}' for b in range(2) for i in range(10) for suffix in ('metric_test','metric_test_partial','worldline_derivative')]
 vals=selected_arrays(case['checkpoint']['file'],names);ARM_AVAILABLE.update({n:v.copy() for n,v in vals.items()})
 g,Ga,k,D=(vals[n] for n in ('source_g','source_Ga','source_k','source_D'));dg=metric_partial(g,Ga)
 q=np.stack([vals[f'b{b}_d{i}_source_metric_test'] for b in range(2) for i in range(10)]);dq=np.stack([vals[f'b{b}_d{i}_source_metric_test_partial'] for b in range(2) for i in range(10)])
 weight=B*source[:,7];v=block(g,dg,k,D,q,dq,weight);ARM_AVAILABLE.update({n:a.copy() for n,a in v.items() if n not in ('metric','worldline_k','D','metric_directions','metric_direction_jets')})
 D_expected=-np.einsum('pa,pab,pb->p',k,g,k);Denv=np.einsum('pa,pab,pb->p',abs(k),abs(g),abs(k));aenv=np.einsum('pa,pab,pb->p',abs(k),abs(dg[:,1]),abs(k))/(2*D)
 inherited=np.stack([vals[f'b{b}_d{i}_source_worldline_derivative'] for b in range(2) for i in range(10)])
 actual=np.concatenate((D.ravel(),v['radial_Euler'].ravel(),v['source_first'].ravel()));expected=np.concatenate((D_expected.ravel(),vals['source_radial_material_Euler'].ravel(),inherited.ravel()));env=np.concatenate((Denv.ravel(),aenv.ravel(),np.maximum(abs(v['source_first']),abs(inherited)).ravel()))
 scaled_check(f's{sig}_unchanged_D_Euler_and_metric_source',actual,expected,env)
 actual=np.concatenate((v['delta_radial_Euler']*D[None,:]+v['radial_Euler'][None,:]*v['delta_D'],v['radial_Euler_Omega'][None,:]*D[None,:]+v['radial_Euler'][None,:]*v['D_Omega'][None,:]),axis=0)
 expected=np.concatenate((v['delta_N_R'],v['N_R_Omega'][None,:]),axis=0);env=np.concatenate((abs(v['delta_radial_Euler']*D[None,:])+abs(v['radial_Euler'][None,:]*v['delta_D']),abs(v['radial_Euler_Omega'][None,:]*D[None,:])+abs(v['radial_Euler'][None,:]*v['D_Omega'][None,:])),axis=0)
 scaled_check(f's{sig}_Euler_Frechet_quotient',actual,expected,env)
 sd=np.sqrt(D);actual=np.concatenate((sd[None,:]*v['delta_p_phi']+v['p_phi'][None,:]*v['delta_D']/(2*sd[None,:]),(sd*v['p_phi_Omega']+v['p_phi']*v['D_Omega']/(2*sd))[None,:],v['source_metric_Omega']),axis=0)
 expected=np.concatenate((v['delta_J'],g[:,3,3][None,:],weight[None,:]*v['delta_p_phi']),axis=0)
 env=np.concatenate((sd[None,:]*abs(v['delta_p_phi'])+abs(v['p_phi'][None,:]*v['delta_D'])/(2*sd[None,:]),(sd*abs(v['p_phi_Omega'])+abs(v['p_phi']*v['D_Omega'])/(2*sd))[None,:],weight[None,:]*(abs(v['delta_J'])/sd[None,:]+abs(v['qkk']*v['J'][None,:])/(2*D[None,:]**1.5))),axis=0)
 scaled_check(f's{sig}_angular_momentum_and_mixed_source_contacts',actual,expected,env)
 c=np.array([(-1.)**i/(i+1) for i in range(20)]);Ac=c@v['qkk'];direct=np.einsum('ip,p,p->i',v['qkk'],v['curvature_weight'],Ac);H=v['metric_Hessian']
 Acenv=abs(c)@abs(v['qkk']);actual=np.concatenate((H.ravel(),(H@c).ravel()));expected=np.concatenate((H.T.ravel(),direct.ravel()));env=np.concatenate((v['metric_Hessian_envelope'].ravel(),np.einsum('ip,p,p->i',abs(v['qkk']),v['curvature_weight'],Acenv)))
 RAW.update(Hessian_fixed_probe=c,Hessian_qkk_probe=Ac,Hessian_qkk_probe_envelope=Acenv,Hessian_matrix_action=H@c,Hessian_independent_node_action=direct)
 scaled_check(f's{sig}_fixed_worldline_Hessian_symmetry_and_action',actual,expected,env)
 # Successful pairs keep each copied input once; transient aliases remain available on error.
 ARM_AVAILABLE.update({n:a.copy() for n,a in RAW.items() if not n.startswith(('loaded_','current_'))});rec=checkpoint('ARM',ARM_AVAILABLE,dict(kind='ordinary_rotating_sheet_first_second_source_and_Euler_contacts',sigma=sig,controls=CHECKS[start:],parent_file=case['checkpoint']['file'],parent_sha256=case['checkpoint']['sha256'],Omega='independent; no update applied',unknowns=dict(material_displacement_history=None,conserved_angular_momentum_initial_data=None,full_metric_correction=None,physical_exterior=None,active_outside_support=None)))
 ARM_AVAILABLE={};return dict(sigma=sig,status='CONDITIONAL_ORDINARY_SOURCE_FRECHET_BLOCK',checkpoint=rec,Omega_nondegenerate_count=int(np.count_nonzero(v['Omega_nondegenerate'])),Omega_degenerate_count=int(np.count_nonzero(~v['Omega_nondegenerate'])),qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded prospective root-only source; parent closure binding and FULL review required.')
 assert not list(BASE.glob(STEM+'_*')),'Own runtime namespace occupied.'
 INPUTS,parent=admission();cases=[];OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_file=PARENT+'_RESULT.json',configuration=dict(controls=CONTROL_COUNT,pairs=PAIR_COUNT,sigma=SIGMAS,tolerance=TOL),qualification=FLAGS))
  import numpy as _np
  np=_np
  source=selected_arrays(parent['checkpoints'][0]['file'],('source_samples32',))['source_samples32'];assert source.shape==(4832,9) and np.all(source[:,7]>=0)
  checkpoint('INPUT',dict(source_samples32=source),dict(kind='unchanged_fixed_rest_mass_annular_samples',parent_file=parent['checkpoints'][0]['file'],parent_sha256=parent['checkpoints'][0]['sha256'],copied_metric_controls=parent['controls'],physical_changes=[]))
  fixtures();available=dict(ARM_AVAILABLE);available.update(RAW);checkpoint('ARITHMETIC_FIXTURES',available,dict(kind='three_independent_flat_rotating_worldline_controls',controls=list(CHECKS)))
  for case in parent['cases']:
   with np.errstate(over='raise',invalid='raise',divide='raise'):cases.append(arm(case,source))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT and all(c['passed'] for c in CHECKS)
  result=dict(owner=OWNER,status='CONDITIONAL_ORDINARY_SOURCE_FRECHET_ARITHMETIC_PASS',cases=cases,controls=CHECKS,checkpoints=RECORDS,parent_file=PARENT+'_RESULT.json',parent_sha256=PINS[PARENT+'_RESULT.json'],qualification=FLAGS)
  recheck();rh=json_file(STEM+'_RESULT.json',result);publish(STEM+'_REPORT.md',(f'# {STEM}\n\n{CONTROL_COUNT} arithmetic controls, four saved ordinary rotating-source blocks.\n\nIndependent Euler and angular-momentum Jacobians retained. No Omega, source, metric or physical velocity correction applied. Full coupled gravity/background/junction and active mapping remain unqualified.\n').encode())
  recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc);recheck();print(result['status'],CONTROL_COUNT,len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_failure=None;closing_failure=None;available=dict(ARM_AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_ordinary_source_operands',context=CONTEXT))
   except BaseException:raw_failure=traceback.format_exc()
  try:seal_created();recheck(False)
  except BaseException:closing_failure=traceback.format_exc()
  name=STEM+'_RECEIPT.json';prior=sha(path(name)) if path(name).exists() else None
  if prior:OUTPUTS[name]=prior
  unknown_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}];unknown_commit=[p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json') if p.name not in {r['commit_file'] for r in RECORDS}]
  error=dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_failure,closing_traceback=closing_failure,context=CONTEXT,checkpoints=RECORDS,controls=CHECKS,completed_cases=cases,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=unknown_npz,unqualified_commits=unknown_commit,qualification=FLAGS)
  eh=json_file(STEM+'_ERROR.json',error)
  if prior is None:
   rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc)
  recheck(False);raise

if __name__=='__main__':main()
