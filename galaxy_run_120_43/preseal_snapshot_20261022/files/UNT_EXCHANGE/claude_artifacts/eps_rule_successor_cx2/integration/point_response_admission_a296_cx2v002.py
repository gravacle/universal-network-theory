#!/usr/bin/env python3
"""Review candidate: saved-record EPS proof adapter with an explicit A296 branch.

Not a drop-in CP1 adapter. Caller supplies independently derived expected_details
and independently approved source/review digests. Hashes establish bytes, never
root approval. No scientific computations, driver imports, custody derivation,
run discovery, file writes or command execution. Frozen C1/guards are unchanged.
A296 proofs deliberately retain refinement_failures=2 and fail old guards.
"""
import ast
import copy
import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import types

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
CERT = ART/'calib_tail_readiness_cx2/certificates_per_point'
RULE_PATH = ART/'eps_rule_successor_cx2/rule/eps_negligible_rule_cx2v003.py'
RULE_SHA = '669f0640b4a9e2a005e91245c27223499dc96a35189c6b4852a11a1e99190e3b'
AUTHORITY_PATH = ART/'eps_rule_successor_cx2/A296_AUTHORITY_CX2V001.json'
AUTHORITY_SHA = 'd1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92'
RESPONSE_PATH = CERT/'point_response_producer_cx2v002.py'
RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
LEGACY_PATH = CERT/'point_response_admission_adapter_cx2v003.py'
LEGACY_SHA = '4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'
COMMON_PATH = CERT/'certs_common_r5_cx2v001.py'
COMMON_SHA = 'c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7'
AUDIT_PATH = ART/'eps_rule_successor_cx2/audit_path/dense_eps_audit_cx2v002.py'
AUDIT_SHA = '618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341'
NEW_VERDICT = 'NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED'
OLD_PASS = 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED'
EPS_SCHEMA = 'UNT_POINT_EPS_NUMERICAL_CX2V001'
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
CUSTODY_KEYS = {'grid_sha256','background_sha256','geometry_sha256','modules_sha256','row_contract_sha256'}


def require(ok, reason):
    if not ok: raise ValueError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def serialized(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()


def strict_json(raw):
    def unique(items):
        result = {}
        for key, value in items:
            require(key not in result, 'EPS_DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError('EPS_NONFINITE_JSON_TOKEN')
    result = json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)
    _finite_tree(result)
    return result


def check_pin(ref):
    require(isinstance(ref,dict) and set(ref)=={'path','sha256'}, 'EPS_EXACT_BYTE_PIN_REQUIRED')
    require(isinstance(ref['path'],str) and bool(ref['path']), 'EPS_PIN_PATH_REQUIRED')
    require(isinstance(ref['sha256'],str) and re.fullmatch('[0-9a-f]{64}',ref['sha256']) is not None, 'EPS_PIN_SHA256_REQUIRED')


def safe_path(value):
    p = Path(value)
    def check(q,root=True):
        parts = q.parts
        require(q.is_absolute() and '..' not in parts, 'EPS_ABSOLUTE_NONTRAVERSING_PATH_REQUIRED')
        require(not any('.codex' == x or x.lower() in ('runs','runs_ext') or 'NGC3198' in x.upper() or
            'V007_POSTSEAL_RECORDS' in x or 'KMAX_A2F10_C5H_RUN_V001' in x or x.startswith('UVT_') for x in parts), 'EPS_FORBIDDEN_PATH')
        if root:
            require(str(q).startswith('/Users/bgm/Research/') or str(q).startswith('/Volumes/External1/'), 'EPS_RESEARCH_PATH_REQUIRED')
    check(p)
    # Resolve components incrementally, checking each symlink target before
    # continuing into it. In particular, do not stat a forbidden run target.
    seen = 0
    pending = list(p.parts[1:]); current = Path('/')
    while pending:
        current = current / pending.pop(0)
        check(current,root=False)
        if current.is_symlink():
            seen += 1
            require(seen <= 40, 'EPS_SYMLINK_CYCLE')
            target = current.readlink()
            if not target.is_absolute(): target = current.parent / target
            import os
            target = Path(os.path.normpath(str(target)))
            check(target)
            pending = list(target.parts[1:]) + pending
            current = Path('/')
    check(current)
    return current


def read_pin(ref, *, document=True):
    check_pin(ref)
    raw = safe_path(ref['path']).read_bytes()
    require(digest(raw)==ref['sha256'], 'EPS_BYTE_PIN_MISMATCH: '+ref['path'])
    return (strict_json(raw),raw) if document else raw


def source_pin(path, sha):
    ref={'path':str(path),'sha256':sha}
    read_pin(ref,document=False)
    return ref


def rule_functions():
    """Execute only pinned pure definitions; never execute main/import top levels."""
    raw = read_pin({'path':str(RULE_PATH),'sha256':RULE_SHA},document=False)
    tree = ast.parse(raw,filename=str(RULE_PATH))
    names = {'Refusal','require','digest','finite','epsilon','check_finiteness','sha_string',
             'pin','pair','strict_json','validate_record','validate_audit','reevaluate'}
    nodes = [n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    require({n.name for n in nodes}==names,'EPS_RULE_DEFINITION_SET_MISMATCH')
    ns = {'copy':copy,'hashlib':hashlib,'math':math,'re':re,'json':json,'M':10,'F':0.1,
        'ABSOLUTE_FLOOR':1e-6,'AUDIT_RATIO_MAX':1.05,'ORIGINAL_PRODUCER_SHA256':RESPONSE_SHA,
        'AUTHORITY_PATH':str(AUTHORITY_PATH),'AUTHORITY_SHA256':AUTHORITY_SHA,
        'NEW_VERDICT':NEW_VERDICT,'OLD_PASS':OLD_PASS,'AUDIT_SCHEMA':'UNT_EPS_NEGLIGIBLE_DENSE_AUDIT_CX2V001'}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(RULE_PATH),'exec'),ns)
    return types.SimpleNamespace(**ns)


