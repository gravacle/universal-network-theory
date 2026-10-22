"""H3 campaign entry (Claude2 h3_campaign_path_c2, c2v004; V006 A192 item 3, verifier B1): successor of h3_campaign_entry_c2v003 (5710e1fa).

c2v004 against c2v003, and nothing else: WRAPPER / WRAPPER_SHA pin the c2v004 wrapper source
calibration_orchestrator_q5b1_ledger_c2v004.py (c2v003 plus B1: a reingest record must be of the call's latest acceptance
pass; reingest_invalid also refuses while the call dir holds TAIL_CERTIFICATE_ACCEPTANCE.json); ENTRY_NAME names this
successor; `reingest` hands its acceptance record to the wrapper's reingest, which refuses under the work-dir lock, before
anything is written, a record that is not of the latest pass.  The generator make_campaign_cascade_c2v004 rewrites exactly
the WRAPPER and WRAPPER_SHA lines when it re-pins the chain.  Text below is c2v003's.

H3 campaign entry (Claude2 h3_campaign_path_c2, c2v003; V006 A192 items 2-3): successor of h3_campaign_entry_c2v002 (75b4cafa).

What it is.  The launch entry of the DDO154 calibration campaign.  It loads the wrapper from its bytes after a sha256 check; the
wrapper pins its core, the core pins the adoption policy and the parent c75a889f, and the wrapper/core replace the parent's
module globals Context, Orchestrator, Mapper, Cache, CampaignExecutor, check_deciding, check_numerics and resolve.  `plan`,
`status`, `run` and `resolve` are the parent's own main(argv) over that patched module (no argument added, removed or
reinterpreted; parent exit codes unchanged).  `reingest` is c2v002's (A191 B2), byte for byte in behaviour.

Changes against c2v002, and nothing else:
  1. WRAPPER / WRAPPER_SHA pin the c2v003 wrapper source calibration_orchestrator_q5b1_ledger_c2v003.py (q5b1 7a6af535 plus
     the R-C8 ledger and the certified MODEL_INVALID path).  The generator make_campaign_cascade_c2v003 rewrites exactly these
     two lines when it re-pins the chain.  ENTRY_NAME names this successor.
  2. `reingest-invalid --wave W --call-index I --acceptance-record /ABS/ACCEPTANCE_RECORD.json --acceptance-record-sha256 H`
     (V006 A192 item 3, F6): before the wrapper is called, the record path is absolute, every gate passes and the wave plan
     has this config_sha256 / gate_digest and holds the call index; then the wrapper's Orchestrator.reingest_invalid (lock,
     prepare, SF1 identity, cache id, spec, the record of THIS call reading NON_LAPSE_TAIL_MATERIAL or BOUND_INSUFFICIENT with
     rows_are_model_output false, its FINISHED receipt and result, its registered point; cache put MODEL_INVALID, source
     TAIL_ACCEPTANCE_CERTIFIED).  No forward call.  Root's act, call by call.  Exit 0 OK, 3 REFUSED, 8 LOCKED.
  3. `points-manifest --out-dir NEW` (design map 3.3, the manifest tool; read-only on the campaign): the read-only probe's
     next-wave misses (core `wave`, L370-373) whose point has no record in the genesis registry or the ledger, each written as
     its mapper-built spec (pending slots) into NEW (exclusive mkdir, under claude_artifacts), plus POINTS_LIST.json, the input
     of the CP-1 list-of-points successor (cp1_points_runner_c2v001).  Exit 0 written, 3 refused.
  4. `ledger-append --records R --records-sha256 H`: the CP-1 list assembler's ledger records (cp1_points_assembler_c2v001
     `records`), appended by the wrapper's Orchestrator.ledger_append under the work-dir lock (every check first, then one
     append; the head sha is printed for the wave record).  Exit 0 OK, 3 REFUSED, 8 LOCKED.
  5. `ledger-status`: read-only; the verified ledger's entries and head.  Exit 0, 3 if the ledger does not verify.

usage:
  python3 -I -B h3_campaign_entry_<SUB>.py plan     --config CFG
  python3 -I -B h3_campaign_entry_<SUB>.py status   --config CFG
  python3 -I -B h3_campaign_entry_<SUB>.py run      --config CFG [--new-campaign] [--max-waves N]
  python3 -I -B h3_campaign_entry_<SUB>.py resolve  --config CFG --wave W (--token T ... | --all --halt-sha256 H)
                                                    --decision retry|retry_with_recovery [--recovery P] --reason TEXT
  python3 -I -B h3_campaign_entry_<SUB>.py reingest --config CFG --wave W --call-index I --bundle /ABS/B --bundle-sha256 H
                                                    --acceptance-record /ABS/ACCEPTANCE_RECORD.json --acceptance-record-sha256 H
  python3 -I -B h3_campaign_entry_<SUB>.py reingest-invalid --config CFG --wave W --call-index I
                                                    --acceptance-record /ABS/ACCEPTANCE_RECORD.json --acceptance-record-sha256 H
  python3 -I -B h3_campaign_entry_<SUB>.py points-manifest --config CFG --out-dir /ABS/NEW_DIR
  python3 -I -B h3_campaign_entry_<SUB>.py ledger-append   --config CFG --records /ABS/LEDGER_RECORDS.json --records-sha256 H
  python3 -I -B h3_campaign_entry_<SUB>.py ledger-status   --config CFG
`run` must be started through launch_setsid_c2v005.py (C4-4: a non-synthetic run refuses unless it is the session leader).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

WRAPPER = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py')
WRAPPER_SHA = '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'
PARENT_SHA = 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'
ENTRY_NAME = 'h3_campaign_entry_c2v004'
REINGEST_EXIT = {'OK': 0, 'REFUSED': 3, 'LOCKED': 8}
HANDOFF = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
           'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}          # A158
ACCEPTANCE_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'                                          # handoff v004 L50
ACCEPTED = ('ACCEPTED', 'ACCEPTED_PASS_FLAGGED')
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
POINTS_LIST_SCHEMA = 'H3_CAMPAIGN_POINTS_LIST_C2V003'
RECORDS_SCHEMA = 'CP1_POINTS_LEDGER_RECORDS_C2V001'                      # cp1_points_assembler_c2v001 `records`
MAX_POINTS_PER_WAVE = 99                                                # CP-1 row = 100 x wave + i


def load_wrapper():
    raw = WRAPPER.read_bytes()
    if hashlib.sha256(raw).hexdigest() != WRAPPER_SHA:
        raise SystemExit('PIN_MISMATCH wrapper %s' % WRAPPER)
    sp = importlib.util.spec_from_file_location('_cx2q5b1l_h3_entry', WRAPPER)
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    exec(compile(raw, str(WRAPPER), 'exec'), m.__dict__)
    return m


def check_patch(M):
    O = M.O
    if hashlib.sha256(Path(O.__file__).read_bytes()).hexdigest() != PARENT_SHA:
        raise SystemExit('PIN_MISMATCH parent %s' % O.__file__)
    if O.Context is not M.Context or O.Orchestrator is not M.Orchestrator or O.Mapper is not M.Mapper:
        raise SystemExit('wrapper patch not installed on the parent module')
    return O


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and isinstance(x['sha256'], str)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def acceptance_problems(M, ctx, call, call_dir, bundle_ref, acceptance_ref):
    """[] iff the record is the adopted handoff's ACCEPTED record for this call, receipt and bundle (A191 B2; c2v002)."""
    O = M.O
    rec = json.loads(O.read_pinned(acceptance_ref, 'acceptance record'))
    if not isinstance(rec, dict):
        return ['REINGEST_ACCEPTANCE_RECORD_SCHEMA: not a JSON object']
    bad = []
    if rec.get('schema') != ACCEPTANCE_SCHEMA:
        bad.append('REINGEST_ACCEPTANCE_RECORD_SCHEMA: %r (%s required)' % (rec.get('schema'), ACCEPTANCE_SCHEMA))
    if rec.get('handoff') != HANDOFF:
        bad.append('REINGEST_ACCEPTANCE_HANDOFF_NOT_A158: %r' % (rec.get('handoff'),))
    guard_ok = (rec.get('guard') or {}).get('ok') if isinstance(rec.get('guard'), dict) else None
    if rec.get('reading') not in ACCEPTED or rec.get('outputs_are_evidence') is not True or guard_ok is not True \
            or rec.get('step4_stop_for_root_ruling') is not False:
        bad.append('REINGEST_ACCEPTANCE_NOT_ACCEPTED: reading %r, outputs_are_evidence %r, guard ok %r, step4 stop %r'
                   % (rec.get('reading'), rec.get('outputs_are_evidence'), guard_ok, rec.get('step4_stop_for_root_ruling')))
    here = Path(call_dir).resolve()
    if rec.get('call_dir') != str(here):
        bad.append('REINGEST_ACCEPTANCE_RECORD_OTHER_CALL: record call_dir %s; this call %s' % (rec.get('call_dir'), here))
    rp, res = here / 'RECEIPT.json', (here / 'out' / 'result.json').resolve()
    if not rp.is_file():
        bad.append('REINGEST_RECEIPT_NOT_FINISHED: no RECEIPT.json in %s' % here)
    else:
        v = ctx.M.verify_receipt(rp, spec_sha256=call['spec_sha256'], driver_sha256=ctx.driver['sha256'])
        r = v.get('receipt') or {}
        rsha = (r.get('result') or {}).get('sha256')
        if not v.get('ok') or r.get('status') != 'FINISHED' or r.get('driver_status') != 'COMPLETED':
            bad.append('REINGEST_RECEIPT_NOT_FINISHED: receipt %s/%s, verifies %s'
                       % (r.get('status'), r.get('driver_status'), v.get('ok')))
        if rec.get('result') != {'path': str(res), 'sha256': rsha} or not res.is_file() or O.sha256_file(res) != rsha:
            bad.append('REINGEST_ACCEPTANCE_RECORD_OTHER_RECEIPT: record result %r; receipt result %s; result file %s'
                       % (rec.get('result'), rsha, res))
    if rec.get('bundle') != bundle_ref:
        bad.append('REINGEST_ACCEPTANCE_BUNDLE_DIFFERS: record bundle %r; --bundle %r' % (rec.get('bundle'), bundle_ref))
    return bad


