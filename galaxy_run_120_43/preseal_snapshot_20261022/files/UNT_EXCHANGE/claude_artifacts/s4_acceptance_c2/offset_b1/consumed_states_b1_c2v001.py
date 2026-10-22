"""r5 complete-state join from explicit own-call replay descriptors.

No discovery sweep or solver. The campaign call's out/result.json and fixed
TAIL_REPLAY_PLAN.json are the only entry points. Every real occurrence must
join an actual full-state/source replay, point check and modeled call record.
Completeness is custody/enumeration only, never GQ/LO approval or launch leave.
"""
import hashlib
import importlib.util
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
PINS={
 'D':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/consumed_states_cx2v005.py','7b7400f331970a5f5fb7f7104f5e1850a765fcd04fc993100b5d1f0f37f4d653'),
 'A':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py','7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'),
 'X':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/execution_graph_cx2v002.py','6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258'),
}
def module(key):
    name,sha=PINS[key];p=H/name;raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('JOIN_MODULE_PIN_MISMATCH')
    sp=importlib.util.spec_from_file_location('cx2_join_'+key,p)
    m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m
    exec(compile(raw,str(p),'exec'),m.__dict__)
    return m
D,A,X=(module(k) for k in ('D','A','X'))
C=A.C
ROLES={
 'current_begin_inferred_from_completion':('route_a_current',['payload','state_digest']),
 'next_built_and_monitor_consumed':('route_a_next',['payload','next_state_digest']),
 'boundary_at_return':('route_a_return',['result','uv_tail','boundary_state_digest_at_return']),
 'inherited_route_a':('stage_tail',['uv_tail','state_digest']),
 'signed_body_minus_route_a':('stage_tail',['uv_tail','state_digest']),
 'own_source_state':('stage_tail',['uv_tail','state_digest']),
}
COMPONENT_ROLES={'body_gas_component','route_a_gas_component'}
RECONSTRUCTION_GAPS={
 'ROUTE_A_STATE_SOURCE_RECONSTRUCTION_UNAVAILABLE','ROUTE_B_STATE_SOURCE_RECONSTRUCTION_UNAVAILABLE',
 'FULL_SOURCE_ROSTER_NOT_ARCHIVED','GUARD_READY_STATES_WITHHELD',
 'POSITIVE_TOTAL_ZERO_MODE_REQUIRED','SIGNED_COMPONENT_RECONSTRUCTION_UNAVAILABLE',
}

def ref(path):
    p=D.safe_path(path)
    if p.stat().st_size>D.MAX_JSON_BYTES:raise ValueError('JOIN_JSON_TOO_LARGE')
    raw=p.read_bytes()
    if len(raw)>D.MAX_JSON_BYTES:raise ValueError('JOIN_JSON_TOO_LARGE')
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()},D._strict_json(raw)

def same_ref(a,b):
    return (isinstance(a,dict) and isinstance(b,dict) and set(a)==set(b)=={'path','sha256'}
            and a['sha256']==b['sha256'] and D.safe_path(a['path'])==D.safe_path(b['path']))

def split_occurrences(discovery):
    rows=discovery['occurrences']
    if not isinstance(rows,list) or [x.get('ordinal') for x in rows]!=list(range(len(rows))):
        raise ValueError('DISCOVERY_ORDINAL_SEQUENCE_INVALID')
    real=[];components=[]
    for o in rows:
        if o.get('role') in COMPONENT_ROLES:
            if o.get('state_sha256_claimed') is not None or not o.get('stage_kind','').startswith('offset_'):
                raise ValueError('INVALID_COMPONENT_PLACEHOLDER')
            components.append(o)
        elif o.get('role') in ROLES and D._hex(o.get('state_sha256_claimed')):
            real.append(o)
        else:raise ValueError('UNSUPPORTED_OR_UNIDENTIFIED_OCCURRENCE')
    if not real:raise ValueError('NO_RECONSTRUCTIBLE_OCCURRENCES')
    signed=[x for x in real if x['role']=='signed_body_minus_route_a']
    for s in signed:
        pair=[x for x in components if x['stage']==s['stage'] and x['evidence']==s['evidence']]
        if len(pair)!=2 or {x['role'] for x in pair}!=COMPONENT_ROLES:
            raise ValueError('SIGNED_COMPONENT_PLACEHOLDER_COVERAGE')
    if len(components)!=2*len(signed):raise ValueError('ORPHAN_COMPONENT_PLACEHOLDER')
    return real,components

