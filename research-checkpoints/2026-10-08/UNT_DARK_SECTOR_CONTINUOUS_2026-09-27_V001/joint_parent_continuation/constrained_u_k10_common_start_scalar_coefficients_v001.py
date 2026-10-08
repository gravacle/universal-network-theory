"""Root-owned scalar recurrence; no producer imports, matrices or propagation."""
from pathlib import Path
from decimal import Decimal as D, localcontext
from datetime import datetime, timezone
import argparse, hashlib, json, math, os
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001'
PARENT='CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002'
PINS={
 'constrained_u_galaxy_horizon_stable_y_gauss_v002.py':'f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531',
 'constrained_u_clock_gradient_early_transfer_v004.py':'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07',
 PARENT+'_MANIFEST.json':'1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94',
 PARENT+'_FINE_CP_002048.json':'da6b2ce2b4576f9914dd88966b866ca5a48ca1e6685122f518a1f90df1bb2077',
 PARENT+'_FINE_CP_002048_COMMIT.json':'83fa8e2adcdc3f00adc612274112e68750b2b823c8ca09b6e857c764aa037cfc',
 PARENT+'_START_CP_001664.json':'8153f119a00e212f91cdab61a849dc4d390b0265f41167aefe87b9abd1d0b726',
 PARENT+'_START_CP_001664_COMMIT.json':'c6f1ac9d7f17bee00165ba988b49c3ab56af3f6ae78656368aada5ff9ea94ac1',
 'CONSTRAINED_U_K10_COMMON_DENSITY_AND_CURRENT_REGULAR_JETS_V001.md':'dcfdf786cd6cdc80ff6182db84d4562a1b0a16150b329fcda8bc5e866fc38282',
 STEM+'.md':'8f831f8c0c8e3aef5cdf1fac5d29c52212445cf8d6c30fe34ada5460939c9495',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lift(v):
 assert type(v) in (int,float) and math.isfinite(v)
 return D.from_float(float(v))
def encode(v):
 if isinstance(v,D):assert v.is_finite();return str(v)
 if isinstance(v,dict):return {k:encode(w) for k,w in v.items()}
 if isinstance(v,list):return [encode(w) for w in v]
 return v

def coefficients(fixed,case,precision):
 with localcontext() as ctx:
  ctx.prec=precision
  t=lift(fixed['fgamma']);r=1-t;Rstar=lift(fixed['curvature'])
  q0=lift(fixed['k_Mpc_inverse'])*299792458/(1000*lift(fixed['Hunit']))
  hr=(lift(fixed['OR'])/lift(fixed['rG'])).sqrt();qinf=(1+lift(fixed['eps'])).sqrt()
  A=Rstar/(D(3)/2+2*r/5);m=(lift(fixed['OB'])+lift(fixed['OA'])*qinf*lift(fixed['d0']))/lift(fixed['OR'])
  h1=m/2;h2=-m*m/8;b3=D(3)*lift(fixed['OB'])/(2*lift(fixed['rG']))
  w3=D(3)*lift(fixed['OA'])*qinf*lift(fixed['d0'])/(2*lift(fixed['rG']))
  beta=b3/(2*hr*hr*t);g0=lift(case['thermal']['g'])*lift(case['a'])**3
  assert 0<t<1 and hr>0 and q0>0 and g0>0
  Phi0=A;Psi0=A*(1+2*r/5)
  Phi1=m*A*5*(8*r-3)/(16*(15+2*r))-12*t*hr*A/((15+2*r)*g0)
  Psi1=-m*A*(15+16*r)/(16*(15+2*r))+4*t*hr*A/((15+2*r)*g0)
  v2=A/(2*hr);v3=(Phi1-m*A/2)/(3*hr)
  R2=-A*q0*q0*(5+4*r)/(120*hr*hr);U4=-Rstar*q0*q0/(36*hr**3);wn4=U4-A*q0*q0/(45*hr**3)
  p3=32*q0*q0*v2/(45*g0);p4=32*q0*q0*v3/(45*g0)-D(11)*hr*p3/(2*g0)
  Pi3=5*p3/2;G03=5*p3/4;G23=p3/4;Pi4=5*p4/2-45*hr*p3/(4*g0)
  G04=Pi4/2-15*hr*p3/(4*g0);G24=Pi4/10-3*hr*p3/(4*g0)
  N2=4*q0*q0*v2/(15*hr);N3=(8*q0*q0*v3/(15*hr)-2*h1*N2)/3;J3=2*A*q0**3/(105*hr**3)
  Knu=2*q0*q0*(wn4-3*h1*v3/4-h2*v2/2)/(15*hr)-3*q0*J3/(20*hr)-3*h1*N3/4-h2*N2/2
  Phi2=(R2-3*hr*hr*(t*p4+r*Knu)/(q0*q0)-hr*h1*v3/4-hr*h2*v2/2)/(D(5)/4+r/10)
  v4=(Phi2/hr-3*h1*v3-2*h2*v2)/4;N4=q0*q0*Phi2/(30*hr*hr)+Knu
  Fbar3=t*p3+r*N3;Fbar4=t*p4+r*N4;Psi2=Phi2+3*hr*hr*Fbar4/(q0*q0)
  J4=(3*q0*N3/(7*hr)-3*h1*J3)/4;Fn44=q0*J3/(9*hr)
  G15=q0*p3/(4*g0);Fg35=3*q0*p3/(7*g0);G35=3*q0*G23/(7*g0)
  I3=(v3-h1*v2)/(3*hr);I4=(v4-h1*v3+(h1*h1-h2)*v2)/(4*hr)
  R3=-q0*q0*I3/15-Fbar3/10-7*h1*R2/5
  R4=-q0*q0*I4/27-q0*q0*R2/(108*hr*hr)-Fbar4/18-3*h1*R3/2
  gp2=3*R2-q0*q0*v2/(2*hr);gp3=3*R3-q0*q0*I3;gp4=3*R4-q0*q0*I4
  gg2=gn2=4*gp2/3;gg3=gn3=4*gp3/3
  gg4=4*R4-q0*q0*(v4+U4-h1*v3+(h1*h1-h2)*v2)/(3*hr)
  gn4=4*R4-q0*q0*(v4+wn4-h1*v3+(h1*h1-h2)*v2)/(3*hr)
  gb2=gp2;gb3=gp3;gb4=3*gg4/4
  U5=gg3/(16*hr)-p3/(8*hr)-(3*h1+4*beta)*U4/4
  U6=gg4/(20*hr)-p4/(10*hr)-(4*h1+5*beta)*U5/5-(3*h2+4*beta*h1)*U4/5
  wn5=gn3/(16*hr)-N3/(8*hr)-3*h1*wn4/4
  wn6=gn4/(20*hr)-N4/(10*hr)-4*h1*wn5/5-3*h2*wn4/5
  W6=4*beta*hr*U4/g0;wb4=wg4=U4;wb5=wg5=U5;wb6=U6-W6;wg6=U6
  S0=2*hr*hr*(t*U4+r*wn4);S1=2*hr*hr*(t*U5+r*wn5)+b3*U4;S2=2*hr*hr*(t*U6+r*wn6)+b3*U5
  names='t r Rstar q0 hr qinf A m h1 h2 b3 w3 beta g0 Phi0 Psi0 Phi1 Psi1 Phi2 Psi2 v2 v3 v4 R2 R3 R4 U4 U5 U6 wn4 wn5 wn6 W6 wb4 wb5 wb6 wg4 wg5 wg6 p3 p4 Pi3 Pi4 G03 G04 G23 G24 N2 N3 N4 J3 J4 Fn44 G15 Fg35 G35 Knu Fbar3 Fbar4 I3 I4 gp2 gp3 gp4 gb2 gb3 gb4 gg2 gg3 gg4 gn2 gn3 gn4 S0 S1 S2'.split()
  values=locals();c={k:values[k] for k in names};checks={}
  def record(name,terms):
   residual=sum(terms,D(0));envelope=sum(map(abs,terms),D(0))
   checks[name]=dict(terms=terms,residual=residual,absolute_term_sum=envelope,normalized=residual/envelope if envelope else None)
  record('background_matter',[b3+w3,-3*hr*hr*h1]);record('background_second',[h1*h1,2*h2])
  record('metric_first',[Phi1,3*Psi1,m*A/4]);record('polarization_sum3',[Pi3,-p3,-G03,-G23]);record('polarization_sum4',[Pi4,-p4,-G04,-G24])
  record('photon_collision0',[8*q0*q0*v2/15,-g0*(p3-Pi3/10)])
  record('photon_collision1',[3*hr*p3,-8*q0*q0*v3/15,g0*(p4-Pi4/10)])
  record('G0_collision0',[-g0*(G03-Pi3/2)]);record('G2_collision0',[-g0*(G23-Pi3/10)])
  record('G0_collision1',[3*hr*G03,g0*(G04-Pi4/2)]);record('G2_collision1',[3*hr*G23,g0*(G24-Pi4/10)])
  record('Vdot0',[2*hr*v2,-Phi0]);record('Vdot1',[3*hr*v3,2*hr*h1*v2,-Phi1]);record('Vdot2',[4*hr*v4,3*hr*h1*v3,2*hr*h2*v2,-Phi2])
  record('curvature0',[Rstar,-Psi0,-hr*v2]);record('curvature1',[-Psi1,-hr*v3,-hr*h1*v2]);record('curvature2',[R2,-Psi2,-hr*v4,-hr*h1*v3,-hr*h2*v2])
  for j,Phi,Psi,Fbar in ((0,Phi0,Psi0,r*N2),(1,Phi1,Psi1,Fbar3),(2,Phi2,Psi2,Fbar4)):record('shear'+str(j),[Psi,-Phi,-3*hr*hr*Fbar/(q0*q0)])
  record('nu_quad0',[2*hr*N2,-8*q0*q0*v2/15]);record('nu_quad1',[3*hr*N3,2*hr*h1*N2,-8*q0*q0*v3/15])
  record('nu_quad2',[4*hr*N4,3*hr*h1*N3,2*hr*h2*N2,-8*q0*q0*(v4+wn4)/15,3*q0*J3/5])
  record('nu_l3_leading',[3*hr*J3,-3*q0*N2/7]);record('nu_l3_next',[4*hr*J4,3*hr*h1*J3,-3*q0*N3/7]);record('nu_l4_leading',[4*hr*Fn44,-4*q0*J3/9])
  record('Udot2',[4*hr*U4,-hr*U4,-gg2/4])
  record('Udot3',[5*hr*U5,4*hr*h1*U4,4*beta*hr*U4,-hr*U5,-hr*h1*U4,-gg3/4,p3/2])
  record('Udot4',[6*hr*U6,5*hr*h1*U5,4*hr*h2*U4,beta*hr*(5*U5+4*h1*U4),-hr*(U6+h1*U5+h2*U4),-gg4/4,p4/2])
  record('nu_velocity2',[4*hr*wn4,-hr*wn4,-gn2/4,N2/2])
  record('nu_velocity3',[5*hr*wn5,4*hr*h1*wn4,-hr*(wn5+h1*wn4),-gn3/4,N3/2])
  record('nu_velocity4',[6*hr*wn6,5*hr*h1*wn5,4*hr*h2*wn4,-hr*(wn6+h1*wn5+h2*wn4),-gn4/4,N4/2])
  record('slip_leading',[hr*U4,gg2/4,-g0*W6/beta]);record('baryon_Euler_leading',[4*hr*U4,-g0*W6/beta])
  rd=[2*hr*R2,hr*(3*R3+2*h1*R2),hr*(4*R4+3*h1*R3+2*h2*R2)]
  for j,s in enumerate((S0,S1,S2)):record('Rdot'+str(j),[rd[j],-s])
  for name,gs,velocity,factor in (('phase',(gp2,gp3,gp4),0,D(1)),('baryon',(gb2,gb3,gb4),wb4,D(1)),('photon',(gg2,gg3,gg4),wg4,D(4)/3),('neutrino',(gn2,gn3,gn4),wn4,D(4)/3)):
   record(name+'_density0',[2*hr*gs[0],-factor*3*rd[0],factor*q0*q0*v2])
   record(name+'_density1',[hr*(3*gs[1]+2*h1*gs[0]),-factor*3*rd[1],factor*q0*q0*v3])
   record(name+'_density2',[hr*(4*gs[2]+3*h1*gs[1]+2*h2*gs[0]),-factor*3*rd[2],factor*q0*q0*(v4+velocity)])
  rad4=D(3)*hr*hr/2;matter3=b3+w3
  record('normal_minus2',[q0*q0*Psi0,3*hr*S0,rad4*(t*gg2+r*gn2)])
  record('normal_minus1',[q0*q0*Psi1,3*hr*(S1+h1*S0),rad4*(t*gg3+r*gn3),matter3*gp2])
  record('normal_zero',[q0*q0*Psi2,3*hr*(S2+h1*S1+h2*S0),rad4*(t*gg4+r*gn4),matter3*gp3])
  record('entropy_baryon_phase4',[gb4,-gp4,-Rstar*q0**4/(144*hr**4)]);record('entropy_photon_nu4',[gg4,-gn4,A*q0**4/(135*hr**4)])
  return dict(precision=precision,coefficients=c,independent_rows=checks)

def pol(c,prefix,powers,a):return sum((c[prefix+str(j)]*a**j for j in powers),D(0))
def finite_predictions(c,a):
 v={key:pol(c,pref,powers,a) for key,pref,powers in [('Gamma_phase','gp',(2,3,4)),('Gamma_b','gb',(2,3,4)),('Gamma_gamma','gg',(2,3,4)),('Gamma_nu','gn',(2,3,4)),('U','U',(4,5,6)),('w_nu','wn',(4,5,6)),('wb','wb',(4,5,6)),('wg','wg',(4,5,6)),('V','v',(2,3,4)),('Phi','Phi',(0,1,2)),('Psi','Psi',(0,1,2))]}
 v.update(R=c['Rstar']+pol(c,'R',(2,3,4),a),W=c['W6']*a**6,F_gamma_2=c['p3']*a**3+c['p4']*a**4,
  G_gamma_0=c['G03']*a**3+c['G04']*a**4,G_gamma_2=c['G23']*a**3+c['G24']*a**4,
  F_nu_2=pol(c,'N',(2,3,4),a),F_nu_3=c['J3']*a**3+c['J4']*a**4,F_nu_4=c['Fn44']*a**4,
  G_gamma_1=c['G15']*a**5,F_gamma_3=c['Fg35']*a**5,G_gamma_3=c['G35']*a**5)
 return v

def run():
 started=datetime.now(timezone.utc).isoformat();selfsha=sha(Path(__file__))
 names=[STEM+s for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')];assert all(not (BASE/n).exists() for n in names)
 def authenticate():
  assert sha(Path(__file__))==selfsha and not Path(__file__).stat().st_mode&0o222
  for n,s in PINS.items():assert sha(BASE/n)==s and not (BASE/n).stat().st_mode&0o222,n
 authenticate();manifest=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text());families=[]
 for label,step in (('FINE',2048),('START',1664)):
  cp=json.loads((BASE/(PARENT+'_'+label+'_CP_'+str(step).zfill(6)+'.json')).read_text())
  commit=json.loads((BASE/(PARENT+'_'+label+'_CP_'+str(step).zfill(6)+'_COMMIT.json')).read_text())
  assert cp['trial']==commit['trial']==label and cp['nstep']==commit['nstep']==step and cp['lineage']==commit['lineage']
  assert commit['sha256']==PINS[commit['payload']] and cp['lineage']['fixed']==manifest['fixed'] and cp['lineage']['inputs']==manifest['inputs']
  assert cp['lineage']['source_sha256']==manifest['source_sha256']==PINS['constrained_u_galaxy_horizon_stable_y_gauss_v002.py']
  snap=cp['snapshots'][0];assert snap['nstep']==0 and cp['ns']==32 and len(snap['cases'])==len(cp['seed_metadata'])==4
  fixed=cp['lineage']['fixed'];assert fixed['k_Mpc_inverse']==10 and cp['lineage']['omegas']==manifest['omegas']
  case0=snap['cases'][0];assert all(c['a']==case0['a'] and c['thermal']==case0['thermal'] and len(c['state'])==84 for c in snap['cases'])
  results=[coefficients(fixed,case0,p) for p in (80,120)];comparisons=[]
  with localcontext() as ctx:
   ctx.prec=160;diff={k:results[1]['coefficients'][k]-results[0]['coefficients'][k] for k in results[0]['coefficients']}
  for result in results:
   with localcontext() as ctx:
    ctx.prec=result['precision'];a=lift(case0['a']);pred=finite_predictions(result['coefficients'],a)
    for arm,case in enumerate(snap['cases']):
     saved={k:lift(case['stable_coordinates'][k]) for k in ('Gamma_phase','Gamma_b','Gamma_gamma','Gamma_nu','U','w_nu','wb','wg','V','R','W')}
     saved.update(Phi=lift(case['Phi']),Psi=lift(case['Psi']))
     for k,i in {'F_gamma_2':9,'F_gamma_3':10,'G_gamma_0':12,'G_gamma_1':13,'G_gamma_2':14,'G_gamma_3':15,'F_nu_2':17,'F_nu_3':18,'F_nu_4':19}.items():saved[k]=lift(case['state'][i])
     comparisons.append(dict(precision=result['precision'],arm=arm,omega=cp['lineage']['omegas'][arm],a=a,predicted=pred,saved=saved,signed_series_minus_saved={k:pred[k]-saved[k] for k in pred},original_seed_metadata=cp['seed_metadata'][arm],seed_parameter_difference={k:result['coefficients'][n]-lift(cp['seed_metadata'][arm][k]) for k,n in [('A','A'),('m','m'),('phi1','Phi1'),('psi1','Psi1')]}))
  families.append(dict(label=label,input_sha256=PINS[commit['payload']],coefficient_evaluations=results,signed_precision120_minus80=diff,finite_comparisons=comparisons))
 result=dict(status='COMPLETED_DESCRIPTIVE_SCALAR_COEFFICIENTS',owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),source_sha256=selfsha,input_sha256=PINS,families=families,
  physical_seed_qualified=False,new_initial_state_constructed=False,original_failure_flags_changed=False,thermal_or_microscopic_origin_qualified=False,full_metric_and_native_history_qualified=False,
  missing_contacts=['Phi3/Phi4/Psi3/Psi4/V5/V6 and absolute-pressure logarithms','W7/W8 for higher baryon Euler','higher angular and native reaction/history jets','finite normal/trace and complete primordial angular history'],new_residual_threshold=None)
 authenticate();data=(json.dumps(encode(result),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with (BASE/names[0]).open('xb') as f:f.write(data)
 (BASE/names[0]).chmod(0o444)
 report='# k10 scalar coefficient diagnostic V001\n\nTwo actual initial input families, two precisions, four unchanged frequency arms. All coefficients, independent row terms and finite series comparisons are saved; no pass threshold or replacement state.\n\nMissing higher metric, native and angular contacts remain explicit. Every original failure flag and live worker is unchanged.\n'
 with (BASE/names[1]).open('x') as f:f.write(report)
 (BASE/names[1]).chmod(0o444);authenticate()
 receipt=dict(status=result['status'],owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=selfsha,input_sha256=PINS,result_sha256=sha(BASE/names[0]),report_sha256=sha(BASE/names[1]))
 with (BASE/names[2]).open('xb') as f:f.write((json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n').encode())
 (BASE/names[2]).chmod(0o444);authenticate();assert sha(BASE/names[0])==receipt['result_sha256'] and sha(BASE/names[1])==receipt['report_sha256']
 print(json.dumps(dict(status=result['status'],pid=os.getpid(),result_sha256=receipt['result_sha256'],receipt_sha256=sha(BASE/names[2]))))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true',required=True);parser.parse_args();run()
