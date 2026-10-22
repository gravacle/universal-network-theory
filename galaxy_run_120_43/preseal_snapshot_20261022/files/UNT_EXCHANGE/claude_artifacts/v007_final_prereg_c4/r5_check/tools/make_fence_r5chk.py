# make_fence_r5chk.py -- builds tools/fence_c4v002.py from the exact copy tools/fence_c4v001.py (f813c430) by anchored edits.
# usage: python3 -I -B make_fence_r5chk.py [--dry-run]
# Each anchor must occur exactly once in v001; the result is written by exclusive create (refuses if it exists).
# Only two READ-ONLY exceptions are added (task rule 5): (a) uvt_*.py source modules outside every runs_ext tree;
# (b) the CLAUDE2 V00*_ADDENDUM*.md root decision records. Every other block is unchanged.
import hashlib, os, sys
T = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(T, 'fence_c4v001.py')
DST = os.path.join(T, 'fence_c4v002.py')
b = open(SRC, 'rb').read()
assert hashlib.sha256(b).hexdigest() == 'f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0', 'v001 copy sha'
s = b.decode('utf-8')
EDITS = [
 ("import os, sys\n",
  "# v002 (r5_check helper, Claude4; task rule 5): ONLY two READ-ONLY exceptions are added to v001 (f813c430):\n"
  "#  (a) a uvt_*.py SOURCE module outside every runs_ext tree may be read: in both the literal and the real path the last\n"
  "#      component (casefolded) starts 'uvt_' and ends '.py', no other component starts 'uvt_', and no component is 'runs_ext';\n"
  "#  (b) the root decision records CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md may be read:\n"
  "#      literal and real path directly in the CLAUDE2 control folder, basename matching that pattern (decision records,\n"
  "#      not data; seal rehearsal D-11). Scratch copies inside this folder were already readable under v001's in-folder rule.\n"
  "#  An exception applies only to an open with no write flag, and lifts only its own rule (UVT component for (a), NGC3198\n"
  "#  data for (b)); the run-tree, C5H-name and target-word rules and every other v001 block are unchanged.\n"
  "import fnmatch, os, sys\n"),
 ("TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n",
  "TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n"
  "V002_CLAUDE2_CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'\n"
  "V002_CLAUDE2_REAL = os.path.realpath(V002_CLAUDE2_CTRL)\n"
  "V002_ADDENDUM_PATTERN = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'\n"),
 ("def _forbidden_read(lit, real):\n"
  "    if any(_under(p, r) for p in (lit, real) for r in RUNS_EXT):\n"
  "        return 'real run tree'\n"
  "    if _under(real, REVIEW):\n"
  "        return None  # my own synthetic look-alikes may carry protected-looking names\n"
  "    for p in (lit, real):\n"
  "        low = p.casefold()\n"
  "        if any(x.startswith('uvt_') for x in low.split(os.sep)):\n"
  "            return 'UVT component'\n",
  "def _v002_uvt_source(p):\n"
  "    \"\"\"v002 (a): p names a uvt_*.py source module outside every runs_ext tree.\"\"\"\n"
  "    comps = p.casefold().split(os.sep)\n"
  "    return (comps[-1].startswith('uvt_') and comps[-1].endswith('.py')\n"
  "            and not any(c.startswith('uvt_') for c in comps[:-1]) and 'runs_ext' not in comps)\n"
  "\n"
  "\n"
  "def _v002_addendum(p):\n"
  "    \"\"\"v002 (b): p names a root decision addendum directly in the CLAUDE2 control folder.\"\"\"\n"
  "    return (os.path.dirname(p) in (V002_CLAUDE2_CTRL, V002_CLAUDE2_REAL)\n"
  "            and fnmatch.fnmatchcase(os.path.basename(p), V002_ADDENDUM_PATTERN))\n"
  "\n"
  "\n"
  "def _forbidden_read(lit, real, writing=True):\n"
  "    if any(_under(p, r) for p in (lit, real) for r in RUNS_EXT):\n"
  "        return 'real run tree'\n"
  "    if _under(real, REVIEW):\n"
  "        return None  # my own synthetic look-alikes may carry protected-looking names\n"
  "    ex_a = (not writing) and _v002_uvt_source(lit) and _v002_uvt_source(real)      # v002 (a), reads only\n"
  "    ex_b = (not writing) and _v002_addendum(lit) and _v002_addendum(real)          # v002 (b), reads only\n"
  "    for p in (lit, real):\n"
  "        low = p.casefold()\n"
  "        if any(x.startswith('uvt_') for x in low.split(os.sep)) and not ex_a:\n"
  "            return 'UVT component'\n"),
 ("        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):\n",
  "        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not ex_b:\n"),
 ("        why = _forbidden_read(lit, real)\n",
  "        why = _forbidden_read(lit, real, _writing(args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None))\n"),
]
for old, new in EDITS:
    n = s.count(old)
    assert n == 1, 'anchor count %d for %r' % (n, old[:60])
    s = s.replace(old, new)
