"""Independent 0558 blinding probe. Fresh synthetic manifests; no production run input."""
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import sys
import time
import types
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py'
EXPECTED='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
BLOCKED=[];READS=set()
def audit(event,args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn','os.fork','os.exec'):
        BLOCKED.append(event);raise RuntimeError('Review forbids process/network')
    if event in ('os.remove','os.rmdir','os.rename','os.replace','shutil.rmtree'):
        BLOCKED.append(event);raise RuntimeError('Review forbids destructive mutation')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])).resolve();s=str(p);low=s.lower()
        if '/.codex/' in low or '/runs/' in low or '/runs_ext/' in low or 'kmax_a2f10_c5h_run_v001' in low:
            BLOCKED.append(s);raise RuntimeError('Review forbids production run/session read')
        if 'ngc3198' in low and any(x in low for x in ('observed','target','rotmod')):
            BLOCKED.append(s);raise RuntimeError('Review forbids NGC target read')
        flags=args[2];mode=args[1]
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or isinstance(flags,int) and flags&(os.O_CREAT|os.O_TRUNC|os.O_RDWR|os.O_WRONLY|os.O_APPEND)
        if writing:
            if not p.is_relative_to(HERE.resolve()) or not flags&os.O_EXCL:
                BLOCKED.append(s);raise RuntimeError('Review writes exclusively in own directory')
        else:READS.add(s)
sys.addaudithook(audit)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    raw=obj if isinstance(obj,bytes) else obj.encode() if isinstance(obj,str) else (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    return pin(p)
raw=SOURCE.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
M=types.ModuleType('_independent_compare_r8');M.__file__=str(SOURCE);sys.modules[M.__name__]=M
exec(compile(raw,str(SOURCE),'exec'),M.__dict__)
run=HERE/('run_'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'_%s'%os.getpid());run.mkdir()
rows=[]
def check(name,ok,detail=None):rows.append({'name':name,'pass':bool(ok),'detail':detail})

# Fresh case registration assembled from the specified static grids and C5H prep normalization.
# Neither a production run nor an existing test fixture is imported.
ctx=M.build_context();uvlib=M.load_uvt_lib();cases={}
uv={'enabled':True,'outer':{'shape':'cylinder','K_big_inverse_kpc':128.0},'source_rule':'continuum_v001',
    'gas':{'interp':'lagrange3_s_gl4','M_s':128},'stars':{'segment_rule':'max16_ceil_kdr_plus8','tail_rule':'t_panels_40a_phase1p5_gl12'},
    'quadrature':{'order':8,'w_perp_max_inverse_kpc':0.05,'w_z_max_inverse_kpc':0.02},
    'domain':{'R_eval_max_kpc':20.0,'z_eval_max_kpc':10.0,'z_src_max_kpc':20.0},
    'asymptote':'EH_exact_minus_quarter','lapse_only':True,'jet_order':{'route_a':2,'route_b':1,'ngc_eval':1},
    'lambda_scale':1.0,'eps_certificate':'NONE_TEST_ONLY','lo_certificate':'NONE_TEST_ONLY'}
for label in M.REGISTERED:
    n=copy.deepcopy(ctx['c5h_numerics_reference']);n['composite_grid_spec']=copy.deepcopy(ctx['grids'][M.EXPECTED_GRID[label]])
    n['truncation']=copy.deepcopy(M.EXPECTED_TRUNCATION[label])
    e={'grid':M.EXPECTED_GRID[label],'truncation':copy.deepcopy(M.EXPECTED_TRUNCATION[label]),
       'drivers_allowed':[M.DRIVER_V009_EXT if label=='C5H' else M.PIN_DRIVER_V010_R5[1]],
       'tail':label!='C5H','ro1_required':label!='C5H','normalized_spec_equal':{'/numerics':n}}
    if label=='C5H':e['call_spec_sha256']=M.PIN_C5H_SPEC[1]
    else:
        n['uv_tail']=copy.deepcopy(uv);u=n['uv_tail']
        if label=='C4T-D5':u['source_rule']={'rule':'nodes_v001','ext_grid':copy.deepcopy(ctx['grids']['G5'])}
        if label=='C4T-C5c':u['outer']={'shape':'cube','K_out_inverse_kpc':5.0}
        if label in M.T3_KBIG_FACTOR:u['outer']['K_big_inverse_kpc']=128.0*M.T3_KBIG_FACTOR[label]
        if label=='C4T-A':u['lambda_scale']=1.05
        e['uv_tail_config_sha256']=uvlib.normalize_config(u)['sha256']
    cases[label]=e
cb={'schema':M.CASE_BLOCK_SCHEMA,'route_a_mode':'parallel8','cases':cases,'note':'Independent synthetic registration only'}
why=M.validate_case_block(cb);check('Fresh case-block passes actual complete validation',not why,why)
assert not why,why
cbpin=write(run/'CASE_BLOCK.json',cb)
pre={'route_a_mode':'parallel8','binding_inputs':{'case_block':cbpin},'note':'Independent test only; unsealed'}
prepin=write(run/'PREREG_TEST.json',pre)
empty={'schema':M.MANIFEST_SCHEMA,'cases':{},'identity_runs':{},'gates':{},'rpair':{},'note':'Independent test only'}
sentinels=['v_73.246813579','v_73.','v_73246813579','v_.732468','v_7.324681e1','v_-73.246813579']
counter=0
def cli(label,mode,manifest=None,prereg=prepin,case='C4T',registry=None,allow=True):
    global counter
    counter+=1;d=run/('%02d_%s'%(counter,label));d.mkdir()
    mp=write(d/'MANIFEST.json',copy.deepcopy(empty) if manifest is None else manifest)
    argv=['--prereg',prereg['path'],'--manifest',mp['path'],'--outdir',str(d/'report'),mode]
    if allow:argv+=['--test-allow-unpinned-prereg']
    if mode=='--validity-only':argv+=['--case',case,'--no-packets']
    if registry:argv+=['--test-producer-registry',registry['path']]
    out=io.StringIO();err=io.StringIO();before=set(READS)
    try:
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):rc=M.main(argv)
        exc=None
    except BaseException as e:rc=None;exc=type(e).__name__+': '+str(e)
    captures={'rc':rc,'exception':exc,'stdout':out.getvalue(),'stderr':err.getvalue(),'reads':sorted(READS-before)}
    capture=write(d/'CAPTURE.json',captures)
    return captures,capture,d

