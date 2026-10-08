"""Additive saved-projector source-strength refinement; no eigensolver."""
import os
import sys
sys.dont_write_bytecode=True
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.resolve()
FREEZE=HERE/'NATIVE_INTERACTING_PROJECTOR_REFINEMENT_V001_FROZEN.json'
INPUT='NATIVE_INTERACTING_SPECTRUM_V001_RESULTS.json'
OLD_FREEZE='NATIVE_INTERACTING_SPECTRUM_V001_FROZEN.json'
PINS={INPUT:'93b9130e3e6d8684865d4852fafa810cc92cf60ae429dde09fd55c44889d4049',
      OLD_FREEZE:'9f254af41d1523b23168f2d29153e86c4b35aad1c01d6ffa9ad4fcef432e8816'}
CONFIG=dict(operator_tolerance=1e-11,spectral_tolerance=1e-10,
            old_derivative_difference_report_threshold=1e-10,
            cases=8,spaces_per_case=3,no_regrouping=True,no_eigensolver=True)


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(path):
    path.resolve().relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unpack(v,n):
    if len(v)!=n*(n+1)//2:raise ValueError('Wrong symmetric matrix length')
    out=np.zeros((n,n));out[np.triu_indices(n)]=v
    return out+out.T-np.diag(out.diagonal())


def authenticate():
    files={}
    def add(path,expected=None):
        value=sha(path)
        if expected is not None and value!=expected:raise ValueError('Hash differs: '+str(path))
        files[str(path.resolve().relative_to(ROOT))]=value
    for name,digest in PINS.items():add(HERE/name,digest)
    old=json.loads((HERE/OLD_FREEZE).read_text())
    for name,digest in old['files'].items():add(ROOT/name,digest)
    wrapper=json.loads((HERE/INPUT).read_text());p=wrapper['payload']
    if wrapper['freeze_sha256']!=sha(HERE/OLD_FREEZE):raise ValueError('Old freeze link differs')
    if wrapper['payload_sha256']!=hashlib.sha256(encode(p)).hexdigest():raise ValueError('Old payload differs')
    if p['status']!='COMPLETE' or p['failures']:raise ValueError('Unexpected producer qualification')
    census={(r['record_occupancy'],r['flip_strength']) for r in p['cases']}
    if len(p['cases'])!=8 or census!={(q,h) for q in (0,1) for h in (.5,.025,.0125,.00625)}:
        raise ValueError('Case census differs')
    for name in (Path(__file__).name,'NATIVE_INTERACTING_PROJECTOR_REFINEMENT_PROTOCOL_V001.md',
                 'NATIVE_INTERACTING_SPECTRUM_AUDIT_FINDING_V001.md'):
        add(HERE/name)
    return p,dict(configuration=CONFIG,files=files)


