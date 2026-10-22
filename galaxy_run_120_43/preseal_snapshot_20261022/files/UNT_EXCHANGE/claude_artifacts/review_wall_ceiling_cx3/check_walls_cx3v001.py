"""Independent 0839/0846 metadata review. No scientific entry point is called."""
import _strptime
import ast
import contextlib
import copy
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import types

H=Path(__file__).parent
A=H.parent
SRC=A/'h11_wall_ceiling_c3'
WORK=H/'INDEPENDENT_CX3V001'
WORK.mkdir()
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip()
paths={
 'B':A/'sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json',
 'C':SRC/'C2V004C_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004C.json',
 'D':SRC/'C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json',
 'buildC':SRC/'build_params_s45_c2v004c_c3v001.py',
 'buildD':SRC/'build_params_s45_c2v004d_c3v001.py',
 'checkC':SRC/'check_headline_caps_c3v001.py',
 'checkD':SRC/'check_s1_pair_caps_c3v001.py',
 'guard':A/'s1_successors_c2/step4_guard_c2v014.py',
 'launcher':A/'s1_successors_c2/step4_launcher_c2v015.py',
 'binder':A/'s1_successors_c2/step4_bind_c2v011.py',
 'pair_guard':A/'s1_pair_concurrent_cx3/v001/step4_guard_c2v014_s1pair_cx3v001.py',
 'monitor':A/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
 'fields':A/'h3_campaign_path_c2/apply_fields_c2v006/apply_h3_fields_c2v006.py',
 'spec_producer':A/'step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py',
 'prelaunch':A/'step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py',
 'sheet':A/'verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md',
 'amendment':A.parent/'FROM_CLAUDE3/0276_2026-10-21_0836-built-DBP-C2V004C-HEADLINE11-wall-to-phase2-ceiling-data-only-sheet-amendment-review-request.md',
}
raw={k:p.read_bytes() for k,p in paths.items()}
pins={k:{'path':str(paths[k]),'sha256':hashlib.sha256(v).hexdigest()} for k,v in raw.items()}
for k,prefix in {'B':'e239d21e','C':'ce9cbef8','D':'5d3f4bb8','buildC':'ab9a054e',
                 'buildD':'1e16b718','checkC':'4efb810b','checkD':'5f24c6bf',
                 'guard':'6efdca01','launcher':'cd987edd','binder':'d3d9702e',
                 'monitor':'ba031c23','sheet':'f2a5eec4','pair_guard':'1274a39a'}.items():
    assert pins[k]['sha256'].startswith(prefix),(k,pins[k])
READS=[]
def audit(event,args):
    if event.startswith('socket.') or event in ('os.remove','os.rmdir','os.rename','os.system','os.kill','os.killpg'):
        raise AssertionError('FENCE '+event)
    if event=='subprocess.Popen' and args[1]!=['/bin/bash','-n']:
        raise AssertionError('NO_EXECUTABLE_PROCESS')
    if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
    p=Path(os.path.realpath(os.fsdecode(args[0])))
    flags=args[2]
    write=isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR))
    if write:
        assert p.is_relative_to(WORK) and not p.exists() and flags&os.O_EXCL,p
    else:
        assert p.is_relative_to(WORK) or p in paths.values() or p==Path(__file__).resolve(),p
        READS.append(str(p))
sys.addaudithook(audit)
def module(key):
    m=types.ModuleType(key);m.__file__=str(paths[key])
    exec(compile(raw[key],str(paths[key]),'exec'),m.__dict__)
    return m
bc,bd,cd=module('buildC'),module('buildD'),module('checkD')
RESULTS=[]
def check(name,fn):
    try:
        value=fn()
        assert value is not False
        RESULTS.append({'name':name,'status':'PASS'})
    except BaseException as exc:
        RESULTS.append({'name':name,'status':'FAIL','detail':repr(exc)})
def flatten(o,trail=()):
    if type(o) is dict and o:
        return {k:v for a,b in o.items() for k,v in flatten(b,trail+(a,)).items()}
    if type(o) is list and o:
        return {k:v for i,b in enumerate(o) for k,v in flatten(b,trail+(str(i),)).items()}
    return {'.'.join(trail):(type(o).__name__,o)}
