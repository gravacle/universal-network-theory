"""Inert FIRAS residual-space source screen. Root owns freeze/run; stdout only."""
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback

sys.dont_write_bytecode = True
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
F = J/'firas_inputs_v001'
THIS = J/'firas_source_screen_v001.py'
PROTOCOL = J/'FIRAS_SOURCE_SCREEN_PROTOCOL_V001.md'
FROZEN = J/'FIRAS_SOURCE_SCREEN_V001_FROZEN.json'
PINS = {
    F/'firas_monopole_spec_v1.txt': 'df793c3dca09ebfa7dbc5aa0ec1951daa8884431bc30eff28a710d7516cf50fa',
    F/'FIRAS_RETRIEVAL_V001.json': '08be3926a29040984598a7a69693b87c4f638cb74bf6ce1037d1f02a4569860d',
    F/'FIRAS_COVARIANCE_SOURCE_V001.json': 'ee9cb861d351cc1b642074b9a68fea82df83630f33e0a6dfda8dcc4949cc1f67',
    J/'CMB_CONTINUOUS_SOURCE_ANALYSIS_V001.md': 'b4cb12de9a11767f91b6441d860711e09f4f8e64ec7d1517c5065e7ffbe50ad4',
    ROOT/'UNT_CMB_NETWORK_THERMAL_HYPOTHESIS_V001.md': 'f25c9c1104defdceba8bb916bc05c59ea06fb41f8d309224b8d29116cdfd9210',
}
CONFIG = dict(temperatures_K=[2.725, 2.728], ratios=[0.5, 0.9, 1.0, 1.1, 4/3, 2.0],
              foregrounds=['dust9_amplitude', 'dust9_amplitude_temperature_tangent',
                           'published_pole_template'], channels=43, expected_baselines=6,
              expected_source_rows=90, nominal_profile_delta_chi2=3.841458820694124,
              identity_tolerance=2e-12, linear_algebra_tolerance=2e-9,
              derivative_tolerance=2e-8, degeneracy_relative_norm=2e-12,
              synthetic_coefficients=[0.3, -0.2, 0.1, -0.05],
              h_SI=6.62607015e-34, kB_SI=1.380649e-23, c_SI=299792458.0,
              Jy_SI=1e-26, dust_reference_K=9.0, dust_peak_kJy_sr=1000.0)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def read(path):
    path.relative_to(ROOT)
    if path.resolve() != path or path.is_symlink():
        raise ValueError('Linked or noncanonical input: '+str(path))
    return path.read_bytes()


def freeze():
    if Path.cwd().resolve() != ROOT or Path(__file__).resolve() != THIS:
        raise ValueError('Wrong workspace/script')
    inputs = []
    for path in sorted(list(PINS)+[THIS, PROTOCOL]):
        raw = read(path)
        if path in PINS and digest(raw) != PINS[path]:
            raise ValueError('Input hash mismatch: '+str(path))
        inputs.append(dict(path=str(path), bytes=len(raw), sha256=digest(raw)))
    return dict(schema='FIRAS_SOURCE_SCREEN_FREEZE_V001', config=CONFIG, inputs=inputs,
                inputs_sha256=digest(encode(inputs)))


class Checks:
    def __init__(self):
        self.rows = []

    def test(self, name, error, tolerance=None):
        tolerance = CONFIG['identity_tolerance'] if tolerance is None else tolerance
        value = float(error)
        self.rows.append(dict(name=name, error=value if math.isfinite(value) else None,
                              tolerance=tolerance, passed=math.isfinite(value) and value <= tolerance))


