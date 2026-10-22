import hashlib,json,itertools
from pathlib import Path
from datetime import datetime,timezone
import inflight_policy_cx1v001 as P
root=Path(__file__).resolve().parent
base=dict(natural_plan_committed=True,registered=True,identity_bound=True,runtime_environment_bound=True,envelope_valid=True,direct_state='RUNNING')
cases=[({},'WAIT_EXTERNAL'),({'direct_state':'REGISTERED_PENDING'},'WAIT_EXTERNAL'),({'direct_state':'UNKNOWN'},'HOLD_UNKNOWN_EXTERNAL_STATE'),({'registered':False},'NORMAL_CAMPAIGN'),({'natural_plan_committed':False},'REFUSE_BEFORE_NATURAL_PLAN'),({'identity_bound':False},'REFUSE_IDENTITY'),({'runtime_environment_bound':False},'REFUSE_RUNTIME_ENVIRONMENT'),({'envelope_valid':False},'REFUSE_ENVELOPE')]
for outcome,want in [('CAP_UNCOUNTED','NORMAL_CAMPAIGN_UNCOUNTED_FALLBACK'),('INFRA_UNCOUNTED','NORMAL_CAMPAIGN_UNCOUNTED_FALLBACK'),('COMPLETED_INVALID','RETAIN_SPECULATIVE_INVALID_FOR_ROOT')]:cases.append((dict(direct_state='TERMINAL',outcome=outcome),want))
for acceptance,want in [(None,'WAIT_ACCEPTANCE'),('INCOMPLETE','WAIT_ACCEPTANCE'),('ACCEPTED','VALIDATE_EXACT_IMPORT'),('ACCEPTED_PASS_FLAGGED','VALIDATE_EXACT_IMPORT'),('NON_LAPSE_TAIL_MATERIAL','RETAIN_FAILED_ACCEPTANCE_FOR_ROOT')]:cases.append((dict(direct_state='TERMINAL',outcome='COMPLETED_VALID',acceptance=acceptance),want))
for change,want in cases:assert P.decide(**dict(base,**change))==want,(change,want)
# All registered nonterminal states prohibit a local launch regardless of claimed outcome/acceptance.
count=0
for state,outcome,acceptance in itertools.product(['REGISTERED_PENDING','RUNNING','UNKNOWN'],[None,'CAP_UNCOUNTED','INFRA_UNCOUNTED','COMPLETED_INVALID','COMPLETED_VALID'],[None,'ACCEPTED','INCOMPLETE']):
 got=P.decide(**dict(base,direct_state=state,outcome=outcome,acceptance=acceptance));assert 'NORMAL_CAMPAIGN' not in got;count+=1
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('inflight_%Y%m%dT%H%M%S%f');case.mkdir(parents=True,exist_ok=False)
r={'status':'PASS','blocking_count':0,'scope':'pure 0837 policy prototype; evidence authentication and runtime hook untested','explicit_cases':len(cases),'nonterminal_no_duplicate_cases':count,'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [Path(P.__file__),Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
