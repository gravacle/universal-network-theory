"""0564 independent A73 presence/absence probes; source and fresh scratch fixtures only."""
import ast
import copy
import hashlib
import json
import os
import sys
import time
import types
import unicodedata
from pathlib import Path

HERE=Path(__file__).resolve().parent
ART=HERE.parents[1]
G6=ART/'tail_scheme_impl_c2/gates_v006'
G5=ART/'tail_scheme_impl_c2/gates_v005'
SOURCE=G6/'run_identity_compare_c2v006.py'
EXPECTED='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
FILL=G5/'tools/fill_picard_member_c2v002.py'
BLOCKED=[];READS=set()
def audit(event,args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn','os.fork','os.exec'):
        BLOCKED.append(event);raise RuntimeError('Forbidden process/network')
    if event in ('os.remove','os.rmdir','os.rename','os.replace','shutil.rmtree'):
        BLOCKED.append(event);raise RuntimeError('Forbidden deletion/move')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])).resolve();s=str(p);low=s.lower()
        if '/.codex/' in low or '/runs/' in low or '/runs_ext/' in low or 'kmax_a2f10_c5h_run_v001' in low or '/out/identity' in low or '/records/r4' in low:
            BLOCKED.append(s);raise RuntimeError('Forbidden production/log/report read')
        if 'ngc3198' in low and any(x in low for x in ('observed','target','rotmod')):
            BLOCKED.append(s);raise RuntimeError('Forbidden target read')
        flags=args[2];mode=args[1]
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or isinstance(flags,int) and flags&(os.O_CREAT|os.O_TRUNC|os.O_RDWR|os.O_WRONLY|os.O_APPEND)
        if writing:
            if not p.is_relative_to(HERE.resolve()) or not flags&os.O_EXCL:
                BLOCKED.append(s);raise RuntimeError('Only exclusive writes under own directory')
        else:READS.add(s)
sys.addaudithook(audit)
def pin(path):
    p=Path(path);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,o):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    raw=o if isinstance(o,bytes) else o.encode() if isinstance(o,str) else (json.dumps(o,indent=2,sort_keys=True)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    return pin(p)
def load(path,name,expected=None):
    raw=Path(path).read_bytes()
    if expected:assert hashlib.sha256(raw).hexdigest()==expected
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(raw,str(path),'exec'),m.__dict__);return m
M=load(SOURCE,'_a73_candidate',EXPECTED)
F=load(FILL,'_a73_inherited_fill','0235398dc1b0ec7b3a80c4e552abdbcce81659f5d80f33c371dea875c18f6c2a')
run=HERE/('run_'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'_%d'%os.getpid());run.mkdir()
rows=[]
def check(item,name,condition,detail=None):rows.append({'item':item,'name':name,'pass':bool(condition),'detail':detail})

# SF1: the RO1 checker is exactly the checker to which RESULT delegates the whole block.
armed={'rule':'RO1','armed':True,'fired':False,'events':[],'worker_sha256':'a'*64,'binding_sha256':'b'*64}
unarmed={'rule':'RO1','armed':False,'fired':False,'events':[],'worker_sha256':None,'binding_sha256':None}
for name,base,fun in [('armed',armed,lambda b:M.check_ro1_armed(b,'a'*64,'b'*64)),('unarmed',unarmed,M.check_ro1_unarmed)]:
    check('SF1',name+' exact six-key positive',fun(base)[0])
    for key,val in [('events_suppressed',2),('custom_payload',{'concealed_invalid':True})]:
        b=copy.deepcopy(base);b[key]=val;ok,det=fun(b)
        check('SF1',name+' must reject extra key '+key,not ok,det)
    b=copy.deepcopy(base);b['inadmissible_record']={}
    check('SF1',name+' explicit inadmissible_record remains rejected',not fun(b)[0])

