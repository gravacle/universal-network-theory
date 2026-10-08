#!/usr/bin/env python3
"""New complete nonuniform full-copy source; no ancestor is imported."""
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
NAME = 'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J/(NAME+'.md')
RESULT = J/(NAME+'_RESULT.json')
REPORT = J/(NAME+'_RESULT.md')
RECEIPT = J/(NAME+'_RECEIPT.json')
CP = J/'bs10_record_feedback_hex_joint_source_v001_checkpoints'
VAC = 'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001'
VAC_CP = J/'bs10_record_feedback_hex_vacuum_v001_checkpoints'
BASE = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
BASE_CP = J/'bs10_record_feedback_hex_finite_v001_checkpoints'
JOINT = 'BS10_RECORD_FEEDBACK_HEX_JOINT_V001'
JOINT_CP = J/'bs10_record_feedback_hex_joint_v001_checkpoints'
Q63 = 'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001'
Q63_CP = J/'bs10_record_feedback_hex_source_v001_checkpoints'
SCALE = 1600
ALPHA = Fraction(1,20)
L_PLUS = (42,41,39,38,39,41)
L_MINUS = tuple(80-a for a in L_PLUS)
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
    'bs10_record_feedback_hex_joint_v001.py':'d27bc48797b49f9c8a27eee43667dafdfc71f404217153cf0e9f0afb17a97cc6',
    'BS10_RECORD_FEEDBACK_HEX_JOINT_V001.md':'1c4bf052ee95773b73d5d823fdb04a316effba469f458eca382ad52389b7cd81',
    'BS10_RECORD_FEEDBACK_HEX_JOINT_V001_RESULT.json':'ec4b754ae9ec867068f68210ad67d17546ad5b5265e1c92baee4b63b765344fd',
    'BS10_RECORD_FEEDBACK_HEX_JOINT_V001_RECEIPT.json':'92719713b13fcc12e7c4bd6c8e1a2352d9cfee3abac0564c9a0624f491a0a868',
    'bs10_record_feedback_hex_source_v001.py':'d34b49b525618034e43c2c865dba5481244675fdb3495d8437c64842f1471be3',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001.md':'e94072efdbe4944d9307e9c4dd3335feb7338dcfa5f3e7ff4506482761efee92',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001_RESULT.json':'98cc4454e6cb044e770a8e2bb21559e6fcba1a365ae36858d187fdcf7fe67ae3',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001_RECEIPT.json':'bfc6852ece20655d4b6cbb90212e1eb961344baaa43f4bdcf12c41d5ce7e39a7',
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



def verify_map(mapping,base,label):
    out = {}
    for name,wanted in mapping.items():
        got = sha(base/name)
        if got != wanted:
            raise RuntimeError(label+' changed: '+name)
        out[name] = got
    return out


def authenticate_packet(tag,directory,source_name,expected):
    result = json.loads((J/(tag+'_RESULT.json')).read_text())
    receipt = json.loads((J/(tag+'_RECEIPT.json')).read_text())
    raw_hash,receipt_hash = sha(J/(tag+'_RESULT.json')),sha(J/(tag+'_RECEIPT.json'))
    if raw_hash != expected[tag+'_RESULT.json'] or receipt_hash != expected[tag+'_RECEIPT.json']:
        raise RuntimeError('Parent raw/receipt anchor mismatch: '+tag)
    if receipt['result_raw_sha256'] != raw_hash or receipt['result_canonical_sha256'] != hashlib.sha256(canonical(result)).hexdigest():
        raise RuntimeError('Parent raw/canonical receipt mismatch: '+tag)
    report_hash = sha(J/(tag+'_RESULT.md'))
    if report_hash != receipt['report_sha256']:
        raise RuntimeError('Parent report mismatch: '+tag)
    for key,name in (('source_sha256',source_name),('protocol_sha256',tag+'.md')):
        if not(result[key]==receipt[key]==expected[name]==sha(J/name)):
            raise RuntimeError('Parent source/protocol mismatch: '+tag)
    input_key = 'authenticated_inputs' if 'authenticated_inputs' in receipt else 'input_sha256'
    if result[input_key] != receipt[input_key] or result['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Parent input/checkpoint equality mismatch: '+tag)
    checkpoints = verify_map(receipt['checkpoint_sha256'],directory,'Parent checkpoint '+tag)
    if not(result['manifest_sha256']==receipt['manifest_sha256']==checkpoints['input_manifest.json']):
        raise RuntimeError('Parent manifest map mismatch: '+tag)
    manifest = json.loads((directory/'input_manifest.json').read_text())
    if manifest['source_sha256'] != receipt['source_sha256'] or manifest['protocol_sha256'] != receipt['protocol_sha256']:
        raise RuntimeError('Parent manifest code pins mismatch: '+tag)
    if input_key in manifest and manifest[input_key] != receipt[input_key]:
        raise RuntimeError('Parent manifest input payload mismatch: '+tag)
    prefix = verify_parent_journal(directory,receipt,receipt_hash,checkpoints,checkpoints['input_manifest.json'])
    if result['checks_failed'] != 0 or receipt['checks_failed'] != 0:
        raise RuntimeError('Parent arithmetic premise missing: '+tag)
    proof = {'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'report_sha256':report_hash,
             'checkpoint_sha256':checkpoints,'journal_prefix_sha256':prefix,'authenticated_inputs':receipt[input_key]}
    return proof,result


