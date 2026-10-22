"""Regenerate the campaign adoption cascade at the step-3 verdict (Claude2 h3_campaign_path_c2, c2v003; V006 A126/A129/A188/A192).

c2v003 (V006 A192 items 2-3) against regenerate_h3_c2v002 (0fc614f5), and nothing else: it pins the generator
make_campaign_cascade_c2v003 (wrapper source calibration_orchestrator_q5b1_ledger_c2v003: the R-C8 ledger and the certified
MODEL_INVALID path; entry template h3_campaign_entry_c2v003); the regenerate record schema is H3_REGENERATE_RECORD_C2V003.
The seal tuple record (schema H3_V007_SEAL_TUPLE_RECORD_C2V001), every refusal rule and the expected diff sizes against the
no-tuple build (policy 2, core 1, wrapper 1, entry 1) are c2v002's.  Text below is c2v002's with the c2v003 names.

c2v002 (V006 A191 B2) against regenerate_h3_c2v001 (1706da77), and nothing else: it pins the generator
make_campaign_cascade_c2v002 (entry template h3_campaign_entry_c2v002, whose reingest takes the acceptance record); the
regenerate record schema is H3_REGENERATE_RECORD_C2V002.  The seal tuple record (schema H3_V007_SEAL_TUPLE_RECORD_C2V001)
and every refusal rule are c2v001's.  Text below is c2v001's with the c2v002 names.

Root fills ONE record, the seal tuple record (template SEAL_TUPLE_RECORD_H3_C2V001_PLACEHOLDER.json), and runs this script.
It refuses, before anything is written, unless the tuple IS the sealed compare's report bytes:
  * the record is ROOT_FILLED (the placeholder status, or any empty field, refuses: EMPTY_TUPLE);
  * V = sha256(report file bytes) = record.report.sha256 (else TUPLE_NOT_REPORT_BYTES);
  * the report's own fields equal the tuple: schema = SCHEMA, script_sha256 = C, prereg.sha256 = P,
    pins_verified.V005_addendum = A (else TUPLE_NOT_REPORT_BYTES);
  * the report reads the sealed ADOPT_TAIL reading: decision.outcome ADOPT_TAIL, decision.tests_read true, test_mode false
    (else REPORT_NOT_SEALED_ADOPT_TAIL; the policy refuses any other report anyway, policy L84-85: this only stops a
    non-adopting tuple from being registered);
  * record.compare is the generator's SEALED_COMPARE path with sha C (else COMPARE_PIN_MISMATCH);
  * then the pinned generator make_campaign_cascade_c2v003 cross-checks C, P, A and SCHEMA against the sealed compare,
    prereg and addendum bytes (generator check_tuple) and builds the cascade with the tuple.
It writes <out>/<SUB>/ (policy, core, q5b1 wrapper, entry; exclusive mkdir) and <out>/REGENERATE_RECORD_<SUB>.json, and
verifies from the written bytes: the policy registers exactly this tuple, the core pins that policy, the wrapper pins that
core, the entry pins that wrapper at its publish path.  The record lists the line diff of every output against the same
SUB built without a tuple (expected: policy 2 lines (P5, P6), core 1, wrapper 1, entry 1) and the publish commands.
Nothing is published: root copies with cp -n (A126/A139 practice) after Codex1 / Claude4 review the four small diffs.

`fill` writes that one record from bytes, so root types no hash: C = sha256(sealed compare), P / A / SCHEMA = the compare's
own V007_PREREG_SHA256 / PIN_ADDENDUM_V005 / SCHEMA_REPORT (read as the generator reads them), V = sha256(report bytes).
It applies every refusal rule above before it writes (exclusive create); `build` re-checks the record from bytes.

usage: python3 -I -B regenerate_h3_c2v003.py fill  --report REPORT.json --filled-by TEXT --ruling TEXT --out NEW_RECORD.json
                                                   [--sub v006r12_c4] [--publish-root DIR]
       python3 -I -B regenerate_h3_c2v003.py build --seal-record SEAL.json --seal-record-sha256 H --out-dir OUT [--dry-run]
exit: 0 written (or dry-run passed), 2 refused.
"""
import argparse
import ast
import difflib
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATOR = (HERE / 'make_campaign_cascade_c2v003.py', 'd7e6d77a8894687cd249a97daaef3c1286782586693af9d01774385e8a32e37a')
RECORD_SCHEMA = 'H3_V007_SEAL_TUPLE_RECORD_C2V001'
PLACEHOLDER_STATUS = 'PLACEHOLDER_EMPTY_UNTIL_THE_V007_VERDICT'
FILLED_STATUS = 'ROOT_FILLED'
TUPLE_KEYS = ('compare_sha256', 'prereg_sha256', 'addendum_sha256', 'report_schema', 'verdict_sha256')
HEX = re.compile(r'[0-9a-f]{64}')


