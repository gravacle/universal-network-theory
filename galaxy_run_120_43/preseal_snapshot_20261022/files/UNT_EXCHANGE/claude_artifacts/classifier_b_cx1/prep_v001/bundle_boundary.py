"""Independent B bundle boundary, based on published input/output contracts.
Pure bytes/dictionaries only: no filesystem or scientific data access.
"""
import hashlib,json,math,re
ROLES=('phase_inputs','freeze_manifest','score','slots','gate_status_list','tsr_flag_record','tsr_support_record','ntest_compare','stage0_status','commitment_status','agree_record','phase1_classification','l1_record','c3_record','root_disclosures','fallback','field_map')
KEYS={'schema','mode','inputs','rosters','sealed','phase1_tool','module_sha256'}
class Defect(ValueError):pass

def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise Defect('DUPLICATE_KEY:'+key)
            result[key]=value
        return result
    def constant(value):raise Defect('NON_FINITE_CONSTANT:'+value)
    def number(value):
        x=float(value)
        if not math.isfinite(x):raise Defect('NON_FINITE_NUMBER:'+value)
        return x
    try: text=raw.decode('utf-8')
    except UnicodeError as e:raise Defect('NOT_UTF8') from e
    try:return json.loads(text,object_pairs_hook=pairs,parse_constant=constant,parse_float=number)
    except Defect:raise
    except (ValueError,RecursionError) as e:raise Defect('JSON_SYNTAX:'+type(e).__name__) from e

def hex64(x):return type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None

def pin(x):
    return type(x) is dict and set(x)=={'path','sha256'} and type(x['path']) is str and bool(x['path']) and hex64(x['sha256'])

def validate_bundle(x):
    # The order is externally visible and follows the published contract.
    if type(x) is not dict or x.get('schema')!='CLASSIFIER_A_BUNDLE_C4V001':raise Defect('BUNDLE_SCHEMA')
    if set(x)!=KEYS:raise Defect('BUNDLE_KEYS:'+repr(sorted(set(x)^KEYS)))
    if x['mode'] not in ('score','prescore'):raise Defect('BUNDLE_MODE')
    if type(x['inputs']) is not dict or set(x['inputs'])!=set(ROLES):raise Defect('BUNDLE_INPUT_ROLES')
    for role in ROLES:
        if x['inputs'][role] is not None and not pin(x['inputs'][role]):raise Defect('BUNDLE_PIN:'+role)
    if type(x['rosters']) is not dict or any(not pin(p) for p in x['rosters'].values()):raise Defect('BUNDLE_ROSTERS')
    s=x['sealed']
    if type(s) is not dict or set(s)!={'text','classifier','tsr_flag_record_sha256','stage0_successor'}:raise Defect('BUNDLE_SEALED')
    if not pin(s['text']) or not pin(s['classifier']) or not hex64(s['tsr_flag_record_sha256']) or (s['stage0_successor'] is not None and not pin(s['stage0_successor'])):raise Defect('BUNDLE_SEALED_PINS')
    t=x['phase1_tool']
    if type(t) is not dict or set(t)!={'sha256','module'} or not hex64(t['sha256']) or type(t['module']) is not str or not t['module']:raise Defect('BUNDLE_PHASE1_TOOL')
    # Selected tool sha/module association is a later semantic check; v003b
    # replaces v003a in the pending final schema. Do not infer it here.
    if not hex64(x['module_sha256']):raise Defect('BUNDLE_MODULE_SHA')
    return x

def parse_bundle(raw):
    try:x=strict_json(raw)
    except Defect as e:raise Defect('BUNDLE_UNREADABLE:'+str(e)) from e
    return validate_bundle(x)

def pinned_value(raw,expected):
    # Crucially, corrupted content is never parsed, even when malformed.
    if not hex64(expected):raise Defect('PIN_FORMAT')
    if hashlib.sha256(raw).hexdigest()!=expected:raise Defect('SHA256_MISMATCH')
    return strict_json(raw)
