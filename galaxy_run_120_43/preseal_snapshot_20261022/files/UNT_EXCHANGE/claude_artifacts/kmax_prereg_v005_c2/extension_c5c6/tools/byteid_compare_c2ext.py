"""Compare c2v008 and c2v009 dry-run outputs pairwise (post-hoc, read-only on the dry-run dirs).
For each pair name X with dry/v008_X and dry/v009_X (or only logs when the call was refused/blocked):
  * stdout and stderr of the two runs, with the driver path and driver sha replaced by a token;
  * DRYRUN_PLAN.txt bytes (same substitution);
  * every file under simulated_call/ (bytes, no substitution);
  * DRYRUN_REPORT.json: deep leaf diff after the substitution; differing leaves are listed (expected: none except the
    static/transitive pin listings, which in c2v009 also contain prep v009).
usage: python3 -I -B byteid_compare_c2ext.py DRYRUN_DIR OUT.json"""
import hashlib
import re
import json
import sys
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V8 = (str(EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py'), 'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28')
V9P = EX / 'kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py'
V9 = (str(V9P), hashlib.sha256(V9P.read_bytes()).hexdigest())


def norm(t, v, rd=None, shamap=None):
    """Driver path/sha -> token; the report dir (absolute, differs per side by construction) -> <RD>; and the sha256 of
    every simulated file -> the sha256 of its <RD>-normalized bytes (so a hash differs only if normalized content does)."""
    p, s = V8 if v == 'v008' else V9
    t = t.replace(p, '<DRIVER>').replace(s, '<DRIVER_SHA>').replace(s[:12], '<DRIVER_SHA12>').replace(s[:16], '<DRIVER_SHA16>')
    if rd is not None:
        t = t.replace(str(rd), '<RD>')
    for a, b in (shamap or {}).items():
        t = t.replace(a, b).replace(a[:12], b[:12]).replace(a[:16], b[:16])
    return t


def sim_files(rd, v):
    """{relpath: (raw sha, normalized-content sha)} for every file under simulated_call/."""
    out = {}
    for f in (rd / 'simulated_call').rglob('*'):
        if f.is_file():
            raw = f.read_bytes()
            out[str(f.relative_to(rd))] = (hashlib.sha256(raw).hexdigest(),
                                           hashlib.sha256(norm(raw.decode('utf-8', 'surrogateescape'), v, rd).encode('utf-8', 'surrogateescape')).hexdigest())
    return out


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + str(k)))
        return out or {p: '{}'}
    if isinstance(o, list):
        out = {}
        for i, v in enumerate(o):
            out.update(leaves(v, p + '[%d]' % i))
        return out or {p: '[]'}
    return {p: json.dumps(o)}


