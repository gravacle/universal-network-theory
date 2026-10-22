"""Root-verify (Claude2) adversarial synthetic tests for values writer v004 (A159 / A205 item 9 / A211).

Independent of Codex2's suites: own fixtures, own expectations. Constants below are derived from the handoff c2v005
bytes (AST, L108/L112/L113-114) at run time, not copied from the writer. Synthetic calls only; no producer, solver,
real call, certificate, query manifest or NGC data is read. Every file is written by exclusive create inside --work.

Groups:
  R  right schema + right handoff sha, wrong route (near-miss strings, types)
  H  handoff pin near-misses (one hex off, case, relative path, predecessor NGC/DDO handoffs, shape)
  S  schema near-misses (DDO, predecessor C2V004, the handoff's own ROOT_SUMMARY schema, non-object)
  P  Phase 1 vs Phase 2 truth for LO_UNCERTIFIED_TRANSIENT / INCOMPLETE / ACCEPTED_PASS_FLAGGED / none
  B  binding and record form (full handoff-form record, early-refusal record, symlinked call dir, cross-point swap)
  O  observations (behaviour recorded, not a pass/fail claim)
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
HANDOFF_PATH = ART + '/ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py'
HANDOFF_SHA = '7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1'      # A211, root from bytes
HANDOFF_V004_SHA = '2721cfd1d27f6b05b831ba53b02a99125bd49033d235530b911453696bb8f29d'  # NGC predecessor (not adopted)
DDO_HANDOFF_SHA = '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'   # DDO acceptance_handoff_c2v004
N = 43


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def handoff_constants():
    raw = Path(HANDOFF_PATH).read_bytes()
    assert sha_b(raw) == HANDOFF_SHA, 'handoff bytes changed'
    want = {'RECORD_SCHEMA', 'SUMMARY_SCHEMA', 'ROUTE', 'READINGS', 'MEMBER_LO_OK'}
    out = {}
    for n in ast.parse(raw).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id in want:
            out[n.targets[0].id] = (n.lineno, ast.literal_eval(n.value))
    return out


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--module', required=True)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    work = Path(a.work).resolve()
    work.mkdir(parents=False, exist_ok=False)
    spec = importlib.util.spec_from_file_location('writer_under_rootverify', a.module)
    W = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(W)
    HC = handoff_constants()
    SCHEMA, ROUTE = HC['RECORD_SCHEMA'][1], HC['ROUTE'][1]
    tests, observations = [], []

    def check(name, ok, detail=None):
        tests.append({'name': name, 'ok': bool(ok), 'detail': detail})

    def observe(name, value):
        observations.append({'name': name, 'value': value})

    def put_bytes(p, raw):
        p = Path(p)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'xb') as f:
            f.write(raw)
        return {'path': str(p), 'sha256': sha_b(raw)}

    def put(p, obj):
        return put_bytes(p, canonical(obj) + b'\n')

    # ---- static: the writer's constants equal the handoff's bytes (derived here, not from Codex2's notes)
    check('C1 handoff L%d RECORD_SCHEMA == writer ACCEPTANCE_SCHEMAS and MEMBER_ACCEPTANCE_PRODUCERS schema'
          % HC['RECORD_SCHEMA'][0],
          HC['RECORD_SCHEMA'][0] == 108 and W.ACCEPTANCE_SCHEMAS == (SCHEMA,)
          and W.MEMBER_ACCEPTANCE_PRODUCERS == ((SCHEMA, HANDOFF_SHA),), [SCHEMA, W.MEMBER_ACCEPTANCE_PRODUCERS])
    check('C2 handoff L%d ROUTE == writer NGC_ACCEPTANCE_ROUTE' % HC['ROUTE'][0],
          HC['ROUTE'][0] == 112 and W.NGC_ACCEPTANCE_ROUTE == ROUTE, ROUTE)
    check('C3 handoff sha from bytes == writer ACCEPTANCE_HANDOFFS', W.ACCEPTANCE_HANDOFFS == (HANDOFF_SHA,))
    check('C4 handoff MEMBER_LO_OK == writer MEMBER_ACCEPTANCE_READINGS (O-1)',
          tuple(HC['MEMBER_LO_OK'][1]) == W.MEMBER_ACCEPTANCE_READINGS == ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT'))
    check('C5 every handoff READING is admitted by the writer whitelist (no NGC reading refuses as unknown)',
          set(HC['READINGS'][1]) <= set(W.ACCEPTANCE_READINGS), [HC['READINGS'][1], W.ACCEPTANCE_READINGS])

    # ---- synthetic calls
    qids = ['RV-Q%02d' % i for i in range(N)]
    rows = [{'id': q, 'valid': i not in (0, 7), 'speed_km_s': None if i in (0, 7) else 30.0 + i,
             'reason': 'RV_SYN_INVALID' if i in (0, 7) else None} for i, q in enumerate(qids)]
    w3 = [i not in (0, 7) for i in range(N)]
    calls = {}

    def make_call(tag, status='COMPLETED', valid=True):
        call = work / 'calls' / tag
        out = call / 'out'
        r = {'status': status, 'valid': valid, 'galaxy': 'NGC3198', 'driver_sha256': W.DRIVER_SHA256,
             'call_spec_sha256': 'c' * 64, 'rows': rows, 'speeds_km_s': {x['id']: x['speed_km_s'] for x in rows}}
        rp = put(out / 'result.json', r)
        put(out / 'finish.json', {'status': status, 'valid': valid, 'result_path': rp['path'],
                                  'result_sha256': rp['sha256']})
        calls[tag] = (call.resolve(), rp)
        return calls[tag]

    for t in ('uA', 'F0', 'F1'):
        make_call(t)
    make_call('inv', 'COMPLETED_INVALID', False)

    def base_record(tag, reading='ACCEPTED'):
        call, rp = calls[tag]
        return {'schema': SCHEMA, 'route': ROUTE, 'handoff': {'path': HANDOFF_PATH, 'sha256': HANDOFF_SHA},
                'call_dir': str(call), 'result': dict(rp), 'reading': reading}

    n_rec = [0]

    def rec_pin(obj):
        n_rec[0] += 1
        return put(work / 'records' / ('rec_%03d.json' % n_rec[0]), obj)

    def vp(tag, kind, acc, call_dir=None):
        call, _ = calls[tag]
        return W.values_point(kind=kind, role='u_A' if kind == 'phase1_values' else 'member', theta_key='d' * 64,
                              query_ids=qids, call_dir=str(call_dir or call), call_spec_sha256='c' * 64,
                              log_index=3 if kind == 'phase2_members' else None, acceptance=acc)[0]

    def refuse(name, code, pin, tag='uA'):
        for kind in ('phase1_values', 'phase2_members'):
            try:
                vp(tag, kind, pin)
                check(name + ' [' + kind + ']', False, 'no refusal (want %s)' % code)
            except W.Refused as exc:
                check(name + ' [' + kind + ']', exc.code == code, exc.code)
            except Exception as exc:     # noqa: BLE001
                check(name + ' [' + kind + ']', False, '%s: %s' % (type(exc).__name__, exc))

    # ---- R: right schema and handoff, wrong route
    for nm, route in (('R1 route with trailing space', ROUTE + ' '),
                      ('R2 route lower case', ROUTE.lower()),
                      ('R3 route without the NGC_ prefix', ROUTE[len('NGC_'):]),
                      ('R4 route as a superstring', 'X_' + ROUTE + '_V2'),
                      ('R5 route as a one-element list', [ROUTE]),
                      ('R6 route explicit null', None),
                      ('R7 route = the record schema string', SCHEMA)):
        refuse(nm, 'ACCEPTANCE_ROUTE', rec_pin(dict(base_record('uA'), route=route)))

    # ---- H: handoff pin near-misses
    flip = lambda s, i: s[:i] + ('0' if s[i] != '0' else '1') + s[i + 1:]
    for nm, h in (('H1 handoff sha one hex off (last nibble)', {'path': HANDOFF_PATH, 'sha256': flip(HANDOFF_SHA, 63)}),
                  ('H2 handoff sha one hex off (first nibble)', {'path': HANDOFF_PATH, 'sha256': flip(HANDOFF_SHA, 0)}),
                  ('H3 handoff sha one hex off (middle nibble)', {'path': HANDOFF_PATH, 'sha256': flip(HANDOFF_SHA, 31)}),
                  ('H4 handoff sha upper-case hex', {'path': HANDOFF_PATH, 'sha256': HANDOFF_SHA.upper()}),
                  ('H5 handoff sha truncated to 63 hex', {'path': HANDOFF_PATH, 'sha256': HANDOFF_SHA[:63]}),
                  ('H6 handoff path relative', {'path': 'ngc_acceptance_handoff_c2v005.py', 'sha256': HANDOFF_SHA}),
                  ('H7 handoff as bare sha string', HANDOFF_SHA),
                  ('H8 handoff pin with an extra key', {'path': HANDOFF_PATH, 'sha256': HANDOFF_SHA, 'reviewed': True}),
                  ('H9 NGC predecessor handoff c2v004 sha with the C2V005 schema', {'path': HANDOFF_PATH.replace('c2v005', 'c2v004'), 'sha256': HANDOFF_V004_SHA}),
                  ('H10 DDO handoff c2v004 sha with the NGC schema and route', {'path': '/x/acceptance_handoff_c2v004.py', 'sha256': DDO_HANDOFF_SHA})):
        refuse(nm, 'ACCEPTANCE_PRODUCER_NOT_REVIEWED', rec_pin(dict(base_record('uA'), handoff=h)))
    refuse('H11 handoff key absent', 'ACCEPTANCE_PRODUCER_NOT_REVIEWED',
           rec_pin({k: v for k, v in base_record('uA').items() if k != 'handoff'}))

    # ---- S: schema near-misses (DDO-schema records refused, A159 / B1)
    for nm, s in (('S1 DDO schema with NGC route and NGC handoff sha', 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'),
                  ('S2 NGC predecessor schema C2V004', 'UNT_NGC_LO_ACCEPTANCE_RECORD_C2V004'),
                  ('S3 the handoff ROOT_SUMMARY schema (blinded summary pinned by mistake)', HC['SUMMARY_SCHEMA'][1]),
                  ('S4 schema with trailing space', SCHEMA + ' ')):
        refuse(nm, 'ACCEPTANCE_SCHEMA', rec_pin(dict(base_record('uA'), schema=s)))
    refuse('S5 record is a JSON list', 'ACCEPTANCE_SCHEMA', rec_pin([base_record('uA')]))
    refuse('S6 DDO-form record (DDO schema and sha, no route)', 'ACCEPTANCE_SCHEMA',
           rec_pin({k: v for k, v in dict(base_record('uA'), schema='DDO154_TAIL_ACCEPTANCE_RECORD_C2V001',
                                          handoff={'path': '/x/acceptance_handoff_c2v004.py', 'sha256': DDO_HANDOFF_SHA}
                                          ).items() if k != 'route'}))
    refuse('S7 reading lower case "accepted"', 'ACCEPTANCE_READING_UNKNOWN', rec_pin(base_record('uA', 'accepted')))
    refuse('S8 reading "PASS" (adapter call_lo_reading form, not a handoff READING)', 'ACCEPTANCE_READING_UNKNOWN',
           rec_pin(base_record('uA', 'PASS')))

    # ---- P: Phase 1 vs Phase 2 for the edge readings, same COMPLETED valid call
    def truth(reading):
        pin = rec_pin(base_record('uA', reading)) if reading else None
        return vp('uA', 'phase1_values', pin), vp('uA', 'phase2_members', pin)
    p1, p2 = truth('LO_UNCERTIFIED_TRANSIENT')
    check('P1 LO_UNCERTIFIED_TRANSIENT Phase 1: valid == W-3 row validity (gate passes); acceptance printed, counts true',
          p1['valid'] == w3 and p1['acceptance']['counts_for_member_valid'] is True and 'member_valid' not in p1)
    check('P2 LO_UNCERTIFIED_TRANSIENT Phase 2: valid == W-3; member_valid true; basis empty',
          p2['valid'] == w3 and p2['member_valid'] is True and p2['member_valid_basis'] == [])
    check('P3 LO_UNCERTIFIED_TRANSIENT: Phase-1 and Phase-2 valid vectors identical', p1['valid'] == p2['valid'])
    p1, p2 = truth('INCOMPLETE')
    check('P4 INCOMPLETE Phase 1: every row invalid (O-2)', p1['valid'] == [False] * N)
    check('P5 INCOMPLETE Phase 2: rows keep W-3; member_valid false; exact basis',
          p2['valid'] == w3 and p2['member_valid'] is False
          and p2['member_valid_basis'] == ['ACCEPTANCE_READING_NOT_ACCEPTED_OR_TRANSIENT: INCOMPLETE'])
    p1, p2 = truth('ACCEPTED_PASS_FLAGGED')
    check('P6 ACCEPTED_PASS_FLAGGED Phase 1: every row invalid (O-1)', p1['valid'] == [False] * N)
    check('P7 ACCEPTED_PASS_FLAGGED Phase 2: member_valid false (O-1)', p2['member_valid'] is False)
    p1, p2 = truth('NON_LAPSE_TAIL_MATERIAL')
    check('P8 NON_LAPSE_TAIL_MATERIAL: Phase 1 all invalid, Phase 2 member_valid false',
          p1['valid'] == [False] * N and p2['member_valid'] is False)
    p1, p2 = truth(None)
    check('P9 no acceptance record: Phase 1 all invalid (UNTESTED, not refused); Phase 2 basis NO_ACCEPTANCE_RECORD',
          p1['valid'] == [False] * N and p1['acceptance'] is None and p2['member_valid'] is False
          and p2['member_valid_basis'] == ['NO_ACCEPTANCE_RECORD'] and p2['valid'] == w3)
    p1, p2 = truth('ACCEPTED')
    check('P10 ACCEPTED: Phase 1 valid == W-3, Phase 2 member_valid true',
          p1['valid'] == w3 and p2['valid'] == w3 and p2['member_valid'] is True)
    pin_inv = rec_pin(base_record('inv', 'LO_UNCERTIFIED_TRANSIENT'))
    pi1, pi2 = vp('inv', 'phase1_values', pin_inv), vp('inv', 'phase2_members', pin_inv)
    check('P11 LO_UNCERTIFIED_TRANSIENT on a COMPLETED_INVALID call: Phase 1 all invalid, member_valid false',
          pi1['valid'] == [False] * N and pi2['member_valid'] is False
          and pi2['member_valid_basis'] == ['CALL_NOT_VALID', 'STATUS_NOT_COMPLETED: COMPLETED_INVALID'])

    # ---- B: binding and the handoff's own record form
    call, rp = calls['F0']
    full = {'schema': SCHEMA, 'route': ROUTE, 'call_dir': str(call), 'reading': 'ACCEPTED', 'blockers': [],
            'states': [], 'registry_kind': 'REGISTERED', 'is_anchor': False, 'scope_disclosure': 'syn',
            'pass_meaning': 'syn', 'handoff': {'path': HANDOFF_PATH, 'sha256': HANDOFF_SHA}, 'execution': None,
            'srb_rot_report': {'label': 'syn', 'gates': False, 'status': 'NOT_RUN', 'code': None, 'report': None},
            'pins': {}, 'high_qinf_ngc_lo_flagged': None, 's2': 'PINNED', 'result': dict(rp),
            'all_readings': [], 'member_lo_ok': True, 'rows_are_model_output': None,
            'root_summary': {'path': str(work / 'x' / 'ROOT_SUMMARY.json'), 'sha256': 'a' * 64}, 'files': []}
    fp = rec_pin(full)
    b1a, b1b = vp('F0', 'phase1_values', fp), vp('F0', 'phase2_members', fp)
    check('B1 full handoff-form record (L577-586 keys + result, canonical JSON), ACCEPTED: admitted in both phases',
          b1a['valid'] == w3 and b1b['member_valid'] is True and b1a['acceptance']['handoff']['sha256'] == HANDOFF_SHA)
    early = {k: v for k, v in full.items() if k not in ('result', 'all_readings', 's2')}
    early.update(reading='INCOMPLETE', member_lo_ok=False, blockers=['FINISHED_RECEIPT_REQUIRED'])
    refuse('B2 handoff early-refusal record (no result key, INCOMPLETE): refused as not-of-this-call',
           'ACCEPTANCE_NOT_OF_THIS_CALL', rec_pin(early), tag='F0')
    refuse('B3 cross-point swap: F0 record supplied for the F1 call', 'ACCEPTANCE_NOT_OF_THIS_CALL',
           rec_pin(base_record('F0')), tag='F1')
    link = work / 'calls' / 'F1_link'
    os.symlink(calls['F1'][0], link)
    good = rec_pin(base_record('F1'))
    lp = vp('F1', 'phase1_values', good, call_dir=link)
    check('B4 writer given a symlinked call dir binds the realpath record (handoff writes realpath)', lp['valid'] == w3)
    linked = dict(base_record('F1'), call_dir=str(link))
    try:
        vp('F1', 'phase1_values', rec_pin(linked), call_dir=link)
        check('B5 record carrying the unresolved symlink call_dir: refused', False, 'no refusal')
    except W.Refused as exc:
        check('B5 record carrying the unresolved symlink call_dir: refused', exc.code == 'ACCEPTANCE_NOT_OF_THIS_CALL',
              exc.code)
    other_path = dict(base_record('F1'), result={'path': str(calls['F1'][0] / 'out' / '..' / 'out' / 'result.json'),
                                                  'sha256': calls['F1'][1]['sha256']})
    refuse('B6 result pin with right sha but unnormalised path', 'ACCEPTANCE_NOT_OF_THIS_CALL', rec_pin(other_path),
           tag='F1')
    refuse('B7 result pin of the right path with another sha', 'ACCEPTANCE_NOT_OF_THIS_CALL',
           rec_pin(dict(base_record('F1'), result=dict(calls['F1'][1], sha256=flip(calls['F1'][1]['sha256'], 5)))),
           tag='F1')
    gp = rec_pin(base_record('F1'))
    refuse('B8 acceptance pin one hex off (record bytes unchanged)', 'PIN_SHA_MISMATCH',
           dict(gp, sha256=flip(gp['sha256'], 63)), tag='F1')
    refuse('B9 acceptance pin with a relative path', 'PIN_INVALID',
           {'path': os.path.relpath(gp['path']), 'sha256': gp['sha256']}, tag='F1')
    raw = Path(gp['path']).read_bytes()
    edited = put_bytes(work / 'records' / 'edited_after_pin.json', raw.replace(b'"ACCEPTED"', b'"ACCEPTED" '))
    refuse('B10 record bytes edited after pinning (pin of the original)', 'PIN_SHA_MISMATCH',
           {'path': edited['path'], 'sha256': gp['sha256']}, tag='F1')

    # ---- O: observations (recorded, not pass/fail)
    o1 = vp('F0', 'phase2_members', rec_pin(dict(base_record('F0', 'INCOMPLETE'), member_lo_ok=True)))
    observe('O1 reading INCOMPLETE with member_lo_ok true: writer derives from reading only',
            {'member_valid': o1['member_valid']})
    o2 = vp('F0', 'phase2_members', rec_pin(dict(base_record('F0', 'ACCEPTED'), member_lo_ok=False,
                                                  blockers=['SYN_BLOCKER'])))
    observe('O2 reading ACCEPTED with member_lo_ok false and a blocker: writer does not cross-check either field',
            {'member_valid': o2['member_valid']})
    o3 = vp('F0', 'phase2_members', rec_pin(dict(base_record('F0'), handoff={'path': '/nonexistent/h.py',
                                                                             'sha256': HANDOFF_SHA})))
    observe('O3 handoff pin path not the handoff file (sha right): writer checks the sha only, path not read',
            {'member_valid': o3['member_valid']})
    o4 = vp('F0', 'phase2_members', rec_pin(dict(base_record('F0'), reading='BOUND_INSUFFICIENT')))
    observe('O4 DDO-only reading BOUND_INSUFFICIENT on an NGC record: admitted by the whitelist, counts false',
            {'member_valid': o4['member_valid'], 'reading': o4['acceptance']['reading']})

    d = {'schema': 'C2_ROOTVERIFY_VALUES_WRITER_V004_ADVERSARIAL_V001',
         'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(), 'label': 'TESTED',
         'module': {'path': str(Path(a.module).resolve()), 'sha256': sha_b(Path(a.module).read_bytes())},
         'script': {'path': str(Path(__file__).resolve()), 'sha256': sha_b(Path(__file__).read_bytes())},
         'handoff_constants_from_bytes': {k: {'line': v[0], 'value': v[1]} for k, v in HC.items()},
         'n': len(tests), 'passed': sum(t['ok'] for t in tests), 'tests': tests, 'observations': observations,
         'synthetic_only': True, 'flags': {'isolated': sys.flags.isolated,
                                           'dont_write_bytecode': sys.flags.dont_write_bytecode}}
    put(work / 'RESULT_ADVERSARIAL_C2.json', d)
    print(json.dumps({'n': d['n'], 'passed': d['passed'], 'failures': [t for t in tests if not t['ok']],
                      'observations': observations}))
    return 0 if d['n'] == d['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
