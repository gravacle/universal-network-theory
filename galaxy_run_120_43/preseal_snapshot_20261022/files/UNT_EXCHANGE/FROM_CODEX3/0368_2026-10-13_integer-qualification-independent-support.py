"""SOURCE ONLY. Independent tiny scalar controls, metadata and profile checks.
Root runtime only; no producer science imports. C161 analytic helper retained.
"""
from fractions import Fraction as Q
from math import factorial,isfinite
from pathlib import Path
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
S=1<<80
SOURCES = {'integer': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/krylov_integer_production_certificate_v001.py', 'sha256': 'da1f4de9026ecc3b2f56d1fd5b91bfc930ebaf2e385397e8b142b4acf02b6736', 'bytes': 6576}, 'reference': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/certified_krylov_reference_v001.py', 'sha256': 'adb77d50bae4d1e230b36e5b97cf7b0d5bbc427a02f8a3bbe135b88393fe9e7d', 'bytes': 11861}, 'controls': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/certified_krylov_controls_v001.py', 'sha256': 'f74de621ba3848bc3651dc7da9d227031a9aa95047f7bb2bdc99b80d0f1d518f', 'bytes': 4020}}
QUAL_INPUTS = {'controls': {'c161': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/SHARED_KRYLOV_CONTROLS_ACCEPTANCE_V001.json', 'sha256': 'e65bc629bd6a7f6f10183237ce382ba8ca9d7da69a57fa8d6eb6eccad40042ba', 'bytes': 11832}}, 'replay': {'c170': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/SHARED_KRYLOV_NATIVE_ONE_STEP_ACCEPTANCE_V001.json', 'sha256': '2758bf7479d18bd650977ff72f4786c42861f6f48faba0e77aa339ab4fa92f09', 'bytes': 2068}, 'pre': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/SHARED_KRYLOV_NATIVE_ONE_STEP_OUTPUT_V001/CERTIFICATE_PRE.json', 'sha256': '24d25201f5d91560dcdb37241bd679538cd12d9f67bbe57f03a521268f22c05c', 'bytes': 5671151}, 'return': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/SHARED_KRYLOV_NATIVE_ONE_STEP_OUTPUT_V001/CERTIFICATE_RETURN.json', 'sha256': 'c9b570d93234998b4798483c6e257c491b7da5a1df48386dce9214e470ca0d78', 'bytes': 556377}}}


def extra_inputs():
    def make(h,negative,K,error,scope):
        return {'rows':[[[0,1,0]]] if h else [[]], 'denominator':1,
            'center':[[-S if negative else S,0]], 'input_L2_error':error,
            'proposal':{'basis_I80':[[[S,0]]], 'projected_H_I80':[[[S if h else 0,0]]],
                'initial_coeff_I80':[[-S if negative else S,0]],'candidate_scope':scope},
            'tau':'1/3','degree':K}
    return [make(False,False,2,str(Q(1,1<<51)),'MANUFACTURED_INHERITED_ERROR'),
            make(True,True,8,'0','MANUFACTURED_SIGNED_NON_DYADIC')]


