"""Successor of LO v001: additionally derive exact state configuration/grid.

v001 is retained byte-for-byte. Current-state admission now independently
checks normalized config SHA, certificate slots, physical domain, jet order,
all kp/kz/wkp/wz node bytes and I1-T before its numerical calculation.
Other algorithms are the pinned v001 implementation; no launch capability.
"""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE/'lo_core_r5_cx2v001.py'
BASE_SHA = '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'
import hashlib
if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
    raise ValueError('LO core pin mismatch')
sp=importlib.util.spec_from_file_location('cx2_lo_core_v001',BASE)
V1=importlib.util.module_from_spec(sp);sys.modules[sp.name]=V1;sp.loader.exec_module(V1)
PR, CU, CC = V1.PR, V1.CU, V1.CC
if CU.sha(PR.__file__) != 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231':
    raise ValueError('point response core pin mismatch')
source_bound_J = V1.source_bound_J
enforce_caps = V1.enforce_caps
aggregate_shares = V1.aggregate_shares
recompute_b1 = V1.recompute_b1
saved_b1_diagnostic = V1.saved_b1_diagnostic
produce_conditional_lo = V1.produce_conditional_lo


def validate_current_config(spec, record, arrays, U):
    raw=copy.deepcopy(spec['numerics']['uv_tail'])
    bound=True
    for key in ('eps_certificate','lo_certificate'):
        expected=raw[key]
        actual=record[key]
        if isinstance(expected,dict) or expected==U.TEST_ONLY_CERT:
            if expected != actual:
                raise ValueError('actual state certificate slot mismatch')
        else:
            bound=False
            raw[key]=actual
        if actual==U.TEST_ONLY_CERT:
            bound=False
    config=U.normalize_config(raw)
    if config['sha256'] != record.get('config_sha256'):
        raise ValueError('actual state normalized config SHA mismatch')
    wanted_kept=U.kept_region(record['stage_kind'],spec['numerics']['truncation'],4/U.KPC_M)
    if record.get('kept')!=wanted_kept or record.get('outer')!=config['outer']:
        raise ValueError('actual state kept/outer mismatch')
    dm=config['domain']
    wanted_domain={'R_eval_max_m':dm['R_eval_max_kpc']*U.KPC_M,
                   'z_eval_max_m':dm['z_eval_max_kpc']*U.KPC_M,
                   'z_src_max_m':dm['z_src_max_kpc']*U.KPC_M}
    if record.get('domain_m')!=wanted_domain or record.get('jet_order')!=config['jet_order']:
        raise ValueError('actual state domain/jet-order mismatch')
    if record.get('i1t',{}).get('verdict')!='PASS':
        raise ValueError('actual state I1-T not PASS')
    g=U._grid(wanted_kept,config['outer'],config['quadrature'],dm['R_eval_max_kpc'])
    for key in ('kp','kz','wkp','wz'):
        if not np.array_equal(np.asarray(arrays[key]),g[key]/U.KPC_M):
            raise ValueError('actual state exact production node mismatch: '+key)
    q=record.get('quadrature',{})
    if q.get('order')!=config['quadrature']['order'] or q.get('N_perp')!=len(g['kp']) or q.get('N_z_plus')!=len(g['kz']):
        raise ValueError('actual state quadrature metadata mismatch')
    return {'normalized_config_sha256':config['sha256'],'exact_production_nodes_verified':True,
            'physical_domain_and_jet_order_verified':True,'i1t_record_pass':True,
            'certificate_slots_bound':bound,
            'grid_arrays':{k:CU.array_record(arrays[k]) for k in ('kp','kz','wkp','wz')}}


def produce_current_lo(spec,state_ref,**kwargs):
    ctx=kwargs.pop('context',None) or PR.point_context(spec)
    obj=V1.reference(state_ref,schema=V1.STATE_SCHEMA)
    V1.scope(obj,ctx)
    tail=obj['tail_state'];record=V1.reference(tail['record'])
    CU.read_pin(tail['arrays'],document=False)
    with np.load(CU.allowed_path(tail['arrays']['path']),allow_pickle=False) as z:
        arrays={k:z[k] for k in ('kp','kz','wkp','wz')}
    U,_,_=CC.uvt_modules()
    validation=validate_current_config(spec,record,arrays,U)
    out=V1.produce_current_lo(spec,state_ref,context=ctx,**kwargs)
    out['producer']=CU.pin(__file__);out['core_producer']=CU.pin(BASE)
    out['state_configuration_validation']=validation
    if not validation['certificate_slots_bound']:
        out['blockers'].append('ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND')
        out['verdict']='BLOCKED'
    return out


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec',required=True);p.add_argument('--out',required=True)
    p.add_argument('--input-ref',required=True);p.add_argument('--expected-state')
    p.add_argument('--trusted-source-producer-sha',action='append',default=[])
    p.add_argument('--trusted-review-sha',action='append',default=[])
    p.add_argument('--settings',choices=tuple(PR.SETTINGS),default='registered')
    p.add_argument('--shells')
    a=p.parse_args();spec=json.loads(CU.allowed_path(a.spec).read_bytes())
    out=produce_current_lo(spec,json.loads(a.input_ref),
        expected_state=None if a.expected_state is None else json.loads(a.expected_state),
        trusted_source_producers=a.trusted_source_producer_sha,trusted_review_hashes=a.trusted_review_sha,
        settings=a.settings,shell_ranges=None if a.shells is None else json.loads(a.shells),
        progress=lambda x:print(json.dumps(x),flush=True))
    print(json.dumps(CU.write_new(a.out,out)))


if __name__=='__main__':main()
