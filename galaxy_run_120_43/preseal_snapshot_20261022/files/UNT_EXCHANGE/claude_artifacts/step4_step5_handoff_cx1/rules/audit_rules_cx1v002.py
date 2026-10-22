"""0631 source-only audit; executes extracted pure classifier on invented numbers only."""
import ast, hashlib, json, math, subprocess, functools, inspect
from pathlib import Path
import numpy as np
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUT=ROOT/'step4_step5_handoff_cx1/rules'
paths={
'authority':Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md'),
'dispatch':ROOT.parent/'FROM_CODEX/0631_2026-10-18_codex1_step4_to_step5_handoff_pipelining.md',
'wrapper':ROOT/'calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py',
'core':ROOT/'calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py',
'parent':ROOT/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
'engine':ROOT/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py',
'freeze':ROOT/'calibration_engine_freeze_v003b_v003d/prediction_freeze_c2v003d.py',
'coordinates':ROOT/'calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json',
'coordinate_addendum':ROOT/'calib_tail_readiness_cx2/COORDINATE_ADDENDUM_CX2V006.json',
'config':ROOT/'calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json',
'c4_inventory':ROOT/'step4_launch_readiness_c4/inventory/INVENTORY_C4V001.json',
'c4_order':ROOT/'step4_launch_readiness_c4/launch_order/LAUNCH_ORDER_C4V001.md',
'c4_root_items':ROOT/'step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V001.md',
'filler':ROOT/'step5_ngc_route_ab_readiness_cx3/tools/fill_step5_cx3v003.py',
'filler_contract':ROOT/'step5_ngc_route_ab_readiness_cx3/HANDOFF_CONTRACT_CX3V002.md',
'filler_policy':ROOT/'step5_ngc_route_ab_readiness_cx3/POLICY_CX3V001.json',
'filler_root_items':ROOT/'step5_ngc_route_ab_readiness_cx3/ROOT_ITEMS_CX3V002.json',
'self':Path(__file__)}
raw={k:p.read_bytes() for k,p in paths.items()}
pins={k:{'path':str(paths[k]),'sha256':hashlib.sha256(b).hexdigest()} for k,b in raw.items()}
names={'_fail_closed','_safe_str','_is_bool','_is_number','_finite_float','_is_true','classify_prediction'}
tree=ast.parse(raw['engine']); body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
assert {n.name for n in body}==names
namespace={'math':math,'np':np,'functools':functools,'inspect':inspect}
exec(compile(ast.Module(body=body,type_ignores=[]),str(paths['engine']),'exec'),namespace)
f=namespace['classify_prediction']; rows=['invented_A','invented_B']; rect={'invented_A':[1.,2.],'invented_B':[3.,4.]}
def evaluate(a,b,valid=True):return f(prediction={'valid':valid,'speeds_km_s':{'invented_A':a,'invented_B':b}},rectangles=rect,row_ids=rows)
checks=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)})
p=evaluate(1.5,3.5); check('inside_is_valid_and_admitted',p['valid'] is True and p['admitted'] is True)
p=evaluate(2.5,3.5); check('valid_outside_is_not_admitted',p['valid'] is True and p['admitted'] is False)
p=evaluate(1.,4.); check('closed_endpoints_are_admitted',p['admitted'] is True)
p=evaluate(1.5,3.5,False);check('invalid_is_not_admitted',p['valid'] is False and p['admitted'] is None)
p=evaluate(float('nan'),3.5);check('nonfinite_is_not_admitted',p['valid'] is False and p['admitted'] is None)
p=evaluate(1.5,3.5,1);check('integer_valid_flag_is_refused',p['valid'] is False and p['admitted'] is None)
first=evaluate(1.5,3.5)
for a,b in [(0.,0.),(2.,4.),(100.,100.)]:evaluate(a,b)
check('later_other_points_do_not_change_first_classification',evaluate(1.5,3.5)==first)
coords=json.loads(raw['coordinates'])['engine_coordinates']; add=json.loads(raw['coordinate_addendum'])
old=[c['name'] for c in coords if c['role']!='fixed']; fixed=add['coordinate_mode']['fixed_engine_coordinates']; new=[n for n in old if n not in fixed]
check('selected_filler_demands_four_u',len(old)==4)
check('native_headline_has_three_u',len(new)==3 and new==add['coordinate_mode']['free_coordinates'])
result={'schema':'UNT_HANDOFF_RULES_AUDIT_CX1V002','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_SOURCE_AUDIT_AND_SYNTHETIC_PURE_CLASSIFIER_ONLY','verdict':'WAIT_FOR_FULL_STEP4_DECISION_UNDER_CURRENT_PUBLISHED_CONTRACT','scientific_membership':'POINTWISE_RECTANGLE_MEMBERSHIP_INDEPENDENT_OF_LATER_POINTS','streaming_contract':'UNDEFINED_NOT_EMITTED_BY_CURRENT_V006R9','native_fixed_distance_u_names':new,'filler_u_names':old,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'pins':pins,'scientific_processes_created':0,'actual_target_or_run_data_opened':False,'production_admission':'UNTESTED'}
assert result['passed']==result['total']
with (OUT/'RULES_AUDIT_CX1V002.json').open('xb') as h:h.write((json.dumps(result,indent=2,sort_keys=True)+'\n').encode())
print(json.dumps({'passed':result['passed'],'total':result['total'],'result_sha256':hashlib.sha256((OUT/'RULES_AUDIT_CX1V002.json').read_bytes()).hexdigest()}))
