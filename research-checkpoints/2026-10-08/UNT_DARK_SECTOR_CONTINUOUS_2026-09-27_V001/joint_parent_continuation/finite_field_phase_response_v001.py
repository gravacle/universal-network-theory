"""Prospective common-phase constitutive screen. Stdout only; no galaxy solver."""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import sys
sys.dont_write_bytecode = True
import base64
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import zlib
import numpy as np
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE / 'FINITE_FIELD_PHASE_RESPONSE_V001_FROZEN.json'
TRANSPORT = 'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json'
TRANSPORT_HASH = '11d5898717488b1ab3fb75e3294e55e5674f2b3f2d623f15cc9bb2e9a54c4db4'
RAW_HASH = '822dd216b33ff4ce08cdcd8b5f1ad5e3e27c583b7833107cef58b158cb3f9cc0'
OLD_FREEZE_HASH = 'e2d80308d159f7d7b0ec4217e6082c1157eda6cc81000ac4d83c4b6255b989cb'
GLOBAL = 'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json'
GLOBAL_HASH = '11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628'
CONFIG = dict(beta=.005, selected_R=[128, 8192], physical_g_m_s2=[1e-12, 1e-10, 1e-8],
    log_lapse=[0., -1e-8, -1e-7], orders=[64, 128], simpson_panels=1024,
    bisections=80, bracket_doublings=64, arithmetic_tolerance=2e-11,
    quadrature_tolerance=2e-8, expected_inputs=144, expected_rows=1296,
    c_m_s=299792458., parsec_m=3.085677581491367e16,
    branch_certificate_eta_squared=1/12,
    selection='R128/R8192 selected after the preceding full five-gap screen, before this screen, to contrast its warmer/kpc and colder/short cosmic scales; exploratory, not an unused observational test')


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files, seen = {}, set()
    def add(path, expected=None):
        path = path.resolve(strict=True); path.relative_to(ROOT)
        actual = sha(path)
        if expected is not None and actual != expected:
            raise RuntimeError('Changed input: ' + str(path))
        files[str(path.relative_to(ROOT))] = actual
        return path
    def manifest(path, expected=None):
        path = add(path, expected)
        if path in seen:
            return
        seen.add(path)
        for name, digest in json.loads(path.read_text())['files'].items():
            raw = Path(name)
            candidates = [raw] if raw.is_absolute() else [ROOT/raw, path.parent/raw]
            owned = set()
            for candidate in candidates:
                candidate = candidate.resolve()
                if not candidate.is_relative_to(ROOT) or not candidate.is_file():
                    continue
                owned.add(candidate)
            if len(owned) != 1:
                raise RuntimeError('Missing or ambiguous ancestor: ' + name)
            member = add(owned.pop(), digest)
            if member.name.endswith('_FROZEN.json'):
                manifest(member)
    def authenticated_wrapper(value, frozen):
        payload = value['payload']
        if value['freeze_sha256'] != sha(frozen):
            raise RuntimeError('Inherited freeze identity differs')
        if value['payload_sha256'] != hashlib.sha256(encode(payload)).hexdigest():
            raise RuntimeError('Inherited payload identity differs')
        if payload['status'] != 'COMPLETE' or payload['failures']:
            raise RuntimeError('Inherited numerical qualification is incomplete')
        return payload
    transport = json.loads(add(HERE/TRANSPORT, TRANSPORT_HASH).read_text())
    if transport['encoding'] != 'zlib_base64_canonical_json':
        raise RuntimeError('Unexpected transport encoding')
    decoder = zlib.decompressobj()
    raw = decoder.decompress(base64.b64decode(transport['data'], validate=True)) + decoder.flush()
    if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise RuntimeError('Transport must contain exactly one complete zlib stream')
    if len(raw) != transport['raw_bytes'] or hashlib.sha256(raw).hexdigest() != RAW_HASH or transport['raw_sha256'] != RAW_HASH:
        raise RuntimeError('Decoded source identity differs')
    old_freeze = HERE/'FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json'
    manifest(old_freeze, OLD_FREEZE_HASH)
    old = authenticated_wrapper(json.loads(raw), old_freeze)
    if len(old['rows']) != 360:
        raise RuntimeError('Original 360-row census changed')
    expected = {(s, r, gap) for s in range(4) for r in range(18) for gap in [32,128,512,2048,8192]}
    if {(r['spectrum_index'], r['reference'], r['R']) for r in old['rows']} != expected:
        raise RuntimeError('Original labels changed')
    global_freeze = HERE/GLOBAL.replace('_RESULTS.json', '_FROZEN.json')
    manifest(global_freeze)
    global_payload = authenticated_wrapper(json.loads(add(HERE/GLOBAL, GLOBAL_HASH).read_text()), global_freeze)
    if len(global_payload['spectra']) != 4 or len(global_payload['references']) != 18:
        raise RuntimeError('Spectrum/reference census changed')
    add(HERE/'FINITE_FIELD_COMMON_PHASE_DENSITY_V001.md', 'cb8ec369a4e70f78b0bd54e2142f746bdf414c8982b141ba9027bd4958d7bb59')
    add(HERE/'MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md', '64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3')
    add(Path(__file__))
    add(HERE/'FINITE_FIELD_PHASE_RESPONSE_PROTOCOL_V001.md')
    selected = [dict(source_row_index=n, **row) for n,row in enumerate(old['rows']) if row['R'] in CONFIG['selected_R']]
    if len(selected) != CONFIG['expected_inputs']:
        raise RuntimeError('Selected-input census differs')
    return selected, global_payload, dict(configuration=CONFIG, files=files)


