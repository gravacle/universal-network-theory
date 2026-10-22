"""Static text/byte audit only. Never executes a reviewed command or module."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).parent
BASE = HERE.parent / 'verdict_day_runbook_c3'
RUN = BASE / 'RUNBOOK_EXEC_C3V001.md'
XREF = BASE / 'XREF_C3V001.json'
raw = RUN.read_bytes()
run_lines = raw.decode().splitlines()
xraw = XREF.read_bytes()
x = json.loads(xraw)
checks = []
def check(name, ok, detail=None):
    checks.append({'name': name, 'pass': bool(ok), 'detail': detail})
def sha(b):
    return hashlib.sha256(b).hexdigest()
pins = {str(RUN): sha(raw), str(XREF): sha(xraw)}
check('runbook_pinned_in_xref', sha(raw) == x['runbook_sha256'])
sources = {}
for key, rec in x['sources'].items():
    # Only the four explicit command-source files; no paths from their contents.
    data = Path(rec['path']).read_bytes()
    pins[rec['path']] = sha(data)
    check('source_pin_' + key, sha(data) == rec['sha256'])
    sources[key] = data.decode().splitlines()

fenced = {}
blocks = collections.Counter()
inside = False
heading = None
for lineno, line in enumerate(run_lines, 1):
    if not inside and line.startswith('## '):
        heading = line[3:].split(' ', 1)[0].removesuffix('.')
    if line == '```bash':
        assert not inside
        inside = True
        blocks[heading] += 1
    elif inside and line == '```':
        inside = False
    elif inside:
        fenced[lineno] = {'text': line, 'block': heading}
check('closed_bash_fences', not inside)
check('xref_has_no_duplicate_line_numbers', len({r['line'] for r in x['lines']}) == len(x['lines']))
check('xref_complete_exact_fence_coverage', set(fenced) == {r['line'] for r in x['lines']}, {'fence_lines': len(fenced), 'xref_rows': len(x['lines'])})

other = []
qos_prefixes = ('/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 ', '/usr/sbin/taskpolicy -b ')
for r in x['lines']:
    n = r['line']
    check('xref_text_and_block_' + str(n), fenced.get(n) == {'text': r['text'], 'block': r['block']})
    if r['kind'] in ('VERBATIM', 'REDERIVED', 'QOS_DROPPED'):
        pattern = r'([JMSV]):L(\d+) minus its taskpolicy/nice prefix \(A274 item 1\)' if r['kind'] == 'QOS_DROPPED' else r'([JMSV]):L(\d+)'
        m = re.fullmatch(pattern, r['ref'])
        check('exact_source_reference_' + str(n), m is not None, r['ref'])
        if m:
            origin = sources[m[1]][int(m[2]) - 1]
            if r['kind'] == 'QOS_DROPPED':
                prefix = next((p for p in qos_prefixes if origin.startswith(p)), None)
                check('qos_allowed_prefix_' + str(n), prefix is not None)
                if prefix:
                    origin = origin[len(prefix):]
                check('qos_python_remainder_' + str(n), origin.startswith('"$PY"'))
            check('source_line_equality_' + str(n), origin == r['text'])
    else:
        other.append(r)
        if r['kind'] == 'DERIVED':
            check('derived_flag_' + str(n), re.match(r'D[1-7](?::|\s|$)', r['ref']) is not None)
        elif r['kind'] == 'COMMENT':
            check('comment_only_' + str(n), r['text'].startswith('#'))
        elif r['kind'] not in ('FIXED', 'PASTE', 'PASTE_GUARD'):
            check('recognized_kind_' + str(n), False, r['kind'])

date_u = subprocess.check_output(['/bin/date', '-u'], env={**os.environ, 'LC_ALL': 'C'}, text=True).strip()
result = {
    'schema': 'RUNBOOK_STATIC_XREF_REVIEW_CX2V002', 'date_u': date_u,
    'status': 'PASS' if all(c['pass'] for c in checks) else 'FAIL',
    'scope': 'TESTED byte pins, fenced-code coverage, exact source equality and allowed QoS prefix deletion; FORMAL semantic review is separate; actual execution UNTESTED',
    'runtime': 'isolated no-bytecode stdlib, single-thread variables; nice unavailable (sandbox); 0514 waiver',
    'checks_passed': sum(c['pass'] for c in checks), 'checks_total': len(checks),
    'bash_fences': dict(blocks), 'executable_blocks_excluding_P0': sum(blocks.values()) - blocks.get('P0', 0),
    'xref_kinds': dict(collections.Counter(r['kind'] for r in x['lines'])),
    'source_pins': pins, 'audit_script_sha256': sha(Path(__file__).read_bytes()),
    'checks': checks, 'semantic_review_inventory': other,
    'execution_limit': 'No reviewed code, generator, shell fragment, fixture or project import executed. /bin/date only metadata child. No path from source contents dereferenced.'
}
out = HERE / 'XREF_STATIC_RESULTS_CX2V002.json'
with out.open('x') as f:
    json.dump(result, f, indent=2, sort_keys=True)
    f.write('\n')
print(json.dumps({k: result[k] for k in ('status', 'checks_passed', 'checks_total', 'executable_blocks_excluding_P0', 'xref_kinds')}, sort_keys=True))
print('RESULT_SHA256 ' + sha(out.read_bytes()))
for c in checks:
    if not c['pass']:
        print(json.dumps(c))
