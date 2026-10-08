"""Two-ordinary-parameter BBN+theta development calibration, then unfit BAO.

Prospective model: SAME K(X), .251 clock,.7 constant,epsilon1e-6,Q0/Hunit100,
KB.02,lambda98,physical a0,Gcos/GN.98. Fit physical GN-omega_b and Hunit
to D/H2.527e-5 and100theta1.0411. Hunit bracket55..80, omega_b.018...026,
at most10 safeguarded secants in each nested root, residual1e-6.
All other parameters/functional/state assumptions remain counted/adopted.
Use BBN YPCMB and fixed-NEVO output Neff in recombination, not former
adopted.245/3.046. This changes the thermal inputs explicitly, no new fit.
All data previously exposed. NO independent validation/superiority claim.
BAO uses the identical stored13-point covariance, NO ruler/BAO fit.
Matched pressureless reference is an ablation at the same parameters/Gcos,
not a best-fit GN LCDM comparison. BBN uses the qualified fixed-NEVO,
dust-clock approximation, inherited baryon-rest H omission, no rate errors.
Numerical gates inherited: BBN D/H5e-5, helium1e-5; atomic xe/Tm2e-3,
observables2e-4,thinning1e-4,quad2e-8,H interpolation2e-7/1e-5.
Final fitted residuals D/H5e-5,theta2e-6. Failures retain receipts.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import subprocess
import time
import numpy as np
import invariant_clock_bbn_v002 as previous
import invariant_clock_acoustic_v001 as acoustic
import invariant_clock_acoustic_bao_v001 as bao

J=Path(__file__).resolve().parent
ROOT=previous.ROOT;OLD=previous.OLD;B=previous.B
PREFIX='INVARIANT_CLOCK_JOINT_CALIBRATION_V002'
OUT=J/(PREFIX+'_RESULT.json')
CSRC=J/'invariant_clock_joint_cal_bbn_v002.c'
OBJ=J/'invariant_clock_joint_cal_bbn_v002.o'
EXE=J/'invariant_clock_joint_cal_bbn_v002'
sha=previous.sha
controls=[];trials=[];calls=[];frozen={}
def save(name,x):
 with (J/(PREFIX+'_'+name+'.json')).open('x') as f:
  json.dump(x,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
def command(label,argv):
 t=time.monotonic()
 p=subprocess.run([str(v) for v in argv],cwd=ROOT,capture_output=True,text=True,timeout=30)
 rec=dict(argv=[str(v) for v in argv],returncode=p.returncode,
          seconds=time.monotonic()-t,stdout=p.stdout,stderr=p.stderr)
 save(label,rec);calls.append(dict(label=label,sha256=sha(J/(PREFIX+'_'+label+'.json'))))
 if p.returncode:raise RuntimeError(label+' failed')
 return p.stdout
def check(name,value,gate):
 controls.append(dict(name=name,error=float(value),gate=gate,passed=bool(value<=gate)))
def root(fun,lo,hi,label):
 left=fun(lo);right=fun(hi)
 if left[0]*right[0]>=0:raise RuntimeError(label+' bracket failed')
 for _ in range(10):
  z=(lo*right[0]-hi*left[0])/(right[0]-left[0])
  if not lo<z<hi:z=(lo+hi)/2
  rr=fun(z)
  if abs(rr[0])<=1e-6:return z,rr[1]
  if rr[0]*left[0]>0:lo,left=z,rr
  else:hi,right=z,rr
 raise RuntimeError(label+' root budget exhausted')
def main():
 started=time.monotonic()
 if Path.cwd().resolve()!=ROOT or OUT.exists() or OBJ.exists() or EXE.exists():
  raise RuntimeError('wrong root or existing outputs')
 if os.environ.get('CPR_NN_DEBUG'):raise RuntimeError('debug forbidden')
 for p,s in previous.PINNED.items():
  if sha(p)!=s:raise RuntimeError('old pin changed')
  frozen[str(p)]=s
 fr=json.loads((OLD/'PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json').read_text())
 for p,s in fr['files'].items():
  if sha(ROOT/p)!=s:raise RuntimeError('old frozen input changed')
 objects=[]
 for rec in json.loads((OLD/'PRIMAT_ORDINARY_BUILD_V001.json').read_text())['payload']['commands']:
  if sha(Path(rec['path']))!=rec['sha256']:raise RuntimeError('old receipt changed')
  rr=json.loads(Path(rec['path']).read_text())['payload']
  if sha(Path(rr['output']['path']))!=rr['output']['sha256']:raise RuntimeError('old object changed')
  if rr['command']['kind']=='compile' and rr['command']['id']!='adapter':objects.append(rr['output']['path'])
 if len(objects)!=22:raise RuntimeError('object census')
 for p in (CSRC,Path(__file__),Path(acoustic.__file__),Path(bao.__file__),Path(previous.__file__),
           Path(acoustic.plasma.__file__),Path(acoustic.plasma.prior.old.base.__file__),
           acoustic.plasma.prior.old.base.SOURCE,
           J/'INVARIANT_CLOCK_BBN_V001_SAME_DENSITY_GN_REFINED.json'):
  frozen[str(p)]=sha(p)
 bbnp=J/'INVARIANT_CLOCK_BBN_V002_RESULT.json'
 if sha(bbnp)!='7e005a416b84634f2d720f76fa95a8b0311e3f4cbd211d679a22382720cf59f8':
  raise RuntimeError('qualified BBN changed')
 frozen[str(bbnp)]=sha(bbnp)
 builds=acoustic.authenticate()
 command('COMPILE',['/usr/bin/clang','-std=gnu11','-O2','-Wall','-Wextra','-pthread','-I'+str(B/'upstream/primat-c/include'),'-c',CSRC,'-o',OBJ])
 command('LINK',['/usr/bin/clang',*objects,OBJ,'-lm','-pthread','-o',EXE])
 counter=0
 def bbn(h,omega,profile='default'):
  nonlocal counter
  counter+=1
  res=json.loads(command('BBN_%03d'%counter,[EXE,profile,'candidate',repr(h),repr(omega)]))
  if res['status']!='COMPLETE_FIXED_NEVO_SCREEN':raise RuntimeError('BBN control failure')
  p=res['physical']
  check('BBN_fixed_vacuum_%03d'%counter,abs((p['h']**2-p['omega_b']-p['omega_c'])/(h/100)**2/.7-1),2e-12)
  check('BBN_density_label_%03d'%counter,abs(p['omega_b']/(.98*omega)-1),2e-12)
  if not all(c['passed'] for c in controls):raise RuntimeError('density bookkeeping failed')
  return res
 # New adapter identity against qualified fixed-calibration point, no new fit.
 # Preserve the EXACT stored GN-control density label, not the one-ulp
 # different physical-density report from the cosmology's exponentiation.
 # V001's failed overly strict identity with a different floating input is
 # retained. No control tolerance or scientific parameter changes.
 old_GN=json.loads(json.loads((J/'INVARIANT_CLOCK_BBN_V001_SAME_DENSITY_GN_REFINED.json').read_text())['stdout'])
 identity=bbn(68.06502010698708,old_GN['physical']['omega_b'],'refined')
 old=json.loads(bbnp.read_text())['finals']['candidate_refined']['final']
 for k,v in old.items():check('adapter_identity_'+k,abs(identity['final'][k]/v-1),5e-10)
 if not all(c['passed'] for c in controls):raise RuntimeError('adapter identity failed')
 seed=json.loads(acoustic.plasma.prior.old.base.SOURCE.read_text())
 seed['inherited']['Q0_over_H0']=100.
 def model_at(h,omega):
  saved=json.loads(json.dumps(seed))
  saved['inherited']['H0_km_s_Mpc']=h
  saved['inherited']['omega_b_cos']=omega*.98/(h/100)**2
  return acoustic.plasma.prior.old.base.Model(saved,1)
 def thermal(b):
  acoustic.plasma.NEFF=b['final']['Neff']
  acoustic.plasma.RN=(7/8)*(4/11)**(4/3)*acoustic.plasma.NEFF
  acoustic.plasma.YHE=b['final']['YPCMB']
 def evaluate(h):
  local=[]
  def br(omega):
   b=bbn(h,omega);r=b['final']['DoH']/2.527e-5-1
   local.append(dict(omega_b=omega,residual=r,final=b['final']))
   return r,b
  omega,b=root(br,.018,.026,'BBN')
  thermal(b);bg=acoustic.Background(model_at(h,omega))
  label='JOINT2_%02d'%len(trials)
  atom,inv=acoustic.invoke(bg,'default',label,builds)
  obs=acoustic.observables(bg,atom);r=obs['theta100']/acoustic.PLANCK_THETA100-1
  trial=dict(Hunit=h,omega_b=omega,OB=bg.model.OB,BBN_trials=local,BBN=b['final'],
             atomic_invocation=inv,observables=obs,residual=r)
  trials.append(trial)
  print(json.dumps(dict(Hunit=h,omega_b=omega,theta100=obs['theta100'],residual=r)),flush=True)
  return r,dict(trial=trial,atom=atom,bbn=b)
 h,selected=root(evaluate,55.,80.,'CMB_theta')
 trial=selected['trial'];omega=trial['omega_b']
 bbf=bbn(h,omega,'refined');bbd=selected['bbn']
 check('BBN_DoH_refinement',abs(bbd['final']['DoH']/bbf['final']['DoH']-1),5e-5)
 for k in ('YPBBN','YPCMB'):check('BBN_'+k+'_refinement',abs(bbd['final'][k]-bbf['final'][k]),1e-5)
 check('final_BBN_calibration',abs(bbf['final']['DoH']/2.527e-5-1),5e-5)
 thermal(bbf);model=model_at(h,omega)
 oldbao=json.loads(bao.OUT.read_text())
 if sha(bao.OUT)!='684da639c34341ba965f06f4b695e9a8f6b3b30e06a47385e92c2bae9b95f4f8':raise RuntimeError('BAO changed')
 frozen[str(bao.OUT)]=sha(bao.OUT)
 data=np.array(oldbao['data']);chol=np.linalg.cholesky(np.array(oldbao['covariance']))
 rows=[]
 for dust in (False,True):
  bg=acoustic.Background(model,dust);kind='REFERENCE' if dust else 'CANDIDATE'
  ca,di=acoustic.invoke(bg,'default','JOINT2_FINAL_'+kind+'_DEFAULT',builds)
  fa,fi=acoustic.invoke(bg,'half','JOINT2_FINAL_'+kind+'_HALF',builds)
  ob=acoustic.observables(bg,fa);oc=acoustic.observables(bg,ca)
  thin=acoustic.observables(bg,fa,thinning=2);quad=acoustic.observables(bg,fa,nquad=128)
  cc=np.array(ca['rows']);ff=np.array(fa['rows'])[::2]
  if cc.shape!=ff.shape or np.max(abs(cc[:,0]-ff[:,0]))>1e-12:raise RuntimeError('atomic grids')
  check(kind+'_xe',np.max(abs(cc[:,1]-ff[:,1])/np.maximum(1e-3,abs(ff[:,1]))),2e-3)
  check(kind+'_Tm',np.max(abs(cc[:,2]/ff[:,2]-1)),2e-3)
  keys=('zstar','rs_Mpc','DM_Mpc','theta100','drag_redshift_interval','drag_ruler_Mpc_interval')
  for k in keys:
   v=np.array(ob[k])
   check(kind+'_'+k+'_atomic',np.max(abs(np.array(oc[k])/v-1)),2e-4)
   check(kind+'_'+k+'_thinning',np.max(abs(np.array(thin[k])/v-1)),1e-4)
   check(kind+'_'+k+'_quadrature',np.max(abs(np.array(quad[k])/v-1)),2e-8)
  inv=dict(default=di,half=fi)
  if not dust:
   alt,ai=acoustic.invoke(bg,'default','JOINT2_FINAL_HGRID',builds,alternate=True)
   ao=acoustic.observables(bg,alt);inv['alternate']=ai
   check('H_grid_pointwise',ai['native_alternate_H_relative_error'],2e-7)
   for k in keys:check(k+'_H_grid',np.max(abs(np.array(ao[k])/np.array(oc[k])-1)),1e-5)
   check('final_theta_calibration',abs(ob['theta100']/acoustic.PLANCK_THETA100-1),2e-6)
  physical=bao.vector(bg,96);coarse=bao.vector(bg,48);ind=bao.vector(bg,96,True)
  check(kind+'_BAO_gauss',np.max(abs(coarse/physical-1)),2e-12)
  check(kind+'_BAO_independent',np.max(abs(ind/physical-1)),2e-11)
  w=np.linalg.solve(chol,physical);wd=np.linalg.solve(chol,data)
  low,high=ob['drag_ruler_Mpc_interval'];ys=[1/high,1/low]
  ymin=float(w@wd/(w@w))
  if ys[0]<ymin<ys[1]:ys.append(ymin)
  scores=[float((y*w-wd)@(y*w-wd)) for y in ys]
  rows.append(dict(kind=kind,H_today=h*float(bg.E(1.)),observables=ob,
   DESI_score_interval=[min(scores),max(scores)],invocations=inv,
   physical_omega_b=bg.omega_b,omega_radiation=bg.OR))
 check('input_bytes_preserved',float(any(sha(Path(p))!=s for p,s in frozen.items())),0)
 result=dict(protocol=__doc__,status='COMPLETED_TWO_PARAMETER_DEVELOPMENT_CALIBRATION',
  all_controls_passed=all(c['passed'] for c in controls),controls=controls,
  selected=dict(Hunit=h,physical_omega_b=omega,OB=model.OB,BBN=bbf['final'],
   eta0b=bbf['physical']['eta0b'],YHe=acoustic.plasma.YHE,Neff=acoustic.plasma.NEFF,
   BBN_library_physical=bbf['physical'],
   BBN_library_h_note='Only Lambda density bookkeeping, not Hunit or present H'),
  fitted_freedoms=2,fixed=model.p,trials=trials,rows=rows,hashes=frozen,BBN_calls=calls,
  elapsed_seconds=time.monotonic()-started)
 save('RESULT',result)
 print(json.dumps(dict(status=result['status'],all_controls_passed=result['all_controls_passed'],
  selected=result['selected'],rows=[{k:v for k,v in r.items() if k!='invocations'} for r in rows],
  failed=[c for c in controls if not c['passed']],elapsed_seconds=result['elapsed_seconds'],
  receipt_sha256=sha(OUT)),indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:
  save('FAILED_ATTEMPT',dict(error=repr(e),controls=controls,trials=trials,calls=calls,
       hashes=frozen,source_sha256=sha(Path(__file__))))
  raise

