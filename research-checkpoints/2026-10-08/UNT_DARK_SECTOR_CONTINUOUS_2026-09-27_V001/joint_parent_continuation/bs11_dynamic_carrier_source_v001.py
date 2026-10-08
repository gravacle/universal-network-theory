#!/usr/bin/env python3
"""New supported BS09/BS11 dynamic-carrier experiment; no old solver replay."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gc
import hashlib
import json
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL = HERE / 'BS11_DYNAMIC_CARRIER_SOURCE_V001.md'
SOURCE = HERE / 'bs11_dynamic_carrier_source_v001.py'
RESULT = HERE / 'BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.json'
REPORT = HERE / 'BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.md'
CHECKPOINTS = HERE / 'bs11_dynamic_carrier_source_v001_checkpoints'
OLD_RESULT = HERE / 'BS11_HELD_FEEDBACK_LOOP_SOURCE_V001_RESULT.json'
REFERENCES = [
    ROOT / 'program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md',
    ROOT / 'program-worktree/MODEL.md',
    HERE / 'BS11_HELD_FEEDBACK_LOOP_SOURCE_V001.md',
    HERE / 'bs11_held_feedback_loop_source_v001.py', OLD_RESULT,
]
CASES = [dict(name=f'Nc{nc}_q{q}', Nc=nc, q=q, lambda_R=.5, lambda_J=.25)
         for nc in (1, 3, 6) for q in (0, 1)]
CASES += [dict(name='Nc3_q0_feedback_off', Nc=3, q=0,
              lambda_R=0., lambda_J=0.)]
UD, DELTA, ER, EP, HFLIP, THOP = 1., 0., 1., 1., .10, .10
OP_TOL, EIG_TOL, SYM_TOL, SELECT_TOL, CHI_TOL = 1e-11, 2e-10, 2e-8, 2e-9, 2e-8
MAX_RSS, MAX_ROW_TIME = 512*1024*1024, 60.


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def hashes():
    return {str(p): sha(p) for p in [PROTOCOL, SOURCE, *REFERENCES]}


def frozen_inputs():
    return dict(cases=CASES, h=HFLIP, t=THOP, Omega=6*HFLIP,
                U_d=UD, bare_Delta=DELTA, d_star=2,
                epsilon_r=ER, epsilon_psi=EP, all_copy_couplings=0,
                exterior_records_carriers=0, exterior_degree=1,
                exterior_hopping_and_flips='clamped off by declared support',
                positions='unit regular hexagon, each exterior at 2R',
                source='whole12node half-edge including hopping, affine nodal lapse',
                carrier_source='epsilon_psi sum_v R_v p_v',
                operator_tolerance=OP_TOL, eigen_tolerance=EIG_TOL,
                symmetry_tolerance=SYM_TOL, selection_tolerance=SELECT_TOL,
                susceptibility_tolerance=CHI_TOL, BLAS_threads=1,
                row_time_limit_seconds=MAX_ROW_TIME, peak_RSS_limit_bytes=MAX_RSS)


def exclusive_json(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')


def journal(event, **details):
    entry = dict(utc=utc(), pid=os.getpid(), event=event, **details)
    with (CHECKPOINTS / 'events.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(entry, sort_keys=True, allow_nan=False)+'\n')
        stream.flush()
        os.fsync(stream.fileno())


def matrix_hash(np, matrix):
    return hashlib.sha256(np.ascontiguousarray(matrix, dtype='<f8').tobytes()).hexdigest()


def rotate_mask(mask, shift):
    return sum(((mask >> v) & 1) << ((v+shift) % 6) for v in range(6))


def setup(np, case):
    pmasks = np.array([p for p in range(64) if p.bit_count() == case['Nc']],
                      dtype=np.int64)
    pindex = {int(p): j for j, p in enumerate(pmasks)}
    nb = np.array([[(n >> e) & 1 for e in range(6)] for n in range(64)], dtype=float)
    pb = np.array([[(int(p) >> v) & 1 for v in range(6)] for p in pmasks], dtype=float)
    m, dim = len(pmasks), 64*len(pmasks)
    positions = np.array([(np.cos(2*np.pi*v/6), np.sin(2*np.pi*v/6))
                          for v in range(6)])
    allpos = np.vstack([positions, 2*positions])
    rows = np.arange(dim)
    nstates = rows // m
    pindices = rows % m
    constant = 6*UD +6*case['q']*ER +case['Nc']*EP \
        +case['lambda_J']*case['Nc'] -6*case['lambda_R']*case['q']
    perm = np.array([rotate_mask(int(n), 1)*m
                     +pindex[rotate_mask(int(pmasks[j]), 1)]
                     for n, j in zip(nstates, pindices)], dtype=np.int64)
    inverse = np.argsort(perm)
    reflected = np.array([
        sum(((int(n) >> e) & 1) << ((-e-1) % 6) for e in range(6))*m
        +pindex[sum(((int(pmasks[j]) >> v) & 1) << ((-v) % 6)
                    for v in range(6))]
        for n,j in zip(nstates, pindices)], dtype=np.int64)
    return dict(pmasks=pmasks, pb=pb, nb=nb, m=m, dim=dim, positions=positions,
                allpos=allpos, rows=rows, ns=nstates, ps=pindices,
                constant=constant, perm=perm, inverse=inverse, reflection=reflected)


def construct(np, case, s):
    """Direct whole-source assembly, without twelve dense node matrices."""
    dim, rows, ns, ps = s['dim'], s['rows'], s['ns'], s['ps']
    nb, pb, pos = s['nb'], s['pb'], s['positions']
    lr, lj, q = case['lambda_R'], case['lambda_J'], case['q']
    H = np.zeros((dim,dim)); Gx = np.zeros_like(H); Gy = np.zeros_like(H)
    diagonal = np.zeros(dim); gx = np.zeros(dim); gy = np.zeros(dim)
    car = np.zeros((dim,2))
    for v in range(6):
        d = 1+nb[ns,(v-1)%6]+nb[ns,v]
        onsite = UD*(d-2)**2+q*ER+EP*pb[ps,v]
        exterior = DELTA+lj*pb[ps,v]-lr*q
        diagonal += onsite+UD+exterior
        owned = onsite+2*UD+1.5*exterior
        gx += pos[v,0]*owned; gy += pos[v,1]*owned
        car += EP*pb[ps,v,None]*pos[v]
    for e in range(6):
        u, v = e, (e+1)%6
        weight = (pos[u]+pos[v])/2
        activity = pb[ps,u]+pb[ps,v]-2*pb[ps,u]*pb[ps,v]
        edge_diag = nb[ns,e]*(DELTA+lj*activity-2*lr*q)
        diagonal += edge_diag
        gx += weight[0]*edge_diag; gy += weight[1]*edge_diag
        target = (ns ^ (1 << e))*s['m']+ps
        H[rows,target] += -HFLIP
        Gx[rows,target] += -HFLIP*weight[0]
        Gy[rows,target] += -HFLIP*weight[1]
        eligible = (nb[ns,e] == 1) & (activity == 1)
        src = rows[eligible]
        swapped = s['pmasks'][ps[eligible]] ^ ((1 << u)|(1 << v))
        pindex = {int(p):j for j,p in enumerate(s['pmasks'])}
        dst = ns[eligible]*s['m']+np.array([pindex[int(p)] for p in swapped],dtype=np.int64)
        H[src,dst] += -THOP
        Gx[src,dst] += -THOP*weight[0]
        Gy[src,dst] += -THOP*weight[1]
    H[rows,rows] = diagonal; Gx[rows,rows] = gx; Gy[rows,rows] = gy
    return H, Gx, Gy, car


def weighted_independent(np, case, s, lapses):
    """Separate scalar weighting of each owned node/edge, no source derivative."""
    dim, rows, ns, ps = s['dim'], s['rows'], s['ns'], s['ps']
    nb, pb, q = s['nb'], s['pb'], case['q']
    lr, lj = case['lambda_R'], case['lambda_J']
    matrix = np.zeros((dim,dim)); diag = np.zeros(dim)
    for v in range(6):
        dv = 1+nb[ns,(v-1)%6]+nb[ns,v]
        diag += lapses[v]*(UD*(dv-2)**2+q*ER+pb[ps,v]*EP)
        diag += lapses[v+6]*UD
        diag += (lapses[v]+lapses[v+6])/2*(DELTA+lj*pb[ps,v]-lr*q)
    for edge in range(6):
        u, v = edge, (edge+1)%6
        w = (lapses[u]+lapses[v])/2
        different = pb[ps,u] != pb[ps,v]
        diag += w*nb[ns,edge]*(DELTA+lj*different.astype(float)-2*lr*q)
        target = (ns ^ (1 << edge))*s['m']+ps
        matrix[rows,target] -= HFLIP*w
        lookup = {int(mask):j for j,mask in enumerate(s['pmasks'])}
        use = rows[(nb[ns,edge] == 1) & different]
        for j in use:
            newmask = int(s['pmasks'][ps[j]]) ^ ((1 << u)|(1 << v))
            targetj = int(ns[j])*s['m']+lookup[newmask]
            matrix[j,targetj] -= THOP*w
    matrix[rows,rows] = diag
    return matrix


def analyze(np, case, s, H, Gx, Gy, car, energies, V, old, elapsed,
            array_path, array_sha, recovered):
    checks = []
    def check(name, passed, evidence=None):
        item = dict(name=name, passed=bool(passed))
        if evidence is not None: item['evidence'] = evidence
        checks.append(item)
    dim, rows, inv = s['dim'], s['rows'], s['inverse']
    scale = max(1., float(np.max(np.sum(np.abs(H),axis=1))))
    gscale = max(1., float(np.max(np.sum(np.abs(Gx),axis=1))),
                 float(np.max(np.sum(np.abs(Gy),axis=1))))
    for name, matrix in (('H',H),('Gx',Gx),('Gy',Gy)):
        check(name+'_hermitian', np.max(np.abs(matrix-matrix.T)) <= OP_TOL)
    check('basis_fixed_count', all(int(p).bit_count()==case['Nc'] for p in s['pmasks']))
    check('finite_full_spectrum', np.all(np.isfinite(energies)) and np.all(np.isfinite(V)))
    check('dimension', dim == 64*len(s['pmasks']))
    check('whole_node_sum', np.max(np.abs(weighted_independent(np,case,s,np.ones(12))-H)) <= OP_TOL)
    eta = np.array([1e-6,-2e-6]); lapses = 1+s['allpos']@eta
    check('positive_lapse_arm', np.min(lapses)>0)
    arm = weighted_independent(np,case,s,lapses)
    check('weighted_affine_source', np.max(np.abs(arm-H-eta[0]*Gx-eta[1]*Gy)) <= OP_TOL)
    del arm
    check('uniform_lapse', np.max(np.abs(weighted_independent(np,case,s,np.full(12,.93))-.93*H)) <= OP_TOL)
    check('joint_C6_H', np.max(np.abs(H[np.ix_(inv,inv)]-H)) <= OP_TOL)
    angle = np.pi/3; co, si = np.cos(angle), np.sin(angle)
    check('dipole_C6_Gx', np.max(np.abs(Gx[np.ix_(inv,inv)]-co*Gx-si*Gy)) <= OP_TOL)
    check('dipole_C6_Gy', np.max(np.abs(Gy[np.ix_(inv,inv)]+si*Gx-co*Gy)) <= OP_TOL)
    ref = s['reflection']
    check('reflection_H', np.max(np.abs(H[np.ix_(ref,ref)]-H)) <= OP_TOL)
    residual = orthogonal = 0.
    for start in range(0,dim,128):
        stop = min(start+128,dim); block=V[:,start:stop]
        residual=max(residual,float(np.max(np.abs(H@block-block*energies[start:stop]))))
        prod=V.T@block
        prod[np.arange(start,stop),np.arange(stop-start)] -= 1.
        orthogonal=max(orthogonal,float(np.max(np.abs(prod))))
    check('full_eigen_residual',residual <= EIG_TOL*scale,dict(maximum=residual,tolerance=EIG_TOL*scale))
    check('full_orthonormality',orthogonal <= EIG_TOL,dict(maximum=orthogonal))
    gaps=energies[1:]-energies[0]; ground=V[:,0]
    check('strict_resolved_ground_gap',gaps[0] > 1e-10*scale,dict(gap=float(gaps[0]),threshold=1e-10*scale))
    c6=float(ground@ground[inv]); reflection=float(ground@ground[ref])
    check('ground_C6_k0',abs(c6-1)<=SYM_TOL)
    check('ground_reflection_even',abs(reflection-1)<=SYM_TOL)
    signed=ground*(1 if np.sum(ground)>=0 else -1)
    check('Perron_ground_nonnegative',float(np.min(signed))>=-EIG_TOL)
    means=np.array([ground@Gx@ground,ground@Gy@ground])
    check('ground_full_dipole_mean_null',np.max(np.abs(means)) <= SYM_TOL*gscale)
    wf=np.column_stack([Gx@ground,Gy@ground])
    wc=car*ground[:,None]; wr=wf-wc
    tf=V[:,1:].T@wf; tc=V[:,1:].T@wc; tr=V[:,1:].T@wr
    check('source_transition_decomposition',np.max(np.abs(tf-tc-tr))<=EIG_TOL*gscale)
    ward=V[:,1:].T@(H@ground)
    check('uniform_time_transition_null',np.max(np.abs(ward))<=EIG_TOL*scale)
    projector=np.zeros_like(wf); rotated=wf.copy()
    for shift in range(6):
        projector += (2/6)*np.cos(2*np.pi*shift/6)*rotated
        rotated=rotated[inv]
    selection=float(np.max(np.abs(projector-wf)))
    check('dipole_only_joint_k_plus_minus_1',selection<=SELECT_TOL*gscale,
          dict(maximum=selection,tolerance=SELECT_TOL*gscale))
    chi=lambda a,b:2*a.T@(b/gaps[:,None])
    full=chi(tf,tf); carr=chi(tc,tc); rest=chi(tr,tr)
    cross=chi(tc,tr)+chi(tr,tc)
    chiscale=max(1.,float(np.max(np.abs(full))))
    check('chi_decomposition',np.max(np.abs(full-carr-rest-cross))<=CHI_TOL*chiscale)
    for name, matrix in (('full',full),('carrier',carr),('rest',rest)):
        check('chi_'+name+'_PSD',float(np.min(np.linalg.eigvalsh(matrix)))>=-CHI_TOL*max(1.,float(np.max(np.abs(matrix)))))
    check('full_chi_isotropic',abs(full[0,0]-full[1,1])<=CHI_TOL*chiscale
          and abs(full[0,1])<=CHI_TOL*chiscale)
    probability=ground.reshape(64,s['m'])**2
    ndist=probability.sum(axis=1); pdist=probability.sum(axis=0)
    pmean=pdist@s['pb']; nmean=ndist@s['nb']
    corr=s['pb'].T@(pdist[:,None]*s['pb'])
    check('normalized_ground_probability',abs(float(probability.sum())-1)<=EIG_TOL)
    check('carrier_count_expectation',abs(float(pmean.sum())-case['Nc'])<=SYM_TOL)
    check('carrier_correlation_diagonal',np.max(np.abs(np.diag(corr)-pmean))<=EIG_TOL)
    check('rotation_invariant_carrier_mean',np.max(np.abs(pmean-case['Nc']/6))<=SYM_TOL)
    check('rotation_invariant_incidence_mean',np.max(np.abs(nmean-nmean[0]))<=SYM_TOL)
    activity=[]; joint=[]; flips=[]; hopping=[]; degree_means=[]; degree_penalties=[]
    pindex={int(mask):j for j,mask in enumerate(s['pmasks'])}
    for e in range(6):
        nextv=(e+1)%6
        a=s['pb'][:,e]+s['pb'][:,nextv]-2*s['pb'][:,e]*s['pb'][:,nextv]
        activity.append(float(pdist@a))
        joint.append(float(np.sum(probability*s['nb'][:,e,None]*a[None,:])))
        flips.append(float(ground@ground[(s['ns']^(1<<e))*s['m']+s['ps']]))
        eligible=(s['nb'][s['ns'],e]==1)&(a[s['ps']]==1)
        src=rows[eligible]
        dst=np.array([int(s['ns'][j])*s['m']+pindex[int(s['pmasks'][s['ps'][j]])^((1<<e)|(1<<nextv))] for j in src],dtype=np.int64)
        hopping.append(float(ground[src]@ground[dst]))
        degree=1+s['nb'][:,(e-1)%6]+s['nb'][:,e]
        degree_means.append(float(ndist@degree))
        degree_penalties.append(float(ndist@(degree-2)**2))
    components=dict(active_degree=UD*sum(degree_penalties),exterior_degree=6*UD,
                    record_storage=6*case['q']*ER,carrier_storage=case['Nc']*EP,
                    external_current_square=case['lambda_J']*case['Nc'],
                    external_record_feedback=-6*case['lambda_R']*case['q'],
                    internal_current_square=case['lambda_J']*sum(joint),
                    internal_record_feedback=-2*case['lambda_R']*case['q']*float(nmean.sum()),
                    incidence_flip=-HFLIP*sum(flips),carrier_hopping=-THOP*sum(hopping),
                    bare_incidence=0.)
    check('absolute_energy_components',abs(sum(components.values())-float(energies[0]))<=EIG_TOL*scale)
    if case['Nc']==6:
        check('fully_occupied_no_current_square',max(map(abs,activity))<=OP_TOL)
        check('fully_occupied_no_hopping',max(map(abs,hopping))<=OP_TOL)
        check('fully_occupied_carrier_source_null',np.max(np.abs(tc))<=EIG_TOL*gscale)
    custody=[]
    if case['Nc']==3 and case['lambda_J']==.25:
        for pattern, mask in [('alternating',42),('cluster',7)]:
            previous=next(r for r in old['rows'] if r['pattern']==pattern
                          and r['q']==case['q'] and r['h_fraction']=='1/10')
            ov=np.array(previous['all_eigenvectors_columns'])
            oe=np.array(previous['all_complete_eigenvalues'])
            oldH=(ov*oe)@ov.T
            j=pindex[mask]; select=np.arange(64)*s['m']+j
            block=H[np.ix_(select,select)]
            err=float(np.max(np.abs(block-oldH)))
            check('sealed_held_H_block_'+pattern,err<=OP_TOL,dict(maximum=err))
            oldg=ov[:,0]; oldt=np.array(previous['all_source_transition_vectors'])
            oldmean=np.array(previous['complete_ground_source_mean'])
            source_error=[]
            for i,G in enumerate((Gx,Gy)):
                expected=ov[:,1:]@oldt[:,i]+oldmean[i]*oldg
                error=float(np.max(np.abs(G[np.ix_(select,select)]@oldg-expected)))
                source_error.append(error)
                check('sealed_held_G_action_'+pattern+'_'+str(i),error<=OP_TOL*gscale,dict(maximum=error))
            custody.append(dict(pattern=pattern,carrier_mask=mask,H_maximum=err,
                                G_action_maximum=source_error,old_matrix_sha256=previous['matrix_sha256']))
    characters=np.empty((6,dim)); turned=V
    for shift in range(6):
        characters[shift]=np.sum(V*turned,axis=0)
        if shift<5: turned=turned[inv]
    weights=np.array([np.sum(np.cos(2*np.pi*k*np.arange(6)/6)[:,None]*characters,axis=0)/6
                      for k in range(6)]).T
    check('C6_projector_weights_normalized',np.max(np.abs(weights.sum(axis=1)-1))<=SYM_TOL)
    check('C6_projector_weights_nonnegative',float(np.min(weights))>=-SYM_TOL)
    grouping_tolerance=1e-9*scale
    groups=[]; start=0
    while start<len(gaps):
        stop=start+1
        while stop<len(gaps) and abs(gaps[stop]-gaps[start])<=grouping_tolerance:
            stop+=1
        sl=slice(start,stop); groupchi=2*tf[sl].T@(tf[sl]/gaps[sl,None])
        groups.append(dict(first_excited_index=start+1,last_excited_index=stop,
                           gap_min=float(gaps[start]),gap_max=float(gaps[stop-1]),
                           C2_parities=characters[3,start+1:stop+1].tolist(),
                           C6_projector_weight_sum=weights[start+1:stop+1].sum(axis=0).tolist(),
                           full_dipole_weight=float(np.sum(tf[sl]**2)),
                           chi_trace=float(np.trace(groupchi)),chi=groupchi.tolist()))
        start=stop
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    check('row_under_60seconds',elapsed<MAX_ROW_TIME,dict(seconds=elapsed,limit=MAX_ROW_TIME))
    check('peak_under_512MiB',peak<MAX_RSS,dict(peak_bytes=peak,limit_bytes=MAX_RSS))
    return dict(case=case,dimension=dim,complete_constant=s['constant'],
                complete_ground_energy=float(energies[0]),lowest_gap=float(gaps[0]),
                ground_C6=c6,ground_reflection=reflection,ground_source_mean=means.tolist(),
                source_identity_means=[float(np.trace(Gx)/dim),float(np.trace(Gy)/dim)],
                chi_full=full.tolist(),chi_carrier=carr.tolist(),chi_rest=rest.tolist(),
                chi_cross_signed=cross.tolist(),chi_traces=dict(full=float(np.trace(full)),
                    carrier=float(np.trace(carr)),rest=float(np.trace(rest)),cross=float(np.trace(cross))),
                carrier_mean=pmean.tolist(),carrier_pair_correlation=corr.tolist(),
                carrier_mask_probabilities={str(int(p)):float(w) for p,w in zip(s['pmasks'],pdist)},
                incidence_mean=nmean.tolist(),active_degree_mean=degree_means,
                active_degree_penalty_mean=degree_penalties,current_square_mean=activity,
                incidence_current_square_mean=joint,incidence_flip_mean=flips,
                occupied_edge_transfer_mean=hopping,
                mean_current='zero for real ground; J is imaginary antisymmetric',
                absolute_energy_components=components,mode_groups=groups,
                all_excited_source_transition_vectors=tf.tolist(),
                all_excited_carrier_source_transition_vectors=tc.tolist(),
                all_excited_rest_source_transition_vectors=tr.tolist(),
                all_C2_parities=characters[3].tolist(),all_C6_projector_weights=weights.tolist(),
                held_block_custody=custody,eigen_residual_maximum=residual,
                orthonormality_maximum=orthogonal,array_path=str(array_path),
                array_sha256=array_sha,recovered_eigensystem_without_solve=recovered,
                elapsed_seconds=elapsed,peak_RSS_bytes=peak,checks=checks,
                passed_count=sum(c['passed'] for c in checks),
                failed_count=sum(not c['passed'] for c in checks))


def write_final(receipt):
    receipt['completed_utc']=utc()
    receipt['check_count']=len(receipt['checks'])+sum(len(r['checks']) for r in receipt['rows'])
    receipt['passed_count']=sum(c['passed'] for c in receipt['checks'])+sum(r['passed_count'] for r in receipt['rows'])
    receipt['failed_count']=receipt['check_count']-receipt['passed_count']
    payload=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with RESULT.open('xb') as stream:stream.write(payload)
    digest=hashlib.sha256(payload).hexdigest()
    lines=['# BS11 dynamic-carrier/source V001: saved result','',
           f"Status: {receipt['status']}. Checks {receipt['passed_count']}/{receipt['check_count']}; failures {receipt['failed_count']}.",'',
           receipt['qualification'],'',
           '| Case | dimension | complete E0 | lowest gap | chi trace | carrier | rest | signed cross |',
           '|---|---:|---:|---:|---:|---:|---:|---:|']
    for row in receipt['rows']:
        c=row['chi_traces']
        lines.append(f"| {row['case']['name']} | {row['dimension']} | {row['complete_ground_energy']:.12g} | {row['lowest_gap']:.12g} | {c['full']:.12g} | {c['carrier']:.12g} | {c['rest']:.12g} | {c['cross']:.12g} |")
    lines+=['','Carrier correlations are predicted in fixed-count cold ground states; records remain held and external support is imposed. Absolute storage and external-link energies are retained as Nc changes.','',
            'Whole-source susceptibility, carrier storage, remaining interactions and signed cross terms are all retained. Soft gaps are not assigned held-loop labels. Complete new eigenstates are saved in exclusive authenticated per-row arrays. No old producer or eigensolver was replayed.','',
            f"Runtime {receipt['runtime_seconds']:.6g}s; peak process RSS {receipt['peak_RSS_bytes']} bytes; PID {receipt['pid']}.",'',
            f'Result JSON SHA256: {digest}','',f"Exact next unfinished case: {receipt.get('next_unfinished_case')}",'',
            'Input SHA256 custody:']
    lines += ['- '+path+': '+value for path,value in receipt['input_sha256'].items()]
    if 'exception' in receipt:lines+=['','ERROR traceback is preserved in JSON.']
    with REPORT.open('x',encoding='utf-8') as stream:stream.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(status=receipt['status'],rows=len(receipt['rows']),
                         checks=receipt['check_count'],passed=receipt['passed_count'],
                         failed=receipt['failed_count'],runtime_seconds=receipt['runtime_seconds'],
                         peak_RSS_bytes=receipt['peak_RSS_bytes'],json_sha256=digest,
                         json_path=str(RESULT),markdown_path=str(REPORT),
                         next_unfinished_case=receipt.get('next_unfinished_case'),
                         exception=receipt.get('exception')),indent=2))


def execute(resume=False):
    if sys.platform!='darwin':raise RuntimeError('This worker is restricted to this Mac')
    if SOURCE.resolve()!=Path(__file__).resolve():raise RuntimeError('Unexpected source location')
    if RESULT.exists() or REPORT.exists():raise FileExistsError('Final output exists; no replay/overwrite')
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
        os.environ[key]='1'
    current_hashes=hashes(); inputs=frozen_inputs()
    manifest_path=CHECKPOINTS/'manifest.json'
    prior_events=[]
    if resume:
        manifest=json.loads(manifest_path.read_text())
        if manifest['input_sha256']!=current_hashes or manifest['inputs']!=inputs:
            raise RuntimeError('Interrupted input custody mismatch; recovery blocked')
        if manifest['host']!=socket.gethostname():raise RuntimeError('Other host recovery forbidden')
        prior_events=[json.loads(line) for line in (CHECKPOINTS/'events.jsonl').read_text().splitlines()]
        prior_starts=[event for event in prior_events if event['event']=='run_start']
        prior_pid=prior_starts[-1]['pid'] if prior_starts else manifest['pid']
        try:os.kill(prior_pid,0)
        except ProcessLookupError:pass
        else:raise RuntimeError('Latest worker PID still exists; execution ownership uncertain')
    else:
        CHECKPOINTS.mkdir()
        manifest=dict(created_utc=utc(),host=socket.gethostname(),pid=os.getpid(),
                      input_sha256=current_hashes,inputs=inputs)
        exclusive_json(manifest_path,manifest)
    started=time.perf_counter()
    receipt=dict(status='RUNNING',started_utc=utc(),host=socket.gethostname(),pid=os.getpid(),
                 input_sha256=current_hashes,inputs=inputs,rows=[],checks=[],
                 qualification='Supported fixed-count BS09/BS11 cold ground states and proposed nodal-lapse source only; no physical gravity, record formation, volume work, h(s), criticality, fit or superiority.',
                 resume=resume,checkpoint_manifest_sha256=sha(manifest_path))
    journal('run_start',resume=resume,input_sha256=current_hashes)
    try:
        import numpy as np
        old=json.loads(OLD_RESULT.read_text())
        for case in CASES:
            name=case['name']; receipt['next_unfinished_case']=name
            row_path=CHECKPOINTS/(name+'.json'); array_path=CHECKPOINTS/(name+'.npz')
            began_path=CHECKPOINTS/(name+'.started.json')
            if row_path.exists():
                row=json.loads(row_path.read_text())
                commits=[event for event in prior_events
                         if event['event']=='row_complete' and event['case']==name]
                if not commits or commits[-1]['row_sha256']!=sha(row_path):
                    raise RuntimeError('Completed row does not match journal commit: '+name)
                if row['input_sha256']!=current_hashes or row['case']!=case or row['array_sha256']!=sha(array_path):
                    raise RuntimeError('Completed row custody mismatch: '+name)
                receipt['rows'].append(row)
                journal('reuse_completed_row',case=name,array_sha256=row['array_sha256'])
                if row['failed_count']:raise RuntimeError('Preserved failed row forbids continuation')
                continue
            if began_path.exists() and not array_path.exists():
                raise RuntimeError('Started row has no recoverable eigensystem; parent decision needed: '+name)
            if not began_path.exists():
                exclusive_json(began_path,dict(case=case,input_sha256=current_hashes,
                                               started_utc=utc(),pid=os.getpid()))
            row_started=time.perf_counter(); s=setup(np,case)
            H,Gx,Gy,car=construct(np,case,s)
            matrix_sha={key:matrix_hash(np,value) for key,value in [('H',H),('Gx',Gx),('Gy',Gy)]}
            recovered=array_path.exists()
            if recovered:
                with np.load(array_path,allow_pickle=False) as archive:
                    if json.loads(str(archive['input_sha256_json']))!=current_hashes \
                       or json.loads(str(archive['case_json']))!=case \
                       or json.loads(str(archive['matrix_sha256_json']))!=matrix_sha \
                       or not np.array_equal(archive['carrier_masks'],s['pmasks']):
                        raise RuntimeError('Orphan eigensystem custody mismatch: '+name)
                    energies=archive['complete_eigenvalues']; V=archive['eigenvectors_columns']
                    if V.shape!=(s['dim'],s['dim']) or energies.shape!=(s['dim'],):
                        raise RuntimeError('Incomplete eigensystem: '+name)
                journal('recover_eigensystem_without_solve',case=name,array_sha256=sha(array_path))
            else:
                journal('solve_start',case=name,dimension=s['dim'],matrix_sha256=matrix_sha)
                H[s['rows'],s['rows']]-=s['constant']
                centered,V=np.linalg.eigh(H)
                H[s['rows'],s['rows']]+=s['constant']
                energies=centered+s['constant']
                with array_path.open('xb') as stream:
                    np.savez(stream,complete_eigenvalues=energies,eigenvectors_columns=V,
                             carrier_masks=s['pmasks'],incidence_states=np.arange(64),
                             input_sha256_json=json.dumps(current_hashes,sort_keys=True),
                             case_json=json.dumps(case,sort_keys=True),
                             matrix_sha256_json=json.dumps(matrix_sha,sort_keys=True))
                    stream.flush();os.fsync(stream.fileno())
                journal('eigensystem_saved',case=name,array_sha256=sha(array_path))
            elapsed=time.perf_counter()-row_started
            row=analyze(np,case,s,H,Gx,Gy,car,energies,V,old,elapsed,array_path,sha(array_path),recovered)
            # Include analysis and persistence in the prospective time/resource gates.
            elapsed=time.perf_counter()-row_started; row['elapsed_seconds']=elapsed
            for c in row['checks']:
                if c['name']=='row_under_60seconds':
                    c.update(passed=elapsed<MAX_ROW_TIME,evidence=dict(seconds=elapsed,limit=MAX_ROW_TIME))
            row['passed_count']=sum(c['passed'] for c in row['checks'])
            row['failed_count']=sum(not c['passed'] for c in row['checks'])
            row['input_sha256']=current_hashes;row['matrix_sha256']=matrix_sha
            exclusive_json(row_path,row)
            journal('row_complete',case=name,row_sha256=sha(row_path),
                    passed=row['passed_count'],failed=row['failed_count'],seconds=elapsed)
            receipt['rows'].append(row)
            print(json.dumps(dict(event='row_complete',case=name,dimension=s['dim'],
                    passed=row['passed_count'],failed=row['failed_count'],seconds=elapsed,
                    lowest_gap=row['lowest_gap'],chi_trace=row['chi_traces']['full'])),flush=True)
            del H,Gx,Gy,car,energies,V,s
            gc.collect()
            if row['failed_count']:break
        receipt['checks'].append(dict(name='input_bytes_unchanged',passed=hashes()==current_hashes))
        receipt['checks'].append(dict(name='all_seven_rows_complete',passed=len(receipt['rows'])==len(CASES)))
        complete_names={r['case']['name'] for r in receipt['rows']}
        receipt['next_unfinished_case']=next((c['name'] for c in CASES if c['name'] not in complete_names),None)
        failed=any(not c['passed'] for c in receipt['checks']) or any(r['failed_count'] for r in receipt['rows'])
        receipt['status']='FAILED' if failed else 'QUALIFIED_ARITHMETIC'
    except Exception:
        receipt['status']='ERROR';receipt['exception']=traceback.format_exc()
        journal('error',exception=receipt['exception'],next_unfinished_case=receipt.get('next_unfinished_case'))
    receipt['runtime_seconds']=time.perf_counter()-started
    receipt['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    journal('run_complete',status=receipt['status'],rows=len(receipt['rows']))
    write_final(receipt)
    return 0 if receipt['status']=='QUALIFIED_ARITHMETIC' else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    if args.resume and not args.execute:parser.error('--resume requires --execute and separate ownership approval')
    if not args.execute:
        print(json.dumps(dict(mode='describe_only',inputs=frozen_inputs(),input_sha256=hashes()),indent=2))
        return 0
    return execute(args.resume)


if __name__=='__main__':
    sys.exit(main())
