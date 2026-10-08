"""Root-owned saved scalar metric completion; no producer or trajectory calls."""
from pathlib import Path
from decimal import Decimal as D, localcontext
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, re
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001'
PRIOR='CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001'
PROOF='CONSTRAINED_U_K10_REGULAR_METRIC_COMPLETION_V001.md'
PINS={
 'constrained_u_k10_common_start_scalar_coefficients_v001.py':'5709f6e12e1c751ea7a253863c60328b1f30208037ccff692c6104966aea4839',
 PRIOR+'.md':'8f831f8c0c8e3aef5cdf1fac5d29c52212445cf8d6c30fe34ada5460939c9495',
 PRIOR+'_RESULT.json':'c8e6b26f229332a3371b46e1a2d8ba80bbaed1ca5fa64689f8c674260ca0dc47',
 PRIOR+'_REPORT.md':'cab7660aa6b467ccf62d86dd4f25cbc2ea151f7fae77b914e6e7e9e5a59fd088',
 PRIOR+'_RECEIPT.json':'f88f042d3332e8ff7de40cb612094d11b74356b416f105b8aa887ebbcecf0209',
 PROOF:'e5d638570320830f5edbdc7390af23819a930474733e6441c70f0536a2752d5f',
 'constrained_u_galaxy_horizon_stable_y_gauss_v002.py':'f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531',
 'CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_MANIFEST.json':'1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94',
 STEM+'.md':'a864cae70c86ee30d08ac24265faf14bbc80a04e80dd1dded7c25c1b458f3503',
}
FLAGS=('physical_seed_qualified','new_initial_state_constructed','original_failure_flags_changed','thermal_or_microscopic_origin_qualified','full_metric_and_native_history_qualified')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lift(v):
 assert type(v) in (int,float) and math.isfinite(v)
 return D.from_float(float(v))
def encode(v):
 if isinstance(v,D):assert v.is_finite();return str(v)
 if isinstance(v,dict):return {k:encode(w) for k,w in v.items()}
 if isinstance(v,list):return [encode(w) for w in v]
 return v
def poly(v):return v if isinstance(v,list) else [D(v),D(0)]
def add(*vs):return [sum((poly(v)[j] for v in vs),D(0)) for j in (0,1)]
def scale(v,k):return [k*z for z in poly(v)]
def L(v,k=6):
 v=poly(v);return [k*v[0]+v[1],k*v[1]]
def invL(v):
 v=poly(v);return [(v[0]-v[1]/6)/6,v[1]/6]
def invmetric(v,r):
 v=poly(v);d=42+8*r/5;c1=v[1]/d;return [(v[0]-13*c1)/d,c1]

