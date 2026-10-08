"""Same saved actions at seven fields; centered roots, no trajectory or fitting."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import prepared_susceptibility_v001 as saved

HERE = Path(__file__).resolve().parent
FREEZE = HERE / 'FIXED_ACTION_FINITE_FIELD_V001_FROZEN.json'
CONFIG = dict(fields=[0.,1e-5,.0025,.01,.04,1.,100.],orders=[64,128],
              radius_bisections=64,tolerance=2e-8,arithmetic_tolerance=2e-12,
              synthetic_delta=.3,synthetic_action=.02,synthetic_h=.2,
              output_target_bytes=1048576)


def inputs():
    returned,states,parent = saved.inputs()
    files = dict(parent['files'])
    for path in (Path(__file__).resolve(),HERE/'FIXED_ACTION_FINITE_FIELD_PROTOCOL_V001.md',
                 HERE/'FIXED_ACTION_FINITE_FIELD_REUSE_V001.md'):
        files[str(path.relative_to(saved.WORKSPACE))] = saved.sha(path)
    phase = json.loads(saved.PHASE.read_text())['payload']
    return returned,states,phase,dict(config=CONFIG,files=files)


def center(k,forcing):
    return 2*np.sqrt(k/3)*np.sinh(np.arcsinh(3*math.sqrt(3)*forcing/(2*k**1.5))/3)


def rule(order):
    nodes,weights = leggauss(order)
    theta = (nodes+1)*math.pi/2
    return np.cos(theta),np.sin(theta),weights*math.pi/2


def geometry(delta,r,h,trig):
    cs,sn,w = trig
    c = center(delta*delta+r*r,delta*h)
    y = c[:,None]+r[:,None]*cs
    q = (y+c[:,None])**2+2*delta[:,None]**2+2*c[:,None]**2+r[:,None]**2
    action = r*r/(math.sqrt(2)*math.pi)*np.sum(w*sn**2*np.sqrt(q),axis=1)
    return c,y,q,action


def orbit(delta,target,h,trig):
    if np.any(delta<=0) or np.any(target<=0):
        raise ValueError('Positive-gap/action orbit required; minimum handled separately')
    lo = np.zeros_like(delta)
    hi = np.sqrt(2*target/delta)
    initial_hi_action = geometry(delta,hi,h,trig)[3]
    for _ in range(CONFIG['radius_bisections']):
        mid = (lo+hi)/2
        value = geometry(delta,mid,h,trig)[3]
        below = value<target
        lo = np.where(below,mid,lo)
        hi = np.where(below,hi,mid)
    r = (lo+hi)/2
    c,y,q,action = geometry(delta,r,h,trig)
    cs,sn,w = trig
    star = center(delta*delta,delta*h)
    shift = -c*r*r/(delta*delta+c*c+c*star+star*star)
    xplus,xminus = shift+r,shift-r
    stiff = delta*delta+3*star*star

    def excess(x):
        return x*x*(stiff/2+star*x+x*x/4)

    excitation = excess(xplus)
    endpoint_other = excess(xminus)
    minimum = -delta*delta*star*star/2-3*star**4/4
    measure = w/np.sqrt(q)
    norm = np.sum(measure,axis=1)

    def mean(values):
        return np.sum(measure*values,axis=1)/norm

    product = r[:,None]**2*sn**2*q/4
    x = shift[:,None]+r[:,None]*cs
    potential_excess = x*x*(stiff[:,None]/2+star[:,None]*x+x*x/4)
    direct = excitation[:,None]-potential_excess
    independent_action = np.sum(w*np.sqrt(2*np.maximum(direct,0))*r[:,None]*sn,axis=1)/math.pi
    period = 2*math.sqrt(2)*norm
    return dict(c=c,r=r,a=c-r,b=c+r,action=action,initial_hi_action=initial_hi_action,
        minimum=minimum,excitation=excitation,endpoint_other=endpoint_other,
        mean_y=mean(y),mean_y2=mean(y*y),mean_y3=mean(y**3),mean_y4=mean(y**4),
        kinetic=mean(product),mean_excess=mean(potential_excess),
        virial=mean(x*(stiff[:,None]*x+3*star[:,None]*x*x+x**3)),
        period=period,independent_action=independent_action,
        factor_error=np.max(abs(product-direct),axis=1),
        negative_direct=np.maximum(0.,-np.min(direct,axis=1)))


def run():
    started = time.perf_counter()
    returned,states,phase,snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze differs')
    counts,maxima,failures = {},{},[]

    def check(name,value,scale=1.,tag='',tol=None,inequality=False):
        limit = CONFIG['tolerance'] if tol is None else tol
        value = np.asarray(value,dtype=float)
        scale = np.asarray(scale,dtype=float)
        error = np.maximum(value,0.) if inequality else abs(value)
        error = error/np.where(scale>0,scale,1.)
        bad = ~np.isfinite(error)|(error>limit)
        maximum = float(np.max(error))
        maxima[name] = max(maxima.get(name,0.),maximum)
        counts[name] = counts.get(name,0)+error.size
        if np.any(bad):
            failures.append(dict(check=name,case=tag,maximum_error=maximum,
                                 failing_entries=int(np.count_nonzero(bad)),tolerance=limit))

    rules = {n:rule(n) for n in CONFIG['orders']}

    def qualify(delta,target,h,o,tag):
        energy = o['excitation']
        check('positive_bracket',target-o['initial_hi_action'],target,tag,inequality=True)
        check('action_target',o['action']-target,target,tag)
        check('turning_endpoints',o['endpoint_other']-energy,energy,tag)
        check('energy_factorization',o['factor_error'],energy,tag)
        check('control_negative_radicand',o['negative_direct'],energy,tag,
              CONFIG['arithmetic_tolerance'])
        check('direct_energy_action',o['independent_action']-target,target,tag)
        check('action_kinetic',o['action']*2*math.pi/o['period']-2*o['kinetic'],energy,tag)
        check('virial',2*o['kinetic']-o['virial'],energy,tag)
        check('energy',o['kinetic']+o['mean_excess']-energy,energy,tag)
        eq = delta*delta*o['mean_y']+o['mean_y3']-delta*h
        force_scale = abs(delta*h)+abs(delta*delta*o['mean_y'])+abs(o['mean_y3'])
        if h != 0:
            check('orbit_equation',eq,force_scale,tag)
        else:
            check('zero_mean_parity',o['mean_y'],o['r'],tag,CONFIG['arithmetic_tolerance'])

    sd = np.array([CONFIG['synthetic_delta']])
    si = np.array([CONFIG['synthetic_action']])
    sh = CONFIG['synthetic_h']
    plus,minus = [orbit(sd,si,h,rules[128]) for h in (sh,-sh)]
    for name,o,h in [('synthetic_plus',plus,sh),('synthetic_minus',minus,-sh)]:
        qualify(sd,si,h,o,name)
    for key,sign in [('c',-1),('mean_y',-1),('r',1),('minimum',1),
                     ('excitation',1),('period',1),('action',1)]:
        check('synthetic_signed_'+key,plus[key]-sign*minus[key],
              np.maximum(abs(plus[key]),abs(minus[key])),tol=CONFIG['arithmetic_tolerance'])
    star = center(sd*sd,sd*sh)
    check('zero_action_cubic',star**3+sd*sd*star-sd*sh,abs(sd*sh),
          tol=CONFIG['arithmetic_tolerance'])
    ground = dict(delta=float(sd[0]),h=sh,action=0.,mean_y=float(star[0]),
                  minimum=float(-sd[0]**2*star[0]**2/2-.75*star[0]**4),
                  excitation=0.,period=float(2*math.pi/np.sqrt(sd[0]**2+3*star[0]**2)))

    case_index = {(c['gap'],c['order'],c['dt'],c['duration']):c for c in states['cases']}
    phase_index = {(r['gap'],r['mode_order'],r['dt'],r['duration'],r['g']):r for r in phase['rows']}
    gs = states['parameters']['gs_internal']
    rows,origin_checks,anchor_checks = [],[],[]
    for index,old in enumerate(returned['rows']):
        key = (old['gap'],old['mode_order'],old['dt'],old['duration'])
        source = case_index[key]
        delta,weights = np.array(source['delta']),np.array(source['weights'])
        target = np.array(old['mode_data']['action'])
        kb = source['Kb']
        md = old['mode_data']
        saved_e,saved_p = np.array(md['zero_source_energy']),np.array(md['zero_source_pressure'])
        mu0 = float(np.sum(weights*3*(saved_e+saved_p)/(delta**4+4*saved_e))/kb)
        for g in CONFIG['fields']:
            h = g/math.sqrt(1+(g/gs)**2)
            hp = (1+(g/gs)**2)**-1.5
            values = [orbit(delta,target,h,rules[n]) for n in CONFIG['orders']]
            for n,o in zip(CONFIG['orders'],values):
                qualify(delta,target,h,o,str(index)+':'+str(g)+':'+str(n))
            low,high = values
            amplitude = np.maximum(abs(high['a']),abs(high['b']))
            check('quadrature_mean',low['mean_y']-high['mean_y'],amplitude,str(index)+':'+str(g))
            check('quadrature_excitation',low['excitation']-high['excitation'],high['excitation'],str(index)+':'+str(g))
            check('quadrature_period',low['period']-high['period'],high['period'],str(index)+':'+str(g))
            forces = [float(g-hp*np.sum(weights*delta*o['mean_y'])/kb) for o in values]
            if g:
                check('quadrature_D_over_g',forces[0]-forces[1],g,str(index)+':'+str(g))
            else:
                forces = [0.,0.]
            minimum = float(np.sum(weights*high['minimum']))
            excitation = float(np.sum(weights*high['excitation']))
            intrinsic = minimum+excitation
            if g == 0:
                check('origin_energy',high['excitation']-saved_e,saved_e,str(index))
                check('origin_pressure',high['mean_y4']/4-saved_p,saved_e,str(index))
                check('origin_turning',high['r']-np.array(md['zero_source_turning_amplitude']),high['r'],str(index))
                chi = (delta*delta+high['mean_y2'])/(delta**4+4*high['excitation'])
                chi_saved = (delta*delta+(saved_e-3*saved_p)/(delta*delta))/(delta**4+4*saved_e)
                check('origin_susceptibility',delta*delta*(chi-chi_saved),tag=str(index))
                origin_checks.append(dict(template=index,computed_E=intrinsic,
                    stored_E=old['return_energy'],computed_P=float(np.sum(weights*high['mean_y4']/4)),
                    stored_P=old['return_pressure'],stored_mu_linear=mu0,
                    computed_mu_linear=float(np.sum(weights*(1-delta*delta*chi))/kb)))
            if g == old['g']:
                anchor = phase_index[(*key,g)]
                am = anchor['mode_data']
                old_amp = np.maximum(abs(np.array(am['turning_low'])),abs(np.array(am['turning_high'])))
                check('held_anchor_mean',high['mean_y']-np.array(am['mean_y']),old_amp,str(index))
                check('held_anchor_excitation',high['excitation']-np.array(am['mode_excitation']),
                      np.array(am['mode_excitation']),str(index))
                check('held_anchor_D',forces[1]-anchor['phase_mean_D'],g,str(index))
                scale = max(abs(old['held_intrinsic_energy']),excitation)
                check('held_anchor_intrinsic_energy',intrinsic-old['held_intrinsic_energy'],scale,str(index))
                anchor_checks.append(dict(template=index,G=g,D=forces[1],old_D=anchor['phase_mean_D'],
                    intrinsic_energy=intrinsic,old_intrinsic_energy=old['held_intrinsic_energy']))
            witnesses = []
            for j in (0,len(delta)//2,len(delta)-1):
                witnesses.append(dict(mode=j,delta=float(delta[j]),target_I=float(target[j]),
                    solved_I=float(high['action'][j]),a=float(high['a'][j]),b=float(high['b'][j]),
                    mean_y=0. if g==0 else float(high['mean_y'][j]),
                    omega=float(2*math.pi/high['period'][j]),
                    energy_minimum=float(high['minimum'][j]),excitation=float(high['excitation'][j])))
            rows.append(dict(template=index,gap=old['gap'],duration=old['duration'],
                preparation_G=old['g'],mode_order=old['mode_order'],dt=old['dt'],
                G=g,h=h,hprime=hp,D=forces[1],D_order64=forces[0],
                D_over_G=forces[1]/g if g else None,mu_linear_origin=mu0,
                finite_G_departure_from_origin_slope=forces[1]/g-mu0 if g else None,
                weighted_energy_minimum=minimum,weighted_excitation=excitation,
                intrinsic_energy=intrinsic,
                ideal_adiabatic_energy_difference=kb*g*g/2+intrinsic-old['return_energy'],
                modal_witnesses=witnesses))
    indexed = {(r['gap'],r['duration'],r['preparation_G'],r['mode_order'],r['dt'],r['G']):r for r in rows}
    differences = []
    for gap in saved.CONFIG['gaps']:
        for duration in saved.CONFIG['durations']:
            for prep in saved.CONFIG['amplitudes']:
                for g in CONFIG['fields']:
                    for left,right,label in (([64,.01],[128,.01],'spectral_order'),([128,.01],[128,.005],'time_step')):
                        a,b = indexed[(gap,duration,prep,*left,g)],indexed[(gap,duration,prep,*right,g)]
                        differences.append(dict(gap=gap,duration=duration,preparation_G=prep,G=g,
                            kind=label,left_template=a['template'],right_template=b['template'],
                            signed_D_difference=b['D']-a['D'],
                            D_difference_over_G=(b['D']-a['D'])/g if g else 0.))
    check('rows',len(rows)-252,tol=0.)
    check('origins',len(origin_checks)-36,tol=0.)
    check('held_anchors',len(anchor_checks)-36,tol=0.)
    check('resolution_comparisons',len(differences)-168,tol=0.)
    payload = dict(config=CONFIG,gs=gs,rows=rows,origin_comparisons=origin_checks,
        held_anchor_comparisons=anchor_checks,resolution_comparisons=differences,
        synthetic_ground=ground,maximum_errors=maxima,check_counts=counts,failures=failures,
        scope='Same scalar fixed actions across fields; no actual new source-work trajectory, no parameter fit or metric/vector solution.',
        original_baseline=returned['baseline'])
    payload_size = len(saved.encoded(payload))
    output = dict(status='COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        freeze_sha256=saved.sha(FREEZE),payload=payload,
        payload_sha256=hashlib.sha256(saved.encoded(payload)).hexdigest(),
        payload_bytes=payload_size,within_output_target=payload_size<=CONFIG['output_target_bytes'],
        seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(output,allow_nan=False))
    return 1 if failures else 0


if __name__=='__main__':
    if sys.argv[1:]==['freeze']:
        print(json.dumps(inputs()[3],indent=2,allow_nan=False))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())
