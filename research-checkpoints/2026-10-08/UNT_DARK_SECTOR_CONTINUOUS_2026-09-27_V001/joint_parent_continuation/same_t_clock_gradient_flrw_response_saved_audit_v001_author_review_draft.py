"""Independent standard-library SAVED-only acceptance; root owns --execute."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import math
import os
import sys

BASE=Path(__file__).resolve().parent
P='SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
A=P+'_SAVED_AUDIT_V001'
PROTOCOL_SHA='1fcdc36c26788cba82f39cd9e22ecd47e93781519c27ed1c14acc4ef866d163e'
PINS={
 'same_t_clock_gradient_flrw_response_v001.py':'61e6191713e5eb628b2ec551de43c200a029a6f236f7da255e867fca1d8d0990',
 P+'.md':'61ee3ff72207a8e25d7a9b4eb736e438ccc409d6d897402dafd58a231e214e9a',
 P+'_RESULT.json':'76549b997b915af67ef35472b3b5faa5004ccf9b490a8c7aa545ec8937f295ac',
 P+'_RECEIPT.json':'d4baa47a6fea4743780446206c56294b4c238fb104c11edfde36f23853b417c4',
 P+'_SAVED_AUDIT_PROTOCOL_V001.md':PROTOCOL_SHA}
CASES=[[k,o] for k in (.01,.1) for o in (0.,.1,1.,10.,100.)]
TRIALS=[['COARSE',16384,48],['FINE',32768,48],['MODES',32768,96]]
FN=['Phi','delta_b','Hunit_v_b','delta_rad','Hunit_v_rad','Hunit_pi',
    'delta_rho_clock_over_rho_star','Z','Z_prime']
PN=['comoving_delta_b','comoving_rad_density','comoving_clock_density',
    'polarization_density','Weyl','normal_acceleration']
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
def authenticate(n,h):
 eq('seal '+n,sha(BASE/n),h);AUTH[n]=h
def assignment(tree,n):
 return ast.literal_eval(next(x.value for x in tree.body if isinstance(x,ast.Assign)
  and any(isinstance(t,ast.Name) and t.id==n for t in x.targets)))

def main():
 for n,h in PINS.items():authenticate(n,h)
 tree=ast.parse((BASE/'same_t_clock_gradient_flrw_response_v001.py').read_text())
 parentpins=assignment(tree,'PINS');parentpins[P+'.md']=assignment(tree,'PROTOCOL_SHA')
 for n,h in parentpins.items():authenticate(n,h)
 eq('producer eight-input census',len(parentpins)+1,8)
 source_sha=PINS['same_t_clock_gradient_flrw_response_v001.py']
 lineage={'inputs':parentpins,'source_sha256':source_sha}
 res=read(P+'_RESULT.json');rec=read(P+'_RECEIPT.json');man=read(P+'_MANIFEST.json')
 eq('receipt lineage',rec['lineage'],lineage);eq('result manifest',res['manifest'],man)
 eq('manifest lineage',man['lineage'],lineage)
 for n,h in [(P+'_MANIFEST.json',rec['manifest_sha256']),
             (P+'_REPORT.md',rec['report_sha256']),(P+'_JOURNAL.jsonl',rec['journal_sha256'])]:authenticate(n,h)
 eq('receipt result',rec['result_sha256'],PINS[P+'_RESULT.json']);eq('receipt status',rec['status'],'COMPLETED')
 eq('cases',man['cases'],CASES);eq('trials',man['trials'],TRIALS)
 eq('seeds',man['seeds'],['fixed_Phi_zero_velocity','zero_Phi_fixed_velocity'])
 eq('native absent',man['extra_native_remainder'],'absent');eq('minimal action',man['minimal_new_same_T_action'],True)
 eq('radiation fixture',man['radiation'],'conserved perfect fluid, no anisotropic stress')
 f=man['fixed'];cal=read('INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json')
 sel=cal['selected'];owned=cal['fixed'];context=cal['trials'][-1]['atomic_invocation']['context']
 fixed={'Hunit':sel['Hunit'],'OA':owned['omega_A'],'OB':sel['OB'],'OR':context['OR'],
        'd0':owned['d0'],'eps':owned['eps'],'rG':owned['rG'],'Q0_over_old_Hunit':owned['Q0_over_H0'],
        'ell_pc':100.,'L':100e-6*sel['Hunit']/299792.458,'seed':SEED,'initial_a':.01}
 eq('fixed inventory',f,fixed);eq('selected Hunit context',context['fixed']['H0_km_s_Mpc'],sel['Hunit'])
 eq('selected baryon context',context['fixed']['omega_b_cos'],sel['OB'])
 eq('physical names',res['physical_names'],PN);eq('result status',res['status'],'COMPLETED')
 rows=res['trials'];eq('three trials',len(rows),3)
 computed=[];normalized=[]
 norm=1/f['eps']-math.log1p(1/f['eps'])
 for row,(label,steps,ns) in zip(rows,TRIALS):
  eq('trial identity',[row['label'],row['steps'],row['ns']],[label,steps,ns])
  nodes=row['snodes'];weights=row['weights'];eq('nodes count',len(nodes),ns);eq('weights count',len(weights),ns)
  ok('nodes open ordered',all(0<x<1 for x in nodes) and all(a<b for a,b in zip(nodes,nodes[1:])))
  ok('positive weights',all(x>0 for x in weights));finite('nodes/weights',nodes+weights)
  snaps=row['snapshots'];eq('65 snapshots',len(snaps),65);dx=-X0/steps
  eq('ordered snapshot steps',[s['n'] for s in snaps],list(range(0,steps+1,steps//64)))
  local=[]
  for snap in snaps:
   n=snap['n'];x=X0+n*dx;eq('snapshot x',snap['x'],x)
   bg=snap['background'];a=math.exp(x);s=bg['s'];ok('positive saved s',s>0)
   qp=math.sqrt(1+f['eps']*s/(1+s));d=f['d0']/a**3;pex=(math.log1p(s)-s/(1+s))/norm
   b=1.5*f['OB']/f['rG']/a**3;r=1.5*f['OR']/f['rG']/a**4
   w=1.5*f['OA']/f['rG']*qp*d;rho=1.5*f['OA']/f['rG']*(1+qp*d-pex)
   h=math.sqrt((2/3)*(b+r+rho));cs=f['eps']*s/(2+(4+3*f['eps'])*s+2*(1+f['eps'])*s*s)
   oracle={'a':a,'h':h,'b':b,'r':r,'w':w,'rho':rho,'cs':cs,'qbar':qp,'s':s,'charge':d,
           'charge_error':abs(2*qp*s/(f['eps']*norm)/d-1)}
   eq('background schema',set(bg),set(oracle))
   for key,val in oracle.items():close('background '+key,bg[key],val,abstol=1e-13 if key=='charge_error' else 0.)
   state=snap['state'];eq('case count',len(state),10);finite('full state',state)
   snaprows=[]
   for c,(k,om) in enumerate(CASES):
    eq('two basis states',len(state[c]),2);q=k*299792.458/f['Hunit']/a
    for seed in range(2):
     y=state[c][seed];eq('full state dimension',len(y),7+2*ns)
     phi,db,ub,dr,ur,u,E=y[:7];zw=[x*y for x,y in zip(y[7:7+ns],weights)];vw=[x*y for x,y in zip(y[7+ns:],weights)]
     Z=math.fsum(zw);Zp=math.fsum(vw);rz=4*ns*EPS*math.fsum(abs(x) for x in zw);rv=4*ns*EPS*math.fsum(abs(x) for x in vw)
     for actual,expected,bound in [(snap['fluids'][c][seed][7],Z,rz),(snap['fluids'][c][seed][8],Zp,rv)]:close('weighted modes',actual,expected,SEED*1e-8,bound)
     vector('fluid primitive',snap['fluids'][c][seed][:7],y[:7],SEED*1e-8)
     # Subsequent serialization identities use authenticated stored moments;
     # independent fsum controls above carry their explicit roundoff bound.
     Z,Zp=snap['fluids'][c][seed][7:]
     mom=b*ub+4*r*ur/3+w*u;terms=[q*q*phi,3*h*mom,b*db,r*dr,E,-q*Z]
     vector('normal terms',snap['normal_terms'][c][seed],terms,SEED*1e-8)
     den=max(math.fsum(abs(v) for v in terms),q*q*SEED*1e-10)
     ne=abs(math.fsum(terms))/den;close('normal error serialization',snap['normal_error'][c][seed],ne,abstol=1e-13)
     physical=[db+3*h*ub,r*(dr+4*h*ur),E+3*h*w*u,-q*Z,2*phi,-q*cs*(E/w+3*h*u)]
     vector('physical readouts',snap['physical'][c][seed],physical,SEED*1e-8)
     sumdensity=b*physical[0]+physical[1]+physical[2]+physical[3]+q*q*phi
     close('weighted comoving normal identity',sumdensity,math.fsum(terms),abstol=128*EPS*math.fsum(abs(v) for v in terms))
     amp=[abs(phi),abs(db),abs(dr),abs(E/w),abs(q*ub),abs(q*ur),abs(q*u),abs(physical[5])]
     vector('amplitude readouts',snap['amplitudes'][c][seed],amp,SEED*1e-8)
     lo=f['eps']*s/((1+s)*qp*(qp+1));hi=f['eps']/((1+s)*qp*(math.sqrt(1+f['eps'])+qp));rate=cs*E/w
     vector('clock domain readouts',snap['clock_domain'][c][seed],[rate,lo,hi,abs(rate)/min(lo,hi)],SEED*1e-8)
     if n==0:
      Phi,U=(SEED,0.) if seed==0 else (0.,SEED/h);Ds=-q*q*Phi/(b+4*r/3+w)-3*h*U
      vector('exact constraint seed',y,[Phi,Ds,U,4*Ds/3,U,U,w*Ds]+[0.]*(2*ns),SEED*1e-8)
     snaprows.append(physical)
   local.append(snaprows)
  computed.append(local);normalized.append(abs(sum(weights)-1))
 events=[json.loads(x) for x in (BASE/(P+'_JOURNAL.jsonl')).read_text().splitlines()]
 eq('42 journal events',len(events),42);eq('owner start',events[0]['event'],'OWNER_START');eq('owner root',events[0]['owner'],'root')
 eq('owner source',events[0]['source_sha256'],source_sha);eq('owner complete',events[-1]['event'],'OWNER_COMPLETE')
 eq('journal raw result',events[-1]['result_sha256'],PINS[P+'_RESULT.json'])
 cpnames=[];ei=1
 for row,(label,steps,ns) in zip(rows,TRIALS):
  for n in range(2048,steps+1,2048):
   stem=P+'_'+label+'_CP_'+str(n).zfill(6);pn=stem+'.json';cn=stem+'_COMMIT.json';event=events[ei];ei+=1
   eq('checkpoint event',[event['event'],event['trial'],event['n'],event['payload']],['CHECKPOINT',label,n,pn])
   authenticate(cn,event['commit_sha256']);authenticate(pn,event['sha256']);commit=read(cn);payload=read(pn)
   eq('commit schema',set(commit),{'lineage','steps','ns','payload','sha256'})
   eq('commit exact',commit,dict(lineage=lineage,steps=steps,ns=ns,payload=pn,sha256=event['sha256']))
   eq('payload schema',set(payload),{'lineage','steps','ns','n','state','snapshots'})
   expected=dict(lineage=lineage,steps=steps,ns=ns,n=n,state=row['snapshots'][n//(steps//64)]['state'],snapshots=row['snapshots'][:n//(steps//64)+1])
   eq('full checkpoint prefix',payload,expected);cpnames +=[pn,cn]
 eq('40 checkpoint pairs',len(cpnames),80)
 eq('no orphan checkpoint files',set(x.name for x in BASE.glob(P+'*_CP_*.json')),set(cpnames))
 gates=[]
 def gate(name,error,tol,**ident):gates.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(math.isfinite(error) and error<=tol),**ident))
 for ri,row in enumerate(rows):
  gate('spectral_normalization',normalized[ri],1e-13,trial=row['label'])
  gate('charge_root',max(s['background']['charge_error'] for s in row['snapshots']),1e-13,trial=row['label'])
  for c,(k,om) in enumerate(CASES):
   for seed in range(2):
    gate('normal_constraint',max(s['normal_error'][c][seed] for s in row['snapshots']),1e-6,trial=row['label'],case=c,seed=seed)
    if om==0:gate('mode_off_zero',max(abs(v) for s in row['snapshots'] for v in s['state'][c][seed][7:]),1e-13,trial=row['label'],case=c,seed=seed)
 for index,name in [(0,'time'),(2,'spectral')]:
  for c in range(10):
   for seed in range(2):
    for vi,label in enumerate(FN):
     fine=[s['fluids'][c][seed][vi] for s in rows[1]['snapshots']];other=[s['fluids'][c][seed][vi] for s in rows[index]['snapshots']]
     er=max(abs(a-b) for a,b in zip(other,fine))/max(max(abs(v) for v in fine),SEED*1e-8)
     gate(name+'_refinement',er,1e-4,case=c,seed=seed,variable=label)
 for c in (0,5):gate('mode_off_spectral_identity',max(abs(a-b) for seed in range(2) for a,b in zip(rows[1]['snapshots'][-1]['state'][c][seed][:7],rows[2]['snapshots'][-1]['state'][c][seed][:7]))/SEED,1e-12,case=c)
 bg=rows[1]['snapshots'][-1]['background'];s=bg['s']
 inventory=abs(bg['h']**2*f['rG']-(f['OA']*(1+bg['qbar']*bg['charge']-(math.log1p(s)-s/(1+s))/norm)+f['OB']+f['OR']))
 gate('fixed_inventory_H_identity',inventory,1e-13)
 eq('441 gate census',len(gates),441);eq('stored441 gates',len(res['numerical_gates']),441)
 for stored,expected in zip(res['numerical_gates'],gates):
  eq('gate identity',{k:v for k,v in stored.items() if k!='error'},{k:v for k,v in expected.items() if k!='error'})
  close('gate arithmetic',stored['error'],expected['error'])
 eq('aggregate qualification',res['all_numerical_gates_passed'],all(g['passed'] for g in gates))
 eq('journal gates',events[-1]['gates'],441);eq('journal passed',events[-1]['passed'],sum(g['passed'] for g in gates))
 eq('20 endpoints',len(res['endpoints']),20);eq('20flags',len(res['physical_fixture_flags']),20);eq('20effect rows',len(res['endpoint_effect_refinements']),20)
 for idx,(c,seed) in enumerate((c,s) for c in range(10) for s in range(2)):
  k,om=CASES[c];ref=0 if c<5 else 5;fine=rows[1]['snapshots'][-1]['physical'];endpoint=res['endpoints'][idx]
  eq('endpoint identity',[endpoint['case'],endpoint['seed'],endpoint['k_Mpc_inverse'],endpoint['omega_over_old_Hunit']],[c,seed,k,om])
  vector('endpoint physical',endpoint['physical'],fine[c][seed],SEED*1e-8)
  paired=[[a-b for a,b in zip(row['snapshots'][-1]['physical'][c][seed],row['snapshots'][-1]['physical'][ref][seed])] for row in rows]
  vector('endpoint signed difference',endpoint['difference_from_mode_off'],paired[1],SEED*1e-8)
  er=res['endpoint_effect_refinements'][idx];eq('effect identity',[er['case'],er['seed']],[c,seed])
  dt=[a-b for a,b in zip(paired[0],paired[1])];ds=[a-b for a,b in zip(paired[2],paired[1])];margin=[3*max(abs(a),abs(b)) for a,b in zip(dt,ds)]
  for key,val in [('coarse_effect',paired[0]),('fine_effect',paired[1]),('spectral_effect',paired[2]),('time_change',dt),('spectral_change',ds),('three_change_margin',margin)]:vector('paired '+key,er[key],val,SEED*1e-8)
  eq('resolution labels',er['resolution'],['control_zero' if om==0 else ('resolved' if abs(v)>m else 'unresolved') for v,m in zip(paired[1],margin)])
  flag=res['physical_fixture_flags'][idx];eq('flag identity',[flag['case'],flag['seed']],[c,seed])
  amp=max(max(s['amplitudes'][c][seed]) for s in rows[1]['snapshots']);domain=max(s['clock_domain'][c][seed][3] for s in rows[1]['snapshots'])
  close('sampled amplitude',flag['maximum_amplitude'],amp);close('sampled domain',flag['maximum_clock_domain_fraction'],domain)
  eq('small flag',flag['small_perturbation'],amp<.01);eq('domain flag',flag['inside_clock_domain'],domain<1)
  ceiling=SEED/domain if domain>0 else None
  if ceiling is None:eq('no bound null',flag['sampled_maximum_basis_amplitude'],None)
  else:close('absolute basis ceiling',flag['sampled_maximum_basis_amplitude'],ceiling)
  eq('sampled scope',flag['scope'],'sampled at65 stored times, not an all-times certificate')
 report=(BASE/(P+'_REPORT.md')).read_text()
 ok('report gate count',f'Numerical gates: {sum(g["passed"] for g in gates)}/441 PASS.' in report)
 ok('report present H',f'Present H / old Hunit: {bg["h"]:.12g}.' in report)
 eq('twenty report rows',sum(x.startswith('| ') and not x.startswith('| k/') and not x.startswith('|---') for x in report.splitlines()),20)
 for row in res['endpoints']:
  line=f'| {row["k_Mpc_inverse"]} | {row["omega_over_old_Hunit"]} | {row["seed"]} | {row["physical"][0]:.12g} | {row["difference_from_mode_off"][0]:.12g} | {row["physical"][4]:.12g} |'
  ok('signed report row',line in report)
 eq('no parent failure artifacts',len(list(BASE.glob(P+'_FAILED_*'))),0)
 for n,h in AUTH.items():eq('final input seal '+n,sha(BASE/n),h)
 summary=dict(status='SAVED_ARITHMETIC_ACCEPTED',assertions=N,maximum_absolute_comparison_difference=MAX_ABS,
  source_sha256=sha(__file__),parent_result_sha256=PINS[P+'_RESULT.json'],parent_receipt_sha256=PINS[P+'_RECEIPT.json'],
  parent_passed=sum(g['passed'] for g in gates),parent_total=441,failed_parent_gates=[g for g in gates if not g['passed']],
  qualified_parent_forecast=res['all_numerical_gates_passed'],trials=3,case_basis_channels=20,snapshots_per_trial=65,
  checkpoint_pairs=40,journal_events=42,inputs=AUTH,scope='saved-only arithmetic; failed parent dispositions and sampled physical flags retained')
 out=BASE/(A+'.json');note=BASE/(A+'.md');receipt=BASE/(A+'_RECEIPT.json')
 for p in [out,note,receipt]:ok('exclusive '+p.name,not p.exists())
 summary['assertions']=N
 with out.open('x') as f:json.dump(summary,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
 out.chmod(0o444)
 with note.open('x') as f:f.write(f'# Same-T saved-only acceptance V001\n\nPASS {N:,} assertions. Parent gates remain {summary["parent_passed"]}/441; failed forecasts are unqualified.\n\nAll3 trials/20case-basis channels/65snapshots,40CPpairs/42events and signed gates/readouts/seeds/domains/effects match. No producer import, RHS, equation solve or evolution. Sampled physical flags and descriptive resolution labels are preserved.\n\nRaw audit: {sha(out)}.\n')
 note.chmod(0o444)
 with receipt.open('x') as f:json.dump(dict(audit_sha256=sha(out),report_sha256=sha(note),source_sha256=sha(__file__),assertions=N,inputs=AUTH),f,sort_keys=True,separators=(',',':'));f.write('\n')
 receipt.chmod(0o444)
 for n,h in AUTH.items():
  if sha(BASE/n)!=h:raise RuntimeError('Post-publication input changed '+n)
 print(json.dumps(dict(status=summary['status'],assertions=N,parent_passed=summary['parent_passed'],parent_total=441,audit_sha256=sha(out),receipt_sha256=sha(receipt))))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true')
 if not p.parse_args().execute:raise SystemExit('Root must explicitly authorize saved-only --execute')
 outputs=[BASE/(A+s) for s in ('.json','.md','_RECEIPT.json','_ERROR.json')]
 if any(x.exists() for x in outputs):raise SystemExit('Audit evidence already exists; no overwrite')
 try:main()
 except Exception as ex:
  ep=BASE/(A+'_ERROR.json')
  with ep.open('x') as f:json.dump(dict(error=repr(ex),assertions=N,pid=os.getpid(),source_sha256=sha(__file__)),f,sort_keys=True);f.write('\n')
  ep.chmod(0o444);raise
