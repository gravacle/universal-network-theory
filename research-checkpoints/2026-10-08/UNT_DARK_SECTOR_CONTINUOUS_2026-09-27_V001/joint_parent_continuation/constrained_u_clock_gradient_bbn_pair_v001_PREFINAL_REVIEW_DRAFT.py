"""NEW exact same-source .99 GN fixed-NEVO BBN pair. Root alone builds/runs."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,subprocess,time
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
LIB=BASE/'bbn_inputs_v001/primat_c_reference_v001'
OLD=LIB/'build_ordinary_v001'
STEM='CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001'
PINS={'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'constrained_u_clock_gradient_flrw_reduced_chart_v002.py': '6d9878bb854bc7147aefcdcd358c6cecd16087a9577960f10686f5c4d17094b9', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md': '5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b', 'NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md': 'b2158042a2ce0867f5984e72cdea06b536975e1817fa48a9198272c0d394fffc', 'invariant_clock_joint_cal_bbn_v002.c': '8a3355dd3708326261fe70c1f31bf894fd5268c39585d6c15bb079e4a1aeaf69', 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_BBN_042.json': '9b3d2781edb486a00387b4128436a1add01b13223b1fa8ec48b1c43c07aec57e', 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_BBN_043.json': '753b5f991f8aa1e9abe6ba9cf9c77a1e50774627da1346a9bc4fd261d8943483', 'constrained_u_clock_gradient_bbn_background_v001.c': '3646527e018cade5e60bfbd95567fb90ce234b879d8e372c4ebc583b8e01c9e8', 'constrained_u_clock_gradient_bbn_adapter_v001.c': '942cacd10d3590cff194aa5d7c0a95f4efd780e428b402dac44a144a451b5f7c', 'bbn_inputs_v001/primat_c_reference_v001/upstream/primat-c/src/background.c': 'd692a9c810d65b2711ebe7aa246c317c0284428305463c0534bf742b8f675064', 'bbn_inputs_v001/primat_c_reference_v001/build_ordinary_v001/PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json': '1ef54049931289f2c8715d56f080566e1aecb01e483aada8681fe7b985d7ed00', 'bbn_inputs_v001/primat_c_reference_v001/build_ordinary_v001/PRIMAT_ORDINARY_BUILD_V001.json': '6a9ef5f2be2cad88e643444c5ec3628815ca2bc351ab9a86028c7df1aa940e74'}
PROTOCOL_SHA='0b92a79d4323b90f1135bf6d4c52e10b7d2ab68c8fc9aa96ad81ccc0152e4706'
COMPILER='/usr/bin/clang'
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
ARMS=('DEFAULT','REFINED')
STAGES=('BUILD',)+ARMS
CREATED={};INPUTS={}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,data):
 p=BASE/name
 with p.open('xb') as f:f.write(data if isinstance(data,bytes) else canonical(data))
 p.chmod(0o444);CREATED[str(p.resolve())]=sha(p);return CREATED[str(p.resolve())]
def journal(event,**kw):
 with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(json.dumps(dict(event=event,time=now(),**kw),sort_keys=True)+'\n')
def authenticate_file(path,h):
 p=Path(path).resolve()
 if p!=Path(COMPILER).resolve() and not p.is_relative_to(ROOT.resolve()):raise AssertionError('Input escapes project')
 if sha(p)!=h:raise AssertionError('Input changed '+str(p))
 if str(p) in INPUTS and INPUTS[str(p)]!=h:raise AssertionError('Conflicting input seal')
 INPUTS[str(p)]=h

def authenticate():
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():authenticate_file(BASE/n,h)
 authenticate_file(COMPILER,COMPILER_SHA)
 cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
 for p,h in cal['hashes'].items():authenticate_file(p,h)
 frozen=json.loads((OLD/'PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json').read_text())
 for p,h in frozen['files'].items():authenticate_file(ROOT/p,h)
 build=json.loads((OLD/'PRIMAT_ORDINARY_BUILD_V001.json').read_text())['payload'];objects=[]
 for item in build['commands']:
  authenticate_file(item['path'],item['sha256']);r=json.loads(Path(item['path']).read_text())['payload']
  authenticate_file(r['output']['path'],r['output']['sha256'])
  if r['command']['kind']=='compile' and r['command']['id'] not in ('adapter','background'):objects.append(r['output']['path'])
 if len(objects)!=21 or len(set(objects))!=21:raise AssertionError('Twenty-one unchanged object census')
 selected,old=cal['selected'],cal['fixed']
 actual=dict(Hstar=selected['Hunit'],physical_omega_b=selected['physical_omega_b'],OA=old['omega_A'],d0=old['d0'],eps=old['eps'],T0=selected['BBN_library_physical']['T0_K'],tau_n=selected['BBN_library_physical']['tau_n_s'],eta=selected['eta0b'],Neff=selected['Neff'],YHe_held=selected['YHe'],Gbare_over_GN=.99,GN=6.6743e-11,Mpc_m=3.0856775814913673e22)
 expected=dict(Hstar=67.49711988577813,physical_omega_b=.02166002225093379,OA=.7,d0=.35857141419482286,eps=1e-6,T0=2.72548,tau_n=878.4,Neff=3.0439772985579183)
 if any(actual[k]!=v for k,v in expected.items()):raise AssertionError('Fixed physical inventory mismatch')
 return cal,objects,actual

def recheck(source):
 for p,h in dict(INPUTS,**CREATED).items():
  if sha(p)!=h:raise AssertionError('Sealed file changed '+p)
 if sha(__file__)!=source:raise AssertionError('Source changed')

def run_command(label,argv,source):
 recheck(source);start=time.monotonic()
 proc=subprocess.run(list(map(str,argv)),cwd=ROOT,capture_output=True,check=False)
 names={k:STEM+'_'+label+'_'+suffix for k,suffix in [('stdout','STDOUT.txt'),('stderr','STDERR.txt'),('receipt','COMMAND.json')]}
 for k in ('stdout','stderr'):write(names[k],getattr(proc,k))
 rec=dict(argv=list(map(str,argv)),returncode=proc.returncode,elapsed_seconds=time.monotonic()-start,
          stdout=dict(name=names['stdout'],sha256=sha(BASE/names['stdout'])),stderr=dict(name=names['stderr'],sha256=sha(BASE/names['stderr'])))
 write(names['receipt'],rec);recheck(source);return rec

def source_checks(data,arm,fixed):
 if data['schema']!=STEM or data['profile']!=arm.lower() or data['status'] not in ('COMPLETE_FIXED_NEVO_SCREEN','FAILED_CONTROLS'):raise AssertionError('C result schema')
 if data['species']!=['n','p','d','t','He3','a','Li7','Be7'] or data['mass_numbers']!=[1,1,2,3,3,4,7,7]:raise AssertionError('Species census')
 if data['numerical']!=dict(nuclear_rtol=1e-7 if arm=='DEFAULT' else 1e-8,LT_rtol_multiplier=10,rate_grid_npts=1000,temperature_samples_per_decade=600,new_tables_generated=False):raise AssertionError('Fixed numerical ABI')
 if len(data['HT_relaxation'])!=2049 or len(data['background'])<2 or not data['nuclear_history']:raise AssertionError('Full history census')
 gates=[]
 def check(name,e,t):gates.append(dict(name=arm+'_'+name,error=float(e),tolerance=t,passed=math.isfinite(e) and e<=t))
 check('internal_controls',data['controls']['failures'],0)
 p=data['physical'];f=data['final']
 for name,got,want in [('GN',p['GN_SI'],.99*fixed['GN']),('omega_b',p['omega_b'],.99*fixed['physical_omega_b']),('T0',p['T0_K'],fixed['T0']),('tau_n',p['tau_n_s'],fixed['tau_n']),('eta',p['eta0b'],fixed['eta']),('Neff',f['Neff'],fixed['Neff'])]:check(name,abs(got/want-1),2e-12)
 charge=[];hs=[];hc=[];hb=[]
 norm=1/fixed['eps']-math.log1p(1/fixed['eps']);hstar=fixed['Hstar']*1000/fixed['Mpc_m'];h100=100000/fixed['Mpc_m']
 for i,row in enumerate(data['background']):
  if len(row)!=14 or any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in row[:8]+row[10:]):raise AssertionError('Background row schema')
  t,T,a,H=row[:4]
  if min(t,T,a,H,*row[4:8],*row[10:13])<=0:raise AssertionError('Background sign')
  if i and not (t>data['background'][i-1][0] and T<data['background'][i-1][1] and a>data['background'][i-1][2]):raise AssertionError('Background order')
  if T>10:
   if row[8:10]!=[None,None]:raise AssertionError('High-T weak null')
  elif any(not isinstance(x,(int,float)) or not math.isfinite(x) or x<0 for x in row[8:10]):raise AssertionError('Weak rate sign')
  d=fixed['d0']/a**3;s=.5*fixed['eps']*norm*d
  for _ in range(5):
   qb=math.sqrt(1+fixed['eps']*s/(1+s));dq=fixed['eps']/(2*qb*(1+s)**2);s-=(s*qb-.5*fixed['eps']*norm*d)/(qb+s*dq)
  qb=math.sqrt(1+fixed['eps']*s/(1+s));pex=(math.log1p(s)-s/(1+s))/norm
  clock=hstar*hstar*fixed['OA']/(.98/.99)*(1+qb*d-pex);bar=.99*fixed['physical_omega_b']*h100*h100/a**3
  charge.append(abs(2*qb*s/(fixed['eps']*norm)/d-1));hs.append(abs(H*H/(row[10]**2+row[11]+row[12])-1));hc.append(abs(row[11]/clock-1));hb.append(abs(row[12]/bar-1))
 check('full_charge',max(charge),5e-13);check('full_H_source',max(hs),2e-12);check('clock_source',max(hc),2e-12);check('baryon_source',max(hb),2e-12)
 miny=math.inf;mass=[]
 for i,row in enumerate(data['nuclear_history']):
  if len(row)!=12 or any(not math.isfinite(x) for x in row) or min(row[:3])<=0:raise AssertionError('Nuclear history row')
  if i and row[0]<data['nuclear_history'][i-1][0]:raise AssertionError('Nuclear time order')
  ys=row[4:];miny=min(miny,*ys);mass.append(abs(sum(a*y for a,y in zip(data['mass_numbers'],ys))-1))
 check('baryon_sum',max(mass),1e-8);check('negative_abundance',max(0.,-miny),1e-12)
 if len(gates)!=13:raise AssertionError('Frozen arm gate census')
 return gates

def main():
 begin=time.monotonic();source=sha(__file__)
 if Path.cwd().resolve()!=ROOT.resolve() or os.environ.get('CPR_NN_DEBUG'):raise AssertionError('Exact root cwd/debug prohibition')
 if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')):raise FileExistsError('Completed artifacts retained')
 cal,objects,fixed=authenticate();lineage=dict(source_sha256=source,inputs=dict(INPUTS),fixed=fixed,stages=list(STAGES))
 mp=BASE/(STEM+'_MANIFEST.json')
 if mp.exists():
  if json.loads(mp.read_text())!=lineage:raise AssertionError('Manifest lineage')
  CREATED[str(mp.resolve())]=sha(mp)
 else:write(mp.name,lineage)
 jp=BASE/(STEM+'_JOURNAL.jsonl');events=[json.loads(x) for x in jp.read_text().splitlines()] if jp.exists() else []
 if any(e['event'] not in ('OWNER_START','CHECKPOINT') or e.get('source_sha256')!=source for e in events):raise AssertionError('Journal schema/source')
 committed=[e for e in events if e['event']=='CHECKPOINT']
 if [e['stage'] for e in committed]!=list(STAGES[:len(committed)]) or len(committed)>3:raise AssertionError('Committed stage order')
 journal('OWNER_START',pid=os.getpid(),owner='root',source_sha256=source)
 objbg=BASE/(STEM+'_background.o');objad=BASE/(STEM+'_adapter.o');exe=BASE/(STEM+'_binary');results=[];stages=[];gates=[]
 for index,stage in enumerate(STAGES):
  cpname=STEM+'_'+stage+'_CP.json';cmname=STEM+'_'+stage+'_CP_COMMIT.json'
  if index<len(committed):
   e=committed[index];cp=json.loads((BASE/cpname).read_text());commit=json.loads((BASE/cmname).read_text())
   if sha(BASE/cmname)!=e['commit_sha256'] or commit!=dict(stage=stage,lineage=lineage,payload=cpname,sha256=sha(BASE/cpname)) or cp['stage']!=stage:raise AssertionError('Checkpoint commit/source')
   for p,h in cp['files'].items():
    if sha(BASE/p)!=h:raise AssertionError('Checkpoint byte changed')
    CREATED[str((BASE/p).resolve())]=h
   CREATED[str((BASE/cpname).resolve())]=sha(BASE/cpname);CREATED[str((BASE/cmname).resolve())]=sha(BASE/cmname)
  else:
   reserved=(list(BASE.glob(STEM+'_'+stage+'_*')) if stage!='BUILD' else list(BASE.glob(STEM+'_BUILD_*'))+[x for x in (objbg,objad,exe) if x.exists()])
   if reserved:raise FileExistsError('Orphan stage prefix retained')
   before=set(CREATED);commands=[]
   if stage=='BUILD':
    inc='-I'+str(LIB/'upstream/primat-c/include')
    for role,target in [('background',objbg),('adapter',objad)]:
     rec=run_command('BUILD_'+role,[COMPILER,'-std=gnu11','-O2','-Wall','-Wextra','-pthread',inc,'-c',BASE/('constrained_u_clock_gradient_bbn_'+role+'_v001.c'),'-o',target],source)
     commands.append(rec)
     if rec['returncode'] or not target.exists():raise RuntimeError('New science source compile failed')
     target.chmod(0o444);CREATED[str(target.resolve())]=sha(target)
    rec=run_command('BUILD_link',[COMPILER,*objects,objbg,objad,'-lm','-pthread','-o',exe],source);commands.append(rec)
    if rec['returncode'] or not exe.exists():raise RuntimeError('New science binary link failed')
    exe.chmod(0o555);CREATED[str(exe.resolve())]=sha(exe)
   else:
    rec=run_command(stage,[exe,stage.lower()],source);commands.append(rec)
    if rec['returncode'] not in (0,2):raise RuntimeError('Nuclear stage failed; raw prefix retained')
   files={Path(p).name:h for p,h in CREATED.items() if p not in before}
   cp=dict(stage=stage,files=files,commands=commands)
   write(cpname,cp);ch=write(cmname,dict(stage=stage,lineage=lineage,payload=cpname,sha256=sha(BASE/cpname)))
   journal('CHECKPOINT',stage=stage,commit_sha256=ch,source_sha256=source)
  # No command is repeated when its complete sealed checkpoint is reused.
  if stage=='BUILD':
   if len(cp['commands'])!=3 or any(x['returncode'] for x in cp['commands']) or any(Path(x['argv'][0])!=Path(COMPILER) for x in cp['commands']):raise AssertionError('Build checkpoint schema')
  else:
   if len(cp['commands'])!=1 or cp['commands'][0]['argv']!=[str(exe),stage.lower()] or cp['commands'][0]['returncode'] not in (0,2):raise AssertionError('Arm checkpoint schema')
   rec=cp['commands'][0]
   if (BASE/rec['stderr']['name']).read_bytes():raise RuntimeError('Nuclear stderr retained, not qualified')
   data=json.loads((BASE/rec['stdout']['name']).read_text());gates.extend(source_checks(data,stage,fixed));results.append(data)
  recheck(source);stages.append(cp);print(json.dumps(dict(stage=stage,status='CHECKPOINT_COMPLETE')),flush=True)
 coarse,fine=results
 for k,t in [('DoH',5e-5),('YPBBN',1e-5),('YPCMB',1e-5)]:
  e=abs(coarse['final'][k]/fine['final'][k]-1) if k=='DoH' else abs(coarse['final'][k]-fine['final'][k]);gates.append(dict(name=k+'_refinement',error=e,tolerance=t,passed=math.isfinite(e) and e<=t))
 if len(coarse['background'])!=len(fine['background']):raise AssertionError('Common background grid')
 for col in range(10):
  errors=[]
  for a,b in zip(coarse['background'],fine['background']):
   if a[col] is None or b[col] is None:
    if a[col]!=b[col]:raise AssertionError('Paired rate null')
   else:errors.append(abs(a[col]-b[col])/max(abs(b[col]),1e-30))
  e=max(errors);gates.append(dict(name='background_column_'+str(col)+'_refinement',error=e,tolerance=2e-12,passed=math.isfinite(e) and e<=2e-12))
 if len(gates)!=39:raise AssertionError('Frozen39-gate census')
 status='FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED' if all(x['passed'] for x in gates) else 'FIXED_NEVO_NEW_ACTION_ARITHMETIC_FAILED'
 result=dict(status=status,lineage=lineage,stages=stages,numerical_gates=gates,all_numerical_gates_passed=all(x['passed'] for x in gates),
   finals={arm:dict(physical=x['physical'],final=x['final'],controls=x['controls']) for arm,x in zip(ARMS,results)},
   signed_difference_from_old_selected={k:fine['final'][k]-v for k,v in cal['selected']['BBN'].items()},
   signed_new_YPCMB_minus_held_atomic_YHe=fine['final']['YPCMB']-fixed['YHe_held'],elapsed_seconds=time.monotonic()-begin,
   scope='Fixed-NEVO full frozen P(X)+baryon H source, no fit/rate uncertainty/new neutrino decoupling/native thermal origin/CMB inheritance')
 recheck(source);rs=write(STEM+'_RESULT.json',result)
 lines=['# NEW same-action fixed-NEVO BBN pair V001','',status+'; '+str(sum(x['passed'] for x in gates))+'/39 controls PASS.','',
  'Full P(X) absolute energy and physical baryon loading are included once at .99 GN. Ordinary plasma/NEVO/rates unchanged; both histories newly computed.',
  'No fit or rate/transport uncertainty qualification. The held atomic helium remains separate from this new yield.','', '| Quantity | DEFAULT | REFINED |','|---|---:|---:|']
 for k in fine['final']:lines.append('| '+k+' | '+format(coarse['final'][k],'.12g')+' | '+format(fine['final'][k],'.12g')+' |')
 lines+=['','| Gate | Error | Tolerance | PASS |','|---|---:|---:|---|']
 for x in gates:lines.append('| '+x['name']+' | '+format(x['error'],'.12g')+' | '+str(x['tolerance'])+' | '+str(x['passed'])+' |')
 rep=write(STEM+'_REPORT.md',('\n'.join(lines)+'\n').encode());recheck(source)
 journal('OWNER_COMPLETE',source_sha256=source,status=status,result_sha256=rs)
 write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=source,inputs=dict(INPUTS),result_sha256=rs,report_sha256=rep,manifest_sha256=sha(mp),journal_sha256=sha(jp),output_sha256=dict(CREATED)))
 print(json.dumps(dict(status=status,passed=sum(x['passed'] for x in gates),total=39,elapsed_seconds=result['elapsed_seconds'],result_sha256=rs)),flush=True)
 return 0 if result['all_numerical_gates_passed'] else 3

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
 if not ap.parse_args().execute:raise SystemExit('Root-owned --execute required; author does not compile/run')
 try:raise SystemExit(main())
 except Exception as e:
  stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
  write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(e),time=now(),pid=os.getpid(),source_sha256=sha(__file__)))
  raise
