#!/usr/bin/env python3
"""Root-owned saved-array aggregation only; no scientific producer/helper imports."""
import argparse
import hashlib
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
STEM = 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001'
PARENT = 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001'
AUTHOR_GUARD = False
PINS = {
 'cross_u_full_flrw_source_constraint_v001.py':'8e2860917a75c44ada5be0df18ac43809dc7fe454846b3787d8a3d3017d1e5c1',
 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_V001.md':'4f2611f0fda44d326034aba5c38bcf532dc69e912f5f3d1d135f335975b5a5a6',
 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_MANIFEST.json':'fba438e9df2246cbefa27f0b5226e41f435de8632e035d0660ed8f5bf3f6b77d',
 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_ERROR.json':'e128383f1c9a1725ec4480c3ad7e87b99d09a3b699a5bd40bac2414e6df9bb03',
 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_RECEIPT.json':'bf5c48b986549b92593ff7d20a4fb05ee5c7b75cbec878ee80c2342db29daafe',
 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001.md':'c6d9d9605c8c3eea7abc62109afdc5bdea77d6c6d0200ff422907806637ca630',
}
FLOOR, STATE_TOL, ROW_TOL, NORMAL_TOL, INCREMENT_TOL = 1e-13, 1e-3, 2e-11, 1e-6, 1e-6
SAMPLE_ALLOWANCE = 16 * 2.**-52
MAXIMA = ('angular_reality','core_rows','density_identity_error','memory_quadrature',
 'metric_momentum','momentum_identity_error','native_rows','normal_error','normal_propagation',
 'ordinary_density','phase_density','phase_quadrature','proper_trace_increment','radiation_density',
 'trace_error','whole_density_increment')
INCREMENTS = ('metric_momentum','ordinary_density','phase_density','radiation_density',
 'proper_trace_increment','whole_density_increment')
WITHDRAWN = ('trace_error','momentum_identity_error')
CONTEXT, OUTPUTS = {}, {}

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(name): return json.loads((BASE/name).read_text())
def encode(v): return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def verify(mapping):
    for name,h in mapping.items():
        if sha(BASE/name)!=h: raise ValueError('Actual byte seal '+name)

def write(name,value):
    raw=value if isinstance(value,bytes) else encode(value)
    p=BASE/name
    with p.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
    if p.read_bytes()!=raw: raise IOError('Exact exclusive byte reread '+name)
    OUTPUTS[name]=sha(p)
    return OUTPUTS[name]

def merge(*maps):
    result={}
    for mapping in maps:
        for name,h in mapping.items():
            key=str((BASE/name).resolve())
            if key in result and result[key]!=h: raise ValueError('Conflicting inherited seal '+key)
            result[key]=h
    return result

def closed_parent():
    verify(PINS)
    m,r,e=read(PARENT+'_MANIFEST.json'),read(PARENT+'_RECEIPT.json'),read(PARENT+'_ERROR.json')
    if r['status']!='ERROR' or r['type']!='ValueError' or r['message']!='Exact common physical frame abscissae': raise ValueError('Original closed error identity')
    if r['owner']!='root' or r['pid']!=65046 or not r['closed'] or r['source_sha256']!=PINS['cross_u_full_flrw_source_constraint_v001.py']: raise ValueError('Original source/owner closure')
    if r['manifest_sha256']!=PINS[PARENT+'_MANIFEST.json'] or e!={k:v for k,v in r.items() if k not in ('closed','output_sha256')}|{'output_sha256':e['output_sha256']}: raise ValueError('Original ERROR/receipt metadata identity')
    if len(r['input_sha256'])!=41 or len(r['output_sha256'])!=1860 or m['input_sha256']!=r['input_sha256']: raise ValueError('Full original map census')
    if not set(e['output_sha256']).issubset(r['output_sha256']) or any(r['output_sha256'][n]!=h for n,h in e['output_sha256'].items()): raise ValueError('ERROR preserved output prefix')
    if any(m['physical_flags'].values()) or r['physical_flags']!=m['physical_flags']: raise ValueError('Original physical-false flags')
    if m['prospective_tolerances']!=dict(algebra=ROW_TOL,increment=INCREMENT_TOL,normal=NORMAL_TOL,state=STATE_TOL): raise ValueError('No threshold change')
    if m['ai']!=.01 or m['af']!=1. or m['amplitude']!=1e-8 or m['action']!='S_cross V003 Eq5/7-9': raise ValueError('Original fixture identity')
    trials=[dict(name=f'{arm}_K{ik}_O{io}',arm=arm,nstep=steps,ns=ns,na=na,k=k,omega=omega)
        for arm,steps,ns,na in [('TIME',2048,32,64),('FINE',4096,32,64),('MODES',4096,64,64),('ANGLE',4096,32,128)]
        for ik,k in enumerate((.01,.1)) for io,omega in enumerate((.1,1.,10.,100.))]
    if m['trials']!=trials or m['owner']!='root' or m['pid']!=65046: raise ValueError('All32 original trial identities')
    inputs=merge(PINS,r['input_sha256'],r['output_sha256']);verify(inputs)
    if (BASE/(PARENT+'_RESULT.json')).exists() or (BASE/(PARENT+'_REPORT.md')).exists(): raise ValueError('Original ERROR must remain unpromoted')
    if read('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json')['manifest']['fixed_parent']!=m['fixed']: raise ValueError('Actual fixed background identity')
    return m,r,e,inputs