def rule(order):
    # Pair theta and pi-theta. These half-interval weights sum to one.
    if order:
        nodes, weights = leggauss(order)
        theta = (nodes+1)*math.pi/4; weights = weights/2
    else:
        n = CONFIG['simpson_panels']; theta = np.linspace(0, math.pi/2, n+1)
        weights = np.ones(n+1); weights[1:-1:2] = 4; weights[2:-1:2] = 2
        weights /= 3*n
    return weights, np.cos(theta), np.sin(theta)**2


def center(r, eta):
    k = 1+r*r
    return 2*math.sqrt(k/3)*math.sinh(math.asinh(3*math.sqrt(3)*eta/(2*k**1.5))/3)


def geometry(r, eta, quadrature):
    w, x, sin2 = quadrature; c = center(r, eta)
    offset_plus = (2*c+r*x)**2+2*c*c+r*r
    offset_minus = (2*c-r*x)**2+2*c*c+r*r
    a = np.sqrt(2+offset_plus); b = np.sqrt(2+offset_minus)
    odd = 4*c*r*x
    inv_even = (1/a+1/b)/2
    inv_odd = -odd/(a*b*(a+b))
    delta = -float(np.dot(w, (offset_plus/(a*(math.sqrt(2)+a)) + offset_minus/(b*(math.sqrt(2)+b)))/2))
    excess = -delta/(1+delta)
    return c, a, b, inv_even, inv_odd, excess


def frequency_excess(r, eta, quadrature):
    return geometry(r, eta, quadrature)[-1]


def action(r, eta, quadrature):
    _, a, b, _, _, _ = geometry(r, eta, quadrature)
    w, _, sin2 = quadrature
    return r*r/math.sqrt(2)*float(np.dot(w, sin2*(a+b)/2))