def planned_call(M, ctx, wave, call_index, tag):
    """The wave plan's call I, refused unless the plan was made under this config_sha256 and gate digest (parent L3320)."""
    O = M.O
    wd = ctx.work_dir / 'waves' / ('wave_%04d' % int(wave))
    pp = wd / 'WAVE_PLAN.json'
    if not pp.is_file():
        return None, None, '%s_NO_WAVE_PLAN: %s' % (tag, pp)
    plan = O.load_json_file(pp, 'wave plan')
    if plan.get('config_sha256') != ctx.config_sha256 or plan.get('gate_digest') != ctx.gate_digest:
        return None, None, ('%s_PLAN_CONFIG_OR_GATES_DIFFER: wave %s was planned under config %s gates %s; this config gives '
                            '%s / %s' % (tag, wave, str(plan.get('config_sha256'))[:16], str(plan.get('gate_digest'))[:16],
                                         ctx.config_sha256[:16], ctx.gate_digest[:16]))
    calls = [c for c in plan.get('calls') or [] if c.get('call_index') == int(call_index)]
    if len(calls) != 1:
        return None, None, '%s_CALL_INDEX_NOT_IN_PLAN: %s' % (tag, call_index)
    return calls[0], wd, None


def reingest(M, config, wave, call_index, bundle_ref, acceptance_ref=None):
    """Entry guards, then the wrapper's own reingest.  Returns the wrapper's dict or a REFUSED dict (c2v002, unchanged)."""
    O = M.O
    if not is_pin(bundle_ref):
        return {'status': 'REFUSED', 'reasons': ['REINGEST_BUNDLE_PIN_REQUIRED: {path, sha256}']}
    if not is_pin(acceptance_ref):
        return {'status': 'REFUSED', 'reasons': ['REINGEST_ACCEPTANCE_RECORD_REQUIRED: {path, sha256} of the acceptance_q2 '
                                                 'v004 record of this call (V006 A191 B2)']}
    rel = [p for p in (bundle_ref['path'], acceptance_ref['path']) if not os.path.isabs(p)]
    if rel:
        return {'status': 'REFUSED', 'reasons': ['REINGEST_ABSOLUTE_PATHS_REQUIRED: %s' % rel]}
    ctx = M.Context(config)
    if not ctx.gates_ok():
        return {'status': 'REFUSED', 'reasons': ['REINGEST_GATES_NOT_PASSED: %s'
                                                 % sorted(k for k, g in ctx.gates.items() if not g.get('ok'))]}
    call, wd, why = planned_call(M, ctx, wave, call_index, 'REINGEST')
    if why:
        return {'status': 'REFUSED', 'reasons': [why]}
    O.read_pinned(bundle_ref, 'post-state certificate bundle')
    bad = acceptance_problems(M, ctx, call, wd / 'campaign' / ('call_%04d' % int(call_index)), bundle_ref, acceptance_ref)
    if bad:
        return {'status': 'REFUSED', 'reasons': bad}
    return M.Orchestrator(ctx).reingest(int(wave), int(call_index), bundle_ref, acceptance_ref)   # c2v004 B1: latest pass


