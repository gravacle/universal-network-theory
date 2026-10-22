"""SOURCE ONLY. Independent analytic all-layer C181 key-count bounds.
Local degrees from counts of unit/double incidences, not subset-set recurrence.
CPython payload size derived from digit/tuple ABI metadata, never labelled RSS.
"""
import struct,sys


def reconstruct(domain,progress,refusal,runtime,C,guard):
    exact,need=C.exact,C.need
    L,nv=domain['L'],domain['vertices'];factors=domain['complete_orbit_polynomial_factors'];m=len(factors);k=len(progress)
    need(refusal['status']=='COUNT_CAP_REFUSAL' and refusal['live_cap']==65536 and 0<=k<m
        and refusal['completed_orbits']==k and refusal['total_orbits']==m,'same actual complete prefix/cap refusal')
    observed=[1]+[row['live_keys'] for row in progress]
    need(all(type(v)is int and 0<=v<=65536 for v in observed),'literal saved nonnegative key counts')
    for index,row in enumerate(progress,1):
        exact(row,{'kind':'EXACT_COEFFICIENT_FRONTIER','completed_orbits':index,'total_orbits':m,
            'live_keys':observed[index],'live_cap':65536,'partial_table_is_dimension':False},'whole accepted layer summary')
    need(max(observed)==refusal['peak_completed_live_keys'],'exact completed prefix peak')
    times=[[] for _ in range(nv)]
    for index,f in enumerate(factors,1):
        for vertex,amount in f['vertex_degree_exponents']:
            need(type(vertex)is int and 0<=vertex<nv and type(amount)is int and amount>0,'literal positive incidence')
            times[vertex].append(index)
    need(all(times),'complete vertex cover')
    first=[v[0] for v in times];last=[v[-1] for v in times]
    unit=[0]*nv;double=[0]*nv;winds=[0,0,0];marks=0;previous=1;layers=[]
    bits=sys.int_info.bits_per_digit;digitbytes=sys.int_info.sizeof_digit;base=sys.getsizeof(1)
    def integer_bytes(bitcount):return base+digitbytes*(max(1,(bitcount+bits-1)//bits)-1)
    tuplebytes=sys.getsizeof(())+3*struct.calcsize('P')
    for index,f in enumerate(factors,1):
        for vertex,amount in f['vertex_degree_exponents']:
            unit[vertex]+=int(amount==1);double[vertex]+=int(amount==2)
        for a in range(3):winds[a]+=f['K_exponents'][a]
        marks+=f['marked_exponent'];active=[v for v in range(nv) if first[v]<=index<last[v]]
        # Positive subset sums <=2 can be exactly0;1 iff oneunit;2 iff
        # onedouble or twodistinct unit orbit contributions. Larger terms do not fit.
        cardinalities=[[v,1+int(unit[v]>0)+int(double[v]>0 or unit[v]>=2)] for v in active]
        kranges=[1+min(L*L,v) for v in winds];yrange=1+min(4,marks)
        coordinate=yrange
        for q in kranges:coordinate*=q
        for v,q in cardinalities:coordinate*=q
        branch=2**index if index<=k else observed[k]*2**(index-k)
        upper=observed[index] if index<=k else min(coordinate,branch)
        need(upper<=coordinate and upper<=branch,'supported complete-layer upper')
        if index==k+1:need(upper>=65537,'preserved first overflow lower witness')
        payload=tuplebytes+integer_bytes(2*nv)+integer_bytes(((L*L+1)**3-1).bit_length())+integer_bytes(3)+integer_bytes(index+1)
        layers.append({'completed_layer':index,'observed_live_keys':observed[index] if index<=k else None,
            'observed_layer_complete':index<=k,'first_overflow_layer':index==k+1,
            'live_key_lower_bound':observed[index] if index<=k else 65537 if index==k+1 else 0,
            'live_key_upper_bound':upper,'branch_upper_bound':branch,'local_coordinate_superset_upper':coordinate,
            'active_vertices':active,'local_degree_cardinalities':cardinalities,'K_range_cardinalities':kranges,
            'marked_range_cardinality':yrange,'coefficient_value_upper':2**index,'packed_degree_bit_upper':2*nv,
            'simultaneously_retained_table_entries_upper':previous+upper,
            'conditional_per_entry_payload_bytes':payload,'conditional_two_table_payload_bytes_upper':payload*(previous+upper),
            'dictionary_allocator_transient_and_interpreter_bytes_included':False})
        previous=upper;guard()
    return {'schema':'P60_C181_SUPPORTED_PROJECTION_V001','L':L,'sector':domain['sector'],'axis_permutation':domain['axis_permutation'],
        'observed_complete_progress':progress,'actual_refusal':refusal,'actual_original_runtime':runtime,'all_layer_bounds':layers,
        'complete_algorithm_peak_live_keys_lower':65537,'complete_algorithm_peak_live_keys_upper':max(v['live_key_upper_bound'] for v in layers),
        'first_refused_complete_layer_size_known':False,'completed_frontier_regenerated':False,
        'first_refused_layer_upper':layers[k]['live_key_upper_bound'],
        'conditional_payload_model':'Current CPython sys.getsizeof maximal key tuple/three integers/coefficient; no dict/allocator/RSS bound',
        'future_seconds_upper':None,'future_RSS_bytes_upper':None,'program_cap_infeasibility_proved':False,
        'completion_within_program_caps_proved':False,'resource_feasibility':'UNDETERMINED',
        'partial_dimension_inferred':False,'higher_cap_run_authorized':False,'physical_release':False}