def orbit(r, eta, quadrature):
    c, a, b, ie, io, excess = geometry(r, eta, quadrature)
    w, x, sin2 = quadrature; omega = 1+excess; L = float(np.dot(w, ie))
    odd = 4*c*r*x
    j_even = (a**-3+b**-3)/2
    j_odd = -odd*(a*a+a*b+b*b)/(a**3*b**3*(a+b))
    def pair_mean(pair, power=1):
        even, odd_part = pair
        ew, ow = (ie, io) if power == 1 else (j_even, j_odd)
        return float(np.dot(w, even*ew+odd_part*ow))
    def multiply(left, right):
        le, lo = left; re, ro = right
        return le*re+lo*ro, le*ro+lo*re
    z = (c, r*x); z2 = (c*c+r*r*x*x, 2*c*r*x)
    z3 = (c**3+3*c*r*r*x*x, 3*c*c*r*x+r**3*x**3)
    z4 = (c**4+6*c*c*r*r*x*x+r**4*x**4, 4*c**3*r*x+4*c*r**3*x**3)
    mean2 = pair_mean(z2)/L; mean3 = pair_mean(z3)/L; mean4 = pair_mean(z4)/L
    mean_z = pair_mean(z)/L
    source_mean = eta-mean3
    d = 1+r*r+3*c*c; cr = -2*c*r/d; ce = 1/d
    qr = (12*c*cr+2*r*(1+x*x), 4*(c+r*cr)*x)
    qe = (12*c*ce, 4*r*ce*x)
    om_r = omega*pair_mean(qr, 3)/(2*L)
    om_eta = omega*pair_mean(qe, 3)/(2*L)
    i = r*r/math.sqrt(2)*float(np.dot(w, sin2*(a+b)/2))
    ir_direct = math.sqrt(2)*r*float(np.dot(w, sin2*(a+b)/2)) + r*r/(2*math.sqrt(2))*pair_mean((sin2*qr[0], sin2*qr[1]))
    ir = r*(d-4*c*c*r*r/d)/omega
    ieta = r*r/(2*math.sqrt(2))*pair_mean((sin2*qe[0], sin2*qe[1]))
    def mderivative(za, qa):
        za3 = multiply(z2, za)
        first = 3*pair_mean(za3)/L
        cov = pair_mean(multiply(z3, qa), 3)/L - mean3*pair_mean(qa, 3)/L
        return first-cov/2
    mr = mderivative((cr, x), qr); me = mderivative((ce, 0), qe)
    c0 = center(0, eta); k0 = 1+3*c0*c0
    shift = -c*r*r/(1+c*c+c*c0+c0*c0)
    xp = r+shift; xm = -r+shift
    def excess_energy(v):
        return v*v*(k0/2+c0*v+v*v/4)
    emin = -.5*c0*c0-.75*c0**4; exc = excess_energy(xp)
    energy = emin+exc
    pressure = mean4/4+eta*source_mean/2
    kinetic = r*r/4*float(np.dot(w, sin2*(a+b)/2))/L
    if r:
        eii = om_r/ir; bi = -mr/ir
        deficit = me-mr*ieta/ir
        maxwell = -(om_eta-om_r*ieta/ir)
        phase_deficit_other = me-mr*om_eta/om_r
    else:
        eii = 3*(1-7*c0*c0)/(4*k0*k0); bi = -3*c0/k0**1.5
        deficit = 3*c0*c0/k0
        maxwell = bi
        phase_deficit_other = 1-(1+5*c0*c0)/(k0*(1-7*c0*c0))
    if eta == 0:
        source_mean = mean_z = mean3 = bi = maxwell = ieta = mr = om_eta = 0.
    return dict(r=r, eta=eta, c=c, i=i, omega=omega, omega_excess=excess,
        epsilon=energy, epsilon_min=emin, epsilon_exc=exc, pressure=pressure,
        mean2=mean2, mean3=mean3, mean4=mean4, b=source_mean,
        direct_mean=mean_z, kinetic=kinetic, eii=eii, b_i=bi,
        susceptibility_deficit_fixed_i=deficit, square_correction=bi*bi/eii,
        phase_deficit_other=phase_deficit_other, maxwell_b_i=maxwell,
        i_r=ir, i_r_direct=ir_direct, i_eta=ieta, omega_r=om_r,
        omega_eta=om_eta, mean3_r=mr, mean3_eta=me,
        other_turning_exc=excess_energy(xm))


def phase_orbit(target, eta, ib, quadrature):
    c0 = center(0, eta); k0 = 1+3*c0*c0
    minimum_excess = 3*c0*c0/(math.sqrt(k0)+1)
    if eta*eta >= CONFIG['branch_certificate_eta_squared']:
        return 'UNCERTIFIED_BRANCH', None
    if target <= minimum_excess:
        return 'EMPTY', orbit(0, eta, quadrature)
    lo = 0.; hi = max(math.sqrt(2*ib), math.sqrt(8*target/3), 1e-100)
    for _ in range(CONFIG['bracket_doublings']):
        if frequency_excess(hi, eta, quadrature) >= target:
            break
        hi *= 2
    else:
        raise RuntimeError('No certified occupied frequency bracket')
    for _ in range(CONFIG['bisections']):
        mid = (lo+hi)/2
        if frequency_excess(mid, eta, quadrature) < target:
            lo = mid
        else:
            hi = mid
    return 'OCCUPIED', orbit((lo+hi)/2, eta, quadrature)


