"""Fixed universal-response null: red/blue and high/low Sersic ESD contrasts.

Declared before computing these scores; the paper's type-dependence and its
reported significance are already exposed. Not blind, not a new discovery
of this observed correlation. This applies a new restriction of our candidate.
At exact common gbar, a universal compact spherical response predicts zero
type contrast regardless of a0,r. Use BOTH published type splits, same seven
gbar>=1e-13 primary bins, all15 and low8 retained. Positive photon/lens metric,
distance and baryon conventions are those of EFFECTIVE_ESD_FORWARD_V001.md.
No force or nuisance fit; no ESD-to-SIS-acceleration conversion. Use supplied
cross-type covariance, corrected once by its product bias. No sum of the two
split statistics: they overlap. No sigma or theory-rejection conversion.
Systematics, type-dependent mass/gas bias, isolation and pair weighting are
not eliminated by matching catalogue stellar-mass distributions. Colour and
Sersic index are not direct measurements of network entanglement.
An additional candidate-specific bin envelope allows arbitrary positive
weights separately for each type, conditional on monotonic ESD in every bin.
The spectral bound is a robustness diagnostic, not a parameter fit. It does
not include mass scatter, bin migration, differential baryons/environment.
All inputs already local; one tiny worker; preserve every output.
"""
import hashlib
import io
import json
import pathlib
import tarfile
import time
import numpy as np
from disk_solver import sha, save_new

ROOT = pathlib.Path(__file__).resolve().parent
ARCHIVE = ROOT/'external_brouwer2021_v001/brouwer2021_rar.tar'
PREDICTIONS = ROOT/'EFFECTIVE_ESD_FORWARD_V001_RESULT.json'
OUTPUT = ROOT/'EFFECTIVE_ESD_TYPE_CONTRAST_V001_RESULT.json'


def main():
    start = time.perf_counter()
    assert sha(ARCHIVE) == '73adc2d4e848fa0a6a43187f7b5447e749b92eaec4a795b9902b0beaf8a78733'
    assert sha(PREDICTIONS) == 'ec9a99b80bebf2a634ae4068407e4ee6767614c43d5376eb6e564076f5b5a433'
    previous = json.loads(PREDICTIONS.read_text())
    gbar = np.asarray(previous['data']['gbar'])
    prediction = previous['results']['inherited_calibrated']['0.0']
    width = (np.asarray(prediction['upper_edge']['prediction_esd'])
             - np.asarray(prediction['lower_edge']['prediction_esd']))
    result = {'script_sha256': sha(pathlib.Path(__file__)), 'archive_sha256': sha(ARCHIVE),
              'prediction_sha256': sha(PREDICTIONS), 'new_fit_parameters': 0, 'splits': {}}
    for kind in ('Color', 'Sersic'):
        names = [f'Fig-8_RAR-KiDS-isolated_{kind}bin_{i}.txt' for i in (1, 2)]
        covname = f'Fig-8_RAR-KiDS-isolated_{kind}bins_covmatrix.txt'
        with tarfile.open(ARCHIVE) as arc:
            blobs = {n: arc.extractfile(n).read() for n in names+[covname]}
        tables = [np.loadtxt(io.BytesIO(blobs[n])) for n in names]
        rows = np.loadtxt(io.BytesIO(blobs[covname]))
        assert all(t.shape == (15, 8) for t in tables) and rows.shape == (900, 7)
        labels = np.unique(rows[:, 0])
        coords = np.unique(rows[:, 2])
        assert len(labels) == 2 and np.max(abs(coords/gbar-1)) <= 1e-10
        assert all(np.max(abs(t[:, 0]/gbar-1)) <= 2e-4 for t in tables)
        cov = np.zeros((30, 30))
        corr = cov.copy()
        biases = cov.copy()
        count = np.zeros((30, 30), dtype=int)
        for row in rows:
            m, n = np.searchsorted(labels, row[:2])
            i, j = np.searchsorted(coords, row[2:4])
            assert labels[m] == row[0] and labels[n] == row[1]
            assert coords[i] == row[2] and coords[j] == row[3]
            u, v = 15*m+i, 15*n+j
            cov[u, v] = row[4]/row[6]
            corr[u, v] = row[5]
            biases[u, v] = row[6]
            count[u, v] += 1
        assert np.all(count == 1)
        bias = np.concatenate([t[:, 4] for t in tables])
        error = np.concatenate([t[:, 3] for t in tables])/bias
        data = np.concatenate([t[:, 1] for t in tables])/bias
        controls = {'bias_relative': float(np.max(abs(biases/np.outer(bias, bias)-1))),
                    'diagonal_error_relative': float(np.max(abs(np.sqrt(np.diag(cov))/error-1))),
                    'symmetry_relative': float(np.max(abs(cov-cov.T))/np.max(abs(cov))),
                    'correlation_absolute': float(np.max(abs(corr-cov/np.sqrt(np.outer(np.diag(cov), np.diag(cov))))))}
        assert controls['bias_relative'] <= 2e-4 and controls['diagonal_error_relative'] <= 2e-4
        assert controls['symmetry_relative'] <= 1e-10 and controls['correlation_absolute'] <= 1e-10
        assert np.linalg.eigvalsh(cov)[0] > 0
        transform = np.concatenate([-np.eye(15), np.eye(15)], axis=1)
        delta = transform@data
        cd = transform@cov@transform.T
        assert np.max(abs(cd-(cov[:15, :15]+cov[15:, 15:]-cov[:15, 15:]-cov[15:, :15]))) < 1e-10
        stats = {}
        for name, mask in {'primary': gbar >= 1e-13, 'flagged_low': gbar < 1e-13,
                           'all': np.ones(15, dtype=bool)}.items():
            ds = delta[mask]
            cs = cd[np.ix_(mask, mask)]
            white = np.linalg.solve(np.linalg.cholesky(cs), ds)
            corr_s = cs/np.sqrt(np.outer(np.diag(cs), np.diag(cs)))
            largest = float(np.linalg.eigvalsh(corr_s)[-1])
            distance = np.maximum(abs(ds)-width[mask], 0.)
            bound = float(np.sum(distance**2/np.diag(cs))/largest)
            ratio = data[15:][mask]/data[:15][mask]
            stats[name] = {'n': int(np.sum(mask)), 'Q_zero_type_contrast': float(white@white),
                'mean_difference_esd': float(np.mean(ds)),
                'high_over_low_ratio_each_bin': ratio.tolist(),
                'log10_arithmetic_mean_ratio': float(np.log10(np.mean(ratio))) if np.all(ratio > 0) else None,
                'bin_weight_envelope_conditional_Q_lower_bound': bound,
                'correlation_largest_eigenvalue': largest}
        result['splits'][kind] = {'labels_low_high': labels.tolist(),
            'member_sha256': {n: hashlib.sha256(b).hexdigest() for n, b in blobs.items()},
            'controls': controls, 'gbar': gbar.tolist(), 'low_esd': data[:15].tolist(),
            'high_esd': data[15:].tolist(), 'high_minus_low_esd': delta.tolist(),
            'contrast_covariance': cd.tolist(), 'statistics': stats}
    result['seconds'] = time.perf_counter()-start
    save_new(OUTPUT, result)
    print(json.dumps({'seconds': result['seconds'], 'splits': {k: v['statistics'] for k, v in result['splits'].items()}}, indent=2))


if __name__ == '__main__':
    main()
