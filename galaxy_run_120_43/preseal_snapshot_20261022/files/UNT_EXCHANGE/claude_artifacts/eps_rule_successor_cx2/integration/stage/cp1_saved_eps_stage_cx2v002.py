"""A298 saved-record EPS stage/import successor; no compute/launch commands.

The old CP1 runner remains the ordinary-point path. This entry authenticates an
A296 successor, links its original failed stage and creates new stage/proof
artifacts only. Distinct root-approved review is mandatory before adaptation.
The adapter's unchanged custody derivation occurs only in an authorized adapt
call; static stage validation never imports a driver or scientific producer.
"""
import argparse
import ast
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import types

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
BASE=ART/'eps_rule_successor_cx2'
LINEAGE={'path':str(BASE/'integration/lookup/eps_lineage_cx2v001.py'),'sha256':'da5329e1f9530dc296b9592361cc86b7b480096f9514a9f4aba8cbfdd29c7abb'}
BRIDGE={'path':str(BASE/'integration/point_response_admission_a296_bridge_cx2v002.py'),'sha256':'1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4'}
CORE={'path':str(BASE/'integration/point_response_admission_a296_cx2v002.py'),'sha256':'1a44bc59a5fc6a72c381d3c0c0875b6aa154c21fc108730d67c9ec529a39d9d7'}
RUNNER={'path':str(ART/'s4rc1_c3/build_c3v004/cp1_runner_c3v004.py'),'sha256':'3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48'}
COMMON={'path':str(ART/'s4rc1_c3/build_c3v005_c2/s4rc1_common_c3v005.py'),'sha256':'2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5'}
GENESIS={'path':str(ART/'s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json'),'sha256':'2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319'}
ORIGINAL_COMMON={'path':str(ART/'s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py'),'sha256':'53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'}
GQ_PRODUCER={'path':str(ART/'calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py'),'sha256':'2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd'}
ANCHOR_KEY='8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8'
DRIVER_SHA='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
REQUEST_SCHEMA='S4RC1_A296_SAVED_EPS_REQUEST_CX2V001'
STAGE_SCHEMA='S4RC1_A296_SAVED_EPS_STAGE_CX2V001'

def need(ok,reason):
    if not ok:raise ValueError('A296_STAGE_'+reason)

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def digest(obj):return hashlib.sha256(canonical(obj)).hexdigest()

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def lexical(path):
    p=Path(os.path.abspath(os.fspath(path)))
    bad={'.codex','runs','runs_ext','unt_internal_runs','v007_postseal_records'}
    need(not any(x.casefold() in bad or x.casefold().startswith('uvt_') or 'ngc3198' in x.casefold()
                 or 'kmax_a2f10_c5h_run_v001' in x.casefold() for x in p.parts),'PROTECTED_PATH')
    need(p.is_relative_to(ART),'ARTIFACT_ROOT_REQUIRED')
    return p

def safe_existing(path):
    p=lexical(path)
    for _ in range(40):
        built=Path(p.anchor);changed=False
        for i,part in enumerate(p.parts[1:],1):
            built=lexical(built/part) if (built/part).is_relative_to(ART) else built/part
            if built.is_symlink():
                target=Path(os.readlink(built))
                if not target.is_absolute():target=built.parent/target
                p=lexical(target.joinpath(*p.parts[i+1:]));changed=True;break
        if not changed:return p
    raise ValueError('A296_STAGE_SYMLINK_LIMIT')

def read(ref):
    need(isinstance(ref,dict) and set(ref)=={'path','sha256'},'EXACT_PIN_REQUIRED')
    raw=safe_existing(ref['path']).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==ref['sha256'],'BYTE_PIN_MISMATCH')
    return raw

def load(ref,name):
    raw=read(ref);m=types.ModuleType(name);m.__file__=ref['path']
    exec(compile(raw,ref['path'],'exec'),m.__dict__)
    return m

def own_pin():
    p=Path(__file__).absolute()
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def _functions(ref,names,namespace):
    nodes=[n for n in ast.parse(read(ref)).body if isinstance(n,ast.FunctionDef) and n.name in names]
    need({n.name for n in nodes}==set(names),'ORIGINAL_FUNCTION_SET')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),ref['path'],'exec'),namespace)
    return namespace

def legacy_check_eps(eps,key,custody):
    original={'path':str(ART/'calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py'),
              'sha256':'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'}
    c=types.SimpleNamespace(SHELL_END=182,canonical_pin=lambda name:original if name=='response_producer' else None)
    ns=_functions(RUNNER,['check_eps'],{'C':c,'EPS_AUDITS':14})
    return ns['check_eps'](eps,key,custody)