for mode in ('--validity-only','--gates-only'):
    cap,cp,d=cli('empty_'+mode[2:],mode)
    check(mode+' empty manifest produces blinded fail-closed report',cap['rc']==0 and not cap['exception'],cp)
    body=json.loads(cap['stdout']);check(mode+' declares synthetic/test and blinded',body.get('test_mode') is True and body.get('blinded') is True)
    def numbers(x):
        if type(x) in (int,float):return [x]
        if isinstance(x,dict):return sum((numbers(y) for y in x.values()),[])
        if isinstance(x,list):return sum((numbers(y) for y in x),[])
        return []
    check(mode+' report contains no numeric JSON values',not numbers(body))

# Actual reader validity path: invented failed result with record-controlled values in multiple fields.
for i,sentinel in enumerate(sentinels):
    rd=run/('invented_failed_%02d'%i);rd.mkdir()
    result={'schema':M.RESULT_SCHEMA,'status':sentinel,'valid':False,'reasons':[sentinel],
            'normalized_spec':{'numerics':cases['C4T']['normalized_spec_equal']['/numerics']},
            'rows':[{'id':rid,'speed_km_s':73.246813579} for rid in ctx['ids']],
            'passes':[],'stage_records':[{'name':sentinel,'exit_code':1}],'label':sentinel}
    write(rd/'result.json',result)
    man=copy.deepcopy(empty);man['cases']['C4T']=str(rd)
    cap,cp,d=cli('record_'+str(i),'--validity-only',man)
    check('Actual validity path suppresses failed-record canary '+str(i),cap['rc']==0 and sentinel not in cap['stdout']+cap['stderr'] and '73.246813579' not in cap['stdout']+cap['stderr'],cp)

# Case hash-only proof: invalid JSON and unreadable synthetic side files must never be parsed/opened.
rd=run/'invented_sha_only';rd.mkdir();write(rd/'result.json',b'INVALID_JSON v_73.246813579')
write(rd/'start.json',b'INVALID_SIDE_DO_NOT_READ');write(rd/'finish.json',b'INVALID_SIDE_DO_NOT_READ')
man=copy.deepcopy(empty);man['cases']['C4T']=str(rd)
before=set(READS);cap,cp,d=cli('case_sha_only','--gates-only',man)
newreads=set(READS)-before
check('Actual gates-only hashes non-JSON case without parsing',cap['rc']==0 and not cap['exception'],cp)
check('Actual gates-only reads no case start/finish side files',str(rd/'start.json') not in newreads and str(rd/'finish.json') not in newreads)
check('Actual gates-only suppresses case byte canary','73.246813579' not in cap['stdout']+cap['stderr'])

