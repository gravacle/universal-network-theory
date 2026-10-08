"""Guarded saved-scalar physical-ruler joint score; no scientific modules."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, time, traceback
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
STEM='CROSS_U_EPS1E5_SAVED_PHYSICAL_RULER_JOINT_SCORE_V001'
AUTHOR_DRAFT=True
PROTOCOL_SHA='3c60743bdb01caa80c8cc08b312cf957f09a3af24113c9a9097ca01f174fda8d'
PINS={'cross_u_eps1e5_fixed_nevo_recombination_ruler_chain_v001.py': '75fe8765520437f6a5990ce40f2c11646398afd650a223069c20dd8e33c8b905', 'CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001.md': 'f511db085e290e3287902e20f9e0eb9cf2679febc4a9af01061f30f10068645b', 'CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001_MANIFEST.json': '84c5282d6c3757ce367c6c41bbb28da37a19b03d1161edc8f2c31f5323fad8d5', 'CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001_RESULT.json': '3e0e5dbcc1b5a8f1d9ff692893b39a294c91fa2fc84a2d45de10101b0277be2f', 'CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001_RECEIPT.json': 'e4cee3eeb4ab155d5650e498b6f844b485c906dfa353b997587da4b38463274d', 'constrained_u_joint_pantheon_desi_shape_v001.py': '3defeaed9f48c761791389776224892ba449ded12f3bbd2ab6c3e41050815941', 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001.md': '6f8869df3f6cc58deda9b73c566c697452988dcdd208c76d5630d6e6799e1820', 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001_MANIFEST.json': '294c7691dcaccc214e73d5eb8fa5b580946af61b7163612728dda551f3ed41f5', 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001_RESULT.json': '8e8f37664e5eed4647a259468678b1c997805d1171c5fb26f5f2c7d2dc8a109d', 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001_RECEIPT.json': 'f7cf2b89ab28e5558a1e7fb74bd6bba643b8c438c649fde35ec95e9c9ee0a006', 'reviewed_cross_u_eps1e5_saved_physical_ruler_joint_score_v001_121.py': '10a501ea92f5216fa6a974836eaacfffb363dd2630805aabe7b09bd29dde84f8', 'reviewed_CROSS_U_EPS1E5_SAVED_PHYSICAL_RULER_JOINT_SCORE_V001_19.md': '02a1d4bf8f739a9fb381aaef2a1d450f6ac2e4fabb44b81a24284e552ceb7392', 'reviewed_cross_u_eps1e5_saved_physical_ruler_joint_score_v001_123.py': '9a5df20551bbaf0c9e0d0994ba961c7663c59314edf5a0183ca7e28fd66e959f'}
EARLY='CROSS_U_EPS1E5_FIXED_NEVO_RECOMBINATION_RULER_CHAIN_V001'
LATE='CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001'
FLAGS={k:False for k in ('physical_joint_qualified','global_EPS_adopted','model_superiority_qualified','independent_validation_qualified','microscopic_budget_closed','CMB_transfer_qualified')}
INPUTS={};OUTPUTS={};AVAILABLE={};OWNER=None

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def encode(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def publish(name,value,raw=False):
 p=BASE/name;b=value if raw else encode(value)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
 if p.read_bytes()!=b:raise AssertionError('Exclusive byte reread '+name)
 OUTPUTS[str(p.resolve())]=sha(p);return OUTPUTS[str(p.resolve())]
def seal(p,w):
 p=Path(p).resolve()
 if not (p.is_relative_to(ROOT) or (p==Path('/usr/bin/clang').resolve() and w=='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818')):raise AssertionError('Outside registered input')
 if sha(p)!=w or (str(p)in INPUTS and INPUTS[str(p)]!=w):raise AssertionError('Input binding '+str(p))
 INPUTS[str(p)]=w
def recheck():
 for p,w in {**INPUTS,**OUTPUTS}.items():
  if sha(p)!=w:raise AssertionError('Immutable byte '+p)
def read(name):return json.loads((BASE/name).read_text())
def closed(st,status):
 rc=read(st+'_RECEIPT.json');r=read(st+'_RESULT.json');m=read(st+'_MANIFEST.json')
 if rc['status']!=status or r['status']!=status or rc['result_sha256']!=sha(BASE/(st+'_RESULT.json')):raise AssertionError('Closed parent status')
 im=rc.get('inputs',rc.get('input_sha256'));om=rc['output_sha256']
 if not im or not om:raise AssertionError('Complete parent byte maps')
 for p,w in {**im,**om}.items():seal(p if Path(p).is_absolute() else BASE/p,w)
 seal(BASE/(st+'_MANIFEST.json'),rc.get('manifest_sha256',sha(BASE/(st+'_MANIFEST.json'))))
 if st==EARLY:
  if rc['owner']!='root' or rc['original_owner_pid']!=rc['closing_pid'] or rc['closing_pid']!=m['owner_pid'] or m['source_sha256']!=rc['source_sha256']:raise AssertionError('Early owner/source')
  seal(BASE/(st+'_JOURNAL.jsonl'),rc['journal_sha256']);ev=[json.loads(x) for x in (BASE/(st+'_JOURNAL.jsonl')).read_text().splitlines()]
  if len(ev)!=16 or ev[0]['event']!='OWNER_START' or ev[-1]['event']!='OWNER_COMPLETE' or ev[-1]['result_sha256']!=rc['result_sha256'] or ev[-1]['status']!=status:raise AssertionError('Natural early closure')
  if not r['all_numerical_gates_passed'] or len(r['completed_cases'])!=14 or sum(map(len,r['stage_gates'].values()))!=78:raise AssertionError('Original early gate census')
  controls=[g for stage in r['stage_gates'].values() for g in stage]
 else:
  if rc['owner']['owner']!='root' or rc['owner']!=m['owner'] or r['manifest']!=m or rc['owner']['source_sha256']!=m['owner']['source_sha256']:raise AssertionError('Late owner/source')
  if not r['all_numerical_controls_passed'] or len(r['native_rows'])!=4 or len(r['numerical_controls'])!=259:raise AssertionError('Original late control census')
  controls=r['numerical_controls']
 if not all(g['passed'] is True for g in controls) or any(r['physical_flags'].values()):raise AssertionError('Parent controls/qualification')
 return r,rc,m

def finite_vector(v,n):
 if not isinstance(v,list) or len(v)!=n or any(type(x) not in (int,float) or not math.isfinite(x) for x in v):raise AssertionError('Complete finite copied vector')
def control(name,got,want,tol):
 e=abs(got-want)
 return dict(name=name,error=e,tolerance=tol,passed=bool(math.isfinite(e) and e<=tol))
def main():
 global OWNER
 if AUTHOR_DRAFT:raise RuntimeError('Guarded unexecuted draft')
 if list(BASE.glob(STEM+'_*')):raise FileExistsError('Unused own namespace required')
 for n,w in {**PINS,STEM+'.md':PROTOCOL_SHA}.items():seal(BASE/n,w)
 seal(__file__,sha(__file__))
 early,erc,em=closed(EARLY,'CONDITIONAL_FIXED_EPS_EARLY_CHAIN_ARITHMETIC_PASS');late,lrc,lm=closed(LATE,'NUMERICAL_PASS')
 OWNER=dict(owner='root',pid=os.getpid(),source_sha256=sha(__file__),started=now());tick=time.monotonic()
 manifest=dict(owner=OWNER,input_sha256=dict(INPUTS),parent_result_sha256={EARLY:erc['result_sha256'],LATE:lrc['result_sha256']},conditional_cross_covariance='zero cross-survey covariance assumed',physical_flags=FLAGS)
 publish(STEM+'_MANIFEST.json',manifest)
 native=next(x for x in late['native_rows'] if x['eps']==1e-5);AVAILABLE['native_old_shape_row']=native
 fixed=early['context']['fixed'];bf=late['baseline']['SN_baseline_copied_exactly']['fixed']
 if {**bf,'eps':native['eps']}!=fixed or fixed['eps']!=1e-5 or fixed['rG']!=.98/.99:raise AssertionError('Same selected EPS/full physical inventory')
 oldordinary=late['baseline']['predicted_ruler_BAO_copied_exactly']['manifest']['ordinary'];ordinary=early['context']['ordinary']
 if any(oldordinary[k]!=ordinary[k] for k in ('Hstar','Neff','T0','omega_b','YHe_old_fixture')):raise AssertionError('Same inherited ordinary thermal inventory')
 ds=late['baseline']['SN_baseline_copied_exactly']['data'];sn=next(x for x in native['SN_payload_copied_exactly']['profile_rows'] if x['arm']=='GAUSS32');sn16=next(x for x in native['SN_payload_copied_exactly']['profile_rows'] if x['arm']=='GAUSS16')
 if ds['selected_rows']!=1590 or ds['total_rows']!=1701 or len(set(ds['original_row_indices']))!=1590:raise AssertionError('Original selected SN identities')
 for prof in (sn,sn16):
  for k in ('magnitude_shape','residual','whitened_residual'):finite_vector(prof[k],1590)
  if not math.isfinite(prof['score']) or not math.isfinite(prof['magnitude_offset']):raise AssertionError('Finite copied SN scalar')
 bao=early['cases']['DESI']['data'];AVAILABLE['physical_ruler_BAO']=bao
 oldbao=late['baseline']['predicted_ruler_BAO_copied_exactly'];order=oldbao['manifest']['order']
 if len(oldbao['data'])!=13 or len(order)!=13 or len(oldbao['covariance'])!=13:raise AssertionError('Original full DESI schema')
 for row in oldbao['covariance']:finite_vector(row,13)
 for n in ('desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt','desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt'):
  p=str((BASE/n).resolve())
  if erc['inputs'][p]!=lrc['input_sha256'][n]:raise AssertionError('Same full DESI data/covariance bytes')
 ruler=early['cases']['ACOUSTIC_HALF']['data']['observables']['drag_ruler_Mpc_interval']
 if bao['ruler_Mpc_interval']!=ruler or len(ruler)!=2 or not 0<ruler[0]<ruler[1] or any(not math.isfinite(x) for x in ruler):raise AssertionError('Own finite physical ruler interval')
 for w in bao['score_witnesses']:
  for k in ('prediction','residual','whitened_residual'):finite_vector(w[k],13)
  if not math.isfinite(w['score']) or not ruler[0]<=w['ruler_Mpc']<=ruler[1]:raise AssertionError('Physical ruler witness')
 family=next(x for x in late['families'] if x['label']=='MATCHED_FIXED_RADIATION');arm=next(x for x in family['arms'] if x['SN_order']==32 and x['BAO_order']==96);ref=arm['best'];AVAILABLE['reference_best']=ref
 if family['primary'] is not True or late['manifest']['comparator_profiled_nuisance_count']!=3:raise AssertionError('Existing common-parameter comparator')
 for k in ('magnitude_shape','residual','whitened_residual'):finite_vector(ref['sn_readout'][k],1590)
 for k in ('prediction','residual','whitened_residual'):finite_vector(ref['bao_fit'][k],13)
 controls=[control('SN16_32_saved_score',sn16['score'],sn['score'],2e-6),control('reference_component_sum',ref['score'],ref['sn_score']+ref['bao_score'],1e-11),control('reference_SN_saved_score',ref['sn_score'],ref['sn_readout']['score'],1e-11),control('reference_BAO_saved_score',ref['bao_score'],ref['bao_fit']['score'],1e-11),control('physical_ruler_interval_saved_min',bao['score_interval'][0],min(w['score'] for w in bao['score_witnesses']),1e-11)]
 AVAILABLE['controls']=controls
 witnesses=[dict(ruler_Mpc=w['ruler_Mpc'],SN_score=sn['score'],BAO_score=w['score'],joint_score=sn['score']+w['score'],score_minus_reference=sn['score']+w['score']-ref['score'],BAO_payload_copied_exactly=w) for w in bao['score_witnesses']]
 sums=[sn['score']+x for x in bao['score_interval']]
 if len(witnesses)!=4 or not all(math.isfinite(x) for x in sums) or not sums[0]<=sums[1]:raise ArithmeticError('Finite saved sum interval')
 status='SAVED_ARITHMETIC_PASS' if all(g['passed'] for g in controls) else 'SAVED_ARITHMETIC_FAILED'
 result=dict(status=status,owner=OWNER,manifest=manifest,physical_flags=FLAGS,fixed=fixed,ordinary=ordinary,own_refined_YPCMB=early['cases']['BBN_PAIR']['data']['helium'],SN_data_registration=ds,SN_raw_metadata=late['baseline']['SN_baseline_copied_exactly']['raw_metadata'],DESI_order=order,physical_ruler_Mpc_interval=ruler,native_SN32_copied_exactly=sn,native_SN16_copied_exactly=sn16,native_physical_ruler_joint_score_interval=sums,score_minus_reference_interval=[x-ref['score'] for x in sums],physical_ruler_witnesses=witnesses,reference_best_copied_exactly=ref,old_native_free_BAO_scale_row_copied_exactly=native,parent_dispositions={EARLY:dict(status=early['status'],stage_gates=early['stage_gates'],physical_flags=early['physical_flags']),LATE:dict(status=late['status'],numerical_controls=late['numerical_controls'],physical_flags=late['physical_flags'])},ancestral_SN_dispositions_copied=late['baseline']['SN_flags_copied_exactly'],ancestral_NGC_dispositions_copied=late['baseline']['SN_baseline_copied_exactly']['original_NGC_flags_copied'],profiling=dict(native=['M'],reference=['Omega_m','M','Aref'],old_native_shape_reference=['M','Aref'],inherited_ordinary_calibrations=late['manifest']['inherited_ordinary_calibration_count'],exposure=late['manifest']['exposure']),controls=controls,elapsed_seconds=time.monotonic()-tick,scope='Conditional saved-score product; zero cross-survey covariance assumed; no ruler/parameter adoption/field replay/observational superiority')
 AVAILABLE['result']=result;recheck();rh=publish(STEM+'_RESULT.json',result)
 report='# Saved EPS1e-5 physical-ruler Pantheon + DESI score\n\n'+status+'\n\nNative physical-ruler score interval: '+repr(sums)+'\n\nExisting matched-radiation common-parameter reference: '+repr(ref['score'])+'\n\nNative M only; reference Omega_m+M+Aref. Adopted calibration/exposure and zero cross-survey covariance premise remain. No AIC, p-value, superiority or global EPS adoption.\n'
 ph=publish(STEM+'_REPORT.md',report.encode(),True);recheck()
 rc=dict(status='CLOSED',result_status=status,owner=OWNER,closed=now(),manifest_sha256=sha(BASE/(STEM+'_MANIFEST.json')),result_sha256=rh,report_sha256=ph,input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),physical_flags=FLAGS)
 publish(STEM+'_RECEIPT.json',rc);recheck()
 if read(STEM+'_RECEIPT.json')!=rc or set(p.resolve() for p in BASE.glob(STEM+'_*') if p.is_file())!=set(map(Path,OUTPUTS)):raise AssertionError('Closed receipt/runtime map')
 print(json.dumps(dict(status=status,joint_score_interval=sums,reference_score=ref['score'])),flush=True)
 return 0 if status=='SAVED_ARITHMETIC_PASS' else 3

def failure(exc):
 prior=BASE/(STEM+'_RECEIPT.json');error=dict(status='SAVED_ARITHMETIC_ERROR',owner=OWNER,error=repr(exc),traceback=traceback.format_exc(),available_context=repr(AVAILABLE),prior_receipt_sha256=sha(prior) if prior.exists() else None)
 if prior.exists():publish(STEM+'_POSTRECEIPT_ERROR.json',error);return
 publish(STEM+'_ERROR.json',error)
 for p in BASE.glob(STEM+'_*'):
  if p.is_file() and p.name!=STEM+'_RECEIPT.json':p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p)
 publish(STEM+'_RECEIPT.json',dict(status='CLOSED_ERROR',owner=OWNER,closed=now(),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),physical_flags=FLAGS))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or not args.root_owned:raise SystemExit('Guarded unexecuted source; root alone may release')
 if list(BASE.glob(STEM+'_*')):raise SystemExit('Existing runtime preserved; no resume')
 try:raise SystemExit(main())
 except Exception as exc:
  if OWNER is not None:failure(exc)
  raise
