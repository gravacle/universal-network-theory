#!/usr/bin/env python3
"""NEW complete overlapping-star bounds; ancestor notes are bytes only."""
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

J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME='LOCAL_RECORD_FEEDBACK_3D_STAR_BOUND_V001'
SOURCE=Path(__file__).resolve()
PROTOCOL=J/(NAME+'.md')
RESULT=J/(NAME+'_RESULT.json')
REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json')
CP=J/'local_record_feedback_3d_star_bound_v001_checkpoints'
INPUTS={
 'LOCAL_RECORD_FEEDBACK_3D_ICE_OPERATOR_CROSSWALK_V001.md':'7f755bbae58c40583f784d469376792cece209193113504136f20e86259b3371',
 'LOCAL_PROPER_BOND_DRESSED_VACUUM_V001.md':'e8b34c02e8d0002f4ab0d8d287f8aa7e74ec5592a856ef5ffcfaf703e129b71f',
 'LOCAL_PROPER_BOND_NORMALIZATION_V001.md':'9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
}
H=Fraction(1,5)
COMPARISONS=(Fraction(0),Fraction(1,2))
INTEGER_SCALE=20
ROUND_SCALE=10**60
FLOOR=1e-100
TARGET=Fraction(1,10**11)
D_VALUES=(Fraction(5),Fraction(3,2),Fraction(0),Fraction(1,2),Fraction(3))
ATTEMPT_CREATED=False
STAGES={}

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

def bounds(value):
    return frac(value['lower']),frac(value['upper'])

def same(first,second):
    return bounds(first)==bounds(second)

def verify_map(mapping,directory,label):
    out = {}
    for name,wanted in mapping.items():
        got = sha(directory/name)
        if got != wanted:
            raise RuntimeError(label+' changed: '+name)
        out[name] = got
    return out

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

def authenticate():
    return verify_map(INPUTS,J,'Frozen current-parent input')


def complete_star_controls():
    checks=[]
    rows=[]
    for word in range(16):
        degree=word.bit_count()
        delta=degree-2
        value=Fraction(delta*delta)-Fraction(delta,2)
        z=[1-2*((word>>e)&1) for e in range(4)]
        pauli=1+sum(Fraction(z[e]*z[f],2) for e in range(4) for f in range(e+1,4))+sum(Fraction(value,4) for value in z)
        nonice=int(delta!=0)
        add(checks,f'word{word}_full_occupied_record_degree_energy',value==D_VALUES[degree])
        add(checks,f'word{word}_exact_longitudinal_Pauli_form',value==pauli)
        add(checks,f'word{word}_D_ge_delta_squared_half',value>=Fraction(delta*delta,2))
        add(checks,f'word{word}_nonice_half_le_D_le5nonice',Fraction(nonice,2)<=value<=5*nonice)
        rows.append({'word':word,'degree':degree,'delta':delta,'D':exact(value),'nonice_projector':nonice})
    add(checks,'blank_BOND_complete_matching_gap1_records_q1',2*(D_VALUES[3]-D_VALUES[2])==1)
    add(checks,'occupied_BOND_complete_matching_gap3_records_q1',2*(D_VALUES[1]-D_VALUES[2])==3)
    add(checks,'two_vertex_owners_recover_full_flip',2*(H/2)==H)
    add(checks,'only_fixed_comparisons0_and_half',COMPARISONS==(Fraction(0),Fraction(1,2)))
    return {'all16_rows':rows,'star_flip_each':exact(-H/2),'complete_flip_each':exact(-H),
            'records_fixed_q1':True,'blank_means_BOND_not_record':True,
            'noncommuting_star_sum_exact_by_two_endpoint_ownership':True,'checks':list(checks)},checks


def star_matrix(a):
    matrix=[[0]*16 for _ in range(16)]
    for word in range(16):
        diagonal=INTEGER_SCALE*(1-a)*D_VALUES[word.bit_count()]
        if diagonal.denominator!=1:
            raise ArithmeticError('Noninteger star diagonal')
        matrix[word][word]=diagonal.numerator
        for e in range(4):
            matrix[word][word^(1<<e)]=-2
    checks=[]
    add(checks,'a'+str(a)+'_complete16_matrix_dimension',len(matrix)==16 and all(len(row)==16 for row in matrix))
    add(checks,'a'+str(a)+'_four_distinct_negative_flip_ports',all(sum(value!=0 for j,value in enumerate(row) if j!=i)==4 and all(value==-2 for j,value in enumerate(row) if j!=i and value!=0) for i,row in enumerate(matrix)))
    add(checks,'a'+str(a)+'_symmetric_complete_matrix',all(matrix[i][k]==matrix[k][i] for i in range(16) for k in range(16)))
    return matrix,checks


