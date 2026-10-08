"""No-evolution control for algebraically identical prefix quadrature.

Gate 1e-12 relative to the absolute-integral envelope, on smooth, signed,
cancellation-sensitive and saved physical fields. New mesh preserves all
old nodes through10L exactly; source/initial-state changes stay below the
existing 1e-3 gate. This does not accept a subsequent buffered trajectory.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_polar_source_v005 as old
import invariant_clock_polar_source_v006 as new

BASE=Path(__file__).resolve().parent


def main():
    beg=time.monotonic();saved=json.loads(old.prev.inherited.SOURCE.read_text())
    model=old.Polar(saved,960,.012);z0=model.initial()
    cp_path=BASE/'INVARIANT_CLOCK_POLAR_SOURCE_MIXED04_CHECKPOINT.json'
    cp=json.loads(cp_path.read_text());z=np.array(cp['state'])
    g=model.geometry(cp['step']*cp['dt'],z);r=model.r;L=model.L
    rows=[]
    for name,parity,power,W,fields in (
        ('mass',1,2,model.massint,[np.ones_like(r),np.cos(r/L),np.cos(r/L)-.9999,g['rhoC']+g['rhoB']]),
        ('lapse',-1,0,model.lapseint,[r/L,np.sin(r/L),np.sin(r/L)-r/L,g['g']])):
        operator=new.PrefixQuadrature(r,parity,power)
        for index,f in enumerate(fields):
            dense=W@f;prefix=operator@f
            envelope=max(float(np.max(abs(W)@abs(f))),1e-30)
            rows.append(dict(name=name,input=index,relative_error=float(np.max(abs(dense-prefix)))/envelope))
    buffered=new.Polar(saved,960,.012,.125,600.);bz=buffered.initial()
    same=np.array_equal(model.r[model.mask],buffered.r[buffered.mask])
    peak=model.initial_peak
    scale=np.array([1e-10,1e-8,1e-12,model.bg0[3]*1e-8,peak*1e-8,1e-12,1e-14,1e-8,1e-10])
    initial_error=np.max(abs(z0[:,model.mask]-bz[:,buffered.mask]),axis=1)/np.maximum(np.max(abs(z0[:,model.mask]),axis=1),scale)
    bg=buffered.geometry(0.,bz);ref=model.geometry(0.,z0)
    force_error=float(np.max(abs(bg['g'][buffered.mask]-ref['g'][model.mask])))/float(np.max(abs(ref['g'][model.mask])))
    diagnosis=buffered.diagnose(0.,bz)
    speed=diagnosis['max_characteristic_rest_speed']
    dx=model.dxgrid;symbol_max=1.37222197980336
    result=dict(protocol=__doc__,quadrature=rows,exact_inner_nodes=same,
        initial_state_relative=initial_error.tolist(),initial_force_relative=force_error,
        buffered_nodes=buffered.n,actual_extent=buffered.extent,cap=.125,buffer=600.,
        ray_distance_in_L=speed*.25*buffered.tdyn/L,
        original_kL1_turn_radius_over_L=symbol_max/dx,
        original_kL1_roundtrip_over_tdyn=2*symbol_max*L/(dx*speed*model.tdyn),
        buffered_initial_diagnostics={k:v for k,v in diagnosis.items() if k not in ('state','r','A_inner','gravity','theta')},
        checks=dict(prefix=max(row['relative_error'] for row in rows)<=1e-12,
                    identical_core_grid=same,initial_state=float(np.max(initial_error))<=1e-3,
                    initial_force=force_error<=1e-3),elapsed_seconds=time.monotonic()-beg,
        identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(old.__file__),Path(new.__file__),cp_path)})
    out=BASE/'INVARIANT_CLOCK_POLAR_MESH_AUDIT_V001_RESULT.json'
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False))


if __name__=='__main__':main()