class Refused(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_generator():
    p, s = GENERATOR
    raw = p.read_bytes()
    if sha(raw) != s:
        raise Refused('GENERATOR_PIN_MISMATCH: %s is not %s' % (p, s))
    spec = importlib.util.spec_from_file_location('_h3_cascade_generator', p)
    g = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(p), 'exec'), g.__dict__)
    return g


def read_record(path, want_sha):
    raw = Path(path).read_bytes()
    if sha(raw) != want_sha:
        raise Refused('SEAL_RECORD_PIN_MISMATCH: %s hashes to %s' % (path, sha(raw)))
    rec = json.loads(raw)
    if not isinstance(rec, dict) or rec.get('schema') != RECORD_SCHEMA:
        raise Refused('SEAL_RECORD_SCHEMA: must be %s' % RECORD_SCHEMA)
    return rec


def check_record(rec, G):
    """-> (tuple, report dict).  Every refusal names its rule."""
    if rec.get('status') != FILLED_STATUS:
        raise Refused('EMPTY_TUPLE: record status %r (root fills the record at the verdict; status %s)'
                      % (rec.get('status'), FILLED_STATUS))
    t = rec.get('tuple') or {}
    missing = [k for k in TUPLE_KEYS if not isinstance(t.get(k), str) or not t.get(k)]
    if missing:
        raise Refused('EMPTY_TUPLE: missing %s' % missing)
    for k in ('compare_sha256', 'prereg_sha256', 'addendum_sha256', 'verdict_sha256'):
        if HEX.fullmatch(t[k]) is None:
            raise Refused('EMPTY_TUPLE: %s is not 64 lowercase hex' % k)
    tup = tuple(t[k] for k in TUPLE_KEYS)
    rp = rec.get('report') or {}
    if not isinstance(rp.get('path'), str) or not os.path.isabs(rp['path']):
        raise Refused('TUPLE_NOT_REPORT_BYTES: record.report.path must be absolute')
    raw = Path(rp['path']).read_bytes()
    if sha(raw) != t['verdict_sha256'] or rp.get('sha256') != t['verdict_sha256']:
        raise Refused('TUPLE_NOT_REPORT_BYTES: sha256(report bytes) %s, tuple V %s, record.report.sha256 %s'
                      % (sha(raw), t['verdict_sha256'], rp.get('sha256')))
    rep = json.loads(raw)
    bad = []
    if rep.get('schema') != t['report_schema']:
        bad.append('schema %r != SCHEMA %r' % (rep.get('schema'), t['report_schema']))
    if rep.get('script_sha256') != t['compare_sha256']:
        bad.append('script_sha256 != C')
    if not isinstance(rep.get('prereg'), dict) or rep['prereg'].get('sha256') != t['prereg_sha256']:
        bad.append('prereg.sha256 != P')
    if (rep.get('pins_verified') or {}).get('V005_addendum') != t['addendum_sha256']:
        bad.append('pins_verified.V005_addendum != A')
    if bad:
        raise Refused('TUPLE_NOT_REPORT_BYTES: %s' % bad)
    dec = rep.get('decision') or {}
    if dec.get('outcome') != 'ADOPT_TAIL' or dec.get('tests_read') is not True or rep.get('test_mode') is not False:
        raise Refused('REPORT_NOT_SEALED_ADOPT_TAIL: decision %r, tests_read %r, test_mode %r'
                      % (dec.get('outcome'), dec.get('tests_read'), rep.get('test_mode')))
    cp = rec.get('compare') or {}
    if cp.get('path') != G.SEALED_COMPARE or cp.get('sha256') != t['compare_sha256']:
        raise Refused('COMPARE_PIN_MISMATCH: record.compare must be {%s, C}' % G.SEALED_COMPARE)
    if sha(Path(cp['path']).read_bytes()) != t['compare_sha256']:
        raise Refused('COMPARE_PIN_MISMATCH: the compare bytes do not hash to C')
    return tup, rep


