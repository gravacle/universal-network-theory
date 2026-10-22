"""Inert preparation for one root-owned, bounded collective-response attempt.

UNT 0423 CAPTURE C2V001: worker V007 (sha256
d691efbb9f62ded53ccde5076af45fe027c5f7456cf21126071f5ce827a7f17e) plus ONLY the raw
reweighting capture binding: sampler pairallk V002, statistics V001 and recipe V009
capture C2V001 are pinned and checked from bytes at load; the full sampler dictionary,
including reweighting_statistics and partial prefixes, is saved unchanged. No acceptance.
Merged sampler and recipe V009 are frozen to separately reviewed bytes. Entire raw sampler output is
saved before any downstream scientific conversion; no automatic retry or fit.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
import traceback
import numpy as np

B = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
SOURCES = {
    'operator': (X/'owned_retained_response_0405/owned_parent_operator_v003.py', 'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07'),
    'sampler': (B/'helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v002.py', 'bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba'),
    'adapter': (B/'helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py', '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77'),
    'occupancy': (B/'helpers/recovered_packet_audit/owned_worldline_occupancy_involution_v002.py', '7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5'),
    'recipe': (X/'reweight_capture_0423/owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py', 'a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95'),
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
            modules = {k: load(k, p, s) for k, (p, s) in SOURCES.items()}
            recipe = modules['recipe']
            result['trial'] = dict(recipe.TRIAL)
            with output.with_name('progress.jsonl').open('x') as progress:
                print('Preparing full-owned L4 collective response', flush=True)
                prepared = recipe.prepare(operator_module=modules['operator'],
                    sampler_module=modules['sampler'], diamond_adapter=modules['adapter'],
                    occupancy_module=modules['occupancy'], statistics_module=modules['statistics'],
                    progress_stream=progress,
                    accepted_sampler_sha256=SOURCES['sampler'][1])
                result['reweighting_capture_request'] = prepared['reweighting_capture_record']
                print('Sampling two chains with occupancy, event-pair and regrowth moves', flush=True)
                sampled = recipe.run_prepared(prepared=prepared)
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
        result['elapsed_seconds'] = time.monotonic()-started
        json.dump(clean(result), destination, indent=2, allow_nan=False)
        destination.write('\n')
        destination.flush()
    print(json.dumps({'status': result['status'], 'elapsed_seconds': result['elapsed_seconds'],
                      'output': str(output)}), flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
