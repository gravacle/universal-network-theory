"""G4 (ks_k3_chain_c2 G-wave c2v001; root A175, A176): EPS adapter point_response_admission_adapter_cx2v003 (4de70486)
over KS2 (custody KS1), for S1_UA_C3T only.

adapt_eps hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 4de70486 module object (P, by path and
sha), whose base 381b3eaa supplies a1dcdea8 and 6810b7c3: its result, proof producer pin included, is 4de70486's. For
S1_UA_C3T it is 4de70486's code with PR = KS2 (shell_plan from the kept K: the 179 unit shells [3,4]..[181,182]),
CU = KS1 (derive_details admits the +-3 cube) and RESPONSE_SHA = KS2's sha; this file's own sha must be approved and
bound by the review (L177-178, L188), and the proof's producer pin names it. The audit filter (L89, 4 <= n < edge) is
unchanged: AUDIT_LO starts at 4, so a K=3 record carries the same 14 audits (wave-1 K2-P4). Edits: this docstring head
and the predecessor block (base 381b3eaa -> the adapter 4de70486 itself, plus KS2), and the first line of adapt_eps.

EPS adapter successor: finite candidates, dominant values, unique audits.

No scientific run/search is executed. A distinct trusted review must bind the
full numeric bytes and this adapter. K64 remains a diagnostic capability;
the coordinator's production K selection is separately enforced by the caller.
"""
import hashlib
import importlib.util
import math
from pathlib import Path
import sys

HERE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # G4: 4de70486's folder
PREDECESSOR=HERE/'point_response_admission_adapter_cx2v003.py'          # G4: the adapter 4de70486 itself (P)
PREDECESSOR_SHA='4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'
if hashlib.sha256(PREDECESSOR.read_bytes()).hexdigest()!=PREDECESSOR_SHA:
    raise ValueError('EPS adapter predecessor pin mismatch')
sp=importlib.util.spec_from_file_location('g4_predecessor_eps_adapter_cx2v003',PREDECESSOR)
P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
RESPONSE_PATH=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/point_response_producer_cx2v002_ks2_c2v001.py')   # G4: KS2 (custody KS1)
if hashlib.sha256(RESPONSE_PATH.read_bytes()).hexdigest()!='99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7':
    raise ValueError('G4: KS2 response producer pin mismatch')
sp=importlib.util.spec_from_file_location('g4_eps_adapter_response_ks2',RESPONSE_PATH)
PR=importlib.util.module_from_spec(sp);sys.modules[sp.name]=PR;sp.loader.exec_module(PR)
CU=PR.CU
RESPONSE_SHA='99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'


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


def validate_numeric_candidates(obj,required,edge):
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
        if type(nf) is not int or nf not in (0,1) or row.get('certified') is not True:
            raise ValueError('EPS_REFINEMENT_FAILURE')
        eps,base,ref,env=(_number(row.get(k),k) for k in ('eps','eps_base','eps_refined','eps_envelope'))
        if ref>1.1*base:raise ValueError('EPS_REFINEMENT_RULE_FAILED')
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
        if base!=levels[str(nf)]['eps'] or ref!=levels[str(nf+1)]['eps']:
            raise ValueError('EPS_DISCRETE_VALUES_INCONSISTENT')
        if nf==1 and levels['1']['eps']<=1.1*levels['0']['eps']:
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
        proofrows.append({'range_inverse_kpc':[lo,hi],'eps':eps,'eps_envelope':env,'refinement_failures':nf})
    maximum=_number(obj.get('eps_max'),'eps_max')
    if maximum!=max(r['eps'] for r in rows):raise ValueError('EPS_MAX_INCONSISTENT')
    if obj.get('eps_max_shell')!=max(rows,key=lambda r:r['eps'])['range_inverse_kpc']:
        raise ValueError('EPS_MAX_SHELL_INCONSISTENT')
    return proofrows


