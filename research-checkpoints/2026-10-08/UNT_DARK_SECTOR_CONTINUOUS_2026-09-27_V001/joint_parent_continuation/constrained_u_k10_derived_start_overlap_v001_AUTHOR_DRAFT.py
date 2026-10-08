"""Prospective short overlap of two derived preparations; root execution only.
This AUTHOR_DRAFT is never executed. Frozen inputs/protocol remain pending.
"""
from pathlib import Path
from decimal import Decimal as D, localcontext
from datetime import datetime, timezone
from functools import lru_cache
import argparse, ast, hashlib, json, math, os, time, traceback
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001'
PARENT='CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002'
COMMON='CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001'
METRIC='CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001'
COMPLETE='CONSTRAINED_U_K10_SAVED_DENSITY_CURRENT_ANGULAR_COMPLETION_V001'
AI=2e-8; AC=3e-8; CURVATURE=1e-5; K=10.; KB=.02; C=1.98; CBAR=.99
CP=299792458.; MPC=3.0856775814913673e22
OMEGAS=(.1,1.,10.,100.); REFINEMENTS=(64,128)
PINS={}; PROTOCOL_SHA='PENDING'; NATIVE_PROOF='PENDING'
DEFINITIONS=('sha','load_declared_helpers','legendre','bessel','si_vector','initial_transport','gauss','equilibrate','to_raw','chart_coefficients','chart_rates','chart_stage_matrix','lagrange_values','cubic_envelope','CubicKernel','stable_anchor','stable_initial_multipoles','compensated_residual','gauss_block_solve','source_vectors','memory_panel','fixed_panel_response','free_history_response','source_envelopes','coupled_gauss','load_optical_namespace','finite_tree')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lift(v):return D.from_float(float(v))
def encode(v):
 if isinstance(v,D):assert v.is_finite();return str(v)
 if isinstance(v,np.ndarray):return encode(v.tolist())
 if isinstance(v,np.generic):return encode(v.item())
 if isinstance(v,dict):return {str(k):encode(w) for k,w in v.items()}
 if isinstance(v,(list,tuple)):return [encode(w) for w in v]
 if type(v) is float:assert math.isfinite(v)
 return v
