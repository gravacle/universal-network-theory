"""Fail-closed EPS numerical-record -> guard proof / real driver-slot adapter.

The numerical JSON is a distinct existing file with real shell values. Its
byte reference becomes driver_certificate. The guard proof references it;
neither file hashes itself. Caller must independently trust the numerical
producer, THIS adapter, and an explicit scientific review of these bytes.
Smoke/subset data cannot pass even if a purported reviewer approves it.
This is certificate conversion, never scientific launch authorization.
"""
import hashlib
import importlib.util
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
RESPONSE=HERE/'point_response_producer_cx2v002.py'
RESPONSE_SHA='a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
if hashlib.sha256(RESPONSE.read_bytes()).hexdigest()!=RESPONSE_SHA:
    raise ValueError('response producer pin mismatch')
sp=importlib.util.spec_from_file_location('cx2_eps_admission_response',RESPONSE)
PR=importlib.util.module_from_spec(sp);sys.modules[sp.name]=PR;sp.loader.exec_module(PR)
CU=PR.CU


def adapt_eps(spec,numeric_ref,*,review_ref=None,approved_producer_sha256=(),approved_review_sha256=()):
    out={'schema':'UNT_POINT_EPS_ADAPTER_RESULT_CX2V001','utc':PR.utc(),'status':'TESTED',
         'verdict':'BLOCKED','blockers':[],'proof':None,'driver_certificate':None}
    try:
        details=CU.derive_details(spec=spec)
        obj=CU.read_pin(numeric_ref)
        if obj.get('schema')!=PR.EPS_SCHEMA or obj.get('gate')!='EPS':
            raise ValueError('EPS_NUMERICAL_SCHEMA_MISMATCH')
        if obj.get('identity')!=details['identity'] or obj.get('custody')!=details['custody']:
            raise ValueError('EPS_NUMERICAL_POINT_CUSTODY_MISMATCH')
        if obj.get('status')!='TESTED' or obj.get('settings')!='registered' or obj.get('full_registered_search_executed') is not True:
            raise ValueError('FULL_REGISTERED_POINT_EPS_UNTESTED')
        if obj.get('coverage_complete') is not True or obj.get('registered_discrete_verdict')!='CERTIFIED':
            raise ValueError('EPS_DISCRETE_RULE_OR_COVERAGE_FAILED')
        approved=set(approved_producer_sha256)
        if obj.get('producer',{}).get('sha256') not in approved or CU.sha(__file__) not in approved:
            raise ValueError('NUMERICAL_PRODUCER_OR_ADAPTER_NOT_INDEPENDENTLY_APPROVED')
        CU.read_pin(obj['producer'],document=False)
        if obj['producer']['sha256']!=RESPONSE_SHA:
            raise ValueError('UNSUPPORTED_NUMERICAL_PRODUCER')
        if not review_ref or review_ref.get('sha256') not in set(approved_review_sha256):
            raise ValueError('INDEPENDENT_NUMERICAL_EPS_REVIEW_MISSING')
        review=CU.read_pin(review_ref)
        if review.get('schema')!='UNT_POINT_EPS_REVIEW_CX2V001' or review.get('verdict')!='APPROVED':
            raise ValueError('EPS_REVIEW_NOT_APPROVED')
        if review.get('numeric_ref')!=numeric_ref or review.get('point_sha256')!=details['point_sha256'] or review.get('custody_sha256')!=details['custody_sha256']:
            raise ValueError('EPS_REVIEW_EXACT_BYTES_OR_SCOPE_MISMATCH')
        if review.get('accepts_registered_numerical_estimate_not_rigorous_sup') is not True:
            raise ValueError('EPS_REVIEW_NUMERICAL_CONVENTION_UNRESOLVED')
        if review.get('adapter_sha256')!=CU.sha(__file__):
            raise ValueError('EPS_REVIEW_ADAPTER_MISMATCH')
        required,_,edge=PR.shell_plan(spec)
        rows=obj.get('shells',[])
        if [r.get('range_inverse_kpc') for r in rows]!=required:
            raise ValueError('EPS_ACTUAL_SHELL_COVERAGE_GAP')
        proofrows=[]
        for row,(lo,hi) in zip(rows,required):
            if row.get('lo_inverse_kpc')!=lo or row.get('hi_inverse_kpc')!=hi:
                raise ValueError('DRIVER_FIELD_BOUND_SHELL_KEYS_MISMATCH')
            nf=row.get('refinements')
            if type(nf) is not int or nf not in (0,1) or row.get('certified') is not True:
                raise ValueError('EPS_REFINEMENT_FAILURE')
            numbers=[row[k] for k in ('eps','eps_base','eps_refined','eps_envelope')]
            if any(type(x) not in (int,float) or not math.isfinite(x) or x<0 for x in numbers):
                raise ValueError('EPS_NONFINITE_OR_NEGATIVE')
            if row['eps_refined']>1.1*row['eps_base'] or row['eps']<max(row['eps_envelope'],row['eps_base'],row['eps_refined'],row['actual']['estimate']):
                raise ValueError('EPS_NUMERICAL_VALUES_INCONSISTENT')
            if row['envelope']['torus_m']!=12 or row['envelope']['direction_count']!=200:
                raise ValueError('EPS_REGISTERED_ENVELOPE_NOT_EXECUTED')
            proofrows.append({'range_inverse_kpc':[lo,hi],'eps':row['eps'],'eps_envelope':row['eps_envelope'],
                              'refinement_failures':nf})
        audit={a['range_inverse_kpc'][0]:a for a in obj.get('envelope_audit',[])}
        required_audits=[n for n in PR.AUDIT_LO if 4<=n<edge]
        if set(audit)!=set(required_audits):
            raise ValueError('EPS_DENSE_AUDIT_COVERAGE_INCOMPLETE')
        for a in audit.values():
            if a['dense_search']['torus_m']!=20 or a['dense_search']['direction_count']!=400:
                raise ValueError('EPS_DENSE_AUDIT_SETTINGS_MISMATCH')
        proof={'schema':'UNT_CALIBRATION_POINT_PROOF_CX2V001','gate':'EPS','utc':PR.utc(),
            'status':'TESTED','verdict':'PASS','point_sha256':details['point_sha256'],
            'custody_sha256':details['custody_sha256'],'producer':CU.pin(__file__),
            'driver_certificate':numeric_ref,'numeric_evidence':numeric_ref,'independent_review':review_ref,
            'envelope_rule':'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS','shells':proofrows,
            'rigorous_supremum':False,'scope':'Independently approved registered numerical convention, not rigorous continuous supremum'}
        out.update(verdict='READY_FOR_MANIFEST',proof=proof,driver_certificate=numeric_ref)
    except (ValueError,KeyError,TypeError,OSError,OverflowError) as e:
        out['blockers'].append(str(e))
    return out