def gate(name,error,tol):
    er=float(error)
    return dict(name=name,error=er,tolerance=tol,passed=math.isfinite(er) and er<=tol)

def validate_arrays(arrays,meta):
    t=meta['trial'];nf=len(meta['frames']);stages=0 if meta['nstep']==0 else 3
    expected=dict(core=(11,2),native=(t['ns']+16,2,2),angular=(t['na']+17,2),
      frame_core=(nf,11,2),frame_native=(nf,t['ns']+16,2,2),frame_angular=(nf,t['na']+17,2),
      last_stage_core=(stages,11,2),last_stage_native=(stages,t['ns']+16,2,2),last_stage_angular=(stages,t['na']+17,2))
    if set(arrays)!=set(expected): raise ValueError('Entire original array inventory')
    count=0
    for name,shape in expected.items():
        a=arrays[name]
        if a.shape!=shape or a.dtype!=np.dtype('complex128' if 'angular' in name else 'float64') or not np.all(np.isfinite(a)): raise ValueError('Accepted shape/dtype/finite '+name)
        count+=a.size
    for name in ('core','native','angular'):
        if meta['frames'][-1]['nstep']==meta['nstep'] and not np.array_equal(arrays[name],arrays['frame_'+name][-1]): raise ValueError('Original terminal/frame identity')
        if stages and not np.array_equal(arrays[name],arrays['last_stage_'+name][-1]): raise ValueError('Original stage/endpoint identity')
    return count

