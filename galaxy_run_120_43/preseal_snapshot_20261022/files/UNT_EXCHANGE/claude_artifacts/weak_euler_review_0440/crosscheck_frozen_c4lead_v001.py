import sys; sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import numpy as np
# crosscheck_frozen_c4lead_v001.py -- Claude4 lead, dispatch 0440/0446 remaining cross-checks.
#  (1) H1 closed-form oracle (algebra_oracle_h1v001.oracle_A_b) vs Claude3 module, random complex
#      vertical-shear cases.
#  (2) F8 root-structured fixture: U_R/U_z real float64 dtype, U_phi purely imaginary, divU and G
#      complex dtype with zero imaginary part (the structure of root's pinned helicity/0438 chain),
#      compared with the H2 loop reference and the H1 oracle; exactness of the real->complex cast;
#      sensitivity of this fixture to a missing conjugate on U_phi.
# Synthetic arrays only. Loads every target by FILE PATH. Writes only the --out JSON.
import hashlib
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PINS = {
    'module': (os.path.join(HERE, 'c3_snapshot_8632bda6', 'weak_euler_assembly_c3v001.py'),
               '8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da'),
    'oracle': (os.path.join(HERE, 'algebra_oracle_h1v001.py'),
               '29fc7fd429c921c4e6e7c04a624ce4db6ffcb0b32a8c0f5a432413ce73feb23e'),
    'reference': (os.path.join(HERE, 'reference_weak_euler_h2v001.py'),
                  '61f1982cbb48a25e1bd1a50afa13c217eb0b77bb905e7db5b19511c714b2a4ac'),
    'contract': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                 'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json',
                 '5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe'),
}
TOL = 1e-12
OUT_KEYS = ('A', 'b', 'E', 'PM', 'VR', 'VP', 'VZ')


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel(got, exp):
    got = np.asarray(got); exp = np.asarray(exp)
    if got.shape != exp.shape:
        return float('inf')
    scale = max(float(np.max(np.abs(exp))) if exp.size else 0.0, 1e-300)
    return float(np.max(np.abs(got - exp)) / scale) if exp.size else 0.0


def base_case(rng, n, k, m, structure):
    R = rng.uniform(0.5, 3.0, n)
    rho = rng.uniform(0.5, 2.0, n)
    K = rng.uniform(0.5, 2.0, n)
    P = K * rho ** (5.0 / 3.0)
    kw = dict(R=R, rho=rho, P=P,
              K_R=rng.uniform(-1, 1, n), K_z=rng.uniform(-1, 1, n),
              P_R=rng.uniform(-1, 1, n), P_z=rng.uniform(-1, 1, n),
              Omega=rng.uniform(0.3, 1.5, n),
              Omega_R=rng.choice([-1, 1], n) * rng.uniform(0.2, 0.8, n),
              Omega_z=rng.choice([-1, 1], n) * rng.uniform(0.2, 0.8, n),
              volume_weights=rng.uniform(0.1, 1.0, n),
              f_R=rng.normal(size=n) + 1j * rng.normal(size=n),
              f_phi=rng.normal(size=n) + 1j * rng.normal(size=n),
              f_z=rng.normal(size=n) + 1j * rng.normal(size=n),
              m=m, gamma=5.0 / 3.0, normalization_scale=float(rng.uniform(0.5, 4.0)),
              provenance='claude4-crosscheck-synthetic')
    if structure == 'general':
        c = lambda: rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
        kw.update(U_R=c(), U_phi=c(), U_z=c(), divU=c(), G=c())
    else:  # 'root': real U_R/U_z (float64), pure-imaginary U_phi, real-valued complex-dtype divU/G
        r = lambda: rng.normal(size=(n, k))
        kw.update(U_R=r(), U_phi=1j * r(), U_z=r(),
                  divU=r().astype(np.complex128), G=r().astype(np.complex128))
    return kw


def oracle_kwargs(kw):
    return {k: v for k, v in kw.items() if k not in ('normalization_scale', 'provenance')}