def scalar_certificate(signed,upward):
    # H=0,e0 or H=1,-e0. Analytic scalar powers; no production residual columns.
    K=8 if signed else 2; t=Q(1,3); error=Q(0) if signed else Q(1,1<<51)
    powers=[[['-1','0']] for _ in range(K+1)] if signed else [[['1','0']]]+[[['0','0']] for _ in range(K)]
    terms=[]; integral=Q(0)
    for k in range(K+1):
        v=Q(int(signed and k==K));w=t**(k+1)/factorial(k+1)
        integral+=upward(v)*w
        terms.append({'power':k,'complete_defect_norm_squared':str(v),
            'norm_upper':str(upward(v)),'integral_factor':str(w)})
    if signed:
        real=-sum(((-1)**j*t**(2*j)/factorial(2*j) for j in range(5)),Q(0))
        imag=sum(((-1)**j*t**(2*j+1)/factorial(2*j+1) for j in range(4)),Q(0))
    else:real,imag=Q(1),Q(0)
    endpoint=[]
    for z in (real,imag):endpoint.append((1 if z>=0 else -1)*(abs(z.numerator)*S//z.denominator))
    r2=(real-Q(endpoint[0],S))**2+(imag-Q(endpoint[1],S))**2
    rounding=upward(r2);added=integral+rounding;total=error+added
    return {'schema':'CERTIFIED_KRYLOV_POLYNOMIAL_DEFECT_V001','dimension':1,'basis_columns':1,
        'degree':K,'tau':str(t),'input_L2_error':str(error),'initial_projection_defect_squared':'0',
        'initial_projection_error_upper':'0','all_basis_residual_norm_squared':['0'],
        'all_projected_powers':powers,'all_polynomial_defect_terms':terms,'integrated_defect_upper':str(integral),
        'endpoint_quantization_norm_squared':str(r2),'endpoint_quantization_error_upper':str(rounding),
        'step_added_L2_error':str(added),'accumulated_L2_error':str(total),'endpoint_I80':[endpoint],
        'step_target_2_minus_64_met':added<=Q(1,1<<64),'original_cumulative_cap_2_minus_51_met':total<Q(1,1<<51),
        'arithmetic':'FULL_EXACT_RATIONAL_WITH_INTEGER_OUTWARD_SQRT','orthogonality_or_backend_flags_trusted':False,
        'exact_input_error_and_H_ancestry_authenticated_here':False,'native_N2_validation_completed':False,'physical_release':False}


def controls(data,A,exact,need,guard):
    names=A.NAMES+['inherited_error_strict_boundary','signed_non_dyadic_endpoint']
    operands=A.expected_inputs()+extra_inputs()
    outputs=A.expected_outcomes()+[{'exception':None,'value':scalar_certificate(v,A.upward_root)} for v in (False,True)]
    for i,name in enumerate(names):
        guard()
        exact(data['CALL_%02d_PRE.json'%i],{'name':name,'payload':operands[i]},'entire PRE '+name)
        exact(data['CALL_%02d_RETURN.json'%i],{'name':name,'payload':outputs[i]},'entire RETURN '+name)
    oldflags={k:True for k in ('full_basis_precision','bad_subspace_wide','candidate_certified','excited_not_ground_precision','ground_exact','three_refusals')}
    original={'schema':'CERTIFIED_KRYLOV_FIXED_EIGHT_CONTROLS_V001','calls':dict(zip(names[:8],outputs[:8])),
        'checks':oldflags,'all_controls':True,'native_N2_validation':False,'physical_release':False}
    inherited,signed=outputs[8]['value'],outputs[9]['value']
    need(inherited['step_added_L2_error']=='0' and inherited['accumulated_L2_error']==str(Q(1,1<<51))
        and inherited['step_target_2_minus_64_met'] is True and inherited['original_cumulative_cap_2_minus_51_met'] is False,
        'independent inherited strict boundary')
    need(signed['endpoint_I80'][0][0]<0 and signed['endpoint_I80'][0][1]>0
        and Q(signed['endpoint_quantization_norm_squared'])>0,'independent signed non-dyadic scalar polynomial')
    result={'schema':'KRYLOV_INTEGER_TEN_CONTROLS_V001','original_eight':original,
        'extras':dict(zip(names[8:],outputs[8:])),
        'checks':{'all_original_eight':True,'inherited_error_exact':True,'signed_quantization_exercised':True},
        'all_controls':True,'calls':10,'events':20,'distinct_complete_comparison_required':True,'physical_release':False}
    exact(data['RESULTS.json'],result,'all original and extra result fields')
    return result


def profile(record,pid,case,exact,need,seconds):
    # Actual durations require root PID/source/runtime provenance. Here validate
    # every key/type/finiteness/bound and preserve complete original record.
    if case=='profile':
        fixed={'schema':'KRYLOV_INTEGER_NATIVE_PHASE_PROFILE_V001','pid':pid,
            'profile_and_finish_serialization_excluded':True,'unclassified_postprocessing_not_assigned_to_calls':True,
            'candidate_source_unchanged':True,'candidate_decimal_regenerated_by_checker':False,
            'speedup_claim':False,'full_N2_released':False}
        fields=['authentication_native_binding_excluding_output_io','input_closing','output_io_before_profile','whole_elapsed_before_profile']
        keys=[a+'_'+b+'_seconds' for a in fields for b in ('wall','cpu')]
        need(set(record)==set(fixed)|set(keys)|{'actual_call_phases'},'closed complete native profile')
        phases=record['actual_call_phases'];need(type(phases)is list and len(phases)==2,'exact two actual phase records')
        for row,name in zip(phases,('unchanged_decimal_candidate','integer_production_certificate')):
            need(type(row)is dict and set(row)=={'name','wall_seconds','cpu_seconds'},'closed phase')
            exact(row['name'],name,'actual phase identity')
            for kind in ('wall','cpu'):
                v=row[kind+'_seconds'];need(type(v)is float and isfinite(v) and 0<=v<=record['whole_elapsed_before_profile_'+kind+'_seconds'],'finite phase within whole')
    else:
        fixed={'schema':'KRYLOV_INTEGER_QUALIFICATION_PROFILE_V001','pid':pid,'case':case,
            'profile_and_finish_serialization_excluded':True,'candidate_regenerated':case=='controls',
            'replay_whole_original_certificate_equal':case=='replay','speedup_claim':False}
        keys=[a+'_'+b+'_seconds' for a in ('measured_phase_including_event_io','phase_event_io','whole_elapsed_before_profile') for b in ('wall','cpu')]
        need(set(record)==set(fixed)|set(keys),'closed complete qualification profile')
        for kind in ('wall','cpu'):
            need(record['phase_event_io_'+kind+'_seconds']<=record['measured_phase_including_event_io_'+kind+'_seconds'], 'I/O subset of phase')
    for k,v in fixed.items():exact(record[k],v,'profile fixed '+k)
    for k in keys:
        v=record[k];need(type(v)is float and isfinite(v) and v>=0,'finite nonnegative measured '+k)
        kind='wall' if '_wall_' in k else 'cpu'
        need(v<=record['whole_elapsed_before_profile_'+kind+'_seconds'],'phase bounded by whole '+k)
    need(record['whole_elapsed_before_profile_wall_seconds']<=seconds,'profile within role wall cap')
    return record
