"""0515 GQ successor: exact v010r4 derive_geometry, all-column/all-kp replay.

This imports only inert libraries, computes static geometry and gas quadrature;
no forward/route-A/route-B executable is called and no new solve is performed.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
def imp(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
    return mod
B=imp(HERE/'box_replay_cx2v001.py','cx2_box_replay_readonly')
CC=B.CC
DRIVER=B.ART/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
assert CC.sha(DRIVER)=='b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
driver=imp(DRIVER,'cx2_geometry_driver_readonly')
start=time.monotonic(); co,points,base=B.setup()
base['producer']=B.pin(Path(__file__))
base['helper']=B.pin(HERE/'box_replay_cx2v001.py')
base['driver']=B.pin(DRIVER)
U,RS,PV=CC.uvt_modules();jn=PV.create_provider()
profile=B.load(Path(CC.PINS['profile'][0]));oldedges=np.asarray(profile['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'])
kept=U.kept_region('route_a',None,4/U.KPC_M)
quad={'order':8,'w_perp_max_inverse_kpc':.05,'w_z_max_inverse_kpc':.02}
grids={k:U._grid(kept,{'shape':'cylinder','K_big_inverse_kpc':float(k)},quad,14.2)['kp'] for k in (64,128)}
union=np.unique(np.concatenate(list(grids.values())))
cases=[]
for D in (4.04,co['distance_Mpc']['lower'],co['distance_Mpc']['upper']):
    derived,monotone,binding,record=driver.derive_geometry('DDO154',float(D),66.0)
    edges=np.asarray(derived['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'])
    # The registered driver bypasses derive_geometry at D4.04; compare exact edges.
    if D==4.04:assert np.array_equal(edges,oldedges)
    radii,rdr=RS.annulus_columns(edges,U.KPC_M);n=len(radii)
    args=dict(s_edges_kpc2=edges,kpc_m=U.KPC_M,column_R_m=radii,column_rdr_m2=rdr,
          present=np.ones(n,bool),elements_z=[np.zeros(1) for _ in range(n)],elements_m=[np.ones(1) for _ in range(n)])
    A=RS.GasColumns(M_s=64,**args);C=RS.GasColumns(M_s=128,**args)
    exact=2*math.pi*np.asarray(rdr)
    za=A.radial_factors(np.array([0.]),jn.j0)[0];zb=C.radial_factors(np.array([0.]),jn.j0)[0]
    zerr=float(max(np.max(np.abs(za/exact-1)),np.max(np.abs(zb/exact-1))))
    worst={k:{'raw':0.,'kp':None,'column_1based':None} for k in grids}
    for k0 in range(0,len(union),256):
        kp=union[k0:k0+256]
        vals=np.abs(A.radial_factors(kp/U.KPC_M,jn.j0)-C.radial_factors(kp/U.KPC_M,jn.j0))/exact
        for k,gg in grids.items():
            present=np.isin(kp,gg)
            if not present.any():continue
            vv=vals[present];idx=np.unravel_index(np.argmax(vv),vv.shape);v=float(vv[idx])
            if v>worst[k]['raw']:worst[k]={'raw':v,'kp':float(kp[present][idx[0]]),'column_1based':int(idx[1])+1}
        if k0%8192==0:print('GQ exact D %.8g kp %d/%d elapsed %.1fs'%(D,k0,len(union),time.monotonic()-start),flush=True)
    payload=json.dumps({'distance_Mpc':D,'inclination_deg':66.,'s_edges_kpc2':edges.tolist(),
       'column_R_m':np.asarray(radii).tolist(),'column_rdr_m2':np.asarray(rdr).tolist(),
       'kpc_m':U.KPC_M},sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    cases.append({'distance_Mpc':D,'kind':'headline' if D==4.04 else 'distance_box_endpoint',
       'geometry_sha256':hashlib.sha256(payload).hexdigest(),'geometry_encoding':'canonical JSON of distance/inclination/edges/radii/rdr/kpc; see producer',
       's_edges_kpc2':edges.tolist(),'driver_geometry_record':record,
       'rescaled_saved_edges_bitwise_equal':bool(np.array_equal(edges,oldedges*(D/4.04)**2)),
       'max_scaled_edges_absolute_diff_kpc2':float(np.max(np.abs(edges-oldedges*(D/4.04)**2))),
       'all_columns':n,'all_production_kperp':{str(k):len(v) for k,v in grids.items()},
       'zero_mode_relative_error':zerr,'M_s':64,'M_s_doubled':128,
       'worst':{str(k):dict(v,conservative_bound=v['raw']/(1-zerr),passes_threshold=v['raw']/(1-zerr)<=1e-12) for k,v in worst.items()},
       'scope':'All nonnegative element masses and arbitrary vertical positions, exact point radial geometry; not a source-state solve'})
    print('GQ exact completed',D,cases[-1]['worst'],flush=True)
base.update(status='TESTED_GEOMETRY_UNIFORM_ALL_PRODUCTION_NODES',cases=cases,
   profile=CC.pin('profile'),modules={k:CC.pin(k) for k in ('uvt_lapse','uvt_roster','uvt_jn')},
   quadrature=quad,R_eval_max_kpc=14.2,kept=kept,provider=jn.custody(),
   seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   limitations=['No claim over untested intermediate D; enforce exact geometry scope',
     'Actual roster nonnegative-mass premise must be checked before admission',
     'POSIX libm arithmetic; no analytic floating-point error proof beyond measured quadrature change',
     'This standalone proof is not automatically installed into a production certificate registry'])
h=B.write('BOX_GQ_EXACT_REPLAY_CX2V002.json',base)
print(json.dumps({'sha256':h,'seconds':base['seconds'],'rss':base['peak_rss_bytes']}))