# SF2: execute only inert pinned driver modules and actual token policy; invent additional triples.
for driver in ('r4','r5'):
    M.DRIVER[:]=M.DRIVERS[driver];M.DRIVER_RAW[:]=[None,None]
    d=M.load_driver()
    for gate,file in [('Z2','TOKENS_Z2_REPLACE_'+driver.upper()+'_C2V006.json'),
                      ('Z2_OFF_RO1','TOKENS_Z2_OFF_RO1_'+driver.upper()+'_C2V006.json'),
                      ('B0P_RERUN','TOKENS_B0P_RERUN_C2V006.json')]:
        tokdoc=M.jloads((G6/'tokens'/file).read_bytes());base=tokdoc['declared']
        check('SF2',driver+' '+gate+' supplied derived baseline policy',M.tokens_policy(gate,base,d)[0])
        for label,triple in [('verdict',['CONVERGED','NOT_CONVERGED','<A73_VERDICT>']),
                             ('numeric_string',['101.125','907.875','<A73_VALUE>'])]:
            own=copy.deepcopy(base)+[triple]
            tp=write(run/('TOKENS_'+driver+'_'+gate+'_'+label+'.json'),{'declared':own,'driver':['FALSE_DRIVER','0'*64]})
            ok,det=M.tokens_policy(gate,own,d)
            pairs,bad,joined=M.build_tokens(own)
            check('SF2',driver+' '+gate+' must refuse non-derived '+label+' triple',not ok or bool(bad),{'policy':det,'pair_errors':bad,'tokens':tp})
    base=M.jloads((G6/'tokens'/('TOKENS_Z2_REPLACE_'+driver.upper()+'_C2V006.json')).read_bytes())['declared']
    changed=copy.deepcopy(base);changed[0][0]='SYNTHETIC_UNDERIVED_REFERENCE';changed[0][2]='<A73_UNDERIVED_LABEL>'
    check('SF2',driver+' Z2 must bind reference and label as well as new side',not M.tokens_policy('Z2',changed,d)[0])

# Actual Side normalization proves non-derived tokens can neutralize verdict and numeric-string differences.
for label,triple in [('classification',['CONVERGED','NOT_CONVERGED','<A73_CLASS>']),('value',['101.125','907.875','<A73_VALUE>'])]:
    refs=[]
    for side,raw in [('reference',triple[0]),('new',triple[1])]:
        root=run/(label+'_'+side);root.mkdir();tree=M.Tree(root);store=M.Store(root,side)
        norm=M.Side(tree,store,[(raw,triple[2])],M.NORMALIZER_MARKERS+(triple[2],))
        refs.append(norm.norm({label:raw}))
    check('SF2','normalizer must retain non-derived '+label+' difference',not M.seq(*refs),refs)

# SF3: the actual allow predicate accepts any existing bytes with the specified sha.
M.DRIVER[:]=M.DRIVERS['r5'];M.DRIVER_RAW[:]=[None,None]
selected=M.driver_tables(M.driver_raw(),M.DRIVER[0]);selected_pairs={tuple(v) for tab in selected.values() for v in tab.values()}
ok,rev=M.static_pin_verifier(None)
own=write(run/'ARBITRARY_NOT_DRIVER_TABLE.bin',b'Independent synthetic non-code bytes\n')
rev['own']=(own['path'],own['sha256'])
check('SF3','arbitrary matching bytes must not be selected-driver pin',not ok('own',own['sha256']),own)
r4raw=Path(M.DRIVERS['r4'][0]).read_bytes();assert M.sha_b(r4raw)==M.DRIVERS['r4'][1]
r4=M.driver_tables(r4raw,M.DRIVERS['r4'][0]);different=next(v for tab in r4.values() for v in tab.values() if tuple(v) not in selected_pairs and Path(v[0]).is_file())
rev['r4only']=tuple(different)
check('SF3','r4-only pin must refuse with r5 selected',not ok('r4only',different[1]),{'pin':different,'selected':'r5'})
selected_pin=next(v for tab in selected.values() for v in tab.values() if Path(v[0]).is_file())
rev['selected']=tuple(selected_pin)
check('SF3','selected-driver matching-byte positive remains admitted',ok('selected',selected_pin[1]),selected_pin)
rev['badsha']=(own['path'],'0'*64)
check('SF3','wrong raw sha still refused',not ok('badsha','0'*64))