docs={k:json.loads(raw[k]) for k in ('B','C','D')}
leaves={k:flatten(d) for k,d in docs.items()}
diff=lambda a,b:sorted(k for k in set(leaves[a])|set(leaves[b]) if leaves[a].get(k)!=leaves[b].get(k))
DIFFS={'C_vs_B':diff('B','C'),'D_vs_C':diff('C','D'),'D_vs_B':diff('B','D')}
head=docs['B']['batches']['HEADLINE']['case_order']
hw={'batches.HEADLINE.caps_per_case.'+c+'.wall_cap_s' for c in head}
pw={'batches.POST_S1.caps_per_case.'+c+'.wall_cap_s'
    for c in docs['B']['batches']['POST_S1']['case_order']}
pc={'schema','supersedes.path','supersedes.sha256','supersedes.what_changes','note_a271'}
pd={'schema','supersedes.path','supersedes.sha256','supersedes.what_changes','note_a284'}
W=(dt.datetime(2026,12,1,5,59,tzinfo=dt.timezone.utc)-
   dt.datetime(2026,10,22,9,30,tzinfo=dt.timezone.utc))//dt.timedelta(seconds=1)
check('independent_integer_wall_3443340',lambda:W==3443340)
check('C_exact_16_leaf_diff',lambda:set(DIFFS['C_vs_B'])==hw|pc and len(hw)==11)
check('D_exact_7_leaf_diff_against_C',lambda:set(DIFFS['D_vs_C'])==pw|pd and len(pw)==2)
check('D_exact_19_leaf_diff_against_B',lambda:set(DIFFS['D_vs_B'])==hw|pw|pc|pd)
check('all_13_D_walls_equal_W',lambda:all(leaves['D'][k]==('int',W) for k in hw|pw))
check('C_non_HEADLINE_batches_unchanged',lambda:all(docs['B']['batches'][k]==v
      for k,v in docs['C']['batches'].items() if k!='HEADLINE'))
check('D_other_batches_unchanged',lambda:all(docs['B']['batches'][k]==v
      for k,v in docs['D']['batches'].items() if k not in ('HEADLINE','POST_S1')))
check('RSS_output_route_order_unchanged',lambda:all(leaves['B'][k]==leaves['D'][k] for k in leaves['B']
      if k.endswith(('.rss_cap_bytes','.output_cap_bytes')) or '.route_a_admission.' in k or '.case_order.' in k))
check('C_rebuild_byte_identical',lambda:bc.build(raw['B'],'2026-10-22T09:30:00Z')[0]==raw['C'])
check('D_rebuild_byte_identical',lambda:bd.build(raw['B'],raw['C'],'2026-10-22T09:30:00Z')[0]==raw['D'])
def cli_builder(mod,label,inputs):
    at=len(READS)
    with contextlib.redirect_stdout(io.StringIO()):
        mod.main(['--fill-utc','2026-10-22T09:30:00Z','--out-dir',str(WORK/label)])
    assert READS[at:]==[str(paths[k]) for k in inputs],READS[at:]
    assert (WORK/label/mod.OUT_NAME).read_bytes()==raw[label]
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (WORK/label).iterdir()}
    try:mod.main(['--fill-utc','2026-10-22T09:30:00Z','--out-dir',str(WORK/label)])
    except SystemExit as exc:assert str(exc).startswith('REFUSED OUT_DIR_MUST_BE_NEW')
    else:raise AssertionError('existing directory accepted')
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (WORK/label).iterdir()}
    return before==after
check('C_main_reads_only_B_exclusive_outputs',lambda:cli_builder(bc,'C',['B']))
check('D_main_reads_only_B_C_exclusive_outputs',lambda:cli_builder(bd,'D',['B','C']))
def put(name,doc):
    p=WORK/name
    data=(json.dumps(doc,sort_keys=True)+'\n').encode()
    with p.open('xb') as f:f.write(data)
    return {'path':str(p),'sha256':hashlib.sha256(data).hexdigest()}
def headline_checker(label,change=None,sha=None):
    caps=copy.deepcopy(docs['C']['batches']['HEADLINE']['caps_per_case'])
    plan={'calls':[dict(case=c,**caps[c]) for c in head]}
    adm={'case_order':head,'caps':copy.deepcopy(caps)}
    if change:change(plan,adm)
    pp,ap=put(label+'_plan.json',plan),put(label+'_admission.json',adm)
    argv=[str(paths['checkC']),str(paths['C']),sha or pins['C']['sha256'],pp['path'],ap['path']]
    old=sys.argv;sys.argv=argv
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(raw['checkC'],str(paths['checkC']),'exec'),{'__name__':'__main__'})
    finally:sys.argv=old
