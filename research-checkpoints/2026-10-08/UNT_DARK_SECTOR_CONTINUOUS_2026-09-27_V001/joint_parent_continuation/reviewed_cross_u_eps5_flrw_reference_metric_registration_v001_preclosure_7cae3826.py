"""Guarded homogeneous EPS5 Euler reference on sealed full-metric test operands."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_EPS5_FLRW_REFERENCE_METRIC_REGISTRATION_V001'
PARENT='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
PARENT_RESULT_SHA=None
PARENT_RECEIPT_SHA=None
PROTOCOL_SHA=None
PINS={
 'reviewed_cross_u_eps5_flrw_reference_metric_registration_v001_workdraft_d5872a9a.py':'d5872a9a46b8e26245d214e1a762371c91d64c4c389d3b77937dd5c4c4099a42',
 'reviewed_cross_u_eps5_flrw_reference_metric_registration_v001_workdraft_70fc7c59.md':'70fc7c59c8a96f7772682afffd2676cbfdca282c92588c48bbcc58da8b2a3b1a',
 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json':'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f',
 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json':'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6',
 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json':'3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c',
 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md':'087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523',
 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md':'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986',
 'cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68',
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001.md':'88fbf64e1568af3f47f1346b809c6d8a35fe7b685a73817938616b9056068e24'}
LIGHT=299792458.;KPC=3.085677581491367e19;C=1.98;TOL=2e-11
CONTROL_COUNT=17;PAIR_COUNT=5
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];RAW={};ARM_AVAILABLE={};CONTEXT={};CHECKS=[]
FLAGS={k:False for k in ('full_metric_solution_qualified','physical_embedding_qualified','physical_junction_qualified','native_history_qualified','material_history_qualified','activity_outside_support_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}
def now():return datetime.now(timezone.utc).isoformat()

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Nonfinite or unsupported metadata: '+type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(n,b):
 p=path(n)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==b;OUTPUTS[n]=sha(p);return OUTPUTS[n]

def json_file(n,v):return publish(n,encode(v))

def array(v,name):
 a=np.asarray(v)
 if a.dtype.kind not in 'fiu' or not np.all(np.isfinite(a)):raise ValueError(name+' must be finite real numeric data.')
 return a.astype(np.float64,copy=False)

def check(name,actual,expected,envelope=None):
 ordinal=len(CHECKS);CONTEXT.update(current_control=name,current_control_ordinal=ordinal)
 a=np.asarray(actual);b=np.asarray(expected);prefix=f'control_{ordinal:03d}_{name}'
 RAW[prefix+'_actual']=a.copy();RAW[prefix+'_expected']=b.copy()
 if envelope is not None:RAW[prefix+'_envelope']=np.asarray(envelope).copy()
 assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
 env=max(1e-30,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0))) if envelope is None else max(1e-30,float(np.max(array(envelope,'control envelope'),initial=0)))
 gap=float(np.max(abs(a-b),initial=0));err=gap/env;assert all(math.isfinite(x) for x in (env,gap,err))
 row=dict(ordinal=ordinal,name=name,absolute_gap=gap,envelope=env,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row)
 assert row['passed'],name
 return row

def checkpoint(tag,arrays,meta):
 md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
 text=encode(md).decode();md=json.loads(text);name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);rec=dict(file=name,sha256=sha(p),metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);OUTPUTS[name]=rec['sha256'];RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert set(f.files)==set(arrays)|{'metadata_json'} and str(f['metadata_json'])==text
  for k,a in arrays.items():assert f[k].dtype==a.dtype and f[k].shape==a.shape and np.array_equal(f[k],a,equal_nan=True)
 return rec

def seal_created():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)

def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('Input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 if strict:assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('Output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for k,s in r['metadata']['schema'].items():assert f[k].shape==tuple(s['shape']) and str(f[k].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[k])))==s['finite']
 if strict:
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}


def admission():
 assert all(isinstance(x,str) and len(x)==64 for x in (PARENT_RESULT_SHA,PARENT_RECEIPT_SHA,PROTOCOL_SHA)), 'Final CLOSED seals pending.'
 inputs={}
 def add(n,h):
  n=str(path(n).resolve());assert n not in inputs or inputs[n]==h;inputs[n]=h
 for n,h in PINS.items():add(n,h)
 add(PARENT+'_RESULT.json',PARENT_RESULT_SHA);add(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA)
 add(STEM+'.md',PROTOCOL_SHA);add(str(Path(__file__).resolve()),sha(__file__))
 receipt=json.loads(path(PARENT+'_RECEIPT.json').read_text());result=json.loads(path(PARENT+'_RESULT.json').read_text())
 assert receipt['status']=='CLOSED' and result['owner']==receipt['owner'] and receipt['result_sha256']==PARENT_RESULT_SHA
 assert result['status']=='CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS'
 assert len(result['controls'])==36 and all(c['passed'] for c in result['controls']) and len(result['checkpoints'])==6
 assert [c['sigma'] for c in result['cases']]==[.1,1.,10.,100.] and all(v is False for v in result['qualification'].values())
 for key in ('input_sha256','output_sha256'):
  for n,h in receipt[key].items():add(n,h)
 for rec in result['checkpoints']:
  assert receipt['output_sha256'][rec['file']]==rec['sha256'] and receipt['output_sha256'][rec['commit_file']]==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 for n,h in inputs.items():assert sha(path(n))==h,('Changed input',n)
 shared=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text());cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 assert cp==next(r for r in shared['rows'] if r['eps']==1e-5)
 fixed=dict(shared['manifest']['fixed_parent']);fixed['eps']=1e-5
 assert fixed['Q0_over_Hstar']==100 and all(math.isfinite(cp['background'][k]) for k in ('h','q','s','w','rho','A'))
 return inputs,result,fixed,cp


def reference(fixed,cp):
 # Saved scalar arithmetic; no old background/helper/trajectory evaluation.
 r=cp['background'];eta=fixed['Hunit']/LIGHT;b=1.5*fixed['OB']/fixed['rG'];rad=1.5*fixed['OR']/fixed['rG'];h=r['h'];w=r['w'];rho=r['rho'];A=r['A']
 hdot=-(b+4*rad/3+w);ep=fixed['eps'];norm=1/ep-math.log1p(1/ep);pe=(math.log1p(r['s'])-r['s']/(1+r['s']))/norm
 d=2*r['q']*r['s']/(ep*norm);d_q=2/(ep*norm)*(r['s']+2*r['q']**2*(1+r['s'])**2/ep);rho_q=A*r['q']*d_q
 RAW.update(reference_charge=np.array(d),reference_charge_q_derivative=np.array(d_q),reference_phase_density_q_derivative=np.array(rho_q))
 check('proper_eta_units',np.array(eta),np.array((fixed['Hunit']*1000/(1000*KPC))*KPC/LIGHT))
 check('saved_Friedmann_ledger',np.array(1.5*h*h),np.array(b+rad+rho))
 check('saved_phase_pressure_allocation',np.array(A*(pe-1)),np.array(w-rho))
 check('saved_absolute_phase_charge',np.array(d),np.array(fixed['d0']))
 check('independent_EOS_sound_squared',np.array(d/(r['q']*d_q)),np.array(r['cs']))
 # Derivative of the complete density budget uses the separately saved sound squared.
 rho_dot=rho_q*(-3*h*r['cs']*r['q']);RAW['reference_phase_density_time_derivative']=np.array(rho_dot)
 check('Friedmann_derivative_charge_ledger',np.array(hdot),np.array((-3*h*b-4*h*rad+rho_dot)/(3*h)))
 fac=eta*eta/C
 coeff=np.array([[-1.5*h*h,0.],[0.,(2*hdot+3*h*h)/2],[rho,0.],[0.,w-rho],[b,0.],[rad,0.],[0.,rad/3]])*fac
 labels=['EH_normal','EH_spatial_Euler','phase_density','phase_pressure','ordinary_dust_density','ordinary_radiation_density','ordinary_radiation_pressure']
 env=np.sum(abs(coeff),axis=0)
 check('homogeneous_normal_Euler_ledger',np.array(coeff[:,0].sum()),np.array(0.),np.array(env[0]))
 check('homogeneous_spatial_Euler_ledger',np.array(coeff[:,1].sum()),np.array(0.),np.array(env[1]))
 snapshot=-1.5*h*h*fac;time_IBP=(hdot+3*h*h)*fac
 check('EH_time_IBP_contact',np.array(snapshot+time_IBP),np.array(coeff[1,1]),np.array(abs(snapshot)+abs(time_IBP)))
 RAW.update(reference_scalars=np.array([eta,b,rad,h,hdot,r['q'],w,rho,A]),reference_coefficients=coeff,reference_coefficient_envelopes=env,EH_snapshot_spatial_coefficient=np.array(snapshot),EH_time_IBP_spatial_contact=np.array(time_IBP))
 checkpoint('REFERENCE',dict(RAW),dict(kind='owned_homogeneous_a1_Euler_ledger',scalar_order=['eta','b','r','h','hdot_Hstar','q','w','rho','A'],components=labels,coefficient_columns=['q_ref00','q_ref_spatial_trace'],controls=list(CHECKS),reference_chart='a=1 comoving FLRW cylindrical frame; measure ratio one',physical_changes=[]))
 return coeff,labels


def arm(case,coeff,labels):
 global RAW,ARM_AVAILABLE
 RAW={};ARM_AVAILABLE={};CONTEXT.update(stage='reference_overlap',sigma=case['sigma']);begin=len(CHECKS);rec=case['checkpoint']
 components=np.zeros((2,10,7));envelopes=np.zeros_like(components);overlaps=np.zeros((2,10,2));node_checks=[];node_expected=[];node_env=[]
 ARM_AVAILABLE.update(reference_components=components,reference_envelopes=envelopes,reference_test_overlaps=overlaps)
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json']))==rec['metadata']
  for iq in range(4):
   R=f[f'q{iq}_R'];dv=f[f'q{iq}_reference_volume'];assert R.dtype==dv.dtype==np.dtype('float64') and R.shape==dv.shape and np.all(R>0) and np.all(dv>0)
   RAW.update(current_reference_R=R,current_reference_volume=dv)
   for ib in range(2):
    for ik in range(10):
     CONTEXT.update(quadrature=iq,rectangle=ib,dyad=ik);q=f[f'b{ib}_d{ik}_q{iq}_metric_test'];RAW['current_metric_test']=q;assert q.dtype==np.dtype('float64') and q.shape==(len(R),4,4) and np.all(np.isfinite(q))
     # Use the actual saved coordinate test, transformed to reference a=1 axes.
     # No trial exp(-2Phi) measure, native reconstruction, subtraction or addition.
     normal=q[:,0,0];spatial=q[:,1,1]+q[:,2,2]+q[:,3,3]/R**2;test=np.column_stack((normal,spatial));RAW['current_reference_test']=test
     density=test@coeff.T;RAW['current_reference_density']=density
     denv=abs(test)@abs(coeff).T;RAW['current_reference_density_envelope']=denv
     components[ib,ik]+=np.einsum('p,pk->k',dv,density);envelopes[ib,ik]+=np.einsum('p,pk->k',dv,denv);overlaps[ib,ik]+=np.einsum('p,pk->k',dv,test)
     node_checks.append(density.sum(axis=1));node_expected.append(np.zeros(len(R)));node_env.append(denv.sum(axis=1))
  original=f['metric_signed_components'].copy();original_envelope=f['metric_uncancelled_envelopes'].copy()
 check(f's{case["sigma"]}_reference_pointwise_ledger',np.concatenate(node_checks),np.concatenate(node_expected),np.concatenate(node_env))
 independently=overlaps@coeff.T;scale=np.maximum(envelopes,1e-30)
 check(f's{case["sigma"]}_independent_reference_integrals',components/scale,independently/scale,np.ones_like(scale))
 arrays=dict(reference_components=components,reference_envelopes=envelopes,reference_test_overlaps=overlaps,independent_reference_integrals=independently,original_trial_components=original,original_trial_envelopes=original_envelope,original_EH_minus_reference_EH=original[:,:,0]-components[:,:,:2].sum(axis=2),original_absolute_phase_minus_reference_phase=original[:,:,8]-components[:,:,2:4].sum(axis=2))
 arrays.update({k:v.copy() for k,v in RAW.items() if k.startswith('control_')})
 ARM_AVAILABLE.update(arrays)
 out=checkpoint('ARM',arrays,dict(kind='homogeneous_reference_overlap_only',sigma=case['sigma'],parent_pair=rec['file'],parent_pair_sha256=rec['sha256'],components=labels,controls=CHECKS[begin:],original_trial_disposition=case['status'],physical_changes=[],unknowns=dict(local_time_dependent_metric=None,local_phase_history=None,native_history=None,ordinary_background_excess_allocation=None,actual_junction=None)))
 ARM_AVAILABLE={}
 return dict(sigma=case['sigma'],checkpoint=out,reference_components=components.tolist(),reference_net=components.sum(axis=2).tolist(),original_trial_components=original.tolist(),qualification=FLAGS)


def main():
 global np,INPUTS,OWNER,RAW
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded draft; FULL review and root-only release required.')
 assert not list(BASE.glob(STEM+'_*')),'Runtime prefix occupied.'
 INPUTS,parent,fixed,cp=admission();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__),scope='saved homogeneous EPS5 reference registration only');cases=[]
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_result=PARENT+'_RESULT.json',parent_result_sha256=PARENT_RESULT_SHA,configuration=dict(controls=CONTROL_COUNT,pairs=PAIR_COUNT,tolerance=TOL),qualification=FLAGS))
  import numpy as _np
  np=_np
  coeff,labels=reference(fixed,cp)
  for c in parent['cases']:
   with np.errstate(over='raise',invalid='raise',divide='raise'):cases.append(arm(c,coeff,labels))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT and all(c['passed'] for c in CHECKS)
  result=dict(owner=OWNER,status='HOMOGENEOUS_REFERENCE_REGISTRATION_ARITHMETIC_PASS',controls=CHECKS,cases=cases,checkpoints=RECORDS,copied_original_controls=parent['controls'],original_disposition=parent['status'],qualification=FLAGS,reference_scope='No original residual or field changed; not a local embedding, counterterm or force correction.')
  recheck();rh=json_file(STEM+'_RESULT.json',result);publish(STEM+'_REPORT.md',(f'# {STEM}\n\n{CONTROL_COUNT} homogeneous reference checks; all original metric/phase/source rows preserved. The time-IBP EH Euler contact and complete ordinary budget are retained. No local metric/history/junction or orbital qualification.\n').encode());recheck()
  receipt=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',receipt);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(receipt);recheck();print('HOMOGENEOUS_REFERENCE_REGISTRATION_ARITHMETIC_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_failure=None;closing_failure=None;available=dict(ARM_AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_reference_operands',context=CONTEXT))
   except BaseException:raw_failure=traceback.format_exc()
  try:seal_created();recheck(False)
  except BaseException:closing_failure=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  if prior:OUTPUTS[STEM+'_RECEIPT.json']=prior
  error=dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_failure,closing_traceback=closing_failure,context=CONTEXT,checkpoints=RECORDS,controls=CHECKS,cases=cases,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}],unqualified_commits=[p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json') if p.name not in {r['commit_file'] for r in RECORDS}],qualification=FLAGS)
  if not path(STEM+'_ERROR.json').exists():eh=json_file(STEM+'_ERROR.json',error)
  else:eh=sha(path(STEM+'_ERROR.json'))
  if prior is None:
   receipt=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',receipt);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(receipt)
  recheck(False);raise

if __name__=='__main__':main()
