"""Independent saved-data audit. No model imports, quadrature, or propagation."""
import hashlib
import itertools
import json
from decimal import Decimal as D, getcontext
from pathlib import Path

getcontext().prec = 50
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def read(name):
    return json.loads((HERE / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def dec(x):
    return D(str(x))


checks = 0
maxima = {}


def exact(condition, name):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(name)


def near(name, a, b, scale=1, tolerance='2e-12'):
    global checks
    checks += 1
    error = abs(dec(a)-dec(b))/abs(dec(scale))
    maxima[name] = max(maxima.get(name, D(0)), error)
    if not error.is_finite() or error > D(tolerance):
        raise AssertionError((name, str(error)))


def below(name, a, b, scale=1, tolerance='2e-12'):
    near(name, max(dec(a)-dec(b), D(0)), 0, scale, tolerance)


freeze_name = 'PREPARED_SUSCEPTIBILITY_V001_FROZEN.json'
result_name = 'PREPARED_SUSCEPTIBILITY_V001_RESULTS.json'
freeze, result = read(freeze_name), read(result_name)
for name, expected in freeze['files'].items():
    path = (ROOT / name).resolve(strict=True)
    exact(path.is_relative_to(ROOT), 'in-scope input')
    exact(digest(path) == expected, 'input hash: '+name)
exact(result['freeze_sha256'] == digest(HERE/freeze_name), 'freeze digest')
exact(result['payload_sha256'] == hashlib.sha256(canonical(result['payload'])).hexdigest(), 'payload digest')
exact(result['status'] == 'COMPLETE', 'completed result')
payload = result['payload']
exact(not payload['failures'], 'no reported failures')
exact(payload['config'] == freeze['config'], 'configuration identity')
exact(sum(payload['check_counts'].values()) == 42491, 'original check census')

ancestor_names = ['PREPARED_ACTION_RETURN_V001_RESULTS.json',
                  'COMMON_HISTORY_MECHANISM_V001_RESULTS.json',
                  'COMMON_HISTORY_PHASE_MEAN_V003_RESULTS.json']
parents = {}
for name in ancestor_names:
    item = read(name)
    oldfreeze = name.replace('_RESULTS.json', '_FROZEN.json')
    exact(item['freeze_sha256'] == digest(HERE/oldfreeze), 'ancestor freeze')
    exact(item['payload_sha256'] == hashlib.sha256(canonical(item['payload'])).hexdigest(), 'ancestor payload')
    oldchecks = item['payload']['checks']
    passed = all(oldchecks.values()) if isinstance(oldchecks, dict) else all(x['passed'] for x in oldchecks)
    exact(passed, 'ancestor checks')
    parents[name] = item['payload']

oldrows = parents[ancestor_names[0]]['rows']
cases = parents[ancestor_names[1]]['cases']
states = {(x['gap'], x['order'], x['dt'], x['duration']): x for x in cases}
rows = payload['rows']
expected = set(itertools.product([.001,.002], [8,16], [.0025,.01,.04], [(64,.01),(128,.01),(128,.005)]))
actual = [(r['gap'],r['duration'],r['g'],(r['mode_order'],r['dt'])) for r in rows]
exact(len(actual) == 36 and set(actual) == expected, '36-state census')
exact(sum(r['mode_order'] for r in rows) == 3840, '3840-mode census')

for index, (row, old) in enumerate(zip(rows, oldrows)):
    exact(row['row_index'] == index, 'row index')
    for name in ('gap','duration','g','mode_order','dt'):
        exact(row[name] == old[name], 'unchanged preparation identity')
    case = states[(old['gap'],old['mode_order'],old['dt'],old['duration'])]
    modal = old['mode_data']
    arrays = [case['delta'],case['weights'],modal['zero_source_energy'],
              modal['zero_source_pressure'],modal['quartic_mean'],
              modal['zero_source_turning_amplitude'],row['modal_q'],row['modal_chi']]
    exact(all(len(a) == old['mode_order'] for a in arrays), 'modal lengths')
    E = P = I0 = S4 = defect = D(0)
    for values in zip(*arrays):
        d,w,e,p,v4,b,q,chi = map(dec,values)
        k = d*d
        energy_turn = k*b*b/2+b**4/4
        mean2 = (e-3*v4)/k
        susceptibility = (k+mean2)/(k+b*b)**2
        alternate_q = 1-k*susceptibility
        near('turning energy',energy_turn,e,e)
        near('pressure fourth moment',p,v4,e,'2e-8')
        near('q reconstructed from fourth moment',q,alternate_q)
        near('scaled susceptibility reconstructed',k*chi,k*susceptibility)
        near('exact contact sum',q+k*chi,1)
        near('q energy-pressure identity',q,3*(e+p)/(k*k+4*e))
        below('q nonnegative',0,q)
        below('q at most one',q,1)
        z = b*b/k
        below('lower turning bound',z/(1+z),q)
        below('upper turning bound',q,z*(2+z)/(1+z)**2)
        below('modal pressure nonnegative',0,p,e,'2e-8')
        below('modal pressure upper',p,e/3,e,'2e-8')
        below('Jensen moment bound',(e-3*p)**2,4*k*k*p,e*e,'2e-8')
        below('energy-defect bound',q*e,12*p,e,'2e-8')
        E += w*e
        P += w*v4
        I0 += w
        S4 += w*d**4
        defect += w*alternate_q
    mu = defect/I0
    pressure_floor = E*E/((S4+3*E).sqrt()+S4.sqrt())**2
    cold_floor = max(D(0),3*(E-15*P)/I0)
    for label,value,scale in [('I0',I0,I0),('S4',S4,S4),('E',E,E),('P',P,E),
                              ('mu_linear',mu,1),('P_over_E',P/E,1),
                              ('pressure_lower_bound',pressure_floor,E),
                              ('conservative_cold_mu_lower_bound',cold_floor,1)]:
        near('aggregate '+label,value,row[label],scale,'2e-8' if label=='P' else '2e-12')
    below('aggregate pressure bound',pressure_floor,P,E,'2e-8')
    below('aggregate contact bound',cold_floor,mu,1,'2e-8')

comparisons = payload['resolution_comparisons']
expected_pairs = set()
index = {(r['gap'],r['duration'],r['g'],r['mode_order'],r['dt']):r['row_index'] for r in rows}
for gap,duration,g in itertools.product([.001,.002],[8,16],[.0025,.01,.04]):
    expected_pairs.add((index[(gap,duration,g,64,.01)],index[(gap,duration,g,128,.01)],'spectral_order'))
    expected_pairs.add((index[(gap,duration,g,128,.01)],index[(gap,duration,g,128,.005)],'old_time_step'))
exact(len(comparisons)==24 and {(d['left_row'],d['right_row'],d['label']) for d in comparisons}==expected_pairs, 'all24 comparisons')
resolution_extrema = {}
for comp in comparisons:
    a,b = rows[comp['left_row']],rows[comp['right_row']]
    for key in ('E','P','mu_linear'):
        diff = b[key]-a[key]
        exact(diff == comp['signed_right_minus_left'][key], 'saved signed resolution delta')
        exact(diff/b[key] == comp['relative_to_right'][key], 'saved relative resolution delta')
        name = comp['label']+':'+key
        resolution_extrema[name] = max(resolution_extrema.get(name,0.),abs(diff/b[key]))

main = [{k:r[k] for k in ('row_index','gap','duration','g','E','P_over_E','mu_linear',
                         'conservative_cold_mu_lower_bound')} for r in rows
        if r['mode_order']==128 and r['dt']==.005]
summary = dict(status='PASS', method='50-digit Decimal saved-data arithmetic; no propagation or scientific imports',
    script_sha256=digest(Path(__file__)), original_result_sha256=digest(HERE/result_name),
    original_freeze_sha256=digest(HERE/freeze_name),original_payload_sha256=result['payload_sha256'],
    authenticated_frozen_files=len(freeze['files']),original_checks=42491,audit_checks=checks,
    maxima={k:float(v) for k,v in maxima.items()},resolution_max_relative_changes=resolution_extrema,
    mu_range=[min(r['mu_linear'] for r in rows),max(r['mu_linear'] for r in rows)],
    template_row=main[0],fine_rows=main,
    runtime_seconds=result['seconds'],peak_self_rss_bytes=result['peak_self_rss_bytes'])
print(json.dumps(summary,indent=2,allow_nan=False))