def write(name,v):
 p=BASE/name;data=(json.dumps(encode(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);return sha(p)
def load_definitions():
 p=BASE/'constrained_u_galaxy_horizon_stable_y_gauss_v002.py';tree=ast.parse(p.read_text())
 nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in DEFINITIONS]
 assert {n.name for n in nodes}==set(DEFINITIONS)
 env=dict(BASE=BASE,Path=Path,ast=ast,hashlib=hashlib,np=np,math=math,json=json,lru_cache=lru_cache,K=K,CP=CP,MPC=MPC,KB=KB,C=C,CBAR=CBAR,CURVATURE=CURVATURE,
  EARLY_SOURCE_SHA=PINS['constrained_u_clock_gradient_early_transfer_v004.py'],OPTICAL_KERNEL_SHA=PINS['actual_opacity_retarded_radiation_kernel_v001.py'],CHECKED_HELPERS=('background','Thermal','Layout','coefficients','rates','stage_matrix','snapshot'))
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<unchanged-short-overlap-definitions>','exec'),env)
 return env
def value(v,x):return D(v[0])+D(v[1])*x if isinstance(v,list) else D(v)
def coefficients(common,metric,completion,index):
 c=dict(common['families'][index]['coefficient_evaluations'][1]['coefficients'])
 m=metric['families'][index]['metric_evaluations'][1]
 c.update(m['scalar_coefficients']);c.update(m['polynomial_coefficients'])
 z=completion['families'][index]['completion_evaluations'][1]
 c.update(z['scalar_coefficients']);c.update(z['polynomial_coefficients'])
 return c,z
def native_coefficients(c,arm,snodes,weights,omega,fixed):
 with localcontext() as ctx:
  ctx.prec=120
  hr,q,Qc,c3,h1,h2,cb=(D(c[k]) for k in ('hr','q0','Qc','c3','h1','h2','Cbar'))
  gp2,gp3,gp4=(D(c['gp'+str(j)]) for j in (2,3,4))
  ww=list(map(lift,weights));frequencies=list(map(lift,omega**2*snodes**2));sigma2=D(arm['sigma2'])
  z6=list(map(lift,arm['original_seed_metadata']['native_z6']));assert len(z6)==len(ww)==len(frequencies)==32
  def average(v):return sum((w*t for w,t in zip(ww,v)),D(0))
  Z6=average(z6);alpha=average(frequencies);Delta0=alpha+2*cb*Qc*Qc/lift(KB);assert Delta0>0
  n5=7*hr*Z6/(Qc*q)-c3*gp2;ell2=lift(fixed['ell_native'])**2
  sigma3=(hr*Qc*q*c3*(7*gp3+6*h1*gp2)-hr*hr*h1*Z6)/Delta0
  z7=[(f*sigma3-90*hr*hr*h1*z)/(56*hr*hr) for f,z in zip(frequencies,z6)];Z7=average(z7)
  R16=average([f*z for f,z in zip(frequencies,z6)])
  sigma4=(hr*Qc*q*c3*(8*gp4+7*h1*gp3+6*h2*gp2)-alpha*q*n5+ell2*q*q*R16-hr*hr*h1*Z7-16*cb*hr*Qc*Z6/lift(KB))/Delta0
  z8=[(f*(sigma4+q*n5-ell2*q*q*z)-119*hr*hr*h1*zz)/(72*hr*hr) for f,z,zz in zip(frequencies,z6,z7)]
  Z8=average(z8);n6=hr*(8*Z7+7*h1*Z6)/(Qc*q)-c3*gp3;n7=hr*(9*Z8+8*h1*Z7+7*h2*Z6)/(Qc*q)-c3*gp4
  P4=lift(KB)*q*n5/2;P5=lift(KB)*q*n6/2;P6=lift(KB)*q*n7/2+cb*Z6
  rows={}
  def record(name,terms):
   residual=sum(terms,D(0));envelope=sum(map(abs,terms),D(0))
   rows[name]=dict(terms=terms,residual=residual,absolute_term_sum=envelope,normalized=residual/envelope if envelope else None)
  for i,(f,v6,v7,v8) in enumerate(zip(frequencies,z6,z7,z8)):
   record('mode6_'+str(i),[42*hr*hr*v6,-f*sigma2])
   record('mode7_'+str(i),[56*hr*hr*v7,90*hr*hr*h1*v6,-f*sigma3])
   record('mode8_'+str(i),[72*hr*hr*v8,119*hr*hr*h1*v7,-f*sigma4,-f*q*n5,f*ell2*q*q*v6])
  record('native_Euler2',[6*hr*P4,cb*Qc*sigma2])
  record('native_Euler3',[7*hr*P5,6*hr*h1*P4,cb*Qc*sigma3])
  record('native_Euler4',[8*hr*P6,7*hr*h1*P5,6*hr*h2*P4,cb*Qc*sigma4])
  return dict(z6=z6,z7=z7,z8=z8,sigma2=sigma2,sigma3=sigma3,sigma4=sigma4,Z6=Z6,Z7=Z7,Z8=Z8,alpha=alpha,Delta0=Delta0,n5=n5,n6=n6,n7=n7,
   binary_input_weight_sum=sum(ww,D(0)),independent_rows=rows,scope='Given saved binary64 z6/sigma2; actual mode-node frequencies and weights lifted separately; no independent physical native qualification')
def derived_seed(a,c,z,arm,fixed,lay,therm,snodes,weights,omega,helpers,env):
 with localcontext() as ctx:
  ctx.prec=120;aa=lift(a);xx=aa.ln()
  def jet(prefix,powers):return sum((value(c[prefix+str(j)],xx)*aa**j for j in powers),D(0))
  y=np.zeros(lay.n);y[0]=float(D(c['Rstar'])+jet('R',range(2,7)))
  y[1]=float(jet('gb',range(2,7)));y[2]=float(jet('U',range(4,9)))
  y[3]=float(jet('gg',range(2,7)));y[4]=float(jet('W',range(6,9)))
  y[5]=float(jet('gn',range(2,7)));y[6]=float(jet('wn',range(4,9)))
  y[7]=float(jet('gp',range(2,6))+value(z['native_arms'][arm]['gp6'],xx)*aa**6)
  y[8]=float(jet('v',range(2,7)))
  y[lay.fg[2]]=float(jet('p',range(3,7)));y[lay.fg[3]]=float(jet('Fg3',range(5,7)))
  y[lay.pol[0]]=float(jet('G0',range(3,7)));y[lay.pol[1]]=float(jet('G1',range(5,7)))
  y[lay.pol[2]]=float(jet('G2',range(3,7)));y[lay.pol[3]]=float(jet('G3',range(5,7)))
  y[lay.fn[2]]=float(jet('N',range(2,7)));y[lay.fn[3]]=float(jet('J',range(3,7)));y[lay.fn[4]]=float(jet('Fn4',range(4,7)))
  nc=native_coefficients(c,z['native_arms'][arm],snodes,weights,omega,fixed)
  bg=helpers['background'](math.log(a),fixed)
  y[lay.z]=sum(np.asarray(nc['z'+str(j)],float)*a**j for j in (6,7,8))
  y[lay.zd]=bg['h']*sum(j*np.asarray(nc['z'+str(j)],float)*a**j for j in (6,7,8))
  before=y.copy();shifts=[]
  for _ in range(3):
   f=env['chart_coefficients'](math.log(a),y,fixed,lay,therm,snodes,weights,omega,helpers)
   P=KB*f['q']*f['ncalc']/2+CBAR*f['Z']
   terms=[f['q']**2*f['psi'],3*f['h']*f['S'],f['b']*y[1],f['rg']*y[3],f['rn']*y[5],f['w']*y[7],-f['q']*P]
   den=f['b']+4*(f['rg']+f['rn'])/3+f['w']+KB*f['q']**2*f['c']/2
   shift=-math.fsum(map(float,terms))/den;shifts.append(shift)
   y[1]+=shift;y[7]+=shift;y[3]+=4*shift/3;y[5]+=4*shift/3
  return y,dict(unrepaired_state=before,normal_shifts=shifts,native_coefficient_packet=nc,
   density_entropy_before=[before[1]-before[7],before[3]-before[5],before[1]-.75*before[3]],
   density_entropy_after=[y[1]-y[7],y[3]-y[5],y[1]-.75*y[3]],
   scope='Derived finite truncation and exact finite normal/shear; no full Cauchy or microscopic birth certificate')
def snapshot(a,y,fixed,lay,therm,snodes,weights,omega,helpers,env):
 dy,f=env['chart_rates'](math.log(a),y,fixed,lay,therm,snodes,weights,omega,helpers)
 q,h,b,rg,rn,w=(f[k] for k in ('q','h','b','rg','rn','w'));P=KB*q*f['ncalc']/2+CBAR*f['Z']
 nt=[q*q*f['psi'],3*h*f['S'],b*y[1],rg*y[3],rn*y[5],w*y[7],-q*P]
 contrast=y[1]+3*h*f['wb'];Eb=b*contrast;Eg=rg*(y[3]+4*h*f['wg']);En=rn*(y[5]+4*h*y[6]);Ec=w*y[7];Ep=-q*P
 raw=env['to_raw'](y,f['bg'],fixed);Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
 reads=[raw[3]/4+f['phi'],q*raw[4],q*raw[2],f['psi']+f['phi'],y[lay.fg[2]],Pi,y[lay.fn[2]],contrast,Eb,Eg+En,Ec,Ep,-KB*q*q*f['ncalc']/2,-CBAR*q*f['Z'],q*f['ncalc']]
 normal=math.fsum(map(float,nt));raw_nt=[q*q*f['psi'],3*h*f['mom'],b*raw[1],rg*raw[3],rn*raw[5],w*raw[7],-q*P]
 normal_error=abs(normal)/max(sum(abs(float(t)) for t in raw_nt),q*q*CURVATURE*1e-10)
 stable_error=abs(normal)/max(sum(abs(float(t)) for t in nt),q*q*CURVATURE*1e-10)
 vdd=(float(weights@dy[lay.zd])-2*f['Ld']*f['vd']-f['Ldd']*f['v'])/f['L']
 nd=vdd-f['bg']['cs_dt']*y[7]-f['c']*dy[7]
 et=[KB*q*nd/2,-KB*h*q*f['ncalc']/2,CBAR*f['Zd'],2*h*P,CBAR*f['Q']*f['sigma']]
 ef=KB*q*CURVATURE*max(h,f['Q'],omega)*1e-10/2
 wbd=f['g']*y[4]/f['rb']-f['c']*y[7]
 wgd=h*f['wg']+y[3]/4-y[lay.fg[2]]/2-f['g']*y[4]-f['c']*y[7]
 Sdot=b*(wbd-3*h*f['wb'])+4*rg*(wgd-4*h*f['wg'])/3+4*rn*(dy[6]-4*h*y[6])/3
 total=b+4*(rg+rn)/3+w;totaldot=-3*h*b-16*h*(rg+rn)/3-3*h*(1+f['c'])*w
 momdot=Sdot+totaldot*y[8]+total*dy[8]
 phid=f['psid']-2*(rg*(dy[lay.fg[2]]-2*h*y[lay.fg[2]])+rn*(dy[lay.fn[2]]-2*h*y[lay.fn[2]]))/q**2
 psidd=momdot-f['bg']['h_dt']*f['phi']-h*phid
 tt=[psidd,h*phid,3*h*f['psid'],(2*f['bg']['h_dt']+3*h*h)*f['phi'],q*q*(f['psi']-f['phi'])/3,-f['c']*w*raw[7],-(rg*raw[3]+rn*raw[5])/3]
 tf=CURVATURE*max(h*h,q*q)*1e-12
 return dict(a=f['bg']['a'],stable_state=y,raw_state=raw,readouts=reads,normal_terms=nt,normal_error=normal_error,
  Phi=f['phi'],Psi=f['psi'],w=w,Gamma_phase=y[7],sigma=f['sigma'],n=f['ncalc'],physical_seed_qualified=False,
  native_Euler_terms=et,native_Euler_error=abs(math.fsum(map(float,et)))/max(sum(abs(float(t)) for t in et),ef),
  proper_trace_terms=tt,proper_trace_error=abs(math.fsum(map(float,tt)))/max(sum(abs(float(t)) for t in tt),tf),
  positive_baryon_drag_used=True,old_failure_flags_changed=False,raw_normal_terms=raw_nt,raw_normal_residual=math.fsum(map(float,raw_nt)),stable_normal_error=stable_error,
  shear_error=abs(f['psi']-f['phi']-2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2)/CURVATURE)
def propagate(n,initial,fixed,lay,therm,snodes,weights,helpers,env,seeds,lineage,authenticate):
 xs=np.linspace(math.log(AI),math.log(AC),n+1);optical=env['CubicKernel'](fixed,therm)
 eta=[0.]
 for lo,hi in zip(xs[:-1],xs[1:]):eta.append(eta[-1]+float(optical.integral(float(lo),float(hi),16)[1]))
 eta=np.array(eta);c1=.5-math.sqrt(3)/6;c2=.5+math.sqrt(3)/6
 moments=[env['stable_initial_multipoles'](y,lay,K*CP/(1000*fixed['Hunit']*AI),helpers['background'](math.log(AI),fixed),fixed) for y in initial]
 targets=[]
 for i in range(1,n+1):
  lo=float(xs[i-1]);dx=float(xs[i]-xs[i-1]);xx=(lo+c1*dx,lo+c2*dx,float(xs[i]))
  targets.append([eta[i-1]+float(optical.integral(lo,xj,16)[1]) if j<2 else float(eta[i]) for j,xj in enumerate(xx)])
 phases=K*(np.asarray(targets)-eta[0]);transported=[];transport_errors=[]
 for mm in moments:
  transported.append({kind:np.array([env['initial_transport'](coeff,phases,l).real for l in range(5)]) for kind,coeff in mm.items()})
  transport_errors.append({kind:float(np.max(abs(transported[-1][kind]-np.array([env['initial_transport'](coeff,phases,l,256).real for l in range(5)]))))/CURVATURE for kind,coeff in mm.items()})
 anchors=[[env['stable_anchor'](xs[0],eta[0],y,fixed,lay,therm,snodes,weights,om,helpers)] for y,om in zip(initial,OMEGAS)]
 error_keys=('stage_error','dense_error','metric_momentum_error','curvature_increment_error','baryon_Euler_error')
 states=[y.copy() for y in initial];errors=[{k:0. for k in error_keys} for _ in OMEGAS];last_stages=[None]*4
 trajectory=[{k:dict(maximum=0.,location=None) for k in error_keys[2:]} for _ in OMEGAS]
 start=0;commits=sorted(BASE.glob(STEM+'_N'+str(n)+'_CP_*_COMMIT.json'))
 expected=list(range(32,n+1,32));seen=[];prior=None
 payloads=[p for p in BASE.glob(STEM+'_N'+str(n)+'_CP_*.json') if not p.name.endswith('_COMMIT.json')]
 assert len(payloads)==len(commits),'Preserved orphan checkpoint requires explicit recovery before reuse'
 for path in commits:
  commit=json.loads(path.read_text());cp=json.loads((BASE/commit['payload']).read_text())
  env['finite_tree'](cp);env['finite_tree'](commit)
  assert set(cp)=={'lineage','owner','pid','n','nstep','xs','eta','states','anchors','moments','seeds','errors','last_stages','optical_controls','trajectory_diagnostics'}
  assert cp['owner']=='root' and type(cp['pid']) is int and cp['pid']>0 and type(cp['nstep']) is int
  assert sha(BASE/commit['payload'])==commit['sha256'] and cp['lineage']==lineage and cp['n']==n
  name=STEM+'_N'+str(n)+'_CP_'+str(cp['nstep']).zfill(6)+'.json'
  assert commit==dict(lineage=lineage,owner='root',pid=cp['pid'],n=n,nstep=cp['nstep'],payload=name,sha256=sha(BASE/name))
  assert cp['xs']==xs.tolist() and cp['eta']==eta.tolist() and cp['moments']==encode(moments) and cp['seeds']==encode(seeds)
  assert len(cp['states'])==len(cp['anchors'])==len(cp['errors'])==len(cp['last_stages'])==4
  assert all(len(y)==lay.n for y in cp['states']) and all(set(e)==set(error_keys) and all(v>=0 for v in e.values()) for e in cp['errors'])
  assert len(cp['trajectory_diagnostics'])==4 and all(set(t)==set(error_keys[2:]) for t in cp['trajectory_diagnostics'])
  for arm,t in enumerate(cp['trajectory_diagnostics']):
   for k,v in t.items():assert set(v)=={'maximum','location'} and v['maximum']==cp['errors'][arm][k] and v['maximum']>=0
  assert set(cp['optical_controls'])==set(optical.maximum) and all(v>=0 for v in cp['optical_controls'].values())
  sk={'x','eta','R','qV','cGamma','Gamma','dipole','Pi'}
  for arm,history in enumerate(cp['anchors']):
   assert len(history)==cp['nstep']+1 and set(history[0])==sk
   for j,row in enumerate(history[1:],1):
    assert set(row)==sk|{'panel_nodes','panel_envelopes'} and len(row['panel_nodes'])==4 and len(row['panel_envelopes'])==3
    pp=row['panel_nodes'];assert all(set(v)==sk for v in pp) and all(v>=0 for v in row['panel_envelopes'])
    assert all(pp[k]['x']<pp[k+1]['x'] and pp[k]['eta']<pp[k+1]['eta'] for k in range(3))
    assert pp[0]=={k:v for k,v in history[j-1].items() if k in sk} and pp[-1]=={k:v for k,v in row.items() if k in sk}
   st=cp['last_stages'][arm]
   assert set(st)=={'x','dx','coordinates','conformal','previous','states','algebraic_states','stage_error','dense_error'}
   assert len(st['states'])==len(st['coordinates'])==len(st['conformal'])==len(st['algebraic_states'])==3
   assert all(len(v)==lay.n for v in st['states']) and all(len(v)==2 for v in st['algebraic_states']) and len(st['previous'])==lay.n
   assert st['states'][-1]==cp['states'][arm] and st['coordinates'][-1]==cp['xs'][cp['nstep']] and st['conformal'][-1]==cp['eta'][cp['nstep']]
  if prior:
   assert all(cp['anchors'][a][:len(prior['anchors'][a])]==prior['anchors'][a] for a in range(4))
   assert all(cp['errors'][a][k]>=prior['errors'][a][k] for a in range(4) for k in prior['errors'][a])
   assert all(cp['optical_controls'][k]>=prior['optical_controls'][k] for k in prior['optical_controls'])
  seen.append(cp['nstep'])
  prior=cp
 assert seen==expected[:len(seen)]
 if commits:
  start=cp['nstep'];states=[np.array(v,float) for v in cp['states']];anchors=cp['anchors'];errors=cp['errors'];last_stages=cp['last_stages'];optical.maximum=cp['optical_controls'];trajectory=cp['trajectory_diagnostics']
 for i in range(start+1,n+1):
  lo=float(xs[i-1]);dx=float(xs[i]-xs[i-1]);xx=(lo+c1*dx,lo+c2*dx,float(xs[i]))
  ee=targets[i-1]
  optical.weight_cache.clear();next_states=[]
  for arm,om in enumerate(OMEGAS):
   iv=[{kind:arr[:,i-1,j] for kind,arr in transported[arm].items()} for j in range(3)]
   stage,err,final,record=env['coupled_gauss'](states[arm],lo,dx,ee,anchors[arm],fixed,lay,therm,snodes,weights,om,helpers,iv,optical,dense=i%32==0)
   previous=states[arm];before=env['chart_coefficients'](lo,previous,fixed,lay,therm,snodes,weights,om,helpers)
   stage_f=[env['chart_coefficients'](xj,yj,fixed,lay,therm,snodes,weights,om,helpers) for xj,yj in zip(xx,stage)]
   after=stage_f[-1]
   tests={
    'metric_momentum_error':(after['psi']-before['psi'],[f['mom']/f['h']-f['phi'] for f in stage_f[:2]],abs(after['psi'])+abs(before['psi'])),
    'curvature_increment_error':(stage[-1][0]-previous[0],[f['Rd']/f['h'] for f in stage_f[:2]],abs(stage[-1][0])+abs(previous[0])),
    'baryon_Euler_error':((stage[-1][8]+after['wb'])-(previous[8]+before['wb']),[(f['phi']+f['g']*stage[j][4]/f['rb'])/f['h'] for j,f in enumerate(stage_f[:2])],abs(stage[-1][8]+after['wb'])+abs(previous[8]+before['wb']))}
   for key,(delta,forces,scale0) in tests.items():
    integral=dx*math.fsum(map(float,forces))/2;residual=delta-integral;scale=scale0+abs(dx)*math.fsum(abs(float(v)) for v in forces)/2
    err[key]=abs(residual)/max(scale,CURVATURE*1e-18)
    if err[key]>trajectory[arm][key]['maximum']:
     trajectory[arm][key]=dict(maximum=err[key],location=dict(nstep=i,a=math.exp(float(xs[i])),delta=delta,gauss_integral=integral,residual=residual,scale=scale,forces=forces,log_step=dx))
   assert record['coordinates'][-1]==float(xs[i]);next_states.append(stage[-1]);anchors[arm].append(final);last_stages[arm]=record
   for k in errors[arm]:errors[arm][k]=max(errors[arm][k],err[k])
  states=next_states
  if i%32==0 or i==n:
   authenticate();name=STEM+'_N'+str(n)+'_CP_'+str(i).zfill(6)+'.json'
   ch=write(name,dict(lineage=lineage,owner='root',pid=os.getpid(),n=n,nstep=i,xs=xs,eta=eta,states=states,anchors=anchors,moments=moments,seeds=seeds,errors=errors,last_stages=last_stages,optical_controls=optical.maximum,trajectory_diagnostics=trajectory))
   write(name[:-5]+'_COMMIT.json',dict(lineage=lineage,owner='root',pid=os.getpid(),n=n,nstep=i,payload=name,sha256=ch));authenticate()
   print('OVERLAP',n,i,flush=True)
 return dict(n=n,endpoint=[snapshot(AC,y,fixed,lay,therm,snodes,weights,om,helpers,env) for y,om in zip(states,OMEGAS)],errors=errors,optical_controls=optical.maximum,initial_angular128_256_errors=transport_errors,trajectory_diagnostics=trajectory)
def main(resume):
 assert PROTOCOL_SHA!='PENDING' and PINS and NATIVE_PROOF!='PENDING'
 started=datetime.now(timezone.utc).isoformat();source_sha=sha(__file__);tick=time.monotonic()
 assert not any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json'))
 if not resume:assert not any(BASE.glob(STEM+'*CP*.json')) and not (BASE/(STEM+'_MANIFEST.json')).exists()
 def authenticate():
  assert sha(__file__)==source_sha and not Path(__file__).stat().st_mode&0o222
  for p,h in PINS.items():assert sha(BASE/p)==h and not (BASE/p).stat().st_mode&0o222,p
 authenticate();fixed=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())['fixed']
 lineage=dict(source_sha256=source_sha,input_sha256=PINS,fixed=fixed,ai=AI,ac=AC,refinements=REFINEMENTS,omegas=OMEGAS,ns=32,numpy_version=np.__version__)
 mp=BASE/(STEM+'_MANIFEST.json')
 if mp.exists():assert json.loads(mp.read_text())==encode(lineage)
 else:write(mp.name,lineage)
 common=json.loads((BASE/(COMMON+'_RESULT.json')).read_text());metric=json.loads((BASE/(METRIC+'_RESULT.json')).read_text());completion=json.loads((BASE/(COMPLETE+'_RESULT.json')).read_text())
 for packet,stem,status in ((common,COMMON,'COMPLETED_DESCRIPTIVE_SCALAR_COEFFICIENTS'),(metric,METRIC,'COMPLETED_DESCRIPTIVE_METRIC_COEFFICIENTS'),(completion,COMPLETE,'COMPLETED_DESCRIPTIVE_DENSITY_CURRENT_ANGULAR_COEFFICIENTS')):
  receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
  assert packet['status']==receipt['status']==status and packet['owner']==receipt['owner']=='root'
  assert packet['source_sha256']==receipt['source_sha256'] and packet['input_sha256']==receipt['input_sha256']
  assert receipt['result_sha256']==PINS[stem+'_RESULT.json'] and receipt['report_sha256']==PINS[stem+'_REPORT.md']
 assert completion['new_state_constructed'] is completion['physical_seed_qualified'] is completion['full_trace_qualified'] is False
 assert all(v is False for v in completion['prior_false_flags'].values()) and completion['new_residual_threshold'] is None
 env=load_definitions();helpers=env['load_declared_helpers']();lay=helpers['Layout'](32,4,4);therm=helpers['Thermal']('HALF',1,fixed)
 nodes,weight=env['gauss'](32);snodes=(nodes+1)/2;weights=weight*snodes;weights/=sum(weights)
 initials=[];fine=[];seeds=[];start_preparation=[]
 for ai,index,label in ((AC,0,'FINE'),(AI,1,'START')):
  c,z=coefficients(common,metric,completion,index);assert common['families'][index]['label']==metric['families'][index]['label']==completion['families'][index]['label']==label
  yy=[];meta=[]
  for arm,om in enumerate(OMEGAS):y,m=derived_seed(ai,c,z,arm,fixed,lay,therm,snodes,weights,om,helpers,env);yy.append(y);meta.append(m)
  seeds.append(dict(label=label,a=ai,metadata=meta))
  if label=='FINE':fine=[snapshot(ai,y,fixed,lay,therm,snodes,weights,om,helpers,env) for y,om in zip(yy,OMEGAS)]
  else:
   initials=yy;start_preparation=[snapshot(ai,y,fixed,lay,therm,snodes,weights,om,helpers,env) for y,om in zip(yy,OMEGAS)]
 prep_name=STEM+'_PREPARATION_CP.json';prep=BASE/prep_name;prep_commit=BASE/(prep_name[:-5]+'_COMMIT.json')
 prepared=dict(lineage=lineage,seeds=seeds,fine_preparation=fine,start_preparation=start_preparation)
 if prep.exists() or prep_commit.exists():
  assert prep.exists() and prep_commit.exists(),'Protected orphan preparation requires explicit recovery'
  commit=json.loads(prep_commit.read_text());previous=json.loads(prep.read_text());env['finite_tree'](previous)
  assert commit['payload']==prep_name and commit['sha256']==sha(prep) and previous['owner']=='root' and type(previous['pid']) is int and previous['pid']>0
  assert commit==dict(owner='root',pid=previous['pid'],payload=prep_name,sha256=sha(prep),lineage=encode(lineage))
  assert {k:v for k,v in previous.items() if k not in ('owner','pid')}==encode(prepared)
 else:
  authenticate();ph=write(prep_name,dict(owner='root',pid=os.getpid(),**prepared))
  write(prep_commit.name,dict(owner='root',pid=os.getpid(),payload=prep_name,sha256=ph,lineage=lineage));authenticate()
 results=[]
 for n in REFINEMENTS:
  row=propagate(n,initials,fixed,lay,therm,snodes,weights,helpers,env,seeds,encode(lineage),authenticate);results.append(row)
 original=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());old=next(r for r in original['comparisons'] if r['label']=='start')['normalization']
 comparisons=[]
 for row in results:
  arms=[]
  for arm,(candidate,reference) in enumerate(zip(row['endpoint'],fine)):
   assert candidate['a']==reference['a'];diff=np.asarray(candidate['readouts'])-np.asarray(reference['readouts']);local=np.maximum(abs(np.asarray(reference['readouts'])),CURVATURE*1e-8)
   arms.append(dict(arm=arm,omega=OMEGAS[arm],signed_difference=diff,original_frozen_normalization=old[arm],error_using_original_normalization=abs(diff)/np.asarray(old[arm]),new_single_frame_normalization=local,new_single_frame_error=abs(diff)/local,
    clock_tolerance=2e-4,clock_short_overlap_passed=bool(abs(diff[10])/float(old[arm][10])<=2e-4)))
  comparisons.append(dict(n=row['n'],arms=arms))
 gates=[]
 def check(label,error,tol,**fields):
  error=float(error);gates.append(dict(label=label,error=error,tolerance=tol,passed=bool(math.isfinite(error) and error<=tol),**fields))
 for label,prepared in (('FINE',fine),('START',start_preparation)):
  for arm,reference in enumerate(prepared):
   for key,tol in (('normal_error',1e-10),('shear_error',2e-13),('native_Euler_error',1e-9),('proper_trace_error',1e-9)):check(label+'_'+key,reference[key],tol,arm=arm)
 for row,comparison in zip(results,comparisons):
  for arm,(endpoint,err) in enumerate(zip(row['endpoint'],row['errors'])):
   for key,tol in (('normal_error',1e-10),('shear_error',2e-13),('native_Euler_error',1e-9),('proper_trace_error',1e-9)):check('END_'+key,endpoint[key],tol,n=row['n'],arm=arm)
   for key in ('stage_error','dense_error'):check(key,err[key],2e-11,n=row['n'],arm=arm)
   for key in ('metric_momentum_error','curvature_increment_error','baryon_Euler_error'):check(key,err[key],1e-5,n=row['n'],arm=arm)
   for kind,v in row['initial_angular128_256_errors'][arm].items():check('initial_angular_'+kind,v,2e-11,n=row['n'],arm=arm)
   for kind in ('error_using_original_normalization','new_single_frame_error'):check('short_clock_'+kind,comparison['arms'][arm][kind][10],2e-4,n=row['n'],arm=arm)
  for name,v in row['optical_controls'].items():check(name,v,2e-11,n=row['n'])
 for arm in range(4):
  high=np.asarray(results[1]['endpoint'][arm]['readouts']);low=np.asarray(results[0]['endpoint'][arm]['readouts']);den=np.maximum(abs(high),CURVATURE*1e-8)
  for variable,error in enumerate(abs(high-low)/den):check('prefix_time_refinement',error,1e-3,arm=arm,variable=variable)
 assert len(gates)==216
 qualified=all(g['passed'] for g in gates)
 result=dict(status='SHORT_DERIVED_START_DIAGNOSTIC_PASS' if qualified else 'SHORT_DERIVED_START_DIAGNOSTIC_FAILED',all_short_diagnostic_gates_passed=qualified,diagnostic_gates=gates,owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,
  source_sha256=source_sha,input_sha256=PINS,seeds=seeds,fine_preparation=fine,start_preparation=start_preparation,propagations=results,comparisons=comparisons,new_finite_truncation_constructed=True,original_failure_flags_changed=False,full_33_frame_start_criterion_qualified=False,physical_seed_qualified=False,
  scope='Finite two-start overlap only; retained higher-order truncations and incoming angular/native history are not a full Cauchy certificate')
 authenticate();rh=write(STEM+'_RESULT.json',result)
 p=BASE/(STEM+'_REPORT.md')
 with p.open('x') as f:f.write('# Derived starting-state overlap V001\n\n'+result['status']+'\n\n'+str(sum(g['passed'] for g in gates))+'/'+str(len(gates))+' short diagnostic checks pass. Four unchanged inertias, two prefix resolutions, same law and first common physical frame. All signed differences and both normalizations are saved. No original failure is changed or full 33-frame test qualified.\n')
 p.chmod(0o444);authenticate();outputs={q.name:sha(q) for q in BASE.glob(STEM+'*CP*.json')};outputs[mp.name]=sha(mp)
 write(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=source_sha,input_sha256=PINS,output_sha256=outputs,result_sha256=rh,report_sha256=sha(p)))
 print(json.dumps(dict(status=result['status'],pid=os.getpid(),result_sha256=rh,receipt_sha256=sha(BASE/(STEM+'_RECEIPT.json')))),flush=True)
 return 0 if qualified else 3
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root-owned',action='store_true',required=True);p.add_argument('--resume',action='store_true');args=p.parse_args()
 if 'AUTHOR_DRAFT' in Path(__file__).name:raise SystemExit('Protected author draft; not a numerical entry point')
 try:raise SystemExit(main(args.resume))
 except Exception:
  write(STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json',dict(owner='root',pid=os.getpid(),traceback=traceback.format_exc()))
  raise
