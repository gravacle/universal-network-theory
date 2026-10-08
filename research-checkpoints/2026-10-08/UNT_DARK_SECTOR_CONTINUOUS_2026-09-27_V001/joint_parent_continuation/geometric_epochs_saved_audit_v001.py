"""Independent standard-library saved-only acceptance; root executes after review."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import time

BASE = Path(__file__).resolve().parent
PARENT = 'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002'
STEM = 'GEOMETRIC_EPOCHS_V002_SAVED_AUDIT_V001'
PINS = {
    'GEOMETRIC_EPOCHS_V002_SAVED_AUDIT_V001_PROTOCOL.md': '6cf6618314bbc51a929474481326d0143c37c0ee03e5c155db5d0f5872957bef',
    'same_t_clock_gradient_geometric_epochs_v002.py': 'eb166dc2644b8c89849fc62b5c79a967850a2513086ecc996d29faadef46200a',
    'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002.md': '1c7fb5b6351bbc35d8cb752834db7eb235b852214271a157a23abf9967ba4b6a',
    'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002_RESULT.json': 'b4fe2f337ceb598182db936328ea49ee5272105b573789dd908ebebef7b4929c',
    'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002_RECEIPT.json': 'ea6c0929d1ce937252cc019c4f4d2bd19d685fe319148e3cf7d72f5edb848a40',
    'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002_MANIFEST.json': '3d77325817a513f882af17624365cc2ce7bb888387d0c9c83f4eecf97ba692a1',
    'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002_REPORT.md': '348484ebfe57e7c3ce72e53e1457ad3304bdc04b9de0b20af10375727117fb57',
}
COUNT, MAX_ERROR = 0, 0.


def sha(name):
    return hashlib.sha256((BASE/name).read_bytes()).hexdigest()


def check(ok, name):
    global COUNT
    COUNT += 1
    if not ok:
        raise AssertionError(name)


def close(got, expected, name, atol=2e-15, rtol=2e-12):
    global MAX_ERROR
    check(math.isfinite(got) and math.isfinite(expected), name+' finite')
    error = abs(got-expected)
    MAX_ERROR = max(MAX_ERROR, error/(1+abs(expected)))
    check(error <= atol+rtol*abs(expected), name+' arithmetic')


def finite_tree(obj):
    if isinstance(obj, dict):
        for val in obj.values():
            finite_tree(val)
    elif isinstance(obj, list):
        for val in obj:
            finite_tree(val)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        check(math.isfinite(obj), 'finite serialized value')


def write(suffix, obj):
    path = BASE/(STEM+suffix)
    with path.open('x') as f:
        json.dump(obj, f, sort_keys=True, separators=(',', ':'), allow_nan=False)
        f.write('\n')
    path.chmod(0o444)
    return sha(path.name)


def audit():
    start = time.monotonic()
    source_sha = sha(Path(__file__).name)
    for n, h in PINS.items():
        check(sha(n) == h, 'direct seal '+n)
    raw = json.loads((BASE/(PARENT+'_RESULT.json')).read_text())
    rec = json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    man = json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())
    report = (BASE/(PARENT+'_REPORT.md')).read_text()
    tree = ast.parse((BASE/'same_t_clock_gradient_geometric_epochs_v002.py').read_text())
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'PINS')
    declared = {(PARENT+'.md' if isinstance(k, ast.BinOp) else ast.literal_eval(k)): ast.literal_eval(v) for k, v in zip(node.value.keys, node.value.values)}
    lineage = dict(source_sha256=PINS['same_t_clock_gradient_geometric_epochs_v002.py'], inputs=declared)
    check(raw['lineage'] == rec['lineage'] == man['lineage'] == lineage, 'all exact lineage')
    check(rec['raw_sha256'] == PINS[PARENT+'_RESULT.json'], 'raw receipt identity')
    check(rec['artifacts'] == {n:PINS[n] for n in (PARENT+'_MANIFEST.json', PARENT+'_REPORT.md')}, 'exact artifact map')
    for n, h in declared.items():
        check(sha(n) == h, 'inherited seal '+n)
    inherited = json.loads((BASE/'SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001_MANIFEST.json').read_text())
    fixed = raw['fixed']
    check(fixed == man['fixed'] == inherited['fixed'], 'fixed physical inventory')
    check(man['method'] == dict(ae=1e-8, panels=64, orders=[16,32,64], root_iterations=80), 'method census')
    finite_tree(raw)
    eps, d0, oa, ob, rad, rg = (fixed[k] for k in ('eps','d0','OA','OB','OR','rG'))
    norm, qcap, ae = 1/eps-math.log1p(1/eps), math.sqrt(1+eps), 1e-8
    roots, expected_gates = raw['roots'], []

    def gate(name, value, limit, sense='le'):
        expected_gates.append(dict(name=name, value=value, limit=limit, sense=sense))

    bm, bp = ob+oa*d0, ob+oa*d0*(3*qcap-2)
    for label, coef in [('lower',bm),('upper',bp)]:
        row = roots[label]
        f = lambda a: 2*oa*a**4-coef*a-2*rad
        check(row['initial'] == [ae,2.] and row['iterations'] == 80, label+' frozen bracket')
        check(row['bracket'][0] <= row['value'] <= row['bracket'][1], label+' root containment')
        for field in ('initial','bracket'):
            signs = row['initial_signs' if field == 'initial' else 'final_signs']
            for a, val in zip(row[field], signs):
                close(val, f(a), label+' endpoint')
            check(signs[0] <= 0 <= signs[1], label+' increasing sign bracket')
        a = row['value']
        residual = abs(f(a))/(2*oa*a**4+coef*a+2*rad)
        close(row['normalized_residual'], residual, label+' residual', rtol=0.)
        gate(label+'_root_residual', row['normalized_residual'], 1e-12)
        gate(label+'_root_width', (row['bracket'][1]-row['bracket'][0])/a, 1e-12)
    ac = roots['actual']; aa = ac['value']
    check(ac['initial'] == [roots['lower']['value'],roots['upper']['value']] and ac['iterations'] == 80, 'actual frozen bracket')
    check(ac['bracket'][0] <= aa <= ac['bracket'][1], 'actual root containment')
    check(ac['initial_signs'][0] >= 0 >= ac['initial_signs'][1] and ac['final_signs'][0] >= 0 >= ac['final_signs'][1], 'actual decreasing F sign bracket')
    gate('actual_root_residual', ac['normalized_residual'], 1e-12)
    gate('actual_root_width', (ac['bracket'][1]-ac['bracket'][0])/aa, 1e-12)
    gate('actual_inside_analytic_bracket', max(roots['lower']['value']-aa,aa-roots['upper']['value'],0.), 0.)
    gate('actual_above_necessary_bound', aa-(d0/2)**(1/3), 0., 'gt')
    width, ceiling = math.log(roots['upper']['value']/roots['lower']['value']), math.log(bp/bm)/3
    close(raw['analytic_width']['value'],width,'bracket width'); close(raw['analytic_width']['upper'],ceiling,'width ceiling')
    gate('analytic_log_bracket_width_excess', width-ceiling, 1e-13)
    check(len(raw['epochs']) == 65, 'epoch census')
    for i, row in enumerate(raw['epochs']):
        a, s = row['a'], row['s']; scale = 1.5*oa/rg
        close(row['x'], math.log(ae)*(1-i/64), 'epoch position', atol=2e-14)
        close(a, math.exp(row['x']), 'epoch a')
        d, qb = d0/a**3, math.sqrt(1+eps*s/(1+s))
        pex = (math.log1p(s)-s/(1+s))/norm
        b, r, w, rho, p = 1.5*ob/rg/a**3,1.5*rad/rg/a**4,scale*qb*d,scale*(1+qb*d-pex),scale*(-1+pex)
        cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
        F, Fx, hx = b+2*r+w+2*p,-3*b-8*r-3*w*(1+3*cs),-2*(b+4*r/3+w)
        values = dict(charge=d,qbar=qb,b=b,r=r,w=w,rho=rho,Pstar=p,cs=cs,F=F,F_x=Fx,h2_x=hx,h=math.sqrt(2*(b+r+rho)/3))
        for k, v in values.items(): close(row[k],v,'epoch '+str(i)+' '+k)
        err = abs(2*qb*s/(eps*norm)/d-1)
        close(row['charge_error'],err,'charge residual')
        low, high = scale*(1+d),scale*(1+qcap*d)
        close(row['density_lower'],low,'density lower'); close(row['density_upper'],high,'density upper')
        gate('charge_'+str(i),row['charge_error'],1e-13)
        gate('density_envelope_'+str(i),max(low-row['rho'],row['rho']-high,0.)/high,1e-13)
        gate('negative_F_derivative_'+str(i),-row['F_x'],0.,'gt')
        if i: gate('decreasing_F_'+str(i),raw['epochs'][i-1]['F']-row['F'],0.,'gt')
        check([z['dx'] for z in row['finite_differences']] == [2e-4,1e-4], 'finite difference census')
        for z in row['finite_differences']:
            ef, eh = abs(z['finite_F_x']/row['F_x']-1),abs(z['finite_h2_x']/row['h2_x']-1)
            close(z['error_F'],ef,'stored F difference'); close(z['error_h2'],eh,'stored H difference')
            gate('F_derivative_'+str(i)+'_'+str(z['dx']),ef,1e-6)
            gate('Friedmann_derivative_'+str(i)+'_'+str(z['dx']),eh,1e-6)
    hrad = math.sqrt(rad/rg)
    re = math.sqrt(1+(ob+oa*qcap*d0)/rad*ae+oa/rad*ae**4)
    tails = dict(age=[ae**2/(2*hrad*re),ae**2/(2*hrad)],horizon=[ae/(hrad*re),ae/hrad],ae=ae,Re=re,hrad=hrad)
    for k, v in tails.items():
        if isinstance(v,list):
            for g,e in zip(raw['tail_bounds'][k],v): close(g,e,'tail '+k)
        else: close(raw['tail_bounds'][k],v,'tail '+k)
    check([(q['epoch'],q['order']) for q in raw['quadratures']] == [(l,o) for l in ('acceleration','today') for o in (16,32,64)], 'six quadrature arms')
    for q in raw['quadratures']:
        label, order = q['epoch'],q['order']; end = aa if label=='acceleration' else 1.
        check(q['end']==end and len(q['nodes'])==len(q['weights'])==order and len(q['panels'])==64,'quadrature shape')
        check(all(-1<x<1 for x in q['nodes']) and all(x<y for x,y in zip(q['nodes'][:-1],q['nodes'][1:])), 'ordered nodes')
        for j in range(order):
            close(q['nodes'][j],-q['nodes'][-1-j],'node symmetry'); close(q['weights'][j],q['weights'][-1-j],'weight symmetry')
        gate(label+'_positive_weights_'+str(order),min(q['weights']),0.,'gt')
        gate(label+'_weights_sum_'+str(order),abs(sum(q['weights'])-2),1e-13)
        left0, step = math.log(ae),(math.log(end)-math.log(ae))/64
        for j,p in enumerate(q['panels']):
            close(p['left'],left0+j*step,'panel left',atol=2e-14); close(p['right'],left0+(j+1)*step,'panel right',atol=2e-14)
            for k in ('age','horizon'):
                check(p[k]>0 and p['old_geometry_'+k]>0,'positive integral panel')
                close(p[k],math.sqrt(rg)*p['old_geometry_'+k],'panel G scaling')
        for k in ('age','horizon','old_geometry_age','old_geometry_horizon'):
            close(q['sums'][k],math.fsum(p[k] for p in q['panels']),'compensated panels '+k)
        for k in ('age','horizon'):
            gate(label+'_'+k+'_G_scale_'+str(order),abs(q['sums'][k]/q['sums']['old_geometry_'+k]/math.sqrt(rg)-1),1e-13)
    check(len(raw['comparisons'])==8,'comparison census')
    index=0; gyr=3.085677581491367e22/(fixed['Hunit']*1000)/(365.25*86400*1e9); light=299792.458/fixed['Hunit']
    for label in ('acceleration','today'):
        arms=[q for q in raw['quadratures'] if q['epoch']==label]; changes=dict(age=[],horizon=[])
        for prev,curr in zip(arms[:-1],arms[1:]):
            for k in ('age','horizon'):
                row=raw['comparisons'][index]; index+=1
                signed=curr['sums'][k]-prev['sums'][k]; err=abs(signed)/curr['sums'][k]
                check((row['epoch'],row['integral'],row['orders'])==(label,k,[prev['order'],curr['order']]),'comparison label')
                close(row['signed'],signed,'signed refinement');close(row['relative'],err,'relative refinement')
                gate(label+'_'+k+'_'+str(prev['order'])+'_to_'+str(curr['order']),err,1e-10);changes[k].append(abs(signed))
        out=raw['readouts'][label];best=arms[-1]['sums'];check(out['a']==arms[-1]['end'],'readout epoch')
        for k,unit in [('age',gyr),('horizon',light)]:
            native=out[k+'_hunit_interval'];physical=out['age_Gyr_tail_interval' if k=='age' else 'horizon_Mpc_tail_interval']
            for j in range(2): close(native[j],best[k]+tails[k][j],'native tail addition');close(physical[j],native[j]*unit,'physical units')
            close(out['max_paired_'+k+'_change_hunit'],max(changes[k]),'all paired maximum')
        check(str(out['age_Gyr_tail_interval']) in report and str(out['horizon_Mpc_tail_interval']) in report,'report readouts')
    phys=raw['physical'];ht=raw['epochs'][-1]['h']
    for key,val in dict(a_acc=aa,z_acc=1/aa-1,H_today_km_s_Mpc=ht*fixed['Hunit'],H_infinity_km_s_Mpc=math.sqrt(oa/rg)*fixed['Hunit']).items(): close(phys[key],val,'physical '+key)
    for key,src in [('H_today_age_interval','age_hunit_interval'),('H_today_light_horizon_over_cp_interval','horizon_hunit_interval')]:
        for g,e in zip(phys[key],raw['readouts']['today'][src]): close(g,ht*e,'dimensionless present product')
    check(len(expected_gates)==len(raw['gates'])==560 and len({g['name'] for g in raw['gates']})==560,'all560 unique gates')
    for got,want in zip(raw['gates'],expected_gates):
        check(set(got)=={'name','value','limit','sense','passed'},'gate exact schema')
        check(all(got[k]==want[k] for k in ('name','limit','sense')),'gate metadata')
        close(got['value'],want['value'],'gate value')
        passed=got['value']<=got['limit'] if got['sense']=='le' else got['value']>got['limit']
        check(got['passed'] is passed,'exact frozen gate disposition')
    summary=dict(total=560,passed=sum(g['passed'] for g in raw['gates']),failed=[g['name'] for g in raw['gates'] if not g['passed']])
    check(summary==raw['gate_summary']==rec['gates'],'summary equality')
    check('All 560 controls: '+str(summary['passed'])+' PASS' in report and 'not certified error bounds' in report,'report qualification scope')
    seals=dict(PINS);seals.update(declared)
    for n,h in seals.items(): check(sha(n)==h,'prepublication seal '+n)
    check(sha(Path(__file__).name)==source_sha,'audit source immutable')
    result=dict(status='SAVED_ONLY_ARITHMETIC_ACCEPTED',assertions=COUNT,max_normalized_arithmetic_discrepancy=MAX_ERROR,parent_gates=summary,parent_result_sha256=PINS[PARENT+'_RESULT.json'],source_sha256=source_sha,inputs=seals,physical=phys,readouts=raw['readouts'],scope='Independent saved arithmetic only; actual F-root residual and panel integrands authenticated, not independently solved; rigorous early-tail bounds plus uncertified converged partial integrals.')
    raw_sha=write('_RESULT.json',result)
    rp=BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:
        f.write('# Saved-only geometric epochs audit V001\n\n'+str(COUNT)+' assertions PASS; original '+str(summary['passed'])+'/560 dispositions preserved.\n\n')
        f.write('All65 saved epochs, six64-panel sums, eight signed refinements, brackets, tails, units and custody checked. No background/root/quadrature solve or producer import. Actual F-root residual and unsaved Gauss integrands remain authenticated rather than independently re-evaluated.\n\n')
        f.write('The early-tail bounds are analytic; total reported intervals do not include a certified partial-quadrature error. No observed agreement, primordial thermal history or constrained-U model qualification follows.\n')
    rp.chmod(0o444)
    write('_RECEIPT.json',dict(raw_sha256=raw_sha,report_sha256=sha(rp.name),source_sha256=source_sha,inputs=seals,assertions=COUNT,pid=os.getpid(),wall_seconds=time.monotonic()-start,finished=datetime.now(timezone.utc).isoformat()))
    if sha(Path(__file__).name)!=source_sha or any(sha(n)!=h for n,h in seals.items()): raise ValueError('Postpublication seal changed; preserve outputs')
    print(json.dumps(dict(status=result['status'],assertions=COUNT,raw_sha256=raw_sha,parent_gates=summary)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true')
    if not parser.parse_args().execute: parser.error('Root-owned --execute required')
    if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json','_ERROR.json')): raise SystemExit('Existing audit artifacts preserved; no replay/overwrite')
    try: audit()
    except Exception as error:
        write('_ERROR.json',dict(error_type=type(error).__name__,error=str(error),assertions=COUNT,source_sha256=sha(Path(__file__).name)))
        raise
