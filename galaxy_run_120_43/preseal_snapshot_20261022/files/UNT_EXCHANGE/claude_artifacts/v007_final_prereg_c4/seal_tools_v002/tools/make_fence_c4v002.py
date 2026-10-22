# Claude4 seal tools v002: build tools/fence_c4v002.py from the exact copy tools/fence_c4v001.py (f813c430) by exact text
# replacements. Each replacement must match exactly once, or the script exits 1 and writes nothing. The output is created
# exclusively (mode 'x'). Only the two read-only exceptions of task rule 5 change; every other block stays byte-identical.
# usage: python3 -I -B make_fence_c4v002.py TOOLS_DIR [--dry-run OUT]
import hashlib, sys
from pathlib import Path

TOOLS = Path(sys.argv[1])
V1 = TOOLS / 'fence_c4v001.py'
V1_SHA = 'f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0'
raw = V1.read_bytes()
if hashlib.sha256(raw).hexdigest() != V1_SHA:
    print('REFUSED: fence_c4v001.py is not f813c430')
    raise SystemExit(1)
text = raw.decode('utf-8')

REPL = [
    # 1. header: say what v002 is (comment lines only)
    ("# Every open of a path inside LOOKALIKES is logged with a stack tag: is it the guard's own marker read, or a body read?\n"
     "import os, sys\n",
     "# Every open of a path inside LOOKALIKES is logged with a stack tag: is it the guard's own marker read, or a body read?\n"
     "# v002 (Claude4 seal tools v002, task rule 5): the ONLY change from fence_c4v001 (f813c430) is two READ-ONLY exceptions\n"
     "# to the open rules (writes outside this folder stay refused for every path):\n"
     "#  (a) a uvt_*.py SOURCE module (basename starts with lowercase 'uvt_' and ends with '.py'; no directory component starts\n"
     "#      with uvt_, any case) outside both runs_ext roots; a .pyc, a UVT_* directory or anything under runs_ext stays refused;\n"
     "#  (b) the root decision files CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md (directory exactly the\n"
     "#      CLAUDE2 control folder, literal and resolved path both), which are decision records, not data (rehearsal D-11).\n"
     "#      Scratch copies of them inside this folder were already readable (this folder is exempt), unchanged.\n"
     "import fnmatch, os, sys\n"),
    # 2. constants for the exceptions (after TARGET_WORDS)
    ("TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n",
     "TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n"
     "CTRL_C2 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'   # v002 (b)\n"
     "CTRL_C2_DIRS = (CTRL_C2, os.path.realpath(CTRL_C2))                                                                         # v002 (b)\n"
     "ROOT_DECISION_GLOB = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'                                    # v002 (b)\n"),
    # 3. the two helper predicates, before _forbidden_read
    ("def _forbidden_read(lit, real):\n",
     "def _uvt_source_module(p):\n"
     "    \"\"\"v002 (a): True only for <dirs>/uvt_*.py where the basename starts with lowercase 'uvt_' and ends with '.py' and no\n"
     "    directory component starts with uvt_ (any case).  The runs_ext test in _forbidden_read runs first and is unchanged.\"\"\"\n"
     "    parts = p.split(os.sep)\n"
     "    base = parts[-1]\n"
     "    if not (base.startswith('uvt_') and base.endswith('.py')):\n"
     "        return False\n"
     "    return not any(x.casefold().startswith('uvt_') for x in parts[:-1])\n"
     "\n"
     "\n"
     "def _root_decision_addendum(p):\n"
     "    \"\"\"v002 (b): True only for CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md (exact folder).\"\"\"\n"
     "    d, b = os.path.split(p)\n"
     "    return d in CTRL_C2_DIRS and fnmatch.fnmatchcase(b, ROOT_DECISION_GLOB)\n"
     "\n"
     "\n"
     "def _forbidden_read(lit, real):\n"),
    # 4. exception (a) in the UVT rule
    ("        if any(x.startswith('uvt_') for x in low.split(os.sep)):\n"
     "            return 'UVT component'\n",
     "        if any(x.startswith('uvt_') for x in low.split(os.sep)) and not _uvt_source_module(p):   # v002 (a)\n"
     "            return 'UVT component'\n"),
    # 5. exception (b) in the NGC3198 rule
    ("        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):\n"
     "            return 'NGC3198 data'\n",
     "        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not _root_decision_addendum(p):   # v002 (b)\n"
     "            return 'NGC3198 data'\n"),
]
out = text
for old, new in REPL:
    n = out.count(old)
    if n != 1:
        print('REFUSED: a replacement matched %d times: %r' % (n, old[:80]))
        raise SystemExit(1)
    out = out.replace(old, new)
compile(out, 'fence_c4v002.py', 'exec')
if len(sys.argv) > 3 and sys.argv[2] == '--dry-run':
    with open(sys.argv[3], 'x') as f:
        f.write(out)
    print('DRY', hashlib.sha256(out.encode('utf-8')).hexdigest(), sys.argv[3])
    raise SystemExit(0)
dst = TOOLS / 'fence_c4v002.py'
with open(dst, 'x') as f:
    f.write(out)
print('WROTE', hashlib.sha256(dst.read_bytes()).hexdigest(), dst)
