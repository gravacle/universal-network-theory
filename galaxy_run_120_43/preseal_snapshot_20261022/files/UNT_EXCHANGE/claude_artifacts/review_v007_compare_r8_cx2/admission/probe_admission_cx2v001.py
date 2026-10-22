"""0558 independent admission probes: invented raw results, no scientific run reads.
The shared case-block is a static registration from the independent blinding lane.
V4/V5 and non-target gate PASS inputs are explicitly injected policy premises.
"""
import copy, hashlib, json, math, os, sys, time, types
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ART=HERE.parents[1]
SRC=ART/'v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py'
EXPECTED='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
CB=ART/'review_v007_compare_r8_cx2/blinding/run_20261018T153200_24947/CASE_BLOCK.json'
READS=set(); BLOCKED=[]
def audit(ev,args):
    if ev.startswith('socket.') or ev in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','os.exec'):
        BLOCKED.append(ev);raise RuntimeError('no network/process')
    if ev in ('os.remove','os.rmdir','os.rename','os.replace','shutil.rmtree'):
        BLOCKED.append(ev);raise RuntimeError('no destructive mutation')
    if ev=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])).resolve(); s=str(p); lo=s.lower(); flags=args[2]; mode=args[1]
        if '/.codex/' in lo or '/runs/' in lo or '/runs_ext/' in lo or 'kmax_a2f10_c5h_run_v001' in lo or ('ngc3198' in lo and any(t in lo for t in ('target','observed','rotmod'))):
            BLOCKED.append(s);raise RuntimeError('prohibited read')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_CREAT|os.O_TRUNC|os.O_RDWR|os.O_WRONLY|os.O_APPEND))
        if writing:
            if not p.is_relative_to(HERE.resolve()) or not flags&os.O_EXCL:
                BLOCKED.append(s);raise RuntimeError('only exclusive own writes')
        else:READS.add(s)
