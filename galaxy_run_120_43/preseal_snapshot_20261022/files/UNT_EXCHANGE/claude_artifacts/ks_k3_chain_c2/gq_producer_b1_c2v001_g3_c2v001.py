"""G3 producer b1 (ks_k3_chain_c2 G-wave c2v001; root A175, A176): gq_producer_b1_c2v001 (3e668a2b) over the G3
geometry successor, for S1_UA_C3T only.

produce() is 3e668a2b's only K site (MAP H6): it hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged
3e668a2b module object (PRED, by path and sha), whose record is its own; for S1_UA_C3T it runs over the G3 kernel
(gq_geometry_r5_cx2v001_g3_c2v001, its own module name: MAP H7). policy() and signed_bound() take no spec and read no
K; they are 3e668a2b's text over KS1 (pin/read_pin are 6810b7c3's): equal outputs, the self-pin aside. Edits: this
docstring head, the kernel pin lines plus the predecessor after them, the first line of produce().

A134 (b1) successor of gq_producer_cx2v005: offset max-component normalization.

No numerical kernel is changed. On offset stages only, the signed GQ bound is
normalized by the larger component zero mode, bounded below by (1-z)*max(M_B,M_A),
so it is b*(M_B+M_A)/((1-z)*max(M_B,M_A)) <= 2b/(1-z). The 0528 item 1 signed-P0
denominator is superseded; the threshold 1e-12 is unchanged. produce() is unchanged
and the uniform GQ producer of record stays gq_producer_cx2v005. Positive geometry
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
sp=importlib.util.spec_from_file_location('g3gq_policy_kernel_g3_for_b1',P)   # G3: a module name of its own (MAP H7)
K=importlib.util.module_from_spec(sp);sys.modules[sp.name]=K;sp.loader.exec_module(K)
C=K.C
# G3: the predecessor, unchanged, by path and sha (it loads c6ffb338 under its own name). Every other spec runs it.
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/gq_producer_b1_c2v001.py'),
             '3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G3: gq_producer_b1 3e668a2b pin mismatch')
_psp=importlib.util.spec_from_file_location('g3_predecessor_gq_producer_b1_c2v001',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
RULING={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/OFFSET_B1_RULING_C2V001.json',
        'sha256':'9b49fd363991c1531a640212c22bda0561bed25e0a88ee35ca655464edd4dca6'}
SUPERSEDED={'ruling':{'path':'/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md',
        'sha256':'d11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83'},'item':1,'branch':'CONSERVATIVE_FINITE_DENOMINATOR'}

def policy():
    C.read_pin(RULING,document=False)
    return {'ruling':RULING,'branch':'MAX_COMPONENT_NORMALIZATION','scope':'OFFSET_STAGES_ONLY',
            'signed_denominator_lower_bound':'(1-z)*max(M_body,M_routeA)','bound_cap':'2*b/(1-z)',
            'nonpositive_lower_bound':'UNAVAILABLE','max_component_alternative_adopted':True,
            'superseded':SUPERSEDED}

def signed_bound(column_bound,zero_error,body_mass,route_a_mass,*,normalizer='MAX_COMPONENT'):
    vals=(column_bound,zero_error,body_mass,route_a_mass)
    if any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in vals) or zero_error>=1:
        raise ValueError('invalid signed-bound inputs')
    tv=body_mass+route_a_mass;largest=max(body_mass,route_a_mass)
    if not math.isfinite(tv):raise ValueError('nonfinite derived total variation')
    lower=(1-zero_error)*largest
    if normalizer!='MAX_COMPONENT':
        result={'status':'UNTESTED','verdict':'BLOCKED','reason':'NORMALIZER_REJECTED_BY_A134_B1'}
    elif lower<=0:
        result={'status':'TESTED','verdict':'BLOCKED','reason':'MAX_COMPONENT_LOWER_BOUND_NONPOSITIVE'}
    else:
        ratio=tv/largest/(1-zero_error)
        if not math.isfinite(ratio):raise ValueError('nonfinite signed mass condition ratio')
        # Divide comparable mass scales first: b*TV can underflow even when
        # the dimensionless final bound is appreciable and fails the gate.
        value=column_bound*ratio
        if not math.isfinite(value):raise ValueError('nonfinite signed bound')
        result={'status':'TESTED','verdict':'PASS' if value<=1e-12 else 'INSUFFICIENT_BOUND',
                'conservative_bound':value,'threshold':1e-12}
    result.update(normalizer='MAX_COMPONENT',total_variation_mass=tv,max_component_mass=largest,
                  denominator_lower_bound_mass=lower)
    result['signed_offset_policy']=policy()
    result['producer']=C.pin(__file__)
    result['numeric_producer']=C.pin(__file__)
    result['certificate_status']='NUMERICAL_BOUND_AVAILABLE' if result['verdict']=='PASS' else 'UNAVAILABLE'
    result['point_status']='PENDING_OTHER_CERTIFICATES' if result['verdict']=='PASS' else 'INCOMPLETE'
    if normalizer!='MAX_COMPONENT':result['reason']='NORMALIZER_REJECTED_BY_A134_B1'
    return result

def produce(spec,*,node_limit=None,progress=None):
    if not C.s1_c3t_spec(spec):return PRED.produce(spec,node_limit=node_limit,progress=progress)   # G3: 3e668a2b's own code
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
