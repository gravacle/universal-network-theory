"""Root-owned, stdout-only endpoint translation; no fit or ancestor execution."""
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
INPUT = HERE / 'CMB_TZ_SOURCE_INTERVAL_INPUTS_V001.json'
PROTOCOL = HERE / 'CMB_TZ_SOURCE_INTERVAL_PROTOCOL_V001.md'
ANALYSIS = HERE / 'CMB_CONTINUOUS_SOURCE_ANALYSIS_V001.md'
ANALYSIS_SHA = 'b4cb12de9a11767f91b6441d860711e09f4f8e64ec7d1517c5065e7ffbe50ad4'
FREEZE = HERE / 'CMB_TZ_SOURCE_INTERVAL_V001_FROZEN.json'
TOL = 2e-14


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot():
    if Path.cwd().resolve() != ROOT or HERE != ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation':
        raise RuntimeError('Wrong project context')
    if sha(ANALYSIS.read_bytes()) != ANALYSIS_SHA:
        raise RuntimeError('Analytical source changed')
    files = []
    for p in [INPUT, PROTOCOL, ANALYSIS, Path(__file__).resolve()]:
        if p.resolve() != p:
            raise RuntimeError('Linked input')
        raw = p.read_bytes()
        files.append(dict(path=str(p), bytes=len(raw), sha256=sha(raw)))
    return dict(schema='CMB_TZ_SOURCE_INTERVAL_FREEZE_V001', files=files, identity_tolerance=TOL,
                expected_observations=3, no_likelihood_combination=True)


def mapped(lo, hi):
    if not lo <= hi:
        raise ValueError('Reversed L endpoints')
    return dict(L=[lo, hi], F_E=[-math.expm1(-4*lo), -math.expm1(-4*hi)],
                F_N=[-math.expm1(-3*lo), -math.expm1(-3*hi)])


def positive(lo, hi):
    return None if hi < 0 else mapped(max(lo, 0.), hi)


def calculate():
    inputs = json.loads(INPUT.read_bytes())
    T0, dT0 = inputs['T0_K'], inputs['T0_reported_error_K']
    rows, checks = [], []
    def check(name, a, b):
        error = abs(a-b)
        checks.append(dict(name=name, error=error, tolerance=TOL,
                           passed=math.isfinite(error) and error <= TOL))
    check('zero_source', math.log(1.), 0.)
    check('half_energy', -math.expm1(-4*math.log(2.)/4), .5)
    if len(inputs['observations']) != 3 or not 0 < dT0 < T0:
        raise RuntimeError('Unexpected input census/range')
    for obs in inputs['observations']:
        z = obs['z']; A = 1+z
        Tl, Th = obs['T_interval_K']
        if not 0 < Tl <= Th or not z > 0:
            raise RuntimeError('Invalid observation')
        fixed = [math.log(T0*A/Th), math.log(T0*A/Tl)]
        rectangle = [math.log((T0-dT0)*A/Th), math.log((T0+dT0)*A/Tl)]
        corners = [math.log(t0*A/tz) for t0 in [T0-dT0,T0+dT0] for tz in [Tl,Th]]
        check(obs['id']+'_min_corner', min(corners), rectangle[0])
        check(obs['id']+'_max_corner', max(corners), rectangle[1])
        for t0 in [T0-dT0, T0, T0+dT0]:
            for tz in [Tl, Th]:
                L = math.log(t0*A/tz); q = tz/(t0*A)
                check(obs['id']+'_energy_identity', -math.expm1(-4*L), 1-q**4)
                check(obs['id']+'_number_identity', -math.expm1(-3*L), 1-q**3)
        nominal = obs['T_central_K']
        rows.append(dict(observation=obs, central_L=None if nominal is None else math.log(T0*A/nominal),
                         fixed_T0=mapped(*fixed), T0_error_rectangle=mapped(*rectangle),
                         nonnegative_net_source_fixed_T0=positive(*fixed),
                         nonnegative_net_source_rectangle=positive(*rectangle),
                         zero_source_temperature_K=T0*A,
                         display_redshift_temperature_difference_K=T0*(obs['display_z']-z),
                         constant_physical_temperature_K=T0,
                         constant_temperature_inside_quoted_T_interval=Tl <= T0 <= Th,
                         temperature_if_half_present_energy_added_K=T0*A*2**(-.25)))
    beta = inputs['constant_beta_summary']; A = 1+beta['reported_z_range'][1]
    blo, bhi = beta['beta_interval']; Llo, Lhi = blo*math.log(A), bhi*math.log(A)
    for b in [blo, beta['beta_central'], bhi]:
        check('constant_beta_identity', -math.expm1(-4*b*math.log(A)), 1-A**(-4*b))
    failures = [c for c in checks if not c['passed']]
    return dict(schema='CMB_TZ_SOURCE_INTERVAL_V001', status='FAILED_NUMERICAL_IDENTITIES' if failures else 'COMPLETE_CONDITIONAL_ENDPOINT_TRANSLATION',
                inputs=inputs, observations=rows, constant_beta=dict(summary=beta, z=beta['reported_z_range'][1],
                signed=mapped(Llo,Lhi), nonnegative=positive(Llo,Lhi)), checks=checks, failures=failures,
                fitted_parameters=0, combined_likelihood=False, global_confidence_coverage_claim=False,
                scope='Conditional net source bookkeeping; not photon identity turnover, full measurement likelihood, native origin, or global cosmological exclusion')


def main():
    frozen = snapshot()
    if sys.argv[1:] == ['freeze']:
        print(encode(frozen).decode()); return
    if sys.argv[1:] != ['run']:
        raise RuntimeError('Use freeze or run')
    raw = FREEZE.read_bytes()
    if json.loads(raw) != frozen:
        raise RuntimeError('Frozen inputs differ')
    p = calculate()
    print(encode(dict(freeze_sha256=sha(raw), payload_sha256=sha(encode(p)), payload=p)).decode())
    if p['failures']:
        sys.exit(2)


if __name__ == '__main__':
    main()
