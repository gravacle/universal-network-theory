"""Owned native writer/carrier cross-response; stdout-only, no new formation."""
import os
import sys
sys.dont_write_bytecode=True
for _key in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[_key]="1"
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
import native_writer_pulse_compute as pulse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.resolve()
FREEZE=HERE/"NATIVE_RULER_DISCRIMINATOR_V001_FROZEN.json"
PINS={
    "native_writer_pulse_compute.py":"28476303e45da4bd186e972addd8c49b0fcc91b2dda3a8db408c4687c0b0fb99",
    "native_writer_pulse_frozen.json":"9dde274111747690e7cfab23cd6f184ba6a5db6388a00b59f4d658e393564092",
    "native_writer_pulse_results.json":"ca023664cd9798999198ff3999b918a95613798d30ce1d434a318669697c49ea",
    "NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md":"335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c",
}
CONFIG=dict(ages=(0.,.25,.5,1.,2.),durations=(.08,.04,.02,.01),
    amplitudes=(.01,.005),tolerance=1e-11,raw_allowance=1e-12,
    null_sector_weight=1e-24,chart_threshold=1e-14,series_order=8,
    synthetic_zeta=.5,output_target_bytes=1048576)


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def sha(path):
    path=path.resolve();path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    old,_=pulse.authenticated_input()
    prior=pulse.snapshot()
    if encode(json.loads((HERE/"native_writer_pulse_frozen.json").read_text()))!=encode(prior):
        raise RuntimeError("Inherited writer source snapshot differs")
    files=dict(prior["files"])
    for name,expected in PINS.items():
        path=HERE/name
        if sha(path)!=expected:
            raise RuntimeError("Pinned source differs: "+name)
        files[str(path.relative_to(ROOT))]=expected
    result=json.loads((HERE/"native_writer_pulse_results.json").read_text())
    if (result["status"]!="COMPLETE"
            or result["freeze_sha256"]!=PINS["native_writer_pulse_frozen.json"]
            or result["payload_sha256"]!=hashlib.sha256(encode(result["payload"])).hexdigest()
            or not all(c["passed"] for c in result["payload"]["checks"])):
        raise RuntimeError("Unqualified inherited writer result")
    for name in ("native_ruler_discriminator_v001.py","NATIVE_RULER_DISCRIMINATOR_PROTOCOL_V001.md",
                 "NATIVE_RULER_STEP_SOURCE_ADDENDUM_V001.md","NATIVE_RELATIONAL_RULER_WITNESS_V001.md"):
        path=HERE/name
        files[str(path.relative_to(ROOT))]=sha(path)
    return old,dict(configuration=CONFIG,files=files)


