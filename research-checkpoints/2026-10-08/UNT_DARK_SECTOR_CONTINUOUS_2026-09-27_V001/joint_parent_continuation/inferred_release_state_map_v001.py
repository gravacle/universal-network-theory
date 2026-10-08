"""Inert all-inferred-state release map; saved arithmetic, stdout only."""
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE/'INFERRED_RELEASE_STATE_MAP_V001_FROZEN.json'
CONFIG = dict(beta=.005, a_kpc=3.2, parsec_m=3.085677581491367e16,
    c_m_s=299792458., G_m3_kg_s2=6.67430e-11, thickness_over_a=[1/8,1/16],
    arithmetic_tolerance=2e-11, expected_states=1340, expected_finite=1180,
    expected_dust_limits=160, expected_points=67, expected_maps=2680,
    output_target_bytes=1048576)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files, seen = {}, set()
    def add(path, expected=None):
        path = path.resolve(strict=True)
        path.relative_to(ROOT)
        digest = sha(path)
        if expected is not None and digest != expected:
            raise RuntimeError('Changed input: '+str(path))
        files[str(path.relative_to(ROOT))] = digest
        return path
    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, digest in json.loads(path.read_text())['files'].items():
            raw = Path(name)
            options = [raw] if raw.is_absolute() else [ROOT/raw, path.parent/raw]
            matches = {p.resolve() for p in options if p.is_file() and p.resolve().is_relative_to(ROOT)}
            if len(matches) != 1:
                raise RuntimeError('Missing/ambiguous ancestor: '+name)
            member = add(matches.pop(), digest)
            if member.name.endswith('_FROZEN.json'):
                manifest(member)
    def packet(stem, digest, frozen_digest=None):
        wrapper = json.loads(add(HERE/(stem+'_RESULTS.json'), digest).read_text())
        frozen = add(HERE/(stem+'_FROZEN.json'), frozen_digest)
        manifest(frozen)
        if wrapper['freeze_sha256'] != sha(frozen):
            raise RuntimeError('Changed freeze identity')
        payload = wrapper['payload']
        if wrapper['payload_sha256'] != hashlib.sha256(encode(payload)).hexdigest():
            raise RuntimeError('Changed payload identity')
        return payload
    inverse = packet('BBN_SHARED_INVERSE_V001',
        'e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0')
    release = packet('SMOOTH_DISK_RELEASE_CERTIFICATE_V001',
        '773a3b57065e9c4fb6894064b6402e31f761dfe1de8beeb0754701c29ef24a04',
        '51ba8aa74282b37ffa252a42798d095bae2f194964bfaf7cc34cbe844a1d8d1a')
    if (inverse['status'] != 'COMPLETE_CONDITIONAL_PROXY_INVERSE' or inverse['failures']
        or inverse['inherited_table_controls']['failures']):
        raise RuntimeError('Unqualified inverse source')
    if release['status'] != 'COMPLETE' or release['failures']:
        raise RuntimeError('Unqualified release source')
    for key in ('beta','a_kpc','parsec_m','c_m_s','G_m3_kg_s2','thickness_over_a','arithmetic_tolerance'):
        if CONFIG[key] != release['configuration'][key]:
            raise RuntimeError('Changed release convention: '+key)
    for name in [Path(__file__).name, 'INFERRED_RELEASE_STATE_MAP_PROTOCOL_V001.md',
                 'PHYSICAL_TIME_AND_RELEASE_STATE_MAP_V001.md']:
        add(HERE/name)
    for name, digest in [
        ('SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md','48dbfeeefc012af2f4d663e1ec37732f9e007efcbbe8fd66bfaced64a4a9a07b'),
        ('NATIVE_SOURCE_BRIDGE_DECISION.md','c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a'),
        ('NATIVE_PHASE_CLOCK_RESULT_V001.md','03804dfcf99cdb8f05f2302f9f566dc033412a3d3a21748201169b48921b41ac'),
        ('NATIVE_FINITE_MEMORY_TRANSPORT_REALIZATION_V001.md','5ffeccf4fe4041348a3e3b74571be43f607cb89908bc65940d68deb10781e64c'),
        ('FINITE_GAP_BBN_DISCRIMINATOR_DESIGN_V001.md','4af69d5eaa08090c9fa8e422f408050de57a8945eec854a8043d24db8edc2ac6')]:
        add(HERE/name, digest)
    states = inverse['state_rows']
    points = inverse['table_points']
    if len(states) != CONFIG['expected_states'] or len(points) != CONFIG['expected_points']:
        raise RuntimeError('Changed inverse census')
    if (sum(s['status']=='FINITE_HARD_STATE' for s in states) != CONFIG['expected_finite']
        or sum(s['status']=='INFINITE_GAP_STANDARD_LIMIT' for s in states) != CONFIG['expected_dust_limits']):
        raise RuntimeError('Changed finite/limit census')
    expected = {(p['point_id'],b['background_id'],si)
                for p in points for b in inverse['backgrounds'] for si in range(4)}
    actual = {(s['point_id'],s['background_id'],s['spectrum_index']) for s in states}
    if actual != expected or len(actual) != len(states):
        raise RuntimeError('Incomplete inverse associations')
    return inverse, release, dict(configuration=CONFIG, files=files)


