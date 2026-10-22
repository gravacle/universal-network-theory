"""Root-verify (Claude2): own mutants of values writer v004, each run against Codex2's gate suite and the root
adversarial suite, to show which near-miss weakenings each suite detects. New copies only (exclusive create)."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ('MA1_handoff_sha_prefix_only',
     "if not is_pin(h) or h['sha256'] not in ACCEPTANCE_HANDOFFS:",
     "if not is_pin(h) or h['sha256'][:60] not in [x[:60] for x in ACCEPTANCE_HANDOFFS]:"),
    ('MA2_route_substring',
     "if rec.get('route') != NGC_ACCEPTANCE_ROUTE:",
     "if NGC_ACCEPTANCE_ROUTE not in str(rec.get('route')):"),
    ('MA3_gate_applied_to_phase2_rows',
     "and (kind != 'phase1_values' or (acc is not None and acc['counts_for_member_valid'] is True))",
     "and (acc is not None and acc['counts_for_member_valid'] is True)"),
    ('MA4_phase1_gate_only_excludes_incomplete',
     "and (kind != 'phase1_values' or (acc is not None and acc['counts_for_member_valid'] is True))",
     "and (kind != 'phase1_values' or (acc is not None and acc['reading'] != 'INCOMPLETE'))"),
    ('MA5_binding_by_result_sha_only',
     "if rec.get('result') != c['result_pin'] or rec.get('call_dir') != str(c['call']):",
     "if (rec.get('result') or {}).get('sha256') != c['result_pin']['sha256'] or rec.get('call_dir') != str(c['call']):"),
    ('MA6_schema_case_insensitive',
     "if not isinstance(rec, dict) or rec.get('schema') not in ACCEPTANCE_SCHEMAS:",
     "if not isinstance(rec, dict) or str(rec.get('schema')).strip().upper() not in ACCEPTANCE_SCHEMAS:"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    for k in ('module', 'gate', 'adversarial', 'work'):
        ap.add_argument('--' + k, required=True)
    a = ap.parse_args()
    root = Path(a.work)
    root.mkdir(parents=False, exist_ok=False)
    src = Path(a.module).read_text()
    rows = []
    for name, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            rows.append({'name': name, 'applied': False, 'site_count': n})
            continue
        d = root / name
        d.mkdir()
        p = d / 'mutant.py'
        with open(p, 'x') as f:
            f.write(src.replace(old, new, 1))
        row = {'name': name, 'applied': True, 'mutant': {'path': str(p), 'sha256': sha(p)}}
        for suite, script, res in (('codex2_gate', a.gate, 'RESULT_GATE_TESTS_CX2V001.json'),
                                   ('root_adversarial', a.adversarial, 'RESULT_ADVERSARIAL_C2.json')):
            run = subprocess.run([sys.executable, '-I', '-B', script, '--module', str(p), '--work', str(d / suite)],
                                 capture_output=True, text=True)
            rp = d / suite / res
            data = json.loads(rp.read_bytes()) if rp.exists() else {}
            fails = [t.get('name') for t in data.get('tests', []) if not t.get('ok')]
            row[suite] = {'exit': run.returncode, 'killed': run.returncode != 0 and bool(fails),
                          'n_fail': len(fails), 'fails': fails[:8],
                          'result': {'path': str(rp), 'sha256': sha(rp)} if rp.exists() else None,
                          'stderr_tail': run.stderr[-300:]}
        rows.append(row)
        print(name, 'codex2_gate', 'KILLED' if row['codex2_gate']['killed'] else 'SURVIVED',
              '| root_adversarial', 'KILLED' if row['root_adversarial']['killed'] else 'SURVIVED', flush=True)
    out = {'schema': 'C2_ROOTVERIFY_OWN_MUTANTS_V001',
           'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
           'module': {'path': a.module, 'sha256': sha(a.module)}, 'gate_sha256': sha(a.gate),
           'adversarial_sha256': sha(a.adversarial), 'script_sha256': sha(__file__), 'mutants': rows,
           'synthetic_only': True}
    with open(root / 'RESULT_OWN_MUTANTS_C2.json', 'x') as f:
        json.dump(out, f, indent=1)
        f.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
