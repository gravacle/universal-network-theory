"""Guarded NEW analytic controls for the full dynamic circle reduction only."""
from pathlib import Path
import hashlib,importlib.util,json,math,os
from fractions import Fraction
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
OUT='FULL_DYNAMIC_METRIC_CIRCLE_CONTROLS_V001_RESULT.json'
KERNEL='author_fragment_full_dynamic_metric_circle_v001.py'
KERNEL_SHA='3be0a9eb635df1e1168fb196f2c18f78ad9d120b8090c52f1730f4afa20959fc'
GEODESIC='cross_u_full_metric_geodesic_and_rotating_material_v001.py'
GEODESIC_SHA='53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa'
np=G=None

def analytic_metric(K,L,Ldot,q):
 R=2.;cp=4.;omega=.125;omegadot=.03125;V=cp*cp-K/R
 g=np.zeros((4,4));dg=np.zeros((4,4,4));g[0,0]=-L*L*V+omega*omega*R*R;g[1,1]=1+q*q*R*R;g[2,2]=1.;g[3,3]=R*R
 for i,j,v in ((0,1,q*omega*R*R),(0,3,omega*R*R),(1,3,q*R*R)):g[i,j]=g[j,i]=v
 dg[0,0,0]=-2*L*Ldot*V+2*omega*omegadot*R*R;dg[1,0,0]=-L*L*K/(R*R)+2*omega*omega*R;dg[1,1,1]=2*q*q*R;dg[1,3,3]=2*R
 for axis,i,j,v in ((0,0,1,q*omegadot*R*R),(0,0,3,omegadot*R*R),(1,0,1,2*q*omega*R),(1,0,3,2*omega*R),(1,1,3,2*q*R)):dg[axis,i,j]=dg[axis,j,i]=v
 frequency=math.sqrt(K/(2*R**3));physical=R*frequency/math.sqrt(V/(cp*cp))
 signs=(0.,) if K==0 else (-1.,1.)
 expected=[dict(Omega=-omega+sign*L*frequency,Omega_dot=-omegadot+sign*Ldot*frequency,velocity=sign*physical,f=-Ldot/L) for sign in signs]
 return g,dg,cp,expected

def plain(x):
 if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [plain(v) for v in x]
 if hasattr(x,'tolist'):return x.tolist()
 return x

def main():
 global np,G
 assert AUTHOR_DRAFT is False and not (BASE/OUT).exists(),'Root reviewed release and exclusive output required'
 assert hashlib.sha256((BASE/KERNEL).read_bytes()).hexdigest()==KERNEL_SHA and hashlib.sha256((BASE/GEODESIC).read_bytes()).hexdigest()==GEODESIC_SHA
 import numpy as numpy
 np=numpy;spec=importlib.util.spec_from_file_location('supplied_metric_fresh_controls_only',BASE/GEODESIC);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G);G.np=np
 exec(compile((BASE/KERNEL).read_text(),str(BASE/KERNEL),'exec'),globals())
 controls=[];cases=[]
 def check(name,actual,expected):
  a=np.asarray(actual,dtype=float);b=np.asarray(expected,dtype=float);assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b));scale=max(1.,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0)));error=float(np.max(abs(a-b),initial=0))/scale
  controls.append(dict(name=name,actual=a.tolist(),expected=b.tolist(),error=error,tolerance=2e-11,passed=error<=2e-11));assert error<=2e-11,(name,error)
 for name,params in (('rotating_flat', (0.,1.,0.,0.)),('rotating_radial_lapse',(1.,1.,0.,0.)),('time_reparameterized_helical_lapse',(1.,2.,.125,.25))):
  g,dg,cp,expected=analytic_metric(*params);geometry=G.metric_geometry(g,dg,cp);result=full_dynamic_circle_candidates(geometry,azimuth=3,meridional=(1,2),radial=1)
  candidates=result['candidates'];assert len(candidates)==len(expected) and not result['rejected'];cases.append(dict(name=name,g=g,dg=dg,expected=expected,result=result))
  for i,(a,b) in enumerate(zip(candidates,expected)):
   prefix=name+'_%d_'%i;check(prefix+'known_frequency_and_time_rate',[a['Omega'],a['Omega_dot']],[b['Omega'],b['Omega_dot']]);check(prefix+'known_normal_observer_speed',a['normal_axial_velocity'],b['velocity']);check(prefix+'known_normalization_rate',a['circle']['f'],b['f']);check(prefix+'independent_full_circle_rows',np.r_[a['circle']['meridional'],a['circle']['axial']],np.zeros(3));check(prefix+'independent_geodesic_acceleration',a['geodesic']['dw_dt'],[0.,0.,b['Omega_dot']])
 for name,q,kind,roots in (('negative_discriminant',[1.,0.,1.],'negative_discriminant_no_circle',[]),('double_root',[1.,-2.,1.],'quadratic_double_root',[1.]),('linear',[1.,2.,0.],'linear',[-.5]),('constant',[1.,0.,0.],'constant_nonzero_no_circle',[]),('identity',[0.,0.,0.],'identically_zero_no_unique_circle',[])):
  actual=full_dynamic_polynomial_roots(q);assert actual['kind']==kind;check('root_diagnostic_'+name,actual['roots'],roots)
 report=dict(status='NEW_FULL_DYNAMIC_CIRCLE_ANALYTIC_CONTROLS_PASS',owner_pid=os.getpid(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),kernel_sha256=KERNEL_SHA,geodesic_sha256=GEODESIC_SHA,controls=controls,cases=plain(cases),old_fixture_or_live_payload_replayed=False,physical_galaxy_metric_supplied=False,revised43_velocities_exist=False,persistent_orbit_stability_or_observational_success=False)
 with (BASE/OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=len(controls),maximum_error=max(q['error'] for q in controls),sha256=hashlib.sha256((BASE/OUT).read_bytes()).hexdigest())))
if __name__=='__main__':main()
