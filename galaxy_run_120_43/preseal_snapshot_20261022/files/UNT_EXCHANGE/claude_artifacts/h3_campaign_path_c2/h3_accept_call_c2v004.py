"""Per-call acceptance step of the DDO154 calibration campaign (Claude2 h3_campaign_path_c2, c2v004; V006 A188 gap 3, A158, A192).

c2v004 (V006 A192 item 3: INCOMPLETE reruns once, failure readings are frozen; verifier B1, ADV rows C03 and C04) against
h3_accept_call_c2v003 (ae5ab4a6), and nothing else:
  * the entry must be a c2v004-line entry (ENTRY_NAME h3_campaign_entry_c2v004, checked before the wrapper loads; else
    ENTRY_NOT_C2V004_LINE): its wrapper refuses a reingest (VALID or certified MODEL_INVALID) whose record is not of the
    call's latest acceptance pass, and a certified MODEL_INVALID while the call dir holds TAIL_CERTIFICATE_ACCEPTANCE.json;
  * passes are counted by the wrapper's acceptance_passes (the handoff's ACCEPTANCE_TAILSTATES_C2V002_A<nnn> directories;
    any other ACCEPTANCE_TAILSTATES_* entry refuses, ACCEPTANCE_PASSES_UNREADABLE);
  * a second pass only after an INCOMPLETE first pass: with one pass in the call dir the step refuses, nothing written,
    unless root pins that pass's acceptance record (--first-pass-record ABS --first-pass-record-sha256 H) and it is the
    adopted handoff's record (A158) of THIS call dir and of its one pass (tailstate_dir) reading INCOMPLETE
    (ACCEPTANCE_RERUN_FIRST_PASS_RECORD_REQUIRED / ACCEPTANCE_RERUN_NOT_AFTER_INCOMPLETE).  An ACCEPTED,
    NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT or any other first reading stands.  Two passes: ACCEPTANCE_RERUN_LIMIT, as
    c2v003.  A first-pass record given while the call dir holds no pass refuses (FIRST_PASS_RECORD_WITHOUT_A_PASS).  The
    pass list is read again under the work-dir lock just before the handoff runs (ACCEPTANCE_PASSES_CHANGED);
  * f6_action of an INCOMPLETE second pass is HALT_ROOT_RULES_PER_CALL (a third pass refuses); the step record (schema
    H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V004) also carries acceptance_passes_after, acceptance_pass (the handoff's
    tailstate_dir) and first_pass_record.
usage: python3 -I -B h3_accept_call_c2v004.py <c2v003 arguments> [--first-pass-record /ABS/ACCEPTANCE_RECORD.json
                                                                   --first-pass-record-sha256 H]   (second pass only)
Text below is c2v003's.

Per-call acceptance step of the DDO154 calibration campaign (Claude2 h3_campaign_path_c2, c2v003; V006 A188 gap 3, A158, A192).

c2v003 (V006 A192 items 2-3) against h3_accept_call_c2v002 (c9058dd5), and nothing else:
  * the entry must be a c2v003-line entry (ENTRY_NAME h3_campaign_entry_c2v003, checked before the wrapper loads; else
    ENTRY_NOT_C2V003_LINE): its wrapper carries the R-C8 ledger and the certified MODEL_INVALID path;
  * step 5 reads the registered point through the wrapper's one lookup, Context.certificate_record (genesis registry U
    ledger), not the genesis registry alone (design map 3.3, ACC L160-163);
  * A192 item 3, INCOMPLETE "reruns once": the step refuses (ACCEPTANCE_RERUN_LIMIT, nothing written) when the call dir
    already holds two handoff passes (two ACCEPTANCE_TAILSTATES_* directories; the handoff makes one per pass, v004 L90, L226);
  * the step record (schema H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V003) also carries the registered prelaunch bundle, the
    handoff's rows_are_model_output, and f6_action, the A192 item 3 row for the reading (CACHED_VALID;
    RERUN_ACCEPTANCE_ONCE_AFTER_ROOT_CHECKS_INPUTS; CERTIFIED_MODEL_INVALID_ELIGIBLE, i.e. root may run the entry's
    reingest-invalid with this record; HALT_ROOT_RULES_PER_CALL).  The step never runs reingest-invalid itself.
Text below is c2v002's.

c2v002 (V006 A191 B2) against h3_accept_call_c2v001 (05651663), and nothing else: the entry must be a c2v002-line entry
(ENTRY_NAME h3_campaign_entry_c2v002, checked before the wrapper loads; else ENTRY_NOT_C2V002_LINE), step 8 passes the
handoff's own acceptance record pin to the entry's reingest (which refuses unless that record is the v004 ACCEPTED record
of this call, receipt and bundle), and the step record schema is H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V002.

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
  8. reingest(wave, call_index, bundle, acceptance record) through the entry (its own guards including the record check,
     the wrapper's lock and write_acceptance, the certificate re-check, classify, cache put).
It writes ACCEPT_STEP_RECORD_W<wave>_C<call>.json (exclusive create) in --records-dir once the handoff ran.

usage: python3 -I -B h3_accept_call_c2v003.py --entry ENTRY.py --entry-sha256 H --config CFG --wave W --call-index I
                                            --deps DEPS.json --deps-sha256 H --records-dir NEW_DIR
exit: 0 accepted and reingested; 3 refused; 8 locked; 13 handoff reading not accepted (nothing reingested).
"""
import argparse
import hashlib
import importlib.util
import json
import os
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
ENTRY_LINE = 'h3_campaign_entry_c2v004'           # c2v004 B1: the entry whose wrapper carries the latest-pass rule
TAILSTATES_PREFIX = 'ACCEPTANCE_TAILSTATES_'      # handoff v004 L90: one directory per acceptance pass
MAX_PASSES = 2                                    # A192 item 3: INCOMPLETE reruns the acceptance step once
CERTIFIABLE_INVALID = ('NON_LAPSE_TAIL_MATERIAL', 'BOUND_INSUFFICIENT')    # A192 item 3 (handoff NOT_MODEL_OUTPUT, L86)
ACCEPTANCE_RECORD_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'           # c2v004 B1: handoff v004 L50
RERUNNABLE = 'INCOMPLETE'                                                    # c2v004 B1: A192 item 3, the only rerun reading