def main():
    out_path = sys.argv[sys.argv.index('--out') + 1]
    report = {'python': sys.version.split()[0], 'numpy': np.__version__, 'hashes': {}, 'checks': []}
    for key, (path, pin) in PINS.items():
        h = sha(path)
        report['hashes'][key] = {'path': path, 'sha256': h, 'pin_ok': h.startswith(pin)}
        if not h.startswith(pin):
            raise SystemExit('pin mismatch for ' + key)
    mod = load(PINS['module'][0], 'c3_frozen_candidate')
    ora = load(PINS['oracle'][0], 'h1_oracle')
    ref = load(PINS['reference'][0], 'h2_reference')
    target = mod.assemble_weak_euler

    def add(name, err, extra=None):
        ok = bool(err <= TOL)
        entry = {'check': name, 'max_rel_err': err, 'pass': ok}
        if extra:
            entry.update(extra)
        report['checks'].append(entry)

    shapes = [(7, 3), (4, 4), (16, 5), (1, 1), (5, 8)]
    # (1) oracle vs module, general complex maps with vertical shear
    worst = 0.0
    for seed in range(6):
        for (n, k) in shapes:
            for m in range(1, 7):
                rng = np.random.default_rng(1000 * seed + 10 * n + k)
                kw = base_case(rng, n, k, m, 'general')
                got = target(**kw)
                A0, b0 = ora.oracle_A_b(**oracle_kwargs(kw))
                s = kw['normalization_scale']
                worst = max(worst, rel(got['A'], A0 / s), rel(got['b'], b0 / s))
    add('oracle_vs_module_general_complex', worst, {'cases': 6 * len(shapes) * 6})

    # (2) F8 root-structured fixture
    worst_ref, worst_ora, worst_cast, min_conj_gap, max_imagA = 0.0, 0.0, 0.0, float('inf'), 0.0
    cast_bitwise = True
    for seed in range(6):
        for (n, k) in shapes:
            for m in range(1, 7):
                rng = np.random.default_rng(7000 + 1000 * seed + 10 * n + k)
                kw = base_case(rng, n, k, m, 'root')
                assert kw['U_R'].dtype == np.float64 and kw['U_z'].dtype == np.float64
                got = target(**kw)
                exp = ref.reference_assemble(**{**kw, 'U_R': kw['U_R'].astype(np.complex128),
                                                'U_z': kw['U_z'].astype(np.complex128)})
                worst_ref = max(worst_ref, max(rel(got[key], exp[key]) for key in OUT_KEYS))
                A0, b0 = ora.oracle_A_b(**oracle_kwargs(kw))
                s = kw['normalization_scale']
                worst_ora = max(worst_ora, rel(got['A'], A0 / s), rel(got['b'], b0 / s))
                # cast exactness: same values supplied as complex128 must give bitwise-identical outputs
                got_c = target(**{**kw, 'U_R': kw['U_R'].astype(np.complex128),
                                  'U_z': kw['U_z'].astype(np.complex128)})
                for key in OUT_KEYS:
                    if not np.array_equal(got[key], got_c[key]):
                        cast_bitwise = False
                    worst_cast = max(worst_cast, rel(got[key], got_c[key]))
                # A is real-valued for this structure (derivation in PARTIAL_REVIEW_0440_V002)
                max_imagA = max(max_imagA, float(np.max(np.abs(got['A'].imag)) /
                                                 max(float(np.max(np.abs(got['A']))), 1e-300)))
                # sensitivity: drop the conjugate on U_phi only (test side of the phi group and of b)
                w, rho = kw['volume_weights'], kw['rho']
                wrho = w * rho
                Up = kw['U_phi']
                AP = got['VP'] * (1j * m * kw['Omega'])[:, None] \
                    + (2 * kw['Omega'] + kw['R'] * kw['Omega_R'])[:, None] * got['VR'] \
                    + (kw['R'] * kw['Omega_z'])[:, None] * got['VZ']
                phi_block_conj = Up.conj().T @ (wrho[:, None] * AP)
                phi_block_noconj = Up.T @ (wrho[:, None] * AP)
                gap = float(np.max(np.abs(phi_block_noconj - phi_block_conj)) /
                            max(float(np.max(np.abs(got['A'] * s))), 1e-300))
                min_conj_gap = min(min_conj_gap, gap)
    add('F8_root_structured_module_vs_H2_reference_all_outputs', worst_ref, {'cases': 6 * len(shapes) * 6})
    add('F8_root_structured_module_vs_H1_oracle_A_b', worst_ora)
    report['checks'].append({'check': 'F8_real_to_complex_cast_bitwise_identical_outputs',
                             'pass': cast_bitwise, 'max_rel_err': worst_cast})
    report['checks'].append({'check': 'F8_structure_A_real_valued (|Im A|/|A|, expected ~1e-16)',
                             'pass': bool(max_imagA <= 1e-13), 'max_rel_imag': max_imagA})
    report['checks'].append({'check': 'F8_missing_conj_on_U_phi_would_change_A (min relative change)',
                             'pass': bool(min_conj_gap > 1e-3), 'min_relative_change': min_conj_gap})

    report['module_sha256_after'] = sha(PINS['module'][0])
    report['all_pass'] = all(c['pass'] for c in report['checks']) and \
        report['module_sha256_after'] == PINS['module'][1]
    with open(out_path, 'w') as fh:
        json.dump(report, fh, indent=1)
        fh.write('\n')
    print(json.dumps({'python': report['python'], 'numpy': report['numpy'], 'all_pass': report['all_pass'],
                      'checks': report['checks']}, indent=1))


if __name__ == '__main__':
    main()
