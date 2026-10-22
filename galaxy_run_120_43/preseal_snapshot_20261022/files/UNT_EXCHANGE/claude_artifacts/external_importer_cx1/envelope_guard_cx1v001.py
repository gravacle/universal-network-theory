"""Private single-read envelope comparison; no snapshot production or launch.
Expected phase/pinset/coverage must come from authenticated root registration.
Passing this prerequisite alone never authorizes import.
"""
import types
from snapshot_cx1v001 import Refusal

SHA='0fac239ad7e5573084bfa494e55a344f40ab4deaa3469d5d54671ca5b457598c'
def need(ok,why):
    if not ok: raise Refusal(why)

def check_envelope(snapshot, *, tool_pin, start_pin, end_pin, phase, pin_set, required_pins):
    raw=snapshot.pin(tool_pin)
    need(tool_pin['sha256']==SHA,'ENVELOPE_TOOL_VERSION')
    m=types.ModuleType('_cx1_envelope');m.__file__=tool_pin['path']
    exec(compile(raw,tool_pin['path'],'exec'),m.__dict__)
    need(type(phase) is str and bool(phase),'ENVELOPE_PHASE_REQUIRED')
    need(type(pin_set) is dict and set(pin_set)=={'body_sha256','file_sha256'},'ENVELOPE_PINSET_REQUIRED')
    for h in pin_set.values():
        need(type(h) is str and len(h)==64 and all(c in '0123456789abcdef' for c in h),'ENVELOPE_PINSET_SHA')
    need(type(required_pins) is list and bool(required_pins),'ENVELOPE_COVERAGE_REQUIRED')
    required=set()
    for p in required_pins:
        need(type(p) is dict and set(p)=={'path','sha256'} and type(p['path']) is str
             and type(p['sha256']) is str,'ENVELOPE_COVERAGE_PIN')
        pair=(p['path'],p['sha256']);need(pair not in required,'ENVELOPE_DUPLICATE_REQUIRED_PIN');required.add(pair)
    allowed={p['path']:p for p in (start_pin,end_pin)}
    need(len(allowed)==2,'ENVELOPE_SAME_MANIFEST')
    def load(path,schema,expected_sha=None):
        need(path in allowed and allowed[path]['sha256']==expected_sha,'ENVELOPE_UNEXPECTED_READ')
        need(m.never_open_reason(path) is None and m.content_guard(path) is None,'ENVELOPE_GUARDED_PATH')
        obj=snapshot.document(allowed[path])
        need(type(obj) is dict and obj.get('schema')==schema,'ENVELOPE_SCHEMA')
        body={k:v for k,v in obj.items() if k!='body_sha256'}
        need(obj.get('body_sha256')==m.sha_b(m.canon(body).encode('ascii')),'ENVELOPE_BODY_HASH')
        need(obj.get('phase')==phase,'ENVELOPE_FOREIGN_PHASE')
        actual=obj.get('pin_set')
        need(type(actual) is dict and all(actual.get(k)==v for k,v in pin_set.items()),'ENVELOPE_FOREIGN_PINSET')
        need(obj.get('unresolved_pins')==[],'ENVELOPE_UNRESOLVED')
        pi,fi=m._index(obj,'import')
        need(required.issubset(pi),'ENVELOPE_REQUIRED_PIN_MISSING')
        for pair in required:
            entry=pi[pair];file=fi[entry['realpath']]
            need(entry.get('match') is True and entry.get('status')=='match'
                 and file.get('status')=='ok' and file.get('sha256_from_bytes')==pair[1], 'ENVELOPE_REQUIRED_PIN_UNMATCHED')
        return obj,expected_sha,path
    m.load_signed=load
    summaries=[];m._summary=summaries.append
    try:
        rc=m.compare(start_pin['path'],end_pin['path'],start_pin['sha256'],end_pin['sha256'],None)
    except m.Refusal as exc:
        raise Refusal('ENVELOPE_COMPARATOR_REFUSED:'+str(exc)) from exc
    need(rc==0,'ENVELOPE_INVALIDATED')
    return {'prerequisites_only':True,'start':dict(start_pin),'end':dict(end_pin),
            'phase':phase,'pin_set':dict(pin_set),'comparison':summaries[-1]}
