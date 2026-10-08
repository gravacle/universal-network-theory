"""Saved-state arithmetic audit only: no dynamics, imports, or orbit quadrature."""
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
name = 'HIGH_GAP_PULSE_V001_RESULTS.json'
frozen_name = 'HIGH_GAP_PULSE_V001_FROZEN.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
encode = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
read = lambda n: json.loads((HERE/n).read_text())
result, frozen = read(name), read(frozen_name)
p = result['payload']; checks = 0; maxima = {}


def require(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)


def near(label, actual, expected, scale=1., tolerance=2e-11):
    error = abs(actual-expected)/max(abs(scale), 1e-300)
    maxima[label] = max(maxima.get(label, 0.), error)
    require(math.isfinite(error) and error <= tolerance, (label,error))


def minimum(delta, h):
    # An independent monotone root reconstruction, not a trajectory.
    lower, upper = 0., h/delta
    for _ in range(100):
        y = (lower+upper)/2
        if y**3+delta**2*y > delta*h:
            upper = y
        else:
            lower = y
    return (lower+upper)/2


for file, digest in frozen['files'].items():
    path = (ROOT/file).resolve(strict=True)
    require(path.is_relative_to(ROOT) and sha(path)==digest, 'frozen identity '+file)
require(sha(HERE/frozen_name)==result['freeze_sha256'], 'freeze identity')
require(hashlib.sha256(encode(p)).hexdigest()==result['payload_sha256'], 'payload identity')
require(result['status']=='COMPLETE', 'status')
require(p['configuration']==frozen['configuration'], 'configuration')
require(len(p['checks'])==276 and all(x['passed'] for x in p['checks']), '276 controls')
for c in p['checks']:
    require(math.isfinite(c['scaled_residual']) and 0<=c['scaled_residual']<=c['tolerance'], 'reported control')
