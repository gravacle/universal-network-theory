# Claude4 seal tools v003 (BUILD helper, continuation run 3): read every mutant run under mutants/final/ and write MUTATION_C4V003.json
# (exclusive create). A mutant is KILLED when its suite run has at least one NOT_OK case and its ENVIRONMENT case (the open V005 did not
# change during the run) is ok; SURVIVED when every case is ok; INVALID when the run has no results file, the environment case failed, the
# fence summary is missing or BLOCKED is not empty after the selftest, or the mutant folder's files are not the manifest's (sources and
# tests equal the dev bytes except the one mutated file, whose sha is the manifest's). Reads only; writes the one output file.
# usage: python3 -I -B run_fenced_c4st2.py analyze_mutants_final_c4v003.py OUT.json SET   (SET: the subfolder of mutants/final/, e.g. round2)
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
FINAL = HERE / 'mutants' / 'final' / sys.argv[2]
DEV = HERE / 'dev'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    out = Path(sys.argv[1])
    man = json.loads((FINAL / 'MUTANTS_FINAL_C4V003.json').read_bytes())
    dev_now = {n: sha(DEV / n) for n in man['dev_sha256']}
    rows, counts = [], {}
    for m in man['mutants']:
        d = FINAL / m['id']
        files_ok = all(sha(d / n) == (m['mutant_sha256'] if n == m['target'] else man['dev_sha256'][n]) for n in man['dev_sha256'])
        runs = sorted((d / 'tests').glob('run_*/TEST_RESULTS_C4V003.json'))
        log = (d / 'run.log').read_text() if (d / 'run.log').is_file() else ''
        summ = [ln for ln in log.splitlines() if ln.startswith('FENCE_C4ST2_SUMMARY ')]
        fence = json.loads(summ[-1].split(' ', 1)[1]) if summ else None
        row = {'id': m['id'], 'target': m['target'], 'old': m['old'], 'new': m['new'], 'mutant_sha256': m['mutant_sha256'], 'files_match_manifest': files_ok,
               'results': None, 'fence_blocked_after_selftest': None if fence is None else fence.get('blocked_after_selftest')}
        if len(runs) != 1:
            row['verdict'] = 'INVALID'
            row['why'] = '%d results files' % len(runs)
        else:
            res = json.loads(runs[0].read_bytes())
            bad = [r for r in res['results'] if not r['ok']]
            env = [r for r in res['results'] if r['tag'] == 'ENVIRONMENT']
            row['results'] = {'path': str(runs[0]), 'sha256': sha(runs[0]), 'passed': res['passed'], 'total': res['total'],
                              'tools_tested_sha256': res['tools']}
            row['failing_cases'] = [{'tool': r['tool'], 'tag': r['tag'], 'case': r['case'], 'codes': r['codes'][:6]} for r in bad]
            if not (files_ok and fence is not None and fence.get('blocked_after_selftest') == [] and len(env) == 1 and env[0]['ok']):
                row['verdict'] = 'INVALID'
                row['why'] = 'files %s, fence %s, environment %s' % (files_ok, None if fence is None else fence.get('blocked_after_selftest'),
                                                                    [e['ok'] for e in env])
            else:
                row['verdict'] = 'KILLED' if bad else 'SURVIVED'
        counts[row['verdict']] = counts.get(row['verdict'], 0) + 1
        rows.append(row)
    doc = {'schema': 'UNT_SEAL_TOOLS_V003_MUTATION_C4V003', 'tool': 'tools/analyze_mutants_final_c4v003.py', 'tool_sha256': sha(__file__),
           'generator': {'path': 'tools/make_mutants_final_c4v003.py', 'sha256': sha(HERE / 'tools/make_mutants_final_c4v003.py')},
           'runner': {'path': 'tools/run_one_mutant_c4v003.sh', 'sha256': sha(HERE / 'tools/run_one_mutant_c4v003.sh')}, 'set': str(FINAL),
           'manifest': {'path': str(FINAL / 'MUTANTS_FINAL_C4V003.json'), 'sha256': sha(FINAL / 'MUTANTS_FINAL_C4V003.json')},
           'dev_sha256_at_generation': man['dev_sha256'], 'dev_sha256_now': dev_now, 'dev_unchanged_since_generation': dev_now == man['dev_sha256'],
           'rule': 'KILLED = at least one NOT_OK case in the mutant\'s full fenced suite run, with the ENVIRONMENT case ok, BLOCKED [] after the '
                   'selftest and the mutant folder equal to the manifest; SURVIVED = every case ok; INVALID otherwise',
           'counts': counts, 'total': len(rows), 'all_killed': counts.get('KILLED', 0) == len(rows) and dev_now == man['dev_sha256'], 'mutants': rows}
    with open(out, 'x') as f:
        json.dump(doc, f, indent=1)
    print(json.dumps({'counts': counts, 'total': len(rows), 'all_killed': doc['all_killed']}))


if __name__ == '__main__':
    main()