sys.addaudithook(audit)
def sh(raw):return hashlib.sha256(raw).hexdigest()
def pin(p):return {'path':str(p),'sha256':sh(Path(p).read_bytes())}
def put(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    raw=obj if isinstance(obj,bytes) else (json.dumps(obj,sort_keys=True,indent=1,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    return pin(p)
def digest(s):return sh(s.encode())
raw=SRC.read_bytes();assert sh(raw)==EXPECTED
M=types.ModuleType('admission_compare_r8');M.__file__=str(SRC);sys.modules[M.__name__]=M
exec(compile(raw,str(SRC),'exec'),M.__dict__)
OUT=HERE/('run_'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'_'+str(os.getpid()));OUT.mkdir()
checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
ctx=M.build_context();cb=json.loads(CB.read_bytes());ctx['case_block']=cb
check('Shared static registration passes complete actual case-block validator',not M.validate_case_block(cb))
ids=ctx['ids'];tau=ctx['tau'];objects={};paths={}

def mk(label,identity=False):
    d=OUT/'positive_raw'/label; d.mkdir(parents=True)
    if identity:
        n={'route_a':{'column_workers':1}};drv=M.PIN_DRIVER_V010_R5[1];sp=digest('identity spec '+label)
    else:
        n=copy.deepcopy(cb['cases'][label]['normalized_spec_equal']['/numerics']);drv=cb['cases'][label]['drivers_allowed'][0]
        sp=M.PIN_C5H_SPEC[1] if label==M.C5H else digest('call spec '+label)
    ns={'galaxy':ctx['anchor']['galaxy'],'physical':copy.deepcopy(ctx['anchor']['physical']),'coefficients':copy.deepcopy(ctx['anchor']['coefficients']),'numerics':n}
    shift={'C2T':-.1,'C3T':-.02}.get(label,0.0)
    vals={rid:20.0+j*.125+shift*tau[rid] for j,rid in enumerate(ids)}
    ps=[]
    for i,off in enumerate((.0004,.0001,0.0)):
        rows=[{'id':rid,'speed_km_s':vals[rid]+off} for rid in ids]
        ps.append({'pass':i+1,'rows':rows,'max_abs_change_km_s':0.0 if i==0 else max(abs(x['speed_km_s']-y['speed_km_s']) for x,y in zip(rows,ps[-1]['rows']))})
    rao={'classification':'CONVERGED','converged_iteration':6}
    if label!=M.C5H:
        armed=label!='B0prime_RERUN';pins=M.PIN_RO1_NODES_CUSTODY if label=='C4T-D5' else M.PIN_RO1_CUSTODY
        cw=n.get('route_a',{}).get('column_workers',1)
        rao['ro1']={'rule':'RO1','fired':False,'armed':armed,'events':[],
                    'worker_sha256':pins['worker' if cw==1 else 'worker_parallel'][1] if armed else None,
                    'binding_sha256':M.PIN_RO1_CUSTODY['binding'][1] if armed else None}
    attempt={'result':{}}
    if not identity and label!=M.C5H:
        attempt['result']['uv_tail']={'schema':M.UVT_RA_RECORD_SCHEMA,'outcome':'CONVERGED_FINITE_FIXED_POINT',
          'production_admissible':True,'admissibility':'production','config_sha256':cb['cases'][label]['uv_tail_config_sha256'],
          'flags':[],'monitor_status':'M_T_WITHIN_THRESHOLD','M_T_threshold':.25,'M_T_accepted':.01,'accepted_iteration':6,
          'E_A_rows_km_s_accepted':[.001*tau[r] for r in ids],'probe_R_m':ctx['row_radii_m']}
    ap=put(d/'attempt.json',attempt);rao.update(result_path=ap['path'],result_sha256=ap['sha256'])
    obj={'schema':M.RESULT_SCHEMA,'label':label,'status':'COMPLETED','valid':True,'normalized_spec':ns,'driver_sha256':drv,
         'call_spec_sha256':sp,'rows':[{'id':rid,'speed_km_s':vals[rid]} for rid in ids],'passes':ps,'final_pass':3,
         'identity':{'route_a':{'custody':{'identity_sha256':digest('route a '+label)}}},'route_a_outcome':rao}
    objects[label]=copy.deepcopy(obj); paths[label]=save(d,obj)
    return M.read_run(label,d,ctx)
def save(d,obj):
    rp=put(d/'result.json',obj);put(d/'finish.json',{'status':'COMPLETED','valid':True,'result_sha256':rp['sha256']})
    put(Path(str(d)+'.receipt.json'),{'schema':M.RECEIPT_SCHEMA,'status':'FINISHED','driver_status':obj['status'],'exit_code':0,'stop_reason':None,
        'result':rp,'pins':{'spec':{'sha256':obj['call_spec_sha256']},'driver':{'sha256':obj['driver_sha256']}}})
    return str(d)
R={l:mk(l) for l in M.REGISTERED};IDR={l:mk(l,True) for l in M.IDENTITY_RUNS}
packets={l:{'V4':True,'V5':True,'premise':'injected synthetic packet-validation premise; no packet/solver'} for l in M.REGISTERED}
G={g:{'gate':g,'status':'PASS','codes':[],'derived':{},'_record_json':{}} for g in M.ALL_GATES}
G['I1T']['derived']['i1t_per_case']={l:'PASS' for l in M.T_CASES}
G['EPS']['derived']['eps_max']=.0001
G['RB_FP']['_record_json']={'eps_max':.0001,'shells':['invented'],'dV_static_shells_km_s':{'invented':[1.0]*12}}
G['SR_K']['_record_json']={'Delta_km_s':{'2':[.001]*12,'3':[.002]*12,'4':[.003]*12}}
G['EA']['_record_json']={'per_case':{l:{'E_A_rows_km_s':[.001*tau[r] for r in ids]} for l in M.REGISTERED}}
G['SRB_ROT']['_record_json']={'eps_max':.0001}
def evaluate(r=None,g=None,idr=None):return M.evaluate_v007(ctx,R if r is None else r,IDR if idr is None else idr,G if g is None else g,packets=packets)
positive=evaluate();put(OUT/'POSITIVE_POLICY_REPORT.json',positive)
check('Actual raw reader and case-validity positive fixture admits every registered case',all(x['valid_all'] for x in positive['validity'].values()),{l:v.get('V3_mismatch') for l,v in positive['validity'].items() if not v['valid_all']})
check('Actual identity-run validator accepts synthetic r5 positive receipts',all(x['valid'] for x in positive['identity_runs'].values()),positive['identity_runs'])
check('Synthetic policy premises allow ADOPT_TAIL positive control',positive['decision']['outcome']=='ADOPT_TAIL',positive['decision'])
put(OUT/'MANIFEST.json',{'schema':M.MANIFEST_SCHEMA,'cases':{l:paths[l] for l in M.REGISTERED},'identity_runs':{l:paths[l] for l in M.IDENTITY_RUNS},'gates':{},'note':'Raw reader fixtures; policy gate and packet premises are injected, not scientific certificates'})

mutations={
 'early_conflicting_duplicate':lambda o:o['passes'][0]['rows'].append(dict(o['passes'][0]['rows'][0],speed_km_s=999.)),
 'final_conflicting_duplicate':lambda o:o['passes'][-1]['rows'].append(dict(o['passes'][-1]['rows'][0],speed_km_s=999.)),
 'unknown_extra_row':lambda o:o['passes'][0]['rows'].append({'id':'INVENTED_UNKNOWN','speed_km_s':999.}),
 'missing_id':lambda o:o['passes'][0]['rows'].pop(),
 'duplicate_replaces_missing':lambda o:o['passes'][0]['rows'].__setitem__(-1,copy.deepcopy(o['passes'][0]['rows'][0])),
 'nonstring_id':lambda o:o['passes'][0]['rows'][0].__setitem__('id',None),
 'present_empty_dict':lambda o:o['passes'][0].__setitem__('rows',{}),
 'present_dict':lambda o:o['passes'][0].__setitem__('rows',{'ROW_01':1.0}),
 'present_string':lambda o:o['passes'][0].__setitem__('rows','ROWS'),
 'present_bool':lambda o:o['passes'][0].__setitem__('rows',False),
 'present_number':lambda o:o['passes'][0].__setitem__('rows',1),
 'nonobject_row':lambda o:o['passes'][0]['rows'].__setitem__(0,1),
 'final_row_duplicate':lambda o:o['rows'].append(copy.deepcopy(o['rows'][0])),
 'final_row_unknown':lambda o:o['rows'].append({'id':'UNKNOWN','speed_km_s':1.}),
 'final_row_missing':lambda o:o['rows'].pop(),
}
for name,mut in mutations.items():
    o=copy.deepcopy(objects['C4T']);mut(o);d=OUT/'mutations'/name;save(d,o);r=M.read_run('C4T',d,ctx)
    ev=evaluate(dict(R,C4T=r));detail={'decision':ev['decision']['outcome'],'validity':ev['validity']['C4T'],'pass_rows_s9':r.get('pass_rows_s9')}
    check('S9 '+name+' cannot adopt',ev['decision']['outcome']=='INCOMPLETE' and not ev['validity']['C4T']['V1'],detail)
for name,value in [('absent',None),('null',None),('empty',[])]:
    o=copy.deepcopy(objects['C4T'])
    if name=='absent':o['passes'][0].pop('rows')
    else:o['passes'][0]['rows']=value
    d=OUT/'mutations'/('gap_'+name);save(d,o);r=M.read_run('C4T',d,ctx);ev=evaluate(dict(R,C4T=r))
    check('B4 '+name+' is gap, not S9, and cannot adopt',not r.get('pass_rows_s9') and bool(r.get('pass_rows_gap')) and ev['decision']['outcome']!='ADOPT_TAIL',ev['decision'])
for lab in M.IDENTITY_RUNS:
    o=copy.deepcopy(objects[lab]);o['driver_sha256']=digest('foreign driver with receipt rebound');d=OUT/'mutations'/('identity_'+lab);save(d,o)
    r=M.read_run(lab,d,ctx);ev=evaluate(idr=dict(IDR,**{lab:r}))
    check('A67 N1 '+lab+' foreign driver with matching receipt refuses',not ev['identity_runs'][lab]['valid'] and ev['decision']['outcome']!='ADOPT_TAIL',ev['identity_runs'][lab])

# Real gate parser, fresh producer/records and registry; no assertion that fixtures are root approvals.
prod=put(OUT/'producer.py',b'# independent inert synthetic producer\n')
base={'schema':M.GATE_SCHEMA,'gate':'SR_K','producer':prod,'verdict':'REPLAYED',
      'states':{s:p[1] for s,p in M.PIN_R3.items()},'Delta_km_s':{'2':[.01]*12,'3':[.02]*12,'4':[.03]*12}}
def gate_case(name,mut=None,registry_mut=None,expected='RECORD_DEFECT',register=True):
    o=copy.deepcopy(base)
    if mut:mut(o)
    rp=put(OUT/'gate_records'/(name+'.json'),o)
    reg={'schema':M.PRODUCER_REGISTRY_SCHEMA,'producers':{'SR_K':[prod['sha256']]},'identity_comparators':[], 'identity_tokens':{},
         'gate_records':{'SR_K':[rp['sha256']] if register else []},'gq_all_nodes_counts':{}}
    if registry_mut:registry_mut(reg)
    rpin=put(OUT/'registries'/(name+'.json'),reg)
    c=dict(ctx,producer_registry=M.load_producer_registry(rpin['path'],rpin['sha256']))
    g=M.evaluate_gate('SR_K',rp['path'],c);ev=evaluate(g=dict(G,SR_K=g))
    check('Registry '+name,g['status']==expected and (expected=='PASS' or ev['decision']['outcome']=='NO_RUN'),{'gate':g,'outcome':ev['decision']['outcome'],'record':rp,'registry':rpin})
gate_case('registered_positive',expected='PASS')
gate_case('record_not_registered',register=False)
gate_case('producer_not_registered',registry_mut=lambda r:r['producers']['SR_K'].clear())
gate_case('wrong_record_pin',registry_mut=lambda r:r['gate_records'].__setitem__('SR_K',[digest('foreign')]))
gate_case('producer_claim_forged',mut=lambda o:o['producer'].__setitem__('sha256',digest('foreign')))
gate_case('bitwise_equal_two_K',mut=lambda o:o['Delta_km_s'].__setitem__('3',o['Delta_km_s']['2']))
gate_case('bitwise_equal_all_K',mut=lambda o:o['Delta_km_s'].update({'3':o['Delta_km_s']['2'],'4':o['Delta_km_s']['2']}))
gate_case('record_wrong_state',mut=lambda o:o['states'].__setitem__('C2R3',digest('wrong saved state')))
gate_case('record_unregistered_verdict',mut=lambda o:o.__setitem__('verdict','PENDING'))
gate_case('A69_deferred_forged_path',mut=lambda o:o['producer'].__setitem__('path',str(OUT/'never_exists.py')),expected='PASS')
try:
    M.producer_registry_from_obj({'schema':M.PRODUCER_REGISTRY_SCHEMA,'producers':{},'identity_comparators':[],'identity_tokens':{},'gate_records':{'SR_K':M.GATE_RECORD_AFTER_SEAL},'gq_all_nodes_counts':{}})
    ok=False
except M.Refused:ok=True
check('A67 SR_K forbids PRODUCED_AFTER_THE_SEAL wildcard',ok)

# Gate status outcomes directly exercise decision wiring, declared policy unit premises only.
for name in M.required_gates(ctx['route_a_mode']):
    for status in ('MISSING','RECORD_DEFECT'):
        gs=copy.deepcopy(G);gs[name].update(status=status,codes=['independent synthetic '+status]);ev=evaluate(g=gs)
        check('Required '+name+' '+status+' never adopts',ev['decision']['outcome']!='ADOPT_TAIL',ev['decision']['outcome'])
flagged=copy.deepcopy(R);u=flagged['C4T']['uvt_record'];u.update(flags=[M.FLAG_TSU],monitor_status='FLAGGED',M_T_accepted=.3)
ev=evaluate(flagged);check('Unruled tail flag never adopts',ev['decision']['outcome']=='FLAG_PENDING_RULING',ev['decision'])
pending=copy.deepcopy(R);pending['C4T']['pass_rows_gap']='PASS_WITHOUT_ROWS';ev=evaluate(pending)
check('Unresolved Picard evidence never adopts',ev['decision']['outcome']!='ADOPT_TAIL',ev['decision'])
check('No blocked reads/processes or nonexclusive writes',not BLOCKED,BLOCKED)
check('Source unchanged after all probes',pin(SRC)['sha256']==EXPECTED)
result={'status':'TESTED','date_u':sys.argv[1] if len(sys.argv)>1 else 'UNRECORDED','waiver':'nice unavailable (sandbox); 0514 waiver',
 'passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'source_before':{'path':str(SRC),'sha256':EXPECTED},'source_after':pin(SRC),
 'harness':pin(__file__),'shared_static_case_block':pin(CB),'reads':[pin(p) for p in sorted(READS) if Path(p).is_file() and not p.startswith(str(OUT))],
 'limitations':['No scientific run/receipt/target read.','Policy positive uses injected V4/V5 and non-target gate PASS premises; not a fully certified scientific world.','Actual raw read_run, adapt_result, case_validity, identity_run_validity, SR_K evaluate_gate, and evaluate_v007 execute unmodified.','No scientific execution or production ADOPT_TAIL authorization.']}
rp=put(OUT/'RESULTS.json',result)
print(json.dumps({'result':rp,'passed':result['passed'],'total':result['total'],'failed':[x for x in checks if not x['pass']]}))
