"""Prospective saved thermal-bracket pair bounds; root alone launches --execute."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,bisect,hashlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
STEM='CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V003'
PROTOCOL_SHA='c9af8663b32739efb9dc3afadc665ffe856b25b69e9a41bdc04ddd57049a3940'
PINS={'constrained_u_clock_gradient_bbn_pair_v001.py': '58ace9542a18cf63a89fe446b4ea40fb834ff6961ceb91185c71ff4732e8a8d5', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001.md': 'f4315e97ef6d4a2585c5f6402a5aed9fa4ba9ad193877567498ed1d099a8c5ff', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RESULT.json': '64e55eefc0079b75994dc749f5e8853835cd3bc72a2566e9627f8b98851fdc36', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': 'e7a9cc7d8f3b59e3b9351a7a3253d5ad4e806a49340908b067600d71783d6685', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_REFINED_STDOUT.txt': 'd0ec0ef40b5202420b1f064bb42b5101eb6008936cfafe8ab69b2862ca44d225', 'constrained_u_clock_gradient_bbn_helium_recombination_pair_v002.py': '713d7ce75c43cea179f6c126424a1fe58b60739186b12089d083ded786c15601', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002.md': '7075a9557ec141c99843c744a135c070dc1a4c90b0be4e27a52cd5b62c7a5d6d', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RESULT.json': '8edf04b504f89b0e378823c2b5eda6547138361bb5ad13f6858bd0e34ce5be20', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': '867911256634977adc8a50cdcc9b3b2e2e7aabaed6435de25c8be80acb6253fd', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_HALF_OUTPUT.json': '1df474629eb706d1315f090de228059c59db3ad58c127be2b614c005dc471386', 'bbn_inputs_v001/primat_c_reference_v001/upstream/primat-c/src/plasma.c': 'ecf991cb5aeee8c9744c34a4c0924fb3509eeadf08e23120bb939665fddb539c', 'bbn_inputs_v001/primat_c_reference_v001/upstream/primat-c/src/constants.c': 'ea97c872858bb103a6479ce42cc60c7b61865ac3981dc3275917acb2618403f2', 'constrained_u_clock_gradient_early_transfer_v004.py': 'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07', 'CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V002.md': '2d66ca4ec9c35bcd67c29914d29a634c1968ed1c2e7e8ab5eb7ba99cdf5b1f47', 'constrained_u_early_pair_opacity_bound_v001.py': '5541534b0a990c856cd12fa650577281267c630308373fb7b9dd196e46ca7e5c', 'CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V001.md': 'eaeea50fa7734bee06e7ae9edd6b7d64eba1ba38356fa2a8dc53d0b8346654dc', 'constrained_u_early_pair_opacity_bound_v002.py': '357bd29fb793e8174cb7fd06e030d45901ef851a06f39e59a3683b1ba292c05f', 'CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V002.md': 'dafbd7a49a3fa3bb73ca2eccfe8d53398abf605e04d4a157d18f1e423cce1fd9'}
BBN='CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001'
AT='CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002'
STARTS=(('PRIMARY',3e-8),('START',2e-8))
COLS=['t_s','Tgamma_MeV','a','H_s_inv','Tnue_MeV','Tnumu_MeV','Tnutau_MeV','rhoB_g_cm3','Gamma_np_s_inv','Gamma_pn_s_inv','thermal_H_s_inv','clock_H2_s_inv2','baryon_H2_s_inv2','native_charge_error']
INPUTS={};CREATED={};PREFIX=[]
PI='3.141592653589793238462643383279502884197169399375105820974944592307816406286'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def read(name):return json.loads((BASE/name).read_text())
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,x):
 p=BASE/name;data=canonical(x) if not isinstance(x,bytes) else x
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);CREATED[str(p.resolve())]=sha(p);return CREATED[str(p.resolve())]
def seal(p,h):
 p=Path(p).resolve()
 if not p.is_relative_to(ROOT.resolve()) and p!=Path('/usr/bin/clang').resolve():raise AssertionError('Input escapes declared project/compiler')
 if sha(p)!=h or (str(p) in INPUTS and INPUTS[str(p)]!=h):raise AssertionError('Changed/conflicting input '+str(p))
 INPUTS[str(p)]=h
def recheck(source):
 for p,h in dict(INPUTS,**CREATED).items():
  if sha(p)!=h:raise AssertionError('Sealed file changed '+p)
 if sha(__file__)!=source:raise AssertionError('Source changed')
def journal(event,**kw):
 p=BASE/(STEM+'_JOURNAL.jsonl')
 with p.open('a') as f:f.write(canonical(dict(event=event,time=now(),**kw)).decode())

def parents():
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
 bundles=[]
 for stem,expected,ng in ((BBN,'FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED',39),(AT,'NEW_ATOMIC_PAIR_ARITHMETIC_PASS',12)):
  result=read(stem+'_RESULT.json');rec=read(stem+'_RECEIPT.json');lin=result['lineage']
  old_inputs=rec['inputs'] if stem==BBN else rec['lineage']['input_sha256']
  if (result['status']!=expected or rec['status']!=expected or len(result['numerical_gates'])!=ng
      or not all(g['passed'] for g in result['numerical_gates']) or rec['result_sha256']!=PINS[stem+'_RESULT.json']
      or (rec['source_sha256'] if stem==BBN else rec['lineage']['source_sha256'])!=lin['source_sha256']
      or (lin['inputs'] if stem==BBN else lin['input_sha256'])!=old_inputs):raise AssertionError('Accepted parent disposition/lineage')
  for p,h in old_inputs.items():seal(p,h)
  for p,h in rec['output_sha256'].items():seal(p,h)
  for suffix,key in (('_MANIFEST.json','manifest_sha256'),('_JOURNAL.jsonl','journal_sha256')):seal(BASE/(stem+suffix),rec[key])
  events=[json.loads(t) for t in (BASE/(stem+'_JOURNAL.jsonl')).read_text().splitlines()]
  labels=('BUILD','DEFAULT','REFINED') if stem==BBN else ('DEFAULT','HALF')
  if ([e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*len(labels)+['OWNER_COMPLETE']
      or events[0]['owner']!='root' or events[0]['pid']<=0 or events[0]['source_sha256']!=lin['source_sha256']
      or events[-1]['status']!=expected or events[-1]['result_sha256']!=PINS[stem+'_RESULT.json']):raise AssertionError('Natural root parent closure')
  for label,event in zip(labels,events[1:-1]):
   pn=stem+'_'+label+'_CP.json';cn=stem+'_'+label+'_CP_COMMIT.json';co=read(cn)
   expected_co=(dict(stage=label,lineage=lin,payload=pn,sha256=sha(BASE/pn)) if stem==BBN
                else dict(arm=label,lineage=lin,checkpoint=pn,sha256=sha(BASE/pn)))
   if co!=expected_co or event['commit_sha256']!=sha(BASE/cn) or event.get('stage',event.get('arm'))!=label:raise AssertionError('Exact parent committed prefix')
   seal(BASE/pn,co['sha256']);seal(BASE/cn,event['commit_sha256'])
  if read(stem+'_MANIFEST.json')!=lin:raise AssertionError('Parent manifest binding')
  bundles.append((result,rec))
 raw=read(BBN+'_REFINED_STDOUT.txt');atomic=read(AT+'_HALF_OUTPUT.json')
 if (raw['profile']!='refined' or raw['status']!='COMPLETE_FIXED_NEVO_SCREEN'
     or raw['final']!=bundles[0][0]['finals']['REFINED']['final']
     or atomic['YHe_atomic']!=raw['final']['YPCMB'] or atomic['status']!='COMPLETE_ATOMIC_HISTORY_ONLY'
     or atomic['MODEL']!=3 or not atomic['zero_injection']):raise AssertionError('Authoritative actual BBN/atomic wrapper')
 ordinary=bundles[1][0]['lineage']['ordinary'];fixed=bundles[0][0]['lineage']['fixed']
 if (atomic['omega_b']!=ordinary['omega_b'] or atomic['T0_K']!=ordinary['T0']
     or atomic['YHe_atomic']!=ordinary['YHe'] or atomic['Hcal_km_s_Mpc']!=ordinary['Hstar']
     or ordinary['Hstar']!=fixed['Hstar'] or fixed['Gbare_over_GN']!=.99):raise AssertionError('Same physical charge/source inventory')
 rows=raw['background']
 if raw['background_columns']!=COLS or len(rows)!=2761:raise AssertionError('Frozen complete BBN background schema/census')
 for i,r in enumerate(rows):
  if len(r)!=14 or any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in r[:8]+r[10:]) or min(r[:8])<=0:raise AssertionError('BBN background row')
  if i and not (r[0]>rows[i-1][0] and r[2]>rows[i-1][2] and r[1]<rows[i-1][1]):raise AssertionError('BBN monotonic thermal ordering')
 if min(atomic['nH0_cm3'],atomic['fHe'])<=0:raise AssertionError('Positive physical ion inventory')
 return rows,atomic,fixed,[b[0]['numerical_gates'] for b in bundles]

def majorants(T):
 with localcontext() as ctx:
  ctx.prec=60;pi=Decimal(PI);m=Decimal('0.51099895')*Decimal('1.602176634e-13')
  hb=Decimal('6.62607015e-34')/(2*pi);c=Decimal('299792458');A=2*(-m/T).exp()/(pi*pi*(hb*c)**3)
  N=A*(m*m*T+2*m*T*T+2*T**3)
  R=A*(m**3*T+3*m*m*T*T+6*m*T**3+6*T**4)
  D=A*(m**4+4*m**3*T+12*m*m*T*T+24*m*T**3+24*T**4)
  return dict(N=N,R=R,D=D,p=R/3,W=4*R/3,Dp=D/3,DW=4*D/3,DN=R/T,m=m,hbar=hb,c=c,pi=pi)

def calculation(label,a,rows,atomic,fixed):
 pos=bisect.bisect_left([r[2] for r in rows],a)
 if not 0<pos<len(rows):raise AssertionError('Start outside actual thermal table')
 left,right=rows[pos-1],rows[pos]
 if not left[2]<=a<=right[2]:raise AssertionError('Immediate actual adjacent bracket')
 with localcontext() as ctx:
  ctx.prec=60;dec=lambda x:Decimal(str(x));aj=dec(a);MeV=Decimal('1.602176634e-13')
  T=dec(left[1])*MeV;Tlow=dec(right[1])*MeV;M=majorants(T);pi,hb,c=M['pi'],M['hbar'],M['c']
  nu=[min(dec(left[i]),dec(right[i]))*MeV for i in (4,5,6)]
  rad=(pi*pi*Tlow**4/15+7*pi*pi*sum(t**4 for t in nu)/120)/(hb*c)**3
  nH=dec(atomic['nH0_cm3'])*Decimal('1e6')/aj**3;fHe=dec(atomic['fHe']);nch=nH*(1+2*fHe)
  sig=Decimal('6.6524587321e-29');mpc=Decimal('3.0856775814913673e22');hs=dec(fixed['Hstar'])*1000/mpc
  GP=c*sig*M['N'];GB=c*sig*nch
  ratios=dict(number_to_charge=M['N']/nch,energy_to_radiation=M['R']/rad,enthalpy_to_radiation=M['W']/rad,
              pressure_to_radiation=M['p']/rad,fixed_zeta_energy_derivative_to_radiation=M['D']/rad,
              fixed_zeta_enthalpy_derivative_to_radiation=M['DW']/rad)
  limits={k:Decimal('1e-6') if k=='number_to_charge' else Decimal('1e-8') for k in ratios}
  flags=[dict(name=label+'_'+k,value=str(v),ceiling=str(limits[k]),passed=bool(v<=limits[k]),
              scope='fixed_zeta_only' if 'derivative' in k else 'neutral_EOS_pair_or_charge_number_envelope') for k,v in ratios.items()]
  majorant_strings={k:str(v) for k,v in M.items()};display={k:math.nextafter(float(v),math.inf) for k,v in M.items()}
  r=float(M['m']/T);Tf=float(T);hbf=float(hb);cf=float(c);pif=float(pi)
  fac=2*math.exp(-r)/(pif*pif*(hbf*cf)**3)
  independent=(fac*Tf**3*(r*r+2*r+2),fac*Tf**4*(r**3+3*r*r+6*r+6),fac*Tf**4*(r**4+4*r**3+12*r*r+24*r+24),float(GP)/float(GB))
  reference=(float(M['N']),float(M['R']),float(M['D']),float(ratios['number_to_charge']))
  controls=[dict(name=label+'_'+name,error=abs(x/y-1),tolerance=2e-13,passed=bool(math.isfinite(x) and abs(x/y-1)<=2e-13))
            for name,x,y in zip(('number_dimensionless','energy_dimensionless','derivative_dimensionless','opacity_number_fraction'),independent,reference)]
  return dict(label=label,a=a,bracket=dict(left_index=pos-1,right_index=pos,left=left,right=right),
      thermal_energy_inputs_strings=dict(T_upper_J=str(T),T_lower_J=str(Tlow),Tnu_lower_J=list(map(str,nu))),
      neutral_pair_majorant_decimal=majorant_strings,positive_display_float=display,
      radiation_lower_J_m3=str(rad),charge_inventory=dict(nH_m3=str(nH),ncharge_m3=str(nch),nH0_cm3=atomic['nH0_cm3'],fHe=atomic['fHe'],YHe=atomic['YHe_atomic']),
      opacity=dict(pair_proper_s_inv=str(GP),baryon_proper_s_inv=str(GB),pair_tau_inv=str(GP/hs),
                   baryon_tau_inv=str(GB/hs),pair_conformal_Mpc_inv=str(aj*sig*M['N']*mpc),Hstar_SI=str(hs)),
      ratios_decimal={k:str(v) for k,v in ratios.items()},fixed_zeta_number_derivative_to_charge=str(M['DN']/nch),
      plasma_C_zero_energy_cutoff=dict(T_me_over_30_MeV=str(Decimal('0.51099895')/30),left_zero=bool(dec(left[1])<Decimal('0.51099895')/30),right_zero=bool(dec(right[1])<Decimal('0.51099895')/30)),
      approximation_flags=flags,numerical_controls=controls,
      full_logarithmic_opacity_derivative=dict(status='NOT_QUALIFIED',prospective_ceiling=1e-4,reason='Varying neutrality/composition chemical contact not supplied'))

def main():
 begin=time.monotonic();source=sha(__file__)
 runtime=[p for p in BASE.glob(STEM+'_*') if p.suffix not in ('.py',)]
 if runtime:raise FileExistsError('Existing exclusive runtime prefix retained')
 if Path.cwd().resolve()!=ROOT.resolve():raise AssertionError('Exact project cwd')
 rows,atomic,fixed,oldgates=parents();lineage=dict(source_sha256=source,inputs=dict(INPUTS),starts=list(STARTS),fixed=fixed,
       atomic_header={k:atomic[k] for k in ('omega_b','T0_K','YHe_atomic','Hcal_km_s_Mpc','nH0_cm3','fHe')})
 write(STEM+'_MANIFEST.json',lineage);journal('OWNER_START',owner='root',pid=os.getpid(),source_sha256=source)
 for index,(label,a) in enumerate(STARTS):
  recheck(source);row=calculation(label,a,rows,atomic,fixed);PREFIX.append(row)
  cpname=STEM+'_'+label+'_CP.json';cn=STEM+'_'+label+'_CP_COMMIT.json'
  ch=write(cpname,dict(index=index,label=label,lineage=lineage,row=row));cmh=write(cn,dict(index=index,label=label,lineage=lineage,payload=cpname,sha256=ch))
  journal('CHECKPOINT',owner='root',pid=os.getpid(),index=index,label=label,commit_sha256=cmh,source_sha256=source)
 controls=[g for r in PREFIX for g in r['numerical_controls']];flags=[g for r in PREFIX for g in r['approximation_flags']]
 if len(PREFIX)!=2 or len(controls)!=8 or len(flags)!=12:raise AssertionError('Frozen output census')
 numeric=all(g['passed'] for g in controls);fixture=all(g['passed'] for g in flags)
 result=dict(status='PAIR_BOUND_ARITHMETIC_PASS' if numeric else 'PAIR_BOUND_ARITHMETIC_FAIL',lineage=lineage,
       rows=PREFIX,numerical_controls=controls,approximation_flags=flags,all_numerical_passed=numeric,
       all_conditional_fixture_flags_passed=fixture,inherited_dispositions=dict(BBN=oldgates[0],atomic=oldgates[1]),
       scope='Saved thermal brackets; neutral paired EOS and fixed-zeta derivatives only; full log-opacity, charged thermal contacts and propagated transfer error unqualified',elapsed_seconds=time.monotonic()-begin)
 recheck(source);rh=write(STEM+'_RESULT.json',result)
 lines=['# Early pair/start bound V003','',result['status']+'; numerical controls8; separate approximation flags12.',
        '','No new thermal solution; actual adjacent saved temperature brackets; full neutrality/composition derivative and propagated error remain unqualified.','',
        '| Start | a | T upper (MeV) | pair/charge upper | pair-energy/radiation upper | flags passed |','|---|---:|---:|---:|---:|---:|']
 for r in PREFIX:lines.append('| '+r['label']+' | '+str(r['a'])+' | '+str(r['bracket']['left'][1])+' | '+r['ratios_decimal']['number_to_charge']+' | '+r['ratios_decimal']['energy_to_radiation']+' | '+str(sum(g['passed'] for g in r['approximation_flags']))+'/6 |')
 report=write(STEM+'_REPORT.md',('\n'.join(lines)+'\n').encode());recheck(source)
 journal('OWNER_COMPLETE',owner='root',pid=os.getpid(),source_sha256=source,result_sha256=rh,status=result['status'],numerical_count=8,fixture_count=12)
 jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp.resolve())]=sha(jp)
 receipt=dict(status=result['status'],source_sha256=source,inputs=dict(INPUTS),output_sha256=dict(CREATED),result_sha256=rh,report_sha256=report,
              manifest_sha256=sha(BASE/(STEM+'_MANIFEST.json')),journal_sha256=sha(jp))
 write(STEM+'_RECEIPT.json',receipt);recheck(source)
 print(json.dumps(dict(status=result['status'],numerical_count=8,fixture_count=12,conditional_fixture_all_pass=fixture,elapsed_seconds=result['elapsed_seconds'])))
 return 0 if numeric else 3

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
 if not args.execute:raise SystemExit('Root-owned prospective readout: --execute required')
 existing=[p for p in BASE.glob(STEM+'_*') if p.suffix!='.py']
 if existing:raise SystemExit('Existing exclusive runtime retained; no new error or overwrite')
 try:raise SystemExit(main())
 except Exception as e:
  name=STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json'
  write(name,dict(error=type(e).__name__,message=str(e),traceback=traceback.format_exc(),completed_prefix=PREFIX,inputs=dict(INPUTS),created=dict(CREATED)))
  raise
