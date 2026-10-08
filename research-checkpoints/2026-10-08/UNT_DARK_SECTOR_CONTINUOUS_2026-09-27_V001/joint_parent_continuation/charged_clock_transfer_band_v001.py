"""Frozen before execution: one fixed candidate, no fitting or observational score.

Extend the completed charged-current response to k=(.001,.003,.01,.03,.1,
.3,1,3,10) Mpc^-1, preserving every model/background/preparation constant.
Use 512/1024/2048 Gauss steps and the SAME 1e-4 trajectory gate and 1e-6
constraint gate. Refine the pressureless comparator at 1024/2048 too.
Report all points, including failures, density/potential transfer ratios,
six-mode operators and sampled validity diagnostics. No primordial spectrum,
data likelihood, formed galaxy, native abundance or superiority is claimed.

The operational output is scale-dependent evolution from the declared
post-recombination preparations. A sign reversal is not negative power;
squared relative transfer is reported without treating the initial amplitude
or absent radiation-era transfer as known. Sampled 5% departures may locate
an engineering comparison scale, not an observational exclusion threshold.
The helper's first-order validity boolean is explicitly not a full nonlinear
or continuous-time certificate. Quadratic kinematic margin ratios are added.
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
OUTPUT = BASE/'CHARGED_CLOCK_TRANSFER_BAND_V001_RESULT.json'
WAVENUMBERS_MPC = (.001, .003, .01, .03, .1, .3, 1., 3., 10.)


def main():
    started = time.monotonic()
    rows = []
    for k in WAVENUMBERS_MPC:
        model.WAVENUMBER = k*model.C_KMS/model.H0_KMS_MPC
        inv = 1/model.WAVENUMBER**2
        model.SCALE = np.array([inv, 1., inv, 1., inv, inv, inv])
        y512 = model.integrate(512)
        y1024 = model.integrate(1024)
        y2048 = model.integrate(2048)
        r1024 = model.integrate(1024, dust=True)
        r2048 = model.integrate(2048, dust=True)
        conv = model.convergence(y1024, y2048)
        refconv = model.convergence(r1024, r2048)
        dg = model.diagnostics(y2048)
        raw = y2048*model.SCALE[None, :, None]
        ref = r2048*model.SCALE[None, :5, None]
        comparisons = []
        quadratic = np.zeros((65, 2))
        for i, x in enumerate(np.linspace(model.X0, 0., 65)):
            b = model.background(float(x))
            kp = model.WAVENUMBER**2/b['a']**2
            yy = raw[i, :, 6:]
            rate = np.array(dg['series']['actual_rate_fraction'][i])
            quad = np.maximum(abs(.5*yy[0]**2-yy[0]*rate), abs(kp*(.5*yy[6]**2+yy[6]*yy[4])))
            quadratic[i] = quad/dg['series']['rate_margin_fraction'][i]
        for col, label in enumerate(('baryon_isocurvature', 'adiabatic_development')):
            ratio = raw[-1, 1, col+6]/ref[-1, 1, col]
            pratio = raw[-1, 0, col+6]/ref[-1, 0, col]
            comparisons.append(dict(preparation=label, delta_b_transfer_ratio=float(ratio),
                                    relative_baryon_transfer_squared=float(ratio**2),
                                    potential_transfer_ratio=float(pratio),
                                    candidate_final_baryon=float(raw[-1, 1, col+6]),
                                    reference_final_baryon=float(ref[-1, 1, col]),
                                    candidate_final_clock_F=float(raw[-1, 3, col+6]),
                                    max_quadratic_kinematic_rate_margin=float(np.max(quadratic[:, col]))))
        controls = dict(trajectory=conv['max_normalized'] <= 1e-4,
                        comparator=refconv['max_normalized'] <= 1e-4,
                        constraint=dg['max_normalized_constraint'] <= 1e-6)
        row = dict(k_Mpc_inverse=k, K=model.WAVENUMBER, numerical_controls=controls,
                   all_numerical_controls_passed=all(controls.values()),
                   convergence_512_1024=model.convergence(y512, y1024),
                   convergence_1024_2048=conv, comparator_convergence=refconv,
                   comparisons=comparisons, diagnostics=dg,
                   final_six_column_operator_scaled=y2048[-1, :, :6].tolist(),
                   final_comparator_states=ref[-1].tolist(), state_scales=model.SCALE.tolist(),
                   trajectory_2048_scaled=y2048.tolist())
        rows.append(row)
        print(json.dumps({key:row[key] for key in ('k_Mpc_inverse', 'all_numerical_controls_passed', 'comparisons')}), flush=True)
    dependencies = {name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in
                    ('charged_clock_response_v001.py', 'bounded_clock_shared_prediction_v001.py',
                     'CHARGED_CLOCK_RESPONSE_V001.md')}
    result = dict(protocol='Frozen in this script docstring/constants before execution.',
                  self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependencies_sha256=dependencies, inherited_parameters=dict(eps=model.EPS, KB=model.KB,
                      lambda_s=model.LAMBDA_S, Q0_over_H0=model.Q0, omega_A=model.OA,
                      omega_b_cos=model.OB, omega_clock_excess=model.OC, d0=model.D0,
                      initial_a=model.AI, initial_amplitude=model.SEED),
                  rows=rows, all_numerical_controls_passed=all(r['all_numerical_controls_passed'] for r in rows),
                  elapsed_seconds=time.monotonic()-started,
                  peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({key:result[key] for key in ('all_numerical_controls_passed', 'elapsed_seconds', 'peak_RSS_bytes')}))
    if not result['all_numerical_controls_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