def complete(base,fixed,precision):
 with localcontext() as ctx:
  ctx.prec=precision;c={k:D(v) for k,v in base.items()};assert len(c)==76 and all(v.is_finite() for v in c.values())
  hr,q,r,t,m,g0=(c[k] for k in ('hr','q0','r','t','m','g0'));h1,h2=(c[k] for k in ('h1','h2'))
  eps,d0,OA,OR,rG=(lift(fixed[k]) for k in ('eps','d0','OA','OR','rG'))
  Nrm=1/eps-(1+1/eps).ln();B=d0*eps*Nrm/(2*c['qinf']);assert Nrm>0 and B>0 and rG>0
  h3=m**3/16;h4=[-5*m**4/128+OA*(1-B.ln()/Nrm)/(2*OR),3*OA/(2*OR*Nrm)]
  p={3:c['p3'],4:c['p4']};a={3:c['G03'],4:c['G04']};b={3:c['G23'],4:c['G24']};pi={3:c['Pi3'],4:c['Pi4']};drivers={};lag={};hs=[D(1),h1,h2]
  def photon(j,velocity):
   driver=8*q*q*velocity/15;tp=hr*sum((hs[l]*(j-1-l)*p[j-1-l] for l in range(j-3)),D(0))
   t0=hr*sum((hs[l]*(j-1-l)*a[j-1-l] for l in range(j-3)),D(0));t2=hr*sum((hs[l]*(j-1-l)*b[j-1-l] for l in range(j-3)),D(0))
   pi[j]=10*(driver-tp-t0-t2)/(3*g0);p[j]=(driver-tp)/g0+pi[j]/10;a[j]=pi[j]/2-t0/g0;b[j]=pi[j]/10-t2/g0
   drivers[str(j)]=driver;lag[str(j)]=dict(Tp=tp,T0=t0,T2=t2)
  photon(5,c['v4']+c['U4']);Tv5=4*h1*c['v4']+3*h2*c['v3']+2*h3*c['v2'];Rv3=h1*c['v4']+h2*c['v3']+h3*c['v2']
  K5=8*q*q*(c['wn5']-Tv5/5)/(75*hr)-3*q*c['J4']/(25*hr)-(4*h1*c['N4']+3*h2*c['N3']+2*h3*c['N2'])/5
  Phi3=(c['R3']-3*hr*hr*(t*p[5]+r*K5)/(q*q)-hr*(Rv3-Tv5/5))/(D(6)/5+8*r/125)
  v5=(Phi3/hr-Tv5)/5;N5=8*q*q*Phi3/(375*hr*hr)+K5;Psi3=c['R3']-hr*(v5+Rv3)
  J5=(3*q*c['N4']/(7*hr)-4*q*c['Fn44']/(7*hr)-4*h1*c['J4']-3*h2*c['J3'])/5
  photon(6,v5+c['U5'])
  Tv=add(5*h1*v5+4*h2*c['v4']+3*h3*c['v3'],scale(h4,2*c['v2']))
  Rv=add(h1*v5+h2*c['v4']+h3*c['v3'],scale(h4,c['v2']))
  E6=add(8*q*q*c['wn6']/(15*hr)-3*q*J5/(5*hr)-5*h1*N5-4*h2*c['N4']-3*h3*c['N3'],scale(h4,-2*c['N2']))
  K4=add(c['R4']-3*hr*hr*t*p[6]/(q*q),scale(Rv,-hr))
  forcing=add(L(L(K4)),scale(add(L(Tv),scale(Tv,8*r/5)),hr),scale(L(E6),-3*hr*hr*r/(q*q)))
  Phi4=invmetric(forcing,r);v6=invL(add(scale(Phi4,1/hr),scale(Tv,-1)));N6=invL(add(scale(v6,8*q*q/(15*hr)),E6));Psi4=add(c['R4'],scale(add(v6,Rv),-hr))
  c3=1/(Nrm*d0*c['qinf']);pressure0=-3*c3*c['w3']*hr*c['v2'];pressure1=-3*c3*c['w3']*hr*(c['v3']+h1*c['v2'])
  scalar=dict(Nrm=Nrm,B=B,h3=h3,p5=p[5],p6=p[6],Pi5=pi[5],Pi6=pi[6],G05=a[5],G06=a[6],G25=b[5],G26=b[6],Tv5=Tv5,Rv3=Rv3,K5=K5,Phi3=Phi3,v5=v5,N5=N5,Psi3=Psi3,J5=J5,c3=c3,raw_pressure0=pressure0,raw_pressure1=pressure1)
  polynomial=dict(h4=h4,Tv=Tv,Rv=Rv,E6=E6,K4=K4,metric_forcing=forcing,Phi4=Phi4,v6=v6,N6=N6,Psi4=Psi4);rows={}
  def record(name,terms):
   terms=[poly(v) for v in terms];res=add(*terms);env=[sum((abs(v[j]) for v in terms),D(0)) for j in (0,1)]
   rows[name]=dict(terms=terms,residual=res,absolute_term_sum=env,normalized=[res[j]/env[j] if env[j] else None for j in (0,1)])
  for j in (5,6):
   record('photon_collision'+str(j),[lag[str(j)]['Tp'],-drivers[str(j)],g0*p[j],-g0*pi[j]/10])
   record('G0_collision'+str(j),[lag[str(j)]['T0'],g0*a[j],-g0*pi[j]/2]);record('G2_collision'+str(j),[lag[str(j)]['T2'],g0*b[j],-g0*pi[j]/10])
   record('Pi_sum'+str(j),[pi[j],-p[j],-a[j],-b[j]])
  record('Vdot3',[5*hr*v5,4*hr*h1*c['v4'],3*hr*h2*c['v3'],2*hr*h3*c['v2'],-Phi3])
  record('curvature3',[c['R3'],-Psi3,-hr*v5,-hr*Rv3]);record('shear3',[Psi3,-Phi3,-3*hr*hr*t*p[5]/(q*q),-3*hr*hr*r*N5/(q*q)])
  record('nu_quad3',[5*hr*N5,4*hr*h1*c['N4'],3*hr*h2*c['N3'],2*hr*h3*c['N2'],-8*q*q*(v5+c['wn5'])/15,3*q*c['J4']/5])
  record('nu_l3_next',[5*hr*J5,4*hr*h1*c['J4'],3*hr*h2*c['J3'],-3*q*c['N4']/7,4*q*c['Fn44']/7])
  record('Vdot4',[scale(L(v6),hr),scale(Tv,hr),scale(Phi4,-1)])
  record('curvature4',[c['R4'],scale(Psi4,-1),scale(v6,-hr),scale(Rv,-hr)])
  record('shear4',[Psi4,scale(Phi4,-1),-3*hr*hr*t*p[6]/(q*q),scale(N6,-3*hr*hr*r/(q*q))])
  record('nu_quad4',[scale(L(N6),hr),scale(v6,-8*q*q/15),-8*q*q*c['wn6']/15,3*q*J5/5,hr*(5*h1*N5+4*h2*c['N4']+3*h3*c['N3']),scale(h4,2*hr*c['N2'])])
  record('metric_polynomial',[L(L(Phi4)),L(Phi4),scale(Phi4,8*r/5),scale(forcing,-1)])
  record('background_log',[h4[1],-3*OA/(2*OR*Nrm)]);record('background_constant',[h4[0],5*m**4/128,-OA*(1-B.ln()/Nrm)/(2*OR)])
  record('raw_pressure_constant',[pressure0,9*OA*hr*c['v2']/(2*rG*Nrm)]);record('raw_pressure_linear',[pressure1,9*OA*hr*(c['v3']+h1*c['v2'])/(2*rG*Nrm)])
  return dict(precision=precision,prior_coefficient_strings=base,calibrated_new_input={k:lift(fixed[k]) for k in ('eps','d0','OA','OR','rG')},scalar_coefficients=scalar,polynomial_coefficients=polynomial,photon_drivers=drivers,photon_derivative_contacts=lag,independent_polynomial_rows=rows)

