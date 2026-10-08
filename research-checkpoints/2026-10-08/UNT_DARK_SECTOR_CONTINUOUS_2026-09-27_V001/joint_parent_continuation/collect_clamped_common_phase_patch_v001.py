"""Inert saved-data collection only; no producer/material import or solve."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/'CLAMPED_COMMON_PHASE_PATCH_COLLECTION_V001_FROZEN.json'
PRODUCER_FREEZE=HERE/'CLAMPED_COMMON_PHASE_PATCH_V001_FROZEN.json'
CASES=[(R,L,n) for R in [128,8192] for L in [1.,2.] for n in [16,32]]
CONFIG=dict(case_labels=[list(c) for c in CASES],seed_multipliers=[1.,2.],grid_pairs=8,clamp_pairs=8,seed_pairs=8,
    interpolation='Bilinear in saved physical x,z coordinates; no extrapolation. Geometry-only common centre coverage.',
    comparison_gate='None. Differences are descriptive. Convergence/Jacobian/control qualifications remain separate.')

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def snapshot():
    files={};seen=set()
    def add(p,expected=None):
        p=p.resolve(strict=True);p.relative_to(ROOT);digest=sha(p)
        if expected is not None and digest!=expected:raise RuntimeError('Changed frozen input '+str(p))
        files[str(p.relative_to(ROOT))]=digest;return p
    def manifest(p):
        p=add(p)
        if p in seen:return
        seen.add(p)
        for name,digest in json.loads(p.read_text())['files'].items():
            path=Path(name);options=[path] if path.is_absolute() else [ROOT/path,p.parent/path]
            candidates={q.resolve() for q in options if q.resolve().is_relative_to(ROOT) and q.is_file()}
            if len(candidates)!=1:raise RuntimeError('Ambiguous or missing ancestor '+name)
            q=add(candidates.pop(),digest)
            if q.name.endswith('_FROZEN.json'):manifest(q)
    manifest(PRODUCER_FREEZE)
    add(Path(__file__));add(HERE/'CLAMPED_COMMON_PHASE_PATCH_COLLECTION_PROTOCOL_V001.md')
    return dict(configuration=CONFIG,producer_freeze_sha256=sha(PRODUCER_FREEZE),files=files)

def read_case(path,index):
    path=path.resolve();path.relative_to(ROOT)
    if not path.is_file():return None,dict(case_index=index,status='MISSING',path=str(path))
    t=json.loads(path.read_text())
    if t.get('encoding')!='zlib_base64_canonical_json':raise RuntimeError('Unexpected case transport '+str(path))
    decoder=zlib.decompressobj()
    raw=decoder.decompress(base64.b64decode(t['data'],validate=True))+decoder.flush()
    if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:raise RuntimeError('Invalid compressed case')
    if len(raw)!=t['raw_bytes'] or hashlib.sha256(raw).hexdigest()!=t['raw_sha256']:raise RuntimeError('Changed raw case')
    v=json.loads(raw);p=v['payload']
    if v['freeze_sha256']!=sha(PRODUCER_FREEZE) or v['payload_sha256']!=hashlib.sha256(encode(p)).hexdigest():raise RuntimeError('Case wrapper differs')
    R,L,n=CASES[index]
    if p['case_index']!=index or (p['R'],p['L'],p['n'])!=(R,L,n):raise RuntimeError('Case identity differs')
    if p['configuration']!=json.loads(PRODUCER_FREEZE.read_text())['configuration']:raise RuntimeError('Case configuration differs')
    seeds=[o['seed_multiplier'] for o in p['outcomes']]
    if p['status']=='FAILED_PREREQUISITES':
        if seeds or p.get('unstarted_seeds')!=[1.,2.]:raise RuntimeError('Prerequisite failure hides seed status')
    elif seeds!=[1.,2.]:raise RuntimeError('Seed census differs')
    if len(p['centres'])!=n or len(p['edges'])!=n+1:raise RuntimeError('Mesh census differs')
    for outcome in p['outcomes']:
        if np.asarray(outcome['u']).shape!=(n,n):raise RuntimeError('Saved field shape differs')
    return p,dict(case_index=index,status='AUTHENTICATED',path=str(path),transport_sha256=sha(path),
        raw_sha256=t['raw_sha256'],payload_sha256=v['payload_sha256'],bytes=t['raw_bytes'])

def metric(a,b,weights):
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float);w=np.asarray(weights,dtype=float)
    if not (a.shape==b.shape==w.shape) or not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):raise RuntimeError('Invalid comparison array')
    d=b-a;total=float(np.sum(w));rms=lambda x:math.sqrt(float(np.sum(w*x*x))/total)
    ar,br,dr=rms(a),rms(b),rms(d);den=(ar+br)/2
    return dict(weighted_RMS_difference=dr,symmetric_relative_RMS=dr/den if den else 0.,
        max_absolute_difference=float(np.max(np.abs(d))),signed_range=[float(np.min(d)),float(np.max(d))],
        first_weighted_RMS=ar,second_weighted_RMS=br,
        first_range=[float(np.min(a)),float(np.max(a))],second_range=[float(np.min(b)),float(np.max(b))])

def interpolate(centres,values,targets):
    # Each target lies within the existing centre rectangle; never extrapolate.
    c=np.asarray(centres);q=np.asarray(targets);v=np.asarray(values,dtype=float)
    if q[0]<c[0] or q[-1]>c[-1]:raise RuntimeError('Interpolation would extrapolate')
    along_z=np.array([np.interp(q,c,row) for row in v])
    return np.array([np.interp(q,c,along_z[:,j]) for j in range(len(q))]).T

def outcome(case,seed):
    if case is None:return None
    return next((o for o in case['outcomes'] if o['seed_multiplier']==seed),None)

def fields(case,o):
    values={'u':o['u'],'Phi':np.asarray(o['u'])*case['epsilon_scale']}
    if 'gradients' in o:
        for axis in ['radial','vertical']:
            values[axis+'_G']=o['gradients'][axis]
            values[axis+'_m_s2']=np.asarray(o['gradients'][axis])*case['source_row']['gstar']
    if 'material' in o:
        for key in ['I','I_over_Ib','deltaT_hard','deltaT_soft','deltaT','hard_E','hard_Pi']:
            values[key]=o['material'][key]
    return values

def pair(kind,cases,i,j,seed_i,seed_j):
    first,second=cases[i],cases[j]
    record=dict(kind=kind,first_case=i,second_case=j,first_seed=seed_i,second_seed=seed_j)
    if first is None or second is None:return dict(**record,status='MISSING_CASE')
    a,b=outcome(first,seed_i),outcome(second,seed_j)
    if a is None or b is None:return dict(**record,status='UNSTARTED_PREREQUISITE_FAILURE')
    record.update(first_solver_status=a['status'],second_solver_status=b['status'],
        both_converged=a['status']=='CONVERGED' and b['status']=='CONVERGED',
        both_jacobians_qualified=bool(a.get('jacobian_qualified',False) and b.get('jacobian_qualified',False)),
        both_case_controls_pass=not first['failures'] and not second['failures'])
    ca=np.asarray(first['centres']);cb=np.asarray(second['centres'])
    take=np.flatnonzero((ca>=max(ca[0],cb[0]))&(ca<=min(ca[-1],cb[-1])))
    if len(take)<2:return dict(**record,status='INSUFFICIENT_GEOMETRIC_COVERAGE')
    target=ca[take];edges=np.asarray(first['edges'])
    widths=np.diff(edges)[take];areas=(np.diff(edges**2)/2)[take]
    weight=areas[:,None]*widths[None,:]
    fa,fb=fields(first,a),fields(second,b);results={}
    for name in sorted(set(fa)&set(fb)):
        av=np.asarray(fa[name],dtype=float)[np.ix_(take,take)]
        bv=interpolate(cb,fb[name],target)
        results[name]=metric(av,bv,weight)
    return dict(**record,status='COMPARED_SAVED_STATES',first_grid_retained_indices=take.tolist(),
        target_centres=target.tolist(),compared_points=len(take)**2,excluded_first_grid_points=len(ca)**2-len(take)**2,
        missing_field_names=sorted(set(fa)^set(fb)),metrics=results,
        interpretation='Difference is second minus first. Bilinear centre interpolation is descriptive, not a conservative re-solve or a new flux qualification.')

def collect(paths):
    cases=[];custody=[]
    for i,path in enumerate(paths):
        p,receipt=read_case(path,i);cases.append(p);custody.append(receipt)
    comparisons=[]
    for i in [0,2,4,6]:
        for seed in [1.,2.]:comparisons.append(pair('grid_N16_to_N32',cases,i,i+1,seed,seed))
    for i in [0,1,4,5]:
        for seed in [1.,2.]:comparisons.append(pair('clamp_L1_to_L2',cases,i,i+2,seed,seed))
    for i in range(8):comparisons.append(pair('seed1_to_seed2',cases,i,i,1.,2.))
    summary=[]
    for i,p in enumerate(cases):
        if p is None:summary.append(dict(case_index=i,status='MISSING'));continue
        seeds=[]
        for o in p['outcomes']:
            s=dict(seed=o['seed_multiplier'],solver_status=o['status'],iterations=len(o['history']),
                jacobian_qualified=o.get('jacobian_qualified',False),residual=o.get('residual'),
                sheet_normal_status=o.get('sheet_normal',{}).get('status'),flux_balance=o.get('flux_balance'))
            if 'local_lengths' in o:
                for axis in ['transverse','longitudinal']:
                    raw=o['local_lengths'][axis+'_width_over_length']
                    flat=[x for row in raw for x in row if x is not None]
                    s[axis+'_width_over_length_range']=[min(flat),max(flat)] if flat else None
                    s[axis+'_invalid_local_lengths']=p['n']**2-len(flat)
            seeds.append(s)
        summary.append(dict(case_index=i,R=p['R'],L=p['L'],N=p['n'],status=p['status'],
            failures=p['failures'],unstarted_seeds=p.get('unstarted_seeds',[]),outcomes=seeds,
            seconds=p['seconds'],peak_self_rss_bytes=p['peak_self_rss_bytes']))
    complete=all(p is not None for p in cases)
    controls_pass=complete and all(not p['failures'] for p in cases)
    all_converged=complete and all(len(p['outcomes'])==2 and all(o['status']=='CONVERGED' for o in p['outcomes']) for p in cases)
    all_jac=complete and all(len(p['outcomes'])==2 and all(o.get('jacobian_qualified',False) for o in p['outcomes']) for p in cases)
    return dict(status='COMPLETE_SAVED_COMPARISON' if complete else 'PARTIAL_CENSUS',
        configuration=CONFIG,census_complete=complete,present_cases=sum(p is not None for p in cases),
        missing_cases=[i for i,p in enumerate(cases) if p is None],all_case_controls_pass=controls_pass,
        all_16_seeds_converged=all_converged,all_16_jacobians_qualified=all_jac,
        numerical_resolution_certified=False,cases=summary,custody=custody,comparisons=comparisons,
        scope='All failures and missing cases retained. No numerical-resolution, unique-branch, full-metric, physical-clamp, halo or observational-success gate is inferred from collection. Grid/clamp differences are descriptive, with geometry-only interpolation masks.')

def main():
    snap=snapshot()
    if sys.argv[1:]==['freeze']:print(encode(snap).decode());return
    if len(sys.argv)<2 or sys.argv[1]!='run':raise RuntimeError('Use freeze or run [eight ordered case paths]')
    if json.loads(FREEZE.read_text())!=snap:raise RuntimeError('Collector freeze differs')
    args=sys.argv[2:]
    if args and len(args)!=8:raise RuntimeError('Supply exactly eight ordered paths, or use the default census')
    paths=[Path(x) for x in args] if args else [HERE/f'CLAMPED_COMMON_PHASE_PATCH_V001_CASE_{i:03d}.json' for i in range(8)]
    p=collect(paths)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())

if __name__=='__main__':main()
