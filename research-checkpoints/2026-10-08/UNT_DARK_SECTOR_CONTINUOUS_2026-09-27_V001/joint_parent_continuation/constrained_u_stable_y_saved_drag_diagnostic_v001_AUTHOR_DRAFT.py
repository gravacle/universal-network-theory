"""Saved-only diagnostic repair; no propagation, solver, eigenproblem or seed."""
from pathlib import Path
from datetime import datetime,timezone
import ast,argparse,hashlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_STABLE_Y_DRAG_DIAGNOSTIC_V001'
PARENT='CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002'
PARENT_SOURCE='constrained_u_galaxy_horizon_stable_y_gauss_v002.py'
PREFIX=STEM+'_PARENT_PREFIX.json'
PROTOCOL_SHA='PENDING'
PINS={PARENT_SOURCE:'f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531',
 'CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002.md':'df0391a2174a25591e6cbd0fd26a0951181e1bf024fa36d483c769efacc681bc',
 PREFIX:'75f86b7af283b68816f52fdd9a3e53efa87700727b06c4f612dcdbce3a96492b'}
SOURCE=None;MANIFEST=None;SEALS={};CREATED={};ENTERED=False
K=10.;CURVATURE=1e-5;CP=299792458.;MPC=3.0856775814913673e22
def require(ok,message):
 if not ok:raise AssertionError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def finite(v):
 if isinstance(v,dict):
  require(all(type(k) is str for k in v),'Native keys')
  for x in v.values():finite(x)
 elif isinstance(v,list):
  for x in v:finite(x)
 elif type(v) is float:require(math.isfinite(v),'Finite scalar')
 elif v is not None:require(type(v) in (str,int,bool),'Builtin serialized scalar')
def canonical(v):finite(v);return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def seal(p,h):
 p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent) or p==Path('/usr/bin/clang').resolve(),'Inherited owned/read-only path');require(sha(p)==h,'Exact bytes '+str(p));require(str(p) not in SEALS or SEALS[str(p)]==h,'Consistent seal');SEALS[str(p)]=h
def recheck():
 require(sha(__file__)==SOURCE,'Frozen source')
 for p,h in dict(SEALS,**CREATED).items():require(sha(p)==h,'Whole input/output bytes')
def write(n,v):
 data=canonical(v);p=BASE/n
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)
def event(kind,**kw):
 v=dict(event=kind,time=datetime.now(timezone.utc).isoformat(),owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,**kw)
 with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(canonical(v).decode())
def checkpoint(stage,v):
 recheck();pn=STEM+'_'+stage+'_CP.json';cn=pn[:-5]+'_COMMIT.json'
 h=write(pn,dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,data=v));ch=write(cn,dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,payload=pn,payload_sha256=h));event('CHECKPOINT',stage=stage,payload=pn,payload_sha256=h,commit=cn,commit_sha256=ch)
