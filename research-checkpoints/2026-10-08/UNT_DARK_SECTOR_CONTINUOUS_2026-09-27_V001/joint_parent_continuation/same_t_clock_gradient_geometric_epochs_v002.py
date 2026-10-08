"""NEW fixed-budget geometry readout; root launches only after full review."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import time
import numpy as np

BASE = Path(__file__).resolve().parent
STEM = 'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002'
PINS = {
    STEM+'.md': '1c7fb5b6351bbc35d8cb752834db7eb235b852214271a157a23abf9967ba4b6a',
    'INVARIANT_CLOCK_GRADIENT_SAME_T_EARLY_ACCELERATION_AND_HORIZON_V001.md': '564922fee24cac57bf2329dd6bed0aa3e47f36e79c355ff8a06e169ca62782b3',
    'same_t_clock_gradient_flrw_response_v001.py': '61e6191713e5eb628b2ec551de43c200a029a6f236f7da255e867fca1d8d0990',
    'SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001_MANIFEST.json': 'a4f0db987121a101efaf29ad60b0722eab58c252dfd562f0f90d4ccf93cb1364',
    'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f',
}
AE, PANELS, ORDERS = 1e-8, 64, (16, 32, 64)
CP_KMS, MPC_M, YEAR_S = 299792.458, 3.085677581491367e22, 365.25*86400


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def save(suffix, obj):
    p = BASE/(STEM+suffix)
    with p.open('x') as f:
        json.dump(obj, f, sort_keys=True, separators=(',', ':'), allow_nan=False)
        f.write('\n')
    p.chmod(0o444)
    return sha(p)


def bisect(fun, lo, hi):
    initial = [lo, hi]
    signs = [fun(lo), fun(hi)]
    if signs[0]*signs[1] > 0:
        raise ValueError('Prospective sign bracket failed; no adaptive repair')
    for _ in range(80):
        mid = (lo+hi)/2
        if fun(lo)*fun(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return dict(value=(lo+hi)/2, initial=initial, initial_signs=signs,
                bracket=[lo, hi], final_signs=[fun(lo), fun(hi)], iterations=80)


def execute():
    start = time.monotonic()
    for name, expected in PINS.items():
        if sha(BASE/name) != expected:
            raise ValueError('Direct seal mismatch: '+name)
    lineage = dict(source_sha256=sha(__file__), inputs=PINS)
    paths = [BASE/(STEM+suf) for suf in ('_MANIFEST.json', '_RESULT.json', '_REPORT.md', '_RECEIPT.json') if (BASE/(STEM+suf)).exists()]
    if paths:
        rawp, recp = BASE/(STEM+'_RESULT.json'), BASE/(STEM+'_RECEIPT.json')
        if rawp.exists() and recp.exists():
            rec = json.loads(recp.read_text())
            raw = json.loads(rawp.read_text())
            if (rec['raw_sha256'] != sha(rawp) or raw['lineage'] != lineage
                    or rec['lineage'] != lineage or rec['gates'] != raw['gate_summary']
                    or json.loads((BASE/(STEM+'_MANIFEST.json')).read_text())['lineage'] != lineage):
                raise ValueError('Completed checkpoint authentication failed')
            for name, expected in rec['artifacts'].items():
                if sha(BASE/name) != expected:
                    raise ValueError('Completed artifact changed: '+name)
            print(json.dumps(dict(status='authenticated completed checkpoint; no recalculation',
                                  gates=raw['gate_summary'])))
            return
        raise ValueError('Partial artifacts preserved; no overwrite or replay')
    manifest = json.loads((BASE/'SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001_MANIFEST.json').read_text())
    fixed = manifest['fixed']
    parsed = ast.parse((BASE/'same_t_clock_gradient_flrw_response_v001.py').read_text())
    defs = [n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == 'background']
    if len(defs) != 1:
        raise ValueError('Exactly one authenticated background definition required')
    namespace = {'math': math}
    exec(compile(ast.Module(body=defs, type_ignores=[]), '<sealed-background-only>', 'exec'), namespace)
    bg = namespace['background']
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    gates = []

    def gate(name, value, limit, sense='le'):
        ok = bool(value <= limit) if sense == 'le' else bool(value > limit)
        gates.append(dict(name=name, value=float(value), limit=float(limit), sense=sense, passed=ok))

    def epoch(a):
        b = bg(math.log(a), fixed)
        pstar = 1.5*OA/rG*(-1+(math.log1p(b['s'])-b['s']/(1+b['s']))/(1/eps-math.log1p(1/eps)))
        b.update(Pstar=pstar, F=b['b']+2*b['r']+b['w']+2*pstar)
        b['F_x'] = -3*b['b']-8*b['r']-3*b['w']*(1+3*b['cs'])
        b['h2_x'] = -2*(b['b']+4*b['r']/3+b['w'])
        return b

    qcap = math.sqrt(1+eps)
    bm, bp = OB+OA*d0, OB+OA*d0*(3*qcap-2)
    roots = {}
    for label, bcoef in [('lower', bm), ('upper', bp)]:
        f = lambda a: 2*OA*a**4-bcoef*a-2*OR
        row = bisect(f, AE, 2.)
        a = row['value']
        row['normalized_residual'] = abs(f(a))/(2*OA*a**4+bcoef*a+2*OR)
        gate(label+'_root_residual', row['normalized_residual'], 1e-12)
        gate(label+'_root_width', (row['bracket'][1]-row['bracket'][0])/a, 1e-12)
        roots[label] = row
    ac = bisect(lambda a: epoch(a)['F'], roots['lower']['value'], roots['upper']['value'])
    aacc = ac['value']
    eacc = epoch(aacc)
    ac['normalized_residual'] = abs(eacc['F'])/(eacc['b']+2*eacc['r']+eacc['w']+2*abs(eacc['Pstar']))
    roots['actual'] = ac
    gate('actual_root_residual', ac['normalized_residual'], 1e-12)
    gate('actual_root_width', (ac['bracket'][1]-ac['bracket'][0])/aacc, 1e-12)
    gate('actual_inside_analytic_bracket', max(roots['lower']['value']-aacc, aacc-roots['upper']['value'], 0.), 0.)
    gate('actual_above_necessary_bound', aacc-(d0/2)**(1/3), 0., 'gt')
    width = math.log(roots['upper']['value']/roots['lower']['value'])
    width_bound = math.log(bp/bm)/3
    gate('analytic_log_bracket_width_excess', width-width_bound, 1e-13)
    epochs = []
    for i, x in enumerate(np.linspace(math.log(AE), 0., 65)):
        row = epoch(math.exp(float(x)))
        gate('charge_'+str(i), row['charge_error'], 1e-13)
        rho_scale = 1.5*OA/rG
        low, high = rho_scale*(1+row['charge']), rho_scale*(1+qcap*row['charge'])
        violation = max(low-row['rho'], row['rho']-high, 0.)/high
        gate('density_envelope_'+str(i), violation, 1e-13)
        gate('negative_F_derivative_'+str(i), -row['F_x'], 0., 'gt')
        if epochs:
            gate('decreasing_F_'+str(i), epochs[-1]['F']-row['F'], 0., 'gt')
        diffs = []
        for dx in (2e-4, 1e-4):
            em, ep = epoch(math.exp(float(x)-dx)), epoch(math.exp(float(x)+dx))
            fdF = (ep['F']-em['F'])/(2*dx)
            fdh = (ep['h']**2-em['h']**2)/(2*dx)
            errF, errh = abs(fdF/row['F_x']-1), abs(fdh/row['h2_x']-1)
            gate('F_derivative_'+str(i)+'_'+str(dx), errF, 1e-6)
            gate('Friedmann_derivative_'+str(i)+'_'+str(dx), errh, 1e-6)
            diffs.append(dict(dx=dx, finite_F_x=fdF, finite_h2_x=fdh, error_F=errF, error_h2=errh))
        row.update(x=float(x), density_lower=low, density_upper=high, finite_differences=diffs)
        epochs.append(row)

    hrad = math.sqrt(OR/rG)
    re = math.sqrt(1+(OB+OA*qcap*d0)/OR*AE+OA/OR*AE**4)
    tails = dict(age=[AE**2/(2*hrad*re), AE**2/(2*hrad)],
                 horizon=[AE/(hrad*re), AE/hrad], ae=AE, Re=re, hrad=hrad)
    quadratures = []
    for label, end in [('acceleration', aacc), ('today', 1.)]:
        edges = np.linspace(math.log(AE), math.log(end), PANELS+1)
        for order in ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            gate(label+'_positive_weights_'+str(order), float(min(weights)), 0., 'gt')
            gate(label+'_weights_sum_'+str(order), abs(float(sum(weights))-2), 1e-13)
            panels = []
            for left, right in zip(edges[:-1], edges[1:]):
                xx = (left+right)/2+(right-left)*nodes/2
                rows = [bg(float(x), fixed) for x in xx]
                age = (right-left)/2*math.fsum(float(w)/b['h'] for w,b in zip(weights, rows))
                hor = (right-left)/2*math.fsum(float(w)/(b['a']*b['h']) for w,b in zip(weights, rows))
                oldage = (right-left)/2*math.fsum(float(w)/(math.sqrt(rG)*b['h']) for w,b in zip(weights, rows))
                oldhor = (right-left)/2*math.fsum(float(w)/(b['a']*math.sqrt(rG)*b['h']) for w,b in zip(weights, rows))
                panels.append(dict(left=float(left), right=float(right), age=age, horizon=hor,
                                   old_geometry_age=oldage, old_geometry_horizon=oldhor))
            sums = {k: math.fsum(p[k] for p in panels) for k in ('age', 'horizon', 'old_geometry_age', 'old_geometry_horizon')}
            for k in ('age', 'horizon'):
                gate(label+'_'+k+'_G_scale_'+str(order), abs(sums[k]/sums['old_geometry_'+k]/math.sqrt(rG)-1), 1e-13)
            quadratures.append(dict(epoch=label, end=end, order=order, nodes=nodes.tolist(),
                                    weights=weights.tolist(), panels=panels, sums=sums))
    comparisons, readouts = [], {}
    seconds_per_hunit = MPC_M/(fixed['Hunit']*1000)
    gyr_per_hunit = seconds_per_hunit/(YEAR_S*1e9)
    mpc_per_hunit_light = CP_KMS/fixed['Hunit']
    for label in ('acceleration', 'today'):
        arms = [r for r in quadratures if r['epoch'] == label]
        changes = {'age': [], 'horizon': []}
        for prev, curr in zip(arms[:-1], arms[1:]):
            for k in changes:
                signed = curr['sums'][k]-prev['sums'][k]
                err = abs(signed)/curr['sums'][k]
                gate(label+'_'+k+'_'+str(prev['order'])+'_to_'+str(curr['order']), err, 1e-10)
                changes[k].append(abs(signed))
                comparisons.append(dict(epoch=label, integral=k, orders=[prev['order'], curr['order']], signed=signed, relative=err))
        best = arms[-1]['sums']
        readouts[label] = dict(a=arms[-1]['end'],
            age_hunit_interval=[best['age']+v for v in tails['age']],
            horizon_hunit_interval=[best['horizon']+v for v in tails['horizon']],
            age_Gyr_tail_interval=[(best['age']+v)*gyr_per_hunit for v in tails['age']],
            horizon_Mpc_tail_interval=[(best['horizon']+v)*mpc_per_hunit_light for v in tails['horizon']],
            max_paired_age_change_hunit=max(changes['age']),
            max_paired_horizon_change_hunit=max(changes['horizon']))
    htoday = epoch(1.)['h']
    result = dict(lineage=lineage, fixed=fixed, roots=roots, analytic_width=dict(value=width, upper=width_bound),
                  tail_bounds=tails, epochs=epochs, quadratures=quadratures, comparisons=comparisons,
                  readouts=readouts, gates=gates,
                  gate_summary=dict(total=len(gates), passed=sum(g['passed'] for g in gates), failed=[g['name'] for g in gates if not g['passed']]),
                  physical=dict(a_acc=aacc, z_acc=1/aacc-1, H_today_km_s_Mpc=htoday*fixed['Hunit'],
                      H_infinity_km_s_Mpc=math.sqrt(OA/rG)*fixed['Hunit'],
                      H_today_age_interval=[htoday*t for t in readouts['today']['age_hunit_interval']],
                      H_today_light_horizon_over_cp_interval=[htoday*t for t in readouts['today']['horizon_hunit_interval']]),
                  scope='formal conserved-radiation zero-mode fixture; numerical geometry, no observed fit or primordial prediction')
    for value in [e['h'] for e in epochs]+[r['sums'][k] for r in quadratures for k in r['sums']]:
        if not math.isfinite(value):
            raise FloatingPointError('Nonfinite saved value')
    if sha(__file__) != lineage['source_sha256'] or any(sha(BASE/n) != h for n,h in PINS.items()):
        raise ValueError('Source/input changed before publication; no result promoted')
    seals = {}
    seals[STEM+'_MANIFEST.json'] = save('_MANIFEST.json', dict(lineage=lineage, fixed=fixed, method=dict(ae=AE, panels=PANELS, orders=ORDERS, root_iterations=80), started=stamp()))
    rawsha = save('_RESULT.json', result)
    rp = BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:
        f.write('# Same-T geometric epochs V001: completed numerical readout\n\n'+stamp()+'\n\n')
        f.write('All '+str(len(gates))+' controls: '+str(sum(g['passed'] for g in gates))+' PASS; failures '+str(result['gate_summary']['failed'])+'.\n\n')
        f.write('Fixed physical sources and the new same-T GN background. One late acceleration transition; this branch does not supply primordial acceleration.\n\n')
        f.write('a_acc='+str(aacc)+', z_acc='+str(1/aacc-1)+'.\n\n')
        for label, row in readouts.items():
            f.write(label+': age_Gyr tail interval '+str(row['age_Gyr_tail_interval'])+'; light horizon_Mpc tail interval '+str(row['horizon_Mpc_tail_interval'])+'.\n\n')
        f.write('Tail intervals are rigorous within the formal conserved-radiation fixture. Quadrature differences are separately saved convergence indicators, not certified error bounds. No high-temperature species, entropy generation, atomic evolution or observational superiority is inferred.\n')
    rp.chmod(0o444)
    seals[rp.name] = sha(rp)
    save('_RECEIPT.json', dict(pid=os.getpid(), finished=stamp(), wall_seconds=time.monotonic()-start,
                              raw_sha256=rawsha, lineage=lineage, artifacts=seals, gates=result['gate_summary']))
    if sha(__file__) != lineage['source_sha256'] or any(sha(BASE/n) != h for n,h in PINS.items()):
        raise ValueError('Source/input changed after publication; preserve for root review')
    print(json.dumps(dict(raw_sha256=rawsha, gates=result['gate_summary'], physical=result['physical'], readouts=readouts)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    if not parser.parse_args().execute:
        parser.error('Root-owned --execute required; no implicit calculation')
    execute()
