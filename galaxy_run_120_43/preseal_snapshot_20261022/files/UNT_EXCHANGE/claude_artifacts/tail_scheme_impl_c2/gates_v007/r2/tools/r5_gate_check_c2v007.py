"""N6 (root V005 A73) gate checks for the r5 identity comparisons, c2v007 (Claude2 gates_v007).  Two subcommands; each exits 0 only when
every item passes, prints one JSON line, and writes nothing else.

  receipts: every named run must have a FINISHED receipt, read strictly (A71 object_pairs_hook): schema
            UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001, status FINISHED, driver_status COMPLETED, exit_code int 0, stop_reason null, retries 0,
            pins.driver.sha256 = the expected driver sha, result.path = <run>/result.json and result.sha256 = sha256 of those bytes.
            A receipt that is absent, a symlink, unparseable or duplicate-keyed refuses.
  verdicts: every named report must exist (regular file), parse strictly, have schema RUN_IDENTITY_COMPARE_C2V007, the expected gate
            and driver, verdict PASS_BITWISE_EQUAL with failing == [], comparator.sha256 == comparator_sha256_at_end == the pinned
            comparator sha, and the comparator process exit code passed on the command line must be 0.

  python3 -I -B r5_gate_check_c2v007.py receipts --ext DIR --driver-sha S RUN [RUN ...]
  python3 -I -B r5_gate_check_c2v007.py verdicts --comparator-sha S --driver r5 GATE=REPORT=EXITCODE [...]
"""
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def _pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('A71 duplicate JSON key %r' % (k,))
        d[k] = v
    return d


def strict(p):
    p = Path(p)
    if not os.path.lexists(p):
        raise ValueError('ABSENT %s' % p)
    if not stat.S_ISREG(os.lstat(p).st_mode):
        raise ValueError('NOT_A_REGULAR_FILE %s' % p)
    b = p.read_bytes()
    return hashlib.sha256(b).hexdigest(), json.loads(b.decode('utf-8'), object_pairs_hook=_pairs)


def receipts(argv):
    ext, dsha, runs = None, None, []
    i = 0
    while i < len(argv):
        if argv[i] == '--ext':
            ext, i = argv[i + 1], i + 2
        elif argv[i] == '--driver-sha':
            dsha, i = argv[i + 1], i + 2
        else:
            runs.append(argv[i])
            i += 1
    if not ext or not dsha or not runs:
        raise SystemExit('usage')
    out, ok = {}, True
    for r in runs:
        row = {}
        try:
            rsha, rc = strict(Path(ext) / (r + '.receipt.json'))
            res = Path(ext) / r / 'result.json'
            row = {'receipt_sha256': rsha,
                   'schema': rc.get('schema') == 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001',
                   'status_FINISHED': rc.get('status') == 'FINISHED',
                   'driver_status_COMPLETED': rc.get('driver_status') == 'COMPLETED',
                   'exit_code_0': type(rc.get('exit_code')) is int and rc.get('exit_code') == 0,
                   'stop_reason_null': 'stop_reason' in rc and rc.get('stop_reason') is None,
                   'retries_0': type(rc.get('retries')) is int and rc.get('retries') == 0,
                   'driver_pin': ((rc.get('pins') or {}).get('driver') or {}).get('sha256') == dsha,
                   'result_path': (rc.get('result') or {}).get('path') == str(res),
                   'result_sha256_from_bytes': res.is_file() and (rc.get('result') or {}).get('sha256') == hashlib.sha256(res.read_bytes()).hexdigest()}
        except (ValueError, OSError) as e:
            row = {'refused': '%s: %s' % (type(e).__name__, e)}
        row['ok'] = 'refused' not in row and all(v for k, v in row.items() if k not in ('receipt_sha256',))
        ok = ok and row['ok']
        out[r] = row
    print(json.dumps({'check': 'receipts', 'ok': ok, 'runs': out}, sort_keys=True))
    return 0 if ok else 1


def verdicts(argv):
    csha, drv, items = None, None, []
    i = 0
    while i < len(argv):
        if argv[i] == '--comparator-sha':
            csha, i = argv[i + 1], i + 2
        elif argv[i] == '--driver':
            drv, i = argv[i + 1], i + 2
        else:
            items.append(argv[i])
            i += 1
    if not csha or not drv or not items:
        raise SystemExit('usage')
    out, ok = {}, True
    for it in items:
        gate, rp, code = it.split('=', 2)
        row = {'exit_code_0': code == '0'}
        try:
            h, rep = strict(rp)
            row.update({'report_sha256': h,
                        'schema': rep.get('schema') == 'RUN_IDENTITY_COMPARE_C2V007',
                        'gate': rep.get('gate') == gate,
                        'driver': rep.get('driver_selected') == drv,
                        'verdict_PASS_BITWISE_EQUAL': rep.get('verdict') == 'PASS_BITWISE_EQUAL',
                        'failing_empty': rep.get('failing') == [],
                        'comparator_pinned': (rep.get('comparator') or {}).get('sha256') == csha and rep.get('comparator_sha256_at_end') == csha,
                        'verdict': rep.get('verdict'), 'failing': rep.get('failing')})
        except (ValueError, OSError) as e:
            row['refused'] = '%s: %s' % (type(e).__name__, e)
        row['ok'] = 'refused' not in row and all(v for k, v in row.items() if k not in ('report_sha256', 'verdict', 'failing'))
        ok = ok and row['ok']
        out[gate] = row
    print(json.dumps({'check': 'verdicts', 'ok': ok, 'reports': out}, sort_keys=True))
    return 0 if ok else 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('receipts', 'verdicts'):
        raise SystemExit('usage: receipts|verdicts ...')
    return receipts(sys.argv[2:]) if sys.argv[1] == 'receipts' else verdicts(sys.argv[2:])


if __name__ == '__main__':
    raise SystemExit(main())