def authenticate():
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
 prefix=read(BASE/PREFIX);seal(BASE/(PARENT+'_MANIFEST.json'),prefix['manifest_sha256']);manifest=read(BASE/(PARENT+'_MANIFEST.json'));lineage=manifest
 require(prefix['parent_stem']==PARENT and prefix['source_sha256']==lineage['source_sha256']==PINS[PARENT_SOURCE],'Frozen partial parent identity')
 for p,h in lineage['inputs'].items():seal(p,h)
 pairs=prefix['selected_pairs'];events=prefix['events'];require(len(pairs)==10 and len(events)==11 and events[0]['event']=='OWNER_START','Fixed10-pair partial census')
 require([(v['trial'],v['nstep']) for v in pairs]==[(t,i) for t in ('BASE','TIME') for i in range(0,513,128)],'Exact fixed trial prefixes')
 for e in events:require(e['owner']=='root' and type(e['pid']) is int and e['pid']>0 and e['pid']==events[0]['pid'] and e['source_sha256']==PINS[PARENT_SOURCE] and e['manifest_sha256']==prefix['manifest_sha256'],'Copied immutable root/source epoch')
 require([e['event'] for e in events]==['OWNER_START']+['CHECKPOINT']*10,'Exact copied partial events')
 tree=ast.parse((BASE/PARENT_SOURCE).read_text());nodes=[v for v in tree.body if isinstance(v,ast.FunctionDef) and v.name=='validate_checkpoint'];require(len(nodes)==1,'Exact complete parent metadata validator')
 metadata=dict(BASE=BASE,STEM=PARENT,finite_tree=finite,sha=sha)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(BASE/PARENT_SOURCE)+'<metadata-validator-only>','exec'),metadata)
 data=[];prior={}
 for row,e in zip(pairs,events[1:]):
  require((e['trial'],e['nstep'])==(row['trial'],row['nstep']) and e['payload_sha256']==row['payload_sha256'] and e['commit_sha256']==row['commit_sha256'],'Copied event byte binding')
  seal(BASE/row['payload'],row['payload_sha256']);seal(BASE/row['commit'],row['commit_sha256']);cp=read(BASE/row['payload']);cm=read(BASE/row['commit'])
  require((BASE/row['payload']).read_bytes()==canonical(cp) and (BASE/row['commit']).read_bytes()==canonical(cm),'Complete canonical pair')
  require(cp['lineage']==lineage and cm==dict(lineage=lineage,trial=row['trial'],nstep=row['nstep'],payload=row['payload'],sha256=row['payload_sha256']) and cp['trial']==row['trial'] and cp['nstep']==row['nstep'],'Complete immutable pair schema')
  expected_n=512 if row['trial']=='BASE' else 1024
  require(row['payload']==PARENT+'_'+row['trial']+'_CP_'+str(row['nstep']).zfill(6)+'.json' and row['commit']==row['payload'][:-5]+'_COMMIT.json','Exact parent pair filenames')
  metadata['validate_checkpoint'](cp,cm,lineage,row['trial'],row['nstep'],expected_n,32,1)
  finite(cp);require(len(cp['states'])==len(cp['last_stages'])==4 and cp['ns']==32 and cp['stride']==1,'Complete selected4-arm axes')
  if row['trial'] in prior:require(cp['snapshots'][:len(prior[row['trial']]['snapshots'])]==prior[row['trial']]['snapshots'],'Exact immutable snapshot prefix')
  require(len(cp['snapshots'])==1+row['nstep']//(cp['step_count']//32),'Exact selected snapshot census')
  require(cp['snapshots'][-1]['nstep']==cp['nstep'] and [c['stable_state'] for c in cp['snapshots'][-1]['cases']]==cp['states'],'Final committed snapshot/state closure')
  prior[row['trial']]=cp;data.append(cp)
 return prefix,lineage,data
def background_namespace():
 # Literal definitions only; no old main/auth/solver/calibration initializers.
 p=BASE/'constrained_u_clock_gradient_early_transfer_v004.py';require(str(p) in SEALS,'Actual physical background/table source sealed')
 tree=ast.parse(p.read_text());names={'background','Thermal'};nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];require({n.name for n in nodes}==names,'Exact two-definition whitelist')
 import numpy as np
 env=dict(BASE=BASE,np=np,math=math,json=json,MPC=MPC,CP=CP,KB=.02,C=1.98,CBAR=.99,K=K,CURVATURE=CURVATURE)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<two-saved-source-definitions>','exec'),env)
 return env
def fields(y,bg,thermal,fixed):
 h,b,r,w,c=(float(bg[k]) for k in ('h','b','r','w','cs'));rg=r*fixed['fgamma'];rn=r*(1-fixed['fgamma']);g=float(thermal['g']);q=K*CP/(1000*fixed['Hunit']*float(bg['a']));rb=3*b/(4*rg)
 B=bg['a']**3*b;G=bg['a']**3*4*rg/3;alpha=G/(B+G);beta=B/(B+G);U,W,V,Gamma=(y[i] for i in (2,4,8,7));wb=U-alpha*W;wg=U+beta*W;psi=y[0]-h*V;S=rg*y[9]+rn*y[17];phi=psi-2*S/(q*q)
 return dict(h=h,b=b,rg=rg,rn=rn,w=w,c=c,g=g,q=q,rb=rb,alpha=alpha,beta=beta,wb=wb,wg=wg,V=V,Gamma=Gamma,psi=psi,phi=phi,shear=S,hd=float(bg['h_dt']))
