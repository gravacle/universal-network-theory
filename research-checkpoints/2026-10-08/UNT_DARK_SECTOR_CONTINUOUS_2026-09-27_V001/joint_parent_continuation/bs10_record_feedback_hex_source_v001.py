#!/usr/bin/env python3
"""One new dipole-source ground certificate; base data are read, never replayed."""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import hashlib
import json
import math
import os
import resource
import sys
import time
import traceback
import numpy as np

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME = 'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J/(NAME+'.md')
RESULT = J/(NAME+'_RESULT.json')
REPORT = J/(NAME+'_RESULT.md')
RECEIPT = J/(NAME+'_RECEIPT.json')
CP = J/'bs10_record_feedback_hex_source_v001_checkpoints'
BASE_NAME = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
BASE_CP = J/'bs10_record_feedback_hex_finite_v001_checkpoints'
H = Fraction(1,5)
ALPHA = Fraction(1,20)
W = (Fraction(1),Fraction(1,2),Fraction(-1,2),Fraction(-1),Fraction(-1,2),Fraction(1,2))
P = (21,42)
SEED_DENOMINATOR = 10**12
EXPANSION_ATTEMPTS = 24
REFINEMENT_STEPS = 32
OFFSETS = (0,1,-1,2,-2)
FRACTIONS = (Fraction(1,2),Fraction(1,3),Fraction(2,3),Fraction(2,5),Fraction(3,5))
TARGET_WIDTH = Fraction(1,10**11)
ATTEMPT_CREATED = False
INERTIA_SERIAL = 0
CP_HASHES = {}
INPUTS = {
    'bs10_record_feedback_hex_finite_v001.py':'5da24abbbccb8d485853cd44caeb1698236be40270be0ba38fc5533c5778e253',
    'BS10_RECORD_FEEDBACK_HEX_FINITE_V001.md':'751fcc756e6ffbbab56f37c7998f29ff6cc32189f77634aeeb2703ccabed78c1',
    'BS10_RECORD_FEEDBACK_HEX_FINITE_V001_RESULT.json':'498a0f582a34e79bd7b56fb76531f93500ee4fa175e9a94d3f62d955e43546ee',
    'BS10_RECORD_FEEDBACK_HEX_FINITE_V001_RECEIPT.json':'7282f7dcf7cc6dbe246f9281f79897898190e0ce0cf82fa754e82423fb8682fd',
    'HELD_HEX_NATIVE_DIPOLE_SOURCE_GATE_V001.md':'bf8e581bbe4038cc276ed81c6230aafb8e3bf29de366ce1b67ade0fc2898480d',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def exact(x):
    x = Fraction(x)
    out = {'numerator':x.numerator,'denominator':x.denominator}
    displays = []
    for mode in (ROUND_FLOOR,ROUND_CEILING):
        with localcontext() as context:
            context.prec,context.rounding = 20,mode
            displays.append(str(Decimal(x.numerator)/Decimal(x.denominator)))
    out['decimal20_lower'],out['decimal20_upper'] = displays
    return out


def fraction(x):
    return Fraction(x['numerator'],x['denominator'])


def interval(lo,hi):
    return {'lower':exact(lo),'upper':exact(hi),'width':exact(hi-lo)}


def exclusive(path,obj):
    with path.open('xb') as stream:
        stream.write(canonical(obj)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def event(kind,**fields):
    row = {'event':kind,'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,**fields}
    with (CP/'journal.jsonl').open('ab') as stream:
        stream.write(canonical(row)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def save_stage(name,obj,**fields):
    digest = exclusive(CP/name,obj)
    CP_HASHES[name] = digest
    event('stage_complete',filename=name,sha256=digest,**fields)
    return digest


def add(checks,label,condition):
    checks.append({'label':label,'passed':bool(condition)})


def authenticate():
    direct = {}
    for name,wanted in INPUTS.items():
        got = sha(J/name)
        if got != wanted:
            raise RuntimeError('Frozen direct input mismatch: '+name)
        direct[name] = got
    base = json.loads((J/(BASE_NAME+'_RESULT.json')).read_text())
    receipt = json.loads((J/(BASE_NAME+'_RECEIPT.json')).read_text())
    if receipt['result_raw_sha256'] != direct[BASE_NAME+'_RESULT.json']:
        raise RuntimeError('Base raw receipt mismatch')
    if receipt['result_canonical_sha256'] != hashlib.sha256(canonical(base)).hexdigest():
        raise RuntimeError('Base canonical receipt mismatch')
    report_hash = sha(J/(BASE_NAME+'_RESULT.md'))
    if report_hash != receipt['report_sha256']:
        raise RuntimeError('Base report byte receipt mismatch')
    for key,name in (('source_sha256','bs10_record_feedback_hex_finite_v001.py'),('protocol_sha256',BASE_NAME+'.md')):
        if base[key] != direct[name] or receipt[key] != direct[name]:
            raise RuntimeError('Base source/protocol mismatch')
    if base['input_sha256'] != receipt['input_sha256'] or base['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Base input/checkpoint map mismatch')
    inherited = {}
    for rel,wanted in receipt['input_sha256'].items():
        got = sha(ROOT/rel)
        if got != wanted:
            raise RuntimeError('Inherited input changed: '+rel)
        inherited[rel] = got
    checkpoints = {}
    for name,wanted in receipt['checkpoint_sha256'].items():
        got = sha(BASE_CP/name)
        if got != wanted:
            raise RuntimeError('Base checkpoint changed: '+name)
        checkpoints[name] = got
    lines = (BASE_CP/'journal.jsonl').read_bytes().splitlines(keepends=True)
    last = json.loads(lines[-1])
    if last['event'] != 'receipt_complete' or last['receipt_sha256'] != direct[BASE_NAME+'_RECEIPT.json']:
        raise RuntimeError('Base final receipt event mismatch')
    if hashlib.sha256(b''.join(lines[:-1])).hexdigest() != receipt['journal_prefix_sha256']:
        raise RuntimeError('Base journal prefix mismatch')
    if base['held_cell_certificate_status'] != 'ISOLATED_PAIR_CERTIFIED' or base['checks_failed'] != 0:
        raise RuntimeError('Base isolated-pair premise is not qualified')
    structure = json.loads((BASE_CP/'structure.json').read_text())
    prefix = structure['checks']
    alias = base['structural_checks']['checks']
    if prefix != alias[:len(prefix)]:
        raise RuntimeError('Preserved base structural-check prefix mismatch')
    for key in ('physical_n_diagonal','P_words','Q_words','H_edges','Q_edges','WWdagger_scalar'):
        if structure[key] != base['structural_checks'][key]:
            raise RuntimeError('Base structural data mismatch: '+key)
    return {'direct_input_sha256':direct,'inherited_input_sha256':inherited,'base_checkpoint_sha256':checkpoints,
            'base_report_sha256':report_hash,
            'base_journal_prefix_sha256':receipt['journal_prefix_sha256'],
            'preserved_base_check_alias':{'checkpoint_count':len(prefix),'result_nested_count':len(alias),'prefix_equal':True}},base


def rotate(n,step):
    return sum(((n>>v)&1)<<((v+step)%6) for v in range(6))


def components(n):
    out = []
    for v in range(6):
        delta = ((n>>((v-1)%6))&1)+((n>>v)&1)-1
        out.append(Fraction(delta*delta)-Fraction(delta,2))
    return out


def source_model(base):
    checks = []
    parent = base['structural_checks']
    base_diag = [fraction(x) for x in parent['physical_n_diagonal']]
    cube_edges = [tuple(x) for x in parent['H_edges']]
    fv = [components(n) for n in range(64)]
    lapses = tuple(1+ALPHA*x for x in W)
    a_diag = [sum((W[v]*values[v] for v in range(6)),Fraction(0)) for values in fv]
    diagonal = [sum((lapses[v]*values[v] for v in range(6)),Fraction(0)) for values in fv]
    opposite_diag = [base_diag[n]-ALPHA*a_diag[n] for n in range(64)]
    edges,a_edges,lookup = [],[],{}
    for n,m in cube_edges:
        xor = n^m
        e = xor.bit_length()-1
        add(checks,f'cube_edge_{n}_{m}',xor == 1<<e)
        a = -H*(W[e]+W[(e+1)%6])/2
        value = -H+ALPHA*a
        edges.append((n,m,value))
        a_edges.append((n,m,a))
        lookup[(n,m)] = value
    for n in range(64):
        add(checks,f'full_native_f_sum_{n}',sum(fv[n],Fraction(0)) == base_diag[n])
        add(checks,f'linear_source_diagonal_{n}',diagonal[n] == base_diag[n]+ALPHA*a_diag[n])
        add(checks,f'rotation3_diagonal_{n}',diagonal[n] == opposite_diag[rotate(n,3)])
        for v in range(6):
            add(checks,f'local_C6_covariance_{n}_{v}',fv[rotate(n,1)][v] == fv[n][(v-1)%6])
    for n,m,a in a_edges:
        key = tuple(sorted((rotate(n,3),rotate(m,3))))
        add(checks,f'rotation3_flip_{n}_{m}',lookup[key] == -H-ALPHA*a)
        add(checks,f'halfedge_sum_identity_{n}_{m}',-H/2-H/2 == -H)
        add(checks,f'linear_source_flip_{n}_{m}',(lookup[(n,m)]+(-H-ALPHA*a))/2 == -H)
    add(checks,'sum_weights_zero',sum(W,Fraction(0)) == 0)
    add(checks,'lowpair_cross_weight_zero',sum(((-1)**v*W[v] for v in range(6)),Fraction(0)) == 0)
    add(checks,'weight_rotation3_negative',all(W[(v+3)%6] == -W[v] for v in range(6)))
    add(checks,'positive_local_lapse',min(lapses) == Fraction(19,20))
    flip_factors = [-(x[2])/H for x in edges]
    add(checks,'positive_flip_profile',min(flip_factors) == Fraction(77,80))
    add(checks,'P_diagonal_A_zero',all(a_diag[n] == 0 for n in P))
    a_neighbors = {p:{} for p in P}
    for n,m,a in a_edges:
        for p in P:
            if p == n:
                a_neighbors[p][m] = a
            elif p == m:
                a_neighbors[p][n] = a
    p_a2 = {p:sum((a*a for a in a_neighbors[p].values()),Fraction(0)) for p in P}
    add(checks,'P_A_P_no_direct_flip',not any(n in P and m in P for n,m,a in a_edges))
    add(checks,'P_A2_diagonal',all(x == Fraction(9,4)*H**2 for x in p_a2.values()))
    add(checks,'P_A2_offdiagonal_zero',not(set(a_neighbors[P[0]])&set(a_neighbors[P[1]])))
    off_sums = [Fraction(0)]*64
    for n,m,a in a_edges:
        off_sums[n] += abs(a)
        off_sums[m] += abs(a)
    add(checks,'A_diagonal_bound_three',max(abs(x) for x in a_diag) <= 3)
    add(checks,'A_offdiagonal_row_sum_3h',all(x == 3*H for x in off_sums))
    for lapse in (Fraction(1,2),Fraction(2)):
        for n in range(64):
            direct = sum((lapse*lapses[v]*fv[n][v] for v in range(6)),Fraction(0))
            add(checks,f'uniform_L{lapse}_diagonal{n}',direct == lapse*diagonal[n])
        for n,m,value in edges:
            e = (n^m).bit_length()-1
            direct = -H*(lapse*lapses[e]+lapse*lapses[(e+1)%6])/2
            add(checks,f'uniform_L{lapse}_flip{n}_{m}',direct == lapse*value)
    structure = {'alpha':exact(ALPHA),'h':exact(H),'w':[exact(x) for x in W],
                 'L_inside':[exact(x) for x in lapses],'base_diagonal_from_sealed_input':[exact(x) for x in base_diag],
                 'source_diagonal':[exact(x) for x in a_diag],'new_Halpha_diagonal':[exact(x) for x in diagonal],
                 'source_edges':[[n,m,exact(a)] for n,m,a in a_edges],
                 'new_Halpha_edges':[[n,m,exact(value)] for n,m,value in edges],
                 'P_A2_P_diagonal':{str(p):exact(x) for p,x in p_a2.items()},
                 'A_norm_upper':exact(3+3*H),'low_pair_dipole_block':'EXACT_ZERO_BY_C6_SELECTION',
                 'direct_second_alpha_contact':'EXACT_ZERO_LINEAR_OWNED_ACTION','checks':list(checks)}
    return {'diagonal':diagonal,'edges':edges},structure,checks


class ZeroMinor(Exception):
    def __init__(self,index,minors):
        self.index,self.minors = index,minors
        super().__init__('Zero leading minor at order '+str(index))


def bareiss(matrix):
    a = [row[:] for row in matrix]
    size,previous,minors,divisions = len(a),1,[],0
    for k in range(size-1):
        pivot = a[k][k]
        minors.append(pivot)
        if pivot == 0:
            raise ZeroMinor(k+1,minors)
        for i in range(k+1,size):
            for j in range(i,size):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                value,remainder = divmod(numerator,previous)
                if remainder:
                    raise ArithmeticError('Nonexact Bareiss division')
                a[i][j] = a[j][i] = value
                divisions += 1
        for i in range(k+1,size):
            a[i][k] = a[k][i] = 0
        previous = pivot
    minors.append(a[-1][-1])
    if minors[-1] == 0:
        raise ZeroMinor(size,minors)
    signs = [1]+[1 if x>0 else -1 for x in minors]
    return minors,sum(a!=b for a,b in zip(signs,signs[1:])),divisions


def direct_det(matrix):
    out = 0
    for order in permutations(range(len(matrix))):
        inversions = sum(order[i]>order[j] for i in range(len(order)) for j in range(i+1,len(order)))
        term = (-1)**inversions
        for i,j in enumerate(order):
            term *= matrix[i][j]
        out += term
    return out


def algorithm_controls():
    checks,rows = [],[]
    for i,matrix in enumerate(([[2,1],[1,-1]],[[0,1],[1,2]],[[2,1,0],[1,3,1],[0,1,-1]])):
        direct = [direct_det([row[:n] for row in matrix[:n]]) for n in range(1,len(matrix)+1)]
        try:
            minors,count,divisions = bareiss(matrix)
            add(checks,f'algorithm_control{i}_minors',minors == direct)
            add(checks,f'algorithm_control{i}_inertia',count == 1)
            rows.append({'matrix':matrix,'direct_minors':direct,'bareiss_minors':minors,'negative_inertia':count})
        except ZeroMinor as error:
            add(checks,f'algorithm_control{i}_zero',i == 1 and error.index == 1 and direct[0] == 0)
            rows.append({'matrix':matrix,'direct_minors':direct,'rejected_zero_order':error.index})
    return {'rows':rows,'checks':list(checks)},checks


def inertia_candidate(model,shift,purpose):
    global INERTIA_SERIAL
    denominators = [shift.denominator]+[x.denominator for x in model['diagonal']]+[x.denominator for n,m,x in model['edges']]
    scale = math.lcm(*denominators)
    matrix = [[0]*64 for _ in range(64)]
    for n,value in enumerate(model['diagonal']):
        matrix[n][n] = int(scale*(value-shift))
    for n,m,value in model['edges']:
        matrix[n][m] = matrix[m][n] = int(scale*value)
    serial = INERTIA_SERIAL
    INERTIA_SERIAL += 1
    row = {'serial':serial,'matrix':'NEW_Halpha_ONLY','dimension':64,'shift':exact(shift),
           'positive_integer_scale':scale,'purpose':purpose}
    try:
        minors,count,divisions = bareiss(matrix)
        row.update({'valid_nonzero_leading_minors':True,'leading_minors_scaled_integer':minors,
                    'negative_inertia':count,'exact_divisions':divisions})
    except ZeroMinor as error:
        row.update({'valid_nonzero_leading_minors':False,'rejected_zero_minor_order':error.index,
                    'leading_minors_scaled_integer':error.minors,'negative_inertia':None})
    name = f'inertia_{serial:04d}.json'
    save_stage(name,row,valid=row['valid_nonzero_leading_minors'])
    row['checkpoint_filename'] = name
    return row


def ground_bracket(model,seed):
    center = Fraction(math.floor(seed*SEED_DENOMINATOR),SEED_DENOMINATOR)
    attempts,lo,hi = [],None,None
    for j in range(EXPANSION_ATTEMPTS):
        radius = Fraction(2**j,SEED_DENOMINATOR)
        endpoints = []
        for side,base in (('lower',center-radius),('upper',center+radius)):
            candidate = None
            for offset in OFFSETS:
                shift = base+Fraction(offset,17*SEED_DENOMINATOR)
                row = inertia_candidate(model,shift,f'expand{j}_{side}_offset{offset}')
                if row['valid_nonzero_leading_minors']:
                    candidate = (shift,row)
                    break
            endpoints.append(candidate)
        attempts.append({'attempt':j,'radius':exact(radius),
                         'lower_checkpoint':None if endpoints[0] is None else endpoints[0][1]['checkpoint_filename'],
                         'upper_checkpoint':None if endpoints[1] is None else endpoints[1][1]['checkpoint_filename']})
        if all(x is not None for x in endpoints):
            if endpoints[0][1]['negative_inertia'] == 0 and endpoints[1][1]['negative_inertia'] == 1:
                lo,hi = endpoints
                break
    if lo is None:
        save_stage('UNRESOLVED_bracket.json',{'attempts':attempts,'center':exact(center)})
        raise ArithmeticError('Frozen expansion attempts exhausted')
    refinements = []
    for step in range(REFINEMENT_STEPS):
        if hi[0]-lo[0] <= TARGET_WIDTH:
            break
        choice = None
        for position in FRACTIONS:
            value = lo[0]+position*(hi[0]-lo[0])
            row = inertia_candidate(model,value,f'refine{step}_fraction{position}')
            if row['valid_nonzero_leading_minors']:
                choice = (value,row)
                break
        if choice is None:
            raise ArithmeticError('All frozen refinement candidates had zero minors')
        if choice[1]['negative_inertia'] == 0:
            lo = choice
        else:
            hi = choice
        refinements.append(choice[1]['checkpoint_filename'])
    if hi[0]-lo[0] > TARGET_WIDTH:
        save_stage('UNRESOLVED_bracket.json',{'attempts':attempts,'refinements':refinements,'interval':interval(lo[0],hi[0])})
        raise ArithmeticError('Frozen refinements exhausted')
    checks = []
    add(checks,'ground_lower_count_zero',lo[1]['negative_inertia'] == 0)
    add(checks,'ground_upper_count_one',hi[1]['negative_inertia'] == 1)
    add(checks,'ground_bracket_target',0<hi[0]-lo[0]<=TARGET_WIDTH)
    row = {'matrix':'NEW_Halpha_ONLY','seed_not_certificate':seed,'center':exact(center),
           'interval':interval(lo[0],hi[0]),'lower_endpoint_evidence':lo[1],'upper_endpoint_evidence':hi[1],
           'expansion_attempts':attempts,'refinements':refinements,'checks':list(checks)}
    save_stage('new_source_ground_bracket.json',row)
    return row,lo[0],hi[0],checks


def format_report(result):
    def rat(x):
        return str(x['numerator'])+'/'+str(x['denominator'])
    lines = ['# Complete native dipole source: held q1 hexagon V001','',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             'Scientific status: '+result['finite_source_status']+'.','',
             '| quantity | exact lower | exact upper | lower Decimal20 | upper Decimal20 |',
             '|---|---:|---:|---:|---:|']
    for label,key in (('base E0','base_E0_interval'),('new Ealpha','new_Ealpha_interval'),('energy drop','energy_drop_interval'),('Falpha','Falpha_interval')):
        data = result[key]
        lines.append('| '+label+' | '+rat(data['lower'])+' | '+rat(data['upper'])+' | '
                     +data['lower']['decimal20_lower']+' | '+data['upper']['decimal20_upper']+' |')
    lines += ['','Native chi0 upper bound: '+rat(result['chi0_conservative_upper_bound'])+'.',
              'Strict chi0 positivity earned from finite drop: '+str(result['chi0_strictly_positive_qualitative_only'])+'.','',
              'The exact low-pair dipole block is zero. The response, if strict, uses higher states; no two-level enhancement from the loop splitting is substituted.','',
              'Falpha is an averaged finite-field curvature, not a numerical chi0 or a physical gravity/metric susceptibility. No numerical lower chi0 is inferred. Raw signed intervals remain untrimmed.','',
              'Base E0/Q bounds and all base artifacts are reused as sealed data: no base eigensolve/inertia replay. One new Halpha eigh supplies seeds only; integer Bareiss certifies the new ground interval.','',
              'Full q1 exterior collar and native half-edge source are owned. No source-dependent identity reset, bulk phase, active-copy matter pole, physical ruler, galaxy law, expansion or superiority claim follows.','']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs,base = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
                'authenticated_inputs':inputs,'alpha':exact(ALPHA),'h':exact(H),'w':[exact(x) for x in W],
                'environment':{key:os.environ.get(key) for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')},
                'base_eigensolve_replayed':False,'base_inertia_replayed':False,'ancestor_imported':False,
                'bracket_policy':{'seed_denominator':SEED_DENOMINATOR,'expansion_attempts':EXPANSION_ATTEMPTS,'refinement_steps':REFINEMENT_STEPS,
                                  'endpoint_offsets':list(OFFSETS),'interior_fractions':[exact(x) for x in FRACTIONS],'target_width':exact(TARGET_WIDTH)}}
    manifest_hash = save_stage('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    model,structure,structural_checks = source_model(base)
    save_stage('new_source_structure.json',structure)
    checks = list(structural_checks)
    controls,extra = algorithm_controls()
    checks.extend(extra)
    save_stage('bareiss_controls.json',controls)
    numeric = np.diag([float(x) for x in model['diagonal']])
    for n,m,value in model['edges']:
        numeric[n,m] = numeric[m,n] = float(value)
    eigenvalues,unused_vectors = np.linalg.eigh(numeric)
    seed = float(eigenvalues[0])
    seed_data = {'numpy_version':np.__version__,'new_Halpha_eigenvalues_seeds_only':[float(x) for x in eigenvalues],
                 'eigenvectors_used_for_physics':False,'base_eigensolve_replayed':False}
    save_stage('new_Halpha_numpy_seed_only.json',seed_data)
    bracket,la,ua,extra = ground_bracket(model,seed)
    checks.extend(extra)
    base_interval = base['eigenvalue_intervals']['E0']
    l0,u0 = fraction(base_interval['lower']),fraction(base_interval['upper'])
    mu = fraction(base['eigenvalue_intervals']['Qmin']['lower'])
    drop_lo,drop_hi = l0-ua,u0-la
    flo,fhi = 2*drop_lo/ALPHA**2,2*drop_hi/ALPHA**2
    strict,contradiction = drop_lo>0,drop_hi<0
    candidate_science = 'STRICT_FINITE_DROP_CERTIFIED_CHI0_POSITIVE' if strict else ('CONCAVITY_CONTRADICTION_PRESERVED' if contradiction else 'STRICT_DROP_UNRESOLVED_IN_RAW_INTERVAL')
    bound = 2*(3+3*H)**2/(mu-u0)
    add(checks,'base_Q_distance_positive',mu-u0>0)
    add(checks,'energy_drop_interval_order',drop_lo<drop_hi)
    add(checks,'Falpha_interval_order',flo<fhi)
    add(checks,'native_chi_upper_positive',bound>0)
    final_inputs,unused = authenticate()
    add(checks,'all_input_checkpoint_bytes_unchanged',final_inputs == inputs)
    add(checks,'source_protocol_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'stage_structural_check_list_unchanged',structure['checks'] == structural_checks)
    failed = sum(not x['passed'] for x in checks)
    science = candidate_science if not failed else 'ARITHMETIC_FAILED_SCIENCE_UNQUALIFIED'
    result = {'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'finite_source_status':science,'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
              'authenticated_inputs':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(CP_HASHES),
              'source_structure':structure,'bareiss_controls':controls,'new_Halpha_numpy_seed_only':seed_data,
              'new_ground_bracket':bracket,'base_E0_interval':base_interval,'base_Q_floor_lower':exact(mu),
              'new_Ealpha_interval':interval(la,ua),'energy_drop_interval':interval(drop_lo,drop_hi),'Falpha_interval':interval(flo,fhi),
              'chi0_conservative_upper_bound':exact(bound),'raw_strict_drop_candidate':strict,
              'raw_scientific_status_candidate':candidate_science,
              'chi0_strictly_positive_qualitative_only':strict and failed == 0,
              'numerical_chi0_lower_inferred_from_Falpha':False,'Falpha_is_chi0':False,
              'low_pair_dipole_block':'EXACT_ZERO_BY_C6_SELECTION',
              'uniform_source_interval_L_half_and_two':{str(lapse):interval(lapse*la,lapse*ua) for lapse in (Fraction(1,2),Fraction(2))},
              'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'concavity_contradiction':contradiction,'base_eigensolve_replayed':False,'base_inertia_replayed':False,
              'bulk_phase_metric_gravity_galaxy_expansion_claim':False,'elapsed_seconds':time.perf_counter()-T0,
              'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = format_report(result)
    table = report.split('| quantity |',1)[1].split('Native chi0 upper bound:',1)[0]
    if table.count('\n| ') != 4:
        raise RuntimeError('Report must contain exactly4 interval DATA rows')
    raw_hash = exclusive(RESULT,result)
    with REPORT.open('x',encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete',raw_sha256=raw_hash,report_sha256=report_hash,checks_passed=result['checks_passed'],checks_total=result['checks_total'])
    receipt = {'schema':NAME+'_RECEIPT','pid':os.getpid(),'result_raw_sha256':raw_hash,
               'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':report_hash,
               'manifest_sha256':manifest_hash,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'checkpoint_sha256':dict(CP_HASHES),
               'source_sha256':source_hash,'protocol_sha256':protocol_hash,'authenticated_inputs':inputs,
               'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],'checks_failed':failed,
               'finite_source_status':science,'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'finite_source_status':science,
                      'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
                      'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}))
    return 0 if not failed and not contradiction else 2


if __name__ == '__main__':
    T0 = time.perf_counter()
    try:
        sys.exit(main())
    except Exception as error:
        if ATTEMPT_CREATED:
            data = {'pid':os.getpid(),'exception_type':type(error).__name__,'error':str(error),
                    'traceback':traceback.format_exc(),'elapsed_seconds':time.perf_counter()-T0}
            path = CP/'ERROR.json'
            if not path.exists():
                digest = exclusive(path,data)
                event('error',filename=path.name,sha256=digest)
        traceback.print_exc()
        sys.exit(3)
