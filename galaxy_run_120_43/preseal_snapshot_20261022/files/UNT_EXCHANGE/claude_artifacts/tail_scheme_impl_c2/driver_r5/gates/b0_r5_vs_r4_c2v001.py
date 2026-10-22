"""Gate B0 (A55 ruling 2): plan identity of driver v010 r5 against r4, on every spec, with the B0-EMPTY rule (A54, Codex2
SHOULD_FIX B0-EMPTY ruled).  Claude2 lane, driver_r5.  Successor in method of driver_r4/gates/b0_plan_identity_c2v002.py (b9aeb78e).

Both drivers run `dry-run` (simulate; no stage is executed) on each spec.  Every file of the two report directories is compared
after the declared substitution map T, which is the pin swap of CASCADE_MAP_R5_C2V001.json (declared old path -> new path,
old sha -> new sha, and the printed basenames of the re-pinned files), plus the driver path + sha and the report directory.
T is never derived from the observed difference: derived file hashes are added only where T(r4 bytes) == r5 bytes (fixpoint,
cmp_dry_check_v001 af853189); DRYRUN_PLAN.txt hash prefixes (12/16 chars) of every full-hash pair are substituted.
No other map is applied (r5 adds no RO1 key, no prep pin and moves no driver line, so r4's ro1/ext/needle maps are not used).
B0-EMPTY rule: a comparison COUNTS only if, on both sides, the dry run exits 0 and the expected reports DRYRUN_REPORT.json and
DRYRUN_PLAN.txt are non-empty (planning completed); counted comparisons PASS_PLAN_IDENTICAL or FAIL.  Two early failures with
equal exit codes and equal terminal lines after T are listed separately as NO_EVIDENCE_EQUAL_EARLY_FAILURE (not counted, not
passed); any other early failure is FAIL.
Spec sets (deduplicated by realpath; every sha from bytes): (a) the r4 B0 standard set and B0_FA set (SPECS / FA_SPECS of
b0_plan_identity_c2v002, read from its pinned bytes); (b) every spec of the r4 V007 registry SPECS_V007_C2V002_R1 (9bfe9674) incl.
identity gates and registered specs; (c) the P=128 V007 specs (SPECS_P128_R5_C2V001: Codex1 registry V002, TEMPLATE + FILLED).
Usage: python3 -I -B b0_r5_vs_r4_c2v001.py R5_PATH R5_SHA MAP_SHA P128_REG_SHA OUTDIR [MAX_PROCS]"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import types
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UVT = EX / 'tail_scheme_impl_c2'
R4 = (UVT / 'driver_r4/galaxy_m0_forward_c2v010.py', 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b')
R4_B0 = (UVT / 'driver_r4/gates/b0_plan_identity_c2v002.py', 'b9aeb78e8a58ab369e923b4092cf504400633259843a7b129183333f7806cef3')
R4_REG = (UVT / 'driver_r4/specs/SPECS_V007_C2V002_R1.json', '9bfe96741a8aa86a8956f67fab9ebcb62548f228aaaf54dd6c1633754d26e69f')
MAP = UVT / 'driver_r5/CASCADE_MAP_R5_C2V001.json'
P128 = UVT / 'driver_r5/specs/SPECS_P128_R5_C2V001.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    ENV[_k] = '1'


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    return sha_b(Path(p).read_bytes())


def dry(driver_path, spec, rd):
    t0 = time.monotonic()
    p = subprocess.run(['nice', '-n', '10', PY, '-I', '-B', str(driver_path), 'dry-run', '--spec', str(spec), '--report-dir', str(rd)],
                       capture_output=True, text=True, env=ENV, cwd=str(Path(rd).parent))
    return {'exit': p.returncode, 'seconds': round(time.monotonic() - t0, 2),
            'stderr_tail': p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else [], 'stdout_bytes': len(p.stdout)}


def files(d):
    d = Path(d)
    return {str(p.relative_to(d)): p.read_bytes() for p in sorted(d.rglob('*')) if p.is_file()} if d.is_dir() else {}


def apply(pairs, b):
    for a, c in pairs:
        b = b.replace(a.encode(), c.encode())
    return b


def declared_map(r5_path, r5_sha):
    m = json.loads(MAP.read_text())
    # re-pinned files only (old sha != new sha); the byte-identical sibling copies are not pins of any consumer
    paths = [(r['old_path'], r['new_path']) for r in m['files'] if r['old_sha256'] != r['new_sha256']]
    paths.sort(key=lambda x: -len(x[0]))
    shas = sorted(m['declared_sha_map'].items())
    names = [(Path(o).name, Path(n).name) for o, n in paths if Path(o).name != Path(n).name]
    pairs = paths + [(str(R4[0]), str(r5_path))] + shas + [(R4[1], r5_sha)] + names
    assert m['declared_sha_map'][R4[1]] == r5_sha and m['declared_path_map'][str(R4[0])] == str(r5_path)
    return pairs


def compare(d4, d5, base):
    f4, f5 = files(d4), files(d5)
    pairs = list(base) + [(str(d4), str(d5))]
    for _ in range(8):
        added = False
        known = {a for a, _ in pairs}
        for n in f4:
            if n in f5:
                h4, h5 = sha_b(f4[n]), sha_b(f5[n])
                if h4 != h5 and h4 not in known and apply(pairs, f4[n]) == f5[n]:
                    pairs.append((h4, h5))
                    added = True
        if not added:
            break
    hp = [(a, b) for a, b in pairs if re.fullmatch('[0-9a-f]{64}', a)]
    prefix = pairs + [(a[:16], b[:16]) for a, b in hp] + [(a[:12], b[:12]) for a, b in hp]
    res = {'files_r4': len(f4), 'files_r5': len(f5), 'only_r4': sorted(set(f4) - set(f5)), 'only_r5': sorted(set(f5) - set(f4)),
           'raw_equal': 0, 'equal_after_T': 0, 'differ': {}, 'derived_hash_pairs': len(pairs) - len(base) - 1,
           'reports_nonempty': all(len(side.get(k, b'')) > 0 for side in (f4, f5) for k in ('DRYRUN_REPORT.json', 'DRYRUN_PLAN.txt'))}
    for n in sorted(set(f4) & set(f5)):
        if f4[n] == f5[n]:
            res['raw_equal'] += 1
            continue
        a = apply(prefix if n.endswith('DRYRUN_PLAN.txt') else pairs, f4[n])
        if a == f5[n]:
            res['equal_after_T'] += 1
            continue
        al, bl = a.decode(errors='replace').splitlines(), f5[n].decode(errors='replace').splitlines()
        dl = [(i, x[:300], y[:300]) for i, (x, y) in enumerate(zip(al, bl)) if x != y]
        res['differ'][n] = {'n_lines': [len(al), len(bl)], 'first_diff_lines': dl[:8], 'n_diff_lines': len(dl)}
    res['identical'] = not res['only_r4'] and not res['only_r5'] and not res['differ']
    return res


def spec_sets():
    for p, s in (R4_B0, R4_REG):
        if sha_f(p) != s:
            raise SystemExit('pin ' + str(p))
    m = types.ModuleType('r4_b0_inert')
    m.__file__ = str(R4_B0[0])
    exec(compile(Path(R4_B0[0]).read_bytes(), str(R4_B0[0]), 'exec'), m.__dict__)
    out, seen = [], {}

    def add(name, path, origin):
        rp = os.path.realpath(str(path))
        if rp in seen:
            seen[rp]['origins'].append(origin)
            return
        seen[rp] = {'name': name, 'spec': str(path), 'spec_sha256': sha_f(path), 'origins': [origin]}
        out.append(seen[rp])
    for name, path, _ in m.SPECS:
        add(name, path, 'r4 B0 standard set')
    for name, path in m.FA_SPECS:
        add(name, path, 'r4 B0_FA set')
    reg = json.loads(R4_REG[0].read_text())
    for e in reg['specs']:
        if sha_f(e['file']) != e['sha256']:
            raise SystemExit('r4 registry spec pin ' + e['file'])
        add('R4REG_' + Path(e['file']).name.replace('.json', ''), e['file'], 'r4 V007 registry: ' + e['role'])
    for k, v in reg['registered_specs_used_unchanged'].items():
        if sha_f(v['path']) != v['sha256']:
            raise SystemExit('r4 registered spec pin ' + k)
        add('R4REG_' + k, v['path'], 'r4 V007 registry registered: ' + k)
    p128 = json.loads(P128.read_text())
    for e in p128['specs']:
        if sha_f(e['file']) != e['sha256']:
            raise SystemExit('P128 spec pin ' + e['file'])
        add('P128_' + Path(e['file']).name.replace('.json', ''), e['file'], e['role'])
    return out


def main():
    r5, r5_sha, map_sha, p128_sha, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], Path(sys.argv[5])
    maxp = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    if sha_f(r5) != r5_sha or sha_f(R4[0]) != R4[1] or sha_f(MAP) != map_sha or sha_f(P128) != p128_sha:
        raise SystemExit('pin')
    jobs = spec_sets()
    base = declared_map(r5, r5_sha)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'dry').mkdir()
    runs = {}
    with cf.ThreadPoolExecutor(max_workers=maxp) as ex:
        fut = {}
        for j in jobs:
            for tag, drv in (('R4', R4[0]), ('R5', r5)):
                fut[ex.submit(dry, drv, j['spec'], out / 'dry' / ('%s_%s' % (tag, j['name'])))] = (tag, j['name'])
        for f in cf.as_completed(fut):
            runs[fut[f]] = f.result()
    rows = {}
    for j in jobs:
        n = j['name']
        a, b = runs[('R4', n)], runs[('R5', n)]
        d4, d5 = out / 'dry' / ('R4_' + n), out / 'dry' / ('R5_' + n)
        cmpd = compare(d4, d5, base)
        t4 = apply(base + [(str(d4), str(d5))], '\n'.join(a['stderr_tail']).encode()).decode()
        term_eq = t4 == '\n'.join(b['stderr_tail'])
        evidence = a['exit'] == 0 and b['exit'] == 0 and cmpd['reports_nonempty']
        if evidence:
            verdict = 'PASS_PLAN_IDENTICAL' if cmpd['identical'] else 'FAIL'
        elif a['exit'] != 0 and b['exit'] != 0 and a['exit'] == b['exit'] and term_eq and cmpd['identical']:
            verdict = 'NO_EVIDENCE_EQUAL_EARLY_FAILURE'
        else:
            verdict = 'FAIL'
        rows[n] = dict(j, r4=a, r5=b, terminal_line_equal_after_T=term_eq, files=cmpd, counted=evidence, verdict=verdict)
    counted = [n for n, r in rows.items() if r['counted']]
    summ = {'specs': len(rows), 'counted_comparisons': len(counted),
            'pass_plan_identical': sorted(n for n in counted if rows[n]['verdict'] == 'PASS_PLAN_IDENTICAL'),
            'fail': sorted(n for n, r in rows.items() if r['verdict'] == 'FAIL'),
            'no_evidence_equal_early_failures': sorted(n for n, r in rows.items() if r['verdict'] == 'NO_EVIDENCE_EQUAL_EARLY_FAILURE')}
    summ['n_pass'] = len(summ['pass_plan_identical'])
    summ['n_no_evidence'] = len(summ['no_evidence_equal_early_failures'])
    summ['verdict_B0'] = 'PASS_PLAN_IDENTICAL' if not summ['fail'] and summ['n_pass'] == len(counted) else 'FAIL'
    rec = {'schema': 'B0_R5_VS_R4_C2V001', 'tool': [str(Path(__file__).resolve()), sha_f(__file__)], 'r5': [str(r5), r5_sha], 'r4': [str(R4[0]), R4[1]],
           'declared_map': [str(MAP), map_sha, len(base)], 'p128_registry': [str(P128), p128_sha], 'r4_b0_tool': [str(R4_B0[0]), R4_B0[1]],
           'r4_registry': [str(R4_REG[0]), R4_REG[1]], 'max_procs': maxp, 'rule': 'B0-EMPTY (A54): counted iff both exit 0 and both '
           'DRYRUN_REPORT.json and DRYRUN_PLAN.txt are non-empty; equal early failures listed as no evidence', 'rows': rows, 'summary': summ}
    with open(out / 'B0_R5_VS_R4_C2V001.json', 'x') as f:
        json.dump(rec, f, indent=1)
    print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 12 else len(v)) for k, v in summ.items()}, indent=1))


if __name__ == '__main__':
    main()
