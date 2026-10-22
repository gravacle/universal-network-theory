"""Mutation check for values_writer_c2v003a (v003's 44 + 3 equivalent, the member_valid sites re-targeted, plus the B1
mutants M45-M50): each mutant is one source edit at a site that occurs exactly once; the suite
must fail on every mutant not marked equivalent. Equivalent mutants (a conjunct implied by a check that refuses earlier)
are run and reported; they are expected to survive and are not counted as kills.
Usage: python3 -I -B mutation_values_writer_c2v003a.py --module <writer.py> --tests <test.py> --work <new dir>
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    # ---- v002's 16, re-targeted to the v003 source where the line changed
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
    ('M07 apply the inclination factor', "            eps.append(float(by_id[q]))",
     "            eps.append(float(by_id[q]) * (co['inclination']['sin_ratio'] or 1.0))"),
    ('M08 skip the other-point refusal', "if not _hex(theta_key) or pt.get('key') != theta_key:", "if not _hex(theta_key):"),
    ('M09 invalid call rows read 0.0 in place of None', "            eps.append(None)\n            why.append('ROW_INVALID_IN_CALL: '",
     "            eps.append(0.0)\n            why.append('ROW_INVALID_IN_CALL: '"),
    ('M10 reorder silently (final_rows order check by set)', "if [r.get('id') for r in rows] != list(query_ids):",
     "if sorted(r.get('id') for r in rows) != sorted(query_ids):"),
    ('M11 skip the explicit coverage check', "if lo < cov[0] - 1e-12 or hi > cov[1] + 1e-12:", "if False:"),
    ('M12 attach without the root-ruling gate',
     "    ruling = check_root_ruling()\n    if kind not in KINDS:\n        raise Refused('KIND', repr(kind))\n    if not isinstance(doc, dict)",
     "    ruling = ROOT_RULING\n    if kind not in KINDS:\n        raise Refused('KIND', repr(kind))\n    if not isinstance(doc, dict)"),
    ('M13 skip the spec eps-pin check', "if uv.get('eps_certificate') != cert_pin:", "if False:"),
    ('M14 accept SMOKE / BIND_CHECK schemas', "rec.get('schema') not in CERT_SCHEMAS", "not str(rec.get('schema')).startswith(CERT_SCHEMAS[0])"),
    ('M15 feed the envelope in place of the larger eps', "'eps': float(eps)})",
     "'eps': float((s.get('envelope') or {}).get('eps_envelope', eps))})"),
    ('M16 skip the row-columns cross-check', "if rows['row_columns'] != co['support_columns']:", "if False:"),
    # ---- v003: the A152 pin
    ('M17 the ruling section sha is not compared', "if hashlib.sha256(ruling_section(raw, r['section'])).hexdigest() != r['sha256']:",
     "if False:"),
    ('M18 the ruling heading need not be unique', "    if len(heads) != 1:", "    if not heads:"),
    # ---- v003: W-3 result and finish
    ('M19 skip the finish.result_sha256 check', "if not _hex(fin.get('result_sha256')) or fin['result_sha256'] != rsha:",
     "if not _hex(fin.get('result_sha256')):"),
    ('M20 skip the finish.result_path check', "    if not path_ok:", "    if False:"),
    ('M21 skip finish/result status and valid agreement',
     "if type(ok) is not bool or res.get('status') != st or res.get('valid') is not ok:", "if type(ok) is not bool:"),
    ('M22 accept an unknown status', "    if st not in CALL_STATUSES:", "    if False:"),
    ('M23 skip the COMPLETED <-> valid invariant',
     "if (st == 'COMPLETED' and ok is not True) or (st == 'COMPLETED_INVALID' and ok is not False):", "if False:"),
    ('M24 result_pin sha taken from the finish file bytes', "'result_pin': {'path': str(rp), 'sha256': fin['result_sha256']},",
     "'result_pin': {'path': str(rp), 'sha256': hashlib.sha256(fraw).hexdigest()},"),
    ('M25 COMPLETED without final rows tolerated', "        if c['status'] == 'COMPLETED':\n            raise Refused('COMPLETED_WITHOUT_FINAL_ROWS')",
     "        if False:\n            raise Refused('COMPLETED_WITHOUT_FINAL_ROWS')"),
    ('M26 skip the result.speeds_km_s cross-check', "if res.get('speeds_km_s') != {r['id']: r.get('speed_km_s') for r in rows}:",
     "if False:"),
    ('M27 valid[q] without the status conjunct', "'valid': [bool(v is True and c['valid'] is True and completed) for v in row_valid],",
     "'valid': [bool(v is True and c['valid'] is True) for v in row_valid],"),
    ('M28 member_valid without the acceptance conjunct (re-targeted to the v003a line)',
     "p['member_valid'] = bool(c['valid'] is True and completed and acc is not None\n                                 and acc['counts_for_member_valid'] is True)",
     "p['member_valid'] = bool(c['valid'] is True and completed)"),
    ('M29 member_valid without the status conjunct', "p['member_valid'] = bool(c['valid'] is True and completed and acc is not None",
     "p['member_valid'] = bool(c['valid'] is True and acc is not None"),
    ('M30 member_valid also accepts ACCEPTED_PASS_FLAGGED', "MEMBER_ACCEPTANCE_READINGS = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT')",
     "MEMBER_ACCEPTANCE_READINGS = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT', 'ACCEPTED_PASS_FLAGGED')"),
    ('M31 skip the acceptance-to-call binding', "if rec.get('result') != c['result_pin'] or rec.get('call_dir') != str(c['call']):",
     "if False:"),
    ('M32 skip the acceptance schema check', "if not isinstance(rec, dict) or rec.get('schema') not in ACCEPTANCE_SCHEMAS:",
     "if not isinstance(rec, dict):"),
    ('M33 skip the acceptance handoff-producer check', "if not is_pin(h) or h['sha256'] not in ACCEPTANCE_HANDOFFS:",
     "if not is_pin(h):"),
    ('M34 accept an unknown acceptance reading', "    if rd not in ACCEPTANCE_READINGS:", "    if False:"),
    # ---- v003: W-3 eps rows
    ('M35 a row with v <= 0 keeps its bound', "        elif not speed[q] > 0:", "        elif False:"),
    ('M36 nonpositive rotation refused as in v002 (W-3 branch removed)', "    if co['rotation_positive'] is False:   # W-3",
     "    if False:   # W-3"),
    ('M37 skip the rotation positivity consistency check',
     "if bool(np.all(omega > 0)) is not positive or (positive is False and c['valid'] is not False):", "if False:"),
    ('M38 skip the post-attach W-3 guard (eps without a speed)', "if e is not None and (s is None or not s > 0):", "if False:"),
    # ---- v003: manifest and inputs
    ('M39 skip the manifest order check', "    if ids != list(query_ids):\n        raise Refused('MANIFEST_ORDER_MISMATCH'",
     "    if False:\n        raise Refused('MANIFEST_ORDER_MISMATCH'"),
    ('M40 skip the manifest radius cross-check', "            if not d <= RADIUS_REL_TOL:", "            if False:"),
    ('M41 Phase-1 roles not checked', "        if sorted(roles) != sorted(PHASE1_ROLES) or", "        if False and sorted(roles) != sorted(PHASE1_ROLES) or"),
    ('M42 members log_index not checked',
     "if not all(type(li) is int and li >= 0 for li in lis) or len(set(lis)) != len(lis):", "if False:"),
    ('M43 radius cross-check by id with the support radius masking the row radius',
     "        pairs = list(row_radius.items()) + list(zip(ri.get('row_ids') or [], ri.get('row_radii_m') or []))",
     "        pairs = list(dict(row_radius, **dict(zip(ri.get('row_ids') or [], ri.get('row_radii_m') or []))).items())"),
    ('M44 no-rows branch skips the spec eps-pin check',
     "        if ns is not None and (not isinstance(ns, dict) or ((ns.get('numerics') or {}).get('uv_tail') or {}).get(",
     "        if False and (not isinstance(ns, dict) or ((ns.get('numerics') or {}).get('uv_tail') or {}).get("),
    # ---- v003a: B1, the member_valid acceptance producer gate
    ('M45 admit the DDO154 handoff c2v004 record for member_valid (the v003 behaviour, B1)',
     "MEMBER_ACCEPTANCE_PRODUCERS = ()", "MEMBER_ACCEPTANCE_PRODUCERS = ((ACCEPTANCE_SCHEMAS[0], ACCEPTANCE_HANDOFFS[0]),)"),
    ('M46 counts_for_member_valid without the producer gate', "'counts_for_member_valid': g5 and rd in MEMBER_ACCEPTANCE_READINGS,",
     "'counts_for_member_valid': rd in MEMBER_ACCEPTANCE_READINGS,"),
    ('M47 counts_for_member_valid without the reading conjunct', "'counts_for_member_valid': g5 and rd in MEMBER_ACCEPTANCE_READINGS,",
     "'counts_for_member_valid': g5,"),
    ('M48 producer matched on the handoff sha alone (not the schema/sha pair)',
     "g5 = (rec['schema'], h['sha256']) in MEMBER_ACCEPTANCE_PRODUCERS",
     "g5 = h['sha256'] in [x[1] for x in MEMBER_ACCEPTANCE_PRODUCERS]"),
    ('M49 member_valid_basis omits the producer gap', "(acc is None or acc['g5_producer'], PRODUCER_GAP),", "(True, PRODUCER_GAP),"),
    ('M50 the members document does not print the member_valid gate', "    if kind == 'phase2_members':    # v003a (B1)",
     "    if False:    # v003a (B1)"),
    # ---- equivalent by construction (reported, expected to survive)
    ('E01 valid[q] without the call-valid conjunct [EQUIVALENT: status COMPLETED implies valid true, refused otherwise (M23 site)]',
     "'valid': [bool(v is True and c['valid'] is True and completed) for v in row_valid],",
     "'valid': [bool(v is True and completed) for v in row_valid],"),
    ('E02 member_valid without the call-valid conjunct [EQUIVALENT: as E01]',
     "p['member_valid'] = bool(c['valid'] is True and completed and acc is not None",
     "p['member_valid'] = bool(completed and acc is not None"),
    ('E03 call_outputs order check removed [EQUIVALENT: final_rows refuses the same order first (M10 site)]',
     "    if ids != list(query_ids):\n        raise Refused('QUERY_ORDER_MISMATCH'", "    if False:\n        raise Refused('QUERY_ORDER_MISMATCH'"),
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
        eq = name.startswith('E')
        if src.count(old) != 1:
            out.append({'mutant': name, 'equivalent': eq, 'applied': False, 'killed': False,
                        'site_count': src.count(old)})
            print('%s: NOT APPLIED (site count %d)' % (name, src.count(old)), flush=True)
            continue
        mut = src.replace(old, new, 1)
        d = work / ('m%02d' % (i + 1))
        d.mkdir()
        mp = d / 'values_writer_c2v003a.py'
        with open(mp, 'x') as f:
            f.write(mut)
        cp = subprocess.run([sys.executable, '-I', '-B', a.tests, '--module', str(mp), '--work', str(d / 'run')],
                            capture_output=True, text=True)
        fails = [ln for ln in cp.stdout.splitlines() if ln.startswith('FAIL')]
        out.append({'mutant': name, 'equivalent': eq, 'applied': True, 'killed': cp.returncode != 0 and bool(fails),
                    'n_failed': len(fails), 'first_failures': fails[:3],
                    'mutant_sha256': hashlib.sha256(mp.read_bytes()).hexdigest()})
        print('%s: %s (%d failing tests)' % (name, 'KILLED' if out[-1]['killed'] else 'SURVIVED', len(fails)), flush=True)
    counted = [o for o in out if not o['equivalent']]
    res = {'module_sha256': hashlib.sha256(Path(a.module).read_bytes()).hexdigest(),
           'tests_sha256': hashlib.sha256(Path(a.tests).read_bytes()).hexdigest(),
           'n': len(counted), 'killed': sum(o['killed'] for o in counted),
           'n_equivalent': len(out) - len(counted), 'equivalent_survived': sum(not o['killed'] for o in out if o['equivalent']),
           'mutants': out}
    with open(work / 'RESULTS_MUTATION_VALUES_WRITER_C2V003A.json', 'x') as f:
        json.dump(res, f, indent=1)
    print('%d/%d mutants killed; %d equivalent (%d survived, as expected)'
          % (res['killed'], res['n'], res['n_equivalent'], res['equivalent_survived']))
    return 0 if res['killed'] == res['n'] and all(o['applied'] for o in out) else 1


if __name__ == '__main__':
    sys.exit(main())
