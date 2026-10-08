#!/usr/bin/env python3
"""Prospective all-record held vacuum certificate; no ancestor is imported."""
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
NAME = 'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J/(NAME+'.md')
RESULT = J/(NAME+'_RESULT.json')
REPORT = J/(NAME+'_RESULT.md')
RECEIPT = J/(NAME+'_RECEIPT.json')
CP = J/'bs10_record_feedback_hex_vacuum_v001_checkpoints'
BASE = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
BASE_CP = J/'bs10_record_feedback_hex_finite_v001_checkpoints'
H = Fraction(1,5)
P = (21,42)
S = 10**12
OFFSETS = (0,1,-1,2,-2)
POSITIONS = (Fraction(1,2),Fraction(1,3),Fraction(2,3),Fraction(2,5),Fraction(3,5))
TARGET = Fraction(1,10**11)
ATTEMPT_CREATED = False
SERIAL = 0
STAGES = {}
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
    displays = []
    for mode in (ROUND_FLOOR,ROUND_CEILING):
        with localcontext() as context:
            context.prec,context.rounding = 20,mode
            displays.append(str(Decimal(x.numerator)/Decimal(x.denominator)))
    return {'numerator':x.numerator,'denominator':x.denominator,
            'decimal20_lower':displays[0],'decimal20_upper':displays[1]}


def frac(x):
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


def save(name,obj,**fields):
    digest = exclusive(CP/name,obj)
    STAGES[name] = digest
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
    base = json.loads((J/(BASE+'_RESULT.json')).read_text())
    receipt = json.loads((J/(BASE+'_RECEIPT.json')).read_text())
    if receipt['result_raw_sha256'] != direct[BASE+'_RESULT.json']:
        raise RuntimeError('Base raw receipt mismatch')
    if receipt['result_canonical_sha256'] != hashlib.sha256(canonical(base)).hexdigest():
        raise RuntimeError('Base canonical receipt mismatch')
    report_hash = sha(J/(BASE+'_RESULT.md'))
    if report_hash != receipt['report_sha256']:
        raise RuntimeError('Base report receipt mismatch')
    for key,name in (('source_sha256','bs10_record_feedback_hex_finite_v001.py'),
                     ('protocol_sha256',BASE+'.md')):
        if base[key] != direct[name] or receipt[key] != direct[name]:
            raise RuntimeError('Base source/protocol mismatch')
    if base['input_sha256'] != receipt['input_sha256'] or base['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Base input/checkpoint map mismatch')
    inherited,checkpoints = {},{}
    for rel,wanted in receipt['input_sha256'].items():
        got = sha(ROOT/rel)
        if got != wanted:
            raise RuntimeError('Inherited input changed: '+rel)
        inherited[rel] = got
    for name,wanted in receipt['checkpoint_sha256'].items():
        got = sha(BASE_CP/name)
        if got != wanted:
            raise RuntimeError('Base checkpoint changed: '+name)
        checkpoints[name] = got
    lines = (BASE_CP/'journal.jsonl').read_bytes().splitlines(keepends=True)
    entries = [json.loads(line) for line in lines]
    if entries[-1]['event'] != 'receipt_complete' or entries[-1]['receipt_sha256'] != direct[BASE+'_RECEIPT.json']:
        raise RuntimeError('Base final receipt event mismatch')
    if hashlib.sha256(b''.join(lines[:-1])).hexdigest() != receipt['journal_prefix_sha256']:
        raise RuntimeError('Base journal prefix mismatch')
    starts = [x for x in entries if x['event'] == 'started']
    if len(starts) != 1 or not(starts[0]['manifest_sha256'] == base['manifest_sha256']
                             == receipt['manifest_sha256'] == checkpoints['input_manifest.json']):
        raise RuntimeError('Base manifest/start seal mismatch')
    structure = json.loads((BASE_CP/'structure.json').read_text())
    prefix,alias = structure['checks'],base['structural_checks']['checks']
    if prefix != alias[:len(prefix)]:
        raise RuntimeError('Preserved base stage/check alias mismatch')
    for key in ('physical_n_diagonal','P_words','Q_words','H_edges','Q_edges','WWdagger_scalar'):
        if structure[key] != base['structural_checks'][key]:
            raise RuntimeError('Base structural data mismatch: '+key)
    if base['checks_failed'] != 0 or base['held_cell_certificate_status'] != 'ISOLATED_PAIR_CERTIFIED':
        raise RuntimeError('Base q63 ground premise unqualified')
    return {'direct_input_sha256':direct,'inherited_input_sha256':inherited,
            'base_checkpoint_sha256':checkpoints,'base_report_sha256':report_hash,
            'base_journal_prefix_sha256':receipt['journal_prefix_sha256'],
            'preserved_base_stage_alias':{'prefix_count':len(prefix),'nested_count':len(alias),'prefix_equal':True}},base


