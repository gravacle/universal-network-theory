"""Saved arrays/custody only; no producer import, orbit, ODE or quadrature."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
RESULT = J/'SPHERICAL_DUST_SHADOW_V001_RESULTS.json'
FREEZE = J/'SPHERICAL_DUST_SHADOW_V001_FROZEN.json'
PINS = {RESULT: '171fb246a4716f5b769c420cb6680a8c474cbc59f676bd10279d1e300a1b8c5d',
        FREEZE: '5b966f80569a25a5e3317e944af530671244cdf097bf29a0872069ce2cfc8868'}
counts = {}; maxima = {}; failures = []


def encoded(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def check(name, actual, expected, tol=2e-11, scale=None):
    a, b = np.asarray(actual), np.asarray(expected)
    if scale is None:
        scale = np.maximum(1., np.maximum(np.abs(a), np.abs(b)))
    err = np.abs(a-b)/np.maximum(np.abs(scale), 1e-300)
    worst = float(np.max(err))
    counts[name] = counts.get(name, 0)+int(err.size)
    maxima[name] = max(maxima.get(name, 0.), worst)
    if not np.all(np.isfinite(err)) or worst > tol:
        failures.append(dict(check=name, error=worst, tolerance=tol))


def yes(name, value):
    check(name, int(bool(value)), 1, 0.)


def digest(path):
    p = path.resolve(strict=True); p.relative_to(ROOT)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def shape(z):
    # Direct polynomial differentiation, no field evaluation or ODE.
    inside = z < 1.; x = np.minimum(z, 1.); C = 3465/128
    mu = C*(1/3-4*x*x/5+6*x**4/7-4*x**6/9+x**8/11)
    dm = C*(-8*x/5+24*x**3/7-8*x**5/3+8*x**7/11)
    dd = C*(-8/5+72*x*x/7-40*x**4/3+56*x**6/11)
    safe = np.maximum(z, 1.)
    return (np.where(inside, mu, safe**-3), np.where(inside, dm, -3*safe**-4),
            np.where(inside, dd, 12*safe**-5),
            np.where(inside, 3465/(512*math.pi)*(1-x*x)**4, 0.))


def geom(vector, z, dm, dd):
    y = np.asarray(vector); f, v, fm, vm, fmm, vmm = y[1:].reshape(6, len(z))
    fz = fm*dm; fzz = fmm*dm*dm+fm*dd
    s = f+z*fz; jac = f*f*s
    jz = 2*f*fz*s+f*f*(2*fz+z*fzz)
    jd = 2*f*v*s+f*f*(v+z*vm*dm)
    return y[0], f, v, fm, fmm, s, jac, jz, jd


def main():
    for p, h in PINS.items(): yes('top_hash', digest(p) == h)
    w = json.loads(RESULT.read_bytes()); d = w['payload']; fr = json.loads(FREEZE.read_bytes())
    yes('payload_hash', hashlib.sha256(encoded(d)).hexdigest() == w['payload_sha256'])
    yes('freeze_binding', w['freeze_sha256'] == PINS[FREEZE])
    for p, h in fr['files'].items(): yes('frozen_member_hash', digest(ROOT/p) == h)
    yes('config', d['configuration'] == fr['configuration'])
    cfg = d['configuration']; z = np.asarray(d['shell_labels']); n = len(z)
    yes('all_cases', [c['gap'] for c in d['cases']] == [128, 8192])
    yes('shell_census', n == 257 and np.array_equal(z, np.arange(257)/16))
    yes('result_status', d['status'] == 'COMPLETE_DUST_SHADOW_ONLY' and not d['failures'])
    yes('scope', d['finite_R_trajectory_qualified'] is False)
    yes('producer_check_count', sum(d['checks'].values()) == 64826)
    for name, error in d['worst_scaled_errors'].items():
        tol = (cfg['material_tolerance'] if name.startswith(('quadrature_', 'saved_anchor_')) else
               cfg['derivative_tolerance'] if name.startswith('parameter_') else
               cfg['state_tolerance'] if name in ('method_state', 'sphere_energy') else
               cfg['readout_tolerance'] if name.startswith('method_') else cfg['arithmetic_tolerance'])
        yes('reported_fixed_gate', math.isfinite(error) and error <= tol)
    old = json.loads((J/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json').read_bytes())['payload']
    mu, dm, dd, seed = shape(z); summaries = []
    for case in d['cases']:
        R = case['gap']; s0 = case['source_state']; ref = case['background_reference']
        originals = [x for x in old['cases'] if x['gap'] == R]
        yes('source_mapping', len(originals) == 2 and all(x['source_state'] == s0 for x in originals))
        yes('reference_mapping', ref == old['reference'])
        yes('case_status', case['status'] == 'COMPLETE_DUST_SHADOW_ONLY' and case['finite_R_trajectory_qualified'] is False)
        G, c, beta = cfg['G_SI'], cfg['c'], cfg['beta']; ell = cfg['ell_kpc']*1000*cfg['parsec_m']
        gs = s0['gstar']; td = math.sqrt(ell/gs); M = gs*ell**2/G; eps = gs*ell/c**2
        stress = gs**2/(4*math.pi*G*originals[0]['Kb']); H0 = ref['H0_s_inverse']
        rb = 3*H0**2*ref['Omega_b']/(8*math.pi*G); rh = stress*beta*R*s0['I']/c**2
        kb = 4*math.pi*rb*ell**3/(3*M); kh = 4*math.pi*rh*ell**3/(3*M)
        for name, val in [('ell_m', ell), ('t_dyn_s', td), ('seed_mass_kg', M), ('epsilon', eps),
                          ('rho0_H1_kg_m3', rh), ('kappa', kb+kh), ('initial_potential_compactness', 693*eps/256)]:
            check('dimensional_'+name, case[name], val, scale=abs(val))
        check('radiation_active_mass', case['radiation_active_mass_per_unit_brightness_kg_m3'],
              3*H0**2*case['ordinary_radiation_H2_omission_fraction_today']/(4*math.pi*G),
              scale=case['radiation_active_mass_per_unit_brightness_kg_m3'])
        times = np.asarray(case['fine_path_times']); path = case['fine_path_vectors']
        yes('fine_path_census', len(path) == 65 and len(times) == 65 and np.array_equal(times, np.arange(65)/1024))
        gpath = [geom(y, z, dm, dd) for y in path]
        for a, f, v, fm, fmm, sr, jac, jz, jd in gpath:
            yes('saved_domain', a > 0 and np.all(f > 0) and np.all(sr > 0) and np.all(np.isfinite(jac)))
        methods = case['method_sample_vectors']; yes('methods', set(methods) == {'RK4_coarse', 'RK4_fine', 'DOPRI54'})
        yes('sample_times', [x['tau'] for x in case['samples']] == cfg['times'])
        for it, sample in enumerate(case['samples']):
            t = sample['tau']; fine = np.asarray(methods['RK4_fine'][it])
            check('path_sample_identity', fine, path[int(round(t*1024))], tol=0.)
            for name in ['RK4_coarse', 'DOPRI54']:
                check('method_state_recombined', methods[name][it], fine, cfg['state_tolerance'])
            a, f, v, fm, fmm, sr, jac, jz, jd = geom(fine, z, dm, dd)
            o = {k: np.asarray(vv) for k, vv in sample['fields'].items()}
            yes('field_lengths', all(vv.shape == (n,) for vv in o.values()))
            check('sample_A', sample['A'], a); check('sample_seconds', sample['seconds'], t*td)
            for name, value in [('f', f), ('f_tau', v), ('f_mu', fm), ('f_mumu', fmm), ('s', sr), ('J', jac), ('J_z', jz),
                                ('I', s0['I']/(a**3*jac)), ('e', R**4*o['r']*(2+o['r'])/4),
                                ('p', o['w']*o['e']), ('action_recovered', o['I']),
                                ('cN_over_c_squared', o['omega']/R*o['cI2']), ('cN2_over_vdyn2', o['omega']/R*o['cI2']/eps),
                                ('aP_over_gstar', o['cN2_over_vdyn2']*jz/(a*sr*jac)), ('peculiar_velocity_over_vdyn', a*z*v),
                                ('vpec2_over_c2', eps*(a*z*v)**2), ('rho0_H_kg_m3', rh/(a**3*jac)),
                                ('rho_b_kg_m3', (rb+M/ell**3*seed)/(a**3*jac)), ('pressure_Pa', stress*beta*o['p']),
                                ('internal_energy_per_restmass_over_vdyn2', o['dE']/eps),
                                ('internal_energy_rate_over_vdyn2_per_tau', o['p']/(R*o['I']*eps)*(-3*sample['H_s_inverse']*td-jd/jac)),
                                ('rest_gravity_energy_defect_kg_m3', o['rho0_H_kg_m3']*o['dE']),
                                ('active_pressure_mass_kg_m3', 3*stress*beta*o['p']/c**2),
                                ('dE', o['dW']-o['p']/(R*o['I']))]:
                check('field_'+name, o[name], value, scale=np.maximum(abs(value), 1e-300))
            check('virial_recombined', o['I']*o['omega'], o['e']+o['p'], scale=o['e'])
            check('common_flow_recombined', o['rho0_H_kg_m3']/o['rho_b_kg_m3'], rh/(rb+M/ell**3*seed))
            for tube in sample['worldtubes']:
                zz = tube['initial_label']; ix = int(round(zz*16)); delta = -math.expm1(3*math.log(f[ix]))
                hx = kh*zz**3*delta; bx = mu[ix]*zz**3+kb*zz**3*delta
                for name, value in [('physical_radius_m', a*zz*f[ix]*ell), ('hard_rest_mass_kg', kh*zz**3*M),
                                    ('hard_rest_excess_over_seed_M', hx), ('baryon_rest_excess_over_seed_M', bx),
                                    ('hard_rest_excess_over_baryon_rest_excess', hx/bx),
                                    ('hard_current_mass_label_over_seed_M', kh*zz**3),
                                    ('baryon_current_mass_label_over_seed_M', mu[ix]*zz**3+kb*zz**3)]:
                    check('worldtube_'+name, tube[name], value, scale=max(abs(value), 1e-300))
        forcing = case['accumulated_forcing']; alt = case['alternate_node_forcing']
        for ledger in (forcing, alt):
            yes('forcing_scope', ledger['actual_force_and_Lipschitz_tube'] == 'NOT_PROVED' and
                ledger['actual_finite_R_acoustic_domain'] == 'NOT_QUALIFIED' and ledger['finite_R_trajectory_qualified'] is False)
            change = np.asarray(case['samples'][-1]['fields']['internal_energy_per_restmass_over_vdyn2'])-np.asarray(case['samples'][0]['fields']['internal_energy_per_restmass_over_vdyn2'])
            check('saved_internal_change', ledger['exact_internal_energy_change_per_restmass_over_vdyn2'], change)
            check('volume_work_defect', np.asarray(ledger['thermodynamic_volume_work_per_restmass_over_vdyn2'])-change,
                  ledger['volume_work_trapezoid_defect_over_vdyn2'])
            for L in (8., 16.): check('interface_margin', ledger['prospective_interface_margins'][str(L)], L-4-ledger['shadow_characteristic_travel_over_ell'])
        check('path_min_J', forcing['sampled_min_J'], min(float(np.min(g[6])) for g in gpath))
        check('path_min_radial', forcing['sampled_min_radial_jacobian'], min(float(np.min(g[5])) for g in gpath))
        check('path_max_v2', forcing['sampled_maxima']['vpec2_over_c2'], max(float(np.max(eps*(g[0]*z*g[2])**2)) for g in gpath))
        summary = dict(gap=R,final_tau=cfg['times'][-1],final_Myr=cfg['times'][-1]*td/(365.25*86400*1e6),
            sampled_min_J=forcing['sampled_min_J'],sampled_min_radial_jacobian=forcing['sampled_min_radial_jacobian'],
            sampled_maxima=forcing['sampled_maxima'],shadow_characteristic_travel_over_ell=forcing['shadow_characteristic_travel_over_ell'],
            final_worldtubes=case['samples'][-1]['worldtubes'],forcing_diagnostic_ranges={},alternate_node_differences={})
        for key, val in forcing.items():
            if isinstance(val, list):
                arr=np.asarray(val); summary['forcing_diagnostic_ranges'][key]=[float(arr.min()),float(arr.max())]
                summary['alternate_node_differences'][key]=float(np.max(abs(arr-np.asarray(alt[key]))))
        summaries.append(summary)
    output=dict(status='PASS_SAVED_ARITHMETIC' if not failures else 'FAILED_SAVED_AUDIT',
        result_sha256=PINS[RESULT],freeze_sha256=PINS[FREEZE],producer_payload_sha256=w['payload_sha256'],
        auditor_sha256=digest(Path(__file__)),frozen_files=len(fr['files']),checks=counts,maxima=maxima,failures=failures,
        producer_checks=sum(d['checks'].values()),producer_seconds=d['seconds'],producer_peak_self_rss_bytes=d['peak_self_rss_bytes'],
        summaries=summaries,scope='No dynamics/material rerun. Sample algebra, saved state-vector comparison and ledger checks only.',
        not_recomputed=['material quadrature/action inversion','adaptive/fixed integrator execution','parameter FD controls',
                        'material-dependent forcing sums at 65 nodes (only state vectors, not all material path fields, are saved)'])
    print(encoded(output).decode())


if __name__ == '__main__': main()
