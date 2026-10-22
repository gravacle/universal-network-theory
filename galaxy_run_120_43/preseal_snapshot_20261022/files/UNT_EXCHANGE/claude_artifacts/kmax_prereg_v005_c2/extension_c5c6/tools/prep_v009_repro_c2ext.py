"""Bitwise reproduction test of the DDO154 route-A prep successor v009 against SAVED route-A prefixes (Claude2 lane,
kmax extension C5/C6).  Operator/symbol evaluation only: no route-A iteration, no column solve, no stage launch.

For one saved prefix run (its stages/01_route_a/request.json, seed and checkpoint), this script
  1. loads prep v009 (this lane, prep_successor/) by path, applies the SAME module patch the saved request applied
     (COEFFICIENT/COEFFICIENT_SHA = the A2 pooled grid), and calls prepare_inputs(**seed.numerical_inputs), exactly the
     call the binding ddo_composite_stable_cached_binding_v002 makes;
  2. recomputes, with the pinned checkpoint module's own digest(), every IDENTITY.inputs_sha256 entry
     (fixed_positions_m, fixed_integrated_columns_J, initial_gas_fourier_J, fixed_source_fourier_J, gas_columns and every
     fourier_arguments entry) and compares it with the saved IDENTITY.json;
  3. builds the pinned lapse-inverse cache facade (owned_scalar_lapse_inverse_cache_v001 on base quadrature v005, a new
     log directory under this lane) and runs ONE prepare at the iteration-0 source current = fixed + gas, exactly as the
     solver does, then compares digest() of gas, current, fixed, prepared wavevectors, prepared weighted responses and the
     whole prepared metric response with the saved iteration_0000/START.json, and the sha256 of the two node-diagnostic
     streams the facade writes with the saved attempt's node_diagnostics/iteration_000000_{nodes,scaled_nodes}.jsonl;
  4. decodes the saved caller record and lists every place the prep path/sha occurs (the only fields a prep successor
     can change in the route-A identity), and checks the prep-loaded source pins against it.
Writes only OUT (must not exist).  numpy only; run with single-thread BLAS env, nice 10.
usage: python3 -I -B prep_v009_repro_c2ext.py RUN_DIR OUT_DIR
"""
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

PREP_V009 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/prep_successor/'
                 'ddo_actual_initial_source_preparation_v009.py')
