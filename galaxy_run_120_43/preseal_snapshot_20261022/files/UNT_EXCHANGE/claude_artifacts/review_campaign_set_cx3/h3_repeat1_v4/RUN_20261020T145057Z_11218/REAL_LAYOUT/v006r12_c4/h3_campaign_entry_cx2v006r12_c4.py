"""H3 campaign entry (Claude2 h3_campaign_path_c2, c2v002; V006 A191 B2): successor of h3_campaign_entry_c2v001 (08068e93).

What it is.  The launch entry of the DDO154 calibration campaign on the q5b1-line wrapper (V006 A139: the wrapper with the
A134 Q5 per-state LO slot rule).  It loads the wrapper from its bytes after a sha256 check; the wrapper pins its core, the
core pins the adoption policy and the parent c75a889f, and the wrapper/core replace the parent's module globals Context,
Orchestrator, Mapper, Cache, CampaignExecutor, check_deciding, check_numerics and resolve.  `plan`, `status`, `run` and
`resolve` are then the parent's own main(argv) over that patched module: no argument is added, removed or reinterpreted,
so the parent's refusal semantics and exit codes (EXIT, parent L204-206) are unchanged.

Changes against w1_campaign_entry_v001 (6a6957f2), as in c2v001:
  1. WRAPPER / WRAPPER_SHA pin the q5b1-line wrapper.  The generator make_campaign_cascade_c2v002 rewrites exactly these two
     lines when it re-pins the chain (this template pins the published q5b1 wrapper 7a6af535; the generator's regression
     reproduces this file byte for byte).  ENTRY_NAME names this successor.
  2. main(argv) = dispatch(load_wrapper(), argv); check_patch() is v001's pin/patch check, factored out unchanged.
  3. Command `reingest` (A188 gap 3): the wrapper's own Orchestrator.reingest(wave, call_index, bundle_ref)
     (q5b1 L335-358: lock, prepare(create=False), SF1 identity, cache id, call index, spec, write_acceptance, classify,
     cache put; no solver call).  Output: one JSON object; exit 0 OK, 3 REFUSED, 8 LOCKED.
Change against c2v001 (V006 A191 B2), and nothing else:
  4. `reingest` also takes --acceptance-record PATH --acceptance-record-sha256 H.  Every refusal below happens before the
     wrapper is called:
       - --bundle and --acceptance-record are absolute paths, each pinned {path, sha256};
       - every gate of this config passes (Context.gates_ok); the wave's WAVE_PLAN exists, was planned under this
         config_sha256 and gate_digest (parent L3320) and holds call_index I; the bundle's bytes verify;
       - the record's bytes hash to its sha and it is the adopted handoff's record (acceptance_q2 v004, A158):
         schema DDO154_TAIL_ACCEPTANCE_RECORD_C2V001 (v004 L50), handoff = {v004 path, 5ff464cc}, reading ACCEPTED or
         ACCEPTED_PASS_FLAGGED, outputs_are_evidence true, guard.ok true, step4_stop_for_root_ruling false (v004 L344-359);
       - the same call: record.call_dir = this call dir, resolved (v004 L341, L344);
       - the same receipt: v004 records the result pin, not the receipt pin (it checks policy.receipt against the result,
         receipt_ok L253-257, L370).  So this call's RECEIPT.json must verify with the pinned monitor for the planned spec
         and the config driver, read FINISHED / COMPLETED, and pin the result that record.result pins (path resolved,
         sha256 equal to the result bytes now);
       - the same bundle: record.bundle = {--bundle, --bundle-sha256} exactly.
     Reasons: REINGEST_ABSOLUTE_PATHS_REQUIRED, REINGEST_ACCEPTANCE_RECORD_REQUIRED, REINGEST_ACCEPTANCE_RECORD_SCHEMA,
     REINGEST_ACCEPTANCE_HANDOFF_NOT_A158, REINGEST_ACCEPTANCE_NOT_ACCEPTED, REINGEST_ACCEPTANCE_RECORD_OTHER_CALL,
     REINGEST_RECEIPT_NOT_FINISHED, REINGEST_ACCEPTANCE_RECORD_OTHER_RECEIPT, REINGEST_ACCEPTANCE_BUNDLE_DIFFERS.

usage:
  python3 -I -B h3_campaign_entry_<SUB>.py plan     --config CFG
  python3 -I -B h3_campaign_entry_<SUB>.py status   --config CFG
  python3 -I -B h3_campaign_entry_<SUB>.py run      --config CFG [--new-campaign] [--max-waves N]
  python3 -I -B h3_campaign_entry_<SUB>.py resolve  --config CFG --wave W (--token T ... | --all --halt-sha256 H)
                                                    --decision retry|retry_with_recovery [--recovery P] --reason TEXT
  python3 -I -B h3_campaign_entry_<SUB>.py reingest --config CFG --wave W --call-index I --bundle /ABS/B --bundle-sha256 H
                                                    --acceptance-record /ABS/ACCEPTANCE_RECORD.json --acceptance-record-sha256 H
`run` must be started through launch_setsid_c2v005.py (C4-4: a non-synthetic run refuses unless it is the session leader).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

WRAPPER = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/h3_repeat1_v4/RUN_20261020T145057Z_11218/REAL_LAYOUT/v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py')
WRAPPER_SHA = '7ac0785126d8b188b9d06c072e0583a03a182f3643910d1a2e5e24b9f61e3f06'
PARENT_SHA = 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'
ENTRY_NAME = 'h3_campaign_entry_c2v002'
REINGEST_EXIT = {'OK': 0, 'REFUSED': 3, 'LOCKED': 8}
HANDOFF = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
           'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}          # A158
ACCEPTANCE_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'                                          # handoff v004 L50
ACCEPTED = ('ACCEPTED', 'ACCEPTED_PASS_FLAGGED')


def load_wrapper():
    raw = WRAPPER.read_bytes()
    if hashlib.sha256(raw).hexdigest() != WRAPPER_SHA:
        raise SystemExit('PIN_MISMATCH wrapper %s' % WRAPPER)
    sp = importlib.util.spec_from_file_location('_cx2q5b1_h3_entry', WRAPPER)
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    exec(compile(raw, str(WRAPPER), 'exec'), m.__dict__)
    return m


def check_patch(M):
    O = M.O
    if hashlib.sha256(Path(O.__file__).read_bytes()).hexdigest() != PARENT_SHA:
        raise SystemExit('PIN_MISMATCH parent %s' % O.__file__)
    if O.Context is not M.Context or O.Orchestrator is not M.Orchestrator:
        raise SystemExit('wrapper patch not installed on the parent module')
    return O


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and isinstance(x['sha256'], str)


def acceptance_problems(M, ctx, call, call_dir, bundle_ref, acceptance_ref):
    """[] iff the record is the adopted handoff's ACCEPTED record for this call, receipt and bundle (A191 B2)."""
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