def reingest_invalid(M, config, wave, call_index, acceptance_ref):
    """c2v003 F6 (V006 A192 item 3): entry guards, then the wrapper's Orchestrator.reingest_invalid."""
    if not is_pin(acceptance_ref):
        return {'status': 'REFUSED', 'reasons': ['REINGEST_INVALID_ACCEPTANCE_RECORD_REQUIRED: {path, sha256}']}
    if not os.path.isabs(acceptance_ref['path']):
        return {'status': 'REFUSED', 'reasons': ['REINGEST_INVALID_ABSOLUTE_PATH_REQUIRED: %s' % acceptance_ref['path']]}
    ctx = M.Context(config)
    if not ctx.gates_ok():
        return {'status': 'REFUSED', 'reasons': ['REINGEST_INVALID_GATES_NOT_PASSED: %s'
                                                 % sorted(k for k, g in ctx.gates.items() if not g.get('ok'))]}
    _, _, why = planned_call(M, ctx, wave, call_index, 'REINGEST_INVALID')
    if why:
        return {'status': 'REFUSED', 'reasons': [why]}
    return M.Orchestrator(ctx).reingest_invalid(int(wave), int(call_index), acceptance_ref)


def lexical_artifacts_dir(p):
    """An absolute, normalized path under claude_artifacts with no run-tree / NGC3198 / UVT_ / C5H / .codex component."""
    if not isinstance(p, str) or not os.path.isabs(p) or os.path.normpath(p) != p or not p.startswith(ART + '/'):
        return 'must be an absolute normalized path under %s' % ART
    for s in Path(p).parts:
        f = s.casefold()
        if f.startswith('uvt_') or 'ngc3198' in f or f in ('runs', 'runs_ext', 'unt_internal_runs', '.codex',
                                                           'kmax_a2f10_c5h_run_v001'):
            return 'forbidden path component %r' % s
    return None


