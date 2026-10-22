"""Mutation check for values_writer_c2v002: each mutant is one source edit; the suite must fail on every mutant.
Usage: python3 -I -B mutation_values_writer_c2v002.py --module <writer.py> --tests <test.py> --work <new dir>
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ('M01 broadcast eps_max into every shell', "out.append({'lo_inverse_kpc': float(lo), 'hi_inverse_kpc': float(hi), 'eps': float(eps)})",
     "out.append({'lo_inverse_kpc': float(lo), 'hi_inverse_kpc': float(hi), 'eps': float(rec.get('eps_max', eps))})"),
    ('M02 the bound at one node (R_q-like) in place of the max over the row columns',
     "sr = lib.srb_rot(st, cert, dict(rows, tau_km_s=",
     "sr = lib.srb_rot(st, cert, dict(rows, row_columns=[[ix[0]] for ix in rows['row_columns']], tau_km_s="),
    ('M03 a declared N_min = 1', "sr = lib.srb_rot(st, cert, dict(rows, tau_km_s=",
     "sr = lib.srb_rot(st, cert, dict(rows, N_min=1.0, tau_km_s="),
    ('M04 v = the call speeds in place of v_c', "sr = lib.srb_rot(st, cert, dict(rows, tau_km_s=",
     "sr = lib.srb_rot(st, cert, dict(rows, v_c_m_s=[1e5] * len(rows['v_c_m_s']), tau_km_s="),
    ('M05 skip the state eps-pin check (adapter L434 analog)', "if record.get('eps_certificate') != cert_pin:", "if False:"),
    ('M06 skip the state digest binding', "expected_digest=finish_uv['state_digest']", "expected_digest=None"),
    ('M07 apply the inclination factor', "eps = [float(by_id[q]) if q in by_id else None for q in query_ids]",
     "eps = [float(by_id[q]) * (co['inclination']['sin_ratio'] or 1.0) if q in by_id else None for q in query_ids]"),
    ('M08 skip the other-point refusal', "if not _hex(theta_key) or pt.get('key') != theta_key:", "if not _hex(theta_key):"),
    ('M09 invalid call rows read 0.0 in place of None', "eps = [float(by_id[q]) if q in by_id else None for q in query_ids]",
     "eps = [float(by_id[q]) if q in by_id else 0.0 for q in query_ids]"),
    ('M10 reorder silently (skip the query-order refusal)', "if ids != list(query_ids):", "if sorted(ids) != sorted(query_ids):"),
    ('M11 skip the explicit coverage check', "if lo < cov[0] - 1e-12 or hi > cov[1] + 1e-12:", "if False:"),
    ('M12 attach without the root ruling', "    if ROOT_RULING is None:\n        raise Refused('ROOT_RULING_PENDING'",
     "    if False:\n        raise Refused('ROOT_RULING_PENDING'"),
    ('M13 skip the spec eps-pin check', "if uv.get('eps_certificate') != cert_pin:", "if False:"),
    ('M14 accept SMOKE / BIND_CHECK schemas', "rec.get('schema') not in CERT_SCHEMAS", "not str(rec.get('schema')).startswith(CERT_SCHEMAS[0])"),
    ('M15 feed the envelope in place of the larger eps', "'eps': float(eps)})",
     "'eps': float((s.get('envelope') or {}).get('eps_envelope', eps))})"),
    ('M16 skip the row-columns cross-check', "if rows['row_columns'] != co['support_columns']:", "if False:"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--module', required=True)
    ap.add_argument('--tests', required=True)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=False)
    src = Path(a.module).read_text()
    out = []
    for i, (name, old, new) in enumerate(MUTANTS):
        if src.count(old) < 1:
            out.append({'mutant': name, 'applied': False, 'killed': False})
            continue
        mut = src.replace(old, new, 1)
        d = work / ('m%02d' % (i + 1))
        d.mkdir()
        mp = d / 'values_writer_c2v002.py'
        with open(mp, 'x') as f:
            f.write(mut)
        cp = subprocess.run([sys.executable, '-I', '-B', a.tests, '--module', str(mp), '--work', str(d / 'run')],
                            capture_output=True, text=True)
        fails = [ln for ln in cp.stdout.splitlines() if ln.startswith('FAIL')]
        out.append({'mutant': name, 'applied': True, 'killed': cp.returncode != 0 and bool(fails),
                    'n_failed': len(fails), 'first_failures': fails[:3],
                    'mutant_sha256': hashlib.sha256(mp.read_bytes()).hexdigest()})
        print('%s: %s (%d failing tests)' % (name, 'KILLED' if out[-1]['killed'] else 'SURVIVED', len(fails)), flush=True)
    res = {'module_sha256': hashlib.sha256(Path(a.module).read_bytes()).hexdigest(),
           'tests_sha256': hashlib.sha256(Path(a.tests).read_bytes()).hexdigest(),
           'n': len(out), 'killed': sum(o['killed'] for o in out), 'mutants': out}
    with open(work / 'RESULTS_MUTATION_VALUES_WRITER_C2V002.json', 'x') as f:
        json.dump(res, f, indent=1)
    print('%d/%d mutants killed' % (res['killed'], res['n']))
    return 0 if res['killed'] == res['n'] else 1


if __name__ == '__main__':
    sys.exit(main())
