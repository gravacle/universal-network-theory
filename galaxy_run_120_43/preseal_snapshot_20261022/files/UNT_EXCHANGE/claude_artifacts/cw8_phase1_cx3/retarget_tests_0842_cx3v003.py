"""Exclusive test successors, source pins and preserved synthetic fixture paths."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
H = Path(__file__).parent
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
mapping = {}
for name in ('phase1_ngc_launch', 'roster_builder_c2v007', 'g26_freeze'):
    old, new = [H/(name+'_cx3cw8v00%d.py'%i) for i in (2,3)]
    mapping[pin(old)['sha256']] = pin(new)['sha256']
legacy = '/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/c2v004_dryrun_final'
preserved = str(H.parent/'g26_fixture_preserve_c2/c2v004_dryrun_final')
rows = []
for stem in ('selector','custody','p112_inherited','commit','inherited','g26','combined',
             'cli_and_custody','0835_F1_F3'):
    old = H/('test_'+stem+'_cx3v002.py')
    new = H/('test_'+stem+'_cx3v003.py')
    text = old.read_text()
    for a,b in mapping.items():
        text = text.replace(a,b)
    text = text.replace('cx3cw8v002','cx3cw8v003').replace('CX3CW8V002','CX3CW8V003')
    text = text.replace('_cx3v002.py','_cx3v003.py')
    text = text.replace(legacy, preserved)
    if stem == 'g26':
        # The preserved JSON still names its original scratch region. Remap
        # that path in the parsed synthetic fixture, never its pinned bytes.
        before = "record = json.loads(raw_pin(CALIBRATION, CALIBRATION_SHA))"
        assert text.count(before) == 1
        text = text.replace(before,
            "record = json.loads(raw_pin(CALIBRATION, CALIBRATION_SHA).decode().replace(\n"
            +repr(legacy)+", str(OLD)))")
    ast.parse(text)
    with new.open('x') as f:
        f.write(text)
    rows.append({'original': pin(old), 'successor': pin(new)})
doc = {'date_u': subprocess.check_output(['/bin/date','-u'],text=True).strip(),
       'schema':'CW8_TEST_RETARGET_0842_CX3V003', 'files':rows,
       'source_sha_mapping':mapping, 'synthetic_fixture_path_mapping':{legacy:preserved},
       'assertions_removed':False}
p=H/'TEST_RETARGET_0842_CX3V003.json'
with p.open('x') as f:
    json.dump(doc,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps(pin(p)))