def authenticate():
    direct = verify_map(INPUTS,J,'Frozen direct input')
    joint_proof,joint = authenticate_packet(JOINT,JOINT_CP,'bs10_record_feedback_hex_joint_v001.py',direct)
    source_proof,q63 = authenticate_packet(Q63,Q63_CP,'bs10_record_feedback_hex_source_v001.py',direct)
    ji,si = joint_proof['authenticated_inputs'],source_proof['authenticated_inputs']
    inherited = {}
    for label,mapping,base in (
        ('joint_direct',ji['direct_input_sha256'],J),
        ('joint_inherited_direct',ji['inherited_direct_input_sha256'],J),
        ('joint_root',ji['inherited_root_input_sha256'],ROOT),
        ('joint_finite_cp',ji['inherited_finite_checkpoint_sha256'],BASE_CP),
        ('joint_vacuum_cp',ji['vacuum_checkpoint_sha256'],VAC_CP),
        ('source_direct',si['direct_input_sha256'],J),
        ('source_root',si['inherited_input_sha256'],ROOT),
        ('source_finite_cp',si['base_checkpoint_sha256'],BASE_CP)):
        inherited[label] = verify_map(mapping,base,'Inherited '+label)
    vacuum_proof,vacuum = authenticate_packet(VAC,VAC_CP,'bs10_record_feedback_hex_vacuum_v001.py',ji['direct_input_sha256'])
    finite_proof,finite = authenticate_packet(BASE,BASE_CP,'bs10_record_feedback_hex_finite_v001.py',si['direct_input_sha256'])
    if vacuum_proof['report_sha256'] != ji['vacuum_report_sha256'] or vacuum_proof['journal_prefix_sha256'] != ji['vacuum_journal_prefix_sha256']:
        raise RuntimeError('Inherited vacuum report/prefix mismatch')
    if finite_proof['report_sha256'] != ji['inherited_finite_report_sha256'] or finite_proof['report_sha256'] != si['base_report_sha256']:
        raise RuntimeError('Inherited finite report mismatch')
    if finite_proof['journal_prefix_sha256'] != ji['inherited_finite_journal_prefix_sha256'] or finite_proof['journal_prefix_sha256'] != si['base_journal_prefix_sha256']:
        raise RuntimeError('Inherited finite prefix mismatch')
    if finite_proof['authenticated_inputs'] != ji['inherited_root_input_sha256'] or finite_proof['authenticated_inputs'] != si['inherited_input_sha256']:
        raise RuntimeError('Inherited finite inputs mismatch')
    if vacuum_proof['checkpoint_sha256'] != ji['vacuum_checkpoint_sha256'] or finite_proof['checkpoint_sha256'] != ji['inherited_finite_checkpoint_sha256'] or finite_proof['checkpoint_sha256'] != si['base_checkpoint_sha256']:
        raise RuntimeError('Inherited parent checkpoint maps mismatch')
    structure = json.loads((BASE_CP/'structure.json').read_text())
    prefix,alias = structure['checks'],finite['structural_checks']['checks']
    if prefix != alias[:len(prefix)]:
        raise RuntimeError('Preserved finite stage-check alias mismatch')
    if ji['preserved_finite_stage_alias'] != {'prefix_count':len(prefix),'nested_count':len(alias),'prefix_equal':True}:
        raise RuntimeError('Joint finite alias metadata mismatch')
    if si['preserved_base_check_alias'] != {'checkpoint_count':len(prefix),'result_nested_count':len(alias),'prefix_equal':True}:
        raise RuntimeError('Source finite alias metadata mismatch')
    if joint['ground_certificate_status'] != 'FULL_HELD_GROUND_INTERVAL_CERTIFIED' or not vacuum['q63_strict_selected'] or not q63['chi0_strictly_positive_qualitative_only']:
        raise RuntimeError('Sealed reference qualification missing')
    if joint['global_vacuum_interval_authenticated'] != vacuum['global_vacuum_interval'] or q63['base_E0_interval'] != vacuum['global_vacuum_interval']:
        raise RuntimeError('Shared zero-source reference mismatch')
    inputs = {'direct_input_sha256':direct,'joint_parent':joint_proof,'q63_source_parent':source_proof,
              'inherited_current_bytes':inherited,'vacuum_parent':vacuum_proof,'finite_parent':finite_proof,
              'preserved_finite_stage_alias':ji['preserved_finite_stage_alias']}
    references = {'E10':joint['final_ground_interval_raw'],'Ebg0':vacuum['global_vacuum_interval'],
                  'Delta0':joint['final_matched_addition_interval_raw'],'Ebg63alpha':q63['new_Ealpha_interval'],
                  'Fbg63':q63['Falpha_interval'],'old20H_diagonal':joint['complete_action_controls']['diagonal20'],
                  'q63_source_structure':q63['source_structure']}
    return inputs,references