def evaluate(v,x):v=poly(v);return v[0]+v[1]*x
def predictions(prior,completion,a):
 c={k:D(v) for k,v in prior.items()};s=completion['scalar_coefficients'];p=completion['polynomial_coefficients'];x=a.ln()
 return dict(Phi=sum((c['Phi'+str(j)]*a**j for j in (0,1,2)),D(0))+s['Phi3']*a**3+evaluate(p['Phi4'],x)*a**4,
  Psi=sum((c['Psi'+str(j)]*a**j for j in (0,1,2)),D(0))+s['Psi3']*a**3+evaluate(p['Psi4'],x)*a**4,
  V=sum((c['v'+str(j)]*a**j for j in (2,3,4)),D(0))+s['v5']*a**5+evaluate(p['v6'],x)*a**6,
  F_gamma_2=c['p3']*a**3+c['p4']*a**4+s['p5']*a**5+s['p6']*a**6,
  G_gamma_0=c['G03']*a**3+c['G04']*a**4+s['G05']*a**5+s['G06']*a**6,
  G_gamma_2=c['G23']*a**3+c['G24']*a**4+s['G25']*a**5+s['G26']*a**6,
  F_nu_2=sum((c['N'+str(j)]*a**j for j in (2,3,4)),D(0))+s['N5']*a**5+evaluate(p['N6'],x)*a**6,
  F_nu_3=c['J3']*a**3+c['J4']*a**4+s['J5']*a**5)

