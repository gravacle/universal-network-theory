"""Technical repair, frozen before execution; no changed scientific inputs.

V001's four low-k rows passed trajectory refinement but failed its relative
Einstein-constraint gate, worst in the initially pure vector-alpha column
at the first checkpoint. Keep those failed receipts. Propagating a redundant
seventh metric variable accumulated error relative to that small induced
metric response. Evolve the six independent variables instead and reconstruct
Phi from the same Einstein constraint at every stage; no equations are removed.

Rerun ONLY k=.001,.003,.01,.03 /Mpc at 512/1024/2048. Keep all fixed model
parameters, preparations and old numerical gates. Reuse V001's separately
converged dust comparator and its other five accepted k rows. Check the
derivative of the algebraic Phi constraint against the independently evolved
momentum equation as a matrix identity before execution (1e-10 relative).
Report the difference from original V001 without overwriting it. No old
failed row becomes evidence until the unchanged gates pass here.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np
import charged_clock_response_v001 as model

BASE = Path(__file__).resolve().parent
OUTPUT = BASE/'CHARGED_CLOCK_TRANSFER_BAND_V002_RESULT.json'


def metric_row(b):
    kp = model.WAVENUMBER**2/b['a']**2
    return -1.5/kp*np.array([b['rb'], 3*b['h']*b['rb'], b['W'],
                             3*b['h']*b['W'], 0., 0.])


def reduced_matrix(x):
    m, b = model.matrix(x)
    w = metric_row(b)
    return m[1:, 1:]+m[1:, :1]*w[None, :], m, b, w


def check_metric_derivative():
    largest = 0.
    for x in np.linspace(model.X0, 0., 33):
        red, m, b, w = reduced_matrix(float(x))
        h, W, rb, s = (b[t] for t in ('h', 'W', 'rb', 'cs2'))
        hp, Wp, rbp = -1.5*(W+rb)/h, -3*(1+s)*W, -3*rb
        kp = model.WAVENUMBER**2/b['a']**2
        wp = 2*w-1.5/kp*np.array([rbp, 3*(hp*rb+h*rbp), Wp,
                                  3*(hp*W+h*Wp), 0., 0.])
        direct = wp+w@red
        momentum = m[0, 1:]+m[0, 0]*w
        largest = max(largest, model.max_relative(direct, momentum))
    return largest


def integrate(nstep):
    y = model.initial(model.background(model.X0))[1:]
    dx = -model.X0/nstep
    saved = []
    scales = model.SCALE[1:]

    def full(z, x):
        w = metric_row(model.background(x))
        phi_scaled = w@(z*scales[:, None])/model.SCALE[0]
        return np.vstack((phi_scaled[None, :], z))

    def matrix(x):
        m, _, _, _ = reduced_matrix(x)
        return m*scales[None, :]/scales[:, None]

    saved.append(full(y, model.X0))
    for i in range(nstep):
        y = model.gauss_step(y, model.X0+i*dx, dx, matrix)
        if (i+1) % (nstep//64) == 0:
            saved.append(full(y, model.X0+(i+1)*dx))
    return np.array(saved)


def main():
    started = time.monotonic()
    original_path = BASE/'CHARGED_CLOCK_TRANSFER_BAND_V001_RESULT.json'
    old = json.loads(original_path.read_text())
    rows = []
    for prior in old['rows']:
        if prior['all_numerical_controls_passed']:
            continue
        k = prior['k_Mpc_inverse']
        assert k in (.001, .003, .01, .03)
        model.WAVENUMBER = k*model.C_KMS/model.H0_KMS_MPC
        inv = 1/model.WAVENUMBER**2
        model.SCALE = np.array([inv, 1., inv, 1., inv, inv, inv])
        algebra = check_metric_derivative()
        histories = {n:integrate(n) for n in (512, 1024, 2048)}
        conv = model.convergence(histories[1024], histories[2048])
        dg = model.diagnostics(histories[2048])
        raw = histories[2048]*model.SCALE[None, :, None]
        ref = np.array(prior['final_comparator_states'])
        comparisons = []
        for j, name in enumerate(('baryon_isocurvature', 'adiabatic_development')):
            ratio = raw[-1, 1, j+6]/ref[1, j]
            comparisons.append(dict(preparation=name, delta_b_transfer_ratio=float(ratio),
                                     relative_baryon_transfer_squared=float(ratio**2),
                                     potential_transfer_ratio=float(raw[-1, 0, j+6]/ref[0, j]),
                                     candidate_final_baryon=float(raw[-1, 1, j+6]),
                                     candidate_final_clock_F=float(raw[-1, 3, j+6])))
        gates = dict(metric_derivative_identity=algebra <= 1e-10,
                     trajectory_convergence=conv['max_normalized'] <= 1e-4,
                     constraint=dg['max_normalized_constraint'] <= 1e-6,
                     inherited_comparator=prior['numerical_controls']['comparator'])
        row = dict(k_Mpc_inverse=k, K=model.WAVENUMBER, controls=gates,
                   all_numerical_controls_passed=all(gates.values()),
                   metric_derivative_identity_error=algebra,
                   convergence_512_1024=model.convergence(histories[512], histories[1024]),
                   convergence_1024_2048=conv,
                   difference_from_failed_seven_variable_receipt=model.convergence(np.array(prior['trajectory_2048_scaled']),histories[2048]),
                   comparisons=comparisons, diagnostics=dg,
                   trajectory_2048_scaled=histories[2048].tolist(), state_scales=model.SCALE.tolist())
        rows.append(row)
        print(json.dumps({key:row[key] for key in ('k_Mpc_inverse','controls','metric_derivative_identity_error','comparisons')}), flush=True)
    result = dict(self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  input_sha256=hashlib.sha256(original_path.read_bytes()).hexdigest(),
                  dependency_sha256=hashlib.sha256((BASE/'charged_clock_response_v001.py').read_bytes()).hexdigest(),
                  rows=rows, all_numerical_controls_passed=all(r['all_numerical_controls_passed'] for r in rows),
                  elapsed_seconds=time.monotonic()-started, peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({key:result[key] for key in ('all_numerical_controls_passed','elapsed_seconds','peak_RSS_bytes')}))
    if not result['all_numerical_controls_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
