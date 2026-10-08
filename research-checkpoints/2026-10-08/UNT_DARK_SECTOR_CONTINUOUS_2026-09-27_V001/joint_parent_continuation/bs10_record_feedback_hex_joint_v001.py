#!/usr/bin/env python3
"""New held full-copy integer ground certificate; no ancestor is imported."""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction
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
NAME = 'BS10_RECORD_FEEDBACK_HEX_JOINT_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J/(NAME+'.md')
RESULT = J/(NAME+'_RESULT.json')
REPORT = J/(NAME+'_RESULT.md')
RECEIPT = J/(NAME+'_RECEIPT.json')
CP = J/'bs10_record_feedback_hex_joint_v001_checkpoints'
VAC = 'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001'
VAC_CP = J/'bs10_record_feedback_hex_vacuum_v001_checkpoints'
BASE = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
BASE_CP = J/'bs10_record_feedback_hex_finite_v001_checkpoints'
DIM = 6*64*64
CERTIFICATE_STAGES = (16,64,256,1024,4096)
MAX_ITERATIONS = 4096
ROUND_SCALE = 10**60
TARGET = Fraction(1,10**6)
DROP_NORM = 1e-14
POSITIVE_FLOOR = 1e-100
ATTEMPT_CREATED = False
STAGES = {}
FLOAT_ACTION_CALLS = 0
INPUTS = {
    'bs10_record_feedback_hex_vacuum_v001.py':'30d5cfbbc9f8107917b19f89b5a14a6cdcbfcf8b735aef4f703bb297b22cfdac',
    'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001.md':'b8df449b4c0fe63e836a6bda789c3d6fdeed88f2b9c0f1954f58ca8a255d19cc',
    'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001_RESULT.json':'4b8047f62cbb6fa98306ebc579364e279b1d90b9a47cf94d296447bd46bb8137',
    'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001_RECEIPT.json':'2c509aba82f0e9ea08d6d0f2f90d552e85a3d96400dbd4babf455cda5d36b850',
    'HELD_HEX_NATIVE_DIPOLE_SOURCE_GATE_V001.md':'bf8e581bbe4038cc276ed81c6230aafb8e3bf29de366ce1b67ade0fc2898480d',
    'HELD_HEX_FULL_COPY_GROUND_CERTIFICATE_GATE_V001.md':'d9b73829b8e77663028da4940f9e6f2d373c929e4e3ca22d2e5133d8542ad819',
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
    entry = {'event':kind,'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,**fields}
    with (CP/'journal.jsonl').open('ab') as stream:
        stream.write(canonical(entry)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def save(name,obj,**fields):
    digest = exclusive(CP/name,obj)
    STAGES[name] = digest
    event('stage_complete',filename=name,sha256=digest,**fields)
    return digest


def add(checks,label,condition):
    checks.append({'label':label,'passed':bool(condition)})


def verify_parent_journal(directory,receipt,receipt_hash,checkpoint_map,manifest_hash):
    rawlines = (directory/'journal.jsonl').read_bytes().splitlines(keepends=True)
    entries = [json.loads(line) for line in rawlines]
    if not entries or entries[-1]['event'] != 'receipt_complete' or entries[-1]['receipt_sha256'] != receipt_hash:
        raise RuntimeError('Parent final receipt commit mismatch: '+str(directory))
    prefix = hashlib.sha256(b''.join(rawlines[:-1])).hexdigest()
    if prefix != receipt['journal_prefix_sha256']:
        raise RuntimeError('Parent journal prefix mismatch: '+str(directory))
    starts = [entry for entry in entries if entry['event'] == 'started']
    if len(starts) != 1 or starts[0]['manifest_sha256'] != manifest_hash:
        raise RuntimeError('Parent manifest/start mismatch: '+str(directory))
    for filename,wanted in checkpoint_map.items():
        commits = [entry for entry in entries if entry.get('filename') == filename and entry.get('sha256') == wanted]
        if len(commits) != 1:
            raise RuntimeError('Parent checkpoint journal commit mismatch: '+filename)
    return prefix


def authenticate():
    direct = {}
    for name,wanted in INPUTS.items():
        got = sha(J/name)
        if got != wanted:
            raise RuntimeError('Frozen direct input mismatch: '+name)
        direct[name] = got
    vacuum = json.loads((J/(VAC+'_RESULT.json')).read_text())
    receipt = json.loads((J/(VAC+'_RECEIPT.json')).read_text())
    if receipt['result_raw_sha256'] != direct[VAC+'_RESULT.json'] or receipt['result_canonical_sha256'] != hashlib.sha256(canonical(vacuum)).hexdigest():
        raise RuntimeError('Vacuum result raw/canonical mismatch')
    vacuum_report_hash = sha(J/(VAC+'_RESULT.md'))
    if vacuum_report_hash != receipt['report_sha256']:
        raise RuntimeError('Vacuum report seal mismatch')
    for key,name in (('source_sha256','bs10_record_feedback_hex_vacuum_v001.py'),('protocol_sha256',VAC+'.md')):
        if receipt[key] != direct[name] or vacuum[key] != direct[name]:
            raise RuntimeError('Vacuum source/protocol mismatch')
    if vacuum['authenticated_inputs'] != receipt['authenticated_inputs'] or vacuum['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Vacuum input/checkpoint map mismatch')
    inherited = receipt['authenticated_inputs']
    inherited_direct,inherited_root,finite_cp = {},{},{}
    for name,wanted in inherited['direct_input_sha256'].items():
        got = sha(J/name)
        if got != wanted:
            raise RuntimeError('Inherited finite/collar input changed: '+name)
        inherited_direct[name] = got
    for rel,wanted in inherited['inherited_input_sha256'].items():
        got = sha(ROOT/rel)
        if got != wanted:
            raise RuntimeError('Inherited frozen input changed: '+rel)
        inherited_root[rel] = got
    for name,wanted in inherited['base_checkpoint_sha256'].items():
        got = sha(BASE_CP/name)
        if got != wanted:
            raise RuntimeError('Inherited finite checkpoint changed: '+name)
        finite_cp[name] = got
    finite = json.loads((J/(BASE+'_RESULT.json')).read_text())
    finite_receipt = json.loads((J/(BASE+'_RECEIPT.json')).read_text())
    if finite_receipt['result_raw_sha256'] != inherited_direct[BASE+'_RESULT.json'] or finite_receipt['result_canonical_sha256'] != hashlib.sha256(canonical(finite)).hexdigest():
        raise RuntimeError('Inherited finite raw/canonical mismatch')
    for key,name in (('source_sha256','bs10_record_feedback_hex_finite_v001.py'),('protocol_sha256',BASE+'.md')):
        if finite_receipt[key] != inherited_direct[name] or finite[key] != inherited_direct[name]:
            raise RuntimeError('Inherited finite source/protocol mismatch')
    finite_report_hash = sha(J/(BASE+'_RESULT.md'))
    if finite_report_hash != finite_receipt['report_sha256'] or finite_report_hash != inherited['base_report_sha256']:
        raise RuntimeError('Inherited finite report mismatch')
    if finite_receipt['checkpoint_sha256'] != finite_cp or finite_receipt['input_sha256'] != inherited_root:
        raise RuntimeError('Inherited finite checkpoint/input equality mismatch')
    if finite['checkpoint_sha256'] != finite_cp or finite['input_sha256'] != inherited_root:
        raise RuntimeError('Inherited finite result maps mismatch')
    if not(finite['manifest_sha256'] == finite_receipt['manifest_sha256'] == finite_cp['input_manifest.json']):
        raise RuntimeError('Inherited finite manifest map mismatch')
    finite_prefix = verify_parent_journal(BASE_CP,finite_receipt,inherited_direct[BASE+'_RECEIPT.json'],finite_cp,finite_cp['input_manifest.json'])
    if finite_prefix != inherited['base_journal_prefix_sha256']:
        raise RuntimeError('Inherited finite prefix mismatch')
    structure = json.loads((BASE_CP/'structure.json').read_text())
    prefix,alias = structure['checks'],finite['structural_checks']['checks']
    if prefix != alias[:len(prefix)] or inherited['preserved_base_stage_alias'] != {'prefix_count':len(prefix),'nested_count':len(alias),'prefix_equal':True}:
        raise RuntimeError('Preserved finite stage-check alias mismatch')
    for key in ('physical_n_diagonal','P_words','Q_words','H_edges','Q_edges','WWdagger_scalar'):
        if structure[key] != finite['structural_checks'][key]:
            raise RuntimeError('Inherited finite structural data mismatch: '+key)
    vacuum_cp = {}
    for name,wanted in receipt['checkpoint_sha256'].items():
        got = sha(VAC_CP/name)
        if got != wanted:
            raise RuntimeError('Vacuum checkpoint changed: '+name)
        vacuum_cp[name] = got
    if not(vacuum['manifest_sha256'] == receipt['manifest_sha256'] == vacuum_cp['input_manifest.json']):
        raise RuntimeError('Vacuum manifest map mismatch')
    vacuum_manifest = json.loads((VAC_CP/'input_manifest.json').read_text())
    if vacuum_manifest['authenticated_inputs'] != inherited or vacuum_manifest['source_sha256'] != direct['bs10_record_feedback_hex_vacuum_v001.py'] or vacuum_manifest['protocol_sha256'] != direct[VAC+'.md']:
        raise RuntimeError('Vacuum manifest source/protocol/input payload mismatch')
    vacuum_prefix = verify_parent_journal(VAC_CP,receipt,direct[VAC+'_RECEIPT.json'],vacuum_cp,vacuum_cp['input_manifest.json'])
    if vacuum['checks_failed'] != 0 or receipt['checks_failed'] != 0 or not vacuum['q63_strict_selected'] or vacuum['record_selection_status'] != 'Q63_STRICT_OCCUPANCY_SECTOR_SELECTED':
        raise RuntimeError('Vacuum global-background qualification missing')
    bounds = vacuum['global_vacuum_interval']
    if not frac(bounds['lower']) < frac(bounds['upper']):
        raise RuntimeError('Vacuum interval order invalid')
    inputs = {'direct_input_sha256':direct,'vacuum_report_sha256':vacuum_report_hash,
              'vacuum_checkpoint_sha256':vacuum_cp,'vacuum_journal_prefix_sha256':vacuum_prefix,
              'inherited_direct_input_sha256':inherited_direct,'inherited_root_input_sha256':inherited_root,
              'inherited_finite_checkpoint_sha256':finite_cp,'inherited_finite_report_sha256':finite_report_hash,
              'inherited_finite_journal_prefix_sha256':finite_prefix,
              'preserved_finite_stage_alias':inherited['preserved_base_stage_alias']}
    return inputs,bounds


def index(q,n,v):
    return 6*(64*q+n)+v


def physical_diagonal20(q,n,v):
    total = 0
    for u in range(6):
        degree = 1+((n>>((u-1)%6))&1)+((n>>u)&1)
        total += 20*(degree-2)**2+((q>>u)&1)*(20-10*degree)
    degree_carrier = 1+((n>>((v-1)%6))&1)+((n>>v)&1)
    return total+20+5*degree_carrier


def build_action():
    diagonal,ports = [],[]
    physical_equal,reciprocal,port_weights = True,True,True
    for q in range(64):
        for n in range(64):
            background20 = 0
            for u in range(6):
                delta = ((n>>((u-1)%6))&1)+((n>>u)&1)-1
                background20 += 20*delta*delta-10*((q>>u)&1)*delta
            for v in range(6):
                degree = 1+((n>>((v-1)%6))&1)+((n>>v)&1)
                d = background20+20+5*degree
                diagonal.append(d)
                physical_equal = physical_equal and d == physical_diagonal20(q,n,v)
                row = [(index(q,n^(1<<e),v),-4,'incidence') for e in range(6)]
                for e,dest in (((v-1)%6,(v-1)%6),(v,(v+1)%6)):
                    if n&(1<<e):
                        row.append((index(q,n,dest),-2,'carrier'))
                row.append((index(q^(1<<v),n,v),-2,'copy'))
                ports.append(row)
                port_weights = port_weights and len({j for j,w,k in row}) == len(row) and all(w<0 for j,w,k in row)
    for i,row in enumerate(ports):
        for j,w,kind in row:
            reciprocal = reciprocal and (i,w,kind) in ports[j]
    checks = []
    add(checks,'full_dimension24576',len(diagonal)==len(ports)==DIM)
    add(checks,'all_complete_physical_diagonals_equal',physical_equal)
    add(checks,'all_ports_reciprocal',reciprocal)
    add(checks,'negative_unique_offdiagonal_ports',port_weights)
    add(checks,'all_diagonals_at_least25',min(diagonal)>=25)
    add(checks,'all_diagonals_at_most205',max(diagonal)<=205)
    for q,n,v,wanted in ((0,0,0,145),(63,0,0,205),(63,63,0,95),(63,21,0,30)):
        add(checks,f'hand_diag_q{q}_n{n}_v{v}',diagonal[index(q,n,v)]==wanted)
    stage = {'basis_order':'i=6(64q+n)+v','dimension':DIM,'diagonal20':diagonal,
             'offdiagonal_port_count':sum(len(row) for row in ports),
             'diagonal_min':min(diagonal),'diagonal_max':max(diagonal),
             'exterior_current20':5,'record_parity_copy_unitary':True,'checks':list(checks)}
    return diagonal,ports,stage,checks


def float_h(x,diagonal):
    global FLOAT_ACTION_CALLS
    FLOAT_ACTION_CALLS += 1
    state = np.asarray(x,dtype=float).reshape(64,64,6)
    out = np.asarray(diagonal,dtype=float).reshape(64,64,6)*state
    words = np.arange(64)
    for e in range(6):
        out -= 4*state[:,words^(1<<e),:]
        occupied = ((words>>e)&1).astype(float)
        out[:,:,e] -= 2*occupied[None,:]*state[:,:,(e+1)%6]
        out[:,:,(e+1)%6] -= 2*occupied[None,:]*state[:,:,e]
    for v in range(6):
        out[:,:,v] -= 2*state[words^(1<<v),:,v]
    return out.reshape(DIM)/20


def round_ratio_even(a,b):
    quotient,remainder = divmod(a,b)
    if 2*remainder>b or (2*remainder==b and quotient%2):
        quotient += 1
    return quotient


def rounding_controls():
    checks = []
    for a,b,wanted in ((1,2,0),(3,2,2),(5,2,2),(7,2,4),(9,4,2),(11,4,3)):
        add(checks,f'nearest_even_{a}_{b}',round_ratio_even(a,b)==wanted)
    for value,wanted in ((0.5,ROUND_SCALE//2),(0.25,ROUND_SCALE//4),(1.0,ROUND_SCALE)):
        a,b = value.as_integer_ratio()
        add(checks,'exact_binary_float_round_'+value.hex(),round_ratio_even(a*ROUND_SCALE,b)==wanted)
    return {'round_scale':ROUND_SCALE,'tie_rule':'nearest_even_by_exact_as_integer_ratio_divmod','checks':list(checks)},checks


def save_float_state(iteration,x,p_previous,diagnostics):
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(p_previous)) or np.min(x)<=0:
        raise ArithmeticError('Nonfinite/nonpositive floating proposal at iteration '+str(iteration))
    obj = {'iteration':iteration,'basis_order':'i=6(64q+n)+v',
           'x_hex':[float(value).hex() for value in x],
           'p_previous_hex':[float(value).hex() for value in p_previous],
           'x_squared_norm':float(np.dot(x,x)),'x_min':float(np.min(x)),
           'diagnostics_trial_only':diagnostics,'elapsed_seconds':time.perf_counter()-T0}
    return save(f'iteration_{iteration:04d}_float_state.json',obj,iteration=iteration)


def optimizer_step(x,p_previous,diagonal):
    hx = float_h(x,diagonal)
    rq = float(np.dot(x,hx))
    residual = hx-rq*x
    basis,kept,dropped = [],[],[]
    for label,column in (('x',x),('residual',residual),('p_previous',p_previous)):
        candidate = column.copy()
        for existing in basis:
            candidate -= float(np.dot(existing,candidate))*existing
        norm = float(np.linalg.norm(candidate))
        if not math.isfinite(norm):
            raise ArithmeticError('Nonfinite MGS column norm')
        if norm <= DROP_NORM:
            dropped.append(label)
        else:
            basis.append(candidate/norm)
            kept.append(label)
    if not basis:
        raise ArithmeticError('Empty frozen projected subspace')
    projected = np.empty((len(basis),len(basis)),dtype=float)
    for j in range(len(basis)):
        action = float_h(basis[j],diagonal)
        for i in range(j+1):
            value = float(np.dot(basis[i],action))
            projected[i,j] = projected[j,i] = value
    if not np.all(np.isfinite(projected)):
        raise ArithmeticError('Nonfinite projected trial matrix')
    values,vectors = np.linalg.eigh(projected)
    trial = sum((vectors[j,0]*basis[j] for j in range(len(basis))),np.zeros(DIM,dtype=float))
    trial = np.maximum(np.abs(trial),POSITIVE_FLOOR)
    norm = float(np.linalg.norm(trial))
    if not math.isfinite(norm) or norm<=0:
        raise ArithmeticError('Nonfinite/zero absolute proposal norm')
    newx = trial/norm
    newp = newx-float(np.dot(x,newx))*x
    if not np.all(np.isfinite(newx)) or not np.all(np.isfinite(newp)) or np.min(newx)<=0:
        raise ArithmeticError('Nonfinite/nonpositive normalized proposal')
    gram = np.array([[float(np.dot(a,b)) for b in basis] for a in basis])
    diagnostics = {'rayleigh_before_trial':rq,'residual_norm_before_trial':float(np.linalg.norm(residual)),
                   'retained_columns':kept,'dropped_columns':dropped,'projected_dimension':len(basis),
                   'projected_eigenvalues_trial_only':[float(value) for value in values],
                   'max_MGS_Gram_error':float(np.max(np.abs(gram-np.eye(len(basis))))),
                   'numpy_eigensolve_dimension_at_most3':True}
    return newx,newp,diagnostics


def integer_apply(z,diagonal,ports):
    return [diagonal[i]*z[i]+sum(w*z[j] for j,w,kind in ports[i]) for i in range(DIM)]


def independent_quadratic(z,diagonal):
    total = sum(diagonal[i]*z[i]*z[i] for i in range(DIM))
    for q in range(64):
        for n in range(64):
            for e in range(6):
                if not n&(1<<e):
                    for v in range(6):
                        total -= 8*z[index(q,n,v)]*z[index(q,n^(1<<e),v)]
                else:
                    total -= 4*z[index(q,n,e)]*z[index(q,n,(e+1)%6)]
            for v in range(6):
                if not q&(1<<v):
                    total -= 4*z[index(q,n,v)]*z[index(q^(1<<v),n,v)]
    return total


def certificate(iteration,x,diagonal,ports,vacuum_bounds):
    rounded = []
    floor_count = 0
    for value in x:
        a,b = float(value).as_integer_ratio()
        candidate = round_ratio_even(a*ROUND_SCALE,b)
        if candidate == 0:
            candidate = 1
            floor_count += 1
        rounded.append(candidate)
    mz = integer_apply(rounded,diagonal,ports)
    min_index,max_index = 0,0
    for i in range(1,DIM):
        if mz[i]*rounded[min_index] < mz[min_index]*rounded[i]:
            min_index = i
        if mz[i]*rounded[max_index] > mz[max_index]*rounded[i]:
            max_index = i
    lower = Fraction(mz[min_index],20*rounded[min_index])
    cw_upper = Fraction(mz[max_index],20*rounded[max_index])
    quadratic = sum(a*b for a,b in zip(rounded,mz))
    norm = sum(a*a for a in rounded)
    upper = Fraction(quadratic,20*norm)
    checks = []
    add(checks,f'iter{iteration}_positive_full_integer_vector',len(rounded)==DIM and min(rounded)>0)
    add(checks,f'iter{iteration}_integer_action_dimension',len(mz)==DIM and all(isinstance(a,int) for a in mz))
    add(checks,f'iter{iteration}_independent_undirected_quadratic',quadratic==independent_quadratic(rounded,diagonal))
    add(checks,f'iter{iteration}_CW_Rayleigh_order',lower<=upper<=cw_upper)
    vector = {'iteration':iteration,'basis_order':'i=6(64q+n)+v','round_scale':ROUND_SCALE,
              'z':rounded,'Mz':mz,'rounded_zero_floor_count':floor_count,
              'exact_quadratic_z_Mz':quadratic,'exact_squared_norm_z':norm}
    vector_hash = save(f'iteration_{iteration:04d}_integer_vector.json',vector,iteration=iteration)
    row = {'iteration':iteration,'integer_vector_filename':f'iteration_{iteration:04d}_integer_vector.json',
           'integer_vector_sha256':vector_hash,'ground_interval_raw':interval(lower,upper),
           'CW_ratio_interval_raw':interval(lower,cw_upper),'rayleigh_upper':exact(upper),
           'minimum_ratio_witness':{'index':min_index,'Mz_i':mz[min_index],'z_i':rounded[min_index],'ratio':exact(lower)},
           'maximum_ratio_witness':{'index':max_index,'Mz_i':mz[max_index],'z_i':rounded[max_index],'ratio':exact(cw_upper)},
           'matched_addition_interval_raw':interval(lower-frac(vacuum_bounds['upper']),upper-frac(vacuum_bounds['lower'])),
           'target_energy_width':exact(TARGET),'raw_target_width_candidate':upper-lower<=TARGET,
           'rounded_zero_floor_count':floor_count,'checks':list(checks),
           'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    return row,lower,upper,checks


def independent_addition_theorem():
    lo,hi = Fraction(7),Fraction(8)
    for step in range(128):
        mid = (lo+hi)/2
        if mid*mid<=53:
            lo = mid
        else:
            hi = mid
    lower = Fraction(23,20)
    upper_expression_lo = Fraction(19,10)-hi/20
    upper_expression_hi = Fraction(19,10)-lo/20
    checks = []
    add(checks,'sqrt53_rational_endpoint_squares',lo*lo<=53<=hi*hi)
    add(checks,'sqrt53_128_fixed_steps',hi-lo==Fraction(1,2**128))
    add(checks,'independent_addition_bound_order',lower<upper_expression_lo<=upper_expression_hi)
    return {'matched_addition_lower':exact(lower),'matched_addition_upper_expression':'19/10-sqrt(53)/20',
            'sqrt53_rational_enclosure':interval(lo,hi),'upper_expression_rational_enclosure':interval(upper_expression_lo,upper_expression_hi),
            'finite_h_no_pole_claim':True,'checks':list(checks)},checks


def report_text(result):
    def rat(value):
        return str(value['numerator'])+'/'+str(value['denominator'])
    lines = ['# Held hexagon: complete carrier/copy ground certificate V001','',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             'Certificate status: '+result['ground_certificate_status']+'.',
             'Requested precision status: '+result['requested_precision_status']+'.','',
             '| completed fixed stage | raw joint lower | raw joint upper | raw width | raw addition lower | raw addition upper |',
             '|---:|---:|---:|---:|---:|---:|']
    for row in result['certificate_stages']:
        joint,addition = row['ground_interval_raw'],row['matched_addition_interval_raw']
        lines.append(f"| {row['iteration']} | "+rat(joint['lower'])+' | '+rat(joint['upper'])+' | '+rat(joint['width'])+' | '+rat(addition['lower'])+' | '+rat(addition['upper'])+' |')
    final,addition = result['final_ground_interval_raw'],result['final_matched_addition_interval_raw']
    theorem = result['independent_held_addition_theorem']
    lines += ['', 'Final raw joint interval: ['+rat(final['lower'])+', '+rat(final['upper'])+'].',
              'Final raw matched addition: ['+rat(addition['lower'])+', '+rat(addition['upper'])+'].',
              'Independent complete-action theorem: 23/20 <= addition <= 19/10-sqrt(53)/20; its upper expression is enclosed by ['+
              rat(theorem['upper_expression_rational_enclosure']['lower'])+', '+rat(theorem['upper_expression_rational_enclosure']['upper'])+'].',
              'The raw interval is not clipped to that theorem. The vacuum is the authenticated all64-q global background; no second background subtraction occurs in H.',
              '', 'The optimizer proposes positive trials only. Exact arbitrary-precision Mz, Collatz-Wielandt and Rayleigh fractions earn the energy bounds. Every fixed-stage lossless float and integer vector is sealed for recovery; no full dense joint matrix, propagation, old producer, ancestor eigensolve or base inertia replay is used.',
              'Native copying is retained on all24576 states. Its negative sign is solely record-parity unitary conjugation; any later physical source/readout must be conjugated as well.',
              'A finite held energy certificate does not establish a matter pole/residue, transport curvature, physical clock/ruler, 3D metric, bulk phase, gravity, expansion or superiority. Unearned requested precision remains explicit; no optimizer fallback, parameter retune or automatic rerun.',
              '',f"Elapsed seconds: {result['elapsed_seconds']}; native peak RSS: {result['ru_maxrss_native']}.",'']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    if sys.argv[1:] != ['--execute']:
        raise RuntimeError('Explicit --execute required; no calculation launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs,vacuum_bounds = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
                'authenticated_inputs':inputs,'dimension':DIM,'parameters':{'EP':exact(1),'j':exact(Fraction(1,4)),'t':exact(Fraction(1,10)),'g_native':exact(Fraction(1,10)),'h_local':exact(Fraction(1,5))},
                'record_parity_negative_copy_unitary':True,'basis_order':'i=6(64q+n)+v',
                'optimizer_frozen':{'maximum_iterations':MAX_ITERATIONS,'certificate_stages':list(CERTIFICATE_STAGES),
                 'drop_norm':DROP_NORM,'positive_float_floor':POSITIVE_FLOOR,'round_scale':ROUND_SCALE,'round_rule':'nearest_even_exact_as_integer_ratio',
                 'target_energy_width':exact(TARGET),'MGS_passes':1,'column_order':['x','residual','p_previous'],'fallback':False},
                'numpy_version':np.__version__,'environment':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')}}
    manifest_hash = save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    diagonal,ports,structure,checks = build_action()
    ones_integer = integer_apply([1]*DIM,diagonal,ports)
    ones_float = float_h(np.ones(DIM,dtype=float),diagonal)
    uniform_error = float(np.max(np.abs(ones_float-np.array(ones_integer,dtype=float)/20)))
    add(checks,'uniform_float_action_matches_exact_integer_row_sum',uniform_error<=1e-12)
    structure['uniform_float_action_max_error'] = uniform_error
    structure['checks'] = list(checks)
    save('complete_action_controls.json',structure)
    checks = list(checks)
    rounding,extra = rounding_controls()
    save('nearest_even_rounding_controls.json',rounding)
    checks.extend(extra)
    theorem,extra = independent_addition_theorem()
    save('independent_held_addition_theorem.json',theorem)
    checks.extend(extra)
    if any(not check['passed'] for check in checks):
        raise ArithmeticError('Pre-optimization action/arithmetic control failed; preserve attempt')
    x = np.full(DIM,1/math.sqrt(DIM),dtype=float)
    p_previous = np.zeros(DIM,dtype=float)
    initial_hash = save_float_state(0,x,p_previous,{'initial_uniform_positive':True})
    rows,precision_earned,last_diagnostics = [],False,{}
    for iteration in range(1,MAX_ITERATIONS+1):
        x,p_previous,last_diagnostics = optimizer_step(x,p_previous,diagonal)
        if iteration not in CERTIFICATE_STAGES:
            continue
        float_hash = save_float_state(iteration,x,p_previous,last_diagnostics)
        row,lower,upper,extra = certificate(iteration,x,diagonal,ports,vacuum_bounds)
        row['float_state_filename'] = f'iteration_{iteration:04d}_float_state.json'
        row['float_state_sha256'] = float_hash
        checks.extend(extra)
        row['controls_failed_through_stage'] = sum(not check['passed'] for check in checks)
        row['target_width_earned_through_stage'] = row['raw_target_width_candidate'] and row['controls_failed_through_stage']==0
        save(f'iteration_{iteration:04d}_energy_certificate.json',row,iteration=iteration)
        rows.append(row)
        print(json.dumps({'pid':os.getpid(),'iteration':iteration,'raw_width_decimal20_upper':row['ground_interval_raw']['width']['decimal20_upper'],
                          'stage_controls_failed':row['controls_failed_through_stage'],'elapsed_seconds':time.perf_counter()-T0}),flush=True)
        if row['target_width_earned_through_stage']:
            precision_earned = True
            break
    if not rows:
        raise ArithmeticError('Frozen optimizer produced no exact certificate stage')
    final = rows[-1]
    addition = final['matched_addition_interval_raw']
    add(checks,'declared_completed_stage_census',all(row['iteration'] in CERTIFICATE_STAGES for row in rows) and [row['iteration'] for row in rows]==list(CERTIFICATE_STAGES[:len(rows)]))
    add(checks,'no_iteration_beyond4096',iteration<=MAX_ITERATIONS)
    add(checks,'final_raw_addition_overlaps_independent_theorem',frac(addition['lower'])<=frac(theorem['upper_expression_rational_enclosure']['upper']) and frac(addition['upper'])>=frac(theorem['matched_addition_lower']))
    final_inputs,final_vacuum = authenticate()
    add(checks,'all_frozen_input_checkpoint_report_bytes_unchanged',final_inputs==inputs and final_vacuum==vacuum_bounds)
    add(checks,'source_protocol_bytes_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'structural_stage_check_list_unchanged',structure['checks']==checks[:len(structure['checks'])])
    failed = sum(not check['passed'] for check in checks)
    result = {'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'ground_certificate_status':'FULL_HELD_GROUND_INTERVAL_CERTIFIED' if not failed else 'RAW_INTERVAL_ARITHMETIC_UNQUALIFIED',
              'requested_precision_status':('TARGET_WIDTH_EARNED' if precision_earned else 'TARGET_WIDTH_UNEARNED_VALID_INTERVAL_PRESERVED') if not failed else 'PRECISION_ARITHMETIC_UNQUALIFIED',
              'raw_target_precision_candidate':final['raw_target_width_candidate'],'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
              'authenticated_inputs':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),
              'dimension':DIM,'basis_order':'i=6(64q+n)+v','complete_action_controls':structure,
              'rounding_controls':rounding,'independent_held_addition_theorem':theorem,
              'global_vacuum_interval_authenticated':vacuum_bounds,'initial_float_state_sha256':initial_hash,
              'certificate_stages':rows,'final_ground_interval_raw':final['ground_interval_raw'],
              'final_matched_addition_interval_raw':addition,'iterations_completed':iteration,
              'floating_H_action_calls':FLOAT_ACTION_CALLS,'maximum_projected_eigensolve_dimension':3,
              'base_matrix_eigensolve_or_inertia_replay':False,'full_dense_joint_matrix_constructed':False,
              'bulk_phase_pole_curvature_clock_metric_gravity_expansion_claim':False,
              'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = report_text(result)
    table = report.split('| completed fixed stage |',1)[1].split('Final raw joint interval:',1)[0]
    if table.count('\n| ') != len(rows):
        raise RuntimeError('Report completed-stage DATA row count mismatch')
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
               'checkpoint_sha256':dict(STAGES),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
               'authenticated_inputs':inputs,'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],'checks_failed':failed,
               'ground_certificate_status':result['ground_certificate_status'],'requested_precision_status':result['requested_precision_status'],
               'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'ground_certificate_status':result['ground_certificate_status'],
                      'requested_precision_status':result['requested_precision_status'],'checks_passed':result['checks_passed'],
                      'checks_total':result['checks_total'],'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
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