def shell_k(lo,hi,per_decade):
    # Exact scalar arithmetic of pinned common shell_k. Only len() is consumed;
    # returning a list avoids importing numpy or the common module.
    j0=math.floor(math.log10(lo)*per_decade);j1=math.ceil(math.log10(hi)*per_decade)
    inner=[10**(j/per_decade) for j in range(j0,j1+1)]
    return [lo]+[x for x in inner if lo<x<hi]+[hi]


PR=types.SimpleNamespace(AUDIT_LO=(4,5,6,8,12,16,19,32,45,63,64,100,128,181),
    CC=types.SimpleNamespace(shell_k=shell_k,PER_DECADE={0:64,1:128,2:256,3:512}))


def _finite_tree(value):
    """Reject nonfinite numbers anywhere, including candidates hidden by max()."""
    if isinstance(value,dict):
        for v in value.values():_finite_tree(v)
    elif isinstance(value,list):
        for v in value:_finite_tree(v)
    elif type(value) is float and not math.isfinite(value):
        raise ValueError('EPS_NONFINITE_NUMERIC_FIELD')


def _number(value,name,*,nonnegative=True):
    if type(value) not in (int,float) or not math.isfinite(value) or (nonnegative and value<0):
        raise ValueError('EPS_INVALID_NUMERICAL_CANDIDATE: '+name)
    return value


def _integer(value,name,lower,upper=None):
    if type(value) is not int or value<lower or (upper is not None and value>upper):
        raise ValueError('EPS_INVALID_SEARCH_METADATA: '+name)
    return value


def _vector(value,name,*,unit=False,torus=False):
    if not isinstance(value,list) or len(value)!=3:
        raise ValueError('EPS_INVALID_VECTOR: '+name)
    for x in value:_number(x,name,nonnegative=False)
    if unit and not math.isclose(sum(x*x for x in value),1.,rel_tol=1e-10,abs_tol=1e-12):
        raise ValueError('EPS_NONUNIT_DIRECTION: '+name)
    if torus and any(x<0 or x>=2*math.pi for x in value):
        raise ValueError('EPS_TORUS_COORDINATE_OUTSIDE_CANONICAL_RANGE')


