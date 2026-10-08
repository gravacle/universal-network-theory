"""Root-owned saved scalar density/current/angular completion; no producer calls."""
from pathlib import Path
from decimal import Decimal as D, localcontext
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, re
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_K10_SAVED_DENSITY_CURRENT_ANGULAR_COMPLETION_V001'
COMMON='CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001'
METRIC='CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001'
MACRO='CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002'
PROOF='CONSTRAINED_U_K10_DENSITY_CURRENT_AND_ANGULAR_COMPLETION_V001.md'
PINS={
 'constrained_u_k10_common_start_scalar_coefficients_v001.py':'5709f6e12e1c751ea7a253863c60328b1f30208037ccff692c6104966aea4839',
 COMMON+'.md':'8f831f8c0c8e3aef5cdf1fac5d29c52212445cf8d6c30fe34ada5460939c9495',
 COMMON+'_RESULT.json':'c8e6b26f229332a3371b46e1a2d8ba80bbaed1ca5fa64689f8c674260ca0dc47',
 COMMON+'_REPORT.md':'cab7660aa6b467ccf62d86dd4f25cbc2ea151f7fae77b914e6e7e9e5a59fd088',
 COMMON+'_RECEIPT.json':'f88f042d3332e8ff7de40cb612094d11b74356b416f105b8aa887ebbcecf0209',
 'constrained_u_k10_saved_metric_completion_v001.py':'a6409e33170e21c1b1423d9f685edff6b7fb0a2d2064f407d00875abf08867c2',
 METRIC+'.md':'a864cae70c86ee30d08ac24265faf14bbc80a04e80dd1dded7c25c1b458f3503',
 METRIC+'_RESULT.json':'04b48d6da753c2cca3b1d95d653a0b34d1c4a8e20a0da3a93bbc1193881bfa81',
 METRIC+'_REPORT.md':'3a12c5d303ab2201ebc80dc71fffd68465ff3a24e12d27294a2993d5506e043b',
 METRIC+'_RECEIPT.json':'42b7a05641f420dea5dea06d36d03a60b485c3de32e6496b51f151e8997203d3',
 PROOF:'c0bb7fc0f58c587fb0182383c894116ff1908533cfa6ad1e754dcf5232edfa4f',
 'constrained_u_galaxy_horizon_stable_y_gauss_v002.py':'f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531',
 MACRO+'_MANIFEST.json':'1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94',
 STEM+'.md':'b8353499e58edd0de0c25a774b0cd810585e42d7d336d7bf638e91efb568f924',
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
def P(v):return v if isinstance(v,list) else [D(v),D(0)]
def add(*vs):return [sum((P(v)[j] for v in vs),D(0)) for j in (0,1)]
def scale(v,k):return [k*z for z in P(v)]
def mul(a,b):
 a,b=P(a),P(b);assert a[1]*b[1]==0,'Unsupported retained log-square product'
 return [a[0]*b[0],a[0]*b[1]+a[1]*b[0]]
def deriv(v,k=0):v=P(v);return [k*v[0]+v[1],k*v[1]]
def inverse(v,k):v=P(v);return [(v[0]-v[1]/k)/k,v[1]/k]
def value(v,x):v=P(v);return v[0]+v[1]*x

def complete(base,metric,fixed,seeds,omegas,precision):
 with localcontext() as ctx:
  ctx.prec=precision;c={k:D(v) for k,v in base.items()};s={k:D(v) for k,v in metric['scalar_coefficients'].items()};p={k:[D(z) for z in v] for k,v in metric['polynomial_coefficients'].items()}
  assert len(c)==76 and metric['precision']==precision and metric['prior_coefficient_strings']==base
  hr,q,r,t,g0,h1,h2,beta,b3=(c[k] for k in ('hr','q0','r','t','g0','h1','h2','beta','b3'));h3,c3=s['h3'],s['c3'];h4=p['h4'];assert hr>0 and q>0 and g0>0 and beta>0 and c['w3']>0
  e1=-h1;e2=h1*h1-h2;e3=-h1**3+2*h1*h2-h3;e4=add(h1**4-3*h1*h1*h2+h2*h2+2*h1*h3,scale(h4,-1));F4=add(scale(h4,2),2*h1*h3+h2*h2)
  hv5=s['v5']+e1*c['v4']+e2*c['v3']+e3*c['v2'];hv6=add(p['v6'],e1*s['v5']+e2*c['v4']+e3*c['v3'],scale(e4,c['v2']))
  Kbar5=hv5+t*(c['U5']+e1*c['U4'])+r*(c['wn5']+e1*c['wn4'])
  Kbar6=add(hv6,t*(c['U6']+e1*c['U5']+e2*c['U4'])+r*(c['wn6']+e1*c['wn5']+e2*c['wn4']))
  R5=(-2*q*q*Kbar5/(15*hr)-t*s['p5']-r*s['N5']-44*h1*c['R4']+4*c3*c['gp2'])/28
  forcing=add(scale(inverse(Kbar6,6),-2*q*q/(3*hr)),-t*s['p6'],scale(p['N6'],-r),-65*h1*R5,scale(add(scale(F4,10),deriv(F4)),-c['R2']),5*c3*c['gp3']+(13*h1-b3/(hr*hr))*c3*c['gp2'])
  R61=forcing[1]/40;R6=[(forcing[0]-13*R61)/40,R61];I5=hv5/(5*hr);I6=scale(inverse(hv6,6),1/hr)
  JU5=(c['U5']-h1*c['U4'])/(5*hr);JU6=(c['U6']-h1*c['U5']+e2*c['U4'])/(6*hr);Jnu5=(c['wn5']-h1*c['wn4'])/(5*hr);Jnu6=(c['wn6']-h1*c['wn5']+e2*c['wn4'])/(6*hr)
  gp5=3*R5-q*q*I5;gb5=3*R5-q*q*(I5+JU5);gg5=4*R5-4*q*q*(I5+JU5)/3;gn5=4*R5-4*q*q*(I5+Jnu5)/3
  gb6=add(scale(R6,3),scale(I6,-q*q),-q*q*(JU6-c['W6']/(6*hr)));gg6=add(scale(R6,4),scale(I6,-4*q*q/3),-4*q*q*JU6/3);gn6=add(scale(R6,4),scale(I6,-4*q*q/3),-4*q*q*Jnu6/3)
  CU5=(5*h1+6*beta)*c['U6']+(4*h2+5*beta*h1)*c['U5']+(3*h3+4*beta*h2)*c['U4'];Cn5=5*h1*c['wn6']+4*h2*c['wn5']+3*h3*c['wn4']
  U7=(gg5/4-s['p5']/2-c3*c['gp2']-hr*CU5)/(6*hr);wn7=(gn5/4-s['N5']/2-c3*c['gp2']-hr*Cn5)/(6*hr)
  CU6=add((6*h1+7*beta)*U7+(5*h2+6*beta*h1)*c['U6']+(4*h3+5*beta*h2)*c['U5']+4*beta*h3*c['U4'],scale(h4,3*c['U4']));Cn6=add(6*h1*wn7+5*h2*c['wn6']+4*h3*c['wn5'],scale(h4,3*c['wn4']))
  U8=scale(inverse(add(scale(gg6,D(1)/4),-s['p6']/2-c3*c['gp3']-beta*c3*c['gp2'],scale(CU6,-hr)),7),1/hr)
  wn8=scale(inverse(add(scale(gn6,D(1)/4),scale(p['N6'],D(-1)/2),-c3*c['gp3'],scale(Cn6,-hr)),7),1/hr)
  W7=beta*(hr*(c['U5']+h1*c['U4'])+c['gg3']/4-c['p3']/2-g0*c['W6'])/g0
  W8=beta*(hr*(c['U6']+h1*c['U5']+h2*c['U4'])+c['gg4']/4-c['p4']/2-g0*W7-6*hr*c['W6'])/g0
  wb7=U7-W7+beta*c['W6'];wg7=U7+beta*c['W6'];wb8=add(U8,-W8+beta*W7-beta*beta*c['W6']);wg8=add(U8,beta*W7-beta*beta*c['W6'])
  G16=(q*(c['G04']-2*c['G24'])/3-5*hr*c['G15'])/g0;Fg36=(3*q*c['p4']/7-5*hr*c['Fg35'])/g0;G36=(3*q*c['G24']/7-5*hr*c['G35'])/g0
  Fn45=(4*q*c['J4']/(9*hr)-4*h1*c['Fn44'])/5;Fn46=(4*q*s['J5']/(9*hr)-5*h1*Fn45-4*h2*c['Fn44'])/6
  J6=(3*q*s['N5']/(7*hr)-4*q*Fn45/(7*hr)-5*h1*s['J5']-4*h2*c['J4']-3*h3*c['J3'])/6
  Qc=lift(fixed['Q0_over_Hstar'])*c['qinf'];Cbar=lift(.99);w0=-c['w3']*c3;rows={};arms=[]
  def record(store,name,terms):
   terms=[P(v) for v in terms];res=add(*terms);env=[sum((abs(v[j]) for v in terms),D(0)) for j in (0,1)]
   store[name]=dict(terms=terms,residual=res,absolute_term_sum=env,normalized=[res[j]/env[j] if env[j] else None for j in (0,1)])
  H={0:D(1),1:h1,2:h2,3:h3,4:h4};R={0:c['Rstar'],2:c['R2'],3:c['R3'],4:c['R4'],5:R5,6:R6};V={2:c['v2'],3:c['v3'],4:c['v4'],5:s['v5'],6:p['v6']}
  U={4:c['U4'],5:c['U5'],6:c['U6'],7:U7,8:U8};wn={4:c['wn4'],5:c['wn5'],6:c['wn6'],7:wn7,8:wn8};wb={4:c['wb4'],5:c['wb5'],6:c['wb6'],7:wb7,8:wb8};wg={4:c['wg4'],5:c['wg5'],6:c['wg6'],7:wg7,8:wg8}
  gg={2:c['gg2'],3:c['gg3'],4:c['gg4'],5:gg5,6:gg6};gn={2:c['gn2'],3:c['gn3'],4:c['gn4'],5:gn5,6:gn6};gb={2:c['gb2'],3:c['gb3'],4:c['gb4'],5:gb5,6:gb6};gp={2:c['gp2'],3:c['gp3'],4:c['gp4'],5:gp5}
  Cc={5:c3*c['gp2'],6:c3*c['gp3']};S={j:add(scale(wg[j+4],2*hr*hr*t),scale(wn[j+4],2*hr*hr*r),scale(wb.get(j+3,D(0)),b3)) for j in range(5)}
  def hd(seq,j,derivative=False):return add(*(scale(mul(h,deriv(seq[j-l],j-l) if derivative else seq[j-l]),hr) for l,h in H.items() if j-l in seq))
  for j in (5,6):
   Fb=add(t*s['p'+str(j)],scale(s['N5'] if j==5 else p['N6'],r));Gb=add(scale(gg[j],t),scale(gn[j],r))
   record(rows,'weighted_current'+str(j),[hd(S,j-2,True),scale(hd(S,j-2),3),scale(Gb,-hr*hr/2),scale(Fb,hr*hr),2*hr*hr*Cc[j],b3*Cc.get(j-1,D(0))])
   record(rows,'Rdot'+str(j),[hd(R,j,True),scale(S[j-2],-1),scale(hd(Cc,j),-1)])
   transport=[30*R5,44*h1*c['R4'],scale(Gb,D(-1)/2),Fb,-4*Cc[5]] if j==5 else [deriv(deriv(R6,6),7),65*h1*R5,scale(add(scale(F4,10),deriv(F4)),c['R2']),scale(Gb,D(-1)/2),Fb,-5*Cc[6],-(13*h1-b3/(hr*hr))*Cc[5]]
   record(rows,'curvature_transport'+str(j),transport)
   for name,G,v,f in (('baryon',gb,wb,D(1)),('photon',gg,wg,D(4)/3),('neutrino',gn,wn,D(4)/3)):
    record(rows,name+'_density'+str(j),[hd(G,j,True),scale(hd(R,j,True),-3*f),scale(add(V[j],v[j]),f*q*q)])
   record(rows,'U_pressure_current'+str(j),[hd(U,j+2,True),scale(hd(U,j+1,True),beta),scale(hd(U,j+2),-1),scale(gg[j],D(-1)/4),s['p'+str(j)]/2,Cc[j],beta*Cc.get(j-1,D(0))])
   record(rows,'nu_pressure_current'+str(j),[hd(wn,j+2,True),scale(hd(wn,j+2),-1),scale(gn[j],D(-1)/4),scale(s['N5'] if j==5 else p['N6'],D(1)/2),Cc[j]])
  record(rows,'phase_density5',[hd(gp,5,True),scale(hd(R,5,True),-3),q*q*s['v5']])
  record(rows,'slip7',[-hr*(c['U5']+h1*c['U4']),-c['gg3']/4,c['p3']/2,g0*c['W6'],g0*W7/beta])
  record(rows,'slip8',[6*hr*c['W6'],-hr*(c['U6']+h1*c['U5']+h2*c['U4']),-c['gg4']/4,c['p4']/2,g0*W7,g0*W8/beta])
  for name,new,drive,old in [('polarization_l1_6',G16,q*(c['G04']-2*c['G24'])/3,c['G15']),('photon_l3_6',Fg36,3*q*c['p4']/7,c['Fg35']),('polarization_l3_6',G36,3*q*c['G24']/7,c['G35'])]:record(rows,name,[g0*new,5*hr*old,-drive])
  record(rows,'nu_l4_5',[5*hr*Fn45,4*hr*h1*c['Fn44'],-4*q*c['J4']/9]);record(rows,'nu_l4_6',[6*hr*Fn46,5*hr*h1*Fn45,4*hr*h2*c['Fn44'],-4*q*s['J5']/9])
  record(rows,'nu_l3_6',[6*hr*J6,5*hr*h1*s['J5'],4*hr*h2*c['J4'],3*hr*h3*c['J3'],-3*q*s['N5']/7,4*q*Fn45/7])
  for j in (7,8):
   record(rows,'baryon_relative_reconstruction'+str(j),[wb[j],scale(U[j],-1),W7 if j==7 else W8,-beta*(c['W6'] if j==7 else W7),D(0) if j==7 else beta*beta*c['W6']])
   record(rows,'photon_relative_reconstruction'+str(j),[wg[j],scale(U[j],-1),-beta*(c['W6'] if j==7 else W7),D(0) if j==7 else beta*beta*c['W6']])
  rad4=3*hr*hr/2
  record(rows,'normal1',[q*q*s['Psi3'],scale(add(S[3],scale(S[2],h1),scale(S[1],h2),scale(S[0],h3)),3*hr),b3*c['gb4'],c['w3']*c['gp4'],scale(add(t*gg5,r*gn5),rad4)])
  record(rows,'normal2',[scale(p['Psi4'],q*q),scale(add(S[4],scale(S[3],h1),scale(S[2],h2),scale(S[1],h3),mul(h4,S[0])),3*hr),b3*gb5,c['w3']*gp5,scale(add(scale(gg6,t),scale(gn6,r)),rad4),w0*c['gp2']])
  assert len(rows)==31 and len(seeds)==len(omegas)==4
  for arm,(seed,omega) in enumerate(zip(seeds,omegas)):
   sigma2=lift(seed['sigma2']);eta6=Cbar*Qc*q*sigma2/(6*hr*c['w3']);gp6=add(scale(R6,3),scale(I6,-q*q),-eta6);ar={}
   record(ar,'eta6_given_saved_sigma2',[6*hr*c['w3']*eta6,-Cbar*Qc*q*sigma2]);record(ar,'phase_density6',[hd({**gp,6:gp6},6,True),scale(hd(R,6,True),-3),scale(p['v6'],q*q),Cbar*Qc*q*sigma2/c['w3']])
   arms.append(dict(arm=arm,omega=omega,original_seed_metadata=seed,sigma2=sigma2,eta6=eta6,gp6=gp6,independent_rows=ar))
  scalar=dict(e1=e1,e2=e2,e3=e3,Kbar5=Kbar5,R5=R5,I5=I5,JU5=JU5,JU6=JU6,Jnu5=Jnu5,Jnu6=Jnu6,gp5=gp5,gb5=gb5,gg5=gg5,gn5=gn5,U7=U7,wn7=wn7,W7=W7,W8=W8,wb7=wb7,wg7=wg7,G16=G16,Fg36=Fg36,G36=G36,J6=J6,Fn45=Fn45,Fn46=Fn46,Qc=Qc,Cbar=Cbar,w0=w0)
  polynomial=dict(e4=e4,F4=F4,Kbar6=Kbar6,curvature_forcing6=forcing,R6=R6,I6=I6,gb6=gb6,gg6=gg6,gn6=gn6,U8=U8,wn8=wn8,wb8=wb8,wg8=wg8)
  return dict(precision=precision,prior_coefficient_strings=base,prior_metric_scalar_strings=metric['scalar_coefficients'],prior_metric_polynomial_strings=metric['polynomial_coefficients'],scalar_coefficients=scalar,polynomial_coefficients=polynomial,native_arms=arms,independent_polynomial_rows=rows)

def predictions(out,a,arm):
 c={k:D(v) for k,v in out['prior_coefficient_strings'].items()};s=out['scalar_coefficients'];p=out['polynomial_coefficients'];x=a.ln();v={}
 for key,prefix,powers in [('Gamma_phase','gp',(2,3,4)),('Gamma_b','gb',(2,3,4)),('Gamma_gamma','gg',(2,3,4)),('Gamma_nu','gn',(2,3,4)),('U','U',(4,5,6)),('w_nu','wn',(4,5,6)),('wb','wb',(4,5,6)),('wg','wg',(4,5,6))]:
  v[key]=sum((c[prefix+str(j)]*a**j for j in powers),D(0));nextpower=5 if prefix in ('gp','gb','gg','gn') else 7;co6=out['native_arms'][arm]['gp6'] if prefix=='gp' else p[prefix+str(nextpower+1)]
  v[key]+=s[prefix+str(nextpower)]*a**nextpower+value(co6,x)*a**(nextpower+1)
 v.update(R=c['Rstar']+sum((c['R'+str(j)]*a**j for j in (2,3,4)),D(0))+s['R5']*a**5+value(p['R6'],x)*a**6,W=c['W6']*a**6+s['W7']*a**7+s['W8']*a**8,
  G_gamma_1=c['G15']*a**5+s['G16']*a**6,F_gamma_3=c['Fg35']*a**5+s['Fg36']*a**6,G_gamma_3=c['G35']*a**5+s['G36']*a**6,
  F_nu_3=c['J3']*a**3+c['J4']*a**4+D(out['prior_metric_scalar_strings']['J5'])*a**5+s['J6']*a**6,F_nu_4=c['Fn44']*a**4+s['Fn45']*a**5+s['Fn46']*a**6)
 return v

def run():
 started=datetime.now(timezone.utc).isoformat();selfsha=sha(Path(__file__));outputs=[STEM+s for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')];assert all(not (BASE/n).exists() for n in outputs);pins=dict(PINS)
 def authenticate():
  assert sha(Path(__file__))==selfsha and not Path(__file__).stat().st_mode&0o222
  for n,s in pins.items():assert sha(BASE/n)==s and not (BASE/n).stat().st_mode&0o222,n
 authenticate();common=json.loads((BASE/(COMMON+'_RESULT.json')).read_text());metric=json.loads((BASE/(METRIC+'_RESULT.json')).read_text())
 for parent,stem,status,source in [(common,COMMON,'COMPLETED_DESCRIPTIVE_SCALAR_COEFFICIENTS','constrained_u_k10_common_start_scalar_coefficients_v001.py'),(metric,METRIC,'COMPLETED_DESCRIPTIVE_METRIC_COEFFICIENTS','constrained_u_k10_saved_metric_completion_v001.py')]:
  receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text());assert parent['status']==receipt['status']==status and parent['owner']==receipt['owner']=='root' and parent['source_sha256']==receipt['source_sha256']==PINS[source] and parent['input_sha256']==receipt['input_sha256']
  assert receipt['result_sha256']==PINS[stem+'_RESULT.json'] and receipt['report_sha256']==PINS[stem+'_REPORT.md']
  for n,s in parent['input_sha256'].items():assert n not in pins or pins[n]==s;pins[n]=s
 for n,s in re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',(BASE/PROOF).read_text(),re.M):assert n not in pins or pins[n]==s;pins[n]=s
 authenticate();assert all(v is False for v in metric['prior_false_flags'].values()) and metric['new_state_constructed'] is metric['full_trace_qualified'] is False and metric['new_residual_threshold'] is None
 fixed=json.loads((BASE/(MACRO+'_MANIFEST.json')).read_text())['fixed'];assert fixed['k_Mpc_inverse']==10 and len(common['families'])==len(metric['families'])==2;families=[]
 for old,met,label,step in zip(common['families'],metric['families'],('FINE','START'),(2048,1664)):
  assert old['label']==met['label']==label and [e['precision'] for e in old['coefficient_evaluations']]==[80,120] and [e['precision'] for e in met['metric_evaluations']]==[80,120]
  cp=json.loads((BASE/(MACRO+'_'+label+'_CP_'+str(step).zfill(6)+'.json')).read_text());assert cp['lineage']['fixed']==fixed and cp['snapshots'][0]['nstep']==0;seeds=cp['seed_metadata'];omegas=cp['lineage']['omegas']
  out=[complete(e['coefficients'],me,fixed,seeds,omegas,e['precision']) for e,me in zip(old['coefficient_evaluations'],met['metric_evaluations'])];comparisons=[]
  with localcontext() as ctx:
   ctx.prec=160;diff={section:{k:add(out[1][section][k],scale(out[0][section][k],D(-1))) for k in out[0][section]} for section in ('scalar_coefficients','polynomial_coefficients')};reaction_diff=[dict(arm=j,eta6=out[1]['native_arms'][j]['eta6']-out[0]['native_arms'][j]['eta6'],gp6=add(out[1]['native_arms'][j]['gp6'],scale(out[0]['native_arms'][j]['gp6'],D(-1)))) for j in range(4)]
  for previous in old['finite_comparisons']:
   assert previous['original_seed_metadata']==seeds[previous['arm']] and previous['omega']==omegas[previous['arm']]
   with localcontext() as ctx:
    ctx.prec=previous['precision'];new=out[0 if ctx.prec==80 else 1];pred=predictions(new,D(previous['a']),previous['arm']);saved={k:previous['saved'][k] for k in pred};prior={k:previous['predicted'][k] for k in pred}
    comparisons.append(dict(precision=ctx.prec,arm=previous['arm'],omega=previous['omega'],a=previous['a'],completed_series=pred,saved=saved,prior_series=prior,signed_series_minus_saved={k:pred[k]-D(saved[k]) for k in pred},completion_minus_prior={k:pred[k]-D(prior[k]) for k in pred}))
  assert len(comparisons)==8;families.append(dict(label=label,completion_evaluations=out,signed_precision120_minus80=diff,native_precision120_minus80=reaction_diff,finite_comparisons=comparisons))
 result=dict(status='COMPLETED_DESCRIPTIVE_DENSITY_CURRENT_ANGULAR_COEFFICIENTS',owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),source_sha256=selfsha,input_sha256=pins,families=families,prior_false_flags=metric['prior_false_flags'],prior_missing_contacts=metric['prior_missing_contacts'],prior_metric_remaining_contacts=metric['remaining_contacts'],new_residual_threshold=None,new_state_constructed=False,full_trace_qualified=False,physical_seed_qualified=False,
  sigma2_scope='Exact saved original binary64 per-arm sigma2; Qc uses fixed Q0_over_Hstar and prior qinf at matching precision. No independent high-precision native certificate.',remaining_contacts=['higher native z7/z8 and reaction/history jets','higher baryon Euler needs W9/W10; finite angular cut is not complete history','all finite normal/shear/trace/momentum/current constraints and all-order remainder'])
 authenticate();data=(json.dumps(encode(result),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with (BASE/outputs[0]).open('xb') as f:f.write(data)
 (BASE/outputs[0]).chmod(0o444)
 with (BASE/outputs[1]).open('x') as f:f.write('# Saved k10 density/current/angular completion V001\n\nTwo unchanged input families at 80/120 digits; four separately retained saved native sigma2 arms. All coefficient strings, original-row residual terms/envelopes and sixteen signed old-state comparisons are stored. No new threshold, initial state, trajectory or physical qualification.\n')
 (BASE/outputs[1]).chmod(0o444);authenticate();receipt=dict(status=result['status'],owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=selfsha,input_sha256=pins,result_sha256=sha(BASE/outputs[0]),report_sha256=sha(BASE/outputs[1]))
 with (BASE/outputs[2]).open('xb') as f:f.write((json.dumps(receipt,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())
 (BASE/outputs[2]).chmod(0o444);authenticate();assert sha(BASE/outputs[0])==receipt['result_sha256'] and sha(BASE/outputs[1])==receipt['report_sha256']
 print(json.dumps(dict(status=result['status'],pid=os.getpid(),result_sha256=receipt['result_sha256'],receipt_sha256=sha(BASE/outputs[2]))))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true',required=True);parser.parse_args();run()
