import ast,copy,json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
P=ROOT/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py'
raw=P.read_bytes();tree=ast.parse(raw);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='finite_difference_jacobian');fn.decorator_list=[]
ns={'np':np,'BOUNDS_SEMANTICS':'INERT','_MAX_REL_STEP':1,'_common_eval_checks':lambda *x:([],{'n':3,'varying':['x','y','z']}),'_positive_float':lambda *x:[],'_nonneg_int':lambda *x:[],'_check_unit_vector':lambda u,*x:([],np.array(u)),'_floats':lambda u:[float(x) for x in u],'_speeds_vector':lambda e,ids:np.array(e['value'])}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(P),'exec'),ns)
seed=np.array([.5,.5,.5]);nominal=[tuple(seed)]
for j in range(3):
 for side in [1,-1]:
  u=seed.copy();u[j]+=.05*side;nominal.append(tuple(u))
def response(u,scenario):
 d=np.array(u)-seed;j=int(np.argmax(abs(d)));v=True
 if scenario=='seed_invalid' and np.all(d==0):v=False
 if scenario.startswith('plus') and d[j]>0 and abs(d[j])>.03:v=False
 if scenario.startswith('minus') and d[j]<0 and abs(d[j])>.03:v=False
 if scenario=='all_invalid' and np.any(d):v=False
 return {'valid':v,'value':[float(sum(u)),float(sum(x*x for x in u))]}
def run(scenario,budget,early):
 cache={u:response(u,scenario) for u in nominal} if early else {};log=[];trace=[];hits=[]
 def evaluate(**kw):
  u=tuple(float(x) for x in kw['u']);trace.append(u);hits.append(u in cache)
  v=copy.deepcopy(cache.get(u,response(u,scenario)))
  v.update(index=len(log),admitted=v['valid'],reasons=[] if v['valid'] else ['INERT_INVALID'],exception=None)
  kw['counter']['used']+=1;log.append(v);return v
 ns['_evaluate_point']=evaluate
 result=ns['finite_difference_jacobian'](forward=None,spec={},region={'row_ids':['a','b']},u0=seed,rel_step=.05,min_step=.005,max_halvings=2,budget=budget,log=log)
 return {'result':result,'trace':trace,'log':log},hits
rows=[]
for scenario in ['valid','seed_invalid','plus_invalid','minus_invalid','all_invalid']:
 for budget in [0,1,2,4,7,120]:
  late,_=run(scenario,budget,False);early,hits=run(scenario,budget,True)
  assert late==early,(scenario,budget)
  assert late['result']['status'] in ['COMPLETE','SEED_INVALID','BUDGET_EXHAUSTED','COMPLETE_WITH_FAILED_COLUMNS']
  if scenario=='plus_invalid':
   for u in nominal[2::2]:assert u not in early['trace']
  rows.append({'scenario':scenario,'budget':budget,'status':early['result']['status'],'calls':len(early['trace']),'early_hits':sum(hits),'equal_result_log_trace':True})
out={'schema':'CX1_0816_INERT_BRANCH_TRACE_V001','verdict':'PASS','cases':rows,'source':{'path':str(P),'sha256':hashlib.sha256(raw).hexdigest()},'scope':'Actual finite_difference_jacobian AST. Input validation/physical evaluation stubbed; deterministic inert response. Tests conditional branch/result/log invariance for precomputed nominal results. Not whole-engine Probe, real cache, custody, F6 or scheduler integration.'}
p=ROOT/'concurrent_jacobian_cx1/BRANCH_TRACE_RESULTS_V001.json'
with p.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'cases':len(rows),'verdict':'PASS','output':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