def f6_action(hrec, accepted, passes_after=1):
    """The A192 item 3 row for this reading (recorded; the step itself only reingests ACCEPTED readings)."""
    reading = hrec.get('reading')
    if accepted:
        return 'CACHED_VALID'
    if reading == 'INCOMPLETE' and passes_after >= MAX_PASSES:           # c2v004 B1: the one rerun is spent
        return 'HALT_ROOT_RULES_PER_CALL (A192 item 3: the one rerun read INCOMPLETE; a third pass refuses)'
    if reading == 'INCOMPLETE' and not hrec.get('tailstate_dir'):         # c2v004 B1: refused before its state export
        return ('RERUN_ACCEPTANCE_ONCE_AFTER_ROOT_CHECKS_INPUTS (A192 item 3; no new forward call; this attempt made no '
                'acceptance pass directory, so the pass count and the --first-pass-record rule are unchanged)')
    if reading == 'INCOMPLETE':
        return ('RERUN_ACCEPTANCE_ONCE_AFTER_ROOT_CHECKS_INPUTS (A192 item 3; no new forward call; pin this acceptance record '
                'as --first-pass-record)')
    if reading in CERTIFIABLE_INVALID and hrec.get('rows_are_model_output') is False \
            and not hrec.get('step4_stop_for_root_ruling'):
        return ('CERTIFIED_MODEL_INVALID_ELIGIBLE (A192 item 3): root may run the entry reingest-invalid with this '
                'acceptance record')
    return 'HALT_ROOT_RULES_PER_CALL (A192 item 3)'


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
    if getattr(E, 'ENTRY_NAME', None) != ENTRY_LINE:
        raise Refused('ENTRY_NOT_C2V004_LINE: ENTRY_NAME %r (%s required: its wrapper carries the latest-pass rule, '
                      'c2v004 B1)' % (getattr(E, 'ENTRY_NAME', None), ENTRY_LINE))
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