def validate_plan(plan,*,call_result_ref,call_spec_ref,real):
    if not isinstance(plan,dict) or set(plan)!={'schema','driver_sha256','call_result','call_spec','replays'}:
        raise ValueError('REPLAY_PLAN_FIELDS')
    if plan['schema']!='DDO154_TAIL_REPLAY_PLAN_CX2V001' or plan['driver_sha256']!=D.DRIVER_SHA:
        raise ValueError('REPLAY_PLAN_SCHEMA_OR_DRIVER')
    if not same_ref(plan['call_result'],call_result_ref) or not same_ref(plan['call_spec'],call_spec_ref):
        raise ValueError('REPLAY_PLAN_CALL_BYTES_MISMATCH')
    entries=plan['replays']
    if not isinstance(entries,list) or any(not isinstance(e,dict) or set(e)!={'ordinal','reconstruction','packet'} for e in entries):
        raise ValueError('REPLAY_PLAN_ENTRY_FIELDS')
    ids=[e['ordinal'] for e in entries]
    if any(type(n) is not int for n in ids) or ids!=[o['ordinal'] for o in real]:
        raise ValueError('REPLAY_PLAN_EXACT_OCCURRENCE_COVERAGE')
    for e in entries:
        for key in ('reconstruction','packet'):
            rr=e[key]
            if not isinstance(rr,dict) or set(rr)!={'path','sha256'} or not D._hex(rr['sha256']):
                raise ValueError('REPLAY_PLAN_EXACT_BYTE_REFERENCE')
    return entries

def accepted_lineage(*,result,real,components,driver_out):
    ar=result['uv_tail']['manifest']
    if not D.safe_path(ar['path']).is_relative_to(driver_out):raise ValueError('ACCEPTED_MANIFEST_OUTSIDE_OWN_CALL')
    accepted=C.read_pin(ar);digest=accepted['state']['digest']
    if not D._hex(digest):raise ValueError('ACCEPTED_MANIFEST_DIGEST_INVALID')
    boundary=[x for x in real if x['role']=='boundary_at_return']
    current=[x for x in real if x['role']=='current_begin_inferred_from_completion']
    if len(boundary)!=1 or not current or boundary[0]['state_sha256_claimed']!=digest or max(current,key=lambda x:x['iteration'])['state_sha256_claimed']!=digest:
        raise ValueError('ACCEPTED_BOUNDARY_CURRENT_DIGEST_MISMATCH')
    for o in real:
        if o['role']=='inherited_route_a' and o['state_sha256_claimed']!=digest:
            raise ValueError('INHERITED_ACCEPTED_STATE_MISMATCH')
        if o['role'] in ('inherited_route_a','signed_body_minus_route_a'):
            u=C.read_pin(o['evidence'])['uv_tail']
            if not same_ref(u.get('route_a_manifest'),ar) or u.get('route_a_state_digest')!=digest:
                raise ValueError('STAGE_ACCEPTED_MANIFEST_LINEAGE_MISMATCH')
    for o in components:
        if o['role']=='route_a_gas_component' and o.get('parent_stellar_plus_gas_state_digest_claimed')!=digest:
            raise ValueError('SIGNED_COMPONENT_PARENT_DIGEST_MISMATCH')
    return ar,digest


def canonical_stage_kind(o):
    if o['role'] in ('current_begin_inferred_from_completion','next_built_and_monitor_consumed','boundary_at_return','inherited_route_a'):
        return 'route_a'
    if o['role']=='signed_body_minus_route_a':return 'offset'
    return o['stage_kind']