def permute(word,mapping):
    return sum(((word>>v)&1)<<mapping[v] for v in range(6))


def group():
    out = []
    for r in range(6):
        out.append({'name':f'rotation{r}','vertex_map':[(v+r)%6 for v in range(6)],
                    'edge_map':[(e+r)%6 for e in range(6)]})
    for r in range(6):
        out.append({'name':f'reflection{r}','vertex_map':[(r-v)%6 for v in range(6)],
                    'edge_map':[(r-e-1)%6 for e in range(6)]})
    return out


def diagonal(q,n):
    total = Fraction(0)
    for v in range(6):
        delta = ((n>>((v-1)%6))&1)+((n>>v)&1)-1
        total += delta*delta-Fraction(((q>>v)&1)*delta,2)
    return total


def physical_diagonal(q,n):
    total = Fraction(0)
    for v in range(6):
        degree = 1+((n>>((v-1)%6))&1)+((n>>v)&1)
        total += (degree-2)**2+((q>>v)&1)*(1-Fraction(degree,2))
    return total


def symmetry_and_physics(base):
    checks,mappings = [],[]
    transformations = group()
    diagonals = {q:[diagonal(q,n) for n in range(64)] for q in range(64)}
    for q in range(64):
        candidates = [(permute(q,g['vertex_map']),i,g) for i,g in enumerate(transformations)]
        rep,index,g = min(candidates,key=lambda x:(x[0],x[1]))
        basis_map = [permute(n,g['edge_map']) for n in range(64)]
        rowchecks = []
        add(rowchecks,'basis_bijection',sorted(basis_map) == list(range(64)))
        for n in range(64):
            add(rowchecks,f'n{n}_complete_storage_feedback',diagonals[q][n] == physical_diagonal(q,n))
            add(rowchecks,f'n{n}_exact_similarity_diagonal',diagonals[q][n] == diagonals[rep][basis_map[n]])
            for e in range(6):
                add(rowchecks,f'n{n}_edge{e}_exact_similarity_flip',
                    basis_map[n^(1<<e)] == (basis_map[n]^(1<<g['edge_map'][e])))
        add(rowchecks,'only_two_reference_zeros',tuple(n for n,x in enumerate(diagonals[q]) if x == 0) == P)
        add(rowchecks,'Q_diagonal_floor_at_least_one',min(x for n,x in enumerate(diagonals[q]) if n not in P) >= 1)
        leading = {}
        for p in P:
            coefficient = -sum((1/diagonals[q][p^(1<<e)] for e in range(6)),Fraction(0))
            leading[str(p)] = exact(coefficient)
            add(rowchecks,f'P{p}_leading_chord_bound',coefficient >= -3-Fraction(q.bit_count(),6))
            if q == 63:
                add(rowchecks,f'P{p}_q63_leading_control',coefficient == -4)
        row = {'qword':q,'q_bits_vertex_order':[int(bool(q&(1<<v))) for v in range(6)],
               'canonical_representative':rep,'transformation_index':index,'transformation':g,
               'incidence_basis_permutation':basis_map,'leading_E2_controls':leading,'checks':list(rowchecks)}
        mappings.append(row)
        checks.extend(rowchecks)
    representatives = sorted({row['canonical_representative'] for row in mappings})
    fixed = [sum(permute(q,g['vertex_map']) == q for q in range(64)) for g in transformations]
    add(checks,'Burnside_rotation_fixed84',sum(fixed[:6]) == 84)
    add(checks,'Burnside_reflection_fixed72',sum(fixed[6:]) == 72)
    add(checks,'Burnside_thirteen_classes',sum(fixed) == 12*13 and len(representatives) == 13)
    add(checks,'q63_base_diagonal_equal',diagonals[63] == [frac(x) for x in base['structural_checks']['physical_n_diagonal']])
    orbits = {str(rep):[row['qword'] for row in mappings if row['canonical_representative'] == rep] for rep in representatives}
    add(checks,'all64_words_once',sorted(q for orbit in orbits.values() for q in orbit) == list(range(64)))
    stage = {'group':transformations,'fixed_word_counts':fixed,'representatives':representatives,
             'orbits':orbits,'all64_mappings':mappings,
             'all64_physical_diagonals':{str(q):[exact(x) for x in d] for q,d in diagonals.items()},
             'record_complement_used':False,'checks':list(checks)}
    return stage,diagonals,representatives,mappings,checks


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
    return minors,sum(x!=y for x,y in zip(signs,signs[1:])),divisions


