#!/usr/bin/env python3
"""NEW all-q native-source vacuum certificate; no ancestor is imported."""
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
NAME = 'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J/(NAME+'.md')
RESULT = J/(NAME+'_RESULT.json')
REPORT = J/(NAME+'_RESULT.md')
RECEIPT = J/(NAME+'_RECEIPT.json')
CP = J/'bs10_record_feedback_hex_source_vacuum_v001_checkpoints'
PARENT = 'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001'
PARENT_CP = J/'bs10_record_feedback_hex_source_v001_checkpoints'
BASE = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
BASE_CP = J/'bs10_record_feedback_hex_finite_v001_checkpoints'
LPLUS = (42,41,39,38,39,41)
LMINUS = tuple(80-x for x in LPLUS)
M_SCALE = 1600
S = 10**12
OFFSETS = (0,1,-1,2,-2)
POSITIONS = (Fraction(1,2),Fraction(1,3),Fraction(2,3),Fraction(2,5),Fraction(3,5))
TARGET = Fraction(1,10**11)
ATTEMPT_CREATED = False
SERIAL = 0
STAGES = {}
INPUTS = {
    'bs10_record_feedback_hex_source_v001.py':'d34b49b525618034e43c2c865dba5481244675fdb3495d8437c64842f1471be3',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001.md':'e94072efdbe4944d9307e9c4dd3335feb7338dcfa5f3e7ff4506482761efee92',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001_RESULT.json':'98cc4454e6cb044e770a8e2bb21559e6fcba1a365ae36858d187fdcf7fe67ae3',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001_RECEIPT.json':'bfc6852ece20655d4b6cbb90212e1eb961344baaa43f4bdcf12c41d5ce7e39a7',
    'HELD_HEX_NATIVE_DIPOLE_SOURCE_GATE_V001.md':'bf8e581bbe4038cc276ed81c6230aafb8e3bf29de366ce1b67ade0fc2898480d',
    'HELD_HEX_COMPLETE_NONUNIFORM_ADDITION_SOURCE_GATE_V001.md':'c99ceb680037c35f87d6b280c0fd11bb456f1bc798fc429175e3d9a8cc55cbdc',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def exact(value):
    value = Fraction(value)
    displays = []
    for mode in (ROUND_FLOOR,ROUND_CEILING):
        with localcontext() as context:
            context.prec,context.rounding = 20,mode
            displays.append(str(Decimal(value.numerator)/Decimal(value.denominator)))
    return {'numerator':value.numerator,'denominator':value.denominator,
            'decimal20_lower':displays[0],'decimal20_upper':displays[1]}


def frac(value):
    return Fraction(value['numerator'],value['denominator'])


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


def verify_journal(directory,result,receipt,receipt_hash,checkpoints):
    lines = (directory/'journal.jsonl').read_bytes().splitlines(keepends=True)
    entries = [json.loads(line) for line in lines]
    if not entries or entries[-1]['event'] != 'receipt_complete' or entries[-1]['receipt_sha256'] != receipt_hash:
        raise RuntimeError('Parent final receipt event mismatch: '+str(directory))
    prefix = hashlib.sha256(b''.join(lines[:-1])).hexdigest()
    if prefix != receipt['journal_prefix_sha256']:
        raise RuntimeError('Parent journal prefix mismatch: '+str(directory))
    starts = [row for row in entries if row['event'] == 'started']
    manifest = checkpoints['input_manifest.json']
    if len(starts) != 1 or not(starts[0]['manifest_sha256'] == result['manifest_sha256'] == receipt['manifest_sha256'] == manifest):
        raise RuntimeError('Parent manifest/start mismatch: '+str(directory))
    for name,wanted in checkpoints.items():
        commits = [row for row in entries if row.get('filename') == name and row.get('sha256') == wanted]
        if len(commits) != 1:
            raise RuntimeError('Parent checkpoint commit mismatch: '+name)
    return prefix


def authenticate():
    direct = {}
    for name,wanted in INPUTS.items():
        got = sha(J/name)
        if got != wanted:
            raise RuntimeError('Frozen direct input mismatch: '+name)
        direct[name] = got
    parent = json.loads((J/(PARENT+'_RESULT.json')).read_text())
    receipt = json.loads((J/(PARENT+'_RECEIPT.json')).read_text())
    if receipt['result_raw_sha256'] != direct[PARENT+'_RESULT.json'] or receipt['result_canonical_sha256'] != hashlib.sha256(canonical(parent)).hexdigest():
        raise RuntimeError('Source parent raw/canonical mismatch')
    parent_report = sha(J/(PARENT+'_RESULT.md'))
    if parent_report != receipt['report_sha256']:
        raise RuntimeError('Source parent CURRENT report mismatch')
    for key,name in (('source_sha256','bs10_record_feedback_hex_source_v001.py'),('protocol_sha256',PARENT+'.md')):
        if parent[key] != direct[name] or receipt[key] != direct[name]:
            raise RuntimeError('Source parent source/protocol mismatch')
    if parent['authenticated_inputs'] != receipt['authenticated_inputs'] or parent['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Source parent input/checkpoint equality mismatch')
    inherited = receipt['authenticated_inputs']
    old_direct,old_root,finite_cp,parent_cp = {},{},{},{}
    for name,wanted in inherited['direct_input_sha256'].items():
        got = sha(J/name)
        if got != wanted:
            raise RuntimeError('Inherited finite/collar direct input changed: '+name)
        old_direct[name] = got
    for rel,wanted in inherited['inherited_input_sha256'].items():
        got = sha(ROOT/rel)
        if got != wanted:
            raise RuntimeError('Inherited root input changed: '+rel)
        old_root[rel] = got
    for name,wanted in inherited['base_checkpoint_sha256'].items():
        got = sha(BASE_CP/name)
        if got != wanted:
            raise RuntimeError('Inherited finite checkpoint changed: '+name)
        finite_cp[name] = got
    finite = json.loads((J/(BASE+'_RESULT.json')).read_text())
    finite_receipt = json.loads((J/(BASE+'_RECEIPT.json')).read_text())
    if finite_receipt['result_raw_sha256'] != old_direct[BASE+'_RESULT.json'] or finite_receipt['result_canonical_sha256'] != hashlib.sha256(canonical(finite)).hexdigest():
        raise RuntimeError('Inherited finite raw/canonical mismatch')
    for key,name in (('source_sha256','bs10_record_feedback_hex_finite_v001.py'),('protocol_sha256',BASE+'.md')):
        if finite[key] != old_direct[name] or finite_receipt[key] != old_direct[name]:
            raise RuntimeError('Inherited finite source/protocol mismatch')
    finite_report = sha(J/(BASE+'_RESULT.md'))
    if finite_report != finite_receipt['report_sha256'] or finite_report != inherited['base_report_sha256']:
        raise RuntimeError('Inherited finite CURRENT report mismatch')
    if finite['checkpoint_sha256'] != finite_cp or finite_receipt['checkpoint_sha256'] != finite_cp or finite['input_sha256'] != old_root or finite_receipt['input_sha256'] != old_root:
        raise RuntimeError('Inherited finite input/checkpoint map mismatch')
    finite_prefix = verify_journal(BASE_CP,finite,finite_receipt,old_direct[BASE+'_RECEIPT.json'],finite_cp)
    if finite_prefix != inherited['base_journal_prefix_sha256']:
        raise RuntimeError('Inherited finite journal prefix mismatch')
    structure = json.loads((BASE_CP/'structure.json').read_text())
    prefix,alias = structure['checks'],finite['structural_checks']['checks']
    if prefix != alias[:len(prefix)] or inherited['preserved_base_check_alias'] != {'checkpoint_count':len(prefix),'result_nested_count':len(alias),'prefix_equal':True}:
        raise RuntimeError('Preserved finite structural-check alias mismatch')
    for key in ('physical_n_diagonal','P_words','Q_words','H_edges','Q_edges','WWdagger_scalar'):
        if structure[key] != finite['structural_checks'][key]:
            raise RuntimeError('Inherited finite structural data mismatch: '+key)
    for name,wanted in receipt['checkpoint_sha256'].items():
        got = sha(PARENT_CP/name)
        if got != wanted:
            raise RuntimeError('Source parent checkpoint changed: '+name)
        parent_cp[name] = got
    parent_prefix = verify_journal(PARENT_CP,parent,receipt,direct[PARENT+'_RECEIPT.json'],parent_cp)
    manifest = json.loads((PARENT_CP/'input_manifest.json').read_text())
    if manifest['authenticated_inputs'] != inherited or manifest['source_sha256'] != direct['bs10_record_feedback_hex_source_v001.py'] or manifest['protocol_sha256'] != direct[PARENT+'.md']:
        raise RuntimeError('Source parent manifest payload mismatch')
    if parent['checks_failed'] != 0 or receipt['checks_failed'] != 0 or parent['status'] != 'EXACT_ARITHMETIC_PASS' or finite['checks_failed'] != 0:
        raise RuntimeError('Source parent or finite arithmetic unqualified')
    bounds = parent['new_Ealpha_interval']
    if not frac(bounds['lower']) < frac(bounds['upper']):
        raise RuntimeError('Reused q63 interval order invalid')
    evidence = parent['new_ground_bracket']
    if evidence['interval'] != bounds or evidence['lower_endpoint_evidence']['negative_inertia'] != 0 or evidence['upper_endpoint_evidence']['negative_inertia'] != 1:
        raise RuntimeError('Reused q63 ground endpoint evidence mismatch')
    inputs = {'direct_input_sha256':direct,'source_parent_report_sha256':parent_report,
              'source_parent_checkpoint_sha256':parent_cp,'source_parent_journal_prefix_sha256':parent_prefix,
              'source_parent_authenticated_inputs':inherited,'inherited_finite_direct_input_sha256':old_direct,
              'inherited_root_input_sha256':old_root,'inherited_finite_checkpoint_sha256':finite_cp,
              'inherited_finite_report_sha256':finite_report,'inherited_finite_journal_prefix_sha256':finite_prefix,
              'preserved_finite_stage_alias':inherited['preserved_base_check_alias']}
    return inputs,parent


def rotate(word):
    return sum(((word>>v)&1)<<((v+3)%6) for v in range(6))


def diagonal1600(q,n,l):
    total = 0
    for v in range(6):
        previous,following = (n>>((v-1)%6))&1,(n>>v)&1
        delta = previous+following-1
        c160 = -4*l[v]+previous*(l[(v-1)%6]+l[v])+following*(l[v]+l[(v+1)%6])+(l[v]+40)
        total += 40*l[v]*delta*delta-20*l[v]*delta+10*(1-((q>>v)&1))*c160
    return total


def physical_diagonal1600(q,n,l):
    # Fixed outside degree2/q1 action supplies +3 once, hence4800 here.
    total = 4800
    for v in range(6):
        previous,following = (n>>((v-1)%6))&1,(n>>v)&1
        delta,record = previous+following-1,(q>>v)&1
        total += 40*l[v]*delta*delta+40*l[v]*record-10*(l[v]+40)*(record+1)
        total -= 10*following*(l[v]+l[(v+1)%6])*(record+((q>>((v+1)%6))&1))
    return total


def source_controls(parent):
    diagonals,rows,checks = {},[],[]
    old = parent['source_structure']
    parent_edges = {(n,m):frac(value) for n,m,value in old['new_Halpha_edges']}
    edge_weights = [-4*(LPLUS[e]+LPLUS[(e+1)%6]) for e in range(6)]
    for q in range(64):
        diagonal = [diagonal1600(q,n,LPLUS) for n in range(64)]
        diagonals[q] = diagonal
        local = []
        for n in range(64):
            add(local,f'q{q}_n{n}_complete_physical_source',diagonal[n] == physical_diagonal1600(q,n,LPLUS))
            add(local,f'q{q}_n{n}_R3_source_diagonal',diagonal[n] == diagonal1600(rotate(q),rotate(n),LMINUS))
            uniform = sum(1600*(((n>>((v-1)%6))&1)+((n>>v)&1)-1)**2
                          -800*((q>>v)&1)*(((n>>((v-1)%6))&1)+((n>>v)&1)-1) for v in range(6))
            add(local,f'q{q}_n{n}_uniform_complete_reduction',diagonal1600(q,n,(40,)*6) == uniform)
            for e in range(6):
                add(local,f'q{q}_n{n}_e{e}_R3_flip_map',rotate(n^(1<<e)) == rotate(n)^(1<<((e+3)%6)))
                add(local,f'q{q}_n{n}_e{e}_R3_flip_weight',edge_weights[e] == -4*(LMINUS[(e+3)%6]+LMINUS[(e+4)%6]))
        rows.append({'qword':q,'q_bits_vertex_order':[int(bool(q&(1<<v))) for v in range(6)],
                     'negative_source_partner_qword':rotate(q),'incidence_R3_basis_permutation':[rotate(n) for n in range(64)],
                     'diagonal1600':diagonal,'checks':list(local)})
        checks.extend(local)
    for n in range(64):
        add(checks,f'q63_saved_source_diagonal_n{n}',Fraction(diagonals[63][n],M_SCALE) == frac(old['new_Halpha_diagonal'][n]))
        for e in range(6):
            m = n^(1<<e)
            key = tuple(sorted((n,m)))
            add(checks,f'q63_saved_source_flip_n{n}_e{e}',Fraction(edge_weights[e],M_SCALE) == parent_edges[key])
    add(checks,'positive_inside_lapses',min(LPLUS)>0 and min(LMINUS)>0)
    add(checks,'strictly_negative_all_flip_ports',all(x<0 for x in edge_weights))
    add(checks,'R3_word_and_basis_bijection',sorted(rotate(x) for x in range(64)) == list(range(64)))
    add(checks,'R3_is_its_own_inverse',all(rotate(rotate(x)) == x for x in range(64)))
    add(checks,'all64_record_words_retained',len(rows)==64 and [row['qword'] for row in rows]==list(range(64)))
    stage = {'M_scale':M_SCALE,'L_plus_numerators_over40':list(LPLUS),'L_minus_numerators_over40':list(LMINUS),
             'external_lapse':exact(1),'occupied_exterior_reference_contribution':exact(3),
             'flip_weights1600':edge_weights,'all64_record_source_controls':rows,
             'record_complement_used':False,'positive_source_symmetry_reduction_used':False,'checks':list(checks)}
    return stage,diagonals,edge_weights,checks


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
    signs = [1]+[1 if value>0 else -1 for value in minors]
    return minors,sum(x!=y for x,y in zip(signs,signs[1:])),divisions


def determinant(matrix):
    total = 0
    for order in permutations(range(len(matrix))):
        inversions = sum(order[i]>order[j] for i in range(len(order)) for j in range(i+1,len(order)))
        term = (-1)**inversions
        for i,j in enumerate(order):
            term *= matrix[i][j]
        total += term
    return total


def algorithm_controls():
    rows,checks = [],[]
    for number,matrix in enumerate(([[2,1],[1,-1]],[[0,1],[1,2]],[[2,1,0],[1,3,1],[0,1,-1]])):
        direct = [determinant([row[:n] for row in matrix[:n]]) for n in range(1,len(matrix)+1)]
        try:
            minors,count,divisions = bareiss(matrix)
            add(checks,f'algorithm{number}_direct_minors',minors == direct)
            add(checks,f'algorithm{number}_known_inertia',count == 1)
            rows.append({'matrix':matrix,'direct_minors':direct,'bareiss_minors':minors,'negative_inertia':count,'exact_divisions':divisions})
        except ZeroMinor as error:
            add(checks,f'algorithm{number}_zero_rejected',number == 1 and error.index == 1 and direct[0] == 0)
            rows.append({'matrix':matrix,'direct_minors':direct,'rejected_zero_order':error.index})
    return {'rows':rows,'checks':list(checks)},checks


def inertia_candidate(q,diagonal,edge_weights,shift,purpose):
    global SERIAL
    numerator,denominator = shift.numerator,shift.denominator
    matrix = [[0]*64 for _ in range(64)]
    for n in range(64):
        matrix[n][n] = denominator*diagonal[n]-M_SCALE*numerator
        for e in range(6):
            matrix[n][n^(1<<e)] = denominator*edge_weights[e]
    serial = SERIAL
    SERIAL += 1
    row = {'serial':serial,'qword':q,'matrix':'NEW_Q_ALPHA_PLUS_ONLY','shift':exact(shift),
           'H_minus_shift_positive_integer_scale':M_SCALE*denominator,'dimension':64,'purpose':purpose}
    try:
        minors,count,divisions = bareiss(matrix)
        row.update({'valid_nonzero_leading_minors':True,'leading_minors_scaled_integer':minors,'negative_inertia':count,'exact_divisions':divisions})
    except ZeroMinor as error:
        row.update({'valid_nonzero_leading_minors':False,'leading_minors_scaled_integer':error.minors,'rejected_zero_minor_order':error.index,'negative_inertia':None})
    name = f'inertia_{serial:04d}_q{q:02d}.json'
    save(name,row,q=q,valid=row['valid_nonzero_leading_minors'])
    row['checkpoint_filename'] = name
    return row


def bracket(q,diagonal,edge_weights,seed):
    center = Fraction(math.floor(seed*S),S)
    attempts,lo,hi = [],None,None
    for j in range(24):
        radius = Fraction(2**j,S)
        endpoints = []
        for side,baseline in (('lower',center-radius),('upper',center+radius)):
            candidate = None
            for offset in OFFSETS:
                value = baseline+Fraction(offset,17*S)
                row = inertia_candidate(q,diagonal,edge_weights,value,f'expand{j}_{side}_offset{offset}')
                if row['valid_nonzero_leading_minors']:
                    candidate = (value,row)
                    break
            endpoints.append(candidate)
        attempts.append({'attempt':j,'radius':exact(radius),
                         'lower_checkpoint':None if endpoints[0] is None else endpoints[0][1]['checkpoint_filename'],
                         'upper_checkpoint':None if endpoints[1] is None else endpoints[1][1]['checkpoint_filename']})
        if all(value is not None for value in endpoints):
            if endpoints[0][1]['negative_inertia'] == 0 and endpoints[1][1]['negative_inertia'] == 1:
                lo,hi = endpoints
                break
    if lo is None:
        save(f'q{q:02d}_UNRESOLVED.json',{'center':exact(center),'attempts':attempts})
        raise ArithmeticError('Frozen expansion exhausted for q'+str(q))
    refinements = []
    for step in range(32):
        if hi[0]-lo[0] <= TARGET:
            break
        choice = None
        for position in POSITIONS:
            value = lo[0]+position*(hi[0]-lo[0])
            row = inertia_candidate(q,diagonal,edge_weights,value,f'refine{step}_fraction{position}')
            if row['valid_nonzero_leading_minors']:
                choice = (value,row)
                break
        if choice is None:
            save(f'q{q:02d}_UNRESOLVED.json',{'attempts':attempts,'refinements':refinements,'reason':'ALL_FROZEN_REFINEMENT_CANDIDATES_ZERO'})
            raise ArithmeticError('All refinement candidates zero for q'+str(q))
        if choice[1]['negative_inertia'] == 0:
            lo = choice
        else:
            hi = choice
        refinements.append(choice[1]['checkpoint_filename'])
    if hi[0]-lo[0] > TARGET:
        save(f'q{q:02d}_UNRESOLVED.json',{'attempts':attempts,'refinements':refinements,'ground_interval':interval(lo[0],hi[0])})
        raise ArithmeticError('Frozen refinement exhausted for q'+str(q))
    checks = []
    add(checks,f'q{q}_lower_inertia0',lo[1]['negative_inertia'] == 0)
    add(checks,f'q{q}_upper_inertia1',hi[1]['negative_inertia'] == 1)
    add(checks,f'q{q}_target_width',0<hi[0]-lo[0]<=TARGET)
    return {'qword':q,'origin':'NEW_NUMPY_SEED_EXACT_BAREISS','numpy_seed_not_certificate':seed,'center':exact(center),
            'ground_interval':interval(lo[0],hi[0]),'lower_endpoint_evidence':lo[1],'upper_endpoint_evidence':hi[1],
            'expansion_attempts':attempts,'refinements':refinements,'checks':list(checks)},lo[0],hi[0],checks


def report_text(result):
    def rat(value):
        return str(value['numerator'])+'/'+str(value['denominator'])
    lines = ['# Held hexagon: complete all-record native source vacuum V001','',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             'Scientific status: '+result['record_selection_status']+'.','',
             '| positive-source q | origin | exact lower | exact upper | negative-source partner q |',
             '|---:|---|---:|---:|---:|']
    for row in result['all64_source_records']:
        bounds = row['ground_interval']
        lines.append(f"| {row['qword']} | {row['origin']} | "+rat(bounds['lower'])+' | '+rat(bounds['upper'])+f" | {row['negative_source_partner_qword']} |")
    for label in ('global_source_vacuum_interval','retained_q63_source_vacuum_interval','other_sector_minus_q63_interval'):
        bounds = result[label]
        lines += ['',label+': ['+rat(bounds['lower'])+', '+rat(bounds['upper'])+'].']
    lines += ['', 'Possible minimizing record words: '+str(result['possible_minimizing_qwords'])+'.',
              'The global static vacuum and the retained q63 sector-ground reference are BOTH saved. Nc0 q conservation does not establish relaxation, an adiabatic history or a record-changing preparation.',
              'All64 physical mixed-q source blocks are retained. Exactly63 NEW64-state ground certificates use one NumPy seed each and exact integer Bareiss. q63 reuses the sealed alpha+ ground interval without replay. Negative-source sectors are exact simultaneous-R3 partner images, not record complements or64 additional runs.',
              'Complete storage, feedback, occupied exterior midpoint and fixed collar reference remain owned once. There is no source-dependent identity reset or q-delta proxy.',
              'No excitation gap, numerical derivative, physical gravity susceptibility, matter residue, bulk phase, ruler, pressure, galaxy law or expansion claim is inferred. Other winners or ambiguous selection remain visible.',
              '',f"Elapsed seconds: {result['elapsed_seconds']}; native peak RSS: {result['ru_maxrss_native']}.",'']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    if sys.argv[1:] != ['--execute']:
        raise RuntimeError('Explicit --execute required; no calculation launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs,parent = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
                'authenticated_inputs':inputs,'h':exact(Fraction(1,5)),'alpha':exact(Fraction(1,20)),
                'L_plus_numerators_over40':list(LPLUS),'outside_lapse':exact(1),'M_scale':M_SCALE,
                'new_qwords':list(range(63)),'reused_qword':63,'q63_eigh_or_inertia_replay':False,'ancestor_imported':False,
                'environment':{key:os.environ.get(key) for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')},
                'bracket_policy':{'seed_denominator':S,'expansion_attempts':24,'refinement_steps':32,'endpoint_offsets':list(OFFSETS),
                                  'interior_fractions':[exact(value) for value in POSITIONS],'target_width':exact(TARGET)}}
    manifest_hash = save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    structure,diagonals,edge_weights,extra = source_controls(parent)
    save('all64_complete_source_and_R3_controls.json',structure)
    checks = list(extra)
    controls,extra = algorithm_controls()
    save('bareiss_algorithm_controls.json',controls)
    checks.extend(extra)
    if any(not check['passed'] for check in checks):
        raise ArithmeticError('Pre-certificate source/algorithm control failed')
    rows,limits,new_count = [],{},0
    for q in range(64):
        started = time.perf_counter()
        if q == 63:
            bounds = parent['new_Ealpha_interval']
            lo,hi = frac(bounds['lower']),frac(bounds['upper'])
            row = {'qword':q,'origin':'REUSED_SEALED_Q63_ALPHA_PLUS_NO_REPLAY','ground_interval':bounds,
                   'source_parent_result_raw_sha256':INPUTS[PARENT+'_RESULT.json'],'source_parent_ground_bracket':parent['new_ground_bracket'],
                   'checks':[{'label':'reused_q63_interval_order','passed':lo<hi}]}
            extra = list(row['checks'])
        else:
            numeric = np.diag(np.array(diagonals[q],dtype=float)/M_SCALE)
            for n in range(64):
                for e in range(6):
                    numeric[n,n^(1<<e)] = edge_weights[e]/M_SCALE
            eigenvalues,unused_vectors = np.linalg.eigh(numeric)
            seed = float(eigenvalues[0])
            if not math.isfinite(seed):
                raise ArithmeticError('Nonfinite NumPy seed for q'+str(q))
            save(f'q{q:02d}_numpy_seed_only.json',{'qword':q,'numpy_version':np.__version__,
                 'eigenvalues_seeds_only':[float(value) for value in eigenvalues],'eigenvectors_used_for_physics':False})
            row,lo,hi,extra = bracket(q,diagonals[q],edge_weights,seed)
            new_count += 1
            del numeric,eigenvalues,unused_vectors
        row['negative_source_partner_qword'] = rotate(q)
        row['elapsed_seconds'] = time.perf_counter()-started
        save(f'q{q:02d}_source_ground_certificate.json',row,q=q,origin=row['origin'])
        rows.append(row)
        limits[q] = (lo,hi)
        checks.extend(extra)
        print(json.dumps({'pid':os.getpid(),'completed_qword':q,'new_ground_certificates':new_count,'elapsed_seconds':time.perf_counter()-T0}),flush=True)
    global_lo,global_hi = min(value[0] for value in limits.values()),min(value[1] for value in limits.values())
    qlo,qhi = limits[63]
    other_lo,other_hi = min(limits[q][0] for q in range(63)),min(limits[q][1] for q in range(63))
    gap_lo,gap_hi = other_lo-qhi,other_hi-qlo
    strict,other_wins = gap_lo>0,other_hi<qlo
    candidate = 'Q63_STRICT_SOURCE_VACUUM_SELECTED' if strict else ('OTHER_SOURCE_SECTOR_BEATS_Q63_PRESERVED' if other_wins else 'SOURCE_SELECTION_DEGENERATE_OR_INCONCLUSIVE_PRESERVED')
    possible = [q for q in range(64) if limits[q][0] <= global_hi]
    negative_rows = [{'qword':q,'positive_source_partner_qword':rotate(q),'ground_interval':interval(*limits[rotate(q)])} for q in range(64)]
    add(checks,'exactly63_NEW_eigh_seed_ground_certificates',new_count == 63)
    add(checks,'all64_source_ground_certificates',len(rows)==64 and [row['qword'] for row in rows] == list(range(64)))
    add(checks,'global_source_interval_order',global_lo<global_hi)
    add(checks,'signed_selection_interval_order',gap_lo<gap_hi)
    add(checks,'possible_minimizer_not_empty',bool(possible))
    add(checks,'negative_source_global_minimum_identical',min(frac(row['ground_interval']['lower']) for row in negative_rows)==global_lo and min(frac(row['ground_interval']['upper']) for row in negative_rows)==global_hi)
    add(checks,'q63_retained_negative_source_interval_identical',negative_rows[63]['ground_interval']==interval(qlo,qhi))
    final_inputs,final_parent = authenticate()
    add(checks,'all_parent_input_checkpoint_report_bytes_unchanged',final_inputs == inputs and final_parent['new_Ealpha_interval']==parent['new_Ealpha_interval'])
    add(checks,'source_protocol_bytes_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'source_stage_check_list_unchanged',structure['checks']==checks[:len(structure['checks'])])
    failed = sum(not check['passed'] for check in checks)
    assembly = {'all64_source_records':rows,'all64_negative_source_records':negative_rows,
                'global_source_vacuum_interval':interval(global_lo,global_hi),'retained_q63_source_vacuum_interval':interval(qlo,qhi),
                'other_sector_minus_q63_interval':interval(gap_lo,gap_hi),'raw_selection_candidate':candidate,'possible_minimizing_qwords':possible}
    save('all64_source_vacuum_selection_assembly.json',assembly)
    result = {'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'record_selection_status':candidate if not failed else 'ARITHMETIC_FAILED_SELECTION_UNQUALIFIED',
              'raw_record_selection_candidate':candidate,'q63_strict_selected':strict and not failed,
              'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,'authenticated_inputs':inputs,
              'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),'complete_source_and_R3_controls':structure,
              'algorithm_controls':controls,**assembly,'new_eigh_count':new_count,'q63_eigh_or_inertia_replayed':False,
              'negative_source_eigh_or_inertia_run':False,'record_complement_or_positive_source_symmetry_reduction_used':False,
              'source_conservation_is_sector_ground_preparation':False,'excitation_gap_claim':False,
              'bulk_phase_matter_residue_metric_gravity_expansion_claim':False,'checks':checks,
              'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = report_text(result)
    table = report.split('| positive-source q |',1)[1].split('global_source_vacuum_interval:',1)[0]
    if table.count('\n| ') != 64:
        raise RuntimeError('Report must contain exactly64 source-record DATA rows')
    raw_hash = exclusive(RESULT,result)
    with REPORT.open('x',encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete',raw_sha256=raw_hash,report_sha256=report_hash,checks_passed=result['checks_passed'],checks_total=result['checks_total'])
    receipt = {'schema':NAME+'_RECEIPT','pid':os.getpid(),'result_raw_sha256':raw_hash,
               'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':report_hash,
               'manifest_sha256':manifest_hash,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'checkpoint_sha256':dict(STAGES),
               'source_sha256':source_hash,'protocol_sha256':protocol_hash,'authenticated_inputs':inputs,
               'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],'checks_failed':failed,
               'record_selection_status':result['record_selection_status'],'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'record_selection_status':result['record_selection_status'],
                      'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
                      'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
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
