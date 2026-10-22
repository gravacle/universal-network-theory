"""Synthetic tail-on and independent real-source spot check at three NGC rings; replay-only."""
import json,sys,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v001 as L
from independent_tail_spot_cxv001 import integral

def main():
    L.env();U,RS,PV=L.modules();jn=PV.create_provider()
    # Tail-on synthetic integration is separate from all program source records.
    class Gaussian:
        kind='synthetic';gas=None;stars=None
        def radial_factors(self,k,j0):return np.exp(-.5*(k*L.KPC)**2)[:,None]
        def vertical_factors(self,k,c):return np.exp(-.5*(k*L.KPC)**2)[:,None].astype(complex)
        def extent(self):return dict(R_src_max_m=5*L.KPC,gas_z_abs_max_m=0.,stars_24h_m=5*L.KPC)
        def record(self):return {'kind':'synthetic','name':'independent gaussian'}
        def digest(self):return 'synthetic_gaussian_spot_v001'
    cfg=U.normalize_config(dict(enabled=True,outer=dict(shape='cylinder',K_big_inverse_kpc=4.),
        source_rule='continuum_v001',gas=dict(interp='lagrange3_s_gl4',M_s=96),
        stars=dict(segment_rule='max16_ceil_kdr_plus8',tail_rule='t_panels_40a_phase1p5_gl12'),
        quadrature=dict(order=8,w_perp_max_inverse_kpc=.05,w_z_max_inverse_kpc=.05),
        domain=dict(R_eval_max_kpc=12.,z_eval_max_kpc=12.,z_src_max_kpc=5.),asymptote='EH_exact_minus_quarter',lapse_only=True,
        jet_order=dict(route_a=1,route_b=2,ngc_eval=1),lambda_scale=1.,eps_certificate='NONE_TEST_ONLY',lo_certificate='NONE_TEST_ONLY'))
    points=[(r*L.KPC,phi,z*L.KPC) for r,phi,z in ((1.5,.2,0.),(5.,.7,1.),(10.5,1.1,2.))]
    st=U.build(config=cfg,kept=dict(shape='cube',K_inverse_kpc=2.),roster=Gaussian(),gamma_eff=1.,c_m_s=1.,
        eval_radii_m=[],jn_provider=jn,i1t={'verdict':'NOT_APPLICABLE_SYNTHETIC'},stage_kind='ngc_ring_eval')
    xyz=np.array([[R*np.cos(phi),R*np.sin(phi),z] for R,phi,z in points])
    got=st.value(xyz);ref=integral(Gaussian(),jn.j0,1.,1.,points,big=4.,width_p=.025,width_z=.025,order=12)
    err=float(np.max(np.abs(got-ref))/max(np.max(np.abs(ref)),1e-300))
    rec=dict(label='TESTED_SYNTHETIC',points=points,module=got.tolist(),independent=ref.tolist(),relative_max=err,
        nonzero=bool(np.any(got!=0)),production_admissible=st.record['production_admissible'],passed=err<=1e-8 and bool(np.any(got!=0)))
    L.write('out/SYNTHETIC_TAIL_ON_V001.json',rec);print('synthetic',rec['passed'],err,flush=True)
    assert rec['passed']
    del st
    # Real NGC source: same declared source roster, distinct tail integrator, no new response solve.
    ctx,cols=L.ctx_with_tail(16.,'cube',False)
    ords=(1,7,15);points=[(cols[32*o]['R_m'],0.,0.) for o in ords]
    got=ctx.tail.value(np.array([[R,0.,z] for R,phi,z in points]));ros=L.source(RS)
    gamma=float.fromhex(json.loads((L.OP/'PREP.json').read_text())['fa_scalars']['gamma'])
    ref=integral(ros,jn.j0,gamma,ctx.c,points)
    err=float(np.max(np.abs(got-ref))/max(np.max(np.abs(ref)),1e-300))
    rec=dict(label='TESTED',ordinals=ords,points=points,module=got.tolist(),independent=ref.tolist(),relative_max=err,
        passed=err<=1e-8,scope='independent tail integration only; shared registered source roster and libm J0 source transform')
    L.write('out/INDEPENDENT_THREE_RINGS_V001.json',rec);print('real spots',rec['passed'],err,flush=True)
if __name__=='__main__':main()
