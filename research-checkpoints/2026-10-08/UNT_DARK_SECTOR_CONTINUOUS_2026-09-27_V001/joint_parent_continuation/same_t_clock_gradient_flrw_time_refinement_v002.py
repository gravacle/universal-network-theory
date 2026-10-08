"""One NEW65536-step time refinement; no completed parent trajectory replay."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import time
import numpy as np

BASE = Path(__file__).resolve().parent
STEM = 'SAME_T_CLOCK_GRADIENT_FLRW_TIME_REFINEMENT_V002'
OLD = 'SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
PROTOCOL_SHA = '7316538aa96810b6c65a66223ecccc97be3a989ec1df8b16f13ede0f64a95a13'
PINS = {
    'same_t_clock_gradient_flrw_response_v001.py': '61e6191713e5eb628b2ec551de43c200a029a6f236f7da255e867fca1d8d0990',
    OLD+'.md': '61ee3ff72207a8e25d7a9b4eb736e438ccc409d6d897402dafd58a231e214e9a',
    OLD+'_RESULT.json': '76549b997b915af67ef35472b3b5faa5004ccf9b490a8c7aa545ec8937f295ac',
    OLD+'_RECEIPT.json': 'd4baa47a6fea4743780446206c56294b4c238fb104c11edfde36f23853b417c4',
}
AI, SEED = .01, 1e-8
X0 = math.log(AI)
CP_KMS = 299792.458
CASES = [(k, om) for k in (.01, .1) for om in (0., .1, 1., 10., 100.)]
FLUID_NAMES = ['Phi', 'delta_b', 'Hunit_v_b', 'delta_rad', 'Hunit_v_rad',
               'Hunit_pi', 'delta_rho_clock_over_rho_star', 'Z', 'Z_prime']
ALLOW = ('sha', 'now', 'write_json', 'journal', 'background', 'rates',
         'initial_state', 'readouts', 'trial')


def load_functions():
    p = BASE/'same_t_clock_gradient_flrw_response_v001.py'
    if hashlib.sha256(p.read_bytes()).hexdigest() != PINS[p.name]:
        raise RuntimeError('Parent source seal mismatch')
    tree = ast.parse(p.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ALLOW]
    if tuple(n.name for n in nodes) != ALLOW:
        raise RuntimeError('Exact reviewed function census mismatch')
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(p), 'exec'), globals())


def main():
    start = time.monotonic()
    load_functions()
    parent = json.loads((BASE/(OLD+'_RESULT.json')).read_text())
    rec = json.loads((BASE/(OLD+'_RECEIPT.json')).read_text())
    pins = dict(parent['manifest']['lineage']['inputs'])
    pins.update(PINS)
    pins[STEM+'.md'] = PROTOCOL_SHA
    for n, h in pins.items():
        if sha(BASE/n) != h:
            raise RuntimeError('Direct/input seal mismatch '+n)
    if rec['result_sha256'] != PINS[OLD+'_RESULT.json'] or parent['status'] != 'COMPLETED':
        raise RuntimeError('Parent natural-closure identity mismatch')
    if parent['manifest']['cases'] != [list(c) for c in CASES]:
        raise RuntimeError('Parent case census mismatch')
    if len(parent['numerical_gates']) != 441:
        raise RuntimeError('Parent gate census mismatch')
    old_failures = [g for g in parent['numerical_gates'] if not g['passed']]
    if len(old_failures) != 15 or any(g['name'] != 'time_refinement' for g in old_failures):
        raise RuntimeError('Unexpected parent qualification state')
    fixed = parent['manifest']['fixed']
    source_sha = sha(__file__)
    lineage = dict(inputs=pins, source_sha256=source_sha)
    manifest = dict(lineage=lineage, fixed=fixed, cases=CASES,
                    new_trial=['NEW_FINE', 65536, 48], reused_trials=['FINE', 'MODES'])
    mp = BASE/(STEM+'_MANIFEST.json')
    if mp.exists():
        if json.loads(mp.read_text()) != json.loads(json.dumps(manifest)):
            raise RuntimeError('Existing refinement manifest mismatch')
    else:
        write_json(mp.name, manifest)
    if (BASE/(STEM+'_RESULT.json')).exists():
        raise RuntimeError('Refinement completed; refusing duplicate execution')
    journal('OWNER_START', owner='root', pid=os.getpid(), source_sha256=source_sha)
    new = trial('NEW_FINE', 65536, 48, fixed, lineage)
    old_fine, old_modes = parent['trials'][1:]
    if (old_fine['label'], old_fine['steps'], old_fine['ns']) != ('FINE', 32768, 48):
        raise RuntimeError('Parent fine census mismatch')
    if (old_modes['label'], old_modes['steps'], old_modes['ns']) != ('MODES', 32768, 96):
        raise RuntimeError('Parent spectral census mismatch')
    gates = [dict(g, inherited_from=PINS[OLD+'_RESULT.json']) for g in parent['numerical_gates']
             if g['name'] != 'time_refinement']

    def check(name, error, tol, **ident):
        gates.append(dict(name=name, error=float(error), tolerance=tol,
                          passed=bool(math.isfinite(error) and error <= tol), **ident))

    nf = np.array([s['fluids'] for s in new['snapshots']])
    of = np.array([s['fluids'] for s in old_fine['snapshots']])
    error = np.max(abs(nf-of), axis=0)/np.maximum(np.max(abs(nf), axis=0), SEED*1e-8)
    check('new_spectral_normalization', abs(sum(new['weights'])-1), 1e-13)
    check('new_charge_root', max(s['background']['charge_error'] for s in new['snapshots']), 1e-13)
    for c, (k, om) in enumerate(CASES):
        for seed in range(2):
            check('new_normal_constraint', max(s['normal_error'][c][seed] for s in new['snapshots']),
                  1e-6, case=c, seed=seed)
            if om == 0:
                check('new_mode_off_zero', max(abs(v) for s in new['snapshots']
                      for v in s['state'][c][seed][7:]), 1e-13, case=c, seed=seed)
            for v, name in enumerate(FLUID_NAMES):
                check('new_time_refinement', error[c, seed, v], 1e-4, case=c, seed=seed, variable=name)
    if len(gates) != 467:
        raise RuntimeError('Current refined gate census mismatch')
    endpoints, flags, effects = [], [], []
    phys_new = np.array(new['snapshots'][-1]['physical'])
    phys_old = np.array(old_fine['snapshots'][-1]['physical'])
    phys_modes = np.array(old_modes['snapshots'][-1]['physical'])
    for c, (k, om) in enumerate(CASES):
        ref = 0 if c < 5 else 5
        for seed in range(2):
            n = phys_new[c, seed]-phys_new[ref, seed]
            o = phys_old[c, seed]-phys_old[ref, seed]
            sp = phys_modes[c, seed]-phys_modes[ref, seed]
            dt, ds = o-n, sp-o
            margin = 3*np.maximum(abs(dt), abs(ds))
            effects.append(dict(case=c, seed=seed, fine_effect=n.tolist(),
                                old_fine_effect=o.tolist(), old_spectral_effect=sp.tolist(),
                                time_change=dt.tolist(), spectral_change=ds.tolist(),
                                three_change_margin=margin.tolist(),
                                resolution=['control_zero' if om == 0 else ('resolved' if abs(v)>m else 'unresolved')
                                            for v, m in zip(n, margin)]))
            endpoints.append(dict(case=c, seed=seed, k_Mpc_inverse=k, omega_over_old_Hunit=om,
                                  physical=phys_new[c, seed].tolist(), difference_from_mode_off=n.tolist()))
            amp = max(max(s['amplitudes'][c][seed]) for s in new['snapshots'])
            domain = max(s['clock_domain'][c][seed][3] for s in new['snapshots'])
            flags.append(dict(case=c, seed=seed, maximum_amplitude=amp, small_perturbation=amp<.01,
                              maximum_clock_domain_fraction=domain, inside_clock_domain=domain<1,
                              sampled_maximum_basis_amplitude=SEED/domain if domain>0 else None,
                              scope='sampled at65 times, not an all-times certificate'))
    result = dict(status='COMPLETED', manifest=manifest, new_trial=new, numerical_gates=gates,
                  all_numerical_gates_passed=all(g['passed'] for g in gates),
                  original_failed_gates_preserved=old_failures, endpoints=endpoints,
                  physical_fixture_flags=flags, endpoint_effect_refinements=effects,
                  physical_names=parent['physical_names'], elapsed_seconds=time.monotonic()-start,
                  scope='One NEW finer time trajectory; original failed attempt retained')
    for n, h in pins.items():
        if sha(BASE/n) != h:
            raise RuntimeError('Input changed during refinement; outputs not published')
    if sha(__file__) != source_sha:
        raise RuntimeError('Source changed during refinement')
    result_sha = write_json(STEM+'_RESULT.json', result)
    report = ['# Same-T FLRW time refinement V002', '',
              f'{sum(g["passed"] for g in gates)}/{len(gates)} current numerical gates PASS.',
              'Original426/441 attempt and15failed radiation time controls remain unchanged.',
              'One NEW65536/48 trajectory; existing32768/48 and96states reused.', '',
              '| k/Mpc | omega/Hunit | basis | comoving db | db minus mode-off | Weyl |',
              '|---|---|---|---|---|---|']
    for row in endpoints:
        report.append('| '+f'{row["k_Mpc_inverse"]} | {row["omega_over_old_Hunit"]} | {row["seed"]} | '
                      f'{row["physical"][0]:.12g} | {row["difference_from_mode_off"][0]:.12g} | '
                      f'{row["physical"][4]:.12g}'+' |')
    report += ['', 'NEW effective basis response, no primordial selection or observational claim.',
               'Domain/linearity flags are sampled; paired effects retain resolution labels.']
    rp = BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:
        f.write('\n'.join(report)+'\n')
    rp.chmod(0o444)
    journal('OWNER_COMPLETE', result_sha256=result_sha, passed=sum(g['passed'] for g in gates), total=len(gates))
    write_json(STEM+'_RECEIPT.json', dict(lineage=lineage, manifest_sha256=sha(mp),
               result_sha256=result_sha, report_sha256=sha(rp),
               journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')), status='COMPLETED'))
    print(json.dumps(dict(status='COMPLETED', passed=sum(g['passed'] for g in gates),
                          total=len(gates), result_sha256=result_sha,
                          elapsed_seconds=result['elapsed_seconds'])), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--execute', action='store_true')
    if not ap.parse_args().execute:
        raise SystemExit('Explicit --execute required')
    try:
        main()
    except Exception as exc:
        if 'write_json' in globals():
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
            write_json(STEM+'_FAILED_'+stamp+'.json', dict(error=repr(exc), time=now(), pid=os.getpid()))
        raise