def reingest(M, config, wave, call_index, bundle_ref, acceptance_ref=None):
    """Entry guards, then the wrapper's own reingest.  Returns the wrapper's dict or a REFUSED dict."""
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
    wd = ctx.work_dir / 'waves' / ('wave_%04d' % int(wave))
    pp = wd / 'WAVE_PLAN.json'
    if not pp.is_file():
        return {'status': 'REFUSED', 'reasons': ['REINGEST_NO_WAVE_PLAN: %s' % pp]}
    plan = O.load_json_file(pp, 'wave plan')
    if plan.get('config_sha256') != ctx.config_sha256 or plan.get('gate_digest') != ctx.gate_digest:
        return {'status': 'REFUSED', 'reasons': ['REINGEST_PLAN_CONFIG_OR_GATES_DIFFER: wave %s was planned under config %s '
                                                 'gates %s; this config gives %s / %s'
                                                 % (wave, str(plan.get('config_sha256'))[:16],
                                                    str(plan.get('gate_digest'))[:16], ctx.config_sha256[:16],
                                                    ctx.gate_digest[:16])]}
    calls = [c for c in plan.get('calls') or [] if c.get('call_index') == int(call_index)]
    if len(calls) != 1:
        return {'status': 'REFUSED', 'reasons': ['REINGEST_CALL_INDEX_NOT_IN_PLAN: %s' % call_index]}
    O.read_pinned(bundle_ref, 'post-state certificate bundle')
    bad = acceptance_problems(M, ctx, calls[0], wd / 'campaign' / ('call_%04d' % int(call_index)), bundle_ref, acceptance_ref)
    if bad:
        return {'status': 'REFUSED', 'reasons': bad}
    return M.Orchestrator(ctx).reingest(int(wave), int(call_index), bundle_ref)


def dispatch(M, argv):
    check_patch(M)
    if argv and argv[0] == 'reingest':
        ap = argparse.ArgumentParser(prog=ENTRY_NAME + ' reingest')
        ap.add_argument('command', choices=('reingest',))
        ap.add_argument('--config', required=True)
        ap.add_argument('--wave', type=int, required=True)
        ap.add_argument('--call-index', type=int, required=True)
        ap.add_argument('--bundle', required=True)
        ap.add_argument('--bundle-sha256', required=True)
        ap.add_argument('--acceptance-record', required=True)
        ap.add_argument('--acceptance-record-sha256', required=True)
        a = ap.parse_args(argv)
        try:
            out = reingest(M, a.config, a.wave, a.call_index, {'path': a.bundle, 'sha256': a.bundle_sha256},
                           {'path': a.acceptance_record, 'sha256': a.acceptance_record_sha256})
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