def trace_terms(y,f,wrong=False):
 h,b,rg,rn,w,c,g,q,rb,V,Gamma=(f[k] for k in ('h','b','rg','rn','w','c','g','q','rb','V','Gamma'));wb,wg=f['wb'],f['wg'];vd=f['phi']+c*Gamma
 wbd=(-1 if wrong else 1)*g*y[4]/rb-c*Gamma;wgd=h*wg+y[3]/4-y[9]/2-g*y[4]-c*Gamma;wnd=h*y[6]+y[5]/4-y[17]/2-c*Gamma
 rel=b*wb+4*rg*wg/3+4*rn*y[6]/3;total=b+4*(rg+rn)/3+w;mom=rel+total*V
 Sd=b*(wbd-3*h*wb)+4*rg*(wgd-4*h*wg)/3+4*rn*(wnd-4*h*y[6])/3;Td=-3*h*b-16*h*(rg+rn)/3-3*h*(1+c)*w;Md=Sd+Td*V+total*vd
 psid=rel+h*c*Gamma-f['hd']*V-h*vd;Pi=y[9]+y[12]+y[14]
 Fgd=8*q*q*(V+wg)/15-3*q*y[10]/5-g*(y[9]-Pi/10);Fnd=8*q*q*(V+y[6])/15-3*q*y[18]/5
 phid=psid-2*(rg*(Fgd-2*h*y[9])+rn*(Fnd-2*h*y[17]))/(q*q);psidd=Md-f['hd']*f['phi']-h*phid
 terms=[psidd,h*phid,3*h*psid,(2*f['hd']+3*h*h)*f['phi'],q*q*(f['psi']-f['phi'])/3,-c*w*(Gamma-3*h*V),-(rg*(y[3]-4*h*V)+rn*(y[5]-4*h*V))/3]
 return terms,Md,mom
def score(terms,floor):return abs(math.fsum(terms))/max(math.fsum(abs(x) for x in terms),floor)
def check(flags,name,residual,scale,**ids):
 error=abs(residual)/max(scale,1e-280);flags.append(dict(name=name,error=error,tolerance=2e-11,passed=bool(math.isfinite(error) and error<=2e-11),**ids))
def snapshot_rows(cps,fixed,flags):
 seen={};rows=[]
 for cp in cps:
  for snap in cp['snapshots']:
   for arm,case in enumerate(snap['cases']):
    key=(cp['trial'],snap['nstep'],arm)
    if key in seen:require(seen[key]==case,'All duplicate snapshots identical');continue
    seen[key]=case;y=case['stable_state'];f=fields(y,case['background'],case['thermal'],fixed);delta=2*f['b']*f['g']*y[4]/f['rb'];old=case['trace_terms'];new=old.copy();new[0]+=delta;direct,Md,mom=trace_terms(y,f);ids=dict(trial=key[0],nstep=key[1],arm=arm)
    check(flags,'complete_corrected_trace_terms',max(abs(a-b) for a,b in zip(new,direct)),math.fsum(abs(v) for v in new+direct),**ids)
    Udot=f['alpha']*(f['h']*y[2]+y[3]/4-y[9]/2)-f['c']*y[7];Wdot=f['h']*f['wg']+y[3]/4-y[9]/2-f['g']*(1+1/f['rb'])*y[4];alphad=-f['h']*f['alpha']*f['beta'];chain=Udot-alphad*y[4]-f['alpha']*Wdot;literal=f['g']*y[4]/f['rb']-f['c']*y[7]
    check(flags,'moving_chart_correct_baryon_drag',chain-literal,abs(Udot)+abs(alphad*y[4])+abs(f['alpha']*Wdot)+abs(literal),**ids)
    error=score(new,case['trace_floor']);rows.append(dict(**ids,a=case['a'],original_trace_terms=old,original_trace_error=case['trace_error'],corrected_trace_terms=new,corrected_trace_error=error,corrected_trace_pass=bool(error<=1e-9),trace_tolerance=1e-9,trace_floor=case['trace_floor'],drag_current_correction=delta,corrected_current_derivative=Md,original_snapshot=case))
 require(len(rows)==200,'Fixed200 unique committed full snapshots');return rows