def run():
    start=time.perf_counter();p,snapshot=authenticate()
    if encode(json.loads(FREEZE.read_text()))!=encode(snapshot):raise ValueError('Refinement freeze differs')
    counts,maxima,failures={},{},[]
    def check(name,a,b=0.,tol=None):
        difference=np.asarray(a)-np.asarray(b)
        err=float(np.max(np.abs(difference)))
        limit=CONFIG['operator_tolerance'] if tol is None else tol
        counts[name]=counts.get(name,0)+difference.size;maxima[name]=max(maxima.get(name,0.),err)
        if not math.isfinite(err) or err>limit:failures.append(dict(check=name,error=err,tolerance=limit))
    V=np.asarray(p['basis']['V']);W=np.asarray(p['basis']['W'])
    M0=np.diag([bin(i).count('1') for i in range(16)]);X0=np.zeros((16,16))
    for i in range(16):
        for bit in range(4):X0[i,i^(1<<bit)]=1.
    rows=[];differences=[]
    for case in p['cases']:
        q,h=case['record_occupancy'],case['flip_strength'];spaces={}
        for label,basis in (('full',np.eye(16)),('bright',V),('dark',W)):
            saved=case[label];n=saved['dimension'];H=unpack(case[label+'_H_upper'],n)
            M=basis.T@M0@basis;X=basis.T@X0@basis
            groups=saved['clusters'];es=[g['energy'] for g in groups]
            Ps=[unpack(g['projector_upper'],n) for g in groups];ng=len(Ps)
            strength=np.zeros((ng,ng));old=np.asarray(saved['source_strengths'])
            for a,Pa in enumerate(Ps):
                for b,Pb in enumerate(Ps):
                    block=Pa@M@Pb
                    strength[a,b]=math.fsum(float(v)*float(v) for v in block.flat)
                    # Transposed multiplication and summation order: no eigensolver.
                    reverse=Pb@M@Pa
                    check('positive_strength_transpose',strength[a,b],np.sum(reverse*reverse))
                    if strength[a,b]<0:raise AssertionError('Norm square is negative')
            check('old_strength_absolute_consistency',strength,old,tol=CONFIG['spectral_tolerance'])
            check('projector_resolution',sum(Ps),np.eye(n))
            check('matrix_from_saved_spectrum',sum(e*P for e,P in zip(es,Ps)),H,tol=CONFIG['spectral_tolerance'])
            outgroups=[]
            for a,(g,Pa) in enumerate(zip(groups,Ps)):
                check('projector_idempotency',Pa@Pa,Pa)
                check('projector_rank',np.trace(Pa),g['rank'])
                residual=H@Pa-es[a]*Pa
                check('saved_projector_eigen_equation',residual,tol=CONFIG['spectral_tolerance'])
                for b,Pb in enumerate(Ps):check('projector_orthogonality',Pa@Pb,Pa if a==b else 0.)
                gaps=[es[a]-e for b,e in enumerate(es) if b!=a]
                if not all(abs(v)>0 for v in gaps):raise ValueError('Unchanged grouping has equal centroids')
                terms=[2*strength[a,b]/(es[a]-e) for b,e in enumerate(es) if b!=a]
                curvature=math.fsum(terms)
                oldreconstructed=math.fsum(2*old[a,b]/(es[a]-e) for b,e in enumerate(es) if b!=a)
                oldcurv=g['source_energy_second_derivative_trace']
                check('old_derivative_algebra',oldreconstructed,oldcurv,tol=CONFIG['spectral_tolerance'])
                moment=float(h*np.trace(Pa@X))
                newmoment=2*math.fsum((e-es[a])*strength[a,b] for b,e in enumerate(es))
                check('signed_sum_rule',newmoment,moment,tol=CONFIG['spectral_tolerance'])
                check('source_strength_closure',math.fsum(strength[a]),np.trace(Pa@M@M),tol=CONFIG['spectral_tolerance'])
                check('saved_moment_identity',moment,g['moment_trace'],tol=CONFIG['spectral_tolerance'])
                minsep=min(abs(v) for v in gaps);resnorm=math.sqrt(math.fsum(float(v)*float(v) for v in residual.flat))
                sensitivity=2*math.fsum(abs(strength[a,b]-old[a,b])/abs(es[a]-e) for b,e in enumerate(es) if b!=a)
                difference=curvature-oldcurv
                out=dict(g,source_energy_second_derivative_trace_old=oldcurv,
                    source_energy_second_derivative_trace_positive=curvature,
                    source_energy_second_derivative_signed_difference=difference,
                    absolute_terms_sum=math.fsum(abs(v) for v in terms),
                    signed_sumrule_positive=newmoment,
                    impulse_work_second_derivative_positive=newmoment/g['rank'],
                    minimum_other_centroid_gap=minsep,all_other_signed_centroid_gaps=gaps,
                    projector_eigen_residual_frobenius=resnorm,
                    projector_eigen_residual_over_minimum_gap=resnorm/minsep,
                    cluster_spread_over_minimum_gap=g['spread']/minsep,
                    raw_to_positive_strength_derivative_sensitivity=sensitivity,
                    exceeds_original_absolute_derivative_tolerance=bool(abs(difference)>CONFIG['old_derivative_difference_report_threshold']),
                    precision_scope='Stable strength arithmetic on unchanged saved projectors; no rigorous derivative error or relative-precision certificate.')
                outgroups.append(out)
                differences.append(dict(q=q,h=h,space=label,cluster=a,rank=g['rank'],old=oldcurv,new=curvature,
                    difference=difference,minimum_gap=minsep,residual_over_gap=resnorm/minsep,
                    exceeds_original_absolute_derivative_tolerance=out['exceeds_original_absolute_derivative_tolerance']))
            spaces[label]=dict(dimension=n,eigenvalues=saved['eigenvalues'],H_upper=case[label+'_H_upper'],
                source_strengths_old=saved['source_strengths'],source_strengths_positive=strength.tolist(),clusters=outgroups)
        rows.append(dict(record_occupancy=q,flip_strength=h,role=case['role'],spaces=spaces,
            unchanged_collective_readout=case['collective_readout'],unchanged_ground_diagnostic=case['ground_diagnostic']))
    check('case_census',len(rows),8,tol=0.)
    check('space_census',sum(len(r['spaces']) for r in rows),24,tol=0.)
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    payload=dict(status='COMPLETE' if not failures else 'FAILED_CHECKS',configuration=CONFIG,
        source_result_sha256=sha(HERE/INPUT),source_payload_sha256=hashlib.sha256(encode(p)).hexdigest(),
        basis=p['basis'],cases=rows,derivative_differences=differences,
        discrepancy_count=sum(v['exceeds_original_absolute_derivative_tolerance'] for v in differences),
        maximum_derivative_change=max(abs(v['difference']) for v in differences),
        check_counts=counts,maximum_errors=maxima,failures=failures,
        scope='Additive stable transition strengths from unchanged saved projectors; no new spectrum, grouping, state, source or relative precision guarantee for near-degenerate excited derivatives.',
        seconds=time.perf_counter()-start,peak_self_rss_bytes=int(peak))
    return dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)


if __name__=='__main__':
    if sys.argv[1:]==['freeze']:out=authenticate()[1]
    elif sys.argv[1:]==['run']:out=run()
    else:raise ValueError('Use freeze or run; stdout only')
    print(encode(out).decode())
    if 'payload' in out and out['payload']['status']!='COMPLETE':sys.exit(2)
