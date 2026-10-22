# Claude4 r5 helper: derive fence_c4v002.py from the exact copy fence_c4v001.py (f813c430) by five anchored edits.
# ONLY two READ-ONLY exceptions are added (task rule 5): (a) uvt_*.py source modules outside every runs_ext tree; (b) the root
# decision addenda in the CLAUDE2 control folder. Every other block of v001 is kept byte-identical. Exclusive create; prints the diff.
import difflib, hashlib, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE / 'fence_c4v001.py'
V2 = HERE / 'fence_c4v002.py'
DIFF = HERE.parent / 'out' / 'FENCE_C4V001_TO_C4V002.diff'
V1_SHA = 'f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0'

src = V1.read_bytes()
assert hashlib.sha256(src).hexdigest() == V1_SHA, 'fence_c4v001 copy is not f813c430'
t = src.decode()

EDITS = [
    # 1. header note + the fnmatch import (the only new import)
    ("import os, sys\n",
     "# v002 (Claude4 r5 helper; prereg r5 / V007 case block): ONLY two READ-ONLY exceptions are added; every other block is unchanged.\n"
     "#  (a) uvt_*.py SOURCE modules outside every runs_ext tree: in both the literal and the real path the basename (casefolded)\n"
     "#      starts 'uvt_' and ends '.py', no directory component starts 'uvt_', and no component is 'runs_ext';\n"
     "#  (b) the root decision addenda CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md (decision records,\n"
     "#      not data; seal rehearsal D-11), literal and real path directly in the CLAUDE2 control folder. Scratch copies of them\n"
     "#      inside this folder were already readable under v001's in-folder rule, so they need no change.\n"
     "#  Both apply only to an open WITHOUT a write flag, and each lifts only its own rule: the real-run-tree, C5H-name and\n"
     "#  target-word rules still apply to the same path. Writes outside this folder stay refused by the unchanged write rule.\n"
     "import fnmatch, os, sys\n"),
    # 2. constants for (b)
    ("TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n",
     "TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')\n"
     "CLAUDE2_CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'  # v002 (b)\n"
     "_CLAUDE2_REAL = os.path.realpath(CLAUDE2_CTRL)                                                                              # v002 (b)\n"
     "ADDENDUM_GLOB = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'                                          # v002 (b)\n"),
    # 3. the two exception predicates, placed just before _forbidden_read
    ("def _forbidden_read(lit, real):\n",
     "def _uvt_source_exception(lit, real):\n"
     "    \"\"\"v002 (a): a uvt_*.py source module outside every runs_ext tree (applied to reads only).\"\"\"\n"
     "    for p in (lit, real):\n"
     "        comps = p.casefold().split(os.sep)\n"
     "        if not (comps[-1].startswith('uvt_') and comps[-1].endswith('.py')):\n"
     "            return False\n"
     "        if any(x.startswith('uvt_') for x in comps[:-1]) or 'runs_ext' in comps:\n"
     "            return False\n"
     "    return True\n"
     "\n"
     "\n"
     "def _addendum_exception(lit, real):\n"
     "    \"\"\"v002 (b): a root decision addendum directly in the CLAUDE2 control folder (applied to reads only).\"\"\"\n"
     "    return (os.path.dirname(lit) in (CLAUDE2_CTRL, _CLAUDE2_REAL) and os.path.dirname(real) == _CLAUDE2_REAL\n"
     "            and fnmatch.fnmatchcase(os.path.basename(lit), ADDENDUM_GLOB)\n"
     "            and fnmatch.fnmatchcase(os.path.basename(real), ADDENDUM_GLOB))\n"
     "\n"
     "\n"
     "def _forbidden_read(lit, real, writing=True):\n"),
    # 4. the rule loop: each exception lifts only its own rule
    ("    for p in (lit, real):\n"
     "        low = p.casefold()\n"
     "        if any(x.startswith('uvt_') for x in low.split(os.sep)):\n"
     "            return 'UVT component'\n",
     "    ex_a = (not writing) and _uvt_source_exception(lit, real)        # v002 (a), read only\n"
     "    ex_b = (not writing) and _addendum_exception(lit, real)          # v002 (b), read only\n"
     "    for p in (lit, real):\n"
     "        low = p.casefold()\n"
     "        comps = low.split(os.sep)\n"
     "        if any(x.startswith('uvt_') for x in (comps[:-1] if ex_a else comps)):\n"
     "            return 'UVT component'\n"),
    ("        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):\n",
     "        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not ex_b:\n"),
    # 5. the open hook passes the write flag (reads only get the exceptions)
    ("        why = _forbidden_read(lit, real)\n",
     "        why = _forbidden_read(lit, real, _writing(args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None))\n"),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, ('anchor count %d' % n, old[:60])
    t = t.replace(old, new)

t += '''

def selftest_v002():
    """v002: the two read-only exceptions, as path predicates only (no protected file is opened). Returns [(name, ok)]."""
    C2 = CLAUDE2_CTRL
    A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_fence_probe_c4r5'
    ADD = C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
    cases = [
        ('a_uvt_source_read_allowed', A + '/uvt_probe_should_not_exist.py', False, None),
        ('a_uvt_source_write_refused', A + '/uvt_probe_should_not_exist.py', True, 'UVT component'),
        ('a_uvt_dir_component_refused', A + '/UVT_probe_dir/uvt_probe.py', False, 'UVT component'),
        ('a_uvt_non_py_refused', A + '/uvt_probe.json', False, 'UVT component'),
        ('a_uvt_under_a_runs_ext_component_refused', A + '/runs_ext/uvt_probe.py', False, 'UVT component'),
        ('a_uvt_c5h_name_still_refused', A + '/kmax_a2f10_c5h_run_v001/uvt_probe.py', False, 'C5H name'),
        ('b_addendum_read_allowed', ADD, False, None),
        ('b_frozen_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', False, None),
        ('b_v004_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md', False, None),
        ('b_addendum_write_refused', ADD, True, 'NGC3198 data'),
        ('b_v001_decisions_not_an_addendum_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md', False, 'NGC3198 data'),
        ('b_addendum_name_in_subfolder_refused', C2 + '/specs/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', False, 'NGC3198 data'),
        ('b_addendum_name_elsewhere_refused', A + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', False, 'NGC3198 data'),
        ('b_addendum_json_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.json', False, 'NGC3198 data'),
        ('b_target_word_still_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_rotmod.md', False, 'target word'),
        ('other_ngc3198_data_refused', A + '/NGC3198_probe_table.dat', False, 'NGC3198 data'),
        ('other_ngc3198_py_allowed_as_v001', A + '/ngc3198_probe_source.py', False, None),
    ]
    out = []
    for name, p, writing, want in cases:
        lit = os.path.abspath(p)
        real = os.path.realpath(lit)
        got = _forbidden_read(lit, real, writing)
        out.append((name, got == want))
    return out
'''
with open(V2, 'x') as f:
    f.write(t)
d = ''.join(difflib.unified_diff(src.decode().splitlines(True), t.splitlines(True), 'fence_c4v001.py', 'fence_c4v002.py'))
with open(DIFF, 'x') as f:
    f.write(d)
print('v2 sha256', hashlib.sha256(V2.read_bytes()).hexdigest())
print('diff sha256', hashlib.sha256(DIFF.read_bytes()).hexdigest(), 'lines', len(d.splitlines()))
