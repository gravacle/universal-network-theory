"""Same compression source, parity-regular inward radial interpolation.

V001 log-radius kernel produces a candidate O(h) origin artifact for smooth
even T0: first midpoint node ratios stay1:3:5:7 under refinement. V002 uses
the separately qualified R² interpolation kernel; same action, coefficient,
preparation, outer data and1e-3 numerical gates. No damping/phase fitting.
Preserve V001 charge-boundary and preboundary-control failures separately.

Runner repair: checkpoint step is ACCEPTED steps, separate attempted step;
V001 failure checkpoints labeled the attempted step but retained the previous
accepted state. Final numerical control failures are explicit, not inferred
from process exit alone. Even a clean short trajectory remains unqualified
until spatial/time/domain and complete physical controls are done.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
import invariant_clock_compression_source_test_v001 as old
import invariant_clock_compression_radial_v003 as radial

ROOT=Path(__file__).resolve().parent
source=old.source
source.radial=radial
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PARENT_SHA='a8b790f2bcf0c80d91e8a9b20b233389272ef57a9e7037364cc7c9d8399334f6'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--nodes',type=int,default=128)
    ap.add_argument('--extent',type=float,default=.002)
    ap.add_argument('--steps',type=int,default=128);ap.add_argument('--dt-factor',type=float,default=.06)
    ap.add_argument('--wall-seconds',type=float,default=45.);ap.add_argument('--tag',required=True)
    args=ap.parse_args();out=ROOT/('INVARIANT_CLOCK_COMPRESSION_SOURCE_'+args.tag+'_RESULT.json')
    cp=ROOT/('INVARIANT_CLOCK_COMPRESSION_SOURCE_'+args.tag+'_CHECKPOINT.json')
    if out.exists() or cp.exists():raise FileExistsError('exclusive result/checkpoint exists')
    if sha(Path(source.__file__))!=PARENT_SHA:raise ValueError('changed source equations')
    if sha(old.oracle.CAL)!=old.oracle.CALSHA:raise ValueError('changed calibration')
    cal=json.loads(old.oracle.CAL.read_text());saved=json.loads(old.oracle.base.SOURCE.read_text())
    saved['inherited']=cal['fixed'];reference=old.oracle.base.Model(saved,1)
    boundary=old.Boundary(reference)
    np.seterr(over='raise',divide='raise',invalid='raise')
    model=source.Polar(saved,args.nodes,args.extent,outer_callback=boundary);boundary.radius=model.r[-1]
    files=(Path(__file__),Path(old.__file__),Path(source.__file__),Path(source.old.__file__),
           Path(source.old.prev.__file__),Path(source.multiplier.__file__),Path(radial.__file__),
           Path(old.oracle.__file__),Path(old.oracle.base.__file__),old.oracle.base.SOURCE,old.oracle.CAL)
    hashes={str(p):sha(p) for p in files}
    started=time.monotonic();snaps=[];z=None;step=0;attempted=0;error=None;prep=None
    reason='requested_steps_completed';dt=args.dt_factor*(model.r[1]-model.r[0]);fluxint=np.zeros(2)
    boundary_error=old.maximum(np.array(boundary.at(0.,64))-np.array(boundary.at(0.,128)))
    def check_controls(snap):
        return [dict(name=k,error=v,gate=2e-12 if k=='inverse' else 1e-3)
                for k,v in snap['controls'].items() if v>(2e-12 if k=='inverse' else 1e-3)]
    def checkpoint():
        if z is not None:
            with cp.open('w') as file:json.dump(dict(hashes=hashes,args=vars(args),step=step,
                attempted_step=attempted,dt=dt,state=z.tolist(),ordinary_flux_integral=fluxint.tolist(),
                snapshots=snaps),file,allow_nan=False)
    def flux(y,g):
        return np.array([2*model.rest_flux(y[ni],g['N']*y[pi]/(g['A']**2*g[en]))[1][-1]
                         for ni,pi,en in ((4,5,'es'),(7,8,'eb'))])
    try:
        z,prep=old.initial(model,reference)
        first,g=old.diagnose(model,0.,z);snaps.append(first)
        if check_controls(first) or boundary_error>1e-10:
            reason='initial_control_failure';raise ValueError(str(check_controls(first)))
        for attempted in range(1,args.steps+1):
            if time.monotonic()-started>args.wall_seconds:
                reason='bounded_wall_checkpoint';break
            t=step*dt
            aa,ga=model.rhs(t,z,True);ya=z+dt*aa/2
            bb,gb=model.rhs(t+dt/2,ya,True);yb=z+dt*bb/2
            cc,gc=model.rhs(t+dt/2,yb,True);yc=z+dt*cc
            dd,gd=model.rhs(t+dt,yc,True)
            nextz=z+dt*(aa+2*bb+2*cc+dd)/6
            # Verify the prospective accepted endpoint before counting it.
            model.geometry(t+dt,nextz)
            fluxint+=dt*(flux(z,ga)+2*flux(ya,gb)+2*flux(yb,gc)+flux(yc,gd))/6
            z=nextz;step=attempted
            if step%64==0:
                snaps.append(old.diagnose(model,step*dt,z,False)[0]);checkpoint()
        if step>0:snaps.append(old.diagnose(model,step*dt,z,True)[0])
        if any(check_controls(s) for s in snaps):reason='final_numerical_control_failure'
    except Exception as exc:
        error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
        if reason=='requested_steps_completed':reason='technical_or_branch_failure'
        if z is not None and step>0:
            try:snaps.append(old.diagnose(model,step*dt,z,False)[0])
            except Exception as last:error['last_state_diagnostic_error']=str(last)
    checkpoint()
    failures=[dict(snapshot=i,**c) for i,s in enumerate(snaps) for c in check_controls(s)]
    result=dict(protocol=__doc__,inherited_preparation_protocol=old.__doc__,args=vars(args),hashes=hashes,
        reason=reason,error=error,steps=step,attempted_step=attempted,dt=dt,
        elapsed_seconds=time.monotonic()-started,preparation=prep,boundary_RK_error=boundary_error,
        snapshots=snaps,failed_numerical_controls=failures,ordinary_flux_integral=fluxint.tolist(),
        trajectory_qualified=False,outstanding='space/time/domain controls and full boundary/work accounting')
    with out.open('x') as file:json.dump(result,file,indent=2,allow_nan=False)
    print(json.dumps(dict(reason=reason,error=error,steps=step,attempted_step=attempted,
        time=step*dt,elapsed_seconds=result['elapsed_seconds'],failed_numerical_controls=failures,
        summaries=[{k:v for k,v in s.items() if k not in
        ('radius_over_L','gravity_excess','ordinary_bare_reference','force_ratio_to_bare_ordinary')} for s in snaps],
        result_sha256=sha(out)),indent=2),flush=True)
    if error or failures:raise SystemExit(1)

if __name__=='__main__':main()
