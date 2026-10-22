"""0859/0330 metadata pre-stage. Does not write C1, ROOT_BOUND, source reviews or launch plans.

prepare authenticates explicit inputs and writes only new nonadmissible metadata.
execute-root-only runs the pinned static F1 replay, never a scientific launcher.
That mode is reserved to Claude2 because F1 reads production custody. It has not
been exercised on production inputs by Codex2. No reviewed source is rewritten.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import types

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = ART/'eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build'
PINFILE = {'path':str(HERE/'SOURCE_PINS_CX2V001.json'),
           'sha256':'76ffd4a204bbc5d9c9be10deab8cd9cbbb2c6218323782c4eb36b9df1ab3fab6'}
PYTHON = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
BLAS = {k:'1' for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
                       'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS')}
PLAN_SCHEMA = 'A296_POST_C1_INPUTS_CX2V001'
PREPARED_SCHEMA = 'A296_POST_C1_PREPARED_CX2V001'
REQUEST_FIELDS = {'schema','records','verification','c1','genesis_registry','approved_producers'}

class Refused(ValueError):
    pass

def need(ok, why):
    if not ok:
        raise Refused(why)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def encode(value):
    return (json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()

def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'DUPLICATE_JSON_KEY');out[k]=v
        return out
    def constant(value):
        raise Refused('NONFINITE_JSON')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)

def exact_pin(ref):
    need(isinstance(ref,dict) and set(ref)=={'path','sha256'},'EXACT_PIN_REQUIRED')
    need(isinstance(ref['path'],str) and isinstance(ref['sha256'],str) and
         len(ref['sha256'])==64 and all(x in '0123456789abcdef' for x in ref['sha256']),
         'MALFORMED_PIN')
    return ref

def lexical(value):
    need(isinstance(value,str) and os.path.isabs(value) and os.path.normpath(value)==value,
         'ABSOLUTE_NORMALIZED_PATH_REQUIRED')
    p=Path(value)
    forbidden={'.codex','runs','runs_ext','unt_internal_runs','v007_postseal_records',
               'kmax_a2f10_c5h_run_v001'}
    need(not any(x.casefold() in forbidden or 'ngc3198' in x.casefold() or
                 x.casefold().startswith('uvt_') for x in p.parts),'PROTECTED_PATH_REFUSED')
    return p

def safe_path(value):
    # Inspect each link destination lexically BEFORE probing that destination.
    p=lexical(str(value));todo=list(p.parts[1:]);current=Path('/');links=0
    while todo:
        part=todo.pop(0)
        if part in ('','.'):
            continue
        if part=='..':
            current=current.parent;continue
        candidate=lexical(str(current/part))
        try: mode=os.lstat(candidate).st_mode
        except FileNotFoundError:
            current=candidate;continue
        if stat.S_ISLNK(mode):
            links+=1;need(links<=40,'SYMLINK_LOOP')
            target=os.readlink(candidate)
            dest=lexical(os.path.normpath(target if os.path.isabs(target) else str(current/target)))
            todo=list(dest.parts[1:])+todo;current=Path('/')
        else:
            current=candidate
    return lexical(str(current))

class Snapshot:
    def __init__(self):
        self.cache={}

    def read(self,ref):
        exact_pin(ref)
        logical=lexical(ref['path'])
        need(logical.is_relative_to(ART),'ARTIFACT_INPUT_REQUIRED')
        p=safe_path(logical);name=str(p)
        if name not in self.cache:
            fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
            try:
                before=os.fstat(fd)
                need(stat.S_ISREG(before.st_mode) and before.st_size<=16*1024*1024,
                     'REGULAR_BOUNDED_INPUT_REQUIRED')
                chunks=[];n=0
                while True:
                    b=os.read(fd,1024*1024)
                    if not b:break
                    n+=len(b);need(n<=16*1024*1024,'INPUT_SIZE_LIMIT');chunks.append(b)
                after=os.fstat(fd);raw=b''.join(chunks)
                need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
                     (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
                     and len(raw)==after.st_size,'INPUT_CHANGED_DURING_READ')
                self.cache[name]=raw
            finally:os.close(fd)
        raw=self.cache[name];need(sha(raw)==ref['sha256'],'INPUT_SHA_MISMATCH')
        return raw

    def doc(self,ref):
        return decode(self.read(ref))

def validate_binding(s,ref,pins):
    # This pinned helper was inspected: pathlib import, constants and function
    # definitions only. Its validator reads bytes; it imports no custody/driver.
    raw=s.read(pins['binding']);m=types.ModuleType('_post_c1_binding')
    m.__file__=pins['binding']['path'];exec(compile(raw,m.__file__,'exec'),m.__dict__)
    bound=m.validate_binding(s,ref)
    c1=s.doc(bound['c1'])
    need(c1.get('schema')=='UNT_DDO154_C1_TAIL_READINESS_H1_C2V002',
         'FROZEN_SUCCESSOR_C1_REQUIRED')
    frozen=c1.get('frozen')
    need(isinstance(frozen,dict) and frozen.get('synthetic_test') is False and
         'placeholder' not in c1,'REAL_FROZEN_C1_REQUIRED')
    return bound

def source_successor(old,pins):
    need(isinstance(old,dict) and bool(old),'SOURCES_REQUIRED')
    new=dict(old)
    for role in ('direct_cert_lookup_a296','direct_preflight_cert_a296','registry_verify_a296','custody_snapshot'):
        choices=pins[role];present=[p for p in choices if p['path'] in new]
        need(len(present)==1 or (role=='custody_snapshot' and not present),
             'MISSING_OR_AMBIGUOUS_SOURCE_SLOT: '+role)
        for p in present:
            need(new[p['path']]==p['sha256'],'STALE_SOURCE_SLOT: '+role)
            del new[p['path']]
        final=choices[-1];new[final['path']]=final['sha256']
    return new

def render(s,binding_ref,inputs_ref,outdir,date_u,*,binding_validator=validate_binding):
    pins=s.doc(PINFILE)
    for role in ('direct_cert_lookup_a296','direct_preflight_cert_a296','registry_verify_a296','custody_snapshot'):
        s.read(pins[role][-1])
    plan=s.doc(inputs_ref)
    need(isinstance(plan,dict) and set(plan)=={'schema','lookup_request_predecessor','records',
         'verification','admission_predecessor','replay_out_dir'} and plan['schema']==PLAN_SCHEMA,'INPUT_PLAN_FIELDS')
    bound=binding_validator(s,binding_ref,pins)
    old=s.doc(plan['lookup_request_predecessor'])
    need(isinstance(old,dict) and set(old) in (REQUEST_FIELDS,REQUEST_FIELDS|{'a296_binding'}) and
         old['schema']=='DIRECT_CERT_LOOKUP_REQUEST_CX2V001','REQUEST_PREDECESSOR_FIELDS')
    genesis=bound['document']['genesis_registry']
    need(old['genesis_registry']==genesis,'REQUEST_GENESIS_CHANGED')
    records=s.doc(plan['records']);verified=s.doc(plan['verification'])
    need(records.get('schema')=='CP1_POINTS_LEDGER_RECORDS_C2V001' and
         records.get('generator')==pins['assembler'] and
         records.get('a296_binding')==binding_ref and records.get('genesis_registry')==genesis,
         'BOUND_RECORDS_REQUIRED')
    approved=bound['tail_readiness']['approved_certificate_producers']
    need(records.get('approved_certificate_producers')==approved,'RECORDS_PRODUCERS_MISMATCH')
    need(verified.get('schema')=='CP1_POINTS_OFFLINE_VERIFY_C2V001' and
         verified.get('generator')==pins['assembler'] and verified.get('a296_binding')==binding_ref and
         verified.get('records')==plan['records'] and verified.get('c1')==bound['c1'] and
         verified.get('genesis_registry')==genesis and verified.get('ok') is True and
         verified.get('c1_policy_gate')=={'ok':True,'blockers':[]},'BOUND_VERIFICATION_REQUIRED')
    # This is only metadata coherence. F1 must still validate and replay fully.
    cfg=s.doc(plan['admission_predecessor'])
    need(isinstance(cfg,dict) and 'source_review' in cfg and
         cfg.get('direct_context') in pins['direct_preflight_cert_a296'],
         'KNOWN_DIRECT_CONTEXT_SLOT_REQUIRED')
    need(isinstance(cfg.get('direct_certificate_lookup'),dict) and
         set(cfg['direct_certificate_lookup'])=={'request','manifest'},'LOOKUP_ADMISSION_SLOT_REQUIRED')
    need(cfg['direct_certificate_lookup']['request']==plan['lookup_request_predecessor'],
         'ADMISSION_REQUEST_PREDECESSOR_MISMATCH')
    dest=lexical(str(outdir));need(dest.is_relative_to(HERE),'OUTPUT_UNDER_PRESTAGE_BUILD_REQUIRED')
    approved_raw=encode({'approved_certificate_producers':approved})
    approved_ref={'path':str(dest/'APPROVED_PRODUCERS.json'),'sha256':sha(approved_raw)}
    request=copy.deepcopy(old)
    request.update(c1=bound['c1'],a296_binding=binding_ref,records=plan['records'],
                   verification=plan['verification'],approved_producers=approved_ref)
    request_raw=encode(request);request_ref={'path':str(dest/'LOOKUP_REQUEST.json'),'sha256':sha(request_raw)}
    cfg=copy.deepcopy(cfg);cfg['direct_context']=pins['direct_preflight_cert_a296'][-1]
    cfg['sources']=source_successor(cfg.get('sources'),pins)
    cfg['direct_certificate_lookup']={'request':request_ref,'manifest':None}
    cfg['source_review']=None
    replay_dir=safe_path(plan['replay_out_dir'])
    lookup_here=safe_path(pins['direct_cert_lookup_a296'][-1]['path']).parent
    need(replay_dir.is_relative_to(lookup_here) and replay_dir!=lookup_here
         and not os.path.lexists(replay_dir) and replay_dir.parent.is_dir(),
         'F1_EXCLUSIVE_OUTPUT_DIRECTORY_REQUIRED')
    argv=[PYTHON,'-I','-B',pins['direct_cert_lookup_a296'][-1]['path'],
          '--request',request_ref['path'],'--request-sha256',request_ref['sha256'],
          '--out-dir',str(replay_dir)]
    command={'schema':'A296_STATIC_F1_REPLAY_COMMAND_CX2V001','role':'STATIC_F1_REPLAY_ONLY_NOT_STEP4_LAUNCHER',
             'date_u':date_u,'argv':argv,'environment':BLAS,'generator':pins['direct_cert_lookup_a296'][-1],
             'requires':'Claude2 root-only custody replay authorization','execution':'UNTESTED',
             'production_admissible':False}
    files={'APPROVED_PRODUCERS.json':approved_raw,'LOOKUP_REQUEST.json':request_raw,
           'ADMISSION_PRESTAGE.json':encode(cfg),'F1_REPLAY_COMMAND.json':encode(command)}
    prepared={'schema':PREPARED_SCHEMA,'date_u':date_u,'binding':binding_ref,'inputs':inputs_ref,
              'generator':pins['direct_cert_lookup_a296'][-1],'source_pins':PINFILE,
              'request':request_ref,'replay_dir':str(replay_dir),'production_admissible':False,
              'status':'PREPARED_ROOT_REPLAY_AND_DISTINCT_SOURCE_REVIEW_REQUIRED',
              'files':{name:{'path':str(dest/name),'sha256':sha(raw)} for name,raw in files.items()}}
    files['PREPARED.json']=encode(prepared)
    return files

def write_new(path,raw):
    with Path(path).open('xb') as f:f.write(raw)

def prepare(binding_ref,inputs_ref,outdir,*,date_u=None,binding_validator=validate_binding):
    dest=safe_path(outdir)
    need(dest==Path(outdir) and dest.is_relative_to(HERE) and not os.path.lexists(dest)
         and dest.parent.is_dir(),'EXCLUSIVE_OUTPUT_DIRECTORY_REQUIRED')
    date_u=date_u or subprocess.check_output(['/bin/date','-u'],text=True).strip()
    files=render(Snapshot(),binding_ref,inputs_ref,dest,date_u,binding_validator=binding_validator)
    os.mkdir(dest)
    for name,raw in files.items():write_new(dest/name,raw)
    return {'path':str(dest/'PREPARED.json'),'sha256':sha(files['PREPARED.json'])}

def root_executor(argv):
    result=subprocess.run(argv,env={**os.environ,**BLAS},stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    need(result.returncode==0,'F1_REPLAY_NONZERO: '+str(result.returncode))
    return decode(result.stdout)

def execute_prepared(prepared_ref,*,executor=root_executor,binding_validator=validate_binding):
    s=Snapshot();p=s.doc(prepared_ref)
    need(p.get('schema')==PREPARED_SCHEMA and p.get('production_admissible') is False,'PREPARED_SCHEMA')
    dest=Path(prepared_ref['path']).parent
    expected=render(s,p['binding'],p['inputs'],dest,p['date_u'],binding_validator=binding_validator)
    need(s.read(prepared_ref)==expected['PREPARED.json'],'PREPARED_RECONSTRUCTION_MISMATCH')
    for name,ref in p['files'].items():
        need(s.read(ref)==expected[name],'PREPARED_FILE_MISMATCH')
    for name in ('ADMISSION_CANDIDATE.json','SOURCE_REVIEW_REQUEST.json','FINALIZE_RESULT.json'):
        need(not os.path.lexists(safe_path(dest/name)),'FINAL_OUTPUT_EXISTS')
    replay_dir=safe_path(p['replay_dir'])
    need(not os.path.lexists(replay_dir),'REPLAY_OUTPUT_EXISTS')
    command=decode(expected['F1_REPLAY_COMMAND.json'])
    # Only this root-only seam executes code outside this finalizer. Tests inject
    # a synthetic executor; neither mode calls the Step4 binder or launcher.
    result=executor(command['argv'])
    need(isinstance(result,dict) and isinstance(result.get('manifest'),dict),'F1_RESULT_REQUIRED')
    manifest_ref=exact_pin(result['manifest'])
    need(manifest_ref['path']==str(replay_dir/'MANIFEST.json'),'F1_MANIFEST_OUTPUT_PATH')
    manifest=s.doc(manifest_ref)
    need(manifest.get('schema')=='DIRECT_CERT_LOOKUP_MANIFEST_CX2V001' and
         manifest.get('generator')==p['generator'] and manifest.get('request')==p['request'] and
         manifest.get('verification_replayed') is True,'GENUINE_FINAL_F1_MANIFEST_REQUIRED')
    request=decode(expected['LOOKUP_REQUEST.json']);records=s.doc(request['records'])
    need(manifest.get('points_list')==records.get('points_list') and
         manifest.get('wave')==records.get('wave'),'F1_MANIFEST_RECORD_BINDING')
    need(isinstance(manifest.get('points'),list) and bool(manifest['points']),'F1_MANIFEST_POINTS')
    for point in manifest['points']:
        ref=exact_pin(point['spec'])
        need(Path(ref['path']).parent==replay_dir and Path(ref['path']).name=='SPEC_'+point['key']+'.json',
             'F1_SPEC_OUTPUT_PATH')
        s.read(ref)
    cfg=decode(expected['ADMISSION_PRESTAGE.json'])
    cfg['direct_certificate_lookup']['manifest']=manifest_ref
    review={'schema':'A296_POST_C1_SOURCE_REVIEW_REQUEST_CX2V001','status':'REVIEW_REQUIRED',
            'requested_sources':cfg['sources'],'predecessor_source_review':
                s.doc(s.doc(p['inputs'])['admission_predecessor']).get('source_review'),
            'production_admissible':False}
    outputs={'ADMISSION_CANDIDATE.json':encode(cfg),'SOURCE_REVIEW_REQUEST.json':encode(review)}
    done={'schema':'A296_POST_C1_FINALIZE_RESULT_CX2V001','date_u':
          subprocess.check_output(['/bin/date','-u'],text=True).strip(),
          'prepared':prepared_ref,'manifest':manifest_ref,'root_replay_returned_success':True,
          'production_admissible':False,'pending':['distinct source-review exact approved_sources',
          'root source/admission publication','actual Step4 binder command entry'],
          'outputs':{n:{'path':str(dest/n),'sha256':sha(raw)} for n,raw in outputs.items()}}
    outputs['FINALIZE_RESULT.json']=encode(done)
    for name,raw in outputs.items():write_new(dest/name,raw)
    return {'path':str(dest/'FINALIZE_RESULT.json'),'sha256':sha(outputs['FINALIZE_RESULT.json'])}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='mode',required=True)
    for mode in ('prepare','finalize-root-only'):
        p=sub.add_parser(mode)
        for arg in ('binding','binding-sha256','inputs','inputs-sha256','out-dir'):p.add_argument('--'+arg,required=True)
        if mode=='finalize-root-only':
            p.add_argument('--actor',choices=('Claude2',),required=True)
            p.add_argument('--ack-root-only-custody-replay',action='store_true',required=True)
    p=sub.add_parser('execute-root-only')
    for arg in ('prepared','prepared-sha256'):p.add_argument('--'+arg,required=True)
    p.add_argument('--actor',choices=('Claude2',),required=True)
    p.add_argument('--ack-root-only-custody-replay',action='store_true',required=True)
    a=ap.parse_args(argv)
    if a.mode in ('prepare','finalize-root-only'):
        result=prepare({'path':a.binding,'sha256':a.binding_sha256},
                       {'path':a.inputs,'sha256':a.inputs_sha256},a.out_dir)
        if a.mode=='finalize-root-only':result=execute_prepared(result)
    else:
        result=execute_prepared({'path':a.prepared,'sha256':a.prepared_sha256})
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    try:main()
    except (Refused,ValueError,KeyError,TypeError,OSError) as exc:
        print('REFUSED: '+str(exc),file=sys.stderr);raise SystemExit(3)
