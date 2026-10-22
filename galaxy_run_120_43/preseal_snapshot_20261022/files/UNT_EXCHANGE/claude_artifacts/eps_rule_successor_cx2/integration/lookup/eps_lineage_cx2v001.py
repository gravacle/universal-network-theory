"""Pinned A296 numerical lineage only; no admission or policy approval.

Original provenance remains exact. A successor's digest is normalized to its
predecessor only after exact byte reconstruction from authenticated evidence.
No scientific producer is imported, no search is run and no file is written.
"""
from pathlib import Path
import hashlib
import json
import types

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
BASE_LOOKUP = {'path':str(ART/'direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py'),
               'sha256':'1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5'}
RULE = {'path':str(ART/'eps_rule_successor_cx2/rule/eps_negligible_rule_cx2v003.py'),
        'sha256':'669f0640b4a9e2a005e91245c27223499dc96a35189c6b4852a11a1e99190e3b'}
AUDIT_PRODUCER = {'path':str(ART/'eps_rule_successor_cx2/audit_path/dense_eps_audit_cx2v002.py'),
                  'sha256':'618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341'}
ORIGINAL_PRODUCER = {'path':str(ART/'calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py'),
                     'sha256':'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'}
AUTHORITY = {'path':str(ART/'eps_rule_successor_cx2/A296_AUTHORITY_CX2V001.json'),
             'sha256':'d1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92'}
VERDICT = 'NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED'


def need(ok, reason):
    if not ok:
        raise ValueError('A296_LINEAGE_' + reason)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def snapshot():
    # Fixed inert metadata module supplies its reviewed path/snapshot fence.
    raw = Path(BASE_LOOKUP['path']).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==BASE_LOOKUP['sha256'], 'SNAPSHOT_SOURCE_PIN')
    module = types.ModuleType('_a296_frozen_lookup_snapshot')
    module.__file__ = BASE_LOOKUP['path']
    exec(compile(raw,BASE_LOOKUP['path'],'exec'),module.__dict__)
    return module.Snapshot()


def authenticate_successor(numeric_ref, snapshot=None):
    """Return (record,evidence), validating bytes but granting no admission."""
    s = snapshot if snapshot is not None else globals()['snapshot']()
    raw = s.read(numeric_ref)
    record = s.doc(numeric_ref)
    need(record.get('verdict')==VERDICT and record.get('producer')==RULE,'SUCCESSOR_VERDICT_OR_PRODUCER')
    need(record.get('registered_discrete_verdict')=='EPS_UNCERTIFIED','DISCRETE_HISTORY')
    authority = record.get('rule_authority')
    need(authority==dict(AUTHORITY,heading='A296'),'AUTHORITY')
    for ref in (RULE,AUDIT_PRODUCER,ORIGINAL_PRODUCER,AUTHORITY):
        s.read(ref)
    predecessor = record.get('predecessor')
    need(isinstance(predecessor,dict) and predecessor.get('producer')==ORIGINAL_PRODUCER,'PREDECESSOR_PRODUCER')
    old_ref = predecessor.get('record')
    old = s.doc(old_ref)
    need(old.get('producer')==ORIGINAL_PRODUCER,'ORIGINAL_PRODUCER')
    need(old.get('identity')==record.get('identity') and old.get('point_sha256')==record.get('point_sha256'),'POINT_IDENTITY')
    accepted = record.get('accepted_shells')
    need(isinstance(accepted,list) and len(accepted)==1,'ONE_ACCEPTED_SHELL_REQUIRED')
    shells = record.get('shells')
    need(isinstance(shells,list),'SHELL_LIST')
    chosen = [sh for sh in shells if isinstance(sh,dict) and sh.get('range_inverse_kpc')==accepted[0]]
    need(len(chosen)==1,'ACCEPTED_SHELL_RANGE')
    audit_ref = (chosen[0].get('negligible_acceptance_evidence') or {}).get('dense_audit')
    audit = s.doc(audit_ref)
    need(audit.get('audit_producer')==AUDIT_PRODUCER,'AUDIT_PRODUCER')
    # This is the new isolated stdlib-only arithmetic tool, never the original
    # EPS producer or audit search. Its main is guarded and is not called.
    R = s.module(RULE,'_a296_pinned_saved_record_rule')
    result, reconstructed = R.reevaluate(old,audit,record_pin=old_ref,audit_pin=audit_ref,
        audit_producer_pin=AUDIT_PRODUCER,successor_producer=RULE,date_u=record.get('successor_date_u'))
    need(result.get('status')==VERDICT and reconstructed is not None,'RULE_REFUSED')
    expected = (json.dumps(reconstructed,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    need(raw==expected,'SUCCESSOR_BYTES_NOT_EXACT_RECONSTRUCTION')
    original_digest = digest({'dependencies':old.get('dependencies'),'producer':old.get('producer')})
    actual_digest = digest({'dependencies':record.get('dependencies'),'producer':record.get('producer')})
    return record, {'mode':'A296_AUTHENTICATED_SUCCESSOR','numeric_record':dict(numeric_ref),
        'predecessor_record':dict(old_ref),'dense_audit':dict(audit_ref),'rule':dict(RULE),
        'audit_producer':dict(AUDIT_PRODUCER),'original_producer':dict(ORIGINAL_PRODUCER),
        'authority':dict(AUTHORITY),'accepted_shells':accepted,
        'normalized_source_pins_digest':original_digest,'actual_source_pins_digest':actual_digest,
        'admission':'NOT_GRANTED_NUMERICAL_LINEAGE_ONLY'}


def source_provenance(numeric_ref, genesis_digest, snapshot=None):
    """Return exact normal digest, or authenticated predecessor digest and trace."""
    s = snapshot if snapshot is not None else globals()['snapshot']()
    record = s.doc(numeric_ref)
    actual = digest({'dependencies':record.get('dependencies'),'producer':record.get('producer')})
    if actual==genesis_digest:
        return {'mode':'ORIGINAL_EXACT_SOURCE_DIGEST','numeric_record':dict(numeric_ref),
                'normalized_source_pins_digest':actual,'actual_source_pins_digest':actual}
    _, evidence = authenticate_successor(numeric_ref,snapshot=s)
    need(evidence['normalized_source_pins_digest']==genesis_digest,'PREDECESSOR_SOURCE_DRIFT_FROM_GENESIS')
    return evidence
