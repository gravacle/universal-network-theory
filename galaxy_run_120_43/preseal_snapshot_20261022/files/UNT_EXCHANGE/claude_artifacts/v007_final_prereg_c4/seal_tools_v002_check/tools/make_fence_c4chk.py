# Claude4 helper (seal tools v002 independent check): build tools/fence_c4v002.py from the exact fence_c4v001.py (f813c430)
# changing ONLY two read-only exceptions (task rule 5): (a) uvt_*.py source modules outside every runs_ext tree; (b) the CLAUDE2
# root decision addenda ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md. Every replacement must match exactly
# once, else exit 1 and nothing is written. Writes with exclusive create.
import hashlib, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = HERE / 'fence_c4v001.py'
DST = HERE / 'fence_c4v002.py'
raw = SRC.read_bytes()
if hashlib.sha256(raw).hexdigest() != 'f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0':
    print('SOURCE_SHA_MISMATCH'); sys.exit(1)
t = raw.decode('utf-8')
REPL = [
    ('import os, sys\n',
     '# v002 (seal tools v002 check, Claude4 helper; task rule 5): the ONLY change from f813c430 is two READ-ONLY exceptions to\n'
     '# the open rules; every write outside this folder stays refused for every path, and every other block is unchanged:\n'
     '#  (a) a uvt_*.py SOURCE module: basename starts with lowercase uvt_ and ends with .py, no directory component starts with\n'
     '#      uvt_ (any case); it is still refused under either runs_ext root (that test runs first), and by the C5H, target-word\n'
     '#      and NGC3198 rules;\n'
     '#  (b) the root decision files ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md directly in the CLAUDE2\n'
     '#      control folder (literal and resolved path both); they are decision records, not data (rehearsal D-11). Only the\n'
     '#      NGC3198 rule is lifted for them. Scratch copies inside this folder were already readable (unchanged).\n'
     'import fnmatch, os, sys\n'),
    ("TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n",
     "TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n"
     "CTRL_C2 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'   # v002 (b)\n"
     "ROOT_DECISION_GLOB = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'                                    # v002 (b)\n"),
    ('def _forbidden_read(lit, real):\n',
     'def _uvt_source_module(p):\n'
     '    """v002 (a): <dirs>/uvt_*.py with a lowercase uvt_ basename, a .py suffix and no uvt_* directory component (any case)."""\n'
     '    parts = p.split(os.sep)\n'
     '    if not (parts[-1].startswith(\'uvt_\') and parts[-1].endswith(\'.py\')):\n'
     '        return False\n'
     '    return not any(x.casefold().startswith(\'uvt_\') for x in parts[:-1])\n'
     '\n'
     '\n'
     'def _root_decision_file(lit, real):\n'
     '    """v002 (b): both the literal and the resolved path are CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md."""\n'
     '    for p in (lit, real):\n'
     '        d, b = os.path.split(p)\n'
     '        if d != CTRL_C2 or not fnmatch.fnmatchcase(b, ROOT_DECISION_GLOB):\n'
     '            return False\n'
     '    return True\n'
     '\n'
     '\n'
     'def _forbidden_read(lit, real):\n'),
    ("        if any(x.startswith('uvt_') for x in low.split(os.sep)):\n",
     "        if any(x.startswith('uvt_') for x in low.split(os.sep)) and not (_uvt_source_module(lit) and _uvt_source_module(real)):   # v002 (a)\n"),
    ("        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):\n",
     "        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not _root_decision_file(lit, real):   # v002 (b)\n"),
]
for old, new in REPL:
    n = t.count(old)
    if n != 1:
        print('REPLACEMENT_COUNT', n, repr(old[:60])); sys.exit(1)
    t = t.replace(old, new)
if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
    print('DRY_RUN_OK', hashlib.sha256(t.encode()).hexdigest()); sys.exit(0)
with open(DST, 'x', encoding='utf-8') as f:
    f.write(t)
print('WROTE', DST, hashlib.sha256(DST.read_bytes()).hexdigest())
