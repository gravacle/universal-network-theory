"""Exclusive review successors and test retargeting; no scientific execution."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

H = Path(__file__).parent
inputs, outputs = [], []
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
def read(name, expected=None):
    p = H/name
    ppin = pin(p)
    assert expected is None or ppin['sha256'] == expected, ppin
    inputs.append(ppin)
    return p.read_text()
def write(name, source):
    ast.parse(source)
    p = H/name
    with p.open('x') as f:
        f.write(source)
    outputs.append(pin(p))
    return outputs[-1]

old_p = '2717daf3117f5f6860e8a585c77344261b62021379751e5b0f8608aa61bfd76c'
old_b = 'bd81967c0aaacf9cf161897e2fc07f9bc8552dbad1c333744abb8b1397cfe857'
old_g = '61055fff7e7974c5235fa648d883d7a51506158c0b16c47de8232e7253dedab7'
s = read('phase1_ngc_launch_cx3cw8_draft003.py', old_p)
old = '# Proposed A177 accounting; requires the root license.'
new = '# A177/A260 accounting, accepted in 0825; requires the root license.'
assert s.count(old) == 1
lp = write('phase1_ngc_launch_cx3cw8v001.py', s.replace(old, new))
s = read('roster_builder_c2v007_cx3cw8_draft003.py', old_b)
assert s.count(old_p) == 1
bp = write('roster_builder_c2v007_cx3cw8v001.py', s.replace(old_p, lp['sha256']))
s = read('g26_freeze_cx3cw8_draft003.py', old_g)
assert s.count(old_b) == 1 and s.count('roster_builder_c2v007_cx3cw8_draft003.py') == 1
gp = write('g26_freeze_cx3cw8v001.py',
           s.replace(old_b, bp['sha256']).replace('roster_builder_c2v007_cx3cw8_draft003.py',
                                                  'roster_builder_c2v007_cx3cw8v001.py'))
tests = {
    'test_selector_draft003.py': 'test_selector_cx3v001.py',
    'test_custody_draft002.py': 'test_custody_cx3v001.py',
    'test_p112_inherited_draft002.py': 'test_p112_inherited_cx3v001.py',
    'test_commit_cw8_draft002.py': 'test_commit_cx3v001.py',
    'test_inherited_cw8_draft003.py': 'test_inherited_cx3v001.py',
    'test_g26_cw8_draft003.py': 'test_g26_cx3v001.py',
    'test_combined_cw8_draft003.py': 'test_combined_cx3v001.py',
}
replacements = {
    'phase1_ngc_launch_cx3cw8_draft003.py': lp['path'].split('/')[-1],
    'roster_builder_c2v007_cx3cw8_draft003.py': bp['path'].split('/')[-1],
    'g26_freeze_cx3cw8_draft003.py': gp['path'].split('/')[-1],
    old_p: lp['sha256'], old_b: bp['sha256'], old_g: gp['sha256'],
    **tests,
}
for oldname, newname in tests.items():
    s = read(oldname)
    for old, new in replacements.items():
        s = s.replace(old, new)
    write(newname, s)
record = {'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
          'schema': 'CW8_REVIEW_PACKAGE_SOURCE_CX3V001', 'inputs': inputs, 'outputs': outputs,
          'semantic_changes_from_draft003': [],
          'changes': ['launcher: one RSS ruling comment', 'builder: exact launcher SHA',
                      'G26: exact builder path/SHA', 'tests: final source/dependency names and pins'],
          'tests_on_final_bytes': 'PENDING'}
p = H/'REVIEW_PACKAGE_SOURCE_CX3V001.json'
with p.open('x') as f:
    json.dump(record, f, indent=2, sort_keys=True); f.write('\n')
print(json.dumps({'package': pin(p), 'launcher': lp, 'builder': bp, 'g26': gp}))
