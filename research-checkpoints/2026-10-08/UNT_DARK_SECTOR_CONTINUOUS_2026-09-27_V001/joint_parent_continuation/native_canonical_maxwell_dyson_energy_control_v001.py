"""Prospective complete native/photon/switch quadratic Dyson ledger.
Root alone executes; no producer import, new H/eigenproblem or trajectory.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001'
PROTOCOL_SHA='77707f652cfbe869e3d71a8c1ad81247ebc906c2a469aeaf300a62df6d3d85dd'
PINS={
 'NATIVE_REGISTERED_MAXWELL_DYSON_ENERGY_LEDGER_V001.md':'2ab45d4575ee2c8569a5e1a59f38dbbf3b4c60854f3ef63100e82ccd6a987306',
 'native_canonical_maxwell_pair_v003.py':'3bb87715229c29719c2246289d5650359e72f1c34ffbbbc4a8c9536e31713e56',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V003.md':'f57e996ffa158b434f82dacb02b8863f9655a2677f9b38a605f91d941d0ce048',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json':'f74554aa51beb5756fb4da8608a436f29d1efeb2e0958c808d7873ff09d9a1ff',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V003_RECEIPT.json':'2fa61745ad09a1aeafee078539f59f4de5258231e5794b0b0ce7c212fd5b2ec2',
 'native_registered_cell_outgoing_source_v001.py':'888ac431d21d828f96a201d5f975dcdc8bf59360ba7dc038b363457ccb821dec',
 'NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001.md':'1b4709beb5ad6c6f52979def111849290d050fec6d31cdc6c6eaf362b992752f',
 'NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RESULT.json':'9ad2f9890d5e909c048c0353365b75a22b86570c91d45488fb6d19b5e018de1b',
 'NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RECEIPT.json':'0c5bf238307def809f53b05cf37e773385542da8816952af89d7308a74832c7e'}
EDGES=(0,3);OMEGAS=(.5,1.,2.);DURATIONS=(.25,1.,2.);ORDERS=(128,256)
AGES=(0.,.03125,.0625,.125,.25,.5,1.,math.pi/2,2.,math.pi,4.)
STAGES=('AUTH','COEFF_Q0','COEFF_Q1','COMPARE','SUMMARY')
FIELDS=('native_change','photon_change','switch_on_work','switch_off_work','net_switch_work')
SOURCE=None;MANIFEST=None;SEALS={};CREATED={};ENTERED=False
def require(ok,message):
 if not ok:raise AssertionError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def finite(v):
 if isinstance(v,dict):
  for x in v.values():finite(x)
 elif isinstance(v,(list,tuple)):
  for x in v:finite(x)
 elif type(v) is float:require(math.isfinite(v),'Finite native scalar')
 elif v is not None:require(type(v) in (str,int,bool),'Native serializable type')
def canonical(v):finite(v);return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,obj):
 data=canonical(obj);p=BASE/name
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)
def seal(p,h):
 p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent),'Owned declared path');require(sha(p)==h,'Exact input bytes');require(str(p) not in SEALS or SEALS[str(p)]==h,'Consistent seal');SEALS[str(p)]=h
def recheck():
 require(sha(__file__)==SOURCE,'Frozen source')
 for p,h in dict(SEALS,**CREATED).items():require(sha(p)==h,'Complete input/output seal')
def event(kind,**kw):
 v=dict(event=kind,time=datetime.now(timezone.utc).isoformat(),owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,**kw)
 with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(canonical(v).decode())
def checkpoint(stage,data):
 recheck();pn=STEM+'_'+stage+'_CP.json';cn=STEM+'_'+stage+'_CP_COMMIT.json'
 h=write(pn,dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,data=data))
 ch=write(cn,dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,payload=pn,payload_sha256=h));event('CHECKPOINT',stage=stage,payload=pn,payload_sha256=h,commit=cn,commit_sha256=ch)
def parent(stem,source,pid,count,status):
 r=read(BASE/(stem+'_RESULT.json'));receipt=read(BASE/(stem+'_RECEIPT.json'));m=read(BASE/(stem+'_MANIFEST.json'))
 require(r['manifest']==m and m['source_sha256']==receipt['source_sha256']==PINS[source] and receipt['result_sha256']==PINS[stem+'_RESULT.json'] and receipt['status']==r['status']==status and receipt['checkpoint_count']==count,'Completed whole parent envelope')
 for key in ('input_sha256','output_sha256'):
  for p,h in receipt[key].items():seal(p,h)
 require(receipt['input_sha256']==m['input_sha256'],'Whole parent input map');seal(BASE/(stem+'_MANIFEST.json'),receipt['manifest_sha256']);seal(BASE/(stem+'_JOURNAL.jsonl'),receipt['journal_sha256'])
 es=[json.loads(s) for s in (BASE/(stem+'_JOURNAL.jsonl')).read_text().splitlines()];require([e['event'] for e in es]==['OWNER_START']+['CHECKPOINT']*count+['OWNER_COMPLETE'],'Complete natural parent lifecycle')
 for e in es:require(e['owner']=='root' and e['pid']==pid and e['source_sha256']==receipt['source_sha256'] and e['manifest_sha256']==receipt['manifest_sha256'],'Complete root/source parent epoch')
 require(es[-1]['status']==r['status'] and es[-1]['result_sha256']==receipt['result_sha256'] and es[-1]['checkpoint_count']==count,'Parent natural terminal')
 if count==216:require(es[0]['completed_prefix']==0 and es[0]['previous_error_sha256'] is None and r['checkpoint_count']==216 and r['configuration']==m['configuration'],'Whole216 start/census/configuration')
 else:require([e['stage'] for e in es[1:-1]]==['AUTH','CATALOG_Q0','CATALOG_Q1','WINDOW_Q0','WINDOW_Q1','SUMMARY'] and es[-1]['control_count']==receipt['control_count']==4716,'Whole6-stage source lifecycle')
 names=set();cp=[]
 for i,e in enumerate(es[1:-1]):
  p=BASE/e['payload'];c=BASE/e['commit'];seal(p,e['payload_sha256']);seal(c,e['commit_sha256']);v=read(p);cm=read(c);require(p.read_bytes()==canonical(v) and c.read_bytes()==canonical(cm),'Parent canonical complete pair')
  require(v['owner']=='root' and v['pid']==pid and v['source_sha256']==receipt['source_sha256'] and v['manifest_sha256']==receipt['manifest_sha256'],'Parent payload actual owner')
  if count==216:
   require(p.name==f'{stem}_CP{i:04d}.json' and c.name==f'{stem}_CP{i:04d}_COMMIT.json','Exact216 checkpoint names')
   require(v['index']==e['index']==i and cm=={k:e[k] for k in ('index','payload','payload_sha256','owner','pid','epoch','source_sha256','manifest_sha256')},'Full canonical216 commit');require(e['epoch']==v['epoch']==es[0]['epoch']==0,'Actual sole parent epoch');require(len(v['rows'])==21,'Complete21 rows per canonical trial');seal(BASE/v['npz'],v['npz_sha256'])
  else:require(p.name==stem+'_'+e['stage']+'_CP.json' and c.name==stem+'_'+e['stage']+'_CP_COMMIT.json' and cm==dict(stage=e['stage'],owner='root',pid=pid,source_sha256=receipt['source_sha256'],manifest_sha256=receipt['manifest_sha256'],payload=e['payload'],payload_sha256=e['payload_sha256']) and v['stage']==e['stage'],'Full outgoing6 commit')
  cp.append(v);names.update((p.name,c.name))
 require({p.name for p in BASE.glob(stem+'_*CP*.json')}==names and not list(BASE.glob(stem+'_FAILED*')),'Whole exact parent pair census/no error')
 if count==216:require([row for c in cp for row in c['rows']]==r['rows'] and len(r['rows'])==4536 and len(r['comparisons'])==3780 and len(r['checks'])==34256 and all(g['passed'] for g in r['checks']),'Complete canonical rows/checks retained')
 else:require(len(r['arithmetic_controls'])==4716 and all(g['passed'] for g in r['arithmetic_controls']) and len(r['catalogs'])==4 and len(r['coherent_windows'])==2,'Complete outgoing accepted source scope')
 return r,receipt
def authenticate():
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
 full,_=parent('NATIVE_CANONICAL_MAXWELL_PAIR_V003','native_canonical_maxwell_pair_v003.py',9633,216,'CANONICAL_MAXWELL_FIXTURE_PASS')
 outgoing,_=parent('NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001','native_registered_cell_outgoing_source_v001.py',13893,6,'OUTGOING_SOURCE_FUNCTION_ARITHMETIC_PASS')
 witnesses=[]
 for q,index in ((0,0),(1,72)):
  path=BASE/f'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP{index:04d}.json';require(str(path) in SEALS,'Consumed complete spectral witness is sealed');d=read(path);w=d['witness'];require(d['stage']=='SPECTRAL_'+str(q) and w['q']==q and len(w['eigenvalues'])==64 and len(w['incidence_spectral'])==2 and w['groups'][0]['qualified'] and len(w['groups'][0]['indices'])==1,'Owned complete64 spectral source');witnesses.append(w)
 path=BASE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json';require(str(path) in SEALS,'Consumed original coherent packet is sealed');packet=read(path);require(packet['status']=='COMPLETE' and not packet['payload']['failures'] and len(packet['payload']['sectors'])==2 and [s['record_occupation'] for s in packet['payload']['sectors']]==[0,1],'Original complete coherent preparations')
 require(hashlib.sha256(canonical(packet['payload'])[:-1]).hexdigest()==packet['payload_sha256'],'Whole source-packet payload');require(full['configuration']['record_occupations']==[0,1] and full['configuration']['incidences']==list(EDGES) and full['configuration']['omegas']==list(OMEGAS) and full['configuration']['durations']==list(DURATIONS) and full['configuration']['kappas']==[0.,-.001,.001] and full['configuration']['cutoffs']==[8,12,16] and full['configuration']['steps']==[128,256],'Unchanged physical canonical census')
 return witnesses,packet['payload'],full,outgoing
def carr(v,np):return np.asarray(v['real'],float)+1j*np.asarray(v['imag'],float)
def cjson(v):return dict(real=v.real.tolist(),imag=v.imag.tolist())
def rect(x,t,np):return t*np.exp(.5j*x*t)*np.sinc(x*t/(2*math.pi))
def preparations(w,sector,np):
 V=carr(w['eigenvectors'],np);E=np.asarray(w['eigenvalues'],float);require(V.shape==(64,64) and E.shape==(64,) and sector['record_occupation']==w['q'] and [(s['preparation'],s['age']) for s in sector['holds']]==[(p,a) for p in ('cycle','tree') for a in AGES],'Whole64/22 axes and every original label')
 ps=[];labels=[]
 for s in sector['holds']:
  p=carr(s['state_vector'],np);require(p.shape==(64,),'Entire coherent vector');ps.append(V.conj().T@p);labels.append(dict(preparation=s['preparation'],age=s['age'],state_source='UNCHANGED_COHERENT_HOLD'))
 ps.append(V.conj().T@V[:,w['groups'][0]['indices'][0]]);labels.append(dict(preparation='complete_native_ground',age=None,state_source='SAVED_PHYSICAL_FRAME_COLUMN_NO_RENORMALIZATION'))
 return E,np.column_stack(ps),labels
def integrate(E,P,psi,omega,tau,order,np):
 x,w=np.polynomial.legendre.leggauss(order);ts=tau*(x+1)/2;ws=tau*w/2;diff=E[:,None]-E[None,:];D=np.zeros_like(psi);C=np.zeros_like(psi);A=np.zeros_like(psi)
 for t,weight in zip(ts,ws):
  phase=np.exp(1j*E*t);Pt=phase[:,None]*P*phase.conj()[None,:];pp=Pt@psi;inner=(P*rect(2*omega+diff,t,np))@psi
  D+=weight*np.exp(-2j*omega*t)*(Pt@inner);C+=weight*np.exp(2j*omega*t)*pp;A+=weight*pp
 return dict(D=D,C=C,A=A)
def expectation(left,right,np):return np.sum(left.conj()*right,axis=0)
def terms(E,P,psi,omega,tau,D,np):
 diff=E[:,None]-E[None,:];C=(P*rect(2*omega+diff,tau,np))@psi;A=(P*rect(diff,tau,np))@psi;phase=np.exp(1j*E*tau);Pt=phase[:,None]*P*phase.conj()[None,:]
 raw=np.sum(abs(C)**2,axis=0);norm=np.sum(abs(psi)**2,axis=0);pc0=expectation(psi,P@psi,np);pct=expectation(psi,Pt@psi,np);ed=expectation(psi,E[:,None]*D,np);ea=expectation(psi,E[:,None]*A,np);cc=expectation(C,E[:,None]*C,np);dd=expectation(psi,D,np);end=np.exp(-2j*omega*tau)*expectation(psi,Pt@C,np)
 jump=2*omega**2*(cc.real-2*ed.real);vac=2*omega*ea.imag;photon=4*omega**3*raw;on=omega*pc0.real;off=-omega*pct.real-4*omega**2*end.imag
 envelope=2*omega**2*(abs(cc)+2*abs(ed))+2*omega*abs(ea)+photon+omega*(abs(pc0)+abs(pct))+4*omega**2*abs(end)
 return dict(C=C,A=A,norm=norm,raw=raw,pc0=pc0,pct=pct,ed=ed,ea=ea,cc=cc,dd=dd,end=end,jump=jump,vac=vac,native=jump+vac,photon=photon,on=on,off=off,net=on+off,envelope=envelope)
def check(flags,name,error,**ids):flags.append(dict(name=name,error=float(error),tolerance=2e-11,passed=bool(math.isfinite(error) and error<=2e-11),**ids))
def coefficient_case(E,P,psi,labels,q,edge,omega,tau,np,flags):
 require(P.shape==(64,64) and psi.shape==(64,23) and len(labels)==23,'Whole operator/preparation axes')
 quadratures={o:integrate(E,P,psi,omega,tau,o,np) for o in ORDERS};fine=terms(E,P,psi,omega,tau,quadratures[256]['D'],np);coarse=terms(E,P,psi,omega,tau,quadratures[128]['D'],np);P2=float(np.sum(abs(P)**2));rows=[]
 for k,label in enumerate(labels):
  ids=dict(q=q,edge=edge,omega=omega,tau=tau,state=k,preparation=label['preparation'],age=label['age']);floor=1e-280
  unorm=fine['raw'][k]+2*abs(fine['dd'][k]);vnorm=abs(fine['pc0'][k])+abs(fine['pct'][k])+2*abs(fine['ea'][k]);enorm=max(float(fine['envelope'][k]),floor);bound=max(.5*tau*tau*P2*math.sqrt(float(fine['norm'][k])),floor);sbound=max(tau*math.sqrt(P2*float(fine['norm'][k])),floor)
  check(flags,'no_photon_unitarity',abs(fine['raw'][k]-2*fine['dd'][k].real)/max(float(unorm),floor),**ids)
  check(flags,'canonical_vacuum_contact',abs(fine['pc0'][k].real-fine['pct'][k].real-2*fine['ea'][k].imag)/max(float(vnorm),floor),**ids)
  check(flags,'inclusive_native_photon_switch',abs(fine['native'][k]+fine['photon'][k]-fine['on'][k]-fine['off'][k])/enorm,**ids)
  check(flags,'ordered_amplitude128_vs256',np.linalg.norm(quadratures[128]['D'][:,k]-quadratures[256]['D'][:,k])/bound,**ids)
  check(flags,'native_coefficient128_vs256',abs(coarse['native'][k]-fine['native'][k])/max(float(coarse['envelope'][k]+fine['envelope'][k]),floor),**ids)
  check(flags,'closed_pair_amplitude_vs256',np.linalg.norm(fine['C'][:,k]-quadratures[256]['C'][:,k])/sbound,**ids)
  check(flags,'closed_vacuum_contact_vs256',np.linalg.norm(fine['A'][:,k]-quadratures[256]['A'][:,k])/sbound,**ids)
  check(flags,'direct_pair_contact128_vs256',max(np.linalg.norm(quadratures[128]['C'][:,k]-quadratures[256]['C'][:,k]),np.linalg.norm(quadratures[128]['A'][:,k]-quadratures[256]['A'][:,k]))/sbound,**ids)
  rows.append(dict(ids,**label,incoming_norm=float(fine['norm'][k]),native_change=float(fine['native'][k]),native_jump_term=float(fine['jump'][k]),native_vacuum_contact=float(fine['vac'][k]),photon_change=float(fine['photon'][k]),switch_on_work=float(fine['on'][k]),switch_off_work=float(fine['off'][k]),net_switch_work=float(fine['net'][k]),raw_pair_function=float(fine['raw'][k]),initial_P=float(fine['pc0'][k].real),final_unperturbed_P=float(fine['pct'][k].real),complex_no_photon_overlap=[float(fine['dd'][k].real),float(fine['dd'][k].imag)],complex_native_D=[float(fine['ed'][k].real),float(fine['ed'][k].imag)],complex_native_A=[float(fine['ea'][k].real),float(fine['ea'][k].imag)],complex_endpoint_pair=[float(fine['end'][k].real),float(fine['end'][k].imag)],operation_envelope=enorm,coarse_native_change=float(coarse['native'][k]),coefficient_units='kappa^2*Eunit',scope='COMPLETE_QUADRATIC_FINITE_CANONICAL_LEDGER_NOT_EXACT_FINITE_KAPPA_OR_CONTINUUM_HISTORY'))
 data=dict(q=q,edge=edge,omega=omega,tau=tau,rows=rows,C_action=cjson(fine['C']),A_action=cjson(fine['A']),D128_action=cjson(quadratures[128]['D']),D256_action=cjson(quadratures[256]['D']),C128_action=cjson(quadratures[128]['C']),C256_action=cjson(quadratures[256]['C']),A128_action=cjson(quadratures[128]['A']),A256_action=cjson(quadratures[256]['A']))
 return data
def comparisons(full,rows):
 index={(r['q'],r['edge'],r['omega'],r['tau'],r['preparation'],r['age']):r for r in rows};old={(r['q'],r['edge'],r['omega'],r['M'],r['steps'],r['tau'],r['preparation'],r['age'],r['kappa']):r for r in full['rows']};out=[]
 require(len(old)==4536,'All4536 inherited rows unique')
 for q in (0,1):
  for e in EDGES:
   for o in OMEGAS:
    for M in (8,12,16):
     for n in (128,256):
      for tau in DURATIONS:
       for prep,age in [('cycle',0.),('cycle',.5),('cycle',2.),('tree',0.),('tree',.5),('tree',2.),('complete_native_ground',None)]:
        key=(q,e,o,M,n,tau,prep,age);minus,zero,plus=(old[(*key,k)] for k in (-.001,0.,.001));theory=index[q,e,o,tau,prep,age];ev={f:(plus[f]+minus[f]-2*zero[f])/(2*.001**2) for f in FIELDS};out.append(dict(q=q,edge=e,omega=o,M=M,steps=n,tau=tau,preparation=prep,age=age,even_quadratic_estimates=ev,dyson_coefficients={f:theory[f] for f in FIELDS},signed_even_minus_dyson={f:ev[f]-theory[f] for f in FIELDS},original_minus=minus,original_zero=zero,original_plus=plus,scope='SIGNED_FINITE_KAPPA_DIAGNOSTIC_NO_EXACT_EQUALITY_GATE_OR_HIGHER_ORDER_BOUND'))
 require(len(out)==1512,'All1512 even comparisons including every cutoff/time arm');return out
def main():
 global SOURCE,MANIFEST,ENTERED
 require(PROTOCOL_SHA!='PENDING' and not list(BASE.glob(STEM+'_*')),'Frozen protocol/exclusive nonresumable namespace');SOURCE=sha(__file__);tick=time.monotonic();witnesses,packet,full,outgoing=authenticate()
 for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ.setdefault(name,'1')
 import numpy as np
 manifest=dict(source_sha256=SOURCE,input_sha256=SEALS.copy(),omegas=list(OMEGAS),durations=list(DURATIONS),incidences=list(EDGES),orders=list(ORDERS),preparations_per_q=23,coefficient_rows=828,arithmetic_controls=6624,finite_even_comparisons=1512,source_templates=36,checkpoint_count=5,numpy_version=np.__version__,scope='FULL_QUADRATIC_NO_PHOTON_NATIVE_PHOTON_SWITCH_LEDGER_ONLY; NO_NEW_H_EIGEN_TRAJECTORY_CONTINUUM_OR_THERMAL_HISTORY',physical_units='tau=Eunit*tproper/hbar; every coefficient multiplies global kappa^2*Eunit; no new physical scale')
 MANIFEST=write(STEM+'_MANIFEST.json',manifest);ENTERED=True;event('OWNER_START');checkpoint('AUTH',dict(canonical_checks=full['checks'],canonical_comparisons=full['comparisons'],canonical_configuration=full['configuration'],outgoing_arithmetic_controls=outgoing['arithmetic_controls'],outgoing_census=outgoing['manifest']['census']))
 flags=[];cases=[];rows=[]
 for q,w in enumerate(witnesses):
  E,psi,labels=preparations(w,packet['sectors'][q],np);qcases=[]
  for edge,raw in zip(EDGES,w['incidence_spectral']):
   P=carr(raw,np)
   for omega in OMEGAS:
    for tau in DURATIONS:
     d=coefficient_case(E,P,psi,labels,q,edge,omega,tau,np,flags);qcases.append(d);cases.append(d);rows.extend(d['rows'])
  checkpoint('COEFF_Q'+str(q),dict(q=q,absolute_native_energies=E.tolist(),unchanged_prepared_states=cjson(psi),labels=labels,cases=qcases,arithmetic_controls=flags.copy()))
 compare=comparisons(full,rows);checkpoint('COMPARE',dict(comparisons=compare,all4536_original_rows=full['rows'],all3780_original_comparisons=full['comparisons']))
 require(len(cases)==36 and len(rows)==828 and len(flags)==6624,'Frozen entire coefficient/control census');failed=[g for g in flags if not g['passed']];status='COMPLETE_DYSON_ENERGY_ARITHMETIC_PASS' if not failed else 'COMPLETE_DYSON_ENERGY_ARITHMETIC_FAILED';checkpoint('SUMMARY',dict(status=status,controls=len(flags),failures=len(failed),coefficient_rows=len(rows),even_comparisons=len(compare)))
 recheck();result=dict(status=status,manifest=manifest,cases=cases,coefficient_rows=rows,arithmetic_controls=flags,finite_even_comparisons=compare,original_canonical_checks=full['checks'],original_canonical_comparisons=full['comparisons'],original_outgoing_controls=outgoing['arithmetic_controls'],physical_rates_or_thermalization_qualified=False,elapsed_seconds=time.monotonic()-tick);rh=write(STEM+'_RESULT.json',result);rp=BASE/(STEM+'_REPORT.md');report='# Complete finite canonical Dyson energy control\n\n'+status+'; '+str(len(flags)-len(failed))+'/6624 controls. All828 coherent coefficient rows and1512 finite-kappa even comparisons retained. Native no-photon/canonical-vacuum, photon and both switching terms are independent. Finite-kappa discrepancies are descriptive; no thermal, continuum or escaped-radiation qualification.\n'
 with rp.open('xb') as f:f.write(report.encode())
 rp.chmod(0o444);CREATED[str(rp)]=sha(rp);event('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=5,control_count=6624);jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp)]=sha(jp);es=[json.loads(s) for s in jp.read_text().splitlines()];require([e['event'] for e in es]==['OWNER_START']+['CHECKPOINT']*5+['OWNER_COMPLETE'] and [e['stage'] for e in es[1:6]]==list(STAGES),'Complete own natural lifecycle')
 for e in es:require(e['owner']=='root' and e['pid']==os.getpid() and e['source_sha256']==SOURCE and e['manifest_sha256']==MANIFEST,'Own root/source identity')
 require(es[-1]['status']==status and es[-1]['result_sha256']==rh and es[-1]['checkpoint_count']==5 and es[-1]['control_count']==6624,'Own exact terminal');names=set()
 for e in es[1:-1]:
  pn=e['payload'];cn=e['commit'];v=read(BASE/pn);c=read(BASE/cn);names.update((pn,cn));require((BASE/pn).read_bytes()==canonical(v) and (BASE/cn).read_bytes()==canonical(c) and sha(BASE/pn)==e['payload_sha256'] and sha(BASE/cn)==e['commit_sha256'],'Own complete canonical pair/event binding');require(c==dict(stage=e['stage'],owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,payload=pn,payload_sha256=e['payload_sha256']) and v['stage']==e['stage'] and v['owner']=='root' and v['pid']==os.getpid() and v['source_sha256']==SOURCE and v['manifest_sha256']==MANIFEST,'Own full commit/payload schema')
 require({p.name for p in BASE.glob(STEM+'_*CP*.json')}==names,'Own complete five-pair census');recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE,input_sha256=SEALS,output_sha256=CREATED.copy(),manifest_sha256=MANIFEST,journal_sha256=sha(jp),result_sha256=rh,checkpoint_count=5,control_count=6624));recheck();return 0 if not failed else 3
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');args=ap.parse_args()
 if not args.execute:raise SystemExit('Root only after full frozen independent review')
 try:raise SystemExit(main())
 except Exception:
  if ENTERED and not (BASE/(STEM+'_RESULT.json')).exists():write(STEM+'_FAILED.json',dict(time=datetime.now(timezone.utc).isoformat(),owner='root',pid=os.getpid(),source_sha256=SOURCE,manifest_sha256=MANIFEST,traceback=traceback.format_exc(),created=CREATED.copy()));event('FAILED')
  raise
