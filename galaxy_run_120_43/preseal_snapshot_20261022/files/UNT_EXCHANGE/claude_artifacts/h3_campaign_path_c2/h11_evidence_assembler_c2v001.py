"""HEADLINE11 evidence assembler (Claude2 h3_campaign_path_c2, c2v001; V006 A192 item 4; design map section 6).

The deciding and capability evidence of the H3 gates is HEADLINE11 #0-#10 (A192 item 4; CP-1 rows 1-9, K L96-104):
  #0 TAIL_REANCHOR -> deciding run `reanchor`;  #1 WORKERS_8_CANDIDATE_ANCHOR -> deciding run `workers_8`;
  #2 HEADLINE_TRIAL and #3-#10 HEADLINE_CORNER_000..111 -> the 9 capability rows (the trial point and the 2^3 box corners of
  the core's probe_points; CORNER_xyz = common_scale_s x, gamma_over_Eref y, ell_F_m z, 0 = lower, 1 = upper).
Root writes one runs manifest (schema H3_HEADLINE11_RUNS_C2V001): runs = 11 objects {index, name, call_dir (absolute),
spec, receipt, result, acceptance_record}, each a {path, sha256} pin.

reuse-test  (DRY; the A192 item 4 deciding test)  The entry's own `status` under the CANDIDATE config (every H3 field set
            except deciding_test, capability_evidence and the anchor pins) lists gates.driver_capability.normalization
            [].spec_sha256 for the 9 probe points (core L313-340).  They are compared with the spec shas HEADLINE11
            #2-#10 ran with (sha256 of each run's spec bytes): REUSE_HEADLINE11 (exit 0) iff the 9 run shas are exactly the 9
            probe shas, one each (the core keys capability rows by spec sha; a run whose name maps to another probe point by
            the CORNER_xyz convention is listed in name_label_mismatches, for root, and does not change the verdict);
            RUN_9_CALLS_AT_THESE_SPEC_SHAS (exit 5) otherwise; UNDECIDED (exit 3) if a probe point does not normalize or the
            manifest is malformed.  Writes nothing unless --out (exclusive create).
assemble    From the 11 FINISHED receipts and their acceptance records, writes in a NEW --out-dir (exclusive mkdir):
            DECIDING_EVIDENCE_H11.json and CAPABILITY_EVIDENCE_H11.json in exactly the forms core check_deciding (L114-197)
            and capability_probe (L313-340) read; then it builds the candidate config plus those two pins and the anchor's
            {result, receipt, spec_sha256} (the reanchor row's pins, core L152-157) in memory and constructs the chain's
            own Context on it: the deciding_test and driver_capability gates must read ok (ASSEMBLY_RECORD_H11.json carries
            both).  Only then H3_DELTA_EVIDENCE_H11.json (the apply delta for those five fields) is written.
Every run, before anything is written: the pins hash from bytes; call_dir is absolute and the result is this call's
out/result.json (the handoff's layout, v004 L341-369; the receipt may live anywhere: it is checked by content); the receipt verifies with the pinned monitor for the spec sha and the config driver and
reads FINISHED / COMPLETED with this result (parent _receipt_ok); finish.json binds the result; the result is COMPLETED, valid,
of this spec and driver; the acceptance record is the adopted handoff's (acceptance_q2 v004, A158, schema
DDO154_TAIL_ACCEPTANCE_RECORD_C2V001) record of this call and result reading ACCEPTED or ACCEPTED_PASS_FLAGGED with
outputs_are_evidence, guard ok and no step-4 stop (A134 Q2: no value is used before acceptance; #0 is the anchor, whose LO
fail is the step-4 stop, A134 L528); #2-#10 ran at exactly the candidate config's 9 probe spec bytes, one each.  It reads no run output
except these pinned files, never launches, and changes no value: run_mode_admitted is set true only for a run that FINISHED,
COMPLETED and was ACCEPTED at exactly that spec.

usage: python3 -I -B h11_evidence_assembler_c2v001.py reuse-test --entry E --entry-sha256 H --config CAND --config-sha256 H
                                                     --runs RUNS.json --runs-sha256 H [--out OUT.json]
       python3 -I -B h11_evidence_assembler_c2v001.py assemble   --entry E --entry-sha256 H --config CAND --config-sha256 H
                                                     --runs RUNS.json --runs-sha256 H --out-dir NEW_DIR
exit: 0 ok / REUSE; 3 refused or UNDECIDED; 5 RUN_9_CALLS (reuse-test).
"""
import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import sys
from pathlib import Path