def one_positive_certificate(a,matrix):
    values,vectors=np.linalg.eigh(np.asarray(matrix,dtype=float)/INTEGER_SCALE)
    if not np.all(np.isfinite(values)) or not np.all(np.isfinite(vectors)):
        raise ArithmeticError('Nonfinite NEW star trial')
    raw=vectors[:,0]
    x=np.maximum(np.abs(raw),FLOOR)
    x=x/float(np.linalg.norm(x))
    if not np.all(np.isfinite(x)) or np.min(x)<=0:
        raise ArithmeticError('Nonpositive NEW star trial')
    z=[]
    floor_count=0
    for value in x:
        numerator,denominator=float(value).as_integer_ratio()
        rounded=round_ratio_even(numerator*ROUND_SCALE,denominator)
        if rounded==0:
            rounded=1
            floor_count+=1
        z.append(rounded)
    mz=[sum(matrix[i][k]*z[k] for k in range(16)) for i in range(16)]
    ratios=[Fraction(mz[i],INTEGER_SCALE*z[i]) for i in range(16)]
    minimum=min(range(16),key=lambda i:ratios[i])
    maximum=max(range(16),key=lambda i:ratios[i])
    quadratic=sum(z[i]*mz[i] for i in range(16))
    independent=sum(matrix[i][i]*z[i]*z[i] for i in range(16))
    for i in range(16):
        for e in range(4):
            if not i&(1<<e):
                independent-=4*z[i]*z[i^(1<<e)]
    norm=sum(value*value for value in z)
    lower=ratios[minimum]
    upper=Fraction(quadratic,INTEGER_SCALE*norm)
    cwupper=ratios[maximum]
    checks=[]
    add(checks,'a'+str(a)+'_strictly_positive_integer_proposal',len(z)==16 and min(z)>0)
    add(checks,'a'+str(a)+'_independent_undirected_quadratic',quadratic==independent)
    add(checks,'a'+str(a)+'_CW_Rayleigh_order',lower<=upper<=cwupper)
    proposal={'a':exact(a),'one_NEW_eigh_trial_only':True,'trial_eigenvalues':[float(value) for value in values],
              'lowest_raw_vector_hex':[float(value).hex() for value in raw],
              'positive_trial_hex':[float(value).hex() for value in x],'integer_scale':INTEGER_SCALE,
              'matrix20':matrix,'round_scale':ROUND_SCALE,'round_rule':'nearest_even_exact_as_integer_ratio',
              'rounded_zero_floor_count':floor_count,'z':z,'Mz':mz,
              'exact_z_Mz':quadratic,'independent_undirected_quadratic':independent,'exact_z_squared_norm':norm,
              'minimum_ratio_witness':{'index':minimum,'Mz_i':mz[minimum],'z_i':z[minimum],'ratio':exact(lower)},
              'maximum_ratio_witness':{'index':maximum,'Mz_i':mz[maximum],'z_i':z[maximum],'ratio':exact(cwupper)},
              'ground_interval_raw':interval(lower,upper),'CW_ratio_interval_raw':interval(lower,cwupper),
              'target_width':exact(TARGET),'raw_target_width_candidate':upper-lower<=TARGET,'checks':list(checks)}
    return proposal,checks


def sqrt_interval(number,lower,upper):
    lower,upper=Fraction(lower),Fraction(upper)
    rows=[]
    for step in range(80):
        midpoint=(lower+upper)/2
        if midpoint*midpoint<=number:
            lower=midpoint
        else:
            upper=midpoint
        rows.append({'step':step+1,'lower':exact(lower),'upper':exact(upper)})
    checks=[]
    add(checks,'sqrt'+str(number)+'_fixed80_steps',len(rows)==80)
    add(checks,'sqrt'+str(number)+'_squared_exact_bounds',0<lower<=upper and lower*lower<=number<=upper*upper)
    return {'radicand':number,'fixed_iterations':80,'interval':interval(lower,upper),
            'rows':rows,'checks':list(checks)},checks


