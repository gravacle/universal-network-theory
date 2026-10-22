"""Finish certificate arithmetic and targeted rho check, using saved own LO integral."""
from pathlib import Path
import importlib.util
import math
import numpy as np
p=Path(__file__).with_name('review_certificates_cx3v003.py')
s=importlib.util.spec_from_file_location('cx3_cert_common',p);C=importlib.util.module_from_spec(s);s.loader.exec_module(C);C.sha(p)
ctx=C.Context();lo=C.read(C.CERT/'gates/LO_CERT_V002.json');mine=C.read(C.OUT/'LO_REVIEW_V001.json')
shell=next(s for s in lo['shells'] if s['range_inverse_kpc']==[64.,128.]);point=shell['rho_envelope_search']
q=np.r_[point['t_at'],point['dir_at'],point['k_at_inverse_kpc']];start=ctx.quantity(q,'RHO');best=start
# Check the producer extremum with independent production-module arithmetic,
# and attempt to refute it by an independently coded local coordinate search.
step=np.array([.04,.04,.04,.02,.02,.02,4.]);evaluations=1
for it in range(60):
    up=False
    for j in range(7):
        for sign in (-1,1):
            r=q.copy();r[j]+=sign*step[j];r[6]=np.clip(r[6],64,128);r[3:6]/=np.linalg.norm(r[3:6])
            value=ctx.quantity(r,'RHO');evaluations+=1
            if value>best:q=r;best=value;up=True
    if not up:step*=.5
    if max(step[:6])<1e-7:break
v=np.array([r['speed_km_s'] for r in ctx.res['passes'][-1]['rows']]);R=np.array(lo['R_kpc'])*ctx.kpc;tau=np.array(lo['tau_km_s'])
B1=mine['integrals'][-1]['B1'];rederived=float(max(v*R/tau)*best*B1/4)
eps=C.read(C.CERT/'gates/EPS_CERT_V006.json')
checks=dict(EPS_shells= len(eps['shells']),EPS_registered_convergence=all(s['refinements']<=1 and s['eps_refined']<=1.1*s['eps_base'] for s in eps['shells']),
    EPS_eps_max_equal=max(s['eps'] for s in eps['shells'])==eps['eps_max'],EPS_envelope_max_equal=max(s['eps_envelope'] for s in eps['shells'])==eps['envelope_bound']['eps_max_envelope_all_shells'],
    EPS_exact_coverage_P128=eps['coverage_inverse_kpc']['DDO'][1]>=math.sqrt(2)*256,
    EPS_exact_coverage_P64=eps['coverage_inverse_kpc']['DDO'][1]>=math.sqrt(2)*128,
    LO_exact_coverage_P128=lo['coverage_inverse_kpc'][1]>=math.sqrt(2)*256,
    LO_all_shells_below_per_shell_gate=all(s['max_over_tau']<=.005 for s in lo['shells']),
    LO_sum_below_gate=lo['summed_max_over_tau']<=.05,
    LO_sum_equal=math.isclose(sum(s['max_over_tau'] for s in lo['shells']),lo['summed_max_over_tau'],rel_tol=1e-15))
assert all(v for k,v in checks.items() if k!='EPS_shells')
lp=C.CERT/'tools/lo_cert_c2v002.py';source=lp.read_text();assert 'M_s=64' in source
C.write('CONTRACT_AND_LO_RHO_REVIEW_V001.json',dict(checks=checks,LO=dict(rho_at_producer_argmax=start,rho_after_own_local_search=best,record_rho=shell['rho_used'],rho_ratio=best/shell['rho_used'],
    source_point='producer rho_envelope_search, independently evaluated and locally perturbed; complements own blind search in LO_REVIEW_V001',evaluations=evaluations,
    rederived_max_over_tau=rederived,record_max_over_tau=shell['max_over_tau'],relative_difference=abs(rederived/shell['max_over_tau']-1),per_shell_threshold=.005,pass_gate=rederived<.005,
    source_M_s=64,producer={'path':str(lp),'sha256':C.sha(lp)},transfer_to_M_s128='UNTESTED: a quadrature change changes S_T and its absolute integral; no mathematical transfer bound is established by this record.'),
    low_shell_field_interpretation='EPS CERTIFIED is the registered convergence test. Every shell carries eps_envelope; first3 eps use actual-set values. The recorded envelope maximum agrees with own search, but eps_max is not the global torus-envelope maximum.',
    this_script={'path':__file__,'sha256':C.sha(__file__)}))
