"""V002 serialization repair; physics, seed and numerical gates unchanged.

V001 reached its first solved row, then failed while JSON-encoding a NumPy
boolean. Its script is preserved unchanged; it wrote no completed receipt.
V002 converts control flags to builtin bool and reruns this short job.

One nonlinear constraint solve for the SAME calibrated isocurvature seed.

Frozen before execution: a_i=.01, k=.01/Mpc, delta_b=1e-5, calibrated
KB=.02, lambda_s=98 and all background quantities from the existing receipt.
Plane-periodic conformal 3-metric A=B=a_i psi^2, uniform expansion k=l=H_i,
N=1,beta=0 initially; u=pi_u=phi_x=T_b,x=0. Uniform constitutive Q, e=p=0.
Impose <psi^6>=1 and baryon rest density rho_b=Rb(1+delta cos y)/Z,
Z=<psi^6(1+delta cos y)>. This fixes actual volume, baryon rest mass and
complete phase slice charge, not just a coordinate-zero-mean density.

The exact constraints reduce to
psi_yy=.75/kp^2 psi^5[h_i^2-rho_clock-Rb(1+delta cos y)/Z],
h_i^2=h_bg^2-(4/3)kp^2<psi_y^2>. Momentum is identically zero.
No branch clipping or seed reduction. This is initial data, not evolution,
galaxy formation or an observational score. Geodesic lapse is not the saved
Newtonian lapse; compare geometric slice data and first-order invariants.

Use even Fourier log-psi with4,8,16 harmonics, respectively64,128,256 nodes;
normalize volume analytically through log1p/expm1 to retain tiny corrections.
Newton with complex-step Jacobian h=1e-24, at most8 steps, residual<=2e-12.
Controls frozen: pointwise scaled Hamiltonian residual<=1e-10, refinement
of nonzero Fourier coefficients<=1e-10 on their common O(1) scale,
volume/mass/charge residual<=2e-12, momentum cancellation<=2e-12.
Independent perturbative preflight: psi=1+s cos y-5s²/4+5s² cos2y/8+O(delta³),
Z-1=3s delta+O(delta³), delta h²=-(2/3)kp²s²+O(delta³),
s=3Rb delta/(4kp²). Compare leading and second-harmonic coefficients at
relative1e-6; report smaller terms without declaring them a separate test.
Preserve exclusive output and any failures. One NumPy worker, no time solve.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np
from bounded_clock_shared_prediction_v001 import charge_root,quantities

BASE=Path(__file__).resolve().parent
INPUT=BASE/'CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json'
OUTPUT=BASE/'PLANE_CMC_INITIAL_DATA_V002_RESULT.json'
AI=.01
K_MPC=.01
SEED=1e-5


def main():
    started=time.monotonic()
    saved=json.loads(INPUT.read_text()); p=saved['adopted']
    K=K_MPC*299792.458/p['H0_km_s_Mpc']; kp2=K*K/AI**2
    Rb=p['omega_b_cos']/AI**3
    ss=charge_root(p['eps'],p['d0']/AI**3)
    q,d,pex,rex,cs2=quantities(p['eps'],ss)
    rhoC=p['omega_A']*(1+rex); hbg2=Rb+rhoC
    scale=.75*Rb*SEED/kp2
    histories=[]

    def geometry(coeff,N):
        M=len(coeff); y=2*math.pi*np.arange(N)/N
        modes=np.arange(1,M+1)[:,None]
        cm=np.cos(modes*y); sm=np.sin(modes*y)
        f=coeff@cm; fy=-(coeff*np.arange(1,M+1))@sm
        fyy=-(coeff*np.arange(1,M+1)**2)@cm
        norm=np.log1p(np.mean(np.expm1(6*scale*f)))/6
        logpsi=scale*f-norm; psi=np.exp(logpsi)
        psi_y=psi*scale*fy
        hdelta=-(4/3)*kp2*np.mean(psi_y**2)
        volume_excess=np.mean(np.expm1(6*logpsi))
        Zminus=np.mean(np.expm1(6*logpsi)*(1+SEED*np.cos(y)))
        residual=fyy+scale*fy*fy+np.exp(4*logpsi)*(
            (np.cos(y)-Zminus/SEED)/(1+Zminus)-hdelta/(Rb*SEED))
        projection=2*np.mean(cm*residual,axis=1)
        return dict(y=y,cm=cm,f=f,fy=fy,fyy=fyy,logpsi=logpsi,psi=psi,
                    psi_y=psi_y,hdelta=hdelta,volume_excess=volume_excess,
                    Zminus=Zminus,residual=residual,projection=projection,norm=norm)

    for M,N in ((4,64),(8,128),(16,256)):
        coeff=np.zeros(M); coeff[0]=1.
        trace=[]
        for iteration in range(8):
            g=geometry(coeff,N)
            norm=float(np.max(abs(g['projection'])))
            trace.append(norm)
            if norm<=2e-12: break
            jac=np.zeros((M,M))
            for j in range(M):
                pert=coeff.astype(complex);pert[j]+=1j*1e-24
                jac[:,j]=geometry(pert,N)['projection'].imag/1e-24
            coeff-=np.linalg.solve(jac,g['projection'])
        g=geometry(coeff,N)
        # An independent, denser evaluation is not used in the solve.
        fine=geometry(coeff,4*N)
        y=fine['y']; lp=fine['logpsi']; psi=fine['psi']
        psi_minus=np.expm1(lp)
        actual_h2=hbg2+float(fine['hdelta'])
        density_b=Rb*(1+SEED*np.cos(y))/(1+fine['Zminus'])
        volume=np.exp(6*lp)
        volume_err=abs(float(fine['volume_excess']))
        mass_err=abs(float(np.mean(np.expm1(6*lp)*(1+SEED*np.cos(y)))-fine['Zminus']))/(1+float(fine['Zminus']))
        # Full canonical momentum constraint in the CMC subset.
        h=math.sqrt(actual_h2)
        ax=bx=2*scale*fine['fy']
        V=AI**3*volume; Vx=V*(ax+2*bx)
        pia=-4*V*h; pib=-8*V*h; piax=-4*h*Vx
        momentum=pia*ax+pib*bx-piax
        momscale=max(float(np.max(abs(pia*ax))),float(np.max(abs(pib*bx))),1e-300)
        c1=float(2*np.mean(psi_minus*np.cos(y)))
        c2=float(2*np.mean(psi_minus*np.cos(2*y)))
        mean_psi=float(np.mean(psi_minus))
        # c2/scale² can amplify roundoff; compute its series-safe exact terms.
        rem=np.expm1(lp)-lp
        c2_stable=scale*coeff[1]+float(2*np.mean(rem*np.cos(2*y)))
        mean_stable=-float(fine['norm'])+float(np.mean(rem))
        controls=dict(Newton=trace[-1]<=2e-12,
                      Hamiltonian=float(np.max(abs(fine['residual'])))<=1e-10,
                      volume=volume_err<=2e-12,mass=mass_err<=2e-12,
                      slice_charge=volume_err<=2e-12,
                      momentum=float(np.max(abs(momentum)))/momscale<=2e-12,
                      metric_positive=bool(np.all(psi>0)),H_squared_positive=actual_h2>0,
                      leading_seed=abs(c1/scale-1)<=1e-6,
                      second_harmonic=abs(c2_stable/(5*scale**2/8)-1)<=1e-6,
                      homogeneous_expansion=abs(float(fine['hdelta'])/(-(2/3)*kp2*scale**2)-1)<=1e-6)
        controls={key:bool(value) for key,value in controls.items()}
        row=dict(harmonics=M,solve_nodes=N,check_nodes=4*N,coefficients=coeff.tolist(),
                 Newton_residuals=trace,controls=controls,all_controls_passed=all(controls.values()),
                 maximum_scaled_Hamiltonian_residual=float(np.max(abs(fine['residual']))),
                 relative_momentum_residual=float(np.max(abs(momentum)))/momscale,
                 volume_residual=volume_err,baryon_mass_residual=mass_err,
                 phase_charge_residual=volume_err,h_squared=actual_h2,h_squared_correction=float(fine['hdelta']),
                 Z_minus_one=float(fine['Zminus']),psi_first_harmonic=c1,
                 psi_second_harmonic_direct=c2,psi_second_harmonic_stable=c2_stable,
                 mean_psi_minus_one_direct=mean_psi,mean_psi_minus_one_stable=mean_stable,
                 samples=dict(y=y.tolist(),logpsi=lp.tolist(),density_b_units=density_b.tolist(),
                              pi_a=pia.tolist(),pi_b=pib.tolist()))
        histories.append(row)
        print(json.dumps({k:row[k] for k in ('harmonics','all_controls_passed','controls',
              'maximum_scaled_Hamiltonian_residual','h_squared_correction','Z_minus_one',
              'psi_second_harmonic_stable','mean_psi_minus_one_stable')}),flush=True)
    refinement=[]
    for a,b in zip(histories,histories[1:]):
        aa=np.pad(a['coefficients'],(0,len(b['coefficients'])-len(a['coefficients'])))
        refinement.append(float(np.max(abs(aa-np.asarray(b['coefficients'])))))
    result=dict(failed_v001_sha256=hashlib.sha256((BASE/'plane_cmc_initial_data_v001.py').read_bytes()).hexdigest(),protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                input_sha256={INPUT.name:hashlib.sha256(INPUT.read_bytes()).hexdigest()},
                dependency_sha256=hashlib.sha256((BASE/'bounded_clock_shared_prediction_v001.py').read_bytes()).hexdigest(),
                inherited=p,fixed=dict(a=AI,k_Mpc_inverse=K_MPC,K=K,seed=SEED,kp_squared=kp2,
                  Rb=Rb,rho_clock=rhoC,Q_over_Q0=q,clock_aux_s=ss,background_h_squared=hbg2,linear_psi_amplitude=scale),
                rows=histories,coefficient_refinements=refinement,
                all_controls_passed=all(r['all_controls_passed'] for r in histories) and max(refinement)<=1e-10,
                elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k] for k in ('all_controls_passed','coefficient_refinements','elapsed_seconds','peak_RSS_bytes')}))
    if not result['all_controls_passed']: raise SystemExit(1)


if __name__=='__main__':main()