require(len(p['cases'])==6 and {(c['gap'],c['amplitude']) for c in p['cases']}==set(itertools.product([32.,64.,128.],[1.,4.])), 'six cases')
gs = p['configuration']['inherited_gs']; summaries=[]; integration_steps=0
for case in p['cases']:
    R, Hp = case['gap'],case['amplitude']; state=case['fine_end_state']; fine=case['controls'][2]
    spec=case['finite_spectrum']; orb=case['orbit_averaged']; duration=16*math.pi/R
    require([(x['method'],x['soft_order'],x['steps_per_cycle']) for x in case['controls']]==
            [('RK4',64,256),('RK4',128,256),('RK4',128,512),('CashKarp5',128,256)], 'four numerical controls')
    require(all(len(v)==129 for v in state.values()), 'complete fine modal arrays')
    d,w,y,v,e = [state[k] for k in ('delta','weights','y','v','energy')]
    kb=math.fsum(w); total=math.fsum(a*b for a,b in zip(w,e))
    soft=math.fsum(a*b for a,b in zip(w[:-1],e[:-1])); B=math.fsum(a*b*c for a,b,c in zip(w,d,y))
    Bdot=math.fsum(a*b*c for a,b,c in zip(w,d,v)); pressure=math.fsum(a*b for a,b in zip(w,state['pressure']))
    mu=math.fsum(a*b for a,b in zip(w,state['contact_defect']))/kb
    for j,(delta,weight,coord,vel,en) in enumerate(zip(d,w,y,v,e)):
        near('modal energy',.5*vel**2+.5*delta**2*coord**2+.25*coord**4,en,en)
        b2=state['b2'][j]; pp=state['pressure'][j]; m2=state['mean_y2'][j]
        near('turning energy',.5*delta**2*b2+.25*b2**2,en,en)
        near('virial energy',delta**2*m2+3*pp,en,en)
        near('action pressure',state['action'][j]*state['frequency'][j]-en,pp,en)
        near('period frequency',state['period'][j]*state['frequency'][j],2*math.pi,2*math.pi)
        near('susceptibility',delta**2*state['chi_y'][j],delta**2*(delta**2+m2)/(delta**4+4*en))
        near('contact defect',state['contact_defect'][j],3*(en+pp)/(delta**4+4*en))
        near('harmonic phase diagnostic',state['harmonic_phase_diagnostic'][j],math.atan2(delta*coord,vel))
        require(0<=pp<=en/3 and 0<=state['contact_defect'][j]<=1, 'physical modal ranges')
    for key,value in [('Kb',kb),('total_energy',total),('soft_energy',soft),('hard_energy',w[-1]*e[-1]),
                      ('final_B',B),('final_Bdot',Bdot),('instantaneous_D_at_zero_source',-B/kb)]:
        near('fine '+key,fine[key],value,max(abs(value),1e-16))
    near('total pressure',orb['total_pressure'],pressure,total)
    near('pressure ratio',orb['pressure_over_energy'],pressure/total)
    near('linear mean defect',orb['mu_linear'],mu)
    near('component defect',orb['mu_linear'],orb['soft_mu_contribution']+orb['hard_mu_contribution'])
    for control in case['controls']:
        integration_steps+=control['steps']
        near('control duration',control['duration'],duration)
        near('control dt',control['dt']*control['steps'],duration)
        near('control work sum',control['total_work'],control['contact_work']+control['mode_work'])
        near('control retained energy',control['total_energy'],control['soft_energy']+control['hard_energy'])
        near('control endpoint ledger',control['total_energy']-control['total_work'],control['endpoint_work_error'])
        near('baseline ledger',control['final_energy_with_constant'],control['initial_energy_with_constant']+control['total_energy'])
        require(control['max_work_identity_error']/control['Eref']<=2e-7, 'work qualification')
    lowered=[.5*delta**2*(ys:=minimum(delta,gs))**2+.75*ys**4 for delta in d]
    du=math.fsum(a*b for a,b in zip(w,lowered)); dus=math.fsum(a*b for a,b in zip(w[:-1],lowered[:-1])); ws=math.fsum(w[:-1])
    for key,value in [('DeltaU',du),('soft_DeltaU',dus),('vacuum_over_2M2',du/kb),
                      ('vacuum_ratio',(du/kb)/(dus/ws)),('a0_window',16*kb/(3*math.pi))]:
        near('finite spectrum '+key,spec[key],value,value)
    for row in case['relaxed_static_census']:
        g=row['g']; h=g/math.sqrt(1+(g/gs)**2); hp=(1+(g/gs)**2)**-1.5
        pol=[weight*delta*minimum(delta,h) for weight,delta in zip(w,d)]
        old=g-hp*math.fsum(pol[:-1])/ws; new=g-hp*math.fsum(pol)/kb
        near('relaxed old force',row['soft_relaxed_force'],old)
        near('relaxed new force',row['new_relaxed_force'],new)
        near('relaxed mixture',new,ws/kb*old+w[-1]/kb*(g-hp*pol[-1]/w[-1]))
        near('relaxed difference',row['difference'],new-old)
    hard_amplitude=w[-1]*d[-1]*math.sqrt(state['b2'][-1])/kb
    soft_amplitude_bound=math.fsum(ww*dd*math.sqrt(bb) for ww,dd,bb in zip(w[:-1],d[:-1],state['b2'][:-1]))/kb
    summaries.append(dict(R=R,Hp=Hp,E=total,P_over_E=pressure/total,mu=mu,soft_energy=soft,
                          vacuum_ratio=spec['vacuum_ratio'],B=B,Bdot=Bdot,D_inst=-B/kb,
                          hard_phase=fine['hard_phase_harmonic_diagnostic'],
                          hard_clamped_zero_source_D_amplitude=hard_amplitude,
                          soft_clamped_zero_source_D_amplitude_upper_bound=soft_amplitude_bound))
require(integration_steps==61440, '24 integrations / 61440 steps')
print(json.dumps(dict(status='PASS',audit_checks=checks,original_checks=276,frozen_inputs=len(frozen['files']),
    script_sha256=sha(Path(__file__)),result_sha256=sha(HERE/name),freeze_sha256=sha(HERE/frozen_name),
    payload_sha256=result['payload_sha256'],maxima=maxima,cases=summaries,
    largest_reported_gate_fraction=max(c['scaled_residual']/c['tolerance'] for c in p['checks']),
    seconds=p['seconds'],peak_self_rss_bytes=p['peak_rss_bytes']),indent=2))
