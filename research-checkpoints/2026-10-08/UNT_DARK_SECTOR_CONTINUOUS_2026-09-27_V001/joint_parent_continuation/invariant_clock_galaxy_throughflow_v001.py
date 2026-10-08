"""Does the regular planar through-flow supply a galaxy-sized active source?

Restricted prescribed static Gaussian lapse, NOT a galaxy/Einstein solution.
Same action/new two-ordinary-parameter joint calibration. Depth=(200km/s/c)^2,
widths5 and20kpc, same prescribed incident tilt-.001; no boundary/halo fit.
Two widths probe length-scaling and lower acceleration, not a parameter search.
Integrate E=Nc-cinf, Z, and BOTH direct and integration-by-parts active-source
integrals. Retain P_transverse and downstream Z/current. Same clock branch.
The leading weak-metric force screen max|Iact|/(2max|N'|) is necessary only;
full spatial/momentum constraints, preferred direction and formation unsolved.
Frozen numerical gates inherited: current1e-11, algebra1e-12, inversefd1e-6,
RK4 512/1024 common-field refinement1e-5; direct/parts integral1e-7,
derivative residual1e-3. No observation-fit gate.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_planar_throughflow_v001 as prior

J=Path(__file__).resolve().parent
OUT=J/'INVARIANT_CLOCK_GALAXY_THROUGHFLOW_V001_RESULT.json'
CAL=J/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json'
CALSHA='c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f'
PRIORSHA='4eb1ddb2aefb53e6665eab9299e6f9e0c6570ce4fa20458842924d1804fc2a47'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Flow(prior.Flow):
 def __init__(self,model,width):
  super().__init__(model,-.001)
  self.depth=(200./299792.458)**2
  self.ell=width/1000.*model.p['H0_km_s_Mpc']/299792.458
  self.Abar=self.mb*self.Xb*(1+2*self.tilt**2)+2*self.Kb
 def stress(self,xi,y):
  a=self.solve(xi,y[:2]);m=self.m
  z=abs(a['p'])/m.bs
  if z>.01:raise ValueError('existing constitutive series regime left')
  Jfun=m.lam*m.bs**2*(2*z**3/3-z**5/5+3*z**7/28-5*z**9/72)
  _,_,_,K,*_=m.constitutive(a['s'])
  PT=(m.KB*a['e']**2+2*m.C*a['e']*a['p']-m.C*(a['p']**2+Jfun)+2*K)/2
  current=self.Jinf/a['N'];M=a['m']*a['q']/a['X']+a['sigma']*a['D']
  nond=M*a['q']-a['w']*current+2*PT
  active=a['rho']+a['P']+2*PT-self.Abar
  a.update(PT=PT,active=active,nonderivative=nond-self.Abar,
   I_direct=y[2],I_parts=(self.cinf+y[0])*y[1]+y[3])
  return a
 def rhs(self,xi,y):
  a=self.stress(xi,y)
  return self.ell*np.array([a['N']*a['e'],a['Zprime'],a['N']*a['active'],
                           a['N']*(a['nonderivative']-a['e']*a['Z'])])
 def integrate(self,n):
  y=np.zeros(4);h=-16/n;s=[]
  for i in range(n+1):
   xi=8+i*h
   if i%(n//128)==0:
    a=self.stress(xi,y);a['xi']=xi;s.append(a)
   if i==n:break
   k1=self.rhs(xi,y);k2=self.rhs(xi+h/2,y+h*k1/2)
   k3=self.rhs(xi+h/2,y+h*k2/2);k4=self.rhs(xi+h,y+h*k3)
   y+=h*(k1+2*k2+2*k3+k4)/6
  return s
 def peak_gradient(self):
  x=math.sqrt(.5)
  for _ in range(8):
   f=1/x-2*x+2*self.depth*x*math.exp(-x*x)
   df=-1/x**2-2+2*self.depth*math.exp(-x*x)*(1-2*x*x)
   x-=f/df
  return math.exp(-self.depth*math.exp(-x*x))*2*self.depth*x*math.exp(-x*x)/self.ell

def main():
 started=time.monotonic()
 if OUT.exists():raise RuntimeError('no overwrites or duplicate run')
 if sha(CAL)!=CALSHA or sha(Path(prior.__file__))!=PRIORSHA:raise RuntimeError('changed inputs')
 cal=json.loads(CAL.read_text());saved=json.loads(prior.base.SOURCE.read_text())
 for p in (Path(prior.base.__file__),prior.base.SOURCE):
  if sha(p)!=cal['hashes'][str(p)]:raise RuntimeError('changed constitutive source')
 saved['inherited']=cal['fixed']
 # Stale unused baryon_GN_normalization metadata is retained, not interpreted.
 model=prior.base.Model(saved,1)
 checks=[];rows=[]
 def check(name,value,gate):
  checks.append(dict(name=name,error=float(value),gate=gate,passed=bool(value<=gate)))
 for width in (5.,20.):
  coarse=Flow(model,width);fine=Flow(model,width)
  a=coarse.integrate(512);b=fine.integrate(1024)
  for key,floor in [('E',1e-30),('Z',1e-30),('p',1e-30),('X_minus_Xbar',1e-30),
                    ('I_direct',1e-30),('I_parts',1e-30)]:
   av=np.array([v[key] for v in a]);bv=np.array([v[key] for v in b])
   check(str(width)+'_'+key+'_RK4',np.max(abs(av-bv))/max(np.max(abs(bv)),floor),1e-5)
  check(str(width)+'_current',fine.max_current,1e-11)
  check(str(width)+'_algebra',fine.max_algebra,1e-12)
  direct=np.array([v['I_direct'] for v in b]);parts=np.array([v['I_parts'] for v in b])
  check(str(width)+'_active_integral_identity',np.max(abs(direct-parts))/max(np.max(abs(direct)),1e-30),1e-7)
  # Independent sample derivative of active integral; use interior only.
  hxi=b[1]['xi']-b[0]['xi'];dd=(direct[:-4]-8*direct[1:-3]+8*direct[3:-1]-direct[4:])/(12*hxi)
  rr=fine.ell*np.array([v['N']*v['active'] for v in b[2:-2]])
  check(str(width)+'_active_derivative',np.max(abs(dd-rr))/max(np.max(abs(rr)),1e-30),1e-3)
  fd=[]
  for v in b[::16]:
   step=1e-9
   state=np.array([v['E'],v['Z']])
   ap=fine.algebra(v['xi'],state,v['p']+step)
   am=fine.algebra(v['xi'],state,v['p']-step)
   fd.append(abs((ap['F']-am['F'])/(2*step)/v['Fp']-1))
  check(str(width)+'_current_inverse_fd',max(fd),1e-6)
  gradient=fine.peak_gradient()
  rows.append(dict(width_kpc=width,ell_Hunit=fine.ell,depth=fine.depth,tilt=fine.tilt,
   peak_imposed_gradient=gradient,peak_imposed_acceleration_over_a0=gradient/(model.bs/(1+model.lam)),
   force_screen=max(abs(direct))/(2*gradient),
   regularity=dict(min_current_inverse=fine.min_inverse,min_branch_fraction=fine.min_f,max_branch_fraction=fine.max_f),
   center=b[64],downstream=b[-1],snapshots=b,
   small_parameters=dict(charge_length=fine.mb*fine.Xb*fine.ell**2/fine.tilt**2,
                         compressibility=model.constitutive(fine.sb)[2]*fine.Xb**2*fine.ell**2)))
  print(json.dumps(dict(width_kpc=width,force_screen=rows[-1]['force_screen'],
                       downstreamZ=b[-1]['Z'],gradient_over_a0=rows[-1]['peak_imposed_acceleration_over_a0'])),flush=True)
 result=dict(protocol=__doc__,status='RESTRICTED_ACTIVE_SOURCE_DIAGNOSTIC_COMPLETE',
  all_controls_passed=all(c['passed'] for c in checks),controls=checks,rows=rows,
  fixed=model.p,calibration_sha256=CALSHA,prior_source_sha256=PRIORSHA,
  source_sha256=sha(Path(__file__)),elapsed_seconds=time.monotonic()-started,
  caveat='Prescribed planar lapse and spatial metric. No formed galaxy, source Einstein constraints, GN or MOND law verified. Incoming tilt/preparation adopted. Phase cap/current inverse necessary, not nonlinear stability.')
 with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
 print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],checks=len(checks),
  failed=[c for c in checks if not c['passed']],elapsed_seconds=result['elapsed_seconds'],
  result_sha256=sha(OUT)),indent=2))
if __name__=='__main__':main()
