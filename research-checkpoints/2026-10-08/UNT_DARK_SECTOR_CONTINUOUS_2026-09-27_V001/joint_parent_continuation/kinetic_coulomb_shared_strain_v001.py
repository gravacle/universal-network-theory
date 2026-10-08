"""New frozen conditional strain gate; no prior worker import or fit."""
import hashlib
import json
import math
import resource
import time
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'KINETIC_COULOMB_SHARED_STRAIN_V001.md'
RESULT = HERE / 'KINETIC_COULOMB_SHARED_STRAIN_V001_RESULT.json'
REPORT = HERE / 'KINETIC_COULOMB_SHARED_STRAIN_V001_RESULT.md'
if RESULT.exists() or REPORT.exists():
    raise SystemExit('Existing output protected; inspect and recover rather than rerun.')
start = time.perf_counter()
checks = []
rows_nr = []
rows_rel = []
derivative_max = {'nr_pressure': 0.0, 'nr_bulk': 0.0,
                  'rel_pressure': 0.0, 'rel_bulk': 0.0}

def gate(name, condition, value=None):
    checks.append({'name': name, 'pass': bool(condition), 'value': value})

def nr(s, r):
    e = r + 1/s**2 - 2/s
    active = r + 3/s**2 - 4/s
    w = r + 5/(3*s**2) - 8/(3*s)
    b = 2*(5-4*s)/(9*s**2)
    pv = 2*(1-s)/(3*s**2)
    return e, active, w, b, pv

def rel(s, alpha):
    q = alpha/s
    e = math.hypot(1, q)
    e0 = math.hypot(1, alpha)
    c = alpha**2/e0
    energy = (1+q*q/(1+alpha*alpha))/(e+q*alpha/e0)
    active = 1/(e*(1+2*q*q+2*q*e)) + 2*q/(e0*(e0+alpha))
    pv = (q*q/e-c/s)/3
    bulk = (5*q*q/e-q**4/e**3-4*c/s)/9
    return energy, active, pv, bulk, e, e-c/s, e+q*q/e-2*c/s

rs = [1.01, 1.1, 1.2, 1.25, 1.28, 4/3, 2, 10, 1000]
ss = [0.8, 1, 1.1, 1.2, 1.25, 1.5, 2, 3, 10]
s = r = F(6, 5)
ex = nr(s, r)
exact_expected = [F(41,180), F(-1,20), F(73,540), F(5,162)]
for i, expected in enumerate(exact_expected):
    gate('exact_witness_'+str(i), ex[i] == expected, str(ex[i]))
gate('exact_sound_ratio', ex[3]/ex[2] == F(50,219), str(ex[3]/ex[2]))
gate('exact_background_q', ex[1]/(2*ex[0]) == F(-9,82), str(ex[1]/(2*ex[0])))
for r in rs:
    for s in ss:
        e, a, w, b, pv = nr(s, r)
        rows_nr.append({'s': s, 'r': r, 'energy': e, 'active': a,
                        'enthalpy': w, 'bulk': b, 'pv': pv,
                        'formal_fluid_causal_acceleration': a<0 and b>0 and w>0 and b<=w})
        scale = max(1, abs(e))
        gate('nr_identity', max(abs(a-e-3*pv), abs(w-e-pv),
             abs(e-(r-1+(s-1)**2/s**2)))/scale < 1e-12)
        if 1 < r < 4/3 and abs(a) > 1e-12:
            root = math.sqrt(4-3*r)
            gate('nr_acceleration_interval', (a<0)==(3/(2+root)<s<3/(2-root)))
        if r >= 4/3:
            gate('nr_large_rest_no_acceleration', a >= -1e-12)
        if abs(b) > 1e-12:
            gate('nr_bulk_sign', (b>0)==(s<1.25))

def derivative_gate(kind, energy_at_s, s, pv, bulk, scale):
    v = s**3
    for step in [1e-3, 3e-4, 1e-4]:
        dv = v*step
        ep = energy_at_s((v+dv)**(1/3))
        em = energy_at_s((v-dv)**(1/3))
        ec = energy_at_s(s)
        # Dimensionless targets are p V and K V; V0=1.
        p_fd_v = -v*(ep-em)/(2*dv)
        b_fd_v = v*v*(ep-2*ec+em)/(dv*dv)
        errp = abs(p_fd_v-pv)/scale
        errb = abs(b_fd_v-bulk)/scale
        derivative_max[kind+'_pressure'] = max(derivative_max[kind+'_pressure'], errp)
        derivative_max[kind+'_bulk'] = max(derivative_max[kind+'_bulk'], errb)
        gate(kind+'_pressure_derivative', errp < 5e-6, errp)
        gate(kind+'_bulk_derivative', errb < 5e-6, errb)