def audit_prefix(m,r,progress):
    events=[json.loads(line) for line in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    if len(events)!=930 or events[0]['event']!='OWNER_START' or events[-1]['event']!='OWNER_ERROR': raise ValueError('Entire closed journal census')
    for event in events:
        for key,value in dict(owner='root',pid=65046,source_sha256=m['source_sha256'],manifest_sha256=r['manifest_sha256']).items():
            if event[key]!=value: raise ValueError('Journal ownership '+key)
    if any(events[-1][key]!=r[key] for key in ('context','type','message')): raise ValueError('Exact closing error event')
    wanted=[(t,step) for t in m['trials'] for step in range(0,t['nstep']+1,128)]
    pairs=[];rows=[];terminal={};names=set();previous=None;entries=0
    for event,(trial,step) in zip(events[1:-1],wanted):
        CONTEXT.update(trial=trial['name'],nstep=step)
        name=f'{PARENT}_{trial["name"]}_CP_{step:06d}.npz';cn=Path(name).stem+'_COMMIT.json';names.update((name,cn))
        if event['event']!='CHECKPOINT' or event['trial']!=trial['name'] or event['nstep']!=step or event['failed'] is not False: raise ValueError('Exact ordered journal checkpoint')
        if r['output_sha256'].get(name)!=event['payload_sha256'] or r['output_sha256'].get(cn)!=event['commit_sha256']: raise ValueError('Journal/receipt pair binding')
        cp=read(cn);meta=cp['metadata'];text=encode(meta)
        expected=dict(schema=1,trial=trial['name'],nstep=step,failed=False,payload=name,payload_sha256=event['payload_sha256'],metadata=meta,owner='root',pid=65046,source_sha256=m['source_sha256'],manifest_sha256=r['manifest_sha256'])
        if cp!=expected: raise ValueError('Entire exact COMMIT')
        keys={'schema','trial','nstep','x','frames','maxima','input_sha256','layout','columns','physical_flags'}
        stride=trial['nstep']//32;frame_steps=list(range(0,step+1,stride))
        if set(meta)!=keys or meta['schema']!=1 or meta['trial']!=trial or meta['nstep']!=step or meta['input_sha256']!=r['input_sha256'] or meta['columns']!=['metric','common_velocity'] or meta['physical_flags']!=m['physical_flags']: raise ValueError('Entire exact accepted metadata')
        if meta['x']!=math.log(m['ai'])+step*((math.log(m['af'])-math.log(m['ai']))/trial['nstep']): raise ValueError('Original coordinate arithmetic identity')
        if [f['nstep'] for f in meta['frames']]!=frame_steps: raise ValueError('Exact rational sample index prefix')
        lay=meta['layout']
        if set(lay)!=set(('nodes','weights','mu','weight_sum')) or len(lay['nodes'])!=trial['ns']+16 or len(lay['weights'])!=trial['ns'] or len(lay['mu'])!=trial['na']+17: raise ValueError('Entire saved layout dimensions')
        if any(not 0<x<1 for x in lay['nodes']) or any(w<=0 for w in lay['weights']) or any(not -1<=u<=1 for u in lay['mu']): raise ValueError('Saved quadrature domain')
        if step and set(meta['maxima'])!=set(MAXIMA): raise ValueError('All16 original maxima')
        for n,d in meta['maxima'].items():
            if set(d)!=set(('error','nstep','a')) or not 1<=d['nstep']<=step or d['error']<0 or not math.isfinite(d['error']): raise ValueError('Exact first-attaining maximum descriptor '+n)
        with np.load(BASE/name,allow_pickle=False) as z:
            if set(z.files)!={'metadata','core','native','angular','frame_core','frame_native','frame_angular','last_stage_core','last_stage_native','last_stage_angular'} or str(z['metadata'])!=text.decode(): raise ValueError('Exact NPZ metadata/keys')
            arrays={n:z[n].copy() for n in z.files if n!='metadata'}
        entries+=validate_arrays(arrays,meta)
        if previous is not None and previous[0]['trial']['name']==trial['name']:
            pm,pa=previous;nf=len(pm['frames'])
            if meta['frames'][:nf]!=pm['frames'] or meta['layout']!=pm['layout']: raise ValueError('Entire immutable metadata/layout prefix')
            if any(not np.array_equal(arrays[n][:nf],pa[n]) for n in ('frame_core','frame_native','frame_angular')): raise ValueError('Entire immutable saved-state frame prefix')
            if any(meta['maxima'][n]['error']<d['error'] for n,d in pm['maxima'].items()): raise ValueError('Retained nondecreasing maxima')
        previous=(meta,{n:arrays[n] for n in ('frame_core','frame_native','frame_angular')})
        pairs.append(dict(trial=trial['name'],nstep=step,payload=name,payload_sha256=event['payload_sha256'],commit=cn,commit_sha256=event['commit_sha256'],array_entries=sum(a.size for a in arrays.values())))
        progress['audited_pairs']=len(pairs)
        if step==trial['nstep']:
            row=dict(trial=trial,frames=meta['frames'],maxima=meta['maxima'],terminal_checkpoint=name)
            rows.append(row);progress['rows'].append(row);terminal[trial['name']]={n:arrays[n] for n in ('frame_native','frame_angular')}
    actual={p.name for p in BASE.glob(PARENT+'_*_CP_*.npz')}|{p.name for p in BASE.glob(PARENT+'_*_CP_*_COMMIT.json')}
    if len(pairs)!=928 or actual!=names or len(rows)!=32 or sum(len(z['frames']) for z in rows)!=1056: raise ValueError('Exact entire pair/prefix/terminal census')
    rawname=PARENT+'_ERROR_RAW.npz'
    if {p.name for p in BASE.glob(PARENT+'_*.npz')}!=set(n for n in names if n.endswith('.npz'))|{rawname}: raise ValueError('No hidden orphan payload')
    with np.load(BASE/rawname,allow_pickle=False) as z:
        rawmeta=json.loads(str(z['metadata']))
        if set(z.files)!=set(rawmeta['arrays'])|{'metadata'} or rawmeta['context']!=r['context'] or rawmeta['type']!=r['type'] or rawmeta['message']!=r['message']: raise ValueError('Untouched ERROR_RAW identity')
        for n,d in rawmeta['arrays'].items():
            a=z[n]
            if list(a.shape)!=d['shape'] or str(a.dtype)!=d['dtype'] or bool(np.all(np.isfinite(a)))!=d['finite']: raise ValueError('Entire original RAW descriptor '+n)
    return rows,terminal,pairs,dict(pair_count=928,numeric_array_entries=entries,error_raw_metadata=rawmeta,journal_event_count=930)

def compare_rows(a,b,terminal,registration):
    checks=[]
    for j,(fa,fb) in enumerate(zip(a['frames'],b['frames'])):
        if fa['nstep']*32!=j*a['trial']['nstep'] or fb['nstep']*32!=j*b['trial']['nstep']: raise ValueError('Common exact j/32 registration')
        aa,ab=fa['a'],fb['a'];env=max(abs(aa),abs(ab));diff=abs(ab-aa)
        passed=math.isfinite(diff) and env>0 and diff<=SAMPLE_ALLOWANCE*env
        registration.append(dict(fine=a['trial']['name'],other=b['trial']['name'],numerator=j,denominator=32,fine_nstep=fa['nstep'],other_nstep=fb['nstep'],fine_a=aa,other_a=ab,signed_difference=ab-aa,relative_difference=diff/env,relative_allowance=SAMPLE_ALLOWANCE,passed=passed,scope='Recorded-coordinate numerical compatibility only'))
        if not passed: raise ValueError('Recorded sample-coordinate compatibility refused')
    for column in range(2):
        for n in range(20):
            v=np.asarray([r['readout'][n][column] for r in a['frames']]);w=np.asarray([r['readout'][n][column] for r in b['frames']]);scale=max(float(np.max(abs(v))),FLOOR)
            diff=abs(w-v)/scale;ix=int(np.argmax(diff));checks.append(dict(name='readout_'+str(n)+'_column_'+str(column),error=float(diff[ix]),signed_difference=float(w[ix]-v[ix]),normalization=scale,first_max_frame=ix,a=a['frames'][ix]['a'],tolerance=STATE_TOL,passed=bool(diff[ix]<=STATE_TOL)))
        for n in range(7):
            v=np.asarray([r['F'][n][column] for r in a['frames']]);w=np.asarray([r['F'][n][column] for r in b['frames']]);scale=max(float(np.max(abs(v))),FLOOR)
            diff=abs(w-v)/scale;ix=int(np.argmax(diff));checks.append(dict(name='angular_moment_'+str(n)+'_column_'+str(column),error=float(diff[ix]),signed_difference=float(w[ix]-v[ix]),normalization=scale,first_max_frame=ix,a=a['frames'][ix]['a'],tolerance=STATE_TOL,passed=bool(diff[ix]<=STATE_TOL)))
    for name,field,count,layoutkey in [('native_probe','native',16,'nodes'),('angular_probe','angular',17,'mu')]:
        av=terminal[a['trial']['name']]['frame_'+field][:,-count:];bv=terminal[b['trial']['name']]['frame_'+field][:,-count:]
        ca=read(Path(a['terminal_checkpoint']).stem+'_COMMIT.json')['metadata']['layout'][layoutkey][-count:]
        cb=read(Path(b['terminal_checkpoint']).stem+'_COMMIT.json')['metadata']['layout'][layoutkey][-count:]
        if ca!=cb: raise ValueError('Actual identical passive probe labels')
        scale=np.maximum(np.max(abs(av),axis=0),FLOOR);error=float(np.max(abs(bv-av)/scale))
        checks.append(dict(name=name,error=error,tolerance=STATE_TOL,passed=math.isfinite(error) and error<=STATE_TOL,scope='Fixed common passive frequencies/angles; complete feedback arrays retained separately'))
    if len(checks)!=56: raise ValueError('Original56 comparison census')
    return checks

def main():
    global np
    if AUTHOR_GUARD: raise RuntimeError('Unsealed author guard')
    tick=time.monotonic();m,r,e,inputs=closed_parent();inputs=merge(inputs,{str(Path(__file__).resolve()):sha(__file__)});verify(inputs)
    if list(BASE.glob(STEM+'_*')): raise FileExistsError('Unused aggregation namespace required; no resume')
    import numpy as np
    owner=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
    progress=dict(audited_pairs=0,rows=[],comparisons=[],registration_controls=[]);manifest=dict(schema=1,**owner,input_sha256=inputs,parent_receipt_sha256=PINS[PARENT+'_RECEIPT.json'],parent_status='ERROR',sample_registration='Exact rational j/32; preserved recorded a',relative_sample_allowance=SAMPLE_ALLOWANCE,original_thresholds=m['prospective_tolerances'],physical_flags=m['physical_flags'])
    try:
        write(STEM+'_MANIFEST.json',manifest)
        rows,terminal,pairs,audit=audit_prefix(m,r,progress)
        controls=[dict(name='zero_data_full_coupled_column',error=None,tolerance=0.,passed=None,disposition='not_serialized_in_parent_ERROR')]
        for row in rows:
            for n,data in row['maxima'].items():
                tol=NORMAL_TOL if n in ('normal_error','normal_propagation') else INCREMENT_TOL if n in INCREMENTS else ROW_TOL
                c=gate(row['trial']['name']+'_'+n,data['error'],tol)
                if n in WITHDRAWN: c['diagnostic_disposition']='invalid_original_diagnostic';c['qualification_withdrawn']=True
                controls.append(c)
            controls.append(gate(row['trial']['name']+'_preparation_normal',max(row['frames'][0]['normal_error']),ROW_TOL))
        comparisons=progress['comparisons'];registration=progress['registration_controls']
        for ik,k in enumerate((.01,.1)):
            for io,omega in enumerate((.1,1.,10.,100.)):
                get=lambda arm:next(z for z in rows if z['trial']['name']==f'{arm}_K{ik}_O{io}')
                for arm in ('TIME','MODES','ANGLE'):
                    CONTEXT.update(comparison=f'{arm}_K{ik}_O{io}')
                    checks=compare_rows(get('FINE'),get(arm),terminal,registration);comparisons.append(dict(k=k,omega=omega,arm=arm,controls=checks))
                    controls.extend(dict(c,name=f'K{ik}_O{io}_{arm}_'+c['name']) for c in checks)
        if len(controls)!=1889 or len(comparisons)!=24 or len(registration)!=792 or sum(c['passed'] is None for c in controls)!=1: raise ValueError('Entire original logical/new registration census')
        verify(inputs);closed_parent()
        status='RECOVERED_NUMERICAL_FAILED'
        result=dict(status=status,manifest=m,aggregation_manifest=manifest,rows=rows,comparisons=comparisons,controls=controls,sample_registration_controls=registration,checkpoint_pairs=pairs,authentication=audit,logical_predicate_count=1889,available_predicate_count=1888,unverified_predicate_count=1,invalid_original_diagnostic_count=64,original_error_copied_exactly=e,original_error_receipt_copied_exactly=r,background_parent_copied_exactly=read('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json'),physical_flags=m['physical_flags'],qualification={n:False for n in ('numerical_pass','instantaneous_trace','instantaneous_momentum','full_physical_state','observed_growth','observed_lensing','primordial_state')},elapsed_seconds=time.monotonic()-tick)
        report=('\n'.join(['# SAME S_cross saved aggregation V001','',status,'',f'{sum(c["passed"] is True for c in controls)}/1888 available original predicates pass; one original zero witness unavailable.',f'792 sample-registration checks;32 trials;928 original pairs;1056 untouched frames.','', 'Original instantaneous trace/momentum booleans and values are preserved; their qualification is withdrawn for the omitted+b*Phi diagnostic contact. Core/normal/increment/refinement failures are unchanged. The original ERROR remains protected. No scientific equation, operator, helper or trajectory was evaluated. All physical qualifications remain false.'])+'\n').encode()
        rh=write(STEM+'_RESULT.json',result);write(STEM+'_REPORT.md',report)
        verify(inputs);closed_parent()
        receipt=dict(status=status,**owner,closed=now(),elapsed_seconds=time.monotonic()-tick,result_sha256=rh,input_sha256=inputs,output_sha256=dict(OUTPUTS),parent_status='ERROR',parent_pid=65046,parent_closed=r['closed'],checkpoint_pairs=928,trial_count=32,logical_predicate_count=1889,available_predicate_count=1888,unverified_predicate_count=1,registration_predicate_count=792)
        write(STEM+'_RECEIPT.json',receipt)
        if read(STEM+'_RECEIPT.json')!=receipt or read(STEM+'_RESULT.json')!=result or read(STEM+'_MANIFEST.json')!=manifest: raise ValueError('Entire exact publication reread')
        verify(inputs);verify(OUTPUTS);closed_parent();print(status,rh,flush=True);return 3
    except Exception as exc:
        error=dict(status='ERROR',**owner,closed=now(),context=dict(CONTEXT),type=type(exc).__name__,message=str(exc),input_sha256=inputs,output_sha256=dict(OUTPUTS),partial=progress,physical_flags=m['physical_flags'])
        existing=BASE/(STEM+'_RECEIPT.json')
        if existing.exists(): error['protected_existing_receipt_sha256']=sha(existing)
        write(STEM+'_ERROR.json',error)
        if not existing.exists(): write(STEM+'_RECEIPT.json',dict(error,output_sha256=dict(OUTPUTS)))
        verify(inputs);verify(OUTPUTS);closed_parent();raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args()
    if not args.root_owned: raise RuntimeError('Root-owned saved arithmetic only')
    raise SystemExit(main())
