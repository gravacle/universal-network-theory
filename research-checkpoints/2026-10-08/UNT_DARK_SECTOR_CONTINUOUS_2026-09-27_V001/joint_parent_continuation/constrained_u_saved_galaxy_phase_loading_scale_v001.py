"""Saved same-action phase-loading scales; root-owned scalar reader only.
No producer import, background root, mode state, source fit or trajectory.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, time
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_SAVED_GALAXY_PHASE_LOADING_SCALE_V001'
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005'
CURRENT='CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001'
CP_KM_S=299792.458
LENGTHS_KPC=(1.,5.,10.,20.,44.)
TOL=1e-12
PROTOCOL_SHA='df999d6e04b300a78cf87674f37ac47b3c8752bec113c629cf6dbe2b80249b95'
PINS={
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005_RESULT.json':'cf005bce78fcd7358c37f6bb53051128b02bf764c1dd8f346d410864931d6c27',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005_RECEIPT.json':'dddb4e40e9dc9c5148245a6d35670cf173b989d61f1fd0d6fe3e9a6e9705f697',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005_MANIFEST.json':'628f483e8d945ce178af88088c85ed6cca5ba29a4b2e23cd21cd7565bf82e3b6',
 'constrained_u_clock_gradient_early_transfer_v005.py':'bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005.md':'027233e02902b2905a5f172e3aaec6ab297a956e5e66a1f058ffbb36f66c93a6',
 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001_MANIFEST.json':'a88e33ac8391f2d9eed1570358040447f088047e64417e4c9120396cc771b2f6',
 'constrained_u_k10_derived_full_common_continuation_v001.py':'90125e5ee7773dab985b3c3d9f26aafff4e56651752aed4fe733a582edf291d3',
 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001.md':'eed23fb57ed87d5c245283d01ba6ba34f7837c9ce2b3e3206e1c8e73c9ffcfb3',
 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md':'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0',
 'NATIVE_CARRIER_LINK_PHOTON_UNIFIED_CURRENT_MATCHING_UNITS_ADDENDUM_V001.md':'80c26b94eb4a2d310a8742cd88474d39c50c3a47e390cfe46ea125aa0ad58f6e',
 'NATIVE_LOCAL_PROPER_MATERIAL_NORMAL_AND_PHASE_SOURCE_MATCHING_V001.md':'40978c4874ea478c1ce03c7bfcaee0e8304f8bd1c80aebf0742282266209b64b',
 'CONSTRAINED_U_RETARDED_GALAXY_PHASE_LOADING_AND_STATIC_POLE_V001.md':'d805c0dc291d383495703360d034836432d3b3ebd42e1839a97504de79793478',
 'CONSTRAINED_U_SAVED_GALAXY_PHASE_LOADING_SCALE_V001.md':'df999d6e04b300a78cf87674f37ac47b3c8752bec113c629cf6dbe2b80249b95'
}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def finite(v):
 if v is None or type(v) in (str,bool,int):return
 if type(v) is float:assert math.isfinite(v);return
 if type(v) is list:
  for x in v:finite(x)
  return
 assert type(v) is dict and all(type(k) is str for k in v)
 for x in v.values():finite(x)

def read_json(name):
 data=(BASE/name).read_bytes();v=json.loads(data);finite(v)
 assert data==(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 return v

def write(name,v):
 finite(v);data=(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();p=BASE/name
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);return sha(p)

def main():
 assert 'PENDING' not in PINS.values() and PINS[STEM+'.md']==PROTOCOL_SHA
 assert not any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json'))
 source_sha=sha(__file__);started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
 def authenticate():
  assert sha(__file__)==source_sha and not Path(__file__).stat().st_mode&0o222
  for name,h in PINS.items():assert sha(BASE/name)==h and not (BASE/name).stat().st_mode&0o222,name
 authenticate();parent=read_json(PARENT+'_RESULT.json');receipt=read_json(PARENT+'_RECEIPT.json')
 old=read_json(PARENT+'_MANIFEST.json');current=read_json(CURRENT+'_MANIFEST.json')
 assert parent['manifest']==old==receipt['lineage'] and old['source_sha256']==PINS['constrained_u_clock_gradient_early_transfer_v005.py']
 assert receipt['manifest_sha256']==PINS[PARENT+'_MANIFEST.json'] and receipt['result_sha256']==PINS[PARENT+'_RESULT.json']
 assert parent['status']==receipt['status']=='NEW_EARLY_TRANSFER_ARITHMETIC_FAILED' and parent['all_numerical_gates_passed'] is False
 assert current['source_sha256']==PINS['constrained_u_k10_derived_full_common_continuation_v001.py']
 assert set(old['fixed'])==set(current['fixed']) and all(old['fixed'][k]==current['fixed'][k] for k in old['fixed'] if k!='k_Mpc_inverse')
 assert old['fixed']['k_Mpc_inverse']==.01 and current['fixed']['k_Mpc_inverse']==10.
 literals=[]
 for node in ast.parse((BASE/'constrained_u_clock_gradient_early_transfer_v005.py').read_text()).body:
  if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Tuple) and [v.id for v in node.targets[0].elts]==['KB','C','CBAR']:
   literals.append(ast.literal_eval(node.value))
 assert literals==[(.02,1.98,.99)];KB,C,CBAR=literals[0]
 assert C==2-KB and CBAR==C/2 and CBAR==.99
 labels=['BASE','TIME','MODES','HIERARCHY','START','ATOMIC','THIN'];assert [v['label'] for v in parent['rows']]==labels
 gates=parent['numerical_gates'];assert len(gates)==527 and all(type(g['passed']) is bool for g in gates)
 assert sum(not g['passed'] for g in gates)==28
 backgrounds=[];endpoint_heads=[]
 for trial in parent['rows']:
  assert len(trial['snapshots'])==68 and trial['snapshots'][-1]['x']==0. and len(trial['snapshots'][-1]['cases'])==4
  for arm,case in enumerate(trial['snapshots'][-1]['cases']):
   assert case['a']==1. and case['x']==0. and case['background']['a']==1.
   backgrounds.append(case['background']);endpoint_heads.append(dict(trial=trial['label'],arm=arm,domain_heads=case['domain_heads']))
 bg=backgrounds[0];assert len(backgrounds)==28 and all(v==bg for v in backgrounds)
 w,cs2=bg['w'],bg['cs'];assert w>0 and cs2>0
 hs=old['fixed']['Hunit'];ell=old['fixed']['ell_native'];assert hs>0 and ell>0
 dnorm=w/cs2;kj2=2*dnorm/C;ell2=ell*ell
 xcrit=(kj2+math.sqrt(kj2*kj2+4*kj2/ell2))/2
 qcrit=math.sqrt(xcrit);qcrit_Mpc=qcrit*hs/CP_KM_S;kj_Mpc=math.sqrt(kj2)*hs/CP_KM_S
 inverse_kpc=1000/qcrit_Mpc;wavelength_kpc=2*math.pi*inverse_kpc
 controls=[]
 def check(name,err):controls.append(dict(name=name,error=float(err),tolerance=TOL,passed=bool(math.isfinite(err) and err<=TOL)))
 check('bare_density_factor_two',abs(C*kj2-2*dnorm)/(2*dnorm))
 check('positive_quadratic_root',abs(ell2*xcrit*xcrit-kj2*ell2*xcrit-kj2)/(ell2*xcrit*xcrit+kj2*ell2*xcrit+kj2))
 check('critical_loading_equality',abs(xcrit*(ell2*xcrit/(1+ell2*xcrit))-kj2)/kj2)
 check('physical_ell_100pc',abs(ell*CP_KM_S/hs-1e-4)/1e-4)
 rows=[]
 for length in LENGTHS_KPC:
  q=CP_KM_S/(hs*(length/1000));y=ell2*q*q;mu=y/(1+y)
  gradient=q*q*mu;ratio=kj2/gradient;coefficient=dnorm-C*gradient/2
  check('normalized_source_coefficient_'+str(length)+'kpc',abs(coefficient-(-C/2)*(gradient-kj2))/(dnorm+C*gradient/2))
  rows.append(dict(inverse_wavenumber_kpc=length,q_over_Hstar=q,physical_wavenumber_Mpc_inverse=1000/length,
   ordinary_wavelength_kpc=2*math.pi*length,F0=1/(1+y),gradient_mu=mu,gradient_q2_mu=gradient,
   loading_kJ2=kj2,load_over_gradient=ratio,gradient_minus_loading=gradient-kj2,
   normalized_baryon_source_per_Phi=coefficient,full_GN_operator_mu=mu-kj2/(q*q)))
 assert len(controls)==9 and len(rows)==5;qualified=all(g['passed'] for g in controls)
 flags=dict(saved_background_scalar_arithmetic_only=True,plane_wave_inverse_length_is_not_galaxy_radius=True,
  imposed_metric_frozen_H0_static_scope=True,local_common_metric_Poisson_premises_qualified=False,physical_parameter_changed=False,parent_failure_flags_changed=False,
  background_trajectory_qualified=False,galaxy_solution_qualified=False,dynamical_galaxy_response_qualified=False,
  full_GR_stability_qualified=False,observational_fit_qualified=False,physical_state_qualified=False)
 result=dict(status='SAVED_PHASE_LOADING_SCALE_ARITHMETIC_PASS' if qualified else 'SAVED_PHASE_LOADING_SCALE_ARITHMETIC_FAILED',
  owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,
  source_sha256=source_sha,input_sha256=PINS,fixed=old['fixed'],KB=KB,C=C,Cbar=CBAR,Gbare_over_GN=CBAR,cp_km_s=CP_KM_S,
  saved_present_background=bg,present_background_copies=28,density_unit='rho_star=2 Mbare^2 Hstar^2',
  Dnorm=dnorm,kJ_squared_over_Hstar_squared=kj2,kJ_Mpc_inverse=kj_Mpc,qcrit_squared_over_Hstar_squared=xcrit,
  qcrit_Mpc_inverse=qcrit_Mpc,inverse_qcrit_kpc=inverse_kpc,ordinary_wavelength_at_qcrit_kpc=wavelength_kpc,
  static_equation='(Dnorm−C*q^2*mu/2)*Phi=delta_rho_b/(2*Mbare^2*Hstar^2); mu=ell^2*q^2/(1+ell^2*q^2)',
  GN_matching='Mbare^2*C=2*MN^2; no additional .99 density or force rescaling',rows=rows,controls=controls,
  arithmetic_qualified=qualified,preserved_parent_status=parent['status'],preserved_parent_all_numerical_gates_passed=parent['all_numerical_gates_passed'],
  preserved_parent_numerical_gates=gates,preserved_all_28_endpoint_domain_heads=endpoint_heads,flags=flags)
 authenticate();rh=write(STEM+'_RESULT.json',result)
 report='# Saved galaxy phase-loading scale V001\n\nSaved a=1 background, all28 identical copies. Nine arithmetic controls; every original527 disposition and28 failures retained. Frozen H0 linear no-incoming operator only. Fixed inverse plane-wave lengths1,5,10,20,44kpc are not galaxy radii or a fitted source. Full GR stability, background/galaxy/state qualification remain false.\n'
 report+='\nkJ²/Hstar²='+str(kj2)+'; inverse qcrit='+str(inverse_kpc)+'kpc; ordinary2pi/qcrit wavelength='+str(wavelength_kpc)+'kpc.\n'
 for row in rows:report+='\nInverse plane-wave length '+str(row['inverse_wavenumber_kpc'])+'kpc: load/gradient='+str(row['load_over_gradient'])+'; signed full-GN operator coefficient='+str(row['full_GN_operator_mu'])+'.\n'
 rp=BASE/(STEM+'_REPORT.md')
 with rp.open('xb') as f:f.write(report.encode())
 rp.chmod(0o444);report_sha=sha(rp);authenticate()
 write(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=source_sha,input_sha256=PINS,result_sha256=rh,report_sha256=report_sha,status=result['status']))
 assert sha(BASE/(STEM+'_RESULT.json'))==rh and sha(rp)==report_sha;authenticate()
 print(json.dumps(dict(status=result['status'],result_sha256=rh,receipt_sha256=sha(BASE/(STEM+'_RECEIPT.json')))),flush=True)
 return 0 if qualified else 3
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root-owned',action='store_true',required=True);p.parse_args()
 raise SystemExit(main())
