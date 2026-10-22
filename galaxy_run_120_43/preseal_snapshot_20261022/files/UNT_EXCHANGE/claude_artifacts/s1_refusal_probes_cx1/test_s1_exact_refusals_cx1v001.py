"""Non-gating A284 N1 controls: exact refusal codes and lock identity.
Uses the byte-pinned release harness setup only; all scientific contexts are inert.
Production sources remain unchanged. Mutants alter one function in memory only.
"""
import ast,copy,hashlib,json,os,sys,types
from pathlib import Path
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
BASE=ART/'s1_pair_concurrent_cx3'
HARNESS=BASE/'test_s1_pair_cx3v002.py'
EXPECTED='4918ed05d1a8cb87c13ba0dcba33d1f5228bfdbd57905647285190af7e3e2623'
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
raw=HARNESS.read_bytes()
assert hashlib.sha256(raw).hexdigest()==EXPECTED,'HARNESS_PIN'
assert sys.flags.isolated and sys.flags.dont_write_bytecode,'USE_-I_-B'
run=Path(sys.argv[1]);assert run.is_absolute() and not run.exists()
sys.argv=[str(HARNESS),str(BASE/'v001'),str(run)]
marker="f=pair_fixture()\ncheck('full_guard_bind_both_separate_C1'"
text=raw.decode();assert text.count(marker)==1
prefix=text.split(marker)[0]
ns={'__name__':'inert_release_fixture_setup','__file__':str(HARNESS)}
exec(compile(prefix,str(HARNESS),'exec'),ns)
G=ns['G'];f=ns['pair_fixture']();ns['f']=f
assert ns['validate_obj'](f)[0]['calls']==f['calls']
cases=ns['CASES'];newj=ns['newj']
launcher=ns['load'](BASE/'v001/step4_launcher_c2v015_s1pair_cx3v001.py')
expected_lock=ART/'step4_launch_packet_cx1/STEP4_MACHINE_LOCK_V001'
def modified_child(change_child=None,change_plan=None):
    cfg=copy.deepcopy(f['cfg']);child=json.loads(Path(f['children'][cases[0]]['path']).read_bytes())
    if change_plan:
        plan=json.loads(Path(child['plan']['path']).read_bytes());change_plan(plan);child['plan']=newj('probe_child_plan',plan)
    if change_child:change_child(child)
    ref=newj('probe_child',child);cfg['s1_pair_admissions'][cases[0]]=ref
    return cfg
def pair_plan(change):
    plan=copy.deepcopy(f['plan']);change(plan)
    return lambda:G.core_priority_admission(plan,copy.deepcopy(f['cfg']))
def shared_c1():
    cfg=modified_child(change_child=lambda c:c.update(config=ns['CONFIGS'][cases[1]]))
    plan=copy.deepcopy(f['plan']);plan['s1_pair_admissions']=copy.deepcopy(cfg['s1_pair_admissions'])
    return lambda:G.core_priority_admission(plan,cfg)
def child_case(change_child=None,change_plan=None):
    cfg=modified_child(change_child,change_plan)
    return lambda:G.pair_case_admission(cfg,copy.deepcopy(f['calls'][0]))
def source_union():
    cfg=copy.deepcopy(f['cfg']);cfg['sources'].pop(ns['MODS']['context']['path'])
    return lambda:G.pair_case_admission(cfg,copy.deepcopy(f['calls'][0]))
