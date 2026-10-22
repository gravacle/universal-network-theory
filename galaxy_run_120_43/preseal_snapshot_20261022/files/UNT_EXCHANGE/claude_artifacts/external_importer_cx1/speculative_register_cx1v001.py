"""Pinned speculative registration prerequisite, never an admission decision.
The caller must authenticate register_pin and context through root-approved inputs.
Statuses are deliberately absent: a register cannot certify completion or failure.
"""
from snapshot_cx1v001 import Refusal

def need(ok,why):
    if not ok: raise Refusal(why)

def select_registered(snapshot, *, register_pin, context, theta_key, spec_pin, driver_pin):
    reg=snapshot.document(register_pin)
    need(type(reg) is dict and set(reg)=={'schema','context','entries'},'REGISTER_SHAPE')
    need(reg['schema']=='CX1_SPECULATIVE_REGISTER_V001','REGISTER_SCHEMA')
    need(type(context) is dict and set(context)=={'config_sha256','cache_id','gate_digest'}
         and all(type(v) is str and bool(v) for v in context.values()),'REGISTER_EXPECTED_CONTEXT')
    need(reg['context']==context,'REGISTER_CONTEXT')
    need(type(reg['entries']) is list,'REGISTER_ENTRIES')
    seen=set();matches=[]
    for entry in reg['entries']:
        need(type(entry) is dict and set(entry)=={'theta_key','spec','driver','direct_plan','case','runtime_environment','envelope_phase'},'REGISTER_ENTRY_SHAPE')
        need(type(entry['theta_key']) is str and bool(entry['theta_key']) and type(entry['case']) is str and bool(entry['case']), 'REGISTER_ENTRY_KEY')
        for key in ('spec','driver','direct_plan','runtime_environment'):
            pin=entry[key]
            need(type(pin) is dict and set(pin)=={'path','sha256'} and type(pin['path']) is str and pin['path'].startswith('/') and type(pin['sha256']) is str and len(pin['sha256'])==64 and all(c in '0123456789abcdef' for c in pin['sha256']), 'REGISTER_PIN')
        need(type(entry['envelope_phase']) is str and bool(entry['envelope_phase']),'REGISTER_PHASE')
        identity=(entry['theta_key'],entry['spec']['sha256'])
        need(identity not in seen,'REGISTER_AMBIGUOUS_REQUEST');seen.add(identity)
        if entry['theta_key']==theta_key and entry['spec']==spec_pin:
            need(entry['driver']==driver_pin,'REGISTER_DRIVER')
            matches.append(entry)
    need(len(matches)<=1,'REGISTER_AMBIGUOUS_REQUEST')
    # No source evidence is read for unrelated speculative calls. In particular,
    # no status/invalid response is imported before a natural plan requests it.
    return matches[0] if matches else None
