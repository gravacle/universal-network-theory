"""Own C1 draft-policy writer; calls only Codex3's read-only checker."""
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3')
CHECK = OUT / 'check_c1_h1_policy_cx3v003.py'
CHECK_SHA = '0ca88680366f4c9a7330021b4b359a4e29f1a1af01b54b471c9ec05ddbc6b7e4'
REPORT = OUT / 'CHECK_C1_H1_POLICY_CX3V003.json'
FINAL = OUT / 'DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V002.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def clean(obj):
    if isinstance(obj, dict):
        assert not ({'synthetic', 'synthetic_fixture'} & set(obj))
        for k, v in obj.items():
            clean(k)
            clean(v)
    elif isinstance(obj, list):
        for v in obj:
            clean(v)
    elif isinstance(obj, str):
        assert '<FILL' not in obj and 'TEMPLATE_NOT_A_REVIEW' not in obj


raw = CHECK.read_bytes()
assert sha(raw) == CHECK_SHA
ns = {'__file__': str(CHECK), '__name__': '_codex3_read_only_policy_checker'}
exec(compile(raw, str(CHECK), 'exec'), ns)
review = ns['checks']()
assert review['check_script'] == {'path': str(CHECK), 'sha256': CHECK_SHA}
assert review['ok'] is True and review['blocking_findings'] == []
assert [x['id'] for x in review['checks']] == ['C%02d' % i for i in range(1, 14)]
assert all(x['result'] == 'PASS' for x in review['checks'])
for ref in review['opened_file_pins']:
    assert sha(Path(ref['path']).read_bytes()) == ref['sha256']
review['date_u'] = subprocess.check_output(['/bin/date', '-u'], text=True).strip()
with REPORT.open('xb') as f:
    f.write(encoded(review))
review['check_record'] = {'path': str(REPORT), 'sha256': sha(REPORT.read_bytes())}
review['signing_tool'] = {'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())}
review['files_opened'] = sorted(set(review['files_opened']) | {str(REPORT), str(Path(__file__))})
review['signed_utc'] = subprocess.check_output(['/bin/date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], text=True).strip()
clean(review)
with FINAL.open('xb') as f:
    f.write(encoded(review))
saved = ns['strict'](FINAL.read_bytes())
assert saved == review
for p in (CHECK, FINAL):
    s = os.lstat(p)
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and s.st_size <= 8388608
    assert p.resolve() == p and all(not x.is_symlink() for x in (p, *p.parents))
print(json.dumps({'review': {'path': str(FINAL), 'sha256': sha(FINAL.read_bytes())},
                  'checker': saved['check_script'], 'checks': 13, 'blocking': 0,
                  'record': saved['check_record']}))
