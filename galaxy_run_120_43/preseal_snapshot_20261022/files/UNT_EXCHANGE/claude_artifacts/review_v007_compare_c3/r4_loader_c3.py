"""Claude3 loader for compare r4 after the 0503 reissue (A53: r5 repoints PIN_REVIEW_V009 to the preserved original).
r4's pinned path now holds the reissued record (d3164b71), so r4 REFUSES at build_context. This loader verifies the r4 bytes
(fc2d6465), applies EXACTLY ONE substitution -- PIN_REVIEW_V009 path -> the byte-identical original copy
REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json (sha 3bce7c02, same pinned sha) -- and execs it. Decision logic is untouched.
load_compare() -> module; load_tests_lib() -> the author's test module (fixture library) bound to that compare;
write_patched_cli(dir) -> a patched copy for subprocess/CLI use (same single substitution)."""
import hashlib, importlib.util, sys, types
from pathlib import Path
R4 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r4')
CMP_SHA = 'fc2d646508cdae832503ac072aef0a421b2cd4b7c8b770c3645d4fe63dbbcfc0'; TST_SHA = 'de4c21e13fdc233b6d535af362eec3ede38b1ee71b3cad8dae763314af80a480'
OLD = "/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001.json'"
NEW = "/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json'"
ORIG = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json')
def _src():
    raw = (R4 / 'kmax_tail_compare_c2v007_r4.py').read_bytes(); assert hashlib.sha256(raw).hexdigest() == CMP_SHA, 'r4 compare bytes changed'
    assert hashlib.sha256(ORIG.read_bytes()).hexdigest() == '3bce7c02926526edf2a594418097ff379604ee1c9760dc1145bcd37ed2882d9f'
    s = raw.decode(); assert s.count(OLD) == 1; return s.replace(OLD, NEW)
def load_compare(name='cmp7r4_c3'):
    if name in sys.modules: return sys.modules[name]
    m = types.ModuleType(name); m.__file__ = str(R4 / 'kmax_tail_compare_c2v007_r4.py'); sys.modules[name] = m
    exec(compile(_src(), m.__file__, 'exec'), m.__dict__); return m
def load_tests_lib(name='t4lib_c3'):
    if name in sys.modules: return sys.modules[name]
    load_compare()
    raw = (R4 / 'tests_kmax_tail_compare_c2v007_r4.py').read_bytes(); assert hashlib.sha256(raw).hexdigest() == TST_SHA
    s = raw.decode(); a = "M = load(CMP, 'cmp7r4')"; assert s.count(a) == 1; s = s.replace(a, "M = __import__('sys').modules['cmp7r4_c3']")
    m = types.ModuleType(name); m.__file__ = str(R4 / 'tests_kmax_tail_compare_c2v007_r4.py'); sys.modules[name] = m
    exec(compile(s, m.__file__, 'exec'), m.__dict__); return m
def write_patched_cli(d):
    p = Path(d) / 'kmax_tail_compare_c2v007_r4_PINPATCHED_C3.py'
    if not p.exists(): p.write_text(_src())
    return p
