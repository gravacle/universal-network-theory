"""New k=.01/Mpc transfer at the sealed joint V003 tuple; no fit/atomic replay.

Only root may launch --execute after complete static review. Imported pure
solver implementation is unchanged and authenticated before importing it.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import math
import os
import sys
import time
import types

BASE = Path(__file__).resolve().parent
STEM = 'INVARIANT_CLOCK_JOINT_V003_RECOMBINATION_TRANSFER_V001'
PROTOCOL = BASE / (STEM + '.md')
PROTOCOL_SHA = '57e38ca36b6adc2488cfa460f147aa04384b6899c4a500639afba14307820b87'
PINS = {'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'invariant_clock_joint_calibration_v003.py': '9610ad24604eac4ac674038c97cccc66c354bb9a2f32037a87d62bccb459eeea', 'invariant_clock_recombination_transfer_v001.py': '6619fdc9cffe95703522acb0969ed45a00c483a994eea005907b789e977fb5b6', 'invariant_clock_recombination_transfer_v002.py': '54674a431945eb7e17fc2b39af2324c923d8cfc5e991dc87a8cf96465dd1fa45', 'invariant_clock_plasma_v001.py': '08cfd9e54759db07683bf652e32ad5aa69ec3006090f548e5d82b5678e8a6a28', 'invariant_clock_radiation_v001.py': '0f30f231996feeeb3abe6f6f40326de3a34478adaac11e0520a5e1cf3e8bea3e', 'invariant_clock_transfer_v001.py': 'fad14451f7658c751a396c660638c5cb59e495b056fcbb5d09b0c8bc5a3415ca', 'invariant_clock_acoustic_v001.py': '9cd21314b29d11cedba04eb6e53799aa7847d40c1280718913d2a392bb3db396', 'plane_canonical_evolution_v001.py': 'e2b634317ff0f22c77541a99c615dfcfcfb65e24c59013d8b09b5d322b740907', 'charged_clock_response_v001.py': 'b7f539c914d3bf4af31f6b523b2a3c55b88c75fd406528358273f6d4ef95e5ba', 'bounded_clock_shared_prediction_v001.py': 'dd3d22e143e10b977fb7c0d6a2ce0a7cd260e0ddb077e3a9cf56e9e471f0b896', 'hyrec_standard_oracle_v001.py': '2b176013f136aafd9495e448c882d1b6860769004be1027c90b5f094880be269', 'PLANE_CMC_INITIAL_DATA_V002_RESULT.json': '04e6cdeac4c581671dac8afe6cb1229993f7ee5eadc54a560fa5fb79efa8535f', 'INVARIANT_CLOCK_RECOMBINATION_TRANSFER_V002_RESULT.json': '07fd5190198b2cf309b14598bfbae25def98d65b34db64b85dfe7a649da144cc', 'INVARIANT_CLOCK_LATE_LENSING_V001_RESULT.json': '642e2289f9ea2fc2790e3c6abcec823855e8b66810cbcd4864175d6f3f31b8c6', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_DEFAULT_OUTPUT.json': '782bf0351bc99e1d72f9cbf215cec95ae99dd0f571d47574d160300208461274', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_HALF_OUTPUT.json': 'f1e9312dc9f1f696a7e65d06f345da9daad814e0076456f9986665f51bb997c1', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_REFERENCE_DEFAULT_OUTPUT.json': '50fe2c2d09b7e4dbc2a3bfac04da53a81d466bf0bd049e93c906c1543d2a779b', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_REFERENCE_HALF_OUTPUT.json': 'd026fb741fda6cd400d9fdca9e4589ba8d9c76adc06bda4ac737d4153d7ccc11', 'hyrec_inputs_v001/HYREC_BAO_POINT10_PANEL_V001_RESULTS.json': 'a43ce0b033b84ddb3f72ed873200e9713e335d6cbc2c54c137807b491a71c623', 'hyrec_inputs_v001/HYREC_BAO_INTERVAL_SAVED_AUDIT_V003_RESULTS.json': 'b53c9b477469641d4db082f0583c633c63863f3b134f57e0b097a9cb19487aba', 'invariant_clock_joint_v003_recombination_transfer_v001_REVIEW_DRAFT_V001.py': '010734aaed729ee87f5a293a5aff682aad886848334df983c2e2105bfe64424c', 'INVARIANT_CLOCK_JOINT_V003_RECOMBINATION_TRANSFER_V001_REVIEW_DRAFT_V001.md': 'ad940e9a9056ca20941effb26b03877f1bb35b04b3282e08d158a0205fa23aa4'}
CAL = BASE / 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json'
CP = BASE / (STEM + '_CHECKPOINTS')
MANIFEST = BASE / (STEM + '_MANIFEST.json')
JOURNAL = BASE / (STEM + '_JOURNAL.jsonl')
RESULT = BASE / (STEM + '_RESULT.json')
REPORT = BASE / (STEM + '_REPORT.md')
RECEIPT = BASE / (STEM + '_RECEIPT.json')
ERROR = BASE / (STEM + '_ERROR.json')
TRIALS = [('COARSE', 4096, 16, 48, 1e-7, 'half', 1),
          ('FINE', 8192, 16, 48, 1e-7, 'half', 1),
          ('START', 8192, 16, 48, 5e-8, 'half', 1),
          ('HIERARCHY', 8192, 20, 64, 1e-7, 'half', 1),
          ('ATOMIC', 8192, 16, 48, 1e-7, 'default', 1),
          ('THIN', 8192, 16, 48, 1e-7, 'half', 2)]
K_PHYSICAL = .01
AF = 1 / 801
CONTROLS = []
INPUTS = {}
GAUSS_STEP_SHA = '53faaa3ad155bae52ac092c3c072e3eb61f863402760a161478cff26b62af8d0'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(o):
    return hashlib.sha256(canonical(o).encode()).hexdigest()


def strict(ok, message):
    if not ok:
        raise AssertionError(message)


def check(name, error, tolerance):
    value = float(error)
    CONTROLS.append(dict(name=name, error=value, tolerance=tolerance,
                         passed=bool(math.isfinite(value) and value <= tolerance)))


def atomic(p, o, markdown=False):
    strict(not p.exists(), 'Exclusive output already exists: ' + str(p))
    tmp = p.with_name(p.name + '.TMP_' + str(os.getpid()))
    strict(not tmp.exists(), 'Preserve orphan temporary output: ' + str(tmp))
    with tmp.open('x') as stream:
        stream.write(o if markdown else json.dumps(o, indent=2, allow_nan=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    strict(not p.exists(), 'Output appeared during write: ' + str(p))
    os.rename(tmp, p)
    p.chmod(0o444)


def seals():
    for p, h in INPUTS.items():
        strict(sha(p) == h, 'Changed input: ' + p)


def load_gauss_only(np):
    name = 'charged_clock_response_v001'
    strict(name not in sys.modules, 'Legacy charged helper already imported')
    path = BASE / (name + '.py')
    source = path.read_text()
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'gauss_step']
    strict(len(nodes) == 1 and hashlib.sha256(ast.get_source_segment(source, nodes[0]).encode()).hexdigest() == GAUSS_STEP_SHA,
           'Exact unchanged Gauss function span')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__dict__.update(math=math, np=np)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), module.__dict__)
    sys.modules[name] = module


def event(stage, **fields):
    rows = [json.loads(s) for s in JOURNAL.read_text().splitlines()] if JOURNAL.exists() else []
    previous = digest(rows[-1]) if rows else None
    row = dict(index=len(rows), stage=stage, pid=os.getpid(),
               input_map_sha256=digest(INPUTS), previous_sha256=previous, **fields)
    with JOURNAL.open('a') as stream:
        stream.write(canonical(row) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def history_schema(hist, identity, names, np):
    strict(hist['steps'] == identity['steps'] and hist['ai'] == identity['ai'], 'Checkpoint time geometry')
    strict(hist['lg'] == identity['lg'] and hist['ln'] == identity['ln'], 'Checkpoint hierarchy')
    strict(hist['dust'] == identity['dust'] and hist['names'] == names, 'Checkpoint branch/layout')
    ss = hist['snapshots']
    strict(len(ss) >= 67 and all(ss[i]['a'] < ss[i+1]['a'] for i in range(len(ss)-1)), 'Checkpoint snapshot order')
    strict(abs(ss[-1]['a'] / AF - 1) < 1e-12, 'Checkpoint endpoint')
    strict(all(len(r['state']) == len(names) and np.isfinite(r['state']).all() for r in ss), 'Checkpoint full states')
    strict(all(np.isfinite(list(r['transfer'].values())).all() for r in ss), 'Checkpoint transfer finiteness')


def trial_run(identity, layout, integrate, model, thermal, K, astar, np):
    name = identity['branch'] + '_' + identity['trial']
    path = CP / (name + '.json')
    commit = CP / (name + '.COMMIT.json')
    strict(path.exists() == commit.exists(), 'Preserve/refuse checkpoint orphan: ' + name)
    if path.exists():
        c = json.loads(commit.read_text())
        strict(set(c) == {'status', 'filename', 'sha256', 'identity', 'input_map_sha256'}, 'COMMIT schema')
        strict(c['status'] == 'COMMITTED' and c['filename'] == path.name, 'COMMIT identity')
        strict(c['input_map_sha256'] == digest(INPUTS) and c['identity'] == identity, 'COMMIT source/specification')
        strict(c['sha256'] == sha(path), 'COMMIT payload seal')
        payload = json.loads(path.read_text())
        strict(set(payload) == {'identity', 'input_sha256', 'history'}, 'Checkpoint envelope schema')
        strict(payload['identity'] == identity and payload['input_sha256'] == INPUTS, 'Checkpoint full custody')
        hist = payload['history']
    else:
        thermal.atomic = identity['atomic']
        thermal.thin = identity['thin']
        hist = integrate(model, thermal, K, identity['steps'], layout, astar, identity['ai'], identity['dust'])
        history_schema(hist, identity, layout.names, np)
        seals()
        atomic(path, dict(identity=identity, input_sha256=INPUTS, history=hist))
        atomic(commit, dict(status='COMMITTED', filename=path.name, sha256=sha(path),
                            identity=identity, input_map_sha256=digest(INPUTS)))
    history_schema(hist, identity, layout.names, np)
    rows = [json.loads(s) for s in JOURNAL.read_text().splitlines()]
    matches = [r for r in rows if r['stage'] == 'trial_complete' and r.get('name') == name]
    strict(len(matches) <= 1, 'Duplicate trial event')
    if matches:
        strict(matches[0]['sha256'] == sha(path) and matches[0]['commit_sha256'] == sha(commit), 'Changed journal checkpoint')
    else:
        event('trial_complete', name=name, sha256=sha(path), commit_sha256=sha(commit))
    print(json.dumps(dict(branch=identity['branch'], trial=identity['trial'],
                          seconds=hist['elapsed_seconds'], constraint=hist['maximum_constraint'])), flush=True)
    return hist


def main(resume):
    started = time.monotonic()
    for name, h in PINS.items():
        strict(sha(BASE / name) == h, 'Direct pin: ' + name)
        INPUTS[str(BASE / name)] = h
    strict(sha(PROTOCOL) == PROTOCOL_SHA, 'Protocol pin')
    INPUTS[str(PROTOCOL)] = PROTOCOL_SHA
    INPUTS[str(Path(__file__).resolve())] = sha(Path(__file__).resolve())
    cal = json.loads(CAL.read_text())
    strict(cal['all_controls_passed'] and cal['fitted_freedoms'] == 2, 'Completed common calibration')
    strict(all(c['passed'] for c in cal['controls']), 'Every inherited calibration control')
    strict(len(cal['hashes']) == 18 and len(cal['controls']) == 149, 'Calibration custody/control census')
    old = json.loads((BASE / 'INVARIANT_CLOCK_RECOMBINATION_TRANSFER_V002_RESULT.json').read_text())
    late = json.loads((BASE / 'INVARIANT_CLOCK_LATE_LENSING_V001_RESULT.json').read_text())
    panel = json.loads((BASE / 'hyrec_inputs_v001/HYREC_BAO_POINT10_PANEL_V001_RESULTS.json').read_text())
    partial = json.loads((BASE / 'hyrec_inputs_v001/HYREC_BAO_INTERVAL_SAVED_AUDIT_V003_RESULTS.json').read_text())
    strict(len(old['controls']) == 76 and all(c['passed'] for c in old['controls']), 'Old qualified transfer unchanged')
    strict(sum(not c['passed'] for c in late['controls']) == 6 and not late['all_numerical_controls_passed'], 'Late-lensing failures retained')
    known_cases = set(partial['all125_summary']['cases']) | set(panel['copied_case_indices']) | set(panel['newly_scored_case_indices'])
    strict(partial['histories'] == 335 and len(known_cases) == 128 and 335-len(known_cases) == 207, 'Earlier partial scan retained')
    for p, h in cal['hashes'].items():
        strict(sha(p) == h, 'Calibration inherited seal: ' + p)
        strict(p not in INPUTS or INPUTS[p] == h, 'Conflicting calibration input')
        INPUTS[p] = h
    strict([r['kind'] for r in cal['rows']] == ['CANDIDATE', 'REFERENCE'], 'Calibration branch order')
    for row in cal['rows']:
        for kind in ('default', 'half'):
            inv = row['invocations'][kind]
            p = BASE / inv['output_path']
            strict(sha(p) == inv['output_sha256'] and INPUTS[str(p)] == inv['output_sha256'], 'Final atomic output pin')
    spec = dict(stem=STEM, input_sha256=INPUTS, input_map_sha256=digest(INPUTS),
                k_Mpc_inverse=K_PHYSICAL, trials=TRIALS, seed=1e-5, end_a=AF)
    if MANIFEST.exists():
        strict(resume and CP.is_dir() and JOURNAL.exists(), 'Existing run requires complete --resume custody')
        strict(json.loads(MANIFEST.read_text()) == json.loads(canonical(spec)), 'Changed manifest')
        events = [json.loads(s) for s in JOURNAL.read_text().splitlines()]
        strict(events and events[0]['stage'] == 'started', 'Journal initial start')
        strict(sum(r['stage'] == 'started' for r in events) == 1, 'Exactly one initial start')
        for i, r in enumerate(events):
            strict(r['index'] == i and r['input_map_sha256'] == digest(INPUTS), 'Journal census/source identity')
            strict(r['previous_sha256'] == (digest(events[i-1]) if i else None), 'Journal chain')
        strict(events[0]['manifest_sha256'] == sha(MANIFEST), 'Start manifest seal')
        strict(not any(r['stage'] == 'completed' for r in events), 'Completed run is immutable')
        event('resumed', manifest_sha256=sha(MANIFEST))
    else:
        strict(not resume and not CP.exists() and not JOURNAL.exists(), 'Preserve/refuse orphan run')
        atomic(MANIFEST, spec)
        CP.mkdir()
        event('started', manifest_sha256=sha(MANIFEST))
    allowed_cp = {branch + '_' + t[0] + suffix for branch in ('KX', 'REF') for t in TRIALS
                  for suffix in ('.json', '.COMMIT.json')}
    strict(all(p.is_file() and p.name in allowed_cp for p in CP.iterdir()), 'Preserve/refuse extra or temporary checkpoint')
    sys.dont_write_bytecode = True
    import numpy as np
    load_gauss_only(np)
    import invariant_clock_recombination_transfer_v001 as pilot
    plasma = pilot.plasma
    def forbidden(*args, **kwargs):
        raise RuntimeError('Atomic/calibration execution forbidden in this packet')
    pilot.acoustic.invoke = forbidden
    pilot.acoustic.oracle.main = forbidden
    for module in (pilot, plasma, plasma.prior, plasma.prior.old, plasma.prior.old.base,
                   plasma.prior.old.solver, pilot.acoustic, pilot.acoustic.oracle):
        p = str(Path(module.__file__).resolve())
        strict(p in INPUTS and sha(p) == INPUTS[p], 'Actual imported implementation: ' + p)
    plasma.NEFF = cal['selected']['Neff']
    plasma.RN = (7 / 8) * (4 / 11)**(4 / 3) * plasma.NEFF
    plasma.YHE = cal['selected']['YHe']
    seed = json.loads(plasma.prior.old.base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0'] = 100.
    seed['inherited']['H0_km_s_Mpc'] = cal['selected']['Hunit']
    seed['inherited']['omega_b_cos'] = cal['selected']['physical_omega_b'] * .98 / (cal['selected']['Hunit'] / 100)**2
    model = plasma.prior.old.base.Model(seed, 1)
    strict(model.p == cal['fixed'], 'Complete fixed V003 parameter tuple')
    class Thermal(pilot.Thermal):
        def __init__(self):
            super().__init__(model, cal)
            values = []
            for row in cal['rows']:
                for kind in ('default', 'half'):
                    raw = json.loads((BASE / row['invocations'][kind]['output_path']).read_text())
                    strict(raw['status'] == 'COMPLETE_ATOMIC_HISTORY_ONLY' and raw['zero_injection'], 'Owned atomic status')
                    strict(raw['omega_b'] == cal['selected']['physical_omega_b'] and raw['YHe_atomic'] == plasma.YHE, 'Atomic baryon/helium tuple')
                    strict(raw['Hcal_km_s_Mpc'] == cal['selected']['Hunit'], 'Atomic Hunit')
                    values.append((raw['nH0_cm3'] * 1e6, 1 + 2 * raw['fHe']))
            strict(len(set(values)) == 1, 'Common HYREC normalization')
            self.nH0, self.xfull = values[0]
    thermal = Thermal()
    plasma.background = thermal.background
    astar = 1 / (1 + cal['rows'][0]['observables']['zstar'])
    for row in cal['rows']:
        check(row['kind'] + '_radiation_tuple', abs(thermal.bg.OR / row['omega_radiation'] - 1), 1e-10)
        check(row['kind'] + '_physical_baryon_tuple', abs(thermal.bg.omega_b / row['physical_omega_b'] - 1), 1e-10)
    layout = plasma.Layout(16, 48)
    common = [n for n in layout.names if n in layout.names[:11] or
              (n.startswith(('fg', 'fn')) and int(n[2:]) <= 4) or (n.startswith('pol') and int(n[3:]) <= 4)]
    K = K_PHYSICAL * 299792.458 / model.p['H0_km_s_Mpc']
    histories = {}
    rows = []
    for dust in (False, True):
        branch = 'REF' if dust else 'KX'
        for aa in (1e-7, 1/8001, astar, AF):
            A, b, _ = plasma.matrix(model, math.log(aa), K, layout, dust)
            cr, crx = plasma.constraint(b, layout)
            residual = crx + cr @ A + (3 + 2 * b['hx']) * cr
            scale = np.maximum(abs(crx) + abs(cr) @ abs(A) + abs((3 + 2*b['hx']) * cr), 1e-30)
            check(branch + '_constraint_identity_' + str(aa), np.max(abs(residual)/scale), 1e-10)
            check(branch + '_physical_background_' + str(aa), abs(b['H']/float(pilot.acoustic.Background(model, dust).E(aa))-1), 1e-10)
        hist = {}
        for label, steps, lg, ln, ai, atomic_kind, thin in TRIALS:
            identity = dict(branch=branch, dust=dust, trial=label, steps=steps, lg=lg, ln=ln,
                            ai=ai, atomic=atomic_kind, thin=thin, k_Mpc_inverse=K_PHYSICAL,
                            seed=plasma.prior.SEED, visibility_a=astar, end_a=AF)
            hist[label] = trial_run(identity, plasma.Layout(lg, ln), pilot.integrate, model, thermal, K, astar, np)
        names = [n for n in common if not (dust and n in ('B', 'Zh'))]
        errors = dict(time=plasma.errors(hist['COARSE'], hist['FINE']),
                      start=plasma.errors(hist['FINE'], hist['START'], endpoint=True),
                      hierarchy=plasma.errors(hist['FINE'], hist['HIERARCHY'], names),
                      atomic=plasma.errors(hist['FINE'], hist['ATOMIC']),
                      interpolation=plasma.errors(hist['FINE'], hist['THIN']))
        for name, value in errors.items():
            check(branch + '_' + name, value['error'], 1e-4)
        for label, h in hist.items():
            check(branch + '_trajectory_constraint_' + label, h['maximum_constraint'], 1e-6)
        rows.append(dict(kind=branch, k_Mpc_inverse=K_PHYSICAL, dust=dust, errors=errors,
                         selected={label:min(hist['FINE']['snapshots'], key=lambda r:abs(r['a']/aa-1))
                                   for label, aa in [('visibility_peak', astar), ('z800', AF)]},
                         linear_clock_margin_ratio=hist['FINE']['linear_clock_margin_ratio'],
                         linear_spatial_ratio=hist['FINE']['linear_spatial_ratio'],
                         cold_baryon_pressure_screen=hist['FINE']['cold_baryon_pressure_screen']))
        histories[dust] = hist
    ca, re = histories[False], histories[True]
    targets = [('visibility_peak', astar), ('z800', AF)]
    targets += [(f'window_z{1/r["a"]-1:.3f}', r['a']) for r in ca['FINE']['snapshots']
                if 900 < 1/r['a']-1 < 1500 and abs(r['a']/astar-1) > 1e-10]
    comparisons = []
    def pick(h, aa):
        return min(h['snapshots'], key=lambda r:abs(r['a']/aa-1))['transfer']
    for label, aa in targets:
        c, r = pick(ca['FINE'], aa), pick(re['FINE'], aa)
        delta = {n:(c[n]-r[n])/plasma.prior.SEED for n in c}
        sensitivity = {}
        for trial in ('COARSE', 'START', 'HIERARCHY', 'ATOMIC', 'THIN'):
            cc, rr = pick(ca[trial], aa), pick(re[trial], aa)
            sensitivity[trial] = dict(paired_difference_change={n:(cc[n]-rr[n])/plasma.prior.SEED-delta[n] for n in c},
                                     candidate_transfer_change={n:(cc[n]-c[n])/plasma.prior.SEED for n in c},
                                     reference_transfer_change={n:(rr[n]-r[n])/plasma.prior.SEED for n in c})
        comparisons.append(dict(k_Mpc_inverse=K_PHYSICAL, epoch=label, a=aa,
                                candidate_per_curvature={n:c[n]/plasma.prior.SEED for n in c},
                                reference_per_curvature={n:r[n]/plasma.prior.SEED for n in r},
                                differences_per_curvature=delta, sensitivity_per_curvature=sensitivity))
    strict(len(rows) == 2 and len(list(CP.glob('*.COMMIT.json'))) == 12, 'Full two-by-six census')
    strict(len(CONTROLS) == 42, 'Frozen complete numerical control census')
    inherited = dict(old_recombination_76_of_76_at_different_Hunit=68.06502010698708,
                     late_lensing_failed_gates=6, earlier_HYREC_scan_uncomputed=207,
                     data_exposed=True, inherited_fitted_freedoms=2, additional_fitted_freedoms=0)
    seals()
    qualified = all(c['passed'] for c in CONTROLS)
    status = 'NUMERICALLY_QUALIFIED_JOINT_V003_LINEAR_TRANSFER' if qualified else 'NUMERICALLY_UNQUALIFIED_JOINT_V003_LINEAR_TRANSFER'
    result = dict(status=status, protocol_sha256=PROTOCOL_SHA, source_sha256=sha(Path(__file__)),
                  gauss_function_span_sha256=GAUSS_STEP_SHA,
                  charged_helper_scope='Only exact gauss_step loaded; no legacy D0/calibration initialization',
                  input_sha256=INPUTS, fixed=model.p, selected_calibration=cal['selected'],
                  inherited_qualifications=inherited, k_Mpc_inverse=K_PHYSICAL,
                  radiation_omega=thermal.bg.OR, nH0_m_inverse3=thermal.nH0,
                  fully_ionized_xe=thermal.xfull, high_z_join_relative_jump=thermal.xfull/thermal.tables[False,'half'][-1,1]-1,
                  rows=rows, comparisons=comparisons, controls=CONTROLS,
                  check_count=len(CONTROLS), all_numerical_controls_passed=qualified,
                  elapsed_seconds=time.monotonic()-started,
                  checkpoint_sha256={p.name:sha(p) for p in sorted(CP.glob('*.json'))})
    text = ['# Joint V003 recombination transfer V001', '', status, '',
            f'k={K_PHYSICAL}/Mpc; Hunit={model.p["H0_km_s_Mpc"]:.14g}; two inherited fits, zero new fits.',
            'Saved HYREC histories reused; no atomic/nuclear/calibration execution.',
            'Old 76-control transfer has a different calibration; late lensing retains six failed gates; old scan retains207 absent points.', '',
            '| Branch | Time | Start | Hierarchy | Atomic | Thinning |', '|---|---:|---:|---:|---:|---:|']
    for row in rows:
        text.append('| ' + row['kind'] + ' | ' + ' | '.join(f'{row["errors"][n]["error"]:.10g}' for n in ('time','start','hierarchy','atomic','interpolation')) + ' |')
    text += ['', '| Epoch | Readout | Candidate / curvature | Reference / curvature | Signed difference | Max paired refinement change |',
             '|---|---|---:|---:|---:|---:|']
    for c in comparisons:
        for n, d in c['differences_per_curvature'].items():
            s = max(abs(v['paired_difference_change'][n]) for v in c['sensitivity_per_curvature'].values())
            text.append(f'| {c["epoch"]} | {n} | {c["candidate_per_curvature"][n]:.12g} | {c["reference_per_curvature"][n]:.12g} | {d:+.12g} | {s:.12g} |')
    text += ['', f'All {len(CONTROLS)} controls retained; failed=' + str([c['name'] for c in CONTROLS if not c['passed']]),
             'Full signed states, diagnostics and candidate/reference sensitivity arrays are lossless in the twelve referenced checkpoints and RESULT.',
             'No TT/TE/EE, likelihood, primordial fit, nonlinear-domain proof or observational superiority is claimed.']
    atomic(RESULT, result)
    atomic(REPORT, '\n'.join(text) + '\n', markdown=True)
    event('completed', status=status, result_sha256=sha(RESULT), report_sha256=sha(REPORT), check_count=len(CONTROLS))
    events = [json.loads(s) for s in JOURNAL.read_text().splitlines()]
    receipt = dict(status=status, source_sha256=sha(Path(__file__)), protocol_sha256=PROTOCOL_SHA,
                   input_sha256=INPUTS, manifest_sha256=sha(MANIFEST), result_sha256=sha(RESULT),
                   report_sha256=sha(REPORT), journal_sha256=sha(JOURNAL), event_count=len(events),
                   checkpoint_count=12, check_count=len(CONTROLS), all_numerical_controls_passed=qualified,
                   initial_pid=events[0]['pid'], closing_pid=os.getpid(), inherited_qualifications=inherited)
    atomic(RECEIPT, receipt)
    seals()
    print(json.dumps(dict(status=status, checks=len(CONTROLS), seconds=result['elapsed_seconds'],
                          result_sha256=sha(RESULT), receipt_sha256=sha(RECEIPT))), flush=True)
    return 0 if qualified else 3


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if not args.execute:
        parser.error('Explicit --execute required; no scientific or output action performed')
    for p in (RESULT, REPORT, RECEIPT, ERROR):
        strict(not p.exists(), 'Preserve completed or failed attempt: ' + str(p))
    try:
        sys.exit(main(args.resume))
    except Exception as exc:
        atomic(ERROR, dict(status='ERROR_INCOMPLETE', error=repr(exc), source_sha256=sha(Path(__file__)),
                           protocol_sha256=PROTOCOL_SHA, input_sha256=INPUTS, controls=CONTROLS,
                           pid=os.getpid(), completed_checkpoint_count=len(list(CP.glob('*.COMMIT.json'))) if CP.exists() else 0))
        raise
