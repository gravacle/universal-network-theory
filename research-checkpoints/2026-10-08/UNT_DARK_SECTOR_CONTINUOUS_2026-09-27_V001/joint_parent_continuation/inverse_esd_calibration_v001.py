"""Required total-baryon offsets with full paired statistical covariance."""
import hashlib
import io
import json
import pathlib
import sys
import tarfile
import time
import numpy as np
import effective_esd_forward_v001 as forward
from disk_solver import sha, save_new

ROOT = pathlib.Path(__file__).resolve().parent
STEM = 'INVERSE_ESD_CALIBRATION_V001'
ARCHIVE = ROOT/'external_brouwer2021_v001/brouwer2021_rar.tar'
SOURCE = ROOT/'EFFECTIVE_ESD_TYPE_CONTRAST_V001_RESULT.json'
CALIBRATION = ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json'


def hashes():
    files = (pathlib.Path(__file__), ROOT/(STEM+'.md'), ARCHIVE, SOURCE, CALIBRATION,
             ROOT/'effective_esd_forward_v001.py', ROOT/'disk_solver.py', forward.inherited.SHAPE_PATH)
    return {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): sha(p) for p in files}


def main():
    if sys.argv[1:] == ['freeze']:
        save_new(ROOT/(STEM+'_FROZEN.json'), {'files': hashes()})
        return
    assert not sys.argv[1:]
    assert json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())['files'] == hashes()
    start = time.perf_counter()
    source = json.loads(SOURCE.read_text())
    a0 = json.loads(CALIBRATION.read_text())['a0_si']['inherited_calibrated']
    model = 'inherited_calibrated'
    grids = []
    for n in (2049, 4097):
        lg = np.linspace(-17., -9., n)
        p = forward.esd(10**lg, model, a0)
        assert np.all(p > 0) and np.all(np.diff(p) > 0)
        grids.append((lg, np.log10(p)))
    edges = np.geomspace(1e-15, 5e-12, 16)
    result = {'files': hashes(), 'force_a0_si': a0, 'checks': {}, 'splits': {}}

    def check(name, value, tolerance):
        result['checks'][name] = {'value': float(value), 'tolerance': tolerance, 'pass': bool(value <= tolerance)}

    for kind, block in source['splits'].items():
        gbar = np.asarray(block['gbar'])
        primary = np.flatnonzero(gbar >= 1e-13)
        paired = np.concatenate([primary, 15+primary])
        esd = np.concatenate([block['low_esd'], block['high_esd']])[paired]
        assert len(primary) == 7 and np.all(esd > 0)
        covname = f'Fig-8_RAR-KiDS-isolated_{kind}bins_covmatrix.txt'
        with tarfile.open(ARCHIVE) as arc:
            raw = arc.extractfile(covname).read()
        assert hashlib.sha256(raw).hexdigest() == block['member_sha256'][covname]
        entries = np.loadtxt(io.BytesIO(raw))
        labels = np.unique(entries[:, 0])
        coords = np.unique(entries[:, 2])
        cov = np.zeros((30, 30))
        for row in entries:
            m, n = np.searchsorted(labels, row[:2])
            i, j = np.searchsorted(coords, row[2:4])
            cov[15*m+i, 15*n+j] = row[4]/row[6]
        c14 = cov[np.ix_(paired, paired)]
        assert np.linalg.eigvalsh(c14)[0] > 0
        inverse_logs = []
        for lg, lp in grids:
            assert np.min(np.log10(esd)) > lp[0] and np.max(np.log10(esd)) < lp[-1]
            inverse_logs.append(np.interp(np.log10(esd), lp, lg))
        coarse, fine = inverse_logs
        check(kind+'_inverse_grid_dex', np.max(abs(coarse-fine)), 1e-6)
        ghat = 10**fine
        check(kind+'_roundtrip', np.max(abs(forward.esd(ghat, model, a0)/esd-1)), 1e-6)

        def slope(logg, h):
            return (np.log(forward.esd(10**logg*np.exp(h), model, a0))
                    - np.log(forward.esd(10**logg*np.exp(-h), model, a0)))/(2*h)

        slopes = slope(fine, 1e-4)
        smaller = slope(fine, 5e-5)
        coarse_slopes = slope(coarse, 1e-4)
        assert np.all(slopes > 0)
        check(kind+'_slope_step', np.max(abs(slopes/smaller-1)), 1e-6)
        check(kind+'_slope_grid', np.max(abs(slopes/coarse_slopes-1)), 1e-5)

        def differential_covariance(s):
            k = 1/(np.log(10)*esd*s)
            jac = np.concatenate([-np.diag(k[:7]), np.diag(k[7:])], axis=1)
            return jac@c14@jac.T

        cd = differential_covariance(slopes)
        coarse_cd = differential_covariance(coarse_slopes)
        check(kind+'_covariance_grid', np.max(abs(cd-coarse_cd))/np.max(abs(cd)), 1e-4)
        assert np.linalg.eigvalsh(cd)[0] > 0
        offsets = fine-np.tile(np.log10(gbar[primary]), 2)
        delta = offsets[7:]-offsets[:7]
        # Independent deep-limit inverse and slope controls in physical ESD units.
        deep_inverse = (4*forward.G*esd/forward.SI_TO_ESD)**2/a0
        deep_delta = np.log10(deep_inverse[7:]/deep_inverse[:7])
        check(kind+'_deep_delta', np.max(abs(deep_delta-2*np.log10(esd[7:]/esd[:7]))), 1e-12)
        check(kind+'_deep_roundtrip', np.max(abs(forward.esd(deep_inverse, 'deep', a0)/esd-1)), 1e-11)
        brackets = np.stack([fine-np.tile(np.log10(edges[primary+1]), 2),
                             fine-np.tile(np.log10(edges[primary]), 2)], axis=1)
        if not all(c['pass'] for c in result['checks'].values()):
            save_new(ROOT/(STEM+'_CONTROL_FAILURE.json'), result)
            raise RuntimeError('Frozen controls failed; no diagnostic calibration fit published.')
        one = np.ones(7)
        precision_one = np.linalg.solve(cd, one)
        mean = float(precision_one@delta/(one@precision_one))
        error = float(1/np.sqrt(one@precision_one))
        residual = delta-mean
        result['splits'][kind] = {'gbar_primary': gbar[primary].tolist(), 'paired_esd': esd.tolist(),
            'paired_covariance': c14.tolist(), 'required_log_gbar': fine.tolist(),
            'required_total_baryon_offsets_dex_low_then_high': offsets.tolist(),
            'conditional_bin_coordinate_brackets_dex': brackets.tolist(),
            'differential_offsets_dex': delta.tolist(), 'differential_covariance': cd.tolist(),
            'differential_stat_error_per_bin': np.sqrt(np.diag(cd)).tolist(),
            'slopes_at_inferred_gbar': slopes.tolist(), 'deep_limit_differential_dex': deep_delta.tolist(),
            'constant_differential_diagnostic': {'fitted_constants': 1, 'offset_dex': mean,
                'total_baryon_ratio': 10**mean, 'delta_method_stat_error_dex': error,
                'residual_shape_Q': float(residual@np.linalg.solve(cd, residual)),
                'bins': 7, 'residual_degrees_if_linear_gaussian': 6},
            'minimum_primary_esd_signal_to_noise': float(np.min(esd/np.sqrt(np.diag(c14))))}
    result['seconds'] = time.perf_counter()-start
    save_new(ROOT/(STEM+'_RESULT.json'), result)
    print(json.dumps({'checks': result['checks'], 'seconds': result['seconds'],
        'splits': {k: {'delta': v['differential_offsets_dex'],
                      'summary': v['constant_differential_diagnostic'],
                      'min_signal_to_noise': v['minimum_primary_esd_signal_to_noise']}
                   for k, v in result['splits'].items()}}, indent=2))


if __name__ == '__main__':
    main()