def first_pass_problems(M, call_dir, passes, ref):
    """c2v004 B1: [] iff ref pins the adopted handoff's record of THIS call dir and of its one pass, reading INCOMPLETE."""
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'} or not all(isinstance(ref[k], str) for k in ref) \
            or not os.path.isabs(ref['path']):
        return ['FIRST_PASS_RECORD_PIN_REQUIRED: an absolute {path, sha256}']
    try:
        rec = json.loads(M.O.read_pinned(ref, 'first-pass acceptance record'))
    except (M.Error, ValueError) as exc:
        return ['FIRST_PASS_RECORD_UNREADABLE: %s' % exc]
    if not isinstance(rec, dict):
        return ['FIRST_PASS_RECORD_SCHEMA: not an object']
    here = Path(call_dir).resolve()
    bad = []
    if rec.get('schema') != ACCEPTANCE_RECORD_SCHEMA:
        bad.append('FIRST_PASS_RECORD_SCHEMA: %r' % (rec.get('schema'),))
    if rec.get('handoff') != HANDOFF:
        bad.append('FIRST_PASS_RECORD_HANDOFF_NOT_A158: %r' % (rec.get('handoff'),))
    if rec.get('call_dir') != str(here):
        bad.append('FIRST_PASS_RECORD_OTHER_CALL: record %s; this call %s' % (rec.get('call_dir'), here))
    if rec.get('tailstate_dir') != str(here / passes[0]):
        bad.append('FIRST_PASS_RECORD_NOT_THE_FIRST_PASS: record pass %s; the call dir\'s one pass %s'
                   % (rec.get('tailstate_dir'), passes[0]))
    if rec.get('reading') != RERUNNABLE:
        bad.append('FIRST_PASS_READING_STANDS: %r (A192 item 3: only INCOMPLETE reruns; failure readings are frozen)'
                   % (rec.get('reading'),))
    return bad


def passes_of(M, call_dir):
    try:
        return M.acceptance_passes(call_dir)
    except (M.Error, OSError) as exc:
        raise Refused('ACCEPTANCE_PASSES_UNREADABLE: %s' % exc)