def index(q,n,v):
    return 6*(64*q+n)+v



def background1600(q,n,l):
    total = 0
    for u in range(6):
        a,b = (n>>((u-1)%6))&1,(n>>u)&1
        delta = a+b-1
        c160 = -4*l[u]+a*(l[(u-1)%6]+l[u])+b*(l[u]+l[(u+1)%6])+(l[u]+40)
        total += 40*l[u]*delta*delta-20*l[u]*delta+10*(1-((q>>u)&1))*c160
    return total


def source_diagonal(q,n,v,l):
    a,b = (n>>((v-1)%6))&1,(n>>v)&1
    return background1600(q,n,l)+40*l[v]+5*(a*(l[(v-1)%6]+l[v])+b*(l[v]+l[(v+1)%6])+(l[v]+40))


def physical_diagonal1600(q,n,v,l):
    total = 4800
    for u in range(6):
        delta = ((n>>((u-1)%6))&1)+((n>>u)&1)-1
        bit = (q>>u)&1
        total += 40*l[u]*delta*delta+40*l[u]*bit-10*(l[u]+40)*(bit+1)
    for e in range(6):
        total -= 10*(l[e]+l[(e+1)%6])*((n>>e)&1)*(((q>>e)&1)+((q>>((e+1)%6))&1))
    a,b = (n>>((v-1)%6))&1,(n>>v)&1
    return total+40*l[v]+5*(a*(l[(v-1)%6]+l[v])+b*(l[v]+l[(v+1)%6])+(l[v]+40))


def rotate3(word):
    return sum(((word>>u)&1)<<((u+3)%6) for u in range(6))


def action_ports(q,n,v,l):
    row = [(index(q,n^(1<<e),v),-4*(l[e]+l[(e+1)%6]),'incidence') for e in range(6)]
    for e,dest in (((v-1)%6,(v-1)%6),(v,(v+1)%6)):
        if n&(1<<e):
            row.append((index(q,n,dest),-2*(l[e]+l[(e+1)%6]),'carrier'))
    row.append((index(q^(1<<v),n,v),-4*l[v],'copy'))
    return row