RUNS_SCHEMA = 'H3_HEADLINE11_RUNS_C2V001'
NAMES = ('TAIL_REANCHOR', 'WORKERS_8_CANDIDATE_ANCHOR', 'HEADLINE_TRIAL') + tuple(
    'HEADLINE_CORNER_%d%d%d' % (a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
HANDOFF = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
           'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}          # A158
ACCEPTANCE_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'
ACCEPTED = ('ACCEPTED', 'ACCEPTED_PASS_FLAGGED')
DECIDING_SCHEMA = 'DDO154_V010R5_DECIDING_CX2V006'                 # core L118
CAPABILITY_SCHEMA = 'DDO154_TAIL_BOX_RUN_CAPABILITY_CX2V006'       # core L322
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'


class Refused(Exception):
    pass


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and isinstance(x['sha256'], str)


def read_pinned(pin, label):
    if not is_pin(pin) or not os.path.isabs(pin['path']):
        raise Refused('%s: an absolute {path, sha256} pin is required' % label)
    raw = Path(pin['path']).read_bytes()
    if sha_bytes(raw) != pin['sha256']:
        raise Refused('%s: sha256 mismatch for %s' % (label, pin['path']))
    return raw


def load_chain(entry, entry_sha):
    raw = Path(entry).read_bytes()
    if sha_bytes(raw) != entry_sha:
        raise Refused('ENTRY_PIN_MISMATCH: %s' % entry)
    sp = importlib.util.spec_from_file_location('_h11_assembler_entry', entry)
    E = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = E
    exec(compile(raw, str(entry), 'exec'), E.__dict__)
    W = E.load_wrapper()
    E.check_patch(W)
    return E, W


def probe_labels(ctx):
    """HEADLINE11 name -> core probe_points label (core/parent L2041-2054)."""
    names = list(ctx.es['varying_names'])
    if len(names) != 3:
        raise Refused('PROBE_COORDINATES: three varying names required for the 2^3 HEADLINE corners, got %s' % names)
    out = {'HEADLINE_TRIAL': 'trial'}
    for n in NAMES[3:]:
        bits = n[-3:]
        out[n] = 'corner ' + ','.join('%s=%s' % (nm, 'hi' if b == '1' else 'lo') for nm, b in zip(names, bits))
    return out


def read_runs(runs_ref, specs_only=False):
    doc = json.loads(read_pinned(runs_ref, 'HEADLINE11 runs manifest'))
    if not isinstance(doc, dict) or doc.get('schema') != RUNS_SCHEMA or not isinstance(doc.get('runs'), list):
        raise Refused('RUNS_SCHEMA: %s with runs[] required' % RUNS_SCHEMA)
    runs = sorted(doc['runs'], key=lambda r: r.get('index') if isinstance(r, dict) and type(r.get('index')) is int else 99)
    if [r.get('index') for r in runs] != list(range(11)) or [r.get('name') for r in runs] != list(NAMES):
        raise Refused('RUNS_MUST_BE_HEADLINE11_0_TO_10: indices 0..10 named %s' % (NAMES,))
    for r in runs:
        keys = ('spec',) if specs_only else ('spec', 'receipt', 'result', 'acceptance_record')
        bad = [k for k in keys if not is_pin(r.get(k))]
        if bad:
            raise Refused('RUN_%d_PINS_REQUIRED: %s' % (r['index'], bad))
    return doc, runs


def status_normalization(E, W, cfg_path):
    """The entry's own `status` (read-only, no lock) under the candidate config -> {label: normalization row}."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = E.dispatch(W, ['status', '--config', cfg_path])
    out = json.loads(buf.getvalue())
    if rc != 0 or out.get('status') != 'OK':
        raise Refused('STATUS_REFUSED: rc %s %s' % (rc, out.get('reasons')))
    rows = ((out.get('gates') or {}).get('driver_capability') or {}).get('normalization')
    if not isinstance(rows, list):
        raise Refused('STATUS_HAS_NO_DRIVER_CAPABILITY_NORMALIZATION')
    return {x.get('point'): x for x in rows}, out


def probe_shas(norm, labels):
    """-> ({spec sha: probe label} of the normalizing probe points, [labels that do not normalize])."""
    by_sha, undecided = {}, []
    for lab in sorted(set(labels.values())):
        n = norm.get(lab) or {}
        if n.get('normalize_ok') is True and isinstance(n.get('spec_sha256'), str):
            by_sha[n['spec_sha256']] = lab
        else:
            undecided.append(lab)
    return by_sha, undecided


def reuse_test(E, W, cfg_path, runs_ref):
    _, runs = read_runs(runs_ref, specs_only=True)
    norm, st = status_normalization(E, W, cfg_path)
    ctx = W.Context(cfg_path)
    labels = probe_labels(ctx)
    by_sha, undecided = probe_shas(norm, labels)
    rows, differ, seen, mism = [], [], [], []
    for r in runs[2:]:
        ran = sha_bytes(read_pinned(r['spec'], 'run %d spec' % r['index']))
        lab = by_sha.get(ran)
        if lab is None:
            differ.append(r['name'])
        else:
            seen.append(lab)
            if lab != labels[r['name']]:
                mism.append({'name': r['name'], 'by_name': labels[r['name']], 'by_spec_sha': lab})
        rows.append({'index': r['index'], 'name': r['name'], 'probe_point_by_spec_sha': lab, 'probe_point_by_name': labels[r['name']],
                     'headline11_spec_sha256': ran, 'equal': lab is not None,
                     'status_spec_sha256_by_name': (norm.get(labels[r['name']]) or {}).get('spec_sha256')})
    if len(set(seen)) != len(seen):
        differ.append('DUPLICATE_PROBE_POINT')
    verdict = 'UNDECIDED' if undecided else ('RUN_9_CALLS_AT_THESE_SPEC_SHAS' if differ else 'REUSE_HEADLINE11')
    return {'schema': 'H3_HEADLINE11_REUSE_TEST_C2V001', 'verdict': verdict, 'rows': rows, 'differ': differ,
            'undecided': undecided, 'name_label_mismatches': mism, 'probe_spec_sha256': sorted(by_sha), 'config': {'path': os.path.abspath(cfg_path), 'sha256': sha_bytes(Path(cfg_path).read_bytes())},
            'runs_manifest': runs_ref, 'cache_id': st.get('cache_id'), 'gate_digest': st.get('gate_digest'),
            'rule': ('V006 A192 item 4: `status` under the candidate config lists gates.driver_capability.normalization'
                     '[].spec_sha256 (core L319, L337); equal to the shas HEADLINE11 #2-#10 ran with -> HEADLINE11 gives the '
                     '9 capability rows and #0/#1 the deciding rows; otherwise 9 calls at exactly these bytes')}


def run_problems(ctx, W, r):
    """Every check of one HEADLINE11 run, before anything is written.  [] when it holds."""
    O = W.O
    bad, label = [], 'HEADLINE11 #%d %s' % (r['index'], r['name'])
    try:
        spec_raw = read_pinned(r['spec'], label + ' spec')
        for k in ('receipt', 'result', 'acceptance_record'):
            read_pinned(r[k], label + ' ' + k)
        cd = r.get('call_dir')
        if not isinstance(cd, str) or not os.path.isabs(cd):
            return [label + ': call_dir must be absolute']
        here = Path(cd).resolve()
        if Path(r['result']['path']).resolve() != here / 'out' / 'result.json':
            bad.append(label + ': the result is not this call\'s out/result.json')
        spec_sha = sha_bytes(spec_raw)
        why = O._receipt_ok(ctx.M, r['receipt'], spec_sha, W.DRIVER_SHA, r['result'], label)
        if why:
            bad.append(label + ': ' + why)
        _, why = O.finish_binding(r['result']['path'], r['result']['sha256'])
        if why:
            bad.append(label + ': ' + why)
        res = json.loads(Path(r['result']['path']).read_bytes())
        if (res.get('call_spec_sha256') != spec_sha or res.get('driver_sha256') != W.DRIVER_SHA
                or res.get('status') != 'COMPLETED' or res.get('valid') is not True):
            bad.append(label + ': the result is not COMPLETED / valid at this spec and driver')
        acc = json.loads(Path(r['acceptance_record']['path']).read_bytes())
        guard_ok = (acc.get('guard') or {}).get('ok') if isinstance(acc.get('guard'), dict) else None
        if acc.get('schema') != ACCEPTANCE_SCHEMA or acc.get('handoff') != HANDOFF:
            bad.append(label + ': the acceptance record is not the adopted handoff\'s (A158)')
        if (acc.get('reading') not in ACCEPTED or acc.get('outputs_are_evidence') is not True or guard_ok is not True):
            bad.append(label + ': NOT_ACCEPTED: reading %r, outputs_are_evidence %r, guard ok %r'
                       % (acc.get('reading'), acc.get('outputs_are_evidence'), guard_ok))
        if acc.get('step4_stop_for_root_ruling') is not False:
            bad.append(label + ': STEP4_STOP_FOR_ROOT_RULING %r (A134 L528)' % (acc.get('step4_stop_for_root_ruling'),))
        if acc.get('call_dir') != str(here):
            bad.append(label + ': the acceptance record is of another call (%s)' % acc.get('call_dir'))
        if acc.get('result') != {'path': str((here / 'out' / 'result.json').resolve()), 'sha256': r['result']['sha256']}:
            bad.append(label + ': the acceptance record pins another result')
    except (Refused, OSError, ValueError, KeyError, TypeError, AttributeError, W.Error) as exc:
        bad.append('%s: %s: %s' % (label, type(exc).__name__, exc))
    return bad


def assemble(E, W, cfg_path, cfg_sha, runs_ref, out_dir, *, me=None):
    O = W.O
    raw = Path(cfg_path).read_bytes()
    if sha_bytes(raw) != cfg_sha:
        raise Refused('CONFIG_PIN_MISMATCH')
    if not os.path.isabs(out_dir) or not out_dir.startswith(ART + '/') or os.path.exists(out_dir):
        raise Refused('OUT_DIR: a new absolute directory under %s is required' % ART)
    _, runs = read_runs(runs_ref)
    ctx = W.Context(cfg_path)
    labels = probe_labels(ctx)
    norm, _ = status_normalization(E, W, cfg_path)
    by_sha, undecided = probe_shas(norm, labels)
    if undecided:
        raise Refused('CANDIDATE_PROBE_POINT_DOES_NOT_NORMALIZE: %s' % undecided)
    bad = []
    for r in runs:
        bad += run_problems(ctx, W, r)
    point = {}
    for r in runs[2:]:
        lab = by_sha.get(r['spec']['sha256'])
        if lab is None:
            bad.append('HEADLINE11 #%d %s: ran at spec %s, which is not one of the candidate config\'s 9 probe specs'
                       % (r['index'], r['name'], r['spec']['sha256'][:16]))
        point[r['index']] = lab
    if sorted(x for x in point.values() if x) != sorted(by_sha.values()):
        bad.append('HEADLINE11 #2-#10 do not cover the 9 probe points one each: %s' % sorted(str(x) for x in point.values()))
    if bad:
        raise Refused('HEADLINE11_RUNS_REFUSED: %s' % bad)
    rean, w8 = runs[0], runs[1]
    drows = [dict({'name': nm, 'spec': r['spec'], 'spec_sha256': r['spec']['sha256'], 'result': r['result'],
                   'receipt': r['receipt']}, headline11_index=r['index'], headline11_name=r['name'],
                  acceptance_record=r['acceptance_record']) for nm, r in (('reanchor', rean), ('workers_8', w8))]
    src = {'runs_manifest': runs_ref, 'config': {'path': os.path.abspath(cfg_path), 'sha256': cfg_sha},
           'assembler': me, 'rule': 'V006 A192 item 4: HEADLINE11 #0-#10, FINISHED and ACCEPTED (A134 Q2)'}
    dec = {'schema': DECIDING_SCHEMA, 'status': 'TESTED', 'ok': True, 'driver_sha256': W.DRIVER_SHA,
           'route_a_column_workers': 8, 'runs': drows, 'source': src}
    cap = {'schema': CAPABILITY_SCHEMA, 'status': 'TESTED', 'ok': True, 'driver_sha256': W.DRIVER_SHA,
           'base_spec_sha256': ctx.base_sha256, 'source': src,
           'rows': [{'spec_sha256': r['spec']['sha256'], 'run_mode_admitted': True, 'point': point[r['index']],
                     'run_mode_basis': 'FINISHED_COMPLETED_AND_ACCEPTED_AT_EXACTLY_THIS_SPEC (HEADLINE11)',
                     'headline11_index': r['index'], 'headline11_name': r['name'], 'receipt': r['receipt'],
                     'result': r['result'], 'acceptance_record': r['acceptance_record']} for r in runs[2:]]}
    os.mkdir(out_dir)

    def put(name, obj):
        b = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
        p = os.path.join(out_dir, name)
        with open(p, 'xb') as f:
            f.write(b)
        return {'path': p, 'sha256': sha_bytes(b)}
    dpin, cpin = put('DECIDING_EVIDENCE_H11.json', dec), put('CAPABILITY_EVIDENCE_H11.json', cap)
    sets = {'deciding_test': dpin, 'capability_evidence': cpin, 'anchor.result': rean['result'],
            'anchor.receipt': rean['receipt'], 'anchor.spec_sha256': rean['spec']['sha256']}
    cfg2 = json.loads(raw)
    cfg2['deciding_test'], cfg2['capability_evidence'] = dpin, cpin
    cfg2['anchor'] = dict(cfg2['anchor'], result=rean['result'], receipt=rean['receipt'], spec_sha256=rean['spec']['sha256'])
    try:
        c2 = W.Context(copy.deepcopy(cfg2))
        gates = {k: {'ok': bool(c2.gates[k].get('ok')), 'reasons': c2.gates[k].get('reasons')}
                 for k in ('deciding_test', 'driver_capability')}
    except (W.Error, OSError, ValueError, KeyError, TypeError) as exc:
        gates = {'context': {'ok': False, 'reasons': ['%s: %s' % (type(exc).__name__, exc)]}}
    ok = all(g['ok'] for g in gates.values())
    rec = {'schema': 'H3_HEADLINE11_ASSEMBLY_RECORD_C2V001', 'ok': ok, 'gate_check': gates, 'deciding_evidence': dpin,
           'capability_evidence': cpin, 'set': sets, 'source': src, 'utc': O.utc(),
           'note': 'the gate check is the chain\'s own Context on the candidate config plus these five fields, in memory'}
    rpin = put('ASSEMBLY_RECORD_H11.json', rec)
    out = {'status': 'OK' if ok else 'REFUSED', 'assembly_record': rpin, 'deciding_evidence': dpin,
           'capability_evidence': cpin, 'gate_check': gates}
    if ok:
        out['delta'] = put('H3_DELTA_EVIDENCE_H11.json', {'set': sets, 'append': {
            'notes': ' | H3 deciding + capability evidence = HEADLINE11 #0-#10 (V006 A192 item 4; h11_evidence_assembler_c2v001).'}})
    else:
        out['reasons'] = ['GATE_CHECK_FAILED: %s' % {k: g['reasons'] for k, g in gates.items() if not g['ok']}]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('reuse-test', 'assemble'):
        s = sub.add_parser(name)
        for k in ('--entry', '--entry-sha256', '--config', '--config-sha256', '--runs', '--runs-sha256'):
            s.add_argument(k, required=True)
        if name == 'assemble':
            s.add_argument('--out-dir', required=True)
        else:
            s.add_argument('--out')
    a = ap.parse_args(argv)
    me = {'path': os.path.realpath(__file__), 'sha256': sha_bytes(Path(os.path.realpath(__file__)).read_bytes())}
    try:
        E, W = load_chain(a.entry, a.entry_sha256)
        if sha_bytes(Path(a.config).read_bytes()) != a.config_sha256:
            raise Refused('CONFIG_PIN_MISMATCH')
        runs_ref = {'path': os.path.abspath(a.runs), 'sha256': a.runs_sha256}
        if a.cmd == 'reuse-test':
            out = reuse_test(E, W, a.config, runs_ref)
            out['assembler'] = me
            if a.out:
                with open(a.out, 'x') as f:
                    json.dump(out, f, indent=1, sort_keys=True)
                    f.write('\n')
            print(json.dumps(out, indent=1, sort_keys=True))
            return {'REUSE_HEADLINE11': 0, 'RUN_9_CALLS_AT_THESE_SPEC_SHAS': 5}.get(out['verdict'], 3)
        out = assemble(E, W, a.config, a.config_sha256, runs_ref, a.out_dir, me=me)
    except (Refused, OSError, ValueError, KeyError, TypeError) as exc:
        out = {'status': 'REFUSED', 'reasons': ['%s: %s' % (type(exc).__name__, exc)]}
    out = dict(out, launches_performed=0)
    print(json.dumps(out, indent=1, sort_keys=True, default=str))
    return 0 if out.get('status') == 'OK' else 3


if __name__ == '__main__':
    sys.exit(main())