def _search(search,lo,hi,*,audit,first=False):
    if not isinstance(search,dict):raise ValueError('EPS_SEARCH_RECORD_MISSING')
    nt,nd=(20,400) if audit else (12,200)
    fractions=[0.,.25,.5,.75,1.] if audit else [0.,.5,1.]
    if type(search.get('torus_m')) is not int or type(search.get('direction_count')) is not int or search['torus_m']!=nt or search['direction_count']!=nd:
        raise ValueError('EPS_REGISTERED_SEARCH_DIMENSIONS_MISMATCH')
    if search.get('radial_fractions')!=fractions or any(type(x) not in (int,float) for x in search['radial_fractions']):
        raise ValueError('EPS_REGISTERED_RADIAL_FRACTIONS_MISMATCH')
    if _integer(search.get('n_grid'),'n_grid',1)!=len(fractions)*nd*nt**3:
        raise ValueError('EPS_SEARCH_GRID_COUNT_MISMATCH')
    # Exact output of this pinned producer: eight starts, plus the previous
    # shell for every subsequent production shell; sixteen audit starts.
    starts=16 if audit else (8 if first else 9)
    if _integer(search.get('starts'),'starts',1)!=starts:
        raise ValueError('EPS_REGISTERED_START_COUNT_MISMATCH')
    _integer(search.get('iterations'),'iterations',1,120)
    seed=20261018+int(lo*17+hi*29)+(100000 if audit else 0)
    if type(search.get('seed')) is not int or search['seed']!=seed:
        raise ValueError('EPS_REGISTERED_SEARCH_SEED_MISMATCH')
    _vector(search.get('dir_at'),'dir_at',unit=True)
    _vector(search.get('t_at'),'t_at',torus=True)
    k=_number(search.get('k_at_inverse_kpc'),'search k')
    if not lo<=k<=hi:raise ValueError('EPS_SEARCH_ARGMAX_OUTSIDE_SHELL')
    return [_number(search.get(k),k) for k in ('estimate','grid_max')]