PREP_V009_SHA = 'b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
H = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit')
PINS = {
    'checkpoint': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'),
    'solver': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py', '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644'),
    'stream': (H / 'owned_scalar_lapse_inverse_cache_v001.py', '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
    'base': (H / 'owned_physical_fourier_metric_quadrature_v005.py', '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
}
OLD_PREPS = {'ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42': 'v007',
             'bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62': 'v008'}


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(name, path, sha):
    if sha_file(path) != sha:
        raise SystemExit('PIN MISMATCH %s %s' % (name, path))
    spec = importlib.util.spec_from_file_location('c2ext_' + name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def walk_find(obj, needle, path='caller'):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if needle in k:
                out.append(path + '[key %r]' % k)
            out += walk_find(v, needle, path + '.' + k)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            out += walk_find(v, needle, path + '[%d]' % i)
    elif isinstance(obj, str) and needle in obj:
        out.append(path)
    return out


def main():
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    rep = {'schema': 'UNT_PREP_V009_REPRO_C2EXT_V001', 'run': str(run), 'prep_v009': {'path': str(PREP_V009), 'sha256': sha_file(PREP_V009)}}
    if rep['prep_v009']['sha256'] != PREP_V009_SHA:
        raise SystemExit('prep v009 sha changed')
    req_p = run / 'stages/01_route_a/request.json'
    req = json.loads(req_p.read_text())
    rep['request'] = {'path': str(req_p), 'sha256': sha_file(req_p)}
    a = req['argv']
    seed_p, seed_sha = Path(a[a.index('--seed') + 1]), a[a.index('--seed-sha256') + 1]
    if sha_file(seed_p) != seed_sha:
        raise SystemExit('seed sha mismatch')
    seed = json.loads(seed_p.read_text())
    ni = seed['numerical_inputs']
    patches = req['module_patches']
    if len(patches) != 1:
        raise SystemExit('expected exactly one prep module patch')
    old_prep_sha = patches[0]['sha256']
    rep['saved_prep'] = {'path': patches[0]['path'], 'sha256': old_prep_sha, 'version': OLD_PREPS.get(old_prep_sha)}
    if (req.get('stage_dict_items') or {}).get('LOCAL', {}).get('prep', {}).get('sha256', old_prep_sha) != old_prep_sha:
        raise SystemExit('LOCAL prep differs from patched prep')
    cm = load('checkpoint', *PINS['checkpoint'])
    solver = load('solver', *PINS['solver'])
    stream = load('stream', *PINS['stream'])
    base = load('base', *PINS['base'])
    prep = load('prep_v009', PREP_V009, PREP_V009_SHA)
    for k, v in patches[0]['set'].items():   # identical semantics to the driver shim: {'__path__': p} -> Path(p)
        setattr(prep, k, Path(v['__path__']) if isinstance(v, dict) and '__path__' in v else v)
    rep['seed'] = {'path': str(seed_p), 'sha256': seed_sha, 'fourier_points_per_axis': ni['fourier_points_per_axis'],
                   'grid_version': (ni.get('composite_grid_spec') or {}).get('version')}
    data = prep.prepare_inputs(**ni)
    rep['t_prepare_inputs_s'] = round(time.time() - t0, 1)
    cp = run / 'stages/01_route_a/checkpoint'
    ident = json.loads((cp / 'IDENTITY.json').read_text())
    saved = ident['identity']['inputs_sha256']
    fa = data['fourier_arguments']
    waves = fa['k_physical']
    fixed = solver._supplied_fixed_source(data['fixed_source_fourier_J'], len(waves))
    gas = solver.np.asarray(data['initial_gas_fourier_J'], dtype=complex)
    mine = {'fixed_positions_m': cm.digest(data['fixed_positions_m']),
            'fixed_integrated_columns_J': cm.digest(data['fixed_integrated_columns_J']),
            'initial_gas_fourier_J': cm.digest(gas), 'fixed_source_fourier_J': cm.digest(fixed),
            'gas_columns': cm.digest(data['gas_columns']),
            'fourier_arguments': {k: cm.digest(v) for k, v in sorted(fa.items())}}
    cmp_id = {}
    for k, v in mine.items():
        if k == 'fourier_arguments':
            for kk, vv in v.items():
                cmp_id['fourier_arguments.' + kk] = vv == saved['fourier_arguments'].get(kk)
            for kk in saved['fourier_arguments']:
                if kk not in v:
                    cmp_id['fourier_arguments.' + kk] = False
        else:
            cmp_id[k] = v == saved.get(k)
    rep['identity_inputs_sha256'] = {'n': len(cmp_id), 'equal': sum(cmp_id.values()), 'differing': sorted(k for k, ok in cmp_id.items() if not ok)}
    # caller record: where the prep path/sha occurs, and source-pin agreement
    caller = cm.decode(ident['identity']['caller']['record'])
    rep['caller_prep_occurrences'] = {'by_sha': walk_find(caller, old_prep_sha), 'by_basename': walk_find(caller, Path(patches[0]['path']).name)}
    sp_saved = caller['source_parameters']['source_pins']
    sp_mine = {k: v for k, v in data['source_pins'].items()}
    prep_path_old = patches[0]['path']
    rep['source_pins'] = {'n_prep_loaded': len(sp_mine),
                          'all_equal_in_saved_caller': all(sp_saved.get(k) == v for k, v in sp_mine.items()),
                          'differing': sorted(k for k, v in sp_mine.items() if sp_saved.get(k) != v),
                          'prep_file_in_prep_loaded_pins': prep_path_old in sp_mine or str(PREP_V009) in sp_mine}
    rep['numerical_controls_equal'] = cm.digest(caller['numerical_controls']) == cm.digest({k: v for k, v in ni.items() if k != 'progress_directory'})
    # iteration-0 prepared response through the pinned cache facade (the solver's first prepare)
    t1 = time.time()
    facade = stream.make_fourier_module(base_module=base, log_directory=out / 'node_diagnostics', start_iteration=0)
    current = fixed + gas
    prepared = facade.prepare(**dict(fa), source_density_fourier=current)
    rep['t_iteration0_prepare_s'] = round(time.time() - t1, 1)
    start = json.loads((cp / 'iteration_0000/START.json').read_text())
    s_cmp = {'gas_fourier_J': cm.digest(gas) == start['gas_fourier_J']['array_sha256'],
             'current_source_fourier_J': cm.digest(current) == start['current_source_fourier_J']['array_sha256'],
             'fixed_source_fourier_J': cm.digest(fixed) == start['fixed_source_fourier_J']['array_sha256'],
             'prepared_wavevectors': cm.digest(prepared['wavevectors']) == start['prepared_wavevectors']['array_sha256'],
             'prepared_weighted_responses': cm.digest(prepared['weighted_responses']) == start['prepared_weighted_responses']['array_sha256'],
             'prepared_metric_response_sha256': cm.digest(prepared) == start['prepared_metric_response_sha256']}
    rep['start_iteration_0000'] = {'path': str(cp / 'iteration_0000/START.json'), 'sha256': sha_file(cp / 'iteration_0000/START.json'),
                                   'checks': s_cmp, 'all_equal': all(s_cmp.values())}
    nd_saved = run / 'stages/01_route_a/attempt_000/node_diagnostics'
    nd = {}
    for nm in ('iteration_000000_nodes.jsonl', 'iteration_000000_scaled_nodes.jsonl'):
        a_, b_ = out / 'node_diagnostics' / nm, nd_saved / nm
        nd[nm] = {'mine_sha256': sha_file(a_), 'saved_sha256': sha_file(b_) if b_.is_file() else None}
        nd[nm]['equal'] = nd[nm]['mine_sha256'] == nd[nm]['saved_sha256']
    rep['node_diagnostics_iteration0'] = nd
    rep['verdict'] = ('PASS_BITWISE' if (not rep['identity_inputs_sha256']['differing'] and rep['start_iteration_0000']['all_equal']
                                          and all(x['equal'] for x in nd.values()) and rep['source_pins']['all_equal_in_saved_caller']
                                          and rep['numerical_controls_equal']) else 'FAIL')
    rep['elapsed_s'] = round(time.time() - t0, 1)
    with open(out / 'PREP_V009_REPRO.json', 'x') as f:
        json.dump(rep, f, indent=1, sort_keys=True)
    print(json.dumps({'run': run.name, 'verdict': rep['verdict'], 'identity': rep['identity_inputs_sha256'],
                      'start': s_cmp, 'nodes': {k: v['equal'] for k, v in nd.items()}, 'elapsed_s': rep['elapsed_s']}))


if __name__ == '__main__':
    main()
