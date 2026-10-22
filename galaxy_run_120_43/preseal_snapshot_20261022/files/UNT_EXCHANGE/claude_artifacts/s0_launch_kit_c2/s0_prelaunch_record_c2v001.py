"""s0_prelaunch_record_c2v001.py -- the M-15 (a)+(1) pre-launch record, by exclusive create (A142 item 6).

What it writes (schema UNT_M15_PRELAUNCH_RECORD_C2V001; R3A draft L138 content plus fields that make the order decidable
from bytes):
  (1) date_u: the `date -u` output captured at write time, verbatim (and its epoch second);
  (2) the V006 sha256 from bytes at write time (path, sha256, bytes);
  (3) every gate-document sha that V006 pins (GATE_PIN lines), each with name, path, the sha as written in V006, the
      sha recomputed from bytes now, and the pinning entry id; the root-listed row-gate list (ROOT_LISTED_ROW_GATES NONE
      gives [] explicitly; ROOT_LISTED_ROW_GATE lines give the list, each verified from bytes);
  plus the planned first call (its V006-registered SPEC_PIN, driver and monitor sha, exact outdir / receipt / launch-record
  strings) and the rule references.
Order (map SCRIPT ORDER 1-4): read V006 once -> hash -> parse the pin lines -> verify each pinned gate from bytes ->
capture date -u -> re-hash V006 (refuse if it changed) -> write by 'x' -> fsync file and directory.
Refuses (exit 3, nothing written) when: the output exists; V006 has no GATE_PIN line, a malformed pin line, a duplicate
name, a pin before any '## A<digits>' entry heading, no root-listed row-gate statement or a contradictory one; any
pinned gate is missing or its bytes do not match; a required pin (GATE_DOCUMENT_PINS_V001.json) is absent from V006 or
differs; the first call's SPEC_PIN is absent (unless --check-only --allow-pending-first-spec); V006 changes during the
write.  --check-only prints the record it would write and writes nothing.
V006 pin-line syntax (column 0; path last, spaces allowed in the path):
  GATE_PIN <NAME> <64 hex> </abs/path>        ROOT_LISTED_ROW_GATES NONE        ROOT_LISTED_ROW_GATE <NAME> <64 hex> </abs/path>
  HANDOFF_PIN <NAME> <64 hex> </abs/path>     SPEC_PIN <NAME> <64 hex> </abs/path>     WATCH_PIN <NAME> <64 hex> </abs/path>
CLI:
  PY -I -B s0_prelaunch_record_c2v001.py --v006 V006.md --out RECORD.json
      --require-pins GATE_DOCUMENT_PINS_V001.json --require-pins-sha256 H
      --first-call S0_SEED_SERIAL --driver-sha256 H --monitor-sha256 H --outdir /Volumes/External1/.../RUN --receipt R
      [--check-only [--allow-pending-first-spec]]
Exit: 0 written (or check-only pass), 3 refused, 2 usage.  It launches nothing and never reads a run tree.
"""
import argparse
import calendar
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SCHEMA = 'UNT_M15_PRELAUNCH_RECORD_C2V001'
KINDS = ('GATE_PIN', 'HANDOFF_PIN', 'SPEC_PIN', 'WATCH_PIN', 'ROOT_LISTED_ROW_GATE')
KEYWORD_RE = re.compile(r'^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|ROOT_LISTED_ROW_GATES|ROOT_LISTED_ROW_GATE)(?=\s|$)')
PIN_RE = re.compile(r'^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|ROOT_LISTED_ROW_GATE) ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$')
NONE_LINE = 'ROOT_LISTED_ROW_GATES NONE'
ENTRY_RE = re.compile(r'^## (A[0-9]+)(?=[\s:.(]|$)')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
DATE_FMT = '%a %b %d %H:%M:%S UTC %Y'
RULES = ['M-15 (a)+(1)', 'A142 item 6', 'A143 D2', 'r3a section 4 L453-456', 'RI45-13']


class Refusal(ValueError):
    pass