def determinant(matrix):
    out = 0
    for order in permutations(range(len(matrix))):
        inversions = sum(order[i]>order[j] for i in range(len(order)) for j in range(i+1,len(order)))
        term = (-1)**inversions
        for i,j in enumerate(order):
            term *= matrix[i][j]
        out += term
    return out


def algorithm_controls():
    rows,checks = [],[]
    for index,matrix in enumerate(([[2,1],[1,-1]],[[0,1],[1,2]],[[2,1,0],[1,3,1],[0,1,-1]])):
        direct = [determinant([row[:n] for row in matrix[:n]]) for n in range(1,len(matrix)+1)]
        try:
            minors,count,divisions = bareiss(matrix)
            add(checks,f'control{index}_minors',minors == direct)
            add(checks,f'control{index}_negative_inertia',count == 1)
            rows.append({'matrix':matrix,'direct_minors':direct,'bareiss_minors':minors,
                         'negative_inertia':count,'exact_divisions':divisions})
        except ZeroMinor as error:
            add(checks,f'control{index}_zero_rejected',index == 1 and error.index == 1 and direct[0] == 0)
            rows.append({'matrix':matrix,'direct_minors':direct,'rejected_zero_order':error.index})
    return {'rows':rows,'checks':list(checks)},checks


def inertia_candidate(q,d,shift,purpose):
    global SERIAL
    scale = math.lcm(H.denominator,shift.denominator,*(x.denominator for x in d))
    matrix = [[0]*64 for _ in range(64)]
    for n in range(64):
        value = scale*(d[n]-shift)
        if value.denominator != 1:
            raise ArithmeticError('Nonintegral scaled diagonal')
        matrix[n][n] = value.numerator
        for e in range(6):
            matrix[n][n^(1<<e)] = int(-scale*H)
    serial = SERIAL
    SERIAL += 1
    row = {'serial':serial,'q_representative':q,'shift':exact(shift),
           'positive_integer_scale':scale,'purpose':purpose,'dimension':64}
    try:
        minors,count,divisions = bareiss(matrix)
        row.update({'valid_nonzero_leading_minors':True,'leading_minors_scaled_integer':minors,
                    'negative_inertia':count,'exact_divisions':divisions})
    except ZeroMinor as error:
        row.update({'valid_nonzero_leading_minors':False,'leading_minors_scaled_integer':error.minors,
                    'rejected_zero_minor_order':error.index,'negative_inertia':None})
    name = f'inertia_{serial:04d}_q{q:02d}.json'
    save(name,row,q=q,valid=row['valid_nonzero_leading_minors'])
    row['checkpoint_filename'] = name
    return row


