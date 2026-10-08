"""Small exact-action qualification, not a new galaxy or native derivation.

No evolution trajectory. Freeze first controls before execution: homogeneous
FLRW RHS and constraints1e-10, forward/inverse velocities1e-8 relative to
perturbations (floor1e-25); exact initial constraint background1e-9 and
perturbation1e-4; total scalar and ordinary charges1e-12, mean shear1e-10;
two-increment constraint-flow identity1e-4 normalized to actual chain-rule
terms, not background energy. Linear first-order metric/phase velocity
recovery uses an amplitude-halving consistency report, not a fitted gate.
Use grids17/33 serially, one tiny worker, preserve failed controls. Exclusive
result, no tolerance relaxation, no field filtering or branch clipping.
"""
from pathlib import Path
import hashlib,json,math,time
import numpy as np
import invariant_clock_periodic_initial_v001 as initial
import invariant_clock_periodic_exact_v001 as exact

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_COMPONENTS_V001_RESULT.json'
CORE='24bf29a2b41de34eb105c1191b2f844be86391675160476fffa478752fe8772b'
sha=initial.sha
def clean(value):
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,np.generic):return value.item()
    raise TypeError(type(value).__name__)

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(exact.__file__)!=CORE:raise ValueError('changed exact action source')
    model,parent=initial.load();checks=[];rows=[];error=None;t0=time.monotonic()
    def check(name,error,gate):
        checks.append(dict(name=name,error=float(error),gate=gate,passed=bool(error<=gate)))
    try:
        for N in (17,33):
            prep=initial.mapped_seed(model,parent,N);run=exact.PeriodicExact(model,N,prep['k'])
            x=prep['x'];bg=run.background(x);zero=np.zeros((8,N))
            f,g=run.rhs(x,zero,return_fields=True)
            cc=run.constraints(x,zero,np.full(N,bg['pi_T_bar']),fields=g)
            check(f'{N}_homogeneous_rhs',np.max(abs(f)),1e-10)
            check(f'{N}_homogeneous_H',np.max(abs(cc['Hamiltonian']))/(6*bg['Vbar']*bg['H']**2),1e-10)
            check(f'{N}_homogeneous_chi',np.max(abs(g['chi']+3*run.cT*bg['H']))/abs(g['chi_bar']),1e-10)
            # Before charge normalization, prepare forward momenta independently
            # from supplied primitive velocities and auxiliary s.
            z=prep['z'].copy();v=prep['mapped_velocities'];s=prep['auxiliary_s']
            fa,fb,u,phase=z[:4];A=bg['abar']*np.exp(fa);B=bg['abar']*np.exp(fb);V=A*B*B
            sig=u/A;c=np.hypot(1,sig);sx=(run.dx(u)-u*run.dx(fa))/A;cx=sig*sx/c
            w=run.dx(phase)/A;X,m,d,K,ms,qr=model.constitutive(s);q=np.hypot(X,w)
            p=sig*q+c*w;e=(v[2]+cx)/A
            Theta=v[0]/c+2*c*v[1]+sig*v[2]/(A*c)+(sx+2*sig*run.dx(fb))/A
            chi=-run.cT*Theta;D=model.C*(e-(1+model.lam*abs(p)/np.hypot(p,model.bs))*p)
            z[4]=-4*V*v[1]+2*V*chi/c-bg['pi_a_bar']
            z[5]=-4*V*(v[0]+v[1])+4*V*c*chi-bg['pi_b_bar']
            z[6]=2*B*B*(model.KB*e+model.C*p+sig*chi/c)
            z[7]=2*V*(m*q/X+sig*D)-run.pi_phi_bar
            inverse=run.fields(x,z)
            actual=np.array([inverse['adot'],inverse['bdot'],inverse['udot'],inverse['q']])
            vscale=np.maximum(np.max(abs(v-np.array([bg['H'],bg['H'],0.,bg['Qbar']])[:,None]),axis=1),1e-25)
            forward_error=np.max(np.max(abs(actual-v),axis=1)/vscale)
            check(f'{N}_independent_forward_inverse',forward_error,1e-8)
            solved=initial.solve_constraints(run,prep);z=solved['z'];piT=solved['piT']
            f,g=run.rhs(x,z,return_fields=True);cc=run.constraints(x,z,piT,fields=g)
            hbg=6*bg['Vbar']*bg['H']**2
            hpert=max(np.max(abs(piT-bg['pi_T_bar'])),np.max(abs(run.dx(cc['boundary']))),1e-30)
            dscale=max(np.max(np.sum(abs(cc['momentum_terms']),axis=0)),1e-30)
            check(f'{N}_initial_H_background',np.max(abs(cc['Hamiltonian']))/hbg,1e-9)
            check(f'{N}_initial_H_perturbation',np.max(abs(cc['Hamiltonian']))/hpert,1e-4)
            check(f'{N}_initial_momentum',np.max(abs(cc['momentum']))/dscale,1e-4)
            check(f'{N}_initial_volume',abs(np.mean(g['V'])/bg['Vbar']-1),1e-12)
            check(f'{N}_initial_scalar_total',abs(np.mean(z[7]))/run.pi_phi_bar,1e-12)
            check(f'{N}_initial_dust_total',abs(np.mean(piT)/bg['pi_T_bar']-1),1e-12)
            check(f'{N}_initial_shear',abs(solved['mean_shear'])/(bg['Vbar']*bg['H']),1e-10)
            check(f'{N}_charge_rhs_mean',abs(np.mean(f[7]))/max(np.max(abs(f[7])),1e-30),1e-12)
            # An off-constraint state probes nonzero Hdot, not just zeros.
            off=z.copy();off[4]+=1e-6*abs(bg['pi_a_bar'])*np.cos(2*prep['spatial_grid'])
            ff,gg=run.rhs(x,off,return_fields=True);co=run.constraints(x,off,piT,fields=gg)
            target=run.dx(co['momentum']/gg['A']**2)
            tangent=[]
            for eps in (1e-8,5e-9):
                plus=run.constraints(x+eps,off+eps*ff,piT)
                minus=run.constraints(x-eps,off-eps*ff,piT)
                # Split state and explicit-background tangents to normalize
                # cancellation in dotD to the actual differentiated terms.
                sp=run.constraints(x,off+eps*ff,piT);sm=run.constraints(x,off-eps*ff,piT)
                tp=run.constraints(x+eps,off,piT);tm=run.constraints(x-eps,off,piT)
                errors={}
                for key,tgt in (('Hamiltonian',target),('momentum',np.zeros(N))):
                    deriv=bg['H']*(plus[key]-minus[key])/(2*eps)
                    terms=[bg['H']*(sp[key]-sm[key])/(2*eps),bg['H']*(tp[key]-tm[key])/(2*eps),tgt]
                    scale=max(np.max(np.sum(abs(np.array(terms)),axis=0)),1e-30)
                    errors[key]=float(np.max(abs(deriv-tgt))/scale)
                    check(f'{N}_constraint_flow_{key}_{eps}',errors[key],1e-4)
                tangent.append(dict(increment=eps,errors=errors))
            rows.append(dict(nodes=N,x=x,state=z,piT=piT,preparation=prep['preparation'],
                volume_shift=prep['volume_shift'],Newton=solved['history'],
                momenta_correction=solved['momenta_correction'],constraint_tangents=tangent,
                inverse_error=g['inverse_error'],min_s=float(np.min(g['s'])),
                min_schur_fraction=float(np.min(g['schur']/g['d'])),
                max_Cj_over_mu=float(np.max(model.C*g['j']/(g['m']/g['X']))),
                initial_density_contrast=piT/(2*g['V'])/(3*model.OB/bg['abar']**3)-1))
    except Exception as exc:
        error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
    result=dict(protocol=__doc__,producer_sha256=sha(__file__),dependencies={str(Path(p)):sha(p) for p in (exact.__file__,initial.__file__,initial.SOURCE)},
        rows=rows,checks=checks,error=error,all_controls_passed=error is None and len(rows)==2 and all(c['passed'] for c in checks),
        exact_action_qualified=False,observational_superiority=False,elapsed_seconds=time.monotonic()-t0)
    with OUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False,default=clean)
    print(json.dumps(dict(checks=checks,error=error,all_pass=result['all_controls_passed'],sha256=sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
