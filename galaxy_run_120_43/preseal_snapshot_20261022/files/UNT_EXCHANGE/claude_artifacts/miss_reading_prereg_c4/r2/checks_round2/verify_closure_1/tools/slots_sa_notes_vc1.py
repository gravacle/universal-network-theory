# verify_closure_1: print only the structural-assumption notes (SA-REACH-01, SA-BH-01) of the target-free slots V003 file.
# Reads one pinned file; prints only the notes_block_for_manifest.structural_assumptions subtree and the top-level key list.
import hashlib, json, sys

PATH = sys.argv[1]
PIN = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
raw = open(PATH, 'rb').read()
sha = hashlib.sha256(raw).hexdigest()
if sha != PIN:
    raise SystemExit('SHA_MISMATCH ' + sha)


def no_dup(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise SystemExit('DUPLICATE_KEY ' + k)
        d[k] = v
    return d


doc = json.loads(raw.decode('utf-8'), object_pairs_hook=no_dup)
print('sha256', sha)
print('top-level keys', sorted(doc.keys()))
nb = doc.get('notes_block_for_manifest', {})
print('notes_block_for_manifest keys', sorted(nb.keys()) if isinstance(nb, dict) else type(nb).__name__)
sa = nb.get('structural_assumptions') if isinstance(nb, dict) else None
print(json.dumps(sa, indent=1, ensure_ascii=False))