def stage_rows(cps,fixed,env,flags):
 th=env['Thermal']('HALF',1,fixed);rows=[]
 for cp in cps:
  if cp['nstep']==0:require(cp['last_stages']==[None]*4,'Actual CP0 has no stage');continue
  for arm,record in enumerate(cp['last_stages']):
   require(set(record)=={'algebraic_states','conformal','coordinates','dense_error','dx','previous','stage_error','states','x'} and len(record['states'])==len(record['coordinates'])==3,'Complete saved last-stage schema')
   xx=record['coordinates'];ys=record['states'];dx=record['dx'];left=record['x'];previous=record['previous'];require(ys[-1]==cp['states'][arm] and len(previous)==len(ys[0])==84,'Full previous/output state closure');fs=[]
   for j,(x,y) in enumerate(zip(xx,ys)):
    bg=env['background'](x,fixed);f=fields(y,bg,th.at(math.exp(x)),fixed);fs.append(f);new,Md,mom=trace_terms(y,f);old,wrongMd,_=trace_terms(y,f,True);delta=2*f['b']*f['g']*y[4]/f['rb'];ids=dict(trial=cp['trial'],nstep=cp['nstep'],arm=arm,node=j)
    check(flags,'saved_stage_drag_trace_difference',Md-wrongMd-delta,abs(Md)+abs(wrongMd)+abs(delta),**ids);floor=CURVATURE*max(f['h']**2,f['q']**2)*1e-12;error=score(new,floor)
    rows.append(dict(**ids,x=x,corrected_trace_terms=new,original_wrong_trace_terms=old,corrected_trace_error=error,corrected_trace_pass=bool(error<=1e-9),trace_tolerance=1e-9,trace_floor=floor,corrected_current_derivative=Md))
   bg=env['background'](left,fixed);prev=fields(previous,bg,th.at(math.exp(left)),fixed);oldub=previous[8]+prev['wb'];newub=ys[-1][8]+fs[-1]['wb'];increment=(ys[-1][8]-previous[8])+(fs[-1]['wb']-prev['wb'])
   correct=[(f['phi']+f['g']*ys[j][4]/f['rb'])/f['h'] for j,f in enumerate(fs[:2])];wrong=[(f['phi']-f['g']*ys[j][4]/f['rb'])/f['h'] for j,f in enumerate(fs[:2])]
   numerator=increment-dx*math.fsum(correct)/2;scale=abs(newub)+abs(oldub)+abs(dx)*math.fsum(abs(v) for v in correct)/2;error=abs(numerator)/max(scale,CURVATURE*1e-18);ids=dict(trial=cp['trial'],nstep=cp['nstep'],arm=arm,node='INTERVAL')
   check(flags,'corrected_minus_wrong_Gauss_integral',dx*(math.fsum(correct)-math.fsum(wrong))/2-dx*math.fsum(f['g']*ys[j][4]/(f['rb']*f['h']) for j,f in enumerate(fs[:2])),abs(dx)*math.fsum(abs(v) for v in correct+wrong),**ids)
   rows.append(dict(**ids,log_step=dx,increment=increment,original_wrong_forces=wrong,corrected_forces=correct,corrected_numerator=numerator,corrected_envelope=scale,corrected_baryon_error=error,corrected_baryon_pass=bool(error<=1e-5),baryon_tolerance=1e-5,original_entire_prefix_errors=cp['errors'][arm],scope='ONLY_THIS_SAVED_LAST_INTERVAL_NOT_ENTIRE_PREFIX_MAXIMUM'))
 require(len(rows)==128,'Fixed96 stage states plus32 selected intervals');return rows