def consumed_states(*,spec,result,call_dir):
    out={'schema':'DDO154_CONSUMED_STATE_JOIN_CX2V010','status':'TESTED','complete':False,'states':[],
         'occurrences':[],'blockers':[],'certificate_status':'UNAVAILABLE','point_status':'INCOMPLETE',
         'science_approval':'GQ, LO, independent packet binding review and policy approval remain separate',
         'driver_sha256':D.DRIVER_SHA,'producer':C.pin(__file__),'verified_files':[]}
    try:
        discovery=D.consumed_states(spec=spec,result=result,call_dir=call_dir)
        out['discovery']=discovery;out['occurrences']=discovery['occurrences']
        real,components=split_occurrences(discovery)
        placeholder_wheres={x['stage']+':'+x['role'] for x in components}
        structural=[b for b in discovery['blockers'] if b['code'] not in RECONSTRUCTION_GAPS
                    and not (b['code']=='STATE_DIGEST_MISSING_OR_INVALID' and b['where'] in placeholder_wheres)]
        if structural:
            out['blockers'].extend(structural);raise ValueError('DISCOVERY_STRUCTURAL_BLOCKERS')
        if discovery['coverage']['fresh_call_scope']!='FRESH_COMPLETED':raise ValueError('CALL_NOT_FRESH_COMPLETED')
        graph=X.validate_graph(spec=spec,result=result);out['execution_graph']=graph
        if graph.get('ok') is not True:raise ValueError('EXPECTED_EXECUTION_GRAPH_INCOMPLETE: '+str(graph.get('blockers')))
        call=D.safe_path(call_dir);driver_out=D.safe_path(call/'out')
        rp,raw_result=ref(driver_out/'result.json');sp,saved_spec=ref(driver_out/'inputs/call_spec.json')
        fp,finish=ref(driver_out/'finish.json')
        if raw_result!=result or saved_spec!=spec or finish.get('result_sha256')!=rp['sha256']:
            raise ValueError('JOIN_CALL_BYTES_CHANGED')
        pp,plan=ref(call/'TAIL_REPLAY_PLAN.json');out['replay_plan']=pp
        entries=validate_plan(plan,call_result_ref=rp,call_spec_ref=sp,real=real)
        accepted_ref,accepted_digest=accepted_lineage(result=result,real=real,components=components,driver_out=driver_out)
        details=C.derive_details(spec=spec)
        out.update(point_sha256=details['point_sha256'],custody_sha256=details['custody_sha256'])
        verified={x['path']:x for x in discovery['verified_files']}
        verified.update({x['path']:x for x in (rp,sp,fp,pp,accepted_ref)})
        custody_refs=[spec['coefficients'],details['row_contract']['prereg'],out['producer']]
        custody_refs += [{'path':path,'sha256':sha} for path,sha in details['modules'].items()]
        custody_refs += [{'path':str(H/name),'sha256':sha} for name,sha in PINS.values()]
        for control in graph['controls']:
            if not D.safe_path(control['path']).is_relative_to(driver_out):raise ValueError('CONTROL_OUTSIDE_OWN_CALL')
            custody_refs.append(control)
        for rr in custody_refs:
            C.read_pin(rr,document=False)
            old=verified.get(rr['path'])
            if old is not None and old['sha256']!=rr['sha256']:raise ValueError('JOIN_CUSTODY_PIN_CONFLICT')
            verified[rr['path']]=rr
        joined=[];states={};resolved_components=[]
        for o,entry in zip(real,entries):
            r,p,i1t=A.compute_i1t(entry['reconstruction'],entry['packet'])
            if r.replay_scope!='PRODUCTION_P128_MS128':raise ValueError('SYNTHETIC_SOURCE_CANNOT_COMPLETE_PRODUCTION_INVENTORY')
            v=A.verify_product(r,p);state=v['state']
            if state['stage_kind']!=canonical_stage_kind(o):raise ValueError('ACTUAL_OCCURRENCE_STAGE_KIND_MISMATCH')
            if state['state_sha256']!=o['state_sha256_claimed']:
                raise ValueError('REPLAY_DISCOVERED_STATE_MISMATCH')
            if o.get('source_sha256_claimed') is not None and state['source_sha256']!=o['source_sha256_claimed']:
                raise ValueError('REPLAY_DISCOVERED_SOURCE_MISMATCH')
            A.verify_point(spec,r,p,details)
            role,path=ROLES[o['role']]
            occurrence={'role':role,'stage':o['stage'],'iteration':o['iteration'],'run_root':str(driver_out),
                        'state_field_path':path,'assertion_ref':o['evidence'],
                        'call_spec_ref':sp,'call_result_ref':rp,'call_finish_ref':fp}
            receipt=A.verify_occurrence(spec,r,p,occurrence)
            if i1t.get('verdict')!='PASS':raise ValueError('COMPUTED_SOURCE_PACKET_IDENTITY_FAILED')
            for rr in i1t['source_files']:
                if not D.safe_path(rr['path']).is_relative_to(driver_out):raise ValueError('SOURCE_PACKET_OUTSIDE_OWN_CALL')
                C.read_pin(rr,document=False)
            desc=r.json(entry['reconstruction'])
            if o['role'] in ('inherited_route_a','boundary_at_return'):
                if desc.get('operation')!='accepted_manifest' or not same_ref(desc.get('manifest'),accepted_ref):
                    raise ValueError('INHERITED_DESCRIPTOR_ACCEPTED_MANIFEST_MISMATCH')
            if role in ('route_a_current','route_a_next'):
                ss=desc.get('source',{})
                if desc.get('operation')!='rebuild' or ss.get('kind')!='route_a' or ss.get('iteration')!=o['iteration'] or len(ss.get('elements',[]))!=o['iteration']:
                    raise ValueError('ROUTE_A_EXACT_SOURCE_PREFIX_REQUIRED')
            if o['role']=='signed_body_minus_route_a':
                if desc.get('operation')!='rebuild' or desc.get('source',{}).get('kind')!='offset' or not same_ref(desc['source'].get('manifest'),accepted_ref):
                    raise ValueError('SIGNED_DESCRIPTOR_ACCEPTED_MANIFEST_MISMATCH')
                if not hasattr(p.source.roster,'a') or set(v['gas'])!={'body','route_a'} or not v['positive_components_verified']:
                    raise ValueError('ACTUAL_SIGNED_COMPONENTS_UNAVAILABLE')
                if state['nonnegative_masses'] is not False:raise ValueError('SIGNED_STATE_MISLABELED_NONNEGATIVE')
                resolved_components.extend(x['ordinal'] for x in components if x['stage']==o['stage'])
            else:
                if state['nonnegative_masses'] is not True:raise ValueError('ACTUAL_SOURCE_HAS_NEGATIVE_MASSES')
                if set(v['gas'])!={'gas'} or v['gas']['gas'].get('positive_gas_zero_mode') is not True:
                    raise ValueError('POSITIVE_GAS_ZERO_MODE_UNESTABLISHED')
            for rr in p.input_pins+i1t['source_files']+list(r.pins.values())+[entry['packet'],entry['reconstruction']]:
                C.read_pin(rr,document=False)
                old=verified.get(rr['path'])
                if old is not None and old['sha256']!=rr['sha256']:raise ValueError('JOIN_INPUT_PIN_CONFLICT')
                verified[rr['path']]=rr
            key=(state['state_sha256'],state['source_sha256'],state['stage_kind'])
            if key in states and states[key]!=state:raise ValueError('SAME_STATE_CONFLICTING_MASS_CLASSIFICATION')
            states[key]=state
            joined.append({'ordinal':o['ordinal'],'state':state,'reconstruction':entry['reconstruction'],
                           'packet':entry['packet'],'occurrence_receipt':receipt,'computed_i1t':i1t})
        if set(resolved_components)!={x['ordinal'] for x in components}:raise ValueError('SIGNED_COMPONENT_COVERAGE_INCOMPLETE')
        # Recheck every pin after all arithmetic; a completed join refers to one
        # immutable byte snapshot, not observations made at different times.
        for rr in verified.values():
            if C.sha(rr['path'])!=rr['sha256']:raise ValueError('JOIN_INPUT_CHANGED_DURING_REPLAY')
        out.update(complete=True,states=list(states.values()),joined_occurrences=joined,
                   resolved_signed_component_ordinals=sorted(resolved_components),verified_files=list(verified.values()),
                   resolved_discovery_blockers=discovery['blockers'],point_status='PENDING_CERTIFICATES')
    except (OSError,ValueError,KeyError,TypeError,AttributeError,IndexError,OverflowError) as exc:
        out['blockers'].append({'code':'STATE_JOIN_UNAVAILABLE','owner':'Codex2 replay-plan/source implementation',
                                'detail':type(exc).__name__+': '+str(exc),'status':'UNTESTED'})
    return out