def need(ok, why):
    if not ok:
        raise Refusal(why)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def parse_v006_pins(raw):
    """All pin lines of V006 bytes -> {'pins': {kind: {name: pin}}, 'row_gates_none': [entries], 'n_lines': N}.
    pin = {kind, name, sha256, path, entry, line}.  Refuses on any malformed or duplicate pin line."""
    text = raw.decode('utf-8')
    pins = {k: {} for k in KINDS}
    none_entries = []
    entry = None
    for i, line in enumerate(text.split('\n'), 1):
        line = line.rstrip('\r')
        m = ENTRY_RE.match(line)
        if m:
            entry = m.group(1)
            continue
        if not KEYWORD_RE.match(line):
            continue
        if line.rstrip() == NONE_LINE:
            need(line == NONE_LINE, 'MALFORMED_PIN_LINE L%d (trailing whitespace)' % i)
            need(entry is not None, 'PIN_BEFORE_ANY_ENTRY_HEADING L%d' % i)
            none_entries.append({'entry': entry, 'line': i})
            continue
        p = PIN_RE.match(line)
        need(p is not None, 'MALFORMED_PIN_LINE L%d' % i)
        need(entry is not None, 'PIN_BEFORE_ANY_ENTRY_HEADING L%d' % i)
        kind, name, sha, path = p.groups()
        need(name not in pins[kind], 'DUPLICATE_PIN %s %s (L%d)' % (kind, name, i))
        pins[kind][name] = {'kind': kind, 'name': name, 'sha256': sha, 'path': path, 'entry': entry, 'line': i}
    return {'pins': pins, 'row_gates_none': none_entries}


def file_sha(path):
    need(os.path.isabs(path), 'PATH_NOT_ABSOLUTE %s' % path)
    try:
        b = Path(path).read_bytes()
    except OSError as e:
        raise Refusal('PINNED_FILE_UNREADABLE %s (%s)' % (path, type(e).__name__)) from None
    return sha_bytes(b), len(b)


def verify_gates(parsed):
    rows = []
    gates = parsed['pins']['GATE_PIN']
    need(len(gates) > 0, 'NO_GATE_PIN_LINES_IN_V006')
    for name in sorted(gates, key=lambda n: gates[n]['line']):
        g = gates[name]
        h, n = file_sha(g['path'])
        need(h == g['sha256'], 'GATE_SHA_MISMATCH %s: V006 %s, bytes %s' % (name, g['sha256'], h))
        rows.append({'name': name, 'path': g['path'], 'sha256_in_v006': g['sha256'], 'sha256_from_bytes': h, 'bytes': n,
                     'entry': g['entry'], 'v006_line': g['line']})
    return rows


def row_gate_list(parsed):
    listed = parsed['pins']['ROOT_LISTED_ROW_GATE']
    nones = parsed['row_gates_none']
    need(bool(listed) or bool(nones), 'GATE_STATUS_LIST_MISSING: V006 states no root-listed row-gate list')
    need(not (listed and nones), 'CONTRADICTORY_ROW_GATE_LIST: ROOT_LISTED_ROW_GATES NONE and ROOT_LISTED_ROW_GATE lines')
    if nones:
        return [], [n['entry'] for n in nones]
    rows = []
    for name in sorted(listed, key=lambda n: listed[n]['line']):
        g = listed[name]
        h, n = file_sha(g['path'])
        need(h == g['sha256'], 'ROW_GATE_SHA_MISMATCH %s' % name)
        rows.append({'name': name, 'path': g['path'], 'sha256_in_v006': g['sha256'], 'sha256_from_bytes': h, 'bytes': n,
                     'entry': g['entry']})
    return rows, sorted({r['entry'] for r in rows})


def check_required(parsed, req_path, req_sha):
    raw = Path(req_path).read_bytes()
    need(sha_bytes(raw) == req_sha, 'REQUIRED_PINS_FILE_SHA_MISMATCH')
    doc = json.loads(raw)
    gates = parsed['pins']['GATE_PIN']
    missing, differ = [], []
    for r in doc['gate_documents']:
        g = gates.get(r['name'])
        if g is None:
            missing.append(r['name'])
        elif g['sha256'] != r['sha256'] or g['path'] != r['path']:
            differ.append(r['name'])
    need(not missing, 'REQUIRED_GATE_PIN_MISSING_IN_V006 %s' % missing)
    need(not differ, 'REQUIRED_GATE_PIN_DIFFERS_IN_V006 %s' % differ)
    want_rows = doc['root_listed_row_gates']['list']
    return {'path': req_path, 'sha256': req_sha, 'n_required': len(doc['gate_documents']), 'all_present': True,
            'required_root_listed_row_gates': want_rows}


def capture_date_u():
    r = subprocess.run(['/bin/date', '-u'], capture_output=True, text=True, env={'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'},
                       timeout=10)
    need(r.returncode == 0, 'DATE_U_FAILED')
    s = r.stdout.rstrip('\n')
    try:
        epoch = calendar.timegm(time.strptime(s, DATE_FMT))
    except ValueError:
        raise Refusal('DATE_U_UNPARSEABLE %r' % s) from None
    return s, epoch


def iso(epoch):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(epoch))


