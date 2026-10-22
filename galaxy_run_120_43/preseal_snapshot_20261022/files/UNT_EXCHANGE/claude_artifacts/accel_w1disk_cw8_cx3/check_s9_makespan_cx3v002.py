"""0818: pure synthetic selection and arithmetic timing model; no run data or scientific execution."""
from pathlib import Path
import ast,copy,hashlib,json,math,subprocess,itertools
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');P=A/'accel_w1disk_cw8_cx3'
C=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
sources={
'DISPATCH':A.parent/'FROM_CODEX/0818_2026-10-21_codex3_S9_makespan_cw1_vs_cw8.md',
'PRIOR_REPORT':P/'LANE_B_CX3V001.md',
'V006':C/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md',
'A133':C/'A133_TWO_PHASE_PROTOCOL_V001.md',
'PHASE1':A/'phase1_c2/phase1_c2v003b.py',
'FREEZE':A/'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
'P112':A/'phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py',
'RUNBOOK':A/'runbook_v002_c2v007_cx2/RUNBOOK_V002_C2V007.md',
'ESTIMATE':A/'ngc_point_producer_c4/ri45_12/estimate/ESTIMATE_RI45_12_NGC_K32_C4V002.json',
'ESTIMATE_VERIFY':A/'ngc_point_producer_c4/ri45_12/verify/VERIFY_RI45_12_C4V001.md',
'CORE':A/'calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py',
'S1_LIB':A/'s1_successors_c2/s1_path_lib_c2v002c.py',
'S45_CONFIG':A/'sched_s45_c2/v004/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004.json',
'CHECKER':Path(__file__).resolve(),
}
raw={k:p.read_bytes() for k,p in sources.items()}
sha=lambda b:hashlib.sha256(b).hexdigest()
pins={k:{'path':str(p),'sha256':sha(raw[k]),'bytes':len(raw[k])} for k,p in sources.items()}
stamp=subprocess.check_output(['date','-u'],text=True).strip()
checks=[]
def ck(n,c,detail=None):
 checks.append({'name':n,'pass':bool(c),'class':'TESTED_SYNTHETIC_OR_ARITHMETIC','detail':detail})
 if not c:raise AssertionError(n)
# Pure freeze selection function, supplied only invented admitted-point projections.
tree=ast.parse(raw['FREEZE']);ns={'math':math,'ROLE_HULL':'hull','ROLE_ANCHOR':'anchor','ROLE_CENTROID':'centroid_nearest','ROLE_INTERIOR':'interior'}
names=['_evenly_spaced_indices','_selection_plan']
nodes=[copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)) for name in names]
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(sources['FREEZE']),'exec'),ns)
pts=[(0,[0.,0.,0.])]
for j in range(3):
 v=[0.,0.,0.];v[j]=1.;pts.append((1+j,v))
for j in range(3):
 v=[0.,0.,0.];v[j]=-1.;pts.append((4+j,v))
countrows=[]
for mask in range(64):
 adm=[pts[0]]+[pts[i+1] for i in range(6) if mask&(1<<i)]
 sel=ns['_selection_plan'](adm,3,0,5);selected={i for i,_ in sel};F={1,2,3}
 union=selected|F;reuse=union&{0,1,2,3};new=union-reuse
 expected_minus={i for i in [4,5,6] if any(p[0]==i for p in adm)}
 ck('nominal_seed_selection_mask_%02d'%mask, new==expected_minus and reuse=={0,1,2,3} and len(union)==4+len(expected_minus))
 countrows.append({'admitted_mask':mask,'n_members':len(sel),'n_total_calls':len(union),'n_S0_reused':len(reuse),'n_new':len(new)})
