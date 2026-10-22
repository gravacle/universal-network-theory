"""Per-call acceptance step of the DDO154 calibration campaign (Claude2 h3_campaign_path_c2, c2v001; V006 A188 gap 3, A158).

Why.  Every finished campaign call reads INFRA CERTIFICATE_ACCEPTANCE_REFUSED at ingest (wrapper q5b1 L295-306) until its
call dir holds TAIL_CERTIFICATE_ACCEPTANCE.json, and only the wrapper's reingest (L335-358) writes it, from a post-state
certificate bundle.  This step makes that bundle the way C1 / CP-1 do (A134 Q2/Q3: the adopted handoff acceptance_q2 v004
5ff464cc, A158, with root's pinned producers) and then calls the entry's reingest.  It never writes a proof, never approves,
never picks a producer version, and changes no reading: the handoff's reading decides.

Steps (each refusal happens before anything is written unless stated):
  1. load the entry by path + sha (it pins the wrapper -> core -> policy -> parent); Context of --config; every gate passes;
  2. the call: waves/wave_W/WAVE_PLAN.json planned under this config_sha256, gate_digest and cache id; call_index I;
     campaign/call_000I/spec.json is the planned spec (bytes and content);
  3. FINISHED: RECEIPT.json verifies with the pinned monitor for this spec and driver, status FINISHED, driver_status
     COMPLETED, its result pin is out/result.json (bytes), finish.json binds it (parent finish_binding) -> else
     CALL_NOT_FINISHED;  the key is not cached already -> else ALREADY_ACCEPTED;
  4. the deps record (root-filled, C1 list; template ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json) by path + sha:
     deps.enumerator == config tail_readiness.state_enumerator (A139: the enumerator the acceptance uses); deps.guard is the
     wrapper's own guard (sha of the file the wrapper loaded); policy.approved_certificate_producers == config
     tail_readiness.approved_certificate_producers, exactly -> else DEPS_DIFFER_FROM_CONFIG;
  5. policy.prelaunch_bundle = the registered point's bundle (registry rec of point_identity(spec)); policy.receipt = this
     call's RECEIPT.json pin;
  6. under the work-dir lock (parent Lock; LOCKED if a run holds it): acceptance v004 accept_call(mode='guard') with
     records under --records-dir (must be new and under claude_artifacts, the handoff's Store rule).  The handoff writes its
     replay inputs and TailState exports into the call dir, as it does for every direct call (writer v002 / Store L219-233);
  7. the handoff reading must be ACCEPTED or ACCEPTED_PASS_FLAGGED with outputs_are_evidence, guard ok, a POST_STATE_BUNDLE
     and no step-4 stop (0690 OPEN-5); otherwise NOT_ACCEPTED (exit 13): nothing is reingested and root rules the call
     (no V006 ruling yet says what an INCOMPLETE / LO_UNCERTIFIED_TRANSIENT / NON_LAPSE_TAIL_MATERIAL campaign call does);
  8. reingest(wave, call_index, bundle) through the entry (its own guards, the wrapper's lock and write_acceptance, the
     certificate re-check, classify, cache put).
It writes ACCEPT_STEP_RECORD_W<wave>_C<call>.json (exclusive create) in --records-dir once the handoff ran.

usage: python3 -I -B h3_accept_call_c2v001.py --entry ENTRY.py --entry-sha256 H --config CFG --wave W --call-index I
                                            --deps DEPS.json --deps-sha256 H --records-dir NEW_DIR
exit: 0 accepted and reingested; 3 refused; 8 locked; 13 handoff reading not accepted (nothing reingested).
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HANDOFF = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
           'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}          # A158
DEPS_SCHEMA = 'H3_CAMPAIGN_ACCEPTANCE_DEPS_C2V001'
DEP_KEYS = ('enumerator', 'evidence', 'lo_core', 'guard', 'writer', 'row_producer', 'lo_adapter', 'srb_adapter')
POLICY_KEYS = ('approved_certificate_producers', 'trusted_source_producers', 'row_policy_reviews', 'packet_binding_reviews',
               'evidence_producer', 'approved_review_sha256', 'approved_evidence_producer_sha256',
               'approved_uniform_producer_sha256', 'root_ruling_refs')
ACCEPTED = ('ACCEPTED', 'ACCEPTED_PASS_FLAGGED')
EXIT = {'OK': 0, 'REFUSED': 3, 'LOCKED': 8, 'NOT_ACCEPTED': 13}


class Refused(Exception):
    pass


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_module(path, sha256, name):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise Refused('PIN_MISMATCH: %s' % path)
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def load_chain(entry_path, entry_sha256):
    E = load_module(entry_path, entry_sha256, '_h3_accept_entry')
    M = E.load_wrapper()
    E.check_patch(M)
    return E, M


def load_handoff(pin=HANDOFF):
    return load_module(pin['path'], pin['sha256'], '_h3_accept_handoff_v004')


def locate(M, config, wave, call_index):
    O = M.O
    ctx = M.Context(config)
    if not ctx.gates_ok():
        raise Refused('ACCEPT_GATES_NOT_PASSED: %s' % sorted(k for k, g in ctx.gates.items() if not g.get('ok')))
    wd = ctx.work_dir / 'waves' / ('wave_%04d' % int(wave))
    if not (wd / 'WAVE_PLAN.json').is_file():
        raise Refused('NO_WAVE_PLAN: %s' % wd)
    plan = O.load_json_file(wd / 'WAVE_PLAN.json', 'wave plan')
    if (plan.get('cache_id'), plan.get('config_sha256'), plan.get('gate_digest')) != \
            (ctx.cache_id, ctx.config_sha256, ctx.gate_digest):
        raise Refused('PLAN_CONFIG_OR_GATES_DIFFER: wave %s was planned under another cache id / config / gate digest' % wave)
    calls = [c for c in plan['calls'] if c['call_index'] == int(call_index)]
    if len(calls) != 1:
        raise Refused('CALL_INDEX_NOT_IN_PLAN: %s' % call_index)
    c = calls[0]
    call_dir = wd / 'campaign' / ('call_%04d' % int(call_index))
    sp = call_dir / 'spec.json'
    if not sp.is_file() or O.sha256_file(sp) != c['spec_sha256'] or O.load_json_file(sp, 'campaign spec') != c['spec']:
        raise Refused('SPEC_NOT_THE_PLANNED_SPEC: %s' % sp)
    return ctx, plan, c, call_dir


def finished(M, ctx, c, call_dir):
    """-> receipt pin.  CALL_NOT_FINISHED unless FINISHED / COMPLETED with a bound result (parent L2737-2771 rules)."""
    O = M.O
    rp = call_dir / 'RECEIPT.json'
    if not rp.is_file():
        raise Refused('CALL_NOT_FINISHED: no RECEIPT.json in %s' % call_dir)
    v = ctx.M.verify_receipt(rp, spec_sha256=c['spec_sha256'], driver_sha256=ctx.driver['sha256'])
    r = v.get('receipt') or {}
    res = call_dir / 'out' / 'result.json'
    if not v.get('ok') or r.get('status') != 'FINISHED' or r.get('driver_status') != 'COMPLETED' or not res.is_file() \
            or (r.get('result') or {}).get('sha256') != O.sha256_file(res):
        raise Refused('CALL_NOT_FINISHED: receipt %s/%s, verifies %s, result %s'
                      % (r.get('status'), r.get('driver_status'), v.get('ok'), res.is_file()))
    fin, why = O.finish_binding(res, O.sha256_file(res))
    if why:
        raise Refused('CALL_NOT_FINISHED: %s' % why)
    return {'path': str(rp), 'sha256': O.sha256_file(rp)}


def read_deps(path, sha256):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise Refused('DEPS_PIN_MISMATCH: %s' % path)
    d = json.loads(raw)
    if d.get('schema') != DEPS_SCHEMA or d.get('status') != 'ROOT_FILLED':
        raise Refused('DEPS_NOT_FILLED: schema %s, status ROOT_FILLED required' % DEPS_SCHEMA)
    pins, pol = d.get('deps') or {}, d.get('policy') or {}
    miss = [k for k in DEP_KEYS if not isinstance(pins.get(k), dict)] + [k for k in POLICY_KEYS if k not in pol]
    if miss:
        raise Refused('DEPS_INCOMPLETE: %s' % miss)
    return d


def accept(E, M, H, *, config, wave, call_index, deps_path, deps_sha256, records_dir):
    O = M.O
    ctx, plan, c, call_dir = locate(M, config, wave, call_index)
    receipt = finished(M, ctx, c, call_dir)
    orch = M.Orchestrator(ctx)
    orch.cache.open(create=False)
    if c['key'] in orch.cache.entries:
        raise Refused('ALREADY_ACCEPTED: key %s is cached' % c['key'][:16])
    d = read_deps(deps_path, deps_sha256)
    tr = ctx.cfg['tail_readiness']
    bad = []
    if d['deps']['enumerator'] != tr.get('state_enumerator'):
        bad.append('deps.enumerator != config tail_readiness.state_enumerator')
    if d['deps']['guard'].get('sha256') != O.sha256_file(M.G.__file__):
        bad.append('deps.guard is not the wrapper guard %s' % O.sha256_file(M.G.__file__)[:16])
    if d['policy']['approved_certificate_producers'] != tr.get('approved_certificate_producers'):
        bad.append('policy.approved_certificate_producers != config tail_readiness.approved_certificate_producers')
    if bad:
        raise Refused('DEPS_DIFFER_FROM_CONFIG: %s' % bad)
    spec = O.load_json_file(call_dir / 'spec.json', 'campaign spec')
    registry = M.M.pin_doc(tr['certificate_registry'], 'certificate registry')
    rec = (registry.get('points') or {}).get(M.M.digest(M.point_identity(spec)))
    if not isinstance(rec, dict) or not isinstance(rec.get('bundle'), dict):
        raise Refused('POINT_NOT_REGISTERED: %s' % M.M.digest(M.point_identity(spec))[:16])
    policy = dict({k: d['policy'][k] for k in POLICY_KEYS}, receipt=receipt, prelaunch_bundle=rec['bundle'])
    lock = O.Lock(ctx.work_dir)
    if not lock.acquire():
        return {'status': 'LOCKED', 'reasons': ['a run holds the work-dir lock']}
    try:
        deps = H.load_deps(d['deps'])
        hrec, hrec_ref = H.accept_call(call_dir=str(call_dir), spec=spec, deps=deps, policy=policy,
                                       records_dir=str(records_dir), mode='guard')
    finally:
        lock.release()
    accepted = (hrec.get('reading') in ACCEPTED and hrec.get('outputs_are_evidence') is True
                and (hrec.get('guard') or {}).get('ok') is True and isinstance(hrec.get('bundle'), dict)
                and not hrec.get('step4_stop_for_root_ruling'))
    out = {'schema': 'H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V001', 'wave': int(wave), 'call_index': int(call_index),
           'key': c['key'], 'spec_sha256': c['spec_sha256'], 'call_dir': str(call_dir), 'receipt': receipt,
           'config_sha256': ctx.config_sha256, 'cache_id': ctx.cache_id, 'gate_digest': ctx.gate_digest,
           'deps_record': {'path': str(Path(deps_path).resolve()), 'sha256': deps_sha256},
           'handoff': {'path': H.__file__, 'sha256': sha_file(H.__file__)}, 'acceptance_record': hrec_ref,
           'reading': hrec.get('reading'), 'all_readings': hrec.get('all_readings'),
           'step4_stop_for_root_ruling': hrec.get('step4_stop_for_root_ruling'), 'bundle': hrec.get('bundle'),
           'guard_ok': (hrec.get('guard') or {}).get('ok'), 'blockers': hrec.get('blockers')}
    if not accepted:
        out.update(status='NOT_ACCEPTED', reingest=None,
                   note='nothing reingested; the call stays INFRA CERTIFICATE_ACCEPTANCE_REFUSED; root rules (F6)')
    else:
        try:
            ri = E.reingest(M, config, int(wave), int(call_index), hrec['bundle'])
        except Exception as exc:                   # noqa: BLE001 -- recorded; a failed reingest is never a pass
            ri = {'status': 'REFUSED', 'reasons': ['%s: %s' % (type(exc).__name__, exc)]}
        out.update(status='OK' if ri.get('status') == 'OK' else ri.get('status', 'REFUSED'), reingest=ri)
    with open(Path(records_dir) / ('ACCEPT_STEP_RECORD_W%04d_C%04d.json' % (int(wave), int(call_index))), 'x') as f:
        json.dump(out, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    return out


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ('--entry', '--entry-sha256', '--config', '--deps', '--deps-sha256', '--records-dir'):
        ap.add_argument(k, required=True)
    ap.add_argument('--wave', type=int, required=True)
    ap.add_argument('--call-index', type=int, required=True)
    return ap.parse_args(argv)


def execute(a, E, M, H):
    """accept() with the CLI's refusal handling and output; -> exit code."""
    try:
        out = accept(E, M, H, config=a.config, wave=a.wave, call_index=a.call_index, deps_path=a.deps,
                     deps_sha256=a.deps_sha256, records_dir=a.records_dir)
    except Refused as exc:
        out = {'status': 'REFUSED', 'reasons': [str(exc)]}
    except Exception as exc:                       # noqa: BLE001 -- any other failure is a refusal, never a pass
        out = {'status': 'REFUSED', 'reasons': ['%s: %s' % (type(exc).__name__, exc)]}
    out = dict(out, launches_performed=0)
    print(json.dumps(out, indent=1, sort_keys=True, default=str))
    return EXIT.get(out.get('status'), 3)


def main(argv=None):
    a = parse(argv)
    try:
        E, M = load_chain(a.entry, a.entry_sha256)
        H = load_handoff()
    except Refused as exc:
        print(json.dumps({'status': 'REFUSED', 'reasons': [str(exc)], 'launches_performed': 0}, indent=1))
        return 3
    return execute(a, E, M, H)


if __name__ == '__main__':
    sys.exit(main())
