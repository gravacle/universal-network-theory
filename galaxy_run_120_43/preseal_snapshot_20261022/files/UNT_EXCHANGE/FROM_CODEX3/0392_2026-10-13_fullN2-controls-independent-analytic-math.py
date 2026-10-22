"""SOURCE ONLY. Analytic full expected18 manufactured continuation controls.
No production controls/caller/math/read functions imported or executed.
"""
from fractions import Fraction as Q
S=1<<80
NAMES=('constant_trapezoid','linear_trapezoid','split_prefix_trapezoid','averaged_law_nonlinearity',
    'missing_integral_rejected','endpoint_equal','endpoint_disagreement','average_disagreement',
    'chain_initial','chain_accepted','chain_missing','chain_wrong_seed','chain_wrong_stop',
    'chain_raw_rejected','chain_strict_error_rejected','chain_phase_rejected','chain_read_rejected','chain_negative_integral_rejected')


def toy_read(error,R):
    e=Q(error);delta=e*(2+e)
    def observable(point,cap):
        return {'center_expectation':Q(point),'interval':[max(Q(0),Q(point)-cap*delta),min(Q(cap),Q(point)+cap*delta)],
            'vector_error_allowance':cap*delta,'operator_norm_upper':cap}
    # Every fixture state has oldword11. The three absent projectors have
    # literal maxweight0 on this deliberately repeated, non-native list.
    words={w:observable(int(w=='11'),int(w=='11')) for w in R.WORDS}
    values=(1,0,1,0,2,2)
    diagonal={name:observable(value,R.CAPS[name]) for name,value in zip(R.DIAGONALS,values)}
    return {'words':words,'statistics':R.statistics({w:v['interval'] for w,v in words.items()}),
        'diagonal':diagonal,'norm_center_squared':Q(1),'L2_error':e,
        'state_phase':'exp(-i(H-(2121/80)I)t), hbar=1','DE':False}


def fixture(P,F,R,callerpin):
    center=[[0,0] for _ in range(10432)];center[0]=[S,0]
    states=[[0,3,1,3,0,1] for _ in range(10431)]+[[1,3,0,15,1,0]]
    read=toy_read(Q(1,S),R)
    flat={**read['words'],**read['diagonal']}
    checkpoint={'schema':'KRYLOV_FULL_N2_CHECKPOINT_V001','seed':F.SEEDS[0],'chunk':0,'step':64,'time':'1/8',
        'phase':F.PHASE,'native_packet':P.INPUTS['packet'],'source_pins':P.SOURCES,'predecessor_acceptances':[],
        'center':center,'L2_error':str(Q(1,S)),'readout':read,'integrals':{k:[v/8 for v in flat[k]['interval']] for k in F.NAMES}}
    gate={'acceptor':'/root','status':'PASS_MANUFACTURED_FIXTURE_ONLY','schema':'KRYLOV_FULL_N2_CHUNK_ACCEPTANCE_V001',
        'role':'SHARED_KRYLOV_FULL_N2_CHUNK_V001','seed':F.SEEDS[0],'chunk':0,'start_step':0,'stop_step':64,
        'source_pins':P.SOURCES,'producer':callerpin,'native_packet':P.INPUTS['packet'],
        'complete_distinct_all_steps_comparison':True,'complete_original_runtime_custody':True,
        'complete_C150_ancestry_opening_and_closing':True,'predecessor_acceptances':[],'checkpoint_reusable':True}
    return F.wire({'manufactured_only':True,'literal_native_basis_claim':False,'states':states,'center':center,
        'initial_error':'0','checkpoint_template':checkpoint,'gate_template':gate,'caller_pin':callerpin})


