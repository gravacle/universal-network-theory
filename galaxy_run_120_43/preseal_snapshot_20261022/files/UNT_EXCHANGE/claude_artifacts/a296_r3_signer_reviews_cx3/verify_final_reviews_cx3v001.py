"""Read back final signed bytes and repeat the optional stage-gate dry check."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/a296_r3_signer_reviews_cx3')
SCRIPT = OUT / 'review_saved_rows_cx3v001.py'
SCRIPT_SHA = '5df410950fcb205ff42892bc0c9ddbd4bf483c62bcc42f298f1fccc3f1ae2c4a'
raw = SCRIPT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == SCRIPT_SHA
ns = {'__file__': str(SCRIPT), '__name__': '_codex3_review_helpers_no_main'}
exec(compile(raw, str(SCRIPT), 'exec'), ns)
dispatch = ns['read_exact'](ns['DISPATCH'], ns['DISPATCH_SHA']).decode()
pins = dict(re.findall(r'`(/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/[^`\n]+)` — `([0-9a-f]{64})`', dispatch))
for path, expected in pins.items():
    ns['read_exact'](path, expected)
hp = OUT / 'HANDOFF_CX3V001.json'
handoff = ns['strict'](hp.read_bytes())
checks = ns['strict'](ns['read_exact'](handoff['checks']['path'], handoff['checks']['sha256']))
assert checks['verdict'] == 'PASS' and not checks['changed_inputs']
results = []
for entry in handoff['reviews']:
    rv = ns['strict'](ns['read_exact'](entry['path'], entry['sha256']))
    row = entry['row']
    assert rv['row'] == row and rv['verdict'] == entry['verdict'] == 'APPROVED'
    assert rv.get('test_fixture_only') is not True
    assert rv['evidence']['checks'] == handoff['checks']
    stage = ns['strict'](ns['read_exact'](ns['named'](pins, f'STAGE_ONLY_ROW{row}_CX2V003.json')))
    new = ns['strict'](ns['read_exact'](ns['named'](pins, f'EPS_ROW{row}_CX2V001.json')))
    cases = ns['gate_controls'](rv, stage, new, pins)
    assert all(c['pass'] for c in cases)
    results.append({'row': row, 'review': entry, 'gate_cases': cases})
record = {'schema': 'CX3_A296_R3_FINAL_BYTE_CHECK_V001',
    'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
    'status': 'TESTED', 'verdict': 'PASS', 'rows': results,
    'scope': 'Final review bytes, including evidence fields, pass the extracted stage gate. The 14 negative controls per row refuse. These are local dry checks with test approval arguments; no root approval, producer execution or adapt call is performed.',
    'handoff': {'path': str(hp), 'sha256': hashlib.sha256(hp.read_bytes()).hexdigest()},
    'helper_source': {'path': str(SCRIPT), 'sha256': SCRIPT_SHA},
    'verifier': {'path': str(Path(__file__)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
dest = OUT / 'FINAL_BYTE_CHECK_CX3V001.json'
with dest.open('xb') as f:
    f.write(ns['serialized'](record))
print(json.dumps({'verdict': 'PASS', 'cases': sum(len(r['gate_cases']) for r in results),
                  'path': str(dest), 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()}))
