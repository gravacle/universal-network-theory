#!/usr/bin/env python3
"""Root-owned saved proper-plane contraction; no sampler, inverse or field solve."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'
import sys,json,hashlib,math,time,traceback
from pathlib import Path
import numpy as np
J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME='LOCAL_RECORD_FEEDBACK_3D_PROPER_PLANE_SOURCE_PROJECTION_V001'
PARENT='LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001'
PROTOCOL='LOCAL_RECORD_FEEDBACK_3D_PROPER_PLANE_SOURCE_PROJECTION_V002.md'
PINS={PROTOCOL:'68a2f8d00e9892029cbb81e568085fc3793494ea7964d2222fa03a1e1a59211e','LOCAL_RECORD_FEEDBACK_3D_PROPER_PLANE_SOURCE_PROJECTION_V001.md':'7a5cd43ab9e7ae896fd7a3e83a988564a6a2fab00741411f362fb734fcf2ecfe','local_record_feedback_3d_local_energy_source_response_v001.py':'cc10b0836b9105192e210a5e17d877044fa2a64fa0ba826863bebcb521924167',PARENT+'.md':'ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58',PARENT+'_RESULT.json':'389df141d19e496c5989d114b67025605f248c4b1aad80f145400e2395a5cfca',PARENT+'_RECEIPT.json':'7e67d3ce3c2f9f4cb8f76d6f3f69dfad1427dd550a2e99339067051292148e33','LOCAL_PROPER_BOND_NORMALIZATION_V001.md':'9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b','LOCAL_RECORD_FEEDBACK_COMMON_METRIC_SOURCE_RESIDUAL_V001.md':'665545ea6e674105e77b5977eecf9fd37287f19d7f1b273be8116867d2fc4bad','local_record_feedback_3d_local_energy_source_response_v001_saved_authored_acceptance_v002.py':'fb81052f8c9ead0f1deccc432986cf185968329df3c09f44e9670063a3d90c73'}
PATHS={s:J/(NAME+s) for s in ('_RESULT.json','_RESULT.md','_RECEIPT.json','_ERROR.json')}
KS=np.array(((0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)))
U=np.array(((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)))/math.sqrt(3)
B=(U[1:]-U[0]).T
# Analytically fixed chart; np.linalg.solve is a 3x3 coordinate transform, not a response inverse.
K=np.linalg.solve(B.T,(2*math.pi/3)*KS.T).T
A=np.exp(1j*math.pi*KS.sum(axis=1)/6)
C=np.column_stack((np.ones(7),A))/math.sqrt(2)
T=np.column_stack((np.ones((7,6)),np.tile(A[:,None],(1,6)),np.ones(7),A))
CHECKS=[];INPUTS={};STARTED=False

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def value(x):return np.asarray(x['real'])+1j*np.asarray(x['imag']) if isinstance(x,dict) and set(x)=={'real','imag'} else np.asarray(x)
def clean(x):
 if isinstance(x,np.ndarray):return {'real':x.real.tolist(),'imag':x.imag.tolist()} if np.iscomplexobj(x) else x.tolist()
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,complex):return {'real':x.real,'imag':x.imag}
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def write(p,x):
 with Path(p).open('xb') as f:f.write(json.dumps(clean(x),indent=2,sort_keys=True,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
 return sha(p)
def exact(label,ok):
 CHECKS.append({'label':label,'passed':bool(ok)})
 if not ok:raise AssertionError(label)
def close(label,a,b):
 a,b=np.asarray(a),np.asarray(b);e=float(np.linalg.norm(a-b));tol=3e-11*max(1,float(np.linalg.norm(b)));exact(label,bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and e<=tol));CHECKS[-1].update(error=e,allowance=tol)
def pin(p,h):exact('input '+str(p),sha(p)==h);INPUTS[str(Path(p).resolve())]=h

def native(raw):
 e,q=raw['mean_E_dynamic'],raw['mean_Q'];ee=raw['second_E_dynamic']-e[:,:,None]*e[:,None,:].conj();qq=raw['second_Q']-q[:,:,None]*q[:,None,:].conj();qe=raw['second_QE_dynamic']-q[:,:,None]*e[:,None,:].conj();contact=raw['score_contact_C2']
 return {'mean_E_dynamic':e,'chi_EE':4*ee,'chi_QQ':4*qq,'chi_QE':4*qe,'chi_EQ':4*qe.conj().transpose(0,2,1),'score_contact_C2':contact,'R_NN':-4*ee-contact/4}
def project(n):
 scalar=lambda x:np.einsum('ks,kst,kt->k',C,x,C.conj())
 qe=T*np.einsum('kqs,ks->kq',n['chi_QE'],C.conj());eq=np.einsum('ks,ksq->kq',C,n['chi_EQ'])*T.conj();qq=T[:,:,None]*n['chi_QQ']*T[:,None,:].conj()/2
 return {'R_phys':scalar(n['R_NN']),'chi_Ephys':scalar(n['chi_EE']),'C2_phys':scalar(n['score_contact_C2']),'E_phys_dynamic':np.einsum('ks,ks->k',C,n['mean_E_dynamic']),'chi_QhatEphys':qe,'chi_EphysQhat':eq,'chi_QtildeEphys':qe/math.sqrt(2),'chi_EphysQtilde':eq/math.sqrt(2),'chi_QtildeQtilde':qq}
def direct(raw):
 # Transform raw first/second moments before centering as an independent contraction control.
 e=np.einsum('ks,ks->k',C,raw['mean_E_dynamic']);ee=np.einsum('ks,kst,kt->k',C,raw['second_E_dynamic'],C.conj())-e*e.conj();contact=np.einsum('ks,kst,kt->k',C,raw['score_contact_C2'],C.conj());q=T*raw['mean_Q'];qe=T*np.einsum('kqs,ks->kq',raw['second_QE_dynamic'],C.conj())-q*e[:,None].conj()
 return {'R_phys':-4*ee-contact/4,'chi_Ephys':4*ee,'C2_phys':contact,'E_phys_dynamic':e,'chi_QhatEphys':4*qe}
def jackknife(reps):
 a=np.asarray(reps);n=len(a);return {'real_se':np.sqrt((n-1)/n*np.sum((a.real-a.real.mean(0))**2,axis=0)),'imag_se':np.sqrt((n-1)/n*np.sum((a.imag-a.imag.mean(0))**2,axis=0))}
def main():
 global STARTED
 if sys.argv[1:]!=['--execute']:raise SystemExit('Root exact --execute required.')
 if any(p.exists() for p in PATHS.values()):raise SystemExit('Exclusive output exists.')
 STARTED=True;began=time.monotonic()
 for name,h in PINS.items():pin(J/name,h)
 acceptance=J/(PARENT+'_AUTHORED_ACCEPTANCE_V002.json');receipt=J/(PARENT+'_AUTHORED_ACCEPTANCE_RECEIPT_V002.json');report=J/(PARENT+'_AUTHORED_ACCEPTANCE_V002.md');ar=read(receipt);a=read(acceptance)
 for f in (acceptance,receipt,report):pin(f,sha(f))
 exact('accepted authored arithmetic ancestor',ar['audit_status']==a['audit_status']=='PASS' and ar['audit_sha256']==sha(acceptance) and ar['report_sha256']==sha(report) and ar['source_sha256']==a['source_sha256']==PINS['local_record_feedback_3d_local_energy_source_response_v001_saved_authored_acceptance_v002.py'] and a['result_sha256']==ar['result_sha256']==PINS[PARENT+'_RESULT.json'] and a['failed_assertions']==0 and all(c['passed'] for c in a['checks']) and a['input_sha256']==ar['input_sha256'])
 exact('accepted audit complete census',a['check_count']==len(a['checks']) and a['assertions']==ar['assertions'] and a['assertions']>=a['check_count'])
 for f,h in a['input_sha256'].items():pin(f,h)
 p=read(J/(PARENT+'_RESULT.json'));r=read(J/(PARENT+'_RECEIPT.json'))
 exact('parent canonical/report custody',r['result_canonical_sha256']==hashlib.sha256(canonical(p)).hexdigest() and r['report_sha256']==sha(J/(PARENT+'_RESULT.md')));pin(J/(PARENT+'_RESULT.md'),r['report_sha256'])
 exact('full two grid/7mode census',len(p['conditions'])==2 and p['mode_order']==KS.tolist() and p['failed']==0)
 close('signed tetra determinant',np.linalg.det(B),-16/(3*math.sqrt(3)));close('reciprocal cell modes',K@B,(2*math.pi/3)*KS);close('sublattice phase',np.exp(-1j*K@U[0]),A);close('physical squared wave number',np.sum(K*K,axis=1),math.pi**2/3*(np.sum(KS*KS,axis=1)-KS.sum(axis=1)**2/4));close('source normalization',np.sum(abs(C)**2,axis=1),np.ones(7))
 coords=np.array(list(__import__('itertools').product(range(3),repeat=3)));positions=np.concatenate((coords@B.T,coords@B.T+U[0]));f=np.exp(-1j*K@positions.T)/math.sqrt(54);close('7 proper node orthonormal planes',f@f.conj().T,np.eye(7));realplanes=np.array([math.sqrt(2)*v for i in (1,3,5) for v in (f[i].real,f[i].imag)]);close('6 real cos sin source norms',realplanes@realplanes.T,np.eye(6))
 conditions=[]
 for index,row in enumerate(p['conditions']):
  exact('ordered qualified beta4 grids',row['condition']==index and row['beta']==4 and row['M']==(64,128)[index] and row['status']=='FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED' and row['pooled_block_counts']==[32]*128)
  blocks={k:value(v) for k,v in row['pooled_block_raw_moments'].items()};exact('128 paired raw blocks',all(len(v)==128 and np.all(np.isfinite(v)) for v in blocks.values()));raw={k:v.mean(0) for k,v in blocks.items()};n=native(raw)
  for key,v in n.items():close('all7 native '+key,v,value(row['estimates'][key]))
  central=project(n)
  for key,v in direct(raw).items():close('project raw first '+key,v,central[key])
  close('source contact identity',central['R_phys'],-central['chi_Ephys']-central['C2_phys']/4);close('mixed ordered reciprocity',central['chi_QhatEphys'],central['chi_EphysQhat'].conj());close('k0 curvature density',central['R_phys'][0],row['estimates']['uniform_R_density']);close('k0 chi density',central['chi_Ephys'][0],row['estimates']['uniform_energy_susceptibility_density']);close('k0 contact density',central['C2_phys'][0],row['estimates']['uniform_contact_density'])
  for key,v in central.items():
   for plus,minus in ((1,2),(3,4),(5,6)):close('partner reality '+key,v[minus],v[plus].conj())
  for key in ('R_phys','chi_Ephys','C2_phys'):close('scalar imaginary cancellation '+key,central[key].imag,np.zeros(7))
  reps={key:[] for key in central}
  for omit in range(128):
   rp=project(native({k:v[np.arange(128)!=omit].mean(0) for k,v in blocks.items()}))
   for key,v in rp.items():reps[key].append(v)
  conditions.append({'condition':index,'beta':4,'M':row['M'],'central':central,'correlated_128_block_errors':{k:jackknife(v) for k,v in reps.items()},'R_sign_census':{'negative':int(np.sum(central['R_phys'].real<0)),'positive':int(np.sum(central['R_phys'].real>0)),'zero':int(np.sum(central['R_phys'].real==0))}})
 difference={k:{'signed_M64_minus_M128':conditions[0]['central'][k]-conditions[1]['central'][k],'independent_grid_component_errors':{part:np.sqrt(conditions[0]['correlated_128_block_errors'][k][part]**2+conditions[1]['correlated_128_block_errors'][k][part]**2) for part in ('real_se','imag_se')}} for k in conditions[0]['central']}
 for f,h in INPUTS.items():exact('final input '+f,sha(f)==h)
 result={'status':'PASS','PID':os.getpid(),'checks':CHECKS,'conditions':conditions,'mode_order':KS,'proper_Kell':K,'sublattice_phase':A,'primitive_volume_over_ell3':16/(3*math.sqrt(3)),'Sbar_continuum_chart_only':8/(3*math.sqrt(3))*np.sum(K*K,axis=1),'nonzero_proper_wavelength_over_ell':4,'C0_restore':'E_phys_full(k0)=E_phys_dynamic(k0)+sqrt(54)*(AR+Sself); no chosen constant','grid_difference':difference,'input_sha256':INPUTS,'source_sha256':sha(__file__),'elapsed_seconds':time.monotonic()-began,'scope':'Saved fixed proper chart contraction of ONE finite-beta environment at two discretizations. No response inverse, long-wave window, fitted G, source selection, environmental contrast or self-generated field.'}
 rh=write(PATHS['_RESULT.json'],result)
 with PATHS['_RESULT.md'].open('x') as out:
  out.write('# Proper-plane source projection V001\n\nAll seven supplied modes, both beta4 discretizations, full finite-M contact and correlated128-block errors retained. Qhat retains per-cell channel normalization; Qtilde uses per-node channel normalization. Nonzero wavelength=4ell; no continuum/long-wave qualification or gravitational field solve.\n\n|M|k|R_phys|correlated SE|\n|---|---|---:|---:|\n')
  for row in conditions:
   for i,k in enumerate(KS):out.write('|%d|%s|%.12g|%.12g|\n'%(row['M'],k.tolist(),row['central']['R_phys'][i].real,row['correlated_128_block_errors']['R_phys']['real_se'][i]))
  out.write('\nAll signs and full mixed-source outputs are in JSON. The two M values represent one environment. Calibrated total G reference matching, physical body loading and mixed/spatial action remain required for the two-potential common-field calculation.\n');out.flush();os.fsync(out.fileno())
 for f,h in INPUTS.items():
  if sha(f)!=h:raise AssertionError('post-output input changed '+f)
 rr=write(PATHS['_RECEIPT.json'],{'status':'PASS','PID':os.getpid(),'result_sha256':rh,'result_canonical_sha256':hashlib.sha256(canonical(clean(result))).hexdigest(),'report_sha256':sha(PATHS['_RESULT.md']),'source_sha256':sha(__file__),'input_sha256':INPUTS,'check_count':len(CHECKS)})
 print(json.dumps({'status':'PASS','result_sha256':rh,'receipt_sha256':rr,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
if __name__=='__main__':
 try:main()
 except Exception as e:
  if STARTED and not PATHS['_ERROR.json'].exists():write(PATHS['_ERROR.json'],{'status':'FAILED_PRESERVED','error':repr(e),'traceback':traceback.format_exc(),'checks':CHECKS,'input_sha256':INPUTS,'source_sha256':sha(__file__)})
  print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