def main():
    d, outp = Path(sys.argv[1]), Path(sys.argv[2])
    names = sorted({p.name[5:] for p in (d / 'logs').glob('v008_*.stdout.txt')} & {p.name[5:] for p in (d / 'logs').glob('v009_*.stdout.txt')})
    names = [n[:-len('.stdout.txt')] for n in names]
    names = [n for n in names if n != 'C5_N8']  # v008_C5_N8 is the negative test (c2v008 must refuse the G5 spec)
    res = {}
    for n in names:
        r = {}
        for ext in ('stdout.txt', 'stderr.txt'):
            a = norm((d / 'logs' / ('v008_%s.%s' % (n, ext))).read_text(), 'v008', (d / 'dry' / ('v008_' + n)).resolve())
            b = norm((d / 'logs' / ('v009_%s.%s' % (n, ext))).read_text(), 'v009', (d / 'dry' / ('v009_' + n)).resolve())
            r[ext + '_raw_identical'] = a == b
            # guard summary line (n_opened differs by the one extra pin file c2v009 verifies) and traceback line numbers
            # (c2v009 is 39 lines longer) are the only allowed differences; both are normalized here and reported raw above.
            a = re.sub(r', line \d+,', ', line N,', a)
            b = re.sub(r', line \d+,', ', line N,', b)
            ga = [json.loads(x) for x in a.splitlines() if x.startswith('{"exit"')]
            gb = [json.loads(x) for x in b.splitlines() if x.startswith('{"exit"')]
            r[ext + '_guard_exit_denied_equal'] = [(g['exit'], g['denied']) for g in ga] == [(g['exit'], g['denied']) for g in gb]
            a = '\n'.join(x for x in a.splitlines() if not x.startswith('{"exit"'))
            b = '\n'.join(x for x in b.splitlines() if not x.startswith('{"exit"'))
            r[ext + '_identical'] = a == b and r[ext + '_guard_exit_denied_equal']
        a8, a9 = (d / 'dry' / ('v008_' + n)).resolve(), (d / 'dry' / ('v009_' + n)).resolve()
        if (a8 / 'DRYRUN_PLAN.txt').is_file() or (a9 / 'DRYRUN_PLAN.txt').is_file():
            s8, s9 = sim_files(a8, 'v008'), sim_files(a9, 'v009')
            m8 = {raw: nrm for raw, nrm in s8.values() if raw != nrm}
            m9 = {raw: nrm for raw, nrm in s9.values() if raw != nrm}
            r['plan_identical_raw_after_driver_token'] = norm((a8 / 'DRYRUN_PLAN.txt').read_text(), 'v008') == norm((a9 / 'DRYRUN_PLAN.txt').read_text(), 'v009')
            r['plan_identical'] = norm((a8 / 'DRYRUN_PLAN.txt').read_text(), 'v008', a8, m8) == norm((a9 / 'DRYRUN_PLAN.txt').read_text(), 'v009', a9, m9)
            f8 = {k: v[1] for k, v in s8.items()}
            f9 = {k: v[1] for k, v in s9.items()}
            r['simulated_files'] = len(f8)
            r['simulated_files_raw_identical'] = sorted(k for k in s8 if s9.get(k, (None,))[0] == s8[k][0])
            r['simulated_files_identical'] = f8 == f9
            r['simulated_files_differing'] = sorted(k for k in set(f8) | set(f9) if f8.get(k) != f9.get(k))
            j8 = leaves(json.loads(norm((a8 / 'DRYRUN_REPORT.json').read_text(), 'v008', a8, m8)))
            j9 = leaves(json.loads(norm((a9 / 'DRYRUN_REPORT.json').read_text(), 'v009', a9, m9)))
            diff = sorted(k for k in set(j8) | set(j9) if j8.get(k) != j9.get(k))
            r['report_leaves'] = len(j8)
            r['report_leaves_differing'] = len(diff)
            r['report_differing_top_keys'] = sorted({k.split('/')[1].split('[')[0] for k in diff})
            r['report_differing_outside_pin_listings'] = [k for k in diff if not k.startswith(('/static_pins', '/transitive_pins'))]
            r['report_pin_listing_additions'] = sorted({k.split('/')[2] if k.count('/') >= 2 else k for k in diff
                                                        if k.startswith(('/static_pins', '/transitive_pins')) and k not in j8})[:6]
        else:
            r['plan_identical'] = None
        r['IDENTICAL'] = (r['stdout.txt_identical'] and r['stderr.txt_identical'] and r['plan_identical'] in (True, None)
                          and r.get('simulated_files_identical', True) and not r.get('report_differing_outside_pin_listings'))
        res[n] = r
    out = {'schema': 'UNT_C2V008_C2V009_DRY_BYTE_IDENTITY_V001', 'v008': V8, 'v009': V9, 'pairs': res,
           'all_identical': all(r['IDENTICAL'] for r in res.values())}
    with open(outp, 'x') as f:
        json.dump(out, f, indent=1)
    for n, r in res.items():
        print(n.ljust(22), 'IDENTICAL' if r['IDENTICAL'] else 'DIFF', {k: v for k, v in r.items() if k in ('plan_identical', 'simulated_files', 'report_leaves_differing', 'report_differing_top_keys', 'report_differing_outside_pin_listings')})
    print('all_identical', out['all_identical'])


if __name__ == '__main__':
    main()