def run(result):
    import numpy as np
    begin = time.perf_counter()
    ck = Checks()
    result['checks'] = ck.rows
    data = np.loadtxt(F/'firas_monopole_spec_v1.txt')
    if data.shape != (43, 5) or not np.isfinite(data).all() or not (data[:, 3] > 0).all():
        raise ValueError('Invalid full43-channel table')
    if not (np.diff(data[:, 0]) > 0).all():
        raise ValueError('Unordered frequencies')
    source = json.loads(read(F/'FIRAS_COVARIANCE_SOURCE_V001.json'))
    q = np.array(source['Q'])
    if q.shape != (43,):
        raise ValueError('Covariance lag census')
    sigma = data[:, 3]
    covariance = sigma[:, None]*sigma[None, :]*q[np.abs(np.arange(43)[:, None]-np.arange(43))]
    L = np.linalg.cholesky(covariance)
    white = lambda a: np.linalg.solve(L, a)
    y = data[:, 2]
    yw = white(y)
    nu = data[:, 0]*100*CONFIG['c_SI']
    pref = 2*CONFIG['h_SI']*nu**3/CONFIG['c_SI']**2/(1000*CONFIG['Jy_SI'])

    def planck(T):
        x = CONFIG['h_SI']*nu/(CONFIG['kB_SI']*T)
        f = 1/np.expm1(x)
        B = pref*f
        dB = pref*x*np.exp(-x)/(T*(-np.expm1(-x))**2)
        return x, B, dB

    def nuisance(T, foreground):
        _, _, dT = planck(T)
        _, Bd, dBd = planck(CONFIG['dust_reference_K'])
        rawdust = nu**2*Bd
        factor = CONFIG['dust_peak_kJy_sr']/np.max(rawdust)
        columns = [dT]
        names = ['temperature_correction_K']
        if foreground == 'published_pole_template':
            columns += [data[:, 4]]
            names += ['pole_template_amplitude']
        else:
            columns += [factor*rawdust]
            names += ['dust9_peak_normalized_amplitude']
            if foreground == 'dust9_amplitude_temperature_tangent':
                columns += [factor*nu**2*dBd]
                names += ['dust9_temperature_tangent_K_times_amplitude']
        return np.column_stack(columns), names

    def fit(A, ywhite=yw):
        Aw = white(A)
        norms = np.linalg.norm(Aw, axis=0)
        Z = Aw/norms
        coeff, _, rank, singular = np.linalg.lstsq(Z, ywhite, rcond=None)
        if rank != A.shape[1]:
            raise ValueError('Unexpected nuisance/full-design rank loss')
        coeff_normal = np.linalg.solve(Z.T@Z, Z.T@ywhite)
        ck.test('least_squares_vs_normal_'+str(len(ck.rows)),
                np.linalg.norm(Z@(coeff-coeff_normal))/max(1, np.linalg.norm(ywhite)),
                CONFIG['linear_algebra_tolerance'])
        cov_scaled = np.linalg.inv(Z.T@Z)
        beta = coeff/norms
        beta_cov = cov_scaled/norms[:, None]/norms[None, :]
        resid = ywhite-Aw@beta
        ck.test('normal_equation_'+str(len(ck.rows)),
                np.linalg.norm(Z.T@resid)/max(1, np.linalg.norm(ywhite)),
                CONFIG['linear_algebra_tolerance'])
        return beta, beta_cov, float(resid@resid), float(singular[0]/singular[-1])

    ck.test('covariance_symmetry', np.max(np.abs(covariance-covariance.T)))
    ck.test('covariance_diagonal', np.max(np.abs(np.diag(covariance)/sigma**2-1)))
    ck.test('cholesky_reconstruction', np.linalg.norm(L@L.T-covariance)/np.linalg.norm(covariance))
    ck.test('whitening_inverse', np.linalg.norm(white(L)-np.eye(43)))
    _, Bproduct, _ = planck(2.725)
    result.update(config=CONFIG, primary_metadata=source, raw_table=data.tolist(),
                  covariance_kJy2_sr2=covariance.tolist(), Q=q.tolist(),
                  covariance_eigenvalue_range=np.linalg.eigvalsh(covariance)[[0, -1]].tolist(),
                  column2_reconstruction_max_abs_kJy_sr=float(np.max(np.abs(1000*data[:, 1]-y-Bproduct))),
                  column2_used_in_likelihood=False, baselines=[], source_rows=[], controls={})
    result['scope'] = ('Exposed, rounded, calibration/foreground-conditioned Table4 residual-space GLS; '
                       'statistical covariance only, not original interferograms or full systematics. '
                       'All nuisance alternatives retained; no microscopic source or production history inferred.')
    result['controls']['moment_defect'] = []
    for r in CONFIG['ratios']:
        defect = (r**4-1)-4*(r**3-1)/3
        factorized = (r-1)**2*(3*r*r+2*r+1)/3
        ck.test('grey_moment_factorization_'+str(r), abs(defect-factorized)/max(1, abs(factorized)))
        result['controls']['moment_defect'].append(dict(r=r, defect=defect))
    ck.test('pure_emission_two_moments_r4over3', abs((4/3)**4-4*(4/3)**3/3))
    for T in CONFIG['temperatures_K']:
        x, B, dT = planck(T)
        G = T*dT
        fd = []
        for step in (1e-3, 5e-4):
            fd.append((planck(T*(1+step))[1]-planck(T*(1-step))[1])/(2*step))
        richardson = (4*fd[1]-fd[0])/3
        ck.test('Planck_tangent_derivative_'+str(T), np.max(np.abs(richardson/G-1)),
                CONFIG['derivative_tolerance'])
        templates = [('mu', -G/x, None), ('y', G*(x/np.tanh(x/2)-4), None),
                     ('inverse_Planck_tangent', G, None)]
        for r in CONFIG['ratios']:
            Br = planck(r*T)[1]
            templates += [('grey_exchange', Br-B, r), ('pure_emission', Br, r)]
        for foreground in CONFIG['foregrounds']:
            A, names = nuisance(T, foreground)
            beta0, cov0, chi0, cond0 = fit(A)
            Aw = white(A)
            Qn, _ = np.linalg.qr(Aw)
            yperp = yw-Qn@(Qn.T@yw)
            result['baselines'].append(dict(T_K=T, foreground=foreground, nuisance_names=names,
                nuisance_coefficients=beta0.tolist(), covariance=cov0.tolist(), chi2=chi0,
                nominal_design_degrees_of_freedom=43-len(names), scaled_condition=cond0,
                model_kJy_sr=(A@beta0).tolist(), residual_kJy_sr=(y-A@beta0).tolist()))
            for family, template, r in templates:
                tw = white(template)
                tp = tw-Qn@(Qn.T@tw)
                ratio = float(np.linalg.norm(tp)/np.linalg.norm(tw)) if np.linalg.norm(tw) else 0.0
                row = dict(T_K=T, foreground=foreground, family=family, r=r,
                           template_kJy_sr=template.tolist(), residualized_template_relative_norm=ratio,
                           nuisance_names=names, chi2_null=chi0)
                if ratio <= CONFIG['degeneracy_relative_norm']:
                    row.update(status='UNIDENTIFIABLE_WITH_PROFILED_TEMPERATURE', amplitude=None,
                               sigma=None, nominal_nonnegative_profile_band=None,
                               reason='Zero source at r=1 or exact Planck-temperature tangent; no finite spectral bound')
                    ck.test('expected_degeneracy_'+str(len(result['source_rows'])),
                            0 if family == 'inverse_Planck_tangent' or (family == 'grey_exchange' and r == 1) else 1,
                            0)
                else:
                    Full = np.column_stack([A, template])
                    beta, beta_cov, chi, cond = fit(Full)
                    hat = float(beta[-1])
                    sig = math.sqrt(float(beta_cov[-1, -1]))
                    hat_projected = float(tp@yperp/(tp@tp))
                    ck.test('profile_amplitude_'+str(len(result['source_rows'])),
                            abs(hat-hat_projected)/max(sig, abs(hat), 1e-300), CONFIG['linear_algebra_tolerance'])
                    ck.test('profile_chi2_'+str(len(result['source_rows'])),
                            abs(chi-(chi0-(tp@yperp)**2/(tp@tp)))/max(1, chi0),
                            CONFIG['linear_algebra_tolerance'])
                    model = Full@beta
                    radius = math.sqrt(max(-hat, 0)**2+CONFIG['nominal_profile_delta_chi2']*sig*sig)
                    band = [max(0.0, hat-radius), max(0.0, hat+radius)]
                    row.update(status='IDENTIFIABLE_CONDITIONAL_LINEAR_SCREEN', amplitude=hat, sigma=sig,
                        nominal_signed_band=[hat-math.sqrt(CONFIG['nominal_profile_delta_chi2'])*sig,
                                             hat+math.sqrt(CONFIG['nominal_profile_delta_chi2'])*sig],
                        nominal_nonnegative_profile_band=band if r is not None else None,
                        nonnegative_optimum=max(0, hat) if r is not None else None,
                        chi2=chi, delta_chi2_from_null=chi0-chi, nominal_design_degrees_of_freedom=43-Full.shape[1],
                        nuisance_coefficients=beta[:-1].tolist(), coefficient_covariance=beta_cov.tolist(),
                        scaled_condition=cond, model_kJy_sr=model.tolist(), residual_kJy_sr=(y-model).tolist())
                    # Independent full-design synthetic recovery, no observed target selection.
                    Z = white(Full)/np.linalg.norm(white(Full), axis=0)
                    known = np.array(CONFIG['synthetic_coefficients'][:Full.shape[1]])
                    synthetic = Z@known
                    found, _, _, _ = np.linalg.lstsq(Z, synthetic, rcond=None)
                    ck.test('synthetic_coefficients_'+str(len(result['source_rows'])),
                            np.max(np.abs(found-known)), CONFIG['linear_algebra_tolerance'])
                    # Reversing every row AND both covariance axes must preserve the estimate.
                    Lrev = np.linalg.cholesky(covariance[::-1, ::-1])
                    Fr = np.linalg.solve(Lrev, Full[::-1])
                    yr = np.linalg.solve(Lrev, y[::-1])
                    nr = np.linalg.norm(Fr, axis=0)
                    br = np.linalg.lstsq(Fr/nr, yr, rcond=None)[0]/nr
                    ck.test('reversed_row_covariance_'+str(len(result['source_rows'])),
                            abs(br[-1]-hat)/max(sig, abs(hat), 1e-300), CONFIG['linear_algebra_tolerance'])
                    if r is not None:
                        energy_factor = r**4-(1 if family == 'grey_exchange' else 0)
                        number_factor = r**3-(1 if family == 'grey_exchange' else 0)
                        upper = band[1]
                        row.update(amplitude_meaning='epsilon times exact instantaneous spectral shape; grey epsilon~integral kappa dt, emission epsilon=integral j dt',
                            signed_energy_change_relative_initial_at_upper=upper*energy_factor,
                            signed_number_change_relative_initial_at_upper=upper*number_factor,
                            max_fractional_channel_change_at_upper=float(np.max(np.abs(upper*template/B))),
                            grey_fixed_bath_mixture_fraction_band=([band[0], min(1.0, band[1])]
                                if family == 'grey_exchange' and band[0] <= 1 else None),
                            temperature_second_order_whitened_norm=float(np.linalg.norm(white(
                                planck(T+beta[0])[1]-B-beta[0]*dT))) if T+beta[0] > 0 else None)
                    if family in ('mu', 'y'):
                        published = source['published_table2_descriptive_reference'][family]
                        row['published_descriptive_comparison'] = dict(published=published,
                            estimate_difference=hat-published['estimate'],
                            statistical_sigma_ratio=sig/published['statistical_sigma'],
                            not_a_reproduction_gate=True, unprovided_systematics_not_added=True)
                result['source_rows'].append(row)
    ck.test('complete_baseline_census', abs(len(result['baselines'])-6), 0)
    ck.test('complete_source_census', abs(len(result['source_rows'])-90), 0)
    ck.test('expected_unidentifiable_census', abs(sum(r['amplitude'] is None for r in result['source_rows'])-12), 0)
    result['check_count'] = len(ck.rows)
    result['failed_checks'] = [c for c in ck.rows if not c['passed']]
    result['seconds'] = time.perf_counter()-begin
    result['status'] = 'COMPLETE' if not result['failed_checks'] else 'FAILED_NUMERICAL_CONTROLS'


def main():
    mode = sys.argv[1] if len(sys.argv) == 2 else None
    frozen = freeze()
    if mode == 'freeze':
        print(encode(frozen).decode())
        return
    if mode != 'run':
        raise SystemExit('Usage: firas_source_screen_v001.py freeze|run')
    raw = read(FROZEN)
    if json.loads(raw) != frozen:
        raise ValueError('Frozen inputs/configuration differ')
    result = dict(schema='FIRAS_SOURCE_SCREEN_V001', status='UNSTARTED')
    try:
        run(result)
    except BaseException:
        result['status'] = 'FAILED_EXECUTION'
        result['exception'] = traceback.format_exc()
    wrapper = dict(freeze_sha256=digest(raw), payload_sha256=digest(encode(result)), payload=result)
    print(encode(wrapper).decode())


if __name__ == '__main__':
    main()