def build_action(references):
    diagonal,ports = [],[]
    physical_equal,reciprocal,negative_unique,r3_diag,r3_ports,uniform_reduction = True,True,True,True,True,True
    for q in range(64):
        for n in range(64):
            for v in range(6):
                i = index(q,n,v)
                d = source_diagonal(q,n,v,L_PLUS)
                row = action_ports(q,n,v,L_PLUS)
                diagonal.append(d)
                ports.append(row)
                physical_equal = physical_equal and d == physical_diagonal1600(q,n,v,L_PLUS)
                uniform_reduction = uniform_reduction and source_diagonal(q,n,v,(40,)*6)==80*references['old20H_diagonal'][i]
                negative_unique = negative_unique and len({a for a,b,c in row})==len(row) and all(b<0 for a,b,c in row)
                qr,nr,vr = rotate3(q),rotate3(n),(v+3)%6
                r3_diag = r3_diag and d == source_diagonal(qr,nr,vr,L_MINUS)
                mapped = []
                for dest,weight,kind in row:
                    qdest,tail = divmod(dest,64*6)
                    ndest,vdest = divmod(tail,6)
                    mapped.append((index(rotate3(qdest),rotate3(ndest),(vdest+3)%6),weight,kind))
                r3_ports = r3_ports and sorted(mapped)==sorted(action_ports(qr,nr,vr,L_MINUS))
    for i,row in enumerate(ports):
        for dest,weight,kind in row:
            reciprocal = reciprocal and (i,weight,kind) in ports[dest]
    checks = []
    add(checks,'full_dimension24576',len(diagonal)==len(ports)==DIM)
    add(checks,'all_complete_physical_diagonals_equal',physical_equal)
    add(checks,'all_ports_reciprocal',reciprocal)
    add(checks,'negative_unique_offdiagonal_ports',negative_unique)
    add(checks,'all_uniform_reference_diagonals80times_sealed20H',uniform_reduction)
    add(checks,'R3_all24576_diagonals',r3_diag)
    add(checks,'R3_all_ports',r3_ports)
    add(checks,'clamped_exterior_feedback_constant_derived_zero',sum(value-40 for value in L_PLUS)==0)
    add(checks,'all_source_nodes_positive',min(L_PLUS)>0)
    for q,n,v,wanted in ((0,0,0,11690),(63,0,0,16490),(63,63,0,7720),(63,21,0,2505),(62,21,0,2475)):
        add(checks,f'hand_diag_q{q}_n{n}_v{v}',diagonal[index(q,n,v)]==wanted)
    old = references['q63_source_structure']
    add(checks,'all_q63_source_background_diagonals_reused_coefficients',all(background1600(63,n,L_PLUS)==SCALE*frac(old['new_Halpha_diagonal'][n]) for n in range(64)))
    add(checks,'all_q63_source_flip_edges_reused_coefficients',all(-4*(L_PLUS[(a^b).bit_length()-1]+L_PLUS[((a^b).bit_length())%6])==SCALE*frac(value) for a,b,value in old['new_Halpha_edges']))
    stage = {'basis_order':'i=6(64q+n)+v','dimension':DIM,'integer_scale':SCALE,
             'L_plus_numerators_over40':list(L_PLUS),'L_minus_numerators_over40':list(L_MINUS),
             'diagonal1600':diagonal,'offdiagonal_port_count':sum(len(row) for row in ports),
             'inactive_exterior_reference1600':4800,'derived_clamped_exterior_feedback_constant1600':-10*sum(value-40 for value in L_PLUS),
             'R3_permutation':[index(rotate3(q),rotate3(n),(v+3)%6) for q in range(64) for n in range(64) for v in range(6)],
             'direct_second_alpha_contact':0,'record_parity_copy_unitary':True,'checks':list(checks)}
    return diagonal,ports,stage,checks



def float_h(x,diagonal):
    global FLOAT_ACTION_CALLS
    FLOAT_ACTION_CALLS += 1
    state = np.asarray(x,dtype=float).reshape(64,64,6)
    out = np.asarray(diagonal,dtype=float).reshape(64,64,6)*state
    words = np.arange(64)
    for e in range(6):
        bond = L_PLUS[e]+L_PLUS[(e+1)%6]
        out -= 4*bond*state[:,words^(1<<e),:]
        occupied = ((words>>e)&1).astype(float)
        out[:,:,e] -= 2*bond*occupied[None,:]*state[:,:,(e+1)%6]
        out[:,:,(e+1)%6] -= 2*bond*occupied[None,:]*state[:,:,e]
    for v in range(6):
        out[:,:,v] -= 4*L_PLUS[v]*state[words^(1<<v),:,v]
    return out.reshape(DIM)/SCALE


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
                bond = L_PLUS[e]+L_PLUS[(e+1)%6]
                if not n&(1<<e):
                    for v in range(6):
                        total -= 8*bond*z[index(q,n,v)]*z[index(q,n^(1<<e),v)]
                else:
                    total -= 4*bond*z[index(q,n,e)]*z[index(q,n,(e+1)%6)]
            for v in range(6):
                if not q&(1<<v):
                    total -= 8*L_PLUS[v]*z[index(q,n,v)]*z[index(q^(1<<v),n,v)]
    return total


