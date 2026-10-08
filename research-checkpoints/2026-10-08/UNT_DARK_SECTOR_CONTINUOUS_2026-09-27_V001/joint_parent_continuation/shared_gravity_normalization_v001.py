"""Frozen before execution: shared early/late normalization audit, no fit.

Keep the tested KB=lambda_s=1 and all bounded-clock inputs. Use ideal-gas
standard thermal counts (gE,gS)=(10.75,10.75) at3MeV and
(2+5.25*(4/11)^(4/3),43/11) at.03MeV, entropy gS0=43/11,
Tgamma0=2.7255K. Calculate exact bounded-clock energy inequalities and
the radiation-expansion ratio at fixed physical temperature. These ideal
thermal counts are scale estimates, NOT an abundance or neutrino solver.

Compare the expansion coefficient with the exposed published BBN-only
95.4% interval [.92,1.04] (Alvey et al1910.10730v2, Eq9); do not turn it
into a new sigma/likelihood or adopt their optional late-time G(t) law.
Derive constraints on the unaltered action family using lower edge g=.92:
KB<2(1-g), lambda_s>=g/(1-g-KB/2). No new point is fitted or adopted.

Also reuse accepted saved modes to report the z0 theoretical lensing/
velocity ratio E=-2aK^2 Phi/(3Dv), Dv=-K^2 Vb/(a^2 h), for BOTH named
preparations, alongside signed numerator/denominator and dust reference.
This is NOT a survey comparison; the example's early normalization fails.
All mode files and dependency identities are retained.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import resource
import numpy as np
import charged_clock_response_v001 as model

BASE = Path(__file__).resolve().parent
OUTPUT = BASE/'SHARED_GRAVITY_NORMALIZATION_V001_RESULT.json'


def main():
    started = time.monotonic()
    c, G, kB, hbar, ev = 299792458., 6.67430e-11, 1.380649e-23, 1.054571817e-34, 1.602176634e-19
    T0, gs0 = 2.7255, 43/11
    ratioG = (1-model.KB/2)*model.LAMBDA_S/(1+model.LAMBDA_S)
    Gcos = G*ratioG
    critical_energy = 3*model.H0_SI**2*c*c/(8*math.pi*Gcos)
    A, baryon0 = model.OA*critical_energy, model.OB*critical_energy
    nQ00 = A*model.D0
    early = []
    for TMeV, ge, gs in ((3.,10.75,10.75),(.03,2+5.25*(4/11)**(4/3),43/11)):
        kT = TMeV*1e6*ev
        a = kB*T0/kT*(gs0/gs)**(1/3)
        rad = math.pi**2*ge*kT**4/(30*hbar**3*c**3)
        lower, upper = nQ00/a**3, math.sqrt(1+model.EPS)*nQ00/a**3
        corrections = [(A+baryon0/a**3+v)/rad for v in (lower, upper)]
        early.append(dict(T_MeV=TMeV, adopted_g_energy=ge, adopted_g_entropy=gs, a=a,
                          radiation_energy_J_m3=rad, clock_excess_over_radiation_bounds=[lower/rad,upper/rad],
                          nonradiation_over_radiation_bounds=corrections,
                          H_over_standard_radiation_bounds=[math.sqrt(ratioG*(1+v)) for v in corrections],
                          H2_over_standard_radiation_bounds=[ratioG*(1+v) for v in corrections]))
    gmin = .92
    family = []
    for kb in (0.,.02,.08,.10,.15):
        lower = gmin/(1-gmin-kb/2)
        family.append(dict(KB=kb, lambda_s_lower=lower,
                           scope='KB=0 is a limiting boundary, not an adopted healthy point.' if kb==0 else 'Necessary published-BBN normalization screen only.'))
    old_path, repaired_path = (BASE/name for name in ('CHARGED_CLOCK_TRANSFER_BAND_V001_RESULT.json',
                                                      'CHARGED_CLOCK_TRANSFER_BAND_V002_RESULT.json'))
    old, repaired = json.loads(old_path.read_text()), json.loads(repaired_path.read_text())
    fix = {r['k_Mpc_inverse']:r for r in repaired['rows']}
    eg_rows = []
    for row in old['rows']:
        accepted = row if row['all_numerical_controls_passed'] else fix[row['k_Mpc_inverse']]
        assert accepted['all_numerical_controls_passed']
        y = np.array(accepted['trajectory_2048_scaled'][-1])*np.array(accepted['state_scales'])[:,None]
        ref = np.array(row['final_comparator_states'])
        K = row['K']
        h = model.background(0.)['h']
        for j,label in enumerate(('baryon_isocurvature','adiabatic_development')):
            phi, vb = y[0,j+6], y[2,j+6]
            num, den = -2*K*K*phi/3, -K*K*vb/h
            rnum, rden = -2*K*K*ref[0,j]/3, -K*K*ref[2,j]
            eg_rows.append(dict(k_Mpc_inverse=row['k_Mpc_inverse'],a=1.,preparation=label,
                                numerator=float(num), velocity_convergence=float(den),
                                E_theory=float(num/den) if den!=0 else None,
                                reference_numerator=float(rnum), reference_velocity_convergence=float(rden),
                                reference_E=float(rnum/rden) if rden!=0 else None,
                                E_ratio=float((num/den)/(rnum/rden)) if den*rden*rnum!=0 else None))
    result = dict(self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  inputs_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (old_path,repaired_path,BASE/'charged_clock_response_v001.py')},
                  ratio_G_cos_GN=ratioG, thermal_scaling_rows=early,
                  published_source='https://arxiv.org/html/1910.10730v2',
                  published_BBN_only_interval_95p4=[.92,1.04],
                  conditional_all_epoch_normalization_screen_passed=all(.92<=r['H2_over_standard_radiation_bounds'][0]<=1.04 for r in early),
                  necessary_family_KB_upper_exclusive=2*(1-gmin), family_coupling_bounds=family,
                  scope='Published-constraint mapping under standard thermal particle physics and stated local GN branch; not a new abundance likelihood.',
                  z0_lensing_velocity_theory=eg_rows,
                  elapsed_seconds=time.monotonic()-started, peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