def reject_checker(label,change=None,sha=None):
    try:headline_checker(label,change,sha)
    except AssertionError:return True
    raise AssertionError('checker accepted adverse caps')
check('C_checker_good_11_calls',lambda:headline_checker('good'))
for field in ('wall_cap_s','rss_cap_bytes','output_cap_bytes'):
    for side in ('plan','admission'):
        def adverse(field=field,side=side):
            def mutate(p,a):
                if side=='plan':p['calls'][0][field]=100800 if field=='wall_cap_s' else 1
                else:a['caps'][head[0]][field]=100800 if field=='wall_cap_s' else 1
            return reject_checker(side+'_'+field,mutate)
        check('C_checker_refuses_'+side+'_'+field,adverse)
check('C_checker_refuses_case_order',lambda:reject_checker('order',lambda p,a:p['calls'].reverse()))
check('C_checker_refuses_wrong_DBP_sha',lambda:reject_checker('sha',sha='0'*64))
def monitor_argv():
    tree=ast.parse(raw['launcher'])
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='monitor_argv')
    ns={'PYTHON':sys.executable}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),str(paths['launcher'])+':monitor_argv','exec'),ns)
    call={'driver':{'path':'/synthetic/never_execute.py','sha256':'0'*64},'spec':{'path':'/synthetic/spec.json'},
          'outdir':'/synthetic/out','receipt':'/synthetic/receipt',**docs['C']['batches']['HEADLINE']['caps_per_case'][head[0]]}
    args=ns['monitor_argv']({'monitor':{'path':'/synthetic/monitor.py'}},call)
    return args[args.index('--wall-cap-s')+1]==str(W)
check('launcher_monitor_argv_preserves_W_no_execution',monitor_argv)
for key in ('fields','spec_producer','prelaunch','binder'):
    check(key+'_has_no_wall_field',lambda key=key:'wall' not in raw[key].decode().lower())
def amendment():
    text=raw['amendment'].decode()
    assert pins['C']['sha256'] in text and 'DBP_C_SHA=' in text
    assert '$BOUND_PLAN' in text and '$BOUND_ADMISSION' in text
    blocks=re.findall(r'```bash\n(.*?)```',text,re.S)
    assert len(blocks)==3
    for b in blocks:
        p=subprocess.run(['/bin/bash','-n'],input=b,text=True,capture_output=True)
        assert p.returncode==0,p.stderr
    return True
check('amendment_pin_copy_targets_and_three_shell_syntax_blocks',amendment)
for key,p in paths.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest()==pins[key]['sha256']
report={'date_u':DATE,'status':'TESTED','reviewer':'Codex3','scope':__doc__,'wall_seconds':W,
        'sources':pins,'leaf_diffs':DIFFS,'cases':RESULTS,
        'passed':sum(c['status']=='PASS' for c in RESULTS),'failed':sum(c['status']!='PASS' for c in RESULTS),
        'source_bytes_unchanged':True,'FORMAL':[
            'guard014 validates positive integer caps and exact root cfg caps; no fixed HEADLINE wall',
            'binder retains input plan bytes and admission caps while binding the final plan pin',
            'monitor parser accepts float wall; run_monitored requires positive wall and compares elapsed time to it',
            'FINAL/H1/PRELAUNCH sources have no wall field; actual future H1 and FINAL outputs were not read'],
        'notes':[
            'The original sheet retains A248 wall wording at lines 136 and 155 as well as line 8. The explicit later DBP_C copy/check is decisive; recommend updating those two descriptions in the successor sheet too.',
            'D checker/README says five records, but enumerates and checks six: pair plan, parent admission, two child admissions, two child plans. Documentation count only.'],
        'UNTESTED':['root actual H1/FINAL/plan/admission fills','multi-week monitor runtime','scientific launches']}
put('TEST_RECORD.json',report)
print(json.dumps({'passed':report['passed'],'failed':report['failed'],
                  'failures':[c for c in RESULTS if c['status']!='PASS']}))
sys.exit(bool(report['failed']))