s += '''

def selftest_v002():
    """v002 exceptions as PATH PREDICATES only (no protected file is opened). Returns [(name, ok)]."""
    C2 = V002_CLAUDE2_CTRL
    X = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/r5chk_fence_probe_dir'
    AD = C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
    cases = [
        ('a_read_uvt_py_allowed', X + '/uvt_probe.py', False, None),
        ('a_write_uvt_py_refused', X + '/uvt_probe.py', True, 'UVT component'),
        ('a_uvt_dir_refused', X + '/UVT_Z2_PROBE_RUN/uvt_probe.py', False, 'UVT component'),
        ('a_uvt_dir_plain_file_refused', X + '/UVT_Z2_PROBE_RUN/result.json', False, 'UVT component'),
        ('a_uvt_non_py_refused', X + '/uvt_probe.json', False, 'UVT component'),
        ('a_uvt_pyc_refused', X + '/uvt_probe.pyc', False, 'UVT component'),
        ('a_runs_ext_component_refused', X + '/runs_ext/uvt_probe.py', False, 'UVT component'),
        ('a_real_runs_ext_root_refused', RUNS_EXT[1] + '/uvt_probe.py', False, 'real run tree'),
        ('a_c5h_name_refused', X + '/KMAX_A2F10_C5H_RUN_V001/uvt_probe.py', False, 'C5H name'),
        ('a_target_word_refused', X + '/uvt_rotmod_probe.py', False, 'target word'),
        ('b_v005_addendum_read_allowed', AD, False, None),
        ('b_v004_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md', False, None),
        ('b_v002_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V002_ADDENDUM.md', False, None),
        ('b_frozen_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', False, None),
        ('b_addendum_write_refused', AD, True, 'NGC3198 data'),
        ('b_v001_decisions_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md', False, 'NGC3198 data'),
        ('b_addendum_in_subfolder_refused', C2 + '/specs/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', False, 'NGC3198 data'),
        ('b_addendum_name_elsewhere_refused', X + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', False, 'NGC3198 data'),
        ('b_addendum_json_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.json', False, 'NGC3198 data'),
        ('b_v010_glob_case_refused', C2 + '/root_decisions_ngc3198_construction_2026-10-17_v005_addendum.md', False, 'NGC3198 data'),
        ('b_target_word_still_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_rotmod.md', False, 'target word'),
        ('other_ngc3198_table_refused', X + '/NGC3198_probe_table.dat', False, 'NGC3198 data'),
        ('other_ngc3198_py_allowed_as_v001', X + '/ngc3198_probe_source.py', False, None),
        ('in_folder_copy_allowed_as_v001', REVIEW + '/scratch/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', False, None),
    ]
    out = []
    for name, p, writing, want in cases:
        lit = os.path.abspath(p)
        real = os.path.realpath(lit)
        out.append((name, _forbidden_read(lit, real, writing) == want))
    return out
'''
r = s.encode('utf-8')
sha = hashlib.sha256(r).hexdigest()
if '--dry-run' in sys.argv:
    print('DRY_RUN fence_c4v002 sha256', sha, len(r), 'bytes')
else:
    with open(DST, 'xb') as f:
        f.write(r)
    print('WROTE', DST, 'sha256', hashlib.sha256(open(DST, 'rb').read()).hexdigest(), len(r), 'bytes')
