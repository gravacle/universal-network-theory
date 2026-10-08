"""Guarded ONE fixed-EPS early chain. Author does not build, import or evaluate science."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, platform, subprocess, time

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
STEM='CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001'
GUARDED_UNEXECUTED=True
PROTOCOL_SHA='f511db085e290e3287902e20f9e0eb9cf2679febc4a9af01061f30f10068645b'
PINS={'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CROSS_U_RETARDED_RESPONSE_AND_BACKGROUND_EQUIVALENCE_V001.md': '78d369efb4efe4bab1f3885c2b11e37959e0860f449e839fa9d447da829ab9f6', 'constrained_u_clock_gradient_bbn_background_v001.c': '3646527e018cade5e60bfbd95567fb90ce234b879d8e372c4ebc583b8e01c9e8', 'cross_u_eps1e5_fixed_nevo_background_v001.c': '1e2244249aacff6cd01e48c8e1b9436afa678170f1616d6cfccbeea0caa9fefa', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_adapter.o': 'db5f6fe1deb8548d030f609b9b2621c29daa155eb356ea6d8bced80fc5930a1f', 'NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md': 'b2158042a2ce0867f5984e72cdea06b536975e1817fa48a9198272c0d394fffc', 'bbn_inputs_v001/primat_c_reference_v001/build_ordinary_v001/PRIMAT_ORDINARY_BUILD_V001.json': '6a9ef5f2be2cad88e643444c5ec3628815ca2bc351ab9a86028c7df1aa940e74', 'bbn_inputs_v001/primat_c_reference_v001/build_ordinary_v001/PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json': '1ef54049931289f2c8715d56f080566e1aecb01e483aada8681fe7b985d7ed00', 'hyrec_inputs_v001/HYREC_LOCAL_BUILD_V001.json': 'b92abea8bc12c963f531976fadecb751402c26625d49b9b8da7bc81d8ebcd63d', 'hyrec_inputs_v001/HYREC_SOURCE_RECEIPT_V001.json': 'd569777d0103c2db74d4af7e1841738a3bb8fc662efa4c7933ea190f2ad4a400', 'hyrec_inputs_v001/build_bin_v001/HYREC_LOCAL_BUILD_V001_FROZEN.json': '1e9689c9519e7517bbab34cf61d04f599bafd5ed9fb474703f47188c164f22a0', 'hyrec_inputs_v001/build_bin_v001/unt_hyrec_full_default': 'ec888d00b17885d04e5e03a4b48edd7f46026cf72d578ffc24f6731815036e96', 'hyrec_inputs_v001/build_bin_v001/unt_hyrec_full_half': 'e028586eb0fa77e4858972fc3a139c19eb593fa31c42f1ca0e20744271f1bdd4', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_DEFAULT_INPUT.txt': 'c0220b397f81d2bb39ffa337a9a6e7d571d6a992a83cbf046e0795c8920e744c', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_HALF_INPUT.txt': '4655b5424f2409fc75d693c8e28e65843b63671a4505f98d5d92a2383efeda59', 'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt': '9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585', 'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt': '252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509', 'desi_dr2_bao_external_v001/README.md': '5f21b88b1a6d6264174f7ecd2b1e0baf78a62c9feb467c5fe3865eb3ba9b70f6', 'constrained_u_clock_gradient_bbn_pair_v001.py': '58ace9542a18cf63a89fe446b4ea40fb834ff6961ceb91185c71ff4732e8a8d5', 'constrained_u_clock_gradient_bbn_helium_recombination_pair_v002.py': '713d7ce75c43cea179f6c126424a1fe58b60739186b12089d083ded786c15601', 'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py': '0440a959e2a662203b57f3da39afee973f41cc90fbe289520415f50f3da94f3b', 'constrained_u_clock_gradient_bbn_desi_bao_v002.py': '9016e6730ee4a243c8a90e5f98f63ba5159fec906b1f94f898f2eea3f44f9ac3', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001.md': 'f4315e97ef6d4a2585c5f6402a5aed9fa4ba9ad193877567498ed1d099a8c5ff', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RESULT.json': '64e55eefc0079b75994dc749f5e8853835cd3bc72a2566e9627f8b98851fdc36', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': 'e7a9cc7d8f3b59e3b9351a7a3253d5ad4e806a49340908b067600d71783d6685', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002.md': '7075a9557ec141c99843c744a135c070dc1a4c90b0be4e27a52cd5b62c7a5d6d', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RESULT.json': '8edf04b504f89b0e378823c2b5eda6547138361bb5ad13f6858bd0e34ce5be20', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': '867911256634977adc8a50cdcc9b3b2e2e7aabaed6435de25c8be80acb6253fd', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001.md': '74e0c0ce3be19e1cb115d47f21eefeaf122f3530b1d4bd6a3eae194c0960051f', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RESULT.json': '844d085f18ab85589793858d24fb4a3333741175c6a7d5b41792d83b331ee403', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': 'e0dab9c7d3e335001908ed10f43972b4f6b97658061490087720a3ffcb2d16d7', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002.md': 'ecb771122c94d8a9a36d2e9d6fc01983a4ffa26ff60d2d5364edbe55253b6b23', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002_RESULT.json': '12743287b22d4dc96ff21b9134f5d8d04db9081c41bd55bd6aabec1f6fdb4979', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002_RECEIPT.json': '9c489ec4ca988b95d067151639dda84aa7f3de689fafd7c44017a7f55e8e0644', 'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001.md': '9125291f442dfd3aebb63199de2c707e3f86ec3d02c236f87d606772f9a879ec', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6'}
HELPERS={'constrained_u_clock_gradient_bbn_pair_v001.py': {'source_checks': 'ca2e1a1b7645505cc623d1c37c0d51896034a0d2eca3d0b3ae5404e871f101e8'}, 'constrained_u_clock_gradient_bbn_helium_recombination_pair_v002.py': {'output_controls': 'dc82c8cc63210b0ec452afadf9df3d3127eb07ce5dc8904860279566deed176a'}, 'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py': {'background': 'eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2', 'quad': '306dd63a17bc3f5435116e94d75f12819672527e0b5957bc7e274314d5a61b24', 'Background': '9cb36538551ee8f9235750ea28ec45d7ddb7fac2b5bb2e0d84b2842009ec09ee', 'distances': '492860563c21bf249408a2691d3bc4e10fc08589b6919ca361f17daea6ab867b', 'observables': 'b46645a4c20395e519737646aecd0a96150298c5debd431ca34685c92627ef26'}, 'constrained_u_clock_gradient_bbn_desi_bao_v002.py': {'distance_vector': 'c4ac7bbe54994926e2953e77a528e214adbcad320c96aa38ef2b1250638dd6c3'}}
COMPILER='/usr/bin/clang'
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
LIB=BASE/'bbn_inputs_v001/primat_c_reference_v001'
OLD=LIB/'build_ordinary_v001'
ATOMIC=BASE/'hyrec_inputs_v001'
OLD_BBN='CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001'
OLD_ATOMIC='CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002'
OLD_ACOUSTIC='CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001'
OLD_BAO='CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002'
PARENTS=((OLD_BBN,'FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED',39),
 (OLD_ATOMIC,'NEW_ATOMIC_PAIR_ARITHMETIC_PASS',12),
 (OLD_ACOUSTIC,'NEW_BBN_ACOUSTIC_ARITHMETIC_PASS',22),
 (OLD_BAO,'NEW_BBN_PREDICTED_RULER_BAO_ARITHMETIC_PASS',5))
STAGES=('BUILD_BACKGROUND','BUILD_LINK','BBN_DEFAULT','BBN_REFINED','BBN_PAIR',
 'ATOMIC_DEFAULT','ATOMIC_HALF','ATOMIC_PAIR','ACOUSTIC_DEFAULT','ACOUSTIC_HALF',
 'ACOUSTIC_THIN','ACOUSTIC_QUADRATURE','ACOUSTIC_PAIR','DESI')
FIELDS=('zstar','rs_Mpc','DM_Mpc','theta100','drag_redshift_interval','drag_ruler_Mpc_interval')
ORDER=[(.295,'DV_over_rs'),(.510,'DM_over_rs'),(.510,'DH_over_rs'),(.706,'DM_over_rs'),
 (.706,'DH_over_rs'),(.934,'DM_over_rs'),(.934,'DH_over_rs'),(1.321,'DM_over_rs'),
 (1.321,'DH_over_rs'),(1.484,'DM_over_rs'),(1.484,'DH_over_rs'),(2.33,'DH_over_rs'),(2.33,'DM_over_rs')]
MPC=3.0856775814913673e22
CP=299792458.
SIGMA_T=6.6524587321e-29
FLAGS={k:False for k in ('physical_thermal_origin','new_neutrino_decoupling',
 'primordial_preparation','CMB_spectrum','perturbation_transfer','native_budget_closure',
 'global_EPS_adoption','ruler_fit','observational_superiority')}
INPUTS={};CREATED={};RAW={};PAIRS=[];DATA={}
RUN_SOURCE='';RUN_MANIFEST='';OWNER_PID=None;ACTIVE='AUTHENTICATION';np=None

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def plain(v):
 if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [plain(x) for x in v]
 if hasattr(v,'item'):return plain(v.item())
 if isinstance(v,Path):return str(v)
 if isinstance(v,float) and not math.isfinite(v):raise ValueError('Nonfinite JSON scalar')
 if v is None or type(v) in (str,int,float,bool):return v
 raise TypeError('Unsupported metadata '+str(type(v)))
def encoded(v):return (json.dumps(plain(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,v,raw=False):
 p=BASE/name;b=v if raw else encoded(v)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
 if p.read_bytes()!=b:raise AssertionError('Exclusive byte reread '+name)
 CREATED[str(p.resolve())]=sha(p);return CREATED[str(p.resolve())]
def track(p,mode=0o444):
 p=Path(p);p.chmod(mode);CREATED[str(p.resolve())]=sha(p);return CREATED[str(p.resolve())]
def seal(p,h):
 p=Path(p).resolve()
 if not (p.is_relative_to(ROOT.resolve()) or (p==Path(COMPILER).resolve() and h==COMPILER_SHA)):
  raise AssertionError('Input outside registered project '+str(p))
 if sha(p)!=h:raise AssertionError('Input byte seal '+str(p))
 if str(p) in INPUTS and INPUTS[str(p)]!=h:raise AssertionError('Conflicting input seal')
 INPUTS[str(p)]=h
def recheck():
 for p,h in dict(INPUTS,**CREATED).items():
  if sha(p)!=h:raise AssertionError('Changed immutable byte '+p)
 if sha(__file__)!=RUN_SOURCE:raise AssertionError('Changed own source')
def journal(event,**kw):
 row=dict(event=event,time=now(),owner='root',pid=os.getpid(),source_sha256=RUN_SOURCE,
  manifest_sha256=RUN_MANIFEST,**kw)
 with (BASE/(STEM+'_JOURNAL.jsonl')).open('ab') as f:f.write(encoded(row));f.flush();os.fsync(f.fileno())

def parent(st,status,count):
 rc=json.loads((BASE/(st+'_RECEIPT.json')).read_text());r=json.loads((BASE/(st+'_RESULT.json')).read_text())
 if rc['status']!=status or r['status']!=status or not r['all_numerical_gates_passed']:
  raise AssertionError('Accepted parent status '+st)
 if len(r['numerical_gates'])!=count or not all(g['passed'] for g in r['numerical_gates']):
  raise AssertionError('Parent original gate census '+st)
 source=rc.get('source_sha256',rc.get('lineage',{}).get('source_sha256'))
 manifest=json.loads((BASE/(st+'_MANIFEST.json')).read_text())
 if source!=manifest['source_sha256'] or rc['result_sha256']!=PINS[st+'_RESULT.json']:
  raise AssertionError('Parent source/result binding '+st)
 maps=rc.get('inputs',rc.get('lineage',rc.get('manifest',{})).get('input_sha256',{}))
 if not maps or not rc['output_sha256']:raise AssertionError('Complete parent maps '+st)
 for p,h in dict(maps,**rc['output_sha256']).items():seal(p,h)
 for suffix,key in (('_MANIFEST.json','manifest_sha256'),('_JOURNAL.jsonl','journal_sha256'),
                    ('_REPORT.md','report_sha256'),('_RESULT.json','result_sha256')):
  seal(BASE/(st+suffix),rc[key])
 ev=[json.loads(x) for x in (BASE/(st+'_JOURNAL.jsonl')).read_text().splitlines()]
 if ev[0]['event']!='OWNER_START' or ev[-1]['event']!='OWNER_COMPLETE' or ev[-1]['status']!=status:
  raise AssertionError('Parent natural closure '+st)
 if ev[-1].get('result_sha256')!=rc['result_sha256']:raise AssertionError('Parent final journal result')
 return r

def authenticate():
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
 seal(__file__,RUN_SOURCE);seal(COMPILER,COMPILER_SHA)
 parents={st:parent(st,status,count) for st,status,count in PARENTS}
 cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
 for p,h in cal['hashes'].items():seal(p,h)
 freeze=json.loads((OLD/'PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json').read_text())
 for p,h in freeze['files'].items():seal(ROOT/p,h)
 build=json.loads((OLD/'PRIMAT_ORDINARY_BUILD_V001.json').read_text())['payload'];objects=[]
 for item in build['commands']:
  seal(item['path'],item['sha256']);r=json.loads(Path(item['path']).read_text())['payload']
  seal(r['output']['path'],r['output']['sha256'])
  if r['command']['kind']=='compile' and r['command']['id'] not in ('adapter','background'):
   objects.append(r['output']['path'])
 if len(objects)!=21 or len(set(objects))!=21:raise AssertionError('Unchanged21 ordinary objects')
 old=(BASE/'constrained_u_clock_gradient_bbn_background_v001.c').read_bytes()
 new=(BASE/'cross_u_eps1e5_fixed_nevo_background_v001.c').read_bytes()
 if old.count(b'#define UNT_EPS 1e-6')!=1 or new!=old.replace(b'#define UNT_EPS 1e-6',b'#define UNT_EPS 1e-5'):
  raise AssertionError('Exactly one EPS macro change')
 selected,oldfix=cal['selected'],cal['fixed'];ctx=cal['trials'][-1]['atomic_invocation']['context']
 fixed=dict(Hunit=selected['Hunit'],OA=oldfix['omega_A'],OB=selected['OB'],OR=ctx['OR'],
  d0=oldfix['d0'],eps=1e-5,rG=.98/.99,Q0_over_Hstar=oldfix['Q0_over_H0'])
 expected=dict(Hunit=67.49711988577813,OA=.7,OB=.04659233656879551,OR=8.996751426107524e-5,
  d0=.35857141419482286,eps=1e-5,rG=.98/.99,Q0_over_Hstar=100.)
 if fixed!=expected or oldfix['eps']!=1e-6:raise AssertionError('Fixed inventory and only targetEPS change')
 ordinary=dict(omega_b=selected['physical_omega_b'],T0=ctx['T0'],Neff=selected['Neff'],Hstar=selected['Hunit'],
  YHe_old_fixture=selected['YHe'],helium_source='Own targetEPS refined BBN YPCMB; no fit')
 bfixed=dict(Hstar=fixed['Hunit'],physical_omega_b=ordinary['omega_b'],OA=fixed['OA'],d0=fixed['d0'],
  eps=fixed['eps'],T0=ordinary['T0'],tau_n=selected['BBN_library_physical']['tau_n_s'],eta=selected['eta0b'],
  Neff=ordinary['Neff'],YHe_held=selected['YHe'],Gbare_over_GN=.99,GN=6.6743e-11,Mpc_m=MPC)
 if (ordinary['omega_b']!=.02166002225093379 or ordinary['T0']!=2.72548 or
  ordinary['Neff']!=3.0439772985579183 or bfixed['tau_n']!=878.4):raise AssertionError('Fixed ordinary plasma')
 oldm=parents[OLD_ACOUSTIC]['manifest'];ledger=oldm['photon_baryon_ledger']
 shared='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001';sr=json.loads((BASE/(shared+'_RESULT.json')).read_text());sc=json.loads((BASE/(shared+'_RECEIPT.json')).read_text())
 if (sr['status']!='NUMERICAL_PASS' or sc['status']!=sr['status'] or sc['owner']!='root' or
  sc['result_sha256']!=PINS[shared+'_RESULT.json'] or sr['manifest']['source_sha256']!=sc['source_sha256'] or
  sc['source_sha256']!=PINS['constrained_u_shared_eps_ngc_pantheon_v001.py'] or sr['manifest']['fixed_parent']!={**fixed,'eps':1e-6}):
  raise AssertionError('Newest fourEPS common late normalization')
 if len(sr['controls'])!=31 or not all(g['passed'] for g in sr['controls']):raise AssertionError('SharedEPS original31 controls')
 for p,h in sr['manifest']['input_sha256'].items():seal(p if Path(p).is_absolute() else BASE/p,h)
 for p,h in sc['output_sha256'].items():seal(p if Path(p).is_absolute() else BASE/p,h)
 seal(BASE/(shared+'_MANIFEST.json'),sc['manifest_sha256'])
 shared_row=next(r for r in sr['rows'] if r['eps']==1e-5)
 if oldm['fixed']!={**fixed,'eps':1e-6} or ledger['Rb0']!=3*fixed['OB']/(4*ctx['og']):
  raise AssertionError('Photon/baryon once-only inherited normalization')
 hy=json.loads((ATOMIC/'HYREC_LOCAL_BUILD_V001.json').read_text());binaries={}
 frozen=ATOMIC/hy['freeze']['path'];seal(frozen,hy['freeze']['sha256'])
 for p,h in json.loads(frozen.read_text())['files'].items():seal(ROOT/p,h)
 for item in json.loads((ATOMIC/'HYREC_SOURCE_RECEIPT_V001.json').read_text())['files']:
  p=ATOMIC/'upstream'/item['name'];seal(p,item['sha256'])
  if p.stat().st_size!=item['bytes']:raise AssertionError('HYREC upstream length')
 for arm in ('default','half'):
  p=ATOMIC/hy['binaries'][arm]['path'];seal(p,hy['binaries'][arm]['sha256'])
  if p.read_bytes()[:16]!=bytes.fromhex('cffaedfe0c0000010000000002000000'):
   raise AssertionError('Existing MacARM64 executable header')
  if p.stat().st_mode&0o777!=0o755:raise AssertionError('Existing HYREC executable permission')
  binaries[arm.upper()]=str(p)
 if platform.system()!='Darwin' or platform.machine() not in ('arm64','aarch64'):
  raise RuntimeError('Only existing DarwinARM64 HYREC binaries admitted; no build/install')
 if 'CPR_NN_DEBUG' in os.environ:raise AssertionError('Nuclear debug override prohibited')
 return dict(fixed=fixed,ordinary=ordinary,bbn_fixed=bfixed,ledger=ledger,objects=objects,binaries=binaries,
  parent_dispositions={st:dict(status=r['status'],numerical_gates=r['numerical_gates']) for st,r in parents.items()},
  shared_late_reference=dict(result_sha256=sc['result_sha256'],background=shared_row['background'],H_today=shared_row['H_today'],
   controls=sr['controls'],prior_numerical_gates_copied=sr['prior_numerical_gates_copied'],physical_flags=sr['physical_flags'],
   ngc_ancestral_flags=sr['ngc_ancestral_flags'],EPS_selection_or_fit=False))

def load_helpers():
 ns=dict(math=math,np=np,MPC=MPC,CP=CP,SIGMA_T=SIGMA_T,FIELDS=FIELDS,ORDER=ORDER)
 for filename,names in HELPERS.items():
  text=(BASE/filename).read_text();tree=ast.parse(text);parts=[]
  for name,h in names.items():
   node=next(a for a in tree.body if isinstance(a,(ast.FunctionDef,ast.ClassDef)) and a.name==name)
   span=ast.get_source_segment(text,node)
   if hashlib.sha256(span.encode()).hexdigest()!=h:raise AssertionError('Pure literal helper '+name)
   parts.append(span)
  local=dict(ns)
  if filename=='constrained_u_clock_gradient_bbn_pair_v001.py':local['STEM']=OLD_BBN
  exec(compile('\n\n'.join(parts),filename+'::function_only','exec'),local)
  for name in names:ns[name]=local[name]
 return ns

def descriptor(a):
 a=np.asarray(a)
 if a.dtype.hasobject:raise TypeError('Object checkpoint array')
 return dict(shape=list(a.shape),dtype=a.dtype.str,finite=bool(np.all(np.isfinite(a))) if a.dtype.kind in 'fc' else True)
def checkpoint(case,arrays,data,gates,files):
 index=STAGES.index(case);arrays={k:np.asarray(v) for k,v in arrays.items()}
 meta=dict(schema=1,case=case,index=index,failed=False,source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,
  original_owner_pid=OWNER_PID,epoch_pid=os.getpid(),data=data,gates=gates,files=files,
  arrays={k:descriptor(a) for k,a in arrays.items()},physical_flags=FLAGS)
 text=encoded(meta);meta=json.loads(text);p=BASE/(STEM+'_'+case+'_CP.npz')
 with p.open('xb') as f:np.savez_compressed(f,__metadata__=np.array(text.decode()),**arrays);f.flush();os.fsync(f.fileno())
 track(p);co=dict(schema=1,case=case,index=index,payload=p.name,sha256=sha(p),metadata=meta,
  source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST)
 cn=STEM+'_'+case+'_COMMIT.json';write(cn,co);PAIRS.append(cn)
 loaded=read_pair(cn)
 for k,a in arrays.items():
  if loaded[1][k].dtype!=a.dtype or not np.array_equal(loaded[1][k],a,equal_nan=True):raise AssertionError('Whole NPZ immediate reread')
 journal('CHECKPOINT',case=case,index=index,commit=cn,commit_sha256=sha(BASE/cn))
 return meta
def read_pair(cn):
 co=json.loads((BASE/cn).read_text());meta=co['metadata'];case=meta['case'];index=STAGES.index(case)
 expected=dict(schema=1,case=case,index=index,payload=STEM+'_'+case+'_CP.npz',sha256=co['sha256'],metadata=meta,
  source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST)
 if co!=expected or set(meta)!=set(('schema','case','index','failed','source_sha256','manifest_sha256',
  'original_owner_pid','epoch_pid','data','gates','files','arrays','physical_flags')):
  raise AssertionError('Exact commit/metadata schema')
 if (meta['schema']!=1 or meta['failed'] is not False or meta['index']!=index or meta['physical_flags']!=FLAGS or
  meta['original_owner_pid']!=OWNER_PID or meta['source_sha256']!=RUN_SOURCE or meta['manifest_sha256']!=RUN_MANIFEST or
  type(meta['epoch_pid']) is not int or meta['epoch_pid']<=0):raise AssertionError('Pair lineage')
 p=BASE/co['payload']
 if sha(p)!=co['sha256']:raise AssertionError('Payload hash')
 with np.load(p,allow_pickle=False) as z:
  if set(z.files)!=set(meta['arrays'])|{'__metadata__'} or json.loads(str(z['__metadata__']))!=meta:
   raise AssertionError('Payload complete metadata/array set')
  arrays={k:z[k].copy() for k in meta['arrays']}
 for k,a in arrays.items():
  if descriptor(a)!=meta['arrays'][k]:raise AssertionError('Whole payload dtype/shape/finite')
 for fn,h in meta['files'].items():
  q=BASE/fn
  if sha(q)!=h:raise AssertionError('Case-owned operand '+fn)
  CREATED[str(q.resolve())]=h
 CREATED[str(p.resolve())]=co['sha256'];CREATED[str((BASE/cn).resolve())]=sha(BASE/cn)
 return meta,arrays

def lineage(resume,context):
 global RUN_MANIFEST,OWNER_PID
 mp=BASE/(STEM+'_MANIFEST.json');jp=BASE/(STEM+'_JOURNAL.jsonl')
 static=dict(schema=1,source_sha256=RUN_SOURCE,input_sha256=dict(INPUTS),context=context,stages=list(STAGES),
  physical_flags=FLAGS,platform=dict(system=platform.system(),machine=platform.machine()),method='One targetEPS; fixed rates/preparation/calibration')
 if resume:
  if not mp.exists() or not jp.exists():raise AssertionError('Explicit resume needs manifest+journal')
  m=json.loads(mp.read_text());OWNER_PID=m['owner_pid']
  if {k:v for k,v in m.items() if k!='owner_pid'}!=static or type(OWNER_PID)is not int or OWNER_PID<=0:
   raise AssertionError('Exact frozen resume inventory')
  CREATED[str(mp.resolve())]=sha(mp);RUN_MANIFEST=sha(mp)
  ev=[json.loads(s) for s in jp.read_text().splitlines()]
  if not ev or ev[0]['event']!='OWNER_START' or ev[0]['pid']!=OWNER_PID:raise AssertionError('Original root owner')
  current=None;commits=[]
  for e in ev:
   if (e['owner']!='root' or e['source_sha256']!=RUN_SOURCE or e['manifest_sha256']!=RUN_MANIFEST
    or type(e['pid'])is not int or e['pid']<=0):raise AssertionError('Journal lineage')
   if e['event']in ('OWNER_START','OWNER_RESUME'):current=e['pid']
   elif e['event']=='CHECKPOINT':
    if e['pid']!=current or e['index']!=len(commits) or e['case']!=STAGES[len(commits)]:raise AssertionError('Contiguous case history')
    if sha(BASE/e['commit'])!=e['commit_sha256']:raise AssertionError('Journal commit seal')
    meta,arrays=read_pair(e['commit'])
    if meta['epoch_pid']!=e['pid']:raise AssertionError('Case epoch')
    PAIRS.append(e['commit']);commits.append(e);DATA[e['case']]=(meta,arrays)
   else:raise AssertionError('Terminal/error journal cannot resume')
  registered={str(Path(p).resolve()) for p in CREATED}|{str(jp.resolve())}
  actual={str(p.resolve()) for p in BASE.glob(STEM+'_*') if p.is_file()}
  if actual!=registered:raise AssertionError('Uncommitted/orphan runtime files; no replay')
  journal('OWNER_RESUME',last_committed_case=STAGES[len(commits)-1] if commits else None)
 else:
  if list(BASE.glob(STEM+'_*')):raise FileExistsError('Unused runtime namespace required')
  OWNER_PID=os.getpid();m={**static,'owner_pid':OWNER_PID};RUN_MANIFEST=write(mp.name,m)
  journal('OWNER_START')

def run_command(case,argv,stdin=None,targets=(),allow_codes=(0,),stderr_empty=False):
 recheck();files={};start=time.monotonic();names={k:STEM+'_'+case+'_'+s for k,s in
  (('stdout','STDOUT.txt'),('stderr','STDERR.txt'),('command','COMMAND.json'))}
 for target in targets:
  if Path(target).exists():raise FileExistsError('No object/binary overwrite')
 if stdin is not None:write(STEM+'_'+case+'_INPUT.txt',stdin,True);files[STEM+'_'+case+'_INPUT.txt']=sha(BASE/(STEM+'_'+case+'_INPUT.txt'))
 RAW['command_intent']=dict(case=case,argv=list(map(str,argv)),targets=[str(p) for p in targets],stdin_sha256=hashlib.sha256(stdin).hexdigest() if stdin is not None else None)
 command_error=None;proc=None
 with (BASE/names['stdout']).open('xb') as out,(BASE/names['stderr']).open('xb') as err:
  try:proc=subprocess.run(list(map(str,argv)),input=stdin,stdout=out,stderr=err,cwd=ROOT,check=False)
  except Exception as exc:command_error=exc
  finally:out.flush();err.flush();os.fsync(out.fileno());os.fsync(err.fileno())
 for k in ('stdout','stderr'):files[names[k]]=track(BASE/names[k])
 for target in targets:
  if Path(target).exists():files[Path(target).name]=track(target,0o555 if str(target).endswith('_binary') else 0o444)
 rec=dict(case=case,argv=list(map(str,argv)),returncode=proc.returncode if proc is not None else None,launch_error=repr(command_error) if command_error is not None else None,elapsed_seconds=time.monotonic()-start,
  stdin_sha256=hashlib.sha256(stdin).hexdigest() if stdin is not None else None,files=dict(files))
 write(names['command'],rec);files[names['command']]=sha(BASE/names['command']);RAW['command']=rec
 if command_error is not None:raise command_error
 if proc.returncode not in allow_codes or (stderr_empty and (BASE/names['stderr']).read_bytes()):
  raise RuntimeError('Command refusal with complete raw outputs '+case)
 recheck();return rec,files

def capture_table(name,rows):
 # C/HYREC JSON nulls stay explicit in a separate mask; no nonfinite successful array.
 mask=np.array([[x is None for x in r] for r in rows],dtype=bool);RAW[name+'_null']=mask
 a=np.array([[0. if x is None else x for x in r] for r in rows],dtype=float);RAW[name]=a
 return {name:a,name+'_null':mask}
def gate(name,e,t):
 return dict(name=name,error=float(e),tolerance=t,passed=bool(math.isfinite(e) and e<=t))
def pair_bbn(a,b):
 gates=[];signed={}
 for k,t in (('DoH',5e-5),('YPBBN',1e-5),('YPCMB',1e-5)):
  signed[k]=a['final'][k]-b['final'][k];e=abs(a['final'][k]/b['final'][k]-1) if k=='DoH' else abs(signed[k])
  gates.append(gate(k+'_refinement',e,t))
 if len(a['background'])!=len(b['background']):raise AssertionError('BBN common background grid')
 for col in range(10):
  errors=[]
  for x,y in zip(a['background'],b['background']):
   if x[col]is None or y[col]is None:
    if x[col]!=y[col]:raise AssertionError('BBN paired null')
   else:errors.append(abs(x[col]-y[col])/max(abs(y[col]),1e-30))
  gates.append(gate('background_column_'+str(col)+'_refinement',max(errors),2e-12))
 return gates,signed

def atomic_packet(arm,ctx,helium,helpers):
 count=105859 if arm=='DEFAULT' else 211717;oldname='INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_'+arm+'_INPUT.txt'
 lines=(BASE/oldname).read_text().splitlines();head=lines[0].split();pars=lines[1].split();o={**ctx['ordinary'],'YHe':helium}
 if (head[:2]!=['UNT_HYREC_EXTERNAL_V001','JOINT3_FINAL_CANDIDATE_'+arm] or len(head)!=3 or len(pars)!=5
  or list(map(float,pars[:4]))!=[o[k] for k in ('omega_b','T0','YHe_old_fixture','Hstar')]
  or int(pars[4])!=count or len(lines)!=count+2):raise AssertionError('Original native grid geometry')
 zz=np.array([float(line.split()[0]) for line in lines[2:]]);RAW['H_grid_z']=zz
 if not np.all(np.isfinite(zz)) or any(abs(z-i*8000/count)>2e-12*max(1,z) for i,z in enumerate(zz)):
  raise AssertionError('Native z geometry')
 hh=np.empty(count);RAW['H_grid']=hh;RAW['H_grid_completed_count']=0
 for i,z in enumerate(zz):
  hh[i]=ctx['fixed']['Hunit']*1000/MPC*helpers['background'](-math.log1p(float(z)),ctx['fixed'])['h'];RAW['H_grid_completed_count']=i+1
 if not np.all(np.isfinite(hh)) or not np.all(hh>0):raise AssertionError('TargetEPS H grid')
 context=dict(source_sha256=RUN_SOURCE,arm=arm,fixed=ctx['fixed'],ordinary=o,
  H_grid_method='Every targetEPS H recomputed; old z geometry only',old_geometry_sha256=sha(BASE/oldname),
  helium_parent_commit_sha256=sha(BASE/(STEM+'_BBN_PAIR_COMMIT.json')),calibration_replayed=False)
 claim=hashlib.sha256(encoded(context).rstrip(b'\n')).hexdigest();label='CROSS_U_EPS1E5_'+arm
 text=['UNT_HYREC_EXTERNAL_V001 '+label+' '+claim,
  ' '.join(format(o[k],'.17g') for k in ('omega_b','T0','YHe','Hstar'))+' '+str(count)]
 text.extend(format(float(z),'.17g')+' '+format(float(h),'.17g') for z,h in zip(zz,hh))
 raw=('\n'.join(text)+'\n').encode()
 err=max(abs(float(hh[i])/(ctx['fixed']['Hunit']*1000/MPC*helpers['background'](-math.log1p(float(zz[i])),ctx['fixed'])['h'])-1)
  for i in [round((count-1)*k/64) for k in range(65)])
 return raw,context,claim,label,zz,hh,err,o

def run_stage(case,ctx,helpers):
 arrays={};data={};gates=[];files={};obj=BASE/(STEM+'_background.o');exe=BASE/(STEM+'_binary')
 if case=='BUILD_BACKGROUND':
  argv=[COMPILER,'-std=gnu11','-O2','-Wall','-Wextra','-pthread','-I'+str(LIB/'upstream/primat-c/include'),
   '-c',str(BASE/'cross_u_eps1e5_fixed_nevo_background_v001.c'),'-o',str(obj)]
  rec,files=run_command(case,argv,targets=(obj,));data=dict(command=rec)
 elif case=='BUILD_LINK':
  argv=[COMPILER,*ctx['objects'],str(obj),str(BASE/(OLD_BBN+'_adapter.o')),'-lm','-pthread','-o',str(exe)]
  rec,files=run_command(case,argv,targets=(exe,));data=dict(command=rec)
 elif case in ('BBN_DEFAULT','BBN_REFINED'):
  arm=case[4:];rec,files=run_command(case,[str(exe),arm.lower()],allow_codes=(0,2),stderr_empty=True)
  raw=json.loads((BASE/(STEM+'_'+case+'_STDOUT.txt')).read_text())
  RAW['bbn_json']=raw
  for name in ('background','nuclear_history','HT_relaxation'):arrays.update(capture_table(name,raw[name]))
  gates=helpers['source_checks'](raw,arm,ctx['bbn_fixed']);data=dict(raw=raw,command=rec)
 elif case=='BBN_PAIR':
  a=DATA['BBN_DEFAULT'][0]['data']['raw'];b=DATA['BBN_REFINED'][0]['data']['raw']
  extra,signed=pair_bbn(a,b);gates=DATA['BBN_DEFAULT'][0]['gates']+DATA['BBN_REFINED'][0]['gates']+extra
  if len(gates)!=39:raise AssertionError('Original39 BBN gates')
  helium=b['final']['YPCMB']
  if not math.isfinite(helium) or not 0<helium<1:raise AssertionError('Own refined helium')
  data=dict(helium=helium,finals={k:DATA['BBN_'+k][0]['data']['raw']['final'] for k in ('DEFAULT','REFINED')},signed_default_minus_refined=signed)
 elif case in ('ATOMIC_DEFAULT','ATOMIC_HALF'):
  arm=case[7:];packet,context,claim,label,zz,hh,err,o=atomic_packet(arm,ctx,DATA['BBN_PAIR'][0]['data']['helium'],helpers)
  rec,files=run_command(case,[ctx['binaries'][arm],str(ATOMIC/'upstream')+'/', 'external'],packet,stderr_empty=True)
  raw=json.loads((BASE/(STEM+'_'+case+'_STDOUT.txt')).read_text());RAW['atomic_json']=raw
  arrays.update(capture_table('atomic_rows',raw['rows']));arrays.update(H_grid_z=zz,H_grid=hh)
  gates=helpers['output_controls'](raw,arm,o,claim,label,zz.tolist(),hh.tolist(),err)
  data=dict(raw=raw,context=context,command=rec,claim=claim)
 elif case=='ATOMIC_PAIR':
  a=DATA['ATOMIC_DEFAULT'][0]['data']['raw']['rows'];b=DATA['ATOMIC_HALF'][0]['data']['raw']['rows'][::2]
  if len(a)!=len(b) or any(x[0]!=y[0] for x,y in zip(a,b)):raise AssertionError('Atomic common z')
  gates=DATA['ATOMIC_DEFAULT'][0]['gates']+DATA['ATOMIC_HALF'][0]['gates'];signed={}
  for key,col in (('xe_refinement',1),('Tm_refinement',2)):
   delta=np.array([x[col]-y[col] for x,y in zip(a,b)]);RAW[key]=delta;arrays[key]=delta
   err=max(abs(x[col]-y[col])/(max(1e-3,abs(y[col])) if col==1 else abs(y[col])) for x,y in zip(a,b))
   gates.append(gate(key,err,2e-3));signed[key]=float(np.max(abs(delta)))
  if len(gates)!=12:raise AssertionError('Original12 atomic gates')
  data=dict(helium=DATA['BBN_PAIR'][0]['data']['helium'],signed_difference_maxima=signed)
 elif case.startswith('ACOUSTIC_') and case!='ACOUSTIC_PAIR':
  label=case[9:];spec={'DEFAULT':('DEFAULT',1,512),'HALF':('HALF',1,512),'THIN':('HALF',2,512),'QUADRATURE':('HALF',1,256)}
  arm,thin,n=spec[label];bg=helpers['Background'](ctx['fixed'],ctx['ledger'])
  obs=helpers['observables'](bg,DATA['ATOMIC_'+arm][0]['data']['raw'],thin,n);RAW['acoustic_observables']=obs
  data=dict(label=label,atomic=arm,thinning=thin,gauss_order=n,observables=obs)
 elif case=='ACOUSTIC_PAIR':
  rows=[DATA['ACOUSTIC_'+a][0]['data'] for a in ('DEFAULT','HALF','THIN','QUADRATURE')];ref=rows[1]['observables'];comparisons=[]
  for index,tol in ((0,2e-4),(2,1e-4),(3,2e-8)):
   signed={}
   for key in FIELDS:
    delta=np.array(rows[index]['observables'][key])/np.array(ref[key])-1;arrays[rows[index]['label']+'_'+key]=delta
    RAW[rows[index]['label']+'_'+key]=delta;signed[key]=delta.tolist();gates.append(gate(rows[index]['label']+'_'+key,float(np.max(abs(delta))),tol))
   comparisons.append(dict(label=rows[index]['label'],signed_fractional_differences=signed))
  for row in rows:
   o=row['observables'];gates.append(gate(row['label']+'_angular_identity',abs(o['theta100']*o['ell_A']/(100*math.pi)-1),1e-13))
  if len(gates)!=22:raise AssertionError('Original22 acoustic gates')
  data=dict(rows=rows,comparisons=comparisons,H_today_km_s_Mpc=ctx['fixed']['Hunit']*helpers['background'](0.,ctx['fixed'])['h'])
 elif case=='DESI':
  lines=[s.split() for s in (BASE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt').read_text().splitlines() if s.strip() and not s.startswith('#')]
  if [(float(r[0]),r[2]) for r in lines]!=ORDER:raise AssertionError('DESI exact13 row order')
  obs=np.array([float(r[1]) for r in lines]);RAW['bao_data']=obs
  cov=np.loadtxt(BASE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt');RAW['bao_covariance']=cov
  if obs.shape!=(13,) or cov.shape!=(13,13) or not np.all(np.isfinite(cov)) or not np.all(obs>0):raise AssertionError('DESI full data/covariance')
  bg=helpers['Background'](ctx['fixed'],ctx['ledger']);f=helpers['distance_vector'](bg,96);RAW['bao_distance96']=f
  co=helpers['distance_vector'](bg,48);RAW['bao_distance48']=co
  si=helpers['distance_vector'](bg,96,True);RAW['bao_distance_simpson2048']=si
  chol=np.linalg.cholesky(cov);RAW['bao_cholesky']=chol
  ci=np.linalg.solve(cov,np.eye(13));RAW['bao_precision']=ci
  A=float(f@ci@f);B=float(f@ci@obs);C0=float(obs@ci@obs)
  lo,hi=DATA['ACOUSTIC_HALF'][0]['data']['observables']['drag_ruler_Mpc_interval']
  if not math.isfinite(lo) or not 0<lo<hi or not np.all(f>0):raise AssertionError('Own positive predicted ruler')
  lowy,highy=1/hi,1/lo;vertex=min(highy,max(lowy,B/A));candidates=(lowy,highy,vertex,2/(lo+hi));witnesses=[];errors=[]
  for i,y in enumerate(candidates):
   prediction=f*y;RAW['bao_prediction_'+str(i)]=prediction;res=prediction-obs;RAW['bao_residual_'+str(i)]=res
   white=np.linalg.solve(chol,res);RAW['bao_white_'+str(i)]=white;score=float(white@white);poly=A*y*y-2*B*y+C0
   errors.append(abs(score-poly));witnesses.append(dict(ruler_Mpc=1/y,score=score,prediction=prediction.tolist(),residual=res.tolist(),whitened_residual=white.tolist(),quadratic_score=poly))
  gates=[gate('covariance_symmetry',float(np.max(abs(cov-cov.T))),2e-12),gate('covariance_inverse',float(np.max(abs(cov@ci-np.eye(13)))),2e-12),
   gate('gauss48_96_distance',float(np.max(abs(co/f-1))),2e-12),gate('independent_simpson_distance',float(np.max(abs(si/f-1))),2e-11),gate('direct_vs_quadratic_score',max(errors),2e-8)]
  arrays=dict(data=obs,covariance=cov,distance96=f,distance48=co,distance_simpson2048=si,cholesky=chol,precision=ci,
   predictions=np.array([w['prediction'] for w in witnesses]),residuals=np.array([w['residual'] for w in witnesses]),whitened_residuals=np.array([w['whitened_residual'] for w in witnesses]))
  data=dict(ruler_Mpc_interval=[lo,hi],score_interval=[witnesses[2]['score'],max(w['score'] for w in witnesses[:2])],
   score_witnesses=witnesses,quadratic=dict(A=A,B=B,C0=C0),H_today_times_ruler_interval=[DATA['ACOUSTIC_PAIR'][0]['data']['H_today_km_s_Mpc']*lo,DATA['ACOUSTIC_PAIR'][0]['data']['H_today_km_s_Mpc']*hi],
   inference_scope='Unprofiled physical ruler interval only; vertex restricted to admitted low-z-drag interval, no free ruler fit')
 else:raise AssertionError('Unknown prospective case')
 return checkpoint(case,arrays,data,gates,files),arrays

def final_recheck():
 recheck()
 for cn in PAIRS:read_pair(cn)
 expected={str(Path(p).resolve()) for p in CREATED}|{str((BASE/(STEM+'_JOURNAL.jsonl')).resolve())}
 actual={str(p.resolve()) for p in BASE.glob(STEM+'_*') if p.is_file()}
 if actual!=expected:raise AssertionError('Complete own file-map equality')

def raw_metadata(v):
 if isinstance(v,dict):return {str(k):raw_metadata(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [raw_metadata(x) for x in v]
 if hasattr(v,'item'):return raw_metadata(v.item())
 if isinstance(v,float) and not math.isfinite(v):return dict(value=None,reason='nonfinite',raw_representation=repr(v))
 return plain(v)

def failure(exc):
 prior=BASE/(STEM+'_RECEIPT.json');priorhash=sha(prior) if prior.exists() else None
 error=dict(status='EXECUTION_ERROR_PRESERVED',case=ACTIVE,error=repr(exc),time=now(),pid=os.getpid(),
  source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,prior_closed_receipt_sha256=priorhash,
  completed_cases=[STAGES[i] for i in range(len(PAIRS))],raw_json={k:raw_metadata(v) for k,v in RAW.items() if not hasattr(v,'dtype')})
 if prior.exists():
  # A postreceipt error publishes separate evidence; never creates an unregistered raw NPZ after CLOSED.
  write(STEM+'_POSTRECEIPT_ERROR.json',error);return
 if np is not None:
  arrays={k:v for k,v in RAW.items() if hasattr(v,'dtype') and not v.dtype.hasobject};text=encoded(error)
  p=BASE/(STEM+'_ERROR_RAW.npz')
  with p.open('xb') as f:np.savez_compressed(f,__metadata__=np.array(text.decode()),**arrays);f.flush();os.fsync(f.fileno())
  track(p);write(STEM+'_ERROR_RAW_COMMIT.json',dict(schema=1,failed=True,payload=p.name,sha256=sha(p),metadata=json.loads(text),arrays={k:descriptor(a) for k,a in arrays.items()}))
 write(STEM+'_ERROR.json',error)
 if (BASE/(STEM+'_JOURNAL.jsonl')).exists():journal('OWNER_ERROR',case=ACTIVE,error=repr(exc))
 # Include raw outputs even if a subprocess or sealing operation refused before registration.
 for p in BASE.glob(STEM+'_*'):
  if p.is_file() and p.name not in (STEM+'_RECEIPT.json',STEM+'_JOURNAL.jsonl'):CREATED[str(p.resolve())]=sha(p)
 write(STEM+'_RECEIPT.json',dict(schema=1,status=error['status'],owner='root',pid=os.getpid(),time=now(),
  source_sha256=RUN_SOURCE,inputs=dict(INPUTS),output_sha256=dict(CREATED),
  journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')) if (BASE/(STEM+'_JOURNAL.jsonl')).exists() else None))

def main(resume):
 global np,RUN_SOURCE,ACTIVE
 tick=time.monotonic();RUN_SOURCE=sha(__file__);ctx=authenticate()
 if (BASE/(STEM+'_RECEIPT.json')).exists():raise FileExistsError('Existing terminal receipt; no replay')
 import numpy as numpy_module
 np=numpy_module;helpers=load_helpers();lineage(resume,ctx)
 stop=None
 for case in STAGES:
  ACTIVE=case;RAW.clear()
  if case not in DATA:DATA[case]=run_stage(case,ctx,helpers)
  meta=DATA[case][0]
  print(json.dumps(dict(case=case,status='SAVED_COMPLETE',passed=sum(g['passed'] for g in meta['gates']),gates=len(meta['gates']))),flush=True)
  if case in ('BBN_PAIR','ATOMIC_PAIR','ACOUSTIC_PAIR','DESI') and not all(g['passed'] for g in meta['gates']):stop=case;break
 stage_gates={case:DATA[case][0]['gates'] for case in ('BBN_PAIR','ATOMIC_PAIR','ACOUSTIC_PAIR','DESI') if case in DATA}
 status='CONDITIONAL_FIXED_EPS_EARLY_CHAIN_ARITHMETIC_PASS' if stop is None else 'CONDITIONAL_FIXED_EPS_EARLY_CHAIN_ARITHMETIC_FAILED'
 if stop is None and sum(map(len,stage_gates.values()))!=78:raise AssertionError('39+12+22+5 original gates')
 result=dict(schema=1,status=status,all_numerical_gates_passed=stop is None,stopped_after=stop,context=ctx,
  completed_cases=[case for case in STAGES if case in DATA],cases={case:DATA[case][0] for case in STAGES if case in DATA},
  stage_gates=stage_gates,physical_flags=FLAGS,elapsed_seconds=time.monotonic()-tick,
  scope='ONE EPS1e-5 fixed-NEVO ordinary thermal chain; no calibration/re-preparation/native thermal origin/new neutrino decoupling/CMB or perturbation transfer/global adoption')
 final_recheck();rh=write(STEM+'_RESULT.json',result)
 report='# ONE EPS1e-5 fixed-NEVO BBN→recombination→ruler→DESI chain\n\n'+status+'\n\n'
 report+='The physical inventory, rates, NEVO, .99 GN and the ordinary thermal preparation are inherited. Only EPS changes. All original stage predicates and raw histories are retained.\n\n'
 for case,gates in stage_gates.items():report+=case+': '+str(sum(g['passed'] for g in gates))+'/'+str(len(gates))+' arithmetic predicates PASS.\n\n'
 if 'DESI'in DATA:report+='Predicted drag ruler interval and correlated DESI score: '+repr(DATA['DESI'][0]['data'])+'\n\n'
 report+='The acoustic tail and low-z drag brackets are conditional. Ancestor theta/data exposure remains; no physical or statistical superiority certificate.\n'
 reph=write(STEM+'_REPORT.md',report.encode(),True);final_recheck()
 journal('OWNER_COMPLETE',status=status,result_sha256=rh,gate_count=sum(map(len,stage_gates.values())))
 rc=dict(schema=1,status=status,owner='root',original_owner_pid=OWNER_PID,closing_pid=os.getpid(),time=now(),
  source_sha256=RUN_SOURCE,inputs=dict(INPUTS),manifest_sha256=RUN_MANIFEST,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),
  result_sha256=rh,report_sha256=reph,output_sha256=dict(CREATED),physical_flags=FLAGS)
 write(STEM+'_RECEIPT.json',rc);final_recheck()
 if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=rc:raise AssertionError('Canonical closed receipt reread')
 return 0 if stop is None else 3

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');ap.add_argument('--resume',action='store_true');args=ap.parse_args()
 if GUARDED_UNEXECUTED or not args.execute:raise SystemExit('Guarded unexecuted author draft; root alone may release --execute')
 # An existing terminal artifact is refused before any catch can mutate it.
 if (BASE/(STEM+'_RECEIPT.json')).exists():raise SystemExit('Existing terminal receipt preserved')
 try:raise SystemExit(main(args.resume))
 except Exception as exc:failure(exc);raise
