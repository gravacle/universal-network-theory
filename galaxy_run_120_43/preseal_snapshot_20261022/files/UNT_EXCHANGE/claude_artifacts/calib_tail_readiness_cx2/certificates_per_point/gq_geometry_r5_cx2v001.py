"""Independent exact-point all-column GQ bound; static computation only.

The measured Ms-versus-2Ms quadrature difference is bounded uniformly over
positive source elements and arbitrary vertical positions. This is the
registered numerical comparison, not an analytic floating-point enclosure.
Signed-source normalization is reported separately and never silently changed.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
CP=HERE/'custody_cx2v002.py'
CS='6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'
if hashlib.sha256(CP.read_bytes()).hexdigest()!=CS:raise ValueError('custody source pin')
sp=importlib.util.spec_from_file_location('cx2gq_custody',CP)
C=importlib.util.module_from_spec(sp);sys.modules[sp.name]=C;sp.loader.exec_module(C)


def produce(spec,*,node_limit=None,progress=None):
    begin=time.monotonic();details=C.derive_details(spec=spec)
    driver,cc=C.libraries();U,RS,PV=cc.uvt_modules();jn=PV.create_provider()
    uv=spec['numerics']['uv_tail'];Kbig=float(uv['outer']['K_big_inverse_kpc']);ms=uv['gas']['M_s']
    if type(ms) is not int or ms<1:raise ValueError('invalid gas quadrature order')
    edges=np.asarray(details['geometry']['profile']['HI_plus_He']['s_edges_kpc2'])
    radii,rdr=RS.annulus_columns(edges,U.KPC_M);n=len(radii)
    if np.any(rdr<=0):raise ValueError('nonpositive annulus weight')
    args=dict(s_edges_kpc2=edges,kpc_m=U.KPC_M,column_R_m=radii,column_rdr_m2=rdr,
              present=np.ones(n,bool),elements_z=[np.zeros(1) for _ in range(n)],elements_m=[np.ones(1) for _ in range(n)])
    a=RS.GasColumns(M_s=ms,**args);b=RS.GasColumns(M_s=2*ms,**args)
    exact=2*math.pi*np.asarray(rdr)
    z=max(float(np.max(np.abs(a.radial_factors(np.array([0.]),jn.j0)[0]/exact-1))),
          float(np.max(np.abs(b.radial_factors(np.array([0.]),jn.j0)[0]/exact-1))))
    kept=U.kept_region('route_a',None,4/U.KPC_M)
    allkp=U._grid(kept,uv['outer'],uv['quadrature'],uv['domain']['R_eval_max_kpc'])['kp']
    if node_limit is not None and (type(node_limit) is not int or node_limit<1):raise ValueError('invalid smoke limit')
    kp=allkp if node_limit is None else allkp[:node_limit]
    worst={'value':0.0,'kp_inverse_kpc':None,'column_1based':None}
    for i in range(0,len(kp),128):
        block=kp[i:i+128]
        delta=np.abs(a.radial_factors(block/U.KPC_M,jn.j0)-b.radial_factors(block/U.KPC_M,jn.j0))/exact
        j=np.unravel_index(np.argmax(delta),delta.shape);value=float(delta[j])
        if value>worst['value']:worst={'value':value,'kp_inverse_kpc':float(block[j[0]]),'column_1based':int(j[1])+1}
        if progress and i%4096==0:progress(i,len(kp))
    full=len(kp)==len(allkp);bound=worst['value']/(1-z) if z<1 else None
    ok=full and bound is not None and math.isfinite(bound) and bound<=1e-12
    return {'schema':'UNT_CALIBRATION_POINT_PROOF_CX2V001','gate':'GQ','status':'TESTED' if full else 'UNTESTED',
      'verdict':'PASS' if ok else ('FAIL' if full else 'INCOMPLETE'),
      'point_sha256':details['point_sha256'],'custody_sha256':details['custody_sha256'],
      'producer':C.pin(__file__),'custody_deriver':C.pin(CP),
      'method':'GEOMETRY_UNIFORM_COLUMN_BOUND','all_columns_included':True,
      'all_production_kperp_nodes':full,'nonnegative_masses_required':True,
      'M_s':ms,'M_s_doubled':2*ms,'K_big_inverse_kpc':Kbig,
      'max_column_difference_over_analytic_Pi0':worst['value'],'max_zero_mode_relative_error':z,
      'conservative_bound':bound,'threshold':1e-12,'worst':worst,
      'columns':n,'nodes_tested':len(kp),'production_nodes':len(allkp),
      'geometry_sha256':details['custody']['geometry_sha256'],'quadrature':uv['quadrature'],
      'provider':jn.custody(),'seconds':time.monotonic()-begin,
      'scope':'Exact point geometry/configuration; all nonnegative element masses; arbitrary vertical positions. Signed offsets require a separate proof and reviewed guard successor.',
      'proof':'Triangle inequality: |delta S| <= c^2 sum_i M_i max_k |Pi_M-Pi_2M|/Pi0_analytic; divide by positive zero mode >= (1-z)c^2 sum_i M_i. Stars cancel in this gas-only comparison.',
      'limitation':'Floating arithmetic and sampled production nodes; not an analytic quadrature-error theorem. No run was launched.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--out',required=True);p.add_argument('--node-limit',type=int)
    a=p.parse_args();spec=json.loads(C.allowed_path(a.spec).read_bytes())
    result=produce(spec,node_limit=a.node_limit,progress=lambda i,n:print('GQ nodes %d/%d'%(i,n),flush=True))
    print(json.dumps(C.write_new(a.out,result)))