def run():
 started=datetime.now(timezone.utc).isoformat();selfsha=sha(Path(__file__));outputs=[STEM+x for x in ('_RESULT.json','_REPORT.md','_RECEIPT.json')];assert all(not (BASE/n).exists() for n in outputs)
 prior=json.loads((BASE/(PRIOR+'_RESULT.json')).read_text());receipt=json.loads((BASE/(PRIOR+'_RECEIPT.json')).read_text());allpins=dict(PINS)
 for n,s in prior['input_sha256'].items():assert n not in allpins or allpins[n]==s;allpins[n]=s
 for n,s in re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',(BASE/PROOF).read_text(),re.M):assert n not in allpins or allpins[n]==s;allpins[n]=s
 def authenticate():
  assert sha(Path(__file__))==selfsha and not Path(__file__).stat().st_mode&0o222
  for n,s in allpins.items():assert sha(BASE/n)==s and not (BASE/n).stat().st_mode&0o222,n
 authenticate();assert prior['status']==receipt['status']=='COMPLETED_DESCRIPTIVE_SCALAR_COEFFICIENTS' and prior['owner']==receipt['owner']=='root'
 assert prior['input_sha256']==receipt['input_sha256'] and prior['source_sha256']==receipt['source_sha256']==PINS['constrained_u_k10_common_start_scalar_coefficients_v001.py']
 assert receipt['result_sha256']==PINS[PRIOR+'_RESULT.json'] and receipt['report_sha256']==PINS[PRIOR+'_REPORT.md'] and all(prior[k] is False for k in FLAGS)
 fixed=json.loads((BASE/'CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_MANIFEST.json').read_text())['fixed'];families=[]
 assert len(prior['families'])==2
 for family,label in zip(prior['families'],('FINE','START')):
  assert family['label']==label and [r['precision'] for r in family['coefficient_evaluations']]==[80,120] and len(family['finite_comparisons'])==8
  out=[complete(e['coefficients'],fixed,e['precision']) for e in family['coefficient_evaluations']];comparison=[]
  with localcontext() as ctx:
   ctx.prec=160;difference={section:{k:add(poly(out[1][section][k]),scale(out[0][section][k],D(-1))) for k in out[0][section]} for section in ('scalar_coefficients','polynomial_coefficients')}
  for original in family['finite_comparisons']:
   precision=original['precision'];new=out[0 if precision==80 else 1]
   with localcontext() as ctx:
    ctx.prec=precision;a=D(original['a']);pred=predictions(new['prior_coefficient_strings'],new,a);saved={k:original['saved'][k] for k in pred};old={k:original['predicted'][k] for k in pred}
    comparison.append(dict(precision=precision,arm=original['arm'],omega=original['omega'],a=original['a'],completed_series=pred,saved=saved,prior_series=old,signed_series_minus_saved={k:pred[k]-D(saved[k]) for k in pred},completion_minus_prior={k:pred[k]-D(old[k]) for k in pred}))
  families.append(dict(label=label,metric_evaluations=out,signed_precision120_minus80=difference,finite_comparisons=comparison))
 result=dict(status='COMPLETED_DESCRIPTIVE_METRIC_COEFFICIENTS',owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),source_sha256=selfsha,input_sha256=allpins,families=families,prior_false_flags={k:prior[k] for k in FLAGS},prior_missing_contacts=prior['missing_contacts'],new_residual_threshold=None,
  remaining_contacts=['higher angular companions and complete primordial history','native z7/z8 and later reaction/phase/current coefficients','complete finite-source normal/shear/trace/momentum/current residuals and all-order remainder'],full_trace_qualified=False,new_state_constructed=False)
 authenticate()
 with (BASE/outputs[0]).open('xb') as f:f.write((json.dumps(encode(result),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())
 (BASE/outputs[0]).chmod(0o444)
 with (BASE/outputs[1]).open('x') as f:f.write('# Saved k10 metric completion V001\n\nBoth prior coefficient families and precision contexts remain unchanged. New metric/polarization/log coefficients, independent polynomial residuals and sixteen old-state comparisons are saved. No threshold, state construction, trace certificate or physical qualification.\n')
 (BASE/outputs[1]).chmod(0o444);authenticate();closed=dict(status=result['status'],owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=selfsha,input_sha256=allpins,result_sha256=sha(BASE/outputs[0]),report_sha256=sha(BASE/outputs[1]))
 with (BASE/outputs[2]).open('xb') as f:f.write((json.dumps(closed,sort_keys=True,separators=(',',':'))+'\n').encode())
 (BASE/outputs[2]).chmod(0o444);authenticate();assert sha(BASE/outputs[0])==closed['result_sha256'] and sha(BASE/outputs[1])==closed['report_sha256']
 print(json.dumps(dict(status=result['status'],pid=os.getpid(),result_sha256=closed['result_sha256'],receipt_sha256=sha(BASE/outputs[2]))))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true',required=True);parser.parse_args();run()
