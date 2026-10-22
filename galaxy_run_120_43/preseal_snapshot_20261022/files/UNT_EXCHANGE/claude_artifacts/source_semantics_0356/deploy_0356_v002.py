"""0356 V002 deploy helper: exclusive-create copies (mode 0444) of the reviewed scratch V002 files into the EXISTING deliverable
directory (V001 files there are left untouched), an exclusive-create FILE_MANIFEST_0356_V002.json, then the builder literal scan over
every V002 deliverable including the manifest. Never overwrites, moves or deletes.
Usage: python3 -I -B deploy_0356_v002.py <scratch_v002_dir> <existing_out_dir>"""
import hashlib, json, os, subprocess, sys

W, OUT = sys.argv[1], sys.argv[2]
FILES = ['SOURCE_SEMANTICS_ADDENDUM_0356_V002.json', 'SOURCE_SEMANTICS_NOTES_0356_V002.md', 'PROBE_EVIDENCE_0356_V002.json',
         'CHANGES_V001_TO_V002.md', 'source_semantics_probe_0356_v002.py', 'build_addendum_0356_v002.py', 'deploy_0356_v002.py']
V001 = ['SOURCE_SEMANTICS_ADDENDUM_0356_V001.json', 'SOURCE_SEMANTICS_NOTES_0356_V001.md', 'PROBE_EVIDENCE_0356_V001.json',
        'source_semantics_probe_0356_v001.py', 'build_addendum_0356_v001.py', 'deploy_0356_v001.py', 'FILE_MANIFEST_0356_V001.json']
sha = lambda b: hashlib.sha256(b).hexdigest()
assert os.path.isdir(OUT)
before = {f: sha(open(os.path.join(OUT, f), 'rb').read()) for f in V001}
rows = []
for name in FILES:
    b = open(os.path.join(W, name), 'rb').read()
    p = os.path.join(OUT, name)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, 'wb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert open(p, 'rb').read() == b
    rows.append({'file': name, 'sha256': sha(b), 'bytes': len(b)})
ev = {r['file']: r['sha256'] for r in rows}
add = json.load(open(os.path.join(OUT, FILES[0])))
assert add['evidence']['probe_evidence']['sha256'] == ev['PROBE_EVIDENCE_0356_V002.json']
assert add['evidence']['probe_script']['sha256'] == ev['source_semantics_probe_0356_v002.py']
builder = os.path.join(OUT, 'build_addendum_0356_v002.py')
pre = subprocess.run([sys.executable, '-I', '-B', builder, 'scan'] + [os.path.join(OUT, f) for f in FILES], capture_output=True, text=True)
assert pre.returncode == 0, pre.stdout[-2000:]
man = {'schema': 'CLAUDE2_FILE_MANIFEST_V001', 'task': '0356 V002 (author CLAUDE2 helper 0356-A)', 'directory': OUT, 'files': rows,
       'addendum_evidence_pins_match': True,
       'literal_scan_of_listed_files': 'PASS (build_addendum_0356_v002.py scan; this manifest is scanned after creation by the deploy step)',
       'v001_retained_unchanged': {f: before[f] for f in V001},
       'inputs_pinned': add['binding_inputs'],
       'reproduce': 'python3 -I -B source_semantics_probe_0356_v002.py <new.json> reproduces PROBE_EVIDENCE_0356_V002.json byte-identically while the '
                    'name-only search roots are unchanged; python3 -I -B build_addendum_0356_v002.py build PROBE_EVIDENCE_0356_V002.json '
                    'source_semantics_probe_0356_v002.py <new.json> [V002 files to scan] reproduces the addendum byte-identically',
       'write_rule': 'O_EXCL creates, mode 0444; nothing overwritten, moved or deleted; nothing written under Universal Network Theory',
       'note': 'this manifest does not list itself; its sha256 is reported in the 0356 helper report'}
mp = os.path.join(OUT, 'FILE_MANIFEST_0356_V002.json')
fd = os.open(mp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
with os.fdopen(fd, 'w') as f:
    json.dump(man, f, indent=1); f.write('\n'); f.flush(); os.fsync(f.fileno())
post = subprocess.run([sys.executable, '-I', '-B', builder, 'scan', mp] + [os.path.join(OUT, f) for f in FILES], capture_output=True, text=True)
after = {f: sha(open(os.path.join(OUT, f), 'rb').read()) for f in V001}
print(json.dumps({'ok': post.returncode == 0 and after == before, 'files': rows, 'manifest_sha256': sha(open(mp, 'rb').read()),
                  'literal_scan_all_v002_including_manifest': json.loads(post.stdout)['literal_scan'], 'v001_unchanged': after == before}, indent=1))