def check_eps(eps,key,custody,*,numeric_ref=None,snapshot=None):
    """Original check dictionary for ordinary records; explicit new A296 checks."""
    if eps.get('verdict')!='NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED':
        return legacy_check_eps(eps,key,custody)
    need(numeric_ref is not None,'SUCCESSOR_PIN_REQUIRED')
    l=load(LINEAGE,'_a296_stage_lineage')
    record,evidence=l.authenticate_successor(numeric_ref,snapshot=snapshot)
    need(record==eps,'SUPPLIED_RECORD_DIFFERS_FROM_PINNED_BYTES')
    old=legacy_check_eps(eps,key,custody)
    for k in ('registered_discrete_CERTIFIED','verdict_review_required','producer_pin_canonical_R4'):old.pop(k)
    old.update(original_discrete_failure_preserved=eps.get('registered_discrete_verdict')=='EPS_UNCERTIFIED',
        a296_exact_reconstruction=True,a296_distinct_verdict=True,
        producer_lineage_authenticated=evidence['rule']==eps['producer'])
    return old

def identity(spec):
    need(spec.get('galaxy')=='DDO154','DDO154_REQUIRED')
    n=copy.deepcopy(spec['numerics'])
    for key in ('eps_certificate','lo_certificate'):n['uv_tail'].pop(key,None)
    return {'driver_sha256':DRIVER_SHA,'physical':spec['physical'],'coefficients':spec['coefficients'],'numerics':n}

def context_roles(start,ctx,predecessor,evidence,*,snapshot,key):
    """Exact saved role map, never follow/execute scientific dependency targets."""
    genesis=snapshot.doc(GENESIS)
    need(evidence['normalized_source_pins_digest']==genesis.get('eps_source_pins_digest'),'PREDECESSOR_SOURCE_DRIFT_FROM_GENESIS')
    dependencies=predecessor.get('dependencies')
    need(isinstance(dependencies,dict) and bool(dependencies),'PREDECESSOR_DEPENDENCY_MAP_REQUIRED')
    need(ctx.get('source_pins')==dependencies,'CONTEXT_ROLE_PIN_MAP_MISMATCH')
    need(dependencies.get('producer')==predecessor.get('producer')==evidence['original_producer'],'CONTEXT_PRODUCER_ROLE')
    need(start.get('common')==ORIGINAL_COMMON,'ORIGINAL_COMMON_PIN')
    snapshot.read(ORIGINAL_COMMON)  # source bytes only, never execute common
    need(start.get('producers')=={'gq':GQ_PRODUCER,'eps':evidence['original_producer']},'ORIGINAL_PRODUCER_ROLES')
    need(start.get('settings')=='registered' and start.get('shell_ranges') is None and start.get('gq_node_limit') is None,'ORIGINAL_REGISTERED_SETTINGS')
    expected={'point_sha256_is_key','custody_sha256_is_digest'}
    if key!=ANCHOR_KEY:expected|={'anchor_context_record_present','source_pins_match_anchor'}
    need(set(ctx['checks'])==expected and all(v is True for v in ctx['checks'].values()),'CONTEXT_CHECK_ROLES')
    info=ctx.get('checks_info',{})
    need(info.get('source_pins_match_anchor') is (None if key==ANCHOR_KEY else True),'CONTEXT_ANCHOR_SOURCE_DECLARATION')
    need(info.get('anchor_context')==('THIS_POINT_IS_THE_ANCHOR' if key==ANCHOR_KEY else 'PRESENT'),'CONTEXT_ANCHOR_DECLARATION')
    need(ctx.get('point_symbol_checks')==predecessor.get('point_symbol_checks'),'CONTEXT_SYMBOL_CHECKS_MISMATCH')