PROBES=[
 ('G01_order','S1_PAIR_EXACT_ORDER_REQUIRED',lambda:pair_plan(lambda p:p['calls'].reverse()),'core_priority_admission'),
 ('G02_third_call','S1_PAIR_TWO_CALLS_REQUIRED',lambda:pair_plan(lambda p:p['calls'].append(copy.deepcopy(p['calls'][1]))),'core_priority_admission'),
 ('G03_distinct_C1','S1_PAIR_DISTINCT_C1_REQUIRED',shared_c1,'core_priority_admission'),
 ('G07_child_lineage','S1_PAIR_CHILD_LINEAGE',lambda:child_case(change_plan=lambda p:p['guard'].update(sha256='0'*64)),'pair_case_admission'),
 ('G08_child_call_bytes','S1_PAIR_CHILD_CALL_BYTES',lambda:child_case(change_plan=lambda p:p['calls'][0].update(extra_unbound_field=True)),'pair_case_admission'),
 ('G09_child_ramp','S1_PAIR_CHILD_RAMP_BINDING',lambda:child_case(change_plan=lambda p:p['route_a_admission'].update(poll_seconds=30)),'pair_case_admission'),
 ('G10_source_union','S1_PAIR_SOURCE_UNION_REQUIRED',source_union,'pair_case_admission'),
 ('G12_child_fill','S1_PAIR_CHILD_FILL_BINDING',lambda:child_case(change_plan=lambda p:p['s1'].update(fill_record=ns['REG'])),'pair_case_admission'),
 ('G13_child_verdict','S1_PAIR_VERDICT_MISMATCH',lambda:child_case(change_child=lambda c:c['v007'].update(verdict=ns['REG'])),'pair_case_admission')]
def evaluate(make,code):
    try:make()()
    except G.Refusal as e:return {'pass':str(e)==code,'actual':str(e),'exception':type(e).__name__}
    except Exception as e:return {'pass':False,'actual':str(e),'exception':type(e).__name__}
    return {'pass':False,'actual':'ADMITTED','exception':None}
results=[];mutants=[]
for name,code,make,funcname in PROBES:
    got=evaluate(make,code);results.append(dict(id=name,expected=code,**got))
    original=getattr(G,funcname)
    tree=ast.parse(Path(G.__file__).read_bytes())
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==funcname)
    count=0
    for call in ast.walk(node):
        if isinstance(call,ast.Call) and isinstance(call.func,ast.Name) and call.func.id=='require' and len(call.args)>=2 and isinstance(call.args[1],ast.Constant) and call.args[1].value==code:
            call.args[0]=ast.Constant(value=True);count+=1
    assert count==1,(name,count)
    ast.fix_missing_locations(node)
    try:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<INERT_SINGLE_GUARD_MUTANT>','exec'),G.__dict__)
        bad=evaluate(make,code)
    finally:setattr(G,funcname,original)
    mutants.append({'id':name,'removed_refusal':code,'detected':not bad['pass'],'mutant_result':bad})
results.append({'id':'L05_lock_path','pass':launcher.LOCK==expected_lock,'expected':str(expected_lock),'actual':str(launcher.LOCK)})
old=launcher.LOCK
launcher.LOCK=run/'WRONG_LOCK_NEVER_OPENED'
mutants.append({'id':'L05_lock_path','detected':launcher.LOCK!=expected_lock,'mutant_result':'constant mismatch; no lock opened'})
launcher.LOCK=old
assert ns['DENIED']==[],ns['DENIED']
assert all(x['pass'] for x in results),results
assert all(x['detected'] for x in mutants),mutants
record={'schema':'CX1_S1_EXACT_REFUSAL_PROBES_V001','status':'PASS','non_gating':True,'controls':results,'mutants':mutants,'n_controls':len(results),'n_detected':sum(x['detected'] for x in mutants),'source_pins':[pin(Path(__file__)),pin(HARNESS),pin(Path(G.__file__)),pin(BASE/'v001/step4_launcher_c2v015_s1pair_cx3v001.py')],'scope':'Exact-code controls for nine guard refusals plus launcher LOCK identity; positive full guard fixture.','seams':['Release-harness synthetic native context, policy, fill replay and disk','Single-function AST mutants in memory only; no production file changed','No worker or scientific process started; no real lock opened'],'untested':['Production mounted volume, real C1s, actual launch and runtime contention','Full scientific or end-to-end production admission'],'audit_denied':ns['DENIED']}
p=run/'REFUSAL_PROBES_REPORT.json'
with p.open('x') as h:json.dump(record,h,indent=2);h.write('\n')
print(json.dumps({'status':'PASS','controls':len(results),'mutants_detected':len(mutants),'report':pin(p)}))