def validate_numeric_candidates(obj,required,edge,*,accepted_range=None,acceptance_metadata=True):
    """Validate complete search metadata before constructing any proof."""
    _finite_tree(obj)
    rows=obj.get('shells',[])
    if not isinstance(rows,list) or [r.get('range_inverse_kpc') for r in rows]!=required:
        raise ValueError('EPS_ACTUAL_SHELL_COVERAGE_GAP')
    audits=obj.get('envelope_audit',[])
    wanted=[float(n) for n in PR.AUDIT_LO if 4<=n<edge]
    if not isinstance(audits,list) or len(audits)!=len(wanted):
        raise ValueError('EPS_DENSE_AUDIT_COUNT_OR_DUPLICATE')
    audit={}
    for entry in audits:
        pair=entry.get('range_inverse_kpc')
        if not isinstance(pair,list) or len(pair)!=2:
            raise ValueError('EPS_DENSE_AUDIT_RANGE_INVALID')
        lo,hi=pair
        _number(lo,'audit lo');_number(hi,'audit hi')
        if lo in audit:raise ValueError('EPS_DENSE_AUDIT_DUPLICATE')
        if hi!=lo+1 or lo not in wanted:
            raise ValueError('EPS_DENSE_AUDIT_RANGE_INVALID')
        audit[lo]=entry
    if set(audit)!=set(wanted):raise ValueError('EPS_DENSE_AUDIT_COVERAGE_INCOMPLETE')
    proofrows=[]
    for index,(row,(lo,hi)) in enumerate(zip(rows,required)):
        if row.get('lo_inverse_kpc')!=lo or row.get('hi_inverse_kpc')!=hi:
            raise ValueError('DRIVER_FIELD_BOUND_SHELL_KEYS_MISMATCH')
        nf=row.get('refinements')
        accepted = row.get('range_inverse_kpc') == accepted_range
        if accepted:
            if type(nf) is not int or nf != 2 or row.get('certified') is not False:
                raise ValueError('EPS_A296_DISCRETE_HISTORY_MISMATCH')
        elif type(nf) is not int or nf not in (0,1) or row.get('certified') is not True:
            raise ValueError('EPS_REFINEMENT_FAILURE')
        eps,base,ref,env=(_number(row.get(k),k) for k in ('eps','eps_base','eps_refined','eps_envelope'))
        if (ref>1.1*base) != accepted:raise ValueError('EPS_REFINEMENT_RULE_FAILED')
        levels=row.get('levels',{})
        keys={'0','1'} if nf==0 else {'0','1','2'}
        if set(levels)!=keys:raise ValueError('EPS_DISCRETE_LEVELS_MISMATCH')
        candidates=[base,ref,env]
        for key in sorted(keys):
            level=levels[key];lv=int(key);nd={0:26,1:52,2:104}[lv]
            nk=len(PR.CC.shell_k(lo,hi,PR.CC.PER_DECADE[lv]))
            if any(type(level.get(k)) is not int or level[k]!=n for k,n in (('n_dirs',nd),('n_k',nk),('n_samples',nd*nk))):
                raise ValueError('EPS_DISCRETE_SAMPLE_COUNT_MISMATCH')
            candidates.append(_number(level.get('eps'),'level eps'))
            _number(level.get('max_abs_imag_q'),'imag q')
            k=_number(level.get('k_at_max_inverse_kpc'),'discrete k')
            if not lo<=k<=hi:raise ValueError('EPS_DISCRETE_ARGMAX_OUTSIDE_SHELL')
            _vector(level.get('dir_at_max'),'discrete direction',unit=True)
        base_level = 1 if accepted else nf
        if base!=levels[str(base_level)]['eps'] or ref!=levels[str(base_level+1)]['eps']:
            raise ValueError('EPS_DISCRETE_VALUES_INCONSISTENT')
        if nf in (1,2) and levels['1']['eps']<=1.1*levels['0']['eps']:
            raise ValueError('EPS_UNNECESSARY_REFINEMENT_DECLARATION')
        actual=row['actual']
        av=[_number(actual.get(k),'actual '+k) for k in ('estimate','dense_max','local_max')]
        if av[0]!=max(av[1:]):raise ValueError('EPS_ACTUAL_VALUES_INCONSISTENT')
        expected_nodes=10000*len(PR.CC.shell_k(lo,hi,256))
        if type(actual.get('dense_nodes')) is not int or actual['dense_nodes']!=expected_nodes:
            raise ValueError('EPS_ACTUAL_DENSE_COUNT_MISMATCH')
        _integer(actual.get('iterations'),'actual iterations',1,120)
        _vector(actual.get('dir_at'),'actual direction',unit=True)
        k=_number(actual.get('k_at_inverse_kpc'),'actual k')
        if not lo<=k<=hi:raise ValueError('EPS_ACTUAL_ARGMAX_OUTSIDE_SHELL')
        candidates.extend(av)
        ev=_search(row['envelope'],lo,hi,audit=False,first=index==0)
        candidates.extend(ev);envelope_candidates=list(ev)
        if lo in audit:
            entry=audit[lo]
            production=_number(entry.get('production'),'audit production')
            dense=_number(entry.get('dense'),'audit dense')
            dv=_search(entry['dense_search'],lo,hi,audit=True)
            if production!=row['envelope']['estimate'] or dense!=entry['dense_search']['estimate']:
                raise ValueError('EPS_DENSE_AUDIT_VALUES_INCONSISTENT')
            ratio=entry.get('dense_over_production')
            if production==0:
                if ratio is not None:raise ValueError('EPS_ZERO_PRODUCTION_AUDIT_RATIO_INVALID')
            elif _number(ratio,'audit ratio')!=dense/production:
                raise ValueError('EPS_DENSE_AUDIT_RATIO_INCONSISTENT')
            candidates.extend([production,dense,*dv]);envelope_candidates.extend([dense,*dv])
        if env<max(envelope_candidates) or eps<max(candidates):
            raise ValueError('EPS_REPORTED_VALUE_UNDERESTIMATES_RECORDED_CANDIDATE')
        proofrow = {'range_inverse_kpc':[lo,hi],'eps':eps,'eps_envelope':env,'refinement_failures':nf}
        if accepted and acceptance_metadata:
            proofrow.update(certified=False, accepted_negligible=True, acceptance='ACCEPTED_NEGLIGIBLE',
                eps_measured_before_negligible_substitution=row['eps_measured_before_negligible_substitution'],
                negligible_acceptance_evidence=row['negligible_acceptance_evidence'])
        proofrows.append(proofrow)
    maximum=_number(obj.get('eps_max'),'eps_max')
    if maximum!=max(r['eps'] for r in rows):raise ValueError('EPS_MAX_INCONSISTENT')
    if obj.get('eps_max_shell')!=max(rows,key=lambda r:r['eps'])['range_inverse_kpc']:
        raise ValueError('EPS_MAX_SHELL_INCONSISTENT')
    return proofrows