def fixed_action_orbit(ib, eta, quadrature):
    lo = 0.; hi = math.sqrt(2*ib)
    if action(hi, eta, quadrature) < ib*(1-1e-14):
        raise RuntimeError('Exact action upper bracket failed')
    for _ in range(CONFIG['bisections']):
        mid = (lo+hi)/2
        if action(mid, eta, quadrature) < ib:
            lo = mid
        else:
            hi = mid
    return orbit((lo+hi)/2, eta, quadrature)


def soft_ground(spectrum, h):
    ds = np.asarray(spectrum['delta']); ws = np.asarray(spectrum['weights'])
    ys = 2*ds/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/(2*ds*ds))/3)
    B = float(np.dot(ws, ds*ys))
    E = -float(np.dot(ws, ds*ds*ys*ys/2+3*ys**4/4))
    return dict(B=B, E=E, Pi=-E,
        deficit=float(np.dot(ws, ys**3/ds)),
        susceptibility_deficit=float(np.dot(ws, 3*ys*ys/(ds*ds+3*ys*ys))),
        maximum_cubic_relative=float(np.max(np.abs(ys*(ds*ds+ys*ys)-ds*h)/np.maximum(np.abs(ds*h), 1e-300))))


def response(o, soft, G, S, R, kb, occupied, phase=True):
    beta = CONFIG['beta']; z = (G/S)**2
    h = G/math.sqrt(1+z); hp = (1+z)**-1.5; hpp = -3*G/S**2*(1+z)**-2.5
    B = soft['B']+beta*R*R*o['b']; F = hp*B
    defect = soft['deficit']+beta*R*R*o['mean3']
    ct = z*(2+z)/(1+z)**2
    kt = kb*ct+hp/G*defect
    kl_local = kb*z*(3+3*z+z*z)/(1+z)**3-hpp*B+hp*hp*(soft['susceptibility_deficit']+beta*o['susceptibility_deficit_fixed_i'])
    square = hp*hp*beta*o['square_correction'] if occupied and phase else 0.
    kl = kl_local-square
    fp = -hp*beta*R*R*o['omega']*o['b_i']/o['eii'] if occupied and phase else 0.
    J = beta*R**4*(o['omega']**2/o['eii']+3*o['i']*o['omega']) if occupied and phase else 0.
    E = soft['E']+beta*R**4*o['epsilon']
    Pi = soft['Pi']+beta*R**4*o['pressure']
    return dict(F=F, D_normalized=G*ct+hp*defect/kb, D_over_G=kt/kb,
        K_transverse=kt, K_longitudinal=kl, K_longitudinal_same_local_fixed_I=kl_local,
        longitudinal_phase_square=square, F_Phi=fp, J_static=J,
        E=E, Pi=Pi, E_plus_3Pi=E+3*Pi,
        hard_E=beta*R**4*o['epsilon'], hard_Pi=beta*R**4*o['pressure'],
        hard_excitation_above_local_min=beta*R**4*o['epsilon_exc'],
        hard_absolute_minimum=beta*R**4*o['epsilon_min'],
        h=h, h_prime=hp, h_second=hpp, B=B, soft=soft)


