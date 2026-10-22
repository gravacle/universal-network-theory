#!/usr/bin/env python3
"""A298 legacy-API bridge. Review candidate, not campaign admission.

Normal path executes the original adapter's pinned pure function definitions
with its ORIGINAL __file__, review identity and proof producer unchanged.
Only A296 verdict admission uses the pinned saved-record validation core.
Existing custody is lazily derived through its unchanged API at caller time.
Importing this bridge reads no data and launches nothing. This review's tests
never call the live custody/driver context. All source loads authenticate bytes.
"""
import ast
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import types

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
CERT=ART/'calib_tail_readiness_cx2/certificates_per_point'
CORE_PATH=Path(__file__).parent/'point_response_admission_a296_cx2v002.py'
CORE_SHA='1a44bc59a5fc6a72c381d3c0c0875b6aa154c21fc108730d67c9ec529a39d9d7'
LEGACY_PATH=CERT/'point_response_admission_adapter_cx2v003.py'
LEGACY_SHA='4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'
CUSTODY_PATH=CERT/'custody_cx2v002.py'
CUSTODY_SHA='6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'
RESPONSE_PATH=CERT/'point_response_producer_cx2v002.py'
RESPONSE_SHA='a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
NEW_VERDICT='NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED'


def pinned(path,sha):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('EPS_BRIDGE_SOURCE_PIN_MISMATCH: '+str(path))
    return raw


def _core():
    # The bridge is the reviewed producer. Its immutable source pins the entire
    # core; therefore proof/review binding is to this bridge, not an unapproved
    # caller-provided producer name. Core has no import-time reads or launches.
    ns={'__file__':str(Path(__file__).absolute()),'__name__':'a296_core_in_bridge'}
    exec(compile(pinned(CORE_PATH,CORE_SHA),str(CORE_PATH),'exec'),ns)
    return types.SimpleNamespace(**ns)


def _custody():
    # Definitions + numpy imports only at module load; derive_details below is
    # the unchanged existing custody path, to run only in an authorized caller.
    raw=pinned(CUSTODY_PATH,CUSTODY_SHA)
    ns={'__file__':str(CUSTODY_PATH),'__name__':'a296_bridge_existing_custody'}
    exec(compile(raw,str(CUSTODY_PATH),'exec'),ns)
    return types.SimpleNamespace(**ns)


def _legacy(cu,core):
    source=pinned(LEGACY_PATH,LEGACY_SHA)
    definitions=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)]
    names={'_finite_tree','_number','_integer','_vector','_search','validate_numeric_candidates','adapt_eps'}
    if {n.name for n in definitions}!=names:raise ValueError('EPS_LEGACY_DEFINITION_SET_MISMATCH')
    pr_source=pinned(RESPONSE_PATH,RESPONSE_SHA)
    shell_nodes=[n for n in ast.parse(pr_source).body if isinstance(n,ast.FunctionDef) and n.name=='shell_plan']
    if len(shell_nodes)!=1:raise ValueError('EPS_SHELL_PLAN_DEFINITION_MISMATCH')
    pr_ns={'math':math}
    exec(compile(ast.Module(body=shell_nodes,type_ignores=[]),str(RESPONSE_PATH),'exec'),pr_ns)
    pr=types.SimpleNamespace(EPS_SCHEMA=core.EPS_SCHEMA,AUDIT_LO=core.PR.AUDIT_LO,CC=core.PR.CC,
        shell_plan=pr_ns['shell_plan'],utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat())
    core.source_pin(core.COMMON_PATH,core.COMMON_SHA)
    ns={'__file__':str(LEGACY_PATH),'math':math,'CU':cu,'PR':pr,'RESPONSE_SHA':RESPONSE_SHA}
    exec(compile(ast.Module(body=definitions,type_ignores=[]),str(LEGACY_PATH),'exec'),ns)
    return types.SimpleNamespace(**ns)


def adapt_eps(spec,numeric_ref,*,review_ref=None,approved_producer_sha256=(),approved_review_sha256=()):
    # Public signature matches the prior adapter exactly. No injectable custody
    # is exposed in this API: production calls derive it through pinned CU.
    try:
        core=_core()
        # Inspect the verdict without traversing the source producer imports.
        # Ordinary records still receive original CU.read_pin and exact old
        # validation behavior in the legacy branch below.
        core.check_pin(numeric_ref)
        raw=core.safe_path(numeric_ref['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=numeric_ref['sha256']:raise ValueError('byte pin mismatch')
        obj=json.loads(raw)
        cu=_custody()
        if isinstance(obj,dict) and obj.get('verdict')==NEW_VERDICT:
            details=cu.derive_details(spec=spec)
            return core.adapt_saved_eps(numeric_ref,expected_details=details,review_ref=review_ref,
                approved_producer_sha256=approved_producer_sha256,approved_review_sha256=approved_review_sha256)
        return _legacy(cu,core).adapt_eps(spec,numeric_ref,review_ref=review_ref,
            approved_producer_sha256=approved_producer_sha256,approved_review_sha256=approved_review_sha256)
    except (ValueError,KeyError,TypeError,OSError,OverflowError,AttributeError) as exc:
        return {'schema':'UNT_POINT_EPS_ADAPTER_RESULT_CX2V002',
            'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'TESTED',
            'verdict':'BLOCKED','blockers':[str(exc)],'proof':None,'driver_certificate':None}
