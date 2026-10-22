"""A296 recorded-integrity branch; no producer truth or review authorization.

The caller's approved producer set is the inherited guard trust boundary. The
adapter/import stage must independently authorize review bytes. This validator
checks their exact binding, not authorship or membership in an approval registry.
No scientific module imports, source-array replay, launches, or writes occur.
"""
import hashlib
from pathlib import Path

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
CORE = {'path':str(ART/'eps_rule_successor_cx2/integration/point_response_admission_a296_cx2v002.py'),
        'sha256':'1a44bc59a5fc6a72c381d3c0c0875b6aa154c21fc108730d67c9ec529a39d9d7'}
BRIDGE = {'path':str(ART/'eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py'),
          'sha256':'1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4'}
TOP_MARKERS = {'a296_acceptance','successor_rule_verdict'}
ROW_MARKERS = {'accepted_negligible','acceptance','eps_measured_before_negligible_substitution','negligible_acceptance_evidence'}


def claims_a296(proof):
    return (bool(TOP_MARKERS.intersection(proof)) or proof.get('registered_discrete_verdict') == 'EPS_UNCERTIFIED' or
        proof.get('numerical_verdict') == 'NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED') or any(
        bool(ROW_MARKERS.intersection(row)) or row.get('refinement_failures') == 2
        for row in proof.get('shells',[]))


def _validate(proof, *, identity, custody, approved, read, allowed_roots):
    """Reconstruct numeric bytes and exact A296 proof projection; return byte pins.

    read is the guard's existing bounded root-scoped hash reader. Only this branch
    uses the pinned core's stricter parser and pre-traversal path exclusion. Each
    core call gets a private namespace, so the I/O binding cannot cross callers.
    """
    evidence = []
    def require(ok, reason):
        if not ok: raise ValueError(reason)
    raw = read(CORE, allowed_roots, False)
    namespace = {'__name__':'a296_guard_validation_core','__file__':CORE['path']}
    exec(compile(raw,CORE['path'],'exec'),namespace)
    safe_path, strict_json = namespace['safe_path'], namespace['strict_json']
    canonical = namespace['canonical']
    def same(a,b): return canonical(a) == canonical(b)
    def checked_read(pin, *, document=True):
        namespace['check_pin'](pin)
        safe_path(pin['path'])  # refuse forbidden lexical/symlink target before traversal
        data = read(pin,allowed_roots,False)
        if pin not in evidence: evidence.append(dict(pin))
        return (strict_json(data),data) if document else data
    namespace['read_pin'] = checked_read
    checked_read(CORE,document=False)
    require(proof.get('producer') == BRIDGE,'EPS_A296_PROOF_PRODUCER_MISMATCH')
    require(BRIDGE['sha256'] in approved,'EPS_A296_BRIDGE_NOT_INDEPENDENTLY_APPROVED')
    checked_read(BRIDGE,document=False)
    numeric_ref = proof.get('numeric_evidence')
    require(proof.get('driver_certificate') == numeric_ref,'EPS_A296_DRIVER_NUMERIC_PIN_MISMATCH')
    details = {'schema':'DDO154_POINT_CUSTODY_CX2V001','identity':identity,'custody':custody,
               'point_sha256':hashlib.sha256(canonical(identity)).hexdigest(),
               'custody_sha256':hashlib.sha256(canonical(custody)).hexdigest()}
    # The independently approved bridge pins this implementation closure. These
    # source hashes are not additional proof producers in C1, nor signer approvals.
    internal_sources = set(approved) | {namespace['RESPONSE_SHA'],namespace['RULE_SHA'],namespace['AUDIT_SHA']}
    numeric, rows, trace = namespace['validate_saved_numeric'](numeric_ref,
        expected_details=details,approved_producer_sha256=internal_sources,test_only=False)
    require(trace is not None,'EPS_A296_NUMERIC_ACCEPTANCE_MISSING')
    require(proof.get('registered_discrete_verdict') == 'EPS_UNCERTIFIED' and
            proof.get('successor_rule_verdict') == 'ACCEPTED_NEGLIGIBLE' and
            proof.get('numerical_verdict') == namespace['NEW_VERDICT'],
            'EPS_A296_PROOF_VERDICT_MISMATCH')
    require(same(proof.get('shells'),rows),'EPS_A296_PROOF_ROWS_MISMATCH')
    require(same(proof.get('a296_acceptance'),trace),'EPS_A296_PROOF_TRACE_MISMATCH')
    require(proof.get('rigorous_supremum') is False,'EPS_A296_NUMERICAL_CONVENTION_REQUIRED')
    review,_ = checked_read(proof.get('independent_review'))
    require(isinstance(review,dict) and review.get('schema') == 'UNT_POINT_EPS_REVIEW_CX2V001'
            and review.get('verdict') == 'APPROVED','EPS_A296_REVIEW_NOT_APPROVED')
    require(not review.get('test_fixture_only'),'EPS_A296_SYNTHETIC_REVIEW_NOT_ADMISSIBLE')
    require(review.get('numeric_ref') == numeric_ref and
            review.get('point_sha256') == details['point_sha256'] and
            review.get('custody_sha256') == details['custody_sha256'],
            'EPS_A296_REVIEW_BYTES_OR_SCOPE_MISMATCH')
    require(review.get('adapter_sha256') == BRIDGE['sha256'],'EPS_A296_REVIEW_ADAPTER_MISMATCH')
    require(review.get('accepts_registered_numerical_estimate_not_rigorous_sup') is True and
            review.get('accepts_a296_negligible_shells') is True and
            same(review.get('a296_acceptance'),trace),'EPS_A296_REVIEW_ACCEPTANCE_MISMATCH')
    # Rehash the complete consulted input set. This authenticates a stable byte
    # snapshot; it is not an assertion that the signer or scientific claim is true.
    for pin in tuple(evidence): checked_read(pin,document=False)
    return evidence


def validate(proof, *, identity, custody, approved, read, allowed_roots):
    try:
        return _validate(proof,identity=identity,custody=custody,approved=approved,
                         read=read,allowed_roots=allowed_roots)
    except (AttributeError,IndexError,RecursionError) as exc:
        raise ValueError('EPS_A296_MALFORMED_EVIDENCE: '+type(exc).__name__) from exc