def bracket(q,d,seed):
    center = Fraction(math.floor(seed*S),S)
    attempts,lo,hi = [],None,None
    for j in range(24):
        radius = Fraction(2**j,S)
        endpoints = []
        for side,baseline in (('lower',center-radius),('upper',center+radius)):
            candidate = None
            for offset in OFFSETS:
                value = baseline+Fraction(offset,17*S)
                row = inertia_candidate(q,d,value,f'expand{j}_{side}_offset{offset}')
                if row['valid_nonzero_leading_minors']:
                    candidate = (value,row)
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
        save(f'q{q:02d}_UNRESOLVED.json',{'center':exact(center),'attempts':attempts})
        raise ArithmeticError('Frozen ground expansion attempts exhausted for q'+str(q))
    refinements = []
    for step in range(32):
        if hi[0]-lo[0] <= TARGET:
            break
        choice = None
        for position in POSITIONS:
            value = lo[0]+position*(hi[0]-lo[0])
            row = inertia_candidate(q,d,value,f'refine{step}_fraction{position}')
            if row['valid_nonzero_leading_minors']:
                choice = (value,row)
                break
        if choice is None:
            save(f'q{q:02d}_UNRESOLVED.json',{'attempts':attempts,'refinements':refinements,
                                           'reason':'ALL_FROZEN_REFINEMENT_CANDIDATES_ZERO'})
            raise ArithmeticError('All frozen refinement candidates zero for q'+str(q))
        if choice[1]['negative_inertia'] == 0:
            lo = choice
        else:
            hi = choice
        refinements.append(choice[1]['checkpoint_filename'])
    if hi[0]-lo[0] > TARGET:
        save(f'q{q:02d}_UNRESOLVED.json',{'attempts':attempts,'refinements':refinements,
                                       'interval':interval(lo[0],hi[0])})
        raise ArithmeticError('Frozen ground refinements exhausted for q'+str(q))
    checks = []
    add(checks,'lower_inertia0',lo[1]['negative_inertia'] == 0)
    add(checks,'upper_inertia1',hi[1]['negative_inertia'] == 1)
    add(checks,'target_width',0<hi[0]-lo[0]<=TARGET)
    return {'q_representative':q,'origin':'NEW_NUMPY_SEED_EXACT_BAREISS',
            'numpy_seed_not_certificate':seed,'center':exact(center),'ground_interval':interval(lo[0],hi[0]),
            'lower_endpoint_evidence':lo[1],'upper_endpoint_evidence':hi[1],
            'expansion_attempts':attempts,'refinements':refinements,'checks':list(checks)},lo[0],hi[0],checks