def assemble(certificates,sqrts):
    mu=certificates[0]['ground_interval_raw']
    k=certificates[1]['ground_interval_raw']
    sqrt29,sqrt229=sqrts
    blank=interval((5-frac(sqrt29['interval']['upper']))/20,(5-frac(sqrt29['interval']['lower']))/20)
    occupied=interval((15-frac(sqrt229['interval']['upper']))/20,(15-frac(sqrt229['interval']['lower']))/20)
    b=interval(-frac(k['upper']),-frac(k['lower']))
    energy=interval(frac(mu['lower']),frac(blank['upper']))
    d_upper=2*(frac(blank['upper'])+frac(b['upper']))
    deviation_upper=2*d_upper
    checks=[]
    add(checks,'blank_BOND_trial_negative_complete_energy',frac(blank['upper'])<0)
    add(checks,'occupied_BOND_control_negative_complete_energy',frac(occupied['upper'])<0)
    add(checks,'blank_BOND_primary_stronger_than_occupied_control',frac(blank['upper'])<frac(occupied['lower']))
    add(checks,'energy_density_envelope_order',frac(energy['lower'])<=frac(energy['upper']))
    add(checks,'b_positive_and_D_upper_nonnegative',frac(b['lower'])>0 and d_upper>=0)
    return {'mu_local_ground_interval_raw':mu,'k_half_comparison_interval_raw':k,'b_interval_raw':b,
            'blank_BOND_matching_trial_density':blank,'occupied_BOND_matching_trial_density_control':occupied,
            'full_q1_sector_ground_energy_density_envelope_raw':energy,
            'D_expectation_per_vertex_upper_raw':exact(d_upper),
            'delta_squared_expectation_per_vertex_upper_raw':exact(deviation_upper),
            'nonice_probability_average_upper_raw':exact(deviation_upper),
            'independent_D_range':[0,5],'independent_delta_squared_range':[0,4],'independent_nonice_probability_range':[0,1],
            'raw_nonice_upper_below1_candidate':deviation_upper<1,
            'raw_delta_squared_upper_below4_candidate':deviation_upper<4,
            'raw_D_upper_below5_candidate':d_upper<5,
            'raw_bounds_clipped':False,'actual_global_star_product_state_assumed':False,'phase_or_preparation_claim':False,
            'checks':list(checks)},checks