def adapt_eps(spec,numeric_ref,*,review_ref=None,approved_producer_sha256=(),approved_review_sha256=()):
    if not CU.s1_c3t_spec(spec):   # G4: 4de70486's own code path
        return P.adapt_eps(spec,numeric_ref,review_ref=review_ref,approved_producer_sha256=approved_producer_sha256,
                           approved_review_sha256=approved_review_sha256)
    out={'schema':'UNT_POINT_EPS_ADAPTER_RESULT_CX2V002','utc':PR.utc(),'status':'TESTED',
         'verdict':'BLOCKED','blockers':[],'proof':None,'driver_certificate':None}
    try:
        details=CU.derive_details(spec=spec);obj=CU.read_pin(numeric_ref)
        if obj.get('schema')!=PR.EPS_SCHEMA or obj.get('gate')!='EPS':raise ValueError('EPS_NUMERICAL_SCHEMA_MISMATCH')
        if obj.get('identity')!=details['identity'] or obj.get('custody')!=details['custody']:raise ValueError('EPS_NUMERICAL_POINT_CUSTODY_MISMATCH')
        if obj.get('status')!='TESTED' or obj.get('settings')!='registered' or obj.get('full_registered_search_executed') is not True:
            raise ValueError('FULL_REGISTERED_POINT_EPS_UNTESTED')
        if obj.get('coverage_complete') is not True or obj.get('registered_discrete_verdict')!='CERTIFIED':raise ValueError('EPS_DISCRETE_RULE_OR_COVERAGE_FAILED')
        approved=set(approved_producer_sha256)
        if obj.get('producer',{}).get('sha256') not in approved or CU.sha(__file__) not in approved:
            raise ValueError('NUMERICAL_PRODUCER_OR_ADAPTER_NOT_INDEPENDENTLY_APPROVED')
        CU.read_pin(obj['producer'],document=False)
        if obj['producer']['sha256']!=RESPONSE_SHA:raise ValueError('UNSUPPORTED_NUMERICAL_PRODUCER')
        if not review_ref or review_ref.get('sha256') not in set(approved_review_sha256):raise ValueError('INDEPENDENT_NUMERICAL_EPS_REVIEW_MISSING')
        review=CU.read_pin(review_ref)
        if review.get('schema')!='UNT_POINT_EPS_REVIEW_CX2V001' or review.get('verdict')!='APPROVED':raise ValueError('EPS_REVIEW_NOT_APPROVED')
        if review.get('numeric_ref')!=numeric_ref or review.get('point_sha256')!=details['point_sha256'] or review.get('custody_sha256')!=details['custody_sha256']:
            raise ValueError('EPS_REVIEW_EXACT_BYTES_OR_SCOPE_MISMATCH')
        if review.get('accepts_registered_numerical_estimate_not_rigorous_sup') is not True:raise ValueError('EPS_REVIEW_NUMERICAL_CONVENTION_UNRESOLVED')
        if review.get('adapter_sha256')!=CU.sha(__file__):raise ValueError('EPS_REVIEW_ADAPTER_MISMATCH')
        required,_,edge=PR.shell_plan(spec)
        proofrows=validate_numeric_candidates(obj,required,edge)
        proof={'schema':'UNT_CALIBRATION_POINT_PROOF_CX2V001','gate':'EPS','utc':PR.utc(),'status':'TESTED','verdict':'PASS',
            'point_sha256':details['point_sha256'],'custody_sha256':details['custody_sha256'],'producer':CU.pin(__file__),
            'driver_certificate':numeric_ref,'numeric_evidence':numeric_ref,'independent_review':review_ref,
            'envelope_rule':'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS','shells':proofrows,'rigorous_supremum':False,
            'scope':'Independently approved registered numerical convention, not rigorous continuous supremum'}
        out.update(verdict='READY_FOR_MANIFEST',proof=proof,driver_certificate=numeric_ref)
    except (ValueError,KeyError,TypeError,OSError,OverflowError) as exc:out['blockers'].append(str(exc))
    return out
