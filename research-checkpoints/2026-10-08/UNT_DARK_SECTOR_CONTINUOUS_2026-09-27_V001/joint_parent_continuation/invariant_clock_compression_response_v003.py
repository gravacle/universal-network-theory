"""Cancellation-safe coordinate repair of the failed zero-elasticity control.

Same six linear equations, source, background and scientific parameters.
Evolve r=varphi+Q*alpha, whose exact derivative is dm/d+Q*E-3H*m*alpha/d.
No metric-potential subtraction in this derivative. Save original field
coordinates/scales so the full-state1e-4 gate is unchanged. Reuse elastic
rows and20kpc zero row. Failed V001/V002 receipts remain intact. Run only
the5kpc zero row with128/256/512; a numerical failure remains a failure.
"""
from pathlib import Path
import json
import time
import numpy as np
import invariant_clock_compression_response_v001 as old

ROOT=Path(__file__).resolve().parent
PREV=ROOT/'INVARIANT_CLOCK_COMPRESSION_RESPONSE_V002_RESULT.json'
PREVSHA='f08a3f422a0a7376c92f055a799d17390f613fcab29a512b41f6b0bdaf4e602d'
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_RESPONSE_V003_RESULT.json'

class Response(old.Response):
    def __init__(self,m,width,cTheta):
        super().__init__(m,width,cTheta)
        self.oldscale=self.scale.copy();self.scale[1]=old.PROBE
    def rhs(self,x,y,diagnostic=False):
        bg=self.bg(x);a,Q,m,d,H,Hd,Hdx,rb,k2=bg
        rt,rtdot,qs,ps,rhos=self.source(x,bg)
        shape=(-1,)+(1,)*(y.ndim-1)
        dm,rel,alpha,Z,db,theta=y[:6]*self.scale.reshape(shape)
        phi=rel-Q*alpha;one=y[6];qs=qs*one;rt=rt*one;rtdot=rtdot*one
        qbase=m*phi+rb*theta+qs
        chi=self.cT/self.F*(1.5*qbase+k2*alpha)
        potential=Z/2-(Q*dm+rb*db+3*H*(m*phi+rb*theta)+rt)/(2*k2)
        pdot=(qbase-chi)/2-H*potential
        E=(Z-self.m.C*rel)/self.m.KB;D=self.m.C*(E-rel)
        dmdot=-3*H*dm+3*m*pdot+k2*(D-m*phi/Q)
        reldot=dm/d+Q*E-3*H*m*alpha/d
        phidot=dm/d+Q*potential
        adot=E-potential;zdot=-H*Z+Q*D-chi+3*self.cT*Hd*alpha
        dbdot=3*pdot-k2*theta;tdot=potential
        qdot=-3*H*(m*phi+rb*theta)+m*phidot+rb*tdot
        u=Q*dm+rb*db+3*H*(m*phi+rb*theta)+rt
        udot=(-3*H*m/d)*dm+Q*dmdot-3*H*rb*db+rb*dbdot+3*Hd*(m*phi+rb*theta)+3*H*qdot+rtdot
        residual=zdot/2-(udot+2*H*u)/(2*k2)-pdot
        scale=np.abs(zdot/2)+np.abs(udot/(2*k2))+np.abs(H*u/k2)+np.abs(pdot)
        self.max_constraint=max(self.max_constraint,float(np.max(abs(residual)/np.maximum(scale,1e-80))))
        ret=np.array([dmdot,reldot,adot,zdot,dbdot,tdot])/self.scale.reshape(shape)/H
        ret=np.concatenate([ret,np.zeros_like(y[6:7])],axis=0)
        if not diagnostic:return ret
        cap=self.m.Q0*np.sqrt(1+self.m.eps)-Q
        return dict(a=a,log_a=x,log_a_formation_intervals=x/self.xf,
            state=(np.array([dm,phi,alpha,Z,db,theta])/self.oldscale).tolist(),
            evolved_relative_phase=float(rel/old.PROBE),
            observables=[float(potential/old.PROBE),float(E/old.PROBE),float(rel/old.PROBE),float(chi/(H*old.PROBE))],
            physical_depth_linear_extrapolation=dict(
                phase_gradient_over_bs=float(np.sqrt(k2)*abs(rel)*1e12/self.m.bs),
                deltaX_over_upper_margin=float(abs(dm/d)*1e12/cap),
                ordinary_contrast=float(abs(db)*1e12),vector_tilt=float(np.sqrt(k2)*abs(alpha)*1e12)),
            infinitesimal_probe_domain=dict(deltaX_over_upper_margin=float(abs(dm/d)/cap),
                phase_gradient_over_bs=float(np.sqrt(k2)*abs(rel)/self.m.bs)))