def report_text(result):
    def rat(value):
        return str(value['numerator'])+'/'+str(value['denominator'])
    lines=['# Current 3D parent: exact overlapping-star envelopes V001','',
           f"Controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
           'Status: '+result['status']+'.',
           'Bounds: '+result['bound_status']+'.','',
           '| local comparison a | exact ground lower | exact ground upper | width | precision |','|---|---:|---:|---:|---|']
    for row in result['local_certificates']:
        bounds=row['ground_interval_raw']
        lines.append('| '+rat(row['a'])+' | '+rat(bounds['lower'])+' | '+rat(bounds['upper'])+' | '+rat(bounds['width'])+' | '+row['requested_precision_status']+' |')
    if len(result['local_certificates'])!=2:
        raise RuntimeError('Fixed two-certificate report census mismatch')
    assembly=result['ground_and_defect_envelopes']
    lines+=['','| matching/control or volume-uniform bound | exact lower | exact upper |','|---|---:|---:|']
    for key in ('blank_BOND_matching_trial_density','occupied_BOND_matching_trial_density_control','full_q1_sector_ground_energy_density_envelope_raw','b_interval_raw'):
        bounds=assembly[key]
        lines.append('| '+key+' | '+rat(bounds['lower'])+' | '+rat(bounds['upper'])+' |')
    for key in ('D_expectation_per_vertex_upper_raw','delta_squared_expectation_per_vertex_upper_raw','nonice_probability_average_upper_raw'):
        lines.append('| '+key+' | 0 | '+rat(assembly[key])+' |')
    lines+=['',
           'All records remain occupiedq1; blank/occupied labels distinguish matching BOND bits. Full degrees0..4, feedback and common identity are retained. The blank-bond primary trial was chosen prospectively and the occupied-bond alternative remains an explicit control.',
           'The local stars overlap and need not commute. Summed operator inequalities are valid without a compatible product of star ground states; no such global state is asserted.',
           'Raw defect bounds remain untrimmed. Independent exact ranges are D0..5, delta-squared0..4 and nonice probability0..1. A loose bound remains loose; no parameter selection/refinement is authorized.',
           'These are energy/defect envelopes for the supplied periodic diamond and declaredNc0q1 sector. They establish neither actual preparation/global record selection nor a Coulomb phase, GNS state, transverse dynamic weight, matter pole, rank-three transport, physical metric/clock/ruler, gravity/volume law, observed superiority or Stage3 completion.',
           'Each positive trial came from oneNEW16-state NumPy calculation. Exact integer CW/Rayleigh certificates and rational sqrt bounds earn the result; no old producer/action/eigensolve/inertia/evolution is replayed.',
           '',f"Elapsed seconds: {result['elapsed_seconds']}; native peak RSS: {result['ru_maxrss_native']}.",'']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    if sys.argv[1:]!=['--execute']:
        raise RuntimeError('Explicit --execute required; no calculation launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive output already exists: '+str(path))
    inputs=authenticate()
    source_hash,protocol_hash=sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED=True
    manifest={'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
              'input_sha256':inputs,'h':exact(H),'comparisons':[exact(a) for a in COMPARISONS],
              'integer_scale':INTEGER_SCALE,'round_scale':ROUND_SCALE,'requested_width':exact(TARGET),
              'one_trial_per_matrix':True,'no_refinement':True,'sqrt_iterations':80,
              'numpy_version':np.__version__,'environment':{key:os.environ.get(key) for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')}}
    manifest_hash=save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    structure,checks=complete_star_controls()
    save('complete_local_star_controls.json',structure)
    rounding,extra=rounding_controls()
    checks.extend(extra)
    save('nearest_even_rounding_controls.json',rounding)
    if any(not check['passed'] for check in checks):
        raise ArithmeticError('Fixed local controls failed')
    certificates=[]
    for serial,a in enumerate(COMPARISONS):
        matrix,extra=star_matrix(a)
        checks.extend(extra)
        row,extra=one_positive_certificate(a,matrix)
        checks.extend(extra)
        row['controls_failed_through_stage']=sum(not check['passed'] for check in checks)
        row['requested_precision_status']=('TARGET_WIDTH_EARNED' if row['raw_target_width_candidate'] else 'TARGET_WIDTH_UNEARNED_VALID_INTERVAL_PRESERVED') if row['controls_failed_through_stage']==0 else 'PRECISION_ARITHMETIC_UNQUALIFIED'
        save(f'local_operator_{serial}_certificate.json',row)
        certificates.append(row)
    sqrts=[]
    for number,lower,upper in ((29,5,6),(229,15,16)):
        row,extra=sqrt_interval(number,lower,upper)
        checks.extend(extra)
        save(f'sqrt{number}_certificate.json',row)
        sqrts.append(row)
    assembly,extra=assemble(certificates,sqrts)
    checks.extend(extra)
    add(checks,'exact_fixed_comparison_census',[row['a'] for row in certificates]==[exact(a) for a in COMPARISONS])
    add(checks,'all_frozen_input_bytes_unchanged',authenticate()==inputs)
    add(checks,'new_source_protocol_bytes_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    failed=sum(not check['passed'] for check in checks)
    qualified=failed==0
    result={'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if qualified else 'ARITHMETIC_FAILED_PRESERVED',
            'bound_status':'VOLUME_UNIFORM_Q1_SECTOR_ENVELOPES_CERTIFIED' if qualified else 'RAW_ENVELOPES_ARITHMETIC_UNQUALIFIED',
            'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,'input_sha256':inputs,
            'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),'complete_local_controls':structure,
            'rounding_controls':rounding,'local_certificates':certificates,'sqrt_certificates':sqrts,
            'ground_and_defect_envelopes':assembly,'one_NEW_numpy_trial_each':True,'NEW_eigh_count':2,
            'unearned_width_outcome_preserved':True,'global_graph_Hilbert_space_calculation':False,
            'old_producer_import_action_eigensolve_inertia_evolution':False,'phase_preparation_physical_units_volume_law_claim':False,
            'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
            'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    raw_hash=exclusive(RESULT,result)
    canonical_hash=hashlib.sha256(canonical(result)).hexdigest()
    event('result_complete',filename=RESULT.name,sha256=raw_hash,canonical_sha256=canonical_hash)
    with REPORT.open('x') as stream:
        stream.write(report_text(result))
        stream.flush()
        os.fsync(stream.fileno())
    report_hash=sha(REPORT)
    event('report_complete',filename=REPORT.name,sha256=report_hash)
    receipt={'schema':NAME+'_RECEIPT','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
             'input_sha256':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),
             'result_raw_sha256':raw_hash,'result_canonical_sha256':canonical_hash,'report_sha256':report_hash,
             'journal_prefix_sha256':sha(CP/'journal.jsonl'),'status':result['status'],
             'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
             'elapsed_seconds':result['elapsed_seconds'],'ru_maxrss_native':result['ru_maxrss_native']}
    receipt_hash=exclusive(RECEIPT,receipt)
    event('receipt_complete',filename=RECEIPT.name,receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'checks_passed':len(checks)-failed,'checks_total':len(checks),
          'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
    return 0 if qualified else 2


if __name__=='__main__':
    T0=time.perf_counter()
    try:
        sys.exit(main())
    except Exception as error:
        if ATTEMPT_CREATED:
            failure={'error_type':type(error).__name__,'error_message':str(error),'traceback':traceback.format_exc(),
                     'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,'checkpoint_sha256':dict(STAGES),
                     'rerun_or_resume_authorized':False}
            try:
                digest=exclusive(CP/'ERROR.json',failure)
                event('error',filename='ERROR.json',sha256=digest,error_type=type(error).__name__)
            except Exception:
                pass
        print(json.dumps({'error_type':type(error).__name__,'error_message':str(error),'pid':os.getpid()}),flush=True)
        sys.exit(3)
