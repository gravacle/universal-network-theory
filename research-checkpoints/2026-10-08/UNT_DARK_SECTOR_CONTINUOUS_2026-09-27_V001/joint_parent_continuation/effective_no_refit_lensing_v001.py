"""Published reduced-data cross-probe comparison; no fitting or new dynamics."""
import json
from pathlib import Path
import numpy as np
import disk_solver as law

ROOT = Path(__file__).resolve().parent
TABLE = np.array([
    [-11.41, -10.65, .06, .03], [-11.65, -10.78, .06, .03],
    [-11.90, -10.88, .06, .00], [-12.15, -11.00, .06, .00],
    [-12.39, -11.11, .05, .02], [-12.64, -11.21, .05, .00],
    [-12.89, -11.29, .05, .01], [-13.13, -11.47, .05, .02],
    [-13.38, -11.59, .05, .01], [-13.63, -11.76, .06, .03],
    [-13.87, -11.93, .07, .05], [-14.12, -12.08, .07, .07],
    [-14.37, -12.27, .08, .13], [-14.61, -12.44, .08, .25],
    [-14.86, -12.85, .12, .67],
])


def main():
    prior = ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json'
    assert law.sha(prior) == 'f8502c04a3f17655172b2f589b48d1eebaa7c46bb64ad9950fd10d34ceb23aa9'
    receipt = json.loads(prior.read_text())
    frozen = json.loads((ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_FROZEN.json').read_text())
    for path in (ROOT/'disk_solver.py', law.SHAPE_PATH):
        assert law.sha(path) == frozen['files'][str(path.relative_to(ROOT.parent))]
    params = receipt['a0_si']
    out = dict(source_url='https://arxiv.org/html/2310.15248v2', table_label='Table1',
        source_exposure='Published table and conclusions read before numerical comparison; no refit.',
        status='COMPLETE_CONDITIONAL_REDUCED_LENSING_COMPARISON', a0_si=params,
        files={p.name: law.sha(p) for p in (Path(__file__), ROOT/'EFFECTIVE_NO_REFIT_LENSING_V001.md', prior)},
        table_columns=['log10_gbar_SI', 'log10_gobs_SI', 'statistical_dex', 'interpolation_exterior_systematic_dex'],
        table=TABLE.tolist(), additional_mass_systematic_dex=.1, comparisons={})
    for shift in (0., -.2, .2, -.125, .125):
        gb = 10**(TABLE[:, 0]+shift)
        aa = params['inherited_calibrated']
        pred = dict(baryons=gb, inherited_calibrated=aa*law.inverse(gb/aa),
                    rar_calibrated=gb/(-np.expm1(-np.sqrt(gb/params['rar_calibrated']))))
        summary = {}
        for name, gp in pred.items():
            residual = np.log10(gp)-TABLE[:, 1]
            subsets = {}
            for label, mask in [('primary_gbar_ge_1e_minus13', TABLE[:, 0] >= -13),
                                ('flagged_lower_acceleration', TABLE[:, 0] < -13),
                                ('all', np.ones(15, dtype=bool))]:
                rr = residual[mask]
                subsets[label] = dict(bins=int(np.sum(mask)), mean_residual_dex=float(np.mean(rr)),
                                      rms_residual_dex=float(np.sqrt(np.mean(rr**2))),
                                      max_abs_residual_dex=float(np.max(np.abs(rr))))
            summary[name] = dict(log10_gpred=np.log10(gp).tolist(), residual_dex=residual.tolist(), subsets=subsets)
        out['comparisons'][str(shift)] = summary
    target = ROOT/'EFFECTIVE_NO_REFIT_LENSING_V001_RESULT.json'
    law.save_new(target, out)
    print(json.dumps(dict(central={m: v['subsets'] for m,v in out['comparisons']['0.0'].items()},
                          sha256=law.sha(target)), indent=2))


if __name__ == '__main__':
    main()