def validate_details(details, obj):
    require(isinstance(details,dict) and details.get('schema')=='DDO154_POINT_CUSTODY_CX2V001', 'EPS_CALLER_DERIVED_DETAILS_REQUIRED')
    identity,custody=details['identity'],details['custody']
    require(isinstance(identity,dict) and identity.get('driver_sha256')==DRIVER_SHA,'EPS_IDENTITY_DRIVER_MISMATCH')
    require(isinstance(custody,dict) and set(custody)==CUSTODY_KEYS,'EPS_CUSTODY_FIELDS_MISMATCH')
    for value in custody.values():
        require(isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None,'EPS_CUSTODY_HASH_INVALID')
    require(digest(canonical(identity))==details['point_sha256'],'EPS_CALLER_POINT_HASH_INCONSISTENT')
    require(digest(canonical(custody))==details['custody_sha256'],'EPS_CALLER_CUSTODY_HASH_INCONSISTENT')
    require(obj.get('identity')==identity and obj.get('custody')==custody and obj.get('point_sha256')==details['point_sha256'],'EPS_NUMERICAL_POINT_CUSTODY_MISMATCH')
    uv=identity['numerics']['uv_tail']
    require(uv.get('enabled') is True and uv.get('source_rule')=='continuum_v001' and uv.get('outer')=={'shape':'cylinder','K_big_inverse_kpc':128.0},'EPS_PRODUCTION_K128_SCOPE_REQUIRED')
    gas=uv.get('gas',{})
    require(gas.get('interp')=='lagrange3_s_gl4' and type(gas.get('M_s')) is int and gas['M_s']==128,'EPS_PRODUCTION_MS128_REQUIRED')


def reconstruct_a296(obj, raw, *, approved, test_only=False):
    require(obj.get('registered_discrete_verdict')=='EPS_UNCERTIFIED','EPS_A296_DISCRETE_HISTORY_MISMATCH')
    require(obj.get('producer')=={'path':str(RULE_PATH),'sha256':RULE_SHA},'EPS_A296_REEVALUATOR_PIN_MISMATCH')
    require(RULE_SHA in approved and AUDIT_SHA in approved,'EPS_A296_SOURCES_NOT_INDEPENDENTLY_APPROVED')
    source_pin(AUTHORITY_PATH,AUTHORITY_SHA)
    source_pin(AUDIT_PATH,AUDIT_SHA)
    rule=rule_functions()
    predecessor_ref=obj['predecessor']['record']
    predecessor,_=read_pin(predecessor_ref)
    require(predecessor.get('producer')==obj['predecessor']['producer'],'EPS_PREDECESSOR_PRODUCER_MISMATCH')
    require(predecessor['producer']['sha256']==RESPONSE_SHA,'EPS_PREDECESSOR_PRODUCER_UNSUPPORTED')
    read_pin(predecessor['producer'],document=False)
    accepted=obj.get('accepted_shells')
    require(isinstance(accepted,list) and len(accepted)==1,'EPS_A296_ONE_ACCEPTED_SHELL_REQUIRED')
    matches=[row for row in obj['shells'] if row.get('range_inverse_kpc')==accepted[0]]
    require(len(matches)==1,'EPS_A296_ACCEPTED_RANGE_MISMATCH')
    row=matches[0]
    require(row.get('certified') is False and type(row.get('refinements')) is int and row['refinements']==2 and row.get('accepted_negligible') is True and row.get('acceptance')=='ACCEPTED_NEGLIGIBLE','EPS_A296_DISCRETE_HISTORY_MISMATCH')
    audit_ref=row['negligible_acceptance_evidence']['dense_audit']
    audit,_=read_pin(audit_ref)
    require(test_only or not predecessor.get("test_fixture_only") and not audit.get("test_fixture_only"), "EPS_SYNTHETIC_INPUT_NOT_ADMISSIBLE")
    require(audit.get('audit_producer')=={'path':str(AUDIT_PATH),'sha256':AUDIT_SHA},'EPS_A296_AUDIT_PRODUCER_MISMATCH')
    stamp=obj.get('successor_date_u')
    require(isinstance(stamp,str) and bool(stamp.strip()),'EPS_A296_DATE_U_REQUIRED')
    validate_numeric_candidates(predecessor,[[float(n),float(n+1)] for n in range(4,182)],182,
        accepted_range=accepted[0],acceptance_metadata=False)
    status,reconstructed=rule.reevaluate(predecessor,audit,record_pin=predecessor_ref,
        audit_pin=audit_ref,audit_producer_pin=audit['audit_producer'],
        successor_producer=obj['producer'],date_u=stamp)
    require(status.get('status')==NEW_VERDICT and reconstructed==obj,'EPS_A296_RECONSTRUCTION_MISMATCH')
    require(serialized(reconstructed)==raw,'EPS_A296_BYTE_RECONSTRUCTION_MISMATCH')
    # A296 audit metadata checks supplement, rather than replace, the pinned
    # re-evaluator's algebraic rule. No dense search is executed here.
    lo,hi=accepted[0]
    dense_candidates=_search(audit['dense_search'],lo,hi,audit=True)
    require(audit['dense']>=max(dense_candidates) and row['eps']>=max(dense_candidates),'EPS_A296_AUDIT_UNDERESTIMATES_CANDIDATE')
    return {'predecessor_ref':predecessor_ref,'audit_ref':audit_ref,'accepted_shells':accepted,
            'authority_sha256':AUTHORITY_SHA,'reevaluator_sha256':RULE_SHA,
            'audit_producer_sha256':AUDIT_SHA,'retains_discrete_failure':True}


