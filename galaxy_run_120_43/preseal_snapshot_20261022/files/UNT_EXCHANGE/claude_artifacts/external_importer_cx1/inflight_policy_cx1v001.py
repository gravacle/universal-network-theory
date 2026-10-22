"""0837 decision policy prototype; no polling, launches, writes or admission.
Inputs must be derived from authenticated registration/receipt/runtime evidence.
Unknown liveness or integrity never licenses a duplicate local launch.
"""
def decide(*, natural_plan_committed, registered, identity_bound,
           runtime_environment_bound, envelope_valid, direct_state,
           outcome=None, acceptance=None):
    if not natural_plan_committed:return 'REFUSE_BEFORE_NATURAL_PLAN'
    if not registered:return 'NORMAL_CAMPAIGN'
    if not identity_bound:return 'REFUSE_IDENTITY'
    if not runtime_environment_bound:return 'REFUSE_RUNTIME_ENVIRONMENT'
    if not envelope_valid:return 'REFUSE_ENVELOPE'
    if direct_state in ('REGISTERED_PENDING','RUNNING'):return 'WAIT_EXTERNAL'
    if direct_state=='UNKNOWN':return 'HOLD_UNKNOWN_EXTERNAL_STATE'
    if direct_state!='TERMINAL':return 'REFUSE_EXTERNAL_STATE'
    if outcome in ('CAP_UNCOUNTED','INFRA_UNCOUNTED'):return 'NORMAL_CAMPAIGN_UNCOUNTED_FALLBACK'
    if outcome=='COMPLETED_INVALID':return 'RETAIN_SPECULATIVE_INVALID_FOR_ROOT'
    if outcome!='COMPLETED_VALID':return 'HOLD_UNCLASSIFIED_OUTCOME'
    if acceptance in (None,'PENDING','INCOMPLETE'):return 'WAIT_ACCEPTANCE'
    if acceptance in ('ACCEPTED','ACCEPTED_PASS_FLAGGED'):return 'VALIDATE_EXACT_IMPORT'
    return 'RETAIN_FAILED_ACCEPTANCE_FOR_ROOT'
