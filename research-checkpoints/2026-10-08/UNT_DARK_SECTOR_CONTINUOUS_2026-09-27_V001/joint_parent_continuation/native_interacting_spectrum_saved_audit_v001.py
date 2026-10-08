"""Saved-matrix/projector recombination only; no eigensolver or evolution."""
import os
import sys
sys.dont_write_bytecode=True
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
import hashlib
import json
import math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def unpack(values,n):
    assert len(values)==n*(n+1)//2
    out=np.zeros((n,n));out[np.triu_indices(n)]=values
    return out+out.T-np.diag(np.diag(out))


def run():
    file=HERE/'NATIVE_INTERACTING_SPECTRUM_V001_RESULTS.json'
    freeze=HERE/'NATIVE_INTERACTING_SPECTRUM_V001_FROZEN.json'
    assert sha(file)=='93b9130e3e6d8684865d4852fafa810cc92cf60ae429dde09fd55c44889d4049'
    assert sha(freeze)=='9f254af41d1523b23168f2d29153e86c4b35aad1c01d6ffa9ad4fcef432e8816'
    outer=json.loads(file.read_text());p=outer['payload'];f=json.loads(freeze.read_text())
    assert p['status']=='COMPLETE' and not p['failures']
    assert outer['freeze_sha256']==sha(freeze)
    assert outer['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    for name,digest in f['files'].items():
        path=ROOT/name;path.resolve().relative_to(ROOT.resolve());assert sha(path)==digest,name
    assert sum(p['check_counts'].values())==87644
    assert len(p['cases'])==8 and {(r['record_occupancy'],r['flip_strength']) for r in p['cases']}=={(q,h) for q in (0,1) for h in (.5,.025,.0125,.00625)}
    count=0;maxima={}

    def check(name,a,b=0.,tol=1e-10):
        nonlocal count
        diff=np.asarray(a)-np.asarray(b);error=float(np.max(np.abs(diff)))
        assert np.isfinite(error) and error<=tol,(name,error)
        maxima[name]=max(maxima.get(name,0.),error);count+=diff.size

    V=np.asarray(p['basis']['V']);W=np.asarray(p['basis']['W']);PB=V@V.T
    masks=((0,),(1,2,4,8),(6,9),(3,5,10,12),(7,11,13,14),(15,))
    VI=np.zeros((16,6))
    for col,group in enumerate(masks):VI[list(group),col]=1/math.sqrt(len(group))
    check('owned_orbit_basis',V,VI)
    check('isometry_V',V.T@V,np.eye(6));check('isometry_W',W.T@W,np.eye(10))
    check('orthogonal',V.T@W);check('complete_basis',PB+W@W.T,np.eye(16))
    bits=np.array([[(i>>j)&1 for j in range(4)] for i in range(16)])
    M=np.diag(bits.sum(axis=1));X=np.zeros((16,16))
    for i in range(16):
        for j in range(4):X[i,i^(1<<j)]=1
    summaries=[];curvature_differences=[]
    for r in p['cases']:
        q,h=r['record_occupancy'],r['flip_strength'];k=2-q;C=4+4*q
        degrees=np.stack([bits[:,0]+bits[:,1],bits[:,2]+bits[:,3],bits[:,0]+bits[:,2],bits[:,1]+bits[:,3]],axis=1)
        diagonal=4*np.diag(M)+((degrees-1)**2).sum(axis=1)+4*q-q*np.diag(M)
        H=np.diag(diagonal)-h*X
        check('native_matrix',unpack(r['full_H_upper'],16),H)
        check('source_double_commutator',M@(H@M-M@H)-(H@M-M@H)@M,h*X)
        check('absolute_blank_energy',r['blank_link_state']['mean_energy'],C)
        check('absolute_blank_variance',r['blank_link_state']['energy_variance'],float(np.dot(H[0,1:],H[1:,0])))
        check('bright_matrix',unpack(r['bright_H_upper'],6),V.T@H@V)
        check('dark_matrix',unpack(r['dark_H_upper'],10),W.T@H@W)
        check('dark_source',unpack(r['dark_M_upper'],10),W.T@M@W)
        check('H_leakage',V.T@H@W);check('M_leakage',V.T@M@W)
        assert r['constants']==dict(U=1.,absolute=float(C),kappa=float(k))
        assert r['role']==('inherited_main' if h==.5 else 'changed_flip_asymptotic_control')
        projectors={}
        for label,basis in (('full',np.eye(16)),('bright',V),('dark',W)):
            data=r[label];n=basis.shape[1];Hb=basis.T@H@basis;Mb=basis.T@M@basis;Xb=basis.T@X@basis
            assert data['dimension']==n and len(data['eigenvalues'])==n
            groups=data['clusters'];Ps=[unpack(g['projector_upper'],n) for g in groups]
            es=[g['energy'] for g in groups]
            check('projector_completeness',sum(Ps),np.eye(n))
            check('spectral_H_reconstruction',sum(e*P for e,P in zip(es,Ps)),Hb)
            cursor=0
            strengths=np.zeros((len(Ps),len(Ps)))
            for a,(ga,Pa) in enumerate(zip(groups,Ps)):
                rank=ga['rank'];assert rank>=1
                listed=data['eigenvalues'][cursor:cursor+rank];cursor+=rank
                check('cluster_mean',ga['energy'],math.fsum(listed)/rank)
                check('cluster_spread',ga['spread'],max(listed)-min(listed))
                assert ga['spread']<=1e-10
                check('projector_idempotency',Pa@Pa,Pa);check('projector_rank',np.trace(Pa),rank)
                check('projector_eigen_equation',Hb@Pa,es[a]*Pa)
                for b,Pb in enumerate(Ps):
                    check('projector_orthogonality',Pa@Pb,Pa if a==b else 0.)
                    # Equivalent positive strength avoids cancellation at forbidden lines.
                    strengths[a,b]=np.sum((Pa@Mb@Pb)**2)
                check('source_trace',ga['source_expectation_trace'],np.trace(Pa@Mb))
                moment=float(h*np.trace(Pa@Xb));signed=2*sum((eb-es[a])*strengths[a,b] for b,eb in enumerate(es))
                curvature=2*sum(strengths[a,b]/(es[a]-eb) for b,eb in enumerate(es) if b!=a)
                saved_curvature=2*sum(data['source_strengths'][a][b]/(es[a]-eb) for b,eb in enumerate(es) if b!=a)
                check('moment_trace',ga['moment_trace'],moment)
                check('independent_signed_sumrule',signed,moment)
                check('saved_sumrule',ga['sumrule_trace'],signed)
                check('saved_curvature_arithmetic',ga['source_energy_second_derivative_trace'],saved_curvature)
                curvature_differences.append(dict(q=q,h=h,space=label,cluster=a,rank=rank,
                    saved=ga['source_energy_second_derivative_trace'],positive_strength_reconstruction=curvature,
                    difference=curvature-ga['source_energy_second_derivative_trace'],
                    minimum_other_gap=min(abs(es[a]-eb) for b,eb in enumerate(es) if b!=a),
                    exceeds_original_absolute_spectral_tolerance=bool(abs(curvature-ga['source_energy_second_derivative_trace'])>1e-10)))
                check('impulse_work_curvature',ga['source_impulse_energy_second_derivative_per_equal_mixture'],moment/rank)
                if label=='full':
                    br=float(np.trace(Pa@PB));check('bright_cluster_rank',br,ga['bright_rank'])
                    check('dark_cluster_rank',rank-br,ga['dark_rank'])
            assert cursor==n
            check('source_strengths',data['source_strengths'],strengths)
            projectors[label]=(Ps,strengths)
        check('full_union_spectrum',r['full']['eigenvalues'],sorted(r['bright']['eigenvalues']+r['dark']['eigenvalues']))
        P0=projectors['full'][0][0];es=r['full']['eigenvalues'];ground=r['ground_diagnostic']
        check('ground_bright',np.trace(P0@PB),1.)
        mean=float(np.trace(P0@M));chi=-r['full']['clusters'][0]['source_energy_second_derivative_trace']
        for name,value in dict(mean_incidence=mean,passive_susceptibility=chi,bordered_solve_susceptibility=chi,
                               energy_first_source_derivative=-mean,energy_second_source_derivative=-chi).items():
            check('ground_'+name,ground[name],value)
        eb=np.asarray(r['bright']['eigenvalues']);S=projectors['bright'][1];out=r['collective_readout']
        curv=eb[2]-2*eb[1]+eb[0];coef=-8*(k+6)/(k*(k+2)*(k+4))
        shifts=np.array([-4/k,2/k-4/(k+2),2/k-2/(k+4)])
        check('curvature',out['first_three_ordered_bright_curvature'],curv)
        check('scaled_curvature',out['curvature_divided_h_squared'],curv/h**2)
        check('curvature_coefficient',out['weak_flip_curvature_coefficient'],coef)
        check('energy_coefficients',out['weak_flip_energy_coefficients'],shifts)
        check('energy_shifts',out['observed_energy_shifts_divided_h_squared'],(eb[:3]-C-np.array([0,k,2*k]))/h**2)
        check('source01',out['source_01_squared'],S[0,1])
        check('source_ladder',out['source_from_level1_strength_ratios'],S[1]/S[0,1])
        check('source_asymptotic_entries',out['observed_abs_source_entries_divided_h'],np.sqrt([S[0,1],S[1,2],S[1,3]])/h)
        check('source_weak_coefficients',out['weak_flip_abs_source_coefficients'],[2/k,math.sqrt(2)/k,2/(k+2)])
        rad=min(k,2)/16
        if h<rad:
            bound=16*rad*(h/rad)**4/(1-(h/rad)**2)
            check('Cauchy_bound',out['curvature_remainder_bound'],bound)
            assert abs(curv-coef*h*h)<=bound+1e-10
            assert np.max(abs(eb[:3]-C-np.array([0,k,2*k])-shifts*h*h))<=bound/4+1e-10
        else:assert out['curvature_remainder_bound'] is None
        summaries.append(dict(q=q,h=h,role=r['role'],full_cluster_count=len(r['full']['clusters']),
            curvature=curv,curvature_over_h2=curv/h**2,source_opposite_ratio=S[1,2]/S[0,1],
            source_adjacent_ratio=S[1,3]/S[0,1],ground_mean=mean,ground_susceptibility=chi,
            bright_energies=eb.tolist(),full_energies=es,
            source_impulse_curvature_range=[min(g['source_impulse_energy_second_derivative_per_equal_mixture'] for g in r['full']['clusters']),max(g['source_impulse_energy_second_derivative_per_equal_mixture'] for g in r['full']['clusters'])]))
    failedfreeze=HERE/'NATIVE_INTERACTING_SPECTRUM_V001_ATTEMPT_001_FROZEN.json'
    failure=HERE/'NATIVE_INTERACTING_SPECTRUM_V001_ATTEMPT_001_FAILURE.json'
    assert json.loads(failedfreeze.read_text())==f
    assert sha(failedfreeze)!=sha(freeze)
    return dict(status='MAIN_AND_MATRIX_CHECKS_ACCEPTED_SECONDARY_DERIVATIVE_REPAIR_NEEDED',script_sha256=sha(Path(__file__)),result_sha256=sha(file),
        freeze_sha256=sha(freeze),payload_sha256=outer['payload_sha256'],frozen_members=len(f['files']),
        producer_checks=sum(p['check_counts'].values()),independent_scalar_comparisons=count,
        maximum_absolute_errors=maxima,cases=summaries,
        energy_source_curvature_differences=curvature_differences,
        secondary_derivative_discrepancy_count=sum(d['exceeds_original_absolute_spectral_tolerance'] for d in curvature_differences),
        maximum_secondary_derivative_discrepancy=max(abs(d['difference']) for d in curvature_differences),
        producer_seconds=p['seconds'],
        producer_peak_self_RSS_bytes=p['peak_self_rss_platform_units'],
        preserved_failed_freeze_sha256=sha(failedfreeze),preserved_failure_sha256=sha(failure),
        limits=['No eigensolver, linear solve, propagation or fit rerun.',
                'Every saved projector checked against independently rebuilt owned matrices and source.',
                'Negative spacing curvature is a finite quantum spectral fact, not continuous-action curvature or instability.',
                'Ground response is a passive spectral diagnostic, not the actual formed state.'])


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
