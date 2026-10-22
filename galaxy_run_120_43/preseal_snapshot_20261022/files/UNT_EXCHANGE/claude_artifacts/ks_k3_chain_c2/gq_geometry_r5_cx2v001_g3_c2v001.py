"""G3 geometry (ks_k3_chain_c2 G-wave c2v001; root A175, A176): gq_geometry_r5_cx2v001 (c6ffb338) with the spec's kept
K in place of the literal 4 of L39, for S1_UA_C3T only.

S1_UA_C3T = KS1's gate (the S1 template's C3T label AND composite_grid_spec equal to CB C3T's, case block 76309ae3,
bitwise). For it, produce() is c6ffb338's computation with one substitution: the kept region of the kperp node grid is
kept_region('route_a', None, K/KPC_M) with K = the spec's kept K (max breaks_inverse_kpc = 3; KS2 kept_k), so the
production nodes are the K=3 grid's (B = {0, 3, 3 sqrt2, K_big}). Custody is KS1 (c6ffb338 L18-26 derived it with
6810b7c3, which refuses the +-3 cube); the record's producer and custody_deriver pins name this file and KS1. Every other
spec is handed to the unchanged c6ffb338 module object (P, by path and sha): its record, pins included, is c6ffb338's.
Edits: this docstring head, the custody pin lines (KS1) plus the predecessor and kept_k() after them, the first line of
produce(), and L39.

Independent exact-point all-column GQ bound; static computation only.

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
CP=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/custody_cx2v002_ks1_c2v001.py')   # G3: KS1 (it hands every other spec to 6810b7c3)
CS='ad020470aee354201ab6c68926784d75d3ebe2e16628323d49280bd2eb18aea6'
if hashlib.sha256(CP.read_bytes()).hexdigest()!=CS:raise ValueError('custody source pin')
sp=importlib.util.spec_from_file_location('g3gq_custody_ks1',CP)
C=importlib.util.module_from_spec(sp);sys.modules[sp.name]=C;sp.loader.exec_module(C)
# G3: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (P).
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_geometry_r5_cx2v001.py'),
             'c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G3: gq_geometry c6ffb338 pin mismatch')
_psp=importlib.util.spec_from_file_location('g3_predecessor_gq_geometry_r5_cx2v001',PREDECESSOR[0])
P=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=P;_psp.loader.exec_module(P)


def kept_k(spec):
    """G3: the spec's kept K, max(breaks_inverse_kpc) (KS2 kept_k). Only S1_UA_C3T reaches it: 3."""
    k=max(spec['numerics']['composite_grid_spec']['breaks_inverse_kpc'])
    if k!=C.S1_C3T_KEPT_K:raise ValueError('S1_UA_C3T kept K must be 3')
    return int(k)


def produce(spec,*,node_limit=None,progress=None):
    if not C.s1_c3t_spec(spec):return P.produce(spec,node_limit=node_limit,progress=progress)   # G3: c6ffb338's own code
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
    kept=U.kept_region('route_a',None,kept_k(spec)/U.KPC_M)   # G3: the kept K (3); c6ffb338 L39 had the literal 4
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
