"""Bounded saved-rate diagnostic; root alone executes literal rate/Decimal arithmetic."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,ast,hashlib,json,math,os,time
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_COMOVING_CHART_SAVED_RATE_ARITHMETIC_V001'
PARENT='CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001'
PROTOCOL_SHA='5c6e2e9e6a6119e19d4b51208fc4f378c02e8bc5d8583910c9232ad41c4385d0'
PINS={'constrained_u_common_boundary_comoving_chart_v001.py': 'dc2181f3ce40166dfded934107705bcffb4b524b29ee36f4ff039baaf33933b3', 'CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001.md': '0db02031c50380af061f60a6ae6560e778b3cc55d1201c8efde0c6e61139812e', 'CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001_RESULT.json': '822f1e6e831ec5cd88e3f18777ef6ce2ebdc195f1e0bffa45dbcd293c1b059d5', 'CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001_RECEIPT.json': 'a7434fd302b0c88e8ed6bb10112dbb0a86d0761e3f5a25f26fb3492265f98454', 'constrained_u_clock_gradient_early_transfer_v005.py': 'bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20', 'CONSTRAINED_U_COMOVING_CURVATURE_AND_RELATIVE_VELOCITY_CHART_V002.md': '2e2102548a82167563f6a7b5ff9af558aea4d9cc85f20957daa72c777c5bdb3a', 'CONSTRAINED_U_FULL_REGULAR_SEED_POWER_LOG_RECURRENCE_V001.md': 'd8f1dbfbfca76839a6064833f76f531254f064cabcda922c6612f1472f405b6b'}
SPANS={'constrained_u_clock_gradient_early_transfer_v005.py:coefficients': 'b9e6a7edca9a67031670d32dba146c289347b9253f32bf16d0f3587597125637', 'constrained_u_clock_gradient_early_transfer_v005.py:rates': '2053ec557e765a899a9468fed8a48d701e010d2f76a0aa666ab209e8dc079354', 'constrained_u_clock_gradient_early_transfer_v005.py:stage_matrix': '0b02c3bb7a1c4d2d4a9ce6e5ddfe964965042d013ba916d50a4eeda63cb040fe', 'constrained_u_common_boundary_comoving_chart_v001.py:to_raw': '223be93f3578256512694cabf985b8150f925ed66d874a081a10263f7322198b', 'constrained_u_common_boundary_comoving_chart_v001.py:chart_transform': 'fa8e735265bb4743b13047b635fd58a53a3363fea3b5f0b66d7b0933b1185234', 'constrained_u_common_boundary_comoving_chart_v001.py:chart_coefficients': 'e789f51ebf7c4231d60df9e8b9997726bba3be7b538bb87d35faffa9d49c5bbe', 'constrained_u_common_boundary_comoving_chart_v001.py:chart_rates': 'b6ba9ea36a79575167c3aef2c6fb51b74190878931777d4d798399fdf6602b4d'}
SOURCE=None;MANIFEST=None;SEALS={};CREATED={};ENTERED=False
EPS=2.220446049250313e-16
FLOOR=1e-5*1e-16
PRECISION=90
SCOPE='Saved392-state arithmetic only; no propagation, background root, thermal lookup, seed, eigenproblem or physical qualification'
def require(ok,msg):
 if not ok:raise AssertionError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def finite(v):
 if isinstance(v,dict):
  for x in v.values():finite(x)
 elif isinstance(v,list):
  for x in v:finite(x)
 elif type(v) is float:require(math.isfinite(v),'Finite JSON number')
 elif v is not None:require(type(v) in (bool,int,str),'Native JSON type')
def write(name,v):
 finite(v);data=canonical(v);p=BASE/name
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)
def event(kind,**kw):
 v=dict(time=datetime.now(timezone.utc).isoformat(),event=kind,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,**kw)
 with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(canonical(v).decode())
def seal(p,h):
 p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent) or p==Path('/usr/bin/clang').resolve(),'Declared input path');require(sha(p)==h,'Input bytes');require(str(p) not in SEALS or SEALS[str(p)]==h,'Consistent seal');SEALS[str(p)]=h
def recheck():
 require(sha(__file__)==SOURCE,'Own source seal')
 for p,h in dict(SEALS,**CREATED).items():require(sha(p)==h,'Inputs/created bytes')
def cp(stage,data):
 recheck();pn=STEM+'_'+stage+'_CP.json';cn=pn[:-5]+'_COMMIT.json';v=dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,data=data);h=write(pn,v)
 ch=write(cn,dict(stage=stage,payload=pn,payload_sha256=h,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST));event('CHECKPOINT',stage=stage,payload=pn,payload_sha256=h,commit=cn,commit_sha256=ch)
def authenticate():
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
 p=read(BASE/(PARENT+'_RESULT.json'));r=read(BASE/(PARENT+'_RECEIPT.json'));m=read(BASE/(PARENT+'_MANIFEST.json'))
 require(p['lineage']==m and m['source_sha256']==r['source_sha256']==PINS['constrained_u_common_boundary_comoving_chart_v001.py'],'Parent lineage/source')
 require(r['result_sha256']==PINS[PARENT+'_RESULT.json'] and r['status']==p['status']=='BOUNDED_COMOVING_CHART_ARITHMETIC_FAILED','Completed failed parent')
 require(len(p['numerical_gates'])==306 and all(g['passed'] for g in p['numerical_gates']) and len(p['chart_gates'])==84 and sum(g['passed'] for g in p['chart_gates'])==56,'306/84 dispositions')
 require(sum(not g['passed'] for g in p['original_numerical_gates'])==32,'Original failures retained')
 for k in ('input_sha256','output_sha256'):
  for path,h in r[k].items():seal(path,h)
 seal(BASE/(PARENT+'_RECEIPT.json'),PINS[PARENT+'_RECEIPT.json']);seal(BASE/(PARENT+'_MANIFEST.json'),r['manifest_sha256']);seal(BASE/(PARENT+'_JOURNAL.jsonl'),r['journal_sha256']);require(r['input_sha256']==m['inputs'],'Exact input map')
 es=[json.loads(x) for x in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()];ex=[(f,s,n) for f in ('OLD','REGULAR') for s in (512,1024) for n in range(0,s+1,128)]
 require([e['event'] for e in es]==['OWNER_START']+['CHECKPOINT']*28+['OWNER_COMPLETE'],'Complete natural30 events');prev={};names=set()
 for e in es:require(e['owner']=='root' and e['pid']==11510 and e['source_sha256']==r['source_sha256'] and e['manifest_sha256']==r['manifest_sha256'],'Root/source/epoch')
 for e,ids in zip(es[1:-1],ex):
  require((e['family'],e['steps'],e['n'])==ids,'Global28 CP prefix');pn=e['payload'];cn=pn[:-5]+'_COMMIT.json';v=read(BASE/pn);c=read(BASE/cn);finite(v)
  require(sha(BASE/pn)==e['sha256'] and sha(BASE/cn)==e['commit_sha256'] and (BASE/pn).read_bytes()==canonical(v) and (BASE/cn).read_bytes()==canonical(c),'Exact canonical pair')
  require(v['lineage']==m and (v['owner'],v['pid'],v['source_sha256'],v['manifest_sha256'],v['family'],v['steps'],v['n'])==('root',11510,r['source_sha256'],r['manifest_sha256'],*ids),'Payload labels')
  require(c==dict(owner='root',pid=11510,source_sha256=r['source_sha256'],manifest_sha256=r['manifest_sha256'],lineage=m,family=ids[0],steps=ids[1],n=ids[2],payload=pn,sha256=e['sha256']),'Commit whole schema')
  require(all(len(v[k])==4 and all(len(y)==392 for y in v[k]) for k in ('state','chart_state')) and [s['n'] for s in v['snapshots']]==list(range(0,ids[2]+1,ids[1]//16)),'Full states/prefix axes')
  require([s['state'] for s in v['snapshots'][-1]['cases']]==v['state'] and [s['chart_state'] for s in v['snapshots'][-1]['cases']]==v['chart_state'],'Snapshot/state closure')
  key=ids[:2]
  if key in prev:require(v['snapshots'][:len(prev[key]['snapshots'])]==prev[key]['snapshots'] and v['seed_metadata']==prev[key]['seed_metadata'] and (prev[key]['n']==0 or v['first_stages']==prev[key]['first_stages']),'Entire immutable prefix')
  prev[key]=v;names.update((pn,cn))
 require({x.name for x in BASE.glob(PARENT+'_*_CP*.json')}==names and es[-1]['result_sha256']==r['result_sha256'] and es[-1]['status']==p['status'],'Complete closure/census')
 for run in p['runs']:
  v=prev[run['family'],run['steps']];require(v['n']==run['steps'] and all(v[k]==run[k] for k in ('snapshots','seed_metadata','first_stages','stage_errors','dense_errors')),'Complete result payloads')
 require(not list(BASE.glob(PARENT+'_FAILED_*')),'Natural failed-disposition exit, no runtime error');return p,r

def definitions(filename,names,env):
 s=(BASE/filename).read_text();ns=[n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name in names]
 require({n.name for n in ns}==set(names),'Exact definition-only whitelist')
 for n in ns:require(hashlib.sha256(ast.get_source_segment(s,n).encode()).hexdigest()==SPANS[filename+':'+n.name],'Literal source span')
 exec(compile(ast.Module(body=ns,type_ignores=[]),str(BASE/filename),'exec'),env)

def D(v):return Decimal.from_float(v) if type(v) is float else Decimal(v)
def dsum(v):return sum(v,Decimal(0))
def decimal_rates(case,cy,fixed,nodes,weights,omega,chart,consistent):
 # Independent exact-float lifted algebra: no producer callback and no background/root/thermal evaluation.
 y=[D(v) for v in cy];bg=case['background'];h,b,r,w,c,Q=(D(bg[k]) for k in ('h','b','r','w','cs','Q'));cd=D(bg['cs_dt']);Hd=D(bg['h_dt']);rg=r*D(fixed['fgamma']);rn=r-rg
 if consistent:Hd=-b-4*r/3-w
 q=D(.01*299792458./(1000*fixed['Hunit']*bg['a']));g=D(case['thermal']['g']);rb=3*b/(4*rg);kb=D(.02);cc=D(1.98);cb=D(.99)
 if chart:
  R,Gb,wb,Gg,wg,Gn,wn,Gamma,V=y[:9];psi=R-h*V;phi=psi-2*(rg*y[9]+rn*y[201])/q**2;S=b*wb+4*rg*wg/3+4*rn*wn/3;Rd=S+h*c*Gamma;psid=Rd-Hd*V-h*(phi+c*Gamma);ug=V+wg;un=V+wn
 else:
  psi,db,ub,dg,ug,dn,un,d,V=y[:9];phi=psi-2*(rg*y[9]+rn*y[201])/q**2;psid=b*ub+4*rg*ug/3+4*rn*un/3+w*V-h*phi;Gamma=d+3*h*V
 ww=[D(v) for v in weights];nn=[D(v) for v in nodes];om=D(omega);Z=dsum(ww[i]*y[328+i] for i in range(32));Zd=dsum(ww[i]*y[360+i] for i in range(32));alpha=om**2*dsum(ww[i]*nn[i]**2 for i in range(32));R1=om**2*dsum(ww[i]*nn[i]**2*y[328+i] for i in range(32))
 L=Q*q;Ld=-h*(1+3*c)*L;Ldd=(h*h*(1+3*c)**2-Hd*(1+3*c)-3*h*cd)*L;v=Z/L;vd=(Zd-Ld*v)/L;n=vd-c*Gamma;Vd=phi+c*Gamma;Bq=1+(D(fixed['ell_native'])*q)**2;Delta=alpha+cc*Q*Q/kb+cb*Q*Q*q*q*c/w
 Fv=-h*n-cc*(Zd+2*h*Z)/(kb*q)+cd*Gamma+c*((3*Rd-q*q*V) if chart else (3*psid-q*q*V+3*Hd*V+3*h*Vd))
 sigma=(L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-alpha*q*n)/Delta;out=[D(0)]*392
 if chart:out[:9]=[Rd,3*Rd-q*q*(V+wb),g/rb*(wg-wb)-c*Gamma,4*Rd-4*q*q*(V+wg)/3,h*wg+Gg/4-y[9]/2+g*(wb-wg)-c*Gamma,4*Rd-4*q*q*(V+wn)/3,h*wn+Gn/4-y[201]/2-c*Gamma,3*Rd-q*q*V-cb*Q*q*sigma/w,Vd]
 else:out[:9]=[psid,3*psid-q*q*ub,phi+g/rb*(ug-ub),4*psid-4*q*q*ug/3,h*ug+phi+dg/4-y[9]/2+g*(ub-ug),4*psid-4*q*q*un/3,h*un+phi+dn/4-y[201]/2,3*psid-q*q*V-cb*Q*q*sigma/w,Vd]
 Pi=y[9]+y[104]+y[106]
 for start,maxl,vel,col in ((9,96,ug,g),(201,128,un,D(0))):
  for l in range(2,maxl+1):
   i=start+l-2;before=4*q*vel/3 if l==2 else y[i-1];after=y[i+1] if l<maxl else D(0);out[i]=q*(l*before-(l+1)*after)/(2*l+1)-col*y[i]
   if l==2 and col:out[i]+=col*Pi/10
 for l in range(97):
  i=104+l;before=y[i-1] if l else D(0);after=y[i+1] if l<96 else D(0);out[i]=q*(l*before-(l+1)*after)/(2*l+1)-g*y[i]
  if l in (0,2):out[i]+=g*Pi*(D('.5') if l==0 else D('.1'))
 for i in range(32):out[328+i]=y[360+i];out[360+i]=-3*h*y[360+i]-om**2*nn[i]**2*(Bq*y[328+i]-q*n-sigma)
 return out,dict(n=n,sigma=sigma,Hd=Hd,h=h)
def ideal_raw(cy,h):
 y=[D(v) for v in cy];out=y.copy()
 for row,f in ((0,1),(1,3),(3,4),(5,4),(7,3)):out[row]=y[row]-f*h*y[8]
 for row in (2,4,6):out[row]=y[row]+y[8]
 return out
def pullback(dy,raw,h,Hd):
 out=dy.copy();dv=dy[8]
 for row,f in ((0,1),(1,3),(3,4),(5,4),(7,3)):out[row]=dy[row]-f*Hd*raw[8]-f*h*dv
 for row in (2,4,6):out[row]=dy[row]+dv
 return out

def main():
 global SOURCE,MANIFEST,ENTERED
 require(not any(BASE.glob(STEM+'_*')),'Exclusive entire runtime prefix; no resume or overwrite');SOURCE=sha(__file__);p,rec=authenticate();tick=time.monotonic()
 import numpy as np
 fixed=p['lineage']['fixed'];env=dict(np=np,math=math,K=.01,CP=299792458.,KB=.02,C=1.98,CBAR=.99)
 require(np.__version__==p['lineage']['numpy_version'],'Same literal float replay runtime');definitions('constrained_u_clock_gradient_early_transfer_v005.py',('coefficients','rates','stage_matrix'),env)
 methods=dict(np=np,math=math);definitions('constrained_u_common_boundary_comoving_chart_v001.py',('chart_coefficients','chart_rates','chart_transform','to_raw'),methods)
 lay=SimpleNamespace(n=392,ns=32,lg=96,ln=128,fg={l:9+l-2 for l in range(2,97)},pol={l:104+l for l in range(97)},fn={l:201+l-2 for l in range(2,129)},z=np.arange(328,360),zd=np.arange(360,392))
 nodes=p['runs'][0]['snodes'];weights=p['runs'][0]['weights'];require(all(r['snodes']==nodes and r['weights']==weights and len(r['state_names'])==392 for r in p['runs']),'Same full spectral inventory')
 manifest=dict(source_sha256=SOURCE,input_sha256=SEALS.copy(),scope=SCOPE,frame_count=288,precision=PRECISION,decimal_inputs='EXACT_BINARY64_FROM_FLOAT',parent_numerical_pass=306,parent_chart_pass=56,parent_chart_fail=28,rate_tolerance=2e-11,original_rate_floor=FLOOR,definitions=SPANS)
 MANIFEST=write(STEM+'_MANIFEST.json',manifest);ENTERED=True;event('OWNER_START');cp('AUTH',dict(parent_result_sha256=rec['result_sha256'],original_numerical_gates=p['original_numerical_gates'],numerical_gates=p['numerical_gates'],chart_gates=p['chart_gates'],operator_fixtures=p['operator_fixtures']))
 frames=[]
 for d in p['direct_seeds']:
  for i,c in enumerate(d['cases']):frames.append((dict(kind='DIRECT',family=d['family'],a=d['a'],omega=p['lineage']['omegas'][i]),c))
 for r in p['runs']:
  for s in r['snapshots']:
   for i,c in enumerate(s['cases']):frames.append((dict(kind='PROPAGATED',family=r['family'],steps=r['steps'],n=s['n'],a=c['a'],omega=p['lineage']['omegas'][i]),c))
 require(len(frames)==288,'All288 frozen frames');rows=[];checks=[]
 for ids,c in frames:
  bg=c['background'];th=c['thermal'];x=c['x'];env['background']=lambda value,fixture,bg=bg,x=x:(require(value==x,'Saved exact x') or dict(bg));thermal=SimpleNamespace(at=lambda a,th=th,bg=bg:(require(a==bg['a'],'Saved exact a') or dict(th)))
  chart_env=dict(env,background=env['background']);y=np.array(c['chart_state']);raw=np.array(c['state']);om=ids['omega'];sn=np.array(nodes);ww=np.array(weights)
  dy,f=methods['chart_rates'](x,y,chart_env,fixed,lay,thermal,sn,ww,om);rr,fr=env['rates'](x,raw,fixed,lay,thermal,sn,ww,om);T,Ti,Td=methods['chart_transform'](bg,lay,np)
  require(methods['to_raw'](y,bg['h'],np).tolist()==c['state'],'Exact producer binaryraw reconstruction');back=Ti[:392,:392]@(dy-Td[:392,:392]@raw);gap=back-rr;oldscale=abs(Ti[:392,:392])@(abs(dy)+abs(Td[:392,:392])@abs(raw))+abs(rr);oldratio=abs(gap)/np.maximum(oldscale,FLOOR);k=int(np.argmax(oldratio));er=float(oldratio[k]);stored=c['chart_contacts']['rate_error']
  require(np.array_equal(oldscale,np.array(c['chart_contacts']['rate_scale'])) and abs(er-stored)<=4096*EPS*max(er,stored,1e-30),'Exact saved parent contact reproduction')
  mat=env['stage_matrix'](x,fixed,lay,thermal,sn,ww,om);require(mat[392,392]==mat[393,393]==1. and mat[392,393]==0.,'Exact two nondynamical reaction rows');ncoef=-mat[392,:392];scoef=-mat[393,:392]-mat[393,392]*ncoef;full=bg['h']*(mat[:392,:392]+mat[:392,392,None]*ncoef+mat[:392,393,None]*scoef)
  expanded=abs(full)@abs(raw)+abs(Ti[:392,:392])@(abs(dy)+abs(Td[:392,:392])@abs(raw));expanded=np.maximum(expanded,FLOOR)
  with localcontext() as context:
   context.prec=PRECISION;cy=c['chart_state'];ideal=ideal_raw(cy,D(bg['h']));ch,cf=decimal_rates(c,cy,fixed,nodes,weights,om,True,False);raw_ideal,rf=decimal_rates(c,ideal,fixed,nodes,weights,om,False,False);raw_saved,sf=decimal_rates(c,c['state'],fixed,nodes,weights,om,False,False);ch_back=pullback(ch,ideal,cf['h'],cf['Hd']);loss=[raw_saved[j]-raw_ideal[j] for j in range(392)];ward=[ch_back[j]-raw_ideal[j] for j in range(392)]
   cc,cfc=decimal_rates(c,cy,fixed,nodes,weights,om,True,True);ri,rfc=decimal_rates(c,ideal,fixed,nodes,weights,om,False,True);bc=pullback(cc,ideal,cfc['h'],cfc['Hd']);algebra=[bc[j]-ri[j] for j in range(392)];alg=max(abs(algebra[j])/D(float(expanded[j])) for j in range(392));passed=alg<=D('2e-11')
   checks.append(dict(name='exact_lift_consistent_background_algebra',error=float(alg),tolerance=2e-11,passed=bool(passed),**ids));debg=D(bg['h_dt'])+D(bg['b'])+4*D(bg['r'])/3+D(bg['w']);h=D(bg['h'])
   dec=dict(original_max_row=k,original_chart_pullback=str(ch_back[k]),original_ideal_raw_rate=str(raw_ideal[k]),original_saved_raw_rate=str(raw_saved[k]),ideal_to_binary_raw_rate_loss=str(loss[k]),rounded_background_contact=str(ward[k]),pure_algebra_contact=str(algebra[k]),background_source_residual=str(debg),exact_chart_slip=str(D(cy[4])-D(cy[2])),saved_raw_slip=str(D(c['state'][4])-D(c['state'][2])),ideal_raw_slip=str(ideal[4]-ideal[2]),native_n_strings=[str(v['n']) for v in (cf,rf,sf)],native_sigma_strings=[str(v['sigma']) for v in (cf,rf,sf)])
  with localcontext() as context:
   context.prec=120;ideal120=ideal_raw(c['chart_state'],D(bg['h']));raw120,_=decimal_rates(c,ideal120,fixed,nodes,weights,om,False,False);saved120,_=decimal_rates(c,c['state'],fixed,nodes,weights,om,False,False);refine=max(max(abs(raw120[j]-raw_ideal[j]),abs((saved120[j]-raw120[j])-loss[j]))/D(float(expanded[j])) for j in range(392))
   checks.append(dict(name='decimal90_vs120_operation_refinement',error=float(refine),tolerance=2e-11,passed=bool(refine<=D('2e-11')),**ids))
  rows.append(dict(**ids,state_count=392,original_max_row=k,original_max_name=p['runs'][0]['state_names'][k],original_rate_error=er,original_passed=bool(er<=2e-11),original_max_signed_difference=float(gap[k]),original_max_rate_scale=float(oldscale[k]),expanded_max_rate_scale=float(expanded[k]),signed_original_rate_difference=gap.tolist(),expanded_operation_envelope=expanded.tolist(),decimal=dec,decimal_algebra_error=float(alg),expanded_original_error=float(np.max(abs(gap)/expanded)),scope='Expanded envelope diagnoses arithmetic and information loss; it never replaces the saved parent gate'))
 require(len(checks)==576 and len(rows)==288,'Fixed frame/independent algebra census');cp('REPLAY',dict(rows=rows,parent_chart_gates=p['chart_gates']));cp('DECIMAL',dict(arithmetic_controls=checks))
 worst=max(rows,key=lambda v:v['original_rate_error']);summary=dict(row_count=288,original_failed_frames=sum(not r['original_passed'] for r in rows),maximum_original_rate_error=worst['original_rate_error'],worst_frame={k:worst[k] for k in ('kind','family','a','omega','original_max_row','original_max_name','original_max_signed_difference','original_max_rate_scale','expanded_max_rate_scale')},maximum_expanded_error=max(v['expanded_original_error'] for v in rows),all_decimal_algebra_controls_passed=all(v['passed'] for v in checks),interpretation='Separate binaryraw reconstruction, internal operation scaling and rounded-background Ward contact; no seed/trajectory or qualification change')
 status='SAVED_RATE_ARITHMETIC_DIAGNOSTIC_COMPLETE' if all(v['passed'] for v in checks) else 'SAVED_RATE_ARITHMETIC_DIAGNOSTIC_FAILED';cp('SUMMARY',dict(status=status,summary=summary));recheck();result=dict(status=status,manifest=manifest,rows=rows,arithmetic_controls=checks,summary=summary,parent_numerical_gates=p['numerical_gates'],parent_chart_gates=p['chart_gates'],original_numerical_gates=p['original_numerical_gates'],qualification_changed=False,elapsed_seconds=time.monotonic()-tick);rh=write(STEM+'_RESULT.json',result)
 report='# Saved rate arithmetic diagnostic\n\n'+status+'\n\nAll288 saved392-state frames retained. Original306/306 and56/84,28 failed chart gates remain unchanged. Decimal uses exact binary64 inputs at90 digits; expanded operation envelopes and consistent-background algebra are diagnostic only, not replacement tolerances or a propagated solution.\n';rp=BASE/(STEM+'_REPORT.md')
 with rp.open('x') as f:f.write(report)
 rp.chmod(0o444);CREATED[str(rp)]=sha(rp);event('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=4,frame_count=288,arithmetic_control_count=576);jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp)]=sha(jp);events=[json.loads(x) for x in jp.read_text().splitlines()];require([e['event'] for e in events]==['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'] and [e['stage'] for e in events[1:5]]==['AUTH','REPLAY','DECIMAL','SUMMARY'],'Own natural closure')
 require(all(e['owner']=='root' and e['pid']==os.getpid() and e['source_sha256']==SOURCE and e['manifest_sha256']==MANIFEST for e in events),'Own root/source identity');recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE,input_sha256=SEALS,output_sha256=CREATED.copy(),manifest_sha256=MANIFEST,journal_sha256=sha(jp),result_sha256=rh,checkpoint_count=4,frame_count=288));recheck();print(json.dumps(summary));return 0 if all(v['passed'] for v in checks) else 3
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');args=ap.parse_args()
 if not args.execute:raise SystemExit('Root reviewed saved-rate arithmetic only requires --execute')
 try:raise SystemExit(main())
 except Exception as e:
  if ENTERED and not (BASE/(STEM+'_RESULT.json')).exists():write(STEM+'_FAILED.json',dict(error_type=type(e).__name__,error=str(e),source_sha256=SOURCE,manifest_sha256=MANIFEST,created=CREATED.copy()));event('FAILED')
  raise
