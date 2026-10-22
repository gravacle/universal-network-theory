"""0361 deploy helper: creates the NEW deliverable directory, exclusive-create copies (mode 0444) of the reviewed scratch files, then an
exclusive-create FILE_MANIFEST_0361_V001.json. Never overwrites, moves or deletes.
Usage: python3 -I -B deploy_0361_v001.py <scratch_dir_d> <locator_script> <new_out_dir>"""
import hashlib, json, os, sys
D, LOC, OUT = sys.argv[1:4]
FILES = [(os.path.join(D, n), n) for n in ('SOURCE_DOCUMENT_DELTA_0361_V001.json', 'NOTES_0361_V001.md', 'SOURCE_DOCUMENT_EVIDENCE_0361_V001.json',
                                           'source_document_evidence_0361_v001.py', 'build_delta_0361_v001.py', 'deploy_0361_v001.py')] + [(LOC, 'pdf_page_locator_0361_v001.py')]
sha = lambda b: hashlib.sha256(b).hexdigest()
os.mkdir(OUT)
rows = []
for src, name in FILES:
    b = open(src, 'rb').read()
    fd = os.open(os.path.join(OUT, name), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, 'wb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert open(os.path.join(OUT, name), 'rb').read() == b
    rows.append({'file': name, 'sha256': sha(b), 'bytes': len(b)})
ev = {r['file']: r['sha256'] for r in rows}
delta = json.load(open(os.path.join(OUT, 'SOURCE_DOCUMENT_DELTA_0361_V001.json')))
assert delta['evidence']['evidence_json']['sha256'] == ev['SOURCE_DOCUMENT_EVIDENCE_0361_V001.json']
assert delta['evidence']['evidence_script']['sha256'] == ev['source_document_evidence_0361_v001.py']
man = {'schema': 'CLAUDE2_FILE_MANIFEST_V001', 'task': '0361 (author CLAUDE2 helper 0361-A)', 'directory': OUT, 'files': rows,
       'delta_evidence_pins_match': True,
       'primary_document': {'path': delta['sparc_paper']['path'], 'sha256': delta['sparc_paper']['sha256']},
       'reproduce': 'python3 -I -B source_document_evidence_0361_v001.py <new.json> reproduces SOURCE_DOCUMENT_EVIDENCE byte-identically while the '
                    'filename-search root is unchanged; python3 -I -B build_delta_0361_v001.py SOURCE_DOCUMENT_EVIDENCE_0361_V001.json '
                    'source_document_evidence_0361_v001.py <new.json> reproduces the delta byte-identically',
       'helper_note': 'pdf_page_locator_0361_v001.py was the first-pass page locator (prints per-page counts only); the evidence script supersedes it',
       'write_rule': 'O_EXCL creates, mode 0444; nothing overwritten, moved or deleted; nothing written under Universal Network Theory',
       'note': 'this manifest does not list itself; its sha256 is reported in the 0361 helper report'}
fd = os.open(os.path.join(OUT, 'FILE_MANIFEST_0361_V001.json'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
with os.fdopen(fd, 'w') as f:
    json.dump(man, f, indent=1); f.write('\n'); f.flush(); os.fsync(f.fileno())
print(json.dumps({'ok': True, 'files': rows, 'manifest_sha256': sha(open(os.path.join(OUT, 'FILE_MANIFEST_0361_V001.json'), 'rb').read())}, indent=1))
