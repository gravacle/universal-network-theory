"""Independent stdlib SAVED-only extension; no trajectory or producer imports."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import sys

BASE=Path(__file__).resolve().parent
OLD='SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
P='SAME_T_CLOCK_GRADIENT_FLRW_TIME_REFINEMENT_V002'
A=P+'_SAVED_AUDIT_V001'
PROTOCOL_SHA='1edefb3a3e0d13807bac8ff66dd8928703d37c2e0e913788e8510dc203030d0a'
PINS={
 'same_t_clock_gradient_flrw_time_refinement_v002.py':'8ae0547f35e344afedfb170195e05b322f1ead052264ff36dc0715964197e401',
 P+'.md':'7316538aa96810b6c65a66223ecccc97be3a989ec1df8b16f13ede0f64a95a13',
 P+'_RESULT.json':'dc562ccae558426fb9e361c5fb93929d3d4d08bc6b1c8377a203a884de7495ff',
 P+'_RECEIPT.json':'264249c4852d7f9eb0c4ebc5195eef30f076cedf172347634a8c3516469132a4',
 'same_t_clock_gradient_flrw_response_saved_audit_v001.py':'a7415fd27881d1df1b3e5ff4b37fb810608a54b961d56da480a53d5935290b69',
 OLD+'_SAVED_AUDIT_V001.json':'06cd50bcbe4c21ab365d09fe0d0de8a4fdb9300cf0e3dc75e263e0240fb08c58',
 OLD+'_SAVED_AUDIT_V001_RECEIPT.json':'6e0c97ae994c552d6e20d1c95e464240c6d4d40f3ba7965ce111751303d7a085',
 OLD+'_RESULT.json':'76549b997b915af67ef35472b3b5faa5004ccf9b490a8c7aa545ec8937f295ac',
 OLD+'_RECEIPT.json':'d4baa47a6fea4743780446206c56294b4c238fb104c11edfde36f23853b417c4',
 P+'_SAVED_AUDIT_PROTOCOL_V001.md':PROTOCOL_SHA}
CASES=[[k,o] for k in (.01,.1) for o in (0.,.1,1.,10.,100.)]
FN=['Phi','delta_b','Hunit_v_b','delta_rad','Hunit_v_rad','Hunit_pi',
    'delta_rho_clock_over_rho_star','Z','Z_prime']
SEED=1e-8; X0=math.log(.01); EPS=sys.float_info.epsilon
N=0; MAX_ABS=0.; AUTH={}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(n):return json.loads((BASE/n).read_text())
def ok(n,c):
 global N
 N+=1
 if not c:raise AssertionError(n)
def eq(n,a,b):ok(n,a==b)
def close(n,a,b,floor=1e-30,abstol=0.):
 global MAX_ABS
 a=float(a);b=float(b);err=abs(a-b);MAX_ABS=max(MAX_ABS,err)
 ok(n,math.isfinite(a) and math.isfinite(b) and err<=max(abstol,1e-11*max(abs(a),abs(b),floor)))
def finite(n,x):
 if isinstance(x,list):
  for v in x:finite(n,v)
 else:ok(n,isinstance(x,(int,float)) and math.isfinite(x))
def vector(n,a,b,floor=1e-30):
 eq(n+' length',len(a),len(b))
 for i,(x,y) in enumerate(zip(a,b)):close(n+' '+str(i),x,y,floor)
def auth(n,h):eq('seal '+n,sha(BASE/n),h);AUTH[n]=h

def main():
 AUTH[Path(__file__).name]=sha(__file__)
 for n,h in PINS.items():auth(n,h)
 old=read(OLD+'_RESULT.json');oldrec=read(OLD+'_RECEIPT.json')
 accepted=read(OLD+'_SAVED_AUDIT_V001.json');acceptedrec=read(OLD+'_SAVED_AUDIT_V001_RECEIPT.json')
 eq('original arithmetic accepted',accepted['status'],'SAVED_ARITHMETIC_ACCEPTED')
 eq('original raw anchor',accepted['parent_result_sha256'],PINS[OLD+'_RESULT.json'])
 eq('original receipt anchor',accepted['parent_receipt_sha256'],PINS[OLD+'_RECEIPT.json'])
 eq('original disposition',[accepted['parent_passed'],accepted['parent_total'],accepted['qualified_parent_forecast']],[426,441,False])
 eq('original audit receipt',acceptedrec['audit_sha256'],PINS[OLD+'_SAVED_AUDIT_V001.json'])
 eq('original audit source',acceptedrec['source_sha256'],PINS['same_t_clock_gradient_flrw_response_saved_audit_v001.py'])
 eq('original audit raw source',accepted['source_sha256'],acceptedrec['source_sha256'])
 eq('original assertion receipt',acceptedrec['assertions'],accepted['assertions'])
 eq('original audit input equality',acceptedrec['inputs'],accepted['inputs'])
 auth(OLD+'_SAVED_AUDIT_V001.md',acceptedrec['report_sha256'])
 for n,h in accepted['inputs'].items():auth(n,h)
 eq('original receipt identity',oldrec['result_sha256'],PINS[OLD+'_RESULT.json'])
 res=read(P+'_RESULT.json');rec=read(P+'_RECEIPT.json');man=read(P+'_MANIFEST.json')
 expected_inputs=dict(old['manifest']['lineage']['inputs'])
 expected_inputs.update({
  'same_t_clock_gradient_flrw_response_v001.py':'61e6191713e5eb628b2ec551de43c200a029a6f236f7da255e867fca1d8d0990',
  OLD+'.md':'61ee3ff72207a8e25d7a9b4eb736e438ccc409d6d897402dafd58a231e214e9a',
  OLD+'_RESULT.json':PINS[OLD+'_RESULT.json'],OLD+'_RECEIPT.json':PINS[OLD+'_RECEIPT.json']})
 expected_inputs[P+'.md']=PINS[P+'.md']
 eq('eleven consumed input pins',len(expected_inputs),11)
 for n,h in expected_inputs.items():auth(n,h)
 lineage=dict(inputs=expected_inputs,source_sha256=PINS['same_t_clock_gradient_flrw_time_refinement_v002.py'])
 eq('result manifest',res['manifest'],man);eq('manifest lineage',man['lineage'],lineage);eq('receipt lineage',rec['lineage'],lineage)
 eq('manifest census',[man['cases'],man['new_trial'],man['reused_trials']],[CASES,['NEW_FINE',65536,48],['FINE','MODES']])
 eq('same fixed inventory',man['fixed'],old['manifest']['fixed']);f=man['fixed']
 eq('completed status',[res['status'],rec['status']],['COMPLETED','COMPLETED'])
 eq('receipt result anchor',rec['result_sha256'],PINS[P+'_RESULT.json'])
 for n,h in [(P+'_MANIFEST.json',rec['manifest_sha256']),(P+'_REPORT.md',rec['report_sha256']),(P+'_JOURNAL.jsonl',rec['journal_sha256'])]:auth(n,h)
 new=res['new_trial'];eq('new trial census',[new['label'],new['steps'],new['ns']],['NEW_FINE',65536,48])
 nodes,weights=new['snodes'],new['weights'];eq('48 nodes/weights',[len(nodes),len(weights)],[48,48])
 ok('ordered positive nodes',all(0<x<1 for x in nodes) and all(a<b for a,b in zip(nodes,nodes[1:])))
 ok('positive weights',all(x>0 for x in weights));finite('nodes/weights',nodes+weights)
 snaps=new['snapshots'];eq('65 new snapshots',len(snaps),65);eq('ordered snapshot steps',[s['n'] for s in snaps],list(range(0,65537,1024)))
 norm=1/f['eps']-math.log1p(1/f['eps']);dx=-X0/65536
 for snap in snaps:
  x=X0+snap['n']*dx;eq('snapshot x',snap['x'],x);bg=snap['background'];s=bg['s'];ok('positive saved s',s>0)
  a=math.exp(x);qp=math.sqrt(1+f['eps']*s/(1+s));d=f['d0']/a**3;pex=(math.log1p(s)-s/(1+s))/norm
  b=1.5*f['OB']/f['rG']/a**3;r=1.5*f['OR']/f['rG']/a**4;w=1.5*f['OA']/f['rG']*qp*d
  rho=1.5*f['OA']/f['rG']*(1+qp*d-pex);h=math.sqrt((2/3)*(b+r+rho))
  cs=f['eps']*s/(2+(4+3*f['eps'])*s+2*(1+f['eps'])*s*s)
  oracle=dict(a=a,h=h,b=b,r=r,w=w,rho=rho,cs=cs,qbar=qp,s=s,charge=d,charge_error=abs(2*qp*s/(f['eps']*norm)/d-1))
  eq('background schema',set(bg),set(oracle))
  for key,val in oracle.items():close('background '+key,bg[key],val,abstol=1e-13 if key=='charge_error' else 0.)
  eq('ten cases',len(snap['state']),10);finite('full new state',snap['state'])
  for c,(k,om) in enumerate(CASES):
   eq('two seeds',len(snap['state'][c]),2);q=k*299792.458/f['Hunit']/a
   for seed in range(2):
    y=snap['state'][c][seed];eq('103 state entries',len(y),103);phi,db,ub,dr,ur,u,E=y[:7]
    for vals,actual in [(y[7:55],snap['fluids'][c][seed][7]),(y[55:],snap['fluids'][c][seed][8])]:
     products=[v*wt for v,wt in zip(vals,weights)];close('independent fsum modes',actual,math.fsum(products),SEED*1e-8,192*EPS*math.fsum(abs(v) for v in products))
    vector('primitive fluids',snap['fluids'][c][seed][:7],y[:7],SEED*1e-8);Z,Zp=snap['fluids'][c][seed][7:]
    mom=b*ub+4*r*ur/3+w*u;terms=[q*q*phi,3*h*mom,b*db,r*dr,E,-q*Z]
    vector('normal terms',snap['normal_terms'][c][seed],terms,SEED*1e-8)
    den=max(math.fsum(abs(v) for v in terms),q*q*SEED*1e-10);close('normal error',snap['normal_error'][c][seed],abs(math.fsum(terms))/den,abstol=1e-13)
    phy=[db+3*h*ub,r*(dr+4*h*ur),E+3*h*w*u,-q*Z,2*phi,-q*cs*(E/w+3*h*u)]
    vector('physical readouts',snap['physical'][c][seed],phy,SEED*1e-8)
    close('density weighted normal',b*phy[0]+phy[1]+phy[2]+phy[3]+q*q*phi,math.fsum(terms),abstol=128*EPS*math.fsum(abs(v) for v in terms))
    vector('amplitudes',snap['amplitudes'][c][seed],[abs(phi),abs(db),abs(dr),abs(E/w),abs(q*ub),abs(q*ur),abs(q*u),abs(phy[5])],SEED*1e-8)
    lo=f['eps']*s/((1+s)*qp*(qp+1));hi=f['eps']/((1+s)*qp*(math.sqrt(1+f['eps'])+qp));rate=cs*E/w
    vector('clock domain',snap['clock_domain'][c][seed],[rate,lo,hi,abs(rate)/min(lo,hi)],SEED*1e-8)
    if snap['n']==0:
     Phi,U=(SEED,0.) if seed==0 else (0.,SEED/h);Ds=-q*q*Phi/(b+4*r/3+w)-3*h*U
     vector('seed',y,[Phi,Ds,U,4*Ds/3,U,U,w*Ds]+[0.]*96,SEED*1e-8)
 events=[json.loads(x) for x in (BASE/(P+'_JOURNAL.jsonl')).read_text().splitlines()]
 eq('34 events',len(events),34);eq('start',[events[0]['event'],events[0]['owner'],events[0]['source_sha256']],['OWNER_START','root',lineage['source_sha256']])
 cpnames=[]
 for i,n in enumerate(range(2048,65537,2048),1):
  pn=P+'_NEW_FINE_CP_'+str(n).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json';ev=events[i]
  eq('checkpoint event',[ev['event'],ev['trial'],ev['n'],ev['payload']],['CHECKPOINT','NEW_FINE',n,pn]);auth(pn,ev['sha256']);auth(cn,ev['commit_sha256'])
  eq('commit',read(cn),dict(lineage=lineage,steps=65536,ns=48,payload=pn,sha256=ev['sha256']))
  eq('full checkpoint payload',read(pn),dict(lineage=lineage,steps=65536,ns=48,n=n,state=snaps[n//1024]['state'],snapshots=snaps[:n//1024+1]));cpnames.extend([pn,cn])
 eq('32 checkpoint pairs',len(cpnames),64);eq('no orphan CP',set(x.name for x in BASE.glob(P+'_NEW_FINE_CP_*.json')),set(cpnames))
 eq('owner complete',[events[-1]['event'],events[-1]['result_sha256']],['OWNER_COMPLETE',PINS[P+'_RESULT.json']])
 oldfails=[g for g in old['numerical_gates'] if not g['passed']]
 eq('fifteen original failures',len(oldfails),15);eq('preserved original failures',res['original_failed_gates_preserved'],oldfails)
 eq('accepted failures',accepted['failed_parent_gates'],oldfails)
 gates=[dict(g,inherited_from=PINS[OLD+'_RESULT.json']) for g in old['numerical_gates'] if g['name']!='time_refinement']
 eq('261 unchanged inherited gates',len(gates),261)
 def gate(name,error,tol,**ident):gates.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(math.isfinite(error) and error<=tol),**ident))
 gate('new_spectral_normalization',abs(sum(weights)-1),1e-13)
 gate('new_charge_root',max(s['background']['charge_error'] for s in snaps),1e-13)
 fine,modes=old['trials'][1:];eq('reused fine/modes',[[q['label'],q['steps'],q['ns']] for q in (fine,modes)],[['FINE',32768,48],['MODES',32768,96]])
 for c,(k,om) in enumerate(CASES):
  for seed in range(2):
   gate('new_normal_constraint',max(s['normal_error'][c][seed] for s in snaps),1e-6,case=c,seed=seed)
   if om==0:gate('new_mode_off_zero',max(abs(v) for s in snaps for v in s['state'][c][seed][7:]),1e-13,case=c,seed=seed)
   for vi,name in enumerate(FN):
    vals=[s['fluids'][c][seed][vi] for s in snaps];older=[s['fluids'][c][seed][vi] for s in fine['snapshots']]
    gate('new_time_refinement',max(abs(a-b) for a,b in zip(vals,older))/max(max(abs(v) for v in vals),SEED*1e-8),1e-4,case=c,seed=seed,variable=name)
 eq('467 gates',len(gates),467);eq('467 stored gates',len(res['numerical_gates']),467)
 for actual,expected in zip(res['numerical_gates'],gates):
  eq('gate exact disposition',{k:v for k,v in actual.items() if k!='error'},{k:v for k,v in expected.items() if k!='error'});close('gate arithmetic',actual['error'],expected['error'])
 passed=sum(g['passed'] for g in gates);eq('aggregate qualification',res['all_numerical_gates_passed'],passed==467)
 eq('journal qualification',[events[-1]['passed'],events[-1]['total']],[passed,467])
 for key in ('endpoints','physical_fixture_flags','endpoint_effect_refinements'):eq('20 '+key,len(res[key]),20)
 eq('physical names',res['physical_names'],old['physical_names'])
 for idx,(c,seed) in enumerate((c,s) for c in range(10) for s in range(2)):
  k,om=CASES[c];ref=0 if c<5 else 5;row=res['endpoints'][idx];newp=snaps[-1]['physical'];oldp=fine['snapshots'][-1]['physical'];modep=modes['snapshots'][-1]['physical']
  eq('endpoint',[row['case'],row['seed'],row['k_Mpc_inverse'],row['omega_over_old_Hunit']],[c,seed,k,om]);vector('endpoint physical',row['physical'],newp[c][seed],SEED*1e-8)
  n=[a-b for a,b in zip(newp[c][seed],newp[ref][seed])];o=[a-b for a,b in zip(oldp[c][seed],oldp[ref][seed])];sp=[a-b for a,b in zip(modep[c][seed],modep[ref][seed])]
  dt=[a-b for a,b in zip(o,n)];ds=[a-b for a,b in zip(sp,o)];margin=[3*max(abs(a),abs(b)) for a,b in zip(dt,ds)]
  vector('signed endpoint',row['difference_from_mode_off'],n,SEED*1e-8);effect=res['endpoint_effect_refinements'][idx];eq('effect identity',[effect['case'],effect['seed']],[c,seed])
  for key,val in [('fine_effect',n),('old_fine_effect',o),('old_spectral_effect',sp),('time_change',dt),('spectral_change',ds),('three_change_margin',margin)]:vector('paired '+key,effect[key],val,SEED*1e-8)
  eq('resolution',effect['resolution'],['control_zero' if om==0 else ('resolved' if abs(v)>m else 'unresolved') for v,m in zip(n,margin)])
  flag=res['physical_fixture_flags'][idx];eq('flag identity',[flag['case'],flag['seed']],[c,seed]);amp=max(max(s['amplitudes'][c][seed]) for s in snaps);domain=max(s['clock_domain'][c][seed][3] for s in snaps)
  close('sampled amplitude',flag['maximum_amplitude'],amp);close('sampled domain',flag['maximum_clock_domain_fraction'],domain);eq('small flag',flag['small_perturbation'],amp<.01);eq('domain flag',flag['inside_clock_domain'],domain<1)
  if domain==0:eq('null ceiling',flag['sampled_maximum_basis_amplitude'],None)
  else:close('absolute ceiling',flag['sampled_maximum_basis_amplitude'],SEED/domain)
  eq('sampled scope',flag['scope'],'sampled at65 times, not an all-times certificate')
 report=(BASE/(P+'_REPORT.md')).read_text();ok('report gate census',str(passed)+'/467 current numerical gates PASS.' in report)
 eq('twenty report rows',sum(x.startswith('| ') and not x.startswith('| k/') and not x.startswith('|---') for x in report.splitlines()),20)
 for row in res['endpoints']:
  line=f'| {row["k_Mpc_inverse"]} | {row["omega_over_old_Hunit"]} | {row["seed"]} | {row["physical"][0]:.12g} | {row["difference_from_mode_off"][0]:.12g} | {row["physical"][4]:.12g} |';ok('signed report row',line in report)
 eq('no failure artifacts',len(list(BASE.glob(P+'_FAILED_*'))),0)
 for n,h in AUTH.items():eq('final seal '+n,sha(BASE/n),h)
 outputs=[BASE/(A+s) for s in ('.json','.md','_RECEIPT.json')]
 for p in outputs:ok('exclusive '+p.name,not p.exists())
 summary=dict(status='SAVED_ARITHMETIC_ACCEPTED',assertions=N,maximum_absolute_comparison_difference=MAX_ABS,parent_passed=passed,parent_total=467,qualified_parent_forecast=res['all_numerical_gates_passed'],original_failed_gates=oldfails,new_failed_gates=[g for g in gates if not g['passed']],source_sha256=sha(__file__),parent_result_sha256=PINS[P+'_RESULT.json'],parent_receipt_sha256=PINS[P+'_RECEIPT.json'],inputs=AUTH,checkpoint_pairs=32,journal_events=34,scope='saved-only extension; original failures retained, sampled flags and nondirected resolution labels')
 with outputs[0].open('x') as f:json.dump(summary,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
 outputs[0].chmod(0o444)
 with outputs[1].open('x') as f:f.write(f'# Same-T time-refinement saved acceptance V001\n\nPASS {N:,} assertions. Current gates {passed}/467; original fifteen failures remain preserved.\n\nAll NEW65 snapshots/20 channels,32CPpairs/34events, signed paired effects and physical flags authenticate. No producer import, root solve, RHS or evolution.\n\nAudit SHA256: {sha(outputs[0])}.\n')
 outputs[1].chmod(0o444)
 with outputs[2].open('x') as f:json.dump(dict(audit_sha256=sha(outputs[0]),report_sha256=sha(outputs[1]),source_sha256=sha(__file__),assertions=N,inputs=AUTH),f,sort_keys=True,separators=(',',':'));f.write('\n')
 outputs[2].chmod(0o444)
 for n,h in AUTH.items():
  if sha(BASE/n)!=h:raise RuntimeError('Post-publication input changed '+n)
 print(json.dumps(dict(status=summary['status'],assertions=N,parent_passed=passed,parent_total=467,audit_sha256=sha(outputs[0]),receipt_sha256=sha(outputs[2]))))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true')
 if not p.parse_args().execute:raise SystemExit('Root must explicitly authorize saved-only --execute')
 if any('PENDING' in h for h in PINS.values()):raise SystemExit('Final accepted closure/protocol seals required')
 if any((BASE/(A+s)).exists() for s in ('.json','.md','_RECEIPT.json','_ERROR.json')):raise SystemExit('Audit evidence exists; no overwrite')
 try:main()
 except Exception as ex:
  ep=BASE/(A+'_ERROR.json')
  with ep.open('x') as f:json.dump(dict(error=repr(ex),assertions=N,pid=os.getpid(),source_sha256=sha(__file__)),f,sort_keys=True);f.write('\n')
  ep.chmod(0o444);raise