def main():
 global SOURCE,MANIFEST,ENTERED
 require(PROTOCOL_SHA!='PENDING' and not list(BASE.glob(STEM+'_*RESULT*')) and not list(BASE.glob(STEM+'_*MANIFEST*')) and not list(BASE.glob(STEM+'_*JOURNAL*')) and not list(BASE.glob(STEM+'_*CP*')) and not list(BASE.glob(STEM+'_*FAILED*')),'Frozen unused nonresumable runtime');SOURCE=sha(__file__);tick=time.monotonic();prefix,lineage,cps=authenticate();fixed=lineage['fixed'];env=background_namespace()
 manifest=dict(source_sha256=SOURCE,input_sha256=SEALS.copy(),parent_prefix=prefix,unique_full_snapshots=200,saved_stage_states=96,saved_intervals=32,arithmetic_controls=528,complete_parent_or_every_step_qualified=False)
 MANIFEST=write(STEM+'_MANIFEST.json',manifest);ENTERED=True;event('OWNER_START');checkpoint('AUTH',dict(parent_prefix=prefix,original_committed_errors=[dict(trial=c['trial'],nstep=c['nstep'],errors=c['errors'],los_diagnostics=c['los_diagnostics']) for c in cps]))
 flags=[];snapshots=snapshot_rows(cps,fixed,flags);checkpoint('SNAPSHOTS',dict(rows=snapshots,controls=flags.copy()));stages=stage_rows(cps,fixed,env,flags);checkpoint('LAST_STAGES',dict(rows=stages,controls=flags.copy()));require(len(flags)==528,'Fixed528 saved arithmetic identities');failed=[v for v in flags if not v['passed']];status='SAVED_DRAG_CORRECTION_ARITHMETIC_PASS' if not failed else 'SAVED_DRAG_CORRECTION_ARITHMETIC_FAILED';checkpoint('SUMMARY',dict(status=status,arithmetic_failures=len(failed),original_prefix_errors=[c['errors'] for c in cps],complete_parent_or_every_step_qualified=False))
 recheck();result=dict(status=status,manifest=manifest,snapshot_rows=snapshots,last_stage_rows=stages,arithmetic_controls=flags,complete_parent_or_every_step_qualified=False,original_live_source_unchanged=True,elapsed_seconds=time.monotonic()-tick);rh=write(STEM+'_RESULT.json',result);report='# Saved stable-Y baryon-drag diagnostic correction\n\n'+status+'. '+str(528-len(failed))+'/528 arithmetic identities;200 unique full snapshots,96 saved stage states and32 selected intervals. Corrected scientific predicates retain original thresholds; original erroneous flags remain. No trajectory, solver, seed, spectral quadrature or live-file change. Every-step maxima and whole706 qualification are UNQUALIFIED.\n';rp=BASE/(STEM+'_REPORT.md')
 with rp.open('xb') as f:f.write(report.encode())
 rp.chmod(0o444);CREATED[str(rp)]=sha(rp);event('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=4,control_count=528);jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp)]=sha(jp);events=read_events=[json.loads(v) for v in jp.read_text().splitlines()];require([e['event'] for e in events]==['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'],'Full own lifecycle')
 for e in events:require(e['owner']=='root' and e['pid']==os.getpid() and e['source_sha256']==SOURCE and e['manifest_sha256']==MANIFEST,'Own root/source epoch')
 require([e['stage'] for e in events[1:-1]]==['AUTH','SNAPSHOTS','LAST_STAGES','SUMMARY'] and events[-1]['result_sha256']==rh and events[-1]['status']==status,'Exact own terminal');names=set()
 for e in events[1:-1]:
  v=read(BASE/e['payload']);c=read(BASE/e['commit']);require(sha(BASE/e['payload'])==e['payload_sha256'] and sha(BASE/e['commit'])==e['commit_sha256'] and (BASE/e['payload']).read_bytes()==canonical(v) and (BASE/e['commit']).read_bytes()==canonical(c),'Complete own canonical pair');require(c==dict(stage=e['stage'],owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,payload=e['payload'],payload_sha256=e['payload_sha256']) and v['stage']==e['stage'] and v['owner']=='root' and v['pid']==os.getpid() and v['source_sha256']==SOURCE and v['manifest_sha256']==MANIFEST,'Full own pair identity');names.update((e['payload'],e['commit']))
 require({p.name for p in BASE.glob(STEM+'_*CP*.json')}==names,'Four own pairs exact');recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE,input_sha256=SEALS,output_sha256=CREATED.copy(),result_sha256=rh,manifest_sha256=MANIFEST,journal_sha256=sha(jp),checkpoint_count=4,control_count=528));recheck();return 0 if not failed else 3
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');args=p.parse_args()
 if not args.execute:raise SystemExit('Root only after frozen full review; saved arithmetic only')
 try:raise SystemExit(main())
 except Exception:
  if ENTERED and not (BASE/(STEM+'_RESULT.json')).exists():write(STEM+'_FAILED.json',dict(source_sha256=SOURCE,manifest_sha256=MANIFEST,owner='root',pid=os.getpid(),created=CREATED.copy(),traceback=traceback.format_exc()));event('FAILED')
  raise
