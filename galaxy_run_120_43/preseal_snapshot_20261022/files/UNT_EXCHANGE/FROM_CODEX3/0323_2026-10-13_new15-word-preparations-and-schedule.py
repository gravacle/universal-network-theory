"""SOURCE ONLY. New initial-word family; original Hamiltonian/kernel unchanged.
No oldq11seed aliases/reuse. Root injects these explicit roles into old executor.
"""
from fractions import Fraction as F
from types import SimpleNamespace

TYPES = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'OLD_READY_SITE0',
         'OLD_COHERENT_PLUS_I', 'OLD_COHERENT_MINUS_I')
WORDS = ('00', '01', '10')
SEEDS = tuple('Q'+word+'_'+kind for word in WORDS for kind in TYPES)
HORIZONS = (F(1, 8), F(1, 4), F(1, 2), F(1))
SCALE = 1 << 80


def need(ok, why):
    if not ok:
        raise ValueError(why)


def identity(seed):
    need(type(seed) is str and seed in SEEDS, 'literal new15 seed; no oldq11 alias')
    return seed[1:3], seed[4:]


def exact_definitions():
    out = {}
    for word in WORDS:
        q = int(word[0])+2*int(word[1])
        a, b, r = (0, 3, 1, q, 0, 1), (0, 3, 2, q, 0, 1), (0, 3, 0, q, 1, 0)
        specs = [[(a, F(1), F(0))], [(b, F(1), F(0))], [(r, F(1), F(0))],
                 [(a, F(3, 5), F(0)), (b, F(0), F(4, 5))],
                 [(a, F(3, 5), F(0)), (b, F(0), F(-4, 5))]]
        for kind, entries in zip(TYPES, specs):
            out['Q'+word+'_'+kind] = entries
    return out


def bind_preparations(full_states, components):
    states = [tuple(s) for s in full_states]
    need(len(states) == len(set(states)) == 20672, 'complete authenticated native input basis')
    native = {s: i for i, s in enumerate(states)}
    need(len(components) == 5 and sorted(map(len, components)) == [2048, 2048, 3072, 3072, 10432], 'all five components')
    flat = [i for g in components for i in g]
    need(all(type(i) is int for i in flat) and sorted(flat) == list(range(20672)), 'whole component partition')
    owner = {i: k for k, g in enumerate(components) for i in g}
    need(len(components[0]) == 10432 and all(owner[i] == 0 for i, s in enumerate(states) if s[0] == 0),
         'unchanged active component includes every old state')
    result = {}
    for seed, terms in exact_definitions().items():
        word, kind = identity(seed)
        entries, weights = [], [F(0)]*5
        for state, re, im in terms:
            i = native[state]
            need(bin(state[2]).count('1')+bin(state[4]).count('1') == 1 and state[4]|state[5] == 1
                 and state[4]&state[5] == 0, 'exact Q1/allAv1 preparation')
            weights[owner[i]] += re*re+im*im
            entries.append({'index': i, 'state': list(state), 'amplitude': [re, im]})
        need(weights == [1, 0, 0, 0, 0], 'full newword exact component weights')
        result[seed] = {'entries': entries, 'all_component_weights': weights, 'sharp_Q': 1,
                        'active_mask': 1, 'old_q_word': word, 'preparation_type': kind,
                        'family': 'P64_NEW15_INITIAL_WORDS_V001',
                        'energy_distribution_matching': 'NOT_ASSUMED_C157_PAIRWISE_CLASSIFICATION_REQUIRED',
                        'S1_physical_preparation': 'NOT_DERIVED'}
    need(tuple(result) == SEEDS, 'entire frozen15 preparation order')
    return result


def stage_schedule(stage):
    need(type(stage) is int and 0 <= stage < 4, 'four frozen horizons')
    start = F(0) if stage == 0 else HORIZONS[stage-1]
    stop = HORIZONS[stage]
    count = (64, 64, 128, 256)[stage]
    times = [start+F(2*k+1, 1024) for k in range(count)]+[stop]
    last, steps = start, []
    for t in times:
        steps.append({'time': t, 'dt': t-last, 'kind': 'ENDPOINT' if t == stop else 'MIDPOINT'})
        last = t
    return {'stage': stage, 'start': start, 'stop': stop, 'steps': steps,
            'full_prefix_panels': int(512*stop), 'new_midpoints': count,
            'seeds_to_launch': SEEDS, 'preexisting_A_prefix_reused': False}


def resource_prospect(stage):
    need(type(stage) is int and 0 <= stage < 4, 'four frozen resource stages')
    steps = (65, 65, 129, 257)[stage]
    payload, headers, reserve = steps*50*10432*48, steps*50*16, 256*2**20
    return {'stage': stage, 'seeds': 15, 'steps_per_seed': steps, 'vector_files_per_seed': steps*50,
            'endpoints_per_seed': steps*50*10432*4, 'actions_per_seed': steps*16,
            'gaussian_visits_per_seed': steps*16*112048, 'vector_payload_bytes_per_seed': payload,
            'vector_headers_bytes_per_seed': headers, 'producer_complete_output_cap_per_seed': payload+headers+reserve,
            'reader_output_cap_per_seed': reserve, 'complete_new_output_cap_stage': 15*(payload+headers+2*reserve),
            'producer_seconds_per_seed': 600, 'producer_RSS_bytes': 2*2**30,
            'reader_seconds_per_seed': 900, 'reader_RSS_bytes': 3*2**30,
            'projected_producer_seconds_per_seed': F('40.202861709')*steps/65,
            'projected_reader_seconds_per_seed': F('81.004821042')*steps/65,
            'projection_is_guarantee': False}


def campaign_storage_prospect():
    parts = [resource_prospect(k) for k in range(4)]
    return {'schema': 'P64_NEW15_COMPLETE_STORAGE_PROSPECT_V001', 'new_seeds': list(SEEDS),
            'producer_stage_jobs': 60, 'reader_stage_jobs': 60, 'vector_files': 15*516*50,
            'raw_complete_vector_bytes': 15*516*50*(16+48*10432),
            'all_stage_scientific_caps_sum': sum(p['complete_new_output_cap_stage'] for p in parts),
            'additional_whole_runtime_bytes_must_be_reserved_by_root': True,
            'root_whole_campaign_and_each_remaining_wave_free_space_required': True,
            'root_pool_exclusive': True, 'no_partial_output_acceptance': True,
            'runtime_projection_is_guarantee': False, 'original_q11_repropagated': False}


def enclose_initial_seed(exact_seed):
    need(isinstance(exact_seed, dict) and exact_seed, 'complete sparse exact initial state')
    center = [(0, 0)]*10432
    norm, error = F(0), F(0)
    for j, value in exact_seed.items():
        need(type(j) is int and 0 <= j < 10432 and len(value) == 2, 'native full seed index')
        need(all(type(z) in (F, int, str) for z in value), 'exact rational seed amplitude')
        re, im = map(F, value)
        a, b = (re*SCALE).__floor__(), (im*SCALE).__floor__()
        center[j] = (a, b)
        norm += re*re+im*im
        error += abs(re-F(a, SCALE))+abs(im-F(b, SCALE))
    need(norm == 1 and error < F(2, SCALE), 'exact norm and unchanged I80 L1-to-L2 seed bound')
    return center, error


def roles():
    """Pinned factory only; root must snapshot this exact source for both roles."""
    P = SimpleNamespace(__file__=__file__, stage_schedule=stage_schedule,
                        resource_prospect=resource_prospect, enclose_initial_seed=enclose_initial_seed)
    S = SimpleNamespace(__file__=__file__, bind_preparations=bind_preparations)
    return P, S
