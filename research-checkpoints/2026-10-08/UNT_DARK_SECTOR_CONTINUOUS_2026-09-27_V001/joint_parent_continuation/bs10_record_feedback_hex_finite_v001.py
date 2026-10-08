#!/usr/bin/env python3
"""Frozen held-cell finite certificate. NumPy only supplies bracket seeds."""
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
J = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
RESULT = J / (NAME + '_RESULT.json')
REPORT = J / (NAME + '_RESULT.md')
RECEIPT = J / (NAME + '_RECEIPT.json')
CP = J / 'bs10_record_feedback_hex_finite_v001_checkpoints'
H = Fraction(1, 5)
P = (21, 42)
SEED_DENOMINATOR = 10**12
EXPANSION_ATTEMPTS = 24
REFINEMENT_STEPS = 32
ENDPOINT_OFFSETS = (0, 1, -1, 2, -2)
INTERIOR_FRACTIONS = (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(2, 5), Fraction(3, 5))
TARGET_WIDTH = Fraction(1, 10**11)
ATTEMPT_CREATED = False
INERTIA_SERIAL = 0
CP_HASHES = {}
INPUTS = {
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/DEGREE_TWO_JOINT_MATTER_REFERENCE_GATE_V001.md': '84e889f6148b43c91c2ef1a0e3194a8723e190bcf5f9a16407013e85b6a02a83',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/recovered_sources/BS_MICRO_ACTION.md': '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
    'program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/THEOREM.md': 'f75edcb115c3f7c86c6598f4597366b36e363df2d03ad919cc607b57dfb6b20c',
    'program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/verify_sixth_order_hamiltonian.py': '6cd1c8533821012e3281310ec0dadc95f8788ecf74729ba912f56d46f5a9b271',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/RECORD_FEEDBACK_LOOP_BACKGROUND_ORDERS_V001.md': '7800587a83941d3c3380af211ba16be584c29f36f26e4c78c5b362c347e1abc9',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001.md': '14a5b2d44887920b7bab1bd32cbc98d1d2395b3f7110a6faed0036037b16fd78',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_record_feedback_hex_ring_v001.py': 'd9f406d945e8e5350c7d397191d7a26bef1aafabeaaab0f50cf06db87c0b2d62',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json': '986554b4c2315f214fef98436f285997d6c37a0884ffa1647a5a513b261fbd8f',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RECEIPT.json': '265692857646e2e271b16ed3e91be60baaab818b6a890e3d3ca41832ffd90fa1',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_record_feedback_diagonal_sixth_v001.py': 'b4ec2a9dede18d6a0d2e286da7a5a1ea35a73f3f60bcd5d89aac43f06407e89f',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001.md': 'b95c3f22a0693985ded173d1a0986bf02a92938b723b8ff7cd8e3af460621911',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001_RESULT.json': '386cad65ddd80cc01ffd5c49ac9b56827c6fd7c25450772f630c5412e7f51c11',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001_RECEIPT.json': '4c49ad2737a5b818d593d1b27c5eb56114647c4d2b6d407289cec649dfe181ba',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def exact(x):
    x = Fraction(x)
    out = {'numerator': x.numerator, 'denominator': x.denominator}
    bounds = []
    for mode in (ROUND_FLOOR, ROUND_CEILING):
        with localcontext() as context:
            context.prec, context.rounding = 20, mode
            bounds.append(str(Decimal(x.numerator)/Decimal(x.denominator)))
    out['decimal20_lower'], out['decimal20_upper'] = bounds
    return out


def fraction(x):
    return Fraction(x['numerator'], x['denominator'])


def interval(lo, hi):
    return {'lower': exact(lo), 'upper': exact(hi), 'width': exact(hi-lo)}


def exclusive(path, obj):
    with path.open('xb') as stream:
        stream.write(canonical(obj)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def event(kind, **fields):
    row = {'event': kind, 'pid': os.getpid(), 'elapsed_seconds': time.perf_counter()-T0, **fields}
    with (CP/'journal.jsonl').open('ab') as stream:
        stream.write(canonical(row)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def save_stage(name, obj, **fields):
    path = CP/name
    digest = exclusive(path, obj)
    CP_HASHES[name] = digest
    event('stage_complete', filename=name, sha256=digest, **fields)
    return digest


def add(checks, name, condition):
    checks.append({'label': name, 'passed': bool(condition)})


def authenticate():
    observed = {}
    for rel, wanted in INPUTS.items():
        got = sha(ROOT/rel)
        if got != wanted:
            raise RuntimeError('Frozen input mismatch: '+rel)
        observed[rel] = got
    for stem, source in (('BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001', 'bs10_record_feedback_diagonal_sixth_v001.py'),
                         ('BS10_RECORD_FEEDBACK_HEX_RING_V001', 'bs10_record_feedback_hex_ring_v001.py')):
        data = json.loads((J/(stem+'_RESULT.json')).read_text())
        receipt = json.loads((J/(stem+'_RECEIPT.json')).read_text())
        if receipt['result_raw_sha256'] != sha(J/(stem+'_RESULT.json')):
            raise RuntimeError('Ancestor raw receipt mismatch: '+stem)
        if receipt['result_canonical_sha256'] != hashlib.sha256(canonical(data)).hexdigest():
            raise RuntimeError('Ancestor canonical receipt mismatch: '+stem)
        for key, name in (('source_sha256', source), ('protocol_sha256', stem+'.md')):
            if data[key] != sha(J/name) or receipt[key] != data[key]:
                raise RuntimeError('Ancestor source/protocol mismatch: '+stem)
        if data['input_sha256'] != receipt['input_sha256']:
            raise RuntimeError('Ancestor input-map mismatch: '+stem)
        for rel, digest in data['input_sha256'].items():
            if observed.get(rel) != digest:
                raise RuntimeError('Ancestor input byte mismatch: '+rel)
    return observed


def diagonal(n):
    return sum((Fraction((((n>>((v-1)%6))&1)+((n>>v)&1)-1)**2)
                +Fraction(1-((n>>((v-1)%6))&1)-((n>>v)&1), 2) for v in range(6)), Fraction(0))


def diagonal_gap(n):
    flipped = n^P[0]
    delta = [0]*6
    for e in range(6):
        if flipped & (1<<e):
            sign = 1-2*((P[0]>>e)&1)
            delta[e] += sign
            delta[(e+1)%6] += sign
    return sum((Fraction(x*x)-Fraction(x, 2) for x in delta), Fraction(0))


def model():
    d = [diagonal(n) for n in range(64)]
    labels = {'H': list(range(64)), 'Q': [n for n in range(64) if n not in P]}
    model_data = {}
    for name, basis in labels.items():
        lookup = {n:i for i,n in enumerate(basis)}
        edges = [(lookup[n], lookup[n^(1<<e)]) for n in basis for e in range(6)
                 if n^(1<<e) in lookup and lookup[n] < lookup[n^(1<<e)]]
        model_data[name] = {'basis': basis, 'diagonal': [d[n] for n in basis], 'edges': edges}
    return d, model_data


def integer_shifted(data, shift):
    factor = math.lcm(H.denominator, shift.denominator, *(x.denominator for x in data['diagonal']))
    dimension = len(data['basis'])
    matrix = [[0]*dimension for _ in range(dimension)]
    for i, value in enumerate(data['diagonal']):
        matrix[i][i] = int(factor*(value-shift))
    for i,j in data['edges']:
        matrix[i][j] = matrix[j][i] = int(-factor*H)
    return matrix, factor


class ZeroMinor(Exception):
    def __init__(self, index, minors):
        self.index, self.minors = index, minors
        super().__init__('Zero leading minor at order '+str(index))


def bareiss_leading(matrix):
    a = [row[:] for row in matrix]
    size, previous, minors, divisions = len(a), 1, [], 0
    for k in range(size-1):
        pivot = a[k][k]
        minors.append(pivot)
        if pivot == 0:
            raise ZeroMinor(k+1, minors)
        for i in range(k+1, size):
            for j in range(i, size):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                value, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError('Nonexact Bareiss division')
                a[i][j] = a[j][i] = value
                divisions += 1
        for i in range(k+1, size):
            a[i][k] = a[k][i] = 0
        previous = pivot
    final = a[-1][-1]
    minors.append(final)
    if final == 0:
        raise ZeroMinor(size, minors)
    signs = [1]+[1 if x>0 else -1 for x in minors]
    inertia = sum(a != b for a,b in zip(signs, signs[1:]))
    return minors, inertia, divisions


def determinant_permutations(matrix):
    size, total = len(matrix), 0
    for order in permutations(range(size)):
        inversions = sum(order[i]>order[j] for i in range(size) for j in range(i+1,size))
        term = (-1)**inversions
        for i,j in enumerate(order):
            term *= matrix[i][j]
        total += term
    return total


def bareiss_controls():
    checks, rows = [], []
    controls = ([[2,1],[1,-1]], [[0,1],[1,2]], [[2,1,0],[1,3,1],[0,1,-1]])
    for index, matrix in enumerate(controls):
        direct = [determinant_permutations([row[:n] for row in matrix[:n]]) for n in range(1,len(matrix)+1)]
        try:
            minors, negative, divisions = bareiss_leading(matrix)
            add(checks, f'control{index}_leading_minors', minors == direct)
            add(checks, f'control{index}_negative_inertia', negative == 1)
            rows.append({'matrix':matrix, 'direct_minors':direct, 'bareiss_minors':minors,
                         'negative_inertia':negative, 'exact_divisions':divisions})
        except ZeroMinor as error:
            add(checks, f'control{index}_zero_rejected', index == 1 and error.index == 1 and direct[0] == 0)
            rows.append({'matrix':matrix, 'direct_minors':direct, 'rejected_zero_minor_order':error.index})
    return {'rows':rows, 'checks':checks}, checks


def formal_control(d):
    amplitudes = [[Fraction(0)]*64 for _ in range(7)]
    energies = [Fraction(0)]*7
    amplitudes[0][P[0]] = Fraction(1)
    qbasis = [n for n in range(64) if n not in P]
    for r in range(1,7):
        energies[r] = -sum((amplitudes[r-1][P[0]^(1<<e)] for e in range(6)), Fraction(0))
        for n in qbasis:
            first = sum((amplitudes[r-1][n^(1<<e)] for e in range(6)), Fraction(0))
            folded = sum((energies[k]*amplitudes[r-k][n] for k in range(1,r+1)), Fraction(0))
            amplitudes[r][n] = (first+folded)/d[n]
    old = json.loads((J/'BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001_RESULT.json').read_text())
    rows = {r['class']:r for r in old['rows'] if r['q'] == 1}
    weights = {'single_add':3, 'single_remove':3, 'pair_add_remove':6,
               'path_add_remove_add':3, 'path_remove_add_remove':3}
    assembled = {r:sum((count*fraction(rows[name]['connected_weights'][str(r)]) for name,count in weights.items()), Fraction(0))
                 for r in (2,4,6)}
    checks = []
    targets = {2:Fraction(-4), 4:Fraction(4,9), 6:Fraction(-80,9)}
    for r,target in targets.items():
        add(checks, f'formal_order{r}_independent_methods', energies[r] == assembled[r] == target)
    for r in (1,3,5):
        add(checks, f'formal_odd_order{r}', energies[r] == 0)
    hex_data = json.loads((J/'BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json').read_text())
    row = next(r for r in hex_data['rows'] if r['qmask'] == 63)
    j = fraction(row['J6'])
    add(checks, 'sealed_hex_J6', j == Fraction(2504,1265625))
    return {'recurrence_coefficients': [exact(x) for x in energies],
            'linked_assembly': {str(r):exact(x) for r,x in assembled.items()},
            'formal_diagonal_at_h': exact(sum((energies[r]*H**r for r in (2,4,6)), Fraction(0))),
            'formal_J6_at_h': exact(j), 'checks':checks}, checks


def inertia_candidate(data, name, shift, purpose):
    global INERTIA_SERIAL
    started = time.perf_counter()
    matrix, scale = integer_shifted(data, shift)
    serial = INERTIA_SERIAL
    INERTIA_SERIAL += 1
    row = {'matrix':name, 'dimension':len(data['basis']), 'shift':exact(shift),
           'positive_integer_scale':scale, 'purpose':purpose, 'serial':serial}
    try:
        minors, negative, divisions = bareiss_leading(matrix)
        row.update({'valid_nonzero_leading_minors':True, 'leading_principal_minors_scaled_integer':minors,
                    'negative_inertia':negative, 'exact_divisions':divisions})
    except ZeroMinor as error:
        row.update({'valid_nonzero_leading_minors':False, 'rejected_zero_minor_order':error.index,
                    'leading_principal_minors_scaled_integer':error.minors, 'negative_inertia':None})
    row['elapsed_seconds'] = time.perf_counter()-started
    filename = f'inertia_{serial:04d}.json'
    save_stage(filename, row, matrix=name, purpose=purpose, valid=row['valid_nonzero_leading_minors'])
    row['checkpoint_filename'] = filename
    return row


def bracket(data, name, index, seed):
    center = Fraction(math.floor(seed*SEED_DENOMINATOR), SEED_DENOMINATOR)
    attempts, low, high = [], None, None
    for j in range(EXPANSION_ATTEMPTS):
        radius = Fraction(2**j, SEED_DENOMINATOR)
        endpoints = []
        for side, base in (('lower', center-radius), ('upper', center+radius)):
            candidate = None
            for offset in ENDPOINT_OFFSETS:
                value = base+Fraction(offset,17*SEED_DENOMINATOR)
                row = inertia_candidate(data, name, value, f'eigen{index}_expand{j}_{side}_offset{offset}')
                if row['valid_nonzero_leading_minors']:
                    candidate = (value,row)
                    break
            endpoints.append(candidate)
        attempts.append({'attempt':j, 'radius':exact(radius),
                         'lower_checkpoint':None if endpoints[0] is None else endpoints[0][1]['checkpoint_filename'],
                         'upper_checkpoint':None if endpoints[1] is None else endpoints[1][1]['checkpoint_filename']})
        if all(x is not None for x in endpoints):
            if endpoints[0][1]['negative_inertia'] == index and endpoints[1][1]['negative_inertia'] == index+1:
                low, high = endpoints
                break
    if low is None:
        save_stage(f'{name}_eigen{index}_UNRESOLVED.json', {'center':exact(center), 'attempts':attempts})
        raise ArithmeticError('Frozen attempts exhausted without certified bracket: '+name+str(index))
    refinements = []
    for step in range(REFINEMENT_STEPS):
        if high[0]-low[0] <= TARGET_WIDTH:
            break
        choice = None
        for position in INTERIOR_FRACTIONS:
            value = low[0]+position*(high[0]-low[0])
            row = inertia_candidate(data, name, value, f'eigen{index}_refine{step}_fraction{position}')
            if row['valid_nonzero_leading_minors']:
                choice = (value,row)
                break
        if choice is None:
            raise ArithmeticError('All frozen refinement candidates had zero minors')
        count = choice[1]['negative_inertia']
        if count <= index:
            low = choice
        else:
            high = choice
        refinements.append(choice[1]['checkpoint_filename'])
    if high[0]-low[0] > TARGET_WIDTH:
        save_stage(f'{name}_eigen{index}_UNRESOLVED.json', {'attempts':attempts, 'refinements':refinements,
                                                        'interval':interval(low[0],high[0])})
        raise ArithmeticError('Frozen refinements exhausted before target width')
    checks = []
    add(checks, 'lower_count', low[1]['negative_inertia'] == index)
    add(checks, 'upper_count', high[1]['negative_inertia'] == index+1)
    add(checks, 'strict_positive_width', low[0] < high[0])
    add(checks, 'frozen_target_width', high[0]-low[0] <= TARGET_WIDTH)
    row = {'matrix':name, 'eigenvalue_zero_based_index':index, 'numpy_seed_not_certificate':seed,
           'center':exact(center), 'interval':interval(low[0],high[0]),
           'lower_endpoint_evidence':low[1], 'upper_endpoint_evidence':high[1],
           'expansion_attempts':attempts, 'refinement_checkpoints':refinements, 'checks':checks}
    save_stage(f'{name}_eigen{index}_bracket.json', row)
    return row, low[0], high[0], checks


def structural(d, models):
    checks = []
    add(checks, 'full64_Q62', len(models['H']['basis']) == 64 and len(models['Q']['basis']) == 62)
    add(checks, 'only_alternating_zero_diagonals', tuple(n for n,x in enumerate(d) if x == 0) == P)
    add(checks, 'Q_zero_coupling_floor_one', min(models['Q']['diagonal']) == 1)
    add(checks, 'six_cube_neighbors', len(models['H']['edges']) == 192)
    for n in range(64):
        add(checks, f'diagonal_gap_{n}', d[n] == diagonal_gap(n))
        add(checks, f'integer_diagonal_{n}', d[n].denominator == 1)
    neighbors = [{p^(1<<e) for e in range(6)} for p in P]
    add(checks, 'P_neighbors_allQ', all(n not in P for ns in neighbors for n in ns))
    add(checks, 'W_row_six_norm', all(len(ns) == 6 for ns in neighbors))
    add(checks, 'W_rows_disjoint', not(neighbors[0] & neighbors[1]))
    add(checks, 'WWdagger_exact_6h2', H**2*len(neighbors[0]) == 6*H**2)
    for lapse in (Fraction(1,2),Fraction(2)):
        for n in range(64):
            scaled_direct = lapse*diagonal(n)
            scaled_gap = lapse*diagonal_gap(n)
            add(checks, f'uniform_L{lapse}_diagonal{n}', scaled_direct == scaled_gap == lapse*d[n])
        add(checks, f'uniform_L{lapse}_whole_flip', -lapse*H == lapse*(-H))
    return {'physical_n_diagonal': [exact(x) for x in d], 'P_words':list(P),
            'Q_words':models['Q']['basis'], 'H_edges':models['H']['edges'],
            'Q_edges':models['Q']['edges'], 'WWdagger_scalar':exact(6*H**2), 'checks':checks}, checks


def numpy_seeds(models):
    seeds, diagnostics = {}, {}
    for name in ('H','Q'):
        data = models[name]
        matrix = np.diag([float(x) for x in data['diagonal']])
        for i,j in data['edges']:
            matrix[i,j] = matrix[j,i] = -float(H)
        eigenvalues, ignored_vectors = np.linalg.eigh(matrix)
        seeds[name] = [float(x) for x in eigenvalues]
        diagnostics[name] = {'dimension':len(data['basis']), 'eigh_eigenvalues_seeds_only':seeds[name]}
    return seeds, {'numpy_version':np.__version__, 'seeds':diagnostics,
                   'eigenvectors_used_for_physics':False, 'certificate_comes_from_numpy':False}


def format_report(result):
    def rat(x):
        return str(x['numerator'])+'/'+str(x['denominator'])
    lines = ['# Held occupied-record hexagon finite certificate V001','',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             f"Held-cell scientific certificate: {result['held_cell_certificate_status']}.",'',
             'All64 internal words retained; Q62 is an exact principal compression. Fixed exterior identity remains owned; these are reference-relative intervals.','',
             '| level | exact lower | exact upper | lower Decimal20 | upper Decimal20 |',
             '|---|---:|---:|---:|---:|']
    for name in ('E0','E1','Qmin'):
        data = result['eigenvalue_intervals'][name]
        lines.append('| '+name+' | '+rat(data['lower'])+' | '+rat(data['upper'])+' | '
                     +data['lower']['decimal20_lower']+' | '+data['upper']['decimal20_upper']+' |')
    for name in ('finite_half_splitting','finite_midpoint','half_splitting_minus_formal','half_splitting_over_formal','midpoint_minus_formal_diagonal'):
        data = result[name]
        lines += ['',name+': ['+rat(data['lower'])+', '+rat(data['upper'])+'].']
    lines += ['','Formal held diagonal: '+rat(result['formal_controls']['formal_diagonal_at_h'])
              +'; formal J6: '+rat(result['formal_controls']['formal_J6_at_h'])+'.','']
    if result['bare_P_projection_weight_lower'] is not None:
        lines += ['Bare alternating-word P projection lower bounds: E0 '
                  +rat(result['bare_P_projection_weight_lower']['E0'])+', E1 '
                  +rat(result['bare_P_projection_weight_lower']['E1'])+'.','']
    lines += ['NumPy supplies seeds only. Rational endpoint inertia uses exact no-pivot Bareiss leading minors; rejected zero minors and partial checkpoints are preserved.','',
              'A positive Q floor certifies a continuous isolated negative pair for0<h<=1/5 under this held collar, and lambda3 at the endpoint is at least the saved Q lower bound. Bare P weight is not physical matter residue.','',
              'No bulk phase, all-volume linked-cluster remainder, Nc1 active-copy pole, physical clock/ruler, gravity or cosmic evolution claim follows. Signed finite/formal differences are retained without a favorable accuracy threshold.','']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(), 'source_sha256':source_hash,
                'protocol_sha256':protocol_hash,'input_sha256':inputs,'h':exact(H),
                'environment':{key:os.environ.get(key) for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')},
                'bracket_policy':{'seed_denominator':SEED_DENOMINATOR,'expansion_attempts':EXPANSION_ATTEMPTS,
                                  'refinement_steps':REFINEMENT_STEPS,'endpoint_offsets':list(ENDPOINT_OFFSETS),
                                  'interior_fractions':[exact(x) for x in INTERIOR_FRACTIONS],'target_width':exact(TARGET_WIDTH)},
                'absolute_exterior_identity':'OWNED_FIXED_SCALAR_NOT_NUMERICALLY_SPECIFIED',
                'old_sources_imported':False}
    manifest_hash = save_stage('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    d,models = model()
    structures,checks = structural(d,models)
    save_stage('structure.json',structures)
    controls,newchecks = bareiss_controls()
    checks += newchecks
    save_stage('bareiss_controls.json',controls)
    formal,newchecks = formal_control(d)
    checks += newchecks
    save_stage('formal_controls.json',formal)
    seeds,seed_data = numpy_seeds(models)
    save_stage('numpy_seeds_only.json',seed_data)
    brackets,limits = {},{}
    for label,name,index in (('E0','H',0),('E1','H',1),('Qmin','Q',0)):
        data,lo,hi,newchecks = bracket(models[name],name,index,seeds[name][index])
        brackets[label],limits[label] = data,(lo,hi)
        checks += newchecks
    lo0,hi0 = limits['E0']
    lo1,hi1 = limits['E1']
    mu,muupper = limits['Qmin']
    jlo,jhi = (lo1-hi0)/2,(hi1-lo0)/2
    mlo,mhi = (lo0+lo1)/2,(hi0+hi1)/2
    jformal = fraction(formal['formal_J6_at_h'])
    mformal = fraction(formal['formal_diagonal_at_h'])
    science = {'Q_floor_positive':mu>0,'both_low_upper_negative':hi0<0 and hi1<0,
               'finite_split_strictly_positive':jlo>0}
    weights = None
    if science['Q_floor_positive'] and science['both_low_upper_negative']:
        weights = {}
        for label,upper in (('E0',hi0),('E1',hi1)):
            distance = mu-upper
            weight = distance**2/(distance**2+6*H**2)
            weights[label] = exact(weight)
            add(checks,label+'_valid_P_lower',0<weight<1)
    for label,(lo,hi) in limits.items():
        add(checks,label+'_interval_order',lo<hi)
    add(checks,'finite_splitting_interval_order',jlo<jhi)
    add(checks,'finite_midpoint_interval_order',mlo<mhi)
    add(checks,'final_input_bytes_unchanged',authenticate()==inputs)
    add(checks,'source_protocol_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    failed = sum(not x['passed'] for x in checks)
    result = {'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'held_cell_certificate_status':'ISOLATED_PAIR_CERTIFIED' if all(science.values()) and not failed else 'FAILED_OR_UNRESOLVED_PRESERVED',
              'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,'input_sha256':inputs,
              'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(CP_HASHES),'structural_checks':structures,
              'formal_controls':formal,'numpy_seeds_only':seed_data,'brackets':brackets,
              'eigenvalue_intervals':{label:interval(*bounds) for label,bounds in limits.items()},
              'finite_half_splitting':interval(jlo,jhi),'finite_midpoint':interval(mlo,mhi),
              'half_splitting_minus_formal':interval(jlo-jformal,jhi-jformal),
              'half_splitting_over_formal':interval(jlo/jformal,jhi/jformal),
              'midpoint_minus_formal_diagonal':interval(mlo-mformal,mhi-mformal),
              'science_gates':science,'bare_P_projection_weight_lower':weights,
              'common_pair_P_projection_weight_lower':None if weights is None else weights['E1'],
              'continuous_interval_Q_floor':exact(min(1,mu)) if mu>0 else None,
              'lambda3_endpoint_lower':exact(mu),'uniform_source_only':True,
              'source_intervals_L_half_and_two':{str(lapse):{label:interval(lapse*lo,lapse*hi) for label,(lo,hi) in limits.items()}
                                                for lapse in (Fraction(1,2),Fraction(2))},
              'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'bulk_phase_or_remainder_claim':False,'matter_clock_ruler_gravity_expansion_claim':False,
              'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = format_report(result)
    table = report.split('| level |',1)[1].split('finite_half_splitting:',1)[0]
    if table.count('\n| ') != 3:
        raise RuntimeError('Report must contain exactly3 interval DATA rows')
    raw_hash = exclusive(RESULT,result)
    with REPORT.open('x',encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete',raw_sha256=raw_hash,report_sha256=report_hash,checks_passed=result['checks_passed'],checks_total=result['checks_total'])
    receipt = {'schema':NAME+'_RECEIPT','pid':os.getpid(),'result_raw_sha256':raw_hash,
               'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':report_hash,
               'manifest_sha256':manifest_hash,'journal_prefix_sha256':sha(CP/'journal.jsonl'),
               'checkpoint_sha256':dict(CP_HASHES),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
               'input_sha256':inputs,'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
               'checks_failed':failed,'held_cell_certificate_status':result['held_cell_certificate_status'],
               'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'held_cell_certificate_status':result['held_cell_certificate_status'],
                      'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
                      'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}))
    return 0 if not failed and all(science.values()) else 2


if __name__ == '__main__':
    T0 = time.perf_counter()
    try:
        sys.exit(main())
    except Exception as error:
        if ATTEMPT_CREATED:
            payload = {'pid':os.getpid(),'exception_type':type(error).__name__,'error':str(error),
                       'traceback':traceback.format_exc(),'elapsed_seconds':time.perf_counter()-T0}
            path = CP/'ERROR.json'
            if not path.exists():
                digest = exclusive(path,payload)
                event('error',filename=path.name,sha256=digest)
        traceback.print_exc()
        sys.exit(3)