# Gate shell labels and numerical arrays: actual gate parser with a fresh registered record.
for i,sentinel in enumerate(sentinels):
    rec={'schema':M.GATE_SCHEMA,'gate':'RB_FP','producer':{'path':'INDEPENDENT_SYNTHETIC','sha256':'a'*64},
         'verdict':'PASS','case':'C4T','c4t_result_sha256':sha(rd/'result.json'),'eps_max':0.001,
         'shells':[sentinel],'dV_static_shells_km_s':{sentinel:[73.246813579]*12},
         'shell_ranges_inverse_kpc':[[4.0,math.sqrt(2)*128]],'full_tail_domain':True}
    rp=write(run/('RB_FP_%02d.json'%i),rec)
    registry={'schema':M.PRODUCER_REGISTRY_SCHEMA,'producers':{'RB_FP':['a'*64]},'identity_comparators':[],
              'identity_tokens':{},'gate_records':{'RB_FP':[rp['sha256']]},'gq_all_nodes_counts':{}}
    regpin=write(run/('REGISTRY_%02d.json'%i),registry)
    ma=copy.deepcopy(man);ma['gates']['RB_FP']=rp['path']
    cap,cp,d=cli('shell_'+str(i),'--gates-only',ma,registry=regpin)
    body=json.loads(cap['stdout'])
    check('Actual gate parses registered RB_FP record '+str(i),body['gates']['RB_FP']['status']=='PASS',cp)
    check('Actual gate suppresses shell label and array values '+str(i),sentinel not in cap['stdout']+cap['stderr'] and '73.246813579' not in cap['stdout']+cap['stderr'],cp)

# The entire CLI boundary includes refusal diagnostics, not only success JSON.
for mode in ('--validity-only','--gates-only'):
    bad=copy.deepcopy(cb);bad['v_73.246813579']='synthetic controlled key'
    bp=write(run/('BAD_CB_'+mode[2:]+'.json'),bad)
    pp=write(run/('BAD_PRE_'+mode[2:]+'.json'),{'binding_inputs':{'case_block':bp}})
    cap,cp,d=cli('refuse_caseblock_'+mode[2:],mode,prereg=pp)
    check(mode+' unknown case-block key refuses',cap['rc']==2,cp)
    check(mode+' refusal suppresses numeric case-block key','73.246813579' not in cap['stdout']+cap['stderr'],cp)
    ma=copy.deepcopy(empty);ma['v_73.246813579']='synthetic controlled key'
    cap,cp,d=cli('refuse_manifest_'+mode[2:],mode,ma)
    check(mode+' unknown manifest key refuses',cap['rc']==2,cp)
    check(mode+' refusal suppresses numeric manifest key','73.246813579' not in cap['stdout']+cap['stderr'],cp)
    registry={'schema':M.PRODUCER_REGISTRY_SCHEMA,'v_73.246813579':True}
    rp=write(run/('BAD_REG_'+mode[2:]+'.json'),registry)
    cap,cp,d=cli('refuse_registry_'+mode[2:],mode,registry=rp)
    check(mode+' unknown registry key refuses',cap['rc']==2,cp)
    check(mode+' refusal suppresses numeric registry key','73.246813579' not in cap['stdout']+cap['stderr'],cp)

cap,cp,d=cli('sealed_unavailable','--validity-only',allow=False)
check('Unsealed source cannot operate without explicit test mode',cap['rc']==2 and 'PENDING_FROM_BYTES' in cap['stderr'],cp)
check('Source hash unchanged after all CLI probes',sha(SOURCE)==EXPECTED)
check('No prohibited reads/process/network or nonexclusive writes attempted',not BLOCKED,BLOCKED)
report={'status':'TESTED','passed':sum(r['pass'] for r in rows),'total':len(rows),'rows':rows,
        'source_before':{'path':str(SOURCE),'sha256':EXPECTED},'source_after':pin(SOURCE),
        'harness':pin(Path(__file__)),'scope':'Own synthetic manifests and fresh case registration, actual CLI functions; no production run records. Static C5H prep allowed by parent. No solver call.',
        'blocked_attempts':BLOCKED,'reads':sorted(READS),'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
result=write(run/'BLINDING_RESULTS.json',report)
print(json.dumps({'result':result,'passed':report['passed'],'total':report['total'],'failed':[r['name'] for r in rows if not r['pass']]}))
