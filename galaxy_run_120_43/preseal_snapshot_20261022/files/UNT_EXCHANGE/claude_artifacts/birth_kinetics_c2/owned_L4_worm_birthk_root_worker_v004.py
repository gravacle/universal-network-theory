"""Inert root-only worm-loop/channel-bearing-Birth/admission/family-pair capture worker V004 (delta of worm worker V003 3b408fb4...).
Requires external 9000s/4GiB RSS/2GiB output guard; soft8800s/3.5GiB/3.2million calls (time-proportional caps x2).
Same physical TRIAL, 1024 warmup (doubled),1024 measurements,2 chains,5 moves/sweep; max_sweeps 4096.
Fixed mixture: .25 occupancy,.10 worm loop,.20 Birth residence (c2v002: owner uniform among channel-bearing owners),.20 admission residence,.25 prior base. Fresh seed2026101702
is bound after preparation and before any sampling. No acceptance or retries.
Durable rows additionally carry the reference-dwell canonical key, Birth census and defect content U (durability V002).
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time
import traceback
import numpy as np

B = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
RELEASE0456={'author_path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0009_2026-10-16_done-0456.md', 'author_sha256': '9c493b325573e1ff5ef9fbf294e3e739fe367999069db40b585dd6970bf7e03f', 'review_path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/admission_residence_review_0457/REVIEW_0457_V001.md', 'review_sha256': '482dc9047c07be8eb111827966179f9d0dbc1c353a0a24bead1d0d05ba9908e2', 'review_return_path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0011_2026-10-16_done-0457.md', 'review_return_sha256': 'e86bf046cefb8fd9edd8ddc08bc8a7fd6dd4a8ce1d36861d0f5f5e9e58c11a4b', 'interface_path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/admission_residence_0456/INTERFACE_0456_V001.md', 'interface_sha256': '337a7973f008b2846aa334dde8855106db14371d7cca5270a899a552cd517e58'}
SOURCES = {
    'admission_module': (X/'admission_residence_0456/admission_residence_transport_c3v001.py', '5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653'),
    'durability': (X/'worm_move_c2_0467/owned_worm_committed_capture_durability_v002.py', 'c0646a9380ef59d1f95732faf732243f91e850ec3b94f8d3510ccdd5602b40f9'),
    'recipe': (X/'birth_kinetics_c2/owned_L4_worm_birthk_recipe_v004.py', '997f4d1ff45112d0d7ce4d409e07b5fd85653348cef3a12cbfd2280152514597'),
    'birth_module': (X/'birth_kinetics_c2/owned_worldline_birth_residence_transport_c2v002.py', '6c14cb85e6a4fbb5d6ee08d18eb38a093a10d071924ad70579ca291756a67a82'),
    'worm_module': (X/'worm_move_c2_0467/owned_worm_loop_whole_path_c2v001.py', '9fef6042eb1e13157d19a4d4381b4c73ef6e26d779f49ad7c477f1d44b9f470d'),
    'operator': (X/'owned_retained_response_0405/owned_parent_operator_v003.py', 'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07'),
    'sampler': (B/'helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v006.py', '896cadbbe4059a77b33f370d643cfa7657c0e031d61d1aa46886e88eb4f576b7'),
    'adapter': (B/'helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py', '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77'),
    'occupancy': (B/'helpers/coefficient_method/owned_current_graph_occupancy_transport_v001.py', 'dedc932832ed41fbbb4661a2cfb97f127aee399f859f8ad3742f66645a8d4837'),
    'family_recipe': (B/'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py', '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7'),
    'statistics': (B/'helpers/coefficient_method/owned_uniform_reweighting_statistics_v001.py', '85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a'),
}


def load(name, path, expected):
    if expected is None or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Missing or changed frozen source: '+str(path))
    spec = importlib.util.spec_from_file_location('root_collective_'+name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def clean(value):
    if isinstance(value, np.ndarray):
        return clean(value.tolist())
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [clean(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return {'nonfinite_diagnostic': repr(value)}
    return value


def main(output):
    started = time.monotonic()
    prepared = None
    result = {
        'scope': 'Full-owned L4 exploratory collective response, all momenta from the same closed paths. Not a calibration or physical galaxy prediction.',
        'source_pins': {k: {'path': str(p), 'sha256': s} for k, (p, s) in SOURCES.items()},
        'coefficients_accepted_for_galaxy': False,
    }
    output = Path(output)
    # Reserve the output exclusively before doing work, preserving earlier runs.
    with output.open('x') as destination:
        try:
            for role in ('author','review','review_return','interface'):
                path=RELEASE0456[role+'_path'];pin=RELEASE0456[role+'_sha256']
                if not path or len(pin)!=64 or hashlib.sha256(Path(path).read_bytes()).hexdigest()!=pin:raise ValueError('Missing or changed frozen 0456/0457 release')
            result['admission_release']=dict(RELEASE0456)
            modules = {k: load(k, p, s) for k, (p, s) in SOURCES.items()}
            recipe = modules['recipe']
            result['trial'] = dict(modules['family_recipe'].TRIAL)
            with output.with_name('progress.jsonl').open('x') as progress:
                print('Preparing full-owned L4 collective response', flush=True)
                prepared = recipe.prepare(family_recipe=modules['family_recipe'],
                    worm_module=modules['worm_module'],birth_module=modules['birth_module'],admission_module=modules['admission_module'],
                    operator_module=modules['operator'],
                    sampler_module=modules['sampler'], diamond_adapter=modules['adapter'],
                    occupancy_module=modules['occupancy'], statistics_module=modules['statistics'],
                    progress_stream=progress,
                    accepted_sampler_sha256=SOURCES['sampler'][1])
                args=prepared['arguments']
                if (len(args['chain_generators'])!=2 or args['burn_in_sweeps']!=512
                    or args['measurement_sweeps']!=1024 or args['move_parameters']['moves_per_sweep']!=5):
                    raise ValueError('Frozen sampling schedule mismatch')
                if (args['caps']!={'max_events_per_path':10000,'max_total_events':2400000,'max_sweeps':3072,'max_channel_enumerations':1600000}
                    or prepared['reweighting_capture_record']['burn_in_per_chain']!=512):
                    raise ValueError('Frozen caps/capture record mismatch')
                # V004: warmup doubled to 1024 (measurements stay 1024); time-proportional caps scaled x2 with
                # the hard wall (4500s->9000s); RSS, output and per-path caps unchanged; max_sweeps=2*(1024+1024).
                args['burn_in_sweeps']=1024
                prepared['reweighting_capture_record']['burn_in_per_chain']=1024
                args['caps']={'max_events_per_path':10000,'max_total_events':4800000,'max_sweeps':4096,'max_channel_enumerations':3200000}
                clock=prepared['counters']
                def budget_state():
                    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    rb=rss if sys.platform=='darwin' else rss*1024
                    elapsed=time.monotonic()-clock['start']
                    return {'elapsed_seconds':elapsed,'peak_rss_bytes':rb,'primitive_calls':clock['primitive_calls'],
                            'stop_requested':elapsed>=8800. or rb>=3584*1024**2 or clock['primitive_calls']>=3200000}
                prepared['budget_state']=budget_state
                args['budget_hook']=lambda: bool(budget_state()['stop_requested'])
                result['schedule_binding']={'burn_in_sweeps':1024,'measurement_sweeps':1024,'chains':2,'moves_per_sweep':5,
                    'prepared_burn_in_sweeps':512,'caps':dict(args['caps']),'prepared_caps':{'max_events_per_path':10000,
                    'max_total_events':2400000,'max_sweeps':3072,'max_channel_enumerations':1600000},
                    'soft_budget':{'wall_seconds':8800.,'peak_rss_bytes':3584*1024**2,'primitive_calls':3200000},
                    'prepared_soft_budget':{'wall_seconds':4400.,'peak_rss_bytes':3584*1024**2,'primitive_calls':1600000},
                    'method':'replaced after preparation and before sampling; budget clock and guarded call counter are the prepared ones'}
                old_seed=prepared['reweighting_capture_record']['rng_entropy']
                args['chain_generators']=[np.random.default_rng(s) for s in np.random.SeedSequence(2026101702).spawn(2)]
                prepared['reweighting_capture_record']['rng_entropy']=2026101702
                result['rng_binding']={'prepared_recipe_entropy':old_seed,'actual_entropy':2026101702,
                    'streams':2,'method':'SeedSequence.spawn(2); replaced before sampling'}
                result['worm_loop_request']={'probability_within_base':2./15.,
                    'total_worm_loop_probability':.75*(2./15.),'total_occupancy_probability':.25,'total_admission_residence_probability':.20,
                    'total_birth_residence_probability':.20,'total_prior_base_probability':.25,
                    'fixed_start_roster':prepared['worm_binding']['owner_roster'],'maximum_walk_steps':modules['worm_module'].MAX_WALK_STEPS,'lookahead':modules['worm_module'].LOOKAHEAD,'selection':'Uniform fixed original start; uniform viable occupied first edge; uniform viable alternating continuation until first revisit; exact reverse-walk Hastings factor; no eligibility resampling'}
                result['reweighting_capture_request'] = prepared['reweighting_capture_record']
                result['birth_residence_request']={'module_version':modules['birth_module'].MODULE_VERSION,
                    'total_birth_residence_probability':.20,'fixed_owner_roster':prepared['worm_binding']['owner_roster'],
                    'selection':'Uniform among fixed-roster owners with a Birth/reverse mark at the reference dwell (one union palette enumeration); uniform mark; exact owner-count and roster Hastings factors'}
                print('Sampling two chains with fixed worm-loop/channel-bearing-Birth/occupancy/family-pair mixture', flush=True)
                durable=modules['durability'].DurableCapture(directory=output.with_name('committed_capture'),
                    sampler=modules['sampler'],statistics=modules['statistics'],prepared=prepared,
                    clean=clean,pins=result['source_pins'],state_labels=modules['operator'].state_labels,
                    dstar=modules['family_recipe'].TRIAL['dstar'])
                durable.install()
                try:
                    sampled = recipe.run_prepared(prepared=prepared)
                finally:
                    durable.close()
            # Preserve every actual returned row, status and uncertainty result.
            # No physical conversion can replace this with an exception status.
            result['sampler_result'] = sampled
            result['status'] = sampled['status']
            result['runtime_counters'] = dict(prepared['counters'])
            result['budget_at_return'] = prepared['budget_state']()
        except BaseException as exc:
            result['status'] = 'FAILED'
            result['exception'] = {'type': type(exc).__name__, 'message': str(exc),
                                   'traceback': traceback.format_exc()}
            if prepared is not None:
                result['runtime_counters'] = dict(prepared['counters'])
        if prepared is not None:
            result['mixture_counters']=dict(prepared['mixture_counters'])
            result['worm_counters']=dict(prepared['worm_binding']['counters'])
            result['partial_output_scope']='Committed capture blocks retained independently; final partial block flushed on ordinary exception. Hard termination can lose at most16 newest rows. Non-resumable; no fabricated RNG/path restart. Full returned sampler prefixes preserved if returned.'
        result['elapsed_seconds'] = time.monotonic()-started
        json.dump(clean(result), destination, indent=2, allow_nan=False)
        destination.write('\n')
        destination.flush()
    print(json.dumps({'status': result['status'], 'elapsed_seconds': result['elapsed_seconds'],
                      'output': str(output)}), flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