def run(old):
    started=time.perf_counter()
    native=pulse.source_module()
    eye=native.I
    o=native.operators()
    k=o["XL"]+o["XR"];r=o["QL"]+o["QR"];n=o["n"]
    P=o["carrier_right"];yc=-o["YC"];ya=native.embed(-native.Y2,2)
    zc=eye-2*P;ys=o["YL"]+o["YR"]
    witness=o["Xa"]@yc@ys
    projectors=[(eye-o["QL"])@(eye-o["QR"]),
                o["QL"]@(eye-o["QR"])+(eye-o["QL"])@o["QR"],o["QL"]@o["QR"]]
    counts,maxima,failures={},{},[]
    ages_out,delays_out,pulses_out,sectors_out,synthetic=[],[],[],[],[]
    knorm=float(np.linalg.norm(k,2));pnorm=float(np.linalg.norm(P,2))

    def check(name,left,right=0.,tolerance=None,upper=False,tag=""):
        tol=CONFIG["tolerance"] if tolerance is None else float(tolerance)
        delta=np.asarray(left)-np.asarray(right)
        error=float(np.max(np.maximum(delta.real,0) if upper else np.abs(delta)))
        counts[name]=counts.get(name,0)+delta.size
        maxima[name]=max(maxima.get(name,0.),error)
        if not math.isfinite(error) or error>tol:
            failures.append(dict(check=name,tag=tag,error=error,tolerance=tol))

    def expect(rho,op,label="expectation"):
        value=np.trace(rho@op)
        check("real_"+label,value.imag)
        return float(value.real)

    check("witness_Hermitian",witness,witness.conj().T)
    check("witness_trace",np.trace(witness))
    check("witness_norm",np.linalg.norm(witness,2),2.)
    check("witness_square_trace",np.trace(witness@witness),32.)
    witness_states=[]
    for sign in (-1,1):
        rho=eye/16+sign*CONFIG["synthetic_zeta"]*witness/32
        check("witness_positive",-np.min(np.linalg.eigvalsh(rho)),upper=True)
        check("witness_normalized",np.trace(rho),1.)
        check("witness_correlation",expect(rho,witness),sign*CONFIG["synthetic_zeta"])
        tensor=rho.reshape(4,2,2,4,2,2)
        for group,size in enumerate((4,2,2)):
            marginal=np.trace(tensor,axis1=group,axis2=group+3).reshape(16//size,16//size)
            check("witness_proper_marginal",marginal,np.eye(16//size)/(16//size))
        witness_states.append((sign,rho))

    for saved in old["payload"]["cases"]:
        name,p=saved["name"],saved["parameters"]
        if tuple(x["time"] for x in saved["hold"])!=CONFIG["ages"]:
            raise RuntimeError("Inherited held-age census differs")
        hmat,_=native.hamiltonian(dict(p,g=0.),o)
        ev,vec=np.linalg.eigh(hmat)
        width=float(ev[-1]-ev[0])
        h,t,lam=p["h"],p["t_hop"],p["lambda_R"]
        gamma=lam*t*h*witness
        C1=pulse.comm(hmat,P);C2=pulse.comm(hmat,C1);C3=pulse.comm(hmat,C2)
        check("first_native_commutator",C1,-1j*t*n@yc,tag=name)
        check("second_native_commutator",C2,-t*h*ya@yc-2*t*t*n@zc,tag=name)
        for j,op in enumerate((P,C1,C2)):
            check("early_source_commutator_"+str(j),pulse.comm(op,k),tag=name)
        check("third_source_commutator",pulse.comm(C3,k),-gamma,tag=name)
        check("native_incidence_source_moment",pulse.comm(n,pulse.comm(hmat,n)),h*o["Xa"],tag=name)
        step_coeff=pulse.response_coefficients(hmat,k,P,CONFIG["series_order"])
        for j in range(3):
            check("step_early_coefficient",step_coeff[j],tag=name)
        check("step_quartic_coefficient",step_coeff[3],gamma/24,tag=name)
        impulse_coeff=[];ad=P.copy()
        for j in range(CONFIG["series_order"]+1):
            impulse_coeff.append(-1j*(1j**j)*pulse.comm(ad,k)/math.factorial(j))
            ad=pulse.comm(hmat,ad)
        check("impulse_cubic_coefficient",impulse_coeff[3],gamma/6,tag=name)
        cache={}
        for tau in CONFIG["durations"]:
            tag=name+":"+str(tau)
            U=pulse.propagator(ev,vec,tau)
            dU=pulse.spectral_tangent(ev,vec,k,tau)
            UT,dUT,detail=pulse.tangent_taylor(hmat,k,tau)
            check("propagator_Taylor",U,UT,CONFIG["raw_allowance"],tag=tag)
            check("source_Taylor",dU,dUT,CONFIG["raw_allowance"],tag=tag)
            operator=dU.conj().T@P@U+U.conj().T@P@dU
            impulse=-1j*pulse.comm(U.conj().T@P@U,k)
            check("step_Hermitian",operator,operator.conj().T,tag=tag)
            for order in (8,16):
                check("step_Kubo"+str(order),operator,pulse.kubo_operator(ev,vec,k,P,tau,order),tag=tag)
            step_series=sum(c*tau**(j+1) for j,c in enumerate(step_coeff))
            impulse_series=sum(c*tau**j for j,c in enumerate(impulse_coeff))
            tailstep=2*knorm*pnorm*tau*math.exp(width*tau)*(width*tau)**8/math.factorial(8)
            tailimp=2*knorm*pnorm*math.exp(width*tau)*(width*tau)**9/math.factorial(9)
            check("step_series8",operator,step_series,tailstep+CONFIG["tolerance"],tag=tag)
            check("impulse_series8",impulse,impulse_series,tailimp+CONFIG["tolerance"],tag=tag)
            energy_derivative=dU.conj().T@hmat@U+U.conj().T@hmat@dU
            check("linear_step_work_operator",energy_derivative,k-U.conj().T@k@U,tag=tag)
            if lam==0:
                check("feedback_off_step_operator",operator,tag=tag)
                check("feedback_off_impulse_operator",impulse,tag=tag)
            finite={}
            for amplitude in CONFIG["amplitudes"]:
                for sign in (-1,1):
                    f=sign*amplitude
                    energy,basis=np.linalg.eigh(hmat+f*k)
                    up=pulse.propagator(energy,basis,tau)
                    upt,_=native.taylor_propagator(hmat+f*k,tau)
                    check("finite_pulse_Taylor",up,upt,CONFIG["raw_allowance"],tag=tag)
                    finite[f]=up
            cache[tau]=dict(U=U,dU=dU,step=operator,impulse=impulse,
                energy_derivative=energy_derivative,finite=finite,
                tailstep=tailstep,tailimpulse=tailimp,taylor=detail)
        for sign,rho in witness_states:
            check("synthetic_energy",expect(rho,hmat),np.trace(hmat).real/16,tag=name)
            check("synthetic_step_leading",expect(rho,step_coeff[3]),sign*CONFIG["synthetic_zeta"]*lam*t*h/24,tag=name)
            check("synthetic_impulse_leading",expect(rho,impulse_coeff[3]),sign*CONFIG["synthetic_zeta"]*lam*t*h/6,tag=name)
            baselines=[];responses=[]
            for tau in CONFIG["durations"]:
                U=cache[tau]["U"]
                value=expect(rho,U.conj().T@P@U)
                check("synthetic_carrier_baseline",value,.5,tag=name)
                baselines.append(value)
                responses.append([tau,expect(rho,cache[tau]["step"]),expect(rho,cache[tau]["impulse"])])
            synthetic.append(dict(preparation_H=name,constructed_sign=sign,
                held_energy=expect(rho,hmat),correlation=expect(rho,witness),
                step_quartic=expect(rho,step_coeff[3]),impulse_cubic=expect(rho,impulse_coeff[3]),
                carrier_baselines=baselines,linear_responses=responses))
        for tau in CONFIG["durations"]:
            for label in ("step","impulse"):
                check("synthetic_opposite_"+label,
                    sum(expect(rho,cache[tau][label]) for _,rho in witness_states),tag=name)
        psi0=np.asarray(saved["formed_vector"]["real"])+1j*np.asarray(saved["formed_vector"]["imag"])
        invariants={}
        for age_row in saved["hold"]:
            age=age_row["time"];tag=name+":"+str(age)
            UH=pulse.propagator(ev,vec,age)
            UHT,_=native.taylor_propagator(hmat,age)
            check("held_Taylor",UH,UHT,tag=tag)
            psi=UH@psi0;rho=np.outer(psi,psi.conj())
            dephased=sum(pr@rho@pr for pr in projectors)
            check("actual_state_norm",np.vdot(psi,psi),1.,tag=tag)
            check("dephased_norm",np.trace(dephased),1.,tag=tag)
            energy0=expect(rho,hmat)
            check("saved_held_energy",energy0,saved["held_energy"],tag=tag)
            check("saved_record_mean",expect(rho,r),age_row["record_count"],tag=tag)
            check("saved_incidence_mean",expect(rho,n),age_row["link_occupation"],tag=tag)
            for label,obs in (("energy",hmat),("record",r),("incidence",n)):
                check("dephased_"+label,expect(dephased,obs),expect(rho,obs),tag=tag)
            coefficient=expect(rho,gamma)
            sector_weight=sector_moment=0.
            for R,pr in enumerate(projectors):
                for s in (-1,1):
                    pi=pr@(eye+s*o["XC"])/2
                    weight=expect(rho,pi);sector_weight+=weight
                    out=dict(preparation=name,age=age,R=R,s=s,weight=weight)
                    if weight<=CONFIG["null_sector_weight"]:
                        check("null_sector_nonnegative",-weight,upper=True,tag=tag)
                        out["status"]="NUMERICALLY_NULL_WEIGHT_NOT_DIVIDED"
                        sectors_out.append(out)
                        continue
                    X=expect(rho,pi@o["Xa"])/weight
                    Y=expect(rho,pi@ya)/weight
                    Z=expect(rho,pi@o["Za"])/weight
                    radius=math.sqrt(X*X+Y*Y+Z*Z)
                    x=2.25-lam*R-t*s;d=math.sqrt(x*x+4*h*h)
                    L=(2*h*X+x*Z)/d;S1=(x*X-2*h*Z)/d;S2=Y
                    action=(radius-L)/2
                    sector_energy=expect(rho,pi@hmat)/weight
                    minimum=3+R+x/2-d*radius/2
                    reconstructed_n=(1-x*radius/d)/2+x*action/d+h*S1/d
                    check("Bloch_radius_upper",radius-1,upper=True,tag=tag)
                    check("compact_action_lower",-action,upper=True,tag=tag)
                    check("compact_action_upper",action-radius,upper=True,tag=tag)
                    check("rotated_sphere",L*L+S1*S1+S2*S2,radius*radius,tag=tag)
                    check("affine_energy",sector_energy,minimum+d*action,tag=tag)
                    check("source_reconstruction",expect(rho,pi@n)/weight,reconstructed_n,tag=tag)
                    if (R,s) not in invariants:
                        invariants[R,s]=(weight,radius,action)
                    check("held_sector_invariants",[weight,radius,action],invariants[R,s],tag=tag)
                    sector_moment+=weight*h*X
                    out.update(status="RETAINED",radius=radius,action=action,capacity=radius,
                        phi=-math.atan2(S2,S1) if math.hypot(S1,S2)>CONFIG["chart_threshold"] else None,
                        energy=sector_energy,minimum=minimum,frequency=d,
                        X=X,Y=Y,Z=Z,incidence=reconstructed_n,signed_source_moment=h*X)
                    if radius>CONFIG["chart_threshold"]:
                        Q0=2*h*radius/d
                        stiffness=4*h*radius*radius/Q0**3
                        inverse_mass=h*Q0
                        check("lower_point_frequency",stiffness*inverse_mass,d*d,tag=tag)
                        check("lower_point_susceptibility",1/stiffness,2*h*h*radius/d**3,tag=tag)
                        out.update(lower_point_stiffness=stiffness,lower_point_inverse_mass=inverse_mass)
                    sectors_out.append(out)
            check("sector_weight_sum",sector_weight,1.,tag=tag)
            check("weighted_source_moment",sector_moment,h*expect(rho,o["Xa"]),tag=tag)
            impulse_work=expect(rho,1j*pulse.comm(k,hmat))
            ages_out.append(dict(preparation=name,age=age,correlation=expect(rho,witness),
                gamma=coefficient,impulse_cubic=coefficient/6,step_quartic=coefficient/24,
                held_energy=energy0,carrier_probability=expect(rho,P),impulse_work_derivative=impulse_work))
            for tau in CONFIG["durations"]:
                data=cache[tau];U=data["U"];base=U@psi
                step=expect(rho,data["step"]);impulse=expect(rho,data["impulse"])
                impulse_tangent=2*np.vdot(base,P@(U@(-1j*k@psi))).real
                check("impulse_state_tangent",impulse,impulse_tangent,tag=tag)
                check("dephased_carrier_baseline",expect(dephased,U.conj().T@P@U),pulse.mean(base,P),tag=tag)
                check("dephased_step_null",expect(dephased,data["step"]),tag=tag)
                check("dephased_impulse_null",expect(dephased,data["impulse"]),tag=tag)
                if name in ("feedback_off","copying_off"):
                    check("actual_control_step_null",step,tag=tag)
                    check("actual_control_impulse_null",impulse,tag=tag)
                changes={}
                for f,up in data["finite"].items():
                    after=up@psi
                    change=pulse.stable_change(base,after,P)
                    won=f*pulse.mean(psi,k);woff=-f*pulse.mean(after,k)
                    delta_energy=pulse.stable_change(psi,after,hmat)
                    check("finite_step_work",delta_energy,won+woff,tag=tag)
                    check("finite_source_energy",pulse.mean(after,hmat+f*k),pulse.mean(psi,hmat+f*k),tag=tag)
                    changes[f]=change
                    if lam==0:
                        check("feedback_off_finite_carrier_null",change,tag=tag)
                    pulses_out.append(dict(preparation=name,age=age,duration=tau,amplitude=f,
                        carrier_change=change,linear_prediction=f*step,work_on=won,work_off=woff,
                        held_energy_change=delta_energy))
                central=[]
                for amplitude in CONFIG["amplitudes"]:
                    value=(changes[amplitude]-changes[-amplitude])/(2*amplitude)
                    bound=pnorm*(2*knorm*tau)**3*amplitude**2/6+CONFIG["raw_allowance"]/amplitude
                    check("central_source_derivative",value,step,bound,tag=tag)
                    central.append(value)
                rich=(4*central[1]-central[0])/3
                f=CONFIG["amplitudes"][0]
                rich_bound=pnorm*(2*knorm*tau)**5*f**4/288+3*CONFIG["raw_allowance"]/f
                check("Richardson_source_derivative",rich,step,rich_bound,tag=tag)
                delays_out.append(dict(preparation=name,age=age,duration=tau,
                    carrier_baseline=pulse.mean(base,P),exact_step_derivative=step,
                    exact_impulse_derivative=impulse,
                    step_minus_quartic=step-coefficient*tau**4/24,
                    impulse_minus_cubic=impulse-coefficient*tau**3/6,
                    central_derivatives=central,Richardson_derivative=rich,
                    step_work_derivative=expect(rho,data["energy_derivative"]),
                    step_series_tail=data["tailstep"],impulse_series_tail=data["tailimpulse"]))
    for label,number,expected in (("ages",len(ages_out),15),("sectors",len(sectors_out),90),
        ("delays",len(delays_out),60),("pulses",len(pulses_out),240),("synthetic",len(synthetic),6)):
        check("census_"+label,number,expected,tolerance=0.)
    return dict(status="COMPLETE" if not failures else "FAILED_NUMERICAL_CONTROLS",
        configuration=CONFIG,check_counts=counts,maximum_errors=maxima,failures=failures,
        ages=ages_out,sectors=sectors_out,delays=delays_out,pulses=pulses_out,
        constructed_witness=synthetic,
        scope="Native source/readout and exact compact-action discriminator; no new formation, continuum, metric, gravity or phase averaging",
        seconds=time.perf_counter()-started,
        peak_self_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("freeze","run"):
        raise SystemExit("Use freeze or run; stdout only")
    old,snapshot=inputs()
    if sys.argv[1]=="freeze":
        print(encode(snapshot).decode());return
    if encode(json.loads(FREEZE.read_text()))!=encode(snapshot):
        raise RuntimeError("Prospective freeze differs")
    payload=run(old)
    output=dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
        payload=payload,within_output_target=len(encode(payload))<=CONFIG["output_target_bytes"])
    print(encode(output).decode())
    if payload["status"]!="COMPLETE":
        raise SystemExit(2)


if __name__=="__main__":
    main()