def certificate(iteration,x,diagonal,ports,references):
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
    lower = Fraction(mz[min_index],SCALE*rounded[min_index])
    cw_upper = Fraction(mz[max_index],SCALE*rounded[max_index])
    quadratic = sum(a*b for a,b in zip(rounded,mz))
    norm = sum(a*a for a in rounded)
    upper = Fraction(quadratic,SCALE*norm)
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
           'retained63_addition_interval_raw':interval(lower-frac(references['Ebg63alpha']['upper']),upper-frac(references['Ebg63alpha']['lower'])),
           'target_energy_width':exact(TARGET),'raw_target_width_candidate':upper-lower<=TARGET,
           'rounded_zero_floor_count':floor_count,'checks':list(checks),
           'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    return row,lower,upper,checks



def finite_source_assembly(joint_alpha,references):
    a2 = ALPHA*ALPHA
    lo,hi = frac(joint_alpha['lower']),frac(joint_alpha['upper'])
    e0lo,e0hi = frac(references['E10']['lower']),frac(references['E10']['upper'])
    delta0lo,delta0hi = frac(references['Delta0']['lower']),frac(references['Delta0']['upper'])
    bglo,bghi = frac(references['Ebg63alpha']['lower']),frac(references['Ebg63alpha']['upper'])
    addlo,addhi = lo-bghi,hi-bglo
    drop_lo,drop_hi = e0lo-hi,e0hi-lo
    f1lo,f1hi = 2*drop_lo/a2,2*drop_hi/a2
    flo,fhi = 2*(delta0lo-addhi)/a2,2*(delta0hi-addlo)/a2
    dlo,dhi = 2*(addlo-delta0hi)/a2,2*(addhi-delta0lo)/a2
    checks = []
    add(checks,'Fadd63_minus_Dalpha63_exact_interval',flo==-dhi and fhi==-dlo)
    bgf = references['Fbg63']
    add(checks,'Fadd63_equals_F1_minus_sealed_Fbg63_interval',flo==f1lo-frac(bgf['upper']) and fhi==f1hi-frac(bgf['lower']))
    add(checks,'joint_alpha_interval_order',lo<=hi)
    add(checks,'retained63_addition_interval_order',addlo<=addhi)
    candidate = 'STRICT_FINITE_JOINT_DROP' if drop_lo>0 else ('CONCAVITY_CONTRADICTION_PRESERVED' if drop_hi<0 else 'JOINT_DROP_ZERO_OR_UNRESOLVED_PRESERVED')
    return {'E1alpha_raw':joint_alpha,'E10_authenticated':references['E10'],
            'Ebg0_authenticated':references['Ebg0'],'Ebg63alpha_authenticated':references['Ebg63alpha'],
            'Delta0_authenticated':references['Delta0'],'Delta_alpha63_raw':interval(addlo,addhi),
            'joint_energy_drop_raw':interval(drop_lo,drop_hi),'F1_raw':interval(f1lo,f1hi),
            'Fbg63_authenticated':bgf,'Fadd63_raw':interval(flo,fhi),'Dalpha63_raw':interval(dlo,dhi),
            'raw_joint_drop_candidate':candidate,'raw_strict_joint_drop_candidate':drop_lo>0,
            'concavity_contradiction_candidate':drop_hi<0,'numerical_zero_field_derivative_claim':False,
            'global_source_addition_status':'UNSTARTED_ROOT_ASSEMBLY_PENDING_ALL_Q_SOURCE_RECEIPT',
            'checks':list(checks)},checks