def prepare(request_ref):
    """Authenticate saved stage context; return new numerical stage, no proof."""
    l=load(LINEAGE,'_a296_stage_lineage');s=l.snapshot()
    request=s.doc(request_ref)
    need(isinstance(request,dict) and request.get('schema')==REQUEST_SCHEMA,'REQUEST_SCHEMA')
    need(set(request)=={'schema','spec','point_start','context','eps_stage','successor'},'REQUEST_FIELDS')
    spec=s.doc(request['spec']);start=s.doc(request['point_start']);ctx=s.doc(request['context']);oldstage=s.doc(request['eps_stage'])
    successor,evidence=l.authenticate_successor(request['successor'],snapshot=s)
    key=digest(identity(spec));custody=ctx.get('custody')
    need(start.get('schema')=='S4RC1_CP1_POINT_START_C3V002' and start.get('point',{}).get('key')==key,'ORIGINAL_START_SCOPE')
    need(start.get('spec')==request['spec'] and start.get('runner')==RUNNER,'ORIGINAL_START_SPEC_OR_RUNNER')
    need(isinstance(start.get('operator_lane'),str) and bool(start['operator_lane'].strip()),'OPERATOR_LANE_REQUIRED')
    need(ctx.get('schema')=='S4RC1_CP1_STAGE_C3V002' and ctx.get('stage')=='CONTEXT' and ctx.get('key')==key,'CONTEXT_SCHEMA_OR_KEY')
    need(ctx.get('point_sha256')==key and ctx.get('custody_sha256')==digest(custody),'CONTEXT_DIGEST')
    need(bool(ctx.get('checks')) and all(v is True for v in ctx['checks'].values()),'ORIGINAL_CONTEXT_NOT_OK')
    need(successor.get('identity')==identity(spec) and successor.get('point_sha256')==key and successor.get('custody')==custody,'SUCCESSOR_SPEC_CUSTODY')
    need(oldstage.get('schema')=='S4RC1_CP1_STAGE_C3V002' and oldstage.get('stage')=='EPS' and oldstage.get('key')==key,'ORIGINAL_EPS_STAGE_SCOPE')
    need(oldstage.get('record')==evidence['predecessor_record'] and oldstage.get('ok') is False,'ORIGINAL_FAILED_STAGE_REQUIRED')
    predecessor=s.doc(evidence['predecessor_record'])
    context_roles(start,ctx,predecessor,evidence,snapshot=s,key=key)
    core=load(CORE,'_a296_stage_validation_core')
    details={'schema':'DDO154_POINT_CUSTODY_CX2V001','identity':identity(spec),'custody':custody,
             'point_sha256':key,'custody_sha256':ctx['custody_sha256']}
    # This fixed dependency closure enables validation only. It is NOT root
    # signer/source approval, and validate_saved_numeric never constructs proof.
    validation_sources=(evidence['original_producer']['sha256'],evidence['rule']['sha256'],evidence['audit_producer']['sha256'])
    validated,proof_rows,acceptance_trace=core.validate_saved_numeric(request['successor'],
        expected_details=details,approved_producer_sha256=validation_sources)
    need(validated==successor,'FULL_NUMERIC_RECORD_MISMATCH')

    original_checks=legacy_check_eps(predecessor,key,custody)
    need(oldstage.get('checks')==original_checks,'ORIGINAL_CHECKS_DIFFER')
    need({k for k,v in original_checks.items() if not v}=={'registered_discrete_CERTIFIED','verdict_review_required'},'ORIGINAL_HAS_OTHER_FAILURE')
    checks=check_eps(successor,key,custody,numeric_ref=request['successor'],snapshot=s)
    checks.update(full_original_and_successor_candidate_metadata=True,context_role_pins_match_genesis=True)
    need(all(v is True for v in checks.values()),'SUCCESSOR_CHECKS_FAILED')
    stage={'schema':STAGE_SCHEMA,'stage':'EPS_SAVED_A296_REEVALUATION','utc':utc(),'status':'TESTED',
        'key':key,'record':request['successor'],'request':request_ref,'original_stage':request['eps_stage'],
        'checks':checks,'original_checks':original_checks,'ok':True,'numeric_lineage':evidence,
        'a296_acceptance':acceptance_trace,
        'custody_sha256':ctx['custody_sha256'],'generator':own_pin(),'numerical_only':True,
        'approved_signer_review_required':True,'production_admissible':False,
        'scope':'New saved-record stage only; original failed stage retained; no computation or admission.'}
    return stage,{'request':request,'spec':spec,'start':start,'context':ctx,'successor':successor,'snapshot':s}

