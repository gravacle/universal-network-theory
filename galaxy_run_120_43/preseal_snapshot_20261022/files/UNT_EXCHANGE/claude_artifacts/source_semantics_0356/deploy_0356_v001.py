"""0356 deploy helper: exclusive-create copies (mode 0444) of the reviewed scratch files into a NEW deliverable directory, then an
exclusive-create FILE_MANIFEST. Never overwrites, moves or deletes. Usage: python3 -I -B deploy_0356_v001.py <scratch_work_dir> <new_out_dir>"""
import hashlib, json, os, sys

W, OUT = sys.argv[1], sys.argv[2]
FILES = [('final/SOURCE_SEMANTICS_ADDENDUM_0356_V001.json', 'SOURCE_SEMANTICS_ADDENDUM_0356_V001.json'),
         ('final/SOURCE_SEMANTICS_NOTES_0356_V001.md', 'SOURCE_SEMANTICS_NOTES_0356_V001.md'),
         ('final/PROBE_EVIDENCE_0356_V001.json', 'PROBE_EVIDENCE_0356_V001.json'),
         ('source_semantics_probe_0356_v001.py', 'source_semantics_probe_0356_v001.py'),
         ('build_addendum_0356_v001.py', 'build_addendum_0356_v001.py'),
         ('deploy_0356_v001.py', 'deploy_0356_v001.py')]
sha = lambda b: hashlib.sha256(b).hexdigest()
os.mkdir(OUT)  # fails if it exists
rows = []
for src, dst in FILES:
    b = open(os.path.join(W, src), 'rb').read()
    p = os.path.join(OUT, dst)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, 'wb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert open(p, 'rb').read() == b
    rows.append({'file': dst, 'sha256': sha(b), 'bytes': len(b)})
add = json.load(open(os.path.join(OUT, 'SOURCE_SEMANTICS_ADDENDUM_0356_V001.json')))
ev = {r['file']: r['sha256'] for r in rows}
assert add['evidence']['probe_evidence']['sha256'] == ev['PROBE_EVIDENCE_0356_V001.json']
assert add['evidence']['probe_script']['sha256'] == ev['source_semantics_probe_0356_v001.py']
man = {'schema': 'CLAUDE2_FILE_MANIFEST_V001', 'task': '0356 (author CLAUDE2 helper 0356-A)', 'directory': OUT, 'files': rows,
       'addendum_evidence_pins_match': True,
       'inputs_pinned': add['binding_inputs'],
       'reproduce': 'python3 -I -B source_semantics_probe_0356_v001.py <new.json> reproduces PROBE_EVIDENCE byte-identically; '
                    'python3 -I -B build_addendum_0356_v001.py PROBE_EVIDENCE_0356_V001.json source_semantics_probe_0356_v001.py <new.json> '
                    'reproduces the addendum byte-identically when run with the same evidence file name',
       'write_rule': 'O_EXCL creates, mode 0444; nothing overwritten, moved or deleted; nothing written under Universal Network Theory',
       'note': 'this manifest does not list itself; its sha256 is reported in the 0356 helper report'}
fd = os.open(os.path.join(OUT, 'FILE_MANIFEST_0356_V001.json'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
with os.fdopen(fd, 'w') as f:
    json.dump(man, f, indent=1); f.write('\n'); f.flush(); os.fsync(f.fileno())
print(json.dumps({'ok': True, 'files': rows, 'manifest_sha256': sha(open(os.path.join(OUT, 'FILE_MANIFEST_0356_V001.json'), 'rb').read())}, indent=1))