def run(inverse, release):
    start = time.perf_counter()
    counts, worst, failures = {}, {}, []
    def check(name, x, y, scale=None):
        denom = max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
        error = abs(x-y)/denom
        counts[name] = counts.get(name,0)+1
        worst[name] = max(worst.get(name,0.),error)
        if not math.isfinite(error) or error > CONFIG['arithmetic_tolerance']:
            failures.append(dict(check=name,error=error,x=x,y=y))
    c, G = CONFIG['c_m_s'], CONFIG['G_m3_kg_s2']
    a = CONFIG['a_kpc']*1000*CONFIG['parsec_m']
    constants = {(q['background_id'],q['spectrum_index']):q for q in inverse['constants']}
    backgrounds = {q['background_id']:q for q in inverse['backgrounds']}
    spectrum_constants = {}
    for co in inverse['constants']:
        si = co['spectrum_index']
        if si not in spectrum_constants:
            spectrum_constants[si] = co
        for key in ('gstar','Kb'):
            check('same_spectrum_'+key,co[key],spectrum_constants[si][key])

    # Geometry is never reevaluated: use saved d, grad(d), Delta(d), and f.
    bases, basis_lookup = [], {}
    for si in sorted(spectrum_constants):
        gs = spectrum_constants[si]['gstar']
        eps = gs*a/c**2
        for oldg in release['geometries']:
            b = oldg['b_over_a']
            U = eps/(2*(1+b))
            dmax = oldg['density_max']
            ell = (1/(2*math.pi*dmax))**(1/3)
            Bgrad = 3*math.pi*eps*dmax*ell  # a*|grad psi| upper bound.
            rows = []
            for p in oldg['points']:
                d, grad, lap = p['density'],p['density_gradient'],p['density_laplacian']
                u = -eps*p['potential']/2
                Alo,Ahi = 4*math.pi*d/(1+u)**6,4*math.pi*d
                eg = 4*math.pi*(8*U*math.hypot(*grad)+6*d*Bgrad)
                el = 4*math.pi*(10*U*abs(lap)+10*Bgrad*math.hypot(*grad)
                               +30*d*Bgrad**2+12*math.pi*eps*d*d)
                # Values multiply Xi for velocity/current in dynamical units.
                v = [-4*math.pi*x/6 for x in grad]
                cur = 4*math.pi*lap/24
                rows.append([p['x'],p['z'],Alo/2,Ahi/2,v[0],v[1],eg/6,
                             cur,cur-el/24,cur+el/24])
            basis_lookup[(si,b)] = len(bases)
            bases.append(dict(spectrum_index=si,b_over_a=b,gstar=gs,epsilon=eps,
                compactness=U,contraction_qualified=U<1,
                dimensionless_metric_gradient_bound=Bgrad,points=rows))

    # Reconstruct all64 already qualified old physical jets as an independent
    # normalization check. These controls do not become inferred-state inputs.
    for old in release['cases']:
        si = release['configuration']['spectrum_index']
        b = old['b_m']/old['a_m']
        basis = bases[basis_lookup[(si,b)]]
        td = math.sqrt(a/old['source_state']['gstar'])
        vd = a/td
        Xi = old['source_state']['cI2']/basis['epsilon']
        for p, q in zip(old['points'],basis['points']):
            for i in range(2):
                check('saved_focusing_jet',q[2+i]/td**2,p['fractional_density_tau2_interval'][i])
                check('saved_velocity_jet',q[4+i]*Xi*vd/td**3,
                      p['orthonormal_velocity_tau3_m_s4_leading'][i])
                check('saved_current_interval',q[8+i]*Xi/td**4,
                      p['canonical_current_tau4_s4_interval'][i],
                      max(abs(p['canonical_current_tau4_s4_leading']),1e-300))
            check('saved_velocity_bound',q[6]*Xi*vd/td**3,
                  p['orthonormal_velocity_tau3_norm_error_m_s4'])
            check('saved_current_jet',q[7]*Xi/td**4,p['canonical_current_tau4_s4_leading'])

    states, mappings = [], []
    for index, src in enumerate(inverse['state_rows']):
        co = constants[(src['background_id'],src['spectrum_index'])]
        bg = backgrounds[src['background_id']]
        finite = src['status']=='FINITE_HARD_STATE'
        ci,w,pressure = (src['cI2'],src['w'],src['pressure']) if finite else (0.,0.,0.)
        du = src['DeltaU'] if finite else src['DeltaU_target']
        gs,kb,E = co['gstar'],co['Kb'],src['E']
        stress = gs*gs/(4*math.pi*G*kb)
        rho = stress*E/c**2
        pr = stress*pressure
        vac = stress*du/c**2
        eps = gs*a/c**2
        Xi = ci/eps
        td = math.sqrt(a/gs)
        vd = a/td
        check('shared_excitation',rho,3*bg['H0_s_inverse']**2*src['Omega_exc']/(8*math.pi*G))
        check('shared_vacuum',vac,3*bg['H0_s_inverse']**2*bg['Omega_Lambda']/(8*math.pi*G))
        check('pressure_normalization',pr,rho*c*c*w)
        check('Xi_time_identity',Xi,(c*math.sqrt(ci)*td/a)**2 if ci else 0.)
        if finite:
            check('saved_cI2',ci,src['I']*src['eII']/src['omega'])
            check('same_state_enthalpy',CONFIG['beta']*src['I']*src['omega'],E+pressure)
            omega_over_H_times_tau = src['omega']/bg['H0_s_inverse']
            omega_tdyn_times_tau = src['omega']*td
        else:
            omega_over_H_times_tau = None
            omega_tdyn_times_tau = None
            check('limit_is_positive_energy',float(E>0 and src['Delta']==0 and src['R'] is None),1.)
        # Null means infinite sound-crossing ratio / undefined native frequency,
        # never zero time or a numerically huge replacement for infinity.
        states.append([index,src['point_id'],src['background_id'],src['spectrum_index'],
            'FINITE' if finite else 'EXACT_MACRO_DUST_LIMIT',src.get('R'),
            ci,w,Xi,1/math.sqrt(Xi) if Xi else None,td,rho,pr,vac,
            omega_over_H_times_tau,omega_tdyn_times_tau])
        for b in CONFIG['thickness_over_a']:
            bi = basis_lookup[(src['spectrum_index'],b)]
            # Multiply basis q2, velocity and current coefficients to recover
            # SI jets. Density scale multiplies BOTH q2 interval endpoints.
            dscale = rho*(1+w)/td**2
            vscale = Xi*vd/td**3
            pscale = Xi/td**4
            pressure_scale = c*c*ci*dscale
            check('velocity_scale_identity',vscale,c*c*ci*gs/a**2)
            check('current_scale_identity',pscale,c*c*ci*gs/a**3)
            mappings.append([index,bi,dscale,pressure_scale,vscale,pscale])
    check('state_census',len(states),CONFIG['expected_states'],1.)
    check('mapping_census',len(mappings),CONFIG['expected_maps'],1.)
    check('finite_census',sum(r[4]=='FINITE' for r in states),CONFIG['expected_finite'],1.)
    check('dust_census',sum(r[4]=='EXACT_MACRO_DUST_LIMIT' for r in states),CONFIG['expected_dust_limits'],1.)
    points = [{key:p[key] for key in ('point_id','omega_b','Delta','roles','coarse_node')}
              | {'local_interpolation_qualified':p['prediction']['local_numerical_rectangle']}
              for p in inverse['table_points']]
    # One complete ranking; ties resolved by existing source index, no winner selected.
    ranking = sorted(range(len(states)),key=lambda i:(states[i][8],i))
    summary = dict(Xi_range=[min(r[8] for r in states),max(r[8] for r in states)],
                   density_range_kg_m3=[min(r[11] for r in states),max(r[11] for r in states)],
                   complete_increasing_Xi_source_indices=ranking)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS',configuration=CONFIG,
        checks=counts,worst_scaled_errors=worst,failures=failures,
        point_metadata=points,backgrounds=inverse['backgrounds'],
        soft_spectra_metadata=inverse['soft_spectra_metadata'],constants=inverse['constants'],
        basis_columns=['x','z','q_tau_dyn2_lower','q_tau_dyn2_upper',
            'velocity_R_per_Xi','velocity_z_per_Xi','velocity_norm_error_per_Xi',
            'canonical_current_per_Xi','canonical_current_lower_per_Xi','canonical_current_upper_per_Xi'],
        geometry_bases=bases,
        state_columns=['source_index','point_id','background_id','spectrum_index','status','R',
            'cI2','w','Xi','t_sound_over_t_dyn_or_null_infinite','t_dyn_seconds',
            'rho_H_kg_m3','p_H_Pa','rho_vac_kg_m3',
            'omega_phys_over_H_times_tau_seconds_or_null','omega_phys_t_dyn_times_tau_seconds_or_null'],
        states=states,
        mapping_columns=['source_index','basis_index','density_tau2_scale_kg_m3_s2',
            'pressure_tau2_scale_Pa_s2','velocity_tau3_scale_m_s4','current_tau4_scale_s4'],
        mappings=mappings,summary=summary,
        scope='Exact adopted-fluid initial jets only. Complete inherited proxy inverse, not exact scalar BBN validation or a finite-age galaxy result. No microscopic tau selected.',
        reconstruction='Multiply basis q2 bounds by density/pressure scales; multiply basis velocity entries and norm bound by velocity scale; multiply basis current entries by current scale. Fractional q2 SI uses basis/tdyn^2. In dynamical units multiply velocity/current basis by Xi.',
        elapsed_seconds=time.perf_counter()-start,peak_bytes=peak)


def main():
    if sys.argv[1:] not in (['freeze'],['run']):
        raise RuntimeError('Use freeze or run; stdout only')
    inverse,release,snapshot = inputs()
    if sys.argv[1:] == ['freeze']:
        print(encode(snapshot).decode())
        return
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze differs')
    payload = run(inverse,release)
    print(encode(dict(payload=payload,payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
        freeze_sha256=sha(FREEZE),within_output_target=len(encode(payload))<=CONFIG['output_target_bytes'])).decode())


if __name__ == '__main__':
    main()