def validate_saved_numeric(numeric_ref, *, expected_details, approved_producer_sha256=(), test_only=False):
    """Validate saved bytes and scope; return rows/trace, NOT an admission proof."""
    require(type(test_only) is bool,'EPS_TEST_MODE_BOOLEAN_REQUIRED')
    source_pin(LEGACY_PATH,LEGACY_SHA);source_pin(COMMON_PATH,COMMON_SHA)
    source_pin(RESPONSE_PATH,RESPONSE_SHA)
    obj,raw=read_pin(numeric_ref)
    require(isinstance(obj,dict) and obj.get('schema')==EPS_SCHEMA and obj.get('gate')=='EPS','EPS_NUMERICAL_SCHEMA_MISMATCH')
    require(not obj.get('test_fixture_only') or test_only,'EPS_SYNTHETIC_FIXTURE_NOT_ADMISSIBLE')
    validate_details(expected_details,obj)
    require(obj.get('status')=='TESTED' and obj.get('settings')=='registered' and obj.get('full_registered_search_executed') is True and obj.get('coverage_complete') is True,'FULL_REGISTERED_POINT_EPS_UNTESTED')
    require(obj.get('required_coverage_inverse_kpc')==[4,182],'EPS_FULL_REGISTERED_COVERAGE_REQUIRED')
    require(obj.get('production_admissible') is False and obj.get('rigorous_supremum') is False,'EPS_NUMERICAL_ONLY_REQUIRED')
    approved=set(approved_producer_sha256)
    require(RESPONSE_SHA in approved,'EPS_ORIGINAL_PRODUCER_NOT_INDEPENDENTLY_APPROVED')
    trace=None
    if obj.get('verdict')==NEW_VERDICT:
        trace=reconstruct_a296(obj,raw,approved=approved,test_only=test_only)
        accepted_range=trace['accepted_shells'][0]
    else:
        require(obj.get('verdict')==OLD_PASS and obj.get('registered_discrete_verdict')=='CERTIFIED','EPS_DISCRETE_RULE_OR_COVERAGE_FAILED')
        require(obj.get('producer',{}).get('sha256')==RESPONSE_SHA,'UNSUPPORTED_NUMERICAL_PRODUCER')
        read_pin(obj['producer'],document=False)
        require('successor_rule_verdict' not in obj and 'accepted_shells' not in obj and all('accepted_negligible' not in row for row in obj['shells']),'EPS_UNDECLARED_SUCCESSOR')
        accepted_range=None
    rows=validate_numeric_candidates(obj,[[float(n),float(n+1)] for n in range(4,182)],182,accepted_range=accepted_range)
    return obj,rows,trace


