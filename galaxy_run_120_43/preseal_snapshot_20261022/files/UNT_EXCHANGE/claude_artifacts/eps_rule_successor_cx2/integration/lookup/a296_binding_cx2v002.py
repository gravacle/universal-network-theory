"""Explicit root-bound C1 compatibility gate; null templates always refuse.

The old six proof producers stay in their original order; only the pinned A296
bridge is added. Custody, enumerator, genesis and every other tail field stay
unchanged. A root-supplied C1/policy byte pin is required; none is invented here.
"""
from pathlib import Path

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OLD_C1={'path':str(ART/'c1_h1_c2/C1_H1_C2V001.json'),'sha256':'4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'}
GENESIS={'path':str(ART/'s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json'),'sha256':'2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319'}
EPS_ADAPTER={'path':str(ART/'eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py'),'sha256':'1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4'}
GUARD={'path':str(ART/'eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py'),'sha256':'3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25'}
AUTHORITY={'path':str(ART/'eps_rule_successor_cx2/A297_A298_AUTHORITY_CX2V001.json'),'sha256':'a672644bb0305356e46d93fa0fc76bbeab511a3b0952b11b0a1cdf49e7791694'}
SCHEMA='A296_CERTIFICATE_BINDING_CX2V001'
DRIVER_SHA='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'


def need(ok,reason):
    if not ok:raise ValueError('A296_BINDING_'+reason)


def validate_binding(s,ref):
    b=s.doc(ref)
    need(isinstance(b,dict) and set(b)=={'schema','status','c1','frozen_c1','genesis_registry','eps_adapter','guard','certificate_policy_review','authority'},'FIELDS')
    need(b['schema']==SCHEMA and b['status']=='ROOT_BOUND','UNBOUND_OR_SCHEMA')
    need(b['frozen_c1']==OLD_C1 and b['genesis_registry']==GENESIS,'FROZEN_LINEAGE')
    need(b['eps_adapter']==EPS_ADAPTER and b['guard']==GUARD and b['authority']==AUTHORITY,'REVIEWED_SOURCE_PINS')
    need(b['c1'] is not None and b['certificate_policy_review'] is not None and b['c1']!=OLD_C1,'NEW_C1_AND_POLICY_REQUIRED')
    old=s.doc(OLD_C1)['tail_readiness']
    current=s.doc(b['c1'])
    tr=current.get('tail_readiness')
    need(isinstance(tr,dict) and set(tr)==set(old),'TAIL_FIELDS_CHANGED')
    need(all(tr[k]==v for k,v in old.items() if k not in ('approved_certificate_producers','certificate_policy_review')),'FROZEN_TAIL_FIELD_CHANGED')
    approved=old['approved_certificate_producers']+[EPS_ADAPTER]
    need(len(old['approved_certificate_producers'])==6 and tr['approved_certificate_producers']==approved,'EXACT_OLD_SIX_PLUS_A296_ADAPTER_REQUIRED')
    need(tr['certificate_policy_review']==b['certificate_policy_review'],'POLICY_PIN_MISMATCH')
    for pin in (GENESIS,EPS_ADAPTER,GUARD,AUTHORITY,tr['custody_deriver'],tr['state_enumerator'],*approved):
        s.read(pin)
    review=s.doc(b['certificate_policy_review'])
    need(review.get('schema')=='DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001' and review.get('status')=='TESTED' and review.get('ok') is True,'POLICY_NOT_TESTED_PASS')
    want={'driver_sha256':DRIVER_SHA,'custody_deriver':tr['custody_deriver'],'state_enumerator':tr['state_enumerator'],
          'approved_certificate_producers':approved,'guard_sha256':GUARD['sha256'],
          'driver_slot_rule':'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE',
          'post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
    need(all(review.get(k)==v for k,v in want.items()),'POLICY_BINDING_MISMATCH')
    return {'binding':dict(ref),'document':b,'c1':dict(b['c1']),'tail_readiness':tr,'policy_review':review}
