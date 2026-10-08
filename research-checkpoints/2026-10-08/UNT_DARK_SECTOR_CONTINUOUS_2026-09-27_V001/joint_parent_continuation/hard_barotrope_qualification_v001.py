"""Inert root-owned C material qualifier. No ancestral producer imports.
freeze/build/benchmark/run emit JSON only. Compiler output is a new local
binary; all receipts are stdout for the root's immutable publisher.
"""
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
ROOT=PROJECT.parent
EXPECTED=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
FREEZE=HERE/'HARD_BAROTROPE_QUALIFICATION_V001_FROZEN.json'
BUILD_RECEIPT=HERE/'HARD_BAROTROPE_QUALIFICATION_V001_BUILD.json'
BUILD_DIR=HERE/'hard_barotrope_build_v001'
BINARY=BUILD_DIR/'unt_hard_barotrope_qualification_v001'
PROTOCOL=HERE/'HARD_BAROTROPE_QUALIFICATION_PROTOCOL_V001.md'
CONFIG=dict(expected_histories=335,expected_labels=1340,expected_backgrounds=5,
    expected_points=67,expected_finite_histories=295,expected_dust_histories=40,
    orders=[64,128],epoch_A=[1.,11.,101.,501.,1101.,3001.,10001.,1e7],
    independent_Simpson=[1024,2048],FD_log_steps=[1e-3,5e-4],
    comparison_atol=2e-13,comparison_rtol=2e-9,
    saved_anchor_rtol=2e-9,FD_atol=2e-11,FD_rtol=2e-6,
    FD_second_atol=2e-8,FD_raw_refinement_rtol=5e-5,
    synthetic_r1=[1e-12,1e-6,1.,1e6],synthetic_A=[1.,10.,1000.],
    domain_a=[1e-7,1.],rho_unit='saved Hcal-normalized excitation coefficient',
    no_CLASS_or_background_solve=True,no_observational_gate=True)
PINS={
 'BBN_SHARED_INVERSE_V001_RESULTS.json':'e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0',
 'BBN_SHARED_INVERSE_V001_FROZEN.json':'0bf25c368e90dddfc46bb418273851b66a426dc7e3ab0edc6d436fa3237ae9f3',
 'FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json':'f5302c8a70befba825b6c1252c75aac17efafc9280770bcc53b46fc0ae38c388',
 'unt_hard_barotrope_v001.h':'abfade89af77e4000bccd169c1ea18226315621f7dcb665901efa879e3a4aab6',
 'unt_hard_barotrope_v001.c':'3003b89d4dcd14a599cf924390b6b4a2151bb14e4221a2336458d89509a3c39d',
 'UNT_HARD_BAROTROPE_PROVIDER_PROTOCOL_V001.md':'308c605954106d70b7376b5665ae2ed2b47725b4a10b663509089ebf539a567a',
 'UNT_HARD_BAROTROPE_PROVIDER_PREFLIGHT_V001.md':'9f2043949371d5d9ad5dfa7cdf3baa5fff84a912731fd5134fb839e408b3f676'}
BAO_SHAS=['31cd0c151a6f6f906fa62ef84f3c3517b5ecbcd79f39beda29ecea2fddc9fdf2',
 '38e4ff97e7158e31b6ae1482f5f4ce7971d256d9b67f4c96beb7b4fc59eb3479',
 '8ac1241d4c378ab7ec6ced9447262cfb5df1772d23ab7a36349ed257437df772',
 'b6c5d0e95efae74f19a09c93c0b2637324fd7535b636cccb5df0a35203802503',
 '3bf9a0d352a64d0570177fdaf628d3c336ed6bb365415abffb69115ae6cd305f']
for _i,_sha in enumerate(BAO_SHAS):PINS[f'FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{_i}.json']=_sha
ARGV=['/usr/bin/clang','-std=c99','-O2','-Wall','-Wextra','-Wpedantic',
      '-fno-fast-math',str(HERE/'unt_hard_barotrope_v001.c'),
      str(HERE/'unt_hard_barotrope_qualification_v001.c'),'-lm','-o',str(BINARY)]