def line_diff(a, b):
    out = []
    for ln in difflib.unified_diff(a.decode('utf-8').splitlines(), b.decode('utf-8').splitlines(), lineterm='', n=0):
        if (ln.startswith('-') or ln.startswith('+')) and not ln.startswith('---') and not ln.startswith('+++'):
            out.append(ln)
    return out


def verify_chain(files, sub, tup, publish_root, G):
    """From the bytes: policy registers exactly tup; core pins the policy; wrapper pins the core; entry pins the wrapper."""
    pol_n, core_n, wrap_n, entry_n = G.names(sub)
    by = dict(files)
    sh = {k: sha(v) for k, v in by.items()}
    seals = None
    for node in ast.parse(by[pol_n]).body:
        if isinstance(node, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'APPROVED_V007_SEALS' for x in node.targets):
            v = node.value
            if isinstance(v, ast.Call) and getattr(v.func, 'id', None) == 'frozenset':
                seals = frozenset(ast.literal_eval(v.args[0])) if v.args else frozenset()
    core, wrap, entry = by[core_n].decode(), by[wrap_n].decode(), by[entry_n].decode()
    checks = {
        'policy_registers_exactly_the_tuple': seals == frozenset({tup}),
        'core_pins_policy': ("parent.parent/'%s/%s'" % (sub, pol_n)) in core and ("!= '%s'" % sh[pol_n]) in core,
        'wrapper_pins_core': ("M=load(HERE/'%s','_cx2v006r1',expected='%s')" % (core_n, sh[core_n])) in wrap,
        'entry_pins_wrapper': ("WRAPPER = Path('%s')" % os.path.join(publish_root, sub, wrap_n)) in entry
                              and ("WRAPPER_SHA = '%s'" % sh[wrap_n]) in entry}
    if not all(checks.values()):
        raise Refused('CHAIN_NOT_REPINNED: %s' % checks)
    return checks


def run(seal_record, seal_record_sha256, out_dir, dry_run=False, G=None):
    G = G or load_generator()
    rec = read_record(seal_record, seal_record_sha256)
    tup, rep = check_record(rec, G)
    sub = rec.get('sub')
    publish_root = rec.get('publish_root') or G.CX2
    try:
        files, outputs, lit = G.build(sub, seal_tuple=tup, publish_root=publish_root)
        base, base_out, _ = G.build(sub, seal_tuple=None, publish_root=publish_root)
    except SystemExit as exc:
        raise Refused('GENERATOR_REFUSED (sealed bytes cross-check, generator check_tuple): exit %s' % exc.code)
    checks = verify_chain(files, sub, tup, publish_root, G)
    bdict = dict(base)
    diffs = {name: line_diff(bdict[name], b) for name, b in files}
    expect = dict(zip(G.names(sub), (2, 1, 1, 1)))
    n_changed = {k: sum(1 for x in v if x.startswith('+')) for k, v in diffs.items()}
    if n_changed != expect:
        raise Refused('UNEXPECTED_DIFF_SIZE vs the no-tuple build of %s: %s (expected %s)' % (sub, n_changed, expect))
    out = Path(out_dir)
    doc = {'schema': 'H3_REGENERATE_RECORD_C2V003', 'seal_record': {'path': str(Path(seal_record).resolve()),
                                                                   'sha256': seal_record_sha256},
           'tuple': dict(zip(TUPLE_KEYS, tup)), 'report': rec['report'], 'compare': rec['compare'], 'sub': sub,
           'publish_root': publish_root, 'generator': {'path': str(GENERATOR[0]), 'sha256': GENERATOR[1]},
           'outputs': outputs, 'resolve_source_literal_sha256_utf8': lit, 'chain_checks': checks,
           'no_tuple_build_outputs': base_out, 'line_diff_vs_no_tuple_build': diffs, 'dry_run': bool(dry_run),
           'publish_commands': ['mkdir "%s"' % os.path.join(publish_root, sub)] +
                               ['cp -n "%s" "%s/"' % (os.path.join(str(out), sub, n), os.path.join(publish_root, sub))
                                for n in G.names(sub)[:3]] +
                               ['shasum -a 256 "%s"/*.py   # must equal outputs' % os.path.join(publish_root, sub)]}
    if not dry_run:
        os.mkdir(out / sub)
        for name, b in files:
            with open(out / sub / name, 'xb') as f:
                f.write(b)
        for name, s in outputs.items():
            if sha((out / sub / name).read_bytes()) != s:
                raise Refused('WRITTEN_BYTES_DIFFER: %s' % name)
        with open(out / ('REGENERATE_RECORD_%s.json' % sub), 'x') as f:
            json.dump(doc, f, indent=1, sort_keys=True)
            f.write('\n')
    return doc


