"""All existing returned actions: exact scalar response, stdout-only arithmetic."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
RETURN = HERE / 'PREPARED_ACTION_RETURN_V001_RESULTS.json'
STATES = HERE / 'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'
PHASE = HERE / 'COMMON_HISTORY_PHASE_MEAN_V003_RESULTS.json'
FREEZE = HERE / 'PREPARED_SUSCEPTIBILITY_V001_FROZEN.json'
RETURN_SHA = 'b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678'
CONFIG = dict(arithmetic_tolerance=2e-12, inherited_moment_tolerance=2e-8,
              gaps=[.001,.002], durations=[8,16], amplitudes=[.0025,.01,.04],
              resolutions=[[64,.01],[128,.01],[128,.005]],
              synthetic_k=[.25,1.], synthetic_u=[.5,1.],
              synthetic_b=[0.,.1,1.,3.], synthetic_y_fraction=[0.,.3,1.])


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        if not path.is_relative_to(WORKSPACE):
            raise RuntimeError('Input outside project: '+str(path))
        digest = sha(path)
        if expected is not None and digest != expected:
            raise RuntimeError('Source identity mismatch: '+str(path))
        files[str(path.relative_to(WORKSPACE))] = digest
        return path

    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, digest in json.loads(path.read_text())['files'].items():
            child = add(path.parent / name, digest)
            if child.name.endswith('_FROZEN.json'):
                manifest(child)

    def wrapper(path):
        path = add(path)
        freeze = path.with_name(path.name.replace('_RESULTS.json','_FROZEN.json'))
        manifest(freeze)
        value = json.loads(path.read_text())
        if (value['freeze_sha256'] != sha(freeze)
                or value['payload_sha256'] != hashlib.sha256(encoded(value['payload'])).hexdigest()):
            raise RuntimeError('Result wrapper mismatch: '+str(path))
        checks = value['payload']['checks']
        qualified = all(checks.values()) if isinstance(checks,dict) else all(c['passed'] for c in checks)
        if not qualified:
            raise RuntimeError('Unqualified input: '+str(path))
        return value['payload']

    add(RETURN, RETURN_SHA)
    returned, states = wrapper(RETURN), wrapper(STATES)
    wrapper(PHASE)
    for path in (Path(__file__), HERE / 'PREPARED_SUSCEPTIBILITY_PROTOCOL_V001.md',
                 HERE / 'FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md'):
        add(path)
    expected = {(gap, order, dt, duration, g) for gap in CONFIG['gaps']
                for order,dt in CONFIG['resolutions'] for duration in CONFIG['durations']
                for g in CONFIG['amplitudes']}
    actual = [(r['gap'],r['mode_order'],r['dt'],r['duration'],r['g']) for r in returned['rows']]
    if len(actual) != 36 or set(actual) != expected:
        raise RuntimeError('Saved-state census mismatch')
    return returned, states, dict(config=CONFIG, files=files)


def run():
    start = time.perf_counter()
    returned, states, snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze differs')
    maxima, counts, failures = {}, {}, []

    def check(name,left,right,scale=1.,inequality=False,inherited=False,tag=''):
        tol = CONFIG['inherited_moment_tolerance'] if inherited else CONFIG['arithmetic_tolerance']
        difference = left-right
        error = (max(0.,difference) if inequality else abs(difference))/(scale or 1.)
        maxima[name] = max(maxima.get(name,0.), error)
        counts[name] = counts.get(name,0)+1
        if not math.isfinite(error) or error > tol:
            failures.append(dict(check=name, tag=tag, normalized_error=error,
                                 tolerance=tol,left=left,right=right,scale=scale))

    for k in CONFIG['synthetic_k']:
        for u in CONFIG['synthetic_u']:
            for b in CONFIG['synthetic_b']:
                e = k*b*b/2+u*b**4/4
                denom = k*k+4*u*e
                check('synthetic_turning_identity',denom,(k+u*b*b)**2,denom)
                for fraction in CONFIG['synthetic_y_fraction']:
                    y = fraction*b
                    numerator = (u*(4*e-4*k*y*y-3*u*y**4)
                                 +(k+3*u*y*y)*(k+u*y*y))
                    check('synthetic_variational_identity',numerator/denom,1.)
                if b == 0:
                    check('synthetic_ground_susceptibility',k*k/denom,1.)

    state_index = {(c['gap'],c['order'],c['dt'],c['duration']):c for c in states['cases']}
    rows = []
    for index, old in enumerate(returned['rows']):
        case = state_index[(old['gap'],old['mode_order'],old['dt'],old['duration'])]
        delta, weights = case['delta'], case['weights']
        md = old['mode_data']
        energies, pressures = md['zero_source_energy'],md['zero_source_pressure']
        quartic, amplitude = md['quartic_mean'],md['zero_source_turning_amplitude']
        if not all(len(a)==old['mode_order'] for a in (delta,weights,energies,pressures,quartic,amplitude)):
            raise RuntimeError('Modal census mismatch at row '+str(index))
        i0 = math.fsum(weights)
        s4 = math.fsum(w*d**4 for w,d in zip(weights,delta))
        check('contact_weight',i0,case['Kb'],case['Kb'],tag=str(index))
        qlist, chilist = [], []
        alt_max = 0.
        for j,(d,w,e,p,v4,b) in enumerate(zip(delta,weights,energies,pressures,quartic,amplitude)):
            tag = str(index)+':'+str(j)
            if not all(math.isfinite(x) for x in (d,w,e,p,v4,b)) or min(d,w,e) <= 0 or b < 0:
                raise RuntimeError('Invalid positive-gap/energy input '+tag)
            k = d*d
            denom = k*k+4*e
            q = 3*(e+p)/denom
            mean2 = (e-3*p)/k
            chi = (k+mean2)/denom
            alt_mean2 = (e-3*v4)/k
            chi_alt = (k+alt_mean2)/(k+b*b)**2
            check('stored_turning_energy',e,k*b*b/2+b**4/4,e,tag=tag)
            check('stored_pressure_virial',p,v4,e,inherited=True,tag=tag)
            check('stored_nonnegative_pressure',0.,p,e,True,True,tag)
            check('stored_pressure_upper',p,e/3,e,True,True,tag)
            check('q_contact_identity',q+k*chi,1.,tag=tag)
            check('q_nonnegative',0.,q,inequality=True,tag=tag)
            check('q_upper',q,1.,inequality=True,tag=tag)
            r = b*b/k
            check('q_turning_lower',r/(1+r),q,inequality=True,tag=tag)
            check('q_turning_upper',q,r*(2+r)/(1+r)**2,inequality=True,tag=tag)
            check('stored_moment_chi',k*chi,k*chi_alt,inherited=True,tag=tag)
            check('modal_energy_pressure_defect_bound',q*e,12*p,e,True,True,tag)
            alt_max = max(alt_max,abs(k*(chi-chi_alt)))
            qlist.append(q)
            chilist.append(chi)
        energy = math.fsum(w*e for w,e in zip(weights,energies))
        pressure = math.fsum(w*p for w,p in zip(weights,pressures))
        mu = math.fsum(w*q for w,q in zip(weights,qlist))/i0
        floor = energy**2/(math.sqrt(s4+3*energy)+math.sqrt(s4))**2
        lower_mu = max(0.,3*(energy-15*pressure)/i0)
        check('old_weighted_energy',energy,old['return_energy'],energy,tag=str(index))
        check('old_weighted_pressure',pressure,old['return_pressure'],energy,tag=str(index))
        check('aggregate_pressure_floor',floor,pressure,energy,True,True,str(index))
        check('aggregate_cold_mu_bound',lower_mu,mu,1.,True,True,str(index))
        rows.append(dict(row_index=index,gap=old['gap'],duration=old['duration'],g=old['g'],
            mode_order=old['mode_order'],dt=old['dt'],I0=i0,S4=s4,E=energy,P=pressure,
            P_over_E=pressure/energy,mu_linear=mu,pressure_lower_bound=floor,
            conservative_cold_mu_lower_bound=lower_mu,q_min=min(qlist),q_max=max(qlist),
            chi_min=min(chilist),chi_max=max(chilist),
            max_k_scaled_stored_moment_chi_difference=alt_max,
            modal_q=qlist,modal_chi=chilist))
    indexed = {(r['gap'],r['duration'],r['g'],r['mode_order'],r['dt']):r for r in rows}
    differences = []
    for gap in CONFIG['gaps']:
        for duration in CONFIG['durations']:
            for g in CONFIG['amplitudes']:
                for a,b,label in (([64,.01],[128,.01],'spectral_order'),
                                  ([128,.01],[128,.005],'old_time_step')):
                    left,right = indexed[(gap,duration,g,*a)],indexed[(gap,duration,g,*b)]
                    differences.append(dict(gap=gap,duration=duration,g=g,label=label,
                        left_row=left['row_index'],right_row=right['row_index'],
                        signed_right_minus_left={k:right[k]-left[k] for k in ('E','P','mu_linear')},
                        relative_to_right={k:(right[k]-left[k])/right[k] for k in ('E','P','mu_linear')}))
    check('rows',len(rows),36.)
    check('modes',sum(r['mode_order'] for r in rows),3840.)
    check('resolution_comparisons',len(differences),24.)
    payload = dict(config=CONFIG,rows=rows,resolution_comparisons=differences,
        maximum_errors=maxima,check_counts=counts,failures=failures,
        original_baseline=returned['baseline'],
        scope=('Same unchanged zero-source returned actions; exact scalar fixed-action susceptibility. '
               'No new preparation, orbit quadrature, gravity propagation, parameter fit or isotropic-vector substitution.'),
        alternative_chi='Virial second-moment reconstruction from saved quartic moment and turning amplitude; not a separately saved second moment.')
    result = dict(status='COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        freeze_sha256=sha(FREEZE),payload=payload,payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
        seconds=time.perf_counter()-start,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result,allow_nan=False))
    return 1 if failures else 0


if __name__=='__main__':
    if sys.argv[1:]==['freeze']:
        print(json.dumps(inputs()[2],indent=2,allow_nan=False))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())