def accept(E, M, H, *, config, wave, call_index, deps_path, deps_sha256, records_dir, first_pass_ref=None):
    O = M.O
    ctx, plan, c, call_dir = locate(M, config, wave, call_index)
    receipt = finished(M, ctx, c, call_dir)
    orch = M.Orchestrator(ctx)
    orch.cache.open(create=False)
    if c['key'] in orch.cache.entries:
        raise Refused('ALREADY_ACCEPTED: key %s is cached' % c['key'][:16])
    passes = passes_of(M, call_dir)                                  # c2v004 B1: the wrapper's pass rule
    if len(passes) >= MAX_PASSES:
        raise Refused('ACCEPTANCE_RERUN_LIMIT: the call dir already holds %d acceptance passes %s (A192 item 3: INCOMPLETE '
                      'reruns once); root rules the call' % (len(passes), passes))
    if passes and first_pass_ref is None:                             # c2v004 B1
        raise Refused('ACCEPTANCE_RERUN_FIRST_PASS_RECORD_REQUIRED: the call dir holds the pass %s; a second pass runs only '
                      'after that pass read INCOMPLETE (A192 item 3): pin its acceptance record' % passes[0])
    if passes:
        bad = first_pass_problems(M, call_dir, passes, first_pass_ref)
        if bad:
            raise Refused('ACCEPTANCE_RERUN_NOT_AFTER_INCOMPLETE: %s' % bad)
    elif first_pass_ref is not None:
        raise Refused('FIRST_PASS_RECORD_WITHOUT_A_PASS: the call dir holds no acceptance pass')
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
    rec = ctx.certificate_record(M.point_identity(spec))           # c2v003: the wrapper's one lookup (genesis U ledger)
    if not isinstance(rec, dict) or not isinstance(rec.get('bundle'), dict):
        raise Refused('POINT_NOT_REGISTERED: %s' % M.M.digest(M.point_identity(spec))[:16])
    policy = dict({k: d['policy'][k] for k in POLICY_KEYS}, receipt=receipt, prelaunch_bundle=rec['bundle'])
    lock = O.Lock(ctx.work_dir)
    if not lock.acquire():
        return {'status': 'LOCKED', 'reasons': ['a run holds the work-dir lock']}
    try:
        if passes_of(M, call_dir) != passes:                          # c2v004 B1: read again under the lock
            raise Refused('ACCEPTANCE_PASSES_CHANGED: another pass appeared in %s' % call_dir)
        deps = H.load_deps(d['deps'])
        hrec, hrec_ref = H.accept_call(call_dir=str(call_dir), spec=spec, deps=deps, policy=policy,
                                       records_dir=str(records_dir), mode='guard')
    finally:
        lock.release()
    accepted = (hrec.get('reading') in ACCEPTED and hrec.get('outputs_are_evidence') is True
                and (hrec.get('guard') or {}).get('ok') is True and isinstance(hrec.get('bundle'), dict)
                and not hrec.get('step4_stop_for_root_ruling'))
    passes_after = len(passes) + (1 if hrec.get('tailstate_dir') else 0)     # c2v004 B1
    out = {'schema': 'H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V004', 'wave': int(wave), 'call_index': int(call_index),
           'key': c['key'], 'spec_sha256': c['spec_sha256'], 'call_dir': str(call_dir), 'receipt': receipt,
           'config_sha256': ctx.config_sha256, 'cache_id': ctx.cache_id, 'gate_digest': ctx.gate_digest,
           'deps_record': {'path': str(Path(deps_path).resolve()), 'sha256': deps_sha256},
           'handoff': {'path': H.__file__, 'sha256': sha_file(H.__file__)}, 'acceptance_record': hrec_ref,
           'reading': hrec.get('reading'), 'all_readings': hrec.get('all_readings'),
           'step4_stop_for_root_ruling': hrec.get('step4_stop_for_root_ruling'), 'bundle': hrec.get('bundle'),
           'guard_ok': (hrec.get('guard') or {}).get('ok'), 'blockers': hrec.get('blockers'),
           'prelaunch_bundle': rec['bundle'], 'rows_are_model_output': hrec.get('rows_are_model_output'),
           'outputs_are_evidence': hrec.get('outputs_are_evidence'),
           'f6_action': f6_action(hrec, accepted, passes_after), 'ledger': ctx.ledger_head(),
           'acceptance_passes_after': passes_after, 'acceptance_pass': hrec.get('tailstate_dir'),   # c2v004 B1
           'first_pass_record': first_pass_ref}
    if not accepted:
        out.update(status='NOT_ACCEPTED', reingest=None,
                   note='nothing reingested; the call stays INFRA CERTIFICATE_ACCEPTANCE_REFUSED; root rules (F6)')
    else:
        try:
            ri = E.reingest(M, config, int(wave), int(call_index), hrec['bundle'], hrec_ref)
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
    ap.add_argument('--first-pass-record')                           # c2v004 B1: second pass only
    ap.add_argument('--first-pass-record-sha256')
    return ap.parse_args(argv)


def execute(a, E, M, H):
    """accept() with the CLI's refusal handling and output; -> exit code."""
    try:
        if (a.first_pass_record is None) != (a.first_pass_record_sha256 is None):
            raise Refused('FIRST_PASS_RECORD_PIN_REQUIRED: --first-pass-record and --first-pass-record-sha256 together')
        fp = None if a.first_pass_record is None else {'path': a.first_pass_record, 'sha256': a.first_pass_record_sha256}
        out = accept(E, M, H, config=a.config, wave=a.wave, call_index=a.call_index, deps_path=a.deps,
                     deps_sha256=a.deps_sha256, records_dir=a.records_dir, first_pass_ref=fp)
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
