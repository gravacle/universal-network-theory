"""0528 typed-admission facade; v001/v002 remain immutable.

Fresh, completed calls only. Source evidence must trace to that call's own
archives. Missing evidence means certificate UNAVAILABLE / point INCOMPLETE;
prelaunch missing enforced/distinctly reviewed caps means NOT_ADMITTED.
No proof/driver adapter is invented for unavailable LO evidence.
"""
import hashlib
import importlib.util
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
CORE=HERE/'lo_producer_cx2v002.py'
CORE_SHA='1819667288c8b63178181c252541b4314abc7c4866b5aedad5e4cb7222cf93a5'
RULING=Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md')
RULING_SHA='d11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83'
if hashlib.sha256(CORE.read_bytes()).hexdigest()!=CORE_SHA or hashlib.sha256(RULING.read_bytes()).hexdigest()!=RULING_SHA:
    raise ValueError('LO successor/ruling byte pin mismatch')
sp=importlib.util.spec_from_file_location('cx2_lo_v002_for_v003',CORE)
V2=importlib.util.module_from_spec(sp);sys.modules[sp.name]=V2;sp.loader.exec_module(V2)
PR,CU=V2.PR,V2.CU


def finish(out,*,prelaunch=False):
    out['admission_facade']=CU.pin(__file__)
    out['ruling']=CU.pin(RULING)
    out['signed_GQ_branch']='CONSERVATIVE_FINITE_DENOMINATOR'
    out['signed_GQ_scope']='recorded root ruling only; GQ producer/guard handles normalization separately'
    out['execution_policy']={'fresh_calls_only':True,'resume_allowed':False,'retry_allowed':False,
                             'interrupted_route_a_invalid':True,'certificates_from_own_run_saved_states':True}
    out['certificate_status']='UNAVAILABLE'
    out['point_status']='NOT_ADMITTED' if prelaunch else 'INCOMPLETE'
    out['production_admissible']=False
    if not out.get('blockers'):
        out['blockers']=['LO_GUARD_AND_DRIVER_CERTIFICATE_ADAPTER_REVIEW_PENDING']
    out['verdict']='UNAVAILABLE'
    # Conditional numerical scope, if established by the core, is preserved
    # separately. It is never silently equated with admission.
    return out


def unavailable(ctx,reason,*,prelaunch=False):
    out=V2.V1.base(ctx,'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE' if prelaunch else 'CURRENT_SAVED_STATE')
    out.update(status='UNTESTED',blockers=[reason],numerical_envelope_executed=False)
    return finish(out,prelaunch=prelaunch)


def produce_current_lo(spec,state_ref=None,**kwargs):
    ctx=kwargs.pop('context',None) or PR.point_context(spec)
    if state_ref is None:
        return unavailable(ctx,'OWN_RUN_REQUIRED_STATE_ARCHIVE_UNAVAILABLE')
    try:
        obj=V2.V1.reference(state_ref,schema=V2.V1.STATE_SCHEMA)
        V2.V1.scope(obj,ctx)
        execution=obj.get('execution',{})
        keys={'fresh_call':True,'resumed':False,'retried':False,'route_a_completed_normally':True}
        if any(execution.get(k) is not v for k,v in keys.items()):
            return unavailable(ctx,'FRESH_COMPLETED_NO_RESUME_NO_RETRY_CALL_NOT_ESTABLISHED')
        root=CU.allowed_path(execution['run_root'])
        src=V2.V1.reference(obj['source_reconstruction'],schema='UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001')
        # TailState P/F may be reconstructed by static replay into a certificate
        # directory; its original source files must belong to this exact run.
        refs=src.get('source_files',[])
        if not refs:
            return unavailable(ctx,'OWN_RUN_SOURCE_ARCHIVES_UNAVAILABLE')
        for ref in refs:
            if not CU.allowed_path(ref['path']).is_relative_to(root):
                return unavailable(ctx,'CROSS_RUN_SOURCE_SUBSTITUTION_FORBIDDEN')
            CU.read_pin(ref,document=False)
        row=V2.V1.reference(obj['row_reference'],schema='UNT_POINT_LO_ROWS_CX2V001')
        row_refs=row.get('state_files',[])
        if not row_refs:
            return unavailable(ctx,'OWN_RUN_READOUT_STATE_ARCHIVES_UNAVAILABLE')
        for ref in row_refs:
            if not CU.allowed_path(ref['path']).is_relative_to(root):
                return unavailable(ctx,'CROSS_RUN_READOUT_SUBSTITUTION_FORBIDDEN')
            CU.read_pin(ref,document=False)
        out=V2.produce_current_lo(spec,state_ref,context=ctx,**kwargs)
        return finish(out)
    except (OSError,KeyError,ValueError,TypeError) as exc:
        return unavailable(ctx,'OWN_RUN_LO_INPUT_UNAVAILABLE_OR_INVALID: '+str(exc))


def produce_conditional_lo(spec,cap_ref=None,*,review_ref=None,**kwargs):
    ctx=kwargs.pop('context',None) or PR.point_context(spec)
    if review_ref is not None:
        try:
            review=CU.read_pin(review_ref)
            if review.get('distinct_from_producer_lane') is not True or not review.get('reviewer_lane'):
                return unavailable(ctx,'DISTINCT_LANE_CAP_REVIEW_UNAVAILABLE',prelaunch=True)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            return unavailable(ctx,'DISTINCT_LANE_CAP_REVIEW_INVALID: '+str(exc),prelaunch=True)
    return finish(V2.produce_conditional_lo(spec,cap_ref,review_ref=review_ref,context=ctx,**kwargs),prelaunch=True)


source_bound_J=V2.source_bound_J
enforce_caps=V2.enforce_caps
validate_current_config=V2.validate_current_config
