"""Root-owned saved DIAGONAL physical-mode shape; no state/operator evolution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,sys,time
BASE=Path(__file__).resolve().parent
NAME='NATIVE_UNIFIED_PARENT_SAVED_PHYSICAL_MODE_THERMAL_SHAPE_V001'
REM='NATIVE_UNIFIED_PARENT_REDUCED_CORRELATION_REMAINDER_V001';PARENT='NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001'
TOL=1e-11;RELATIVE_FLOOR=1e-14;CASES=(('native',1.,.5),('feedback_off',1.,0.),('copy_off',0.,.5));MS=(8,12,16);KS=(0.,-.001,.001);TS=(0.,.25,.5,1.,2.)
PINS={REM+'_RESULT.json':'6e85cf97be74cc36185e929b333a929ec3a0367982041bd2aea64b7019b3c0b0',REM+'_RECEIPT.json':'1bfa3a4cb52d408ba1a88949826dd7622b27fc3245946bdf79f78bfcdba8ca21',
 'native_unified_parent_reduced_correlation_remainder_v001.py':'f66f37ef6a8bc86ade6fcb35bc2d576031ff17370b6f23526c36c9892f64fb37',REM+'.md':'2bca11d70888856b4b43489068bbeb3184cdf7066f34ef4b45ccb11843d0246a',
 PARENT+'_RESULT.json':'d2ad69ba985d5b5ef21ecd2caa687578231c621a79c0d4eb34cdefb344ad90d3',PARENT+'_RECEIPT.json':'91bc8a7feafdbf6bc72ab8e072e7a1575ae0641c64d9c8b91eb1c6c7e64dd073',
 'native_record_copy_canonical_maxwell_v001.py':'607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a',PARENT+'.md':'28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048',
 'NATIVE_UNIFIED_PARENT_PHYSICAL_MODE_MARGINAL_AND_THERMAL_ONSET_V001.md':'f97636a2851631cecbe215072f61082cd890334f9b48152e9ad174c7991854f7','PHYSICAL_MODE_PAIR_BUNCHING_ONSET_V001.md':'416ce614bde2d7bf89b0ec06c59261ee78165a5b5983c82c1e5004f516deb111',NAME+'.md':'e826529c95777419b9a48098659ca9a4c6e6cb6820e76b11ac0cbb4992a3a28c'}
OUTS=[BASE/(NAME+s) for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def finite(v):
 if type(v) in (str,int,bool,type(None)):return
 if type(v) is float:assert math.isfinite(v);return
 if type(v) is list:
  for x in v:finite(x)
  return
 assert type(v) is dict and all(type(k) is str for k in v)
 for x in v.values():finite(x)
def canonical(v):finite(v);return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(p,data):
 with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
def verify(source_hash):
 assert sha(__file__)==source_hash and not Path(__file__).stat().st_mode&0o222
 for n,h in PINS.items():assert sha(BASE/n)==h and not (BASE/n).stat().st_mode&0o222,n
 return dict(PINS,**{Path(__file__).name:source_hash})
def main():
 assert not any('PENDING' in v for v in PINS.values()) and sys.argv[1:]==['--root-owned'] and not any(p.exists() for p in OUTS)
 started=datetime.now(timezone.utc).isoformat();tick=time.monotonic();source_hash=sha(__file__);inputs=verify(source_hash)
 rem=json.loads((BASE/(REM+'_RESULT.json')).read_bytes());rr=json.loads((BASE/(REM+'_RECEIPT.json')).read_bytes())
 parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_bytes());pr=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_bytes())
 for name,data,receipt,src,count in ((REM,rem,rr,'native_unified_parent_reduced_correlation_remainder_v001.py',6345),(PARENT,parent,pr,'native_record_copy_canonical_maxwell_v001.py',3348)):
  finite(data);finite(receipt)
  assert data['owner']==receipt['owner']=='root' and data['PID']==receipt['PID'] and data['inputs']==receipt['inputs']
  assert data['source_sha256']==data['inputs'][src]==PINS[src] and receipt['outputs'][name+'_RESULT.json']==PINS[name+'_RESULT.json']
  assert data['status']==receipt['status']=='PASS' and data['failed']==receipt['failed']==0 and len(data['controls'])==count and all(type(c['passed']) is bool and c['passed'] for c in data['controls'])
  assert data['started_utc']==receipt['started_utc'] and datetime.fromisoformat(data['started_utc'])<=datetime.fromisoformat(data['finished_utc'])<=datetime.fromisoformat(receipt['closed_utc'])
  assert len(data['trials'])==27 and len(data['rows'])==135 and len(data['comparisons'])==90 and (receipt['trials'],receipt['states'],receipt['comparisons'])==(27,135,90)
 assert rr['controls']==6345 and rr['original_controls']==3348 and rr['component_controls']==3528 and pr['checks']==3348
 assert rem['original_controls']==parent['controls'] and len(rem['component_controls'])==3528 and all(c['passed'] for c in rem['component_controls'])
 assert rem['parent_physical_claims']==parent['physical_claims'] and all(v is False for v in rem['physical_claims'].values())
 assert rem['inputs'][PARENT+'_RESULT.json']==PINS[PARENT+'_RESULT.json'] and rem['inputs'][PARENT+'_RECEIPT.json']==PINS[PARENT+'_RECEIPT.json']
 expected={(c,k,M,t) for c,g,l in CASES for k in KS for M in MS for t in TS}
 original={(v['case'],v['kappa'],v['M'],v['tau']):v for v in parent['rows']};assert set(original)==expected and len(original)==len(parent['rows'])
 trials={(v['case'],v['kappa'],v['M']):(v['g'],v['lambda_R']) for v in rem['trials']}
 assert len(trials)==27 and trials=={(c,k,M):(g,l) for c,g,l in CASES for k in KS for M in MS}
 controls=[];rows=[];look={}
 def check(label,error,scale=1.,reason=None):
  scale=max(1.,float(scale));controls.append(dict(label=label,error=float(error),scale=scale,tolerance=TOL,passed=bool(math.isfinite(error) and error<=TOL*scale),reason=reason))
 for row in rem['rows']:
  key=(row['case'],row['kappa'],row['M'],row['tau']);assert key in expected and key not in look and set(row['methods'])=={'spectral','taylor'}
  M=row['M'];tag=':'.join(map(str,key));methods={}
  for method in ('spectral','taylor'):
   z=row['methods'][method];a=z['matrices']['rho_field'];assert set(a)=={'real','imag'} and all(len(a[k])==M+1 and all(len(v)==M+1 for v in a[k]) for k in a)
   diag=[a['real'][j][j] for j in range(M+1)];imag=[a['imag'][j][j] for j in range(M+1)]
   populations=[math.fsum(diag[j]/(j+1) for j in range(m,M+1)) for m in range(M+1)]
   trace=math.fsum(diag);local_trace=math.fsum(populations);local_mean=math.fsum(m*v for m,v in enumerate(populations));total=math.fsum(2*j*v for j,v in enumerate(diag));mu=total/4
   factorial=math.fsum(j*(j-1)*v for j,v in enumerate(diag))/3;local_factorial=math.fsum(m*(m-1)*v for m,v in enumerate(populations));thermal_factorial=2*mu*mu
   envelope=math.fsum(abs(v) for v in diag);mean_envelope=math.fsum(2*j*abs(v) for j,v in enumerate(diag));reason=None
   if mu>=0:
    r=mu/(1+mu);reference=[(1-r)*r**m for m in range(M+1)];tail=r**(M+1);signed=[a-b for a,b in zip(populations,reference)];distance=.5*(math.fsum(abs(v) for v in signed)+tail)
   else:r=reference=tail=signed=distance=None;reason='negative_raw_mean_reference_unavailable'
   relative=distance/mu if distance is not None and mu>RELATIVE_FLOOR else None
   relative_reason=None if relative is not None else (reason or 'raw_mean_not_above_1e-14')
   vals=dict(raw_diagonal=diag,raw_diagonal_imag=imag,raw_trace=trace,raw_trace_defect=trace-1.,raw_local_populations=populations,raw_local_trace=local_trace,raw_local_mean=local_mean,raw_total_mean=total,raw_factorial_moment=factorial,local_factorial_moment=local_factorial,thermal_factorial_reference=thermal_factorial,signed_factorial_minus_thermal=factorial-thermal_factorial,g2=factorial/(mu*mu) if mu>RELATIVE_FLOOR else None,g2_reason=None if mu>RELATIVE_FLOOR else 'raw_mean_not_above_1e-14',mu=mu,r=r,geometric_reference=reference,infinite_reference_tail=tail,signed_population_minus_reference=signed,raw_half_L1=distance,relative_raw_half_L1_over_mu=relative,relative_reason=relative_reason,reference_reason=reason)
   ptag=tag+':'+method;stats=z['scalars']
   check(ptag+':diagonal_imag',max(abs(v) for v in imag),envelope);check(ptag+':diagonal_nonnegative',max(0.,-min(diag)),envelope)
   check(ptag+':trace_saved_norm',abs(trace-stats['norm']),envelope);check(ptag+':local_trace',abs(local_trace-trace),envelope)
   check(ptag+':local_mean',abs(local_mean-mu),mean_envelope);check(ptag+':number_saved_remainder',abs(total-stats['photon_number']),mean_envelope)
   check(ptag+':norm_defect',abs(trace-1.),envelope);check(ptag+':geometric_sum',abs(math.fsum(reference)+tail-1.) if reference is not None else 0.,reason=reason)
   if reference is None:controls[-1]['passed']=False
   check(ptag+':factorial_identity',abs(local_factorial-factorial),math.fsum(j*(j-1)*abs(v) for j,v in enumerate(diag)))
   if method=='spectral':check(ptag+':original_number',abs(total-original[key]['number']),mean_envelope)
   methods[method]=vals
  a,c=methods['spectral'],methods['taylor'];pd=[x-y for x,y in zip(a['raw_local_populations'],c['raw_local_populations'])]
  scalars={k:a[k]-c[k] for k in ('raw_trace','raw_local_mean','raw_total_mean','mu','raw_factorial_moment','signed_factorial_minus_thermal')};scalars['raw_half_L1']=a['raw_half_L1']-c['raw_half_L1'] if a['raw_half_L1'] is not None and c['raw_half_L1'] is not None else None
  check(tag+':method_populations',max(abs(v) for v in pd),max(math.fsum(abs(v) for v in a['raw_local_populations']),math.fsum(abs(v) for v in c['raw_local_populations'])))
  check(tag+':method_scalars',max(abs(v) for v in scalars.values() if v is not None),max(1.,abs(a['raw_total_mean']),abs(c['raw_total_mean'])))
  relative_differences={v:a[v]-c[v] if a[v] is not None and c[v] is not None else None for v in ('g2','relative_raw_half_L1_over_mu')}
  out=dict(case=key[0],kappa=key[1],M=M,tau=key[3],methods=methods,method_difference=dict(populations=pd,scalars=scalars,relative_diagnostics=relative_differences));rows.append(out);look[key]=out
 assert set(look)==expected and len(rows)==135
 comparisons=[]
 for c,g,l in CASES:
  for k in KS:
   for lo,hi in ((8,12),(12,16)):
    for t in TS:
     methods={};tag=f'{c}:{k}:{lo}:{hi}:{t}'
     for method in ('spectral','taylor'):
      a=look[(c,k,lo,t)]['methods'][method];z=look[(c,k,hi,t)]['methods'][method];embedded=a['raw_local_populations']+[0.]*(hi-lo);dp=[x-y for x,y in zip(z['raw_local_populations'],embedded)]
      ds={v:z[v]-a[v] for v in ('raw_trace','raw_local_mean','raw_total_mean','mu','raw_factorial_moment','signed_factorial_minus_thermal')};ds['raw_half_L1']=z['raw_half_L1']-a['raw_half_L1'] if z['raw_half_L1'] is not None and a['raw_half_L1'] is not None else None
      check(tag+':'+method+':cutoff_populations',max(abs(v) for v in dp),max(1.,abs(a['raw_trace']),abs(z['raw_trace'])))
      check(tag+':'+method+':cutoff_scalars',max(abs(v) for v in ds.values() if v is not None),max(1.,abs(a['raw_total_mean']),abs(z['raw_total_mean'])))
      relative_differences={v:z[v]-a[v] if z[v] is not None and a[v] is not None else None for v in ('g2','relative_raw_half_L1_over_mu')}
      methods[method]=dict(signed_populations_high_minus_embedded_low=dp,high_marginal_tail=z['raw_local_populations'][lo+1:],signed_scalars_high_minus_low=ds,signed_relative_diagnostics_high_minus_low=relative_differences)
     comparisons.append(dict(case=c,kappa=k,M_low=lo,M_high=hi,tau=t,methods=methods))
 assert len(comparisons)==90 and len(controls)==3195 and verify(source_hash)==inputs
 failed=sum(not c['passed'] for c in controls);flags=dict(normalized_physical_distance_qualified=False,temperature_qualified=False,common_Planck_spectrum_qualified=False,whole_field_Gibbs_qualified=False,KMS_qualified=False,fluid_qualified=False,cosmology_qualified=False,physical_initial_state_qualified=False)
 result=dict(name=NAME,owner='root',PID=os.getpid(),started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,inputs=inputs,source_sha256=source_hash,status='PASS' if failed==0 else 'FAIL',failed=failed,controls=controls,rows=rows,comparisons=comparisons,trials=[dict(case=c,g=g,lambda_R=l,kappa=k,M=M) for c,g,l in CASES for k in KS for M in MS],relative_floor=RELATIVE_FLOOR,reference='raw geometric bare one-physical-mode shape; no normalization or temperature adoption',original_controls=parent['controls'],component_controls=rem['component_controls'],correlation_controls=rem['controls'],parent_physical_claims=parent['physical_claims'],component_physical_claims=rem['component_physical_claims'],correlation_physical_claims=rem['physical_claims'],physical_claims=flags)
 report=f'# Saved one-physical-mode shape\n\n{result["status"]}: {len(controls)-failed}/{len(controls)} arithmetic controls;27 trials,135 spectral/Taylor rows and90 cutoff pairs. Raw trace defects and every null are retained. Geometric reference is a bare marginal shape, not a temperature, common Planck spectrum, full-field Gibbs state or fluid closure. All inherited3348+3528+6345 dispositions remain unchanged.\n'
 for c,g,l in CASES:
  selected=[v for v in rows if v['case']==c and v['M']==16]
  for v in selected:
   z=v['methods']['spectral'];report+=f'\n{c} kappa={v["kappa"]} tau={v["tau"]}: mu={z["mu"]}; rawhalfL1={z["raw_half_L1"]}; relative={z["relative_raw_half_L1_over_mu"]}; factorial={z["raw_factorial_moment"]}; thermal_factorial={z["thermal_factorial_reference"]}; g2={z["g2"]}; trace_defect={z["raw_trace_defect"]}.\n'
 verify(source_hash);write(OUTS[0],canonical(result));write(OUTS[1],report.encode());verify(source_hash)
 receipt=dict(owner='root',PID=os.getpid(),started_utc=started,closed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,outputs={p.name:sha(p) for p in OUTS[:2]},status=result['status'],failed=failed,trials=27,states=135,comparisons=90,controls=3195,original_controls=3348,component_controls=3528,correlation_controls=6345)
 write(OUTS[2],canonical(receipt));assert verify(source_hash)==inputs and all(sha(BASE/n)==h for n,h in receipt['outputs'].items())
 print(json.dumps(dict(status=result['status'],failed=failed,controls=3195,result_sha256=sha(OUTS[0]),receipt_sha256=sha(OUTS[2]))));return 0 if failed==0 else 3
if __name__=='__main__':raise SystemExit(main())