def expected(name,fixture,F,R,C):
    failures={'missing_integral_rejected':'complete ten integral sums','chain_missing':'all prior accepted chunks',
        'chain_wrong_seed':'whole causal accepted predecessor','chain_wrong_stop':'whole causal accepted predecessor',
        'chain_raw_rejected':'whole causal accepted predecessor','chain_strict_error_rejected':'retained cumulative error',
        'chain_phase_rejected':'exact checkpoint identity/ancestry','chain_read_rejected':'full accepted checkpoint read',
        'chain_negative_integral_rejected':'ordered accumulated integral'}
    if name in failures:return {'exception':'ValueError','message':failures[name],'value':None}
    if name=='chain_initial':
        value={'center':fixture['center'],'L2_error':'0','readout':toy_read(Q(0),R),
            'integrals':{k:[Q(0),Q(0)] for k in F.NAMES},'step':0,'time':'0'}
    elif name=='chain_accepted':
        value={k:fixture['checkpoint_template'][k] for k in ('center','L2_error','readout','integrals','step','time')}
    else:
        values={k:Q(1,4) if k in R.WORDS else Q(1) if k=='Nq_old' else Q(2) if k=='Nq_all' else Q(1,2) for k in F.NAMES}
        integrals={k:[v/8,v/8] for k,v in values.items()}
        if name=='linear_trapezoid':
            integrals={k:[Q(5,128) if k=='00' else Q(3,128) if k=='01' else Q(1,32) if k in ('10','11') else Q(1,128)]*2 for k in F.NAMES}
        elif name=='averaged_law_nonlinearity':integrals={k:[Q(1,16) if k in ('00','11') else Q(0)]*2 for k in F.NAMES}
        average=F.average(F.SEEDS[0],64,integrals,None,Q(0),R,C)
        if name in ('endpoint_equal','endpoint_disagreement','average_disagreement'):
            avrows=[];ptrows=[]
            for k in F.NAMES:
                group='averaged_words' if k in R.WORDS else 'averaged_diagonal'
                a,b=average[group][k]['interval'];c,d=(Q(0),Q(0)) if name=='average_disagreement' and k=='00' else (a,b)
                avrows.append({'observable':k,'krylov_interval':[a,b],'C150_interval':[c,d],
                    'signed_difference_interval':[a-d,b-c],'nonempty_intersection':not(b<c or d<a)})
                ptrows.append({'observable':k,'krylov_interval':[values[k],values[k]],'C150_interval':[values[k],values[k]],
                    'signed_difference_interval':[Q(0),Q(0)],'nonempty_intersection':True})
            different=name=='endpoint_disagreement'
            value={'schema':'KRYLOV_FULL_N2_C150_COMPARISON_V001','endpoint_center_difference_squared':Q(int(different)),
                'sum_L2_radii':Q(0),'squared_sum_L2_radii':Q(0),'full_endpoint_bound_met':not different,
                'all_ten_continuous_average_comparisons':avrows,'all_ten_endpoint_read_comparisons':ptrows,
                'all_average_intersections':name!='average_disagreement','all_endpoint_read_intersections':True,
                'same_midpoint_trajectories_claimed':False,'scientific_acceptance':False}
        else:
            prefix={k:[x/2 for x in pair] for k,pair in integrals.items()} if name=='split_prefix_trapezoid' else None
            nonlinear=None
            if name=='averaged_law_nonlinearity':
                laws=[{w:[Q(int(w==('00' if index%2==0 else '11')))]*2 for w in R.WORDS} for index in range(65)]
                # Each endpoint is deterministic, hence covariance exactly0.
                # Equal half-cell weights give mixedlaw covariance1/4.
                nonlinear={'endpoint_word_laws':laws,'endpoint_covariances':[[Q(0),Q(0)] for _ in range(65)],
                    'trapezoid_of_endpoint_covariances':[Q(0),Q(0)],
                    'closed_form_average_law':{'00':Q(1,2),'01':Q(0),'10':Q(0),'11':Q(1,2)},
                    'closed_form_covariance_of_average':Q(1,4),'closed_form_average_covariance':Q(0)}
            value={'integrals':integrals,'serialized_half_prefix':prefix,'average':average,'nonlinear_reference':nonlinear}
    return {'exception':None,'message':None,'value':F.wire(value)}
