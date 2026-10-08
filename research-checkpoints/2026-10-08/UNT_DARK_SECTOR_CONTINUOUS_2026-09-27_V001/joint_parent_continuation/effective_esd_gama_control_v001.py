"""No-refit spectroscopic-selection control after the KiDS ESD screen.

Declared before scoring GAMA, but the paper's qualitative agreement and
first four rows have been seen. Not blind. Reuse ALL saved fixed-parameter
predictions, with no recalculation or selection of favorable mass shifts.
Use GAMA same-acceleration profiles/covariance from the same public archive.
Seven matched primary bins are directly comparable descriptively; all15 and
eight lower bins retained as a GAMA extension (not a KiDS-isolation pass).
GAMA spectroscopic redshifts improve isolation selection, but smaller area
makes errors larger. Source shapes/footprint can overlap KiDS; no joint
likelihood, significance of sample difference, or causal attribution without
cross-covariance and matched samples. More permissive errors are not stronger
evidence. Distance, baryon, compact-source and metric caveats unchanged.
Source: https://arxiv.org/html/2106.11677v1 sections3,5.2 and appendixA.
"""
import io
import json
import pathlib
import tarfile
import time
import hashlib
import numpy as np
from disk_solver import sha, save_new

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT/'EFFECTIVE_ESD_FORWARD_V001_RESULT.json'
ARCHIVE = ROOT/'external_brouwer2021_v001/brouwer2021_rar.tar'
PROFILE = 'Fig-4-C1_RAR-GAMA-isolated_Nobins.txt'
COV = 'Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt'
OUTPUT = ROOT/'EFFECTIVE_ESD_GAMA_CONTROL_V001_RESULT.json'


def main():
    started = time.perf_counter()
    assert sha(SOURCE) == 'ec9a99b80bebf2a634ae4068407e4ee6767614c43d5376eb6e564076f5b5a433'
    assert sha(ARCHIVE) == '73adc2d4e848fa0a6a43187f7b5447e749b92eaec4a795b9902b0beaf8a78733'
    saved = json.loads(SOURCE.read_text())
    with tarfile.open(ARCHIVE) as arc:
        members = {n: arc.extractfile(n).read() for n in (PROFILE, COV)}
    data = np.loadtxt(io.BytesIO(members[PROFILE]))
    entries = np.loadtxt(io.BytesIO(members[COV]))
    assert data.shape == (15, 8) and entries.shape == (225, 7)
    coords = np.unique(entries[:, 2])
    assert np.max(abs(coords/np.asarray(saved['data']['gbar'])-1)) <= 1e-10
    assert np.max(abs(data[:, 0]/coords-1)) <= 2e-4
    cov = np.zeros((15, 15))
    correlation = cov.copy()
    bias = cov.copy()
    counts = np.zeros((15, 15), dtype=int)
    for row in entries:
        i, j = np.searchsorted(coords, row[2:4])
        assert coords[i] == row[2] and coords[j] == row[3]
        assert row[0] == row[1] == -999
        cov[i, j] = row[4]/row[6]
        correlation[i, j] = row[5]
        bias[i, j] = row[6]
        counts[i, j] += 1
    assert np.all(counts == 1)
    errors = data[:, 3]/data[:, 4]
    observed = data[:, 1]/data[:, 4]
    check_values = {'diagonal_error_relative': float(np.max(abs(np.sqrt(np.diag(cov))/errors-1))),
                    'bias_relative': float(np.max(abs(bias/np.outer(data[:, 4], data[:, 4])-1))),
                    'symmetry_relative': float(np.max(abs(cov-cov.T))/np.max(abs(cov))),
                    'correlation_absolute': float(np.max(abs(correlation-cov/np.sqrt(np.outer(np.diag(cov), np.diag(cov))))))}
    assert check_values['diagonal_error_relative'] <= 2e-4
    assert check_values['bias_relative'] <= 2e-4
    assert check_values['symmetry_relative'] <= 1e-10
    assert check_values['correlation_absolute'] <= 1e-10
    assert np.linalg.eigvalsh(cov)[0] > 0
    masks = {'matched_primary': coords >= 1e-13, 'low_extension': coords < 1e-13,
             'all': np.ones(15, dtype=bool)}
    results = {}
    for model, shifts in saved['results'].items():
        results[model] = {}
        for shift, modes in shifts.items():
            results[model][shift] = {}
            for mode, case in modes.items():
                prediction = np.asarray(case['prediction_esd'])
                scores = {}
                for name, mask in masks.items():
                    residual = prediction[mask]-observed[mask]
                    white = np.linalg.solve(np.linalg.cholesky(cov[np.ix_(mask, mask)]), residual)
                    scores[name] = {'n': int(np.sum(mask)), 'Q': float(white@white),
                                    'Q_per_bin': float(white@white/np.sum(mask)),
                                    'residual_esd': residual.tolist()}
                results[model][shift][mode] = scores
    result = {'source_sha256': sha(SOURCE), 'archive_sha256': sha(ARCHIVE),
              'script_sha256': sha(pathlib.Path(__file__)),
              'member_sha256': {n: hashlib.sha256(b).hexdigest() for n, b in members.items()},
              'checks': check_values, 'negative_observations_retained': int(np.sum(observed < 0)),
              'new_fit_parameters': 0, 'gbar': coords.tolist(),
              'esd_corrected': observed.tolist(), 'error_corrected': errors.tolist(),
              'covariance_corrected': cov.tolist(), 'results': results,
              'seconds': time.perf_counter()-started}
    save_new(OUTPUT, result)
    print(json.dumps({'checks': check_values, 'seconds': result['seconds'],
                      'central': {m: r['0.0']['centre'] for m, r in results.items()}}, indent=2))


if __name__ == '__main__':
    main()