def report_text(result):
    def rat(x):
        return str(x['numerator'])+'/'+str(x['denominator'])
    lines = ['# Held hexagon: complete record-occupancy vacuum selection V001','',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             'Scientific status: '+result['record_selection_status']+'.','',
             '| representative | orbit size | origin | exact lower | exact upper |',
             '|---:|---:|---|---:|---:|']
    for row in result['representative_certificates']:
        x = row['ground_interval']
        lines.append(f"| {row['q_representative']} | {row['orbit_size']} | {row['origin']} | "+rat(x['lower'])+' | '+rat(x['upper'])+' |')
    lines += ['', '| record word | representative | exact lower | exact upper |',
              '|---:|---:|---:|---:|']
    for row in result['all64_records']:
        x = row['ground_interval']
        lines.append(f"| {row['qword']} | {row['canonical_representative']} | "+rat(x['lower'])+' | '+rat(x['upper'])+' |')
    for label in ('global_vacuum_interval','other_sector_minus_q63_interval'):
        x = result[label]
        lines += ['',label+': ['+rat(x['lower'])+', '+rat(x['upper'])+'].']
    lines += ['', 'Possible minimizing record words: '+str(result['possible_minimizing_qwords'])+'.',
              'Qualified direct-sum excitation-gap lower bound: '+('unowned' if result['full_Nc0_gap_lower_if_q63_selected'] is None
                  else rat(result['full_Nc0_gap_lower_if_q63_selected']))+'.','',
              'All64 conserved inside record words are retained. Twelve new64-state ground certificates use NumPy seeds and exact no-pivot Bareiss; q63 reuses its sealed certificate without replay. No record-complement reduction is used.',
              'A selected occupancy sector does not select occupied content or cause dynamical formation. All statements concern this held collar/alphabet, with native copying zero in Nc0 and required in subsequent Nc1 work.',
              'No finite-volume pressure, bulk phase, matter pole, physical clock/ruler, metric, gravity or cosmic-expansion claim follows. Signed selection intervals are preserved without favorable retuning.','']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    if sys.argv[1:] != ['--execute']:
        raise RuntimeError('Explicit --execute required; no calculation launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs,base = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,
                'protocol_sha256':protocol_hash,'authenticated_inputs':inputs,'h':exact(H),
                'q_values':list(range(64)),'base_q63_replay':False,'record_complement_used':False,
                'environment':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')},
                'bracket_policy':{'seed_denominator':S,'expansion_attempts':24,'refinement_steps':32,
                                  'endpoint_offsets':list(OFFSETS),'interior_fractions':[exact(x) for x in POSITIONS],
                                  'target_width':exact(TARGET)}}
    manifest_hash = save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    structure,diagonals,reps,mappings,extra = symmetry_and_physics(base)
    save('all64_physics_and_dihedral_maps.json',structure)
    checks = list(extra)
    controls,extra = algorithm_controls()
    save('bareiss_algorithm_controls.json',controls)
    checks.extend(extra)
    rows,limits,new_count = [],{},0
    for q in reps:
        started = time.perf_counter()
        if q == 63:
            bounds = base['eigenvalue_intervals']['E0']
            lo,hi = frac(bounds['lower']),frac(bounds['upper'])
            row = {'q_representative':q,'origin':'REUSED_SEALED_Q63_NO_REPLAY','ground_interval':bounds,
                   'base_result_raw_sha256':INPUTS[BASE+'_RESULT.json'],
                   'base_E0_endpoint_evidence':base['brackets']['E0'],
                   'checks':[{'label':'reused_q63_interval_order','passed':lo<hi}]}
            extra = list(row['checks'])
        else:
            numeric = np.diag([float(x) for x in diagonals[q]])
            for n in range(64):
                for e in range(6):
                    numeric[n,n^(1<<e)] = -float(H)
            eigenvalues,unused_vectors = np.linalg.eigh(numeric)
            seed = float(eigenvalues[0])
            save(f'q{q:02d}_numpy_seed_only.json',{'q_representative':q,'numpy_version':np.__version__,
                 'eigenvalues_seeds_only':[float(x) for x in eigenvalues],'eigenvectors_used_for_physics':False})
            row,lo,hi,extra = bracket(q,diagonals[q],seed)
            new_count += 1
            del numeric,eigenvalues,unused_vectors
        row['orbit_size'] = len(structure['orbits'][str(q)])
        row['elapsed_seconds'] = time.perf_counter()-started
        save(f'q{q:02d}_representative_certificate.json',row,q=q,origin=row['origin'])
        rows.append(row)
        limits[q] = (lo,hi)
        checks.extend(extra)
    all_records = []
    for mapping in mappings:
        rep = mapping['canonical_representative']
        all_records.append({'qword':mapping['qword'],'canonical_representative':rep,
                            'ground_interval':interval(*limits[rep]),'exact_symmetry_map':mapping['transformation'],
                            'incidence_basis_permutation':mapping['incidence_basis_permutation']})
    global_lo,global_hi = min(x[0] for x in limits.values()),min(x[1] for x in limits.values())
    qlo,qhi = limits[63]
    other_lo = min(limits[q][0] for q in reps if q != 63)
    other_hi = min(limits[q][1] for q in reps if q != 63)
    gap_lo,gap_hi = other_lo-qhi,other_hi-qlo
    strict,other_wins = gap_lo>0,other_hi<qlo
    candidate = 'Q63_STRICT_OCCUPANCY_SECTOR_SELECTED' if strict else ('OTHER_SECTOR_BEATS_Q63_PRESERVED' if other_wins else 'SELECTION_DEGENERATE_OR_INCONCLUSIVE_PRESERVED')
    possible = [row['qword'] for row in all_records if frac(row['ground_interval']['lower']) <= global_hi]
    add(checks,'twelve_NEW_representative_eighs',new_count == 12)
    add(checks,'thirteen_representative_certificates',len(rows) == 13)
    add(checks,'all64_mapped_intervals',len(all_records) == 64 and [r['qword'] for r in all_records] == list(range(64)))
    add(checks,'global_vacuum_interval_order',global_lo<global_hi)
    add(checks,'selection_interval_order',gap_lo<gap_hi)
    add(checks,'possible_minimum_not_empty',bool(possible))
    final_inputs,unused = authenticate()
    add(checks,'all_input_checkpoint_bytes_unchanged',final_inputs == inputs)
    add(checks,'source_protocol_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'symmetry_stage_check_list_unchanged',structure['checks'] == checks[:len(structure['checks'])])
    failed = sum(not x['passed'] for x in checks)
    gap = None
    if strict and not failed:
        gap = min(frac(base['eigenvalue_intervals']['E1']['lower'])-qhi,gap_lo)
    result = {'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'record_selection_status':candidate if not failed else 'ARITHMETIC_FAILED_SELECTION_UNQUALIFIED',
              'raw_record_selection_candidate':candidate,'q63_strict_selected':strict and not failed,
              'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
              'authenticated_inputs':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),
              'dihedral_and_physical_controls':structure,'algorithm_controls':controls,
              'representative_certificates':rows,'all64_records':all_records,
              'global_vacuum_interval':interval(global_lo,global_hi),'other_sector_minus_q63_interval':interval(gap_lo,gap_hi),
              'possible_minimizing_qwords':possible,'possible_minimizing_representatives':sorted({all_records[q]['canonical_representative'] for q in possible}),
              'full_Nc0_gap_lower_if_q63_selected':None if gap is None else exact(gap),
              'new_eigh_count':new_count,'base_q63_eigh_or_inertia_replayed':False,'record_complement_used':False,
              'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'bulk_phase_record_formation_matter_metric_gravity_expansion_claim':False,
              'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    save('all64_record_selection_assembly.json',{'all64_records':all_records,'global_vacuum_interval':result['global_vacuum_interval'],
         'other_sector_minus_q63_interval':result['other_sector_minus_q63_interval'],'raw_selection_candidate':candidate,
         'possible_minimizing_qwords':possible})
    result['checkpoint_sha256'] = dict(STAGES)
    report = report_text(result)
    rep_table = report.split('| representative |',1)[1].split('| record word |',1)[0]
    word_table = report.split('| record word |',1)[1].split('global_vacuum_interval:',1)[0]
    if rep_table.count('\n| ') != 13 or word_table.count('\n| ') != 64:
        raise RuntimeError('Report must contain13 representative and64 record DATA rows')
    raw_hash = exclusive(RESULT,result)
    with REPORT.open('x',encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete',raw_sha256=raw_hash,report_sha256=report_hash,
          checks_passed=result['checks_passed'],checks_total=result['checks_total'])
    receipt = {'schema':NAME+'_RECEIPT','pid':os.getpid(),'result_raw_sha256':raw_hash,
               'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':report_hash,
               'manifest_sha256':manifest_hash,'journal_prefix_sha256':sha(CP/'journal.jsonl'),
               'checkpoint_sha256':dict(STAGES),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
               'authenticated_inputs':inputs,'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
               'checks_failed':failed,'record_selection_status':result['record_selection_status'],
               'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'record_selection_status':result['record_selection_status'],
                      'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
                      'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}))
    return 0 if not failed else 2


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