def build(a):
    out = Path(a.out)
    need(out.is_absolute(), 'OUT_NOT_ABSOLUTE')
    need(not os.path.lexists(out), 'RECORD_EXISTS %s' % out)
    need(out.parent.is_dir(), 'OUT_PARENT_MISSING')
    need(HEX64.match(a.driver_sha256 or '') and HEX64.match(a.monitor_sha256 or ''), 'DRIVER_OR_MONITOR_SHA_NOT_64_HEX')
    need(os.path.isabs(a.outdir) and a.receipt == a.outdir + '.receipt.json', 'OUTDIR_RECEIPT_FORM')
    need(not (a.allow_pending_first_spec and not a.check_only), 'ALLOW_PENDING_ONLY_WITH_CHECK_ONLY')
    v006 = Path(a.v006)
    need(v006.is_absolute(), 'V006_NOT_ABSOLUTE')
    raw = v006.read_bytes()                                  # 1. read once, hash
    v_sha = sha_bytes(raw)
    parsed = parse_v006_pins(raw)                            # 2. parse the pin lines (same bytes)
    gates = verify_gates(parsed)                             #    verify each from bytes
    row_gates, row_entries = row_gate_list(parsed)
    req = check_required(parsed, a.require_pins, a.require_pins_sha256)
    need(sorted(r['name'] for r in row_gates) == sorted(r['name'] for r in req['required_root_listed_row_gates']),
         'ROW_GATE_LIST_DIFFERS_FROM_REQUIRED (V006 %s, required %s)' % ([r['name'] for r in row_gates],
                                                                         [r['name'] for r in req['required_root_listed_row_gates']]))
    spec_pin = parsed['pins']['SPEC_PIN'].get(a.first_call)
    if spec_pin is None:
        need(a.allow_pending_first_spec, 'FIRST_CALL_SPEC_NOT_REGISTERED_IN_V006 SPEC_PIN %s' % a.first_call)
        spec = {'name': a.first_call, 'sha256': 'PENDING', 'registered_path': None, 'entry': None}
    else:
        spec = {'name': a.first_call, 'sha256': spec_pin['sha256'], 'registered_path': spec_pin['path'],
                'entry': spec_pin['entry']}
    du, epoch = capture_date_u()                             # 3. date -u at write time
    rec = {
        'schema': SCHEMA,
        'date_u': du,
        'date_u_epoch_s': epoch,
        'date_u_iso': iso(epoch),
        'v006': {'path': str(v006), 'sha256': v_sha, 'bytes': len(raw)},
        'gate_documents_pinned_in_v006': gates,
        'root_listed_row_gates': row_gates,
        'root_listed_row_gates_entries': row_entries,
        'required_pins': req,
        'first_launch': {'spec': spec, 'driver_sha256': a.driver_sha256, 'monitor_sha256': a.monitor_sha256,
                         'outdir': a.outdir, 'receipt': a.receipt, 'launch_receipt': a.receipt + '.launch.json'},
        'v006_write_freeze': 'from this record until the first step-5 NGC launch receipt (the .launch.json utc of the first launch)',
        'on_time_rule': 'a gate is ON-TIME iff its sha256 is pinned in the V006 logged here and this record precedes the first '
                        'launch receipt (launch utc epoch > date_u_epoch_s); any other root-listed gate is LATE',
        'rules': RULES,
        'writer': {'path': str(Path(__file__).resolve()), 'sha256': sha_bytes(Path(__file__).read_bytes())},
        'written_by': 'Claude2 (root), through s0_launch_kit_c2',
    }
    raw2 = v006.read_bytes()                                 # V006 must not change between hash and stamp
    need(sha_bytes(raw2) == v_sha, 'V006_CHANGED_DURING_RECORD')
    return rec


def write_x(path, obj):
    b = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        os.write(fd, b)
        os.fsync(fd)
    finally:
        os.close(fd)
    dfd = os.open(os.path.dirname(path), os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return sha_bytes(b)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ('v006', 'out', 'require-pins', 'require-pins-sha256', 'first-call', 'driver-sha256', 'monitor-sha256', 'outdir',
              'receipt'):
        ap.add_argument('--' + k, required=True)
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--allow-pending-first-spec', action='store_true')
    a = ap.parse_args(argv)
    try:
        rec = build(a)
        if a.check_only:
            print(json.dumps({'status': 'CHECK_ONLY_PASS', 'written': False, 'record': rec}, indent=1, sort_keys=True))
            return 0
        h = write_x(a.out, rec)                              # 4. exclusive create + fsync
    except (Refusal, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({'status': 'REFUSED', 'written': False, 'reason': '%s: %s' % (type(e).__name__, e)}))
        return 3
    print(json.dumps({'status': 'WRITTEN', 'path': a.out, 'sha256': h, 'date_u': rec['date_u'],
                      'date_u_epoch_s': rec['date_u_epoch_s'], 'v006_sha256': rec['v006']['sha256'],
                      'n_gate_documents': len(rec['gate_documents_pinned_in_v006']),
                      'root_listed_row_gates': rec['root_listed_row_gates']}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
