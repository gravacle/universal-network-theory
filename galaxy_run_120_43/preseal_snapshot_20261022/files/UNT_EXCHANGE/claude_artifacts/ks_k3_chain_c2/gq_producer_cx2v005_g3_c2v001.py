"""G3 producer (ks_k3_chain_c2 G-wave c2v001; root A175, A176): gq_producer_cx2v005 (2832ceb9) over the G3 geometry
successor, for S1_UA_C3T only.

The kernel is gq_geometry_r5_cx2v001_g3_c2v001 (by path and sha, under a module name of its own: MAP H7); C is its
custody, KS1. produce() hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 2832ceb9 module object
(PRED, by path and sha), so its record, both producer pins included, is 2832ceb9's. For S1_UA_C3T it is 2832ceb9's code
over the G3 kernel: numeric_producer = the G3 geometry, producer = this file. policy() and signed_bound() take no spec
and read no K; they are 2832ceb9's text over KS1 (whose pin/read_pin are 6810b7c3's): equal outputs, the self-pin aside.
Edits: this docstring head, the kernel pin lines plus the predecessor after them, the first line of produce().

0528 policy facade over reviewed-correction candidate v002; static only.

No numerical kernel is changed. Every result states the adopted finite signed
branch. Root has not adopted a max-component normalization. Positive geometry
proofs are still conditional on reconstructed actual-source premises.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/gq_geometry_r5_cx2v001_g3_c2v001.py')   # G3: the geometry successor (c6ffb338 for every other spec)
S='572c86c6a9c49c8946c8be424644dd33932f2f1c3961623f15a036a1830a249b'
if hashlib.sha256(P.read_bytes()).hexdigest()!=S:raise ValueError('GQ kernel pin mismatch')
sp=importlib.util.spec_from_file_location('g3gq_policy_kernel_g3_for_v005',P)   # G3: a module name of its own (MAP H7)
K=importlib.util.module_from_spec(sp);sys.modules[sp.name]=K;sp.loader.exec_module(K)
C=K.C
# G3: the predecessor, unchanged, by path and sha (it loads c6ffb338 under its own name). Every other spec runs it.
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py'),
             '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G3: gq_producer 2832ceb9 pin mismatch')
_psp=importlib.util.spec_from_file_location('g3_predecessor_gq_producer_cx2v005',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
RULING={'path':'/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md',
        'sha256':'d11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83'}

def policy():
    C.read_pin(RULING,document=False)
    return {'ruling':RULING,'branch':'CONSERVATIVE_FINITE_DENOMINATOR',
            'signed_denominator_lower_bound':'abs(M_body-M_routeA)-z*(M_body+M_routeA)',
            'nonpositive_lower_bound':'UNAVAILABLE','max_component_alternative_adopted':False}

def signed_bound(column_bound,zero_error,body_mass,route_a_mass,*,normalizer='SIGNED_P0'):
    vals=(column_bound,zero_error,body_mass,route_a_mass)
    if any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in vals) or zero_error>=1:
        raise ValueError('invalid signed-bound inputs')
    tv=body_mass+route_a_mass;net=abs(body_mass-route_a_mass)
    if not math.isfinite(tv):raise ValueError('nonfinite derived total variation')
    lower=net-zero_error*tv
    if normalizer!='SIGNED_P0':
        result={'status':'UNTESTED','verdict':'BLOCKED','reason':'NORMALIZER_REJECTED_BY_0528'}
    elif lower<=0:
        result={'status':'TESTED','verdict':'BLOCKED','reason':'SIGNED_P0_LOWER_BOUND_NONPOSITIVE'}
    else:
        ratio=tv/lower
        if not math.isfinite(ratio):raise ValueError('nonfinite signed mass condition ratio')
        # Divide comparable mass scales first: b*TV can underflow even when
        # the dimensionless final bound is appreciable and fails the gate.
        value=column_bound*ratio
        if not math.isfinite(value):raise ValueError('nonfinite signed bound')
        result={'status':'TESTED','verdict':'PASS' if value<=1e-12 else 'INSUFFICIENT_BOUND',
                'conservative_bound':value,'threshold':1e-12}
    result.update(normalizer='SIGNED_P0',total_variation_mass=tv,signed_P0_mass=net,
                  denominator_lower_bound_mass=lower)
    result['signed_offset_policy']=policy()
    result['producer']=C.pin(__file__)
    result['numeric_producer']=C.pin(__file__)
    result['certificate_status']='NUMERICAL_BOUND_AVAILABLE' if result['verdict']=='PASS' else 'UNAVAILABLE'
    result['point_status']='PENDING_OTHER_CERTIFICATES' if result['verdict']=='PASS' else 'INCOMPLETE'
    if normalizer!='SIGNED_P0':result['reason']='NORMALIZER_REJECTED_BY_0528'
    return result

def produce(spec,*,node_limit=None,progress=None):
    if not C.s1_c3t_spec(spec):return PRED.produce(spec,node_limit=node_limit,progress=progress)   # G3: 2832ceb9's own code
    result=K.produce(spec,node_limit=node_limit,progress=progress)
    result['numeric_producer']=result['producer'];result['producer']=C.pin(__file__)
    result['signed_offset_policy']=policy()
    result['actual_source_premises']='UNAVAILABLE until own-call reconstruction verifies positivity, positive total zero mode, exact point/configuration and complete state inventory'
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--out',required=True);p.add_argument('--node-limit',type=int)
    a=p.parse_args();spec=json.loads(C.allowed_path(a.spec).read_bytes())
    print(json.dumps(C.write_new(a.out,produce(spec,node_limit=a.node_limit))))