def adapt_saved_eps(numeric_ref, *, expected_details, review_ref=None,
                    approved_producer_sha256=(), approved_review_sha256=(), test_only=False):
    """Reviewable conversion only. Caller trust and downstream adoption are external.

    Synthetic mode always emits SYNTHETIC_TEST_ONLY / SYNTHETIC_PASS and cannot
    produce a TESTED/PASS proof or READY_FOR_MANIFEST result.
    """
    out={'schema':'UNT_POINT_EPS_A296_ADAPTER_RESULT_CX2V001',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'SYNTHETIC_TEST_ONLY' if test_only else 'TESTED', 'verdict':'BLOCKED',
        'blockers':[],'proof':None,'driver_certificate':None,
        'admission_authorized':False,'interface':'CALLER_DERIVED_DETAILS_REQUIRED'}
    try:
        adapter_ref={'path':str(Path(__file__).absolute()),'sha256':digest(Path(__file__).read_bytes())}
        require(adapter_ref['sha256'] in set(approved_producer_sha256),'EPS_ADAPTER_NOT_INDEPENDENTLY_APPROVED')
        obj,rows,trace=validate_saved_numeric(numeric_ref,expected_details=expected_details,
            approved_producer_sha256=approved_producer_sha256,test_only=test_only)
        require(review_ref is not None and review_ref.get('sha256') in set(approved_review_sha256),'INDEPENDENT_NUMERICAL_EPS_REVIEW_MISSING')
        review,_=read_pin(review_ref)
        require(isinstance(review,dict) and review.get('schema')=='UNT_POINT_EPS_REVIEW_CX2V001' and review.get('verdict')=='APPROVED','EPS_REVIEW_NOT_APPROVED')
        require(not review.get('test_fixture_only') or test_only,'EPS_SYNTHETIC_REVIEW_NOT_ADMISSIBLE')
        require(review.get('numeric_ref')==numeric_ref and review.get('point_sha256')==expected_details['point_sha256'] and review.get('custody_sha256')==expected_details['custody_sha256'],'EPS_REVIEW_EXACT_BYTES_OR_SCOPE_MISMATCH')
        require(review.get('accepts_registered_numerical_estimate_not_rigorous_sup') is True,'EPS_REVIEW_NUMERICAL_CONVENTION_UNRESOLVED')
        require(review.get('adapter_sha256')==adapter_ref['sha256'],'EPS_REVIEW_ADAPTER_MISMATCH')
        if trace is not None:
            require(review.get('accepts_a296_negligible_shells') is True and review.get('a296_acceptance')==trace,'EPS_A296_REVIEW_EXACT_ACCEPTANCE_REQUIRED')
        proof={'schema':'UNT_CALIBRATION_POINT_PROOF_CX2V001','gate':'EPS','utc':out['utc'],
            'status':'SYNTHETIC_TEST_ONLY' if test_only else 'TESTED',
            'verdict':'SYNTHETIC_PASS' if test_only else 'PASS',
            'point_sha256':expected_details['point_sha256'],'custody_sha256':expected_details['custody_sha256'],
            'producer':adapter_ref,'driver_certificate':numeric_ref,'numeric_evidence':numeric_ref,
            'independent_review':review_ref,'envelope_rule':'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS',
            'shells':rows,'rigorous_supremum':False,
            'scope':'Independently approved registered numerical convention, not rigorous continuous supremum',
            'scope_contract':'Caller must derive expected_details independently using the approved custody path; byte hashes do not establish that approval.'}
        if trace is not None:
            proof.update(registered_discrete_verdict='EPS_UNCERTIFIED',successor_rule_verdict='ACCEPTED_NEGLIGIBLE',
                numerical_verdict=NEW_VERDICT,a296_acceptance=trace)
        out.update(verdict='SYNTHETIC_READY_NOT_ADMISSIBLE' if test_only else 'READY_FOR_MANIFEST',
            proof=proof,driver_certificate=numeric_ref)
    except (ValueError,KeyError,TypeError,OSError,OverflowError,AttributeError,IndexError,RecursionError) as exc:
        out['blockers'].append(str(exc))
    return out
