"""Post-screen, no-fit bound on arbitrary positive within-bin averaging.

Declared after central Q was seen, before evaluating this diagnostic.
Does not modify the original protocol, central result or parameters.
For R=D^-1 C D^-1 and every p_i in [lo_i,hi_i],
Q >= sum(distance(data_i,[lo_i,hi_i])**2/Cii)/lambda_max(R).
Hence this is an optimistic lower bound, not a fitted/achievable prediction.
Mass shifts remain separate fixed-catalogue sensitivity cases, not a prior.
No assertion about full systematics or a p-value follows from this bound.
"""
import json
import pathlib
import time
import numpy as np
from disk_solver import sha, save_new

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT/'EFFECTIVE_ESD_FORWARD_V001_RESULT.json'
OUTPUT = ROOT/'EFFECTIVE_ESD_BIN_BOUND_V001_RESULT.json'
EXPECTED = 'ec9a99b80bebf2a634ae4068407e4ee6767614c43d5376eb6e564076f5b5a433'


def main():
    start = time.perf_counter()
    assert sha(SOURCE) == EXPECTED
    j = json.loads(SOURCE.read_text())
    mask = np.asarray(j['data']['gbar']) >= 1e-13
    cov = np.asarray(j['data']['covariance_corrected'])[np.ix_(mask, mask)]
    d = np.asarray(j['data']['esd_corrected'])[mask]
    variance = np.diag(cov)
    corr = cov/np.sqrt(np.outer(variance, variance))
    eigenvalues = np.linalg.eigvalsh(corr)
    assert eigenvalues[0] > 0
    # Verify the spectral inequality on deterministic test vectors and the
    # identity-matrix special case; no sampling of science parameters.
    vectors = np.vstack([np.eye(7), -np.eye(7), np.ones(7), np.arange(7)-3])
    spectral_slacks = []
    for v in vectors:
        lhs = v@np.linalg.solve(corr, v)
        rhs = v@v/eigenvalues[-1]
        assert lhs >= rhs-1e-12*max(1., lhs)
        spectral_slacks.append(float(lhs-rhs))
    results = {}
    for model, shifts in j['results'].items():
        results[model] = {}
        for shift, modes in shifts.items():
            lo = np.asarray(modes['lower_edge']['prediction_esd'])[mask]
            hi = np.asarray(modes['upper_edge']['prediction_esd'])[mask]
            assert np.all(lo <= hi)
            # Closed intervals contain every positive weighted average of a
            # continuous monotone profile across the same fixed gbar bin.
            nearest = np.clip(d, lo, hi)
            marginal_min = float(np.sum((nearest-d)**2/variance))
            bound = marginal_min/eigenvalues[-1]
            centre_q = modes['centre']['scores']['primary']['Q']
            assert centre_q >= bound-1e-10
            results[model][shift] = {'Q_lower_bound_any_positive_bin_weights': float(bound),
                'marginal_squared_distance_sum': marginal_min,
                'data_outside_prediction_interval': int(np.sum((d < lo)|(d > hi))),
                'nearest_interval_residual_esd': (nearest-d).tolist(),
                'central_Q_unchanged': centre_q}
    result = {'source_sha256': EXPECTED, 'script_sha256': sha(pathlib.Path(__file__)),
              'scope': 'seven primary bins; post-screen robustness diagnostic; no refit',
              'correlation_eigenvalues': eigenvalues.tolist(),
              'numerical_spectral_control_slacks': spectral_slacks,
              'results': results, 'seconds': time.perf_counter()-start}
    save_new(OUTPUT, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