def fill(report_path, filled_by, ruling, out, sub='v006r12_c4', publish_root=None, G=None):
    """The seal tuple record from bytes (sealed compare constants as the generator reads them; V from the report)."""
    G = G or load_generator()
    if not isinstance(filled_by, str) or not filled_by.strip() or not isinstance(ruling, str) or not ruling.strip():
        raise Refused('FILLED_BY_AND_RULING_REQUIRED')
    csha, k = G.sealed_constants()
    rraw = Path(report_path).read_bytes()
    rec = {'schema': RECORD_SCHEMA, 'status': FILLED_STATUS, 'sub': sub, 'publish_root': publish_root or G.CX2,
           'tuple': dict(zip(TUPLE_KEYS, (csha, k.get('V007_PREREG_SHA256'), k.get('PIN_ADDENDUM_V005'), k.get('SCHEMA_REPORT'),
                                          sha(rraw)))),
           'report': {'path': os.path.abspath(report_path), 'sha256': sha(rraw)},
           'compare': {'path': G.SEALED_COMPARE, 'sha256': csha}, 'filled_by': filled_by, 'ruling': ruling,
           'filled_from': 'regenerate_h3_c2v003 fill: sealed compare constants + report bytes'}
    check_record(rec, G)
    raw = (json.dumps(rec, indent=1, sort_keys=True) + '\n').encode()
    with open(out, 'xb') as f:
        f.write(raw)
    return {'path': os.path.abspath(out), 'sha256': sha(raw), 'tuple': rec['tuple']}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('fill')
    for k in ('--report', '--filled-by', '--ruling', '--out'):
        f.add_argument(k, required=True)
    f.add_argument('--sub', default='v006r12_c4')
    f.add_argument('--publish-root')
    b = sub.add_parser('build')
    b.add_argument('--seal-record', required=True)
    b.add_argument('--seal-record-sha256', required=True)
    b.add_argument('--out-dir', required=True)
    b.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(argv)
    try:
        if a.cmd == 'fill':
            out = fill(a.report, a.filled_by, a.ruling, a.out, sub=a.sub, publish_root=a.publish_root)
            print(json.dumps(dict(out, status='OK'), indent=1))
            return 0
        doc = run(a.seal_record, a.seal_record_sha256, a.out_dir, dry_run=a.dry_run)
    except (Refused, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': '%s: %s' % (type(exc).__name__, exc)}, indent=1))
        return 2
    except SystemExit as exc:                      # the generator's own refusal (sealed constants unreadable, ...)
        print(json.dumps({'status': 'REFUSED', 'reason': 'GENERATOR_REFUSED: exit %s' % exc.code}, indent=1))
        return 2
    print(json.dumps({'status': 'OK', 'dry_run': doc['dry_run'], 'sub': doc['sub'], 'outputs': doc['outputs'],
                      'chain_checks': doc['chain_checks'], 'publish_commands': doc['publish_commands']}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