def main():
    started=time.monotonic()
    if OUT.exists():raise RuntimeError('no overwrite/duplicate worker')
    if old.sha(PREV)!=PREVSHA:raise ValueError('changed previous receipt')
    result=json.loads(PREV.read_text())
    if old.sha(Path(old.__file__))!=result['source_sha256']:raise ValueError('changed original source')
    if old.sha(old.CAL)!=result['calibration_sha256']:raise ValueError('changed calibration')
    for path,digest in result['dependencies'].items():
        if old.sha(Path(path))!=digest:raise ValueError('changed dependency')
    saved=json.loads(old.base.SOURCE.read_text());saved['inherited']=result['fixed'];m=old.base.Model(saved,1)
    # Independent exact time-dependent coordinate transformation of RHS.
    before=old.Response(m,5.,0.);after=Response(m,5.,0.)
    transform_error=0.
    for x in (0.,after.xf*.4,after.xf*2):
        a,Q,charge,d,H,*_=after.bg(x)
        T=np.eye(7);T[:6,:6]=np.diag(after.scale/before.scale)
        T[1,2]=-Q*after.scale[2]/before.scale[1]
        Tx=np.zeros((7,7));Tx[1,2]=3*charge/d*after.scale[2]/before.scale[1]
        lhs=before.rhs(x,np.eye(7))@T
        rhs=T@after.rhs(x,np.eye(7))+Tx
        transform_error=max(transform_error,float(np.max(abs(lhs-rhs))/max(np.max(abs(lhs)),1e-80)))
    new=[Response(m,5.,0.).integrate(n) for n in (128,256,512)]
    row=next(r for r in result['rows'] if r['width_kpc']==5. and r['cTheta']==0.)
    row['old_variable_histories']=row['histories'];row['histories']=new
    values={'5.0kpc_cT0.0_state_refinement':old.discrepancy(new[-2],new[-1],'state'),
            '5.0kpc_cT0.0_observable_refinement':old.discrepancy(new[-2],new[-1],'observables'),
            '5.0kpc_cT0.0_Einstein_derivative':max(h['constraint_defect'] for h in new),
            '5.0kpc_cT0.0_source_conservation':max(h['source_defect'] for h in new)}
    for c in result['controls']:
        if c['name'] in values:c['error']=values[c['name']];c['passed']=bool(c['error']<=c['gate'])
    result['controls'].append(dict(name='relative_phase_exact_RHS_transformation',error=transform_error,
        gate=1e-12,passed=bool(transform_error<=1e-12)))
    snaps=new[-1]['snapshots'];row['final']=snaps[-1];row['one_formation']=snaps[32]
    row['peak_abs_observables']=np.max(abs(np.array([r['observables'] for r in snaps])),axis=0).tolist()
    row['maximum_physical_extrapolation']={key:max(r['physical_depth_linear_extrapolation'][key] for r in snaps)
        for key in snaps[0]['physical_depth_linear_extrapolation']}
    result.update(coordinate_repair_protocol=__doc__,coordinate_repair_source_sha256=old.sha(Path(__file__)),
        coordinate_repair_parent_sha256=PREVSHA,coordinate_repair_elapsed_seconds=time.monotonic()-started,
        all_controls_passed=all(c['passed'] for c in result['controls']))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],errors=values,
        transform_error=transform_error,failed=[c for c in result['controls'] if not c['passed']],
        elapsed_seconds=result['coordinate_repair_elapsed_seconds'],result_sha256=old.sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
