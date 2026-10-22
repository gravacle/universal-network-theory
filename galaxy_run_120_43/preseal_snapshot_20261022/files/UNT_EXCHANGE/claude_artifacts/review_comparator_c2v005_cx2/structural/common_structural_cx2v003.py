"""Structural comparator review support; isolated files, no process or network calls."""
import hashlib
import io
import json
import os
import sys
import types
from pathlib import Path
import numpy as np

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUT=ART/'review_comparator_c2v005_cx2/structural'
BLOCKED=[]

def audit(event,args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn',
            'os.fork','os.forkpty','os.exec','pty.spawn'):
        BLOCKED.append(event);raise RuntimeError('REVIEW_NO_PROCESS_OR_NETWORK '+event)
    if event in ('os.remove','os.rmdir','os.rename','os.replace','shutil.rmtree'):
        BLOCKED.append(event);raise RuntimeError('REVIEW_NO_DELETE_OR_MOVE '+event)
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])).resolve();low=str(p).lower()
        if '/runs_ext/uvt_' in low or 'kmax_a2f10_c5h_run_v001' in low or '/.codex/' in low:
            raise RuntimeError('REVIEW_FORBIDDEN_READ '+str(p))
        if 'ngc3198' in low and any(x in low for x in ('target','observed','rotmod')):
            raise RuntimeError('REVIEW_FORBIDDEN_TARGET '+str(p))
        mode=args[1] if len(args)>1 else ''
        flags=args[2] if len(args)>2 else 0
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (
            isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing and (not p.is_relative_to(OUT.resolve()) or not isinstance(flags,int) or not flags&os.O_EXCL):
            raise RuntimeError('REVIEW_EXCLUSIVE_OWN_WRITES_ONLY '+str(p))
sys.addaudithook(audit)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def write(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    raw=value if isinstance(value,bytes) else canonical(value)+b'\n'
    with p.open('xb') as f:f.write(raw)
    return pin(p)
def load(p,name,expected=None):
    raw=Path(p).read_bytes()
    if expected is not None and hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('SOURCE_PIN_MISMATCH')
    m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m
    exec(compile(raw,str(p),'exec'),m.__dict__);return m
def array_bytes(npz=False):
    buf=io.BytesIO()
    if npz:np.savez(buf,pressure=np.array([1.25,2.5],dtype=np.float64))
    else:np.save(buf,np.array([3.75],dtype=np.float64),allow_pickle=False)
    return buf.getvalue()

def build_tree(root,driver,cmp,cm,*,defect=None,reorder=False,both_input=False):
    """Invent a tiny saved tree. No driver normalization, scientific execution, or copying a prior fixture."""
    root=Path(root)
    tables=cmp.driver_tables(driver[0])
    start={'driver':driver[0],'driver_sha256':driver[1],'fixture_only':True,'utc':'2026-10-18T00:00:00Z'}
    result={'driver_sha256':driver[1],'status':'COMPLETED','valid':True,'final_pass':1,'speeds_km_s':{'synthetic':1.25},
        'rows':[{'id':'synthetic','speed':1.25}],
        'passes':[{'pass':1,'rows':[{'id':'synthetic','speed':1.25}],'max_abs_change_km_s':None}],
        'scientific_context':{'equation':'synthetic','nested':[{'pressure_scale':1.25,'converged':True}]},
        'ended_unix_ns':100}
    if defect=='result_nested_pressure':result['scientific_context']['nested'][0]['pressure_scale']=1.2500000000000002
    if defect=='result_key_removed':result['scientific_context']['nested'][0].pop('converged')
    if defect=='result_key_added':result['scientific_context']['unexpected_constraint']=False
    if defect=='result_clock_only':result['ended_unix_ns']=999
    if reorder:result=dict(reversed(list(result.items())))
    result_pin=write(root/'result.json',result)
    write(root/'start.json',start)
    finish={'status':'COMPLETED','valid':True,'result_path':str(root/'result.json'),
            'result_sha256':result_pin['sha256'],'completion_measure':{'residual':0.125},'ended_unix_ns':101}
    if defect=='finish_nested_residual':finish['completion_measure']['residual']=0.25
    if defect=='finish_status':finish['status']='FAILED'
    write(root/'finish.json',finish)
    inp={'physical':{'mass_scale':2.0},'solver_contract':{'exact_mode':'SYNTHETIC'},'record_sequence':[1,2,3]}
    if defect=='input_nested_contract':inp['solver_contract']['exact_mode']='FOREIGN'
    write(root/'inputs/call_contract.json',inp)
    if defect!='input_missing_raw':write(root/'inputs/unaligned_source.bin',b'\x01\x02\x03\x04' if defect!='input_raw_byte' else b'\x01\x02\x03\x05')
    if both_input:write(root/'inputs/parallel_metadata.json',{'same_extension':{'enabled':True}})
    if defect=='input_extra':write(root/'inputs/extra_admission.json',{'hidden':True})
    for dirname,kind in [('01_route_a','route_a'),('02_reference','reference'),('03_body','body')]:
        if defect=='missing_body' and kind=='body':continue
        if defect=='renamed_body' and kind=='body':dirname='03_body_hidden'
        d=root/'stages'/dirname
        if kind=='route_a':
            worker=tables['PARALLEL_ROUTE_A']['worker'];solver=tables['PARALLEL_ROUTE_A']['solver']
            argv=['--column-workers','8','--solver',solver[0],'--solver-sha256',solver[1]]
        else:
            worker=tables['SCRIPTS'][kind]
            argv=['--contract',str(root/'inputs/call_contract.json')]
        write(d/'request.json',{'kind':kind,'script':worker[0],'script_sha256':worker[1],'argv':argv})
        if kind=='route_a':
            ident={'kind':'identity','format':cm.FORMAT,'identity':{'caller':{'record':cm.encode({'fixture_only':True,'s':1.25})}}}
            ident['payload_sha256']=cm._sha(cm._canonical(ident))
            write(d/'checkpoint/IDENTITY.json',cm._canonical(ident)+b'\n')
            write(d/'checkpoint/blobs/canary.npy',array_bytes())
            write(d/'checkpoint/iteration_0000/COMPLETED.json',{'iteration':0,'fixture_only':True})
            write(d/'attempt_000/arrays/000000_state.npz',array_bytes(True))
            attempt={'status':'COMPLETED','scientific_measure':{'entropy':4.5},'contraction':[0.5,0.25]}
            if defect=='attempt_entropy':attempt['scientific_measure']['entropy']=4.500000000000001
            if defect=='attempt_key_removed':attempt.pop('contraction')
            write(d/'attempt_000/result.json',attempt)
            write(d/'attempt_000/start.json',{'fixture_only':True,'iteration_start':0})
        else:
            value={'kind':kind,'nested':{'force':3.5},'ended_unix_ns':102}
            if defect=='body_payload' and kind=='body':value['nested']['force']=7.
            write(d/'data/result.json',value)
    if defect in ('duplicate_body_first','duplicate_body_last'):
        extra='00_body' if defect.endswith('first') else '97_body'
        write(root/'stages'/extra/'data/result.json',{'kind':'body','nested':{'force':99.}})
    if defect=='paired_duplicate_body':
        write(root/'stages/44_body/data/result.json',{'kind':'body','nested':{'force':3.5},'ended_unix_ns':102})
    if defect=='triple_body_collision':
        write(root/'stages/00_body/data/result.json',{'kind':'body','nested':{'force':3.5},'ended_unix_ns':102})
        write(root/'stages/88_body/data/result.json',{'kind':'body','nested':{'force':19.},'ended_unix_ns':102})
        write(root/'stages/99_body/data/result.json',{'kind':'body','nested':{'force':3.5},'ended_unix_ns':102})
    if defect=='empty_extra_stage':(root/'stages/77_unexpected').mkdir(parents=True)
    return root