def review_gate(review_ref,stage,context,*,approved_review_sha256,approved_signer_lanes,approved_producer_sha256,output_root):
    need(review_ref is not None,'INDEPENDENT_REVIEW_REQUIRED')
    need(review_ref.get('sha256')==approved_review_sha256,'REVIEW_HASH_NOT_ROOT_APPROVED')
    need(not safe_existing(review_ref['path']).is_relative_to(safe_existing(output_root)),'REVIEW_INSIDE_OUTPUT_ROOT')
    rv=context['snapshot'].doc(review_ref)
    need(isinstance(rv,dict),'REVIEW_OBJECT_REQUIRED')
    ns=_functions(COMMON,['contains_template_marker','distinct_review_problems'],{})
    problems=ns['distinct_review_problems'](rv,approved_signer_lanes=approved_signer_lanes,
        excluded_lanes={context['start']['operator_lane'],'Codex2'})
    need(not problems,'REVIEW_NOT_DISTINCT_OR_APPROVED: '+'; '.join(problems))
    want={'schema':'UNT_POINT_EPS_REVIEW_CX2V001','verdict':'APPROVED','numeric_ref':stage['record'],
        'point_sha256':stage['key'],'custody_sha256':stage['custody_sha256'],'adapter_sha256':BRIDGE['sha256'],
        'accepts_registered_numerical_estimate_not_rigorous_sup':True,'accepts_a296_negligible_shells':True}
    need(all(rv.get(k)==v for k,v in want.items()),'REVIEW_SCOPE_OR_ADAPTER_MISMATCH')
    need(rv.get('accepts_registered_numerical_estimate_not_rigorous_sup') is True and rv.get('accepts_a296_negligible_shells') is True,'REVIEW_BOOLEAN_ACCEPTANCE_REQUIRED')
    need(canonical(rv.get('a296_acceptance'))==canonical(stage['a296_acceptance']),'REVIEW_EXACT_A296_TRACE_REQUIRED')

    required={BRIDGE['sha256'],context['successor']['producer']['sha256'],stage['numeric_lineage']['audit_producer']['sha256'],stage['numeric_lineage']['original_producer']['sha256']}
    need(required.issubset(set(approved_producer_sha256)),'SOURCE_APPROVALS_REQUIRED')
    return rv

def adapt(request_ref,*,review_ref,approved_review_sha256,approved_signer_lanes,approved_producer_sha256,output_root):
    """No outputs on refusal. Only an authorized caller should invoke live adaptation."""
    stage,context=prepare(request_ref)
    review_gate(review_ref,stage,context,approved_review_sha256=approved_review_sha256,
        approved_signer_lanes=approved_signer_lanes,approved_producer_sha256=approved_producer_sha256,output_root=output_root)
    adapter=load(BRIDGE,'_a296_stage_adapter')
    result=adapter.adapt_eps(context['spec'],stage['record'],review_ref=review_ref,
        approved_producer_sha256=approved_producer_sha256,approved_review_sha256=(approved_review_sha256,))
    need(result.get('verdict')=='READY_FOR_MANIFEST' and isinstance(result.get('proof'),dict),'ADAPTER_BLOCKED: '+str(result.get('blockers')))
    proof=result['proof']
    need(proof.get('status')=='TESTED' and proof.get('verdict')=='PASS' and proof.get('producer')==BRIDGE,'PROOF_STATUS_OR_PRODUCER')
    need(proof.get('point_sha256')==stage['key'] and proof.get('custody_sha256')==stage['custody_sha256'] and proof.get('driver_certificate')==stage['record'],'PROOF_SCOPE')
    return stage,result,proof

def write_new(path,obj):
    p=lexical(path);parent=safe_existing(p.parent)
    need(parent.is_dir() and p.parent==parent,'OUTPUT_PARENT_NOT_CANONICAL')
    raw=(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb')as f:f.write(raw)
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    p.add_argument('action',choices=['stage','adapt'])
    p.add_argument('--request',required=True);p.add_argument('--request-sha256',required=True)
    p.add_argument('--output-root',required=True)
    p.add_argument('--review');p.add_argument('--review-sha256');p.add_argument('--approved-review-sha256')
    p.add_argument('--approved-signer-lane',action='append',default=[])
    p.add_argument('--approved-producer-sha256',action='append',default=[])
    a=p.parse_args(argv)
    try:
        out=safe_existing(a.output_root);need(out.is_dir(),'OUTPUT_ROOT_REQUIRED')
        req={'path':a.request,'sha256':a.request_sha256}
        if a.action=='stage':
            stage,_=prepare(req)
            path=out/('STAGE_EPS_A296_'+stage['key'][:16]+'.json')
            result={'stage':write_new(path,stage),'production_admissible':False}
        else:
            rv=None if a.review is None else {'path':a.review,'sha256':a.review_sha256}
            stage,result,proof=adapt(req,review_ref=rv,approved_review_sha256=a.approved_review_sha256,
                approved_signer_lanes=a.approved_signer_lane,approved_producer_sha256=a.approved_producer_sha256,output_root=out)
            paths=[out/('EPS_A296_ADAPTER_RESULT_'+stage['key'][:16]+'.json'),out/('EPS_A296_PROOF_'+stage['key'][:16]+'.json')]
            need(not any(x.exists() for x in paths),'OUTPUT_EXISTS')
            result={'adapter_result':write_new(paths[0],result),'proof':write_new(paths[1],proof)}
        print(json.dumps(result,sort_keys=True));return 0
    except (ValueError,KeyError,TypeError,OSError,OverflowError,AttributeError)as e:
        print(json.dumps({'status':'REFUSED','reason':str(e)}));return 2

if __name__=='__main__':raise SystemExit(main())
