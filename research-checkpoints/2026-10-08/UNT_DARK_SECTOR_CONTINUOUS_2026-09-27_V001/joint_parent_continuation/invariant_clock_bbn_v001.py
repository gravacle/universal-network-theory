"""Fixed current CMB-calibration BBN prediction; five small serial runs.

Prospective controls (declared before execution): old-point final abundances
relative 5e-10; nuclear refinement D/H relative5e-5, both helium fractions
absolute1e-5; equal physical eta and a(T)2e-12; G-only H ratio2e-12.
Inherited raw abundance >=-1e-12, baryon conservation1e-8.
No observational acceptance gate, tuning, Monte Carlo, new NEVO or rate tables.
Output preserves complete histories and every failed invocation exclusively.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import time
import numpy as np

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=Path(__file__).resolve().parent
B=J/'bbn_inputs_v001/primat_c_reference_v001'
OLD=B/'build_ordinary_v001'
PREFIX='INVARIANT_CLOCK_BBN_V001'
OUT=J/(PREFIX+'_RESULT.json')
SOURCE=J/'invariant_clock_bbn_v001.c'
BINARY=J/'invariant_clock_bbn_v001'
OBJECT=J/'invariant_clock_bbn_v001.o'
PINNED={
 OLD/'PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json':'1ef54049931289f2c8715d56f080566e1aecb01e483aada8681fe7b985d7ed00',
 OLD/'PRIMAT_ORDINARY_BUILD_V001.json':'6a9ef5f2be2cad88e643444c5ec3628815ca2bc351ab9a86028c7df1aa940e74',
 OLD/'receipts/run_refined.json':'0c76bc2b05e9a821de3c411b5441cbb8f0b1ba8127d2f90bc4b18444e8320475',
 J/'INVARIANT_CLOCK_CMB_CALIBRATION_V001_RESULT.json':'af1a41ed9b0d0f1ea2f2d8ac7ee9df67d2a3282989d09e019bbe3959c68ee9e1',
}
def sha(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):
 with (J/(PREFIX+'_'+name+'.json')).open('x') as f:
  json.dump(x,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
def invoke(name,argv):
 start=time.monotonic()
 p=subprocess.run([str(v) for v in argv],cwd=ROOT,env=os.environ.copy(),
                  text=True,capture_output=True,timeout=30)
 result=dict(argv=[str(v) for v in argv],seconds=time.monotonic()-start,
             returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
 save(name,result)
 if p.returncode:raise RuntimeError(name+' returned '+str(p.returncode))
 return p.stdout
def main():
 if Path.cwd().resolve()!=ROOT or OUT.exists() or OBJECT.exists() or BINARY.exists():
  raise RuntimeError('wrong root or existing outputs; no overwrite/relaunch')
 if os.environ.get('CPR_NN_DEBUG'):raise RuntimeError('debug override forbidden')
 started=time.monotonic()
 evidence={str(p):sha(p) for p in PINNED}
 if evidence!= {str(p):s for p,s in PINNED.items()}:raise RuntimeError('pinned input changed')
 frozen=json.loads((OLD/'PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json').read_text())
 for p,s in frozen['files'].items():
  if sha(ROOT/p)!=s:raise RuntimeError('old frozen source/data changed: '+p)
 build=json.loads((OLD/'PRIMAT_ORDINARY_BUILD_V001.json').read_text())['payload']
 objects=[]
 for record in build['commands']:
  p=Path(record['path'])
  if sha(p)!=record['sha256']:raise RuntimeError('old command receipt changed')
  rec=json.loads(p.read_text())['payload']
  if sha(Path(rec['output']['path']))!=rec['output']['sha256']:
   raise RuntimeError('old compiled output changed')
  if rec['command']['kind']=='compile' and rec['command']['id']!='adapter':
   objects.append(Path(rec['output']['path']))
 if len(objects)!=22:raise RuntimeError('library object census changed')
 source_sha=sha(SOURCE); runner_sha=sha(Path(__file__))
 invoke('COMPILE',['/usr/bin/clang','-std=gnu11','-O2','-Wall','-Wextra','-pthread',
  '-I'+str(B/'upstream/primat-c/include'),'-c',SOURCE,'-o',OBJECT])
 invoke('LINK',['/usr/bin/clang',*objects,OBJECT,'-lm','-pthread','-o',BINARY])
 runs={}
 for mode,profile in [('identity','refined'),('candidate','default'),
                      ('candidate','refined'),('same_density_GN','default'),
                      ('same_density_GN','refined')]:
  key=mode+'_'+profile
  runs[key]=json.loads(invoke(key.upper(),[BINARY,profile,mode]))
  if runs[key]['status']!='COMPLETE_FIXED_NEVO_SCREEN':
   raise RuntimeError(key+' producer controls failed')
 tests=[]
 def check(name,value,gate):
  tests.append(dict(name=name,value=float(value),gate=gate,passed=bool(value<=gate)))
 old=json.loads((OLD/'receipts/run_refined.json').read_text())['payload']['result']
 ident=runs['identity_refined']
 for k,v in old['final'].items():
  check('identity_'+k,abs(ident['final'][k]/v-1),5e-10)
 for mode in ('candidate','same_density_GN'):
  fine=runs[mode+'_refined'];coarse=runs[mode+'_default']
  check(mode+'_DoH_refinement',abs(coarse['final']['DoH']/fine['final']['DoH']-1),5e-5)
  for k in ('YPBBN','YPCMB'):check(mode+'_'+k+'_refinement',abs(coarse['final'][k]-fine['final'][k]),1e-5)
 cand=runs['candidate_refined'];ref=runs['same_density_GN_refined']
 check('equal_eta',abs(cand['physical']['eta0b']/ref['physical']['eta0b']-1),2e-12)
 bc=np.array(cand['background'],dtype=float);br=np.array(ref['background'],dtype=float)
 if bc.shape!=br.shape:raise RuntimeError('fixed thermal grids differ')
 for col in (1,2,4,5,6,7):
  check('same_thermal_grid_column_'+str(col),np.max(abs(bc[:,col]/br[:,col]-1)),2e-12)
 check('G_only_H_ratio',np.max(abs(bc[:,3]/br[:,3]/math.sqrt(.98)-1)),2e-12)
 check('input_source_preserved',float(sha(SOURCE)!=source_sha),0)
 check('old_data_preserved',float(any(sha(ROOT/p)!=s for p,s in frozen['files'].items())),0)
 # Approximation screens at actual fixed NEVO temperature grid, not abundance bounds.
 G=cand['physical']['GN_SI']; H=bc[:,3];a=bc[:,2]
 rho_clock=cand['physical']['omega_c']*3*(100./3.085677581491367e19)**2/(8*math.pi*G)/a**3
 rho_included=3*H**2/(8*math.pi*G)
 baryon_ratio=bc[:,7]*1000./rho_included
 clock_fraction=rho_clock/rho_included
 # Stable sqrt(1+x)-1 for small x.
 baryon_delta=baryon_ratio/(np.sqrt(1+baryon_ratio)+1)
 eps=1e-6
 clock_bound=.5*(eps/(math.sqrt(1+eps)+1))*clock_fraction
 screens=[]
 for T in (1.,.1,.01,.001):
  i=int(np.argmin(abs(bc[:,1]-T)))
  screens.append(dict(T_MeV=bc[i,1],a=a[i],baryon_omission_deltaH_overH=baryon_delta[i],
   clock_dust_deltaH_bound=clock_bound[i],clock_fraction=clock_fraction[i]))
 observations={}
 for mode in ('candidate','same_density_GN'):
  v=runs[mode+'_refined']['final']
  observations[mode]=dict(DoH=v['DoH'],YPBBN=v['YPBBN'],YPCMB=v['YPCMB'],
   DoH_signed_observation_only_sigma=(v['DoH']-2.527e-5)/.030e-5,
   YPBBN_signed_observation_only_sigma=(v['YPBBN']-.2453)/.0034,
   YPCMB_minus_adopted_HYREC_helium=v['YPCMB']-.245)
 result=dict(schema=PREFIX,status='NUMERICALLY_QUALIFIED_FIXED_NEVO_SCREEN' if all(t['passed'] for t in tests) else 'FAILED_NUMERICAL_CONTROLS',
  seconds=time.monotonic()-started,source_sha256=source_sha,runner_sha256=runner_sha,
  binary_sha256=sha(BINARY),pinned_inputs=evidence,
  controls=tests,finals={k:dict(physical=v['physical'],final=v['final'],controls=v['controls']) for k,v in runs.items()},
  observations=observations,approximation_screens=screens,
  fixed_inputs=dict(Hunit=68.06502010698708,OB=.049,clock_dust=.251,OA=.7,Gcos_over_GN=.98,T0=2.72548,epsilon=1e-6),
  qualification='Fixed-NEVO transport and cached rates; nuclear tolerance only. No nuclear-rate covariance or abundance likelihood. Observations previously exposed, not holdout. YPBBN and YPCMB differ. Inherited baryon-rest omission bounded in H, not abundances. Fixed NEVO Neff3.043977 versus CMB3.046. Mean baryon mass eta convention uses24.7% helium. Hunit fit to theta; NO BBN parameters fitted. This is not native network radiation production.',
  observations_sources=['https://arxiv.org/abs/1710.11129v3','https://arxiv.org/html/2010.04180v1'])
 save('RESULT',result)
 print(json.dumps(dict(status=result['status'],seconds=result['seconds'],
  tests=len(tests),failed=[t for t in tests if not t['passed']],
  observations=observations,screens=screens,sha256=sha(OUT)),indent=2))
if __name__=='__main__':main()