def points_manifest(M, config, out_dir):
    """c2v003 (design map 3.3): the next wave's probe misses whose point is not registered, as mapper-built specs."""
    O = M.O
    bad = lexical_artifacts_dir(out_dir)
    if bad:
        return {'status': 'REFUSED', 'reasons': ['POINTS_MANIFEST_OUT_DIR: %s' % bad]}
    ctx = M.Context(config)
    orch = M.Orchestrator(ctx)
    orch.prepare(create=False)
    pr = orch.probe.run(orch.cache, 'probe')
    if pr.get('complete'):
        return {'status': 'REFUSED', 'reasons': ['POINTS_MANIFEST_PROBE_COMPLETE: no next wave (the next run step is the replay)']}
    misses = orch._dedup(pr['misses'])
    wave = len(orch.wave_dirs()) + 1
    pts, seen, registered = [], set(), 0
    for m in misses:
        b = ctx.mapper.build(m['theta'])
        if b['key'] != m['key']:
            return {'status': 'REFUSED', 'reasons': ['POINTS_MANIFEST_MAPPER_KEY_DIFFERS_FROM_PROBE_KEY']}
        pk = b['certificate_point_key']
        if ctx.certificate_record(b['certificate_identity']) is not None:
            registered += 1
            continue
        if pk in seen:
            continue
        seen.add(pk)
        pts.append((m, b, pk))
    if not pts:
        return {'status': 'REFUSED', 'reasons': ['POINTS_MANIFEST_NOTHING_TO_CERTIFY: every next-wave point is registered '
                                                 '(%d calls)' % len(misses)]}
    if len(pts) > MAX_POINTS_PER_WAVE:
        return {'status': 'REFUSED', 'reasons': ['POINTS_MANIFEST_TOO_MANY_POINTS: %d > %d' % (len(pts), MAX_POINTS_PER_WAVE)]}
    os.mkdir(out_dir)
    out = []
    for i, (m, b, pk) in enumerate(pts):
        sp = os.path.join(out_dir, 'SPEC_W%04d_P%02d_%s.json' % (wave, i, pk[:16]))
        with open(sp, 'xb') as f:
            f.write(b['raw'])
        if sha_bytes(Path(sp).read_bytes()) != b['sha256']:
            raise M.Error('POINTS_MANIFEST_WRITTEN_SPEC_DIFFERS')
        out.append({'row': 100 * wave + i, 'label': 'W%04d_P%02d' % (wave, i), 'key': pk, 'theta': m['theta'],
                    'call_key': m['key'], 'family': m.get('family'), 'branch': m.get('branch'), 'purpose': m.get('purpose'),
                    'spec': {'path': sp, 'sha256': b['sha256']}, 'pending_spec_sha256': b['sha256']})
    entry = os.path.realpath(globals()['__file__']) if globals().get('__file__') else None
    doc = {'schema': POINTS_LIST_SCHEMA, 'wave': wave, 'n_points': len(out), 'n_next_wave_calls': len(misses),
           'n_registered_skipped': registered, 'points': out, 'config_sha256': ctx.config_sha256, 'cache_id': ctx.cache_id,
           'ledger': ctx.ledger_head(), 'entry': {'path': entry, 'sha256': sha_bytes(Path(entry).read_bytes())} if entry else None,
           'wrapper': {'path': str(WRAPPER), 'sha256': WRAPPER_SHA}, 'utc': O.utc(),
           'rule': ('V006 A192 item 2 / design map 3.3: the read-only probe (core wave L370-373) lists the next wave; every '
                    'point without a genesis or ledger record is written as its mapper-built spec (pending slots).  The CP-1 '
                    'list-of-points successor certifies exactly these points; ledger-append then registers them.')}
    raw = (json.dumps(doc, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    lp = os.path.join(out_dir, 'POINTS_LIST.json')
    with open(lp, 'xb') as f:
        f.write(raw)
    return {'status': 'OK', 'points_list': {'path': lp, 'sha256': sha_bytes(raw)}, 'wave': wave, 'n_points': len(out),
            'n_next_wave_calls': len(misses), 'n_registered_skipped': registered,
            'points': [{k: p[k] for k in ('row', 'label', 'key', 'pending_spec_sha256')} for p in out]}


def ledger_append(M, config, records_ref):
    """c2v003 L1: the CP-1 list assembler's records -> the wrapper's Orchestrator.ledger_append (under the lock)."""
    O = M.O
    if not is_pin(records_ref) or not os.path.isabs(records_ref['path']):
        return {'status': 'REFUSED', 'reasons': ['LEDGER_RECORDS_PIN_REQUIRED: an absolute {path, sha256}']}
    doc = json.loads(O.read_pinned(records_ref, 'ledger records'))
    if not isinstance(doc, dict) or doc.get('schema') != RECORDS_SCHEMA or not isinstance(doc.get('records'), list):
        return {'status': 'REFUSED', 'reasons': ['LEDGER_RECORDS_SCHEMA: %s required' % RECORDS_SCHEMA]}
    items = []
    for r in doc['records']:
        if not isinstance(r, dict):
            return {'status': 'REFUSED', 'reasons': ['LEDGER_RECORDS_ITEM_NOT_AN_OBJECT']}
        items.append({k: r.get(k) for k in ('key', 'theta', 'record', 'wave', 'pending_spec_sha256')})
    ctx = M.Context(config)
    return M.Orchestrator(ctx).ledger_append(items, {'records': dict(records_ref), 'points_list': doc.get('points_list')})


def ledger_status(M, config):
    ctx = M.Context(config)
    head = ctx.ledger_head()
    entries = ctx.ledger_entries()
    led = ctx.cfg['tail_readiness'].get('certificate_ledger')
    p = Path(led['path']) if led else None
    return {'status': 'OK', 'ledger': led, 'head': head, 'gates_ok': ctx.gates_ok(), 'cache_id': ctx.cache_id,
            'file_sha256': sha_bytes(p.read_bytes()) if p is not None and p.is_file() else None,
            'entries': [{k: e.get(k) for k in ('seq', 'key', 'wave', 'planned_spec_sha256', 'entry_sha256')} for e in entries]}


def dispatch(M, argv):
    check_patch(M)
    cmds = ('reingest', 'reingest-invalid', 'points-manifest', 'ledger-append', 'ledger-status')
    if argv and argv[0] in cmds:
        ap = argparse.ArgumentParser(prog=ENTRY_NAME + ' ' + argv[0])
        ap.add_argument('command', choices=cmds)
        ap.add_argument('--config', required=True)
        if argv[0] in ('reingest', 'reingest-invalid'):
            ap.add_argument('--wave', type=int, required=True)
            ap.add_argument('--call-index', type=int, required=True)
            ap.add_argument('--acceptance-record', required=True)
            ap.add_argument('--acceptance-record-sha256', required=True)
        if argv[0] == 'reingest':
            ap.add_argument('--bundle', required=True)
            ap.add_argument('--bundle-sha256', required=True)
        if argv[0] == 'points-manifest':
            ap.add_argument('--out-dir', required=True)
        if argv[0] == 'ledger-append':
            ap.add_argument('--records', required=True)
            ap.add_argument('--records-sha256', required=True)
        a = ap.parse_args(argv)
        try:
            if a.command == 'reingest':
                out = reingest(M, a.config, a.wave, a.call_index, {'path': a.bundle, 'sha256': a.bundle_sha256},
                               {'path': a.acceptance_record, 'sha256': a.acceptance_record_sha256})
            elif a.command == 'reingest-invalid':
                out = reingest_invalid(M, a.config, a.wave, a.call_index,
                                       {'path': a.acceptance_record, 'sha256': a.acceptance_record_sha256})
            elif a.command == 'points-manifest':
                out = points_manifest(M, a.config, a.out_dir)
            elif a.command == 'ledger-append':
                out = ledger_append(M, a.config, {'path': a.records, 'sha256': a.records_sha256})
            else:
                out = ledger_status(M, a.config)
        except (M.Error, M.CertificateRefusal, OSError, ValueError, KeyError, TypeError) as exc:
            out = {'status': 'REFUSED', 'reasons': ['%s: %s' % (type(exc).__name__, exc)]}
        out = dict(out, launches_performed=0)
        print(json.dumps(out, indent=1, sort_keys=True, default=str))
        return REINGEST_EXIT.get(out.get('status'), 3)
    return M.O.main(argv)


def main(argv):
    return dispatch(load_wrapper(), argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
