"""Prospective full nonlinear shared pulse; stdout-only freeze/run."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.resolve()
FREEZE = HERE/"HIGH_GAP_PULSE_V001_FROZEN.json"
OLD = HERE/"COMMON_HISTORY_MECHANISM_V001_RESULTS.json"
OLD_FREEZE = HERE/"COMMON_HISTORY_MECHANISM_V001_FROZEN.json"
OLD_SHA = "e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a"
OLD_FREEZE_SHA = "13d05e24680166cb903e02fb961717a2bef1a89771a1d76c80156ab50cbe76ef"
OLD_PAYLOAD_SHA = "91793086852fe6fe12908bae49f6eb983c7aa15d7211cd7abf496a7827d4691e"
CONFIG = dict(epsilon=.001, hard_weight=.005, hard_gaps=(32.,64.,128.),
              amplitudes=(1.,4.), cycles=8, inherited_gs=21.65919852693508,
              primary_census=((64,256),(128,256),(128,512)),
              independent_census=(128,256), orbit_orders=(64,128),
              source_quadrature_order=256, root_bisections=96,
              static_sources=(.0001,.001,.01,.1,1.,10.,100.),
              vector_tolerance=5e-7, work_tolerance=2e-7,
              spectral_tolerance=2e-6, orbit_tolerance=2e-9,
              algebra_tolerance=2e-11, output_limit_bytes=1048576,
              tiny_soft_scale_absolute=1e-14, tiny_soft_scale_relative=1e-12)
SOURCES = ("high_gap_pulse_v001.py", "HIGH_GAP_PULSE_PROTOCOL_V001.md",
           "HIGH_GAP_SHARED_SPECTRUM_CANDIDATE_V001.md",
           "FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md",
           "SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md")


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",",":"), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owned(path):
    path = path.resolve()
    path.relative_to(PROJECT)
    return path


def authenticate():
    if sha(OLD) != OLD_SHA or sha(OLD_FREEZE) != OLD_FREEZE_SHA:
        raise RuntimeError("Inherited source bytes differ")
    old = json.loads(OLD.read_text())
    if (old["payload_sha256"] != OLD_PAYLOAD_SHA
            or hashlib.sha256(encode(old["payload"])).hexdigest() != OLD_PAYLOAD_SHA
            or old["freeze_sha256"] != OLD_FREEZE_SHA):
        raise RuntimeError("Inherited payload/freeze identity differs")
    if not all(old["payload"]["checks"].values()):
        raise RuntimeError("Inherited numerical source was not qualified")
    gs = old["payload"]["parameters"]["gs_internal"]
    if gs != CONFIG["inherited_gs"]:
        raise RuntimeError("Inherited source scale differs")
    files, visited = {}, set()

    def visit(path):
        path = owned(path)
        if path in visited:
            return
        visited.add(path)
        files[str(path.relative_to(PROJECT))] = sha(path)
        for name, digest in json.loads(path.read_text())["files"].items():
            member = owned(Path(name) if Path(name).is_absolute() else path.parent/name)
            if sha(member) != digest:
                raise RuntimeError("Inherited source changed: "+str(member))
            files[str(member.relative_to(PROJECT))] = digest
            if member.name.endswith("FROZEN.json"):
                visit(member)

    visit(OLD_FREEZE)
    files[str(OLD.relative_to(PROJECT))] = OLD_SHA
    for name in SOURCES:
        path = owned(HERE/name)
        files[str(path.relative_to(PROJECT))] = sha(path)
    return float(gs), dict(files=files, configuration=CONFIG,
                           inherited_payload_sha256=OLD_PAYLOAD_SHA)


def spectrum(order, hard_gap):
    z, w = leggauss(order)
    delta = CONFIG["epsilon"]+(z+1)*(1-CONFIG["epsilon"])/2
    weights = w*(1-CONFIG["epsilon"])/2*delta
    return np.r_[delta,hard_gap], np.r_[weights,CONFIG["hard_weight"]]


def equilibrium(delta, source):
    return 2*delta/math.sqrt(3)*np.sinh(
        np.arcsinh(3*math.sqrt(3)*source/(2*delta**2))/3)


def held(g, gs):
    factor = 1+(g/gs)**2
    return g/math.sqrt(factor), factor**-1.5


def pulse(t, duration, gap, amplitude, gs):
    if t <= 0 or t >= duration:
        return 0.,0.,0.,0.
    a = math.pi*t/duration
    h = amplitude*math.sin(a)**2*math.cos(gap*t)
    hd = amplitude*(math.pi/duration*math.sin(2*a)*math.cos(gap*t)
                    -gap*math.sin(a)**2*math.sin(gap*t))
    denominator = 1-(h/gs)**2
    if denominator <= 0:
        raise ValueError("Pulse exceeds the owned bounded source")
    return h,hd,h/math.sqrt(denominator),hd/denominator**1.5


def energy(y, v, delta):
    return .5*v*v+.5*delta*delta*y*y+.25*y**4


def integrate(order, steps_per_cycle, gap, amplitude, gs, method):
    delta, weights = spectrum(order, gap)
    count, kb = len(delta), float(np.sum(weights))
    duration = 2*math.pi*CONFIG["cycles"]/gap
    steps = CONFIG["cycles"]*steps_per_cycle
    dt = duration/steps
    state = np.zeros(2*count+2)
    eharm = amplitude**2*math.pi**2*CONFIG["cycles"]**2/8
    eref = kb*amplitude**2+CONFIG["hard_weight"]*eharm
    maximum_work_error = maximum_contact_error = maximum_hard_curvature = 0.
    maximum_soft_curvature = 0.

    def rhs(t, z):
        y, v = z[:count], z[count:2*count]
        h, hd, g, gd = pulse(t, duration, gap, amplitude, gs)
        out = np.empty_like(z)
        out[:count] = v
        out[count:2*count] = delta*h-delta**2*y-y**3
        out[-2] = kb*g*gd
        out[-1] = -float(np.dot(weights,delta*y))*hd
        return out

    for j in range(steps):
        t = j*dt
        next_time = duration if j+1 == steps else (j+1)*dt
        if method == "RK4":
            k1 = rhs(t,state)
            k2 = rhs(t+dt/2,state+dt*k1/2)
            k3 = rhs(t+dt/2,state+dt*k2/2)
            k4 = rhs(next_time,state+dt*k3)
            state += dt*(k1+2*k2+2*k3+k4)/6
        elif method == "CashKarp5":
            k1 = rhs(t,state)
            k2 = rhs(t+dt/5,state+dt*k1/5)
            k3 = rhs(t+3*dt/10,state+dt*(3*k1/40+9*k2/40))
            k4 = rhs(t+3*dt/5,state+dt*(3*k1/10-9*k2/10+6*k3/5))
            k5 = rhs(next_time,state+dt*(-11*k1/54+5*k2/2-70*k3/27+35*k4/27))
            k6 = rhs(t+7*dt/8,state+dt*(1631*k1/55296+175*k2/512
                +575*k3/13824+44275*k4/110592+253*k5/4096))
            state += dt*(37*k1/378+250*k3/621+125*k4/594+512*k6/1771)
        else:
            raise ValueError("Unknown fixed integrator")
        if not np.all(np.isfinite(state)):
            raise FloatingPointError("Nonfinite full nonlinear trajectory")
        y, v = state[:count], state[count:2*count]
        h, _, g, _ = pulse(next_time, duration, gap, amplitude, gs)
        total = kb*g*g/2+float(np.dot(weights,energy(y,v,delta)-delta*h*y))
        maximum_work_error = max(maximum_work_error,abs(total-state[-2]-state[-1]))
        maximum_contact_error = max(maximum_contact_error,abs(kb*g*g/2-state[-2]))
        maximum_hard_curvature = max(maximum_hard_curvature,3*y[-1]**2/gap**2)
        maximum_soft_curvature = max(maximum_soft_curvature,float(np.max(3*y[:-1]**2/delta[:-1]**2)))
    y, v = state[:count].copy(),state[count:2*count].copy()
    modal = energy(y,v,delta)
    ys = equilibrium(delta,gs)
    endpoint_energy = .5*delta**2*ys**2+.75*ys**4
    du = float(np.dot(weights,endpoint_energy))
    b, bd = float(np.dot(weights,delta*y)),float(np.dot(weights,delta*v))
    total = float(np.dot(weights,modal))
    summary = dict(method=method,soft_order=order,steps_per_cycle=steps_per_cycle,
        steps=steps,dt=dt,duration=duration,Kb=kb,Eref=eref,total_energy=total,
        DeltaU=du,soft_DeltaU=float(np.dot(weights[:-1],endpoint_energy[:-1])),
        vacuum_over_2M2=du/kb,initial_energy_with_constant=du,
        final_energy_with_constant=du+total,
        soft_energy=float(np.dot(weights[:-1],modal[:-1])),
        hard_energy=float(weights[-1]*modal[-1]),hard_modal_energy=float(modal[-1]),
        contact_work=float(state[-2]),mode_work=float(state[-1]),
        total_work=float(state[-2]+state[-1]),endpoint_work_error=float(total-state[-2]-state[-1]),
        max_work_identity_error=maximum_work_error,max_contact_identity_error=maximum_contact_error,
        max_hard_tangent_curvature_fraction=maximum_hard_curvature,
        max_soft_tangent_curvature_fraction=maximum_soft_curvature,
        final_B=b,final_Bdot=bd,instantaneous_D_at_zero_source=-b/kb,
        initial_contact_energy=0.,final_contact_energy=0.,
        harmonic_hard_modal_energy=eharm,hard_energy_over_harmonic=float(modal[-1]/eharm),
        hard_phase_harmonic_diagnostic=float(math.atan2(gap*y[-1],v[-1])),
        n_times_hard_e_over_R4=float(CONFIG["cycles"]*modal[-1]/gap**4))
    return dict(summary=summary,delta=delta,weights=weights,y=y,v=v,energy=modal)


def orbit(delta, modal, order):
    z, weights = leggauss(order)
    theta = (z+1)*math.pi/4
    weights = weights*math.pi/4
    b2 = 4*modal/(delta**2+np.sqrt(delta**4+4*modal))
    sine, cosine = np.sin(theta)**2,np.cos(theta)**2
    q = delta[:,None]**2+b2[:,None]*(1+sine)/2
    time_weight = weights/np.sqrt(q)
    denom = np.sum(time_weight,axis=1)
    y2 = b2*np.sum(time_weight*sine,axis=1)/denom
    y4 = b2*b2*np.sum(time_weight*sine*sine,axis=1)/denom
    period = 4*denom
    action = 2/math.pi*b2*np.sum(weights*cosine*np.sqrt(q),axis=1)
    pressure = y4/4
    chi = (delta**2+y2)/(delta**4+4*modal)
    defect = 3*(modal+pressure)/(delta**4+4*modal)
    return dict(b2=b2,period=period,frequency=2*math.pi/period,action=action,
                pressure=pressure,mean_y2=y2,chi_y=chi,contact_defect=defect)


def run():
    started = time.perf_counter()
    gs, frozen = authenticate()
    if encode(json.loads(FREEZE.read_text())) != encode(frozen):
        raise RuntimeError("Prospective source snapshot changed")
    checks, cases = [],[]

    def check(name, actual, expected=0., scale=1., tolerance=None):
        tol = CONFIG["algebra_tolerance"] if tolerance is None else tolerance
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))/np.asarray(scale)))
        checks.append(dict(name=name,scaled_residual=error,tolerance=tol,
                           passed=bool(math.isfinite(error) and error<=tol)))

    for gap in CONFIG["hard_gaps"]:
        for amplitude in CONFIG["amplitudes"]:
            label = f'R{gap}:Hp{amplitude}'
            runs = [integrate(q,s,gap,amplitude,gs,"RK4") for q,s in CONFIG["primary_census"]]
            independent = integrate(*CONFIG["independent_census"],gap,amplitude,gs,"CashKarp5")
            all_runs = runs+[independent]
            fine = runs[-1]
            delta, weights, modal = fine["delta"],fine["weights"],fine["energy"]
            kb, eref = fine["summary"]["Kb"],fine["summary"]["Eref"]
            tiny = max(CONFIG["tiny_soft_scale_absolute"],CONFIG["tiny_soft_scale_relative"]*eref)
            comparisons = []
            for i,r in enumerate(all_runs):
                summary = r["summary"]
                check(label+f':run{i}:work',summary["max_work_identity_error"],scale=eref,tolerance=CONFIG["work_tolerance"])
                check(label+f':run{i}:contact',summary["max_contact_identity_error"],scale=eref,tolerance=CONFIG["work_tolerance"])
                check(label+f':run{i}:Kb',summary["Kb"],(1-CONFIG["epsilon"]**2)/2+CONFIG["hard_weight"])
            for other,name in ((runs[1],"RK4_half_step"),(independent,"independent_method")):
                vector_error = max(float(np.max(abs(delta*(other["y"]-fine["y"])))),
                                   float(np.max(abs(other["v"]-fine["v"]))))
                check(label+':'+name+':vector',vector_error,scale=amplitude*CONFIG["cycles"],tolerance=CONFIG["vector_tolerance"])
                record = dict(label=name,phase_space_error=vector_error)
                for key in ("total_energy","soft_energy","hard_energy","total_work"):
                    err = abs(other["summary"][key]-fine["summary"][key])
                    scale = tiny if key=="soft_energy" else eref
                    check(label+':'+name+':'+key,err,scale=scale,
                          tolerance=CONFIG["spectral_tolerance"] if key=="soft_energy" else CONFIG["work_tolerance"])
                    record[key+"_absolute_difference"] = err
                    record[key+"_raw_relative_difference"] = err/max(abs(fine["summary"][key]),1e-300)
                comparisons.append(record)
            coarse, same_step = runs[0]["summary"],runs[1]["summary"]
            spectral = dict(label="same_step_soft_quadrature")
            for key,scale in (("total_energy",eref),("soft_energy",tiny),
                              ("final_B",kb*amplitude*CONFIG["cycles"]),
                              ("final_Bdot",kb*gap*amplitude*CONFIG["cycles"])):
                error = abs(coarse[key]-same_step[key])
                check(label+':quadrature:'+key,error,scale=scale,tolerance=CONFIG["spectral_tolerance"])
                spectral[key+"_absolute_difference"] = error
                spectral[key+"_raw_relative_difference"] = error/max(abs(same_step[key]),1e-300)
            comparisons.append(spectral)
            low,high = [orbit(delta,modal,q) for q in CONFIG["orbit_orders"]]
            for key in ("action","pressure","mean_y2"):
                check(label+':orbit_quadrature:'+key,low[key],high[key],np.maximum(abs(high[key]),1e-300),CONFIG["orbit_tolerance"])
            check(label+':orbit_virial',delta**2*high["mean_y2"]+3*high["pressure"],modal,np.maximum(modal,1e-300))
            check(label+':orbit_action_pressure',high["action"]*high["frequency"]-modal,high["pressure"],np.maximum(modal,1e-300))
            check(label+':susceptibility',1-delta**2*high["chi_y"],high["contact_defect"])
            z = high["b2"]/delta**2
            check(label+':defect_lower_bound',np.minimum(high["contact_defect"]-z/(1+z),0.))
            check(label+':defect_upper_bound',np.maximum(high["contact_defect"]-z*(2+z)/(1+z)**2,0.))
            ys = equilibrium(delta,gs)
            lo,hi = np.zeros_like(delta),np.cbrt(delta*gs)
            for _ in range(CONFIG["root_bisections"]):
                mid = (lo+hi)/2
                above = mid**3+delta**2*mid>delta*gs
                hi,lo = np.where(above,mid,hi),np.where(above,lo,mid)
            check(label+':endpoint_root',ys,(lo+hi)/2)
            endpoint = .5*delta**2*ys**2+.75*ys**4
            du = float(np.dot(weights,endpoint))
            dus = float(np.dot(weights[:-1],endpoint[:-1]))
            ws = float(np.sum(weights[:-1]))
            wel = float(np.dot(weights,.5*(gs-delta*ys)**2+.25*ys**4))
            check(label+':baseline_identity',du,kb*gs*gs/2-wel)
            static = []
            for g in CONFIG["static_sources"]:
                h,hp = held(g,gs)
                eq = equilibrium(delta,h)
                bsoft = float(np.dot(weights[:-1],delta[:-1]*eq[:-1]))
                bhard = float(weights[-1]*delta[-1]*eq[-1])
                old_force = g-hp*bsoft/ws
                new_force = g-hp*(bsoft+bhard)/kb
                check(label+f':static_mixture:{g}',new_force,(1-weights[-1]/kb)*old_force+weights[-1]/kb*(g-hp*gap*eq[-1]))
                static.append(dict(g=g,soft_relaxed_force=old_force,new_relaxed_force=new_force,
                                   difference=new_force-old_force,ratio=new_force/old_force))
            duration = fine["summary"]["duration"]
            gn,gw = leggauss(CONFIG["source_quadrature_order"])
            tt = (gn+1)*duration/2
            source_h = np.array([pulse(t,duration,gap,amplitude,gs)[0] for t in tt])
            resonant = duration/2*np.dot(gw,source_h*np.exp(1j*gap*tt))
            check(label+':resonant_real',resonant.real,amplitude*duration/4,amplitude*duration)
            check(label+':resonant_imag',resonant.imag,scale=amplitude*duration)
            check(label+':source_endpoints',pulse(0.,duration,gap,amplitude,gs)+pulse(duration,duration,gap,amplitude,gs))
            total_pressure = float(np.dot(weights,high["pressure"]))
            total_defect = float(np.dot(weights,high["contact_defect"])/kb)
            data = dict(delta=delta.tolist(),weights=weights.tolist(),y=fine["y"].tolist(),v=fine["v"].tolist(),
                energy=modal.tolist(),harmonic_phase_diagnostic=np.arctan2(delta*fine["y"],fine["v"]).tolist())
            data.update({key:value.tolist() for key,value in high.items()})
            rminus = gap*(1-1/CONFIG["cycles"])
            soft_harmonic_bound = 2*amplitude**2*(1-CONFIG["epsilon"]**6)/6/(rminus**2-1)**2
            cases.append(dict(gap=gap,amplitude=amplitude,cycles=CONFIG["cycles"],
                controls=[r["summary"] for r in all_runs],comparisons=comparisons,
                tiny_soft_energy_check_scale=tiny,finite_spectrum=dict(Kb=kb,soft_weight=ws,
                    hard_fraction=CONFIG["hard_weight"]/kb,DeltaU=du,soft_DeltaU=dus,
                    vacuum_over_2M2=du/kb,soft_vacuum_over_2M2=dus/ws,
                    vacuum_ratio=(du/kb)/(dus/ws),a0_window=16*kb/(3*math.pi),
                    soft_a0_window=16*ws/(3*math.pi)),
                orbit_averaged=dict(total_pressure=total_pressure,soft_pressure=float(np.dot(weights[:-1],high["pressure"][:-1])),
                    hard_pressure=float(weights[-1]*high["pressure"][-1]),pressure_over_energy=total_pressure/fine["summary"]["total_energy"],
                    mu_linear=total_defect,hard_mu_contribution=float(weights[-1]*high["contact_defect"][-1]/kb),
                    soft_mu_contribution=float(np.dot(weights[:-1],high["contact_defect"][:-1])/kb),
                    hard_frequency=float(high["frequency"][-1]),hard_frequency_shift_fraction=float(high["frequency"][-1]/gap-1)),
                harmonic_soft_energy_bound=soft_harmonic_bound,
                actual_soft_energy_over_harmonic_bound=fine["summary"]["soft_energy"]/soft_harmonic_bound,
                fine_end_state=data,relaxed_static_census=static))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!="darwin":
        peak *= 1024
    payload = dict(configuration=CONFIG,checks=checks,cases=cases,
                   seconds=time.perf_counter()-started,peak_rss_bytes=int(peak),
                   interpretation="Synthetic full scalar pulse; orbit readouts do not establish phase mixing, native sourcing, or gravity evolution.")
    return dict(status="COMPLETE" if all(row["passed"] for row in checks) else "FAILED_CHECKS",
                freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)


def main():
    if sys.argv[1:]==["freeze"]:
        output = authenticate()[1]
    elif sys.argv[1:]==["run"]:
        output = run()
    else:
        raise ValueError("usage: high_gap_pulse_v001.py freeze|run")
    content = encode(output)
    if len(content)>CONFIG["output_limit_bytes"]:
        raise RuntimeError("Output exceeds the prospectively fixed 1MiB budget")
    print(content.decode())


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status="ERROR",error_type=type(exc).__name__,error=str(exc))))
        sys.exit(1)
