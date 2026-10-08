"""Saved-scalar conditional ADM constituent bounds; root execution only.
No constituent inversion, new state, pressure fluid, or producer import.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, time
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_SAVED_ADM_CONSTITUENT_BOUNDS_V001'
PARENT='CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001'
STEP=640
PROTOCOL_SHA='PENDING'
PINS={
 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001_FINE_CP_000640.json':'67d338a116ed28add27e021e434d97abd7460e98365b93fccb17e86d4ed16f34',
 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001_FINE_CP_000640_COMMIT.json':'e66feb94ace0e17ccb1d5e95d08ec972cc08da23fed1bc23ca5bbf5c181c7f1f',
 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001_MANIFEST.json':'a88e33ac8391f2d9eed1570358040447f088047e64417e4c9120396cc771b2f6',
 'constrained_u_k10_derived_full_common_continuation_v001.py':'90125e5ee7773dab985b3c3d9f26aafff4e56651752aed4fe733a582edf291d3',
 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001.md':'eed23fb57ed87d5c245283d01ba6ba34f7837c9ce2b3e3206e1c8e73c9ffcfb3',
 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md':'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0',
 'NATIVE_CARRIER_LINK_PHOTON_UNIFIED_CURRENT_MATCHING_UNITS_ADDENDUM_V001.md':'80c26b94eb4a2d310a8742cd88474d39c50c3a47e390cfe46ea125aa0ad58f6e',
 'NATIVE_LOCAL_PROPER_MATERIAL_NORMAL_AND_PHASE_SOURCE_MATCHING_V001.md':'40978c4874ea478c1ce03c7bfcaee0e8304f8bd1c80aebf0742282266209b64b',
 'CONSTRAINED_U_STABLE_ANGULAR_RADIATION_MEMORY_CHART_V001.md':'8471e9d40bb02dca8deed6dfc2bd49e1c4d1f00cd18af456b27df5082e62b04c',
 'CONSTRAINED_U_NONLINEAR_ADM_PHASE_CHARGE_INVERSION_AND_SOURCE_CONTACTS_V001.md':'c5cf5f19f6a7333d4f807a771bf7033b694924b28f5624980c5050fd8b7d5b82',
 'CONSTRAINED_U_SAVED_ADM_CONSTITUENT_BOUNDS_V001.md':'PENDING'
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

def write(name,v):
 finite(v);data=(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 p=BASE/name
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);return sha(p)

def read_json(name):
 p=BASE/name;data=p.read_bytes();v=json.loads(data);finite(v)
 assert data==(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 return v

def main():
 assert 'PENDING' not in PINS.values() and PINS[STEM+'.md']==PROTOCOL_SHA
 assert not any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json'))
 source_sha=sha(__file__);started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
 def authenticate():
  assert sha(__file__)==source_sha and not Path(__file__).stat().st_mode&0o222
  for name,h in PINS.items():assert sha(BASE/name)==h and not (BASE/name).stat().st_mode&0o222,name
 authenticate()
 name=PARENT+'_FINE_CP_'+str(STEP).zfill(6)+'.json';cp=read_json(name);commit=read_json(name[:-5]+'_COMMIT.json');manifest=read_json(PARENT+'_MANIFEST.json')
 assert set(cp)=={'lineage','owner','pid','group','nstep','xs','eta','incoming_binding','states','anchors','moments','snapshots','errors','trajectory_diagnostics','los_diagnostics','trace_integrals','trace_absolute_integrals','trace_initial_current','last_stages','optical_controls','initial_angular_errors','conformal_grid_error'}
 assert cp['lineage']==manifest and cp['owner']=='root' and cp['pid']==34057 and cp['group']=='FINE' and cp['nstep']==STEP
 assert manifest['source_sha256']==PINS['constrained_u_k10_derived_full_common_continuation_v001.py']
 assert commit==dict(lineage=manifest,owner='root',pid=cp['pid'],group='FINE',nstep=STEP,payload=name,sha256=PINS[name])
 assert [s['nstep'] for s in cp['snapshots']]==list(range(0,STEP+1,64)) and len(cp['snapshots'])==11
 assert len(cp['states'])==len(cp['anchors'])==len(cp['last_stages'])==4 and all(len(s)==84 for s in cp['states'])
 assert cp['states']==[s['stable_state'] for s in cp['snapshots'][-1]['cases']]
 assert len(cp['xs'])==len(cp['eta'])==2049 and all(cp['xs'][i]<cp['xs'][i+1] and cp['eta'][i]<cp['eta'][i+1] for i in range(2048))
 for arm in range(4):
  assert len(cp['anchors'][arm])==STEP+1 and cp['anchors'][arm][-1]['x']==cp['xs'][STEP] and cp['anchors'][arm][-1]['eta']==cp['eta'][STEP]
  keys={'x','eta','R','qV','cGamma','Gamma','dipole','Pi'}
  assert set(cp['anchors'][arm][0])==keys
  for j,row in enumerate(cp['anchors'][arm][1:],1):
   assert set(row)==keys|{'panel_nodes','panel_envelopes'} and row['x']==cp['xs'][j] and row['eta']==cp['eta'][j]
   assert len(row['panel_nodes'])==4 and len(row['panel_envelopes'])==3 and all(v>=0 for v in row['panel_envelopes'])
   assert all(set(v)==keys for v in row['panel_nodes']) and all(row['panel_nodes'][k]['x']<row['panel_nodes'][k+1]['x'] and row['panel_nodes'][k]['eta']<row['panel_nodes'][k+1]['eta'] for k in range(3))
   assert row['panel_nodes'][0]=={k:cp['anchors'][arm][j-1][k] for k in keys} and row['panel_nodes'][-1]=={k:row[k] for k in keys}
  assert cp['last_stages'][arm]['states'][-1]==cp['states'][arm] and cp['last_stages'][arm]['coordinates'][-1]==cp['xs'][STEP] and cp['last_stages'][arm]['conformal'][-1]==cp['eta'][STEP]
  assert len(cp['last_stages'][arm]['states'])==len(cp['last_stages'][arm]['algebraic_states'])==3 and all(len(v)==84 for v in cp['last_stages'][arm]['states']) and all(len(v)==2 for v in cp['last_stages'][arm]['algebraic_states'])
 eps=manifest['fixed']['eps'];assert eps>0
 cap=math.sqrt(1+eps);csmax=eps/(4+3*eps+4*cap);rows=[]
 for frame in cp['snapshots']:
  assert set(frame)=={'nstep','cases'} and len(frame['cases'])==4
  for arm,case in enumerate(frame['cases']):
   assert len(case['stable_state'])==84 and len(case['readouts'])==15 and case['x']==cp['xs'][frame['nstep']]
   assert case['physical_seed_qualified'] is case['old_failure_flags_changed'] is False
   heads=case['domain_heads'];qb=case['background']['qbar'];velocity=heads['phase_velocity']
   assert qb>=1 and type(heads['inside_sampled_linear_domain']) is bool
   eta2=(qb*velocity)**2;root=math.sqrt(1+eta2)
   energy_upper=eta2/(root+1);energy_lower=eta2/(math.sqrt(cap*cap+eta2)+cap)
   density_deficit_upper=eta2/(root*(root+1));streaming_upper=eta2/root
   row=dict(nstep=frame['nstep'],arm=arm,omega=manifest['omega'][arm],a=case['a'],qbar=qb,signed_phase_velocity=velocity,
    linear_dictionary_p2_over_Q0_squared=eta2,energy_increment_lower_per_positive_shifted_charge_Q0=energy_lower,
    energy_increment_upper_per_positive_shifted_charge_Q0=energy_upper,constituent_density_deficit_upper_per_positive_shifted_charge=density_deficit_upper,
    streaming_stress_upper_per_positive_shifted_charge_Q0=streaming_upper,pressure_deficit_upper_per_positive_shifted_charge_Q0=csmax*energy_upper,
    preserved_domain_heads=heads,preserved_physical_seed_qualified=case['physical_seed_qualified'],preserved_old_failure_flags_changed=case['old_failure_flags_changed'])
   finite(row);assert 0<=energy_lower<=energy_upper and 0<=density_deficit_upper<1 and streaming_upper>=0
   rows.append(row)
 assert len(rows)==44
 summaries=[]
 for arm in range(4):
  arm_rows=[v for v in rows if v['arm']==arm];peaks={}
  for key in ('linear_dictionary_p2_over_Q0_squared','energy_increment_upper_per_positive_shifted_charge_Q0','constituent_density_deficit_upper_per_positive_shifted_charge','streaming_stress_upper_per_positive_shifted_charge_Q0','pressure_deficit_upper_per_positive_shifted_charge_Q0'):
   peak=max(arm_rows,key=lambda v:v[key]);peaks[key]=dict(value=peak[key],nstep=peak['nstep'],a=peak['a'])
  old=max(arm_rows,key=lambda v:v['preserved_domain_heads']['phase_square_over_gap'])
  summaries.append(dict(arm=arm,omega=manifest['omega'][arm],conditional_bound_maxima=peaks,old_phase_square_over_gap_maximum=dict(value=old['preserved_domain_heads']['phase_square_over_gap'],nstep=old['nstep'],a=old['a']),all_preserved_first_order_inside_flags=all(v['preserved_domain_heads']['inside_sampled_linear_domain'] for v in arm_rows)))
 flags=dict(conditional_bounds_only=True,linear_gradient_dictionary_disclosed=True,positive_held_shifted_charge_is_a_premise=True,shifted_charge_positivity_qualified=False,second_order_Cauchy_completion_qualified=False,full_reaction_native_Hilbert_state_qualified=False,exact_nonlinear_domain_qualified=False,nonlinear_trajectory_qualified=False,original_failure_flags_changed=False,global_continuation_qualified=False)
 result=dict(status='SAVED_CONDITIONAL_ADM_CONSTITUENT_BOUND_READOUT',owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,source_sha256=source_sha,input_sha256=PINS,checkpoint_root_pid=cp['pid'],checkpoint_nstep=STEP,checkpoint_group='FINE',frame_count=11,row_count=44,eps=eps,Qcap_over_Q0=cap,sound_speed_squared_maximum=csmax,gradient_dictionary='p²/Q0²=qbar²*(qV)²; p_i=-Q V_i is the disclosed linear reconstruction, not an exact nonlinear Cauchy slice',positive_shifted_charge_scope='Held qtilde=Pi/sqrt(gamma)+M²C N sigma^t >0; its value, positivity and reaction completion are not derived from these snapshots',normalizations='Conditional per unit qtilde Q0 (energy/stress) or qtilde (number); no actual energy difference or density inversion is performed',rows=rows,summaries=summaries,preserved_running_diagnostics=cp['errors'],flags=flags)
 authenticate();rh=write(STEM+'_RESULT.json',result)
 report='# Saved conditional ADM constituent bounds V001\n\nFixed FINE CP640,11 frames,four arms,44 saved-scalar rows. Exact conditional constituent bounds use a disclosed linear gradient dictionary and positive held shifted charge. The charge premise and full nonlinear/native/reaction state are unearned. All old heads and failure/physical flags remain unchanged. No new physical success gate or global continuation qualification is introduced.\n'
 for row in summaries:report+='\nOmega '+str(row['omega'])+': conditional energy-bound maximum '+str(row['conditional_bound_maxima']['energy_increment_upper_per_positive_shifted_charge_Q0']['value'])+' per positive held qtilde Q0; preserved phase-square/gap maximum '+str(row['old_phase_square_over_gap_maximum']['value'])+'. These are different diagnostics, not a qualified physical state.\n'
 rp=BASE/(STEM+'_REPORT.md')
 with rp.open('xb') as f:f.write(report.encode())
 rp.chmod(0o444);report_sha=sha(rp);authenticate()
 write(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=source_sha,input_sha256=PINS,result_sha256=rh,report_sha256=report_sha,status=result['status']))
 assert sha(BASE/(STEM+'_RESULT.json'))==rh and sha(rp)==report_sha;authenticate()
 print(json.dumps(dict(status=result['status'],result_sha256=rh,receipt_sha256=sha(BASE/(STEM+'_RECEIPT.json')))),flush=True)
 return 0
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root-owned',action='store_true',required=True);p.parse_args()
 if 'AUTHOR_DRAFT' in Path(__file__).name:raise SystemExit('Mutable author draft is not a numerical entry point')
 raise SystemExit(main())