for r in [1.2, 10]:
    for s in [0.9, 1, 1.2, 2]:
        e, a, w, b, pv = nr(s, r)
        derivative_gate('nr', lambda t: nr(t,r)[0], s, pv, b, 1)

for alpha in [1e-3, 0.1, 1, 10, 1000]:
    for s in ss:
        en, a, pv, b, e, en_direct, a_direct = rel(s,alpha)
        rows_rel.append({'alpha': alpha, 's': s, 'energy': en,
                         'active': a, 'pv': pv, 'bulk': b,
                         'direct_relative_error': max(abs(en-en_direct),abs(a-a_direct))/e})
        gate('rel_positive_energy', en>0, en)
        gate('rel_positive_active', a>0, a)
        gate('rel_stable_direct', max(abs(en-en_direct), abs(a-a_direct))/e < 1e-10)
        gate('rel_active_identity', abs(a-en-3*pv)/e < 1e-10)
    gate('rel_reference_virial', abs(rel(1,alpha)[2])/math.hypot(1,alpha) < 1e-12)
for alpha in [0.1, 1, 10]:
    for s in [0.9, 1, 1.2, 2]:
        en,a,pv,b,e,_,_ = rel(s,alpha)
        derivative_gate('rel', lambda t: rel(t,alpha)[0], s, pv, b, e)

mixtures = []
for s in ss:
    populations = [rel(s,a) for a in [0.1,1,10]]
    weights = [0.25,0.5,0.25]
    en = sum(w*x[0] for w,x in zip(weights,populations))
    active = sum(w*x[1] for w,x in zip(weights,populations))
    gate('rel_mixture_positive', en>0 and active>0)
    mixtures.append({'s':s,'energy':en,'active':active})

receipt = {
    'protocol': PROTOCOL.name,
    'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
    'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'utc': datetime.now(timezone.utc).isoformat(),
    'runtime_seconds': time.perf_counter()-start,
    'max_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'checks_total':len(checks), 'checks_passed':sum(x['pass'] for x in checks),
    'failed_checks':[x for x in checks if not x['pass']],
    'derivative_max_errors':derivative_max, 'nr_rows':rows_nr,
    'rel_rows':rows_rel, 'mixtures':mixtures,
    'qualification':'Conditional arithmetic gate only. Formal NR acceleration lies outside NR rest-energy control; exact relativistic virial Coulomb continuation has strictly positive active source. No native response, donor formation, total cosmology or observational qualification.'}
with RESULT.open('x') as f:
    json.dump(receipt,f,indent=2,allow_nan=False)
    f.write('\n')
report = f'''# Shared kinetic/Coulomb scalar gate result V001

Checks: {receipt['checks_passed']}/{receipt['checks_total']}. Runtime {receipt['runtime_seconds']:.6f} seconds; macOS maximum RSS {receipt['max_rss_bytes_macos']/2**20:.2f} MiB.

The formal r=s=6/5 witness has positive energy, positive bulk and a causal fluid ratio 50/219, with negative network-only q=-9/82. This is not a physical nonrelativistic accelerating solution: the required kinetic/rest ratio exceeds 3/4. The exact relativistic massive-constituent control has positive energy and active source for every frozen control; the analytical positive decomposition extends that sign to all positive strains and fixed nonnegative momentum mixtures.

This conditional Coulomb continuation is not an accelerating shared model. It is a completed gate on one proposed material mechanism. A different owned tensile/driven interaction or a derived gravity action must supply the missing cosmic response. Static gravity normalization, complete supports/cross energies, formation, shear causality and observational comparison remain unqualified.

Maximum derivative errors: {json.dumps(derivative_max,sort_keys=True)}.

Protocol SHA256: `{receipt['protocol_sha256']}`.
Driver SHA256: `{receipt['driver_sha256']}`.

Failed checks: {len(receipt['failed_checks'])}. Full immutable-grid rows and gates are in `{RESULT.name}`. No fit or previous worker was rerun.
'''
with REPORT.open('x') as f:
    f.write(report)
print(json.dumps({k:receipt[k] for k in ['checks_total','checks_passed','runtime_seconds','max_rss_bytes_macos','derivative_max_errors','failed_checks']},sort_keys=True))
raise SystemExit(0 if not receipt['failed_checks'] else 2)