def report_text(result):
    def rat(value):
        return str(value['numerator'])+'/'+str(value['denominator'])
    lines = ['# Held hexagon: complete nonuniform carrier/copy source V001','',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             'Ground certificate status: '+result['ground_certificate_status']+'.',
             'Precision status: '+result['requested_precision_status']+'.',
             'Finite source status: '+result['finite_source_status']+'.','',
             '| completed fixed stage | raw joint lower | raw joint upper | raw width | retained63 addition lower | retained63 addition upper |',
             '|---:|---:|---:|---:|---:|---:|']
    for row in result['certificate_stages']:
        joint,addition = row['ground_interval_raw'],row['retained63_addition_interval_raw']
        lines.append(f"| {row['iteration']} | "+rat(joint['lower'])+' | '+rat(joint['upper'])+' | '+rat(joint['width'])+' | '+rat(addition['lower'])+' | '+rat(addition['upper'])+' |')
    assembly = result['finite_source_assembly']
    lines += ['', '| signed finite quantity | exact lower | exact upper |','|---|---:|---:|']
    for name in ('Delta_alpha63_raw','joint_energy_drop_raw','F1_raw','Fbg63_authenticated','Fadd63_raw','Dalpha63_raw'):
        bounds = assembly[name]
        lines.append('| '+name+' | '+rat(bounds['lower'])+' | '+rat(bounds['upper'])+' |')
    lines += ['', 'Global source/addition: '+assembly['global_source_addition_status']+'.',
              'Only alpha+ is numerically certified; alpha- follows the all-words/ports exact R3 map. Complete current, feedback, storage, hopping, incidence flips and copy are sourced by their owned native vertices, including fixed exterior endpoints.',
              'The retained63 reference is sector-ground preparation or a static sector-ground comparison. Nc0 record conservation alone proves neither relaxation nor an adiabatic/source-switch history. Global equilibrium source selection is a separate disjoint packet and must not be assumed.',
              'Fadd63 is the finite-field decrease of the matched addition; Dalpha63 is its exact opposite finite-field increase. All signs are retained; none is a numerical zero-field derivative, physical lapse calibration or gravity law.',
              'A strict joint drop with all controls passing earns qualitative chi1(0)>0 only. The discrete held carrier-injection line is visible for a definite-q sector ground by Perron positivity, without a measured residue, transport curvature, 3D metric or phase.',
              'Positive trial rounding/optimization does not change H. Every declared stage and full z/Mz is preserved; no old operator, eigensolve/inertia/propagation, alpha-minus run or dense joint matrix is replayed.',
              'Full Stage3 observational/galaxy-and-expansion obligations remain open. No installations, remote work, Goal, scheduler, favorable retuning or automatic rerun.',
              '',f"Elapsed seconds: {result['elapsed_seconds']}; native peak RSS: {result['ru_maxrss_native']}.",'']
    return '\n'.join(lines)