# Exact general combinatorial upper bound at m_id<=3, interior=5, no assertion all points exist.
ck('selection_general_upper_bound',2*3+1+1+5+3==16)
est=json.loads(raw['ESTIMATE']);rows=[]
for scenario in ['E','U']:
 serial=est['serial']['point_h'][scenario]
 p8=est['column_workers_8']['point_h'][scenario]
 readout=est['serial']['readout_after_convergence_s'][scenario]/3600
 a8=est['column_workers_8']['route_a_tree_h'][scenario]-readout
 # Frozen report tables round to .01h. Preserve that accuracy in scheduling inputs.
 a8=round(a8,2);tail=round(p8-a8,2)
 for reserve in [0,2,4,6]:
  B=18-reserve
  for n in [1,2,3]:
   n_batches=math.ceil(n//1/(B//8))
   all8=round(n_batches*a8+tail,2)
   best=min(serial,all8)
   row={'scenario':scenario,'n_new':n,'fixed_other_cpu_units':reserve,'available_units':B,'cw8_A_loop_h':a8,'cw8_serial_tail_h':tail,'all_cw1_h':serial,'all_cw8_h':all8,'best_model_h':best,'best_mode':'all_cw8' if all8<serial else 'all_cw1','best_saving_h':round(serial-best,2),'E_half_day_gate_met':scenario=='E' and serial-best>=12}
   rows.append(row)
   # For n<=3 and B>=12, earlier completed A phases leave <=2 1-unit tails;
   # each successive A batch still fits. Any mixed assignment retaining >=1 fresh
   # cw1 job has completion >= serial, while all-cw1 is feasible (n<=3<=B).
   ck('model_capacity_%s_q%d_n%d'%(scenario,reserve,n),8*(B//8)<=B and (n-1)+8<=B)
 for key in ['E','U']:
  pass
ck('no_E_case_meets_12h',all(not r['E_half_day_gate_met'] for r in rows))
ck('favorable_E_bound_below_gate',est['serial']['point_h']['E']-est['column_workers_8']['point_h']['E']<12)
ck('U_onecall_saving',round(est['serial']['point_h']['U']-est['column_workers_8']['point_h']['U'],2)==32.92)
# Metadata only; current source requires 8 DDO route-A workers, S1 build changes no worker leaf.
core=ast.parse(raw['CORE']);validate=next(n for n in core.body if isinstance(n,ast.FunctionDef) and n.name=='validate_block')
ck('DDO_CORE_requires_routeA_8',"block['route_a'].get('column_workers') != 8" in ast.unparse(validate))
s1=ast.parse(raw['S1_LIB']);build=next(n for n in s1.body if isinstance(n,ast.FunctionDef) and n.name=='build_case')
ck('S1_build_no_worker_assignment',not any(isinstance(n,ast.Subscript) and isinstance(n.ctx,ast.Store) and 'column_workers' in ast.unparse(n) for n in ast.walk(build)))
cfg=json.loads(raw['S45_CONFIG'])
ck('pinned_S45_block_cw8',cfg['numerics']['block']['route_a']['column_workers']==8)
summary={'date_u':stamp,'classification':'FORMAL conditional scheduling model, TESTED arithmetic/synthetic metadata only','sources':pins,'host':{'logical_cpus':18,'RAM_GiB':128,'basis':'0818 root statement; direct sysctl hw.ncpu hw.memsize in this sandbox returned Operation not permitted, not independently measured here'},'actual_roster':{'exact_count':None,'reason':'No actual post-B_P1 selection/FDPLAN/P112 config was supplied; source membership depends on future admitted data. No production run tree read.','formula':'n_unique = |keys(M) union keys(F)|; n_new = n_unique minus exact verified reusable S0 identities','expected_nominal_seed_case':{'n_total':[4,5,6,7],'n_reused_S0':4,'n_new':[0,1,2,3]},'general_source_upper_bound_distinct_before_reuse':16,'terminal_or_zero_identified_case_new_calls':0},'nominal_seed_synthetic_cases':countrows,'contention_model':{'capacity':18,'cw1_CPU_units':1,'cw8_A_loop_CPU_units':8,'readout_routeB_CPU_units':1,'fixed_other_units':[0,2,4,6],'common_delay_h':'T, if needed to leave S8 route A; cancels in like-for-like table','S0_remaining_h':'R: total S9 = T + max(R, tabulated new-call duration); S8/seal/acceptance can further mask gains','limits':'18 equal scheduling units is an explicit optimistic model, not a macOS performance measurement; CPU type/QoS/tail-build/I/O contention not known. Tables cover 0-3 newly needed calls in expected nominal seed path. All cw8 means every new call, not relaunching old S0.'},'model_rows':rows,'checks':checks,'n_pass':len(checks),'decision':'0.5 d E build gate NOT_SHOWN; no cw8 build justified on these inputs; no new physics/custody changes recommended','UNTESTED':['exact production roster','actual S0 remaining times','actual S8 staged CPU demand/duration','measured cw8 runtime','phase-wide contention and S10 completion','actual pair/adoption/launch closure']}
p=P/'S9_MAKESPAN_EVIDENCE_CX3V002.json'
with p.open('x') as f:json.dump(summary,f,indent=2,sort_keys=True);f.write('\n')
print(p.name,sha(p.read_bytes()),p.stat().st_size,'checks',len(checks))
for x in rows:
 if x['fixed_other_cpu_units'] in [2,6]:print(x['scenario'],x['fixed_other_cpu_units'],x['n_new'],x['all_cw1_h'],x['all_cw8_h'],x['best_saving_h'])