REMOVE_ENV=['CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','OBJC_INCLUDE_PATH',
            'LIBRARY_PATH','DYLD_LIBRARY_PATH','DYLD_INSERT_LIBRARIES']

def encoded(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(x):return hashlib.sha256(x).hexdigest()
def bound(p):
    p=Path(p).absolute();p.relative_to(PROJECT)
    for q in [p,*p.parents]:
        if q==PROJECT.parent:break
        if q.is_symlink():raise RuntimeError('Symlink not permitted: '+str(q))
    p.resolve().relative_to(PROJECT.resolve())
    return p
def read(p):return bound(p).read_bytes()
def wrapper(p,freeze_sha):
    w=json.loads(read(p))
    if w['freeze_sha256']!=freeze_sha or digest(encoded(w['payload']))!=w['payload_sha256']:
        raise RuntimeError('Changed wrapper: '+str(p))
    return w['payload']

def inputs():
    if HERE!=EXPECTED:raise RuntimeError('Wrong task/project location')
    files={}
    def register(p,expected=None):
        raw=read(p);sha=digest(raw)
        if expected is not None and sha!=expected:raise RuntimeError('Changed input: '+str(p))
        name=str(p.relative_to(ROOT))
        if name in files and files[name]!=sha:raise RuntimeError('Inconsistent ancestor')
        files[name]=sha
        return raw
    for name,sha in PINS.items():register(HERE/name,sha)
    for name in ['BBN_SHARED_INVERSE_V001_FROZEN.json','FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json']:
        for rel,sha in json.loads(read(HERE/name))['files'].items():register(ROOT/rel,sha)
    inv=wrapper(HERE/'BBN_SHARED_INVERSE_V001_RESULTS.json',PINS['BBN_SHARED_INVERSE_V001_FROZEN.json'])
    if inv['status']!='COMPLETE_CONDITIONAL_PROXY_INVERSE' or inv['failures']:
        raise RuntimeError('Unqualified inherited inverse')
    state={(r['background_id'],r['point_id'],r['spectrum_index']):r for r in inv['state_rows']}
    if len(state)!=1340 or len(inv['backgrounds'])!=5 or len(inv['table_points'])!=67:
        raise RuntimeError('Inverse census differs')
    histories=[]
    for bi in range(5):
        p=wrapper(HERE/f'FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{bi}.json',PINS['FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json'])
        if p['status']!='COMPLETE_BACKGROUND_SUBSET' or p['failures'] or p['selected_background_id']!=bi or len(p['records'])!=67:
            raise RuntimeError('Background subset not qualified')
        histories.extend(p['records'])
    histories.sort(key=lambda r:(r['background_id'],r['point_id']))
    if len(histories)!=335 or len({(r['background_id'],r['point_id']) for r in histories})!=335:
        raise RuntimeError('History census differs')
    if sum(r['finite_gap'] for r in histories)!=295:raise RuntimeError('Finite/dust census differs')
    for r in histories:
        if r['status']!='COMPLETE_CONDITIONAL_BACKGROUND':raise RuntimeError('Incomplete history')
        for si in range(4):
            s=state[(r['background_id'],r['point_id'],si)]
            expected='FINITE_HARD_STATE' if r['finite_gap'] else 'INFINITE_GAP_STANDARD_LIMIT'
            if s['status']!=expected:raise RuntimeError('History/label branch mismatch')
    for name in [Path(__file__).name,'unt_hard_barotrope_qualification_v001.c',PROTOCOL.name]:register(HERE/name)
    frozen=dict(schema='HARD_BAROTROPE_QUALIFICATION_FREEZE_V001',configuration=CONFIG,
                files=files,build_argv=ARGV,compiler_version_argv=['/usr/bin/clang','--version'],
                only_generated_binary=str(BINARY),environment_remove=REMOVE_ENV)
    return inv,state,histories,frozen

def environment():
    e=os.environ.copy()
    for key in REMOVE_ENV:e.pop(key,None)
    e.update(LC_ALL='C',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
             MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    return e

def invoke(argv,data=None):
    start=time.perf_counter();p=None;out=err=b'';exception=None
    def signal_child(sig):
        try:os.killpg(p.pid,sig)
        except ProcessLookupError:pass
    try:
        p=subprocess.Popen(argv,cwd=ROOT,env=environment(),stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        out,err=p.communicate(data)
    except BaseException as exc:
        exception=type(exc).__name__+': '+str(exc)
        if p is not None:
            if p.poll() is None:signal_child(signal.SIGTERM)
            try:out,err=p.communicate(timeout=5.)
            except subprocess.TimeoutExpired:
                signal_child(signal.SIGKILL);out,err=p.communicate()
    return dict(argv=argv,returncode=None if p is None else p.returncode,exception=exception,
                seconds=time.perf_counter()-start,stdout_sha256=digest(out),stderr_sha256=digest(err),
                stdout_base64=base64.b64encode(out).decode(),stderr_base64=base64.b64encode(err).decode()),out

def build(frozen):
    bound(BUILD_DIR)
    if not BUILD_DIR.exists():BUILD_DIR.mkdir(mode=0o700)
    if not BUILD_DIR.is_dir():raise RuntimeError('Build path not a directory')
    bound(BINARY)
    if BINARY.exists() or BINARY.is_symlink():raise RuntimeError('Refuse overwrite of existing binary')
    version,_=invoke(['/usr/bin/clang','--version'])
    if version['returncode']!=0:return dict(status='COMPILER_IDENTITY_FAILED',version=version)
    receipt,_=invoke(ARGV)
    okay=receipt['returncode']==0 and receipt['exception'] is None and BINARY.is_file()
    binary=None
    if BINARY.exists():
        raw=read(BINARY);binary=dict(path=str(BINARY),bytes=len(raw),sha256=digest(raw))
    return dict(status='COMPLETE_BUILD' if okay else 'FAILED_BUILD',version=version,compiler=receipt,binary=binary)

def run(state,histories,benchmark,freeze_sha):
    build_payload=wrapper(BUILD_RECEIPT,freeze_sha)
    if build_payload['status']!='COMPLETE_BUILD' or build_payload['compiler']['argv']!=ARGV:
        raise RuntimeError('Missing matching successful build')
    if build_payload['binary']['sha256']!=digest(read(BINARY)):raise RuntimeError('Binary differs from build receipt')
    selected=histories
    if benchmark:
        selected=[next(r for r in histories if not r['finite_gap']),next(r for r in histories if r['finite_gap'])]
    lines=[];mapping=[];ids={};hmeta=[]
    for r in selected:
        bi,pi=r['background_id'],r['point_id'];idx=histories.index(r)
        hmeta.append(dict(history_id=idx,background_id=bi,point_id=pi,point_roles=r['point_roles'],finite_gap=r['finite_gap']))
        for si in range(4):
            s=state[(bi,pi,si)];rowid=4*idx+si;finite=r['finite_gap']
            values=[rowid,1 if finite else 2,1 if si==0 else 0,
                    s['R'] if finite else 0.,s['I'] if finite else 0.,s['hard_energy'] if finite else 0.,s['Omega_exc'],
                    s['w'] if finite else 0.,s['cI2'] if finite else 0.,s['omega']/s['R'] if finite else 0.,r['r1']]
            lines.append(' '.join(str(x) for x in values));ids[rowid]=(r,s)
            mapping.append(dict(id=rowid,history_id=idx,background_id=bi,point_id=pi,spectrum_index=si,status=s['status']))
    data=(f'1 {len(lines)}\n'+'\n'.join(lines)+'\n').encode()
    process,raw=invoke([str(BINARY)],data)
    try:
        material=json.loads(raw)
        encoded(material) # reject nonfinite JSON before publication, preserving raw
    except Exception:material=None
    checks=[]
    def ck(name,a,b,atol=2e-13,rtol=2e-9,context=None):
        finite=isinstance(a,(int,float)) and isinstance(b,(int,float)) and math.isfinite(a) and math.isfinite(b)
        error=abs(a-b)/(atol+rtol*max(abs(a),abs(b))) if finite else None
        checks.append(dict(check=name,context=context,tolerance_fraction=error,passed=error is not None and error<=1.))
    validation_error=None;material_passed=False
    try:
        if material is None:raise RuntimeError('C stdout is not a JSON packet')
        if material['schema']!='UNT_HARD_QUALIFIER_C_V001':raise RuntimeError('C output schema differs')
        rows={r['id']:r for r in material['rows']}
        if len(rows)!=len(material['rows']) or set(rows)!=set(ids)|{-1,-2,-3,-4}:
            raise RuntimeError('C output census differs')
        for rowid,(old,s) in ids.items():
            out=rows[rowid]
            if rowid%4 or not out['epochs']:continue
            epochs_by_A={e[0]:e for e in out['epochs']}
            for olde in old['epochs']:
                A=olde['A']
                if A not in epochs_by_A:continue # C failed evaluation remains in material failures
                new=epochs_by_A[A]
                for index,key in [(1,'energy_over_present'),(2,'w'),(3,'cI2')]:
                    ck('saved_history_'+key,new[index],olde[key],context=[rowid,A])
        for r in selected:
            idx=histories.index(r);ref=rows[4*idx]['epochs']
            for si in range(1,4):
                other=rows[4*idx+si]['epochs']
                if ref and other:
                    for k in ([2,3,4,5] if r['finite_gap'] else [2,3]):
                        ck('four_copy_present_identity',ref[0][k],other[0][k],context=[idx,si,k])
        if not isinstance(material['failures'],list) or not isinstance(material['checks'],int):
            raise RuntimeError('C control ledger differs')
        status=material['status']
        if status not in ('COMPLETE_MATERIAL_QUALIFICATION','FAILED_CONTROLS'):
            raise RuntimeError('C status differs')
        material_passed=status=='COMPLETE_MATERIAL_QUALIFICATION'
        if material_passed and material['failures']:
            raise RuntimeError('Success status contains failed controls')
    except Exception as exc:
        validation_error=type(exc).__name__+': '+str(exc)
    passed=validation_error is None and material_passed and process['returncode']==0 and process['exception'] is None and all(c['passed'] for c in checks)
    # Always retain byte-exact stdout, including malformed/partial packets.
    return dict(status=('COMPLETE_BENCHMARK_ONLY' if benchmark else 'COMPLETE_335_HISTORY_MATERIAL_QUALIFICATION') if passed else 'FAILED_QUALIFICATION',
                benchmark_only=benchmark,history_count=len(selected),label_count=len(ids),configuration=CONFIG,
                history_metadata=hmeta,retained_label_mapping=mapping,stdin_sha256=digest(data),process=process,
                epoch_columns=['A','rho_over_rho1','w','ca2','omega_over_R','r','dw_dln_a','dca2_dln_a','log_action_residual','reference_energy_relative_error'],
                material=material,validation_error=validation_error,comparison_count=len(checks),comparison_maximum=max((c['tolerance_fraction'] for c in checks if c['tolerance_fraction'] is not None),default=0.),
                comparison_nonfinite=sum(c['tolerance_fraction'] is None for c in checks),
                comparison_failures=[c for c in checks if not c['passed']],
                scope='Standalone material qualification, not CLASS, recombination, CMB or observational success.')

def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ('freeze','build','benchmark','run'):
        raise RuntimeError('Use freeze, build, benchmark or run')
    _,state,histories,frozen=inputs();mode=sys.argv[1]
    if mode=='freeze':print(encoded(frozen).decode());return
    frozen_raw=read(FREEZE)
    if json.loads(frozen_raw)!=frozen:raise RuntimeError('Source/input freeze differs')
    fsha=digest(frozen_raw)
    payload=build(frozen) if mode=='build' else run(state,histories,mode=='benchmark',fsha)
    packet=dict(freeze_sha256=fsha,payload_sha256=digest(encoded(payload)),payload=payload)
    print(encoded(packet).decode())
    if payload['status'].startswith('FAILED') or payload['status']=='COMPILER_IDENTITY_FAILED':sys.exit(1)

if __name__=='__main__':main()