def main():
    global ATTEMPT_CREATED
    if sys.argv[1:] != ['--execute']:
        raise RuntimeError('Explicit --execute required; no calculation launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs,references = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
                'authenticated_inputs':inputs,'dimension':DIM,'integer_scale':SCALE,'alpha':exact(ALPHA),
                'L_plus_numerators_over40':list(L_PLUS),'L_exterior':1,'record_parity_negative_copy_unitary':True,
                'basis_order':'i=6(64q+n)+v','optimizer_frozen':{'initial':'uniform_positive_norm1','maximum_iterations':MAX_ITERATIONS,
                  'certificate_stages':list(CERTIFICATE_STAGES),'drop_norm':DROP_NORM,'positive_float_floor':POSITIVE_FLOOR,
                  'round_scale':ROUND_SCALE,'round_rule':'nearest_even_exact_as_integer_ratio','target_energy_width':exact(TARGET),
                  'MGS_passes':1,'column_order':['x','residual','p_previous'],'fallback':False},
                'numpy_version':np.__version__,'environment':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')}}
    manifest_hash = save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    diagonal,ports,structure,checks = build_action(references)
    ones_integer = integer_apply([1]*DIM,diagonal,ports)
    ones_float = float_h(np.ones(DIM,dtype=float),diagonal)
    uniform_error = float(np.max(np.abs(ones_float-np.array(ones_integer,dtype=float)/SCALE)))
    add(checks,'uniform_NEW_float_action_matches_exact_integer_row_sum',uniform_error<=1e-12)
    structure['uniform_NEW_float_action_max_error'] = uniform_error
    structure['checks'] = list(checks)
    save('complete_nonuniform_action_controls.json',structure)
    checks = list(checks)
    rounding,extra = rounding_controls()
    save('nearest_even_rounding_controls.json',rounding)
    checks.extend(extra)
    if any(not check['passed'] for check in checks):
        raise ArithmeticError('Pre-optimization complete source control failed; preserve attempt')
    x = np.full(DIM,1/math.sqrt(DIM),dtype=float)
    p_previous = np.zeros(DIM,dtype=float)
    initial_hash = save_float_state(0,x,p_previous,{'initial_uniform_positive':True})
    rows,precision_earned,last_diagnostics = [],False,{}
    for iteration in range(1,MAX_ITERATIONS+1):
        x,p_previous,last_diagnostics = optimizer_step(x,p_previous,diagonal)
        if iteration not in CERTIFICATE_STAGES:
            continue
        float_hash = save_float_state(iteration,x,p_previous,last_diagnostics)
        row,lower,upper,extra = certificate(iteration,x,diagonal,ports,references)
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
        raise ArithmeticError('Frozen source optimizer produced no exact certificate')
    final = rows[-1]
    assembly,extra = finite_source_assembly(final['ground_interval_raw'],references)
    checks.extend(extra)
    add(checks,'declared_completed_stage_census',[row['iteration'] for row in rows]==list(CERTIFICATE_STAGES[:len(rows)]))
    add(checks,'no_iteration_beyond4096',iteration<=MAX_ITERATIONS)
    final_inputs,final_references = authenticate()
    add(checks,'all_frozen_input_checkpoint_report_bytes_unchanged',final_inputs==inputs and final_references==references)
    add(checks,'source_protocol_bytes_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'structural_stage_check_list_unchanged',structure['checks']==checks[:len(structure['checks'])])
    failed = sum(not check['passed'] for check in checks)
    qualified = failed==0
    result = {'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if qualified else 'ARITHMETIC_FAILED_PRESERVED',
              'ground_certificate_status':'FULL_HELD_SOURCE_GROUND_INTERVAL_CERTIFIED' if qualified else 'RAW_SOURCE_INTERVAL_ARITHMETIC_UNQUALIFIED',
              'requested_precision_status':('TARGET_WIDTH_EARNED' if precision_earned else 'TARGET_WIDTH_UNEARNED_VALID_INTERVAL_PRESERVED') if qualified else 'PRECISION_ARITHMETIC_UNQUALIFIED',
              'finite_source_status':assembly['raw_joint_drop_candidate'] if qualified else 'FINITE_SOURCE_ARITHMETIC_UNQUALIFIED',
              'chi1_strictly_positive_qualitative_only':qualified and assembly['raw_strict_joint_drop_candidate'],
              'raw_target_precision_candidate':final['raw_target_width_candidate'],'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
              'authenticated_inputs':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),
              'dimension':DIM,'integer_scale':SCALE,'basis_order':'i=6(64q+n)+v','complete_nonuniform_action_controls':structure,
              'rounding_controls':rounding,'initial_float_state_sha256':initial_hash,'certificate_stages':rows,
              'final_ground_interval_raw':final['ground_interval_raw'],'finite_source_assembly':assembly,
              'alpha_minus_eigenvalue_from_exact_R3_only':True,'alpha_minus_run':False,'direct_second_alpha_contact':0,
              'global_source_addition_status':assembly['global_source_addition_status'],
              'iterations_completed':iteration,'floating_NEW_H_action_calls':FLOAT_ACTION_CALLS,'maximum_projected_eigensolve_dimension':3,
              'old_operator_eigensolve_inertia_propagation_replay':False,'full_dense_joint_matrix_constructed':False,
              'numeric_zero_field_derivative_gravity_clock_metric_claim':False,
              'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = report_text(result)
    stages_table = report.split('| completed fixed stage |',1)[1].split('| signed finite quantity |',1)[0]
    quantity_table = report.split('| signed finite quantity |',1)[1].split('Global source/addition:',1)[0]
    if stages_table.count('\n| ') != len(rows) or quantity_table.count('\n| ') != 6:
        raise RuntimeError('Report stage/six-signed-quantity DATA row count mismatch')
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
               'finite_source_status':result['finite_source_status'],'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'ground_certificate_status':result['ground_certificate_status'],
                      'requested_precision_status':result['requested_precision_status'],'finite_source_status':result['finite_source_status'],
                      'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
                      'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
    return 0 if qualified else 2


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
