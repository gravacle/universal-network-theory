"""Prospective follow-up fixed in CHARGED_CLOCK_RESPONSE_RESULT_V001.md.

No model fitting. Reuse the completed response; one comparator refinement,
quadratic kinematics and constrained principal-mode inspection only.
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
OUTPUT = BASE/'CHARGED_CLOCK_MODE_DIAGNOSTIC_V001_RESULT.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started = time.monotonic()
    inp = BASE/'CHARGED_CLOCK_RESPONSE_V001_RESULT.json'
    source = json.loads(inp.read_text())
    history = np.array(source['trajectories_scaled']['2048'])
    raw = history*model.SCALE[None, :, None]
    xs = np.array(source['x_checkpoints'])
    series = source['diagnostics']['series']
    quadratic_ratios = np.zeros((len(xs), 2))
    charge_contrast, gradient_contrast = [], []
    for i, x in enumerate(xs):
        b = model.background(float(x))
        kp = model.WAVENUMBER**2/b['a']**2
        y = raw[i, :, 6:]
        rate = np.array(series['actual_rate_fraction'][i])
        pterm = .5*y[0]**2-y[0]*rate
        vterm = kp*(.5*y[6]**2+y[6]*y[4])
        quadratic_ratios[i] = np.maximum(abs(pterm), abs(vterm))/series['rate_margin_fraction'][i]
        gradient = kp*y[5]/(3*b['W'])
        charge_contrast.append((y[3]+gradient).tolist())
        gradient_contrast.append(gradient.tolist())
    ref1024 = model.integrate(1024, dust=True)
    ref2048 = np.array(source['comparator_trajectory_scaled'])
    reference_convergence = model.convergence(ref1024, ref2048)
    spectra = []
    original_K = model.WAVENUMBER
    for a in (.1, .3, 1.):
        for multiple in (1, 2, 4, 8, 16, 32):
            model.WAVENUMBER = original_K*multiple
            m, b = model.matrix(math.log(a))
            k2 = model.WAVENUMBER**2/a**2
            # Algebraically constrained metric potential from the six other states.
            w = -1.5/k2*np.array([b['rb'], 3*b['h']*b['rb'], b['W'],
                                 3*b['h']*b['W'], 0., 0.])
            reduced = m[1:, 1:]+m[1:, :1]*w[None, :]
            scales = np.array([1., 1/model.WAVENUMBER**2, 1.,
                               1/model.WAVENUMBER**2, 1/model.WAVENUMBER**2,
                               1/model.WAVENUMBER**2])
            reduced_scaled = reduced*scales[None, :]/scales[:, None]
            eigs, vecs = np.linalg.eig(reduced_scaled)
            residual = np.linalg.norm(reduced_scaled@vecs-vecs*eigs[None, :])/(np.linalg.norm(reduced_scaled)*np.linalg.norm(vecs))
            ordering = np.lexsort((eigs.imag, eigs.real))
            spectra.append(dict(a=a, K=model.WAVENUMBER,
                                eigenvalues_per_ln_a=[[float(z.real), float(z.imag)] for z in eigs[ordering]],
                                max_positive_real_per_K=float(max(0., np.max(eigs.real))/model.WAVENUMBER),
                                max_imaginary_per_physical_k=float(np.max(abs(eigs.imag))*b['h']*a/model.WAVENUMBER),
                                proposed_principal_speed_squared=2*model.C*b['Q']**2*b['cs2']/(3*model.KB*b['W']),
                                eigenpair_relative_residual=float(residual)))
    model.WAVENUMBER = original_K
    result = dict(scope='Mode and kinematic diagnostic; not a new observational or nonlinear test.',
                  input_sha256=sha(inp), self_sha256=sha(Path(__file__)),
                  diagnostic_protocol_sha256=sha(BASE/'CHARGED_CLOCK_RESPONSE_RESULT_V001.md'),
                  dependency_sha256={p.name:sha(p) for p in
                                     (BASE/'charged_clock_response_v001.py', BASE/'bounded_clock_shared_prediction_v001.py')},
                  max_quadratic_kinematic_rate_to_margin=np.max(quadratic_ratios, axis=0).tolist(),
                  quadratic_ratio_series=quadratic_ratios.tolist(),
                  charge_density_contrast_series=charge_contrast,
                  gradient_density_contrast_series=gradient_contrast,
                  reference_convergence=reference_convergence,
                  comparator_numerical_gate_passed=reference_convergence['max_normalized'] <= 1e-4,
                  spectra=spectra, elapsed_seconds=time.monotonic()-started,
                  peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({key:result[key] for key in ('max_quadratic_kinematic_rate_to_margin',
                      'comparator_numerical_gate_passed', 'elapsed_seconds', 'peak_RSS_bytes')}, indent=2))
    print('final charge contrast', charge_contrast[-1], 'gradient contrast', gradient_contrast[-1])
    for row in spectra:
        print(json.dumps(row))


if __name__ == '__main__':
    main()