# N3: wholly new scratch directories, no forbidden production string or real run path involved.
plain=run/'SCRATCH_REGISTERED';(plain/'child').mkdir(parents=True)
def guard(name,path,registered,expect_refuse=True):
    real,why=F.guarded_resolve(str(path),registered=str(registered),marker='synthetic_forbidden_marker')
    check('N3',name,(why is not None)==expect_refuse,{'given':str(path),'registered':str(registered),'resolved':real,'reason':why})
guard('ordinary child containment positive',plain/'child',plain)
alias=Path('/System/Volumes/Data'+str(plain))
same=os.path.samefile(alias,plain)
check('N3','scratch firmlink aliases same inode',same)
guard('firmlink alias must be contained',alias/'child',plain)
nfc=run/'SCRATCH_CAFÉ';(nfc/'child').mkdir(parents=True)
nfd=Path(unicodedata.normalize('NFD',str(nfc)))
check('N3','scratch NFD aliases same inode',os.path.samefile(nfd,nfc))
guard('NFD alias must be contained',nfd/'child',nfc)
guard('sibling does not falsely match',run/'SCRATCH_REGISTERED_OTHER',plain,False)
guard('own marker remains blocked',run/'synthetic_forbidden_marker_probe',plain)

# N6: source-only. Do not execute the command script or writer: both name production runs.
cmd=G5/'R5_IDENTITY_COMPARE_COMMANDS.sh';cmdtext=cmd.read_text()
writer=G6/'tools/write_identity_records_c2v006.py';wtree=ast.parse(writer.read_bytes())
status_uses=[];verdict_predicates=[]
for node in ast.walk(wtree):
    if isinstance(node,(ast.If,ast.Assert)):
        text=ast.unparse(node.test)
        if 'status' in text or 'exit_code' in text:status_uses.append(text)
        if "rep.get('verdict')" in text:verdict_predicates.append(text)
check('N6','r5 command successor exists in c2v006 bundle',(G6/'R5_IDENTITY_COMPARE_COMMANDS.sh').exists())
check('N6','prior command requires receipt status, not merely existence','FINISHED' in cmdtext and 'receipt' in cmdtext,{'command':pin(cmd),'receipt_check':'existence-only source inspection; command not executed'})
check('N6','record writer predicates on receipt status or exit code',any('receipt' in x or 'rc.' in x for x in status_uses),{'all_status_predicates':status_uses,'writer':pin(writer)})
check('N6','record writer explicitly predicates on each comparator verdict',bool(verdict_predicates),verdict_predicates)

check('HYGIENE','candidate pin unchanged',pin(SOURCE)['sha256']==EXPECTED)
check('HYGIENE','no prohibited operation attempted',not BLOCKED,BLOCKED)
source_paths=[SOURCE,FILL,G6/'BUILD.md',G6/'DIFF_c2v005_c2v006.diff',G6/'tools/make_tokens_c2v006.py',writer,cmd,Path(__file__)]
result={'schema':'CX2_COMPARATOR_C2V006_A73_PROBES_V001','status':'TESTED','source_before':{'path':str(SOURCE),'sha256':EXPECTED},
 'source_after':pin(SOURCE),'passed':sum(x['pass'] for x in rows),'total':len(rows),'rows':rows,
 'scope':'A73 requirement predicates and synthetic scratch alias tests. False rows demonstrate missing requested restrictions, not test harness failures. No whole scientific gate comparison or production evidence read.',
 'source_pins':[pin(x) for x in source_paths],'reads':sorted(READS),'blocked_attempts':BLOCKED,'scientific_launches':0,
 'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
out=write(run/'A73_RESULTS.json',result)
print(json.dumps({'result':out,'passed':result['passed'],'total':result['total'],'failed':[x['name'] for x in rows if not x['pass']]}))