def run(selected, inherited):
    started = time.perf_counter(); counts = {}; maxima = {}; failures = []; rows = []; baselines = []
    def check(name, a, b, scale=None, tolerance=None):
        scale = max(abs(a), abs(b), 1e-300) if scale is None else max(abs(scale), 1e-300)
        error = abs(a-b)/scale
        tol = CONFIG['arithmetic_tolerance'] if tolerance is None else tolerance
        counts[name] = counts.get(name, 0)+1; maxima[name] = max(maxima.get(name, 0), error)
        if not math.isfinite(error) or error > tol:
            failures.append(dict(check=name, error=error, tolerance=tol, row=len(rows)))
    def controls(o):
        check('center_cubic', o['c']*(1+o['r']**2+o['c']**2), o['eta'], max(abs(o['eta']), 1e-300))
        scale = o['epsilon_exc']+abs(o['epsilon_min'])
        check('energy_turning_points', o['epsilon_exc'], o['other_turning_exc'], scale)
        check('absolute_energy', o['epsilon'], o['kinetic']+o['mean2']/2+o['mean4']/4-o['eta']*o['b'], scale)
        check('action_energy_pressure', o['i']*o['omega'], o['epsilon']+o['pressure'], scale)
        check('action_kinetic', o['i']*o['omega'], 2*o['kinetic'], scale)
        check('virial', 2*o['kinetic'], o['mean2']+o['mean4']-o['eta']*o['b'], scale)
        check('mean_equation', o['b'], o['direct_mean'], max(abs(o['eta']), abs(o['b']), 1e-300))
        if o['r']:
            check('direct_action_derivative', o['i_r'], o['i_r_direct'])
            check('maxwell', o['b_i'], o['maxwell_b_i'], max(abs(o['b_i']), abs(o['eta']), 1e-300))
            check('phase_chain_rule', o['susceptibility_deficit_fixed_i']-o['square_correction'], o['phase_deficit_other'], max(abs(o['susceptibility_deficit_fixed_i']), abs(o['square_correction']), 1e-300))
            lower = (1-12*o['eta']**2)/((2+6*o['eta']**2+2*abs(o['eta'])+2*o['r']**2)*(1+o['r']**2+3*o['eta']**2))
            check('certified_positive_eii', min(o['eii']-lower, 0.), 0., max(abs(o['eii']), abs(lower)))
    quadratures = {'GL128':rule(128), 'GL64':rule(64), 'Simpson1024':rule(None)}
    for r, eta in [(0.,0.), (.2,0.), (.2,.03), (.2,-.03)]:
        o = orbit(r,eta,quadratures['GL128']); controls(o)
        reflected = orbit(r,-eta,quadratures['GL128'])
        for key in ('i','epsilon','pressure','omega_excess','eii','susceptibility_deficit_fixed_i'):
            check('synthetic_even_'+key, o[key], reflected[key], max(abs(o[key]),1e-300))
        for key in ('b','b_i','i_eta'):
            check('synthetic_odd_'+key, o[key], -reflected[key], max(abs(o[key]),abs(eta),1e-300))
    empty_status, empty = phase_orbit(0., .03, .02, quadratures['GL128'])
    check('synthetic_empty_status', int(empty_status=='EMPTY'), 1)
    check('empty_pressure', empty['pressure'], -empty['epsilon'])
    beta = CONFIG['beta']; quadtol = CONFIG['quadrature_tolerance']
    for src in selected:
        si, ri, R = src['spectrum_index'], src['reference'], src['R']
        spec = inherited['spectra'][si]['spectrum']; kb = math.fsum(spec['weights'])+beta
        ib = src['I']/R**3; energy = src['E']/beta
        b2 = 4*energy/(R*R+math.sqrt(R**4+4*energy)); rb = math.sqrt(b2)/R
        baseline = orbit(rb,0.,quadratures['GL128']); controls(baseline)
        for key, observed, expected in [('action',baseline['i']*R**3,src['I']),
            ('omega',baseline['omega']*R,src['omega']),('eII',baseline['eii']/R**2,src['eII']),
            ('pressure',baseline['pressure']*beta*R**4,src['pressure'])]:
            check('saved_origin_'+key, observed, expected, tolerance=quadtol)
        check('saved_origin_K0', beta*baseline['susceptibility_deficit_fixed_i'], src['K0'], tolerance=quadtol)
        baseJ = beta*R**4*(baseline['omega']**2/baseline['eii']+3*baseline['i']*baseline['omega'])
        check('saved_origin_J', baseJ, src['J_static'], tolerance=quadtol)
        baselines.append(dict(source_row_index=src['source_row_index'], spectrum_index=si, reference=ri, R=R,
            stable_omega_excess=baseline['omega_excess'], old_rounded_excess=src['omega']/R-1,
            all_field_certificate_margin=1-12*(src['S']/R**2)**2))
        for physical_g in CONFIG['physical_g_m_s2']:
            G = physical_g/src['gstar']; h = G/math.sqrt(1+(G/src['S'])**2); eta = h/R**2
            soft = soft_ground(spec,h)
            check('soft_cubic', soft['maximum_cubic_relative'],0.,1.)
            fixed = {name:fixed_action_orbit(ib,eta,q) for name,q in quadratures.items()}
            for o in fixed.values():
                controls(o); check('fixed_Ib_target',o['i'],ib)
            fixed_readout = response(fixed['GL128'],soft,G,src['S'],R,kb,True,phase=False)
            for Phi in CONFIG['log_lapse']:
                target = baseline['omega_excess']*math.exp(-Phi)+math.expm1(-Phi)
                label = dict(source_row_index=src['source_row_index'], spectrum_index=si, reference=ri, R=R,
                    physical_g_m_s2=physical_g, G=G, Phi=Phi, gstar_m_s2=src['gstar'], S=src['S'],
                    Kb=kb, DeltaU=src['DeltaU'], cosmic_I=src['I'], cosmic_E=src['E'],
                    cosmic_static_length_pc=src['static_length_pc'], target_omega_excess=target,
                    eta=eta, all_field_certificate_margin=1-12*(src['S']/R**2)**2)
                try:
                    solved = {name:phase_orbit(target,eta,ib,q) for name,q in quadratures.items()}
                    status, o = solved['GL128']
                    if o is None:
                        rows.append(dict(**label, branch_status=status, response=None)); continue
                    readout = response(o,soft,G,src['S'],R,kb,status=='OCCUPIED')
                    controls(o)
                    if status == 'OCCUPIED':
                        check('phase_frequency_target',o['omega_excess'],target)
                        ihg = readout['h_prime']*R*o['b_i']/o['eii']
                        omega = R*o['omega']; I = R**3*o['i']; eii = o['eii']/R**2; BI = o['b_i']/R
                        tg = 2*readout['h_prime']*soft['B'] + beta*((omega+3*I*eii)*ihg+(2*R*R*o['b']-3*I*BI)*readout['h_prime'])
                        check('envelope_source_identity',tg,2*readout['F']-readout['F_Phi'],max(abs(tg),abs(readout['F']),abs(readout['F_Phi']),1e-300))
                    else:
                        check('empty_complementarity',max(target-o['omega_excess'],0.),0.,max(target,o['omega_excess'],1e-300))
                        check('empty_no_occupied_J',readout['J_static'],0.,1.)
                    for name,(other_status,other) in solved.items():
                        if name == 'GL128': continue
                        check(name+'_branch',int(other_status==status),1)
                        if other is None: continue
                        controls(other)
                        for key in ('i','omega_excess','eii','b_i','susceptibility_deficit_fixed_i','pressure','epsilon_exc'):
                            scale = max(abs(o[key]),abs(other[key]),1e-300)
                            check(name+'_'+key,other[key],o[key],scale,tolerance=quadtol)
                        alt = response(other,soft,G,src['S'],R,kb,status=='OCCUPIED')
                        for key in ('K_transverse','K_longitudinal','F_Phi','J_static','D_over_G'):
                            check(name+'_'+key,alt[key],readout[key],max(abs(alt[key]),abs(readout[key]),1e-300),tolerance=quadtol)
                        for key in ('i','eii','pressure','susceptibility_deficit_fixed_i'):
                            check('fixed_'+name+'_'+key,fixed[name][key],fixed['GL128'][key],tolerance=quadtol)
                    check('same_local_square',readout['K_longitudinal_same_local_fixed_I']-readout['K_longitudinal'],readout['longitudinal_phase_square'],max(abs(readout['K_longitudinal']),abs(readout['longitudinal_phase_square']),1e-300))
                    lengths = {}
                    for axis,key in [('transverse','K_transverse'),('longitudinal','K_longitudinal')]:
                        lengths[axis+'_pc'] = CONFIG['c_m_s']**2/src['gstar']*math.sqrt(readout[key]/readout['J_static'])/CONFIG['parsec_m'] if readout[key]>0 and readout['J_static']>0 else None
                    rows.append(dict(**label,branch_status=status,hard=o,hard_I=R**3*o['i'],hard_I_over_cosmic_I=o['i']/ib,
                        response=readout,local_lengths=lengths,
                        elliptic_local=readout['K_transverse']>0 and readout['K_longitudinal']>0,
                        same_g_fixed_cosmic_I=dict(hard=fixed['GL128'],response=fixed_readout),
                        signed_D_over_G_difference_from_fixed_Ib=readout['D_over_G']-fixed_readout['D_over_G']))
                except (RuntimeError, FloatingPointError, ZeroDivisionError, OverflowError) as error:
                    failures.append(dict(check='branch_numerical_failure',row=len(rows),message=str(error)))
                    rows.append(dict(**label,branch_status='NUMERICAL_BRANCH_FAILURE',response=None,error=str(error)))
    check('row_census',len(rows),CONFIG['expected_rows'])
    expected = {(s,r,g,G,P) for s in range(4) for r in range(18) for g in CONFIG['selected_R'] for G in CONFIG['physical_g_m_s2'] for P in CONFIG['log_lapse']}
    actual = {(r['spectrum_index'],r['reference'],r['R'],r['physical_g_m_s2'],r['Phi']) for r in rows}
    check('label_census',int(actual==expected),1)
    branch_counts = {name:sum(r['branch_status']==name for r in rows) for name in sorted({r['branch_status'] for r in rows})}
    summaries = []
    for R in CONFIG['selected_R']:
        for G in CONFIG['physical_g_m_s2']:
            for Phi in CONFIG['log_lapse']:
                subset = [r for r in rows if r['R']==R and r['physical_g_m_s2']==G and r['Phi']==Phi and r['response'] is not None]
                keys = ('D_over_G','K_transverse','K_longitudinal','F_Phi','J_static','E','Pi')
                summaries.append(dict(R=R,physical_g_m_s2=G,Phi=Phi,rows=len(subset),
                    ranges={key:[min(r['response'][key] for r in subset),max(r['response'][key] for r in subset)] for key in keys} if subset else {},
                    hard_I_over_cosmic_I=[min(r['hard_I_over_cosmic_I'] for r in subset),max(r['hard_I_over_cosmic_I'] for r in subset)] if subset else None,
                    elliptic_count=sum(r['elliptic_local'] for r in subset)))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    return dict(status='FAILED_NUMERICAL_CONTROLS' if failures else ('COMPLETE_WITH_UNCERTIFIED_BRANCHES' if branch_counts.get('UNCERTIFIED_BRANCH') else 'COMPLETE'),
        configuration=CONFIG,counts=counts,maxima=maxima,failures=failures,branch_counts=branch_counts,
        baselines=baselines,rows=rows,summaries=summaries,seconds=time.perf_counter()-started,
        peak_self_rss_bytes=int(peak),scope='Exploratory exact scalar common-phase local constitutive response with unchanged soft ground modes, finite-gap calibration and absolute DeltaU. No spatial boundary-value solution, chosen hard density profile, galaxy fit, state-selection proof, native identification or stability certification.')


def main():
    selected,inherited,snapshot = inputs()
    if sys.argv[1:] == ['freeze']:
        print(encode(snapshot).decode()); return
    if sys.argv[1:] != ['run']:
        raise RuntimeError('Use freeze or run')
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze differs')
    payload = run(selected,inherited)
    raw = encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload))
    transport = dict(encoding='zlib_base64_canonical_json',raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest(),
        data=base64.b64encode(zlib.compress(raw,9)).decode(),summary=dict(status=payload['status'],rows=len(payload['rows']),
        checks=sum(payload['counts'].values()),failures=len(payload['failures']),seconds=payload['seconds'],
        peak_self_rss_bytes=payload['peak_self_rss_bytes'],branch_counts=payload['branch_counts']))
    print(encode(transport).decode())
    return 0 if not payload['failures'] else 2


if __name__ == '__main__':
    sys.exit(main())
